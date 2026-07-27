#!/usr/bin/env python3
"""Targeted bootstrap calibration for difficult paired null scenarios."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from paired_differential_mi.core import paired_bootstrap_t, paired_mi_tests
from paired_differential_mi.distributions import PairedScenario


def target_scenarios() -> list[PairedScenario]:
    return [
        PairedScenario(
            "balanced_2x2_n50_pair08",
            "challenging",
            2,
            2,
            50,
            "balanced",
            "balanced",
            0.10,
            0.10,
            0.8,
            "ordinal",
            "ordinal",
        ),
        PairedScenario(
            "weak_2x2_n100_pair08",
            "challenging",
            2,
            2,
            100,
            "balanced",
            "strong",
            0.05,
            0.05,
            0.8,
        ),
        PairedScenario(
            "regular_3x3_n150_pair08",
            "regular",
            3,
            3,
            150,
            "balanced",
            "strong",
            0.10,
            0.10,
            0.8,
        ),
        PairedScenario(
            "sparse_3x3_n50_pair08",
            "challenging",
            3,
            3,
            50,
            "strong",
            "strong",
            0.05,
            0.05,
            0.8,
            "ordinal",
            "ordinal",
        ),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tables", type=int, default=500)
    parser.add_argument("--bootstrap-replicates", type=int, default=999)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("PairedDifferentialMI/results/bootstrap_calibration"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if min(args.tables, args.bootstrap_replicates) <= 0:
        raise ValueError("Replicate counts must be positive.")
    rng = np.random.default_rng(args.seed)
    rows: list[dict] = []
    for scenario in target_scenarios():
        _, _, coupling, diagnostics = scenario.materialize()
        cells = scenario.rows * scenario.columns
        tables = rng.multinomial(
            scenario.n, coupling.reshape(-1), size=args.tables
        ).reshape(args.tables, cells, cells)
        for table_index, counts in enumerate(tables):
            analytic = paired_mi_tests(counts, (scenario.rows, scenario.columns))
            bootstrap = paired_bootstrap_t(
                counts,
                (scenario.rows, scenario.columns),
                replicates=args.bootstrap_replicates,
                rng=rng,
            )
            rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "regime": scenario.regime,
                    "table_index": table_index,
                    "true_delta": diagnostics["true_delta"],
                    "wald_p": analytic["paired_wald_normal_p"],
                    "jackknife_p": analytic["paired_jackknife_t_p"],
                    "bootstrap_p": bootstrap.p_value,
                    "bootstrap_seconds": bootstrap.elapsed_seconds,
                    "bootstrap_valid_replicates": bootstrap.valid_replicates,
                }
            )
        print(f"Completed {scenario.scenario_id}", flush=True)

    frame = pd.DataFrame(rows)
    summary = (
        frame.groupby(["scenario_id", "regime"], as_index=False)
        .agg(
            tables=("table_index", "size"),
            wald_fpr_05=("wald_p", lambda values: np.mean(values <= 0.05)),
            jackknife_fpr_05=(
                "jackknife_p",
                lambda values: np.mean(values <= 0.05),
            ),
            bootstrap_fpr_05=(
                "bootstrap_p",
                lambda values: np.mean(values <= 0.05),
            ),
            bootstrap_valid_mean=("bootstrap_valid_replicates", "mean"),
            bootstrap_median_ms=(
                "bootstrap_seconds",
                lambda values: 1000 * np.median(values),
            ),
        )
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output_dir / "replicates.csv.gz", index=False)
    summary.to_csv(args.output_dir / "summary.csv", index=False)
    (args.output_dir / "REPORT.md").write_text(
        "# Targeted Paired Bootstrap Calibration\n\n"
        f"Each scenario uses {args.tables} null tables and "
        f"{args.bootstrap_replicates} bootstrap replicates per table.\n\n"
        "```text\n"
        + summary.to_string(index=False)
        + "\n```\n"
    )


if __name__ == "__main__":
    main()
