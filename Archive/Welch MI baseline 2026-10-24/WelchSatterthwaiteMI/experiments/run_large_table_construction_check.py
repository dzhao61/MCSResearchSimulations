#!/usr/bin/env python3
"""Run the four matched large-table settings without changing the main study."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

from audit_focused_study import audit
from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, ROOT, SCHEMA_VERSION,
    TOLERANCES, digest, influence_variance, source_fingerprint,
)
from run_focused_study import (
    aggregate, atomic_json, audit_records, file_hash, load_records, run_configuration,
)
from run_unequal_sample_check import checked_base_identity
from thesis_redesign_core import construct_additive, margin
from welch_differential_mi.welch import _variance_influence_component_df

MI_PAIRS = ((.02, .02), (.02, .03))
SAMPLE_SIZES = (1000, 10000)
DEFAULT_BASE = ROOT / "results/focused_study"
DEFAULT_OUTPUT = ROOT / "results/large_table_construction_check"


def build_construction_design():
    configurations, populations, arrays = [], [], {}
    for mi_p, mi_q in MI_PAIRS:
        spec = {"k": 16, "profile": "different_skew", "mi_p": mi_p,
                "mi_q": mi_q, "construction": "four_cell"}
        pair_id = "pair_" + digest(spec)[:16]
        population = {"pair_id": pair_id, **spec}
        pair = []
        for side, rho, target in zip("pq", (.7, .8), (mi_p, mi_q), strict=True):
            a = margin(16, rho)
            result = construct_additive(a, a, target, "first", TOLERANCES)
            variance = float(influence_variance(result.probability))
            _, sensitivity_variance = _variance_influence_component_df(
                result.probability, np.asarray(variance))
            sensitivity_variance = float(sensitivity_variance)
            if not (np.isfinite(variance) and variance > 0
                    and np.isfinite(sensitivity_variance) and sensitivity_variance > 0):
                raise ValueError("Population first-order assumptions fail.")
            population.update({
                f"strength_{side}": result.strength,
                f"achieved_mi_{side}": result.achieved_mi,
                f"endpoint_mi_{side}": result.endpoint_mi,
                f"variance_{side}": variance,
                f"variance_sensitivity_variance_{side}": sensitivity_variance,
                f"minimum_probability_{side}": float(result.probability.min()),
                f"normalization_error_{side}": result.normalization_error,
                f"row_margin_error_{side}": result.row_margin_error,
                f"column_margin_error_{side}": result.column_margin_error,
                f"margin_{side}": a.tolist(),
            })
            pair.append(result.probability)
        populations.append(population)
        arrays[pair_id] = tuple(pair)
        for n in SAMPLE_SIZES:
            configurations.append({
                "configuration_id": "setting_" + digest([pair_id, n, n])[:16],
                "pair_id": pair_id, **spec, "n_p": n, "n_q": n,
                "delta": round(mi_p-mi_q, 12), "replicates": REPLICATES,
            })
    return (sorted(configurations, key=lambda c: c["configuration_id"]),
            sorted(populations, key=lambda p: p["pair_id"]), arrays)


def extension_fingerprint():
    return digest({"runner": file_hash(Path(__file__)),
                   "sampling_runner": file_hash(Path(__file__).with_name("run_focused_study.py")),
                   "base_identity_check": file_hash(Path(__file__).with_name("run_unequal_sample_check.py")),
                   "audit": file_hash(Path(__file__).with_name("audit_focused_study.py"))})


def audit_check(output: Path):
    identity = json.loads((output / "study_identity.json").read_text())
    configs, populations, arrays = build_construction_design()
    if (identity["source"] != source_fingerprint()
            or identity["extension_source"] != extension_fingerprint()
            or identity["design_digest"] != digest([configs, populations])
            or identity["phase"] != "full" or identity["count"] != REPLICATES):
        raise AssertionError("Construction protocol, source or phase differs from the run.")
    saved = pd.read_csv(output / "configuration_manifest.csv").to_dict("records")
    if saved != configs or json.loads((output / "population_definitions.json").read_text()) != populations:
        raise AssertionError("Saved construction design differs from the four planned settings.")
    with np.load(output / "populations.npz", allow_pickle=False) as stored:
        expected_keys = {f"{key}_{side}" for key in arrays for side in "pq"}
        if set(stored.files) != expected_keys:
            raise AssertionError("Unexpected population arrays.")
        for key, pair in arrays.items():
            for side, probability in zip("pq", pair, strict=True):
                np.testing.assert_array_equal(stored[f"{key}_{side}"], probability)
    for config in configs:
        directory = output / "records" / config["configuration_id"]
        metadata = json.loads((directory / "identity.json").read_text())
        expected = {"configuration": config, "count": REPLICATES, "phase": "full",
                    "fingerprint": digest(identity), "chunk_size": CHUNK_SIZE}
        if metadata != expected:
            raise AssertionError("Checkpoint provenance differs from its run identity.")
        audit_records(config, load_records(directory, REPLICATES))
    audit(output, expected_settings=4, expected_pairs=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "pilot", "full", "audit"))
    parser.add_argument("--base-results", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-size", type=int, default=250)
    args = parser.parse_args()
    if args.batch_size <= 0:
        parser.error("Batch size must be positive.")
    # Neither this extension nor its pilot may overwrite the original records.
    if args.output.resolve() == args.base_results.resolve():
        parser.error("The supporting check must not overwrite the focused study.")
    configs, populations, arrays = build_construction_design()
    if args.mode == "audit":
        audit_check(args.output)
        return
    phase = "pilot" if args.mode == "pilot" else "full"
    count = 200 if phase == "pilot" else REPLICATES
    output = args.output / "pilot" if phase == "pilot" else args.output
    base_identity = checked_base_identity(args.base_results)
    identity = {
        "schema": SCHEMA_VERSION, "master_seed": MASTER_SEED,
        "source": source_fingerprint(), "extension_source": extension_fingerprint(),
        "numpy": np.__version__, "scipy": scipy.__version__,
        "python": platform.python_version(), "machine": platform.machine(),
        "platform": platform.platform(), "phase": phase, "count": count,
        "chunk_size": CHUNK_SIZE, "design_digest": digest([configs, populations]),
        "alpha": ALPHA, "comparison_source_identity": base_identity,
    }
    output.mkdir(parents=True, exist_ok=True)
    identity_path = output / "study_identity.json"
    if identity_path.exists() and json.loads(identity_path.read_text()) != identity:
        raise RuntimeError("Construction run identity changed; use a separate output directory.")
    atomic_json(identity_path, identity)
    atomic_json(output / "population_definitions.json", populations)
    pd.DataFrame(configs).to_csv(output / "configuration_manifest.csv", index=False)
    with (output / "populations.npz").open("wb") as handle:
        np.savez_compressed(handle, **{
            f"{key}_{side}": probability for key, pair in arrays.items()
            for side, probability in zip("pq", pair, strict=True)})
    print(f"Large-table construction check: 4 settings, 2 new pairs; {phase}.", flush=True)
    if args.mode == "preflight":
        return
    start = perf_counter()
    completion = []
    for config in configs:
        row = run_configuration((config, *arrays[config["pair_id"]], output / "records",
                                 count, args.batch_size, phase, digest(identity)))
        completion.append(row)
        print(f"Completed n={config['n_p']}, MI(Q)={config['mi_q']:.2f} "
              f"in {perf_counter()-start:.1f}s", flush=True)
    pd.DataFrame(completion).to_csv(output / "execution.csv", index=False)
    aggregate(output, configs, populations, count)
    if phase == "full":
        audit_check(output)


if __name__ == "__main__":
    main()
