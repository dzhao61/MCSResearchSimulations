#!/usr/bin/env python3
"""Run a fresh, untuned population-grid audit of the Welch MI reference."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.random_validation import (  # noqa: E402
    generate_random_scenarios,
    scenario_diagnostics,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


DEFAULT_SCENARIO_SEED = 64_190_217
DEFAULT_SIMULATION_SEED = 81_357_029
DEFAULT_BOOTSTRAP_SEED = 91_827
HARD_SHAPES = frozenset(
    {
        (2, 2),
        (2, 5),
        (3, 7),
        (4, 6),
        (5, 5),
        (5, 10),
    }
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=10_000)
    parser.add_argument("--strong-null-replicates", type=int, default=5_000)
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    return parser.parse_args()


def _bootstrap_mean_interval(
    values: np.ndarray,
    *,
    seed: int,
    samples: int = 100_000,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    bootstrap_means = np.mean(
        rng.choice(values, size=(samples, values.size), replace=True),
        axis=1,
    )
    return (
        float(np.quantile(bootstrap_means, 0.025)),
        float(np.quantile(bootstrap_means, 0.975)),
    )


def _aggregate(
    scenarios: pd.DataFrame,
    *,
    stage: str,
    mask: pd.Series,
    bootstrap_seed: int,
) -> dict[str, int | float | str]:
    group = scenarios.loc[mask]
    gain_05 = group["normal_error_05"] - group["welch_error_05"]
    gain_10 = group["normal_error_10"] - group["welch_error_10"]
    interval_05 = _bootstrap_mean_interval(gain_05.to_numpy(), seed=bootstrap_seed)
    interval_10 = _bootstrap_mean_interval(
        gain_10.to_numpy(),
        seed=bootstrap_seed + 1,
    )
    return {
        "stage": stage,
        "population_pairs": len(group),
        "table_pairs_per_population": int(group["replicates"].iloc[0]),
        "normal_mean_fpr_05": float(group["normal_fpr_05"].mean()),
        "welch_mean_fpr_05": float(group["welch_fpr_05"].mean()),
        "normal_mae_05": float(group["normal_error_05"].mean()),
        "welch_mae_05": float(group["welch_error_05"].mean()),
        "mean_mae_gain_05": float(gain_05.mean()),
        "mean_mae_gain_05_low": interval_05[0],
        "mean_mae_gain_05_high": interval_05[1],
        "improved_scenarios_05": int((gain_05 > 0).sum()),
        "worsened_scenarios_05": int((gain_05 < 0).sum()),
        "tied_scenarios_05": int((gain_05 == 0).sum()),
        "normal_mae_10": float(group["normal_error_10"].mean()),
        "welch_mae_10": float(group["welch_error_10"].mean()),
        "mean_mae_gain_10": float(gain_10.mean()),
        "mean_mae_gain_10_low": interval_10[0],
        "mean_mae_gain_10_high": interval_10[1],
        "normal_only_rejections_05": int(group["normal_only_rejections_05"].sum()),
        "welch_only_rejections_05": int(group["welch_only_rejections_05"].sum()),
        "minimum_valid_rate": float(group["valid_rate"].min()),
    }


def main() -> None:
    args = parse_args()
    if args.replicates <= 0 or args.strong_null_replicates <= 0:
        raise ValueError("replicate counts must be positive.")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    scenarios = generate_random_scenarios(args.scenario_seed)
    child_sequences = np.random.SeedSequence(args.simulation_seed).spawn(
        len(scenarios)
    )
    rows = []
    for index, (scenario, child) in enumerate(zip(scenarios, child_sequences)):
        simulation_seed = int(child.generate_state(1)[0])
        rng = np.random.default_rng(simulation_seed)
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
        valid = values["valid"]
        normal_p = values["normal_p_value"][valid]
        welch_p = values["welch_p_value"][valid]
        diagnostics = scenario_diagnostics(scenario)
        row = {
            "null_type": "weak",
            "scenario_id": scenario.scenario_id,
            "rows": scenario.rows,
            "columns": scenario.columns,
            "design_index": scenario.design_index,
            "n_p": scenario.n_p,
            "n_q": scenario.n_q,
            "replicates": args.replicates,
            "simulation_seed": simulation_seed,
            "true_delta": diagnostics["true_delta"],
            "minimum_joint_expected_p": diagnostics["min_joint_expected_p"],
            "minimum_joint_expected_q": diagnostics["min_joint_expected_q"],
            "valid_rate": float(valid.mean()),
            "median_welch_df": float(
                np.median(values["welch_degrees_of_freedom"][valid])
            ),
        }
        for label, alpha in (("10", 0.10), ("05", 0.05)):
            normal_reject = normal_p <= alpha
            welch_reject = welch_p <= alpha
            normal_fpr = float(normal_reject.mean())
            welch_fpr = float(welch_reject.mean())
            row[f"normal_fpr_{label}"] = normal_fpr
            row[f"welch_fpr_{label}"] = welch_fpr
            row[f"normal_error_{label}"] = abs(normal_fpr - alpha)
            row[f"welch_error_{label}"] = abs(welch_fpr - alpha)
            row[f"normal_only_rejections_{label}"] = int(
                np.count_nonzero(normal_reject & ~welch_reject)
            )
            row[f"welch_only_rejections_{label}"] = int(
                np.count_nonzero(welch_reject & ~normal_reject)
            )
        rows.append(row)
        print(f"[{index + 1}/{len(scenarios)}] {scenario.scenario_id}", flush=True)

    scenario_frame = pd.DataFrame(rows)
    strong_rows = []
    strong_children = np.random.SeedSequence(
        [args.simulation_seed, 9_919]
    ).spawn(len(scenarios))
    for index, (scenario, child) in enumerate(zip(scenarios, strong_children)):
        simulation_seed = int(child.generate_state(1)[0])
        rng = np.random.default_rng(simulation_seed)
        table_p = rng.multinomial(
            scenario.n_p,
            scenario.probability_p.reshape(-1),
            size=args.strong_null_replicates,
        ).reshape(
            args.strong_null_replicates,
            scenario.rows,
            scenario.columns,
        )
        table_q = rng.multinomial(
            scenario.n_q,
            scenario.probability_p.reshape(-1),
            size=args.strong_null_replicates,
        ).reshape(
            args.strong_null_replicates,
            scenario.rows,
            scenario.columns,
        )
        values = differential_mi_pvalues(table_p, table_q)
        valid = values["valid"]
        normal_p = values["normal_p_value"][valid]
        welch_p = values["welch_p_value"][valid]
        row = {
            "null_type": "strong",
            "scenario_id": scenario.scenario_id,
            "rows": scenario.rows,
            "columns": scenario.columns,
            "design_index": scenario.design_index,
            "n_p": scenario.n_p,
            "n_q": scenario.n_q,
            "replicates": args.strong_null_replicates,
            "simulation_seed": simulation_seed,
            "true_delta": 0.0,
            "minimum_joint_expected_p": (
                scenario.n_p * scenario.probability_p.min()
            ),
            "minimum_joint_expected_q": (
                scenario.n_q * scenario.probability_p.min()
            ),
            "valid_rate": float(valid.mean()),
            "median_welch_df": float(
                np.median(values["welch_degrees_of_freedom"][valid])
            ),
        }
        for label, alpha in (("10", 0.10), ("05", 0.05)):
            normal_reject = normal_p <= alpha
            welch_reject = welch_p <= alpha
            normal_fpr = float(normal_reject.mean())
            welch_fpr = float(welch_reject.mean())
            row[f"normal_fpr_{label}"] = normal_fpr
            row[f"welch_fpr_{label}"] = welch_fpr
            row[f"normal_error_{label}"] = abs(normal_fpr - alpha)
            row[f"welch_error_{label}"] = abs(welch_fpr - alpha)
            row[f"normal_only_rejections_{label}"] = int(
                np.count_nonzero(normal_reject & ~welch_reject)
            )
            row[f"welch_only_rejections_{label}"] = int(
                np.count_nonzero(welch_reject & ~normal_reject)
            )
        strong_rows.append(row)
        print(
            f"[strong {index + 1}/{len(scenarios)}] {scenario.scenario_id}",
            flush=True,
        )
    strong_frame = pd.DataFrame(strong_rows)

    hard_mask = (
        scenario_frame["design_index"].eq(5)
        & pd.Series(
            list(
                zip(
                    scenario_frame["rows"],
                    scenario_frame["columns"],
                )
            ),
            index=scenario_frame.index,
        ).isin(HARD_SHAPES)
    )
    aggregates = pd.DataFrame(
        [
            _aggregate(
                scenario_frame,
                stage="fresh_broad",
                mask=pd.Series(True, index=scenario_frame.index),
                bootstrap_seed=DEFAULT_BOOTSTRAP_SEED,
            ),
            _aggregate(
                scenario_frame,
                stage="frozen_hard_design",
                mask=hard_mask,
                bootstrap_seed=DEFAULT_BOOTSTRAP_SEED + 10,
            ),
            _aggregate(
                strong_frame,
                stage="fresh_strong_null",
                mask=pd.Series(True, index=strong_frame.index),
                bootstrap_seed=DEFAULT_BOOTSTRAP_SEED + 20,
            ),
        ]
    )

    scenario_frame.to_csv(args.output_dir / "scenario_summary.csv", index=False)
    strong_frame.to_csv(
        args.output_dir / "strong_null_scenario_summary.csv",
        index=False,
    )
    aggregates.to_csv(args.output_dir / "method_summary.csv", index=False)
    metadata = {
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "bootstrap_seed": DEFAULT_BOOTSTRAP_SEED,
        "replicates": args.replicates,
        "strong_null_replicates": args.strong_null_replicates,
        "population_pairs": len(scenarios),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(aggregates.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
