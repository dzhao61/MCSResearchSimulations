#!/usr/bin/env python3
"""Run the pre-specified paired differential-MI feasibility pilot."""

from __future__ import annotations

import argparse
import platform
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

from paired_differential_mi.distributions import pilot_scenarios
from paired_differential_mi.validation import (
    run_bootstrap_anchors,
    run_scenario,
    save_results,
    summarize,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "pilot"), default="pilot")
    parser.add_argument("--null-replicates", type=int, default=3000)
    parser.add_argument("--power-replicates", type=int, default=2000)
    parser.add_argument("--bootstrap-tables", type=int, default=8)
    parser.add_argument("--bootstrap-replicates", type=int, default=999)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("PairedDifferentialMI/results/pilot"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if min(
        args.null_replicates,
        args.power_replicates,
        args.bootstrap_tables,
        args.bootstrap_replicates,
    ) <= 0:
        raise ValueError("All replicate counts must be positive.")
    scenarios = pilot_scenarios(args.profile)
    seed_sequence = np.random.SeedSequence(args.seed)
    child_sequences = seed_sequence.spawn(len(scenarios) + 1)
    replicate_frames: list[pd.DataFrame] = []
    diagnostics: list[dict] = []
    start = perf_counter()

    for index, (scenario, child) in enumerate(
        zip(scenarios, child_sequences[:-1], strict=True), start=1
    ):
        replicates = (
            args.power_replicates
            if scenario.regime == "power"
            else args.null_replicates
        )
        seed = int(child.generate_state(1)[0])
        print(
            f"[{index:02d}/{len(scenarios):02d}] "
            f"{scenario.scenario_id}: {replicates} replicates",
            flush=True,
        )
        frame, scenario_diagnostics = run_scenario(
            scenario, replicates=replicates, seed=seed
        )
        replicate_frames.append(frame)
        diagnostics.append(scenario_diagnostics)

    all_replicates = pd.concat(replicate_frames, ignore_index=True)
    scenario_frame = pd.DataFrame(diagnostics)
    summary = summarize(all_replicates, scenario_frame)

    anchor_ids = {
        "regular_2x2_bal_n50_positive",
        "regular_2x2_weak_n100_negative",
        "regular_3x3_weak_n150_positive",
        "sparse_3x3_strong_n50_positive",
        "sparse_5x5_strong_n150_positive",
        "boundary_2x2_weak_n250",
    }
    anchors = [
        scenario for scenario in scenarios if scenario.scenario_id in anchor_ids
    ]
    bootstrap = run_bootstrap_anchors(
        anchors,
        tables_per_scenario=args.bootstrap_tables,
        bootstrap_replicates=args.bootstrap_replicates,
        seed=int(child_sequences[-1].generate_state(1)[0]),
    )
    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "null_replicates": args.null_replicates,
        "power_replicates": args.power_replicates,
        "bootstrap_tables_per_scenario": args.bootstrap_tables,
        "bootstrap_replicates": args.bootstrap_replicates,
        "scenarios": len(scenarios),
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    save_results(
        args.output_dir,
        all_replicates,
        scenario_frame,
        summary,
        bootstrap,
        metadata,
    )
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
