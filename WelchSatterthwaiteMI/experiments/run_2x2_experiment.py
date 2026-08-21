#!/usr/bin/env python3
"""Run interpretable, fixed-configuration 2x2 differential-MI experiments."""

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
from scipy.optimize import brentq
from scipy.stats import norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.distributions import mutual_information_probability  # noqa: E402
from differential_mi.statistics import influence_variance, plugin_mi  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


METHODS = {
    "normal_wald": {
        "label": "Normal Wald",
        "p_value": "normal_p_value",
        "valid": "base_valid",
        "df": None,
    },
    "simple_welch": {
        "label": "Simple Welch",
        "p_value": "welch_p_value",
        "valid": "simple_valid",
        "df": "welch_degrees_of_freedom",
    },
    "expanded_welch": {
        "label": "Expanded Welch",
        "p_value": "expanded_welch_p_value",
        "valid": "expanded_valid",
        "df": "expanded_welch_degrees_of_freedom",
    },
}
METHOD_ORDER = tuple(METHODS)
ALPHAS = (0.10, 0.05, 0.01)
CALIBRATION_ALPHAS = np.linspace(0.0, 0.10, 101)
DEFAULT_SEED = 2_026_082_101

PROFILE_SETTINGS = {
    "smoke": {"replicates": 500, "blocks": 1},
    "screening": {"replicates": 10_000, "blocks": 5},
    "confirmatory": {"replicates": 50_000, "blocks": 5},
}


@dataclass(frozen=True)
class PopulationPair:
    pair_id: str
    purpose: str
    probability_p: np.ndarray
    probability_q: np.ndarray
    u_p: float
    v_p: float
    u_q: float
    v_q: float
    delta_p: float
    delta_q: float
    direction_p: int
    direction_q: int
    mi_p: float
    mi_q: float


@dataclass(frozen=True)
class Configuration:
    configuration_id: str
    experiment: str
    pair: PopulationPair
    n_p: int
    n_q: int
    true_delta: float
    effect_delta_i: float
    power_family: str | None = None
    calibration_key: str | None = None


def _token(value: float) -> str:
    return f"{value:.8g}".replace("-", "m").replace(".", "p")


def probability_table(u: float, v: float, delta: float) -> np.ndarray:
    """Construct a 2x2 table with fixed margins and association delta."""
    if not (0.0 < u < 1.0 and 0.0 < v < 1.0):
        raise ValueError("Margins must lie strictly between zero and one.")
    table = np.array(
        [
            [(1.0 - u) * (1.0 - v) + delta, (1.0 - u) * v - delta],
            [u * (1.0 - v) - delta, u * v + delta],
        ],
        dtype=float,
    )
    if np.any(table < 0.0) or not np.isclose(table.sum(), 1.0, atol=1e-13):
        raise ValueError("Association delta produces invalid probabilities.")
    return table


def solve_target_mi(
    u: float,
    v: float,
    target_mi: float,
    direction: int = 1,
    *,
    tolerance: float = 1e-12,
) -> tuple[np.ndarray, float]:
    """Solve the positive or negative association branch for target MI."""
    if target_mi < 0.0 or direction not in (-1, 1):
        raise ValueError("Target MI must be nonnegative and direction must be +/-1.")
    if target_mi <= tolerance:
        return probability_table(u, v, 0.0), 0.0

    if direction > 0:
        boundary = min((1.0 - u) * v, u * (1.0 - v))
    else:
        boundary = min(u * v, (1.0 - u) * (1.0 - v))
    endpoint = direction * boundary * (1.0 - 1e-12)

    def objective(delta: float) -> float:
        return mutual_information_probability(probability_table(u, v, delta)) - target_mi

    if objective(endpoint) < 0.0:
        maximum = mutual_information_probability(probability_table(u, v, endpoint))
        raise ValueError(
            f"Target MI {target_mi:.12g} exceeds branch maximum {maximum:.12g}."
        )
    lower, upper = (0.0, endpoint) if direction > 0 else (endpoint, 0.0)
    delta = float(brentq(objective, lower, upper, xtol=tolerance, rtol=1e-13))
    table = probability_table(u, v, delta)
    achieved = mutual_information_probability(table)
    if abs(achieved - target_mi) > 1e-10:
        raise RuntimeError("Target-MI solver did not reach the requested value.")
    return table, delta


def make_pair(
    pair_id: str,
    purpose: str,
    margins_p: tuple[float, float],
    margins_q: tuple[float, float],
    target_p: float,
    target_q: float | None = None,
    directions: tuple[int, int] = (1, 1),
) -> PopulationPair:
    """Build one deterministic population pair."""
    target_q = target_p if target_q is None else target_q
    p, delta_p = solve_target_mi(*margins_p, target_p, directions[0])
    q, delta_q = solve_target_mi(*margins_q, target_q, directions[1])
    return PopulationPair(
        pair_id=pair_id,
        purpose=purpose,
        probability_p=p,
        probability_q=q,
        u_p=margins_p[0],
        v_p=margins_p[1],
        u_q=margins_q[0],
        v_q=margins_q[1],
        delta_p=delta_p,
        delta_q=delta_q,
        direction_p=directions[0],
        direction_q=directions[1],
        mi_p=mutual_information_probability(p),
        mi_q=mutual_information_probability(q),
    )


def fixed_null_pairs() -> dict[str, PopulationPair]:
    specifications = (
        ("N0", "Identical-population control", (0.50, 0.50), (0.50, 0.50), 0.1000, (1, 1)),
        ("N1", "Same margins, opposite association", (0.50, 0.50), (0.50, 0.50), 0.1000, (1, -1)),
        ("N2", "Mild margin mismatch", (0.50, 0.50), (0.30, 0.40), 0.1000, (1, 1)),
        ("N3", "One skewed population", (0.30, 0.40), (0.10, 0.30), 0.0300, (1, 1)),
        ("N4", "Two sparse, differently shaped populations", (0.10, 0.10), (0.05, 0.20), 0.0100, (1, 1)),
        ("N5", "Extreme rare categories", (0.02, 0.02), (0.01, 0.05), 0.0050, (1, 1)),
        ("N6", "Sparse margins and opposite association", (0.10, 0.10), (0.05, 0.20), 0.0050, (1, -1)),
        ("N7", "Ultra-rare categories", (0.005, 0.005), (0.002, 0.010), 0.0005, (1, 1)),
    )
    return {
        pair_id: make_pair(pair_id, purpose, p, q, target, directions=directions)
        for pair_id, purpose, p, q, target, directions in specifications
    }


