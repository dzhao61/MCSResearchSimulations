#!/usr/bin/env python3
"""Map paired-test calibration across sample size and pairing strength."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from paired_differential_mi.distributions import PairedScenario
from paired_differential_mi.validation import run_scenario, summarize


def scenarios() -> list[PairedScenario]:
    result: list[PairedScenario] = []
    designs = (
        ("balanced_2x2", 2, "balanced", "balanced", 0.10, "ordinal", "ordinal"),
        ("weak_2x2", 2, "balanced", "strong", 0.05, "ordinal", "cyclic"),
        ("sparse_3x3", 3, "strong", "strong", 0.05, "ordinal", "ordinal"),
    )
    for design, size, margin_a, margin_b, target, pattern_a, pattern_b in designs:
        for n in (50, 100, 200, 500, 1000):
            for pairing in (0.0, 0.4, 0.8):
                pairing_label = str(pairing).replace(".", "")
                result.append(
                    PairedScenario(
                        scenario_id=f"{design}_n{n}_pair{pairing_label}",
                        regime=design,
                        rows=size,
                        columns=size,
                        n=n,
                        margin_a=margin_a,
                        margin_b=margin_b,
                        target_mi_a=target,
                        target_mi_b=target,
                        pairing=pairing,
                        pattern_a=pattern_a,
                        pattern_b=pattern_b,
                    )
                )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("PairedDifferentialMI/results/operating_boundary"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.replicates <= 0:
        raise ValueError("replicates must be positive.")
    planned = scenarios()
    seeds = np.random.SeedSequence(args.seed).spawn(len(planned))
    frames: list[pd.DataFrame] = []
    diagnostics: list[dict] = []
    for index, (scenario, sequence) in enumerate(
        zip(planned, seeds, strict=True), start=1
    ):
        print(f"[{index:02d}/{len(planned):02d}] {scenario.scenario_id}", flush=True)
        frame, metadata = run_scenario(
            scenario,
            replicates=args.replicates,
            seed=int(sequence.generate_state(1)[0]),
        )
        frames.append(frame)
        diagnostics.append(metadata)

    all_replicates = pd.concat(frames, ignore_index=True)
    scenario_frame = pd.DataFrame(diagnostics)
    summary = summarize(all_replicates, scenario_frame)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_replicates.to_csv(args.output_dir / "replicates.csv.gz", index=False)
    scenario_frame.to_csv(args.output_dir / "scenarios.csv", index=False)
    summary.to_csv(args.output_dir / "summary.csv", index=False)

    columns = [
        "scenario_id",
        "regime",
        "n",
        "population_score_correlation",
        "min_expected_joint",
        "paired_wald_normal_reject_05",
        "paired_jackknife_t_reject_05",
        "unpaired_wald_normal_reject_05",
    ]
    report = [
        "# Pairing and Sample-Size Operating Boundary",
        "",
        f"Each cell uses {args.replicates} repeated null samples.",
        "",
        "```text",
        summary[columns].to_string(index=False),
        "```",
        "",
        "The full numerical output is in `summary.csv`.",
    ]
    (args.output_dir / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
