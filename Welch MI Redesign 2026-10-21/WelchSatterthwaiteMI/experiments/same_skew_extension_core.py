"""Matched same-skew additions, without modifying the original study design."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from focused_study_core import (
    COMMON_MI, DIFFERENCES, REPLICATES, ROOT, SIZES, TOLERANCES,
    build_design, construct_copying, digest, influence_variance,
)
from run_large_table_construction_check import build_construction_design
from run_unequal_sample_check import ALLOCATIONS, MI_PAIRS, build_allocation_design
from thesis_redesign_core import construct_additive, margin
from welch_differential_mi.welch import _variance_influence_component_df

DEFAULT_OUTPUT = ROOT / "results/same_skew_extension"
ORIGINAL_DIRECTORIES = {
    "focused_study": ROOT / "results/focused_study",
    "large_table_construction_check": ROOT / "results/large_table_construction_check",
    "unequal_sample_check": ROOT / "results/unequal_sample_check",
}
DISPLAY_COUNTS = {"null": 120, "association": 28, "detection": 162,
                  "construction": 32, "allocation": 12}


def build_extended_design():
    base, _, populations, arrays = build_design()
    large, large_populations, large_arrays = build_construction_design()
    allocation, _, _ = build_allocation_design()
    original = {c["configuration_id"]: c for c in base + large + allocation}
    configs = dict(original)
    pairs = {p["pair_id"]: p for p in populations + large_populations}
    arrays = {**arrays, **large_arrays}
    origins = {c["configuration_id"]: "focused_study" for c in base}
    origins.update({c["configuration_id"]: "large_table_construction_check" for c in large})
    for config in allocation:
        origins.setdefault(config["configuration_id"], "unequal_sample_check")
    displays = set()

    def add(study, k, profile, mi_p, mi_q, n_p, n_q=None, construction="copying"):
        n_q = n_p if n_q is None else n_q
        spec = {"k": k, "profile": profile, "mi_p": round(mi_p, 12),
                "mi_q": round(mi_q, 12), "construction": construction}
        pair_id = "pair_" + digest(spec)[:16]
        if pair_id not in pairs:
            population = {"pair_id": pair_id, **spec}
            tables = []
            for side in "pq":
                a = margin(k, .8)
                result = (construct_copying(a, spec[f"mi_{side}"]) if construction == "copying"
                          else construct_additive(a, a, spec[f"mi_{side}"], "first", TOLERANCES))
                variance = float(influence_variance(result.probability))
                _, tau2 = _variance_influence_component_df(result.probability, np.asarray(variance))
                tau2 = float(tau2)
                if not (np.isfinite(variance) and variance > 0 and np.isfinite(tau2) and tau2 > 0):
                    raise ValueError("Population first-order assumptions fail.")
                population.update({
                    f"strength_{side}": result.strength,
                    f"achieved_mi_{side}": result.achieved_mi,
                    f"endpoint_mi_{side}": result.endpoint_mi,
                    f"variance_{side}": variance,
                    f"variance_sensitivity_variance_{side}": tau2,
                    f"minimum_probability_{side}": float(result.probability.min()),
                    f"normalization_error_{side}": result.normalization_error,
                    f"row_margin_error_{side}": result.row_margin_error,
                    f"column_margin_error_{side}": result.column_margin_error,
                    f"margin_{side}": a.tolist(),
                })
                tables.append(result.probability)
            if profile != "same_skew":
                raise AssertionError("Only missing same-skew populations may be added.")
            pairs[pair_id] = population
            arrays[pair_id] = tuple(tables)
        key = "setting_" + digest([pair_id, n_p, n_q])[:16]
        config = {"configuration_id": key, "pair_id": pair_id, **spec,
                  "n_p": n_p, "n_q": n_q, "delta": round(mi_p-mi_q, 12),
                  "replicates": REPLICATES}
        if key in configs and configs[key] != config:
            raise AssertionError("A reused setting changed.")
        configs[key] = config
        origins.setdefault(key, "same_skew_extension")
        displays.add((study, key))

    for config in base:
        if config["mi_p"] == config["mi_q"] == .02 and config["construction"] == "copying":
            displays.add(("null", config["configuration_id"]))
    for profile in ("same_skew", "different_skew"):
        for common in COMMON_MI:
            for n in (100, 1000):
                add("association", 4, profile, common, common, n)
    cases = {(k, profile) for k in SIZES for profile in ("same_skew", "different_skew")}
    cases.add((4, "uniform"))
    for k, profile in sorted(cases):
        for difference in DIFFERENCES:
            for n in (1000, 10000):
                add("detection", k, profile, .02, .02+difference, n)
    for profile in ("same_skew", "different_skew"):
        for k in (4, 16):
            for mi_p, mi_q in MI_PAIRS:
                for n in (1000, 10000):
                    for construction in ("copying", "four_cell"):
                        add("construction", k, profile, mi_p, mi_q, n, construction=construction)
        for mi_p, mi_q in MI_PAIRS:
            for n_p, n_q in ALLOCATIONS:
                add("allocation", 4, profile, mi_p, mi_q, n_p, n_q)
    all_configs = sorted(configs.values(), key=lambda c: c["configuration_id"])
    new = [c for c in all_configs if c["configuration_id"] not in original]
    if len(original) != 240 or len(new) != 72 or len(all_configs) != 312 or len(pairs) != 104:
        raise AssertionError("Unexpected extension scope.")
    display_rows = [{"study": study, "configuration_id": key} for study, key in sorted(displays)]
    for study, count in DISPLAY_COUNTS.items():
        if sum(r["study"] == study for r in display_rows) != count:
            raise AssertionError(f"Unexpected display scope: {study}")
    return all_configs, display_rows, sorted(pairs.values(), key=lambda p: p["pair_id"]), arrays, origins


def extension_design():
    configs, displays, populations, arrays, origins = build_extended_design()
    new = [c for c in configs if origins[c["configuration_id"]] == "same_skew_extension"]
    pair_ids = {c["pair_id"] for c in new}
    return (new, [r for r in displays if origins[r["configuration_id"]] == "same_skew_extension"],
            [p for p in populations if p["pair_id"] in pair_ids],
            {key: value for key, value in arrays.items() if key in pair_ids})


def directories(output=DEFAULT_OUTPUT):
    return {**ORIGINAL_DIRECTORIES, "same_skew_extension": Path(output)}


def combined_frames(output=DEFAULT_OUTPUT):
    """Select each unique setting from its original, authenticated location."""
    configs, displays, populations, arrays, origins = build_extended_design()
    frames = {name: [] for name in ("method_results", "paired_results", "diagnostics")}
    for origin, directory in directories(output).items():
        ids = {key for key, source in origins.items() if source == origin}
        for name in frames:
            frame = pd.read_csv(directory / f"{name}.csv")
            frame = frame[frame.configuration_id.isin(ids)]
            multiplier = {"method_results": 6, "paired_results": 2, "diagnostics": 1}[name]
            if len(frame) != len(ids)*multiplier or set(frame.configuration_id) != ids:
                raise AssertionError(f"Incomplete combined evidence: {origin}/{name}")
            frames[name].append(frame)
    result = {name: pd.concat(parts, ignore_index=True) for name, parts in frames.items()}
    result.update(configurations=pd.DataFrame(configs), displays=pd.DataFrame(displays))
    return result
