#!/usr/bin/env python3
"""Evaluate joint-influence Edgeworth corrections on the 16-config design."""

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

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.statistics import plugin_mi  # noqa: E402
from welch_differential_mi import joint_influence_pvalues  # noqa: E402

from run_supervisor_experiment import (  # noqa: E402
    DEFAULT_SCENARIO_SEED,
    DEFAULT_SIMULATION_SEED,
    DESIGN_TO_REGIME,
    REGIMES,
    generate_configuration_scenarios,
    _scenario_simulation_seeds,
)


ALPHAS = (0.10, 0.05, 0.01)
CALIBRATION_ALPHAS = np.linspace(0.0, 0.10, 101)
METHODS = {
    "normal_wald": ("Normal Wald", "normal_p_value", "base_valid"),
    "simple_welch": ("Simple Welch", "welch_p_value", "simple_valid"),
    "expanded_welch": (
        "Expanded Welch",
        "expanded_welch_p_value",
        "expanded_valid",
    ),
    "edgeworth_normal": (
        "Joint Edgeworth",
        "edgeworth_normal_p_value",
        "edgeworth_valid",
    ),
    "joint_influence_welch": (
        "Joint-Influence Welch",
        "joint_influence_welch_p_value",
        "joint_influence_welch_valid",
    ),
}
METHOD_COLORS = {
    "normal_wald": "#2f6f9f",
    "simple_welch": "#8a7f2d",
    "expanded_welch": "#c34a36",
    "edgeworth_normal": "#64748b",
    "joint_influence_welch": "#16836b",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=5_000)
    parser.add_argument("--population-replicates", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=1_000)
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "joint_influence_16_config",
    )
    return parser.parse_args()


def _simulate_scenario(
    scenario,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> tuple[list[dict], np.ndarray]:
    rng = np.random.default_rng(seed)
    method_names = tuple(METHODS)
    p_values = np.full((len(method_names), replicates), np.nan, dtype=float)
    delta_values = np.full(replicates, np.nan, dtype=float)
    standard_errors = np.full(replicates, np.nan, dtype=float)
    skewness = np.full(replicates, np.nan, dtype=float)
    covariance = np.full(replicates, np.nan, dtype=float)
    adjustment = np.full(replicates, np.nan, dtype=float)

    for start in range(0, replicates, batch_size):
        count = min(batch_size, replicates - start)
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.ravel(),
            size=count,
        ).reshape(count, scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_q.ravel(),
            size=count,
        ).reshape(count, scenario.rows, scenario.columns)
        values = joint_influence_pvalues(table_p, table_q)
        delta_values[start : start + count] = values["delta_corrected"]
        standard_errors[start : start + count] = values["standard_error"]
        skewness[start : start + count] = values[
            "standardized_third_cumulant"
        ]
        covariance[start : start + count] = values[
            "studentization_covariance"
        ]
        adjustment[start : start + count] = values["edgeworth_adjustment"]
        for method_index, (_, p_key, _) in enumerate(METHODS.values()):
            p_values[method_index, start : start + count] = values[p_key]

    true_delta = float(
        plugin_mi(scenario.probability_p)
        - plugin_mi(scenario.probability_q)
    )
    estimator_valid = np.isfinite(delta_values) & np.isfinite(standard_errors)
    common = {
        "scenario_id": scenario.scenario_id,
        "configuration_id": scenario.configuration_id,
        "rows": scenario.rows,
        "columns": scenario.columns,
        "condition": DESIGN_TO_REGIME[scenario.design_index],
        "condition_label": REGIMES[
            DESIGN_TO_REGIME[scenario.design_index]
        ]["label"],
        "n_p": scenario.n_p,
        "n_q": scenario.n_q,
        "population_replication": scenario.population_replication,
        "target_mi": scenario.target_mi,
        "true_delta": true_delta,
        "simulation_seed": seed,
        "replicates": replicates,
        "mean_delta_error": float(
            np.mean(delta_values[estimator_valid] - true_delta)
        ),
        "empirical_delta_sd": float(
            np.std(delta_values[estimator_valid], ddof=1)
        ),
        "mean_standard_error": float(np.mean(standard_errors[estimator_valid])),
        "mean_standardized_third_cumulant": float(np.nanmean(skewness)),
        "mean_studentization_covariance": float(np.nanmean(covariance)),
        "mean_absolute_edgeworth_adjustment": float(
            np.nanmean(np.abs(adjustment))
        ),
    }
    rows = []
    for method_index, (method, (label, _, _)) in enumerate(METHODS.items()):
        method_p = p_values[method_index]
        valid = np.isfinite(method_p)
        row = {
            **common,
            "method": method,
            "method_label": label,
            "valid_replicates": int(np.count_nonzero(valid)),
            "valid_rate": float(np.mean(valid)),
        }
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            row[f"fpr_{suffix}"] = (
                float(np.mean(method_p[valid] <= alpha))
                if np.any(valid)
                else np.nan
            )
        rows.append(row)
    return rows, p_values