def _configuration(
    experiment: str,
    pair: PopulationPair,
    n_p: int,
    n_q: int,
    suffix: str,
    *,
    effect_delta_i: float = 0.0,
    power_family: str | None = None,
    calibration_key: str | None = None,
) -> Configuration:
    return Configuration(
        configuration_id=f"{experiment}_{pair.pair_id}_{suffix}",
        experiment=experiment,
        pair=pair,
        n_p=int(n_p),
        n_q=int(n_q),
        true_delta=pair.mi_p - pair.mi_q,
        effect_delta_i=effect_delta_i,
        power_family=power_family,
        calibration_key=calibration_key,
    )


def build_null_configurations() -> tuple[list[Configuration], list[dict]]:
    """Build C1-C4 without filtering on expected counts."""
    result: list[Configuration] = []
    infeasible: list[dict] = []
    pairs = fixed_null_pairs()

    for pair in pairs.values():
        for n in (10, 20, 30, 50, 100, 200, 500, 1000):
            result.append(_configuration("C1", pair, n, n, f"n{n}"))

    for pair_id in ("N0", "N3", "N5", "N7"):
        pair = pairs[pair_id]
        for smaller in (10, 20, 50, 100, 200):
            for ratio in (2, 5, 10):
                larger = ratio * smaller
                result.append(
                    _configuration(
                        "C2", pair, smaller, larger, f"np{smaller}_nq{larger}"
                    )
                )
                result.append(
                    _configuration(
                        "C2", pair, larger, smaller, f"np{larger}_nq{smaller}"
                    )
                )

    target_values = (0.0, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1)
    c3_pairs = (
        ("same_balanced", "Near-zero MI with identical balanced margins", (0.5, 0.5), (0.5, 0.5)),
        ("shape_mismatch", "Near-zero MI with different margins", (0.5, 0.5), (0.3, 0.4)),
    )
    for label, purpose, margins_p, margins_q in c3_pairs:
        for target in target_values:
            pair_id = f"C3_{label}_i{_token(target)}"
            pair = make_pair(pair_id, purpose, margins_p, margins_q, target)
            for n in (20, 50, 100, 200, 500, 1000):
                result.append(_configuration("C3", pair, n, n, f"n{n}"))

    for s in (0.20, 0.10, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001):
        for target in (1e-4, 0.005):
            pair_id = f"C4_s{_token(s)}_i{_token(target)}"
            try:
                pair = make_pair(
                    pair_id,
                    "Rare-cell breakdown ladder",
                    (s, s),
                    (s / 2.0, 2.0 * s),
                    target,
                )
            except ValueError as error:
                infeasible.append(
                    {
                        "experiment": "C4",
                        "pair_id": pair_id,
                        "s": s,
                        "target_mi": target,
                        "reason": str(error),
                    }
                )
                continue
            for n in (10, 20, 50, 100, 200, 500, 1000):
                result.append(_configuration("C4", pair, n, n, f"n{n}"))

    identifiers = [item.configuration_id for item in result]
    if len(identifiers) != len(set(identifiers)):
        raise RuntimeError("Null configuration identifiers are not unique.")
    return result, infeasible


POWER_FAMILIES = {
    "balanced_mild": {
        "label": "Balanced/mild",
        "margins_p": (0.50, 0.50),
        "margins_q": (0.30, 0.40),
        "mi_p": 0.050,
        "effects": (-0.040, -0.025, -0.010, -0.005, 0.0, 0.005, 0.010, 0.025, 0.050, 0.100),
    },
    "sparse": {
        "label": "Sparse",
        "margins_p": (0.10, 0.10),
        "margins_q": (0.05, 0.20),
        "mi_p": 0.010,
        "effects": (-0.009, -0.005, -0.002, 0.0, 0.002, 0.005, 0.010, 0.020, 0.040),
    },
    "extreme_rare": {
        "label": "Extreme rare",
        "margins_p": (0.02, 0.02),
        "margins_q": (0.01, 0.05),
        "mi_p": 0.001,
        "effects": (-0.0009, -0.0005, 0.0, 0.0005, 0.001, 0.002, 0.005, 0.010),
    },
}


def _power_pair(family: str, effect: float) -> PopulationPair:
    specification = POWER_FAMILIES[family]
    target_q = float(specification["mi_p"]) + effect
    return make_pair(
        f"{family}_di{_token(effect)}",
        f"{specification['label']} power family",
        specification["margins_p"],
        specification["margins_q"],
        float(specification["mi_p"]),
        target_q,
    )


def _calibration_key(family: str, n_p: int, n_q: int) -> str:
    return f"{family}_np{n_p}_nq{n_q}"


def build_power_configurations() -> list[Configuration]:
    result: list[Configuration] = []
    for family, specification in POWER_FAMILIES.items():
        for effect in specification["effects"]:
            pair = _power_pair(family, float(effect))
            for n in (10, 20, 30, 50, 100, 200, 500, 1000):
                key = _calibration_key(family, n, n)
                result.append(
                    _configuration(
                        "P1",
                        pair,
                        n,
                        n,
                        f"n{n}",
                        effect_delta_i=float(effect),
                        power_family=family,
                        calibration_key=key,
                    )
                )
            if effect >= 0.0:
                for smaller in (20, 50, 100):
                    for ratio in (2, 5, 10):
                        larger = smaller * ratio
                        key = _calibration_key(family, smaller, larger)
                        result.append(
                            _configuration(
                                "P2",
                                pair,
                                smaller,
                                larger,
                                f"np{smaller}_nq{larger}",
                                effect_delta_i=float(effect),
                                power_family=family,
                                calibration_key=key,
                            )
                        )
    identifiers = [item.configuration_id for item in result]
    if len(identifiers) != len(set(identifiers)):
        raise RuntimeError("Power configuration identifiers are not unique.")
    return result


