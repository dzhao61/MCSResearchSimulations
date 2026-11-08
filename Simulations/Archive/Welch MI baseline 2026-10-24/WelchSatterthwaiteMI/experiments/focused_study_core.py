"""Question-led population design and auditable summaries for the focused study."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import brentq

from thesis_redesign_core import (
    ROOT, construct_additive, margin, mutual_information, validate_table,
)
from differential_mi.statistics import influence_variance, plugin_mi
from welch_differential_mi import differential_mi_pvalues
from welch_differential_mi.welch import _variance_influence_component_df
from run_detection_breakdown_sweep import paired_difference_interval, wilson_interval

MASTER_SEED = 20261006
REPLICATES = 20000
ALPHA = 0.05
CHUNK_SIZE = 1000
SIZES = (2, 4, 8, 16)
PROFILES = {"uniform": (None, None), "same_skew": (.8, .8), "different_skew": (.7, .8)}
SAMPLE_SIZES = (10, 20, 50, 100, 250, 500, 1000, 2500, 10000, 50000)
COMMON_MI = (.0001, .0003, .001, .003, .01, .02, .05)
DIFFERENCES = (0, .001, .002, .005, .01, .02, .05, .1, .2)
TOLERANCES = {"mi_absolute": 1e-12, "mi_relative": 1e-8,
              "normalization": 1e-12, "margins": 1e-12}
SCHEMA_VERSION = 1


def digest(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def seed_for(*parts: Any) -> int:
    return int(digest([MASTER_SEED, *parts])[:16], 16)


def construct_copying(a: np.ndarray, target: float):
    a = np.asarray(a, dtype=float)
    if a.ndim != 1 or len(a) < 2 or not np.isfinite(a).all() or np.any(a <= 0):
        raise ValueError("Expected a strictly positive marginal probability vector.")
    if abs(a.sum() - 1) > 1e-12:
        raise ValueError("Marginal probabilities must sum to one.")
    endpoint_mi = float(-np.sum(a * np.log(a)))
    if not np.isfinite(target) or not 0 <= target < endpoint_mi:
        raise ValueError("Target MI must lie below the copying entropy endpoint.")
    base, diagonal = np.outer(a, a), np.diag(a)
    strength = 0.0 if target == 0 else float(brentq(
        lambda value: mutual_information((1-value)*base + value*diagonal) - target,
        0, 1, xtol=1e-15, rtol=1e-14,
    ))
    return validate_table((1-strength)*base + strength*diagonal, a, a, target,
                          strength, 1.0, endpoint_mi, TOLERANCES)


def build_design() -> tuple[list[dict], list[dict], list[dict], dict]:
    configurations: dict[str, dict] = {}
    pairs: dict[str, dict] = {}
    displays: list[dict] = []
    arrays: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    def add(study: str, k: int, profile: str, p_mi: float, q_mi: float,
            n: int, construction: str = "copying") -> None:
        # Decimal canonicalisation makes reused targets independent of float addition.
        spec = {"k": k, "profile": profile, "mi_p": round(p_mi, 12),
                "mi_q": round(q_mi, 12), "construction": construction}
        pair_id = "pair_" + digest(spec)[:16]
        if pair_id not in pairs:
            constructed = []
            row = {"pair_id": pair_id, **spec}
            for side, rho, target in zip("pq", PROFILES[profile], (spec["mi_p"], spec["mi_q"]), strict=True):
                a = margin(k, rho)
                result = (construct_copying(a, target) if construction == "copying" else
                          construct_additive(a, a, target, "first", TOLERANCES))
                v = float(influence_variance(result.probability))
                _, eta = _variance_influence_component_df(result.probability, np.asarray(v))
                if v <= 0 or not np.isfinite(v) or float(eta) <= 0 or not np.isfinite(eta):
                    raise ValueError("Population first-order assumptions fail.")
                row.update({f"strength_{side}": result.strength, f"achieved_mi_{side}": result.achieved_mi,
                            f"endpoint_mi_{side}": result.endpoint_mi, f"variance_{side}": v,
                            f"variance_sensitivity_variance_{side}": float(eta),
                            f"minimum_probability_{side}": float(result.probability.min()),
                            f"normalization_error_{side}": result.normalization_error,
                            f"row_margin_error_{side}": result.row_margin_error,
                            f"column_margin_error_{side}": result.column_margin_error,
                            f"margin_{side}": a.tolist()})
                constructed.append(result.probability)
            pairs[pair_id] = row
            arrays[pair_id] = tuple(constructed)
        config_id = "setting_" + digest([pair_id, n, n])[:16]
        configurations.setdefault(config_id, {"configuration_id": config_id, "pair_id": pair_id,
                                               **spec, "n_p": n, "n_q": n,
                                               "delta": round(p_mi-q_mi, 12), "replicates": REPLICATES})
        displays.append({"study": study, "configuration_id": config_id})

    for k in SIZES:
        for profile in PROFILES:
            for n in SAMPLE_SIZES:
                add("null", k, profile, .02, .02, n)
    for common in COMMON_MI:
        for n in (100, 1000):
            add("association", 4, "different_skew", common, common, n)
    detection_cases = {(k, "different_skew") for k in SIZES} | {(4, p) for p in PROFILES}
    for k, profile in sorted(detection_cases):
        for difference in DIFFERENCES:
            for n in (1000, 10000):
                add("detection", k, profile, .02, .02+difference, n)
    for q_mi in (.02, .03):
        for n in (1000, 10000):
            add("construction", 4, "different_skew", .02, q_mi, n, "four_cell")
    return (sorted(configurations.values(), key=lambda row: row["configuration_id"]),
            displays, sorted(pairs.values(), key=lambda row: row["pair_id"]), arrays)


def evaluate_tables(p: np.ndarray, q: np.ndarray) -> dict[str, np.ndarray]:
    values = differential_mi_pvalues(p, q, include_simple=False, include_unbiased_sensitivity=False)
    keys = ("delta_corrected", "influence_variance_p", "influence_variance_q", "standard_error",
            "statistic", "normal_p_value", "expanded_component_degrees_of_freedom_p",
            "expanded_component_degrees_of_freedom_q", "variance_influence_variance_p",
            "variance_influence_variance_q", "expanded_welch_degrees_of_freedom",
            "expanded_welch_p_value", "base_valid", "expanded_valid")
    records = {key: np.asarray(values[key]) for key in keys}
    records["squared_standard_error"] = records["standard_error"]**2
    for side, counts in (("p", p), ("q", q)):
        total = counts.sum(axis=(-2, -1))
        mi = np.asarray(plugin_mi(counts))
        records[f"plugin_mi_{side}"] = mi
        records[f"corrected_mi_{side}"] = mi - (counts.shape[-2]-1)*(counts.shape[-1]-1)/(2*total)
        records[f"empty_cells_{side}"] = np.sum(counts == 0, axis=(-2, -1)).astype(np.uint16)
        records[f"empty_rows_{side}"] = np.sum(counts.sum(axis=-1) == 0, axis=-1).astype(np.uint16)
        records[f"empty_columns_{side}"] = np.sum(counts.sum(axis=-2) == 0, axis=-1).astype(np.uint16)
    # Independent reason bits allow overlapping failures to be audited.
    base_reason = np.zeros_like(records["delta_corrected"], dtype=np.uint16)
    for bit, failure in enumerate((
        ~np.isfinite(records["delta_corrected"]),
        ~((records["influence_variance_p"]+records["influence_variance_q"]) > 1e-14),
        ~(np.isfinite(records["standard_error"]) & (records["standard_error"] > 0)),
        records["base_valid"] & ~np.isfinite(records["normal_p_value"]),
    )):
        base_reason |= failure.astype(np.uint16) << bit
    expanded_reason = base_reason.copy()
    for bit, key in enumerate(("expanded_component_degrees_of_freedom_p",
                               "expanded_component_degrees_of_freedom_q",
                               "expanded_welch_degrees_of_freedom"), start=4):
        expanded_reason |= (~(np.isfinite(records[key]) & (records[key] > 0))).astype(np.uint16) << bit
    expanded_reason |= (records["expanded_valid"] & ~np.isfinite(records["expanded_welch_p_value"])).astype(np.uint16) << 7
    records["normal_invalid_reasons"] = base_reason
    records["expanded_invalid_reasons"] = expanded_reason
    return records


def simulate_chunk(config: dict, p: np.ndarray, q: np.ndarray, index: int,
                   count: int, batch_size: int, phase: str) -> dict[str, np.ndarray]:
    if count <= 0 or batch_size <= 0:
        raise ValueError("Chunk and batch sizes must be positive.")
    # Fixed chunks and independent P/Q streams preserve samples across batching/resume.
    rng_p = np.random.default_rng(seed_for(phase, config["configuration_id"], index, "p"))
    rng_q = np.random.default_rng(seed_for(phase, config["configuration_id"], index, "q"))
    parts: dict[str, list] = {}
    for start in range(0, count, batch_size):
        size = min(batch_size, count-start)
        counts_p = rng_p.multinomial(config["n_p"], p.ravel(), size=size).reshape(size, *p.shape)
        counts_q = rng_q.multinomial(config["n_q"], q.ravel(), size=size).reshape(size, *q.shape)
        for key, value in evaluate_tables(counts_p, counts_q).items():
            parts.setdefault(key, []).append(value)
    return {key: np.concatenate(value) for key, value in parts.items()}


def rate_summary(rejected: np.ndarray, valid: np.ndarray, mask: np.ndarray) -> dict:
    total = int(mask.sum())
    rejections = int((rejected & mask).sum())
    valid_count = int((valid & mask).sum())
    low, high = wilson_interval(rejections, total)
    valid_low, valid_high = wilson_interval(valid_count, total)
    rate = rejections/total if total else math.nan
    return {"replicates": total, "rejections": rejections, "valid_replicates": valid_count,
            "rejection_rate": rate, "rejection_low": low, "rejection_high": high,
            "rejection_mcse": math.sqrt(rate*(1-rate)/total) if total else math.nan,
            "valid_rate": valid_count/total if total else math.nan,
            "valid_low": valid_low, "valid_high": valid_high}


def paired_summary(a: np.ndarray, b: np.ndarray, mask: np.ndarray) -> dict:
    total = int(mask.sum())
    only_a = int((a & ~b & mask).sum())
    only_b = int((b & ~a & mask).sum())
    estimate, se, low, high = paired_difference_interval(only_a, only_b, total)
    return {"replicates": total, "only_wald": only_a, "only_expanded": only_b,
            "both_reject": int((a & b & mask).sum()), "neither_reject": int((~a & ~b & mask).sum()),
            "difference": estimate, "mcse": se, "low": low, "high": high}


def summarize(config: dict, population: dict, records: dict) -> tuple[list[dict], list[dict], dict]:
    delta = records["delta_corrected"]
    total = len(delta)
    valid_w = records["base_valid"].astype(bool)
    valid_e = records["expanded_valid"].astype(bool)
    reject_w = valid_w & (records["normal_p_value"] <= ALPHA)
    reject_e = valid_e & (records["expanded_welch_p_value"] <= ALPHA)
    common = valid_w & valid_e
    if np.any(reject_e & ~reject_w):
        raise AssertionError("Expanded rejection is not a subset of Wald rejection.")
    if np.any(valid_e & ~valid_w):
        raise AssertionError("Expanded validity is not a subset of Wald validity.")
    all_mask = np.ones(total, dtype=bool)
    methods = []
    for name, reject, valid in (("normal_wald", reject_w, valid_w), ("expanded_welch", reject_e, valid_e)):
        for denominator, mask in (("all", all_mask), ("method_valid", valid), ("common_valid", common)):
            methods.append({"configuration_id": config["configuration_id"], "method": name,
                            "denominator": denominator, **rate_summary(reject, valid, mask)})
    paired = [{"configuration_id": config["configuration_id"], "denominator": label,
               **paired_summary(reject_w, reject_e, mask)}
              for label, mask in (("all", all_mask), ("common_valid", common))]
    finite = np.isfinite(delta)
    matched = finite & np.isfinite(records["squared_standard_error"])
    d = delta[finite]
    observed_var = float(np.var(d, ddof=1)) if len(d) > 1 else math.nan
    matched_var = float(np.var(delta[matched], ddof=1)) if matched.sum() > 1 else math.nan
    estimated_var = float(np.mean(records["squared_standard_error"][matched])) if matched.any() else math.nan
    first_var = population["variance_p"]/config["n_p"] + population["variance_q"]/config["n_q"]
    diagnostic = {"configuration_id": config["configuration_id"], "replicates": total,
                  "finite_difference_count": int(finite.sum()), "matched_variance_count": int(matched.sum()),
                  "difference_bias": float(np.mean(d)-config["delta"]) if len(d) else math.nan,
                  "observed_variance": observed_var, "bias_mcse": math.sqrt(observed_var/len(d)) if len(d) > 1 else math.nan,
                  "matched_observed_variance": matched_var, "mean_estimated_variance": estimated_var,
                  "estimated_observed_ratio": estimated_var/matched_var if matched_var > 0 else math.nan,
                  "first_order_variance": first_var,
                  "first_order_observed_ratio": first_var/observed_var if observed_var > 0 else math.nan,
                  "degrees_of_freedom_count": int(valid_e.sum())}
    for key, quantile in (("df_p05", .05), ("df_median", .5), ("df_p95", .95)):
        diagnostic[key] = float(np.quantile(records["expanded_welch_degrees_of_freedom"][valid_e], quantile)) if valid_e.any() else math.nan
    for side in "pq":
        finite_mi = np.isfinite(records[f"corrected_mi_{side}"])
        diagnostic[f"bias_{side}"] = float(np.mean(records[f"corrected_mi_{side}"][finite_mi])-population[f"mi_{side}"]) if finite_mi.any() else math.nan
        for item in ("cells", "rows", "columns"):
            diagnostic[f"mean_empty_{item}_{side}"] = float(np.mean(records[f"empty_{item}_{side}"]))
        for method, key in (("normal", "normal_invalid_reasons"), ("expanded", "expanded_invalid_reasons")):
            for bit in range(8):
                diagnostic[f"{method}_invalid_bit_{bit}"] = int(np.count_nonzero(records[key] & (1 << bit)))
    return methods, paired, diagnostic


def source_fingerprint() -> str:
    files = [Path(__file__), ROOT / "src/welch_differential_mi/welch.py",
             ROOT.parent / "DifferentialMI/src/differential_mi/statistics.py",
             Path(__file__).with_name("thesis_redesign_core.py"),
             Path(__file__).with_name("run_detection_breakdown_sweep.py")]
    return digest({path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files})
