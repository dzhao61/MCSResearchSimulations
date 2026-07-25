#!/usr/bin/env python3
"""Run the pre-specified randomized regular-case validation."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.random_validation import (
    ANCHOR_POSITIONS,
    DETERMINISTIC_METHODS,
    PERMUTATION_METHODS,
    generate_random_scenarios,
    run_deterministic_scenario,
    run_permutation_anchor,
    scenario_diagnostics,
    strong_null_version,
    summarize_deterministic,
    summarize_permutation,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("smoke", "broad", "anchors", "all", "strong", "followup"),
        default="smoke",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--scenario-seed", type=int, default=2026072501)
    parser.add_argument("--simulation-seed", type=int, default=2026072502)
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--anchor-replicates", type=int)
    parser.add_argument("--permutations", type=int)
    parser.add_argument("--scenario-id", action="append", dest="scenario_ids")
    return parser.parse_args()


def _write_scenarios(scenarios: list, output_dir: Path) -> pd.DataFrame:
    rows = []
    for scenario in scenarios:
        row = scenario_diagnostics(scenario)
        row["probability_p_json"] = json.dumps(scenario.probability_p.tolist())
        row["probability_q_json"] = json.dumps(scenario.probability_q.tolist())
        rows.append(row)
    frame = pd.DataFrame(rows)
    frame.to_csv(output_dir / "random_scenarios.csv", index=False)
    return frame


def _plot_calibration(summary: pd.DataFrame, output_dir: Path) -> None:
    methods = list(DETERMINISTIC_METHODS)
    fig, axes = plt.subplots(1, len(methods), figsize=(16, 5), sharey=True)
    for axis, method in zip(axes, methods):
        rates = summary[f"{method}_fpr_05"]
        colors = np.maximum(
            summary["mean_expected_below_5_p"],
            summary["mean_expected_below_5_q"],
        )
        scatter = axis.scatter(
            summary["rows"] * summary["columns"],
            rates,
            c=colors,
            cmap="viridis",
            s=30,
            alpha=0.85,
        )
        axis.axhline(0.05, color="black", linestyle="--", linewidth=1)
        axis.axhspan(0.035, 0.065, color="grey", alpha=0.12)
        axis.set_xscale("log")
        axis.set_xlabel("Number of cells")
        axis.set_title(method)
    axes[0].set_ylabel("Null rejection rate at alpha=0.05")
    colorbar = fig.colorbar(scatter, ax=axes, shrink=0.85)
    colorbar.set_label("Mean fraction of expected counts below 5")
    fig.suptitle("Randomized equal-MI weak-null calibration")
    fig.subplots_adjust(left=0.07, right=0.91, bottom=0.13, top=0.86, wspace=0.12)
    fig.savefig(output_dir / "randomized_calibration.png", dpi=170)
    plt.close(fig)


def _aggregate_deterministic(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method in DETERMINISTIC_METHODS:
        rates = summary[f"{method}_fpr_05"]
        coverages = summary[f"{method}_coverage_95"]
        rows.append(
            {
                "method": method,
                "scenarios": len(summary),
                "mean_absolute_fpr_error_05": float(np.mean(np.abs(rates - 0.05))),
                "median_absolute_fpr_error_05": float(np.median(np.abs(rates - 0.05))),
                "within_035_065": float(np.mean(rates.between(0.035, 0.065))),
                "minimum_fpr_05": float(rates.min()),
                "maximum_fpr_05": float(rates.max()),
                "mean_coverage_95": float(coverages.mean()),
                "within_coverage_935_965": float(
                    np.mean(coverages.between(0.935, 0.965))
                ),
                "mean_absolute_bias": float(
                    np.mean(np.abs(summary[f"{method}_bias"]))
                ),
            }
        )
    return pd.DataFrame(rows)


def _aggregate_anchors(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method in (*PERMUTATION_METHODS, *DETERMINISTIC_METHODS):
        rates = summary[f"{method}_fpr_05"]
        rows.append(
            {
                "method": method,
                "anchors": len(summary),
                "mean_absolute_fpr_error_05": float(np.mean(np.abs(rates - 0.05))),
                "median_absolute_fpr_error_05": float(np.median(np.abs(rates - 0.05))),
                "within_035_065": float(np.mean(rates.between(0.035, 0.065))),
                "minimum_fpr_05": float(rates.min()),
                "maximum_fpr_05": float(rates.max()),
            }
        )
    return pd.DataFrame(rows)


def _markdown_table(frame: pd.DataFrame) -> list[str]:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        rendered = [
            f"{value:.4f}" if isinstance(value, (float, np.floating)) else str(value)
            for value in values
        ]
        lines.append("| " + " | ".join(rendered) + " |")
    return lines


def _write_report(
    mode: str,
    output_dir: Path,
    deterministic_aggregate: pd.DataFrame | None,
    anchor_aggregate: pd.DataFrame | None,
    deterministic_summary: pd.DataFrame | None,
    anchor_summary: pd.DataFrame | None,
) -> None:
    lines = [
        "# Randomized Regular-Case Validation",
        "",
        f"Run mode: `{mode}`.",
        "",
        "Near-independence was excluded by design. Every population MI target was",
        "at least 0.03 nats, and each weak-null pair had equal population MI.",
        "",
    ]
    if deterministic_aggregate is not None:
        lines.extend(["## Deterministic Screen", ""])
        lines.extend(_markdown_table(deterministic_aggregate))
        lines.extend(
            [
                "",
                f"Mean vectorized deterministic runtime: "
                f"{deterministic_summary['deterministic_microseconds_per_pair'].mean():.2f} "
                "microseconds per table pair.",
                "",
            ]
        )
    if anchor_aggregate is not None:
        lines.extend(["## Pre-Selected Permutation Anchors", ""])
        lines.extend(_markdown_table(anchor_aggregate))
        lines.extend(
            [
                "",
                f"Mean full permutation runtime: "
                f"{anchor_summary['mean_permutation_ms'].mean():.3f} ms per table pair.",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation",
            "",
            "The jackknife should be retained only if it improves materially over the",
            "classical analytic correction. Raw permutation is included to test the",
            "weak-null failure predicted by theory, not as the expected winner.",
            "",
            "See the CSV files for scenario-level Wilson intervals, diagnostics, and",
            "the complete saved probability tables.",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.mode == "followup" and not args.scenario_ids:
        raise ValueError("Follow-up mode requires at least one --scenario-id.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = generate_random_scenarios(args.scenario_seed)
    if args.mode == "strong":
        scenarios = [strong_null_version(scenario) for scenario in scenarios]
    if args.scenario_ids:
        wanted = set(args.scenario_ids)
        scenarios = [scenario for scenario in scenarios if scenario.scenario_id in wanted]
        missing = wanted - {scenario.scenario_id for scenario in scenarios}
        if missing:
            raise ValueError(f"Unknown scenario IDs: {sorted(missing)}")
    if args.mode == "smoke":
        scenarios = scenarios[:8]
    scenario_frame = _write_scenarios(scenarios, args.output_dir)

    run_broad = args.mode in {"smoke", "broad", "all", "strong", "followup"}
    run_anchors = args.mode in {"smoke", "anchors", "all", "followup"}
    deterministic_replicates = args.replicates or (
        200 if args.mode == "smoke" else 10_000 if args.mode == "followup" else 3_000
    )
    anchor_replicates = args.anchor_replicates or (
        30 if args.mode == "smoke" else 3_000 if args.mode == "followup" else 1_000
    )
    permutations = args.permutations or (99 if args.mode == "smoke" else 999)

    seed_sequence = np.random.SeedSequence(args.simulation_seed)
    child_seeds = iter(
        int(child.generate_state(1)[0])
        for child in seed_sequence.spawn(2 * len(scenarios))
    )

    deterministic_summary = None
    deterministic_aggregate = None
    if run_broad:
        frames = []
        for index, scenario in enumerate(scenarios, 1):
            print(
                f"[deterministic {index}/{len(scenarios)}] {scenario.scenario_id}",
                flush=True,
            )
            frames.append(
                run_deterministic_scenario(
                    scenario,
                    replicates=deterministic_replicates,
                    seed=next(child_seeds),
                )
            )
        deterministic_replicates_frame = pd.concat(frames, ignore_index=True)
        deterministic_replicates_frame.to_csv(
            args.output_dir / "deterministic_replicates.csv.gz",
            index=False,
            compression="gzip",
        )
        deterministic_summary = summarize_deterministic(
            deterministic_replicates_frame
        )
        deterministic_summary = scenario_frame.merge(
            deterministic_summary, on="scenario_id"
        )
        deterministic_summary.to_csv(
            args.output_dir / "deterministic_summary.csv", index=False
        )
        deterministic_aggregate = _aggregate_deterministic(deterministic_summary)
        deterministic_aggregate.to_csv(
            args.output_dir / "deterministic_aggregate.csv", index=False
        )
        _plot_calibration(deterministic_summary, args.output_dir)

    anchor_summary = None
    anchor_aggregate = None
    if run_anchors:
        anchors = [
            scenario
            for scenario in scenarios
            if (scenario.shape_index, scenario.design_index) in ANCHOR_POSITIONS
        ]
        if args.mode == "followup":
            anchors = scenarios
        if args.mode == "smoke":
            anchors = anchors[:2]
        frames = []
        for index, scenario in enumerate(anchors, 1):
            print(
                f"[permutation {index}/{len(anchors)}] {scenario.scenario_id}",
                flush=True,
            )
            frames.append(
                run_permutation_anchor(
                    scenario,
                    replicates=anchor_replicates,
                    permutations=permutations,
                    seed=next(child_seeds),
                )
            )
        if frames:
            anchor_replicates_frame = pd.concat(frames, ignore_index=True)
            anchor_replicates_frame.to_csv(
                args.output_dir / "anchor_replicates.csv.gz",
                index=False,
                compression="gzip",
            )
            anchor_summary = summarize_permutation(anchor_replicates_frame)
            anchor_summary = scenario_frame.merge(anchor_summary, on="scenario_id")
            anchor_summary.to_csv(
                args.output_dir / "anchor_summary.csv", index=False
            )
            anchor_aggregate = _aggregate_anchors(anchor_summary)
            anchor_aggregate.to_csv(
                args.output_dir / "anchor_aggregate.csv", index=False
            )

    _write_report(
        args.mode,
        args.output_dir,
        deterministic_aggregate,
        anchor_aggregate,
        deterministic_summary,
        anchor_summary,
    )
    metadata = {
        "mode": args.mode,
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "deterministic_replicates": deterministic_replicates,
        "anchor_replicates": anchor_replicates,
        "permutations": permutations,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scenarios": len(scenarios),
        "scenario_ids": [scenario.scenario_id for scenario in scenarios],
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