def power_calibration_configuration(config: Configuration) -> Configuration:
    if config.power_family is None or config.calibration_key is None:
        raise ValueError("Expected a power configuration.")
    specification = POWER_FAMILIES[config.power_family]
    target = float(specification["mi_p"])
    pair = make_pair(
        f"PCAL_{config.calibration_key}",
        f"{specification['label']} size-adjustment null",
        specification["margins_p"],
        specification["margins_q"],
        target,
        target,
    )
    return _configuration(
        "PCAL",
        pair,
        config.n_p,
        config.n_q,
        config.calibration_key,
        power_family=config.power_family,
        calibration_key=config.calibration_key,
    )


def _seed(base_seed: int, *parts: object) -> int:
    text = "|".join([str(base_seed), *(str(part) for part in parts)])
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "little")


def _sample_diagnostics(table: np.ndarray) -> dict[str, np.ndarray]:
    row = table.sum(axis=2)
    column = table.sum(axis=1)
    return {
        "any_zero_cell": np.any(table == 0, axis=(1, 2)),
        "empty_margin": np.any(row == 0, axis=1) | np.any(column == 0, axis=1),
        "zero_cell_fraction": np.mean(table == 0, axis=(1, 2)),
    }


def simulate_configuration(
    config: Configuration,
    *,
    replicates: int,
    blocks: int,
    base_seed: int,
    stream: str,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], list[dict]]:
    """Simulate one exact configuration in independent seed blocks."""
    if replicates < blocks or replicates % blocks != 0:
        raise ValueError("Replicates must be positive and divisible by blocks.")
    per_block = replicates // blocks
    pieces: dict[str, list[np.ndarray]] = {}
    diagnostic_pieces: dict[str, list[np.ndarray]] = {}
    block_rows: list[dict] = []

    for block in range(blocks):
        rng = np.random.default_rng(
            _seed(base_seed, stream, config.configuration_id, block)
        )
        table_p = rng.multinomial(
            config.n_p,
            config.pair.probability_p.reshape(-1),
            size=per_block,
        ).reshape(per_block, 2, 2)
        table_q = rng.multinomial(
            config.n_q,
            config.pair.probability_q.reshape(-1),
            size=per_block,
        ).reshape(per_block, 2, 2)
        values = differential_mi_pvalues(table_p, table_q)
        diagnostics_p = _sample_diagnostics(table_p)
        diagnostics_q = _sample_diagnostics(table_q)

        for name, value in values.items():
            pieces.setdefault(name, []).append(np.asarray(value))
        for name, value in diagnostics_p.items():
            diagnostic_pieces.setdefault(f"p_{name}", []).append(value)
        for name, value in diagnostics_q.items():
            diagnostic_pieces.setdefault(f"q_{name}", []).append(value)

        for method, specification in METHODS.items():
            valid = np.asarray(values[specification["valid"]], dtype=bool)
            p_values = np.asarray(values[specification["p_value"]], dtype=float)
            rejected = valid & (p_values <= 0.05)
            block_rows.append(
                {
                    "configuration_id": config.configuration_id,
                    "experiment": config.experiment,
                    "block": block,
                    "stream": stream,
                    "method": method,
                    "method_label": specification["label"],
                    "replicates": per_block,
                    "valid_count": int(np.count_nonzero(valid)),
                    "valid_rate": float(np.mean(valid)),
                    "reject_count_05": int(np.count_nonzero(rejected)),
                    "rejection_rate_valid_05": (
                        float(np.mean(p_values[valid] <= 0.05))
                        if np.any(valid)
                        else np.nan
                    ),
                    "unconditional_rejection_rate_05": float(np.mean(rejected)),
                }
            )

    combined = {name: np.concatenate(value) for name, value in pieces.items()}
    diagnostics = {
        name: np.concatenate(value) for name, value in diagnostic_pieces.items()
    }
    return combined, diagnostics, block_rows


def _wilson(successes: int, total: int) -> tuple[float, float]:
    if total <= 0:
        return np.nan, np.nan
    z = norm.ppf(0.975)
    proportion = successes / total
    denominator = 1.0 + z * z / total
    center = (proportion + z * z / (2.0 * total)) / denominator
    radius = (
        z
        * np.sqrt(proportion * (1.0 - proportion) / total + z * z / (4.0 * total**2))
        / denominator
    )
    return float(center - radius), float(center + radius)


def _invalidity_counts(values: dict[str, np.ndarray], method: str) -> dict[str, int]:
    """Count shared-statistic and method-specific validity failures."""
    base_valid = np.asarray(values["base_valid"], dtype=bool)
    result = {
        "invalid_shared_statistic_count": int(np.count_nonzero(~base_valid)),
        "invalid_reference_count": 0,
        "invalid_component_p_count": 0,
        "invalid_component_q_count": 0,
        "invalid_combined_df_count": 0,
    }
    if method == "normal_wald":
        return result

    valid_name = "simple_valid" if method == "simple_welch" else "expanded_valid"
    method_valid = np.asarray(values[valid_name], dtype=bool)
    result["invalid_reference_count"] = int(
        np.count_nonzero(base_valid & ~method_valid)
    )
    if method == "expanded_welch":
        component_p = np.asarray(
            values["expanded_component_degrees_of_freedom_p"], dtype=float
        )
        component_q = np.asarray(
            values["expanded_component_degrees_of_freedom_q"], dtype=float
        )
        combined = np.asarray(
            values["expanded_welch_degrees_of_freedom"], dtype=float
        )
        result["invalid_component_p_count"] = int(
            np.count_nonzero(base_valid & (~np.isfinite(component_p) | (component_p <= 0)))
        )
        result["invalid_component_q_count"] = int(
            np.count_nonzero(base_valid & (~np.isfinite(component_q) | (component_q <= 0)))
        )
        result["invalid_combined_df_count"] = int(
            np.count_nonzero(base_valid & (~np.isfinite(combined) | (combined <= 0)))
        )
    return result


