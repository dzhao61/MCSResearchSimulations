"""
Stage 10: Compact weighted-sparsity formulas for effective-DF correction.

This stage takes the broad Stage 9 simulation data and fits small, interpretable
formula candidates for:

    T = 2N I(X;Y)  ~=  a_hat * chi2(nu_hat)

where

    nu_hat = nu0 * nu_norm_hat
    nu0    = (kx - 1)(ky - 1)

The Stage 9 regression lab showed that the strongest descriptors are not just
lambda_min or lambda_tp.  The key signal is the geometry of sparse cells:

    - what fraction/count of cells have expected count < 1 or < 5
    - rare-cell severity weighted by that sparse fraction/count
    - lambda_tp as a global harmonic sparsity scale

This script turns that insight into compact candidate formulas, validates them
with random k-fold CV and leave-one-pair-family-out CV, and checks whether the
resulting scaled chi-square approximation improves q95/q99 tail calibration.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
STAGE9 = ROOT / "EffectiveDFCorrection_Stage9_RobustRegressions"
OUT = Path(__file__).resolve().parent

sys.path.insert(0, str(STAGE9))
import robust_regressions as rr  # noqa: E402


os.environ["XDG_CACHE_HOME"] = str(OUT / ".cache")
os.environ.setdefault("MPLCONFIGDIR", str(OUT / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)


ALPHAS = rr.RIDGE_ALPHAS


FORMULAS: dict[str, list[str]] = {
    "baseline_lambda_tp": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
    ],
    "baseline_mixed": [
        "inv_lam_min",
        "inv_sqrt_lam_min",
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
    ],
    "weighted_frac": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "inv_lam_min_x_frac_lt1",
        "inv_sqrt_lam_min_x_frac_lt1",
        "inv_lam_min_x_frac_lt5",
        "inv_sqrt_lam_min_x_frac_lt5",
    ],
    "weighted_count": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
        "inv_lam_min_x_n_lt1_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt1_norm_nu0",
        "inv_lam_min_x_n_lt5_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt5_norm_nu0",
    ],
    "hybrid_weighted": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
        "inv_lam_min_x_frac_lt1",
        "inv_sqrt_lam_min_x_frac_lt1",
        "inv_lam_min_x_n_lt1_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt1_norm_nu0",
    ],
}


def load_data(path: Path, dedupe: bool) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded Stage 9 data: {path} ({len(df)} rows)")
    if dedupe:
        df = rr.dedupe_highest_bootstrap(df)
    return rr.add_regression_features(df).replace([np.inf, -np.inf], np.nan)


def r2(y: np.ndarray, pred: np.ndarray) -> float:
    return rr.r2_score(y, pred)


def mae(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y - pred)))


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def fit_one_formula(
    df: pd.DataFrame,
    target: str,
    formula_name: str,
    features: list[str],
    cv_folds: int,
    seed: int,
) -> tuple[dict, pd.DataFrame]:
    clean = df.dropna(subset=[target] + features + ["pair_family", "config_id"])
    X = clean[features].to_numpy(dtype=float)
    y = clean[target].to_numpy(dtype=float)
    y_delta = y - 1.0
    groups = clean["pair_family"].astype(str).to_numpy()
    rng = np.random.default_rng(seed)

    best = None
    for alpha in ALPHAS:
        beta, pred_delta, _ = rr.fit_ridge_zero_asymptote(X, y_delta, alpha)
        pred = 1.0 + pred_delta
        cv_delta = rr.kfold_predictions(X, y_delta, alpha, cv_folds, rng)
        cv_mask = np.isfinite(cv_delta)
        group_delta = rr.group_predictions(X, y_delta, groups, alpha)
        group_mask = np.isfinite(group_delta)
        row = dict(
            target=target,
            formula=formula_name,
            n=len(clean),
            n_features=len(features),
            alpha=alpha,
            train_r2=r2(y, pred),
            random_cv_r2=r2(y[cv_mask], 1.0 + cv_delta[cv_mask]),
            group_cv_r2=(
                r2(y[group_mask], 1.0 + group_delta[group_mask])
                if group_mask.sum() >= 3
                else np.nan
            ),
            train_mae=mae(y, pred),
            train_rmse=rmse(y, pred),
            features=",".join(features),
            coefficients=json.dumps(
                {name: float(value) for name, value in zip(features, beta)},
                sort_keys=True,
            ),
        )
        score = row["random_cv_r2"]
        if best is None or score > best[0]["random_cv_r2"]:
            best = (row, beta, pred)

    assert best is not None
    row, beta, pred = best
    prediction = pd.DataFrame(
        {
            "config_id": clean["config_id"].values,
            "target": target,
            "formula": formula_name,
            "observed": y,
            "predicted": pred,
            "residual": y - pred,
        }
    )
    return row, prediction


def fit_all(df: pd.DataFrame, args: argparse.Namespace) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    preds = []
    for target in ["nu_norm", "a"]:
        for i, (formula_name, features) in enumerate(FORMULAS.items()):
            row, pred = fit_one_formula(
                df,
                target,
                formula_name,
                features,
                args.cv_folds,
                args.seed + 101 * i + (0 if target == "nu_norm" else 10_000),
            )
            rows.append(row)
            preds.append(pred)

    results = pd.DataFrame(rows).sort_values(
        ["target", "random_cv_r2", "group_cv_r2"],
        ascending=[True, False, False],
    )
    predictions = pd.concat(preds, ignore_index=True)
    return results, predictions


def selected_predictions(results: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    selected = []
    for target in ["nu_norm", "a"]:
        best = results[results["target"] == target].sort_values(
            ["random_cv_r2", "group_cv_r2"],
            ascending=False,
        ).iloc[0]
        pred = predictions[
            (predictions["target"] == target)
            & (predictions["formula"] == best["formula"])
        ].copy()
        selected.append(pred.rename(columns={"predicted": f"pred_{target}"}))
    out = selected[0][["config_id", "pred_nu_norm"]].merge(
        selected[1][["config_id", "pred_a"]],
        on="config_id",
    )
    return out


def tail_calibration(
    df: pd.DataFrame,
    results: pd.DataFrame,
    predictions: pd.DataFrame,
    nu_norm_floor: float,
    a_floor: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    pred = selected_predictions(results, predictions)
    d = df.merge(pred, on="config_id")
    d["pred_nu_norm_clipped"] = np.maximum(d["pred_nu_norm"], nu_norm_floor)
    d["pred_a_clipped"] = np.maximum(d["pred_a"], a_floor)
    d["pred_nu"] = d["pred_nu_norm_clipped"] * d["nu0"]
    d["pred_a"] = d["pred_a_clipped"]

    rows = []
    for q in [0.95, 0.99]:
        q_suffix = int(q * 100)
        empirical = d[f"T_q{q_suffix}"]
        standard = d[f"q{q_suffix}_chi2"]
        true_mm = d["a"] * stats.chi2.ppf(q, df=np.maximum(d["nu"], 1e-8))
        pred_mm = d["pred_a"] * stats.chi2.ppf(q, df=d["pred_nu"])

        for model, values in [
            ("standard_chi2", standard),
            ("true_moment_matched", true_mm),
            ("predicted_formula", pred_mm),
        ]:
            ratio = values / empirical
            abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
            rows.append(
                dict(
                    q=q,
                    model=model,
                    n=len(d),
                    median_ratio=float(np.median(ratio)),
                    mean_abs_log_error=float(abs_log.mean()),
                    median_abs_log_error=float(np.median(abs_log)),
                    within_10pct=float((abs_log < np.log(1.10)).mean()),
                    within_20pct=float((abs_log < np.log(1.20)).mean()),
                    p01=float(np.quantile(ratio, 0.01)),
                    p05=float(np.quantile(ratio, 0.05)),
                    p95=float(np.quantile(ratio, 0.95)),
                    p99=float(np.quantile(ratio, 0.99)),
                )
            )
            d[f"{model}_q{q_suffix}_ratio_emp"] = ratio

    by_sparse = []
    d["sparse_bin"] = pd.cut(
        d["frac_cells_lt_1"],
        bins=[-0.001, 0, 0.25, 0.5, 0.75, 1.0],
        include_lowest=True,
    )
    for (q, sparse_bin), grp in d.groupby(["lam_target", "sparse_bin"], observed=True):
        by_sparse.append(
            dict(
                lam_target=q,
                sparse_bin=str(sparse_bin),
                n=len(grp),
                median_q95_standard=float(np.median(grp["standard_chi2_q95_ratio_emp"])),
                median_q95_formula=float(np.median(grp["predicted_formula_q95_ratio_emp"])),
                median_nu_norm=float(np.median(grp["nu_norm"])),
                median_a=float(np.median(grp["a"])),
            )
        )

    return pd.DataFrame(rows), pd.DataFrame(by_sparse)


def save_formula_summary(
    results: pd.DataFrame,
    out_path: Path,
    nu_norm_floor: float,
    a_floor: float,
) -> None:
    rows = []
    for target in ["nu_norm", "a"]:
        best = results[results["target"] == target].sort_values(
            ["random_cv_r2", "group_cv_r2"],
            ascending=False,
        ).iloc[0]
        rows.append(
            dict(
                target=target,
                formula=best["formula"],
                equation=(
                    f"{target}_raw = 1 + sum(beta_j * feature_j); "
                    f"{target}_hat = max({target}_raw, "
                    f"{nu_norm_floor if target == 'nu_norm' else a_floor})"
                ),
                alpha=best["alpha"],
                floor=nu_norm_floor if target == "nu_norm" else a_floor,
                random_cv_r2=best["random_cv_r2"],
                group_cv_r2=best["group_cv_r2"],
                features=best["features"],
                coefficients=best["coefficients"],
            )
        )
    pd.DataFrame(rows).to_csv(out_path, index=False)


def plot_summary(
    df: pd.DataFrame,
    results: pd.DataFrame,
    predictions: pd.DataFrame,
    out_path: Path,
    nu_norm_floor: float,
    a_floor: float,
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        print(f"Skipping plot; matplotlib import failed: {exc}")
        return

    pred = selected_predictions(results, predictions)
    d = df.merge(pred, on="config_id")
    d["pred_nu"] = np.maximum(d["pred_nu_norm"], nu_norm_floor) * d["nu0"]
    d["pred_a"] = np.maximum(d["pred_a"], a_floor)
    d["pred_q95"] = d["pred_a"] * stats.chi2.ppf(0.95, df=d["pred_nu"])
    d["pred_q95_ratio_emp"] = d["pred_q95"] / d["T_q95"]

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    panels = [
        ("nu_norm", "pred_nu_norm", r"$\nu_{eff}/\nu_0$"),
        ("a", "pred_a", "scale a"),
    ]
    for ax, (obs, pred_col, label) in zip(axes[0], panels):
        ax.scatter(d[obs], d[pred_col], s=10, alpha=0.35)
        lo = min(d[obs].min(), d[pred_col].min())
        hi = max(d[obs].max(), d[pred_col].max())
        ax.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1)
        ax.set_xlabel(f"observed {label}")
        ax.set_ylabel(f"predicted {label}")
        ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1][0]
    ax.scatter(d["frac_cells_lt_1"], d["nu_norm"] - d["pred_nu_norm"], s=10, alpha=0.35)
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("fraction cells with expected count < 1")
    ax.set_ylabel("nu_norm residual")
    ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1][1]
    ax.scatter(d["q95_ratio_chi2"], d["pred_q95_ratio_emp"], s=10, alpha=0.35)
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.axvline(1, color="black", linestyle=":", linewidth=1)
    ax.set_xlabel("empirical q95 / standard chi2 q95")
    ax.set_ylabel("formula q95 / empirical q95")
    ax.grid(True, alpha=0.25, linestyle="--")

    fig.suptitle("Stage 10: weighted-sparsity effective-DF formula")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def print_summary(results: pd.DataFrame, tail: pd.DataFrame) -> None:
    print("\n=== Formula comparison ===")
    print(
        results[
            [
                "target",
                "formula",
                "n_features",
                "alpha",
                "train_r2",
                "random_cv_r2",
                "group_cv_r2",
                "train_mae",
                "train_rmse",
            ]
        ].to_string(index=False)
    )

    print("\n=== Selected formulas ===")
    for target in ["nu_norm", "a"]:
        best = results[results["target"] == target].sort_values(
            ["random_cv_r2", "group_cv_r2"],
            ascending=False,
        ).iloc[0]
        print(
            f"{target}: {best['formula']}  "
            f"CV R2={best['random_cv_r2']:.4f}, group R2={best['group_cv_r2']:.4f}"
        )
        coefs = json.loads(best["coefficients"])
        for name, value in coefs.items():
            print(f"  {name:<36} {value:+.6g}")

    print("\n=== Tail calibration ===")
    print(
        tail[
            [
                "q",
                "model",
                "median_ratio",
                "mean_abs_log_error",
                "within_10pct",
                "within_20pct",
                "p05",
                "p95",
            ]
        ].to_string(index=False)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        default=str(STAGE9 / "robust_regression_data.csv"),
        help="Stage 9 robust_regression_data.csv path.",
    )
    parser.add_argument("--out-dir", default=str(OUT))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--cv-folds", type=int, default=5)
    parser.add_argument("--nu-norm-floor", type=float, default=0.2)
    parser.add_argument("--a-floor", type=float, default=0.2)
    parser.add_argument("--dedupe-highest-bootstrap", action="store_true", default=True)
    parser.add_argument("--no-dedupe-highest-bootstrap", dest="dedupe_highest_bootstrap", action="store_false")
    parser.add_argument("--no-plot", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(Path(args.data), args.dedupe_highest_bootstrap)
    results, predictions = fit_all(df, args)
    tail, by_sparse = tail_calibration(
        df,
        results,
        predictions,
        args.nu_norm_floor,
        args.a_floor,
    )

    results_path = out_dir / "weighted_formula_results.csv"
    predictions_path = out_dir / "weighted_formula_predictions.csv"
    formula_path = out_dir / "selected_weighted_formulas.csv"
    tail_path = out_dir / "weighted_formula_tail_calibration.csv"
    sparse_path = out_dir / "weighted_formula_sparse_bins.csv"
    plot_path = out_dir / "weighted_formula_summary.png"

    results.to_csv(results_path, index=False)
    predictions.to_csv(predictions_path, index=False)
    tail.to_csv(tail_path, index=False)
    by_sparse.to_csv(sparse_path, index=False)
    save_formula_summary(results, formula_path, args.nu_norm_floor, args.a_floor)

    print(f"Saved results: {results_path}")
    print(f"Saved predictions: {predictions_path}")
    print(f"Saved selected formulas: {formula_path}")
    print(f"Saved tail calibration: {tail_path}")
    print(f"Saved sparse-bin summary: {sparse_path}")

    if not args.no_plot:
        plot_summary(
            df,
            results,
            predictions,
            plot_path,
            args.nu_norm_floor,
            args.a_floor,
        )
        print(f"Saved plot: {plot_path}")

    print_summary(results, tail)


if __name__ == "__main__":
    main()
