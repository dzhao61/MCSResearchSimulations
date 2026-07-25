"""
Stage 14: Stage-2-style null comparison.

Compare four null approximations for discrete mutual information:

    1. JIDT analytic chi-square significance
    2. Stage 12 moment model
    3. empirical product null, using the JIDT example's fresh independent
       bootstrap loop with JIDT computing every MI
    4. JIDT empirical permutation significance, via computeSignificance(repeats)

The default configuration is binary and Stage-2-like: several sparse and dense
Bernoulli settings.  For each setting we create one observed independent
dataset with deterministic margins, then compare:

    - observed p-values
    - q95/q99 thresholds
    - CDF overlays in T = 2 N I_hat units
"""

from __future__ import annotations

import argparse
import json
import os
import sys
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
class Config:
    label: str
    p_x: np.ndarray
    p_y: np.ndarray
    N: int


def normalize(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    return p / p.sum()


def binary(p_rare: float) -> np.ndarray:
    return np.asarray([1.0 - p_rare, p_rare], dtype=float)


def stage2_configs(profile: str) -> list[Config]:
    base = [
        Config("p=0.50, N=20", binary(0.50), binary(0.50), 20),
        Config("p=0.50, N=50", binary(0.50), binary(0.50), 50),
        Config("p=0.50, N=200", binary(0.50), binary(0.50), 200),
        Config("p=0.10, N=50", binary(0.10), binary(0.10), 50),
        Config("p=0.10, N=100", binary(0.10), binary(0.10), 100),
        Config("p=0.10, N=500", binary(0.10), binary(0.10), 500),
        Config("p=0.05, N=100", binary(0.05), binary(0.05), 100),
        Config("p=0.05, N=500", binary(0.05), binary(0.05), 500),
        Config("pX=0.20, pY=0.05, N=500", binary(0.20), binary(0.05), 500),
    ]
    smoke = [
        Config("p=0.50, N=20", binary(0.50), binary(0.50), 20),
        Config("p=0.10, N=100", binary(0.10), binary(0.10), 100),
        Config("p=0.05, N=500", binary(0.05), binary(0.05), 500),
    ]
    return smoke if profile == "smoke" else base


def rounded_counts(p: np.ndarray, N: int) -> np.ndarray:
    raw = normalize(p) * N
    counts = np.floor(raw).astype(int)
    remaining = int(N - counts.sum())
    if remaining > 0:
        order = np.argsort(raw - counts)[::-1]
        for idx in order[:remaining]:
            counts[idx] += 1
    return counts


def sample_from_counts(counts: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    values = np.concatenate([np.full(int(c), i, dtype=int) for i, c in enumerate(counts)])
    rng.shuffle(values)
    return values


def empirical_probs(values: np.ndarray, k: int) -> np.ndarray:
    counts = np.bincount(values, minlength=k).astype(float)
    support = counts > 0
    return counts[support] / counts[support].sum()


def relabel_observed_support(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    labels, inverse = np.unique(values, return_inverse=True)
    return inverse.astype(int), labels


def make_observed(cfg: Config, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x_counts = rounded_counts(cfg.p_x, cfg.N)
    y_counts = rounded_counts(cfg.p_y, cfg.N)
    x = sample_from_counts(x_counts, rng)
    y = sample_from_counts(y_counts, rng)
    x, x_labels = relabel_observed_support(x)
    y, y_labels = relabel_observed_support(y)
    p_x_emp = empirical_probs(x, len(x_labels))
    p_y_emp = empirical_probs(y, len(y_labels))
    return x, y, p_x_emp, p_y_emp


def jidt_T(calc, x: np.ndarray, y: np.ndarray) -> float:
    calc.initialise()
    calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
    mi_bits = float(calc.computeAverageLocalOfObservations())
    return float(2.0 * len(x) * mi_bits * np.log(2.0))


def jidt_analytic_standard(x_obs: np.ndarray, y_obs: np.ndarray):
    """
    JIDT's built-in analytic chi-square significance object.

    JIDT's distribution methods use MI in bits internally.  The rest of this
    stage reports T = 2 N I_nats, so estimates from this object are converted
    by multiplying MI_bits by 2 N log(2).
    """
    calc = MICalcDiscrete(int(max(x_obs.max(), y_obs.max()) + 1))
    calc.initialise()
    calc.addObservations(JArray(JInt)(x_obs.tolist()), JArray(JInt)(y_obs.tolist()))
    calc.computeAverageLocalOfObservations()
    return calc.computeSignificance()


def jidt_estimate_to_T(mi_bits: float, N: int) -> float:
    return float(2.0 * N * mi_bits * np.log(2.0))


def jidt_T_to_estimate(T: float, N: int) -> float:
    return float(T / (2.0 * N * np.log(2.0)))


def jidt_analytic_quantile(standard_dist, q: float, N: int) -> float:
    # computeEstimateForGivenPValue takes a right-tail p-value.
    mi_bits = float(standard_dist.computeEstimateForGivenPValue(1.0 - q))
    return jidt_estimate_to_T(mi_bits, N)


def jidt_analytic_cdf(standard_dist, T_grid: np.ndarray, N: int) -> np.ndarray:
    cdf = []
    for T in T_grid:
        mi_bits = jidt_T_to_estimate(float(T), N)
        p_tail = float(standard_dist.computePValueForGivenEstimate(mi_bits))
        cdf.append(1.0 - p_tail)
    return np.asarray(cdf, dtype=float)


def jidt_analytic_p_value(standard_dist) -> float:
    p_value = float(standard_dist.pValue)
    if np.isfinite(p_value):
        return p_value
    actual = max(float(standard_dist.actualValue), 0.0)
    return float(standard_dist.computePValueForGivenEstimate(actual))


def sample_categorical(p: np.ndarray, N: int, rng: np.random.Generator) -> np.ndarray:
    return np.searchsorted(np.cumsum(p), rng.random(N)).astype(int)


def product_null_T(
    p_x: np.ndarray,
    p_y: np.ndarray,
    N: int,
    repeats: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Product-null bootstrap used in the JIDT null-distribution example:
    draw fresh independent x and y samples, then use JIDT to compute MI.

    JIDT does not expose this as a separate computeSignificance API; the toolkit
    API is fixed-marginal permutation significance.  This loop mirrors the
    JIDT example's non-toolkit branch, generalized to arbitrary categorical
    marginals.
    """
    calc = MICalcDiscrete(int(max(len(p_x), len(p_y))))
    T = np.empty(repeats)
    for i in range(repeats):
        x = sample_categorical(p_x, N, rng)
        y = sample_categorical(p_y, N, rng)
        T[i] = jidt_T(calc, x, y)
    return T


def permutation_null_T(
    x_obs: np.ndarray,
    y_obs: np.ndarray,
    repeats: int,
    rng: np.random.Generator,
) -> np.ndarray:
    calc = MICalcDiscrete(int(max(x_obs.max(), y_obs.max()) + 1))
    T = np.empty(repeats)
    for i in range(repeats):
        T[i] = jidt_T(calc, x_obs, rng.permutation(y_obs))
    return T


def jidt_permutation_null_T(
    x_obs: np.ndarray,
    y_obs: np.ndarray,
    repeats: int,
) -> tuple[np.ndarray, float]:
    """
    JIDT's built-in significance routine permutes observations internally.

    This is the fixed-marginal null: the supplied observed x and y arrays are
    kept as the marginal samples, and JIDT builds a null distribution by
    randomising their pairing.
    """
    calc = MICalcDiscrete(int(max(x_obs.max(), y_obs.max()) + 1))
    calc.initialise()
    calc.addObservations(JArray(JInt)(x_obs.tolist()), JArray(JInt)(y_obs.tolist()))
    null_dist = calc.computeSignificance(repeats)
    mi_bits = np.asarray([float(v) for v in null_dist.distribution], dtype=float)
    return 2.0 * len(x_obs) * mi_bits * np.log(2.0), float(null_dist.pValue)


def selected_coefficients(path: Path) -> dict[str, dict[str, float]]:
    selected = pd.read_csv(path)
    return {
        str(row["target"]): json.loads(row["coefficients"])
        for _, row in selected.iterrows()
    }


def stage12_prediction(
    p_x: np.ndarray,
    p_y: np.ndarray,
    N: int,
    coefs: dict[str, dict[str, float]],
    log_clip: float,
) -> tuple[dict[str, float], pd.Series]:
    desc = rr.pair_descriptors(p_x, p_y, N)
    row = {
        "config_id": "observed",
        "shape_x": "observed",
        "shape_y": "observed",
        "family_x": "observed",
        "family_y": "observed",
        "pair_family": "observed|observed",
        "symmetric_shape": len(p_x) == len(p_y) and np.allclose(p_x, p_y),
        "lam_target": float(desc["lam_min"]),
        **desc,
    }
    features = mm.add_moment_features(pd.DataFrame([row])).iloc[0]
    pred_log_mu = sum(value * float(features[name]) for name, value in coefs["log_mu_ratio"].items())
    pred_log_var = sum(
        value * float(features[name]) for name, value in coefs["log_sigma2_ratio"].items()
    )
    pred_log_mu = float(np.clip(pred_log_mu, -log_clip, log_clip))
    pred_log_var = float(np.clip(pred_log_var, -log_clip, log_clip))
    mu = float(features["mu_bartlett"] * np.exp(pred_log_mu))
    sigma2 = float(features["sigma2_bartlett"] * np.exp(pred_log_var))
    a = float(sigma2 / max(2.0 * mu, 1e-12))
    nu = float(2.0 * mu**2 / max(sigma2, 1e-12))
    pred = {
        "stage12_mu": mu,
        "stage12_sigma2": sigma2,
        "stage12_a": a,
        "stage12_nu": nu,
        "stage12_nu_norm": nu / max(float(features["nu0"]), 1e-12),
        "stage12_log_mu_ratio": pred_log_mu,
        "stage12_log_sigma2_ratio": pred_log_var,
    }
    return pred, features


def empirical_p_value(T_null: np.ndarray, T_obs: float) -> float:
    return float((1.0 + np.sum(T_null >= T_obs)) / (len(T_null) + 1.0))


def summarize_config(
    cfg: Config,
    T_obs: float,
    product_T: np.ndarray,
    permutation_T: np.ndarray,
    permutation_p_obs: float,
    standard_dist,
    pred: dict[str, float],
    features: pd.Series,
) -> dict[str, float | str | int]:
    nu0 = float(features["nu0"])
    row: dict[str, float | str | int] = {
        "config": cfg.label,
        "N": cfg.N,
        "kx": len(features.index) and int(features["kx"]),
        "ky": int(features["ky"]),
        "nu0": nu0,
        "T_obs": T_obs,
        "I_obs_nats": T_obs / (2.0 * cfg.N),
        "lam_min": float(features["lam_min"]),
        "lam_tp": float(features["lam_tp"]),
        "frac_cells_lt_1": float(features["frac_cells_lt_1"]),
        "expected_zero_frac": float(features["expected_zero_frac"]),
        "expected_singleton_frac": float(features["expected_singleton_frac"]),
        "product_mu": float(product_T.mean()),
        "product_sigma2": float(product_T.var(ddof=1)),
        "permutation_mu": float(permutation_T.mean()),
        "permutation_sigma2": float(permutation_T.var(ddof=1)),
        "standard_p_obs": jidt_analytic_p_value(standard_dist),
        "stage12_p_obs": float(stats.chi2.sf(T_obs / pred["stage12_a"], df=pred["stage12_nu"])),
        "product_emp_p_obs": empirical_p_value(product_T, T_obs),
        "permutation_emp_p_obs": float(permutation_p_obs),
    }
    row.update(pred)
    for q in [0.95, 0.99]:
        suffix = int(q * 100)
        row[f"product_q{suffix}"] = float(np.quantile(product_T, q))
        row[f"permutation_q{suffix}"] = float(np.quantile(permutation_T, q))
        row[f"standard_q{suffix}"] = jidt_analytic_quantile(standard_dist, q, cfg.N)
        row[f"stage12_q{suffix}"] = float(
            pred["stage12_a"] * stats.chi2.ppf(q, df=pred["stage12_nu"])
        )
        row[f"standard_to_product_q{suffix}"] = row[f"standard_q{suffix}"] / row[f"product_q{suffix}"]
        row[f"stage12_to_product_q{suffix}"] = row[f"stage12_q{suffix}"] / row[f"product_q{suffix}"]
        row[f"standard_to_permutation_q{suffix}"] = (
            row[f"standard_q{suffix}"] / row[f"permutation_q{suffix}"]
        )
        row[f"stage12_to_permutation_q{suffix}"] = (
            row[f"stage12_q{suffix}"] / row[f"permutation_q{suffix}"]
        )
        row[f"permutation_to_product_q{suffix}"] = (
            row[f"permutation_q{suffix}"] / row[f"product_q{suffix}"]
        )
    return row


def run_comparison(args: argparse.Namespace) -> tuple[pd.DataFrame, dict[str, dict[str, np.ndarray]]]:
    rng = np.random.default_rng(args.seed)
    coefs = selected_coefficients(Path(args.selected_model))
    rows = []
    nulls: dict[str, dict[str, np.ndarray]] = {}
    configs = stage2_configs(args.profile)

    print(f"Running Stage 14 profile={args.profile}, configs={len(configs)}, repeats={args.repeats}")
    for i, cfg in enumerate(configs, start=1):
        x_obs, y_obs, p_x_emp, p_y_emp = make_observed(cfg, rng)
        calc = MICalcDiscrete(int(max(x_obs.max(), y_obs.max()) + 1))
        T_obs = jidt_T(calc, x_obs, y_obs)
        pred, features = stage12_prediction(p_x_emp, p_y_emp, cfg.N, coefs, args.log_clip)
        standard_dist = jidt_analytic_standard(x_obs, y_obs)
        product_T = product_null_T(p_x_emp, p_y_emp, cfg.N, args.repeats, rng)
        if args.permutation_method == "jidt":
            permutation_T, permutation_p = jidt_permutation_null_T(x_obs, y_obs, args.repeats)
        else:
            permutation_T = permutation_null_T(x_obs, y_obs, args.repeats, rng)
            permutation_p = empirical_p_value(permutation_T, T_obs)
        row = summarize_config(
            cfg,
            T_obs,
            product_T,
            permutation_T,
            permutation_p,
            standard_dist,
            pred,
            features,
        )
        rows.append(row)
        nulls[cfg.label] = {
            "product": product_T,
            "permutation": permutation_T,
            "standard_dist": standard_dist,
            "standard_grid": np.asarray([]),
            "stage12_grid": np.asarray([]),
        }
        print(
            f"[{i:2d}/{len(configs)}] {cfg.label:<25} "
            f"Tobs={T_obs:.3g} p_std={row['standard_p_obs']:.3g} "
            f"p_s12={row['stage12_p_obs']:.3g} "
            f"p_prod={row['product_emp_p_obs']:.3g} "
            f"p_perm={row['permutation_emp_p_obs']:.3g} "
            f"q95 s12/product={row['stage12_to_product_q95']:.3f} "
            f"s12/perm={row['stage12_to_permutation_q95']:.3f}",
            flush=True,
        )
    return pd.DataFrame(rows), nulls


def calibration_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in [0.95, 0.99]:
        suffix = int(q * 100)
        for reference in ["product", "permutation"]:
            for model in ["standard", "stage12"]:
                col = f"{model}_to_{reference}_q{suffix}"
                ratio = df[col].to_numpy(dtype=float)
                abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
                rows.append(
                    dict(
                        q=q,
                        reference=reference,
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
        pp = df[f"permutation_to_product_q{suffix}"].to_numpy(dtype=float)
        abs_log = np.abs(np.log(np.maximum(pp, 1e-300)))
        rows.append(
            dict(
                q=q,
                reference="product",
                model="permutation_empirical",
                n=len(df),
                median_ratio=float(np.median(pp)),
                mean_abs_log_error=float(abs_log.mean()),
                within_05pct=float((abs_log < np.log(1.05)).mean()),
                within_10pct=float((abs_log < np.log(1.10)).mean()),
                p05=float(np.quantile(pp, 0.05)),
                p95=float(np.quantile(pp, 0.95)),
            )
        )
    return pd.DataFrame(rows)


def pvalue_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for reference in ["product", "permutation"]:
        ref_col = f"{reference}_emp_p_obs"
        for model in ["standard", "stage12"]:
            model_col = f"{model}_p_obs"
            err = df[model_col].to_numpy(dtype=float) - df[ref_col].to_numpy(dtype=float)
            rows.append(
                dict(
                    reference=reference,
                    model=model,
                    n=len(df),
                    mean_error=float(err.mean()),
                    median_abs_error=float(np.median(np.abs(err))),
                    mean_abs_error=float(np.mean(np.abs(err))),
                    max_abs_error=float(np.max(np.abs(err))),
                )
            )
    diff = df["permutation_emp_p_obs"].to_numpy(dtype=float) - df["product_emp_p_obs"].to_numpy(dtype=float)
    rows.append(
        dict(
            reference="product",
            model="permutation_empirical",
            n=len(df),
            mean_error=float(diff.mean()),
            median_abs_error=float(np.median(np.abs(diff))),
            mean_abs_error=float(np.mean(np.abs(diff))),
            max_abs_error=float(np.max(np.abs(diff))),
        )
    )
    return pd.DataFrame(rows)


def hist_cdf(values: np.ndarray, bins: int, upper: float) -> tuple[np.ndarray, np.ndarray]:
    counts, edges = np.histogram(values, bins=bins, range=(0.0, upper))
    centres = 0.5 * (edges[:-1] + edges[1:])
    cdf = np.cumsum(counts / max(len(values), 1))
    return centres, cdf


def plot_cdfs(df: pd.DataFrame, nulls: dict[str, dict[str, np.ndarray]], out_path: Path, bins: int) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        print(f"Skipping plot; matplotlib import failed: {exc}")
        return

    n = len(df)
    n_cols = 3
    n_rows = int(np.ceil(n / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.2 * n_cols, 3.9 * n_rows), squeeze=False)

    for idx, (_, row) in enumerate(df.iterrows()):
        ax = axes[idx // n_cols][idx % n_cols]
        label = str(row["config"])
        product_T_raw = nulls[label]["product"]
        permutation_T_raw = nulls[label]["permutation"]
        xmax = float(
            max(
                np.quantile(product_T_raw, 0.995),
                np.quantile(permutation_T_raw, 0.995),
                row["stage12_q99"],
            )
        )
        grid = np.linspace(0.0, xmax * 1.08, 400)
        product_x, product_cdf = hist_cdf(product_T_raw, bins, grid.max())
        permutation_x, permutation_cdf = hist_cdf(permutation_T_raw, bins, grid.max())

        ax.plot(product_x, product_cdf, color="red", linewidth=2.0, label="product null")
        ax.plot(
            permutation_x,
            permutation_cdf,
            color="purple",
            linewidth=1.8,
            linestyle="-.",
            label="JIDT permutation null",
        )
        ax.plot(
            grid,
            jidt_analytic_cdf(nulls[label]["standard_dist"], grid, int(row["N"])),
            color="green",
            linewidth=1.8,
            label="JIDT analytic chi2",
        )
        ax.plot(
            grid,
            stats.chi2.cdf(grid / float(row["stage12_a"]), df=float(row["stage12_nu"])),
            color="darkorange",
            linewidth=2.0,
            linestyle="--",
            label="Stage12 moment",
        )
        ax.axhline(0.95, color="blue", linewidth=1.0, alpha=0.6)
        ax.axvline(float(row["T_obs"]), color="black", linewidth=1.0, alpha=0.75)
        ax.set_xlim(0, grid.max())
        ax.set_ylim(0, 1.02)
        ax.set_title(label, fontsize=10, fontweight="bold")
        ax.set_xlabel("T = 2 N I_hat")
        ax.set_ylabel("CDF")
        ax.grid(True, alpha=0.2, linestyle="--")
        if idx == 0:
            ax.legend(fontsize=7.5, loc="lower right")

    for idx in range(n, n_rows * n_cols):
        axes[idx // n_cols][idx % n_cols].set_visible(False)

    fig.suptitle("Stage 14: product null vs permutation null vs chi-square approximations")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def print_summary(df: pd.DataFrame, summary: pd.DataFrame, pvalues: pd.DataFrame) -> None:
    print("\n=== Per-config p-values ===")
    print(
        df[
            [
                "config",
                "T_obs",
                "standard_p_obs",
                "stage12_p_obs",
                "product_emp_p_obs",
                "permutation_emp_p_obs",
            ]
        ].to_string(index=False)
    )
    print("\n=== Quantile calibration ===")
    print(summary.to_string(index=False))
    print("\n=== Observed p-value errors ===")
    print(pvalues.to_string(index=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["smoke", "stage2"], default="stage2")
    parser.add_argument("--repeats", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--log-clip", type=float, default=4.0)
    parser.add_argument("--permutation-method", choices=["jidt", "manual"], default="jidt")
    parser.add_argument("--plot-bins", type=int, default=100)
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

    df, nulls = run_comparison(args)
    summary = calibration_summary(df)
    pvalues = pvalue_summary(df)

    data_path = out_dir / "stage2_null_comparison_data.csv"
    summary_path = out_dir / "stage2_null_comparison_summary.csv"
    pvalue_path = out_dir / "stage2_null_comparison_pvalues.csv"
    plot_path = out_dir / "stage2_null_comparison_cdfs.png"
    df.to_csv(data_path, index=False)
    summary.to_csv(summary_path, index=False)
    pvalues.to_csv(pvalue_path, index=False)
    print(f"Saved data: {data_path}")
    print(f"Saved summary: {summary_path}")
    print(f"Saved p-value summary: {pvalue_path}")

    if not args.no_plot:
        plot_cdfs(df, nulls, plot_path, args.plot_bins)
        print(f"Saved CDF plot: {plot_path}")

    print_summary(df, summary, pvalues)


if __name__ == "__main__":
    main()
