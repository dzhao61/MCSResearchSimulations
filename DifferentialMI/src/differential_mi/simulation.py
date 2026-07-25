"""Simulation runner and summaries for differential-MI validation."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from .inference import compare_tables
from .scenarios import Scenario, build_distributions


P_VALUE_COLUMNS = [
    "naive_perm_plugin_p",
    "student_perm_plugin_p",
    "student_perm_analytic_p",
    "student_perm_jackknife_p",
    "wald_plugin_p",
    "wald_analytic_p",
    "wald_jackknife_p",
]


@dataclass(frozen=True)
class SimulationSettings:
    null_replicates: int
    power_replicates: int
    permutations: int
    seed: int


def run_scenario(
    scenario: Scenario,
    settings: SimulationSettings,
    *,
    scenario_seed: int,
) -> tuple[pd.DataFrame, dict]:
    probability_p, probability_q, diagnostics = build_distributions(scenario)
    replicates = (
        settings.power_replicates
        if scenario.family == "power"
        else settings.null_replicates
    )
    rng = np.random.default_rng(scenario_seed)
    rows: list[dict] = []
    start = perf_counter()
    for replicate in range(replicates):
        table_p = rng.multinomial(scenario.n_p, probability_p.reshape(-1)).reshape(
            scenario.rows, scenario.columns
        )
        table_q = rng.multinomial(scenario.n_q, probability_q.reshape(-1)).reshape(
            scenario.rows, scenario.columns
        )
        result = compare_tables(
            table_p,
            table_q,
            permutations=settings.permutations,
            rng=rng,
        ).to_dict()
        result.update(
            {
                "scenario_id": scenario.scenario_id,
                "family": scenario.family,
                "regular": scenario.regular,
                "replicate": replicate,
                "scenario_seed": scenario_seed,
                "true_delta": diagnostics["true_delta"],
                "zero_cells_p": int(np.count_nonzero(table_p == 0)),
                "zero_cells_q": int(np.count_nonzero(table_q == 0)),
            }
        )
        rows.append(result)
    diagnostics["scenario_seconds"] = perf_counter() - start
    diagnostics["replicates"] = replicates
    return pd.DataFrame(rows), diagnostics


def _wilson_interval(rejections: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=confidence, method="wilson"
    )
    return float(interval.low), float(interval.high)


def summarize_replicates(replicates: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for scenario_id, group in replicates.groupby("scenario_id", sort=False):
        base = {
            "scenario_id": scenario_id,
            "family": group["family"].iloc[0],
            "regular": bool(group["regular"].iloc[0]),
            "replicates": len(group),
            "true_delta": float(group["true_delta"].iloc[0]),
            "mean_zero_cells_p": float(group["zero_cells_p"].mean()),
            "mean_zero_cells_q": float(group["zero_cells_q"].mean()),
            "studentization_valid_rate": float(group["valid_studentization"].mean()),
            "mean_deterministic_ms": float(1000 * group["deterministic_seconds"].mean()),
            "mean_permutation_ms": float(1000 * group["permutation_seconds"].mean()),
            "wald_jackknife_95_coverage": float(
                np.mean(
                    (group["delta_jackknife"] - 1.959963984540054 * group["standard_error"] <= group["true_delta"])
                    & (group["true_delta"] <= group["delta_jackknife"] + 1.959963984540054 * group["standard_error"])
                )
            ),
            "mean_delta_plugin_bias": float(
                (group["delta_plugin"] - group["true_delta"]).mean()
            ),
            "mean_delta_analytic_bias": float(
                (group["delta_analytic"] - group["true_delta"]).mean()
            ),
            "mean_delta_jackknife_bias": float(
                (group["delta_jackknife"] - group["true_delta"]).mean()
            ),
        }
        for column in P_VALUE_COLUMNS:
            method = column.removesuffix("_p")
            valid = group[column].dropna()
            for alpha in (0.10, 0.05):
                rejections = int(np.count_nonzero(valid <= alpha))
                total = int(valid.size)
                rate = rejections / total if total else float("nan")
                low, high = (
                    _wilson_interval(rejections, total)
                    if total
                    else (float("nan"), float("nan"))
                )
                suffix = f"{int(alpha * 100):02d}"
                base[f"{method}_fpr_{suffix}"] = rate
                base[f"{method}_fpr_{suffix}_low"] = low
                base[f"{method}_fpr_{suffix}_high"] = high
                base[f"{method}_valid_n"] = total
        rows.append(base)
    return pd.DataFrame(rows)
