#!/usr/bin/env python3
"""Run one explainable validation of three analytic equal-MI tests."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from matplotlib.colors import TwoSlopeNorm
from scipy.stats import binomtest, norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.random_validation import (  # noqa: E402
    RandomScenario,
    scenario_diagnostics,
)
from differential_mi.distributions import (  # noqa: E402
    interaction_pattern,
    table_with_target_mi_from_interaction,
)
from differential_mi.statistics import influence_variance  # noqa: E402
from differential_mi.scenarios import (  # noqa: E402
    build_distributions,
    power_curve_scenarios,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


ALPHAS = (0.10, 0.05, 0.01)
CALIBRATION_ALPHAS = tuple(index / 1_000 for index in range(101))
MINIMUM_SAMPLE_SIZE = 50
MAXIMUM_SAMPLE_SIZE = 1_000
SHAPES = (
    (2, 2),
    (3, 3),
    (5, 5),
    (8, 8),
)
METHODS = {
    "normal_wald": {
        "label": "Normal Wald",
        "p_value": "normal_p_value",
        "degrees_of_freedom": None,
        "validity": "base_valid",
    },
    "simple_welch": {
        "label": "Simple Welch",
        "p_value": "welch_p_value",
        "degrees_of_freedom": "welch_degrees_of_freedom",
        "validity": "simple_valid",
    },
    "expanded_welch": {
        "label": "Expanded Welch",
        "p_value": "expanded_welch_p_value",
        "degrees_of_freedom": "expanded_welch_degrees_of_freedom",
        "validity": "expanded_valid",
    },
}
REGIMES = {
    "balanced_control": {
        "label": "Balanced control",
        "designs": (0,),
        "description": (
            "Uniform margins, equal sample sizes, and approximately 15 "
            "observations per cell."
        ),
    },
    "moderate_sparse": {
        "label": "Moderate sparsity",
        "designs": (1,),
        "description": (
            "Dominant row and column mass 0.70, equal sample sizes, and "
            "approximately eight observations per cell."
        ),
    },
    "ultra_sparse": {
        "label": "Ultra-sparsity",
        "designs": (2,),
        "description": (
            "Dominant row and column mass 0.90, equal sample sizes, and "
            "approximately three observations per cell."
        ),
    },
    "ultra_imbalanced": {
        "label": "Ultra-sparsity with imbalance",
        "designs": (3,),
        "description": (
            "The same 0.90 margin template and low-density smaller sample, "
            "with a 5:1 sample-size ratio."
        ),
    },
}
REGIME_ORDER = tuple(REGIMES)
DESIGN_TO_REGIME = {
    design: regime
    for regime, specification in REGIMES.items()
    for design in specification["designs"]
}
CONFIGURATIONS = {
    0: {
        "key": "balanced_control",
        "margin_profile": "uniform",
        "dominant_margin_mass": None,
        "target_mi": 0.10,
        "density": 15,
        "minimum_n": 100,
        "sample_size_ratio": 1,
    },
    1: {
        "key": "moderate_sparse",
        "margin_profile": "dominant_0.70",
        "dominant_margin_mass": 0.70,
        "target_mi": 0.10,
        "density": 8,
        "minimum_n": 50,
        "sample_size_ratio": 1,
    },
    2: {
        "key": "ultra_sparse",
        "margin_profile": "dominant_0.90",
        "dominant_margin_mass": 0.90,
        "target_mi": 0.10,
        "density": 3,
        "minimum_n": 50,
        "sample_size_ratio": 1,
    },
    3: {
        "key": "ultra_imbalanced",
        "margin_profile": "dominant_0.90",
        "dominant_margin_mass": 0.90,
        "target_mi": 0.10,
        "density": 3,
        "minimum_n": 50,
        "sample_size_ratio": 5,
    },
}
PROFILE_SETTINGS = {
    "smoke": {
        "null_replicates": 300,
        "population_replicates": 2,
        "power_replicates": 500,
        "batch_size": 150,
        "runtime_repetitions": 20,
        "shape_limit": None,
    },
    "full": {
        "null_replicates": 5_000,
        "population_replicates": 10,
        "power_replicates": 10_000,
        "batch_size": 1_000,
        "runtime_repetitions": 200,
        "shape_limit": None,
    },
}
DEFAULT_SCENARIO_SEED = 2_026_080_501
DEFAULT_SIMULATION_SEED = 2_026_080_502


@dataclass(frozen=True)
class ValidationScenario(RandomScenario):
    """One saved population realization within a design configuration."""

    configuration_id: str
    population_replication: int
    population_seed: int
    margin_profile: str
    dominant_margin_mass: float
    planned_density: int


def _configuration_sample_sizes(
    cells: int,
    *,
    density: int,
    ratio: int,
    minimum_n: int,
) -> tuple[int, int]:
    """Apply the pre-specified sample-size formula for one configuration."""
    n_p = max(minimum_n, cells * density)
    n_q = ratio * n_p
    if not (
        MINIMUM_SAMPLE_SIZE <= n_p <= MAXIMUM_SAMPLE_SIZE
        and MINIMUM_SAMPLE_SIZE <= n_q <= MAXIMUM_SAMPLE_SIZE
    ):
        raise ValueError("Configuration sample sizes exceed experiment bounds.")
    return n_p, n_q


def _fixed_margin(
    size: int,
    dominant_mass: float | None,
    dominant_index: int,
) -> np.ndarray:
    """Construct an exact uniform or one-dominant-category margin."""
    if dominant_mass is None:
        return np.full(size, 1.0 / size)
    if not 1.0 / size < dominant_mass < 1.0:
        raise ValueError("Dominant mass must exceed the uniform category mass.")
    margin = np.full(size, (1.0 - dominant_mass) / (size - 1))
    margin[dominant_index] = dominant_mass
    return margin


def _population_seed(
    base_seed: int,
    shape_index: int,
    design_index: int,
    population_replication: int,
) -> int:
    return int(
        np.random.SeedSequence(
            [base_seed, shape_index, design_index, population_replication]
        ).generate_state(1)[0]
    )


def _structured_interaction(
    rows: int,
    columns: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw from bounded, interpretable interaction families."""
    pattern_name = ("ordinal", "checkerboard", "cyclic")[
        int(rng.integers(3))
    ]
    return interaction_pattern(rows, columns, pattern_name)


