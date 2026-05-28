"""
Stage 13: JIDT validation of the Stage 12 moment model.

Stage 12 learned a cheap approximation to the null moments of

    T = 2 N I_hat(X;Y)

using an analytic Bartlett core plus sparse occupancy corrections.  Stage 13
checks that model against fresh JIDT null samples on a modest, deliberately
out-of-training validation grid:

    - shape parameters not used in Stage 9 training
    - rectangular alphabets
    - sparse and dense expected-count regimes

This is not a new training stage.  It loads the selected Stage 12 coefficients,
predicts mu and sigma2 from table descriptors only, and compares those
predictions with JIDT-estimated null moments and tails.
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
    raise FileNotFoundError(
        f"JIDT jar not found at {JIDT_JAR}. Set JIDT_JAR or edit the default path."
    )
if not isJVMStarted():
    startJVM(getDefaultJVMPath(), "-ea", f"-Djava.class.path={JIDT_JAR}")

MICalcDiscrete = JPackage("infodynamics.measures.discrete").MutualInformationCalculatorDiscrete


@dataclass(frozen=True)
class ValidationConfig:
    label: str
    p_x: np.ndarray
    p_y: np.ndarray
    shape_x: str
    shape_y: str
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


def dirichlet_shape(k: int, alpha: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    for _ in range(500):
        p = rng.dirichlet(np.full(k, alpha))
        if k * p.min() >= 0.02:
            return p
    return p


def shape_library() -> dict[str, tuple[np.ndarray, str]]:
    return {
        "uniform_3": (np.full(3, 1.0 / 3), "uniform"),
        "uniform_4": (np.full(4, 1.0 / 4), "uniform"),
        "uniform_6": (np.full(6, 1.0 / 6), "uniform"),
        "uniform_8": (np.full(8, 1.0 / 8), "uniform"),
        "one_rare_0p1_5": (one_rare(5, 0.1), "one_rare_oos"),
        "one_rare_0p3_7": (one_rare(7, 0.3), "one_rare_oos"),
        "two_rare_0p2_6": (two_rare(6, 0.2), "two_rare_oos"),
        "zipf_a0p9_6": (zipf(6, 0.9), "zipf_oos"),
        "zipf_a1p5_8": (zipf(8, 1.5), "zipf_oos"),
        "geom_q0p7_7": (geometric(7, 0.7), "geometric_oos"),
        "geom_q0p9_5": (geometric(5, 0.9), "geometric_oos"),
        "dirichlet_a0p6_6": (dirichlet_shape(6, 0.6, 91), "dirichlet_oos"),
        "dirichlet_a1p4_8": (dirichlet_shape(8, 1.4, 137), "dirichlet_oos"),
    }


def validation_pairs(profile: str) -> list[tuple[str, str]]:
    smoke = [
        ("uniform_4", "uniform_4"),
        ("one_rare_0p1_5", "uniform_6"),
        ("zipf_a0p9_6", "geom_q0p7_7"),
        ("uniform_3", "zipf_a1p5_8"),
    ]
    moderate_extra = [
        ("uniform_8", "uniform_8"),
        ("two_rare_0p2_6", "geom_q0p9_5"),
        ("dirichlet_a0p6_6", "uniform_4"),
        ("dirichlet_a1p4_8", "one_rare_0p3_7"),
    ]
    return smoke if profile == "smoke" else smoke + moderate_extra


def make_validation_configs(args: argparse.Namespace) -> list[ValidationConfig]:
    lib = shape_library()
    lam_targets = [float(x.strip()) for x in args.lambda_targets.split(",") if x.strip()]
    configs: list[ValidationConfig] = []
    seen: set[tuple[str, str, int]] = set()
    for shape_x, shape_y in validation_pairs(args.profile):
        p_x, family_x = lib[shape_x]
        p_y, family_y = lib[shape_y]
        pi_min = float(p_x.min() * p_y.min())
        for lam_target in lam_targets:
            N = int(round(lam_target / pi_min))
            if N < args.min_N:
                N = args.min_N
            if N > args.max_N:
                continue
            key = (shape_x, shape_y, N)
            if key in seen:
                continue
            seen.add(key)
            label = f"{shape_x}__{shape_y}__N{N}__lam{lam_target:g}"
            configs.append(
                ValidationConfig(
                    label=label,
                    p_x=p_x,
                    p_y=p_y,
                    shape_x=shape_x,
                    shape_y=shape_y,
                    family_x=family_x,
                    family_y=family_y,
                    lam_target=lam_target,
                    N=N,
                )
            )
    if args.max_configs and len(configs) > args.max_configs:
        rng = np.random.default_rng(args.seed)
        idx = np.sort(rng.choice(len(configs), size=args.max_configs, replace=False))
        configs = [configs[i] for i in idx]
    return configs


def sample_categorical(p: np.ndarray, N: int, rng: np.random.Generator) -> np.ndarray:
    return np.searchsorted(np.cumsum(p), rng.random(N)).astype(int)


def jidt_null_T(
    p_x: np.ndarray,
    p_y: np.ndarray,
    N: int,
    repeats: int,
    rng: np.random.Generator,
) -> np.ndarray:
    base = int(max(len(p_x), len(p_y)))
    calc = MICalcDiscrete(base)
    T = np.empty(repeats, dtype=float)
    for s in range(repeats):
        x = sample_categorical(p_x, N, rng)
        y = sample_categorical(p_y, N, rng)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mi_bits = float(calc.computeAverageLocalOfObservations())
        T[s] = 2.0 * N * mi_bits * np.log(2.0)
    return T


def selected_coefficients(path: Path) -> dict[str, dict[str, float]]:
    selected = pd.read_csv(path)
    out: dict[str, dict[str, float]] = {}
    for _, row in selected.iterrows():
        out[str(row["target"])] = json.loads(row["coefficients"])
    missing = {"log_mu_ratio", "log_sigma2_ratio"} - set(out)
    if missing:
        raise ValueError(f"Missing selected Stage 12 targets: {sorted(missing)}")
    return out


def descriptors_for_config(cfg: ValidationConfig) -> pd.DataFrame:
    desc = rr.pair_descriptors(cfg.p_x, cfg.p_y, cfg.N)
    row = {
        "config_id": cfg.label,
        "shape_x": cfg.shape_x,
        "shape_y": cfg.shape_y,
        "family_x": cfg.family_x,
        "family_y": cfg.family_y,
        "pair_family": f"{cfg.family_x}|{cfg.family_y}",
        "symmetric_shape": cfg.shape_x == cfg.shape_y and len(cfg.p_x) == len(cfg.p_y),
        "lam_target": cfg.lam_target,
        **desc,
    }
    return mm.add_moment_features(pd.DataFrame([row]))


def predict_stage12_moments(
    features: pd.DataFrame,
    coefs: dict[str, dict[str, float]],
    log_clip: float,
    nu_norm_floor: float,
    a_floor: float,
) -> dict[str, float]:
    row = features.iloc[0]
    pred_log_mu = sum(value * float(row[name]) for name, value in coefs["log_mu_ratio"].items())
    pred_log_sigma2 = sum(
        value * float(row[name]) for name, value in coefs["log_sigma2_ratio"].items()
    )
    pred_log_mu = float(np.clip(pred_log_mu, -log_clip, log_clip))
    pred_log_sigma2 = float(np.clip(pred_log_sigma2, -log_clip, log_clip))
    pred_mu = float(row["mu_bartlett"] * np.exp(pred_log_mu))
    pred_sigma2 = float(row["sigma2_bartlett"] * np.exp(pred_log_sigma2))
    pred_a = max(pred_sigma2 / max(2.0 * pred_mu, 1e-12), a_floor)
    pred_nu = 2.0 * pred_mu**2 / max(pred_sigma2, 1e-12)
    pred_nu = max(pred_nu, nu_norm_floor * float(row["nu0"]))
    return {
        "pred_log_mu_ratio": pred_log_mu,
        "pred_log_sigma2_ratio": pred_log_sigma2,
        "pred_mu": pred_mu,
        "pred_sigma2": pred_sigma2,
        "pred_a": float(pred_a),
        "pred_nu": float(pred_nu),
        "pred_nu_norm": float(pred_nu / max(float(row["nu0"]), 1e-12)),
    }


def summarize_config(
    cfg: ValidationConfig,
    T: np.ndarray,
    features: pd.DataFrame,
    pred: dict[str, float],
) -> dict[str, float | str | int]:
    row = features.iloc[0].to_dict()
    mu = float(T.mean())
    sigma2 = float(T.var(ddof=1))
    nu = float(2.0 * mu**2 / sigma2)
    a = float(sigma2 / (2.0 * mu))
    q95 = float(np.quantile(T, 0.95))
    q99 = float(np.quantile(T, 0.99))
    nu0 = float(row["nu0"])
    out = {
        "config_id": cfg.label,
        "shape_x": cfg.shape_x,
        "shape_y": cfg.shape_y,
        "family_x": cfg.family_x,
        "family_y": cfg.family_y,
        "pair_family": f"{cfg.family_x}|{cfg.family_y}",
        "kx": len(cfg.p_x),
        "ky": len(cfg.p_y),
        "N": cfg.N,
        "bootstrap": len(T),
        "lam_target": cfg.lam_target,
        "lam_min": float(row["lam_min"]),
        "lam_tp": float(row["lam_tp"]),
        "frac_cells_lt_1": float(row["frac_cells_lt_1"]),
        "expected_zero_frac": float(row["expected_zero_frac"]),
        "expected_singleton_frac": float(row["expected_singleton_frac"]),
        "nu0": nu0,
        "mu": mu,
        "sigma2": sigma2,
        "nu": nu,
        "nu_norm": nu / max(nu0, 1e-12),
        "a": a,
        "T_q95": q95,
        "T_q99": q99,
        "q95_chi2": float(row["q95_chi2"]),
        "q99_chi2": float(row["q99_chi2"]),
        "mu_bartlett": float(row["mu_bartlett"]),
        "sigma2_bartlett": float(row["sigma2_bartlett"]),
        "a_bartlett": float(row["a_bartlett"]),
        "nu_bartlett": float(row["nu_bartlett"]),
    }
    out.update(pred)
    for q, emp in [(0.95, q95), (0.99, q99)]:
        suffix = int(q * 100)
        out[f"standard_q{suffix}"] = float(stats.chi2.ppf(q, df=nu0))
        out[f"bartlett_q{suffix}"] = float(out["a_bartlett"] * stats.chi2.ppf(q, df=out["nu_bartlett"]))
        out[f"true_mm_q{suffix}"] = float(a * stats.chi2.ppf(q, df=max(nu, 1e-8)))
        out[f"stage12_q{suffix}"] = float(pred["pred_a"] * stats.chi2.ppf(q, df=max(pred["pred_nu"], 1e-8)))
        for model in ["standard", "bartlett", "true_mm", "stage12"]:
            out[f"{model}_q{suffix}_ratio_emp"] = out[f"{model}_q{suffix}"] / emp
    return out


def run_validation(args: argparse.Namespace) -> pd.DataFrame:
    configs = make_validation_configs(args)
    coefs = selected_coefficients(Path(args.selected_model))
    rng = np.random.default_rng(args.seed)
    rows = []
    print(
        f"Running Stage 13 profile={args.profile}, configs={len(configs)}, "
        f"JIDT repeats={args.bootstrap}"
    )
    for i, cfg in enumerate(configs, start=1):
        features = descriptors_for_config(cfg)
        pred = predict_stage12_moments(
            features,
            coefs,
            args.log_clip,
            args.nu_norm_floor,
            args.a_floor,
        )
        start = time.time()
        T = jidt_null_T(cfg.p_x, cfg.p_y, cfg.N, args.bootstrap, rng)
        row = summarize_config(cfg, T, features, pred)
        rows.append(row)
        print(
            f"[{i:3d}/{len(configs)}] {cfg.shape_x} vs {cfg.shape_y} "
            f"N={cfg.N:5d} lam_min={row['lam_min']:.3g} "
            f"mu ratio={row['pred_mu']/row['mu']:.3f} "
            f"var ratio={row['pred_sigma2']/row['sigma2']:.3f} "
            f"q95 ratio={row['stage12_q95_ratio_emp']:.3f} "
            f"({time.time() - start:.2f}s)",
            flush=True,
        )
    return pd.DataFrame(rows)


def tail_calibration(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in [0.95, 0.99]:
        suffix = int(q * 100)
        for model in ["standard", "bartlett", "true_mm", "stage12"]:
            ratio = df[f"{model}_q{suffix}_ratio_emp"].to_numpy(dtype=float)
            abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
            rows.append(
                dict(
                    q=q,
                    model=model,
                    n=len(df),
                    median_ratio=float(np.median(ratio)),
                    mean_abs_log_error=float(abs_log.mean()),
                    median_abs_log_error=float(np.median(abs_log)),
                    within_05pct=float((abs_log < np.log(1.05)).mean()),
                    within_10pct=float((abs_log < np.log(1.10)).mean()),
                    within_20pct=float((abs_log < np.log(1.20)).mean()),
                    p05=float(np.quantile(ratio, 0.05)),
                    p95=float(np.quantile(ratio, 0.95)),
                )
            )
    return pd.DataFrame(rows)


def moment_errors(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for target, pred in [
        ("mu", "pred_mu"),
        ("sigma2", "pred_sigma2"),
        ("a", "pred_a"),
        ("nu", "pred_nu"),
    ]:
        ratio = df[pred].to_numpy(dtype=float) / np.maximum(df[target].to_numpy(dtype=float), 1e-12)
        abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
        rows.append(
            dict(
                target=target,
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


def plot_summary(df: pd.DataFrame, out_path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        print(f"Skipping plot; matplotlib import failed: {exc}")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    panels = [
        ("mu", "pred_mu", "mean"),
        ("sigma2", "pred_sigma2", "variance"),
    ]
    for ax, (obs, pred, label) in zip(axes[0], panels):
        ax.scatter(df[obs], df[pred], s=28, alpha=0.75)
        lo = float(min(df[obs].min(), df[pred].min()))
        hi = float(max(df[obs].max(), df[pred].max()))
        ax.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1)
        ax.set_xlabel(f"JIDT {label}")
        ax.set_ylabel(f"Stage12 predicted {label}")
        ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1][0]
    ax.scatter(df["lam_min"], df["stage12_q95_ratio_emp"], s=28, alpha=0.75, label="q95")
    ax.scatter(df["lam_min"], df["stage12_q99_ratio_emp"], s=28, alpha=0.55, label="q99")
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.axhspan(0.9, 1.1, color="green", alpha=0.08)
    ax.set_xscale("log")
    ax.set_xlabel("lambda_min")
    ax.set_ylabel("Stage12 quantile / JIDT empirical quantile")
    ax.legend()
    ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1][1]
    ax.scatter(df["frac_cells_lt_1"], df["pred_sigma2"] / df["sigma2"], s=28, alpha=0.75)
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.axhspan(0.9, 1.1, color="green", alpha=0.08)
    ax.set_xlabel("fraction cells with expected count < 1")
    ax.set_ylabel("predicted variance / JIDT variance")
    ax.grid(True, alpha=0.25, linestyle="--")

    fig.suptitle("Stage 13: JIDT validation of Stage 12 moment model")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def print_summary(tail: pd.DataFrame, moments: pd.DataFrame) -> None:
    print("\n=== Moment prediction errors ===")
    print(moments.to_string(index=False))
    print("\n=== Tail calibration vs JIDT empirical quantiles ===")
    print(tail.to_string(index=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["smoke", "moderate"], default="moderate")
    parser.add_argument("--bootstrap", type=int, default=400)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--lambda-targets", default="0.5,1,2,5")
    parser.add_argument("--min-N", type=int, default=20)
    parser.add_argument("--max-N", type=int, default=5000)
    parser.add_argument("--max-configs", type=int, default=0)
    parser.add_argument("--log-clip", type=float, default=4.0)
    parser.add_argument("--nu-norm-floor", type=float, default=0.05)
    parser.add_argument("--a-floor", type=float, default=0.05)
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

    df = run_validation(args)
    tail = tail_calibration(df)
    moments = moment_errors(df)

    data_path = out_dir / "jidt_validation_data.csv"
    tail_path = out_dir / "jidt_validation_tail_calibration.csv"
    moments_path = out_dir / "jidt_validation_moment_errors.csv"
    plot_path = out_dir / "jidt_validation_summary.png"

    df.to_csv(data_path, index=False)
    tail.to_csv(tail_path, index=False)
    moments.to_csv(moments_path, index=False)
    print(f"Saved validation data: {data_path}")
    print(f"Saved tail calibration: {tail_path}")
    print(f"Saved moment errors: {moments_path}")

    if not args.no_plot:
        plot_summary(df, plot_path)
        print(f"Saved plot: {plot_path}")

    print_summary(tail, moments)


if __name__ == "__main__":
    main()
