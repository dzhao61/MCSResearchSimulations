#!/usr/bin/env python3
"""Run and authenticate the 72 pre-specified matched same-skew additions."""

from __future__ import annotations

import argparse
import json
import platform
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

from audit_focused_study import audit
from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, digest, source_fingerprint,
)
from run_focused_study import aggregate, atomic_json, audit_records, file_hash, load_records, run_configuration
from run_large_table_construction_check import audit_check as audit_large
from run_unequal_sample_check import audit_check as audit_allocation
from same_skew_extension_core import (
    DEFAULT_OUTPUT, ORIGINAL_DIRECTORIES, build_extended_design, combined_frames, extension_design,
)


def extension_fingerprint():
    return digest({name: file_hash(Path(__file__).with_name(name)) for name in (
        "run_same_skew_extension.py", "same_skew_extension_core.py", "run_focused_study.py",
        "run_large_table_construction_check.py", "run_unequal_sample_check.py", "audit_focused_study.py")})


def original_inputs():
    return {origin: {name: file_hash(directory / name) for name in (
        "study_identity.json", "configuration_manifest.csv", "population_definitions.json",
        "populations.npz", "method_results.csv", "paired_results.csv", "diagnostics.csv")}
        for origin, directory in ORIGINAL_DIRECTORIES.items()}


def audit_extension(output=DEFAULT_OUTPUT, *, audit_originals=True):
    configs, displays, populations, arrays = extension_design()
    identity = json.loads((output / "study_identity.json").read_text())
    expected = {"source": source_fingerprint(), "extension_source": extension_fingerprint(),
                "design_digest": digest([configs, displays, populations]), "phase": "full",
                "count": REPLICATES, "master_seed": MASTER_SEED, "chunk_size": CHUNK_SIZE,
                "alpha": ALPHA, "original_inputs": original_inputs()}
    if any(identity.get(key) != value for key, value in expected.items()):
        raise AssertionError("Extension identity, original evidence or protocol changed.")
    for name, rows in (("configuration_manifest.csv", configs), ("display_manifest.csv", displays)):
        saved = pd.read_csv(output / name, keep_default_na=False, float_precision="round_trip")
        pd.testing.assert_frame_equal(saved, pd.DataFrame(rows), check_dtype=False, check_exact=True)
    if json.loads((output / "population_definitions.json").read_text()) != populations:
        raise AssertionError("Extension population definitions changed.")
    with np.load(output / "populations.npz", allow_pickle=False) as stored:
        if set(stored.files) != {f"{key}_{side}" for key in arrays for side in "pq"}:
            raise AssertionError("Unexpected extension population identifiers.")
        for key, pair in arrays.items():
            for side, value in zip("pq", pair, strict=True):
                np.testing.assert_array_equal(stored[f"{key}_{side}"], value)
    for config in configs:
        directory = output / "records" / config["configuration_id"]
        metadata = json.loads((directory / "identity.json").read_text())
        if metadata != {"configuration": config, "count": REPLICATES, "phase": "full",
                        "fingerprint": digest(identity), "chunk_size": CHUNK_SIZE}:
            raise AssertionError("Extension checkpoint provenance changed.")
        audit_records(config, load_records(directory, REPLICATES))
    if audit_originals:
        audit(ORIGINAL_DIRECTORIES["focused_study"])
        audit_large(ORIGINAL_DIRECTORIES["large_table_construction_check"])
        audit_allocation(ORIGINAL_DIRECTORIES["unequal_sample_check"])
    audit(output, expected_settings=len(configs), expected_pairs=len(populations))
    all_configs, all_displays, all_populations, _, origins = build_extended_design()
    frames = combined_frames(output)
    for name, frame in frames.items():
        frame.to_csv(output / f"combined_{name}.csv", index=False)
    atomic_json(output / "combined_population_definitions.json", all_populations)
    atomic_json(output / "combined_verification.json", {
        "all_pass": True, "settings": len(all_configs), "population_pairs": len(all_populations),
        "new_settings": len(configs), "table_pairs": len(all_configs)*REPLICATES,
        "new_table_pairs": len(configs)*REPLICATES, "original_inputs": original_inputs(),
        "display_counts": pd.DataFrame(all_displays).groupby("study").size().to_dict(),
        "record_origins": origins,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "pilot", "full", "audit"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=250)
    args = parser.parse_args()
    if args.workers <= 0 or args.batch_size <= 0:
        parser.error("Workers and batch size must be positive.")
    if any(args.output.resolve() == directory.resolve() for directory in ORIGINAL_DIRECTORIES.values()):
        parser.error("Extension output must not overwrite original evidence.")
    if args.mode == "audit":
        audit_extension(args.output)
        return
    configs, displays, populations, arrays = extension_design()
    phase = "pilot" if args.mode == "pilot" else "full"
    count = 200 if phase == "pilot" else REPLICATES
    output = args.output / "pilot" if phase == "pilot" else args.output
    identity = {"schema": 1, "master_seed": MASTER_SEED, "source": source_fingerprint(),
                "extension_source": extension_fingerprint(), "numpy": np.__version__,
                "scipy": scipy.__version__, "python": platform.python_version(),
                "machine": platform.machine(), "platform": platform.platform(),
                "phase": phase, "count": count, "chunk_size": CHUNK_SIZE, "alpha": ALPHA,
                "design_digest": digest([configs, displays, populations]), "original_inputs": original_inputs()}
    output.mkdir(parents=True, exist_ok=True)
    identity_path = output / "study_identity.json"
    if identity_path.exists() and json.loads(identity_path.read_text()) != identity:
        raise RuntimeError("Extension identity changed; use a separate output directory.")
    atomic_json(identity_path, identity)
    atomic_json(output / "population_definitions.json", populations)
    pd.DataFrame(configs).to_csv(output / "configuration_manifest.csv", index=False)
    pd.DataFrame(displays).to_csv(output / "display_manifest.csv", index=False)
    with (output / "populations.npz").open("wb") as handle:
        np.savez_compressed(handle, **{f"{key}_{side}": value for key, pair in arrays.items()
                                      for side, value in zip("pq", pair, strict=True)})
    print(f"Same-skew extension: {len(configs)} new settings, {len(configs)*count:,} sampled pairs ({phase}).", flush=True)
    if args.mode == "preflight":
        return
    start = perf_counter()
    tasks = [(config, *arrays[config["pair_id"]], output / "records", count,
              args.batch_size, phase, digest(identity)) for config in configs]
    completion = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        for future in as_completed([executor.submit(run_configuration, task) for task in tasks]):
            completion.append(future.result())
            if len(completion) % 12 == 0:
                print(f"Completed {len(completion)}/{len(tasks)} settings in {perf_counter()-start:.1f}s", flush=True)
    pd.DataFrame(completion).to_csv(output / "execution.csv", index=False)
    aggregate(output, configs, populations, count)
    if phase == "full":
        audit_extension(output)


if __name__ == "__main__":
    main()
