"""Run the full 120-setting nominal-power grid at MI 0.02 versus 0.03."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import platform
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

from focused_study_core import (
    ROOT, PROFILES, SAMPLE_SIZES, SIZES, construct_copying, digest,
    evaluate_tables, summarize,
)
from thesis_redesign_core import margin
from redesign_study import independent_values
from run_focused_study import audit_records

OUTPUT = ROOT / "results/fixed_gap_power_2026-11-01"
MASTER_SEED = 20261101
REPLICATES = 100000
CHUNK = 10000
FIELDS = (
    "delta_corrected", "standard_error", "statistic", "squared_standard_error",
    "normal_p_value", "expanded_welch_p_value", "expanded_welch_degrees_of_freedom",
    "base_valid", "expanded_valid", "influence_variance_p", "influence_variance_q",
    "plugin_mi_p", "plugin_mi_q", "corrected_mi_p", "corrected_mi_q",
    "empty_cells_p", "empty_cells_q", "empty_rows_p", "empty_rows_q",
    "empty_columns_p", "empty_columns_q", "normal_invalid_reasons",
    "expanded_invalid_reasons",
)


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    tmp.replace(path)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint():
    paths = [Path(__file__), Path(__file__).with_name("focused_study_core.py"),
             Path(__file__).with_name("run_focused_study.py"),
             Path(__file__).with_name("redesign_study.py"),
             ROOT / "src/welch_differential_mi/welch.py",
             ROOT.parent / "DifferentialMI/src/differential_mi/statistics.py"]
    return digest({str(p.relative_to(ROOT.parent)): sha(p) for p in paths})


def seed_for(config_id, chunk, side):
    return int(digest([MASTER_SEED, "fixed_gap_power_evaluation", config_id, chunk, side])[:16], 16)


def build_design():
    configs, populations, arrays = [], {}, {}
    for k in SIZES:
        for profile, dominant in PROFILES.items():
            spec = dict(k=k, profile=profile, mi_p=.02, mi_q=.03, construction="copying")
            pair_id = "pair_" + digest(spec)[:16]
            population = {"pair_id": pair_id, **spec}
            tables = []
            for side, rho, target in zip("pq", dominant, (.02, .03), strict=True):
                a = margin(k, rho)
                result = construct_copying(a, target)
                from differential_mi.statistics import influence_variance
                population.update({f"variance_{side}": float(influence_variance(result.probability)),
                    f"achieved_mi_{side}": result.achieved_mi, f"strength_{side}": result.strength,
                    f"endpoint_mi_{side}": result.endpoint_mi,
                    f"minimum_probability_{side}": float(result.probability.min()),
                    f"normalization_error_{side}": result.normalization_error,
                    f"row_margin_error_{side}": result.row_margin_error,
                    f"column_margin_error_{side}": result.column_margin_error,
                    f"margin_{side}": a.tolist(), f"probability_{side}": result.probability.tolist()})
                tables.append(result.probability)
            populations[pair_id] = population
            arrays[pair_id] = tuple(tables)
            for n in SAMPLE_SIZES:
                config_id = "setting_" + digest([pair_id, n, n])[:16]
                configs.append(dict(configuration_id=config_id, pair_id=pair_id, **spec,
                    n_p=n, n_q=n, delta=-.01, replicates=REPLICATES))
    assert len(configs) == 120 and len(populations) == 12
    assert len({c["configuration_id"] for c in configs}) == 120
    return configs, populations, arrays


def check_scalar(cp, cq, records):
    for i in range(min(8, len(cp))):
        parts, delta, se, stat, _ = independent_values(cp[i], cq[i], 1.)
        for field, expected in [("delta_corrected", delta), ("standard_error", se), ("statistic", stat)]:
            np.testing.assert_allclose(records[field][i], expected, atol=1e-11, rtol=2e-10, equal_nan=True)
        for side, part in zip("pq", parts, strict=True):
            for name, value in [("influence_variance_", part[1]),
                                ("variance_influence_variance_", part[2]),
                                ("expanded_component_degrees_of_freedom_", part[3])]:
                np.testing.assert_allclose(records[name + side][i], value,
                                           atol=2e-10, rtol=2e-9, equal_nan=True)
    return min(8, len(cp))


def run_setting(task):
    output, config, p, q, count, batch, fp = task
    directory = Path(output) / "evaluation" / config["configuration_id"]
    directory.mkdir(parents=True, exist_ok=True)
    identity = dict(configuration=config, count=count, fingerprint=fp,
                    master_seed=MASTER_SEED, chunk_size=CHUNK)
    identity_path = directory / "identity.json"
    if identity_path.exists() and json.loads(identity_path.read_text()) != identity:
        raise RuntimeError(f"Incompatible checkpoint: {directory}")
    atomic_json(identity_path, identity)
    started = perf_counter()
    for index, offset in enumerate(range(0, count, CHUNK)):
        path = directory / f"chunk_{index:03d}.npz"
        meta_path = path.with_suffix(".json")
        size = min(CHUNK, count-offset)
        if path.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text())
            if meta["sha256"] != sha(path) or meta["count"] != size:
                raise RuntimeError(f"Corrupt checkpoint: {path}")
            continue
        rp = np.random.default_rng(seed_for(config["configuration_id"], index, "p"))
        rq = np.random.default_rng(seed_for(config["configuration_id"], index, "q"))
        parts, scalar_checks = {}, 0
        for start in range(0, size, batch):
            b = min(batch, size-start)
            cp = rp.multinomial(config["n_p"], p.ravel(), size=b).reshape(b, *p.shape)
            cq = rq.multinomial(config["n_q"], q.ravel(), size=b).reshape(b, *q.shape)
            records = evaluate_tables(cp, cq)
            audit_records(config, records)
            if index == 0 and start == 0:
                scalar_checks = check_scalar(cp, cq, records)
            for field in FIELDS:
                parts.setdefault(field, []).append(records[field])
        tmp = path.with_suffix(".tmp")
        with tmp.open("wb") as handle:
            np.savez_compressed(handle, **{key: np.concatenate(value) for key, value in parts.items()})
        tmp.replace(path)
        atomic_json(meta_path, dict(sha256=sha(path), count=size, scalar_checks=scalar_checks))
    return dict(configuration_id=config["configuration_id"], seconds=perf_counter()-started)


def load_records(output, config, count):
    directory = Path(output) / "evaluation" / config["configuration_id"]
    parts, scalar_checks = {}, 0
    for index, offset in enumerate(range(0, count, CHUNK)):
        path = directory / f"chunk_{index:03d}.npz"
        meta = json.loads(path.with_suffix(".json").read_text())
        assert meta["sha256"] == sha(path) and meta["count"] == min(CHUNK, count-offset)
        scalar_checks += meta["scalar_checks"]
        with np.load(path, allow_pickle=False) as data:
            assert set(data.files) == set(FIELDS)
            for key in data.files:
                assert data[key].shape == (meta["count"],)
                parts.setdefault(key, []).append(data[key])
    return {key: np.concatenate(value) for key, value in parts.items()}, scalar_checks


def aggregate(output, configs, populations, count):
    methods, paired, diagnostics = [], [], []
    scalar_checks = 0
    for c in configs:
        r, checked = load_records(output, c, count)
        scalar_checks += checked
        m, p, d = summarize(c, populations[c["pair_id"]], r)
        w = r["base_valid"] & (r["normal_p_value"] <= .05)
        e = r["expanded_valid"] & (r["expanded_welch_p_value"] <= .05)
        for name, reject in [("wald", w), ("expanded", e)]:
            d[f"{name}_positive_rejections"] = int((reject & (r["statistic"] > 0)).sum())
            d[f"{name}_negative_rejections"] = int((reject & (r["statistic"] < 0)).sum())
        metadata = {k: c[k] for k in ["configuration_id", "k", "profile", "n_p", "n_q", "mi_p", "mi_q"]}
        methods.extend({**metadata, **row} for row in m)
        paired.extend({**metadata, **row} for row in p)
        diagnostics.append({**metadata, **d})
    rates = pd.DataFrame(methods)
    rates.to_csv(output / "rates.csv", index=False)
    pd.DataFrame(paired).to_csv(output / "paired.csv", index=False)
    pd.DataFrame(diagnostics).to_csv(output / "diagnostics.csv", index=False)
    a = rates[rates.denominator.eq("all")]
    assert len(a) == 2*len(configs) and a.replicates.eq(count).all()
    np.testing.assert_allclose(a.rejection_rate, a.rejections/a.replicates)
    assert scalar_checks == 8*len(configs)
    audit = dict(passed=True, configurations=len(configs), pairs=len(configs)*count,
                 independently_reconstructed_pairs=scalar_checks,
                 checks=["population MI, positive cells and fixed margins", "complete fixed grid",
                         "checkpoint hashes and record dimensions", "scalar probability formulas",
                         "variance and corrected-difference identities", "validity definitions",
                         "Expanded Welch rejection/validity subsets", "all-repetition denominators"])
    atomic_json(output / "audit.json", audit)
    print(json.dumps(audit), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--mode", choices=["preflight", "smoke", "full", "summarize"], default="preflight")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--batch", type=int, default=500)
    args = parser.parse_args()
    configs, populations, arrays = build_design()
    if args.mode == "smoke":
        configs = [c for c in configs if c["n_p"] in (10, 1000, 50000)]
    count = 200 if args.mode == "smoke" else REPLICATES
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    fp = fingerprint()
    identity = dict(master_seed=MASTER_SEED, count=count, configurations=configs,
                    source_fingerprint=fp, alpha=.05, mode="smoke" if args.mode == "smoke" else "full")
    meta_path = output / "manifest.json"
    if meta_path.exists() and json.loads(meta_path.read_text()) != identity:
        raise RuntimeError("Output belongs to a different design or source version")
    atomic_json(meta_path, identity)
    atomic_json(output / "populations.json", list(populations.values()))
    pd.DataFrame(configs).to_csv(output / "configurations.csv", index=False)
    atomic_json(output / "environment.json", dict(python=platform.python_version(),
        numpy=np.__version__, scipy=scipy.__version__, pandas=pd.__version__))
    print(f"Preflight: {len(configs)} settings; {len(configs)*count:,} independent table pairs", flush=True)
    if args.mode == "preflight":
        return
    if args.mode != "summarize":
        tasks = [(str(output), c, *arrays[c["pair_id"]], count, args.batch, fp) for c in configs]
        execution = []
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for future in as_completed([pool.submit(run_setting, task) for task in tasks]):
                execution.append(future.result())
                print(f"Completed {len(execution)}/{len(tasks)} settings", flush=True)
        pd.DataFrame(execution).to_csv(output / "execution.csv", index=False)
    aggregate(output, configs, populations, count)


if __name__ == "__main__":
    main()
