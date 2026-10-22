#!/usr/bin/env python3
"""Run the pre-specified differential-MI validation profiles."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.scenarios import build_distributions, scenarios_for_profile
from differential_mi.simulation import (
    P_VALUE_COLUMNS,
    SimulationSettings,
    run_scenario,
    summarize_replicates,
)


PROFILE_SETTINGS = {
    "smoke": SimulationSettings(40, 40, 99, 20260725),
    "screen": SimulationSettings(300, 300, 199, 20260725),
    "decisive": SimulationSettings(2_000, 1_000, 999, 20260725),
    "adversarial": SimulationSettings(2_000, 1_000, 999, 20260726),
    "power_curve": SimulationSettings(1_000, 1_500, 499, 20260727),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=PROFILE_SETTINGS, default="smoke")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--null-replicates", type=int)
    parser.add_argument("--power-replicates", type=int)
    parser.add_argument("--permutations", type=int)
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


def resolved_settings(args: argparse.Namespace) -> SimulationSettings:
    defaults = PROFILE_SETTINGS[args.profile]
    return SimulationSettings(
        null_replicates=args.null_replicates or defaults.null_replicates,
        power_replicates=args.power_replicates or defaults.power_replicates,
        permutations=args.permutations or defaults.permutations,
        seed=args.seed if args.seed is not None else defaults.seed,
    )


def plot_calibration(summary: pd.DataFrame, output_dir: Path) -> None:
    null = summary[summary["family"].isin(["strong_null", "weak_null", "near_boundary"])]
    methods = [column.removesuffix("_p") for column in P_VALUE_COLUMNS]
    x = np.arange(len(null))
    width = 0.15
    fig, ax = plt.subplots(figsize=(15, 7))
    for index, method in enumerate(methods):
        ax.bar(
            x + (index - 2) * width,
            null[f"{method}_fpr_05"],
            width,
            label=method,
        )
    ax.axhline(0.05, color="black", linewidth=1.5, linestyle="--", label="nominal 0.05")
    ax.axhspan(0.035, 0.065, color="grey", alpha=0.12)
    ax.set_xticks(x, null["scenario_id"], rotation=45, ha="right")
    ax.set_ylabel("Rejection rate at alpha=0.05")
    ax.set_title("Differential-MI null calibration")
    ax.legend(ncol=2)
    fig.tight_layout()
    fig.savefig(output_dir / "calibration_05.png", dpi=160)
    plt.close(fig)


def frame_to_markdown(frame: pd.DataFrame) -> list[str]:
    """Render a compact Markdown table without pandas' optional tabulate package."""
    headers = [str(column) for column in frame.columns]
    rows = []
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, (float, np.floating)):
                rendered.append(f"{value:.4f}")
            else:
                rendered.append(str(value))
        rows.append(rendered)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def write_report(
    profile: str,
    settings: SimulationSettings,
    scenarios_frame: pd.DataFrame,
    summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    null = summary[summary["family"].isin(["strong_null", "weak_null", "near_boundary"])]
    regular_weak = summary[(summary["family"] == "weak_null") & summary["regular"]]
    power = summary[summary["family"] == "power"]

    def mean_error(method: str) -> float:
        if regular_weak.empty:
            return float("nan")
        return float(np.mean(np.abs(regular_weak[f"{method}_fpr_05"] - 0.05)))

    naive_error = mean_error("naive_perm_plugin")
    student_error = mean_error("student_perm_jackknife")
    reduction = (
        1.0 - student_error / naive_error
        if np.isfinite(naive_error) and naive_error > 0
        else float("nan")
    )
    student_within = (
        float(
            np.mean(
                regular_weak["student_perm_jackknife_fpr_05"].between(0.035, 0.065)
            )
        )
        if not regular_weak.empty
        else float("nan")
    )
    naive_failures = (
        int(
            np.count_nonzero(
                (np.abs(regular_weak["naive_perm_plugin_fpr_05"] - 0.05) >= 0.02)
                & (
                    (regular_weak["naive_perm_plugin_fpr_05_low"] > 0.05)
                    | (regular_weak["naive_perm_plugin_fpr_05_high"] < 0.05)
                )
            )
        )
        if not regular_weak.empty
        else 0
    )

    lines = [
        f"# Differential-MI Validation: {profile}",
        "",
        "## Run",
        "",
        f"- Null replicates per scenario: {settings.null_replicates}",
        f"- Power replicates per scenario: {settings.power_replicates}",
        f"- Permutations per replicate: {settings.permutations}",
        f"- Seed: {settings.seed}",
        "",
        "## Pre-Specified Decision Metrics",
        "",
        f"- Regular weak-null mean absolute FPR error, naive permutation: {naive_error:.4f}",
        f"- Regular weak-null mean absolute FPR error, studentized jackknife permutation: {student_error:.4f}",
        f"- Relative calibration-error reduction: {reduction:.1%}",
        f"- Regular weak-null studentized cases within [0.035, 0.065]: {student_within:.1%}",
        f"- Material naive failures with Wilson interval excluding 0.05: {naive_failures}",
        "",
        "These metrics are decisive only for the `decisive` profile. Smoke and screen",
        "runs are exploratory because their Monte Carlo intervals are wide.",
        "",
        "## Calibration",
        "",
    ]
    columns = [
        "scenario_id",
        "family",
        "regular",
        "naive_perm_plugin_fpr_05",
        "student_perm_plugin_fpr_05",
        "student_perm_jackknife_fpr_05",
        "wald_plugin_fpr_05",
        "wald_jackknife_fpr_05",
        "wald_jackknife_95_coverage",
    ]
    lines.extend(frame_to_markdown(null[columns]))
    if not power.empty:
        lines.extend(["", "## Power", ""])
        lines.extend(frame_to_markdown(power[columns]))
    lines.extend(
        [
            "",
            "## Runtime",
            "",
            f"- Mean deterministic time: {summary['mean_deterministic_ms'].mean():.3f} ms/table",
            f"- Mean permutation time: {summary['mean_permutation_ms'].mean():.3f} ms/table",
            "",
            "See `summary.csv`, `replicates.csv`, and `scenarios.csv` for full results.",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    settings = resolved_settings(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = scenarios_for_profile(args.profile)
    seed_sequence = np.random.SeedSequence(settings.seed)
    scenario_seeds = [
        int(child.generate_state(1)[0]) for child in seed_sequence.spawn(len(scenarios))
    ]

    replicate_frames = []
    scenario_rows = []
    for index, (scenario, scenario_seed) in enumerate(zip(scenarios, scenario_seeds), 1):
        probability_p, probability_q, diagnostics = build_distributions(scenario)
        print(
            f"[{index}/{len(scenarios)}] {scenario.scenario_id}: "
            f"MI=({diagnostics['true_mi_p']:.6f}, {diagnostics['true_mi_q']:.6f})",
            flush=True,
        )
        frame, run_diagnostics = run_scenario(
            scenario, settings, scenario_seed=scenario_seed
        )
        replicate_frames.append(frame)
        row = scenario.to_dict()
        row.update(run_diagnostics)
        row["probability_p_json"] = json.dumps(probability_p.tolist())
        row["probability_q_json"] = json.dumps(probability_q.tolist())
        row["scenario_seed"] = scenario_seed
        scenario_rows.append(row)

    replicates = pd.concat(replicate_frames, ignore_index=True)
    scenario_frame = pd.DataFrame(scenario_rows)
    summary = summarize_replicates(replicates)
    summary = scenario_frame.merge(summary, on=["scenario_id", "family", "regular"])

    replicates.to_csv(args.output_dir / "replicates.csv", index=False)
    scenario_frame.to_csv(args.output_dir / "scenarios.csv", index=False)
    summary.to_csv(args.output_dir / "summary.csv", index=False)
    plot_calibration(summary, args.output_dir)
    write_report(args.profile, settings, scenario_frame, summary, args.output_dir)

    metadata = {
        "profile": args.profile,
        "settings": settings.__dict__,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "pid": os.getpid(),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
