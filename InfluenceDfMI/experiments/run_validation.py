#!/usr/bin/env python3
"""Run the frozen one-shot validation of MI-specific influence degrees of freedom."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from dataclasses import replace
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest, norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "WelchSatterthwaiteMI" / "src"))

from differential_mi.inference import analytic_wald_test  # noqa: E402
from differential_mi.random_validation import (  # noqa: E402
    RandomScenario,
    generate_random_scenarios,
    scenario_diagnostics,
)
from differential_mi.scenarios import (  # noqa: E402
    build_distributions,
    power_curve_scenarios,
)
from influence_df_mi import (  # noqa: E402
    differential_mi_pvalues,
    influence_df_test,
    variance_functional_influence,
)
from welch_differential_mi import welch_satterthwaite_test  # noqa: E402


POPULATION_SEEDS = (73_105_913, 84_207_631)
SIMULATION_SEED = 52_611_907
RUNTIME_SEED = 31_845_071
BOOTSTRAP_SEED = 22_719_043

BROAD_REPLICATES = 5_000
HARD_REPLICATES = 20_000
STRONG_REPLICATES = 5_000
STRESS_REPLICATES = 10_000
POWER_REPLICATES = 10_000

HARD_IDS = frozenset(
    {
        "random_2x2_d5",
        "random_2x5_d5",
        "random_3x7_d5",
        "random_4x6_d5",
        "random_5x5_d5",
        "random_5x10_d5",
    }
)
DF_AUDIT_IDS = frozenset(
    {
        "random_2x2_d0",
        "random_2x2_d5",
        "random_2x5_d5",
        "random_4x6_d5",
        "random_5x5_d2",
    }
)
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
METHODS = {
    "wald_normal": ("normal_p_value", None),
    "welch_n_minus_1": ("naive_welch_p_value", "naive_welch_df"),
    "if_satterthwaite": ("influence_welch_p_value", "influence_welch_df"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def _entries() -> dict[str, list[tuple[int, RandomScenario]]]:
    result: dict[str, list[tuple[int, RandomScenario]]] = {
        "broad": [],
        "hard": [],
        "strong": [],
        "stress": [],
    }
    for population_seed in POPULATION_SEEDS:
        scenarios = generate_random_scenarios(population_seed)
        by_id = {scenario.scenario_id: scenario for scenario in scenarios}
        result["broad"].extend((population_seed, scenario) for scenario in scenarios)
        result["hard"].extend(
            (population_seed, scenario)
            for scenario in scenarios
            if scenario.scenario_id in HARD_IDS
        )
        result["strong"].extend(
            (
                population_seed,
                replace(
                    scenario,
                    scenario_id=f"strong_{scenario.scenario_id}",
                    margin_alpha_q=scenario.margin_alpha_p,
                    association_q=scenario.association_p,
                    probability_q=scenario.probability_p.copy(),
                ),
            )
            for scenario in scenarios
        )
        for source_id, n_p, n_q in STRESS_CONFIGS:
            source = by_id[source_id]
            result["stress"].append(
                (
                    population_seed,
                    replace(
                        source,
                        scenario_id=f"stress_{source_id}_n{n_p}_{n_q}",
                        n_p=n_p,
                        n_q=n_q,
                    ),
                )
            )
    return result


def _population_influence_df(scenario: RandomScenario) -> tuple[float, float, float]:
    p = variance_functional_influence(scenario.probability_p)
    q = variance_functional_influence(scenario.probability_q)
    variance_p = float(p["variance"])
    variance_q = float(q["variance"])
    tau_p = float(p["influence_variance"])
    tau_q = float(q["influence_variance"])
    component_p = variance_p / scenario.n_p
    component_q = variance_q / scenario.n_q
    component_df_p = 2.0 * scenario.n_p * variance_p**2 / tau_p
    component_df_q = 2.0 * scenario.n_q * variance_q**2 / tau_q
    combined = 2.0 * (component_p + component_q) ** 2 / (
        tau_p / scenario.n_p**3 + tau_q / scenario.n_q**3
    )
    return component_df_p, component_df_q, combined


def _wilson(rejections: int, total: int) -> tuple[float, float]:
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    return float(interval.low), float(interval.high)


def _empirical_df(values: np.ndarray) -> float:
    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    variance = np.var(finite, ddof=1)
    if finite.size <= 1 or not np.isfinite(variance) or variance <= 0:
        return float("nan")
    return float(2.0 * np.mean(finite) ** 2 / variance)


def _scenario_metadata(
    stage: str,
    population_seed: int,
    scenario: RandomScenario,
) -> dict:
    diagnostics = scenario_diagnostics(scenario)
    diagnostics.update(
        {
            "stage": stage,
            "population_seed": population_seed,
            "scenario_key": f"{stage}:{population_seed}:{scenario.scenario_id}",
            "probability_p_json": json.dumps(scenario.probability_p.tolist()),
            "probability_q_json": json.dumps(scenario.probability_q.tolist()),
        }
    )
    return diagnostics


def _run_null(
    stage: str,
    population_seed: int,
    scenario: RandomScenario,
    *,
    replicates: int,
    simulation_seed: int,
) -> tuple[dict, dict]:
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
    elapsed = perf_counter() - start
    valid = np.asarray(values["valid"], dtype=bool)
    valid_n = int(np.count_nonzero(valid))
    true_delta = float(scenario_diagnostics(scenario)["true_delta"])
    component_p = np.asarray(values["variance_component_p"])
    component_q = np.asarray(values["variance_component_q"])
    total_component = component_p + component_q
    population_df_p, population_df_q, population_total_df = (
        _population_influence_df(scenario)
    )

    row: dict[str, int | float | str] = {
        "stage": stage,
        "population_seed": population_seed,
        "scenario_id": scenario.scenario_id,
        "scenario_key": f"{stage}:{population_seed}:{scenario.scenario_id}",
        "simulation_seed": simulation_seed,
        "rows": scenario.rows,
        "columns": scenario.columns,
        "design_index": scenario.design_index,
        "n_p": scenario.n_p,
        "n_q": scenario.n_q,
        "replicates": replicates,
        "valid_n": valid_n,
        "valid_rate": valid_n / replicates,
        "true_delta": true_delta,
        "minimum_joint_expected_p": float(
            scenario.n_p * scenario.probability_p.min()
        ),
        "minimum_joint_expected_q": float(
            scenario.n_q * scenario.probability_q.min()
        ),
        "mean_zero_fraction_p": float(np.mean(table_p == 0)),
        "mean_zero_fraction_q": float(np.mean(table_q == 0)),
        "batch_seconds": elapsed,
        "batch_microseconds_per_pair": 1e6 * elapsed / replicates,
        "empirical_component_df_p": _empirical_df(component_p),
        "empirical_component_df_q": _empirical_df(component_q),
        "empirical_total_df": _empirical_df(total_component),
        "median_naive_total_df": float(
            np.nanmedian(np.asarray(values["naive_welch_df"])[valid])
        ),
        "median_if_total_df": float(
            np.nanmedian(np.asarray(values["influence_welch_df"])[valid])
        ),
        "population_if_component_df_p": population_df_p,
        "population_if_component_df_q": population_df_q,
        "population_if_total_df": population_total_df,
        "correlation_delta_total_variance": float(
            np.corrcoef(
                np.asarray(values["delta_corrected"]),
                total_component,
            )[0, 1]
        ),
    }

    standard_error = np.asarray(values["standard_error"])
    delta = np.asarray(values["delta_corrected"])
    critical_values = {
        "wald_normal": np.full(replicates, norm.ppf(0.975)),
        "welch_n_minus_1": t.ppf(
            0.975,
            df=np.asarray(values["naive_welch_df"]),
        ),
        "if_satterthwaite": t.ppf(
            0.975,
            df=np.asarray(values["influence_welch_df"]),
        ),
    }
    for method, (p_key, df_key) in METHODS.items():
        p_values = np.asarray(values[p_key])[valid]
        row[f"{method}_coverage_95"] = float(
            np.mean(
                np.abs(delta[valid] - true_delta)
                <= critical_values[method][valid] * standard_error[valid]
            )
        )
        if df_key is not None:
            row[f"{method}_median_df"] = float(
                np.nanmedian(np.asarray(values[df_key])[valid])
            )
        for label, alpha in (("10", 0.10), ("05", 0.05)):
            rejections = int(np.count_nonzero(p_values <= alpha))
            rate = rejections / valid_n if valid_n else float("nan")
            low, high = (
                _wilson(rejections, valid_n)
                if valid_n
                else (float("nan"), float("nan"))
            )
            row[f"{method}_fpr_{label}"] = rate
            row[f"{method}_fpr_{label}_low"] = low
            row[f"{method}_fpr_{label}_high"] = high
            row[f"{method}_error_{label}"] = abs(rate - alpha)
    return row, _scenario_metadata(stage, population_seed, scenario)


def _run_power(scenario, *, simulation_seed: int) -> tuple[list[dict], dict]:
    probability_p, probability_q, diagnostics = build_distributions(scenario)
    rng = np.random.default_rng(simulation_seed)
    table_p = rng.multinomial(
        scenario.n_p,
        probability_p.reshape(-1),
        size=POWER_REPLICATES,
    ).reshape(POWER_REPLICATES, scenario.rows, scenario.columns)
    table_q = rng.multinomial(
        scenario.n_q,
        probability_q.reshape(-1),
        size=POWER_REPLICATES,
    ).reshape(POWER_REPLICATES, scenario.rows, scenario.columns)
    values = differential_mi_pvalues(table_p, table_q)
    valid = np.asarray(values["valid"], dtype=bool)
    true_delta = float(diagnostics["true_delta"])
    delta = np.asarray(values["delta_corrected"])
    standard_error = np.asarray(values["standard_error"])
    critical_values = {
        "wald_normal": np.full(POWER_REPLICATES, norm.ppf(0.975)),
        "welch_n_minus_1": t.ppf(
            0.975,
            df=np.asarray(values["naive_welch_df"]),
        ),
        "if_satterthwaite": t.ppf(
            0.975,
            df=np.asarray(values["influence_welch_df"]),
        ),
    }
    rows = []
    for method, (p_key, df_key) in METHODS.items():
        p_values = np.asarray(values[p_key])[valid]
        row = {
            "scenario_id": scenario.scenario_id,
            "simulation_seed": simulation_seed,
            "method": method,
            "replicates": POWER_REPLICATES,
            "valid_rate": float(valid.mean()),
            "true_delta": true_delta,
            "power_05": float(np.mean(p_values <= 0.05)),
            "coverage_95": float(
                np.mean(
                    np.abs(delta[valid] - true_delta)
                    <= critical_values[method][valid] * standard_error[valid]
                )
            ),
        }
        if df_key is not None:
            row["median_df"] = float(
                np.nanmedian(np.asarray(values[df_key])[valid])
            )
        rows.append(row)

    metadata = scenario.to_dict()
    metadata.update(diagnostics)
    metadata.update(
        {
            "stage": "power",
            "simulation_seed": simulation_seed,
            "scenario_key": f"power:{scenario.scenario_id}",
            "probability_p_json": json.dumps(probability_p.tolist()),
            "probability_q_json": json.dumps(probability_q.tolist()),
        }
    )
    return rows, metadata


def _aggregate(
    scenario_summary: pd.DataFrame,
    *,
    bootstrap_seed: int,
) -> pd.DataFrame:
    groups: list[tuple[str, pd.DataFrame]] = list(
        scenario_summary.groupby("stage", sort=False)
    )
    groups.append(
        (
            "broad_balanced_design0",
            scenario_summary[
                scenario_summary["stage"].eq("broad")
                & scenario_summary["design_index"].eq(0)
            ],
        )
    )
    rows = []
    for group_index, (stage, group) in enumerate(groups):
        for method, _ in METHODS.items():
            row: dict[str, int | float | str] = {
                "stage": stage,
                "method": method,
                "population_pairs": len(group),
                "table_pairs": int(group["replicates"].sum()),
                "aggregate_valid_rate": float(
                    group["valid_n"].sum() / group["replicates"].sum()
                ),
                "minimum_scenario_valid_rate": float(group["valid_rate"].min()),
                "mean_coverage_95": float(
                    group[f"{method}_coverage_95"].mean()
                ),
            }
            for label, alpha in (("10", 0.10), ("05", 0.05)):
                rates = group[f"{method}_fpr_{label}"]
                row[f"mean_fpr_{label}"] = float(rates.mean())
                row[f"mean_absolute_fpr_error_{label}"] = float(
                    np.mean(np.abs(rates - alpha))
                )
                row[f"minimum_fpr_{label}"] = float(rates.min())
                row[f"maximum_fpr_{label}"] = float(rates.max())
            if method == "if_satterthwaite":
                gain = (
                    group["welch_n_minus_1_error_05"]
                    - group["if_satterthwaite_error_05"]
                ).to_numpy()
                rng = np.random.default_rng(bootstrap_seed + group_index)
                bootstrap = np.mean(
                    rng.choice(gain, size=(50_000, len(gain)), replace=True),
                    axis=1,
                )
                row["paired_mae_gain_vs_naive_05"] = float(np.mean(gain))
                row["paired_mae_gain_05_low"] = float(
                    np.quantile(bootstrap, 0.025)
                )
                row["paired_mae_gain_05_high"] = float(
                    np.quantile(bootstrap, 0.975)
                )
            rows.append(row)
    return pd.DataFrame(rows)


def _runtime_audit(
    entries: list[tuple[int, RandomScenario]],
    *,
    repetitions: int = 200,
) -> pd.DataFrame:
    rng = np.random.default_rng(RUNTIME_SEED)
    selected = entries
    rows = []
    for population_seed, scenario in selected:
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.reshape(-1),
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_q.reshape(-1),
        ).reshape(scenario.rows, scenario.columns)
        analytic_wald_test(table_p, table_q)
        welch_satterthwaite_test(table_p, table_q)
        influence_df_test(table_p, table_q)
        timings = {"wald_normal": [], "welch_n_minus_1": [], "if_satterthwaite": []}
        for _ in range(repetitions):
            start = perf_counter()
            analytic_wald_test(table_p, table_q)
            timings["wald_normal"].append(perf_counter() - start)
            start = perf_counter()
            welch_satterthwaite_test(table_p, table_q)
            timings["welch_n_minus_1"].append(perf_counter() - start)
            start = perf_counter()
            influence_df_test(table_p, table_q)
            timings["if_satterthwaite"].append(perf_counter() - start)
        row: dict[str, int | float | str] = {
            "population_seed": population_seed,
            "scenario_id": scenario.scenario_id,
            "rows": scenario.rows,
            "columns": scenario.columns,
            "repetitions": repetitions,
        }
        for method, values in timings.items():
            row[f"median_{method}_ms"] = 1000.0 * float(np.median(values))
        row["if_over_normal"] = (
            row["median_if_satterthwaite_ms"] / row["median_wald_normal_ms"]
        )
        rows.append(row)
    return pd.DataFrame(rows)


def _decision(
    aggregate: pd.DataFrame,
    power: pd.DataFrame,
    runtime: pd.DataFrame,
    df_audit: pd.DataFrame,
) -> tuple[str, dict]:
    indexed = aggregate.set_index(["stage", "method"])
    hard_naive = indexed.loc[("hard", "welch_n_minus_1")]
    hard_candidate = indexed.loc[("hard", "if_satterthwaite")]
    broad_naive = indexed.loc[("broad", "welch_n_minus_1")]
    broad_candidate = indexed.loc[("broad", "if_satterthwaite")]
    balanced_normal = indexed.loc[("broad_balanced_design0", "wald_normal")]
    balanced_candidate = indexed.loc[
        ("broad_balanced_design0", "if_satterthwaite")
    ]
    strong_naive = indexed.loc[("strong", "welch_n_minus_1")]
    strong_candidate = indexed.loc[("strong", "if_satterthwaite")]
    power_mean = power.groupby("method")["power_05"].mean()
    median_normal_ms = float(runtime["median_wald_normal_ms"].median())
    median_candidate_ms = float(runtime["median_if_satterthwaite_ms"].median())

    naive_df_error = float(
        np.median(
            np.abs(
                np.log(
                    df_audit["median_naive_total_df"]
                    / df_audit["empirical_total_df"]
                )
            )
        )
    )
    candidate_df_error = float(
        np.median(
            np.abs(
                np.log(
                    df_audit["median_if_total_df"]
                    / df_audit["empirical_total_df"]
                )
            )
        )
    )
    criteria = {
        "hard_alpha05_mae_at_least_10pct_lower_than_naive": (
            float(hard_candidate["mean_absolute_fpr_error_05"])
            <= 0.90 * float(hard_naive["mean_absolute_fpr_error_05"])
        ),
        "hard_alpha10_mae_does_not_increase": (
            float(hard_candidate["mean_absolute_fpr_error_10"])
            <= float(hard_naive["mean_absolute_fpr_error_10"])
        ),
        "broad_alpha05_mae_within_0_00025_of_naive": (
            float(broad_candidate["mean_absolute_fpr_error_05"])
            <= float(broad_naive["mean_absolute_fpr_error_05"]) + 0.00025
        ),
        "balanced_alpha05_mae_within_0_00050_of_normal": (
            float(balanced_candidate["mean_absolute_fpr_error_05"])
            <= float(balanced_normal["mean_absolute_fpr_error_05"]) + 0.00050
        ),
        "strong_alpha05_mae_within_0_00025_of_naive": (
            float(strong_candidate["mean_absolute_fpr_error_05"])
            <= float(strong_naive["mean_absolute_fpr_error_05"]) + 0.00025
        ),
        "mean_power_loss_vs_naive_at_most_0_01": (
            float(power_mean["welch_n_minus_1"] - power_mean["if_satterthwaite"])
            <= 0.01
        ),
        "broad_hard_strong_valid_rate_at_least_0_995": all(
            float(indexed.loc[(stage, "if_satterthwaite")]["aggregate_valid_rate"])
            >= 0.995
            for stage in ("broad", "hard", "strong")
        ),
        "scalar_runtime_below_3x_normal_and_1ms": (
            median_candidate_ms / median_normal_ms < 3.0
            and median_candidate_ms < 1.0
        ),
        "df_log_error_at_least_50pct_lower_than_naive": (
            candidate_df_error <= 0.5 * naive_df_error
        ),
    }
    metrics = {
        "hard_naive_mae_05": float(
            hard_naive["mean_absolute_fpr_error_05"]
        ),
        "hard_candidate_mae_05": float(
            hard_candidate["mean_absolute_fpr_error_05"]
        ),
        "hard_relative_improvement": float(
            1.0
            - hard_candidate["mean_absolute_fpr_error_05"]
            / hard_naive["mean_absolute_fpr_error_05"]
        ),
        "broad_naive_mae_05": float(
            broad_naive["mean_absolute_fpr_error_05"]
        ),
        "broad_candidate_mae_05": float(
            broad_candidate["mean_absolute_fpr_error_05"]
        ),
        "power_loss_vs_naive": float(
            power_mean["welch_n_minus_1"] - power_mean["if_satterthwaite"]
        ),
        "median_normal_ms": median_normal_ms,
        "median_candidate_ms": median_candidate_ms,
        "runtime_ratio": median_candidate_ms / median_normal_ms,
        "naive_median_absolute_log_df_error": naive_df_error,
        "candidate_median_absolute_log_df_error": candidate_df_error,
        "criteria": criteria,
    }
    return ("GO" if all(criteria.values()) else "NO-GO"), metrics


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


def _write_report(
    output_dir: Path,
    decision: str,
    metrics: dict,
    aggregate: pd.DataFrame,
    power: pd.DataFrame,
    runtime: pd.DataFrame,
    df_audit: pd.DataFrame,
) -> None:
    aggregate_view = aggregate[
        [
            "stage",
            "method",
            "population_pairs",
            "mean_fpr_05",
            "mean_absolute_fpr_error_05",
            "mean_absolute_fpr_error_10",
            "mean_coverage_95",
        ]
    ]
    power_view = power[
        ["scenario_id", "method", "true_delta", "power_05", "coverage_95"]
    ]
    runtime_view = runtime[
        [
            "scenario_id",
            "rows",
            "columns",
            "median_wald_normal_ms",
            "median_welch_n_minus_1_ms",
            "median_if_satterthwaite_ms",
            "if_over_normal",
        ]
    ]
    df_view = df_audit[
        [
            "population_seed",
            "scenario_id",
            "empirical_total_df",
            "median_naive_total_df",
            "median_if_total_df",
            "population_if_total_df",
        ]
    ]
    criteria_lines = [
        f"- [{'x' if passed else ' '}] `{name}`"
        for name, passed in metrics["criteria"].items()
    ]
    lines = [
        "# MI-Specific Influence-DF Validation",
        "",
        f"## Decision: {decision}",
        "",
        (
            "The hard-grid alpha-0.05 MAE changed from "
            f"`{metrics['hard_naive_mae_05']:.5f}` for the naive Welch "
            f"reference to `{metrics['hard_candidate_mae_05']:.5f}` for the "
            "MI-specific influence reference "
            f"(`{metrics['hard_relative_improvement']:.1%}` improvement)."
        ),
        (
            "Across the broad grid, MAE changed from "
            f"`{metrics['broad_naive_mae_05']:.5f}` to "
            f"`{metrics['broad_candidate_mae_05']:.5f}`."
        ),
        "",
        *criteria_lines,
        "",
        "## Null Calibration",
        "",
        _markdown(aggregate_view),
        "",
        "## Degrees-of-Freedom Audit",
        "",
        _markdown(df_view, 3),
        "",
        "## Power",
        "",
        _markdown(power_view, 4),
        "",
        "## Scalar Runtime",
        "",
        _markdown(runtime_view, 4),
        "",
        "The small-sample stress stage is diagnostic only and cannot change",
        "the prospective decision. See the CSV files for all scenario-level",
        "Wilson intervals, seeds, population probabilities, and diagnostics.",
    ]
    (output_dir / "REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    run_start = perf_counter()
    entries = _entries()
    replicates_by_stage = {
        "broad": BROAD_REPLICATES,
        "hard": HARD_REPLICATES,
        "strong": STRONG_REPLICATES,
        "stress": STRESS_REPLICATES,
    }
    total_jobs = sum(len(stage_entries) for stage_entries in entries.values())
    power_scenarios = power_curve_scenarios()
    child_sequences = np.random.SeedSequence(SIMULATION_SEED).spawn(
        total_jobs + len(power_scenarios)
    )
    child_seeds = iter(
        int(child.generate_state(1)[0]) for child in child_sequences
    )

    scenario_rows = []
    population_rows = []
    completed = 0
    for stage, stage_entries in entries.items():
        for population_seed, scenario in stage_entries:
            completed += 1
            simulation_seed = next(child_seeds)
            print(
                f"[{completed}/{total_jobs}] {stage} "
                f"{population_seed}:{scenario.scenario_id}",
                flush=True,
            )
            summary, metadata = _run_null(
                stage,
                population_seed,
                scenario,
                replicates=replicates_by_stage[stage],
                simulation_seed=simulation_seed,
            )
            scenario_rows.append(summary)
            population_rows.append(metadata)

    power_rows = []
    for scenario in power_scenarios:
        simulation_seed = next(child_seeds)
        rows, metadata = _run_power(
            scenario,
            simulation_seed=simulation_seed,
        )
        power_rows.extend(rows)
        population_rows.append(metadata)

    scenario_summary = pd.DataFrame(scenario_rows)
    population_frame = pd.DataFrame(population_rows)
    power = pd.DataFrame(power_rows)
    aggregate = _aggregate(scenario_summary, bootstrap_seed=BOOTSTRAP_SEED)
    runtime = _runtime_audit(entries["hard"])
    df_audit = scenario_summary[
        scenario_summary["stage"].eq("broad")
        & scenario_summary["scenario_id"].isin(DF_AUDIT_IDS)
    ].copy()
    decision, metrics = _decision(aggregate, power, runtime, df_audit)

    scenario_summary.to_csv(
        args.output_dir / "scenario_summary.csv",
        index=False,
    )
    population_frame.to_csv(args.output_dir / "scenarios.csv", index=False)
    aggregate.to_csv(args.output_dir / "method_summary.csv", index=False)
    power.to_csv(args.output_dir / "power_summary.csv", index=False)
    runtime.to_csv(args.output_dir / "runtime_summary.csv", index=False)
    df_audit.to_csv(args.output_dir / "df_audit.csv", index=False)
    _write_report(
        args.output_dir,
        decision,
        metrics,
        aggregate,
        power,
        runtime,
        df_audit,
    )

    metadata = {
        "protocol_frozen": "2026-07-27",
        "population_seeds": POPULATION_SEEDS,
        "simulation_seed": SIMULATION_SEED,
        "runtime_seed": RUNTIME_SEED,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "replicates": replicates_by_stage,
        "power_replicates": POWER_REPLICATES,
        "population_pairs": {
            stage: len(stage_entries)
            for stage, stage_entries in entries.items()
        },
        "table_pairs": {
            stage: len(entries[stage]) * replicates_by_stage[stage]
            for stage in entries
        },
        "decision": decision,
        "decision_metrics": metrics,
        "elapsed_seconds": perf_counter() - run_start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method_sha256": hashlib.sha256(
            (PROJECT_ROOT / "src" / "influence_df_mi" / "method.py").read_bytes()
        ).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Decision: {decision}", flush=True)
    print(json.dumps(metrics, indent=2), flush=True)
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
