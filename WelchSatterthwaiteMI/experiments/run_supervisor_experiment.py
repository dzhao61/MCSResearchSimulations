#!/usr/bin/env python3
"""Run one explainable validation of three analytic equal-MI tests."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
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

from differential_mi.random_validation import (  # noqa: E402
    RandomScenario,
    SHAPES,
    generate_random_scenarios,
    scenario_diagnostics,
)
from differential_mi.distributions import (  # noqa: E402
    random_interaction_pattern,
    table_with_target_mi_from_interaction,
)
from differential_mi.statistics import influence_variance  # noqa: E402
from differential_mi.scenarios import (  # noqa: E402
    build_distributions,
    power_curve_scenarios,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


ALPHAS = (0.10, 0.05, 0.01)
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
    "well_sampled": {
        "label": "Well sampled",
        "designs": (0, 3),
        "description": (
            "Equal sample sizes and high observations per cell; includes one "
            "near-balanced and one skewed-margin variant."
        ),
    },
    "moderate": {
        "label": "Moderate",
        "designs": (1, 4),
        "description": (
            "A 2:1 sample-size ratio and moderate observations per cell, with "
            "increasingly heterogeneous margins."
        ),
    },
    "sparse_imbalanced": {
        "label": "Sparse and imbalanced",
        "designs": (2, 5),
        "description": (
            "A 4:1 sample-size ratio, low observations per cell, and "
            "heterogeneous margins."
        ),
    },
    "highly_sparse": {
        "label": "Highly skewed and sparse",
        "designs": (6, 7),
        "description": (
            "Both populations have minimum true expected cell counts from "
            "1 (inclusive) to 5 (exclusive), with heterogeneous margins."
        ),
    },
    "ultra_sparse": {
        "label": "Ultra-skewed and sparse",
        "designs": (8, 9),
        "description": (
            "Both populations have positive minimum true expected cell counts "
            "below 1, so their rarest cells are usually unobserved."
        ),
    },
    "widespread_sparse": {
        "label": "Widespread sparsity",
        "designs": (10, 11),
        "description": (
            "In both populations, 25-50% of cells have true expected counts "
            "below 1 and at least half have expected counts below 5."
        ),
    },
    "shape_mismatch": {
        "label": "Equal-MI shape mismatch",
        "designs": (12, 13),
        "description": (
            "A near-balanced population is compared with a strongly skewed "
            "population having exactly the same mutual information."
        ),
    },
    "extreme_imbalance": {
        "label": "Extreme sample imbalance",
        "designs": (14, 15),
        "description": (
            "Sample-size ratios of 1:10 and 1:20 stress the unequal-variance "
            "combination beyond the main grid."
        ),
    },
    "support_instability": {
        "label": "Support instability",
        "designs": (16, 17),
        "description": (
            "At least one complete row or column in each population has a "
            "true expected total below 1 and is frequently absent in samples."
        ),
    },
}
REGIME_ORDER = tuple(REGIMES)
DESIGN_TO_REGIME = {
    design: regime
    for regime, specification in REGIMES.items()
    for design in specification["designs"]
}
DESIGN_TO_VARIANT = {
    design: f"variant_{index + 1}"
    for specification in REGIMES.values()
    for index, design in enumerate(specification["designs"])
}

# These designs add controlled sparsity stress tests to the broad randomized
# grid. The internal lower bound for the ultra-sparse designs keeps the rarest
# expected count away from numerical zero while remaining strictly below one.
EXPECTED_COUNT_STRESS_DESIGNS = {
    6: {
        "margin_alpha_p": 0.8,
        "margin_alpha_q": 0.8,
        "target_mi": 0.10,
        "sample_size_ratio": 1,
        "minimum_expected_lower": 1.0,
        "minimum_expected_upper": 5.0,
    },
    7: {
        "margin_alpha_p": 1.0,
        "margin_alpha_q": 0.6,
        "target_mi": 0.15,
        "sample_size_ratio": 4,
        "minimum_expected_lower": 1.0,
        "minimum_expected_upper": 5.0,
    },
    8: {
        "margin_alpha_p": 0.6,
        "margin_alpha_q": 0.6,
        "target_mi": 0.10,
        "sample_size_ratio": 1,
        "minimum_expected_lower": 0.20,
        "minimum_expected_upper": 1.0,
    },
    9: {
        "margin_alpha_p": 0.8,
        "margin_alpha_q": 0.45,
        "target_mi": 0.15,
        "sample_size_ratio": 4,
        "minimum_expected_lower": 0.20,
        "minimum_expected_upper": 1.0,
    },
}
ADVERSARIAL_DESIGNS = {
    10: {
        "kind": "widespread_sparse",
        "margin_alpha_p": 0.35,
        "margin_alpha_q": 0.35,
        "target_mi": 0.03,
        "sample_size_ratio": 1,
    },
    11: {
        "kind": "widespread_sparse",
        "margin_alpha_p": 0.50,
        "margin_alpha_q": 0.25,
        "target_mi": 0.03,
        "sample_size_ratio": 1,
    },
    12: {
        "kind": "shape_mismatch",
        "margin_alpha_p": 50.0,
        "margin_alpha_q": 0.35,
        "target_mi": 0.07,
        "density": 25,
        "sample_size_ratio": 1,
    },
    13: {
        "kind": "shape_mismatch",
        "margin_alpha_p": 50.0,
        "margin_alpha_q": 0.35,
        "target_mi": 0.15,
        "density": 50,
        "sample_size_ratio": 1,
    },
    14: {
        "kind": "extreme_imbalance",
        "margin_alpha_p": 5.0,
        "margin_alpha_q": 1.0,
        "target_mi": 0.07,
        "density": 25,
        "sample_size_ratio": 10,
    },
    15: {
        "kind": "extreme_imbalance",
        "margin_alpha_p": 2.0,
        "margin_alpha_q": 0.8,
        "target_mi": 0.15,
        "density": 10,
        "sample_size_ratio": 20,
    },
    16: {
        "kind": "support_instability",
        "support_axis": "row",
        "margin_alpha_p": 0.25,
        "margin_alpha_q": 0.25,
        "target_mi": 0.02,
        "sample_size_ratio": 1,
    },
    17: {
        "kind": "support_instability",
        "support_axis": "column",
        "margin_alpha_p": 0.25,
        "margin_alpha_q": 0.25,
        "target_mi": 0.02,
        "sample_size_ratio": 1,
    },
}
PROFILE_SETTINGS = {
    "smoke": {
        "null_replicates": 300,
        "power_replicates": 500,
        "batch_size": 150,
        "runtime_repetitions": 20,
        "shape_limit": 3,
    },
    "full": {
        "null_replicates": 10_000,
        "power_replicates": 10_000,
        "batch_size": 1_000,
        "runtime_repetitions": 200,
        "shape_limit": None,
    },
}
DEFAULT_SCENARIO_SEED = 2_026_080_501
DEFAULT_SIMULATION_SEED = 2_026_080_502


def _draw_stress_margin(
    size: int,
    concentration: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw a positive heterogeneous margin suitable for stress scenarios."""
    for _ in range(2_000):
        margin = rng.dirichlet(np.full(size, concentration))
        if margin.min() >= 1e-4 and margin.max() <= 0.98:
            return margin
    raise RuntimeError("Could not draw a numerically usable stress margin.")