def _metadata(config: Configuration) -> dict:
    p = config.pair.probability_p
    q = config.pair.probability_q
    expected_p = config.n_p * p
    expected_q = config.n_q * q
    return {
        "configuration_id": config.configuration_id,
        "experiment": config.experiment,
        "population_pair_id": config.pair.pair_id,
        "purpose": config.pair.purpose,
        "power_family": config.power_family,
        "calibration_key": config.calibration_key,
        "n_p": config.n_p,
        "n_q": config.n_q,
        "sample_size_ratio_q_over_p": config.n_q / config.n_p,
        "u_p": config.pair.u_p,
        "v_p": config.pair.v_p,
        "u_q": config.pair.u_q,
        "v_q": config.pair.v_q,
        "association_direction_p": config.pair.direction_p,
        "association_direction_q": config.pair.direction_q,
        "association_delta_p": config.pair.delta_p,
        "association_delta_q": config.pair.delta_q,
        "true_mi_p": config.pair.mi_p,
        "true_mi_q": config.pair.mi_q,
        "true_delta_p_minus_q": config.true_delta,
        "effect_delta_i_q_minus_p": config.effect_delta_i,
        "minimum_probability_p": float(np.min(p)),
        "minimum_probability_q": float(np.min(q)),
        "minimum_expected_p": float(np.min(expected_p)),
        "minimum_expected_q": float(np.min(expected_q)),
        "minimum_expected_either": float(min(np.min(expected_p), np.min(expected_q))),
        "probability_p_json": json.dumps(p.tolist()),
        "probability_q_json": json.dumps(q.tolist()),
        "expected_p_json": json.dumps(expected_p.tolist()),
        "expected_q_json": json.dumps(expected_q.tolist()),
        "population_variance_p": float(influence_variance(p)),
        "population_variance_q": float(influence_variance(q)),
    }


def configuration_frame(configurations: list[Configuration]) -> pd.DataFrame:
    return pd.DataFrame([_metadata(config) for config in configurations])


def summarize_null(
    config: Configuration,
    values: dict[str, np.ndarray],
    diagnostics: dict[str, np.ndarray],
) -> tuple[list[dict], list[dict], dict]:
    metadata = _metadata(config)
    summary_rows: list[dict] = []
    curve_rows: list[dict] = []
    delta = np.asarray(values["delta_corrected"], dtype=float)
    standard_error = np.asarray(values["standard_error"], dtype=float)

    mechanism = {
        **metadata,
        "replicates": len(delta),
        "mean_delta_corrected": float(np.nanmean(delta)),
        "sd_delta_corrected": float(np.nanstd(delta, ddof=1)),
        "mean_standard_error": float(np.nanmean(standard_error)),
        "rms_standard_error": float(np.sqrt(np.nanmean(standard_error**2))),
        "sd_to_rms_se_ratio": (
            float(np.nanstd(delta, ddof=1) / np.sqrt(np.nanmean(standard_error**2)))
            if np.nanmean(standard_error**2) > 0
            else np.nan
        ),
        "mean_influence_variance_p": float(np.nanmean(values["influence_variance_p"])),
        "mean_influence_variance_q": float(np.nanmean(values["influence_variance_q"])),
        "mean_variance_influence_variance_p": float(
            np.nanmean(values["variance_influence_variance_p"])
        ),
        "mean_variance_influence_variance_q": float(
            np.nanmean(values["variance_influence_variance_q"])
        ),
        "any_zero_cell_rate_p": float(np.mean(diagnostics["p_any_zero_cell"])),
        "any_zero_cell_rate_q": float(np.mean(diagnostics["q_any_zero_cell"])),
        "empty_margin_rate_p": float(np.mean(diagnostics["p_empty_margin"])),
        "empty_margin_rate_q": float(np.mean(diagnostics["q_empty_margin"])),
        "mean_zero_cell_fraction_p": float(np.mean(diagnostics["p_zero_cell_fraction"])),
        "mean_zero_cell_fraction_q": float(np.mean(diagnostics["q_zero_cell_fraction"])),
        "zero_estimated_variance_rate_p": float(
            np.mean(np.asarray(values["influence_variance_p"]) <= 1e-14)
        ),
        "zero_estimated_variance_rate_q": float(
            np.mean(np.asarray(values["influence_variance_q"]) <= 1e-14)
        ),
    }

    for method, specification in METHODS.items():
        valid = np.asarray(values[specification["valid"]], dtype=bool)
        p_values = np.asarray(values[specification["p_value"]], dtype=float)
        valid_count = int(np.count_nonzero(valid))
        row = {
            **metadata,
            "method": method,
            "method_label": specification["label"],
            "replicates": len(valid),
            "valid_count": valid_count,
            "invalid_count": len(valid) - valid_count,
            "valid_rate": float(np.mean(valid)),
        }
        row.update(_invalidity_counts(values, method))

        if specification["df"] is None:
            degrees = np.full(len(valid), np.inf)
        else:
            degrees = np.asarray(values[specification["df"]], dtype=float)
        finite_degrees = degrees[valid & np.isfinite(degrees)]
        row.update(
            {
                "mean_degrees_of_freedom": (
                    float(np.mean(finite_degrees)) if finite_degrees.size else np.inf
                ),
                "median_degrees_of_freedom": (
                    float(np.median(finite_degrees)) if finite_degrees.size else np.inf
                ),
                "p10_degrees_of_freedom": (
                    float(np.quantile(finite_degrees, 0.10))
                    if finite_degrees.size
                    else np.inf
                ),
                "p90_degrees_of_freedom": (
                    float(np.quantile(finite_degrees, 0.90))
                    if finite_degrees.size
                    else np.inf
                ),
            }
        )

        if method == "normal_wald":
            critical = np.full(len(valid), norm.ppf(0.975))
        else:
            critical = t.ppf(0.975, df=degrees)
        covered = valid & (
            np.abs(delta - config.true_delta) <= critical * standard_error
        )
        row["coverage_95_valid"] = (
            float(np.count_nonzero(covered) / valid_count) if valid_count else np.nan
        )

        for alpha in ALPHAS:
            label = f"{int(round(alpha * 100)):02d}"
            rejected = valid & (p_values <= alpha)
            false_positive_count = int(np.count_nonzero(rejected))
            true_negative_count = valid_count - false_positive_count
            fpr = false_positive_count / valid_count if valid_count else np.nan
            tnr = true_negative_count / valid_count if valid_count else np.nan
            low, high = _wilson(false_positive_count, valid_count)
            row.update(
                {
                    f"false_positive_count_{label}": false_positive_count,
                    f"true_negative_count_{label}": true_negative_count,
                    f"false_positive_rate_{label}": fpr,
                    f"true_negative_rate_{label}": tnr,
                    f"fpr_wilson_low_{label}": low,
                    f"fpr_wilson_high_{label}": high,
                    f"absolute_fpr_error_{label}": abs(fpr - alpha),
                    f"unconditional_rejection_rate_{label}": float(np.mean(rejected)),
                }
            )

        for alpha in CALIBRATION_ALPHAS:
            rejected_count = int(np.count_nonzero(valid & (p_values <= alpha)))
            rate = rejected_count / valid_count if valid_count else np.nan
            curve_rows.append(
                {
                    "configuration_id": config.configuration_id,
                    "experiment": config.experiment,
                    "population_pair_id": config.pair.pair_id,
                    "n_p": config.n_p,
                    "n_q": config.n_q,
                    "method": method,
                    "method_label": specification["label"],
                    "nominal_alpha": float(alpha),
                    "rejection_count": rejected_count,
                    "valid_count": valid_count,
                    "rejection_rate": rate,
                    "true_negative_rate": 1.0 - rate if np.isfinite(rate) else np.nan,
                }
            )
        summary_rows.append(row)

    for name in (
        "welch_degrees_of_freedom",
        "expanded_welch_degrees_of_freedom",
        "expanded_component_degrees_of_freedom_p",
        "expanded_component_degrees_of_freedom_q",
    ):
        array = np.asarray(values[name], dtype=float)
        finite = array[np.isfinite(array)]
        mechanism[f"mean_{name}"] = float(np.mean(finite)) if finite.size else np.nan
        mechanism[f"median_{name}"] = (
            float(np.median(finite)) if finite.size else np.nan
        )
    return summary_rows, curve_rows, mechanism


