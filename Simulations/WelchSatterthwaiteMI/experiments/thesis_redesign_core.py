"""Population construction, manifest expansion and simulation for the thesis redesign."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import xlogy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parent / "DifferentialMI" / "src"))

from differential_mi.distributions import (  # noqa: E402
    interaction_pattern,
    table_with_target_mi_from_interaction,
)
from differential_mi.statistics import influence_variance  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402

from run_detection_breakdown_sweep import (  # noqa: E402
    _sample_diagnostics,
    paired_difference_interval,
    stable_seed,
    wilson_interval,
)

METHODS = {
    "normal_wald": ("Normal Wald", "normal_p_value", "base_valid"),
    "expanded_welch": (
        "Expanded Welch",
        "expanded_welch_p_value",
        "expanded_valid",
    ),
}


def parse_shape(shape: str) -> tuple[int, int]:
    rows, columns = shape.split("x", maxsplit=1)
    return int(rows), int(columns)


def canonical_float(value: float) -> str:
    return format(float(value), ".17g")


def hash_payload(payload: Any, length: int = 16) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:length]


def margin(size: int, dominant: float | None) -> np.ndarray:
    if size < 2:
        raise ValueError("Every dimension must have at least two categories.")
    if dominant is None:
        return np.full(size, 1.0 / size)
    if not 0 < dominant < 1:
        raise ValueError("Dominant marginal probability must be between zero and one.")
    values = np.full(size, (1.0 - dominant) / (size - 1))
    values[0] = dominant
    return values


def profile_margins(
    shape: str,
    protocol: dict[str, Any],
    profile: str | None = None,
    dominant_p: float | None = None,
    dominant_q: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rows, columns = parse_shape(shape)
    profile = None if profile is None or pd.isna(profile) else profile
    dominant_p = None if dominant_p is None or pd.isna(dominant_p) else float(dominant_p)
    dominant_q = None if dominant_q is None or pd.isna(dominant_q) else float(dominant_q)
    if profile is not None:
        definition = protocol["profiles"][profile]
        dominant_p = definition["p_dominant"]
        dominant_q = definition["q_dominant"]
    return (
        margin(rows, dominant_p),
        margin(columns, dominant_p),
        margin(rows, dominant_q),
        margin(columns, dominant_q),
    )


def change_matrix(rows: int, columns: int, pattern: str) -> np.ndarray:
    result = np.zeros((rows, columns))
    if pattern in {"first", "rare"}:
        row_start = 0 if pattern == "first" else rows - 2
        column_start = 0 if pattern == "first" else columns - 2
        result[row_start : row_start + 2, column_start : column_start + 2] = (
            np.array([[1.0, -1.0], [-1.0, 1.0]])
        )
    elif pattern == "spread":
        result = np.outer(
            np.linspace(-1.0, 1.0, rows),
            np.linspace(-1.0, 1.0, columns),
        )
    else:
        raise ValueError(f"Unknown change pattern: {pattern}")
    if np.max(np.abs(result.sum(axis=0))) > 1e-14:
        raise ValueError("Change matrix does not preserve column margins.")
    if np.max(np.abs(result.sum(axis=1))) > 1e-14:
        raise ValueError("Change matrix does not preserve row margins.")
    return result


def mutual_information(probability: np.ndarray) -> float:
    values = np.asarray(probability, dtype=float)
    if values.ndim != 2 or np.any(values < 0) or not np.isfinite(values).all():
        raise ValueError("Expected a finite nonnegative probability table.")
    values = values / values.sum()
    independent = np.outer(values.sum(axis=1), values.sum(axis=0))
    return float(np.sum(xlogy(values, values / independent)))


@dataclass(frozen=True)
class ConstructedTable:
    probability: np.ndarray
    achieved_mi: float
    strength: float
    endpoint_strength: float
    endpoint_mi: float
    normalization_error: float
    row_margin_error: float
    column_margin_error: float


def construct_additive(
    row: np.ndarray,
    column: np.ndarray,
    target_mi: float,
    pattern: str,
    tolerances: dict[str, float],
) -> ConstructedTable:
    base = np.outer(row, column)
    changes = change_matrix(row.size, column.size, pattern)
    endpoint = float(np.min(base[changes < 0] / -changes[changes < 0]))
    endpoint_table = base + endpoint * changes
    endpoint_mi = mutual_information(endpoint_table)
    target_tolerance = tolerances["mi_absolute"] + tolerances["mi_relative"] * target_mi
    if target_mi < 0 or target_mi >= endpoint_mi - target_tolerance:
        raise ValueError(
            f"Target MI {target_mi:.17g} is not strictly inside additive range "
            f"[0, {endpoint_mi:.17g})."
        )
    if target_mi == 0:
        strength = 0.0
    else:
        strength = float(
            brentq(
                lambda current: mutual_information(base + current * changes) - target_mi,
                0.0,
                endpoint,
                xtol=1e-15,
                rtol=1e-14,
            )
        )
    probability = base + strength * changes
    return validate_table(
        probability,
        row,
        column,
        target_mi,
        strength,
        endpoint,
        endpoint_mi,
        tolerances,
    )


def construct_loglinear(
    row: np.ndarray,
    column: np.ndarray,
    target_mi: float,
    tolerances: dict[str, float],
) -> ConstructedTable:
    interaction = interaction_pattern(row.size, column.size, "ordinal")
    probability, strength = table_with_target_mi_from_interaction(
        row,
        column,
        target_mi,
        interaction,
        mi_tolerance=tolerances["mi_absolute"] / 10.0,
        max_association=512.0,
    )
    return validate_table(
        probability,
        row,
        column,
        target_mi,
        float(strength),
        math.nan,
        math.nan,
        tolerances,
    )


def validate_table(
    probability: np.ndarray,
    row: np.ndarray,
    column: np.ndarray,
    target_mi: float,
    strength: float,
    endpoint_strength: float,
    endpoint_mi: float,
    tolerances: dict[str, float],
) -> ConstructedTable:
    values = np.asarray(probability, dtype=float)
    achieved = mutual_information(values)
    normalization_error = abs(float(values.sum()) - 1.0)
    row_error = float(np.max(np.abs(values.sum(axis=1) - row)))
    column_error = float(np.max(np.abs(values.sum(axis=0) - column)))
    mi_tolerance = tolerances["mi_absolute"] + tolerances["mi_relative"] * target_mi
    if np.any(values <= 0):
        raise ValueError("Constructed table is not strictly positive.")
    if normalization_error > tolerances["normalization"]:
        raise ValueError("Constructed table does not sum to one.")
    if max(row_error, column_error) > tolerances["margins"]:
        raise ValueError("Constructed table does not preserve its margins.")
    if abs(achieved - target_mi) > mi_tolerance:
        raise ValueError(
            f"Constructed MI error {abs(achieved-target_mi):.3g} exceeds {mi_tolerance:.3g}."
        )
    return ConstructedTable(
        probability=values,
        achieved_mi=achieved,
        strength=strength,
        endpoint_strength=endpoint_strength,
        endpoint_mi=endpoint_mi,
        normalization_error=normalization_error,
        row_margin_error=row_error,
        column_margin_error=column_error,
    )


def construct_pair(specification: dict[str, Any], protocol: dict[str, Any]) -> dict[str, Any]:
    shape = specification["shape"]
    rows, columns = parse_shape(shape)
    requested_profile = specification.get("profile")
    profile = None if requested_profile is None or pd.isna(requested_profile) else requested_profile
    requested_dominant_p = specification.get("dominant_p")
    requested_dominant_q = specification.get("dominant_q")
    dominant_p = None if requested_dominant_p is None or pd.isna(requested_dominant_p) else float(requested_dominant_p)
    dominant_q = None if requested_dominant_q is None or pd.isna(requested_dominant_q) else float(requested_dominant_q)
    row_p, column_p, row_q, column_q = profile_margins(
        shape,
        protocol,
        profile,
        dominant_p,
        dominant_q,
    )
    constructor = specification["constructor"]
    pattern = specification["pattern"]
    target_p = float(specification["target_mi_p"])
    target_q = float(specification["target_mi_q"])
    tolerances = protocol["population_tolerances"]
    if constructor == "additive":
        p = construct_additive(row_p, column_p, target_p, pattern, tolerances)
        q = construct_additive(row_q, column_q, target_q, pattern, tolerances)
        direction = change_matrix(rows, columns, pattern)
    elif constructor == "loglinear":
        p = construct_loglinear(row_p, column_p, target_p, tolerances)
        q = construct_loglinear(row_q, column_q, target_q, tolerances)
        direction = interaction_pattern(rows, columns, "ordinal")
    else:
        raise ValueError(f"Unknown constructor: {constructor}")
    probability_payload = {
        "p": [canonical_float(value) for value in p.probability.ravel()],
        "q": [canonical_float(value) for value in q.probability.ravel()],
        "shape": shape,
    }
    pair_id = "pair_" + hash_payload(probability_payload)
    return {
        "pair_id": pair_id,
        "shape": shape,
        "rows": rows,
        "columns": columns,
        "profile": profile or "custom_extreme",
        "dominant_p": dominant_p,
        "dominant_q": dominant_q,
        "constructor": constructor,
        "pattern": pattern,
        "target_mi_p": target_p,
        "target_mi_q": target_q,
        "achieved_mi_p": p.achieved_mi,
        "achieved_mi_q": q.achieved_mi,
        "signed_mi_difference_q_minus_p": q.achieved_mi - p.achieved_mi,
        "absolute_mi_difference": abs(q.achieved_mi - p.achieved_mi),
        "strength_p": p.strength,
        "strength_q": q.strength,
        "endpoint_strength_p": p.endpoint_strength,
        "endpoint_strength_q": q.endpoint_strength,
        "endpoint_mi_p": p.endpoint_mi,
        "endpoint_mi_q": q.endpoint_mi,
        "normalization_error_p": p.normalization_error,
        "normalization_error_q": q.normalization_error,
        "row_margin_error_p": p.row_margin_error,
        "row_margin_error_q": q.row_margin_error,
        "column_margin_error_p": p.column_margin_error,
        "column_margin_error_q": q.column_margin_error,
        "minimum_probability_p": float(p.probability.min()),
        "minimum_probability_q": float(q.probability.min()),
        "population_variance_p": float(influence_variance(p.probability)),
        "population_variance_q": float(influence_variance(q.probability)),
        "row_margin_p_json": json.dumps(row_p.tolist(), separators=(",", ":")),
        "column_margin_p_json": json.dumps(column_p.tolist(), separators=(",", ":")),
        "row_margin_q_json": json.dumps(row_q.tolist(), separators=(",", ":")),
        "column_margin_q_json": json.dumps(column_q.tolist(), separators=(",", ":")),
        "direction_json": json.dumps(direction.tolist(), separators=(",", ":")),
        "probability_p_json": json.dumps(p.probability.tolist(), separators=(",", ":")),
        "probability_q_json": json.dumps(q.probability.tolist(), separators=(",", ":")),
        "probability_p": p.probability,
        "probability_q": q.probability,
    }


def _target_pair(baseline: float, difference: float, mi_direction: str) -> tuple[float, float]:
    if mi_direction == "q_higher":
        return baseline, baseline + difference
    if mi_direction == "p_higher":
        return baseline + difference, baseline
    raise ValueError(f"Unknown MI direction: {mi_direction}")


def _add_curve(
    slots: list[dict[str, Any]],
    *,
    section: str,
    figure_key: str,
    row_key: str,
    row_label: str,
    column_key: str,
    column_label: str,
    shape: str,
    baseline: float,
    differences: Iterable[float],
    n_p: int,
    n_q: int,
    profile: str | None = None,
    dominant_p: float | None = None,
    dominant_q: float | None = None,
    pattern: str = "first",
    constructor: str = "additive",
    mi_direction: str = "q_higher",
    x_kind: str = "mi_difference",
) -> None:
    for difference in differences:
        target_p, target_q = _target_pair(baseline, float(difference), mi_direction)
        slots.append(
            {
                "section": section,
                "figure_key": figure_key,
                "row_key": row_key,
                "row_label": row_label,
                "column_key": column_key,
                "column_label": column_label,
                "x_kind": x_kind,
                "x_value": int(n_p) if x_kind == "sample_size" else float(difference),
                "shape": shape,
                "profile": profile,
                "dominant_p": dominant_p,
                "dominant_q": dominant_q,
                "pattern": pattern,
                "constructor": constructor,
                "baseline_mi": float(baseline),
                "mi_direction": mi_direction,
                "mi_difference": float(difference),
                "target_mi_p": target_p,
                "target_mi_q": target_q,
                "n_p": int(n_p),
                "n_q": int(n_q),
            }
        )


def expand_design(protocol: dict[str, Any]) -> pd.DataFrame:
    slots: list[dict[str, Any]] = []
    main = protocol["main"]
    for shape in main["shapes"]:
        for profile in main["profiles"]:
            for n in main["sample_sizes"]:
                group = "small" if n <= 10 else "moderate" if n <= 100 else "large"
                _add_curve(
                    slots, section="main", figure_key=f"main_{shape}_{group}",
                    row_key=profile, row_label=profile.replace("_", " "),
                    column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                    profile=profile, baseline=main["baseline_mi"],
                    differences=main["mi_differences"], n_p=n, n_q=n,
                )

    design = protocol["baseline"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for baseline in design["baseline_mi"]:
                for n in design["sample_sizes"]:
                    _add_curve(
                        slots, section="baseline", figure_key=f"baseline_{shape}_{profile}",
                        row_key=canonical_float(baseline), row_label=f"baseline MI={baseline:g}",
                        column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                        profile=profile, baseline=baseline,
                        differences=design["mi_differences"], n_p=n, n_q=n,
                    )

    design = protocol["patterns"]
    for shape in design["shapes"]:
        for pattern in design["patterns_by_shape"][shape]:
            for n in design["sample_sizes"]:
                _add_curve(
                    slots, section="patterns", figure_key=f"patterns_{shape}",
                    row_key=pattern, row_label=pattern.replace("_", " "),
                    column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                    profile=design["profile"], baseline=design["baseline_mi"],
                    differences=design["mi_differences"], n_p=n, n_q=n,
                    pattern=pattern,
                )

    design = protocol["imbalance"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for direction in design["mi_directions"]:
                for pair_index, (n_p, n_q) in enumerate(design["sample_pairs"]):
                    group = "a" if pair_index < 4 else "b"
                    _add_curve(
                        slots, section="imbalance",
                        figure_key=f"imbalance_{shape}_{profile}_{group}",
                        row_key=direction, row_label=direction.replace("_", " "),
                        column_key=f"{n_p}_{n_q}", column_label=f"nP={n_p}, nQ={n_q}",
                        shape=shape, profile=profile, baseline=design["baseline_mi"],
                        differences=design["mi_differences"], n_p=n_p, n_q=n_q,
                        mi_direction=direction,
                    )

    design = protocol["broad_effect"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for n in design["sample_sizes"]:
                _add_curve(
                    slots, section="broad_effect", figure_key=f"broad_{shape}_{profile}",
                    row_key="broad", row_label="broad MI range", column_key=str(n),
                    column_label=f"nP=nQ={n}", shape=shape, profile=profile,
                    baseline=design["baseline_mi"], differences=design["mi_differences"],
                    n_p=n, n_q=n,
                )

    design = protocol["rectangular"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for n in design["sample_sizes"]:
                _add_curve(
                    slots, section="rectangular", figure_key=f"rectangular_{shape}_{profile}",
                    row_key="rectangular", row_label="rectangular table", column_key=str(n),
                    column_label=f"nP=nQ={n}", shape=shape, profile=profile,
                    baseline=design["baseline_mi"], differences=design["mi_differences"],
                    n_p=n, n_q=n,
                )

    design = protocol["construction"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for baseline in design["baseline_mi"]:
                for constructor in design["constructors"]:
                    for n in design["sample_sizes"]:
                        _add_curve(
                            slots, section="construction",
                            figure_key=f"construction_{shape}_{profile}_b{canonical_float(baseline)}",
                            row_key=constructor, row_label=constructor,
                            column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                            profile=profile, baseline=baseline,
                            differences=design["mi_differences"], n_p=n, n_q=n,
                            constructor=constructor,
                        )

    design = protocol["extreme"]
    for shape in design["shapes"]:
        for dominant_p, dominant_q in design["dominant_pairs"]:
            row_key = f"dp{dominant_p:g}_dq{dominant_q:g}"
            for sample_index, n in enumerate(design["sample_sizes"]):
                group = "small" if sample_index < 3 else "moderate" if sample_index < 5 else "large"
                _add_curve(
                    slots, section="extreme", figure_key=f"extreme_{shape}_{group}",
                    row_key=row_key, row_label=f"dP={dominant_p:g}, dQ={dominant_q:g}",
                    column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                    dominant_p=dominant_p, dominant_q=dominant_q,
                    baseline=design["baseline_mi"], differences=design["mi_differences"],
                    n_p=n, n_q=n,
                )

    design = protocol["rare_stress"]
    dominant_p, dominant_q = design["dominant_pair"]
    for shape in design["shapes"]:
        for pattern in design["patterns"]:
            for sample_index, n in enumerate(design["sample_sizes"]):
                group = "small" if sample_index < 3 else "moderate" if sample_index < 5 else "large"
                _add_curve(
                    slots, section="rare_stress", figure_key=f"rare_stress_{shape}_{group}",
                    row_key=pattern, row_label=pattern.replace("_", " "),
                    column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                    dominant_p=dominant_p, dominant_q=dominant_q, pattern=pattern,
                    baseline=design["baseline_mi"], differences=design["mi_differences"],
                    n_p=n, n_q=n,
                )

    design = protocol["independence"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for n in design["sample_sizes"]:
                _add_curve(
                    slots, section="independence", figure_key=f"independence_{shape}",
                    row_key=profile, row_label=profile.replace("_", " "),
                    column_key=str(n), column_label=f"nP=nQ={n}", shape=shape,
                    profile=profile, baseline=0, differences=design["mi_differences"],
                    n_p=n, n_q=n,
                )

    design = protocol["convergence"]
    for shape in design["shapes"]:
        for profile in design["profiles"]:
            for baseline in design["baseline_mi"]:
                for n in design["sample_sizes"]:
                    _add_curve(
                        slots, section="convergence", figure_key=f"convergence_{shape}",
                        row_key=f"{profile}_b{canonical_float(baseline)}",
                        row_label=f"{profile.replace('_', ' ')}, baseline={baseline:g}",
                        column_key="curve", column_label="sample-size curve", shape=shape,
                        profile=profile, baseline=baseline, differences=[0], n_p=n, n_q=n,
                        x_kind="sample_size",
                    )
    for shape in design["rare_shapes"]:
        for n in design["sample_sizes"]:
            _add_curve(
                slots, section="convergence", figure_key=f"convergence_rare_{shape}",
                row_key="rare", row_label="different skew, rare block",
                column_key="curve", column_label="sample-size curve", shape=shape,
                profile=design["rare_profile"], baseline=design["rare_baseline_mi"],
                differences=[0], n_p=n, n_q=n, pattern="rare", x_kind="sample_size",
            )

    display = pd.DataFrame(slots)
    display.insert(0, "display_id", [f"display_{index:05d}" for index in range(len(display))])
    return display


def build_manifests(
    protocol: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, tuple[np.ndarray, np.ndarray]]]:
    display = expand_design(protocol)
    pair_cache: dict[tuple[Any, ...], dict[str, Any]] = {}
    pairs_by_id: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    display_pair_ids: list[str | None] = []
    for record in display.to_dict("records"):
        profile = None if pd.isna(record.get("profile")) else record.get("profile")
        dominant_p = None if pd.isna(record.get("dominant_p")) else record.get("dominant_p")
        dominant_q = None if pd.isna(record.get("dominant_q")) else record.get("dominant_q")
        key = (
            record["shape"], profile, dominant_p,
            dominant_q, record["constructor"], record["pattern"],
            canonical_float(record["target_mi_p"]), canonical_float(record["target_mi_q"]),
        )
        try:
            if key not in pair_cache:
                pair_cache[key] = construct_pair(record, protocol)
            pair = pair_cache[key]
            pairs_by_id.setdefault(pair["pair_id"], pair)
            display_pair_ids.append(pair["pair_id"])
        except Exception as error:  # preflight records the exact requested slot
            display_pair_ids.append(None)
            failures.append(
                {"display_id": record["display_id"], "error_type": type(error).__name__,
                 "error": str(error), **record}
            )
    display["pair_id"] = display_pair_ids
    if failures:
        return display, pd.DataFrame(), pd.DataFrame(failures), {}

    configuration_lookup: dict[tuple[str, int, int], str] = {}
    configuration_rows: list[dict[str, Any]] = []
    configuration_ids: list[str] = []
    for record in display.to_dict("records"):
        key = (record["pair_id"], int(record["n_p"]), int(record["n_q"]))
        if key not in configuration_lookup:
            configuration_id = "config_" + hash_payload(key)
            configuration_lookup[key] = configuration_id
            pair = pairs_by_id[record["pair_id"]]
            configuration_rows.append(
                {
                    "configuration_id": configuration_id,
                    "pair_id": record["pair_id"],
                    "shape": pair["shape"],
                    "rows": pair["rows"],
                    "columns": pair["columns"],
                    "profile": pair["profile"],
                    "dominant_p": pair["dominant_p"],
                    "dominant_q": pair["dominant_q"],
                    "constructor": pair["constructor"],
                    "pattern": pair["pattern"],
                    "target_mi_p": pair["target_mi_p"],
                    "target_mi_q": pair["target_mi_q"],
                    "achieved_mi_p": pair["achieved_mi_p"],
                    "achieved_mi_q": pair["achieved_mi_q"],
                    "signed_mi_difference_q_minus_p": pair["signed_mi_difference_q_minus_p"],
                    "absolute_mi_difference": pair["absolute_mi_difference"],
                    "n_p": int(record["n_p"]),
                    "n_q": int(record["n_q"]),
                    "replicates": int(protocol["replicates"]),
                    "simulation_seed": stable_seed(protocol["master_seed"], configuration_id),
                }
            )
        configuration_ids.append(configuration_lookup[key])
    display["configuration_id"] = configuration_ids
    configurations = pd.DataFrame(configuration_rows).sort_values("configuration_id").reset_index(drop=True)
    pair_rows = []
    population_arrays: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for pair_id, pair in sorted(pairs_by_id.items()):
        population_arrays[pair_id] = (pair["probability_p"], pair["probability_q"])
        pair_rows.append({key: value for key, value in pair.items() if key not in {"probability_p", "probability_q"}})
    populations = pd.DataFrame(pair_rows)
    return display, configurations, populations, population_arrays


def smoke_configuration_ids(display: pd.DataFrame) -> set[str]:
    selected: set[str] = set()
    grouping = ["section", "shape", "profile", "dominant_p", "dominant_q", "pattern", "constructor", "baseline_mi", "mi_direction"]
    prepared = display.copy()
    prepared[["profile"]] = prepared[["profile"]].fillna("custom_extreme")
    prepared[["dominant_p", "dominant_q"]] = prepared[["dominant_p", "dominant_q"]].fillna(-1.0)
    for _, frame in prepared.groupby(grouping, dropna=False, sort=False):
        n_values = sorted(set(zip(frame["n_p"], frame["n_q"])))
        differences = sorted(frame["mi_difference"].unique())
        for sample_pair in {n_values[0], n_values[-1]}:
            for difference in {differences[0], differences[-1]}:
                matches = frame[
                    frame["n_p"].eq(sample_pair[0])
                    & frame["n_q"].eq(sample_pair[1])
                    & np.isclose(frame["mi_difference"], difference)
                ]
                selected.update(matches["configuration_id"])
    return selected


def _summary(values: list[np.ndarray]) -> tuple[float, float, float]:
    finite = np.concatenate(values) if values else np.array([], dtype=float)
    finite = finite[np.isfinite(finite)]
    if not finite.size:
        return math.nan, math.nan, math.nan
    return float(np.median(finite)), float(np.quantile(finite, 0.05)), float(np.quantile(finite, 0.95))


def simulate_configuration(task: dict[str, Any]) -> dict[str, Any]:
    row = task["configuration"]
    probability_p = np.asarray(task["probability_p"], dtype=float)
    probability_q = np.asarray(task["probability_q"], dtype=float)
    alpha = float(task["alpha"])
    batch_size = int(task["batch_size"])
    replicates = int(row["replicates"])
    rng = np.random.default_rng(int(row["simulation_seed"]))
    valid_counts = {method: 0 for method in METHODS}
    reject_counts = {method: 0 for method in METHODS}
    common_valid_count = 0
    common_reject_counts = {method: 0 for method in METHODS}
    paired_counts = {"both": 0, "neither": 0, "only_welch": 0, "only_wald": 0}
    invalid_reasons = {method: {} for method in METHODS}
    diagnostic_sums = {
        "observed_zero_fraction_p": 0.0, "observed_zero_fraction_q": 0.0,
        "empty_row_p": 0.0, "empty_row_q": 0.0,
        "empty_column_p": 0.0, "empty_column_q": 0.0,
    }
    standard_errors: list[np.ndarray] = []
    statistics: list[np.ndarray] = []
    expanded_df: list[np.ndarray] = []
    completed = 0
    while completed < replicates:
        current = min(batch_size, replicates - completed)
        tables_p = rng.multinomial(int(row["n_p"]), probability_p.ravel(), size=current).reshape(current, *probability_p.shape)
        tables_q = rng.multinomial(int(row["n_q"]), probability_q.ravel(), size=current).reshape(current, *probability_q.shape)
        sample_p, sample_q = _sample_diagnostics(tables_p), _sample_diagnostics(tables_q)
        for suffix, sample in (("p", sample_p), ("q", sample_q)):
            diagnostic_sums[f"observed_zero_fraction_{suffix}"] += float(sample["zero_fraction"].sum())
            diagnostic_sums[f"empty_row_{suffix}"] += int(sample["empty_row"].sum())
            diagnostic_sums[f"empty_column_{suffix}"] += int(sample["empty_column"].sum())
        if int(row["n_p"]) <= 1 or int(row["n_q"]) <= 1:
            for method in METHODS:
                invalid_reasons[method]["invalid_input_total"] = (
                    invalid_reasons[method].get("invalid_input_total", 0) + current
                )
            paired_counts["neither"] += current
            completed += current
            continue
        values = differential_mi_pvalues(
            tables_p, tables_q, include_simple=False, include_expanded=True,
            include_unbiased_sensitivity=False,
        )
        standard_errors.append(np.asarray(values["standard_error"], dtype=float))
        statistics.append(np.asarray(values["statistic"], dtype=float))
        expanded_df.append(np.asarray(values["expanded_welch_degrees_of_freedom"], dtype=float))
        masks: dict[str, np.ndarray] = {}
        rejects: dict[str, np.ndarray] = {}
        for method, (_, p_key, valid_key) in METHODS.items():
            valid = np.asarray(values[valid_key], dtype=bool)
            p_value = np.asarray(values[p_key], dtype=float)
            reject = valid & (p_value <= alpha)
            masks[method] = valid
            rejects[method] = reject
            valid_counts[method] += int(valid.sum())
            reject_counts[method] += int(reject.sum())
        base = masks["normal_wald"]
        invalid_reasons["normal_wald"]["invalid_base"] = (
            invalid_reasons["normal_wald"].get("invalid_base", 0) + int((~base).sum())
        )
        df_p = np.asarray(values["expanded_component_degrees_of_freedom_p"])
        df_q = np.asarray(values["expanded_component_degrees_of_freedom_q"])
        df = np.asarray(values["expanded_welch_degrees_of_freedom"])
        reason_masks = {
            "invalid_base": ~base,
            "invalid_component_p": base & (~np.isfinite(df_p) | (df_p <= 0)),
            "invalid_component_q": base & (~np.isfinite(df_q) | (df_q <= 0)),
            "invalid_combined_df": base & (~np.isfinite(df) | (df <= 0)),
        }
        for reason, mask in reason_masks.items():
            invalid_reasons["expanded_welch"][reason] = (
                invalid_reasons["expanded_welch"].get(reason, 0) + int(mask.sum())
            )
        common = masks["normal_wald"] & masks["expanded_welch"]
        common_valid_count += int(common.sum())
        for method in METHODS:
            common_reject_counts[method] += int((common & rejects[method]).sum())
        wald, welch = rejects["normal_wald"], rejects["expanded_welch"]
        paired_counts["both"] += int((wald & welch).sum())
        paired_counts["neither"] += int((~wald & ~welch).sum())
        paired_counts["only_welch"] += int((~wald & welch).sum())
        paired_counts["only_wald"] += int((wald & ~welch).sum())
        completed += current

    expected_p = int(row["n_p"]) * probability_p
    expected_q = int(row["n_q"]) * probability_q
    shared = {
        **row,
        "minimum_true_expected_p": float(expected_p.min()),
        "minimum_true_expected_q": float(expected_q.min()),
        "true_expected_below_1_p": float(np.mean(expected_p < 1)),
        "true_expected_below_1_q": float(np.mean(expected_q < 1)),
        "true_expected_below_5_p": float(np.mean(expected_p < 5)),
        "true_expected_below_5_q": float(np.mean(expected_q < 5)),
        **{name: value / replicates for name, value in diagnostic_sums.items()},
    }
    se_median, se_p05, se_p95 = _summary(standard_errors)
    statistic_median, statistic_p05, statistic_p95 = _summary(statistics)
    df_median, df_p05, df_p95 = _summary(expanded_df)
    cell_rows = []
    for method, (label, _, _) in METHODS.items():
        valid = valid_counts[method]
        rejected = reject_counts[method]
        low, high = wilson_interval(rejected, replicates)
        cell_rows.append(
            {
                **shared, "method": method, "method_label": label,
                "nominal_alpha": alpha, "valid_replicates": valid,
                "valid_rate": valid / replicates, "rejections": rejected,
                "unconditional_rejection_rate": rejected / replicates,
                "conditional_rejection_rate": rejected / valid if valid else math.nan,
                "common_valid_replicates": common_valid_count,
                "common_valid_rate": common_valid_count / replicates,
                "common_valid_rejections": common_reject_counts[method],
                "common_valid_rejection_rate": common_reject_counts[method] / common_valid_count if common_valid_count else math.nan,
                "wilson_95_low": low, "wilson_95_high": high,
                "monte_carlo_standard_error": math.sqrt((rejected / replicates) * (1 - rejected / replicates) / replicates),
                "invalid_reason_counts_json": json.dumps(invalid_reasons[method], sort_keys=True),
                "standard_error_median": se_median, "standard_error_p05": se_p05, "standard_error_p95": se_p95,
                "statistic_median": statistic_median, "statistic_p05": statistic_p05, "statistic_p95": statistic_p95,
                "expanded_df_median": df_median if method == "expanded_welch" else math.nan,
                "expanded_df_p05": df_p05 if method == "expanded_welch" else math.nan,
                "expanded_df_p95": df_p95 if method == "expanded_welch" else math.nan,
            }
        )
    difference, paired_se, paired_low, paired_high = paired_difference_interval(
        paired_counts["only_welch"], paired_counts["only_wald"], replicates
    )
    paired_row = {
        **row, "nominal_alpha": alpha, "method_a": "expanded_welch",
        "method_b": "normal_wald", "both_reject": paired_counts["both"],
        "neither_rejects": paired_counts["neither"],
        "only_method_a_rejects": paired_counts["only_welch"],
        "only_method_b_rejects": paired_counts["only_wald"],
        "rejection_rate_difference_a_minus_b": difference,
        "paired_standard_error": paired_se, "paired_95_low": paired_low,
        "paired_95_high": paired_high,
    }
    return {"cell_rows": cell_rows, "paired_rows": [paired_row]}