def _aggregate(
    scenario_results: pd.DataFrame,
    group_columns: list[str],
) -> pd.DataFrame:
    rows = []
    for keys, group in scenario_results.groupby(
        [*group_columns, "method", "method_label"],
        sort=False,
    ):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip([*group_columns, "method", "method_label"], keys))
        row["population_pairs"] = len(group)
        row["mean_valid_rate"] = float(group["valid_rate"].mean())
        row["mean_delta_error"] = float(group["mean_delta_error"].mean())
        row["mean_empirical_delta_sd"] = float(
            group["empirical_delta_sd"].mean()
        )
        row["mean_standard_error"] = float(group["mean_standard_error"].mean())
        row["mean_absolute_edgeworth_adjustment"] = float(
            group["mean_absolute_edgeworth_adjustment"].mean()
        )
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            values = group[f"fpr_{suffix}"].to_numpy()
            row[f"mean_fpr_{suffix}"] = float(np.mean(values))
            row[f"mean_absolute_fpr_error_{suffix}"] = float(
                np.mean(np.abs(values - alpha))
            )
            row[f"population_sd_fpr_{suffix}"] = float(
                np.std(values, ddof=1)
            )
        rows.append(row)
    return pd.DataFrame(rows)


def _overall_summary(configuration_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method, group in configuration_summary.groupby("method", sort=False):
        row = {
            "method": method,
            "method_label": group["method_label"].iloc[0],
            "configurations": len(group),
            "mean_valid_rate": float(group["mean_valid_rate"].mean()),
        }
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            errors = np.abs(group[f"mean_fpr_{suffix}"] - alpha)
            row[f"mean_fpr_{suffix}"] = float(
                group[f"mean_fpr_{suffix}"].mean()
            )
            row[f"configuration_mae_{suffix}"] = float(errors.mean())
            row[f"configurations_closer_than_normal_{suffix}"] = 0
        rows.append(row)
    result = pd.DataFrame(rows)
    normal = configuration_summary[
        configuration_summary["method"] == "normal_wald"
    ].set_index("configuration_id")
    for row_index, row in result.iterrows():
        candidate = configuration_summary[
            configuration_summary["method"] == row["method"]
        ].set_index("configuration_id")
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            candidate_error = np.abs(candidate[f"mean_fpr_{suffix}"] - alpha)
            normal_error = np.abs(normal[f"mean_fpr_{suffix}"] - alpha)
            result.loc[
                row_index,
                f"configurations_closer_than_normal_{suffix}",
            ] = int(np.count_nonzero(candidate_error < normal_error))
    return result


def _calibration_summary(
    p_values: np.ndarray,
    scenarios,
) -> pd.DataFrame:
    rows = []
    for method_index, (method, (label, _, _)) in enumerate(METHODS.items()):
        for condition in REGIMES:
            scenario_indices = [
                index
                for index, scenario in enumerate(scenarios)
                if DESIGN_TO_REGIME[scenario.design_index] == condition
            ]
            rates = []
            for index in scenario_indices:
                values = p_values[index, method_index]
                values = values[np.isfinite(values)]
                rates.append(
                    np.array(
                        [np.mean(values <= alpha) for alpha in CALIBRATION_ALPHAS]
                    )
                    if values.size
                    else np.full(len(CALIBRATION_ALPHAS), np.nan)
                )
            stacked_rates = np.asarray(rates)
            valid_counts = np.count_nonzero(np.isfinite(stacked_rates), axis=0)
            mean_rates = np.divide(
                np.nansum(stacked_rates, axis=0),
                valid_counts,
                out=np.full(len(CALIBRATION_ALPHAS), np.nan),
                where=valid_counts > 0,
            )
            for alpha, rate in zip(CALIBRATION_ALPHAS, mean_rates):
                rows.append(
                    {
                        "condition": condition,
                        "condition_label": REGIMES[condition]["label"],
                        "method": method,
                        "method_label": label,
                        "nominal_alpha": alpha,
                        "actual_rejection_rate": rate,
                    }
                )
    return pd.DataFrame(rows)


def _plot_calibration(calibration: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), sharex=True, sharey=True)
    for axis, condition in zip(axes.ravel(), REGIMES):
        subset = calibration[calibration["condition"] == condition]
        axis.plot([0, 0.1], [0, 0.1], color="#9ca3af", linestyle="--")
        for method, (label, _, _) in METHODS.items():
            values = subset[subset["method"] == method]
            axis.plot(
                values["nominal_alpha"],
                values["actual_rejection_rate"],
                label=label,
                color=METHOD_COLORS[method],
                linewidth=1.8,
            )
        axis.set_title(REGIMES[condition]["label"])
        axis.grid(alpha=0.2)
    axes[1, 0].set_xlabel("Nominal alpha")
    axes[1, 1].set_xlabel("Nominal alpha")
    axes[0, 0].set_ylabel("Actual rejection rate")
    axes[1, 0].set_ylabel("Actual rejection rate")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.suptitle("Joint-influence rejection calibration")
    fig.tight_layout(rect=(0, 0.08, 1, 0.96))
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def _write_report(
    output_path: Path,
    overall: pd.DataFrame,
    configuration: pd.DataFrame,
) -> None:
    def markdown_table(frame: pd.DataFrame) -> str:
        headings = [str(column) for column in frame.columns]
        lines = [
            "| " + " | ".join(headings) + " |",
            "| " + " | ".join("---" for _ in headings) + " |",
        ]
        for values in frame.itertuples(index=False, name=None):
            cells = [
                f"{value:.6f}" if isinstance(value, (float, np.floating)) else str(value)
                for value in values
            ]
            lines.append("| " + " | ".join(cells) + " |")
        return "\n".join(lines)

    columns = [
        "method_label",
        "mean_valid_rate",
        "configuration_mae_10",
        "configuration_mae_05",
        "configuration_mae_01",
    ]
    best = overall.sort_values("configuration_mae_05").iloc[0]
    joint = overall[overall["method"] == "joint_influence_welch"].iloc[0]
    normal = overall[overall["method"] == "normal_wald"].iloc[0]
    expanded = overall[overall["method"] == "expanded_welch"].iloc[0]
    equal_sample = configuration[
        configuration["condition"] != "ultra_imbalanced"
    ]
    equal_mae = (
        equal_sample.assign(
            error=lambda frame: np.abs(frame["mean_fpr_05"] - 0.05)
        )
        .groupby("method_label")["error"]
        .mean()
        .sort_values()
    )
    text = [
        "# Joint-Influence Experiment",
        "",
        "This experiment reuses the 16 fixed configurations, ten population "
        "realizations per configuration, and the requested null replicate "
        "count. No configuration-specific tuning is used.",
        "",
        "## Overall calibration",
        "",
        markdown_table(overall[columns]),
        "",
        f"The lowest alpha=0.05 configuration MAE was produced by "
        f"**{best['method_label']}** ({best['configuration_mae_05']:.6f}).",
        f"Joint-Influence Welch changed MAE from "
        f"{expanded['configuration_mae_05']:.6f} for Expanded Welch and "
        f"{normal['configuration_mae_05']:.6f} for Normal Wald to "
        f"{joint['configuration_mae_05']:.6f}.",
        "",
        "## Equal-sample configurations",
        "",
        markdown_table(
            equal_mae.rename("alpha_05_mae")
            .rename_axis("method_label")
            .reset_index()
        ),
        "",
        "The Edgeworth methods report invalid results when their approximate "
        "CDF leaves [0,1]; these replicates are not silently clipped or routed "
        "to another method.",
    ]
    output_path.write_text("\n".join(text) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    if min(args.replicates, args.population_replicates, args.batch_size) <= 0:
        raise ValueError("Replicate and batch counts must be positive.")
    start_time = perf_counter()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = generate_configuration_scenarios(
        args.scenario_seed,
        args.population_replicates,
    )
    seeds = _scenario_simulation_seeds(scenarios, args.simulation_seed)
    all_rows = []
    p_value_archive = np.full(
        (len(scenarios), len(METHODS), args.replicates),
        np.nan,
        dtype=float,
    )
    for scenario_index, scenario in enumerate(scenarios):
        rows, p_values = _simulate_scenario(
            scenario,
            replicates=args.replicates,
            batch_size=args.batch_size,
            seed=seeds[scenario.scenario_id],
        )
        all_rows.extend(rows)
        p_value_archive[scenario_index] = p_values

    scenario_results = pd.DataFrame(all_rows)
    configuration_summary = _aggregate(
        scenario_results,
        ["configuration_id", "rows", "columns", "condition", "condition_label", "n_p", "n_q"],
    )
    regime_summary = _aggregate(
        scenario_results,
        ["condition", "condition_label"],
    )
    overall_summary = _overall_summary(configuration_summary)
    calibration = _calibration_summary(p_value_archive, scenarios)

    scenario_results.to_csv(args.output_dir / "scenario_results.csv", index=False)
    configuration_summary.to_csv(
        args.output_dir / "configuration_summary.csv",
        index=False,
    )
    regime_summary.to_csv(args.output_dir / "regime_summary.csv", index=False)
    overall_summary.to_csv(args.output_dir / "overall_summary.csv", index=False)
    calibration.to_csv(
        args.output_dir / "rejection_calibration.csv",
        index=False,
    )
    np.savez_compressed(
        args.output_dir / "null_pvalues.npz",
        p_values=p_value_archive,
        scenario_ids=np.asarray([scenario.scenario_id for scenario in scenarios]),
        methods=np.asarray(tuple(METHODS)),
    )
    _plot_calibration(calibration, args.output_dir / "rejection_calibration.png")
    _write_report(
        args.output_dir / "REPORT.md",
        overall_summary,
        configuration_summary,
    )
    metadata = {
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "configurations": 16,
        "population_replicates": args.population_replicates,
        "scenarios": len(scenarios),
        "null_replicates_per_scenario": args.replicates,
        "total_table_pairs": len(scenarios) * args.replicates,
        "batch_size": args.batch_size,
        "methods": list(METHODS),
        "elapsed_seconds": perf_counter() - start_time,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(overall_summary.to_string(index=False))
    print(f"Saved results to {args.output_dir}")


if __name__ == "__main__":
    main()
