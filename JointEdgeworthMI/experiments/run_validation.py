#!/usr/bin/env python3
"""Run the frozen validation of joint studentized Edgeworth MI inference."""

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
sys.path.insert(0, str(REPOSITORY_ROOT / "InfluenceDfMI" / "src"))
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
from influence_df_mi import influence_df_test  # noqa: E402
from joint_edgeworth_mi import (  # noqa: E402
    differential_mi_pvalues,
    joint_edgeworth_test,
    studentized_edgeworth_cdf,
)
from joint_edgeworth_mi.method import _joint_influence_moments  # noqa: E402
from welch_differential_mi import welch_satterthwaite_test  # noqa: E402


POPULATION_SEEDS = (91_370_211, 47_628_903)
SIMULATION_SEED = 68_314_527
RUNTIME_SEED = 55_290_811
BOOTSTRAP_SEED = 30_714_983

REPLICATES = {
    "broad": 5_000,
    "hard": 20_000,
    "strong": 5_000,
    "stress": 10_000,
}
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
CUMULANT_AUDIT_IDS = frozenset(
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
    "wald_normal": ("normal_p_value", None, "base_valid"),
    "welch_n_minus_1": ("naive_welch_p_value", "naive_welch_df", "base_valid"),
    "if_satterthwaite": (
        "influence_welch_p_value",
        "influence_welch_df",
        "base_valid",
    ),
    "joint_edgeworth": ("edgeworth_p_value", None, "edgeworth_valid"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def _entries() -> dict[str, list[tuple[int, RandomScenario]]]:
    entries: dict[str, list[tuple[int, RandomScenario]]] = {
        "broad": [],
        "hard": [],
        "strong": [],
        "stress": [],
    }
    for population_seed in POPULATION_SEEDS:
        scenarios = generate_random_scenarios(population_seed)
        by_id = {scenario.scenario_id: scenario for scenario in scenarios}
        entries["broad"].extend((population_seed, item) for item in scenarios)
        entries["hard"].extend(
            (population_seed, item)
            for item in scenarios
            if item.scenario_id in HARD_IDS
        )
        entries["strong"].extend(
            (
                population_seed,
                replace(
                    item,
                    scenario_id=f"strong_{item.scenario_id}",
                    margin_alpha_q=item.margin_alpha_p,
                    association_q=item.association_p,
                    probability_q=item.probability_p.copy(),
                ),
            )
            for item in scenarios
        )
        for source_id, n_p, n_q in STRESS_CONFIGS:
            source = by_id[source_id]
            entries["stress"].append(
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
    return entries


def _population_cumulants(scenario: RandomScenario) -> dict[str, float]:
    p = _joint_influence_moments(scenario.probability_p)
    q = _joint_influence_moments(scenario.probability_q)
    h = (
        float(p["variance"]) / scenario.n_p
        + float(q["variance"]) / scenario.n_q
    )
    third = (
        float(p["third_moment"]) / scenario.n_p**2
        - float(q["third_moment"]) / scenario.n_q**2
    )
    covariance = (
        float(p["covariance"]) / scenario.n_p**2
        - float(q["covariance"]) / scenario.n_q**2
    )
    return {
        "population_first_order_variance": h,
        "population_numerator_third_cumulant": third,
        "population_numerator_variance_covariance": covariance,
        "population_standardized_third_cumulant": third / h**1.5,
        "population_standardized_variance_covariance": covariance / h**1.5,
    }


def _wilson(rejections: int, total: int) -> tuple[float, float]:
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    return float(interval.low), float(interval.high)


def _third_cumulant(values: np.ndarray) -> float:
    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    centered = finite - np.mean(finite)
    return float(np.mean(centered**3))


def _skewness(values: np.ndarray) -> float:
    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    centered = finite - np.mean(finite)
    variance = np.mean(centered**2)
    if not np.isfinite(variance) or variance <= 0:
        return float("nan")
    return float(np.mean(centered**3) / variance**1.5)


def _scenario_metadata(
    stage: str,
    population_seed: int,
    scenario: RandomScenario,
) -> dict:
    row = scenario_diagnostics(scenario)
    row.update(
        {
            "stage": stage,
            "population_seed": population_seed,
            "scenario_key": f"{stage}:{population_seed}:{scenario.scenario_id}",
            "probability_p_json": json.dumps(scenario.probability_p.tolist()),
            "probability_q_json": json.dumps(scenario.probability_q.tolist()),
        }
    )
    return row


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
    batch_seconds = perf_counter() - start
    base_valid = np.asarray(values["base_valid"], dtype=bool)
    edgeworth_valid = np.asarray(values["edgeworth_valid"], dtype=bool)
    delta = np.asarray(values["delta_corrected"])
    standard_error = np.asarray(values["standard_error"])
    squared_standard_error = standard_error**2
    true_delta = float(scenario_diagnostics(scenario)["true_delta"])
    population = _population_cumulants(scenario)

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
        "base_valid_n": int(np.count_nonzero(base_valid)),
        "base_valid_rate": float(np.mean(base_valid)),
        "edgeworth_valid_n": int(np.count_nonzero(edgeworth_valid)),
        "edgeworth_valid_rate": float(np.mean(edgeworth_valid)),
        "true_delta": true_delta,
        "minimum_joint_expected_p": float(
            scenario.n_p * scenario.probability_p.min()
        ),
        "minimum_joint_expected_q": float(
            scenario.n_q * scenario.probability_q.min()
        ),
        "mean_zero_fraction_p": float(np.mean(table_p == 0)),
        "mean_zero_fraction_q": float(np.mean(table_q == 0)),
        "batch_seconds": batch_seconds,
        "batch_microseconds_per_pair": 1e6 * batch_seconds / replicates,
        "empirical_delta_variance": float(np.var(delta, ddof=1)),
        "empirical_delta_third_cumulant": _third_cumulant(delta),
        "empirical_delta_variance_covariance": float(
            np.cov(delta, squared_standard_error, ddof=1)[0, 1]
        ),
        "empirical_mean_statistic": float(
            np.nanmean(np.asarray(values["statistic"])[base_valid])
        ),
        "empirical_statistic_skewness": _skewness(
            np.asarray(values["statistic"])[base_valid]
        ),
        "population_predicted_mean_statistic": (
            -population["population_standardized_variance_covariance"] / 2.0
        ),
        "population_predicted_statistic_skewness": (
            population["population_standardized_third_cumulant"]
            - 3.0
            * population["population_standardized_variance_covariance"]
        ),
        "median_plugin_standardized_third_cumulant": float(
            np.nanmedian(values["standardized_third_cumulant"])
        ),
        "median_plugin_standardized_variance_covariance": float(
            np.nanmedian(values["standardized_variance_covariance"])
        ),
        "median_absolute_edgeworth_correction": float(
            np.nanmedian(np.abs(values["edgeworth_correction"]))
        ),
        "minimum_edgeworth_density_factor": float(
            np.nanmin(values["edgeworth_density_factor"])
        ),
        **population,
    }

    critical_values = {
        "wald_normal": np.full(replicates, norm.ppf(0.975)),
        "welch_n_minus_1": t.ppf(0.975, df=values["naive_welch_df"]),
        "if_satterthwaite": t.ppf(
            0.975,
            df=values["influence_welch_df"],
        ),
    }
    for method, (p_key, df_key, valid_key) in METHODS.items():
        valid = np.asarray(values[valid_key], dtype=bool)
        valid_n = int(np.count_nonzero(valid))
        p_values = np.asarray(values[p_key])[valid]
        row[f"{method}_valid_n"] = valid_n
        row[f"{method}_valid_rate"] = valid_n / replicates
        if method == "joint_edgeworth":
            # Equal-tailed Edgeworth intervals invert the corrected CDF.
            row[f"{method}_coverage_95"] = float(
                np.mean(p_values > 0.05)
            )
        else:
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
    delta = np.asarray(values["delta_corrected"])
    standard_error = np.asarray(values["standard_error"])
    true_delta = float(diagnostics["true_delta"])
    centered_edgeworth = studentized_edgeworth_cdf(
        (delta - true_delta) / standard_error,
        values["standardized_third_cumulant"],
        values["standardized_variance_covariance"],
    )
    critical_values = {
        "wald_normal": np.full(POWER_REPLICATES, norm.ppf(0.975)),
        "welch_n_minus_1": t.ppf(0.975, df=values["naive_welch_df"]),
        "if_satterthwaite": t.ppf(
            0.975,
            df=values["influence_welch_df"],
        ),
    }
    rows = []
    for method, (p_key, df_key, valid_key) in METHODS.items():
        valid = np.asarray(values[valid_key], dtype=bool)
        p_values = np.asarray(values[p_key])[valid]
        if method == "joint_edgeworth":
            coverage_valid = (
                np.asarray(values["base_valid"], dtype=bool)
                & np.asarray(centered_edgeworth["valid"], dtype=bool)
            )
            coverage = float(
                np.mean(
                    np.asarray(centered_edgeworth["p_value"])[coverage_valid]
                    > 0.05
                )
            )
        else:
            coverage = float(
                np.mean(
                    np.abs(delta[valid] - true_delta)
                    <= critical_values[method][valid] * standard_error[valid]
                )
            )
        row = {
            "scenario_id": scenario.scenario_id,
            "simulation_seed": simulation_seed,
            "method": method,
            "replicates": POWER_REPLICATES,
            "valid_n": int(np.count_nonzero(valid)),
            "valid_rate": float(np.mean(valid)),
            "true_delta": true_delta,
            "power_05": float(np.mean(p_values <= 0.05)),
            "coverage_95": coverage,
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
        for method in METHODS:
            valid_n = group[f"{method}_valid_n"].sum()
            row: dict[str, int | float | str] = {
                "stage": stage,
                "method": method,
                "population_pairs": len(group),
                "table_pairs": int(group["replicates"].sum()),
                "aggregate_valid_rate": float(
                    valid_n / group["replicates"].sum()
                ),
                "minimum_scenario_valid_rate": float(
                    group[f"{method}_valid_rate"].min()
                ),
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
            if method == "joint_edgeworth":
                for comparator in (
                    "wald_normal",
                    "welch_n_minus_1",
                    "if_satterthwaite",
                ):
                    gain = (
                        group[f"{comparator}_error_05"]
                        - group["joint_edgeworth_error_05"]
                    ).to_numpy()
                    rng = np.random.default_rng(
                        bootstrap_seed + 10 * group_index + len(comparator)
                    )
                    bootstrap = np.mean(
                        rng.choice(
                            gain,
                            size=(50_000, len(gain)),
                            replace=True,
                        ),
                        axis=1,
                    )
                    row[f"paired_gain_vs_{comparator}_05"] = float(
                        np.mean(gain)
                    )
                    row[f"paired_gain_vs_{comparator}_05_low"] = float(
                        np.quantile(bootstrap, 0.025)
                    )
                    row[f"paired_gain_vs_{comparator}_05_high"] = float(
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
    rows = []
    for population_seed, scenario in entries:
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.reshape(-1),
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_q.reshape(-1),
        ).reshape(scenario.rows, scenario.columns)
        functions = {
            "wald_normal": analytic_wald_test,
            "welch_n_minus_1": welch_satterthwaite_test,
            "if_satterthwaite": influence_df_test,
            "joint_edgeworth": joint_edgeworth_test,
        }
        for function in functions.values():
            function(table_p, table_q)
        timings = {method: [] for method in functions}
        for _ in range(repetitions):
            for method, function in functions.items():
                start = perf_counter()
                function(table_p, table_q)
                timings[method].append(perf_counter() - start)
        row: dict[str, int | float | str] = {
            "population_seed": population_seed,
            "scenario_id": scenario.scenario_id,
            "rows": scenario.rows,
            "columns": scenario.columns,
            "repetitions": repetitions,
        }
        for method, values in timings.items():
            row[f"median_{method}_ms"] = 1000.0 * float(np.median(values))
        row["joint_over_normal"] = (
            row["median_joint_edgeworth_ms"]
            / row["median_wald_normal_ms"]
        )
        rows.append(row)
    return pd.DataFrame(rows)


def _decision(
    aggregate: pd.DataFrame,
    power: pd.DataFrame,
    runtime: pd.DataFrame,
) -> tuple[str, dict]:
    indexed = aggregate.set_index(["stage", "method"])
    hard_naive = indexed.loc[("hard", "welch_n_minus_1")]
    hard_influence = indexed.loc[("hard", "if_satterthwaite")]
    hard_candidate = indexed.loc[("hard", "joint_edgeworth")]
    broad_naive = indexed.loc[("broad", "welch_n_minus_1")]
    broad_candidate = indexed.loc[("broad", "joint_edgeworth")]
    balanced_normal = indexed.loc[("broad_balanced_design0", "wald_normal")]
    balanced_candidate = indexed.loc[
        ("broad_balanced_design0", "joint_edgeworth")
    ]
    strong_naive = indexed.loc[("strong", "welch_n_minus_1")]
    strong_candidate = indexed.loc[("strong", "joint_edgeworth")]
    power_mean = power.groupby("method")["power_05"].mean()
    normal_ms = float(runtime["median_wald_normal_ms"].median())
    candidate_ms = float(runtime["median_joint_edgeworth_ms"].median())

    criteria = {
        "hard_alpha05_mae_at_least_10pct_lower_than_naive": (
            float(hard_candidate["mean_absolute_fpr_error_05"])
            <= 0.90 * float(hard_naive["mean_absolute_fpr_error_05"])
        ),
        "hard_alpha10_mae_does_not_exceed_naive": (
            float(hard_candidate["mean_absolute_fpr_error_10"])
            <= float(hard_naive["mean_absolute_fpr_error_10"])
        ),
        "hard_alpha05_mae_within_0_00050_of_influence_df": (
            float(hard_candidate["mean_absolute_fpr_error_05"])
            <= float(hard_influence["mean_absolute_fpr_error_05"]) + 0.00050
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
            float(power_mean["welch_n_minus_1"] - power_mean["joint_edgeworth"])
            <= 0.01
        ),
        "broad_hard_strong_valid_rate_at_least_0_995": all(
            float(indexed.loc[(stage, "joint_edgeworth")]["aggregate_valid_rate"])
            >= 0.995
            for stage in ("broad", "hard", "strong")
        ),
        "scalar_runtime_below_3x_normal_and_1ms": (
            candidate_ms / normal_ms < 3.0 and candidate_ms < 1.0
        ),
    }
    metrics = {
        "hard_naive_mae_05": float(
            hard_naive["mean_absolute_fpr_error_05"]
        ),
        "hard_influence_df_mae_05": float(
            hard_influence["mean_absolute_fpr_error_05"]
        ),
        "hard_candidate_mae_05": float(
            hard_candidate["mean_absolute_fpr_error_05"]
        ),
        "broad_naive_mae_05": float(
            broad_naive["mean_absolute_fpr_error_05"]
        ),
        "broad_candidate_mae_05": float(
            broad_candidate["mean_absolute_fpr_error_05"]
        ),
        "balanced_normal_mae_05": float(
            balanced_normal["mean_absolute_fpr_error_05"]
        ),
        "balanced_candidate_mae_05": float(
            balanced_candidate["mean_absolute_fpr_error_05"]
        ),
        "power_loss_vs_naive": float(
            power_mean["welch_n_minus_1"] - power_mean["joint_edgeworth"]
        ),
        "median_normal_ms": normal_ms,
        "median_candidate_ms": candidate_ms,
        "runtime_ratio": candidate_ms / normal_ms,
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
    cumulant_audit: pd.DataFrame,
) -> None:
    aggregate_view = aggregate[
        [
            "stage",
            "method",
            "population_pairs",
            "aggregate_valid_rate",
            "mean_fpr_05",
            "mean_absolute_fpr_error_05",
            "mean_absolute_fpr_error_10",
        ]
    ]
    power_view = power[
        ["scenario_id", "method", "true_delta", "valid_rate", "power_05"]
    ]
    cumulant_view = cumulant_audit[
        [
            "population_seed",
            "scenario_id",
            "population_standardized_third_cumulant",
            "median_plugin_standardized_third_cumulant",
            "population_standardized_variance_covariance",
            "median_plugin_standardized_variance_covariance",
        ]
    ]
    runtime_view = runtime[
        [
            "scenario_id",
            "rows",
            "columns",
            "median_wald_normal_ms",
            "median_joint_edgeworth_ms",
            "joint_over_normal",
        ]
    ]
    criteria = [
        f"- [{'x' if passed else ' '}] `{name}`"
        for name, passed in metrics["criteria"].items()
    ]
    lines = [
        "# Joint Studentized Edgeworth MI Validation",
        "",
        f"## Decision: {decision}",
        "",
        (
            "Hard alpha-0.05 MAE: normal/naive/influence-df/joint = "
            f"`{aggregate.set_index(['stage', 'method']).loc[('hard', 'wald_normal'), 'mean_absolute_fpr_error_05']:.5f}` / "
            f"`{metrics['hard_naive_mae_05']:.5f}` / "
            f"`{metrics['hard_influence_df_mae_05']:.5f}` / "
            f"`{metrics['hard_candidate_mae_05']:.5f}`."
        ),
        (
            "Broad alpha-0.05 MAE changed from "
            f"`{metrics['broad_naive_mae_05']:.5f}` for naive Welch to "
            f"`{metrics['broad_candidate_mae_05']:.5f}`."
        ),
        "",
        *criteria,
        "",
        "## Null Calibration",
        "",
        _markdown(aggregate_view),
        "",
        "## Cumulant Diagnostics",
        "",
        _markdown(cumulant_view, 4),
        "",
        "## Power",
        "",
        _markdown(power_view, 4),
        "",
        "## Runtime",
        "",
        _markdown(runtime_view, 4),
        "",
        "The stress stage is diagnostic and cannot rescue a failed decision.",
        "See the CSV files for all population probabilities, seeds, validity",
        "rates, Wilson intervals, and empirical joint-moment diagnostics.",
    ]
    (output_dir / "REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    start = perf_counter()
    entries = _entries()
    total_jobs = sum(len(items) for items in entries.values())
    power_scenarios = power_curve_scenarios()
    children = np.random.SeedSequence(SIMULATION_SEED).spawn(
        total_jobs + len(power_scenarios)
    )
    simulation_seeds = iter(
        int(child.generate_state(1)[0]) for child in children
    )

    scenario_rows = []
    population_rows = []
    completed = 0
    for stage, stage_entries in entries.items():
        for population_seed, scenario in stage_entries:
            completed += 1
            simulation_seed = next(simulation_seeds)
            print(
                f"[{completed}/{total_jobs}] {stage} "
                f"{population_seed}:{scenario.scenario_id}",
                flush=True,
            )
            summary, metadata = _run_null(
                stage,
                population_seed,
                scenario,
                replicates=REPLICATES[stage],
                simulation_seed=simulation_seed,
            )
            scenario_rows.append(summary)
            population_rows.append(metadata)

    power_rows = []
    for scenario in power_scenarios:
        simulation_seed = next(simulation_seeds)
        rows, metadata = _run_power(
            scenario,
            simulation_seed=simulation_seed,
        )
        power_rows.extend(rows)
        population_rows.append(metadata)

    scenario_summary = pd.DataFrame(scenario_rows)
    populations = pd.DataFrame(population_rows)
    power = pd.DataFrame(power_rows)
    aggregate = _aggregate(
        scenario_summary,
        bootstrap_seed=BOOTSTRAP_SEED,
    )
    runtime = _runtime_audit(entries["hard"])
    cumulant_audit = scenario_summary[
        scenario_summary["stage"].eq("broad")
        & scenario_summary["scenario_id"].isin(CUMULANT_AUDIT_IDS)
    ].copy()
    decision, metrics = _decision(aggregate, power, runtime)

    scenario_summary.to_csv(
        args.output_dir / "scenario_summary.csv",
        index=False,
    )
    populations.to_csv(args.output_dir / "scenarios.csv", index=False)
    aggregate.to_csv(args.output_dir / "method_summary.csv", index=False)
    power.to_csv(args.output_dir / "power_summary.csv", index=False)
    runtime.to_csv(args.output_dir / "runtime_summary.csv", index=False)
    cumulant_audit.to_csv(
        args.output_dir / "cumulant_audit.csv",
        index=False,
    )
    _write_report(
        args.output_dir,
        decision,
        metrics,
        aggregate,
        power,
        runtime,
        cumulant_audit,
    )

    metadata = {
        "protocol_frozen": "2026-07-27",
        "population_seeds": POPULATION_SEEDS,
        "simulation_seed": SIMULATION_SEED,
        "runtime_seed": RUNTIME_SEED,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "replicates": REPLICATES,
        "power_replicates": POWER_REPLICATES,
        "population_pairs": {
            stage: len(items) for stage, items in entries.items()
        },
        "table_pairs": {
            stage: len(entries[stage]) * REPLICATES[stage]
            for stage in entries
        },
        "decision": decision,
        "decision_metrics": metrics,
        "elapsed_seconds": perf_counter() - start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method_sha256": hashlib.sha256(
            (PROJECT_ROOT / "src" / "joint_edgeworth_mi" / "method.py").read_bytes()
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