def generate_configuration_scenarios(
    seed: int,
    population_replicates: int,
) -> list[ValidationScenario]:
    """Generate replicated populations for the 16 pre-specified design cells."""
    if population_replicates <= 0:
        raise ValueError("Population replicate count must be positive.")

    scenarios: list[ValidationScenario] = []
    for shape_index, (rows, columns) in enumerate(SHAPES):
        cells = rows * columns
        for design_index, design in CONFIGURATIONS.items():
            n_p, n_q = _configuration_sample_sizes(
                cells,
                density=design["density"],
                ratio=design["sample_size_ratio"],
                minimum_n=design["minimum_n"],
            )
            for population_replication in range(population_replicates):
                population_seed = _population_seed(
                    seed,
                    shape_index,
                    design_index,
                    population_replication,
                )
                rng = np.random.default_rng(population_seed)
                last_error: Exception | None = None
                for attempt in range(1, 5_001):
                    try:
                        row_p = _fixed_margin(
                            rows,
                            design["dominant_margin_mass"],
                            0,
                        )
                        column_p = _fixed_margin(
                            columns,
                            design["dominant_margin_mass"],
                            0,
                        )
                        row_q = _fixed_margin(
                            rows,
                            design["dominant_margin_mass"],
                            0,
                        )
                        column_q = _fixed_margin(
                            columns,
                            design["dominant_margin_mass"],
                            0,
                        )
                        probability_p, association_p = (
                            table_with_target_mi_from_interaction(
                                row_p,
                                column_p,
                                design["target_mi"],
                                _structured_interaction(rows, columns, rng),
                            )
                        )
                        probability_q, association_q = (
                            table_with_target_mi_from_interaction(
                                row_q,
                                column_q,
                                design["target_mi"],
                                _structured_interaction(rows, columns, rng),
                            )
                        )
                        probability_p = probability_p[
                            rng.permutation(rows), :
                        ][:, rng.permutation(columns)]
                        probability_q = probability_q[
                            rng.permutation(rows), :
                        ][:, rng.permutation(columns)]
                        if min(probability_p.min(), probability_q.min()) < 1e-12:
                            raise ValueError(
                                "Generated cell probability is too small."
                            )
                        if np.abs(probability_p - probability_q).sum() < 0.05:
                            raise ValueError(
                                "Generated equal-MI pair is too similar."
                            )
                        if min(
                            float(influence_variance(probability_p)),
                            float(influence_variance(probability_q)),
                        ) < 1e-6:
                            raise ValueError(
                                "Generated influence variance is degenerate."
                            )
                    except (RuntimeError, ValueError) as error:
                        last_error = error
                        continue
                    break
                else:
                    raise RuntimeError(
                        f"Failed to generate shape={rows}x{columns}, "
                        f"design={design_index}, population="
                        f"{population_replication}: {last_error}"
                    )

                scenarios.append(
                    ValidationScenario(
                        scenario_id=(
                            f"config_{rows}x{columns}_d{design_index}_"
                            f"p{population_replication:02d}"
                        ),
                        shape_index=shape_index,
                        design_index=design_index,
                        rows=rows,
                        columns=columns,
                        n_p=n_p,
                        n_q=n_q,
                        target_mi=design["target_mi"],
                        margin_alpha_p=np.nan,
                        margin_alpha_q=np.nan,
                        association_p=association_p,
                        association_q=association_q,
                        generation_attempts=attempt,
                        probability_p=probability_p,
                        probability_q=probability_q,
                        configuration_id=(
                            f"{rows}x{columns}_{design['key']}"
                        ),
                        population_replication=population_replication,
                        population_seed=population_seed,
                        margin_profile=design["margin_profile"],
                        dominant_margin_mass=(
                            1.0 / rows
                            if design["dominant_margin_mass"] is None
                            else design["dominant_margin_mass"]
                        ),
                        planned_density=design["density"],
                    )
                )
    return scenarios


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare normal Wald, simple Welch, and expanded Welch on one "
            "broad equal-MI grid."
        )
    )
    parser.add_argument("--profile", choices=PROFILE_SETTINGS, default="smoke")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "supervisor_experiment",
    )
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    parser.add_argument("--null-replicates", type=int)
    parser.add_argument("--population-replicates", type=int)
    parser.add_argument("--power-replicates", type=int)
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--runtime-repetitions", type=int)
    return parser.parse_args()


def _settings(args: argparse.Namespace) -> dict[str, int | None]:
    settings = dict(PROFILE_SETTINGS[args.profile])
    for name in (
        "null_replicates",
        "population_replicates",
        "power_replicates",
        "batch_size",
        "runtime_repetitions",
    ):
        value = getattr(args, name)
        if value is not None:
            settings[name] = value
    if min(
        int(settings["null_replicates"]),
        int(settings["population_replicates"]),
        int(settings["power_replicates"]),
        int(settings["batch_size"]),
        int(settings["runtime_repetitions"]),
    ) <= 0:
        raise ValueError("Replicate, batch, and runtime counts must be positive.")
    return settings