def _size_adjustment_thresholds(values: dict[str, np.ndarray]) -> list[dict]:
    rows: list[dict] = []
    for method, specification in METHODS.items():
        valid = np.asarray(values[specification["valid"]], dtype=bool)
        p_values = np.asarray(values[specification["p_value"]], dtype=float)
        usable = p_values[valid & np.isfinite(p_values)]
        threshold = (
            float(np.quantile(usable, 0.05, method="linear"))
            if usable.size
            else np.nan
        )
        rows.append(
            {
                "method": method,
                "method_label": specification["label"],
                "valid_count": int(usable.size),
                "valid_rate": float(np.mean(valid)),
                "p_value_threshold_for_five_percent": threshold,
            }
        )
    return rows


def summarize_power(
    config: Configuration,
    values: dict[str, np.ndarray],
    thresholds: dict[str, float],
) -> list[dict]:
    rows: list[dict] = []
    metadata = _metadata(config)
    is_null = abs(config.effect_delta_i) < 1e-15
    for method, specification in METHODS.items():
        valid = np.asarray(values[specification["valid"]], dtype=bool)
        p_values = np.asarray(values[specification["p_value"]], dtype=float)
        valid_count = int(np.count_nonzero(valid))
        rejected = valid & (p_values <= 0.05)
        reject_count = int(np.count_nonzero(rejected))
        nonreject_count = valid_count - reject_count
        rejection_rate = reject_count / valid_count if valid_count else np.nan
        low, high = _wilson(reject_count, valid_count)
        adjusted_threshold = thresholds.get(method, np.nan)
        adjusted_rejected = valid & (p_values <= adjusted_threshold)
        adjusted_count = int(np.count_nonzero(adjusted_rejected))
        adjusted_rate = adjusted_count / valid_count if valid_count else np.nan
        rows.append(
            {
                **metadata,
                "method": method,
                "method_label": specification["label"],
                "truth": "null" if is_null else "alternative",
                "replicates": len(valid),
                "valid_count": valid_count,
                "invalid_count": len(valid) - valid_count,
                "valid_rate": float(np.mean(valid)),
                **_invalidity_counts(values, method),
                "reject_count_05": reject_count,
                "nonreject_count_05": nonreject_count,
                "false_positive_count_05": reject_count if is_null else np.nan,
                "true_negative_count_05": nonreject_count if is_null else np.nan,
                "true_positive_count_05": reject_count if not is_null else np.nan,
                "false_negative_count_05": nonreject_count if not is_null else np.nan,
                "false_positive_rate_05": rejection_rate if is_null else np.nan,
                "true_negative_rate_05": 1.0 - rejection_rate if is_null else np.nan,
                "true_positive_rate_05": rejection_rate if not is_null else np.nan,
                "false_negative_rate_05": 1.0 - rejection_rate if not is_null else np.nan,
                "nominal_rejection_rate_05": rejection_rate,
                "rejection_wilson_low_05": low,
                "rejection_wilson_high_05": high,
                "unconditional_rejection_rate_05": float(np.mean(rejected)),
                "size_adjustment_p_threshold": adjusted_threshold,
                "size_adjusted_reject_count": adjusted_count,
                "size_adjusted_rejection_rate": adjusted_rate,
                "size_adjusted_power": adjusted_rate if not is_null else np.nan,
                "size_adjusted_fpr": adjusted_rate if is_null else np.nan,
            }
        )
    return rows


