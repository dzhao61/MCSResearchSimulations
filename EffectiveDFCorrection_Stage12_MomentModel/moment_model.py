"""
Stage 12: Moment-first sparse correction model.

Stages 9 and 10 modeled the scaled chi-square parameters directly:

    T = 2 N I_hat(X;Y) ~= a * chi2(nu_eff)

This stage moves one level upstream.  It predicts the null moments

    mu     = E[T]
    sigma2 = Var[T]

then derives

    a      = sigma2 / (2 mu)
    nu_eff = 2 mu^2 / sigma2.

The explainable core is the first-order Bartlett moment expansion:

    mu     ~= nu0 + B / N
    sigma2 ~= 2 nu0 + 4 B / N

with nu0 = (kx - 1)(ky - 1).  When exact Stage 9 descriptors are available,
this script uses

    B = ((sum_i 1/p_i - 1)(sum_j 1/q_j - 1)) / 6.

Otherwise it falls back to a symmetric proxy from sum_ij 1 / pi_ij.

The fitted part is only a residual correction for sparse-cell, occupancy, and
shape-asymmetry effects that the regular Bartlett term cannot explain.
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
STAGE10 = ROOT / "EffectiveDFCorrection_Stage10_WeightedSparsityFormula"
OUT = Path(__file__).resolve().parent

sys.path.insert(0, str(STAGE9))
import robust_regressions as rr  # noqa: E402


os.environ["XDG_CACHE_HOME"] = str(OUT / ".cache")
os.environ.setdefault("MPLCONFIGDIR", str(OUT / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)


ALPHAS = rr.RIDGE_ALPHAS
TARGETS = ["log_mu_ratio", "log_sigma2_ratio"]


MOMENT_FORMULAS: dict[str, list[str]] = {
    "bartlett_only": [],
    "sparse_thresholds": [
        "frac_cells_lt_0p5",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
    ],
    "harmonic_sparse": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "tp_x_frac_cells_lt_0p5",
        "tp_x_frac_cells_lt_1",
        "tp_x_frac_cells_lt_5",
        "tp_x_expected_cv",
        "tp_x_one_minus_cell_simpson_n",
    ],
    "weighted_sparse": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
        "inv_lam_min_x_frac_lt1",
        "inv_sqrt_lam_min_x_frac_lt1",
        "inv_lam_min_x_n_lt1_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt1_norm_nu0",
    ],
    "occupancy_collision": [
        "inv_lambda_simpson",
        "inv_sqrt_lambda_simpson",
        "expected_zero_frac",
        "expected_singleton_frac",
        "expected_doubleton_frac",
        "expected_le1_frac",
        "expected_zero_norm_nu0",
        "expected_singleton_norm_nu0",
        "doubleton_pressure_simpson",
        "zero_pressure_min",
        "singleton_pressure_min",
        "birthday_inverse",
        "sparse_collision_pressure",
    ],
    "exact_occupancy": [
        "expected_zero_frac",
        "expected_singleton_frac",
        "expected_doubleton_frac",
        "expected_le1_frac",
        "expected_le2_frac",
        "expected_zero_norm_nu0",
        "expected_singleton_norm_nu0",
        "expected_le1_norm_nu0",
        "expected_nonempty_frac",
        "birthday_inverse",
        "inv_lambda_simpson",
    ],
    "hybrid_moment": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "frac_cells_lt_0p5",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
        "inv_lam_min_x_frac_lt1",
        "inv_sqrt_lam_min_x_frac_lt1",
        "inv_lam_min_x_n_lt1_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt1_norm_nu0",
        "inv_lambda_simpson",
        "expected_zero_frac",
        "expected_singleton_frac",
        "expected_le1_frac",
        "expected_zero_norm_nu0",
        "expected_singleton_norm_nu0",
        "zero_pressure_min",
        "birthday_inverse",
        "tp_x_expected_cv",
        "tp_x_one_minus_cell_simpson_n",
        "tp_x_asym_min_p",
    ],
}


def load_data(path: Path, dedupe: bool) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded Stage 9 data: {path} ({len(df)} rows)")
    if dedupe:
        df = rr.dedupe_highest_bootstrap(df)
    return add_moment_features(df).replace([np.inf, -np.inf], np.nan)


def add_moment_features(df: pd.DataFrame) -> pd.DataFrame:
    d = rr.add_regression_features(df)
    eps = 1e-12

    # Older Stage 9 data stores only sum_ij 1 / pi_ij.  New/enriched data
    # stores bartlett_B exactly.  Keep the proxy as a fallback so the script
    # still runs on old CSVs.
    inv_pi_sum = np.maximum(d["inv_pi_sum"].to_numpy(dtype=float), 1.0)
    b_proxy = np.maximum(inv_pi_sum - 2.0 * np.sqrt(inv_pi_sum) + 1.0, 0.0) / 6.0
    d["B_proxy"] = b_proxy
    if "bartlett_B" in d.columns:
        d["B_active"] = d["bartlett_B"]
    else:
        d["B_active"] = d["B_proxy"]
    d["B_over_N"] = d["B_active"] / np.maximum(d["N"], eps)
    d["B_over_nu0_N"] = d["B_active"] / np.maximum(d["nu0"] * d["N"], eps)

    d["mu_bartlett"] = d["nu0"] + d["B_over_N"]
    d["sigma2_bartlett"] = 2.0 * d["nu0"] + 4.0 * d["B_over_N"]
    d["a_bartlett"] = d["sigma2_bartlett"] / np.maximum(2.0 * d["mu_bartlett"], eps)
    d["nu_bartlett"] = 2.0 * d["mu_bartlett"] ** 2 / np.maximum(d["sigma2_bartlett"], eps)
    d["nu_norm_bartlett"] = d["nu_bartlett"] / np.maximum(d["nu0"], eps)

    if {"mu", "sigma2"}.issubset(d.columns):
        d["mu_ratio_bartlett"] = d["mu"] / np.maximum(d["mu_bartlett"], eps)
        d["sigma2_ratio_bartlett"] = d["sigma2"] / np.maximum(d["sigma2_bartlett"], eps)
        d["log_mu_ratio"] = np.log(np.maximum(d["mu_ratio_bartlett"], eps))
        d["log_sigma2_ratio"] = np.log(np.maximum(d["sigma2_ratio_bartlett"], eps))

    lambda_simpson = d["N"] / np.maximum(d["cell_simpson"], eps)
    d["lambda_simpson"] = lambda_simpson
    d["inv_lambda_simpson"] = 1.0 / np.maximum(lambda_simpson, eps)
    d["inv_sqrt_lambda_simpson"] = 1.0 / np.sqrt(np.maximum(lambda_simpson, eps))
    d["zero_pressure_simpson"] = np.exp(-np.minimum(lambda_simpson, 700.0))
    d["singleton_pressure_simpson"] = lambda_simpson * d["zero_pressure_simpson"]
    d["doubleton_pressure_simpson"] = 0.5 * lambda_simpson**2 * d["zero_pressure_simpson"]
    d["zero_pressure_min"] = d["frac_cells_lt_1"] * np.exp(-np.minimum(d["lam_min"], 700.0))
    d["singleton_pressure_min"] = d["frac_cells_lt_1"] * d["lam_min"] * np.exp(
        -np.minimum(d["lam_min"], 700.0)
    )
    d["birthday_inverse"] = np.sqrt(np.maximum(d["cell_simpson"], eps)) / np.maximum(d["N"], eps)
    if "collision_prob" not in d.columns:
        d["collision_prob"] = 1.0 / np.maximum(d["cell_simpson"], eps)
    if "expected_collision_count" not in d.columns:
        d["expected_collision_count"] = d["N"] * (d["N"] - 1.0) * d["collision_prob"] / 2.0
    d["sparse_collision_pressure"] = d["frac_cells_lt_1"] * d["inv_lambda_simpson"]

    if "expected_zero_count" not in d.columns:
        d["expected_zero_count"] = d["k_cells"] * d["zero_pressure_simpson"]
    if "expected_singleton_count" not in d.columns:
        d["expected_singleton_count"] = d["k_cells"] * d["singleton_pressure_simpson"]
    if "expected_doubleton_count" not in d.columns:
        d["expected_doubleton_count"] = d["k_cells"] * d["doubleton_pressure_simpson"]
    if "expected_le1_count" not in d.columns:
        d["expected_le1_count"] = d["expected_zero_count"] + d["expected_singleton_count"]
    if "expected_le2_count" not in d.columns:
        d["expected_le2_count"] = d["expected_le1_count"] + d["expected_doubleton_count"]
    if "expected_nonempty_count" not in d.columns:
        d["expected_nonempty_count"] = d["k_cells"] - d["expected_zero_count"]

    d["expected_zero_frac"] = d["expected_zero_count"] / np.maximum(d["k_cells"], eps)
    d["expected_singleton_frac"] = d["expected_singleton_count"] / np.maximum(d["k_cells"], eps)
    d["expected_doubleton_frac"] = d["expected_doubleton_count"] / np.maximum(d["k_cells"], eps)
    d["expected_le1_frac"] = d["expected_le1_count"] / np.maximum(d["k_cells"], eps)
    d["expected_le2_frac"] = d["expected_le2_count"] / np.maximum(d["k_cells"], eps)
    d["expected_nonempty_frac"] = d["expected_nonempty_count"] / np.maximum(d["k_cells"], eps)
    d["expected_zero_norm_nu0"] = d["expected_zero_count"] / np.maximum(d["nu0"], 1.0)
    d["expected_singleton_norm_nu0"] = d["expected_singleton_count"] / np.maximum(d["nu0"], 1.0)
    d["expected_le1_norm_nu0"] = d["expected_le1_count"] / np.maximum(d["nu0"], 1.0)

    return d


def r2(y: np.ndarray, pred: np.ndarray) -> float:
    return rr.r2_score(y, pred)


def mae(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y - pred)))


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def fit_empty_formula(clean: pd.DataFrame, target: str, formula_name: str) -> tuple[dict, pd.DataFrame]:
    y = clean[target].to_numpy(dtype=float)
    pred = np.zeros_like(y)
    row = dict(
        target=target,
        formula=formula_name,
        n=len(clean),
        n_features=0,
        alpha=np.nan,
        train_r2=r2(y, pred),
        random_cv_r2=r2(y, pred),
        group_cv_r2=r2(y, pred),
        train_mae=mae(y, pred),
        train_rmse=rmse(y, pred),
        features="",
        coefficients=json.dumps({}, sort_keys=True),
    )
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


def fit_one_formula(
    df: pd.DataFrame,
    target: str,
    formula_name: str,
    features: list[str],
    cv_folds: int,
    seed: int,
) -> tuple[dict, pd.DataFrame]:
    clean = df.dropna(subset=[target] + features + ["pair_family", "config_id"])
    if not features:
        return fit_empty_formula(clean, target, formula_name)

    X = clean[features].to_numpy(dtype=float)
    y = clean[target].to_numpy(dtype=float)
    groups = clean["pair_family"].astype(str).to_numpy()
    rng = np.random.default_rng(seed)

    best = None
    for alpha in ALPHAS:
        beta, pred, _ = rr.fit_ridge_zero_asymptote(X, y, alpha)
        cv_pred = rr.kfold_predictions(X, y, alpha, cv_folds, rng)
        cv_mask = np.isfinite(cv_pred)
        group_pred = rr.group_predictions(X, y, groups, alpha)
        group_mask = np.isfinite(group_pred)
        row = dict(
            target=target,
            formula=formula_name,
            n=len(clean),
            n_features=len(features),
            alpha=alpha,
            train_r2=r2(y, pred),
            random_cv_r2=r2(y[cv_mask], cv_pred[cv_mask]),
            group_cv_r2=(
                r2(y[group_mask], group_pred[group_mask])
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
        score = row["random_cv_r2"] if np.isfinite(row["random_cv_r2"]) else row["train_r2"]
        if best is None or score > best[0]:
            best = (score, row, pred)

    assert best is not None
    _, row, pred = best
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
    for target in TARGETS:
        for i, (formula_name, features) in enumerate(MOMENT_FORMULAS.items()):
            row, pred = fit_one_formula(
                df,
                target,
                formula_name,
                features,
                args.cv_folds,
                args.seed + 101 * i + (0 if target == "log_mu_ratio" else 10_000),
            )
            rows.append(row)
            preds.append(pred)

    results = pd.DataFrame(rows).sort_values(
        ["target", "random_cv_r2", "group_cv_r2"],
        ascending=[True, False, False],
    )
    predictions = pd.concat(preds, ignore_index=True)
    return results, predictions


def best_formula(results: pd.DataFrame, target: str) -> pd.Series:
    return results[results["target"] == target].sort_values(
        ["random_cv_r2", "group_cv_r2"],
        ascending=False,
    ).iloc[0]


def selected_predictions(results: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    for target in TARGETS:
        best = best_formula(results, target)
        pred = predictions[
            (predictions["target"] == target)
            & (predictions["formula"] == best["formula"])
        ].copy()
        pieces.append(pred.rename(columns={"predicted": f"pred_{target}"}))
    out = pieces[0][["config_id", "pred_log_mu_ratio"]].merge(
        pieces[1][["config_id", "pred_log_sigma2_ratio"]],
        on="config_id",
    )
    return out


def add_moment_predictions(
    df: pd.DataFrame,
    results: pd.DataFrame,
    predictions: pd.DataFrame,
    log_clip: float,
    nu_norm_floor: float,
    a_floor: float,
) -> pd.DataFrame:
    pred = selected_predictions(results, predictions)
    d = df.merge(pred, on="config_id")
    d["pred_log_mu_ratio_clipped"] = d["pred_log_mu_ratio"].clip(-log_clip, log_clip)
    d["pred_log_sigma2_ratio_clipped"] = d["pred_log_sigma2_ratio"].clip(-log_clip, log_clip)
    d["pred_mu"] = d["mu_bartlett"] * np.exp(d["pred_log_mu_ratio_clipped"])
    d["pred_sigma2"] = d["sigma2_bartlett"] * np.exp(d["pred_log_sigma2_ratio_clipped"])
    d["pred_a_raw"] = d["pred_sigma2"] / np.maximum(2.0 * d["pred_mu"], 1e-12)
    d["pred_nu_raw"] = 2.0 * d["pred_mu"] ** 2 / np.maximum(d["pred_sigma2"], 1e-12)
    d["pred_nu_norm_raw"] = d["pred_nu_raw"] / np.maximum(d["nu0"], 1e-12)
    d["pred_a"] = np.maximum(d["pred_a_raw"], a_floor)
    d["pred_nu_norm"] = np.maximum(d["pred_nu_norm_raw"], nu_norm_floor)
    d["pred_nu"] = d["pred_nu_norm"] * d["nu0"]
    return d


def load_stage10_direct_formula(df: pd.DataFrame) -> pd.DataFrame | None:
    results_path = STAGE10 / "weighted_formula_results.csv"
    predictions_path = STAGE10 / "weighted_formula_predictions.csv"
    if not results_path.exists() or not predictions_path.exists():
        return None

    try:
        results = pd.read_csv(results_path)
        predictions = pd.read_csv(predictions_path)
    except Exception:
        return None

    pieces = []
    for target in ["nu_norm", "a"]:
        sub = results[results["target"] == target]
        if sub.empty:
            return None
        best = sub.sort_values(["random_cv_r2", "group_cv_r2"], ascending=False).iloc[0]
        pred = predictions[
            (predictions["target"] == target)
            & (predictions["formula"] == best["formula"])
        ][["config_id", "predicted"]].rename(columns={"predicted": f"stage10_pred_{target}"})
        pieces.append(pred)

    out = pieces[0].merge(pieces[1], on="config_id")
    return df[["config_id", "nu0"]].merge(out, on="config_id", how="inner")


def calibration_rows(
    d: pd.DataFrame,
    q: float,
    model_values: list[tuple[str, pd.Series | np.ndarray]],
) -> list[dict]:
    q_suffix = int(q * 100)
    empirical = d[f"T_q{q_suffix}"]
    rows = []
    for model, values in model_values:
        ratio = np.asarray(values, dtype=float) / np.asarray(empirical, dtype=float)
        abs_log = np.abs(np.log(np.maximum(ratio, 1e-300)))
        rows.append(
            dict(
                q=q,
                model=model,
                n=len(d),
                median_ratio=float(np.median(ratio)),
                mean_abs_log_error=float(abs_log.mean()),
                median_abs_log_error=float(np.median(abs_log)),
                within_05pct=float((abs_log < np.log(1.05)).mean()),
                within_10pct=float((abs_log < np.log(1.10)).mean()),
                within_20pct=float((abs_log < np.log(1.20)).mean()),
                p01=float(np.quantile(ratio, 0.01)),
                p05=float(np.quantile(ratio, 0.05)),
                p95=float(np.quantile(ratio, 0.95)),
                p99=float(np.quantile(ratio, 0.99)),
            )
        )
        d[f"{model}_q{q_suffix}_ratio_emp"] = ratio
    return rows


def tail_calibration(
    df: pd.DataFrame,
    results: pd.DataFrame,
    predictions: pd.DataFrame,
    log_clip: float,
    nu_norm_floor: float,
    a_floor: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    d = add_moment_predictions(df, results, predictions, log_clip, nu_norm_floor, a_floor)
    stage10 = load_stage10_direct_formula(d)
    if stage10 is not None:
        d = d.merge(stage10.drop(columns=["nu0"]), on="config_id", how="left")
        d["stage10_pred_nu"] = np.maximum(d["stage10_pred_nu_norm"], nu_norm_floor) * d["nu0"]
        d["stage10_pred_a"] = np.maximum(d["stage10_pred_a"], a_floor)

    rows = []
    for q in [0.95, 0.99]:
        q_suffix = int(q * 100)
        standard = d[f"q{q_suffix}_chi2"]
        true_mm = d["a"] * stats.chi2.ppf(q, df=np.maximum(d["nu"], 1e-8))
        bartlett = d["a_bartlett"] * stats.chi2.ppf(q, df=np.maximum(d["nu_bartlett"], 1e-8))
        pred_mm = d["pred_a"] * stats.chi2.ppf(q, df=np.maximum(d["pred_nu"], 1e-8))
        model_values: list[tuple[str, pd.Series | np.ndarray]] = [
            ("standard_chi2", standard),
            ("bartlett_proxy", bartlett),
            ("true_moment_matched", true_mm),
            ("predicted_moment_model", pred_mm),
        ]
        if "stage10_pred_nu" in d:
            stage10_values = d["stage10_pred_a"] * stats.chi2.ppf(
                q,
                df=np.maximum(d["stage10_pred_nu"], 1e-8),
            )
            model_values.append(("stage10_direct_formula", stage10_values))
        rows.extend(calibration_rows(d, q, model_values))

    by_sparse = []
    d["sparse_bin"] = pd.cut(
        d["frac_cells_lt_1"],
        bins=[-0.001, 0, 0.25, 0.5, 0.75, 1.0],
        include_lowest=True,
    )
    for (lam_target, sparse_bin), grp in d.groupby(["lam_target", "sparse_bin"], observed=True):
        by_sparse.append(
            dict(
                lam_target=lam_target,
                sparse_bin=str(sparse_bin),
                n=len(grp),
                median_mu_ratio=float(np.median(grp["pred_mu"] / grp["mu"])),
                median_sigma2_ratio=float(np.median(grp["pred_sigma2"] / grp["sigma2"])),
                median_q95_standard=float(np.median(grp["standard_chi2_q95_ratio_emp"])),
                median_q95_bartlett=float(np.median(grp["bartlett_proxy_q95_ratio_emp"])),
                median_q95_moment=float(np.median(grp["predicted_moment_model_q95_ratio_emp"])),
                median_nu_norm=float(np.median(grp["nu_norm"])),
                median_a=float(np.median(grp["a"])),
            )
        )

    return pd.DataFrame(rows), pd.DataFrame(by_sparse), d


def save_formula_summary(
    results: pd.DataFrame,
    out_path: Path,
    log_clip: float,
    nu_norm_floor: float,
    a_floor: float,
) -> None:
    rows = []
    for target in TARGETS:
        best = best_formula(results, target)
        rows.append(
            dict(
                target=target,
                formula=best["formula"],
                equation=(
                    f"{target}_hat = clip(sum(beta_j * feature_j), +/-{log_clip}); "
                    "mu_hat = mu_bartlett * exp(log_mu_ratio_hat); "
                    "sigma2_hat = sigma2_bartlett * exp(log_sigma2_ratio_hat); "
                    f"nu_norm floor={nu_norm_floor}; a floor={a_floor}"
                ),
                alpha=best["alpha"],
                random_cv_r2=best["random_cv_r2"],
                group_cv_r2=best["group_cv_r2"],
                features=best["features"],
                coefficients=best["coefficients"],
            )
        )
    pd.DataFrame(rows).to_csv(out_path, index=False)


def plot_summary(
    calibrated: pd.DataFrame,
    results: pd.DataFrame,
    out_path: Path,
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        print(f"Skipping plot; matplotlib import failed: {exc}")
        return

    d = calibrated
    d["pred_q95"] = d["pred_a"] * stats.chi2.ppf(0.95, df=np.maximum(d["pred_nu"], 1e-8))
    d["pred_q95_ratio_emp"] = d["pred_q95"] / d["T_q95"]

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    panels = [
        ("mu", "pred_mu", "mean mu"),
        ("sigma2", "pred_sigma2", "variance sigma2"),
    ]
    for ax, (obs, pred, label) in zip(axes[0], panels):
        ax.scatter(d[obs], d[pred], s=10, alpha=0.35)
        lo = float(min(d[obs].min(), d[pred].min()))
        hi = float(max(d[obs].max(), d[pred].max()))
        ax.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1)
        ax.set_xlabel(f"observed {label}")
        ax.set_ylabel(f"predicted {label}")
        ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1][0]
    ax.scatter(d["frac_cells_lt_1"], d["pred_mu"] / d["mu"], s=10, alpha=0.35, label="mu")
    ax.scatter(
        d["frac_cells_lt_1"],
        d["pred_sigma2"] / d["sigma2"],
        s=10,
        alpha=0.25,
        label="sigma2",
    )
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("fraction cells with expected count < 1")
    ax.set_ylabel("predicted / observed")
    ax.legend()
    ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1][1]
    ax.scatter(d["q95_ratio_chi2"], d["pred_q95_ratio_emp"], s=10, alpha=0.35)
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.axvline(1, color="black", linestyle=":", linewidth=1)
    ax.set_xlabel("empirical q95 / standard chi2 q95")
    ax.set_ylabel("moment-model q95 / empirical q95")
    ax.grid(True, alpha=0.25, linestyle="--")

    title_bits = []
    for target in TARGETS:
        best = best_formula(results, target)
        title_bits.append(f"{target}: {best['formula']}")
    fig.suptitle("Stage 12: moment-first sparse correction (" + "; ".join(title_bits) + ")")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def print_summary(results: pd.DataFrame, tail: pd.DataFrame) -> None:
    print("\n=== Moment residual model comparison ===")
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

    print("\n=== Selected moment models ===")
    for target in TARGETS:
        best = best_formula(results, target)
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
                "within_05pct",
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
    parser.add_argument("--log-clip", type=float, default=4.0)
    parser.add_argument("--nu-norm-floor", type=float, default=0.05)
    parser.add_argument("--a-floor", type=float, default=0.05)
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
    tail, by_sparse, calibrated = tail_calibration(
        df,
        results,
        predictions,
        args.log_clip,
        args.nu_norm_floor,
        args.a_floor,
    )

    results_path = out_dir / "moment_model_results.csv"
    predictions_path = out_dir / "moment_model_predictions.csv"
    selected_path = out_dir / "selected_moment_models.csv"
    tail_path = out_dir / "moment_model_tail_calibration.csv"
    sparse_path = out_dir / "moment_model_sparse_bins.csv"
    calibrated_path = out_dir / "moment_model_calibrated_predictions.csv"
    plot_path = out_dir / "moment_model_summary.png"

    results.to_csv(results_path, index=False)
    predictions.to_csv(predictions_path, index=False)
    tail.to_csv(tail_path, index=False)
    by_sparse.to_csv(sparse_path, index=False)
    calibrated.to_csv(calibrated_path, index=False)
    save_formula_summary(
        results,
        selected_path,
        args.log_clip,
        args.nu_norm_floor,
        args.a_floor,
    )

    print(f"Saved results: {results_path}")
    print(f"Saved predictions: {predictions_path}")
    print(f"Saved selected moment models: {selected_path}")
    print(f"Saved tail calibration: {tail_path}")
    print(f"Saved sparse-bin summary: {sparse_path}")
    print(f"Saved calibrated predictions: {calibrated_path}")

    if not args.no_plot:
        plot_summary(calibrated, results, plot_path)
        print(f"Saved plot: {plot_path}")

    print_summary(results, tail)


if __name__ == "__main__":
    main()
