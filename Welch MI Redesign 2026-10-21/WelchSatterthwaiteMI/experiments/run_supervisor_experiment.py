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
    scenario_diagnostics,
)
from differential_mi.distributions import (  # noqa: E402
    random_interaction_pattern,
    table_with_target_mi_from_interaction,
)
from differential_mi.statistics import influence_variance  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


ALPHAS = (0.10, 0.05, 0.01)
# Preregistered decision rules (frozen before any run; see FINAL_PROTOCOL).
# Adequate size control follows Bradley's (1978) liberal criterion: the
# empirical rejection rate must lie within a factor of 1.5 of the nominal
# level. Acceptable validity is a floor on the fraction of replicates for
# which a method's statistic is even computable; below it, a scenario is
# reported as a method failure rather than folded into a calibration mean.
BRADLEY_LIBERAL_LOWER = 0.5
BRADLEY_LIBERAL_UPPER = 1.5
MINIMUM_ACCEPTABLE_VALID_RATE = 0.90
# Power effect sizes are relative to each population pair's own null MI, so
# that a 2x2 table at I0 = 0.10 and an 8x8 table at I0 = 0.10 are probed by
# comparably sized departures rather than one fixed absolute nats value that
# is a large effect for a small table and a small one for a large table.
RELATIVE_EFFECTS = (0.5, 1.0)
CALIBRATION_ALPHAS = tuple(index / 1_000 for index in range(101))
MINIMUM_SAMPLE_SIZE = 50
MAXIMUM_SAMPLE_SIZE = 1_000
SHAPES = (
    (2, 2),
    (2, 5),
    (3, 3),
    (3, 5),
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
    "strong_null": {
        "label": "Strong null (P = Q)",
        "designs": (-2, -1),
        "description": (
            "Population Q is set identically equal to population P (equal "
            "or 2:1 sample sizes). This is a positive control: a "
            "calibrated method must reject at close to the nominal rate "
            "here, since a systematic departure reflects an "
            "implementation or approximation fault rather than a "
            "finite-sample effect from P and Q genuinely differing."
        ),
    },
    "well_sampled": {
        "label": "Well sampled",
        "designs": (0, 1),
        "description": (
            "Equal sample sizes, near-balanced margins, "
            "and approximately 15 observations per cell."
        ),
    },
    "moderate": {
        "label": "Moderate",
        "designs": (2, 3),
        "description": (
            "Moderately heterogeneous margins, six to eight observations per "
            "cell, and sample-size ratios of 1:1 or 2:1."
        ),
    },
    "highly_sparse": {
        "label": "Highly skewed and sparse",
        "designs": (4, 5),
        "description": (
            "Both populations have minimum true expected cell counts from "
            "1 (inclusive) to 5 (exclusive), with ratios of 1:1 or 2:1."
        ),
    },
    "ultra_sparse": {
        "label": "Ultra-skewed and sparse",
        "designs": (6, 7),
        "description": (
            "Both populations have positive minimum true expected cell counts "
            "below 1, with ratios of 1:1 or 10:1."
        ),
    },
    "widespread_sparse": {
        "label": "Widespread sparsity",
        "designs": (8, 9),
        "description": (
            "In both populations, 25-50% of cells have true expected counts "
            "below 1 and at least half have expected counts below 5. This is "
            "the explicit failure-boundary check."
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

STRONG_NULL_DESIGNS = {
    -2: {
        "margin_alpha": 50.0,
        "target_mi": 0.10,
        "density": 15,
        "minimum_n": 200,
        "sample_size_ratio": 1,
    },
    -1: {
        "margin_alpha": 8.0,
        "target_mi": 0.15,
        "density": 8,
        "minimum_n": 100,
        "sample_size_ratio": 2,
    },
}

FIXED_DENSITY_DESIGNS = {
    0: {
        "margin_alpha_p": 50.0,
        "margin_alpha_q": 50.0,
        "target_mi": 0.10,
        "density": 15,
        "minimum_n": 200,
        "sample_size_ratio": 1,
    },
    1: {
        "margin_alpha_p": 50.0,
        "margin_alpha_q": 50.0,
        "target_mi": 0.15,
        "density": 15,
        "minimum_n": 200,
        "sample_size_ratio": 1,
    },
    2: {
        "margin_alpha_p": 8.0,
        "margin_alpha_q": 4.0,
        "target_mi": 0.10,
        "density": 8,
        "minimum_n": 100,
        "sample_size_ratio": 1,
    },
    3: {
        "margin_alpha_p": 8.0,
        "margin_alpha_q": 2.0,
        "target_mi": 0.15,
        "density": 6,
        "minimum_n": 100,
        "sample_size_ratio": 2,
    },
}

EXPECTED_COUNT_STRESS_DESIGNS = {
    4: {
        "margin_alpha_p": 2.0,
        "margin_alpha_q": 2.0,
        "target_mi": 0.10,
        "sample_size_ratio": 1,
        "minimum_expected_lower": 1.0,
        "minimum_expected_upper": 5.0,
    },
    5: {
        "margin_alpha_p": 10.0,
        "margin_alpha_q": 2.0,
        "target_mi": 0.15,
        "sample_size_ratio": 2,
        "minimum_expected_lower": 1.0,
        "minimum_expected_upper": 5.0,
    },
    6: {
        "margin_alpha_p": 0.8,
        "margin_alpha_q": 0.8,
        "target_mi": 0.10,
        "sample_size_ratio": 1,
        "minimum_expected_lower": 0.05,
        "minimum_expected_upper": 1.0,
    },
    7: {
        "margin_alpha_p": 10.0,
        "margin_alpha_q": 0.8,
        "target_mi": 0.15,
        "sample_size_ratio": 10,
        "minimum_expected_lower": 0.05,
        "minimum_expected_upper": 1.0,
    },
}
ADVERSARIAL_DESIGNS = {
    8: {
        "kind": "widespread_sparse",
        "margin_alpha_p": 0.35,
        "margin_alpha_q": 0.35,
        "target_mi": 0.10,
        "sample_size_ratio": 1,
    },
    9: {
        "kind": "widespread_sparse",
        "margin_alpha_p": 1.0,
        "margin_alpha_q": 0.35,
        "target_mi": 0.15,
        "sample_size_ratio": 2,
    },
}
PROFILE_SETTINGS = {
    "smoke": {
        "null_replicates": 300,
        "power_replicates": 500,
        "power_calibration_replicates": 500,
        "batch_size": 150,
        "runtime_repetitions": 20,
        "shape_limit": 3,
    },
    "full": {
        "null_replicates": 10_000,
        "power_replicates": 10_000,
        "power_calibration_replicates": 10_000,
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
    minimum_n: int = MINIMUM_SAMPLE_SIZE,
    maximum_n: int = MAXIMUM_SAMPLE_SIZE,
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
        maximum_n // ratio,
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
    maximum_n_p = MAXIMUM_SAMPLE_SIZE // ratio
    boundaries = [float(MINIMUM_SAMPLE_SIZE), float(maximum_n_p)]
    boundaries.extend((1.0 / probability_p).reshape(-1).tolist())
    boundaries.extend((5.0 / probability_p).reshape(-1).tolist())
    boundaries.extend((1.0 / (ratio * probability_q)).reshape(-1).tolist())
    boundaries.extend((5.0 / (ratio * probability_q)).reshape(-1).tolist())
    boundaries = sorted(
        value
        for value in boundaries
        if MINIMUM_SAMPLE_SIZE <= value <= maximum_n_p
    )

    candidates = {MINIMUM_SAMPLE_SIZE, maximum_n_p}
    for boundary in boundaries:
        candidates.add(int(np.floor(boundary)))
        candidates.add(int(np.ceil(boundary)))
    for left, right in zip(boundaries, boundaries[1:]):
        candidates.add(int(np.floor((left + right) / 2.0)))

    valid_candidates = []
    for n_p in candidates:
        if not MINIMUM_SAMPLE_SIZE <= n_p <= maximum_n_p:
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


def _fixed_density_sample_sizes(
    cells: int,
    *,
    density: int,
    ratio: int,
    minimum_n: int = MINIMUM_SAMPLE_SIZE,
) -> tuple[int, int]:
    """Choose bounded sample sizes for one fixed-density scenario."""
    n_p = max(minimum_n, cells * density)
    n_p = min(n_p, MAXIMUM_SAMPLE_SIZE // ratio)
    n_q = ratio * n_p
    if not (
        MINIMUM_SAMPLE_SIZE <= n_p <= MAXIMUM_SAMPLE_SIZE
        and MINIMUM_SAMPLE_SIZE <= n_q <= MAXIMUM_SAMPLE_SIZE
    ):
        raise ValueError("Fixed-density sample sizes exceed experiment bounds.")
    return n_p, n_q


def generate_strong_null_scenarios(seed: int) -> list[RandomScenario]:
    """Generate positive-control scenarios where Q equals P exactly.

    Every other regime enforces a minimum population separation
    (``L1(P, Q) >= 0.05``) because the thesis targets the weak null
    ``I(P) = I(Q)`` with ``P != Q``. This regime is the deliberate
    exception: it checks that every method is calibrated when the two
    tables are drawn from literally the same population, so a failure here
    cannot be attributed to a genuine finite-sample weak-null effect.
    """
    rng = np.random.default_rng(seed)
    scenarios = []
    for shape_index, (rows, columns) in enumerate(SHAPES):
        cells = rows * columns
        for design_index, design in STRONG_NULL_DESIGNS.items():
            n_p, n_q = _fixed_density_sample_sizes(
                cells,
                density=design["density"],
                ratio=design["sample_size_ratio"],
                minimum_n=design["minimum_n"],
            )
            last_error: Exception | None = None
            for attempt in range(1, 5_001):
                try:
                    row_p = _draw_stress_margin(
                        rows, design["margin_alpha"], rng
                    )
                    column_p = _draw_stress_margin(
                        columns, design["margin_alpha"], rng
                    )
                    probability_p, association_p = (
                        table_with_target_mi_from_interaction(
                            row_p,
                            column_p,
                            design["target_mi"],
                            random_interaction_pattern(rows, columns, rng),
                        )
                    )
                    if probability_p.min() < 1e-12:
                        raise ValueError("Generated cell probability is too small.")
                    if float(influence_variance(probability_p)) < 1e-6:
                        raise ValueError("Generated influence variance is degenerate.")
                except (RuntimeError, ValueError) as error:
                    last_error = error
                    continue
                break
            else:
                raise RuntimeError(
                    f"Failed to generate strong-null shape={rows}x{columns}, "
                    f"design={design_index}: {last_error}"
                )

            scenarios.append(
                RandomScenario(
                    scenario_id=f"strong_null_{rows}x{columns}_d{design_index}",
                    shape_index=shape_index,
                    design_index=design_index,
                    rows=rows,
                    columns=columns,
                    n_p=n_p,
                    n_q=n_q,
                    target_mi=design["target_mi"],
                    margin_alpha_p=design["margin_alpha"],
                    margin_alpha_q=design["margin_alpha"],
                    association_p=association_p,
                    association_q=association_p,
                    generation_attempts=attempt,
                    probability_p=probability_p,
                    probability_q=probability_p.copy(),
                )
            )
    return scenarios


def generate_fixed_density_scenarios(seed: int) -> list[RandomScenario]:
    """Generate the well-sampled and moderate equal-MI scenarios."""
    rng = np.random.default_rng(seed)
    scenarios = []
    for shape_index, (rows, columns) in enumerate(SHAPES):
        cells = rows * columns
        for design_index, design in FIXED_DENSITY_DESIGNS.items():
            n_p, n_q = _fixed_density_sample_sizes(
                cells,
                density=design["density"],
                ratio=design["sample_size_ratio"],
                minimum_n=design["minimum_n"],
            )
            last_error: Exception | None = None
            for attempt in range(1, 5_001):
                try:
                    row_p = _draw_stress_margin(
                        rows, design["margin_alpha_p"], rng
                    )
                    column_p = _draw_stress_margin(
                        columns, design["margin_alpha_p"], rng
                    )
                    row_q = _draw_stress_margin(
                        rows, design["margin_alpha_q"], rng
                    )
                    column_q = _draw_stress_margin(
                        columns, design["margin_alpha_q"], rng
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
                    if np.abs(probability_p - probability_q).sum() < 0.05:
                        raise ValueError("Generated equal-MI pair is too similar.")
                    if min(
                        float(influence_variance(probability_p)),
                        float(influence_variance(probability_q)),
                    ) < 1e-6:
                        raise ValueError("Generated influence variance is degenerate.")
                except (RuntimeError, ValueError) as error:
                    last_error = error
                    continue
                break
            else:
                raise RuntimeError(
                    f"Failed to generate fixed-density shape={rows}x{columns}, "
                    f"design={design_index}: {last_error}"
                )

            scenarios.append(
                RandomScenario(
                    scenario_id=f"fixed_{rows}x{columns}_d{design_index}",
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

                    sample_sizes = _widespread_sparsity_sample_sizes(
                        probability_p,
                        probability_q,
                        ratio=design["sample_size_ratio"],
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
    parser.add_argument("--power-calibration-replicates", type=int)
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--runtime-repetitions", type=int)
    return parser.parse_args()


def _settings(args: argparse.Namespace) -> dict[str, int | None]:
    settings = dict(PROFILE_SETTINGS[args.profile])
    for name in (
        "null_replicates",
        "power_replicates",
        "power_calibration_replicates",
        "batch_size",
        "runtime_repetitions",
    ):
        value = getattr(args, name)
        if value is not None:
            settings[name] = value
    if min(
        int(settings["null_replicates"]),
        int(settings["power_replicates"]),
        int(settings["power_calibration_replicates"]),
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
            "common_valid_rejections": {alpha: 0 for alpha in ALPHAS},
            "calibration_rejections": np.zeros(
                len(CALIBRATION_ALPHAS),
                dtype=np.int64,
            ),
            "degrees_of_freedom": [],
        }
        for method in METHODS
    }
    common_valid_count = 0
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

        common_valid_batch = np.ones(count, dtype=bool)
        for specification in METHODS.values():
            common_valid_batch &= values[specification["validity"]]
        common_valid_count += int(np.count_nonzero(common_valid_batch))
        for method, specification in METHODS.items():
            common_p_values = values[specification["p_value"]][common_valid_batch]
            for alpha in ALPHAS:
                method_counts[method]["common_valid_rejections"][alpha] += int(
                    np.count_nonzero(common_p_values <= alpha)
                )

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
            "common_valid_replicates": common_valid_count,
            "common_valid_rate": common_valid_count / replicates,
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
            "acceptable_validity": (
                method_valid_count / replicates >= MINIMUM_ACCEPTABLE_VALID_RATE
            ),
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
            # Unconditional: invalid replicates count as non-rejections, so
            # the denominator is every replicate rather than only the valid
            # ones. Common-valid: restricted to replicates where every
            # method's statistic is defined, so the three methods' rates in
            # one row always refer to the same underlying replicates.
            row[f"unconditional_fpr_{label}"] = rejections / replicates
            common_valid_rejections = method_counts[method][
                "common_valid_rejections"
            ][alpha]
            row[f"common_valid_fpr_{label}"] = (
                common_valid_rejections / common_valid_count
                if common_valid_count
                else np.nan
            )
            row[f"adequate_size_control_{label}"] = bool(
                np.isfinite(fpr)
                and BRADLEY_LIBERAL_LOWER * alpha
                <= fpr
                <= BRADLEY_LIBERAL_UPPER * alpha
            )
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
            "shape_index": scenario.shape_index,
            "design_index": scenario.design_index,
            "rows": scenario.rows,
            "columns": scenario.columns,
            "n_p": scenario.n_p,
            "n_q": scenario.n_q,
            "target_mi": scenario.target_mi,
            "regime": common["regime"],
            "regime_label": common["regime_label"],
            "variant": common["variant"],
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
                "scenarios_below_valid_rate_floor": int(
                    (~group["acceptable_validity"]).sum()
                ),
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
                row[f"mean_unconditional_fpr_{label}"] = float(
                    group[f"unconditional_fpr_{label}"].mean()
                )
                row[f"mean_common_valid_fpr_{label}"] = float(
                    group[f"common_valid_fpr_{label}"].mean()
                )
                row[f"adequate_size_control_count_{label}"] = int(
                    group[f"adequate_size_control_{label}"].sum()
                )
                row[f"inadequate_size_control_count_{label}"] = int(
                    (~group[f"adequate_size_control_{label}"]).sum()
                )
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


def _build_power_alternative(
    scenario: RandomScenario,
    relative_effect: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, float, float]:
    """Build an alternative Q with MI shifted relative to the null pair.

    Reuses Q's own row and column margins from the null scenario (recovered
    from its probability table) so the alternative keeps the same marginal
    shape as the calibration pair; only the association strength, and hence
    I(Q), changes. The effect is expressed relative to the pair's own null
    MI (``target_mi``) so that a small table and a large table are probed by
    comparably sized departures rather than one fixed absolute nats value.
    Raises ``ValueError`` if the requested MI is infeasible for these
    margins or produces a degenerate influence variance, so that the caller
    can log every dropped configuration explicitly rather than have it
    disappear silently from the output.
    """
    row_q = scenario.probability_q.sum(axis=1)
    column_q = scenario.probability_q.sum(axis=0)
    target_mi_alt = scenario.target_mi * (1.0 + relative_effect)
    try:
        probability_q_alt, association_alt = table_with_target_mi_from_interaction(
            row_q,
            column_q,
            target_mi_alt,
            random_interaction_pattern(scenario.rows, scenario.columns, rng),
        )
    except (RuntimeError, ValueError) as error:
        raise ValueError(
            f"Target MI {target_mi_alt:.6f} is infeasible for these margins: {error}"
        ) from error
    if probability_q_alt.min() < 1e-12:
        raise ValueError("Generated cell probability is too small.")
    if float(influence_variance(probability_q_alt)) < 1e-6:
        raise ValueError("Generated influence variance is degenerate.")
    return probability_q_alt, association_alt, target_mi_alt


def _aggregate_power(power_results: pd.DataFrame) -> pd.DataFrame:
    """Summarize power by regime and relative effect size.

    Mirrors ``_aggregate_scenarios``: the full per-population-pair power
    results remain in ``power_summary.csv`` so that a regime-level average
    cannot conceal a specific configuration's power loss.
    """
    rows = []
    regime_groups = [
        (regime, power_results[power_results["regime"].eq(regime)])
        for regime in REGIME_ORDER
    ]
    regime_groups.append(("all", power_results))
    for regime, regime_frame in regime_groups:
        for relative_effect in sorted(power_results["relative_effect"].unique()):
            effect_frame = regime_frame[
                regime_frame["relative_effect"].eq(relative_effect)
            ]
            if effect_frame.empty:
                continue
            for method, specification in METHODS.items():
                group = effect_frame[effect_frame["method"].eq(method)]
                if group.empty:
                    continue
                rows.append(
                    {
                        "regime": regime,
                        "regime_label": (
                            "All regimes"
                            if regime == "all"
                            else REGIMES[regime]["label"]
                        ),
                        "relative_effect": relative_effect,
                        "method": method,
                        "method_label": specification["label"],
                        "population_pairs": len(group),
                        "mean_valid_rate": float(group["valid_rate"].mean()),
                        "mean_power_05": float(group["power_05"].mean()),
                        "mean_size_adjusted_power": float(
                            group["size_adjusted_power"].mean()
                        ),
                        "mean_coverage_95": float(group["coverage_95"].mean()),
                    }
                )
    return pd.DataFrame(rows)


def _simulate_power(
    scenarios: list[RandomScenario],
    *,
    relative_effects: tuple[float, ...],
    replicates: int,
    calibration_replicates: int,
    batch_size: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Power across every null population pair, at effects relative to I0.

    Alongside nominal power at alpha = 0.05, also reports size-adjusted
    power: the alternative-hypothesis rejection rate against an empirical
    threshold, the 5th percentile of that method's p-values under fresh null
    replicates of the *same* population pair, drawn from an independent RNG
    stream that never touches the null replicates used for the primary FPR
    report or the alternative replicates used for nominal power. Nominal
    power alone is not a fair method comparison when methods do not share
    the same actual size; size-adjusted power isolates the power difference
    that is not explained by a size difference. It is reported as a
    diagnostic, not as an achievable procedure, since the oracle threshold
    is not available to an analyst working from one real dataset.

    Returns the power results and a second frame logging every (scenario,
    relative effect) combination for which no alternative could be
    constructed, so infeasible configurations are visible rather than
    silently absent from the output.
    """
    rows = []
    infeasible = []
    top_children = np.random.SeedSequence(seed).spawn(
        len(scenarios) * len(relative_effects)
    )
    child_index = 0
    for scenario in scenarios:
        regime = _regime_for(scenario)
        for relative_effect in relative_effects:
            construction_seed, calibration_seed, simulation_seed = (
                int(child.generate_state(1)[0])
                for child in top_children[child_index].spawn(3)
            )
            child_index += 1

            construction_rng = np.random.default_rng(construction_seed)
            try:
                probability_q_alt, association_alt, target_mi_alt = (
                    _build_power_alternative(
                        scenario, relative_effect, construction_rng
                    )
                )
            except ValueError as error:
                infeasible.append(
                    {
                        "scenario_id": scenario.scenario_id,
                        "regime": regime,
                        "relative_effect": relative_effect,
                        "null_mi": scenario.target_mi,
                        "reason": str(error),
                    }
                )
                continue
            true_delta = scenario.target_mi - target_mi_alt

            calibration_rng = np.random.default_rng(calibration_seed)
            calibration_p_values = {method: [] for method in METHODS}
            for start in range(0, calibration_replicates, batch_size):
                count = min(batch_size, calibration_replicates - start)
                table_p_cal = calibration_rng.multinomial(
                    scenario.n_p,
                    scenario.probability_p.reshape(-1),
                    size=count,
                ).reshape(count, scenario.rows, scenario.columns)
                table_q_cal = calibration_rng.multinomial(
                    scenario.n_q,
                    scenario.probability_q.reshape(-1),
                    size=count,
                ).reshape(count, scenario.rows, scenario.columns)
                cal_values = _method_values(table_p_cal, table_q_cal)
                for method, specification in METHODS.items():
                    method_valid = cal_values[specification["validity"]]
                    calibration_p_values[method].append(
                        cal_values[specification["p_value"]][method_valid]
                    )
            thresholds = {
                method: (
                    float(np.quantile(np.concatenate(parts), 0.05))
                    if parts and sum(part.size for part in parts)
                    else np.nan
                )
                for method, parts in calibration_p_values.items()
            }

            rng = np.random.default_rng(simulation_seed)
            method_counts = {
                method: {
                    "valid": 0,
                    "rejections": 0,
                    "size_adjusted_rejections": 0,
                    "coverage": 0,
                    "df": [],
                }
                for method in METHODS
            }
            for start in range(0, replicates, batch_size):
                count = min(batch_size, replicates - start)
                table_p = rng.multinomial(
                    scenario.n_p,
                    scenario.probability_p.reshape(-1),
                    size=count,
                ).reshape(count, scenario.rows, scenario.columns)
                table_q = rng.multinomial(
                    scenario.n_q,
                    probability_q_alt.reshape(-1),
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
                    if np.isfinite(thresholds[method]):
                        method_counts[method]["size_adjusted_rejections"] += int(
                            np.count_nonzero(p_values <= thresholds[method])
                        )
                    delta_error = values["delta_corrected"][method_valid] - true_delta
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
                        "scenario_id": scenario.scenario_id,
                        "regime": regime,
                        "regime_label": REGIMES[regime]["label"],
                        "rows": scenario.rows,
                        "columns": scenario.columns,
                        "n_p": scenario.n_p,
                        "n_q": scenario.n_q,
                        "null_mi": scenario.target_mi,
                        "relative_effect": relative_effect,
                        "alternative_mi_q": target_mi_alt,
                        "true_delta": true_delta,
                        "construction_seed": construction_seed,
                        "calibration_seed": calibration_seed,
                        "simulation_seed": simulation_seed,
                        "replicates": replicates,
                        "calibration_replicates": calibration_replicates,
                        "method": method,
                        "method_label": specification["label"],
                        "valid_rate": (
                            method_valid_count / replicates if replicates else np.nan
                        ),
                        "power_05": (
                            method_counts[method]["rejections"] / method_valid_count
                            if method_valid_count
                            else np.nan
                        ),
                        "size_adjusted_threshold": thresholds[method],
                        "size_adjusted_power": (
                            method_counts[method]["size_adjusted_rejections"]
                            / method_valid_count
                            if method_valid_count and np.isfinite(thresholds[method])
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
    return pd.DataFrame(rows), pd.DataFrame(infeasible)


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
                include_simple=False,
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
    columns = 3
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
    figure.suptitle("Equal-MI null calibration by sampling regime")
    figure.tight_layout()
    figure.savefig(output_dir / "calibration_summary.png", dpi=180)
    plt.close(figure)


def _plot_rejection_calibration(
    calibration: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Plot empirical null rejection rates over the lower p-value tail."""
    columns = 3
    rows = int(np.ceil(len(REGIME_ORDER) / columns))
    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(14.4, 13.2),
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
    power: pd.DataFrame,
    power_infeasible: pd.DataFrame,
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
    power_agg = _aggregate_power(power)
    power_view = power_agg[power_agg["regime"].isin(REGIME_ORDER)][
        [
            "regime_label",
            "relative_effect",
            "method_label",
            "mean_power_05",
            "mean_size_adjusted_power",
            "mean_coverage_95",
        ]
    ].rename(
        columns={
            "regime_label": "Regime",
            "relative_effect": "Effect (relative to I0)",
            "method_label": "Method",
            "mean_power_05": "Power at 0.05",
            "mean_size_adjusted_power": "Size-adjusted power",
            "mean_coverage_95": "95% coverage",
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
    well_sampled = summary[summary["regime"].eq("well_sampled")].set_index(
        "method"
    )
    difficult_regimes = (
        "highly_sparse",
        "ultra_sparse",
        "widespread_sparse",
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
        index=["scenario_id", "relative_effect"],
        columns="method",
        values="power_05",
    )
    power_loss = power_pivot["normal_wald"] - power_pivot["expanded_welch"]
    expanded_mean_power_loss = float(power_loss.mean())
    expanded_max_power_loss = float(power_loss.max())
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
            "## Decision rules and reporting conventions",
            "",
            "These were fixed before this run and are not adjusted after seeing",
            "results.",
            "",
            f"- **Adequate size control** at a nominal level `alpha` means the",
            f"  empirical false-positive rate falls in Bradley's liberal interval",
            f"  `[{BRADLEY_LIBERAL_LOWER} * alpha, {BRADLEY_LIBERAL_UPPER} * alpha]`.",
            f"  `adequate_size_control_count_{{label}}` and",
            f"  `inadequate_size_control_count_{{label}}` in `regime_summary.csv`",
            f"  report how many population pairs pass and fail this rule; the",
            f"  continuous mean-absolute-error metric is reported alongside it,",
            f"  never in place of it.",
            f"- **Acceptable validity** requires a method's valid rate at or above",
            f"  `{MINIMUM_ACCEPTABLE_VALID_RATE:.0%}`. Below that floor a scenario is",
            f"  reported as a method failure (`scenarios_below_valid_rate_floor`),",
            f"  not folded into a calibration mean as if it were a well-defined",
            f"  result.",
            f"- **Three rejection-rate denominators are always reported**:",
            f"  `fpr_{{label}}` is conditional on validity; `unconditional_fpr_{{label}}`",
            f"  treats an invalid replicate as a non-rejection (the operational",
            f"  fallback an analyst actually has); `common_valid_fpr_{{label}}`",
            f"  restricts to replicates where every method's statistic is defined,",
            f"  so the three methods in one row always refer to the same",
            f"  underlying replicates. Conditioning on validity alone can be",
            f"  misleading precisely because invalidity is not independent of the",
            f"  test outcome for these estimators.",
            "",
            "## Rejection calibration",
            "",
            "The figure traces the empirical rejection probability over nominal",
            "significance levels from 0 to 0.10. A calibrated test follows the",
            "diagonal. Curves above it are liberal and curves below it are",
            "conservative. Each line is the equal-weight mean across population",
            "pairs in that regime; shading spans their 10th to 90th percentiles.",
            "",
            "![Rejection calibration](rejection_calibration.png)",
            "",
            "## Main calibration results",
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
            f"- Across every population pair and relative effect size, expanded",
            f"  Welch lost `{expanded_mean_power_loss:.4f}` power on average and at",
            f"  most `{expanded_max_power_loss:.4f}` relative to normal Wald at the",
            f"  matched nominal threshold. Nominal power is not a fair comparison",
            f"  when methods do not share the same actual size; size-adjusted power",
            f"  in the table below isolates the difference that remains once size",
            f"  is matched via an independently calibrated per-method threshold.",
            "- The simple Welch correction changed both calibration and power only",
            "  slightly, consistent with its usually large effective degrees of freedom.",
            "- Scenario-level Wilson intervals, sparsity diagnostics, validity rates,",
            "  and effective degrees of freedom are retained in `scenario_results.csv`;",
            "  every population pair's power at every relative effect size is",
            "  retained in `power_summary.csv`.",
            "",
            "## Power",
            "",
            "Effect sizes are relative to each population pair's own null MI",
            "(`I0`), e.g. an effect of `1.0` doubles `I(Q)` relative to `I(P)`.",
            "Size-adjusted power uses a threshold from an independently simulated",
            "null of the same population pair rather than the nominal",
            "`alpha = 0.05` cutoff, and is a diagnostic rather than an achievable",
            "procedure. Per-population-pair power is in `power_summary.csv`.",
            f"{len(power_infeasible)} of "
            f"{power[['scenario_id', 'relative_effect']].drop_duplicates().shape[0] + len(power_infeasible)}"
            " requested (population pair, relative effect) combinations were",
            "infeasible at the requested effect size and are logged, with a",
            "reason, in `power_infeasible_configurations.csv` rather than",
            "silently absent.",
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
            "- `scenario_results.csv`: every scenario-method result, including",
            "  all three rejection-rate denominators and the decision-rule flags.",
            "- `regime_summary.csv`: the presentation-level aggregate table,",
            "  including counts of population pairs passing and failing the",
            "  preregistered decision rules.",
            "- `rejection_calibration_scenarios.csv`: scenario-level rejection",
            "  curves over 101 nominal significance levels.",
            "- `rejection_calibration_regimes.csv`: mean curves and population",
            "  variability bands for each regime and method.",
            "- `null_pvalues.npz`: complete null p-value arrays for follow-up",
            "  calibration or Q-Q plots without rerunning the simulation.",
            "- `power_summary.csv`: alternative-hypothesis power and coverage for",
            "  every population pair at every relative effect size, including",
            "  the independently calibrated size-adjustment threshold.",
            "- `power_infeasible_configurations.csv`: every (population pair,",
            "  relative effect) combination that could not be constructed, with",
            "  a reason, so infeasibility is logged rather than silent.",
            "- `runtime_summary.csv`: end-to-end timing by table size.",
            "- `calibration_summary.png`: one visual comparison across regimes.",
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

    scenarios = generate_strong_null_scenarios(args.scenario_seed - 1)
    scenarios.extend(generate_fixed_density_scenarios(args.scenario_seed))
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
    rejection_calibration = _aggregate_rejection_calibration(
        scenario_calibration
    )
    power_summary, power_infeasible = _simulate_power(
        scenarios,
        relative_effects=RELATIVE_EFFECTS,
        replicates=int(settings["power_replicates"]),
        calibration_replicates=int(settings["power_calibration_replicates"]),
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
    power_infeasible.to_csv(
        args.output_dir / "power_infeasible_configurations.csv",
        index=False,
    )
    runtime_summary.to_csv(
        args.output_dir / "runtime_summary.csv",
        index=False,
    )
    _plot_calibration(regime_summary, args.output_dir)
    _plot_rejection_calibration(rejection_calibration, args.output_dir)
    _write_report(
        args.output_dir,
        profile=args.profile,
        settings=settings,
        scenario_results=scenario_results,
        summary=regime_summary,
        power=power_summary,
        power_infeasible=power_infeasible,
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
