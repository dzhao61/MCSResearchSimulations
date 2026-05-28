"""
Stage 15: Fresh large-alphabet stress test for the Stage 12 moment model.

This stage does not reuse Stage 9 or Stage 13 validation rows.  It creates a
new out-of-training grid of larger alphabets and skew shapes, generates fresh
JIDT product-null samples, and compares:

    - standard chi-square
    - Stage 12 predicted moment model
    - true moment-matched chi-square from the fresh JIDT samples

The only thing reused is the selected Stage 12 coefficient file, because that
is the fitted method being tested.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from jpype import JArray, JInt, JPackage, getDefaultJVMPath, isJVMStarted, startJVM


ROOT = Path(__file__).resolve().parents[1]
STAGE9 = ROOT / "EffectiveDFCorrection_Stage9_RobustRegressions"
STAGE12 = ROOT / "EffectiveDFCorrection_Stage12_MomentModel"
OUT = Path(__file__).resolve().parent

sys.path.insert(0, str(STAGE9))
sys.path.insert(0, str(STAGE12))
import robust_regressions as rr  # noqa: E402
import moment_model as mm  # noqa: E402


os.environ["XDG_CACHE_HOME"] = str(OUT / ".cache")
os.environ.setdefault("MPLCONFIGDIR", str(OUT / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

JIDT_JAR = os.environ.get(
    "JIDT_JAR",
    "/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/jidt/infodynamics.jar",
)
if not os.path.exists(JIDT_JAR):
    raise FileNotFoundError(f"JIDT jar not found at {JIDT_JAR}.")
if not isJVMStarted():
    startJVM(getDefaultJVMPath(), "-ea", f"-Djava.class.path={JIDT_JAR}")

MICalcDiscrete = JPackage("infodynamics.measures.discrete").MutualInformationCalculatorDiscrete


@dataclass(frozen=True)
class ScratchConfig:
    label: str
    p_x: np.ndarray
    p_y: np.ndarray
    family_x: str
    family_y: str
    lam_target: float
    N: int


def normalize(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    return p / p.sum()


def one_rare(k: int, ratio: float) -> np.ndarray:
    p_rare = ratio / k
    return np.concatenate([[p_rare], np.full(k - 1, (1.0 - p_rare) / (k - 1))])


def two_rare(k: int, ratio: float) -> np.ndarray:
    p_rare = ratio / k
    return np.concatenate([[p_rare, p_rare], np.full(k - 2, (1.0 - 2.0 * p_rare) / (k - 2))])


def zipf(k: int, alpha: float) -> np.ndarray:
    ranks = np.arange(1, k + 1, dtype=float)
    return normalize(ranks ** (-alpha))


def geometric(k: int, q: float) -> np.ndarray:
    ranks = np.arange(k, dtype=float)
    return normalize(q**ranks)


def dirichlet_shape(k: int, alpha: float, rng: np.random.Generator) -> np.ndarray:
    # Reject extreme tiny-probability shapes so the test stresses sparse tables
    # without making N astronomically large.
    for _ in range(1_000):
        p = rng.dirichlet(np.full(k, alpha))
        if k * p.min() >= 0.04:
            return p
    return p


def shape_pairs(k: int, rng: np.random.Generator) -> list[tuple[str, np.ndarray, str, np.ndarray]]:
    return [
        ("uniform", np.full(k, 1.0 / k), "uniform", np.full(k, 1.0 / k)),
        (
            "uniform",
            np.full(k, 1.0 / k),
            "zipf_a1p45_rect",
            zipf(k + 3, 1.45),
        ),
        (
            "one_rare_0p25",
            one_rare(k, 0.25),
            "geom_q0p72",
            geometric(k, 0.72),
        ),
        (
            "zipf_a0p85",
            zipf(k, 0.85),
            "two_rare_0p35_rect",
            two_rare(k + 2, 0.35),
        ),
        (
            "dirichlet_a0p55",
            dirichlet_shape(k, 0.55, rng),
            "dirichlet_a1p60_rect",
            dirichlet_shape(k + 1, 1.60, rng),
        ),
    ]


def make_configs(args: argparse.Namespace) -> list[ScratchConfig]:
    rng = np.random.default_rng(args.seed + 91_000)
    k_values = [int(x.strip()) for x in args.k_values.split(",") if x.strip()]
    lam_targets = [float(x.strip()) for x in args.lambda_targets.split(",") if x.strip()]
    configs = []
    for k in k_values:
        for fx, px, fy, py in shape_pairs(k, rng):
            pi_min = float(px.min() * py.min())
            for lam in lam_targets:
                N = int(round(lam / pi_min))
                if N < args.min_N or N > args.max_N:
                    continue
                label = f"kx={len(px)}|ky={len(py)}|x={fx}|y={fy}|N={N}|lam={lam:g}"
                configs.append(ScratchConfig(label, px, py, fx, fy, lam, N))

    if args.max_configs and len(configs) > args.max_configs:
        chooser = np.random.default_rng(args.seed + 92_000)
        idx = np.sort(chooser.choice(len(configs), args.max_configs, replace=False))
        configs = [configs[i] for i in idx]
    return configs


def sample_categorical(p: np.ndarray, N: int, rng: np.random.Generator) -> np.ndarray:
    return np.searchsorted(np.cumsum(p), rng.random(N)).astype(int)


def jidt_T(calc, x: np.ndarray, y: np.ndarray) -> float:
    calc.initialise()
    calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
    mi_bits = float(calc.computeAverageLocalOfObservations())
    return float(2.0 * len(x) * mi_bits * np.log(2.0))


def jidt_product_null_T(
    p_x: np.ndarray,
    p_y: np.ndarray,
    N: int,
    repeats: int,
    rng: np.random.Generator,
) -> np.ndarray:
    calc = MICalcDiscrete(int(max(len(p_x), len(p_y))))
    T = np.empty(repeats, dtype=float)
    for i in range(repeats):
        x = sample_categorical(p_x, N, rng)
        y = sample_categorical(p_y, N, rng)
        T[i] = jidt_T(calc, x, y)
    return T


def selected_coefficients(path: Path) -> dict[str, dict[str, float]]:
    selected = pd.read_csv(path)
    return {
        str(row["target"]): json.loads(row["coefficients"])
        for _, row in selected.iterrows()
    }


def stage12_predict(cfg: ScratchConfig, coefs: dict[str, dict[str, float]], log_clip: float) -> tuple[dict, pd.Series]:
    desc = rr.pair_descriptors(cfg.p_x, cfg.p_y, cfg.N)
    row = {
        "config_id": cfg.label,
        "shape_x": cfg.family_x,
        "shape_y": cfg.family_y,
        "family_x": cfg.family_x,
        "family_y": cfg.family_y,
        "pair_family": f"{cfg.family_x}|{cfg.family_y}",
        "symmetric_shape": cfg.family_x == cfg.family_y and len(cfg.p_x) == len(cfg.p_y),
        "lam_target": cfg.lam_target,
        **desc,
    }
    features = mm.add_moment_features(pd.DataFrame([row])).iloc[0]
    log_mu = sum(value * float(features[name]) for name, value in coefs["log_mu_ratio"].items())
    log_var = sum(value * float(features[name]) for name, value in coefs["log_sigma2_ratio"].items())
    log_mu = float(np.clip(log_mu, -log_clip, log_clip))
    log_var = float(np.clip(log_var, -log_clip, log_clip))
    mu = float(features["mu_bartlett"] * np.exp(log_mu))
    sigma2 = float(features["sigma2_bartlett"] * np.exp(log_var))
    a = float(sigma2 / max(2.0 * mu, 1e-12))
    nu = float(2.0 * mu**2 / max(sigma2, 1e-12))
    return (
        {
            "pred_mu": mu,
            "pred_sigma2": sigma2,
            "pred_a": a,
            "pred_nu": nu,
            "pred_nu_norm": nu / max(float(features["nu0"]), 1e-12),
        },
        features,
    )


def summarize(cfg: ScratchConfig, T: np.ndarray, pred: dict, features: pd.Series) -> dict:
    mu = float(T.mean())
    sigma2 = float(T.var(ddof=1))
    nu = float(2.0 * mu**2 / sigma2)
    a = float(sigma2 / (2.0 * mu))
    row = {
        "config_id": cfg.label,
        "family_x": cfg.family_x,
        "family_y": cfg.family_y,
        "pair_family": f"{cfg.family_x}|{cfg.family_y}",
        "kx": int(features["kx"]),
        "ky": int(features["ky"]),
        "kmax": int(max(features["kx"], features["ky"])),
        "N": cfg.N,
        "bootstrap": len(T),
        "lam_target": cfg.lam_target,
        "lam_min": float(features["lam_min"]),
        "lam_tp": float(features["lam_tp"]),
        "frac_cells_lt_1": float(features["frac_cells_lt_1"]),
        "expected_zero_frac": float(features["expected_zero_frac"]),
        "expected_singleton_frac": float(features["expected_singleton_frac"]),
        "nu0": float(features["nu0"]),
        "mu": mu,
        "sigma2": sigma2,
        "nu": nu,
        "a": a,
        "nu_norm": nu / max(float(features["nu0"]), 1e-12),
        "T_q95": float(np.quantile(T, 0.95)),
        "T_q99": float(np.quantile(T, 0.99)),
        "standard_q95": float(stats.chi2.ppf(0.95, df=float(features["nu0"]))),
        "standard_q99": float(stats.chi2.ppf(0.99, df=float(features["nu0"]))),
        "true_mm_q95": float(a * stats.chi2.ppf(0.95, df=max(nu, 1e-8))),
        "true_mm_q99": float(a * stats.chi2.ppf(0.99, df=max(nu, 1e-8))),
    }
    row.update(pred)
    row["stage12_q95"] = float(pred["pred_a"] * stats.chi2.ppf(0.95, df=max(pred["pred_nu"], 1e-8)))
    row["stage12_q99"] = float(pred["pred_a"] * stats.chi2.ppf(0.99, df=max(pred["pred_nu"], 1e-8)))
    for model in ["standard", "true_mm", "stage12"]:
        for q in [95, 99]:
            row[f"{model}_q{q}_ratio_emp"] = row[f"{model}_q{q}"] / row[f"T_q{q}"]
    for target, pred_col in [
        ("mu", "pred_mu"),
        ("sigma2", "pred_sigma2"),
        ("a", "pred_a"),
        ("nu", "pred_nu"),
    ]:
        row[f"{target}_ratio_pred"] = row[pred_col] / max(row[target], 1e-12)
    return row


def run_test(args: argparse.Namespace) -> pd.DataFrame:
    configs = make_configs(args)
    coefs = selected_coefficients(Path(args.selected_model))
    rng = np.random.default_rng(args.seed)
    rows = []
    print(
        f"Running Stage 15 fresh stress test: configs={len(configs)}, "
        f"JIDT repeats={args.bootstrap}"
    )
    for i, cfg in enumerate(configs, start=1):
        pred, features = stage12_predict(cfg, coefs, args.log_clip)
        start = time.time()
        T = jidt_product_null_T(cfg.p_x, cfg.p_y, cfg.N, args.bootstrap, rng)
        row = summarize(cfg, T, pred, features)
        rows.append(row)
        print(
            f"[{i:3d}/{len(configs)}] k={row['kx']}x{row['ky']} "
            f"{cfg.family_x} vs {cfg.family_y} N={cfg.N:6d} "
            f"lam_min={row['lam_min']:.3g} "
            f"mu={row['mu_ratio_pred']:.3f} var={row['sigma2_ratio_pred']:.3f} "
            f"q95={row['stage12_q95_ratio_emp']:.3f} q99={row['stage12_q99_ratio_emp']:.3f} "
            f"({time.time() - start:.2f}s)",
            flush=True,
        )
    return pd.DataFrame(rows)


def ratio_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in [95, 99]:
        for model in ["standard", "true_mm", "stage12"]:
            ratio = df[f"{model}_q{q}_ratio_emp"].to_numpy(dtype=float)
            abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
            rows.append(
                dict(
                    q=q / 100.0,
                    group="all",
                    model=model,
                    n=len(df),
                    median_ratio=float(np.median(ratio)),
                    mean_abs_log_error=float(abs_log.mean()),
                    within_05pct=float((abs_log < np.log(1.05)).mean()),
                    within_10pct=float((abs_log < np.log(1.10)).mean()),
                    p05=float(np.quantile(ratio, 0.05)),
                    p95=float(np.quantile(ratio, 0.95)),
                )
            )
    return pd.DataFrame(rows)


def grouped_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (kmax, family), grp in df.groupby(["kmax", "pair_family"], observed=True):
        for q in [95, 99]:
            ratio = grp[f"stage12_q{q}_ratio_emp"].to_numpy(dtype=float)
            abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
            rows.append(
                dict(
                    kmax=kmax,
                    pair_family=family,
                    q=q / 100.0,
                    n=len(grp),
                    median_ratio=float(np.median(ratio)),
                    within_10pct=float((abs_log < np.log(1.10)).mean()),
                    max_abs_log_error=float(abs_log.max()),
                )
            )
    return pd.DataFrame(rows)


def plot_summary(df: pd.DataFrame, out_path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        print(f"Skipping plot; matplotlib import failed: {exc}")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes[0][0].scatter(df["mu"], df["pred_mu"], s=26, alpha=0.75)
    axes[0][0].set_xlabel("JIDT product-null mean")
    axes[0][0].set_ylabel("Stage12 predicted mean")
    axes[0][1].scatter(df["sigma2"], df["pred_sigma2"], s=26, alpha=0.75)
    axes[0][1].set_xlabel("JIDT product-null variance")
    axes[0][1].set_ylabel("Stage12 predicted variance")
    for ax in axes[0]:
        lo, hi = ax.get_xlim()
        lo2, hi2 = ax.get_ylim()
        lo, hi = min(lo, lo2), max(hi, hi2)
        ax.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.grid(True, alpha=0.25, linestyle="--")

    for q, ax in [(95, axes[1][0]), (99, axes[1][1])]:
        ax.scatter(df["kmax"], df[f"stage12_q{q}_ratio_emp"], s=28, alpha=0.75)
        ax.axhline(1, color="black", linestyle="--", linewidth=1)
        ax.axhspan(0.9, 1.1, color="green", alpha=0.08)
        ax.set_xlabel("max(kx, ky)")
        ax.set_ylabel(f"Stage12 q{q} / JIDT empirical q{q}")
        ax.grid(True, alpha=0.25, linestyle="--")

    fig.suptitle("Stage 15: fresh large-alphabet JIDT product-null stress test")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k-values", default="10,15,20,30")
    parser.add_argument("--lambda-targets", default="0.5,1,2,5")
    parser.add_argument("--bootstrap", type=int, default=800)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--min-N", type=int, default=20)
    parser.add_argument("--max-N", type=int, default=25_000)
    parser.add_argument("--max-configs", type=int, default=0)
    parser.add_argument("--log-clip", type=float, default=4.0)
    parser.add_argument(
        "--selected-model",
        default=str(STAGE12 / "selected_moment_models.csv"),
        help="Selected Stage 12 coefficient CSV.",
    )
    parser.add_argument("--out-dir", default=str(OUT))
    parser.add_argument("--no-plot", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = run_test(args)
    summary = ratio_summary(df)
    groups = grouped_summary(df)

    data_path = out_dir / "scratch_large_alphabet_data.csv"
    summary_path = out_dir / "scratch_large_alphabet_summary.csv"
    group_path = out_dir / "scratch_large_alphabet_groups.csv"
    plot_path = out_dir / "scratch_large_alphabet_summary.png"
    df.to_csv(data_path, index=False)
    summary.to_csv(summary_path, index=False)
    groups.to_csv(group_path, index=False)
    print(f"Saved data: {data_path}")
    print(f"Saved summary: {summary_path}")
    print(f"Saved grouped summary: {group_path}")
    if not args.no_plot:
        plot_summary(df, plot_path)
        print(f"Saved plot: {plot_path}")

    print("\n=== Overall quantile calibration ===")
    print(summary.to_string(index=False))
    print("\n=== Worst Stage12 groups ===")
    print(
        groups.sort_values("max_abs_log_error", ascending=False)
        .head(12)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
