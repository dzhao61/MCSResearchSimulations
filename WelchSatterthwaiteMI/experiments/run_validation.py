#!/usr/bin/env python3
"""Run the pre-specified Welch-Satterthwaite differential-MI validation."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from dataclasses import replace
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest, norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.inference import analytic_wald_test, compare_tables
from differential_mi.random_validation import (
    RandomScenario,
    generate_random_scenarios,
    scenario_diagnostics,
)
from differential_mi.scenarios import (
    build_distributions,
    power_curve_scenarios,
)
from welch_differential_mi import (
    differential_mi_pvalues,
    welch_satterthwaite_test,
)


METHOD_COLUMNS = {
    "wald_normal": "normal_p_value",
    "welch_reference": "welch_p_value",
    "welch_unbiased": "unbiased_welch_p_value",
}
HARD_IDS = (
    "random_2x2_d5",
    "random_2x5_d5",
    "random_3x7_d5",
    "random_4x6_d5",
    "random_5x5_d5",
    "random_5x10_d5",
)
SCENARIO_SEEDS = (2026072501, 2026072601)
SIMULATION_SEED = 2026072801
STRESS_CONFIGS = (
    ("random_2x2_d0", 20, 20),
    ("random_2x2_d0", 30, 30),
    ("random_2x2_d0", 50, 50),
    ("random_2x2_d0", 100, 100),
    ("random_2x5_d5", 30, 120),
    ("random_2x5_d5", 50, 200),
    ("random_2x5_d5", 100, 400),
    ("random_3x3_d2", 30, 120),
    ("random_3x3_d2", 50, 200),
    ("random_3x3_d2", 100, 400),
    ("random_4x6_d5", 50, 200),
    ("random_4x6_d5", 100, 400),
    ("random_4x6_d5", 200, 800),
)
PROFILE_SETTINGS = {
    "smoke": {
        "broad_replicates": 200,
        "hard_replicates": 500,
        "stress_replicates": 500,
        "power_replicates": 500,
        "permutation_replicates": 20,
        "scenario_seeds": SCENARIO_SEEDS[:1],
        "broad_limit": 8,
        "hard_limit": 2,
        "stress_limit": 4,
    },
    "decisive": {
        "broad_replicates": 5_000,
        "hard_replicates": 20_000,
        "stress_replicates": 10_000,
        "power_replicates": 10_000,
        "permutation_replicates": 1_000,
        "scenario_seeds": SCENARIO_SEEDS,
        "broad_limit": None,
        "hard_limit": None,
        "stress_limit": None,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=PROFILE_SETTINGS, default="smoke")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--simulation-seed", type=int, default=SIMULATION_SEED)
    parser.add_argument("--broad-replicates", type=int)
    parser.add_argument("--hard-replicates", type=int)
    parser.add_argument("--stress-replicates", type=int)
    parser.add_argument("--power-replicates", type=int)
    parser.add_argument("--permutation-replicates", type=int)
    parser.add_argument("--permutations", type=int, default=999)
    return parser.parse_args()


def _settings(args: argparse.Namespace) -> dict:
    result = dict(PROFILE_SETTINGS[args.profile])
    for name in (
        "broad_replicates",
        "hard_replicates",
        "stress_replicates",
        "power_replicates",
        "permutation_replicates",
    ):
        value = getattr(args, name)
        if value is not None:
            result[name] = value
    return result


def _scenario_entries(settings: dict) -> dict[str, list[tuple[int, RandomScenario]]]:
    broad: list[tuple[int, RandomScenario]] = []
    hard: list[tuple[int, RandomScenario]] = []
    stress: list[tuple[int, RandomScenario]] = []
    hard_ids = set(HARD_IDS)
    for scenario_seed in settings["scenario_seeds"]:
        scenarios = generate_random_scenarios(scenario_seed)
        by_id = {scenario.scenario_id: scenario for scenario in scenarios}
        broad.extend((scenario_seed, scenario) for scenario in scenarios)
        hard.extend(
            (scenario_seed, scenario)
            for scenario in scenarios
            if scenario.scenario_id in hard_ids
        )
        for source_id, n_p, n_q in STRESS_CONFIGS:
            source = by_id[source_id]
            stress_scenario = replace(
                source,
                scenario_id=f"stress_{source_id}_n{n_p}_{n_q}",
                n_p=n_p,
                n_q=n_q,
            )
            stress.append((scenario_seed, stress_scenario))
    if settings["broad_limit"] is not None:
        broad = broad[: settings["broad_limit"]]
    if settings["hard_limit"] is not None:
        hard = hard[: settings["hard_limit"]]
    if settings["stress_limit"] is not None:
        stress = stress[: settings["stress_limit"]]
    return {"broad": broad, "hard": hard, "stress": stress}


def _sample_diagnostics(tables: np.ndarray) -> dict[str, np.ndarray]:
    counts = np.asarray(tables, dtype=float)
    totals = counts.sum(axis=(1, 2))
    row = counts.sum(axis=2)
    column = counts.sum(axis=1)
    expected = row[:, :, None] * column[:, None, :] / totals[:, None, None]
    return {
        "zero_fraction": np.mean(counts == 0, axis=(1, 2)),
        "expected_below_1": np.mean(expected < 1.0, axis=(1, 2)),
        "expected_below_5": np.mean(expected < 5.0, axis=(1, 2)),
        "minimum_expected": expected.min(axis=(1, 2)),
    }


def _scenario_metadata(
    stage: str,
    scenario_seed: int,
    scenario: RandomScenario,
) -> dict:
    row = scenario_diagnostics(scenario)
    row.update(
        {
            "stage": stage,
            "scenario_seed": scenario_seed,
            "scenario_key": (
                f"{stage}:{scenario_seed}:{scenario.scenario_id}"
            ),
            "probability_p_json": json.dumps(scenario.probability_p.tolist()),
            "probability_q_json": json.dumps(scenario.probability_q.tolist()),
        }
    )
    return row


def _simulate_null(
    stage: str,
    scenario_seed: int,
    scenario: RandomScenario,
    *,
    replicates: int,
    simulation_seed: int,
    permutation_replicates: int,
    permutations: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    rng = np.random.default_rng(simulation_seed)
    table_p = rng.multinomial(
        scenario.n_p,
        scenario.probability_p.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    table_q = rng.multinomial(
        scenario.n_q,
        scenario.probability_q.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)

    start = perf_counter()
    values = differential_mi_pvalues(table_p, table_q)
    batch_seconds = perf_counter() - start
    diagnostics_p = _sample_diagnostics(table_p)
    diagnostics_q = _sample_diagnostics(table_q)
    normal_critical = norm.ppf(0.975)
    welch_critical = t.ppf(
        0.975,
        df=values["welch_degrees_of_freedom"],
    )
    unbiased_critical = t.ppf(
        0.975,
        df=values["unbiased_welch_degrees_of_freedom"],
    )

    frame = pd.DataFrame(
        {
            "stage": stage,
            "scenario_seed": scenario_seed,
            "scenario_id": scenario.scenario_id,
            "scenario_key": f"{stage}:{scenario_seed}:{scenario.scenario_id}",
            "replicate": np.arange(replicates),
            "simulation_seed": simulation_seed,
            "true_delta": scenario_diagnostics(scenario)["true_delta"],
            "delta_corrected": values["delta_corrected"],
            "standard_error": values["standard_error"],
            "statistic": values["statistic"],
            "normal_p_value": values["normal_p_value"],
            "welch_degrees_of_freedom": values["welch_degrees_of_freedom"],
            "welch_p_value": values["welch_p_value"],
            "unbiased_standard_error": values["unbiased_standard_error"],
            "unbiased_statistic": values["unbiased_statistic"],
            "unbiased_welch_degrees_of_freedom": values[
                "unbiased_welch_degrees_of_freedom"
            ],
            "unbiased_welch_p_value": values["unbiased_welch_p_value"],
            "valid": values["valid"],
            "normal_coverage_95": (
                np.abs(values["delta_corrected"])
                <= normal_critical * values["standard_error"]
            ),
            "welch_coverage_95": (
                np.abs(values["delta_corrected"])
                <= welch_critical * values["standard_error"]
            ),
            "unbiased_welch_coverage_95": (
                np.abs(values["delta_corrected"])
                <= unbiased_critical * values["unbiased_standard_error"]
            ),
            "zero_fraction_p": diagnostics_p["zero_fraction"],
            "zero_fraction_q": diagnostics_q["zero_fraction"],
            "expected_below_1_p": diagnostics_p["expected_below_1"],
            "expected_below_1_q": diagnostics_q["expected_below_1"],
            "expected_below_5_p": diagnostics_p["expected_below_5"],
            "expected_below_5_q": diagnostics_q["expected_below_5"],
            "minimum_expected_p": diagnostics_p["minimum_expected"],
            "minimum_expected_q": diagnostics_q["minimum_expected"],
        }
    )

    permutation_rows = []
    permutation_count = min(permutation_replicates, replicates)
    for replicate in range(permutation_count):
        permutation_rng = np.random.default_rng(
            np.random.SeedSequence(
                [simulation_seed, replicate, 8171]
            )
        )
        result = compare_tables(
            table_p[replicate],
            table_q[replicate],
            permutations=permutations,
            rng=permutation_rng,
        )
        permutation_rows.append(
            {
                "stage": stage,
                "scenario_seed": scenario_seed,
                "scenario_id": scenario.scenario_id,
                "scenario_key": (
                    f"{stage}:{scenario_seed}:{scenario.scenario_id}"
                ),
                "replicate": replicate,
                "normal_p_value": values["normal_p_value"][replicate],
                "welch_p_value": values["welch_p_value"][replicate],
                "unbiased_welch_p_value": values[
                    "unbiased_welch_p_value"
                ][replicate],
                "student_perm_analytic_p_value": (
                    result.student_perm_analytic_p
                ),
                "permutation_seconds": result.permutation_seconds,
                "permutations": permutations,
            }
        )
    run_diagnostics = {
        "stage": stage,
        "scenario_seed": scenario_seed,
        "scenario_id": scenario.scenario_id,
        "scenario_key": f"{stage}:{scenario_seed}:{scenario.scenario_id}",
        "replicates": replicates,
        "batch_seconds": batch_seconds,
        "batch_microseconds_per_pair": 1e6 * batch_seconds / replicates,
    }
    return frame, pd.DataFrame(permutation_rows), run_diagnostics


def _simulate_power(
    scenario,
    *,
    replicates: int,
    simulation_seed: int,
) -> tuple[pd.DataFrame, dict]:
    probability_p, probability_q, diagnostics = build_distributions(scenario)
    rng = np.random.default_rng(simulation_seed)
    table_p = rng.multinomial(
        scenario.n_p,
        probability_p.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    table_q = rng.multinomial(
        scenario.n_q,
        probability_q.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    values = differential_mi_pvalues(table_p, table_q)
    true_delta = diagnostics["true_delta"]
    normal_critical = norm.ppf(0.975)
    welch_critical = t.ppf(
        0.975,
        df=values["welch_degrees_of_freedom"],
    )
    unbiased_critical = t.ppf(
        0.975,
        df=values["unbiased_welch_degrees_of_freedom"],
    )
    frame = pd.DataFrame(
        {
            "stage": "power",
            "scenario_seed": simulation_seed,
            "scenario_id": scenario.scenario_id,
            "scenario_key": f"power:{scenario.scenario_id}",
            "replicate": np.arange(replicates),
            "true_delta": true_delta,
            "delta_corrected": values["delta_corrected"],
            "standard_error": values["standard_error"],
            "normal_p_value": values["normal_p_value"],
            "welch_degrees_of_freedom": values["welch_degrees_of_freedom"],
            "welch_p_value": values["welch_p_value"],
            "unbiased_standard_error": values["unbiased_standard_error"],
            "unbiased_welch_degrees_of_freedom": values[
                "unbiased_welch_degrees_of_freedom"
            ],
            "unbiased_welch_p_value": values["unbiased_welch_p_value"],
            "valid": values["valid"],
            "normal_coverage_95": (
                np.abs(values["delta_corrected"] - true_delta)
                <= normal_critical * values["standard_error"]
            ),
            "welch_coverage_95": (
                np.abs(values["delta_corrected"] - true_delta)
                <= welch_critical * values["standard_error"]
            ),
            "unbiased_welch_coverage_95": (
                np.abs(values["delta_corrected"] - true_delta)
                <= unbiased_critical * values["unbiased_standard_error"]
            ),
        }
    )
    metadata = scenario.to_dict()
    metadata.update(diagnostics)
    metadata.update(
        {
            "stage": "power",
            "scenario_seed": simulation_seed,
            "scenario_key": f"power:{scenario.scenario_id}",
            "probability_p_json": json.dumps(probability_p.tolist()),
            "probability_q_json": json.dumps(probability_q.tolist()),
        }
    )
    return frame, metadata


def _wilson(rejections: int, total: int) -> tuple[float, float]:
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    return float(interval.low), float(interval.high)


def _summarize_null(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scenario_key, group in frame.groupby("scenario_key", sort=False):
        valid = group["valid"]
        row = {
            "stage": group["stage"].iloc[0],
            "scenario_seed": int(group["scenario_seed"].iloc[0]),
            "scenario_id": group["scenario_id"].iloc[0],
            "scenario_key": scenario_key,
            "replicates": len(group),
            "valid_rate": float(valid.mean()),
            "mean_zero_fraction_p": float(group["zero_fraction_p"].mean()),
            "mean_zero_fraction_q": float(group["zero_fraction_q"].mean()),
            "mean_expected_below_1_p": float(group["expected_below_1_p"].mean()),
            "mean_expected_below_1_q": float(group["expected_below_1_q"].mean()),
            "mean_expected_below_5_p": float(group["expected_below_5_p"].mean()),
            "mean_expected_below_5_q": float(group["expected_below_5_q"].mean()),
            "median_welch_df": float(
                group.loc[valid, "welch_degrees_of_freedom"].median()
            ),
            "p05_welch_df": float(
                group.loc[valid, "welch_degrees_of_freedom"].quantile(0.05)
            ),
            "minimum_welch_df": float(
                group.loc[valid, "welch_degrees_of_freedom"].min()
            ),
        }
        for method, column in METHOD_COLUMNS.items():
            values = group.loc[valid, column]
            for alpha_label, alpha in (("10", 0.10), ("05", 0.05)):
                rejections = int((values <= alpha).sum())
                rate = rejections / len(values) if len(values) else float("nan")
                low, high = (
                    _wilson(rejections, len(values))
                    if len(values)
                    else (float("nan"), float("nan"))
                )
                row[f"{method}_fpr_{alpha_label}"] = rate
                row[f"{method}_fpr_{alpha_label}_low"] = low
                row[f"{method}_fpr_{alpha_label}_high"] = high
            coverage_column = {
                "wald_normal": "normal_coverage_95",
                "welch_reference": "welch_coverage_95",
                "welch_unbiased": "unbiased_welch_coverage_95",
            }[method]
            row[f"{method}_coverage_95"] = float(
                group.loc[valid, coverage_column].mean()
            )
        rows.append(row)
    return pd.DataFrame(rows)


def _aggregate_null(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for stage, group in summary.groupby("stage", sort=False):
        for method in METHOD_COLUMNS:
            row = {
                "stage": stage,
                "method": method,
                "scenarios": len(group),
                "mean_valid_rate": float(group["valid_rate"].mean()),
                "mean_coverage_95": float(
                    group[f"{method}_coverage_95"].mean()
                ),
            }
            for alpha_label, alpha in (("10", 0.10), ("05", 0.05)):
                rates = group[f"{method}_fpr_{alpha_label}"]
                row[f"mean_fpr_{alpha_label}"] = float(rates.mean())
                row[f"mean_absolute_fpr_error_{alpha_label}"] = float(
                    np.mean(np.abs(rates - alpha))
                )
                row[f"minimum_fpr_{alpha_label}"] = float(rates.min())
                row[f"maximum_fpr_{alpha_label}"] = float(rates.max())
            row["within_035_065"] = float(
                group[f"{method}_fpr_05"].between(0.035, 0.065).mean()
            )
            rows.append(row)
    return pd.DataFrame(rows)


def _summarize_power(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scenario_key, group in frame.groupby("scenario_key", sort=False):
        valid = group["valid"]
        for method, column in METHOD_COLUMNS.items():
            coverage_column = {
                "wald_normal": "normal_coverage_95",
                "welch_reference": "welch_coverage_95",
                "welch_unbiased": "unbiased_welch_coverage_95",
            }[method]
            rows.append(
                {
                    "scenario_key": scenario_key,
                    "scenario_id": group["scenario_id"].iloc[0],
                    "method": method,
                    "replicates": int(valid.sum()),
                    "valid_rate": float(valid.mean()),
                    "true_delta": float(group["true_delta"].iloc[0]),
                    "power_05": float(
                        (group.loc[valid, column] <= 0.05).mean()
                    ),
                    "coverage_95": float(
                        group.loc[valid, coverage_column].mean()
                    ),
                    "median_welch_df": float(
                        group.loc[valid, "welch_degrees_of_freedom"].median()
                    ),
                }
            )
    return pd.DataFrame(rows)


def _summarize_permutation(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    method_columns = {
        **METHOD_COLUMNS,
        "student_perm_analytic": "student_perm_analytic_p_value",
    }
    rows = []
    for scenario_key, group in frame.groupby("scenario_key", sort=False):
        row = {
            "scenario_key": scenario_key,
            "scenario_seed": int(group["scenario_seed"].iloc[0]),
            "scenario_id": group["scenario_id"].iloc[0],
            "replicates": len(group),
            "permutations": int(group["permutations"].iloc[0]),
            "mean_permutation_ms": 1000.0
            * float(group["permutation_seconds"].mean()),
        }
        for method, column in method_columns.items():
            for alpha_label, alpha in (("10", 0.10), ("05", 0.05)):
                row[f"{method}_fpr_{alpha_label}"] = float(
                    (group[column] <= alpha).mean()
                )
        rows.append(row)
    return pd.DataFrame(rows)


def _runtime_audit(
    entries: list[tuple[int, RandomScenario]],
    *,
    repetitions: int,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    selected = entries[: min(12, len(entries))]
    for scenario_seed, scenario in selected:
        table_p = rng.multinomial(
            scenario.n_p, scenario.probability_p.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q, scenario.probability_q.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)
        analytic_wald_test(table_p, table_q)
        welch_satterthwaite_test(table_p, table_q)
        normal_times = []
        welch_times = []
        for _ in range(repetitions):
            start = perf_counter()
            analytic_wald_test(table_p, table_q)
            normal_times.append(perf_counter() - start)
            start = perf_counter()
            welch_satterthwaite_test(table_p, table_q)
            welch_times.append(perf_counter() - start)
        rows.append(
            {
                "scenario_seed": scenario_seed,
                "scenario_id": scenario.scenario_id,
                "rows": scenario.rows,
                "columns": scenario.columns,
                "repetitions": repetitions,
                "median_normal_ms": 1000.0 * float(np.median(normal_times)),
                "median_welch_ms": 1000.0 * float(np.median(welch_times)),
                "welch_over_normal": float(
                    np.median(welch_times) / np.median(normal_times)
                ),
            }
        )
    return pd.DataFrame(rows)


def _markdown(frame: pd.DataFrame, digits: int = 5) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, (float, np.floating)):
                rendered.append(f"{value:.{digits}f}")
            else:
                rendered.append(str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def _plot_results(
    null_summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    hard = null_summary[null_summary["stage"] == "hard"].copy()
    x = np.arange(len(hard))
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    width = 0.25
    for index, method in enumerate(METHOD_COLUMNS):
        axes[0].bar(
            x + (index - 1) * width,
            hard[f"{method}_fpr_05"],
            width,
            label=method,
        )
    axes[0].axhline(0.05, color="black", linestyle="--")
    axes[0].axhspan(0.035, 0.065, color="grey", alpha=0.12)
    axes[0].set_xticks(x, hard["scenario_id"], rotation=55, ha="right")
    axes[0].set_ylabel("False-positive rate at alpha=0.05")
    axes[0].set_title("Targeted hard weak-null grid")
    axes[0].legend()

    broad = null_summary[null_summary["stage"] == "broad"]
    axes[1].scatter(
        broad["wald_normal_fpr_05"],
        broad["welch_reference_fpr_05"],
        s=18,
        alpha=0.65,
    )
    limits = [0.025, max(0.085, float(broad["wald_normal_fpr_05"].max()) + 0.005)]
    axes[1].plot(limits, limits, color="black", linestyle="--")
    axes[1].axhline(0.05, color="grey", linewidth=1)
    axes[1].axvline(0.05, color="grey", linewidth=1)
    axes[1].set_xlim(limits)
    axes[1].set_ylim(limits)
    axes[1].set_xlabel("Normal-Wald FPR")
    axes[1].set_ylabel("Welch-reference FPR")
    axes[1].set_title("Broad-grid paired calibration")
    fig.tight_layout()
    fig.savefig(output_dir / "calibration_comparison.png", dpi=170)
    plt.close(fig)


def _decision(
    aggregate: pd.DataFrame,
    power_summary: pd.DataFrame,
    runtime: pd.DataFrame,
) -> tuple[str, dict]:
    indexed = aggregate.set_index(["stage", "method"])
    normal_hard = indexed.loc[("hard", "wald_normal")]
    welch_hard = indexed.loc[("hard", "welch_reference")]
    normal_broad = indexed.loc[("broad", "wald_normal")]
    welch_broad = indexed.loc[("broad", "welch_reference")]
    hard_normal_error = float(normal_hard["mean_absolute_fpr_error_05"])
    hard_welch_error = float(welch_hard["mean_absolute_fpr_error_05"])
    hard_improvement = (
        1.0 - hard_welch_error / hard_normal_error
        if hard_normal_error > 0
        else float("-inf")
    )
    power_means = power_summary.groupby("method")["power_05"].mean()
    power_loss = float(
        power_means["wald_normal"] - power_means["welch_reference"]
    )
    median_normal_ms = float(runtime["median_normal_ms"].median())
    median_welch_ms = float(runtime["median_welch_ms"].median())
    runtime_ratio = median_welch_ms / median_normal_ms
    criteria = {
        "hard_alpha05_mae_reduction_at_least_20pct": hard_improvement >= 0.20,
        "hard_alpha10_mae_does_not_increase": (
            float(welch_hard["mean_absolute_fpr_error_10"])
            <= float(normal_hard["mean_absolute_fpr_error_10"])
        ),
        "broad_alpha05_mae_increase_at_most_0_001": (
            float(welch_broad["mean_absolute_fpr_error_05"])
            <= float(normal_broad["mean_absolute_fpr_error_05"]) + 0.001
        ),
        "broad_in_band_drop_at_most_0_02": (
            float(welch_broad["within_035_065"])
            >= float(normal_broad["within_035_065"]) - 0.02
        ),
        "mean_power_loss_at_most_0_03": power_loss <= 0.03,
        "valid_rate_at_least_0_995": (
            float(welch_broad["mean_valid_rate"]) >= 0.995
            and float(welch_hard["mean_valid_rate"]) >= 0.995
        ),
        "runtime_below_2x_and_1ms": (
            runtime_ratio < 2.0 and median_welch_ms < 1.0
        ),
    }
    metrics = {
        "hard_normal_mae_05": hard_normal_error,
        "hard_welch_mae_05": hard_welch_error,
        "hard_relative_improvement": hard_improvement,
        "broad_normal_mae_05": float(
            normal_broad["mean_absolute_fpr_error_05"]
        ),
        "broad_welch_mae_05": float(
            welch_broad["mean_absolute_fpr_error_05"]
        ),
        "mean_power_loss": power_loss,
        "median_normal_ms": median_normal_ms,
        "median_welch_ms": median_welch_ms,
        "runtime_ratio": runtime_ratio,
        "criteria": criteria,
    }
    return ("GO" if all(criteria.values()) else "NO-GO"), metrics


def _write_report(
    output_dir: Path,
    profile: str,
    aggregate: pd.DataFrame,
    null_summary: pd.DataFrame,
    power_summary: pd.DataFrame,
    permutation_summary: pd.DataFrame,
    runtime: pd.DataFrame,
    decision: str,
    decision_metrics: dict,
) -> None:
    aggregate_view = aggregate[
        [
            "stage",
            "method",
            "mean_fpr_05",
            "mean_absolute_fpr_error_05",
            "within_035_065",
            "mean_coverage_95",
        ]
    ]
    power_view = power_summary[
        ["scenario_id", "method", "true_delta", "power_05", "coverage_95"]
    ]
    criteria = decision_metrics["criteria"]
    lines = [
        "# Welch-Satterthwaite Differential-MI Validation",
        "",
        f"Profile: `{profile}`.",
        "",
        f"## Decision: {decision}",
        "",
        f"Hard-grid alpha-0.05 MAE changed from "
        f"`{decision_metrics['hard_normal_mae_05']:.5f}` to "
        f"`{decision_metrics['hard_welch_mae_05']:.5f}`, a relative "
        f"improvement of `{decision_metrics['hard_relative_improvement']:.1%}`.",
        f"Broad-grid MAE changed from "
        f"`{decision_metrics['broad_normal_mae_05']:.5f}` to "
        f"`{decision_metrics['broad_welch_mae_05']:.5f}`.",
        "",
    ]
    lines.extend(
        f"- [{'x' if passed else ' '}] `{name}`"
        for name, passed in criteria.items()
    )
    lines.extend(
        [
            "",
            "The sensitivity variant cannot overturn the primary decision.",
            "",
            "## Null Calibration",
            "",
            _markdown(aggregate_view),
            "",
            "## Power",
            "",
            _markdown(power_view, 4),
            "",
            "## Runtime",
            "",
            _markdown(runtime, 4),
            "",
        ]
    )
    if not permutation_summary.empty:
        permutation_view = permutation_summary[
            [
                "scenario_id",
                "replicates",
                "wald_normal_fpr_05",
                "welch_reference_fpr_05",
                "student_perm_analytic_fpr_05",
                "mean_permutation_ms",
            ]
        ]
        lines.extend(
            [
                "## Permutation Anchors",
                "",
                _markdown(permutation_view, 4),
                "",
            ]
        )
    hard = null_summary[null_summary["stage"] == "hard"]
    lines.extend(
        [
            "## Degrees of Freedom",
            "",
            f"Hard-grid median effective df ranged from "
            f"`{hard['median_welch_df'].min():.2f}` to "
            f"`{hard['median_welch_df'].max():.2f}`.",
            "",
            "JIDT does not provide this independent two-sample equal-MI test.",
            "The permutation comparator is the optimized table-level",
            "studentized analytic implementation for the same estimand.",
            "",
            "See the CSV and compressed replicate files for complete",
            "scenario-level intervals, paired p-values, seeds, and diagnostics.",
        ]
    )
    (output_dir / "REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    settings = _settings(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    entries = _scenario_entries(settings)
    total_jobs = sum(len(stage_entries) for stage_entries in entries.values())
    power_scenarios = power_curve_scenarios()
    seed_sequence = np.random.SeedSequence(args.simulation_seed)
    child_seeds = iter(
        int(child.generate_state(1)[0])
        for child in seed_sequence.spawn(total_jobs + len(power_scenarios))
    )

    null_frames = []
    permutation_frames = []
    scenario_rows = []
    batch_runtime_rows = []
    completed = 0
    run_start = perf_counter()
    for stage, stage_entries in entries.items():
        replicates = settings[f"{stage}_replicates"]
        for scenario_seed, scenario in stage_entries:
            completed += 1
            simulation_seed = next(child_seeds)
            print(
                f"[{completed}/{total_jobs}] {stage} "
                f"{scenario_seed}:{scenario.scenario_id}",
                flush=True,
            )
            permutation_replicates = (
                settings["permutation_replicates"]
                if stage == "hard"
                else 0
            )
            frame, permutation_frame, run_diagnostics = _simulate_null(
                stage,
                scenario_seed,
                scenario,
                replicates=replicates,
                simulation_seed=simulation_seed,
                permutation_replicates=permutation_replicates,
                permutations=args.permutations,
            )
            null_frames.append(frame)
            if not permutation_frame.empty:
                permutation_frames.append(permutation_frame)
            scenario_rows.append(
                _scenario_metadata(stage, scenario_seed, scenario)
            )
            batch_runtime_rows.append(run_diagnostics)

    power_frames = []
    for scenario in power_scenarios:
        simulation_seed = next(child_seeds)
        frame, metadata = _simulate_power(
            scenario,
            replicates=settings["power_replicates"],
            simulation_seed=simulation_seed,
        )
        power_frames.append(frame)
        scenario_rows.append(metadata)

    null_frame = pd.concat(null_frames, ignore_index=True)
    permutation_frame = (
        pd.concat(permutation_frames, ignore_index=True)
        if permutation_frames
        else pd.DataFrame()
    )
    power_frame = pd.concat(power_frames, ignore_index=True)
    scenario_frame = pd.DataFrame(scenario_rows)
    batch_runtime = pd.DataFrame(batch_runtime_rows)

    null_summary = _summarize_null(null_frame)
    aggregate = _aggregate_null(null_summary)
    power_summary = _summarize_power(power_frame)
    permutation_summary = _summarize_permutation(permutation_frame)
    runtime = _runtime_audit(
        entries["hard"] or entries["broad"],
        repetitions=30 if args.profile == "smoke" else 200,
        seed=args.simulation_seed + 73,
    )
    decision, decision_metrics = _decision(
        aggregate,
        power_summary,
        runtime,
    )

    scenario_frame.to_csv(args.output_dir / "scenarios.csv", index=False)
    null_frame.to_csv(
        args.output_dir / "null_replicates.csv.gz",
        index=False,
        compression="gzip",
    )
    null_summary.to_csv(args.output_dir / "null_summary.csv", index=False)
    aggregate.to_csv(args.output_dir / "method_summary.csv", index=False)
    power_frame.to_csv(
        args.output_dir / "power_replicates.csv.gz",
        index=False,
        compression="gzip",
    )
    power_summary.to_csv(args.output_dir / "power_summary.csv", index=False)
    if not permutation_frame.empty:
        permutation_frame.to_csv(
            args.output_dir / "permutation_replicates.csv.gz",
            index=False,
            compression="gzip",
        )
        permutation_summary.to_csv(
            args.output_dir / "permutation_summary.csv",
            index=False,
        )
    batch_runtime.to_csv(args.output_dir / "batch_runtime.csv", index=False)
    runtime.to_csv(args.output_dir / "runtime_summary.csv", index=False)
    _plot_results(null_summary, args.output_dir)
    _write_report(
        args.output_dir,
        args.profile,
        aggregate,
        null_summary,
        power_summary,
        permutation_summary,
        runtime,
        decision,
        decision_metrics,
    )

    metadata = {
        "profile": args.profile,
        "settings": settings,
        "simulation_seed": args.simulation_seed,
        "permutations": args.permutations,
        "elapsed_seconds": perf_counter() - run_start,
        "decision": decision,
        "decision_metrics": decision_metrics,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Decision: {decision}", flush=True)
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
