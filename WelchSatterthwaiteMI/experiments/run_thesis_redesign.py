#!/usr/bin/env python3
"""Preflight, smoke-test and run the redesigned thesis experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter_ns, perf_counter
from typing import Any

import numpy as np
import pandas as pd
import scipy

from thesis_redesign_core import (
    ROOT,
    build_manifests,
    hash_payload,
    simulate_configuration,
    smoke_configuration_ids,
    stable_seed,
)

PROTOCOL = Path(__file__).with_name("THESIS_REDESIGN_PROTOCOL.json")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_revision() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT.parent, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def atomic_json(path: Path, payload: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=PROTOCOL)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight-only", action="store_true")
    mode.add_argument("--smoke", action="store_true")
    mode.add_argument("--full", action="store_true")
    mode.add_argument("--report-only", action="store_true")
    mode.add_argument("--timing-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--no-report", action="store_true")
    return parser.parse_args()


def save_preflight(
    output: Path,
    protocol_path: Path,
    protocol: dict[str, Any],
    display: pd.DataFrame,
    configurations: pd.DataFrame,
    populations: pd.DataFrame,
    failures: pd.DataFrame,
    profile: str,
) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    display.to_csv(output / "display_manifest.csv", index=False)
    configurations.to_csv(output / "configuration_manifest.csv", index=False)
    populations.to_csv(output / "population_definitions.csv", index=False)
    failures.to_csv(output / "infeasible_configurations.csv", index=False)
    (output / "protocol.json").write_text(protocol_path.read_text(encoding="utf-8"), encoding="utf-8")
    summary = {
        "profile": profile,
        "protocol_sha256": sha256(protocol_path),
        "display_slots": int(len(display)),
        "unique_configurations": int(len(configurations)),
        "population_pairs": int(len(populations)),
        "infeasible_display_slots": int(len(failures)),
        "table_pairs": int(configurations["replicates"].sum()) if not configurations.empty else 0,
        "method_evaluations": int(2 * configurations["replicates"].sum()) if not configurations.empty else 0,
        "figure_count": int(display["figure_key"].nunique()),
    }
    atomic_json(output / "preflight_summary.json", summary)
    return summary


def task_for(
    row: dict[str, Any],
    arrays: dict[str, tuple[np.ndarray, np.ndarray]],
    protocol: dict[str, Any],
    batch_size: int,
) -> dict[str, Any]:
    p, q = arrays[row["pair_id"]]
    return {
        "configuration": row,
        "probability_p": p,
        "probability_q": q,
        "alpha": float(protocol["alpha"]),
        "batch_size": batch_size,
    }


def checkpoint_fingerprint(row: dict[str, Any]) -> str:
    fields = {
        key: row[key]
        for key in ["configuration_id", "pair_id", "n_p", "n_q", "replicates", "simulation_seed"]
    }
    return hash_payload(fields, length=64)


def load_checkpoint(path: Path, row: dict[str, Any]) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload["configuration_id"] != row["configuration_id"]:
        raise RuntimeError(f"Checkpoint identity mismatch in {path}")
    if payload.get("configuration_fingerprint") != checkpoint_fingerprint(row):
        raise RuntimeError(f"Checkpoint configuration changed: {path}")
    return payload["result"]


def save_checkpoint(path: Path, row: dict[str, Any], result: dict[str, Any]) -> None:
    atomic_json(
        path,
        {"configuration_id": row["configuration_id"],
         "configuration_fingerprint": checkpoint_fingerprint(row), "result": result},
    )


def aggregate_checkpoints(output: Path, configurations: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    cell_rows: list[dict[str, Any]] = []
    paired_rows: list[dict[str, Any]] = []
    checkpoints = output / "checkpoints"
    for row in configurations.to_dict("records"):
        configuration_id = row["configuration_id"]
        result = load_checkpoint(checkpoints / f"{configuration_id}.json", row)
        cell_rows.extend(result["cell_rows"])
        paired_rows.extend(result["paired_rows"])
    cells = pd.DataFrame(cell_rows).sort_values(["configuration_id", "method"]).reset_index(drop=True)
    paired = pd.DataFrame(paired_rows).sort_values("configuration_id").reset_index(drop=True)
    cells.to_csv(output / "cell_results.csv", index=False)
    paired.to_csv(output / "paired_method_results.csv", index=False)
    return cells, paired


def verify_results(
    configurations: pd.DataFrame,
    populations: pd.DataFrame,
    cells: pd.DataFrame,
    paired: pd.DataFrame,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    expected_methods = set(protocol["methods"])
    method_counts = cells.groupby("configuration_id")["method"].agg(lambda values: set(values))
    checks = {
        "all_configurations_present": set(cells["configuration_id"]) == set(configurations["configuration_id"]),
        "exactly_two_methods": bool(method_counts.map(lambda value: value == expected_methods).all()),
        "unique_method_rows": not cells.duplicated(["configuration_id", "method"]).any(),
        "one_paired_row_per_configuration": len(paired) == len(configurations) and paired["configuration_id"].is_unique,
        "replicate_denominators": bool((cells["rejections"] <= cells["valid_replicates"]).all()),
        "rates_recalculate": bool(np.allclose(cells["unconditional_rejection_rate"], cells["rejections"] / cells["replicates"])),
        "valid_rates_recalculate": bool(np.allclose(cells["valid_rate"], cells["valid_replicates"] / cells["replicates"])),
        "population_mi": bool(
            np.all(np.abs(populations["achieved_mi_p"] - populations["target_mi_p"]) <= 1e-12 + 1e-8 * populations["target_mi_p"])
            and np.all(np.abs(populations["achieved_mi_q"] - populations["target_mi_q"]) <= 1e-12 + 1e-8 * populations["target_mi_q"])
        ),
        "strictly_positive_populations": bool((populations[["minimum_probability_p", "minimum_probability_q"]] > 0).all().all()),
        "margins_and_normalization": bool(
            (populations[["normalization_error_p", "normalization_error_q", "row_margin_error_p", "row_margin_error_q", "column_margin_error_p", "column_margin_error_q"]] <= 1e-12).all().all()
        ),
        "expanded_rejection_subset": int(paired["only_method_a_rejects"].sum()) == 0,
        "paired_counts_sum": bool(
            ((paired["both_reject"] + paired["neither_rejects"] + paired["only_method_a_rejects"] + paired["only_method_b_rejects"]) == paired["replicates"]).all()
        ),
        "n1_explicitly_invalid": bool((cells.loc[cells["n_p"].eq(1), "valid_rate"] == 0).all()),
    }
    return {"all_pass": all(checks.values()), "checks": checks}


def run_simulation(
    output: Path,
    configurations: pd.DataFrame,
    arrays: dict[str, tuple[np.ndarray, np.ndarray]],
    protocol: dict[str, Any],
    workers: int,
    batch_size: int,
) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    checkpoints = output / "checkpoints"
    checkpoints.mkdir(parents=True, exist_ok=True)
    pending = []
    for row in configurations.to_dict("records"):
        path = checkpoints / f"{row['configuration_id']}.json"
        if path.exists():
            load_checkpoint(path, row)
        else:
            pending.append(row)
    print(
        f"Resume check: {len(configurations)-len(pending):,} complete; "
        f"{len(pending):,} configurations pending.", flush=True,
    )
    start = perf_counter()
    completed = len(configurations) - len(pending)
    if workers == 1:
        for row in pending:
            result = simulate_configuration(task_for(row, arrays, protocol, batch_size))
            save_checkpoint(checkpoints / f"{row['configuration_id']}.json", row, result)
            completed += 1
            if completed % 25 == 0 or completed == len(configurations):
                pairs = int(configurations.iloc[:completed]["replicates"].sum())
                print(f"Completed {completed:,}/{len(configurations):,} configurations ({pairs:,} requested pairs indexed)", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(simulate_configuration, task_for(row, arrays, protocol, batch_size)): row
                for row in pending
            }
            for future in as_completed(futures):
                row = futures[future]
                result = future.result()
                save_checkpoint(checkpoints / f"{row['configuration_id']}.json", row, result)
                completed += 1
                if completed % 25 == 0 or completed == len(configurations):
                    print(f"Completed {completed:,}/{len(configurations):,} configurations", flush=True)
    elapsed = perf_counter() - start
    cells, paired = aggregate_checkpoints(output, configurations)
    return cells, paired, elapsed


def runtime_experiment(
    output: Path,
    protocol: dict[str, Any],
    display: pd.DataFrame,
    arrays: dict[str, tuple[np.ndarray, np.ndarray]],
) -> pd.DataFrame:
    from welch_differential_mi import differential_mi_pvalues

    design = protocol["runtime"]
    selected = display[
        display["section"].isin(["main", "rectangular"])
        & display["shape"].isin(design["shapes"])
        & display["profile"].isin(design["profiles"])
        & display["n_p"].isin(design["sample_sizes"])
        & display["n_q"].isin(design["sample_sizes"])
        & display["mi_difference"].isin(design["mi_differences"])
    ].drop_duplicates(["pair_id", "n_p", "n_q"])
    records: list[dict[str, Any]] = []
    for _, row in selected.iterrows():
        p, q = arrays[row["pair_id"]]
        key = f"timing:{row['pair_id']}:{row['n_p']}:{row['n_q']}"
        rng = np.random.default_rng(stable_seed(protocol["timing_seed"], key))
        count = int(design["inputs_per_regime"])
        tables_p = rng.multinomial(int(row["n_p"]), p.ravel(), size=count).reshape(count, *p.shape)
        tables_q = rng.multinomial(int(row["n_q"]), q.ravel(), size=count).reshape(count, *q.shape)

        def call(method: str, index: int) -> bool:
            try:
                values = differential_mi_pvalues(
                    tables_p[index], tables_q[index], include_simple=False,
                    include_expanded=method == "expanded_welch",
                    include_unbiased_sensitivity=False,
                )
                key_valid = "expanded_valid" if method == "expanded_welch" else "base_valid"
                return bool(values[key_valid])
            except ValueError:
                return False

        for method in protocol["methods"]:
            for index in range(min(int(design["warmup_calls"]), count)):
                call(method, index)
        timings = {method: np.empty((int(design["timed_passes"]), count)) for method in protocol["methods"]}
        validity = {method: np.zeros(count, dtype=bool) for method in protocol["methods"]}
        methods = list(protocol["methods"])
        for pass_index in range(int(design["timed_passes"])):
            order = methods if pass_index % 2 == 0 else list(reversed(methods))
            for method in order:
                for index in range(count):
                    start = perf_counter_ns()
                    valid = call(method, index)
                    timings[method][pass_index, index] = perf_counter_ns() - start
                    validity[method][index] = valid
        medians = {method: np.median(timings[method], axis=0) / 1000.0 for method in methods}
        for index in range(count):
            for method in methods:
                records.append(
                    {
                        "pair_id": row["pair_id"], "shape": row["shape"],
                        "profile": row["profile"], "n_p": int(row["n_p"]),
                        "n_q": int(row["n_q"]), "baseline_mi": row["baseline_mi"],
                        "mi_difference": row["mi_difference"], "input_index": index,
                        "method": method, "median_microseconds": medians[method][index],
                        "valid": bool(validity[method][index]),
                    }
                )
    result = pd.DataFrame(records)
    result.to_csv(output / "runtime_inputs.csv", index=False)
    keys = ["shape", "profile", "n_p", "n_q", "baseline_mi", "mi_difference", "method"]
    summary = result.groupby(keys, as_index=False).agg(
        median_microseconds=("median_microseconds", "median"),
        q1_microseconds=("median_microseconds", lambda x: x.quantile(0.25)),
        q3_microseconds=("median_microseconds", lambda x: x.quantile(0.75)),
        valid_rate=("valid", "mean"),
    )
    pivot = summary.pivot(index=keys[:-1], columns="method", values="median_microseconds")
    ratios = (pivot["expanded_welch"] / pivot["normal_wald"]).rename("expanded_to_wald_ratio").reset_index()
    summary = summary.merge(ratios, on=keys[:-1], how="left")
    summary.to_csv(output / "runtime_summary.csv", index=False)
    return summary


def call_report(protocol_path: Path, output: Path) -> None:
    from report_thesis_redesign import build_report
    build_report(protocol_path, output)


def main() -> None:
    args = parse_args()
    if args.workers < 1:
        raise ValueError("Workers must be positive.")
    protocol_path = args.protocol.resolve()
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    profile = "smoke" if args.smoke else "full"
    default = (
        ROOT / "results/thesis_redesign_smoke"
        if args.smoke
        else protocol_path.parent / protocol["output_directory"]
    )
    output = (args.output_dir or default).resolve()
    if args.report_only:
        call_report(protocol_path, output)
        return

    started = utc_now()
    display, configurations, populations, arrays = build_manifests(protocol)
    failures = pd.DataFrame()
    if configurations.empty:
        _, _, failures, _ = build_manifests(protocol)
    if args.smoke:
        selected = smoke_configuration_ids(display)
        configurations = configurations[configurations["configuration_id"].isin(selected)].copy()
        configurations["replicates"] = int(protocol["smoke_replicates"])
        configurations["simulation_seed"] = configurations["configuration_id"].map(
            lambda value: stable_seed(protocol["master_seed"] + 1, "smoke:" + value)
        )
        display = display[display["configuration_id"].isin(selected)].copy()
    summary = save_preflight(
        output, protocol_path, protocol, display, configurations, populations, failures, profile
    )
    if summary["infeasible_display_slots"]:
        raise RuntimeError("Population preflight failed; no sampling was run.")
    print(
        f"Preflight passed: {summary['unique_configurations']:,} unique configurations, "
        f"{summary['population_pairs']:,} population pairs, "
        f"{summary['table_pairs']:,} sampled pairs planned.", flush=True,
    )
    if args.preflight_only or (not args.smoke and not args.full and not args.timing_only):
        return
    if args.full and protocol["status"] != "frozen_for_confirmatory_run":
        raise RuntimeError("Full run requires protocol status frozen_for_confirmatory_run.")

    batch_size = args.batch_size or int(protocol["batch_size"])
    cells = paired = None
    elapsed = 0.0
    if not args.timing_only:
        cells, paired, elapsed = run_simulation(
            output, configurations, arrays, protocol, args.workers, batch_size
        )
        verification = verify_results(configurations, populations, cells, paired, protocol)
        atomic_json(output / "verification.json", verification)
        if not verification["all_pass"]:
            raise RuntimeError("One or more simulation verification checks failed.")
        print("Simulation verification passed.", flush=True)
    timing_summary = None
    if args.full or args.timing_only:
        timing_summary = runtime_experiment(output, protocol, display, arrays)
        print(f"Runtime experiment completed: {len(timing_summary):,} summary rows.", flush=True)
    metadata = {
        **summary, "status": "complete", "started_at_utc": started,
        "finished_at_utc": utc_now(), "simulation_elapsed_seconds_this_invocation": elapsed,
        "workers": args.workers, "batch_size": batch_size, "git_revision": git_revision(),
        "python_version": platform.python_version(), "numpy_version": np.__version__,
        "pandas_version": pd.__version__, "scipy_version": scipy.__version__,
        "platform": platform.platform(),
        "input_sha256": {
            str(path.relative_to(ROOT.parent)): sha256(path)
            for path in [protocol_path, Path(__file__), Path(__file__).with_name("thesis_redesign_core.py"),
                         ROOT / "src/welch_differential_mi/welch.py",
                         ROOT.parent / "DifferentialMI/src/differential_mi/statistics.py",
                         ROOT.parent / "DifferentialMI/src/differential_mi/distributions.py"]
        },
    }
    atomic_json(output / "run_metadata.json", metadata)
    if not args.no_report:
        call_report(protocol_path, output)
        print(f"Wrote report from saved outputs in {output}.", flush=True)


if __name__ == "__main__":
    main()
