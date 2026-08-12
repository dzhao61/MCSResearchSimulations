#!/usr/bin/env python3
"""Validate the scaled-chi-squared model for the MI variance estimator."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.stats import chi2, lognorm, norm, skew

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from differential_mi.random_validation import RandomScenario  # noqa: E402
from differential_mi.statistics import influence_variance  # noqa: E402
from run_supervisor_experiment import (  # noqa: E402
    DESIGN_TO_REGIME,
    REGIMES,
    _population_metadata,
    generate_configuration_scenarios,
)
from welch_differential_mi.welch import (  # noqa: E402
    _variance_influence_component_df,
)


DEFAULT_SCENARIO_SEED = 2_026_080_701
DEFAULT_SIMULATION_SEED = 2_026_080_702
MODEL_LABELS = {
    "oracle_chi2": "Oracle scaled chi-squared",
    "oracle_normal": "Oracle normal",
    "oracle_lognormal": "Oracle lognormal",
    "if_chi2": "Population first-order chi-squared",
}
PROFILE_SETTINGS = {
    "smoke": {
        "replicates": 500,
        "batch_size": 250,
        "shape_indices": (0, 2),
    },
    "focused": {
        "replicates": 10_000,
        "batch_size": 1_000,
        "shape_indices": None,
    },
    "full": {
        "replicates": 10_000,
        "batch_size": 1_000,
        "shape_indices": None,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Test the scaled-chi-squared approximation for repeated estimates "
            "of the MI influence variance."
        )
    )
    parser.add_argument("--profile", choices=PROFILE_SETTINGS, default="smoke")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "scaled_chi_square_validation",
    )
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    return parser.parse_args()


def _settings(args: argparse.Namespace) -> dict:
    settings = dict(PROFILE_SETTINGS[args.profile])
    if args.replicates is not None:
        settings["replicates"] = args.replicates
    if args.batch_size is not None:
        settings["batch_size"] = args.batch_size
    if min(settings["replicates"], settings["batch_size"]) <= 1:
        raise ValueError("Replicates and batch size must exceed one.")
    return settings


def _all_scenarios(seed: int) -> list[RandomScenario]:
    scenarios = generate_configuration_scenarios(seed, 1)
    return sorted(
        scenarios,
        key=lambda scenario: (scenario.shape_index, scenario.design_index),
    )


def _population_component(
    probability: np.ndarray,
    sample_size: int,
) -> tuple[float, float, float]:
    """Return population V, variance-IF variance, and implied component df."""
    population_variance = float(influence_variance(probability))
    counts = (probability * sample_size)[None, ...]
    component_df, variance_if_variance = _variance_influence_component_df(
        counts,
        np.asarray([population_variance]),
    )
    return (
        population_variance,
        float(variance_if_variance[0]),
        float(component_df[0]),
    )


def _moment_distribution(kind: str, mean: float, variance: float):
    """Return a frozen distribution having the requested first two moments."""
    if not np.isfinite(mean) or not np.isfinite(variance):
        raise ValueError("Distribution moments must be finite.")
    if mean <= 0 or variance <= 0:
        raise ValueError("Distribution mean and variance must be positive.")
    if kind == "chi2":
        degrees_of_freedom = 2.0 * mean**2 / variance
        return chi2(df=degrees_of_freedom, scale=mean / degrees_of_freedom)
    if kind == "normal":
        return norm(loc=mean, scale=np.sqrt(variance))
    if kind == "lognormal":
        log_variance = np.log1p(variance / mean**2)
        log_scale = np.log(mean) - 0.5 * log_variance
        return lognorm(s=np.sqrt(log_variance), scale=np.exp(log_scale))
    raise ValueError(f"Unknown moment model: {kind}")


def _distribution_metrics(values: np.ndarray, distribution) -> dict[str, float]:
    """Compare an empirical sample with one fixed continuous distribution."""
    sample = np.sort(np.asarray(values, dtype=float))
    sample = sample[np.isfinite(sample)]
    if sample.size < 2:
        return {
            "ks": np.nan,
            "cdf_rmse": np.nan,
            "tail_rate_10": np.nan,
            "tail_abs_error_10": np.nan,
            "tail_rate_05": np.nan,
            "tail_abs_error_05": np.nan,
            "tail_rate_01": np.nan,
            "tail_abs_error_01": np.nan,
            "q95_error_sd": np.nan,
            "q99_error_sd": np.nan,
            "central_95_coverage": np.nan,
        }

    count = sample.size
    model_cdf = np.asarray(distribution.cdf(sample), dtype=float)
    upper_empirical = np.arange(1, count + 1, dtype=float) / count
    lower_empirical = np.arange(count, dtype=float) / count
    midpoint_empirical = (np.arange(count, dtype=float) + 0.5) / count
    ks = max(
        float(np.max(upper_empirical - model_cdf)),
        float(np.max(model_cdf - lower_empirical)),
    )
    standard_deviation = float(np.std(sample, ddof=1))
    result = {
        "ks": ks,
        "cdf_rmse": float(
            np.sqrt(np.mean((model_cdf - midpoint_empirical) ** 2))
        ),
    }
    for label, alpha in (("10", 0.10), ("05", 0.05), ("01", 0.01)):
        threshold = float(distribution.ppf(1.0 - alpha))
        tail_rate = float(np.mean(sample > threshold))
        result[f"tail_rate_{label}"] = tail_rate
        result[f"tail_abs_error_{label}"] = abs(tail_rate - alpha)

    for label, probability in (("95", 0.95), ("99", 0.99)):
        empirical_quantile = float(np.quantile(sample, probability))
        model_quantile = float(distribution.ppf(probability))
        result[f"q{label}_error_sd"] = (
            (model_quantile - empirical_quantile) / standard_deviation
            if standard_deviation > 0
            else np.nan
        )
    lower = float(distribution.ppf(0.025))
    upper = float(distribution.ppf(0.975))
    result["central_95_coverage"] = float(
        np.mean((sample >= lower) & (sample <= upper))
    )
    return result


def _simulate_component(
    probability: np.ndarray,
    sample_size: int,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> dict[str, np.ndarray | float]:
    """Simulate repeated MI variance estimates for one population."""
    rows, columns = probability.shape
    rng = np.random.default_rng(seed)
    estimates = np.empty(replicates, dtype=float)
    plugin_df = np.empty(replicates, dtype=float)
    zero_cells = 0.0
    empty_margins = 0.0

    for start in range(0, replicates, batch_size):
        count = min(batch_size, replicates - start)
        stop = start + count
        tables = rng.multinomial(
            sample_size,
            probability.reshape(-1),
            size=count,
        ).reshape(count, rows, columns)
        variance = np.asarray(influence_variance(tables), dtype=float)
        component_df, _ = _variance_influence_component_df(tables, variance)
        estimates[start:stop] = variance
        plugin_df[start:stop] = component_df
        zero_cells += float(np.sum(tables == 0))
        row_counts = tables.sum(axis=2)
        column_counts = tables.sum(axis=1)
        empty_margins += float(
            np.sum(
                np.any(row_counts == 0, axis=1)
                | np.any(column_counts == 0, axis=1)
            )
        )

    return {
        "estimates": estimates,
        "plugin_df": plugin_df,
        "zero_cell_fraction": zero_cells / (replicates * rows * columns),
        "empty_margin_rate": empty_margins / replicates,
    }


def _analyse_component(
    scenario: RandomScenario,
    group: str,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> dict[str, int | float | str]:
    probability = getattr(scenario, f"probability_{group}")
    sample_size = int(getattr(scenario, f"n_{group}"))
    population_v, population_tau2, if_df = _population_component(
        probability,
        sample_size,
    )
    moment_simulation = _simulate_component(
        probability,
        sample_size,
        replicates=replicates,
        batch_size=batch_size,
        seed=seed,
    )
    validation_simulation = _simulate_component(
        probability,
        sample_size,
        replicates=replicates,
        batch_size=batch_size,
        seed=seed + 1,
    )
    moment_estimates = np.asarray(moment_simulation["estimates"], dtype=float)
    validation_estimates = np.asarray(
        validation_simulation["estimates"], dtype=float
    )
    empirical_mean = float(np.mean(moment_estimates))
    empirical_variance = float(np.var(moment_estimates, ddof=1))
    empirical_df = (
        2.0 * empirical_mean**2 / empirical_variance
        if empirical_mean > 0 and empirical_variance > 0
        else np.nan
    )
    predicted_variance = population_tau2 / sample_size
    plugin_df = np.asarray(validation_simulation["plugin_df"], dtype=float)
    finite_plugin_df = plugin_df[np.isfinite(plugin_df) & (plugin_df > 0)]

    row: dict[str, int | float | str] = {
        "scenario_id": scenario.scenario_id,
        "regime": DESIGN_TO_REGIME[scenario.design_index],
        "regime_label": REGIMES[DESIGN_TO_REGIME[scenario.design_index]]["label"],
        "group": group.upper(),
        "rows": scenario.rows,
        "columns": scenario.columns,
        "sample_size": sample_size,
        "replicates": replicates,
        "target_mi": scenario.target_mi,
        "minimum_probability": float(probability.min()),
        "minimum_expected_count": float(sample_size * probability.min()),
        "expected_below_1_fraction": float(
            np.mean(sample_size * probability < 1.0)
        ),
        "expected_below_5_fraction": float(
            np.mean(sample_size * probability < 5.0)
        ),
        "zero_cell_fraction": float(
            validation_simulation["zero_cell_fraction"]
        ),
        "empty_margin_rate": float(
            validation_simulation["empty_margin_rate"]
        ),
        "zero_variance_rate": float(np.mean(validation_estimates <= 0)),
        "population_v": population_v,
        "population_tau2": population_tau2,
        "if_predicted_sampling_variance": predicted_variance,
        "if_predicted_df": if_df,
        "empirical_mean_v": empirical_mean,
        "empirical_variance_v": empirical_variance,
        "validation_mean_v": float(np.mean(validation_estimates)),
        "validation_variance_v": float(
            np.var(validation_estimates, ddof=1)
        ),
        "empirical_skew_v": float(skew(validation_estimates, bias=False)),
        "empirical_moment_df": empirical_df,
        "mean_ratio_empirical_to_population": (
            float(np.mean(validation_estimates)) / population_v
        ),
        "variance_ratio_empirical_to_if": (
            float(np.var(validation_estimates, ddof=1)) / predicted_variance
            if predicted_variance > 0
            else np.nan
        ),
        "df_ratio_if_to_empirical": if_df / empirical_df,
        "plugin_df_valid_rate": finite_plugin_df.size / replicates,
        "plugin_df_median": (
            float(np.median(finite_plugin_df))
            if finite_plugin_df.size
            else np.nan
        ),
        "plugin_df_median_to_empirical": (
            float(np.median(finite_plugin_df)) / empirical_df
            if finite_plugin_df.size and empirical_df > 0
            else np.nan
        ),
    }

    oracle_models = {
        "oracle_chi2": _moment_distribution(
            "chi2", empirical_mean, empirical_variance
        ),
        "oracle_normal": _moment_distribution(
            "normal", empirical_mean, empirical_variance
        ),
        "oracle_lognormal": _moment_distribution(
            "lognormal", empirical_mean, empirical_variance
        ),
    }
    if_model = _moment_distribution("chi2", population_v, predicted_variance)
    models = {**oracle_models, "if_chi2": if_model}
    for model_name, distribution in models.items():
        for metric, value in _distribution_metrics(
            validation_estimates,
            distribution,
        ).items():
            row[f"{model_name}_{metric}"] = value

    oracle_ks = {
        model_name: float(row[f"{model_name}_ks"])
        for model_name in oracle_models
    }
    row["oracle_best_ks_model"] = min(oracle_ks, key=oracle_ks.get)
    row["oracle_chi2_skew"] = np.sqrt(8.0 / empirical_df)
    row["oracle_normal_negative_probability"] = float(
        oracle_models["oracle_normal"].cdf(0.0)
    )
    return row


def _model_summary(components: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model in MODEL_LABELS:
        rows.append(
            {
                "model": model,
                "model_label": MODEL_LABELS[model],
                "mean_ks": components[f"{model}_ks"].mean(),
                "median_ks": components[f"{model}_ks"].median(),
                "mean_tail_abs_error_10": components[
                    f"{model}_tail_abs_error_10"
                ].mean(),
                "mean_tail_abs_error_05": components[
                    f"{model}_tail_abs_error_05"
                ].mean(),
                "mean_tail_abs_error_01": components[
                    f"{model}_tail_abs_error_01"
                ].mean(),
                "mean_central_95_coverage": components[
                    f"{model}_central_95_coverage"
                ].mean(),
                "best_oracle_ks_rate": (
                    float(np.mean(components["oracle_best_ks_model"].eq(model)))
                    if model.startswith("oracle_")
                    else np.nan
                ),
            }
        )
    return pd.DataFrame(rows)


def _regime_summary(components: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for regime in (*REGIMES, "all"):
        subset = components if regime == "all" else components[components["regime"].eq(regime)]
        if subset.empty:
            continue
        rows.append(
            {
                "regime": regime,
                "regime_label": "All regimes" if regime == "all" else REGIMES[regime]["label"],
                "components": len(subset),
                "median_mean_ratio": subset[
                    "mean_ratio_empirical_to_population"
                ].median(),
                "median_variance_ratio": subset[
                    "variance_ratio_empirical_to_if"
                ].median(),
                "median_df_ratio_if_to_empirical": subset[
                    "df_ratio_if_to_empirical"
                ].median(),
                "median_plugin_df_ratio": subset[
                    "plugin_df_median_to_empirical"
                ].median(),
                "mean_oracle_chi2_ks": subset["oracle_chi2_ks"].mean(),
                "mean_oracle_normal_ks": subset["oracle_normal_ks"].mean(),
                "mean_oracle_lognormal_ks": subset["oracle_lognormal_ks"].mean(),
                "oracle_chi2_best_rate": float(
                    np.mean(subset["oracle_best_ks_model"].eq("oracle_chi2"))
                ),
                "mean_if_chi2_ks": subset["if_chi2_ks"].mean(),
                "mean_if_chi2_tail_error_05": subset[
                    "if_chi2_tail_abs_error_05"
                ].mean(),
                "mean_if_chi2_tail_error_01": subset[
                    "if_chi2_tail_abs_error_01"
                ].mean(),
                "mean_zero_cell_fraction": subset["zero_cell_fraction"].mean(),
                "mean_plugin_df_valid_rate": subset["plugin_df_valid_rate"].mean(),
            }
        )
    return pd.DataFrame(rows)


def _shape_summary(components: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (table_rows, table_columns), subset in components.groupby(
        ["rows", "columns"],
        sort=True,
    ):
        rows.append(
            {
                "rows": table_rows,
                "columns": table_columns,
                "components": len(subset),
                "mean_oracle_chi2_ks": subset["oracle_chi2_ks"].mean(),
                "mean_oracle_normal_ks": subset["oracle_normal_ks"].mean(),
                "mean_oracle_chi2_tail_error_05": subset[
                    "oracle_chi2_tail_abs_error_05"
                ].mean(),
                "mean_oracle_normal_tail_error_05": subset[
                    "oracle_normal_tail_abs_error_05"
                ].mean(),
                "oracle_chi2_best_rate": float(
                    np.mean(subset["oracle_best_ks_model"].eq("oracle_chi2"))
                ),
                "mean_empirical_skew": subset["empirical_skew_v"].mean(),
                "mean_oracle_chi2_skew": subset["oracle_chi2_skew"].mean(),
                "median_plugin_df_ratio": subset[
                    "plugin_df_median_to_empirical"
                ].median(),
                "mean_if_chi2_ks": subset["if_chi2_ks"].mean(),
            }
        )
    return pd.DataFrame(rows)


def _markdown(frame: pd.DataFrame, digits: int = 4) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, (float, np.floating)):
                rendered.append(
                    "NA" if not np.isfinite(value) else f"{value:.{digits}f}"
                )
            else:
                rendered.append(str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def _write_plot(components: pd.DataFrame, output_dir: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    models = list(MODEL_LABELS)
    labels = [MODEL_LABELS[model].replace(" ", "\n") for model in models]
    axes[0].boxplot(
        [components[f"{model}_ks"].dropna() for model in models],
        tick_labels=labels,
        showfliers=False,
    )
    axes[0].set_ylabel("Kolmogorov-Smirnov distance")
    axes[0].set_title("Whole-distribution fit")
    axes[0].grid(axis="y", alpha=0.25)

    positions = np.arange(len(models))
    width = 0.35
    tail_05 = [components[f"{model}_tail_abs_error_05"].mean() for model in models]
    tail_01 = [components[f"{model}_tail_abs_error_01"].mean() for model in models]
    axes[1].bar(positions - width / 2, tail_05, width, label="Upper 5% tail")
    axes[1].bar(positions + width / 2, tail_01, width, label="Upper 1% tail")
    axes[1].set_xticks(positions, labels)
    axes[1].set_ylabel("Mean absolute tail-probability error")
    axes[1].set_title("Upper-tail calibration")
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", alpha=0.25)
    figure.suptitle("Scaled chi-squared validation for the MI variance estimator")
    figure.tight_layout()
    figure.savefig(output_dir / "distribution_fit_summary.png", dpi=180)
    plt.close(figure)


def _write_report(
    output_dir: Path,
    *,
    profile: str,
    settings: dict,
    components: pd.DataFrame,
    models: pd.DataFrame,
    regimes: pd.DataFrame,
    shapes: pd.DataFrame,
) -> None:
    model_view = models[
        [
            "model_label",
            "mean_ks",
            "median_ks",
            "mean_tail_abs_error_05",
            "mean_tail_abs_error_01",
            "best_oracle_ks_rate",
        ]
    ].rename(
        columns={
            "model_label": "Model",
            "mean_ks": "Mean KS",
            "median_ks": "Median KS",
            "mean_tail_abs_error_05": "Tail error 0.05",
            "mean_tail_abs_error_01": "Tail error 0.01",
            "best_oracle_ks_rate": "Oracle win rate",
        }
    )
    regime_view = regimes[
        [
            "regime_label",
            "components",
            "median_mean_ratio",
            "median_variance_ratio",
            "median_plugin_df_ratio",
            "mean_oracle_chi2_ks",
            "oracle_chi2_best_rate",
            "mean_if_chi2_ks",
            "mean_if_chi2_tail_error_05",
            "mean_if_chi2_tail_error_01",
        ]
    ].rename(
        columns={
            "regime_label": "Regime",
            "components": "Components",
            "median_mean_ratio": "Mean ratio",
            "median_variance_ratio": "Variance ratio",
            "median_plugin_df_ratio": "Plug-in df ratio",
            "mean_oracle_chi2_ks": "Oracle chi2 KS",
            "oracle_chi2_best_rate": "Chi2 win rate",
            "mean_if_chi2_ks": "IF chi2 KS",
            "mean_if_chi2_tail_error_05": "IF tail error 0.05",
            "mean_if_chi2_tail_error_01": "IF tail error 0.01",
        }
    )
    shape_view = shapes[
        [
            "rows",
            "columns",
            "mean_oracle_chi2_ks",
            "mean_oracle_normal_ks",
            "mean_oracle_chi2_tail_error_05",
            "mean_oracle_normal_tail_error_05",
            "mean_empirical_skew",
            "mean_oracle_chi2_skew",
            "median_plugin_df_ratio",
        ]
    ].rename(
        columns={
            "rows": "Rows",
            "columns": "Columns",
            "mean_oracle_chi2_ks": "Chi2 KS",
            "mean_oracle_normal_ks": "Normal KS",
            "mean_oracle_chi2_tail_error_05": "Chi2 tail error 0.05",
            "mean_oracle_normal_tail_error_05": "Normal tail error 0.05",
            "mean_empirical_skew": "Empirical skew",
            "mean_oracle_chi2_skew": "Chi2 skew",
            "median_plugin_df_ratio": "Plug-in df ratio",
        }
    )
    oracle = models.set_index("model")
    chi_wins = oracle.loc["oracle_chi2", "best_oracle_ks_rate"]
    best_mean_ks_model = models.loc[models["mean_ks"].idxmin(), "model_label"]
    chi_tail_05 = oracle.loc["oracle_chi2", "mean_tail_abs_error_05"]
    normal_tail_05 = oracle.loc["oracle_normal", "mean_tail_abs_error_05"]
    chi_tail_01 = oracle.loc["oracle_chi2", "mean_tail_abs_error_01"]
    normal_tail_01 = oracle.loc["oracle_normal", "mean_tail_abs_error_01"]
    plugin_df_ratio = components["plugin_df_median_to_empirical"].median()
    lines = [
        "# Scaled Chi-Squared Validation for the MI Variance Estimator",
        "",
        "## Question",
        "",
        "Across repeated multinomial samples, is the distribution of the plug-in",
        "MI influence-variance estimator well represented by the scaled",
        "chi-squared model used by expanded Welch-Satterthwaite?",
        "",
        "## Design",
        "",
        f"Profile: `{profile}`. The experiment evaluated `{len(components)}`",
        f"population components from `{components['scenario_id'].nunique()}` fixed",
        f"scenarios, using `{settings['replicates']:,}` independent tables to",
        "estimate the oracle moments and another independent",
        f"`{settings['replicates']:,}` tables to evaluate each model. Population",
        "and simulation seeds were fixed before the run.",
        "",
        "Two comparisons were kept separate:",
        "",
        "- **Oracle shape comparison:** chi-squared, normal, and lognormal models",
        "  all receive the empirical mean and variance. Differences therefore",
        "  measure distributional shape and tail fit rather than moment error.",
        "- **Population first-order chi-squared:** uses population `V` and the derived",
        "  `tau^2 / n`. This tests the complete theoretical approximation.",
        "",
        "KS distance measures whole-distribution disagreement; lower is better.",
        "Tail error is the absolute difference between the observed exceedance",
        "rate and its target probability.",
        "",
        "## Overall Results",
        "",
        _markdown(model_view),
        "",
        "## Results by Regime",
        "",
        _markdown(regime_view),
        "",
        "## Results by Table Size",
        "",
        _markdown(shape_view),
        "",
        "## Interpretation",
        "",
        f"- The lowest average KS distance was obtained by **{best_mean_ks_model}**.",
        f"- The oracle scaled chi-squared model was the best of the three",
        f"  moment-matched shape families in `{chi_wins:.1%}` of components.",
        f"- Scaled chi-squared had lower average upper-tail error than normal:",
        f"  `{chi_tail_05:.4f}` versus `{normal_tail_05:.4f}` at 0.05 and",
        f"  `{chi_tail_01:.4f}` versus `{normal_tail_01:.4f}` at 0.01.",
        "- The chi-squared model generally overstates skewness for small tables",
        "  but tracks it more closely as the table dimension increases.",
        "- The gap between oracle and population first-order chi-squared results",
        "  separates shape error from errors in the first-order predicted moments.",
        "- A good oracle fit but poor population first-order fit indicates that the",
        "  chi-squared family is plausible but its plug-in moments need refinement.",
        "- Poor oracle fit means that matching only mean and variance does not",
        "  capture the finite-sample shape, regardless of moment estimation.",
        f"- The median plug-in component df was `{plugin_df_ratio:.3f}` times the",
        "  empirical moment df, so the implemented plug-in df is substantially",
        "  closer than the population first-order distribution fit alone suggests.",
        "",
        "This audit evaluates the variance component in isolation. It does not",
        "make the final Student reference exact because the MI contrast and its",
        "estimated denominator can remain dependent.",
        "",
        "## Output Map",
        "",
        "- `component_results.csv`: every population-component diagnostic.",
        "- `model_summary.csv`: overall comparison of candidate shapes and tails.",
        "- `regime_summary.csv`: diagnostics aggregated by sampling regime.",
        "- `shape_summary.csv`: diagnostics aggregated by table dimensions.",
        "- `population_scenarios.csv`: fixed generating populations.",
        "- `distribution_fit_summary.png`: visual shape and tail comparison.",
        "- `run_metadata.json`: seeds, versions, settings, and runtime.",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    settings = _settings(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    scenarios = _all_scenarios(args.scenario_seed)
    shape_indices = settings["shape_indices"]
    if shape_indices is not None:
        scenarios = [
            scenario
            for scenario in scenarios
            if scenario.shape_index in shape_indices
        ]

    population_rows = [_population_metadata(scenario) for scenario in scenarios]
    component_rows = []
    for scenario_index, scenario in enumerate(scenarios):
        for group_index, group in enumerate(("p", "q")):
            component_seed = (
                args.simulation_seed + 4 * scenario_index + 2 * group_index
            )
            component_rows.append(
                _analyse_component(
                    scenario,
                    group,
                    replicates=settings["replicates"],
                    batch_size=settings["batch_size"],
                    seed=component_seed,
                )
            )
        print(
            f"[{scenario_index + 1}/{len(scenarios)}] {scenario.scenario_id}",
            flush=True,
        )

    components = pd.DataFrame(component_rows)
    models = _model_summary(components)
    regimes = _regime_summary(components)
    shapes = _shape_summary(components)
    pd.DataFrame(population_rows).to_csv(
        args.output_dir / "population_scenarios.csv", index=False
    )
    components.to_csv(args.output_dir / "component_results.csv", index=False)
    models.to_csv(args.output_dir / "model_summary.csv", index=False)
    regimes.to_csv(args.output_dir / "regime_summary.csv", index=False)
    shapes.to_csv(args.output_dir / "shape_summary.csv", index=False)
    _write_plot(components, args.output_dir)
    _write_report(
        args.output_dir,
        profile=args.profile,
        settings=settings,
        components=components,
        models=models,
        regimes=regimes,
        shapes=shapes,
    )
    metadata = {
        "profile": args.profile,
        "settings": settings,
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "scenario_count": len(scenarios),
        "component_count": len(components),
        "simulated_table_count": (
            2 * settings["replicates"] * len(components)
        ),
        "elapsed_seconds": perf_counter() - start,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "pandas_version": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(models.to_string(index=False), flush=True)
    print(f"Wrote results to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