def _sample_sizes_in_expected_band(
    minimum_probability_p: float,
    minimum_probability_q: float,
    *,
    ratio: int,
    lower: float,
    upper: float,
    minimum_n: int = 120,
) -> tuple[int, int] | None:
    """Choose integer sample sizes placing both minimum counts in one band."""
    lower_n_p = max(
        float(minimum_n),
        lower / minimum_probability_p,
        lower / (ratio * minimum_probability_q),
    )
    upper_n_p = min(
        upper / minimum_probability_p,
        upper / (ratio * minimum_probability_q),
    )
    minimum_n_p = int(np.ceil(lower_n_p))
    maximum_n_p = min(
        int(np.ceil(upper_n_p) - 1),
        5_000_000 // ratio,
    )
    if minimum_n_p > maximum_n_p:
        return None

    n_p = (minimum_n_p + maximum_n_p) // 2
    n_q = ratio * n_p
    expected_minima = (
        n_p * minimum_probability_p,
        n_q * minimum_probability_q,
    )
    if not all(lower <= value < upper for value in expected_minima):
        return None
    return n_p, n_q


def _widespread_sparsity_sample_sizes(
    probability_p: np.ndarray,
    probability_q: np.ndarray,
    *,
    ratio: int,
) -> tuple[int, int] | None:
    """Find sample sizes satisfying cell-wide sparsity constraints."""
    maximum_n_p = 5_000_000 // ratio
    boundaries = [120.0, float(maximum_n_p)]
    boundaries.extend((1.0 / probability_p).reshape(-1).tolist())
    boundaries.extend((5.0 / probability_p).reshape(-1).tolist())
    boundaries.extend((1.0 / (ratio * probability_q)).reshape(-1).tolist())
    boundaries.extend((5.0 / (ratio * probability_q)).reshape(-1).tolist())
    boundaries = sorted(
        value for value in boundaries if 120 <= value <= maximum_n_p
    )

    candidates = {120, maximum_n_p}
    for boundary in boundaries:
        candidates.add(int(np.floor(boundary)))
        candidates.add(int(np.ceil(boundary)))
    for left, right in zip(boundaries, boundaries[1:]):
        candidates.add(int(np.floor((left + right) / 2.0)))

    valid_candidates = []
    for n_p in candidates:
        if not 120 <= n_p <= maximum_n_p:
            continue
        n_q = ratio * n_p
        expected_p = n_p * probability_p
        expected_q = n_q * probability_q
        below_1_p = float(np.mean(expected_p < 1.0))
        below_1_q = float(np.mean(expected_q < 1.0))
        below_5_p = float(np.mean(expected_p < 5.0))
        below_5_q = float(np.mean(expected_q < 5.0))
        if not (
            0.25 <= below_1_p <= 0.50
            and 0.25 <= below_1_q <= 0.50
            and below_5_p >= 0.50
            and below_5_q >= 0.50
        ):
            continue
        score = (
            abs(below_1_p - 0.375)
            + abs(below_1_q - 0.375)
            + abs(below_5_p - 0.75)
            + abs(below_5_q - 0.75)
        )
        valid_candidates.append((score, n_p, n_q))
    if not valid_candidates:
        return None
    _, n_p, n_q = min(valid_candidates)
    return n_p, n_q


