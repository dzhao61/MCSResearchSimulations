#!/usr/bin/env python3
"""Consolidate the completed randomized validation runs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.distributions import mutual_information_probability
from differential_mi.statistics import influence_variance


DETERMINISTIC_METHODS = ("wald_plugin", "wald_analytic", "wald_jackknife")
ANCHOR_METHODS = (
    "naive_perm_plugin",
    "student_perm_plugin",
    "student_perm_analytic",
    "student_perm_jackknife",
    *DETERMINISTIC_METHODS,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "randomized_combined",
    )
    return parser.parse_args()


def _method_rows(
    frame: pd.DataFrame,
    *,
    experiment: str,
    methods: tuple[str, ...],
) -> list[dict[str, int | float | str]]:
    rows = []
    for method in methods:
        rates = frame[f"{method}_fpr_05"]
        row: dict[str, int | float | str] = {
            "experiment": experiment,
            "method": method,
            "scenarios": len(frame),
            "mean_absolute_fpr_error_05": float(np.mean(np.abs(rates - 0.05))),
            "median_absolute_fpr_error_05": float(
                np.median(np.abs(rates - 0.05))
            ),
            "within_035_065": float(np.mean(rates.between(0.035, 0.065))),
            "minimum_fpr_05": float(rates.min()),
            "maximum_fpr_05": float(rates.max()),
        }
        coverage_column = f"{method}_coverage_95"
        if coverage_column in frame:
            coverage = frame[coverage_column]
            row["mean_coverage_95"] = float(coverage.mean())
            row["within_coverage_935_965"] = float(
                np.mean(coverage.between(0.935, 0.965))
            )
        rows.append(row)
    return rows


def _add_mixture_diagnostics(
    summary: pd.DataFrame, scenario_file: Path
) -> pd.DataFrame:
    scenarios = pd.read_csv(scenario_file)
    diagnostics = []
    for scenario in scenarios.itertuples(index=False):
        p = np.asarray(json.loads(scenario.probability_p_json), dtype=float)
        q = np.asarray(json.loads(scenario.probability_q_json), dtype=float)
        weight = scenario.n_p / (scenario.n_p + scenario.n_q)
        mixture = weight * p + (1.0 - weight) * q
        diagnostics.append(
            {
                "scenario_id": scenario.scenario_id,
                "pooled_mixture_mi_recalculated": (
                    mutual_information_probability(mixture)
                ),
                "pooled_mixture_variance_recalculated": float(
                    influence_variance(mixture)
                ),
            }
        )
    return summary.merge(pd.DataFrame(diagnostics), on="scenario_id")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = PROJECT_ROOT / "results"

    broad_parts = []
    for run, directory in (
        ("A", "randomized_broad"),
        ("B", "randomized_broad_replication"),
    ):
        frame = pd.read_csv(results / directory / "deterministic_summary.csv")
        frame["distribution_run"] = run
        broad_parts.append(frame)
    broad = pd.concat(broad_parts, ignore_index=True)
    broad.to_csv(args.output_dir / "combined_broad_summary.csv", index=False)

    anchor_parts = []
    for run, directory in (
        ("A", "randomized_anchors"),
        ("B", "randomized_anchors_replication"),
    ):
        frame = pd.read_csv(results / directory / "anchor_summary.csv")
        frame = _add_mixture_diagnostics(
            frame, results / directory / "random_scenarios.csv"
        )
        frame["distribution_run"] = run
        anchor_parts.append(frame)
    anchors = pd.concat(anchor_parts, ignore_index=True)
    anchors.to_csv(args.output_dir / "combined_anchor_summary.csv", index=False)

    strong = pd.read_csv(
        results / "randomized_strong_null" / "deterministic_summary.csv"
    )
    followup_deterministic = pd.read_csv(
        results / "randomized_followup" / "deterministic_summary.csv"
    )
    followup_anchor = pd.read_csv(
        results / "randomized_followup" / "anchor_summary.csv"
    )

    rows = []
    rows.extend(
        _method_rows(
            broad,
            experiment="randomized_weak_null_2_seeds",
            methods=DETERMINISTIC_METHODS,
        )
    )
    rows.extend(
        _method_rows(
            strong,
            experiment="randomized_strong_null",
            methods=DETERMINISTIC_METHODS,
        )
    )
    rows.extend(
        _method_rows(
            anchors,
            experiment="permutation_anchors_all",
            methods=ANCHOR_METHODS,
        )
    )
    supported_anchors = anchors[
        anchors["pooled_mixture_variance_recalculated"] >= 1e-4
    ]
    rows.extend(
        _method_rows(
            supported_anchors,
            experiment="permutation_anchors_regular_mixture",
            methods=ANCHOR_METHODS,
        )
    )
    rows.extend(
        _method_rows(
            followup_deterministic,
            experiment="posthoc_hard_deterministic",
            methods=DETERMINISTIC_METHODS,
        )
    )
    rows.extend(
        _method_rows(
            followup_anchor,
            experiment="posthoc_hard_permutation",
            methods=ANCHOR_METHODS,
        )
    )
    method_summary = pd.DataFrame(rows)
    method_summary.to_csv(args.output_dir / "method_summary.csv", index=False)

    speedup = anchors["mean_permutation_ms"] / anchors["mean_deterministic_ms"]
    runtime = pd.DataFrame(
        [
            {
                "comparison": "999 table permutations vs all deterministic estimators",
                "table_pairs": int(anchors["replicates"].sum()),
                "mean_deterministic_ms": float(
                    anchors["mean_deterministic_ms"].mean()
                ),
                "mean_permutation_ms": float(
                    anchors["mean_permutation_ms"].mean()
                ),
                "mean_speedup": float(speedup.mean()),
                "minimum_speedup": float(speedup.min()),
                "maximum_speedup": float(speedup.max()),
            }
        ]
    )
    runtime.to_csv(args.output_dir / "runtime_summary.csv", index=False)

    metadata = {
        "weak_null_scenarios": len(broad),
        "weak_null_replicates": int(broad["replicates"].sum()),
        "strong_null_scenarios": len(strong),
        "strong_null_replicates": int(strong["replicates"].sum()),
        "permutation_anchor_scenarios": len(anchors),
        "permutation_anchor_replicates": int(anchors["replicates"].sum()),
        "regular_mixture_anchors": len(supported_anchors),
        "posthoc_deterministic_replicates": int(
            followup_deterministic["replicates"].sum()
        ),
        "posthoc_permutation_replicates": int(
            followup_anchor["replicates"].sum()
        ),
    }
    (args.output_dir / "summary_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Combined results written to {args.output_dir}")


if __name__ == "__main__":
    main()