def correctness_checks() -> pd.DataFrame:
    rows: list[dict] = []
    pairs = list(fixed_null_pairs().values())
    pairs.extend(config.pair for config in build_power_configurations()[:3])
    for pair in pairs:
        for label, table, u, v, target, delta in (
            ("P", pair.probability_p, pair.u_p, pair.v_p, pair.mi_p, pair.delta_p),
            ("Q", pair.probability_q, pair.u_q, pair.v_q, pair.mi_q, pair.delta_q),
        ):
            checks = {
                "sum_to_one": abs(float(table.sum()) - 1.0) <= 1e-12,
                "strictly_positive": bool(np.all(table > 0.0)),
                "row_margin": np.allclose(table.sum(axis=1), [1.0 - u, u], atol=1e-12),
                "column_margin": np.allclose(table.sum(axis=0), [1.0 - v, v], atol=1e-12),
                "target_mi": abs(mutual_information_probability(table) - target) <= 1e-10,
                "plugin_probability_mi": abs(float(plugin_mi(table)) - target) <= 1e-10,
                "delta_reconstruction": np.allclose(table, probability_table(u, v, delta), atol=1e-12),
            }
            for check, passed in checks.items():
                rows.append(
                    {
                        "pair_id": pair.pair_id,
                        "population": label,
                        "check": check,
                        "passed": passed,
                    }
                )

    table_p = np.array([[18, 2], [3, 17]])
    table_q = np.array([[60, 5], [8, 47]])
    base = differential_mi_pvalues(table_p, table_q)
    swapped = differential_mi_pvalues(table_q, table_p)
    relabelled = differential_mi_pvalues(
        table_p[::-1, ::-1], table_q[::-1, ::-1]
    )
    invariants = {
        "swap_statistic_sign": np.isclose(base["statistic"], -swapped["statistic"]),
        "swap_expanded_p": np.isclose(
            base["expanded_welch_p_value"], swapped["expanded_welch_p_value"]
        ),
        "relabel_expanded_p": np.isclose(
            base["expanded_welch_p_value"], relabelled["expanded_welch_p_value"]
        ),
        "bias_df_is_one": (table_p.shape[0] - 1) * (table_p.shape[1] - 1) == 1,
    }
    for check, passed in invariants.items():
        rows.append(
            {"pair_id": "implementation", "population": "pair", "check": check, "passed": bool(passed)}
        )
    result = pd.DataFrame(rows)
    if not bool(result["passed"].all()):
        failures = result.loc[~result["passed"]].to_dict(orient="records")
        raise RuntimeError(f"Correctness checks failed: {failures}")
    return result


def _markdown(frame: pd.DataFrame, digits: int = 5) -> str:
    def format_value(value: object) -> str:
        if pd.isna(value):
            return "-"
        if isinstance(value, (float, np.floating)):
            if np.isinf(value):
                return "inf" if value > 0 else "-inf"
            return f"{float(value):.{digits}g}"
        return str(value).replace("|", "\\|").replace("\n", " ")

    headers = [str(column).replace("|", "\\|") for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(format_value(value) for value in row) + " |")
    return "\n".join(lines)


