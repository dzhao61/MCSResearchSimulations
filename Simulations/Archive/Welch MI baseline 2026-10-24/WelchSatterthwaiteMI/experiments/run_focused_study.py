#!/usr/bin/env python3
"""Run, resume and independently summarise the focused MI study."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, ROOT, SCHEMA_VERSION,
    build_design, digest, seed_for, simulate_chunk, source_fingerprint, summarize,
)
from welch_differential_mi import differential_mi_pvalues

DEFAULT_OUTPUT = ROOT / "results/focused_study"


def atomic_json(path: Path, value: dict | list) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def run_configuration(task: tuple) -> dict:
    config, p, q, directory, count, batch, phase, fingerprint = task
    directory = Path(directory) / config["configuration_id"]
    directory.mkdir(parents=True, exist_ok=True)
    metadata = {"configuration": config, "count": count, "phase": phase,
                "fingerprint": fingerprint, "chunk_size": CHUNK_SIZE}
    metadata_path = directory / "identity.json"
    if metadata_path.exists():
        if json.loads(metadata_path.read_text()) != metadata:
            raise RuntimeError(f"Incompatible checkpoint: {directory}")
    else:
        if list(directory.glob("chunk_*")):
            raise RuntimeError(f"Unidentified checkpoint chunks: {directory}")
        atomic_json(metadata_path, metadata)
    start = perf_counter()
    resumed = 0
    for index, offset in enumerate(range(0, count, CHUNK_SIZE)):
        size = min(CHUNK_SIZE, count-offset)
        path = directory / f"chunk_{index:03d}.npz"
        checksum_path = directory / f"chunk_{index:03d}.json"
        if path.exists() and checksum_path.exists():
            checksum = json.loads(checksum_path.read_text())
            if checksum != {"sha256": file_hash(path), "replicates": size}:
                raise RuntimeError(f"Corrupted checkpoint: {path}")
            resumed += size
            continue
        records = simulate_chunk(config, p, q, index, size, batch, phase)
        temporary = path.with_suffix(".tmp")
        with temporary.open("wb") as handle:
            np.savez_compressed(handle, **records)
        temporary.replace(path)
        atomic_json(checksum_path, {"sha256": file_hash(path), "replicates": size})
    return {"configuration_id": config["configuration_id"], "seconds": perf_counter()-start,
            "replicates": count, "resumed_replicates": resumed}


def load_records(directory: Path, count: int) -> dict:
    parts: dict[str, list] = {}
    for index, offset in enumerate(range(0, count, CHUNK_SIZE)):
        path = directory / f"chunk_{index:03d}.npz"
        checksum = json.loads(path.with_suffix(".json").read_text())
        size = min(CHUNK_SIZE, count-offset)
        if checksum != {"sha256": file_hash(path), "replicates": size}:
            raise AssertionError(f"Checksum mismatch: {path}")
        with np.load(path, allow_pickle=False) as records:
            for key in records.files:
                value = records[key]
                if value.shape != (size,):
                    raise AssertionError(f"Invalid chunk shape: {path}, {key}")
                parts.setdefault(key, []).append(value)
    result = {key: np.concatenate(value) for key, value in parts.items()}
    if any(len(value) != count for value in result.values()):
        raise AssertionError("Incomplete scalar record.")
    return result


def audit_records(config: dict, values: dict) -> None:
    np.testing.assert_allclose(values["delta_corrected"], values["corrected_mi_p"]-values["corrected_mi_q"], atol=1e-13, rtol=1e-12)
    np.testing.assert_allclose(values["squared_standard_error"],
                               values["influence_variance_p"]/config["n_p"] + values["influence_variance_q"]/config["n_q"], atol=1e-13, rtol=1e-12)
    expected_base = (np.isfinite(values["delta_corrected"])
                     & ((values["influence_variance_p"]+values["influence_variance_q"]) > 1e-14)
                     & np.isfinite(values["standard_error"]) & (values["standard_error"] > 0)
                     & np.isfinite(values["normal_p_value"]))
    np.testing.assert_array_equal(values["base_valid"], expected_base)
    expanded = expected_base.copy()
    for key in ("expanded_component_degrees_of_freedom_p", "expanded_component_degrees_of_freedom_q", "expanded_welch_degrees_of_freedom"):
        expanded &= np.isfinite(values[key]) & (values[key] > 0)
    expanded &= np.isfinite(values["expanded_welch_p_value"])
    np.testing.assert_array_equal(values["expanded_valid"], expanded)
    for key in ("normal_p_value", "expanded_welch_p_value"):
        finite = values[key][np.isfinite(values[key])]
        if np.any((finite < 0) | (finite > 1)):
            raise AssertionError("P-value outside [0,1].")
    for side in "pq":
        if np.any(values[f"empty_cells_{side}"] > config["k"]**2):
            raise AssertionError("Invalid empty-cell count.")
        for item in ("rows", "columns"):
            if np.any(values[f"empty_{item}_{side}"] > config["k"]):
                raise AssertionError("Invalid empty-margin count.")
    np.testing.assert_array_equal(values["normal_invalid_reasons"] == 0, values["base_valid"])
    np.testing.assert_array_equal(values["expanded_invalid_reasons"] == 0, values["expanded_valid"])


def aggregate(output: Path, configs: list, populations: list, count: int) -> None:
    population_by_id = {p["pair_id"]: p for p in populations}
    rates, paired, diagnostics = [], [], []
    for config in configs:
        values = load_records(output / "records" / config["configuration_id"], count)
        audit_records(config, values)
        method_rows, pair_rows, diagnostic = summarize(config, population_by_id[config["pair_id"]], values)
        rates.extend(method_rows)
        paired.extend(pair_rows)
        diagnostics.append(diagnostic)
    pd.DataFrame(rates).to_csv(output / "method_results.csv", index=False)
    pd.DataFrame(paired).to_csv(output / "paired_results.csv", index=False)
    pd.DataFrame(diagnostics).to_csv(output / "diagnostics.csv", index=False)
    atomic_json(output / "verification.json", {"all_pass": True, "settings": len(configs),
                "replicates_per_setting": count, "table_pairs": count*len(configs),
                "checks": ["all chunks present and checksum verified", "scalar field dimensions",
                           "difference and variance algebra", "validity masks and reason bits",
                           "probability bounds", "paired rejection subset", "all diagnostic masks"]})


def timing(output: Path, configs: list, arrays: dict) -> None:
    rows = []
    selected = [c for c in configs if c["construction"] == "copying" and c["profile"] == "different_skew"
                and c["n_p"] == 1000 and c["mi_p"] == c["mi_q"] == .02]
    for config in sorted(selected, key=lambda c: c["k"]):
        p, q = arrays[config["pair_id"]]
        rng = np.random.default_rng(seed_for("timing", config["configuration_id"]))
        counts_p = rng.multinomial(1000, p.ravel(), size=200).reshape(200, *p.shape)
        counts_q = rng.multinomial(1000, q.ravel(), size=200).reshape(200, *q.shape)
        for expanded in (False, True):
            for i in range(20):
                differential_mi_pvalues(counts_p[i], counts_q[i], include_simple=False,
                                       include_expanded=expanded, include_unbiased_sensitivity=False)
        # Alternate order to reduce a systematic timing-order effect.
        for pass_index in range(5):
            for expanded in ((False, True) if pass_index % 2 == 0 else (True, False)):
                for i in range(200):
                    start = perf_counter()
                    differential_mi_pvalues(counts_p[i], counts_q[i], include_simple=False,
                                           include_expanded=expanded, include_unbiased_sensitivity=False)
                    rows.append({"k": config["k"], "method": "expanded_welch" if expanded else "normal_wald",
                                 "pass": pass_index, "input": i, "microseconds": (perf_counter()-start)*1e6})
    records = pd.DataFrame(rows)
    records.to_csv(output / "timing_records.csv", index=False)
    summary = records.groupby(["k", "method"])["microseconds"].agg(
        median="median", q25=lambda s: s.quantile(.25), q75=lambda s: s.quantile(.75))
    summary.to_csv(output / "timing_summary.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "pilot", "full", "audit", "timing"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=250)
    args = parser.parse_args()
    if args.workers <= 0 or args.batch_size <= 0:
        parser.error("Workers and batch size must be positive.")
    configs, displays, populations, arrays = build_design()
    if len(configs) != 232 or len(populations) != 68:
        raise AssertionError("Design scope changed.")
    output = args.output / "pilot" if args.mode == "pilot" else args.output
    phase = "pilot" if args.mode == "pilot" else "full"
    count = 200 if phase == "pilot" else REPLICATES
    identity = {"schema": SCHEMA_VERSION, "master_seed": MASTER_SEED, "source": source_fingerprint(),
                "numpy": np.__version__, "scipy": scipy.__version__, "python": platform.python_version(),
                "machine": platform.machine(), "platform": platform.platform(),
                "phase": phase, "count": count, "chunk_size": CHUNK_SIZE,
                "design_digest": digest([configs, populations]), "alpha": ALPHA}
    output.mkdir(parents=True, exist_ok=True)
    identity_path = output / "study_identity.json"
    if identity_path.exists() and json.loads(identity_path.read_text()) != identity:
        raise RuntimeError("Study identity changed; use a separate output directory.")
    atomic_json(identity_path, identity)
    atomic_json(output / "population_definitions.json", populations)
    pd.DataFrame(configs).to_csv(output / "configuration_manifest.csv", index=False)
    pd.DataFrame(displays).to_csv(output / "display_manifest.csv", index=False)
    with (output / "populations.npz").open("wb") as handle:
        np.savez_compressed(handle, **{f"{key}_{side}": value for key, pair in arrays.items() for side, value in zip("pq", pair, strict=True)})
    print(f"Preflight: {len(configs)} settings, {len(populations)} pairs, {len(configs)*count:,} sampled pairs ({phase}).", flush=True)
    if args.mode == "preflight":
        return
    if args.mode == "timing":
        timing(output, configs, arrays)
        return
    if args.mode != "audit":
        start = perf_counter()
        tasks = [(c, *arrays[c["pair_id"]], output / "records", count, args.batch_size, phase, digest(identity)) for c in configs]
        completion = []
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(run_configuration, task) for task in tasks]
            for future in as_completed(futures):
                completion.append(future.result())
                if len(completion) % 20 == 0 or len(completion) == len(configs):
                    print(f"Completed {len(completion)}/{len(configs)} settings in {perf_counter()-start:.1f}s", flush=True)
        pd.DataFrame(completion).to_csv(output / "execution.csv", index=False)
    aggregate(output, configs, populations, count)
    print("Saved scalar records, summaries and verification; all checks passed.", flush=True)


if __name__ == "__main__":
    main()