def _margin_is_near_balanced(margin: np.ndarray) -> bool:
    uniform = 1.0 / margin.size
    return bool(
        margin.max() <= 1.5 * uniform
        and margin.min() >= 0.5 * uniform
    )


def _margin_is_strongly_skewed(margin: np.ndarray) -> bool:
    uniform = 1.0 / margin.size
    return bool(
        margin.max() >= 1.5 * uniform
        and margin.min() <= 0.5 * uniform
    )


def generate_expected_count_stress_scenarios(seed: int) -> list[RandomScenario]:
    """Generate equal-MI pairs with explicitly constrained expected counts."""
    rng = np.random.default_rng(seed)
    scenarios = []
    for shape_index, (rows, columns) in enumerate(SHAPES):
        for design_index, design in EXPECTED_COUNT_STRESS_DESIGNS.items():
            last_error: Exception | None = None
            for attempt in range(1, 5_001):
                try:
                    row_p = _draw_stress_margin(
                        rows,
                        design["margin_alpha_p"],
                        rng,
                    )
                    column_p = _draw_stress_margin(
                        columns,
                        design["margin_alpha_p"],
                        rng,
                    )
                    row_q = _draw_stress_margin(
                        rows,
                        design["margin_alpha_q"],
                        rng,
                    )
                    column_q = _draw_stress_margin(
                        columns,
                        design["margin_alpha_q"],
                        rng,
                    )
                    probability_p, association_p = (
                        table_with_target_mi_from_interaction(
                            row_p,
                            column_p,
                            design["target_mi"],
                            random_interaction_pattern(rows, columns, rng),
                        )
                    )
                    probability_q, association_q = (
                        table_with_target_mi_from_interaction(
                            row_q,
                            column_q,
                            design["target_mi"],
                            random_interaction_pattern(rows, columns, rng),
                        )
                    )
                    if min(probability_p.min(), probability_q.min()) < 1e-12:
                        raise ValueError("Generated cell probability is too small.")
                    sample_sizes = _sample_sizes_in_expected_band(
                        float(probability_p.min()),
                        float(probability_q.min()),
                        ratio=design["sample_size_ratio"],
                        lower=design["minimum_expected_lower"],
                        upper=design["minimum_expected_upper"],
                    )
                    if sample_sizes is None:
                        raise ValueError(
                            "No sample sizes satisfy the expected-count band."
                        )
                    if np.abs(probability_p - probability_q).sum() < 0.05:
                        raise ValueError("Generated weak-null pair is too similar.")
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
                    f"Failed to generate stress shape={rows}x{columns}, "
                    f"design={design_index}: {last_error}"
                )

            n_p, n_q = sample_sizes
            scenarios.append(
                RandomScenario(
                    scenario_id=f"stress_{rows}x{columns}_d{design_index}",
                    shape_index=shape_index,
                    design_index=design_index,
                    rows=rows,
                    columns=columns,
                    n_p=n_p,
                    n_q=n_q,
                    target_mi=design["target_mi"],
                    margin_alpha_p=design["margin_alpha_p"],
                    margin_alpha_q=design["margin_alpha_q"],
                    association_p=association_p,
                    association_q=association_q,
                    generation_attempts=attempt,
                    probability_p=probability_p,
                    probability_q=probability_q,
                )
            )
    return scenarios


