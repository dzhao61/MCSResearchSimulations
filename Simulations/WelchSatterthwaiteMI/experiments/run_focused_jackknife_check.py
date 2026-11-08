#!/usr/bin/env python3
"""Bounded jackknife centering diagnostic on the original focused-study samples."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm

from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, ROOT, evaluate_tables, seed_for,
    source_fingerprint,
)
from differential_mi.statistics import jackknife_mi
from run_detection_breakdown_sweep import paired_difference_interval, wilson_interval
from run_focused_study import atomic_json, file_hash, load_records

DEFAULT_INPUT = ROOT / "results/focused_study"
DEFAULT_OUTPUT = ROOT / "results/focused_jackknife_check"
SETTINGS = ((1000, .02), (1000, .03), (10000, .02), (10000, .03))
BOOTSTRAP_REPETITIONS = 1000


def select_settings(configurations: pd.DataFrame) -> list[dict]:
    selected = []
    for n, mi_q in SETTINGS:
        rows = configurations.loc[
            (configurations.k == 16)
            & (configurations.profile == "different_skew")
            & (configurations.construction == "copying")
            & (configurations.n_p == n) & (configurations.n_q == n)
            & np.isclose(configurations.mi_p, .02, rtol=0, atol=1e-12)
            & np.isclose(configurations.mi_q, mi_q, rtol=0, atol=1e-12)
        ]
        if len(rows) != 1:
            raise ValueError(f"Expected one original setting for n={n}, I(Q)={mi_q}.")
        selected.append(rows.iloc[0].to_dict())
    return selected


def original_counts(config: dict, p, q, index: int, size: int):
    rng_p = np.random.default_rng(seed_for("full", config["configuration_id"], index, "p"))
    rng_q = np.random.default_rng(seed_for("full", config["configuration_id"], index, "q"))
    counts_p = rng_p.multinomial(int(config["n_p"]), p.ravel(), size=size).reshape(size, *p.shape)
    counts_q = rng_q.multinomial(int(config["n_q"]), q.ravel(), size=size).reshape(size, *q.shape)
    return counts_p, counts_q


def literal_mi(table: np.ndarray) -> float:
    table = np.asarray(table, float)
    n = table.sum()
    rows, columns = table.sum(axis=1), table.sum(axis=0)
    occupied = table > 0
    denominator = np.outer(rows, columns)
    return float(np.sum(table[occupied]/n * np.log(table[occupied]*n/denominator[occupied])))


def literal_jackknife(table: np.ndarray) -> float:
    """Independent cell-weighted evaluation of the delete-one definition."""
    table = np.asarray(table, float)
    n = table.sum()
    if n <= 1:
        raise ValueError("Jackknife requires at least two observations.")
    leave_one_out = 0.0
    for i, j in np.argwhere(table > 0):
        reduced = table.copy()
        reduced[i, j] -= 1
        leave_one_out += table[i, j]/n * literal_mi(reduced)
    return n*literal_mi(table) - (n-1)*leave_one_out


def fixed_se_test(delta, standard_error, base_valid):
    delta, standard_error = np.asarray(delta), np.asarray(standard_error)
    valid = np.asarray(base_valid, bool) & np.isfinite(delta)
    valid &= np.isfinite(standard_error) & (standard_error > 0)
    statistic = np.divide(delta, standard_error, out=np.full_like(delta, np.nan, dtype=float),
                          where=valid)
    valid &= np.isfinite(statistic)
    p_value = np.where(valid, 2*norm.sf(np.abs(statistic)), np.nan)
    return valid, statistic, p_value


def mean_interval(values) -> dict:
    values = np.asarray(values, float)
    if len(values) < 2 or not np.isfinite(values).all():
        raise ValueError("Monte Carlo means require at least two finite values.")
    mean = float(np.mean(values))
    mcse = float(np.std(values, ddof=1)/np.sqrt(len(values)))
    return {"mean": mean, "mcse": mcse, "low": mean-1.96*mcse, "high": mean+1.96*mcse}


def rate_interval(mask) -> dict:
    mask = np.asarray(mask, bool)
    count, total = int(mask.sum()), len(mask)
    low, high = wilson_interval(count, total)
    return {"count": count, "rate": count/total, "low": low, "high": high}


def variance_ratio_interval(delta, squared_se, seed: int) -> list[float] | None:
    # This bootstrap quantifies Monte Carlo uncertainty in saved-output summaries,
    # not uncertainty for an individual MI comparison or a bootstrap test.
    delta, squared_se = np.asarray(delta), np.asarray(squared_se)
    if len(delta) < 2 or np.var(delta, ddof=1) <= 0:
        return None
    rng = np.random.default_rng(seed)
    ratios = []
    for offset in range(0, BOOTSTRAP_REPETITIONS, 25):
        count = min(25, BOOTSTRAP_REPETITIONS-offset)
        index = rng.integers(0, len(delta), size=(count, len(delta)))
        observed = np.var(delta[index], axis=1, ddof=1)
        if np.any(observed <= 0):
            return None
        ratios.extend((np.mean(squared_se[index], axis=1)/observed).tolist())
    return np.quantile(ratios, [.025, .975]).tolist()


def estimator_summary(delta, mi_p, mi_q, standard_error, base_valid, config, method):
    delta = np.asarray(delta)
    if not np.isfinite(delta).all():
        raise AssertionError("All estimator outputs must be reported; nonfinite values encountered.")
    valid, statistic, p_value = fixed_se_test(delta, standard_error, base_valid)
    rejected = valid & (p_value <= ALPHA)
    true_delta = float(config["delta"])
    squared_se = np.asarray(standard_error)**2
    variance = float(np.var(delta, ddof=1))
    row = {
        "configuration_id": config["configuration_id"], "n": int(config["n_p"]),
        "mi_p": float(config["mi_p"]), "mi_q": float(config["mi_q"]),
        "true_delta": true_delta, "method": method, "repetitions": len(delta),
        "valid_count": int(valid.sum()), "valid_rate": float(valid.mean()),
        "mean_difference": float(delta.mean()), "bias": mean_interval(delta-true_delta),
        "bias_p": mean_interval(np.asarray(mi_p)-config["mi_p"]),
        "bias_q": mean_interval(np.asarray(mi_q)-config["mi_q"]),
        "observed_sd": float(np.sqrt(variance)),
        "rmse": float(np.sqrt(np.mean((delta-true_delta)**2))),
        "mean_squared_se": float(squared_se.mean()),
        "se_variance_ratio": float(squared_se.mean()/variance),
        "se_variance_ratio_interval": variance_ratio_interval(
            delta, squared_se, seed_for("jackknife_mc", config["configuration_id"])),
        "rejection": rate_interval(rejected),
        "negative_mi_p": rate_interval(np.asarray(mi_p) < 0),
        "negative_mi_q": rate_interval(np.asarray(mi_q) < 0),
        "correct_direction": None, "opposite_direction": None,
        "opposite_fraction_among_rejections": None,
    }
    if true_delta != 0:
        correct = rejected & (delta*true_delta > 0)
        opposite = rejected & (delta*true_delta < 0)
        if int(correct.sum()+opposite.sum()) != int(rejected.sum()):
            raise AssertionError("Direction counts do not partition alternative rejections.")
        row["correct_direction"] = rate_interval(correct)
        row["opposite_direction"] = rate_interval(opposite)
        if rejected.any():
            row["opposite_fraction_among_rejections"] = float(opposite.sum()/rejected.sum())
    return row, rejected, valid, statistic, p_value


def paired_summary(analytic_delta, jackknife_delta, analytic_reject, jackknife_reject, true_delta):
    estimate, mcse, low, high = paired_difference_interval(
        int((jackknife_reject & ~analytic_reject).sum()),
        int((analytic_reject & ~jackknife_reject).sum()), len(analytic_reject))
    return {
        "bias_change_jackknife_minus_analytic": mean_interval(jackknife_delta-analytic_delta),
        "squared_error_change_jackknife_minus_analytic": mean_interval(
            (jackknife_delta-true_delta)**2 - (analytic_delta-true_delta)**2),
        "rejection_change_jackknife_minus_analytic": {
            "estimate": estimate, "mcse": mcse, "low": low, "high": high,
            "only_jackknife": int((jackknife_reject & ~analytic_reject).sum()),
            "only_analytic": int((analytic_reject & ~jackknife_reject).sum()),
        },
    }


def protocol_for(input_dir: Path, configurations: list[dict]) -> dict:
    identity = json.loads((input_dir/"study_identity.json").read_text())
    expected = {"phase": "full", "count": REPLICATES, "chunk_size": CHUNK_SIZE,
                "master_seed": MASTER_SEED, "alpha": ALPHA, "source": source_fingerprint(),
                "numpy": np.__version__, "scipy": scipy.__version__}
    for key, value in expected.items():
        if identity[key] != value:
            raise AssertionError(f"Original study identity mismatch: {key}.")
    return {
        "question": "Does jackknife centering reduce unequal bias and wrong-direction rejections?",
        "scope": configurations, "replicates_per_setting": REPLICATES, "alpha": ALPHA,
        "methods": ["analytic_normal", "jackknife_fixed_se_normal"],
        "correction": "Delete-one jackknife of raw plug-in MI replaces the analytic correction.",
        "uncertainty": "Original per-sample delta-method standard errors and normal cutoffs are fixed.",
        "interpretation": "Estimator diagnostic, not an automatically validated new test.",
        "rules": ["No clipping negative MI", "Report all four settings regardless of outcome",
                  "No new populations or estimator grid", "Original records remain unchanged"],
        "monte_carlo": {"mean_intervals": "normal 95%", "rate_intervals": "Wilson 95%",
                        "rejection_contrasts": "paired normal 95%",
                        "variance_ratio_intervals": "paired saved-output percentile bootstrap 95%",
                        "bootstrap_repetitions": BOOTSTRAP_REPETITIONS},
        "original_identity": identity,
        "input_hashes": {name: file_hash(input_dir/name) for name in (
            "study_identity.json", "configuration_manifest.csv", "populations.npz")},
        "original_record_hashes": {
            str(path.relative_to(input_dir)): file_hash(path)
            for config in configurations
            for path in sorted((input_dir/"records"/config["configuration_id"]).glob("*"))
            if path.is_file()
        },
        "diagnostic_source_hash": file_hash(Path(__file__)),
        "original_loader_hash": file_hash(Path(__file__).with_name("run_focused_study.py")),
    }


def run_setting(config, p, q, input_dir: Path):
    original = load_records(input_dir/"records"/config["configuration_id"], REPLICATES)
    parts_p, parts_q = [], []
    sample_digest = hashlib.sha256()
    literal_checks = 0
    for index, offset in enumerate(range(0, REPLICATES, CHUNK_SIZE)):
        size = min(CHUNK_SIZE, REPLICATES-offset)
        counts_p, counts_q = original_counts(config, p, q, index, size)
        regenerated = evaluate_tables(counts_p, counts_q)
        for key, value in regenerated.items():
            np.testing.assert_allclose(value, original[key][offset:offset+size],
                                       atol=1e-13, rtol=1e-11, equal_nan=True,
                                       err_msg=f"Original-sample mismatch: {key}, chunk {index}.")
        for counts in (counts_p, counts_q):
            sample_digest.update(counts.astype("<i8", copy=False).tobytes())
        jk_p, jk_q = np.asarray(jackknife_mi(counts_p)), np.asarray(jackknife_mi(counts_q))
        if index == 0:
            for counts, result in ((counts_p, jk_p), (counts_q, jk_q)):
                for sample in range(2):
                    np.testing.assert_allclose(result[sample], literal_jackknife(counts[sample]),
                                               atol=3e-11, rtol=1e-9)
                    literal_checks += 1
        parts_p.append(jk_p)
        parts_q.append(jk_q)
    jk_p, jk_q = np.concatenate(parts_p), np.concatenate(parts_q)
    jk_delta = jk_p-jk_q
    common = (original["standard_error"], original["base_valid"], config)
    analytic = estimator_summary(original["delta_corrected"], original["corrected_mi_p"],
                                 original["corrected_mi_q"], *common, "analytic_normal")
    jackknife = estimator_summary(jk_delta, jk_p, jk_q, *common, "jackknife_fixed_se_normal")
    np.testing.assert_allclose(analytic[4], original["normal_p_value"], atol=1e-13, rtol=1e-11)
    np.testing.assert_array_equal(jackknife[2], analytic[2])
    paired = {"configuration_id": config["configuration_id"], "n": int(config["n_p"]),
              "true_delta": float(config["delta"]),
              **paired_summary(original["delta_corrected"], jk_delta, analytic[1], jackknife[1],
                               config["delta"])}
    records = {
        "analytic_delta": original["delta_corrected"], "jackknife_delta": jk_delta,
        "jackknife_mi_p": jk_p, "jackknife_mi_q": jk_q,
        "standard_error": original["standard_error"], "base_valid": original["base_valid"],
        "jackknife_statistic": jackknife[3], "jackknife_p_value": jackknife[4],
        "analytic_rejected": analytic[1], "jackknife_rejected": jackknife[1],
    }
    verification = {"configuration_id": config["configuration_id"],
                    "original_sample_pairs_verified": REPLICATES, "literal_checks": literal_checks,
                    "sample_counts_sha256": sample_digest.hexdigest(),
                    "all_estimators_finite": True, "validity_masks_unchanged": True}
    return [analytic[0], jackknife[0]], paired, records, verification


def flat_row(row: dict) -> dict:
    flat = {}
    for key, value in row.items():
        if isinstance(value, dict):
            flat.update({f"{key}_{name}": item for name, item in value.items()})
        else:
            flat[key] = value
    return flat


def report_text(rows, paired) -> str:
    lines = ["# Focused Jackknife Diagnostic", "",
             "Original standard errors and normal-distribution cutoffs are unchanged.",
             "The jackknife replaces the analytic correction; negative estimates are retained.",
             "All rates use all 20,000 repetitions. Direction is undefined under equal MI.", "",
             "| n | True difference | Correction | Difference bias | Observed SD | SE variance ratio | Rejection | Correct-direction rejection | Opposite-direction rejection |",
             "| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in rows:
        direction = [f"{row[key]['rate']:.4f}" if row[key] is not None else "N/A"
                     for key in ("correct_direction", "opposite_direction")]
        name = "Analytic" if row["method"] == "analytic_normal" else "Jackknife"
        lines.append(f"| {row['n']:,} | {row['true_delta']:.2f} | {name} | "
                     f"{row['bias']['mean']:.5f} | {row['observed_sd']:.5f} | "
                     f"{row['se_variance_ratio']:.3f} | {row['rejection']['rate']:.4f} | "
                     f"{direction[0]} | {direction[1]} |")
    lines += ["", "## Paired Changes", "",
              "Intervals below quantify Monte Carlo uncertainty, not uncertainty for one observed dataset.", ""]
    for row in paired:
        bias = row["bias_change_jackknife_minus_analytic"]
        rejection = row["rejection_change_jackknife_minus_analytic"]
        lines.append(f"- n={row['n']:,}, true difference={row['true_delta']:.2f}: "
                     f"bias change {bias['mean']:.5f} [{bias['low']:.5f}, {bias['high']:.5f}]; "
                     f"rejection-rate change {rejection['estimate']:.4f} "
                     f"[{rejection['low']:.4f}, {rejection['high']:.4f}].")
    lines += ["", "These fixed-standard-error results are a diagnostic. Check the standard-error",
              "variance ratio before treating the changed numerator as a calibrated test.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "run", "audit"))
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Use a separate output directory from the original study.")
    configs = select_settings(pd.read_csv(args.input/"configuration_manifest.csv"))
    protocol = protocol_for(args.input, configs)
    args.output.mkdir(parents=True, exist_ok=True)
    protocol_path = args.output/"protocol.json"
    if protocol_path.exists():
        if json.loads(protocol_path.read_text()) != protocol:
            raise RuntimeError("Diagnostic identity changed; use a separate output directory.")
    elif args.mode == "audit":
        raise RuntimeError("No diagnostic protocol to audit.")
    else:
        atomic_json(protocol_path, protocol)
    if args.mode == "preflight":
        print(f"Protocol saved: {len(configs)} settings, {REPLICATES:,} pairs each; no outcomes evaluated.")
        return
    if args.mode == "run" and list(args.output.glob("*.npz")):
        raise RuntimeError("Results already exist; use audit or a new output directory.")
    rows, paired, checks = [], [], []
    start = perf_counter()
    with np.load(args.input/"populations.npz", allow_pickle=False) as populations:
        for config in configs:
            key, pair_id = config["configuration_id"], config["pair_id"]
            summary, comparison, records, check = run_setting(
                config, populations[f"{pair_id}_p"], populations[f"{pair_id}_q"], args.input)
            path = args.output/f"{key}.npz"
            if args.mode == "run":
                np.savez_compressed(path, **records)
            else:
                with np.load(path, allow_pickle=False) as saved:
                    if set(saved.files) != set(records):
                        raise AssertionError("Saved diagnostic record fields changed.")
                    for name, value in records.items():
                        np.testing.assert_array_equal(saved[name], value)
            check["record_sha256"] = file_hash(path)
            rows.extend(summary)
            paired.append(comparison)
            checks.append(check)
            print(f"Verified n={config['n_p']}, true difference={config['delta']:.2f}: "
                  f"20,000 original pairs; {perf_counter()-start:.1f}s elapsed.", flush=True)
    evidence = {"protocol": protocol, "estimators": rows, "paired": paired}
    estimator_csv = pd.DataFrame([flat_row(row) for row in rows]).to_csv(index=False)
    paired_csv = pd.DataFrame([flat_row(row) for row in paired]).to_csv(index=False)
    verification = {"all_pass": True, "settings": 4, "original_sample_pairs_verified": 80000,
                    "original_input_hashes_unchanged": True, "checks": checks}
    if protocol_for(args.input, configs) != protocol:
        raise AssertionError("Original inputs or diagnostic sources changed during the run.")
    if args.mode == "audit":
        if json.loads((args.output/"evidence.json").read_text()) != evidence:
            raise AssertionError("Saved evidence changed.")
        if json.loads((args.output/"verification.json").read_text()) != verification:
            raise AssertionError("Saved verification changed.")
        if (args.output/"RESULTS.md").read_text() != report_text(rows, paired):
            raise AssertionError("Saved report changed.")
        for name, expected in (("estimator_results.csv", estimator_csv), ("paired_results.csv", paired_csv)):
            if (args.output/name).read_text() != expected:
                raise AssertionError(f"Saved summary changed: {name}.")
    else:
        atomic_json(args.output/"evidence.json", evidence)
        atomic_json(args.output/"verification.json", verification)
        (args.output/"estimator_results.csv").write_text(estimator_csv)
        (args.output/"paired_results.csv").write_text(paired_csv)
        (args.output/"RESULTS.md").write_text(report_text(rows, paired))
    print(f"All checks passed; outputs in {args.output}.", flush=True)


if __name__ == "__main__":
    main()
