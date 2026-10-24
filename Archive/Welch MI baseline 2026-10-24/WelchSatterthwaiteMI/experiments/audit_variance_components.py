#!/usr/bin/env python3
"""Audit the component-df assumption used by the Welch MI reference."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.random_validation import generate_random_scenarios  # noqa: E402
from differential_mi.statistics import influence_variance  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


SCENARIO_SEED = 64_190_217
SCENARIO_IDS = (
    "random_2x2_d0",
    "random_2x2_d5",
    "random_2x5_d5",
    "random_4x6_d5",
    "random_5x5_d2",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=50_000)
    return parser.parse_args()


def _variance_functional_components(
    probability: np.ndarray,
    sample_size: int,
) -> tuple[float, float, float]:
    """Return V/n, the IF-derived component df, and the IF weighted mean."""
    row = probability.sum(axis=1)
    column = probability.sum(axis=0)
    score = np.log(probability / (row[:, None] * column[None, :]))
    mean = float(np.sum(probability * score))
    second_moment = float(np.sum(probability * score * score))
    variance = second_moment - mean * mean
    row_score_mean = np.sum(probability * score, axis=1) / row
    column_score_mean = np.sum(probability * score, axis=0) / column
    variance_if = (
        score * score
        - second_moment
        + 2.0
        * (
            score
            - row_score_mean[:, None]
            - column_score_mean[None, :]
            + mean
        )
        - 2.0 * mean * (score - mean)
    )
    weighted_mean = float(np.sum(probability * variance_if))
    variance_if_variance = float(
        np.sum(probability * (variance_if - weighted_mean) ** 2)
    )
    component_df = (
        2.0 * sample_size * variance * variance / variance_if_variance
    )
    return variance / sample_size, component_df, weighted_mean


def _empirical_df(values: np.ndarray) -> float:
    return float(2.0 * np.mean(values) ** 2 / np.var(values, ddof=1))


def main() -> None:
    args = parse_args()
    if args.replicates <= 1:
        raise ValueError("replicates must exceed one.")
    scenarios = {
        scenario.scenario_id: scenario
        for scenario in generate_random_scenarios(SCENARIO_SEED)
    }
    rows = []
    for index, scenario_id in enumerate(SCENARIO_IDS):
        scenario = scenarios[scenario_id]
        rng = np.random.default_rng(77_100 + index)
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.reshape(-1),
            size=args.replicates,
        ).reshape(args.replicates, scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_q.reshape(-1),
            size=args.replicates,
        ).reshape(args.replicates, scenario.rows, scenario.columns)
        values = differential_mi_pvalues(table_p, table_q)
        component_p = values["influence_variance_p"] / scenario.n_p
        component_q = values["influence_variance_q"] / scenario.n_q
        total_component = component_p + component_q
        population_a, predicted_df_p, mean_if_p = (
            _variance_functional_components(
                scenario.probability_p,
                scenario.n_p,
            )
        )
        population_b, predicted_df_q, mean_if_q = (
            _variance_functional_components(
                scenario.probability_q,
                scenario.n_q,
            )
        )
        predicted_total_df = (population_a + population_b) ** 2 / (
            population_a**2 / predicted_df_p
            + population_b**2 / predicted_df_q
        )
        rows.append(
            {
                "scenario_id": scenario_id,
                "n_p": scenario.n_p,
                "n_q": scenario.n_q,
                "replicates": args.replicates,
                "naive_component_df_p": scenario.n_p - 1,
                "empirical_component_df_p": _empirical_df(component_p),
                "if_predicted_component_df_p": predicted_df_p,
                "naive_component_df_q": scenario.n_q - 1,
                "empirical_component_df_q": _empirical_df(component_q),
                "if_predicted_component_df_q": predicted_df_q,
                "median_naive_total_df": float(
                    np.nanmedian(values["welch_degrees_of_freedom"])
                ),
                "empirical_total_df": _empirical_df(total_component),
                "if_predicted_total_df": predicted_total_df,
                "correlation_delta_total_variance": float(
                    np.corrcoef(
                        values["delta_corrected"],
                        total_component,
                    )[0, 1]
                ),
                "weighted_mean_variance_if_p": mean_if_p,
                "weighted_mean_variance_if_q": mean_if_q,
            }
        )

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(result.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
