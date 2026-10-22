#!/usr/bin/env python3
"""Run a fixed-total allocation check without changing the focused study."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

from audit_focused_study import audit
from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, ROOT, SCHEMA_VERSION,
    build_design, digest, source_fingerprint,
)
from run_focused_study import (
    aggregate, atomic_json, audit_records, file_hash, load_records, run_configuration,
)

ALLOCATIONS = ((1000, 1000), (400, 1600), (1600, 400))
MI_PAIRS = ((.02, .02), (.02, .03))
DEFAULT_BASE = ROOT / "results/focused_study"
DEFAULT_OUTPUT = ROOT / "results/unequal_sample_check"


def build_allocation_design():
    base_configs, _, base_populations, base_arrays = build_design()
    balanced = [c for c in base_configs if c["k"] == 4
                and c["profile"] == "different_skew" and c["construction"] == "copying"
                and c["n_p"] == c["n_q"] == 1000
                and (c["mi_p"], c["mi_q"]) in MI_PAIRS]
    if len(balanced) != 2:
        raise AssertionError("Expected exactly two balanced comparisons.")
    configurations = []
    for template in balanced:
        for n_p, n_q in ALLOCATIONS:
            configurations.append({**template, "n_p": n_p, "n_q": n_q,
                                   "configuration_id": "setting_" + digest(
                                       [template["pair_id"], n_p, n_q])[:16]})
    ids = {c["pair_id"] for c in configurations}
    populations = [p for p in base_populations if p["pair_id"] in ids]
    arrays = {key: pair for key, pair in base_arrays.items() if key in ids}
    return sorted(configurations, key=lambda c: c["configuration_id"]), populations, arrays


def extension_fingerprint():
    return digest({"runner": file_hash(Path(__file__)),
                   "sampling_runner": file_hash(Path(__file__).with_name("run_focused_study.py")),
                   "audit": file_hash(Path(__file__).with_name("audit_focused_study.py"))})


def checked_base_identity(base: Path):
    identity = json.loads((base / "study_identity.json").read_text())
    configs, _, populations, _ = build_design()
    if (identity["source"] != source_fingerprint() or identity["phase"] != "full"
            or identity["count"] != REPLICATES
            or identity["design_digest"] != digest([configs, populations])):
        raise AssertionError("Balanced results do not match the unchanged focused study.")
    return identity


def import_balanced(config: dict, base: Path, output: Path, base_identity: dict):
    source = base / "records" / config["configuration_id"]
    metadata = json.loads((source / "identity.json").read_text())
    expected = {"configuration": config, "count": REPLICATES, "phase": "full",
                "fingerprint": digest(base_identity), "chunk_size": CHUNK_SIZE}
    if metadata != expected:
        raise AssertionError("Balanced checkpoint identity does not match its setting.")
    values = load_records(source, REPLICATES)
    audit_records(config, values)
    target = output / "records" / config["configuration_id"]
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.iterdir()):
        if path.name != "identity.json" and not path.name.startswith("chunk_"):
            continue
        destination = target / path.name
        if destination.exists():
            if file_hash(destination) != file_hash(path):
                raise AssertionError("Imported balanced checkpoint differs from the original.")
        else:
            shutil.copyfile(path, destination)


def audit_check(output: Path):
    identity = json.loads((output / "study_identity.json").read_text())
    configs, populations, arrays = build_allocation_design()
    if (identity["extension_source"] != extension_fingerprint()
            or identity["design_digest"] != digest([configs, populations])
            or identity["phase"] != "full" or identity["count"] != REPLICATES):
        raise AssertionError("Allocation protocol, source or phase differs from the run.")
    saved = pd.read_csv(output / "configuration_manifest.csv").to_dict("records")
    if saved != configs or json.loads((output / "population_definitions.json").read_text()) != populations:
        raise AssertionError("Saved allocation design differs from the planned comparisons.")
    with np.load(output / "populations.npz", allow_pickle=False) as stored:
        for key, pair in arrays.items():
            for side, probability in zip("pq", pair, strict=True):
                np.testing.assert_array_equal(stored[f"{key}_{side}"], probability)
    balanced_ids = sorted(c["configuration_id"] for c in configs if c["n_p"] == c["n_q"])
    if identity["imported_balanced_ids"] != balanced_ids:
        raise AssertionError("Balanced reuse is not recorded correctly.")
    base_identity = identity["balanced_source_identity"]
    if base_identity["source"] != source_fingerprint():
        raise AssertionError("Imported balanced results use different statistical code.")
    for config in configs:
        metadata = json.loads((output / "records" / config["configuration_id"] / "identity.json").read_text())
        expected = {"configuration": config, "count": REPLICATES, "phase": "full",
                    "fingerprint": digest(base_identity if config["n_p"] == config["n_q"] else identity),
                    "chunk_size": CHUNK_SIZE}
        if metadata != expected:
            raise AssertionError("Checkpoint provenance differs from its run identity.")
        audit_records(config, load_records(output / "records" / config["configuration_id"], REPLICATES))
    audit(output, expected_settings=6, expected_pairs=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "pilot", "full", "audit"))
    parser.add_argument("--base-results", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-size", type=int, default=250)
    args = parser.parse_args()
    if args.batch_size <= 0:
        parser.error("Batch size must be positive.")
    if args.output.resolve() == args.base_results.resolve():
        parser.error("The supporting check must not overwrite the focused study.")
    configs, populations, arrays = build_allocation_design()
    if args.mode == "audit":
        audit_check(args.output)
        return
    phase = "pilot" if args.mode == "pilot" else "full"
    count = 200 if phase == "pilot" else REPLICATES
    output = args.output / "pilot" if phase == "pilot" else args.output
    base_identity = checked_base_identity(args.base_results)
    balanced_ids = sorted(c["configuration_id"] for c in configs if c["n_p"] == c["n_q"])
    identity = {"schema": SCHEMA_VERSION, "master_seed": MASTER_SEED,
                "source": source_fingerprint(), "extension_source": extension_fingerprint(),
                "numpy": np.__version__, "scipy": scipy.__version__, "python": platform.python_version(),
                "machine": platform.machine(), "platform": platform.platform(),
                "phase": phase, "count": count, "chunk_size": CHUNK_SIZE,
                "design_digest": digest([configs, populations]), "alpha": ALPHA,
                "balanced_source_identity": base_identity,
                "imported_balanced_ids": balanced_ids if phase == "full" else []}
    output.mkdir(parents=True, exist_ok=True)
    identity_path = output / "study_identity.json"
    if identity_path.exists() and json.loads(identity_path.read_text()) != identity:
        raise RuntimeError("Allocation run identity changed; use a separate output directory.")
    atomic_json(identity_path, identity)
    atomic_json(output / "population_definitions.json", populations)
    pd.DataFrame(configs).to_csv(output / "configuration_manifest.csv", index=False)
    with (output / "populations.npz").open("wb") as handle:
        np.savez_compressed(handle, **{f"{key}_{side}": probability
                           for key, pair in arrays.items() for side, probability in zip("pq", pair, strict=True)})
    print(f"Allocation check: 6 settings, 2 fixed pairs; {phase}.", flush=True)
    if args.mode == "preflight":
        return
    start = perf_counter()
    completion = []
    for config in configs:
        if phase == "full" and config["n_p"] == config["n_q"]:
            import_balanced(config, args.base_results, output, base_identity)
            completion.append({"configuration_id": config["configuration_id"],
                               "origin": "reused_balanced", "new_replicates": 0})
        else:
            task = (config, *arrays[config["pair_id"]], output / "records", count,
                    args.batch_size, phase, digest(identity))
            row = run_configuration(task)
            completion.append({**row, "origin": "pilot" if phase == "pilot" else "new_unequal",
                               "new_replicates": count-row["resumed_replicates"]})
        print(f"Completed {config['n_p']}/{config['n_q']}, MI(Q)={config['mi_q']:.2f} "
              f"in {perf_counter()-start:.1f}s", flush=True)
    pd.DataFrame(completion).to_csv(output / "execution.csv", index=False)
    aggregate(output, configs, populations, count)
    if phase == "full":
        audit_check(output)


if __name__ == "__main__":
    main()
