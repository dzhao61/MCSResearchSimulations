#!/usr/bin/env python3
"""Regenerate frozen tables to audit invalid Edgeworth cases and tail balance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "InfluenceDfMI" / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "WelchSatterthwaiteMI" / "src"))

from joint_edgeworth_mi import differential_mi_pvalues  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenario_summary = pd.read_csv(args.results_dir / "scenario_summary.csv")
    populations = pd.read_csv(args.results_dir / "scenarios.csv")
    populations = populations[populations["stage"].ne("power")].set_index(
        "scenario_key"
    )
    rows = []
    for index, summary in enumerate(scenario_summary.itertuples(), start=1):
        population = populations.loc[summary.scenario_key]
        probability_p = np.asarray(
            json.loads(population["probability_p_json"]),
            dtype=float,
        )
        probability_q = np.asarray(
            json.loads(population["probability_q_json"]),
            dtype=float,
        )
        rng = np.random.default_rng(int(summary.simulation_seed))
        table_p = rng.multinomial(
            int(summary.n_p),
            probability_p.reshape(-1),
            size=int(summary.replicates),
        ).reshape(
            int(summary.replicates),
            int(summary.rows),
            int(summary.columns),
        )
        table_q = rng.multinomial(
            int(summary.n_q),
            probability_q.reshape(-1),
            size=int(summary.replicates),
        ).reshape(
            int(summary.replicates),
            int(summary.rows),
            int(summary.columns),
        )
        values = differential_mi_pvalues(table_p, table_q)
        base_valid = np.asarray(values["base_valid"], dtype=bool)
        edge_valid = np.asarray(values["edgeworth_valid"], dtype=bool)
        invalid = base_valid & ~edge_valid
        statistic = np.asarray(values["statistic"])
        raw_cdf = norm.cdf(statistic) + np.asarray(
            values["edgeworth_correction"]
        )
        density = np.asarray(values["edgeworth_density_factor"])
        normal_p = np.asarray(values["normal_p_value"])
        edge_p = np.asarray(values["edgeworth_p_value"])

        row: dict[str, int | float | str] = {
            "stage": summary.stage,
            "population_seed": int(summary.population_seed),
            "scenario_id": summary.scenario_id,
            "scenario_key": summary.scenario_key,
            "replicates": int(summary.replicates),
            "base_valid_n": int(np.count_nonzero(base_valid)),
            "edgeworth_valid_n": int(np.count_nonzero(edge_valid)),
            "invalid_n": int(np.count_nonzero(invalid)),
            "invalid_rate": float(np.mean(invalid)),
            "invalid_raw_cdf_below_zero_n": int(
                np.count_nonzero(invalid & (raw_cdf < 0.0))
            ),
            "invalid_raw_cdf_above_one_n": int(
                np.count_nonzero(invalid & (raw_cdf > 1.0))
            ),
            "invalid_nonpositive_density_n": int(
                np.count_nonzero(invalid & (density <= 0.0))
            ),
            "invalid_nonfinite_n": int(
                np.count_nonzero(
                    invalid
                    & (
                        ~np.isfinite(raw_cdf)
                        | ~np.isfinite(density)
                        | ~np.isfinite(statistic)
                    )
                )
            ),
            "invalid_median_abs_statistic": (
                float(np.median(np.abs(statistic[invalid])))
                if np.any(invalid)
                else float("nan")
            ),
            "invalid_normal_rejection_rate_05": (
                float(np.mean(normal_p[invalid] <= 0.05))
                if np.any(invalid)
                else float("nan")
            ),
            "invalid_normal_rejection_rate_10": (
                float(np.mean(normal_p[invalid] <= 0.10))
                if np.any(invalid)
                else float("nan")
            ),
        }
        for label, alpha in (("10", 0.10), ("05", 0.05)):
            candidate_reject = edge_valid & (edge_p <= alpha)
            normal_reject = base_valid & (normal_p <= alpha)
            denominator = int(np.count_nonzero(base_valid))
            candidate_count = int(np.count_nonzero(candidate_reject))
            fallback_normal_count = candidate_count + int(
                np.count_nonzero(invalid & (normal_p <= alpha))
            )
            row[f"candidate_valid_only_fpr_{label}"] = (
                candidate_count / int(np.count_nonzero(edge_valid))
            )
            row[f"candidate_invalid_nonreject_fpr_{label}"] = (
                candidate_count / denominator
            )
            row[f"candidate_invalid_reject_fpr_{label}"] = (
                (candidate_count + int(np.count_nonzero(invalid))) / denominator
            )
            row[f"candidate_normal_fallback_fpr_{label}"] = (
                fallback_normal_count / denominator
            )
            row[f"candidate_left_rejections_{label}"] = int(
                np.count_nonzero(candidate_reject & (statistic < 0))
            )
            row[f"candidate_right_rejections_{label}"] = int(
                np.count_nonzero(candidate_reject & (statistic >= 0))
            )
            row[f"normal_left_rejections_{label}"] = int(
                np.count_nonzero(normal_reject & (statistic < 0))
            )
            row[f"normal_right_rejections_{label}"] = int(
                np.count_nonzero(normal_reject & (statistic >= 0))
            )
        rows.append(row)
        print(
            f"[{index}/{len(scenario_summary)}] "
            f"{summary.stage}:{summary.scenario_id}",
            flush=True,
        )

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(
        result.groupby("stage").agg(
            scenarios=("scenario_key", "size"),
            invalid_n=("invalid_n", "sum"),
            replicates=("replicates", "sum"),
            mean_normal_fallback_fpr_05=(
                "candidate_normal_fallback_fpr_05",
                "mean",
            ),
            mean_valid_only_fpr_05=("candidate_valid_only_fpr_05", "mean"),
        ).to_string(),
        flush=True,
    )


if __name__ == "__main__":
    main()