def generate_adversarial_scenarios(seed: int) -> list[RandomScenario]:
    """Generate pre-specified difficult equal-MI population pairs."""
    rng = np.random.default_rng(seed)
    scenarios = []
    for shape_index, (rows, columns) in enumerate(SHAPES):
        cells = rows * columns
        for design_index, design in ADVERSARIAL_DESIGNS.items():
            last_error: Exception | None = None
            for attempt in range(1, 10_001):
                try:
                    row_p = _draw_stress_margin(
                        rows,
                        design["margin_alpha_p"],
                        rng,
                    )
                    column_p = _draw_stress_margin(
                        columns,
                        design["margin_alpha_p"],
                        rng,
                    )
                    row_q = _draw_stress_margin(
                        rows,
                        design["margin_alpha_q"],
                        rng,
                    )
                    column_q = _draw_stress_margin(
                        columns,
                        design["margin_alpha_q"],
                        rng,
                    )
                    if design["kind"] == "shape_mismatch" and not (
                        _margin_is_near_balanced(row_p)
                        and _margin_is_near_balanced(column_p)
                        and _margin_is_strongly_skewed(row_q)
                        and _margin_is_strongly_skewed(column_q)
                    ):
                        raise ValueError(
                            "Margins do not satisfy the shape-mismatch rule."
                        )

                    probability_p, association_p = (
                        table_with_target_mi_from_interaction(
                            row_p,
                            column_p,
                            design["target_mi"],
                            random_interaction_pattern(rows, columns, rng),
                        )
                    )
                    probability_q, association_q = (
                        table_with_target_mi_from_interaction(
                            row_q,
                            column_q,
                            design["target_mi"],
                            random_interaction_pattern(rows, columns, rng),
                        )
                    )
                    if min(probability_p.min(), probability_q.min()) < 1e-12:
                        raise ValueError("Generated cell probability is too small.")

                    if design["kind"] == "widespread_sparse":
                        sample_sizes = _widespread_sparsity_sample_sizes(
                            probability_p,
                            probability_q,
                            ratio=design["sample_size_ratio"],
                        )
                    elif design["kind"] == "support_instability":
                        if design["support_axis"] == "row":
                            minimum_probability_p = float(
                                probability_p.sum(axis=1).min()
                            )
                            minimum_probability_q = float(
                                probability_q.sum(axis=1).min()
                            )
                        else:
                            minimum_probability_p = float(
                                probability_p.sum(axis=0).min()
                            )
                            minimum_probability_q = float(
                                probability_q.sum(axis=0).min()
                            )
                        sample_sizes = _sample_sizes_in_expected_band(
                            minimum_probability_p,
                            minimum_probability_q,
                            ratio=design["sample_size_ratio"],
                            lower=0.20,
                            upper=1.0,
                            minimum_n=30,
                        )
                    else:
                        n_p = max(120, cells * design["density"])
                        sample_sizes = (
                            n_p,
                            n_p * design["sample_size_ratio"],
                        )
                    if sample_sizes is None:
                        raise ValueError(
                            "No sample sizes satisfy the adversarial rule."
                        )
                    if np.abs(probability_p - probability_q).sum() < 0.05:
                        raise ValueError("Generated weak-null pair is too similar.")
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
                    f"Failed to generate adversarial shape={rows}x{columns}, "
                    f"design={design_index}: {last_error}"
                )

            n_p, n_q = sample_sizes
            scenarios.append(
                RandomScenario(
                    scenario_id=f"adversarial_{rows}x{columns}_d{design_index}",
                    shape_index=shape_index,
                    design_index=design_index,
                    rows=rows,
                    columns=columns,
                    n_p=n_p,
                    n_q=n_q,
                    target_mi=design["target_mi"],
                    margin_alpha_p=design["margin_alpha_p"],
                    margin_alpha_q=design["margin_alpha_q"],
                    association_p=association_p,
                    association_q=association_q,
                    generation_attempts=attempt,
                    probability_p=probability_p,
                    probability_q=probability_q,
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
    parser.add_argument("--power-replicates", type=int)
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--runtime-repetitions", type=int)
    return parser.parse_args()


def _settings(args: argparse.Namespace) -> dict[str, int | None]:
    settings = dict(PROFILE_SETTINGS[args.profile])
    for name in (
        "null_replicates",
        "power_replicates",
        "batch_size",
        "runtime_repetitions",
    ):
        value = getattr(args, name)
        if value is not None:
            settings[name] = value
    if min(
        int(settings["null_replicates"]),
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


def _population_metadata(scenario: RandomScenario) -> dict:
    diagnostics = scenario_diagnostics(scenario)
    p = scenario.probability_p
    q = scenario.probability_q
    regime = _regime_for(scenario)
    cells = scenario.rows * scenario.columns
    return {
        **diagnostics,
        "regime": regime,
        "regime_label": REGIMES[regime]["label"],
        "variant": DESIGN_TO_VARIANT[scenario.design_index],
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


def _simulate_null_scenario(
    scenario: RandomScenario,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> list[dict]:
    rng = np.random.default_rng(seed)
    method_counts = {
        method: {
            "valid": 0,
            "coverage": 0,
            "rejections": {alpha: 0 for alpha in ALPHAS},
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
            for alpha in ALPHAS:
                method_counts[method]["rejections"][alpha] += int(
                    np.count_nonzero(p_values <= alpha)
                )
            df_column = specification["degrees_of_freedom"]
            if df_column is None:
                critical = norm.ppf(0.975)
            else:
                degrees_of_freedom = values[df_column][method_valid]
                method_counts[method]["degrees_of_freedom"].append(
                    degrees_of_freedom
                )
                critical = t.ppf(0.975, df=degrees_of_freedom)
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
            "mean_delta_error": delta_sum / valid_count,
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
            "mean_standard_error": standard_error_sum / valid_count,
            **{
                f"mean_sample_{name}": total / replicates
                for name, total in diagnostic_sums.items()
            },
        }
    )

    rows = []
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
    return rows


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
            method: {"rejections": 0, "coverage": 0, "df": []}
            for method in METHODS
        }
        valid_count = 0
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
            valid = values["valid"] & values["expanded_valid"]
            valid_count += int(np.count_nonzero(valid))
            delta_error = (
                values["delta_corrected"][valid] - diagnostics["true_delta"]
            )
            standard_error = values["standard_error"][valid]
            for method, specification in METHODS.items():
                p_values = values[specification["p_value"]][valid]
                method_counts[method]["rejections"] += int(
                    np.count_nonzero(p_values <= 0.05)
                )
                df_column = specification["degrees_of_freedom"]
                if df_column is None:
                    critical = norm.ppf(0.975)
                else:
                    df = values[df_column][valid]
                    method_counts[method]["df"].append(df)
                    critical = t.ppf(0.975, df=df)
                method_counts[method]["coverage"] += int(
                    np.count_nonzero(
                        np.abs(delta_error) <= critical * standard_error
                    )
                )
        for method, specification in METHODS.items():
            df_parts = method_counts[method]["df"]
            rows.append(
                {
                    **scenario.to_dict(),
                    **diagnostics,
                    "simulation_seed": scenario_seed,
                    "replicates": replicates,
                    "valid_rate": valid_count / replicates,
                    "method": method,
                    "method_label": specification["label"],
                    "power_05": method_counts[method]["rejections"] / valid_count,
                    "coverage_95": method_counts[method]["coverage"] / valid_count,
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
    target_shapes = ((2, 2), (5, 5), (10, 10), (20, 20))
    selected = []
    for shape in target_shapes:
        matches = [
            scenario
            for scenario in scenarios
            if (scenario.rows, scenario.columns) == shape
            and scenario.design_index == 4
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
    columns = 3
    rows = int(np.ceil(len(REGIME_ORDER) / columns))
    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(5 * columns, 4.6 * rows),
        sharey=True,
    )
    axes = np.asarray(axes).reshape(-1)
    colors = ("#355070", "#D97745", "#4F7C64")
    width = 0.24
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
                x + (index - 1) * width,
                errors,
                width,
                color=colors[index],
                label=specification["label"],
            )
        axis.set_xticks(x, [f"{alpha:.2f}" for alpha in ALPHAS])
        axis.set_title(REGIMES[regime]["label"])
        axis.set_xlabel("Nominal alpha")
        axis.grid(axis="y", alpha=0.2)
    for axis in axes[len(REGIME_ORDER) :]:
        axis.set_visible(False)
    axes[0].set_ylabel("Mean absolute false-positive-rate error")
    axes[-1].legend(frameon=False)
    figure.suptitle("Equal-MI null calibration by sampling regime")
    figure.tight_layout()
    figure.savefig(output_dir / "calibration_summary.png", dpi=180)
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
            "regime_label": "Regime",
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
        ["rows", "columns", "method_label", "median_time_ms", "relative_to_normal"]
    ].rename(
        columns={
            "rows": "Rows",
            "columns": "Columns",
            "method_label": "Method",
            "median_time_ms": "Median ms",
            "relative_to_normal": "Relative to Wald",
        }
    )
    well_sampled = summary[summary["regime"].eq("well_sampled")].set_index(
        "method"
    )
    difficult_regimes = (
        "sparse_imbalanced",
        "highly_sparse",
        "ultra_sparse",
        "widespread_sparse",
        "shape_mismatch",
        "extreme_imbalance",
        "support_instability",
    )
    target_reductions = {}
    for regime in difficult_regimes:
        difficult = summary[summary["regime"].eq(regime)].set_index("method")
        target_reductions[regime] = {
            label: 1.0
            - difficult.loc[
                "expanded_welch",
                f"mean_absolute_fpr_error_{label}",
            ]
            / difficult.loc[
                "normal_wald",
                f"mean_absolute_fpr_error_{label}",
            ]
            for label in ("05", "01")
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
        f"Profile: `{profile}`. Each null population used "
        f"`{settings['null_replicates']:,}` independently simulated table pairs.",
        "",
        "## Experiment in one sentence",
        "",
        "Generate two different categorical populations with exactly equal true",
        "mutual information, repeatedly sample one table from each, and check how",
        "often each analytic test incorrectly rejects equality.",
        "",
        "## Design",
        "",
        f"The null grid contains {scenario_results['scenario_id'].nunique()} fixed",
        f"population pairs across {len(REGIME_ORDER)} regimes. Every method sees",
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
            "## Main calibration results",
            "",
            _markdown(key_rows),
            "",
            "False-positive-rate error is the absolute difference between observed",
            "and nominal rejection rates among valid calculations, so lower is",
            "better. Validity is reported separately and is part of method",
            "performance in the support-instability boundary regime.",
            "",
            "## Overall summary",
            "",
            _markdown(overall),
            "",
            "## Direct interpretation",
            "",
            "- Relative calibration changes in the difficult regimes are",
            "  reported directly below; positive percentages mean that expanded",
            "  Welch reduced error relative to normal Wald.",
            *[
                f"- **{REGIMES[regime]['label']}:** "
                f"{reductions['05']:.1%} at alpha 0.05 and "
                f"{reductions['01']:.1%} at alpha 0.01."
                for regime, reductions in target_reductions.items()
            ],
            f"- This was not a universal improvement. In well-sampled tables at",
            f"  alpha 0.05, expanded Welch increased mean absolute error from",
            f"  `{well_sampled.loc['normal_wald', 'mean_absolute_fpr_error_05']:.5f}`",
            f"  to `{well_sampled.loc['expanded_welch', 'mean_absolute_fpr_error_05']:.5f}`",
            f"  by becoming mildly conservative.",
            f"- Across the five power scenarios, expanded Welch lost",
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
            "All three timings use the same implementation path. The expanded method",
            "remains deterministic and scans each table a fixed number of times.",
            "",
            "## Output map",
            "",
            "- `population_scenarios.csv`: the fixed generating distributions and",
            "  difficulty diagnostics.",
            "- `scenario_results.csv`: every scenario-method result.",
            "- `regime_summary.csv`: the presentation-level aggregate table.",
            "- `power_summary.csv`: alternative-hypothesis power and coverage.",
            "- `runtime_summary.csv`: end-to-end timing by table size.",
            "- `calibration_summary.png`: one visual comparison across regimes.",
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

    scenarios = generate_random_scenarios(args.scenario_seed)
    scenarios.extend(
        generate_expected_count_stress_scenarios(args.scenario_seed + 1)
    )
    scenarios.extend(
        generate_adversarial_scenarios(args.scenario_seed + 2)
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
    population_frame = pd.DataFrame(
        [_population_metadata(scenario) for scenario in scenarios]
    )
    children = np.random.SeedSequence(args.simulation_seed).spawn(
        len(scenarios)
    )
    scenario_rows = []
    for index, (scenario, child) in enumerate(zip(scenarios, children)):
        seed = int(child.generate_state(1)[0])
        scenario_rows.extend(
            _simulate_null_scenario(
                scenario,
                replicates=int(settings["null_replicates"]),
                batch_size=int(settings["batch_size"]),
                seed=seed,
            )
        )
        print(
            f"[{index + 1}/{len(scenarios)}] "
            f"{REGIMES[_regime_for(scenario)]['label']}: "
            f"{scenario.scenario_id}",
            flush=True,
        )

    scenario_results = pd.DataFrame(scenario_rows)
    regime_summary = _aggregate_scenarios(scenario_results)
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
    power_summary.to_csv(
        args.output_dir / "power_summary.csv",
        index=False,
    )
    runtime_summary.to_csv(
        args.output_dir / "runtime_summary.csv",
        index=False,
    )
    _plot_calibration(regime_summary, args.output_dir)
    _write_report(
        args.output_dir,
        profile=args.profile,
        settings=settings,
        scenario_results=scenario_results,
        summary=regime_summary,
        power=power_summary,
        runtime=runtime_summary,
    )

    metadata = {
        "profile": args.profile,
        "settings": settings,
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "scenario_count": len(scenarios),
        "methods": list(METHODS),
        "alphas": list(ALPHAS),
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