def _method_values(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> dict[str, np.ndarray]:
    return differential_mi_pvalues(
        table_p,
        table_q,
        include_expanded=True,
        include_unbiased_sensitivity=False,
    )


def _regime_for(scenario: RandomScenario) -> str:
    return DESIGN_TO_REGIME[scenario.design_index]


def _scenario_simulation_seeds(
    scenarios: list[RandomScenario],
    seed: int,
) -> dict[str, int]:
    """Assign one deterministic simulation seed to each scenario."""
    children = np.random.SeedSequence(seed).spawn(len(scenarios))
    return {
        scenario.scenario_id: int(child.generate_state(1)[0])
        for scenario, child in zip(scenarios, children)
    }


def _population_metadata(scenario: ValidationScenario) -> dict:
    diagnostics = scenario_diagnostics(scenario)
    diagnostics.pop("margin_alpha_p", None)
    diagnostics.pop("margin_alpha_q", None)
    p = scenario.probability_p
    q = scenario.probability_q
    regime = _regime_for(scenario)
    cells = scenario.rows * scenario.columns
    return {
        **diagnostics,
        "regime": regime,
        "regime_label": REGIMES[regime]["label"],
        "variant": f"population_{scenario.population_replication:02d}",
        "cells": cells,
        "observations_per_cell_p": scenario.n_p / cells,
        "observations_per_cell_q": scenario.n_q / cells,
        "sample_size_ratio_q_to_p": scenario.n_q / scenario.n_p,
        "minimum_joint_expected_pair": min(
            scenario.n_p * float(p.min()),
            scenario.n_q * float(q.min()),
        ),
        "joint_expected_below_1_p": float(np.mean(scenario.n_p * p < 1.0)),
        "joint_expected_below_1_q": float(np.mean(scenario.n_q * q < 1.0)),
        "joint_expected_below_5_p": float(np.mean(scenario.n_p * p < 5.0)),
        "joint_expected_below_5_q": float(np.mean(scenario.n_q * q < 5.0)),
        "minimum_row_expected_p": float(
            scenario.n_p * p.sum(axis=1).min()
        ),
        "minimum_row_expected_q": float(
            scenario.n_q * q.sum(axis=1).min()
        ),
        "minimum_column_expected_p": float(
            scenario.n_p * p.sum(axis=0).min()
        ),
        "minimum_column_expected_q": float(
            scenario.n_q * q.sum(axis=0).min()
        ),
        "maximum_row_margin_p": float(p.sum(axis=1).max()),
        "maximum_column_margin_p": float(p.sum(axis=0).max()),
        "maximum_row_margin_q": float(q.sum(axis=1).max()),
        "maximum_column_margin_q": float(q.sum(axis=0).max()),
        "probability_p_json": json.dumps(p.tolist()),
        "probability_q_json": json.dumps(q.tolist()),
    }


def _sample_diagnostics(tables: np.ndarray) -> dict[str, np.ndarray]:
    counts = np.asarray(tables, dtype=float)
    totals = counts.sum(axis=(1, 2))
    rows = counts.sum(axis=2)
    columns = counts.sum(axis=1)
    expected = rows[:, :, None] * columns[:, None, :] / totals[:, None, None]
    return {
        "zero_fraction": np.mean(counts == 0, axis=(1, 2)),
        "expected_below_1": np.mean(expected < 1.0, axis=(1, 2)),
        "expected_below_5": np.mean(expected < 5.0, axis=(1, 2)),
        "minimum_expected": expected.min(axis=(1, 2)),
        "empty_row_fraction": np.mean(rows == 0, axis=1),
        "empty_column_fraction": np.mean(columns == 0, axis=1),
        "has_empty_margin": np.any(rows == 0, axis=1)
        | np.any(columns == 0, axis=1),
    }


def _wilson(rejections: int, total: int) -> tuple[float, float]:
    if total == 0:
        return np.nan, np.nan
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    return float(interval.low), float(interval.high)


def _wilson_many(
    rejections: np.ndarray,
    total: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized 95% Wilson intervals for a rejection-calibration curve."""
    counts = np.asarray(rejections, dtype=float)
    if total == 0:
        missing = np.full(counts.shape, np.nan)
        return missing, missing.copy()
    z = float(norm.ppf(0.975))
    probability = counts / total
    denominator = 1.0 + z**2 / total
    center = (probability + z**2 / (2.0 * total)) / denominator
    half_width = (
        z
        * np.sqrt(
            probability * (1.0 - probability) / total
            + z**2 / (4.0 * total**2)
        )
        / denominator
    )
    return center - half_width, center + half_width


def _critical_values(
    method: str,
    values: dict[str, np.ndarray],
    method_valid: np.ndarray,
) -> np.ndarray | float:
    """Return the 95% reference cutoff selected by one method."""
    if method == "normal_wald":
        return norm.ppf(0.975)
    specification = METHODS[method]
    return t.ppf(
        0.975,
        df=values[specification["degrees_of_freedom"]][method_valid],
    )


def _simulate_null_scenario(
    scenario: RandomScenario,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> tuple[list[dict], list[dict], dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)
    p_value_samples = {
        method: np.full(replicates, np.nan, dtype=float)
        for method in METHODS
    }
    method_counts = {
        method: {
            "valid": 0,
            "coverage": 0,
            "rejections": {alpha: 0 for alpha in ALPHAS},
            "calibration_rejections": np.zeros(
                len(CALIBRATION_ALPHAS),
                dtype=np.int64,
            ),
            "degrees_of_freedom": [],
        }
        for method in METHODS
    }
    valid_count = 0
    delta_sum = 0.0
    delta_square_sum = 0.0
    standard_error_sum = 0.0
    diagnostic_sums = {
        f"{name}_{group}": 0.0
        for name in (
            "zero_fraction",
            "expected_below_1",
            "expected_below_5",
            "minimum_expected",
            "empty_row_fraction",
            "empty_column_fraction",
            "has_empty_margin",
        )
        for group in ("p", "q")
    }
    true_delta = float(scenario_diagnostics(scenario)["true_delta"])

    for start in range(0, replicates, batch_size):
        count = min(batch_size, replicates - start)
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.reshape(-1),
            size=count,
        ).reshape(count, scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_q.reshape(-1),
            size=count,
        ).reshape(count, scenario.rows, scenario.columns)
        values = _method_values(table_p, table_q)
        base_valid = values["base_valid"]
        valid_count += int(np.count_nonzero(base_valid))

        delta = values["delta_corrected"][base_valid]
        standard_error = values["standard_error"][base_valid]
        delta_error = delta - true_delta
        delta_sum += float(np.sum(delta_error))
        delta_square_sum += float(np.sum(delta_error**2))
        standard_error_sum += float(np.sum(standard_error))

        for method, specification in METHODS.items():
            method_valid = values[specification["validity"]]
            method_counts[method]["valid"] += int(
                np.count_nonzero(method_valid)
            )
            p_values = values[specification["p_value"]][method_valid]
            batch_p_values = np.full(count, np.nan, dtype=float)
            batch_p_values[method_valid] = p_values
            p_value_samples[method][start : start + count] = batch_p_values
            for alpha in ALPHAS:
                method_counts[method]["rejections"][alpha] += int(
                    np.count_nonzero(p_values <= alpha)
                )
            method_counts[method]["calibration_rejections"] += np.searchsorted(
                np.sort(p_values),
                CALIBRATION_ALPHAS,
                side="right",
            )
            df_column = specification["degrees_of_freedom"]
            if df_column is not None:
                degrees_of_freedom = values[df_column][method_valid]
                finite_df = degrees_of_freedom[
                    np.isfinite(degrees_of_freedom)
                ]
                if finite_df.size:
                    method_counts[method]["degrees_of_freedom"].append(
                        finite_df
                    )
            critical = _critical_values(method, values, method_valid)
            method_counts[method]["coverage"] += int(
                    np.count_nonzero(
                        np.abs(
                            values["delta_corrected"][method_valid]
                            - true_delta
                        )
                        <= critical
                        * values["standard_error"][method_valid]
                    )
            )

        for group, tables in (("p", table_p), ("q", table_q)):
            diagnostics = _sample_diagnostics(tables)
            for name, values_array in diagnostics.items():
                diagnostic_sums[f"{name}_{group}"] += float(
                    np.sum(values_array)
                )

    common = _population_metadata(scenario)
    common.update(
        {
            "simulation_seed": seed,
            "replicates": replicates,
            "estimator_valid_replicates": valid_count,
            "estimator_valid_rate": valid_count / replicates,
            "mean_delta_error": (
                delta_sum / valid_count if valid_count else np.nan
            ),
            "empirical_delta_sd": np.sqrt(
                max(
                    0.0,
                    (
                        delta_square_sum
                        - delta_sum**2 / valid_count
                    )
                    / (valid_count - 1),
                )
            )
            if valid_count > 1
            else np.nan,
            "mean_standard_error": (
                standard_error_sum / valid_count if valid_count else np.nan
            ),
            **{
                f"mean_sample_{name}": total / replicates
                for name, total in diagnostic_sums.items()
            },
        }
    )

    rows = []
    calibration_rows = []
    for method, specification in METHODS.items():
        method_valid_count = method_counts[method]["valid"]
        row = {
            **common,
            "method": method,
            "method_label": specification["label"],
            "valid_replicates": method_valid_count,
            "valid_rate": method_valid_count / replicates,
            "coverage_95": (
                method_counts[method]["coverage"] / method_valid_count
                if method_valid_count
                else np.nan
            ),
        }
        df_parts = method_counts[method]["degrees_of_freedom"]
        if df_parts:
            degrees_of_freedom = np.concatenate(df_parts)
            row["median_effective_df"] = float(
                np.median(degrees_of_freedom)
            )
            row["p05_effective_df"] = float(
                np.quantile(degrees_of_freedom, 0.05)
            )
        else:
            row["median_effective_df"] = np.nan
            row["p05_effective_df"] = np.nan
        for alpha in ALPHAS:
            label = f"{int(round(100 * alpha)):02d}"
            rejections = method_counts[method]["rejections"][alpha]
            fpr = (
                rejections / method_valid_count
                if method_valid_count
                else np.nan
            )
            low, high = _wilson(rejections, method_valid_count)
            row[f"fpr_{label}"] = fpr
            row[f"fpr_{label}_low"] = low
            row[f"fpr_{label}_high"] = high
            row[f"absolute_fpr_error_{label}"] = abs(fpr - alpha)
        rows.append(row)

        calibration_rejections = method_counts[method][
            "calibration_rejections"
        ]
        calibration_rates = (
            calibration_rejections / method_valid_count
            if method_valid_count
            else np.full(len(CALIBRATION_ALPHAS), np.nan)
        )
        calibration_low, calibration_high = _wilson_many(
            calibration_rejections,
            method_valid_count,
        )
        calibration_common = {
            "scenario_id": scenario.scenario_id,
            "configuration_id": common["configuration_id"],
            "population_replication": common["population_replication"],
            "shape_index": scenario.shape_index,
            "design_index": scenario.design_index,
            "rows": scenario.rows,
            "columns": scenario.columns,
            "n_p": scenario.n_p,
            "n_q": scenario.n_q,
            "target_mi": scenario.target_mi,
            "regime": common["regime"],
            "regime_label": common["regime_label"],
            "margin_profile": common["margin_profile"],
            "method": method,
            "method_label": specification["label"],
            "valid_replicates": method_valid_count,
            "valid_rate": method_valid_count / replicates,
        }
        for index, nominal_alpha in enumerate(CALIBRATION_ALPHAS):
            rejection_rate = float(calibration_rates[index])
            calibration_rows.append(
                {
                    **calibration_common,
                    "nominal_alpha": nominal_alpha,
                    "rejections": int(calibration_rejections[index]),
                    "rejection_rate": rejection_rate,
                    "rejection_rate_low": float(calibration_low[index]),
                    "rejection_rate_high": float(calibration_high[index]),
                    "absolute_calibration_error": abs(
                        rejection_rate - nominal_alpha
                    ),
                }
            )
    return rows, calibration_rows, p_value_samples


def _aggregate_rejection_calibration(
    scenario_calibration: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize rejection curves while retaining population heterogeneity."""
    summary = (
        scenario_calibration.groupby(
            [
                "regime",
                "regime_label",
                "method",
                "method_label",
                "nominal_alpha",
            ],
            sort=False,
        )
        .agg(
            population_pairs=("scenario_id", "nunique"),
            mean_rejection_rate=("rejection_rate", "mean"),
            median_rejection_rate=("rejection_rate", "median"),
            p10_rejection_rate=(
                "rejection_rate",
                lambda values: values.quantile(0.10),
            ),
            p90_rejection_rate=(
                "rejection_rate",
                lambda values: values.quantile(0.90),
            ),
            minimum_rejection_rate=("rejection_rate", "min"),
            maximum_rejection_rate=("rejection_rate", "max"),
            mean_absolute_calibration_error=(
                "absolute_calibration_error",
                "mean",
            ),
        )
        .reset_index()
    )
    regime_order = {regime: index for index, regime in enumerate(REGIME_ORDER)}
    method_order = {method: index for index, method in enumerate(METHODS)}
    summary["_regime_order"] = summary["regime"].map(regime_order)
    summary["_method_order"] = summary["method"].map(method_order)
    return (
        summary.sort_values(
            ["_regime_order", "_method_order", "nominal_alpha"]
        )
        .drop(columns=["_regime_order", "_method_order"])
        .reset_index(drop=True)
    )


def _aggregate_scenarios(scenario_results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    regime_groups = [
        (regime, scenario_results[scenario_results["regime"].eq(regime)])
        for regime in REGIME_ORDER
    ]
    regime_groups.append(("all", scenario_results))
    for regime, regime_frame in regime_groups:
        normal = regime_frame[regime_frame["method"].eq("normal_wald")].set_index(
            "scenario_id"
        )
        for method, specification in METHODS.items():
            group = regime_frame[regime_frame["method"].eq(method)].copy()
            group = group.set_index("scenario_id")
            row = {
                "regime": regime,
                "regime_label": (
                    "All regimes" if regime == "all" else REGIMES[regime]["label"]
                ),
                "method": method,
                "method_label": specification["label"],
                "population_pairs": len(group),
                "replicates_per_population": int(group["replicates"].iloc[0]),
                "mean_valid_rate": float(group["valid_rate"].mean()),
                "mean_coverage_95": float(group["coverage_95"].mean()),
                "median_effective_df": float(
                    group["median_effective_df"].median()
                ),
            }
            for alpha in ALPHAS:
                label = f"{int(round(100 * alpha)):02d}"
                fpr = group[f"fpr_{label}"]
                error = group[f"absolute_fpr_error_{label}"]
                normal_error = normal[f"absolute_fpr_error_{label}"]
                row[f"mean_fpr_{label}"] = float(fpr.mean())
                row[f"mean_absolute_fpr_error_{label}"] = float(error.mean())
                row[f"median_absolute_fpr_error_{label}"] = float(error.median())
                row[f"minimum_fpr_{label}"] = float(fpr.min())
                row[f"maximum_fpr_{label}"] = float(fpr.max())
                row[f"improved_vs_normal_{label}"] = int(
                    (error < normal_error).sum()
                )
                row[f"worsened_vs_normal_{label}"] = int(
                    (error > normal_error).sum()
                )
                row[f"tied_vs_normal_{label}"] = int(
                    (error == normal_error).sum()
                )
            rows.append(row)
    return pd.DataFrame(rows)


def _aggregate_configurations(
    scenario_results: pd.DataFrame,
) -> pd.DataFrame:
    """Average population-level results within each of the 16 design cells."""
    rows = []
    grouped = scenario_results.groupby(
        ["shape_index", "design_index", "configuration_id", "method"],
        sort=False,
    )
    for (_, _, configuration_id, method), group in grouped:
        first = group.iloc[0]
        row = {
            "configuration_id": configuration_id,
            "shape_index": int(first["shape_index"]),
            "design_index": int(first["design_index"]),
            "rows": int(first["rows"]),
            "columns": int(first["columns"]),
            "condition": first["regime"],
            "condition_label": first["regime_label"],
            "margin_profile": first["margin_profile"],
            "dominant_margin_mass": float(first["dominant_margin_mass"]),
            "target_mi": float(first["target_mi"]),
            "n_p": int(first["n_p"]),
            "n_q": int(first["n_q"]),
            "population_pairs": int(group["scenario_id"].nunique()),
            "replicates_per_population": int(group["replicates"].iloc[0]),
            "method": method,
            "method_label": METHODS[method]["label"],
            "mean_valid_rate": float(group["valid_rate"].mean()),
            "mean_coverage_95": float(group["coverage_95"].mean()),
            "median_effective_df": float(
                group["median_effective_df"].median()
            ),
        }
        for alpha in ALPHAS:
            label = f"{int(round(100 * alpha)):02d}"
            fpr = group[f"fpr_{label}"]
            error = group[f"absolute_fpr_error_{label}"]
            row[f"mean_fpr_{label}"] = float(fpr.mean())
            row[f"population_sd_fpr_{label}"] = float(fpr.std(ddof=1))
            row[f"population_se_fpr_{label}"] = float(
                fpr.std(ddof=1) / np.sqrt(len(fpr))
            )
            row[f"mean_absolute_fpr_error_{label}"] = float(error.mean())
            row[f"minimum_fpr_{label}"] = float(fpr.min())
            row[f"maximum_fpr_{label}"] = float(fpr.max())
        rows.append(row)
    return (
        pd.DataFrame(rows)
        .sort_values(["shape_index", "design_index", "method"])
        .reset_index(drop=True)
    )


def _simulate_power(
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    scenarios = power_curve_scenarios()
    children = np.random.SeedSequence(seed).spawn(len(scenarios))
    for scenario, child in zip(scenarios, children):
        scenario_seed = int(child.generate_state(1)[0])
        probability_p, probability_q, diagnostics = build_distributions(scenario)
        method_counts = {
            method: {
                "valid": 0,
                "rejections": 0,
                "coverage": 0,
                "df": [],
            }
            for method in METHODS
        }
        rng = np.random.default_rng(scenario_seed)
        for start in range(0, replicates, batch_size):
            count = min(batch_size, replicates - start)
            table_p = rng.multinomial(
                scenario.n_p,
                probability_p.reshape(-1),
                size=count,
            ).reshape(count, scenario.rows, scenario.columns)
            table_q = rng.multinomial(
                scenario.n_q,
                probability_q.reshape(-1),
                size=count,
            ).reshape(count, scenario.rows, scenario.columns)
            values = _method_values(table_p, table_q)
            for method, specification in METHODS.items():
                method_valid = values[specification["validity"]]
                method_counts[method]["valid"] += int(
                    np.count_nonzero(method_valid)
                )
                p_values = values[specification["p_value"]][method_valid]
                method_counts[method]["rejections"] += int(
                    np.count_nonzero(p_values <= 0.05)
                )
                delta_error = (
                    values["delta_corrected"][method_valid]
                    - diagnostics["true_delta"]
                )
                standard_error = values["standard_error"][method_valid]
                df_column = specification["degrees_of_freedom"]
                if df_column is not None:
                    df = values[df_column][method_valid]
                    finite_df = df[np.isfinite(df)]
                    if finite_df.size:
                        method_counts[method]["df"].append(finite_df)
                critical = _critical_values(method, values, method_valid)
                method_counts[method]["coverage"] += int(
                    np.count_nonzero(
                        np.abs(delta_error) <= critical * standard_error
                    )
                )
        for method, specification in METHODS.items():
            df_parts = method_counts[method]["df"]
            method_valid_count = method_counts[method]["valid"]
            rows.append(
                {
                    **scenario.to_dict(),
                    **diagnostics,
                    "simulation_seed": scenario_seed,
                    "replicates": replicates,
                    "valid_rate": method_valid_count / replicates,
                    "method": method,
                    "method_label": specification["label"],
                    "power_05": (
                        method_counts[method]["rejections"] / method_valid_count
                        if method_valid_count
                        else np.nan
                    ),
                    "coverage_95": (
                        method_counts[method]["coverage"] / method_valid_count
                        if method_valid_count
                        else np.nan
                    ),
                    "median_effective_df": (
                        float(np.median(np.concatenate(df_parts)))
                        if df_parts
                        else np.nan
                    ),
                }
            )
    return pd.DataFrame(rows)


def _runtime_audit(
    scenarios: list[RandomScenario],
    *,
    repetitions: int,
    seed: int,
) -> pd.DataFrame:
    target_shapes = ((2, 2), (3, 3), (5, 5), (8, 8))
    selected = []
    for shape in target_shapes:
        matches = [
            scenario
            for scenario in scenarios
            if (scenario.rows, scenario.columns) == shape
            and scenario.design_index == 0
        ]
        if matches:
            selected.append(matches[0])
    rng = np.random.default_rng(seed)
    rows = []
    for scenario in selected:
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.reshape(-1),
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_q.reshape(-1),
        ).reshape(scenario.rows, scenario.columns)

        def normal_method() -> None:
            differential_mi_pvalues(
                table_p,
                table_q,
                include_simple=False,
                include_expanded=False,
                include_unbiased_sensitivity=False,
            )

        def simple_method() -> None:
            differential_mi_pvalues(
                table_p,
                table_q,
                include_simple=True,
                include_expanded=False,
                include_unbiased_sensitivity=False,
            )

        def expanded_method() -> None:
            differential_mi_pvalues(
                table_p,
                table_q,
                include_simple=True,
                include_expanded=True,
                include_unbiased_sensitivity=False,
            )

        functions = {
            "normal_wald": normal_method,
            "simple_welch": simple_method,
            "expanded_welch": expanded_method,
        }
        for function in functions.values():
            function()
        timings = {method: [] for method in METHODS}
        for _ in range(repetitions):
            for method, function in functions.items():
                start = perf_counter()
                function()
                timings[method].append(perf_counter() - start)
        for method, specification in METHODS.items():
            values = np.asarray(timings[method])
            rows.append(
                {
                    "rows": scenario.rows,
                    "columns": scenario.columns,
                    "cells": scenario.rows * scenario.columns,
                    "n_p": scenario.n_p,
                    "n_q": scenario.n_q,
                    "repetitions": repetitions,
                    "method": method,
                    "method_label": specification["label"],
                    "reference_route": specification["label"],
                    "median_time_ms": 1_000.0 * float(np.median(values)),
                    "p05_time_ms": 1_000.0 * float(np.quantile(values, 0.05)),
                    "p95_time_ms": 1_000.0 * float(np.quantile(values, 0.95)),
                }
            )
    runtime = pd.DataFrame(rows)
    normal = runtime[runtime["method"].eq("normal_wald")].set_index(
        ["rows", "columns"]
    )["median_time_ms"]
    runtime["relative_to_normal"] = [
        row.median_time_ms / normal.loc[(row.rows, row.columns)]
        for row in runtime.itertuples(index=False)
    ]
    return runtime


def _plot_calibration(summary: pd.DataFrame, output_dir: Path) -> None:
    columns = 2
    rows = int(np.ceil(len(REGIME_ORDER) / columns))
    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(5 * columns, 4.6 * rows),
        sharey=True,
    )
    axes = np.asarray(axes).reshape(-1)
    colors = ("#355070", "#D97745", "#4F7C64", "#A33B20")
    width = 0.19
    x = np.arange(len(ALPHAS))
    for axis, regime in zip(axes, REGIME_ORDER):
        group = summary[summary["regime"].eq(regime)].set_index("method")
        for index, (method, specification) in enumerate(METHODS.items()):
            errors = [
                group.loc[
                    method,
                    f"mean_absolute_fpr_error_{int(round(alpha * 100)):02d}",
                ]
                for alpha in ALPHAS
            ]
            axis.bar(
                x + (index - (len(METHODS) - 1) / 2) * width,
                errors,
                width,
                color=colors[index],
                label=specification["label"],
            )
        axis.set_xticks(x, [f"{alpha:.2f}" for alpha in ALPHAS])
        axis.set_title(REGIMES[regime]["label"])
        axis.set_xlabel("Nominal alpha")
        axis.grid(axis="y", alpha=0.2)
    unused_axes = axes[len(REGIME_ORDER) :]
    for axis in unused_axes:
        axis.set_axis_off()
    axes[0].set_ylabel("Mean absolute false-positive-rate error")
    legend_axis = unused_axes[0] if len(unused_axes) else axes[-1]
    handles, labels = axes[0].get_legend_handles_labels()
    legend_axis.legend(handles, labels, loc="center", frameon=False)
    figure.suptitle("Equal-MI null calibration by sampling condition")
    figure.tight_layout()
    figure.savefig(output_dir / "calibration_summary.png", dpi=180)
    plt.close(figure)


def _plot_configuration_fpr(
    configurations: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Show the alpha=0.05 false-positive rate in every design cell."""
    figure = plt.figure(figsize=(16.2, 5.2))
    grid = figure.add_gridspec(
        1,
        len(METHODS) + 1,
        width_ratios=(1.0, 1.0, 1.0, 0.045),
        wspace=0.30,
    )
    axes = [figure.add_subplot(grid[0, index]) for index in range(len(METHODS))]
    color_axis = figure.add_subplot(grid[0, -1])
    condition_labels = [
        "Balanced\ncontrol",
        "Moderate\nsparsity",
        "Ultra-\nsparsity",
        "Ultra + 5:1\nimbalance",
    ]
    shape_labels = [f"{rows}x{columns}" for rows, columns in SHAPES]
    color_norm = TwoSlopeNorm(vmin=0.0, vcenter=0.05, vmax=0.12)
    image = None
    for axis, (method, specification) in zip(axes, METHODS.items()):
        method_frame = configurations[configurations["method"].eq(method)]
        values = np.full((len(SHAPES), len(CONFIGURATIONS)), np.nan)
        for row in method_frame.itertuples(index=False):
            values[row.shape_index, row.design_index] = row.mean_fpr_05
        image = axis.imshow(values, cmap="RdBu_r", norm=color_norm)
        for row_index in range(values.shape[0]):
            for column_index in range(values.shape[1]):
                value = values[row_index, column_index]
                axis.text(
                    column_index,
                    row_index,
                    f"{value:.3f}",
                    ha="center",
                    va="center",
                    fontsize=10,
                    color="black",
                )
        axis.set_xticks(range(len(condition_labels)), condition_labels)
        axis.set_yticks(range(len(shape_labels)), shape_labels)
        axis.set_title(specification["label"], fontsize=12)
        axis.set_xlabel("Sampling condition")
        axis.tick_params(axis="both", length=0)
    axes[0].set_ylabel("Table shape")
    figure.suptitle(
        "False-positive rate at nominal alpha = 0.05",
        fontsize=16,
        fontweight="semibold",
    )
    color_bar = figure.colorbar(image, cax=color_axis)
    color_bar.set_label("False-positive rate")
    figure.subplots_adjust(left=0.07, right=0.94, bottom=0.16, top=0.84)
    figure.savefig(output_dir / "configuration_fpr.png", dpi=220)
    figure.savefig(output_dir / "configuration_fpr.pdf")
    plt.close(figure)


def _plot_rejection_calibration(
    calibration: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Plot empirical null rejection rates over the lower p-value tail."""
    columns = 2
    rows = int(np.ceil(len(REGIME_ORDER) / columns))
    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(11.5, 10.8),
        sharex=True,
        sharey=True,
    )
    axes = np.asarray(axes).reshape(-1)
    styles = {
        "normal_wald": {"color": "#24557A", "linewidth": 2.0},
        "simple_welch": {
            "color": "#D17A22",
            "linewidth": 1.8,
            "linestyle": "--",
        },
        "expanded_welch": {"color": "#23856D", "linewidth": 2.4},
    }
    axis_limit = 0.115

    for axis, regime in zip(axes, REGIME_ORDER):
        regime_frame = calibration[calibration["regime"].eq(regime)]
        axis.plot(
            [0.0, axis_limit],
            [0.0, axis_limit],
            color="#787878",
            linewidth=1.2,
            linestyle=":",
            label="Ideal",
            zorder=1,
        )
        for method, specification in METHODS.items():
            curve = regime_frame[regime_frame["method"].eq(method)].sort_values(
                "nominal_alpha"
            )
            alpha = curve["nominal_alpha"].to_numpy()
            mean = curve["mean_rejection_rate"].to_numpy()
            lower = curve["p10_rejection_rate"].to_numpy()
            upper = curve["p90_rejection_rate"].to_numpy()
            style = styles[method]
            axis.fill_between(
                alpha,
                lower,
                upper,
                color=style["color"],
                alpha=0.075,
                linewidth=0,
                zorder=2,
            )
            axis.plot(
                alpha,
                mean,
                label=specification["label"],
                markevery=10,
                marker="o",
                markersize=2.6,
                zorder=3,
                **style,
            )
        axis.axvline(0.05, color="#B6B6B6", linewidth=0.8, linestyle="--")
        axis.set_title(REGIMES[regime]["label"], fontsize=11.5, pad=8)
        axis.set_xlim(0.0, axis_limit)
        axis.set_ylim(0.0, axis_limit)
        axis.set_aspect("equal", adjustable="box")
        axis.grid(color="#D9D9D9", linewidth=0.5, alpha=0.45)
        axis.set_axisbelow(True)

    for axis in axes[len(REGIME_ORDER) :]:
        axis.set_axis_off()
    for index, axis in enumerate(axes[: len(REGIME_ORDER)]):
        if index % columns == 0:
            axis.set_ylabel("Actual rejection rate")
        if index // columns == rows - 1:
            axis.set_xlabel("Nominal significance level")
        axis.set_xticks((0.00, 0.025, 0.05, 0.075, 0.10))
        axis.set_yticks((0.00, 0.025, 0.05, 0.075, 0.10))

    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=4,
        frameon=False,
    )
    figure.suptitle(
        "Rejection calibration under the equal-MI null",
        fontsize=17,
        fontweight="semibold",
        y=0.995,
    )
    figure.text(
        0.5,
        0.972,
        "Diagonal = perfect calibration; shading = 10th-90th percentile across population pairs",
        ha="center",
        va="top",
        fontsize=10.5,
        color="#4D4D4D",
    )
    figure.tight_layout(rect=(0.02, 0.02, 0.98, 0.94))
    figure.savefig(output_dir / "rejection_calibration.png", dpi=220)
    figure.savefig(output_dir / "rejection_calibration.pdf")
    plt.close(figure)


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
                rendered.append(
                    "NA" if not np.isfinite(value) else f"{value:.{digits}f}"
                )
            else:
                rendered.append(str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def _write_report(
    output_dir: Path,
    *,
    profile: str,
    settings: dict,
    scenario_results: pd.DataFrame,
    summary: pd.DataFrame,
    configurations: pd.DataFrame,
    power: pd.DataFrame,
    runtime: pd.DataFrame,
) -> None:
    key_rows = summary[summary["regime"].isin(REGIME_ORDER)][
        [
            "regime_label",
            "method_label",
            "mean_fpr_05",
            "mean_absolute_fpr_error_05",
            "mean_fpr_01",
            "mean_absolute_fpr_error_01",
            "mean_valid_rate",
            "mean_coverage_95",
        ]
    ].rename(
        columns={
            "regime_label": "Condition",
            "method_label": "Method",
            "mean_fpr_05": "FPR at 0.05",
            "mean_absolute_fpr_error_05": "Error at 0.05",
            "mean_fpr_01": "FPR at 0.01",
            "mean_absolute_fpr_error_01": "Error at 0.01",
            "mean_valid_rate": "Valid rate",
            "mean_coverage_95": "95% coverage",
        }
    )
    overall = summary[summary["regime"].eq("all")][
        [
            "method_label",
            "mean_absolute_fpr_error_10",
            "mean_absolute_fpr_error_05",
            "mean_absolute_fpr_error_01",
            "mean_valid_rate",
            "mean_coverage_95",
        ]
    ].rename(
        columns={
            "method_label": "Method",
            "mean_absolute_fpr_error_10": "MAE at 0.10",
            "mean_absolute_fpr_error_05": "MAE at 0.05",
            "mean_absolute_fpr_error_01": "MAE at 0.01",
            "mean_valid_rate": "Mean valid rate",
            "mean_coverage_95": "95% coverage",
        }
    )
    power_view = power[
        ["scenario_id", "true_delta", "method_label", "power_05", "coverage_95"]
    ].rename(
        columns={
            "scenario_id": "Scenario",
            "true_delta": "True MI difference",
            "method_label": "Method",
            "power_05": "Power at 0.05",
            "coverage_95": "95% coverage",
        }
    )
    runtime_view = runtime[
        [
            "rows",
            "columns",
            "method_label",
            "reference_route",
            "median_time_ms",
            "relative_to_normal",
        ]
    ].rename(
        columns={
            "rows": "Rows",
            "columns": "Columns",
            "method_label": "Method",
            "reference_route": "Route",
            "median_time_ms": "Median ms",
            "relative_to_normal": "Relative to Wald",
        }
    )
    configuration_index = [
        "shape_index",
        "design_index",
        "rows",
        "columns",
        "condition_label",
        "n_p",
        "n_q",
    ]
    configuration_view = (
        configurations.pivot(
            index=configuration_index,
            columns="method",
            values="mean_fpr_05",
        )
        .reset_index()
        .sort_values(["shape_index", "design_index"])
    )
    expanded_valid = (
        configurations[configurations["method"].eq("expanded_welch")]
        .set_index(configuration_index)["mean_valid_rate"]
    )
    configuration_view["expanded_valid"] = [
        expanded_valid.loc[tuple(row)]
        for row in configuration_view[configuration_index].itertuples(
            index=False,
            name=None,
        )
    ]
    configuration_view["Shape"] = [
        f"{rows}x{columns}"
        for rows, columns in configuration_view[["rows", "columns"]].itertuples(
            index=False,
            name=None,
        )
    ]
    configuration_view = configuration_view[
        [
            "Shape",
            "condition_label",
            "n_p",
            "n_q",
            "normal_wald",
            "simple_welch",
            "expanded_welch",
            "expanded_valid",
        ]
    ].rename(
        columns={
            "condition_label": "Condition",
            "n_p": "n_P",
            "n_q": "n_Q",
            "normal_wald": "Normal Wald FPR",
            "simple_welch": "Simple Welch FPR",
            "expanded_welch": "Expanded Welch FPR",
            "expanded_valid": "Expanded valid rate",
        }
    )
    condition_comparisons = {}
    for regime in REGIME_ORDER:
        condition = summary[summary["regime"].eq(regime)].set_index("method")
        condition_comparisons[regime] = {
            "normal_fpr": condition.loc["normal_wald", "mean_fpr_05"],
            "expanded_fpr": condition.loc["expanded_welch", "mean_fpr_05"],
            "normal_error": condition.loc[
                "normal_wald", "mean_absolute_fpr_error_05"
            ],
            "expanded_error": condition.loc[
                "expanded_welch", "mean_absolute_fpr_error_05"
            ],
        }
    power_pivot = power.pivot(
        index="scenario_id",
        columns="method",
        values="power_05",
    )
    expanded_mean_power_loss = float(
        (power_pivot["normal_wald"] - power_pivot["expanded_welch"]).mean()
    )
    expanded_max_power_loss = float(
        (power_pivot["normal_wald"] - power_pivot["expanded_welch"]).max()
    )
    lines = [
        "# Supervisor Experiment: Differential Mutual Information",
        "",
        f"Profile: `{profile}`. Each of the "
        f"{configurations['configuration_id'].nunique()} design configurations used "
        f"`{settings['population_replicates']}` independently generated population "
        f"pairs, with `{settings['null_replicates']:,}` sampled table pairs per "
        "population pair.",
        "",
        "## Experiment in one sentence",
        "",
        "Generate two different categorical populations with exactly equal true",
        "mutual information, repeatedly sample one table from each, and check how",
        "often each analytic test incorrectly rejects equality.",
        "",
        "## Design",
        "",
        "The null grid crosses four table shapes with four sampling conditions,",
        f"giving {configurations['configuration_id'].nunique()} configurations and "
        f"{scenario_results['scenario_id'].nunique()}",
        "saved population pairs. Every method sees",
        "the same table pairs and uses the same bias-corrected MI difference and",
        "standard error.",
        "",
    ]
    for regime in REGIME_ORDER:
        lines.append(
            f"- **{REGIMES[regime]['label']}:** "
            f"{REGIMES[regime]['description']}"
        )
    lines.extend(
        [
            "",
            "The methods differ only in reference calibration: normal Wald uses",
            "a standard normal distribution, simple Welch uses ordinary `n-1`",
            "component degrees of freedom, and expanded Welch estimates component",
            "degrees of freedom from the MI-variance influence function.",
            "",
            "## Rejection calibration",
            "",
            "The figure traces the empirical rejection probability over nominal",
            "significance levels from 0 to 0.10. A calibrated test follows the",
            "diagonal. Curves above it are liberal and curves below it are",
            "conservative. Each line is the equal-weight mean across population",
            "pairs in that condition; shading spans their 10th to 90th percentiles.",
            "",
            "![Rejection calibration](rejection_calibration.png)",
            "",
            "## Results for all 16 configurations",
            "",
            "Each row averages the independently generated population pairs in one",
            "fixed design cell. The target false-positive rate is 0.05.",
            "",
            "![Configuration false-positive rates](configuration_fpr.png)",
            "",
            _markdown(configuration_view),
            "",
            "## Results averaged by sampling condition",
            "",
            _markdown(key_rows),
            "",
            "False-positive-rate error is the absolute difference between observed",
            "and nominal rejection rates among valid calculations, so lower is",
            "better. Validity is reported separately so undefined calculations",
            "are not hidden by conditioning only on successful results.",
            "",
            "## Overall summary",
            "",
            _markdown(overall),
            "",
            "## Direct interpretation",
            "",
            "- The condition-level comparisons below report the direct change",
            "  from Normal Wald to Expanded Welch at alpha 0.05.",
            *[
                f"- **{REGIMES[regime]['label']}:** "
                f"mean FPR {values['normal_fpr']:.5f} to "
                f"{values['expanded_fpr']:.5f}; mean absolute error "
                f"{values['normal_error']:.5f} to "
                f"{values['expanded_error']:.5f}."
                for regime, values in condition_comparisons.items()
            ],
            f"- Across the {power['scenario_id'].nunique()} power scenarios, "
            "expanded Welch lost",
            f"  `{expanded_mean_power_loss:.4f}` power on average and at most",
            f"  `{expanded_max_power_loss:.4f}` relative to normal Wald.",
            "- The simple Welch correction changed both calibration and power only",
            "  slightly, consistent with its usually large effective degrees of freedom.",
            "- Scenario-level Wilson intervals, sparsity diagnostics, validity rates,",
            "  and effective degrees of freedom are retained in `scenario_results.csv`.",
            "",
            "## Power",
            "",
            _markdown(power_view, 4),
            "",
            "## Runtime",
            "",
            _markdown(runtime_view, 4),
            "",
            "Runtime includes the complete calculation from the two count tables.",
            "All three timings use the same implementation path. Every method",
            "remains deterministic and scans each table a fixed number of times.",
            "",
            "## Output map",
            "",
            "- `population_scenarios.csv`: the fixed generating distributions and",
            "  difficulty diagnostics.",
            "- `scenario_results.csv`: every scenario-method result.",
            "- `configuration_summary.csv`: the 16 design-cell summaries.",
            "- `regime_summary.csv`: the presentation-level aggregate table.",
            "- `rejection_calibration_scenarios.csv`: scenario-level rejection",
            "  curves over 101 nominal significance levels.",
            "- `rejection_calibration_regimes.csv`: mean curves and population",
            "  variability bands for each regime and method.",
            "- `null_pvalues.npz`: complete null p-value arrays for follow-up",
            "  calibration or Q-Q plots without rerunning the simulation.",
            "- `power_summary.csv`: alternative-hypothesis power and coverage.",
            "- `runtime_summary.csv`: end-to-end timing by table size.",
            "- `calibration_summary.png`: one visual comparison across regimes.",
            "- `configuration_fpr.png` and `.pdf`: the 4x4 design-cell results.",
            "- `rejection_calibration.png` and `.pdf`: lower-tail rejection",
            "  calibration with scenario-variability bands.",
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
    run_start = perf_counter()

    scenarios = generate_configuration_scenarios(
        args.scenario_seed,
        population_replicates=int(settings["population_replicates"]),
    )
    scenarios.sort(
        key=lambda scenario: (scenario.shape_index, scenario.design_index)
    )
    if settings["shape_limit"] is not None:
        scenarios = [
            scenario
            for scenario in scenarios
            if scenario.shape_index < int(settings["shape_limit"])
        ]
    if any(
        not (
            MINIMUM_SAMPLE_SIZE <= scenario.n_p <= MAXIMUM_SAMPLE_SIZE
            and MINIMUM_SAMPLE_SIZE <= scenario.n_q <= MAXIMUM_SAMPLE_SIZE
        )
        for scenario in scenarios
    ):
        raise RuntimeError("Generated scenario violates the sample-size bounds.")
    population_frame = pd.DataFrame(
        [_population_metadata(scenario) for scenario in scenarios]
    )
    scenario_seeds = _scenario_simulation_seeds(
        scenarios,
        args.simulation_seed,
    )
    scenario_rows = []
    calibration_rows = []
    raw_p_values = []
    for index, scenario in enumerate(scenarios):
        seed = scenario_seeds[scenario.scenario_id]
        scenario_result, scenario_calibration, scenario_p_values = (
            _simulate_null_scenario(
                scenario,
                replicates=int(settings["null_replicates"]),
                batch_size=int(settings["batch_size"]),
                seed=seed,
            )
        )
        scenario_rows.extend(scenario_result)
        calibration_rows.extend(scenario_calibration)
        raw_p_values.append(
            np.stack(
                [scenario_p_values[method] for method in METHODS],
                axis=0,
            )
        )
        print(
            f"[{index + 1}/{len(scenarios)}] "
            f"{REGIMES[_regime_for(scenario)]['label']}: "
            f"{scenario.scenario_id}",
            flush=True,
        )

    scenario_results = pd.DataFrame(scenario_rows)
    scenario_calibration = pd.DataFrame(calibration_rows)
    regime_summary = _aggregate_scenarios(scenario_results)
    configuration_summary = _aggregate_configurations(scenario_results)
    rejection_calibration = _aggregate_rejection_calibration(
        scenario_calibration
    )
    power_summary = _simulate_power(
        replicates=int(settings["power_replicates"]),
        batch_size=int(settings["batch_size"]),
        seed=args.simulation_seed + 10_001,
    )
    runtime_summary = _runtime_audit(
        scenarios,
        repetitions=int(settings["runtime_repetitions"]),
        seed=args.simulation_seed + 20_001,
    )

    population_frame.to_csv(
        args.output_dir / "population_scenarios.csv",
        index=False,
    )
    scenario_results.to_csv(
        args.output_dir / "scenario_results.csv",
        index=False,
    )
    regime_summary.to_csv(
        args.output_dir / "regime_summary.csv",
        index=False,
    )
    configuration_summary.to_csv(
        args.output_dir / "configuration_summary.csv",
        index=False,
    )
    scenario_calibration.to_csv(
        args.output_dir / "rejection_calibration_scenarios.csv",
        index=False,
    )
    rejection_calibration.to_csv(
        args.output_dir / "rejection_calibration_regimes.csv",
        index=False,
    )
    np.savez_compressed(
        args.output_dir / "null_pvalues.npz",
        p_values=np.stack(raw_p_values, axis=0),
        scenario_ids=np.asarray(
            [scenario.scenario_id for scenario in scenarios]
        ),
        methods=np.asarray(list(METHODS)),
        simulation_seeds=np.asarray(
            [scenario_seeds[scenario.scenario_id] for scenario in scenarios],
            dtype=np.uint32,
        ),
    )
    power_summary.to_csv(
        args.output_dir / "power_summary.csv",
        index=False,
    )
    runtime_summary.to_csv(
        args.output_dir / "runtime_summary.csv",
        index=False,
    )
    _plot_calibration(regime_summary, args.output_dir)
    _plot_configuration_fpr(configuration_summary, args.output_dir)
    _plot_rejection_calibration(rejection_calibration, args.output_dir)
    _write_report(
        args.output_dir,
        profile=args.profile,
        settings=settings,
        scenario_results=scenario_results,
        summary=regime_summary,
        configurations=configuration_summary,
        power=power_summary,
        runtime=runtime_summary,
    )

    metadata = {
        "profile": args.profile,
        "settings": settings,
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "design_configuration_count": len(SHAPES) * len(CONFIGURATIONS),
        "scenario_count": len(scenarios),
        "methods": list(METHODS),
        "alphas": list(ALPHAS),
        "calibration_alphas": {
            "minimum": min(CALIBRATION_ALPHAS),
            "maximum": max(CALIBRATION_ALPHAS),
            "points": len(CALIBRATION_ALPHAS),
        },
        "null_pvalue_archive_dtype": "float64",
        "elapsed_seconds": perf_counter() - run_start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
