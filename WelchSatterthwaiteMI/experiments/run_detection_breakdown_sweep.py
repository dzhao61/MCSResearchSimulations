#!/usr/bin/env python3
"""Run the frozen detection-and-breakdown experiment for differential MI."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.distributions import (  # noqa: E402
    association_table_from_interaction,
    interaction_pattern,
    mutual_information_probability,
    random_interaction_pattern,
    table_with_target_mi_from_interaction,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


METHODS = {
    "normal_wald": ("Normal Wald", "normal_p_value", "base_valid"),
    "simple_welch": ("Simple Welch", "welch_p_value", "simple_valid"),
    "expanded_welch": (
        "Expanded Welch",
        "expanded_welch_p_value",
        "expanded_valid",
    ),
}
METHOD_COLORS = {
    "normal_wald": "#1f4e79",
    "simple_welch": "#e67e22",
    "expanded_welch": "#b23a73",
}
PAIRWISE_METHODS = (
    ("expanded_welch", "normal_wald"),
    ("simple_welch", "normal_wald"),
    ("expanded_welch", "simple_welch"),
)
PROFILE_SMOKE = {
    "primary_shapes": ["2x2", "3x5"],
    "primary_skewness": ["balanced", "ultra"],
    "relationships": ["identical_distribution", "equal_mi_different_shape"],
    "calibration_sample_sizes": [2, 5, 20, 100],
    "power_sample_sizes": [5, 20, 100],
    "power_effects": [0.1, 0.6],
    "interaction_shapes": ["3x5"],
    "interaction_skewness": ["ultra"],
    "interaction_sample_sizes": [5, 20],
    "interaction_effects": [0, 0.6],
    "imbalance_shapes": ["2x2"],
    "imbalance_skewness": ["ultra"],
    "imbalance_sample_sizes": [5, 20],
    "imbalance_ratios": [2, 10],
    "imbalance_effects": [0, 0.4],
    "replicates": 200,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_revision() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def stable_seed(master_seed: int, configuration_id: str) -> int:
    """Return an order-independent seed for one exact configuration."""
    payload = f"{master_seed}:{configuration_id}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little")


def parse_shape(shape: str) -> tuple[int, int]:
    rows, columns = shape.lower().split("x", maxsplit=1)
    return int(rows), int(columns)


def entropy(probabilities: np.ndarray) -> float:
    values = np.asarray(probabilities, dtype=float)
    positive = values > 0
    return float(-np.sum(values[positive] * np.log(values[positive])))


def entropy_mi_upper_bound(row: np.ndarray, column: np.ndarray) -> float:
    return min(entropy(row), entropy(column))


def dominant_margin(size: int, skewness: str) -> np.ndarray:
    dominant = {"mild": 0.70, "strong": 0.90, "ultra": 0.95}
    if skewness == "balanced":
        return np.full(size, 1.0 / size)
    if skewness not in dominant:
        raise ValueError(f"Unknown skewness level: {skewness}")
    result = np.full(size, (1.0 - dominant[skewness]) / (size - 1))
    result[0] = dominant[skewness]
    return result


def reachable_path_maximum(
    row: np.ndarray,
    column: np.ndarray,
    interaction: np.ndarray,
    probes: list[float],
    tolerance: float,
) -> tuple[float, float, list[dict[str, float]]]:
    """Measure the monotone, numerically reachable MI range of one path."""
    records: list[dict[str, float]] = []
    previous = -math.inf
    for association in probes:
        try:
            table = association_table_from_interaction(
                row, column, float(association), interaction
            )
        except (ValueError, RuntimeError):
            break
        achieved = mutual_information_probability(table)
        if achieved + tolerance < previous:
            raise ValueError("Reachable MI path is not nondecreasing.")
        records.append({"association": float(association), "mi": achieved})
        previous = achieved
    if not records:
        raise RuntimeError("No association-strength probe was constructible.")
    return records[-1]["mi"], records[-1]["association"], records


def _random_interaction(rows: int, columns: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(stable_seed(seed, f"{rows}x{columns}"))
    return random_interaction_pattern(rows, columns, rng)


def _interaction_pair(
    rows: int,
    columns: int,
    name: str,
    protocol: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, str, str]:
    if name == "primary":
        ordinal = interaction_pattern(rows, columns, "ordinal")
        return ordinal, -ordinal, "ordinal", "negative_ordinal"
    if name == "checkerboard_and_cyclic":
        return (
            interaction_pattern(rows, columns, "checkerboard"),
            interaction_pattern(rows, columns, "cyclic"),
            "checkerboard",
            "cyclic",
        )
    if name == "fixed_random_A_and_fixed_random_B":
        seed_a, seed_b = protocol["robustness_interactions"]["fixed_random_seeds"]
        return (
            _random_interaction(rows, columns, int(seed_a)),
            _random_interaction(rows, columns, int(seed_b)),
            f"fixed_random_{seed_a}",
            f"fixed_random_{seed_b}",
        )
    raise ValueError(f"Unknown interaction pair: {name}")


def _profile_factors(protocol: dict[str, Any], profile: str) -> dict[str, Any]:
    if profile == "smoke":
        return dict(PROFILE_SMOKE)
    return {
        "primary_shapes": protocol["population_construction"]["shapes"],
        "primary_skewness": list(protocol["population_construction"]["skewness"]),
        "relationships": protocol["population_construction"]["relationships"],
        "calibration_sample_sizes": protocol["experiment_2_calibration"]["sample_sizes"],
        "power_sample_sizes": protocol["experiment_3_power"]["sample_sizes"],
        "power_effects": protocol["experiment_3_power"]["relative_effects"],
        "interaction_shapes": protocol["robustness_interactions"]["shapes"],
        "interaction_skewness": protocol["robustness_interactions"]["skewness"],
        "interaction_sample_sizes": protocol["robustness_interactions"]["sample_sizes"],
        "interaction_effects": protocol["robustness_interactions"]["relative_effects"],
        "imbalance_shapes": protocol["robustness_sample_imbalance"]["shapes"],
        "imbalance_skewness": protocol["robustness_sample_imbalance"]["skewness"],
        "imbalance_sample_sizes": protocol["robustness_sample_imbalance"]["smaller_sample_sizes"],
        "imbalance_ratios": protocol["robustness_sample_imbalance"]["n_q_to_n_p_ratios"],
        "imbalance_effects": protocol["robustness_sample_imbalance"]["relative_effects"],
        "replicates": protocol["experiment_2_calibration"]["replicates_per_cell"],
    }


def _configuration_row(
    *,
    experiment: str,
    shape: str,
    skewness: str,
    relationship: str,
    interaction_pair: str,
    n_p: int,
    n_q: int,
    relative_effect: float,
    replicates: int,
    master_seed: int,
) -> dict[str, Any]:
    effect_text = format(float(relative_effect), ".6g").replace(".", "p")
    config_id = (
        f"{experiment}__{shape}__{skewness}__{relationship}__"
        f"{interaction_pair}__np{n_p}__nq{n_q}__e{effect_text}"
    )
    rows, columns = parse_shape(shape)
    return {
        "configuration_id": config_id,
        "experiment": experiment,
        "shape": shape,
        "rows": rows,
        "columns": columns,
        "skewness": skewness,
        "relationship": relationship,
        "interaction_pair": interaction_pair,
        "n_p": int(n_p),
        "n_q": int(n_q),
        "sample_size_ratio_q_to_p": n_q / n_p,
        "relative_effect": float(relative_effect),
        "replicates": int(replicates),
        "structural_breakdown": bool(min(n_p, n_q) < max(rows, columns)),
        "simulation_seed": stable_seed(master_seed, config_id),
    }


def generate_configuration_manifest(
    protocol: dict[str, Any], profile: str
) -> pd.DataFrame:
    """Expand the protocol into one row per exact simulation cell."""
    factors = _profile_factors(protocol, profile)
    seed = int(protocol["master_seed"])
    reps = int(factors["replicates"])
    rows: list[dict[str, Any]] = []

    for shape in factors["primary_shapes"]:
        for skewness in factors["primary_skewness"]:
            for relationship in factors["relationships"]:
                for n in factors["calibration_sample_sizes"]:
                    rows.append(
                        _configuration_row(
                            experiment="calibration",
                            shape=shape,
                            skewness=skewness,
                            relationship=relationship,
                            interaction_pair="primary",
                            n_p=n,
                            n_q=n,
                            relative_effect=0,
                            replicates=reps,
                            master_seed=seed,
                        )
                    )
                for n in factors["power_sample_sizes"]:
                    for effect in factors["power_effects"]:
                        rows.append(
                            _configuration_row(
                                experiment="power",
                                shape=shape,
                                skewness=skewness,
                                relationship=relationship,
                                interaction_pair="primary",
                                n_p=n,
                                n_q=n,
                                relative_effect=effect,
                                replicates=reps,
                                master_seed=seed,
                            )
                        )

    for shape in factors["interaction_shapes"]:
        for skewness in factors["interaction_skewness"]:
            for pair in protocol["robustness_interactions"]["interaction_pairs"]:
                for n in factors["interaction_sample_sizes"]:
                    for effect in factors["interaction_effects"]:
                        rows.append(
                            _configuration_row(
                                experiment="robustness_interaction",
                                shape=shape,
                                skewness=skewness,
                                relationship="equal_mi_different_shape",
                                interaction_pair=pair,
                                n_p=n,
                                n_q=n,
                                relative_effect=effect,
                                replicates=reps,
                                master_seed=seed,
                            )
                        )

    for shape in factors["imbalance_shapes"]:
        for skewness in factors["imbalance_skewness"]:
            for n_p in factors["imbalance_sample_sizes"]:
                for ratio in factors["imbalance_ratios"]:
                    for effect in factors["imbalance_effects"]:
                        rows.append(
                            _configuration_row(
                                experiment="robustness_imbalance",
                                shape=shape,
                                skewness=skewness,
                                relationship="equal_mi_different_shape",
                                interaction_pair="primary",
                                n_p=n_p,
                                n_q=int(n_p * ratio),
                                relative_effect=effect,
                                replicates=reps,
                                master_seed=seed,
                            )
                        )

    manifest = pd.DataFrame(rows).sort_values("configuration_id").reset_index(drop=True)
    if manifest["configuration_id"].duplicated().any():
        raise RuntimeError("The protocol generated duplicate configuration identifiers.")
    if profile == "full":
        expected = int(protocol["totals"]["all_cell_count"])
        if len(manifest) != expected:
            raise RuntimeError(f"Expected {expected} full cells, generated {len(manifest)}.")
    return manifest


def _population_key(row: pd.Series) -> tuple[str, str, str, str, float]:
    return (
        str(row["shape"]),
        str(row["skewness"]),
        str(row["relationship"]),
        str(row["interaction_pair"]),
        float(row["relative_effect"]),
    )


def _build_population_blueprint(
    shape: str,
    skewness: str,
    pair_name: str,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    """Compute the effect-invariant margins, paths, range, and baseline P."""
    rows, columns = parse_shape(shape)
    row_p = dominant_margin(rows, skewness)
    column_p = dominant_margin(columns, skewness)
    row_q = np.roll(row_p, 1)
    column_q = np.roll(column_p, -1)
    interaction_p, interaction_q, label_p, label_q = _interaction_pair(
        rows, columns, pair_name, protocol
    )
    construction = protocol["population_construction"]
    probes = [float(value) for value in construction["association_strength_probe"]]
    tolerance = float(construction["target_mi_tolerance"])
    max_p, max_assoc_p, trace_p = reachable_path_maximum(
        row_p, column_p, interaction_p, probes, tolerance
    )
    max_q, max_assoc_q, trace_q = reachable_path_maximum(
        row_q, column_q, interaction_q, probes, tolerance
    )
    shared = min(max_p, max_q)
    if shared <= float(construction["minimum_usable_M"]):
        raise ValueError(f"Shared reachable MI scale is too small: M={shared:.12g}.")
    target_p = 0.20 * shared
    probability_p, association_p = table_with_target_mi_from_interaction(
        row_p,
        column_p,
        target_p,
        interaction_p,
        mi_tolerance=tolerance / 10,
        max_association=max(probes),
    )
    return {
        "rows": rows,
        "columns": columns,
        "row_p": row_p,
        "column_p": column_p,
        "row_q": row_q,
        "column_q": column_q,
        "interaction_p": interaction_p,
        "interaction_q": interaction_q,
        "label_p": label_p,
        "label_q": label_q,
        "probes": probes,
        "tolerance": tolerance,
        "max_p": max_p,
        "max_q": max_q,
        "max_assoc_p": max_assoc_p,
        "max_assoc_q": max_assoc_q,
        "trace_p": trace_p,
        "trace_q": trace_q,
        "shared": shared,
        "target_p": target_p,
        "probability_p": probability_p,
        "association_p": association_p,
    }


def construct_population(
    key: tuple[str, str, str, str, float],
    protocol: dict[str, Any],
    blueprint: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    """Construct and validate one fixed population pair."""
    shape, skewness, relationship, pair_name, effect = key
    if blueprint is None:
        blueprint = _build_population_blueprint(
            shape, skewness, pair_name, protocol
        )
    rows = blueprint["rows"]
    columns = blueprint["columns"]
    row_p = blueprint["row_p"]
    column_p = blueprint["column_p"]
    row_q = blueprint["row_q"]
    column_q = blueprint["column_q"]
    interaction_p = blueprint["interaction_p"]
    interaction_q = blueprint["interaction_q"]
    label_p = blueprint["label_p"]
    label_q = blueprint["label_q"]
    construction = protocol["population_construction"]
    probes = blueprint["probes"]
    tolerance = blueprint["tolerance"]
    max_p = blueprint["max_p"]
    max_q = blueprint["max_q"]
    max_assoc_p = blueprint["max_assoc_p"]
    max_assoc_q = blueprint["max_assoc_q"]
    trace_p = blueprint["trace_p"]
    trace_q = blueprint["trace_q"]
    shared = blueprint["shared"]
    target_p = blueprint["target_p"]
    target_q = (0.20 + effect) * shared
    maximum_target = float(construction["maximum_target_fraction_of_M"]) * shared
    if target_q > maximum_target + tolerance:
        raise ValueError("Requested target exceeds the frozen 0.8M limit.")

    probability_p = blueprint["probability_p"]
    association_p = blueprint["association_p"]
    if relationship == "identical_distribution":
        if effect == 0:
            probability_q = probability_p.copy()
            association_q = association_p
        else:
            probability_q, association_q = table_with_target_mi_from_interaction(
                row_p,
                column_p,
                target_q,
                interaction_p,
                mi_tolerance=tolerance / 10,
                max_association=max(probes),
            )
        effective_row_q = row_p
        effective_column_q = column_p
        effective_label_q = label_p
        effective_interaction_q = interaction_p
    elif relationship == "equal_mi_different_shape":
        probability_q, association_q = table_with_target_mi_from_interaction(
            row_q,
            column_q,
            target_q,
            interaction_q,
            mi_tolerance=tolerance / 10,
            max_association=max(probes),
        )
        effective_row_q = row_q
        effective_column_q = column_q
        effective_label_q = label_q
        effective_interaction_q = interaction_q
    else:
        raise ValueError(f"Unknown population relationship: {relationship}")

    achieved_p = mutual_information_probability(probability_p)
    achieved_q = mutual_information_probability(probability_q)
    if abs(achieved_p - target_p) > tolerance or abs(achieved_q - target_q) > tolerance:
        raise RuntimeError("Constructed population did not attain its target MI.")
    l1_distance = float(np.abs(probability_p - probability_q).sum())
    if effect == 0 and relationship == "equal_mi_different_shape":
        if abs(achieved_p - achieved_q) > tolerance:
            raise RuntimeError("Weak-null population pair does not have equal MI.")
        if l1_distance <= 1e-8:
            raise RuntimeError("Weak-null population pair is numerically identical.")

    population_id = (
        f"{shape}__{skewness}__{relationship}__{pair_name}__"
        f"e{format(effect, '.6g').replace('.', 'p')}"
    )
    metadata = {
        "population_id": population_id,
        "shape": shape,
        "rows": rows,
        "columns": columns,
        "skewness": skewness,
        "relationship": relationship,
        "interaction_pair": pair_name,
        "interaction_p": label_p,
        "interaction_q": effective_label_q,
        "relative_effect": effect,
        "entropy_upper_bound_p": entropy_mi_upper_bound(row_p, column_p),
        "entropy_upper_bound_q": entropy_mi_upper_bound(
            effective_row_q, effective_column_q
        ),
        "reachable_mi_p": max_p,
        "reachable_mi_q": max_q,
        "shared_reachable_mi": shared,
        "maximum_probe_association_p": max_assoc_p,
        "maximum_probe_association_q": max_assoc_q,
        "target_mi_p": target_p,
        "target_mi_q": target_q,
        "achieved_mi_p": achieved_p,
        "achieved_mi_q": achieved_q,
        "absolute_mi_difference": abs(achieved_q - achieved_p),
        "l1_distance": l1_distance,
        "association_p": association_p,
        "association_q": association_q,
        "row_margin_p_json": json.dumps(row_p.tolist()),
        "column_margin_p_json": json.dumps(column_p.tolist()),
        "row_margin_q_json": json.dumps(effective_row_q.tolist()),
        "column_margin_q_json": json.dumps(effective_column_q.tolist()),
        "interaction_matrix_p_json": json.dumps(interaction_p.tolist()),
        "interaction_matrix_q_json": json.dumps(effective_interaction_q.tolist()),
        "probe_trace_p_json": json.dumps(trace_p),
        "probe_trace_q_json": json.dumps(trace_q),
        "probability_p_json": json.dumps(probability_p.tolist()),
        "probability_q_json": json.dumps(probability_q.tolist()),
    }
    return metadata, probability_p, probability_q


def construct_all_populations(
    manifest: pd.DataFrame,
    protocol: dict[str, Any],
) -> tuple[dict[tuple[str, str, str, str, float], tuple[np.ndarray, np.ndarray]], pd.DataFrame, pd.DataFrame]:
    populations: dict[
        tuple[str, str, str, str, float], tuple[np.ndarray, np.ndarray]
    ] = {}
    definitions: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    blueprints: dict[tuple[str, str, str], dict[str, Any]] = {}
    for key in sorted({_population_key(row) for _, row in manifest.iterrows()}):
        try:
            blueprint_key = (key[0], key[1], key[3])
            if blueprint_key not in blueprints:
                blueprints[blueprint_key] = _build_population_blueprint(
                    key[0], key[1], key[3], protocol
                )
            metadata, probability_p, probability_q = construct_population(
                key, protocol, blueprints[blueprint_key]
            )
        except (ValueError, RuntimeError) as error:
            failures.append(
                {
                    "shape": key[0],
                    "skewness": key[1],
                    "relationship": key[2],
                    "interaction_pair": key[3],
                    "relative_effect": key[4],
                    "error_type": type(error).__name__,
                    "reason": str(error),
                }
            )
            continue
        populations[key] = (probability_p, probability_q)
        definitions.append(metadata)
    failure_columns = [
        "shape",
        "skewness",
        "relationship",
        "interaction_pair",
        "relative_effect",
        "error_type",
        "reason",
    ]
    return (
        populations,
        pd.DataFrame(definitions),
        pd.DataFrame(failures, columns=failure_columns),
    )


def wilson_interval(successes: int, total: int) -> tuple[float, float]:
    if total <= 0:
        return math.nan, math.nan
    z = float(norm.ppf(0.975))
    estimate = successes / total
    denominator = 1.0 + z * z / total
    center = (estimate + z * z / (2.0 * total)) / denominator
    half = (
        z
        * math.sqrt(estimate * (1.0 - estimate) / total + z * z / (4 * total * total))
        / denominator
    )
    return center - half, center + half


def _sample_diagnostics(tables: np.ndarray) -> dict[str, np.ndarray]:
    counts = np.asarray(tables)
    row_counts = counts.sum(axis=2)
    column_counts = counts.sum(axis=1)
    return {
        "zero_fraction": np.mean(counts == 0, axis=(1, 2)),
        "empty_row": np.any(row_counts == 0, axis=1),
        "empty_column": np.any(column_counts == 0, axis=1),
    }


def paired_difference_interval(
    only_a: int, only_b: int, total: int
) -> tuple[float, float, float, float]:
    if total <= 1:
        return math.nan, math.nan, math.nan, math.nan
    difference = (only_a - only_b) / total
    second_moment = (only_a + only_b) / total
    variance = max(0.0, total / (total - 1.0) * (second_moment - difference**2))
    standard_error = math.sqrt(variance / total)
    return (
        difference,
        standard_error,
        difference - 1.96 * standard_error,
        difference + 1.96 * standard_error,
    )


def sustained_frontier(
    sample_sizes: list[int], qualifies: list[bool], required: int = 3
) -> int | None:
    for index in range(len(sample_sizes) - required + 1):
        if all(qualifies[index : index + required]):
            return int(sample_sizes[index])
    return None


def _method_invalid_reasons(
    method: str, values: dict[str, np.ndarray]
) -> dict[str, int]:
    base = np.asarray(values["base_valid"], dtype=bool)
    if method == "normal_wald":
        return {"invalid_base": int(np.sum(~base))}
    if method == "simple_welch":
        df = np.asarray(values["welch_degrees_of_freedom"])
        return {
            "invalid_base": int(np.sum(~base)),
            "invalid_df": int(np.sum(base & (~np.isfinite(df) | (df <= 0)))),
        }
    df_p = np.asarray(values["expanded_component_degrees_of_freedom_p"])
    df_q = np.asarray(values["expanded_component_degrees_of_freedom_q"])
    df = np.asarray(values["expanded_welch_degrees_of_freedom"])
    return {
        "invalid_base": int(np.sum(~base)),
        "invalid_component_p": int(np.sum(base & (~np.isfinite(df_p) | (df_p <= 0)))),
        "invalid_component_q": int(np.sum(base & (~np.isfinite(df_q) | (df_q <= 0)))),
        "invalid_combined_df": int(np.sum(base & (~np.isfinite(df) | (df <= 0)))),
    }


def _simulate_configuration(task: dict[str, Any]) -> dict[str, Any]:
    row = task["configuration"]
    probability_p = task["probability_p"]
    probability_q = task["probability_q"]
    alphas = task["alphas"]
    batch_size = task["batch_size"]
    replicates = int(row["replicates"])
    rng = np.random.default_rng(int(row["simulation_seed"]))

    method_valid_counts = {method: 0 for method in METHODS}
    reject_counts = {method: np.zeros(len(alphas), dtype=np.int64) for method in METHODS}
    common_reject_counts = {
        method: np.zeros(len(alphas), dtype=np.int64) for method in METHODS
    }
    paired = {
        pair: {
            "both": np.zeros(len(alphas), dtype=np.int64),
            "neither": np.zeros(len(alphas), dtype=np.int64),
            "only_a": np.zeros(len(alphas), dtype=np.int64),
            "only_b": np.zeros(len(alphas), dtype=np.int64),
        }
        for pair in PAIRWISE_METHODS
    }
    invalid_reasons = {method: {} for method in METHODS}
    common_valid_count = 0
    diagnostic_sums = {
        "observed_zero_fraction_p": 0.0,
        "observed_zero_fraction_q": 0.0,
        "empty_row_p": 0.0,
        "empty_row_q": 0.0,
        "empty_column_p": 0.0,
        "empty_column_q": 0.0,
    }
    df_values: dict[str, list[np.ndarray]] = {
        "expanded_component_degrees_of_freedom_p": [],
        "expanded_component_degrees_of_freedom_q": [],
        "expanded_welch_degrees_of_freedom": [],
    }

    completed = 0
    while completed < replicates:
        current = min(batch_size, replicates - completed)
        tables_p = rng.multinomial(
            int(row["n_p"]), probability_p.ravel(), size=current
        ).reshape(current, *probability_p.shape)
        tables_q = rng.multinomial(
            int(row["n_q"]), probability_q.ravel(), size=current
        ).reshape(current, *probability_q.shape)
        values = differential_mi_pvalues(
            tables_p,
            tables_q,
            include_simple=True,
            include_expanded=True,
            include_unbiased_sensitivity=False,
        )
        sample_p = _sample_diagnostics(tables_p)
        sample_q = _sample_diagnostics(tables_q)
        diagnostic_sums["observed_zero_fraction_p"] += float(sample_p["zero_fraction"].sum())
        diagnostic_sums["observed_zero_fraction_q"] += float(sample_q["zero_fraction"].sum())
        diagnostic_sums["empty_row_p"] += int(sample_p["empty_row"].sum())
        diagnostic_sums["empty_row_q"] += int(sample_q["empty_row"].sum())
        diagnostic_sums["empty_column_p"] += int(sample_p["empty_column"].sum())
        diagnostic_sums["empty_column_q"] += int(sample_q["empty_column"].sum())

        valid_masks: dict[str, np.ndarray] = {}
        p_values: dict[str, np.ndarray] = {}
        for method, (_, p_key, valid_key) in METHODS.items():
            valid = np.asarray(values[valid_key], dtype=bool)
            p_value = np.asarray(values[p_key], dtype=float)
            if np.any(valid & (~np.isfinite(p_value) | (p_value < 0) | (p_value > 1))):
                raise RuntimeError("A p-value marked valid lies outside [0, 1].")
            valid_masks[method] = valid
            p_values[method] = p_value
            method_valid_counts[method] += int(valid.sum())
            for index, alpha in enumerate(alphas):
                reject_counts[method][index] += int(np.sum(valid & (p_value <= alpha)))
            reasons = _method_invalid_reasons(method, values)
            for reason, count in reasons.items():
                invalid_reasons[method][reason] = invalid_reasons[method].get(reason, 0) + count

        common_valid = np.logical_and.reduce(list(valid_masks.values()))
        common_valid_count += int(common_valid.sum())
        for method in METHODS:
            for index, alpha in enumerate(alphas):
                common_reject_counts[method][index] += int(
                    np.sum(common_valid & (p_values[method] <= alpha))
                )

        for method_a, method_b in PAIRWISE_METHODS:
            for index, alpha in enumerate(alphas):
                reject_a = valid_masks[method_a] & (p_values[method_a] <= alpha)
                reject_b = valid_masks[method_b] & (p_values[method_b] <= alpha)
                paired[(method_a, method_b)]["both"][index] += int(np.sum(reject_a & reject_b))
                paired[(method_a, method_b)]["neither"][index] += int(np.sum(~reject_a & ~reject_b))
                paired[(method_a, method_b)]["only_a"][index] += int(np.sum(reject_a & ~reject_b))
                paired[(method_a, method_b)]["only_b"][index] += int(np.sum(~reject_a & reject_b))

        expanded_valid = valid_masks["expanded_welch"]
        for key in df_values:
            finite = np.asarray(values[key], dtype=float)[expanded_valid]
            df_values[key].append(finite[np.isfinite(finite)])
        completed += current

    true_expected_p = int(row["n_p"]) * probability_p
    true_expected_q = int(row["n_q"]) * probability_q
    shared = {
        **row,
        "minimum_true_expected_p": float(true_expected_p.min()),
        "minimum_true_expected_q": float(true_expected_q.min()),
        "true_expected_below_1_p": float(np.mean(true_expected_p < 1)),
        "true_expected_below_1_q": float(np.mean(true_expected_q < 1)),
        "true_expected_below_5_p": float(np.mean(true_expected_p < 5)),
        "true_expected_below_5_q": float(np.mean(true_expected_q < 5)),
        **{key: value / replicates for key, value in diagnostic_sums.items()},
    }
    cell_rows: list[dict[str, Any]] = []
    for method, (method_label, _, _) in METHODS.items():
        valid_total = method_valid_counts[method]
        reason_json = json.dumps(invalid_reasons[method], sort_keys=True)
        for index, alpha in enumerate(alphas):
            rejects = int(reject_counts[method][index])
            common_rejects = int(common_reject_counts[method][index])
            unconditional = rejects / replicates
            conditional = rejects / valid_total if valid_total else math.nan
            common_rate = common_rejects / common_valid_count if common_valid_count else math.nan
            low, high = wilson_interval(rejects, replicates)
            cell = {
                **shared,
                "method": method,
                "method_label": method_label,
                "nominal_alpha": alpha,
                "valid_replicates": valid_total,
                "valid_rate": valid_total / replicates,
                "common_valid_replicates": common_valid_count,
                "common_valid_rate": common_valid_count / replicates,
                "rejections": rejects,
                "common_valid_rejections": common_rejects,
                "unconditional_rejection_rate": unconditional,
                "conditional_rejection_rate": conditional,
                "common_valid_rejection_rate": common_rate,
                "wilson_95_low": low,
                "wilson_95_high": high,
                "monte_carlo_standard_error": math.sqrt(
                    unconditional * (1.0 - unconditional) / replicates
                ),
                "absolute_calibration_error": (
                    abs(unconditional - alpha) if float(row["relative_effect"]) == 0 else math.nan
                ),
                "invalid_reason_counts_json": reason_json,
            }
            if method == "expanded_welch":
                for df_key, arrays in df_values.items():
                    combined = np.concatenate(arrays) if arrays else np.array([])
                    prefix = df_key.replace("expanded_", "")
                    cell[f"{prefix}_median"] = float(np.median(combined)) if combined.size else math.nan
                    cell[f"{prefix}_p05"] = float(np.quantile(combined, 0.05)) if combined.size else math.nan
                    cell[f"{prefix}_p95"] = float(np.quantile(combined, 0.95)) if combined.size else math.nan
                    cell[f"{prefix}_fraction_below_1"] = float(np.mean(combined < 1)) if combined.size else math.nan
                    cell[f"{prefix}_fraction_above_1e4"] = float(np.mean(combined > 1e4)) if combined.size else math.nan
            cell_rows.append(cell)

    paired_rows: list[dict[str, Any]] = []
    for (method_a, method_b), counts in paired.items():
        for index, alpha in enumerate(alphas):
            only_a = int(counts["only_a"][index])
            only_b = int(counts["only_b"][index])
            difference, standard_error, low, high = paired_difference_interval(
                only_a, only_b, replicates
            )
            paired_rows.append(
                {
                    **row,
                    "nominal_alpha": alpha,
                    "method_a": method_a,
                    "method_b": method_b,
                    "both_reject": int(counts["both"][index]),
                    "neither_rejects": int(counts["neither"][index]),
                    "only_method_a_rejects": only_a,
                    "only_method_b_rejects": only_b,
                    "rejection_rate_difference_a_minus_b": difference,
                    "paired_standard_error": standard_error,
                    "paired_95_low": low,
                    "paired_95_high": high,
                }
            )
    return {"cell_rows": cell_rows, "paired_rows": paired_rows}


def _frontier_table(results: pd.DataFrame, protocol: dict[str, Any]) -> pd.DataFrame:
    settings = protocol["operating_frontiers"]
    alpha = float(settings["alpha"])
    required = int(settings["sustained_points_required"])
    validity_floor = float(settings["validity_threshold"])
    calibration_low, calibration_high = map(float, settings["bradley_interval"])
    detection_effect = float(settings["detection_effect"])
    power_floor = float(settings["detection_power_threshold"])
    primary = results[
        results["experiment"].isin(["calibration", "power"])
        & np.isclose(results["nominal_alpha"], alpha)
    ]
    grouping = ["shape", "skewness", "relationship", "interaction_pair", "method"]
    rows: list[dict[str, Any]] = []
    for keys, frame in primary.groupby(grouping, sort=False):
        null = frame[frame["experiment"].eq("calibration")].sort_values("n_p")
        sizes = null["n_p"].astype(int).tolist()
        valid = (null["valid_rate"] >= validity_floor).tolist()
        calibrated = null["unconditional_rejection_rate"].between(
            calibration_low, calibration_high
        ).tolist()
        operational = [a and b for a, b in zip(valid, calibrated)]
        power = frame[
            frame["experiment"].eq("power")
            & np.isclose(frame["relative_effect"], detection_effect)
        ].sort_values("n_p")
        power_sizes = power["n_p"].astype(int).tolist()
        null_by_n = null.set_index("n_p")
        detection_qualifies = []
        for _, power_row in power.iterrows():
            n = int(power_row["n_p"])
            null_row = null_by_n.loc[n] if n in null_by_n.index else None
            detection_qualifies.append(
                bool(
                    null_row is not None
                    and null_row["valid_rate"] >= validity_floor
                    and calibration_low
                    <= null_row["unconditional_rejection_rate"]
                    <= calibration_high
                    and power_row["unconditional_rejection_rate"] >= power_floor
                )
            )
        values = dict(zip(grouping, keys))
        rows.append(
            {
                **values,
                "validity_frontier_n": sustained_frontier(sizes, valid, required),
                "calibration_frontier_n": sustained_frontier(sizes, calibrated, required),
                "operational_frontier_n": sustained_frontier(sizes, operational, required),
                "detection_frontier_n": sustained_frontier(
                    power_sizes, detection_qualifies, required
                ),
            }
        )
    return pd.DataFrame(rows)


def _flag_power_reversals(results: pd.DataFrame) -> pd.DataFrame:
    power = results[
        results["experiment"].isin(["power", "robustness_interaction", "robustness_imbalance"])
        & np.isclose(results["nominal_alpha"], 0.05)
        & (results["relative_effect"] > 0)
    ]
    grouping = [
        "experiment",
        "shape",
        "skewness",
        "relationship",
        "interaction_pair",
        "n_p",
        "n_q",
        "method",
    ]
    flags: list[dict[str, Any]] = []
    for keys, frame in power.groupby(grouping, sort=False):
        ordered = frame.sort_values("relative_effect")
        previous = None
        for _, row in ordered.iterrows():
            if previous is not None:
                decline = previous["unconditional_rejection_rate"] - row["unconditional_rejection_rate"]
                threshold = 3.0 * math.sqrt(
                    previous["monte_carlo_standard_error"] ** 2
                    + row["monte_carlo_standard_error"] ** 2
                )
                if decline > threshold:
                    flags.append(
                        {
                            **dict(zip(grouping, keys)),
                            "effect_from": previous["relative_effect"],
                            "effect_to": row["relative_effect"],
                            "power_from": previous["unconditional_rejection_rate"],
                            "power_to": row["unconditional_rejection_rate"],
                            "decline": decline,
                            "three_mcse_threshold": threshold,
                        }
                    )
            previous = row
    columns = grouping + [
        "effect_from",
        "effect_to",
        "power_from",
        "power_to",
        "decline",
        "three_mcse_threshold",
    ]
    return pd.DataFrame(flags, columns=columns)


def _save_line_figure(
    frame: pd.DataFrame,
    path: Path,
    title: str,
    y_column: str,
    x_column: str,
    x_label: str,
    y_label: str,
    facet_column: str,
    facet_order: list[Any],
    horizontal: float | None = None,
    log_x: bool = False,
) -> None:
    facets = [value for value in facet_order if value in set(frame[facet_column])]
    if not facets:
        return
    columns = min(5, len(facets))
    rows = math.ceil(len(facets) / columns)
    figure, axes = plt.subplots(
        rows, columns, figsize=(3.2 * columns, 2.8 * rows), sharey=True, squeeze=False
    )
    for axis, facet in zip(axes.flat, facets):
        subset = frame[frame[facet_column].eq(facet)]
        for method, (label, _, _) in METHODS.items():
            line = subset[subset["method"].eq(method)].sort_values(x_column)
            if line.empty:
                continue
            axis.plot(
                line[x_column],
                line[y_column],
                marker="o",
                markersize=3,
                linewidth=1.4,
                color=METHOD_COLORS[method],
                label=label,
            )
        if horizontal is not None:
            axis.axhline(horizontal, color="#777777", linestyle=":", linewidth=1)
        if log_x:
            axis.set_xscale("log")
        axis.set_title(str(facet), fontsize=9)
        axis.grid(alpha=0.2)
        axis.set_xlabel(x_label)
    for axis in axes[:, 0]:
        axis.set_ylabel(y_label)
    for axis in axes.flat[len(facets) :]:
        axis.set_visible(False)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.suptitle(title, y=0.99, fontsize=13)
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.95),
        ncol=3,
        frameon=False,
    )
    figure.tight_layout(rect=(0, 0, 1, 0.86))
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def generate_figures(
    results: pd.DataFrame,
    paired: pd.DataFrame,
    frontiers: pd.DataFrame,
    protocol: dict[str, Any],
    output_directory: Path,
) -> list[str]:
    figures = output_directory / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    alpha = results[np.isclose(results["nominal_alpha"], 0.05)].copy()
    core_shapes = protocol["main_figure_subset"]["shapes"]
    core_skew = protocol["main_figure_subset"]["skewness"]

    controls = alpha[
        alpha["experiment"].eq("calibration")
        & alpha["skewness"].eq("balanced")
        & alpha["shape"].isin(core_shapes)
    ].copy()
    controls["panel"] = controls["relationship"] + ": " + controls["shape"]
    control_path = figures / "control_calibration.png"
    _save_line_figure(
        controls,
        control_path,
        "Balanced strong- and weak-null controls",
        "unconditional_rejection_rate",
        "n_p",
        "Sample size per population",
        "False-positive rate",
        "panel",
        [f"{relationship}: {shape}" for relationship in ["identical_distribution", "equal_mi_different_shape"] for shape in core_shapes],
        horizontal=0.05,
        log_x=True,
    )
    if control_path.exists():
        saved.append(str(control_path.relative_to(output_directory)))

    for relationship in ["identical_distribution", "equal_mi_different_shape"]:
        for skewness in core_skew:
            breakdown = alpha[
                alpha["experiment"].eq("calibration")
                & alpha["relationship"].eq(relationship)
                & alpha["skewness"].eq(skewness)
                & alpha["shape"].isin(core_shapes)
            ]
            path = figures / f"breakdown_{relationship}_{skewness}.png"
            _save_line_figure(
                breakdown,
                path,
                f"Calibration: {relationship}, {skewness}",
                "unconditional_rejection_rate",
                "n_p",
                "Sample size per population",
                "False-positive rate",
                "shape",
                core_shapes,
                horizontal=0.05,
                log_x=True,
            )
            if path.exists():
                saved.append(str(path.relative_to(output_directory)))

    for relationship in ["identical_distribution", "equal_mi_different_shape"]:
        for skewness in core_skew:
            for shape in core_shapes:
                positive = alpha[
                    alpha["experiment"].eq("power")
                    & alpha["relationship"].eq(relationship)
                    & alpha["skewness"].eq(skewness)
                    & alpha["shape"].eq(shape)
                ]
                power_sample_sizes = set(positive["n_p"])
                power = alpha[
                    alpha["experiment"].isin(["calibration", "power"])
                    & alpha["relationship"].eq(relationship)
                    & alpha["skewness"].eq(skewness)
                    & alpha["shape"].eq(shape)
                    & alpha["n_p"].isin(power_sample_sizes)
                ].copy()
                if power.empty:
                    continue
                power["sample_panel"] = power["n_p"].astype(int)
                sample_order = sorted(set(power["sample_panel"]))
                path = figures / f"power_{relationship}_{skewness}_{shape}.png"
                _save_line_figure(
                    power,
                    path,
                    f"Power: {relationship}, {skewness}, {shape}",
                    "unconditional_rejection_rate",
                    "absolute_mi_difference",
                    "Absolute MI difference (nats)",
                    "Rejection rate",
                    "sample_panel",
                    sample_order,
                    horizontal=0.05,
                )
                if path.exists():
                    saved.append(str(path.relative_to(output_directory)))

    calibration = alpha[alpha["experiment"].eq("calibration")]
    for relationship in ["identical_distribution", "equal_mi_different_shape"]:
        for skewness in core_skew:
            for method in METHODS:
                frame = calibration[
                    calibration["relationship"].eq(relationship)
                    & calibration["skewness"].eq(skewness)
                    & calibration["method"].eq(method)
                    & calibration["shape"].isin(core_shapes)
                ]
                if frame.empty:
                    continue
                pivot = frame.pivot(index="shape", columns="n_p", values="valid_rate").reindex(core_shapes)
                figure, axis = plt.subplots(figsize=(9, 3.4))
                image = axis.imshow(pivot.to_numpy(), aspect="auto", vmin=0, vmax=1, cmap="cividis")
                axis.set_yticks(range(len(pivot.index)), labels=pivot.index)
                axis.set_xticks(range(len(pivot.columns)), labels=pivot.columns, rotation=45, ha="right")
                axis.set_xlabel("Sample size per population")
                axis.set_title(f"Validity: {METHODS[method][0]}, {relationship}, {skewness}")
                figure.colorbar(image, ax=axis, label="Valid rate")
                figure.tight_layout()
                path = figures / f"validity_{method}_{relationship}_{skewness}.png"
                figure.savefig(path, dpi=180, bbox_inches="tight")
                plt.close(figure)
                saved.append(str(path.relative_to(output_directory)))

    if not frontiers.empty:
        figure, axis = plt.subplots(figsize=(10, 5))
        usable = frontiers[
            frontiers["relationship"].eq("equal_mi_different_shape")
            & frontiers["skewness"].isin(core_skew)
            & frontiers["shape"].isin(core_shapes)
        ].copy()
        usable["operational_frontier_n"] = pd.to_numeric(
            usable["operational_frontier_n"], errors="coerce"
        )
        shape_positions = {shape: index for index, shape in enumerate(core_shapes)}
        offsets = {"normal_wald": -0.16, "simple_welch": 0.0, "expanded_welch": 0.16}
        markers = {"balanced": "o", "strong": "s", "ultra": "^"}
        finite_frontiers = usable[np.isfinite(usable["operational_frontier_n"])]
        for (method, skewness), frame in finite_frontiers.groupby(["method", "skewness"]):
            axis.scatter(
                [shape_positions[value] + offsets[method] for value in frame["shape"]],
                frame["operational_frontier_n"],
                color=METHOD_COLORS[method],
                marker=markers[skewness],
                label=f"{METHODS[method][0]}, {skewness}",
            )
        axis.set_xticks(range(len(core_shapes)), core_shapes)
        if finite_frontiers.empty:
            axis.text(
                0.5,
                0.5,
                "No sustained operational frontier was reached\nin the tested profile.",
                ha="center",
                va="center",
                transform=axis.transAxes,
            )
            axis.set_yticks([])
        else:
            axis.set_yscale("log")
            axis.set_ylabel("Operational frontier sample size")
            axis.grid(alpha=0.2)
            axis.legend(ncol=3, fontsize=8, frameon=False)
        axis.set_xlabel("Table shape")
        axis.set_title("Sustained validity and calibration frontier")
        figure.tight_layout()
        path = figures / "operating_frontier.png"
        figure.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(figure)
        saved.append(str(path.relative_to(output_directory)))

    contrast = paired[
        np.isclose(paired["nominal_alpha"], 0.05)
        & paired["method_a"].eq("expanded_welch")
        & paired["method_b"].eq("normal_wald")
        & paired["experiment"].isin(["robustness_interaction", "robustness_imbalance"])
    ].sort_values(["experiment", "n_p", "relative_effect"])
    if not contrast.empty:
        figure, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
        for axis, experiment in zip(axes, ["robustness_interaction", "robustness_imbalance"]):
            frame = contrast[contrast["experiment"].eq(experiment)]
            for effect, group in frame.groupby("relative_effect"):
                axis.scatter(group["n_p"], group["rejection_rate_difference_a_minus_b"], s=22, label=f"e={effect:g}", alpha=0.8)
            axis.axhline(0, color="#777777", linestyle=":")
            axis.set_xscale("log")
            axis.set_xlabel("Smaller sample size")
            axis.set_title(experiment.replace("_", " ").title())
            axis.grid(alpha=0.2)
        axes[0].set_ylabel("Expanded Welch minus Wald rejection rate")
        axes[1].legend(frameon=False)
        figure.tight_layout()
        path = figures / "robustness_paired_difference.png"
        figure.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(figure)
        saved.append(str(path.relative_to(output_directory)))
    return saved


def _verification_checks(
    manifest: pd.DataFrame,
    populations: pd.DataFrame,
    results: pd.DataFrame,
    protocol: dict[str, Any],
    profile: str,
) -> dict[str, Any]:
    tolerance = float(protocol["population_construction"]["target_mi_tolerance"])
    expected_cells = len(generate_configuration_manifest(protocol, profile))
    expected_result_rows = expected_cells * len(METHODS) * 3
    checks = {
        "manifest_cell_count": len(manifest),
        "manifest_cell_count_expected": expected_cells,
        "manifest_count_pass": len(manifest) == expected_cells,
        "manifest_unique_pass": bool(manifest["configuration_id"].is_unique),
        "result_row_count": len(results),
        "result_row_count_expected": expected_result_rows,
        "result_count_pass": len(results) == expected_result_rows,
        "target_mi_tolerance_pass": bool(
            ((populations["achieved_mi_p"] - populations["target_mi_p"]).abs() <= tolerance).all()
            and ((populations["achieved_mi_q"] - populations["target_mi_q"]).abs() <= tolerance).all()
        ),
        "unconditional_rejections_within_valid_pass": bool(
            (results["rejections"] <= results["valid_replicates"]).all()
        ),
    }
    fully_valid_ids = (
        results.groupby("configuration_id")["valid_rate"]
        .min()
        .loc[lambda value: np.isclose(value, 1.0)]
        .index
    )
    all_valid = results[results["configuration_id"].isin(fully_valid_ids)]
    checks["three_denominators_equal_when_fully_valid_pass"] = bool(
        np.allclose(
            all_valid["unconditional_rejection_rate"],
            all_valid["conditional_rejection_rate"],
            equal_nan=True,
        )
        and np.allclose(
            all_valid["unconditional_rejection_rate"],
            all_valid["common_valid_rejection_rate"],
            equal_nan=True,
        )
    )
    n_two = results[
        results["experiment"].eq("calibration")
        & results["method"].eq("expanded_welch")
        & results["n_p"].eq(2)
        & np.isclose(results["nominal_alpha"], 0.05)
    ]
    checks["n2_expanded_zero_validity_pass"] = bool(
        not n_two.empty and np.allclose(n_two["valid_rate"], 0.0)
    )
    checks["all_pass"] = all(
        value for key, value in checks.items() if key.endswith("_pass")
    )
    return checks


def _write_report(
    output_directory: Path,
    metadata: dict[str, Any],
    results: pd.DataFrame,
    paired: pd.DataFrame,
    checks: dict[str, Any],
    figures: list[str],
) -> None:
    alpha = results[np.isclose(results["nominal_alpha"], 0.05)]
    primary_null = alpha[
        alpha["experiment"].eq("calibration")
        & alpha["relationship"].eq("equal_mi_different_shape")
    ]
    comparison = primary_null.pivot(
        index="configuration_id", columns="method", values="absolute_calibration_error"
    ).dropna()
    expanded_wins = int((comparison["expanded_welch"] < comparison["normal_wald"]).sum())
    wald_wins = int((comparison["expanded_welch"] > comparison["normal_wald"]).sum())
    ties = int(len(comparison) - expanded_wins - wald_wins)
    lines = [
        "# Detection and Breakdown Sweep",
        "",
        f"Profile: `{metadata['profile']}`  ",
        f"Frozen Git revision: `{metadata.get('git_revision')}`  ",
        f"Simulation cells: {metadata['completed_cells']:,}  ",
        f"Table pairs: {metadata['completed_table_pairs']:,}  ",
        f"Elapsed time: {metadata['elapsed_seconds']:.1f} seconds",
        "",
        "## Verification",
        "",
        f"All automated run checks passed: **{checks['all_pass']}**.",
        "",
        "## Primary comparison",
        "",
        "At alpha = 0.05 under the equal-MI, different-shape null, Expanded "
        f"Welch had lower absolute calibration error than Normal Wald in {expanded_wins} "
        f"of {len(comparison)} exact cells; Wald was lower in {wald_wins}, with {ties} exact ties. "
        "Configuration-level results remain the primary evidence.",
        "",
        "## Files",
        "",
        "- `configuration_manifest.csv`: every predeclared simulation cell.",
        "- `population_definitions.csv`: every fixed population pair.",
        "- `cell_results.csv`: rejection, validity, uncertainty, sparsity, and df diagnostics.",
        "- `paired_method_results.csv`: paired rejection contrasts.",
        "- `breakdown_frontier.csv`: sustained operating frontiers.",
        "- `power_reversal_flags.csv`: declines exceeding three combined Monte Carlo standard errors.",
        "- `verification_checks.json`: automated completeness and numerical checks.",
        "",
        "## Figures",
        "",
    ]
    lines.extend(f"- `{path}`" for path in figures)
    lines.extend(
        [
            "",
            "## Interpretation note",
            "",
            "Unconditional rejection rates are primary: invalid outcomes count as non-rejections. "
            "Power must be read beside the matching null false-positive rate; a liberal method's "
            "higher raw power is not automatically better.",
            "",
        ]
    )
    (output_directory / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=Path(__file__).with_name("FINAL_PROTOCOL.json"),
    )
    parser.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument("--batch-size", type=int, default=2000)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.workers < 1 or args.batch_size < 1:
        raise ValueError("Workers and batch size must be positive.")
    protocol_path = args.protocol.resolve()
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    default_output = (protocol_path.parent / protocol["output_directory"]).resolve()
    output_directory = (args.output_dir or default_output).resolve()
    if output_directory.exists() and any(output_directory.iterdir()) and not args.overwrite:
        raise FileExistsError(
            f"Output directory is not empty: {output_directory}. Use a new path or --overwrite."
        )
    output_directory.mkdir(parents=True, exist_ok=True)

    manifest = generate_configuration_manifest(protocol, args.profile)
    manifest.to_csv(output_directory / "configuration_manifest.csv", index=False)
    if args.manifest_only:
        print(f"Wrote {len(manifest):,} configurations to {output_directory}")
        return

    started_at = _utc_now()
    start = perf_counter()
    populations, definitions, failures = construct_all_populations(manifest, protocol)
    definitions.to_csv(output_directory / "population_definitions.csv", index=False)
    failures.to_csv(output_directory / "infeasible_configurations.csv", index=False)
    if not failures.empty:
        failures.to_csv(output_directory / "infeasible_configurations.csv", index=False)
        raise RuntimeError(
            f"Population preflight failed for {len(failures)} definitions; no simulation was run."
        )
    if args.preflight_only:
        print(
            f"Preflight passed for {len(definitions):,} population definitions "
            f"covering {len(manifest):,} configurations.",
            flush=True,
        )
        return

    definition_lookup = {
        (
            row["shape"],
            row["skewness"],
            row["relationship"],
            row["interaction_pair"],
            float(row["relative_effect"]),
        ): row
        for _, row in definitions.iterrows()
    }
    alphas = [float(protocol["hypothesis"]["primary_alpha"])] + [
        float(value) for value in protocol["hypothesis"]["secondary_alphas"]
    ]
    alphas = sorted(set(alphas), reverse=True)
    tasks = []
    for _, config in manifest.iterrows():
        key = _population_key(config)
        probability_p, probability_q = populations[key]
        population = definition_lookup[key]
        task_row = config.to_dict()
        task_row["population_id"] = population["population_id"]
        task_row["target_mi_p"] = population["target_mi_p"]
        task_row["target_mi_q"] = population["target_mi_q"]
        task_row["achieved_mi_p"] = population["achieved_mi_p"]
        task_row["achieved_mi_q"] = population["achieved_mi_q"]
        task_row["shared_reachable_mi"] = population["shared_reachable_mi"]
        task_row["absolute_mi_difference"] = population["absolute_mi_difference"]
        task_row["population_l1_distance"] = population["l1_distance"]
        tasks.append(
            {
                "configuration": task_row,
                "probability_p": probability_p,
                "probability_q": probability_q,
                "alphas": alphas,
                "batch_size": args.batch_size,
            }
        )

    cell_rows: list[dict[str, Any]] = []
    paired_rows: list[dict[str, Any]] = []
    completed = 0
    if args.workers == 1:
        iterator = map(_simulate_configuration, tasks)
        for result in iterator:
            cell_rows.extend(result["cell_rows"])
            paired_rows.extend(result["paired_rows"])
            completed += 1
            if completed % 25 == 0 or completed == len(tasks):
                print(f"Completed {completed:,}/{len(tasks):,} cells", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_simulate_configuration, task) for task in tasks]
            for future in as_completed(futures):
                result = future.result()
                cell_rows.extend(result["cell_rows"])
                paired_rows.extend(result["paired_rows"])
                completed += 1
                if completed % 25 == 0 or completed == len(tasks):
                    print(f"Completed {completed:,}/{len(tasks):,} cells", flush=True)

    results = pd.DataFrame(cell_rows).sort_values(
        ["configuration_id", "method", "nominal_alpha"]
    )
    paired = pd.DataFrame(paired_rows).sort_values(
        ["configuration_id", "method_a", "method_b", "nominal_alpha"]
    )
    results.to_csv(output_directory / "cell_results.csv", index=False)
    paired.to_csv(output_directory / "paired_method_results.csv", index=False)
    frontiers = _frontier_table(results, protocol)
    frontiers.to_csv(output_directory / "breakdown_frontier.csv", index=False)
    reversal_flags = _flag_power_reversals(results)
    reversal_flags.to_csv(output_directory / "power_reversal_flags.csv", index=False)
    checks = _verification_checks(manifest, definitions, results, protocol, args.profile)
    (output_directory / "verification_checks.json").write_text(
        json.dumps(checks, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if not checks["all_pass"]:
        raise RuntimeError("One or more frozen-protocol verification checks failed.")

    figures = generate_figures(results, paired, frontiers, protocol, output_directory)
    elapsed = perf_counter() - start
    metadata = {
        "title": protocol["title"],
        "profile": args.profile,
        "master_seed": protocol["master_seed"],
        "started_at_utc": started_at,
        "finished_at_utc": _utc_now(),
        "elapsed_seconds": elapsed,
        "workers": args.workers,
        "batch_size": args.batch_size,
        "completed_cells": len(manifest),
        "completed_table_pairs": int(manifest["replicates"].sum()),
        "git_revision": _git_revision(),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "scipy_version": scipy.__version__,
        "matplotlib_version": plt.matplotlib.__version__,
        "protocol_path": str(protocol_path),
        "protocol_sha256": _sha256(protocol_path),
        "runner_sha256": _sha256(Path(__file__)),
        "configuration_manifest_sha256": _sha256(output_directory / "configuration_manifest.csv"),
        "verification_checks": checks,
        "power_reversal_flag_count": len(reversal_flags),
        "figures": figures,
    }
    (output_directory / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_report(output_directory, metadata, results, paired, checks, figures)
    print(
        f"Completed {len(manifest):,} cells and {int(manifest['replicates'].sum()):,} "
        f"table pairs in {elapsed:.1f}s. Outputs: {output_directory}",
        flush=True,
    )


if __name__ == "__main__":
    main()