def write_case_sheets(
    output_dir: Path,
    configurations: pd.DataFrame,
    null_summary: pd.DataFrame,
    power_summary: pd.DataFrame,
) -> None:
    directory = output_dir / "case_sheets"
    directory.mkdir(parents=True, exist_ok=True)
    null_configs = configurations[configurations["experiment"].str.startswith("C")]
    for pair_id, config_group in null_configs.groupby("population_pair_id", sort=True):
        details = config_group.iloc[0]
        results = null_summary[null_summary["population_pair_id"].eq(pair_id)]
        view = results[
            [
                "configuration_id",
                "experiment",
                "n_p",
                "n_q",
                "minimum_expected_either",
                "method_label",
                "false_positive_rate_05",
                "true_negative_rate_05",
                "coverage_95_valid",
                "valid_rate",
                "median_degrees_of_freedom",
            ]
        ].sort_values(["experiment", "n_p", "n_q", "method_label"])
        lines = [
            f"# {pair_id}: {details['purpose']}",
            "",
            "## Population tables",
            "",
            f"- True MI: P = `{details['true_mi_p']:.10g}`, Q = `{details['true_mi_q']:.10g}` nats.",
            f"- P margins: `({details['u_p']:.6g}, {details['v_p']:.6g})`.",
            f"- Q margins: `({details['u_q']:.6g}, {details['v_q']:.6g})`.",
            f"- P probabilities: `{details['probability_p_json']}`.",
            f"- Q probabilities: `{details['probability_q_json']}`.",
            "",
            "## Configuration-level results at alpha = 0.05",
            "",
            _markdown(view),
            "",
            "No row is averaged with another population pair or sample-size setting.",
            "",
        ]
        (directory / f"{pair_id}.md").write_text("\n".join(lines), encoding="utf-8")

    for family, specification in POWER_FAMILIES.items():
        results = power_summary[power_summary["power_family"].eq(family)]
        view = results[
            [
                "configuration_id",
                "experiment",
                "n_p",
                "n_q",
                "effect_delta_i_q_minus_p",
                "method_label",
                "truth",
                "nominal_rejection_rate_05",
                "size_adjusted_rejection_rate",
                "valid_rate",
            ]
        ].sort_values(
            ["experiment", "n_p", "n_q", "effect_delta_i_q_minus_p", "method_label"]
        )
        lines = [
            f"# Power family: {specification['label']}",
            "",
            f"P margins: `{specification['margins_p']}`; Q margins: `{specification['margins_q']}`.",
            f"Baseline I(P): `{specification['mi_p']}` nats.",
            "",
            "## Configuration-level rejection results",
            "",
            _markdown(view),
            "",
        ]
        (directory / f"POWER_{family}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )


COLORS = {
    "normal_wald": "#24557A",
    "simple_welch": "#D87928",
    "expanded_welch": "#16806A",
}


def plot_results(
    output_dir: Path,
    null_summary: pd.DataFrame,
    rejection_curves: pd.DataFrame,
    power_summary: pd.DataFrame,
) -> None:
    figures = output_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.dpi": 130, "font.size": 9})

    c1 = null_summary[null_summary["experiment"].eq("C1")]
    for pair_id, group in c1.groupby("population_pair_id", sort=True):
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for method in METHOD_ORDER:
            curve = group[group["method"].eq(method)].sort_values("n_p")
            axes[0].plot(
                curve["n_p"],
                curve["false_positive_rate_05"],
                marker="o",
                label=METHODS[method]["label"],
                color=COLORS[method],
            )
            axes[1].plot(
                curve["n_p"],
                curve["valid_rate"],
                marker="o",
                label=METHODS[method]["label"],
                color=COLORS[method],
            )
        axes[0].axhline(0.05, color="black", linestyle=":", linewidth=1)
        axes[0].set_ylabel("False-positive rate")
        axes[1].set_ylabel("Valid-result rate")
        for axis in axes:
            axis.set_xscale("log")
            axis.set_xlabel("Sample size in each population")
            axis.grid(alpha=0.25)
        axes[0].legend(frameon=False, fontsize=8)
        fig.suptitle(f"{pair_id}: configuration-level null results")
        fig.tight_layout()
        fig.savefig(figures / f"C1_{pair_id}_fpr_validity.png", bbox_inches="tight")
        plt.close(fig)

    selected_curves = rejection_curves[
        rejection_curves["experiment"].eq("C1")
        & rejection_curves["n_p"].isin([10, 50, 200, 1000])
    ]
    for (pair_id, n), group in selected_curves.groupby(
        ["population_pair_id", "n_p"], sort=True
    ):
        fig, axis = plt.subplots(figsize=(5, 4.5))
        axis.plot([0, 0.1], [0, 0.1], color="black", linestyle=":", label="Ideal")
        for method in METHOD_ORDER:
            curve = group[group["method"].eq(method)].sort_values("nominal_alpha")
            axis.plot(
                curve["nominal_alpha"],
                curve["rejection_rate"],
                label=METHODS[method]["label"],
                color=COLORS[method],
            )
        axis.set_xlabel("Nominal significance level")
        axis.set_ylabel("Actual rejection rate")
        axis.set_title(f"{pair_id}, nP = nQ = {n}")
        axis.grid(alpha=0.25)
        axis.legend(frameon=False, fontsize=8)
        fig.tight_layout()
        fig.savefig(figures / f"CAL_{pair_id}_n{n}.png", bbox_inches="tight")
        plt.close(fig)

    equal_power = power_summary[power_summary["experiment"].eq("P1")]
    for family, family_group in equal_power.groupby("power_family", sort=True):
        for n, group in family_group.groupby("n_p", sort=True):
            fig, axis = plt.subplots(figsize=(5.5, 4.3))
            for method in METHOD_ORDER:
                curve = group[group["method"].eq(method)].sort_values(
                    "effect_delta_i_q_minus_p"
                )
                axis.plot(
                    curve["effect_delta_i_q_minus_p"],
                    curve["nominal_rejection_rate_05"],
                    marker="o",
                    label=METHODS[method]["label"],
                    color=COLORS[method],
                )
            axis.axvline(0.0, color="black", linestyle=":", linewidth=1)
            axis.set_xlabel("True MI difference: I(Q) - I(P), nats")
            axis.set_ylabel("Rejection rate at alpha = 0.05")
            axis.set_title(f"{POWER_FAMILIES[family]['label']}, nP = nQ = {n}")
            axis.grid(alpha=0.25)
            axis.legend(frameon=False, fontsize=8)
            fig.tight_layout()
            fig.savefig(figures / f"POWER_{family}_n{n}.png", bbox_inches="tight")
            plt.close(fig)


def write_report(
    output_dir: Path,
    profile: str,
    configurations: pd.DataFrame,
    null_summary: pd.DataFrame,
    power_summary: pd.DataFrame,
    infeasible: pd.DataFrame,
) -> None:
    lines = [
        "# 2x2 Expanded Welch-Satterthwaite Experiment",
        "",
        "## Scope",
        "",
        f"Profile: `{profile}`.",
        f"Exact simulated configurations: `{len(configurations):,}`.",
        "Each result below belongs to one exact population pair and sample-size setting.",
        "No false-positive rate or power value is averaged across configurations.",
        "",
        "## Equal-size null calibration",
        "",
    ]
    c1 = null_summary[null_summary["experiment"].eq("C1")]
    for pair_id, group in c1.groupby("population_pair_id", sort=True):
        pivot = group.pivot_table(
            index=["n_p", "minimum_expected_either"],
            columns="method_label",
            values=["false_positive_rate_05", "true_negative_rate_05", "valid_rate"],
            aggfunc="first",
        )
        pivot.columns = [f"{metric}: {method}" for metric, method in pivot.columns]
        pivot = pivot.reset_index()
        lines.extend(
            [
                f"### {pair_id}",
                "",
                _markdown(pivot),
                "",
                f"Full case sheet: [`case_sheets/{pair_id}.md`](case_sheets/{pair_id}.md).",
                "",
            ]
        )

    lines.extend(
        [
            "## Other null experiments",
            "",
            "C2-C4 are reported configuration by configuration in `null_summary.csv` and",
            "the corresponding files under `case_sheets/`.",
            "",
            "## Power",
            "",
            "Power rows distinguish the null point from true alternatives and include",
            "false-positive, true-negative, true-positive, and false-negative counts.",
            "Nominal and size-adjusted rejection rates are both retained.",
            "",
        ]
    )
    for family, specification in POWER_FAMILIES.items():
        lines.append(
            f"- [{specification['label']}](case_sheets/POWER_{family}.md)"
        )
    if not infeasible.empty:
        lines.extend(
            [
                "",
                "## Mathematically infeasible requests",
                "",
                "These settings were not simulated because the requested MI exceeds the",
                "attainable range for the fixed margins. They were not removed for low",
                "expected counts.",
                "",
                _markdown(infeasible),
            ]
        )
    lines.extend(
        [
            "",
            "## Output guide",
            "",
            "- `configurations.csv`: exact P, Q, sample sizes, MI, and expected counts.",
            "- `null_summary.csv`: configuration-specific null decisions and diagnostics.",
            "- `power_summary.csv`: configuration-specific null/alternative decisions.",
            "- `rejection_curves.csv.gz`: lower-tail calibration for every null configuration.",
            "- `mechanism_diagnostics.csv`: estimator, standard-error, sparsity, and df diagnostics.",
            "- `replicate_blocks.csv`: independent seed-block stability.",
            "- `power_null_thresholds.csv`: independent size-adjustment thresholds.",
            "- `case_sheets/`: readable records for each population pair.",
            "- `figures/`: unpooled calibration, validity, and power plots.",
            "",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=PROFILE_SETTINGS, default="smoke")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--blocks", type=int)
    parser.add_argument("--sections", choices=("all", "null", "power"), default="all")
    parser.add_argument("--configuration-limit", type=int)
    parser.add_argument("--selection-file", type=Path)
    return parser.parse_args()


def _selected_ids(path: Path | None) -> tuple[set[str] | None, set[str] | None]:
    if path is None:
        return None, None
    values = json.loads(path.read_text(encoding="utf-8"))
    return set(values.get("null_configuration_ids", [])), set(
        values.get("power_configuration_ids", [])
    )


def main() -> None:
    args = parse_args()
    settings = dict(PROFILE_SETTINGS[args.profile])
    if args.replicates is not None:
        settings["replicates"] = args.replicates
    if args.blocks is not None:
        settings["blocks"] = args.blocks
    replicates = int(settings["replicates"])
    blocks = int(settings["blocks"])
    if replicates % blocks != 0:
        raise ValueError("Replicates must be divisible by blocks.")
    if args.profile == "confirmatory" and args.selection_file is None:
        raise ValueError("Confirmatory runs require --selection-file.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    checks = correctness_checks()
    null_configs, infeasible_rows = build_null_configurations()
    power_configs = build_power_configurations()
    selected_null, selected_power = _selected_ids(args.selection_file)
    if selected_null is not None:
        null_configs = [c for c in null_configs if c.configuration_id in selected_null]
    if selected_power is not None:
        power_configs = [c for c in power_configs if c.configuration_id in selected_power]
    if args.configuration_limit is not None:
        null_configs = null_configs[: args.configuration_limit]
        power_configs = power_configs[: args.configuration_limit]
    if args.sections == "null":
        power_configs = []
    elif args.sections == "power":
        null_configs = []

    null_rows: list[dict] = []
    curve_rows: list[dict] = []
    mechanism_rows: list[dict] = []
    block_rows: list[dict] = []
    for index, config in enumerate(null_configs, start=1):
        values, diagnostics, blocks_for_config = simulate_configuration(
            config,
            replicates=replicates,
            blocks=blocks,
            base_seed=args.seed,
            stream="null_simulation",
        )
        summary, curves, mechanism = summarize_null(config, values, diagnostics)
        null_rows.extend(summary)
        curve_rows.extend(curves)
        mechanism_rows.append(mechanism)
        block_rows.extend(blocks_for_config)
        if index % 25 == 0 or index == len(null_configs):
            print(f"Null configurations: {index}/{len(null_configs)}", flush=True)

    threshold_rows: list[dict] = []
    thresholds_by_key: dict[str, dict[str, float]] = {}
    calibration_configs: dict[str, Configuration] = {}
    for config in power_configs:
        if config.calibration_key not in calibration_configs:
            calibration_configs[config.calibration_key] = power_calibration_configuration(config)
    for index, (key, config) in enumerate(calibration_configs.items(), start=1):
        values, _, blocks_for_config = simulate_configuration(
            config,
            replicates=replicates,
            blocks=blocks,
            base_seed=args.seed,
            stream="power_calibration",
        )
        rows = _size_adjustment_thresholds(values)
        thresholds_by_key[key] = {
            row["method"]: row["p_value_threshold_for_five_percent"] for row in rows
        }
        for row in rows:
            row.update(
                {
                    "calibration_key": key,
                    "configuration_id": config.configuration_id,
                    "power_family": config.power_family,
                    "n_p": config.n_p,
                    "n_q": config.n_q,
                    "replicates": replicates,
                }
            )
            threshold_rows.append(row)
        block_rows.extend(blocks_for_config)
        if index % 10 == 0 or index == len(calibration_configs):
            print(
                f"Power null calibrations: {index}/{len(calibration_configs)}",
                flush=True,
            )

    power_rows: list[dict] = []
    for index, config in enumerate(power_configs, start=1):
        values, _, blocks_for_config = simulate_configuration(
            config,
            replicates=replicates,
            blocks=blocks,
            base_seed=args.seed,
            stream="power",
        )
        power_rows.extend(
            summarize_power(
                config,
                values,
                thresholds_by_key[config.calibration_key],
            )
        )
        block_rows.extend(blocks_for_config)
        if index % 25 == 0 or index == len(power_configs):
            print(f"Power configurations: {index}/{len(power_configs)}", flush=True)

    all_configs = [*null_configs, *power_configs, *calibration_configs.values()]
    configurations = configuration_frame(all_configs)
    null_summary = pd.DataFrame(null_rows)
    rejection_curves = pd.DataFrame(curve_rows)
    mechanisms = pd.DataFrame(mechanism_rows)
    power_summary = pd.DataFrame(power_rows)
    thresholds = pd.DataFrame(threshold_rows)
    blocks_frame = pd.DataFrame(block_rows)
    infeasible = pd.DataFrame(infeasible_rows)

    checks.to_csv(args.output_dir / "correctness_checks.csv", index=False)
    configurations.to_csv(args.output_dir / "configurations.csv", index=False)
    infeasible.to_csv(args.output_dir / "infeasible_configurations.csv", index=False)
    null_summary.to_csv(args.output_dir / "null_summary.csv", index=False)
    rejection_curves.to_csv(
        args.output_dir / "rejection_curves.csv.gz", index=False, compression="gzip"
    )
    mechanisms.to_csv(args.output_dir / "mechanism_diagnostics.csv", index=False)
    power_summary.to_csv(args.output_dir / "power_summary.csv", index=False)
    thresholds.to_csv(args.output_dir / "power_null_thresholds.csv", index=False)
    blocks_frame.to_csv(args.output_dir / "replicate_blocks.csv", index=False)

    if not null_summary.empty or not power_summary.empty:
        write_case_sheets(
            args.output_dir, configurations, null_summary, power_summary
        )
    if not null_summary.empty:
        plot_results(args.output_dir, null_summary, rejection_curves, power_summary)
    write_report(
        args.output_dir,
        args.profile,
        configurations,
        null_summary,
        power_summary,
        infeasible,
    )

    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "replicates_per_configuration": replicates,
        "blocks": blocks,
        "sections": args.sections,
        "null_configurations": len(null_configs),
        "power_configurations": len(power_configs),
        "power_calibration_configurations": len(calibration_configs),
        "infeasible_requests": len(infeasible_rows),
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "welch_implementation_sha256": hashlib.sha256(
            (PROJECT_ROOT / "src" / "welch_differential_mi" / "welch.py").read_bytes()
        ).hexdigest(),
        "differential_statistics_sha256": hashlib.sha256(
            (
                REPOSITORY_ROOT
                / "DifferentialMI"
                / "src"
                / "differential_mi"
                / "statistics.py"
            ).read_bytes()
        ).hexdigest(),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
