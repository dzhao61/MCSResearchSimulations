#!/usr/bin/env python3
"""Run the pre-specified influence-saddlepoint validation stages."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.inference import influence_saddlepoint_test
from differential_mi.random_validation import (
    RandomScenario,
    generate_random_scenarios,
    scenario_diagnostics,
)


DEFAULT_SCENARIO_SEEDS = (2026072501, 2026072601)
DEFAULT_SIMULATION_SEED = 2026072701


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("smoke", "broad"), default="smoke")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--scenario-seed", type=int, action="append", dest="scenario_seeds"
    )
    parser.add_argument("--simulation-seed", type=int, default=DEFAULT_SIMULATION_SEED)
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--scenario-limit", type=int)
    return parser.parse_args()


def _run_scenario(
    scenario: RandomScenario,
    *,
    scenario_seed: int,
    replicates: int,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    tables_p = rng.multinomial(
        scenario.n_p,
        scenario.probability_p.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    tables_q = rng.multinomial(
        scenario.n_q,
        scenario.probability_q.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)

    rows: list[dict[str, float | int | bool | str]] = []
    for replicate, (table_p, table_q) in enumerate(zip(tables_p, tables_q)):
        result = influence_saddlepoint_test(table_p, table_q)
        rows.append(
            {
                "scenario_seed": scenario_seed,
                "scenario_id": scenario.scenario_id,
                "replicate": replicate,
                "replicate_seed": seed,
                "rows": scenario.rows,
                "columns": scenario.columns,
                "n_p": scenario.n_p,
                "n_q": scenario.n_q,
                "target_mi": scenario.target_mi,
                "delta_corrected": result.delta_corrected,
                "standard_error": result.standard_error,
                "wald_analytic_p": result.wald_p_value,
                "influence_saddlepoint_p": result.saddlepoint_p_value,
                "route": result.route,
                "support_lower": result.support_lower,
                "support_upper": result.support_upper,
                "saddlepoint_root": result.saddlepoint_root,
                "root_residual": result.root_residual,
                "root_iterations": result.root_iterations,
                "cgf_second_at_root": result.cgf_second_at_root,
                "lugannani_rice_w": result.lugannani_rice_w,
                "lugannani_rice_u": result.lugannani_rice_u,
                "tail_was_clipped": result.tail_was_clipped,
                "valid": result.valid_first_order_calculation,
                "saddlepoint_seconds": result.elapsed_seconds,
            }
        )
    return pd.DataFrame(rows)


def _summarize(replicates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    keys = ["scenario_seed", "scenario_id"]
    for (scenario_seed, scenario_id), group in replicates.groupby(keys, sort=False):
        row: dict[str, float | int | str] = {
            "scenario_seed": int(scenario_seed),
            "scenario_id": str(scenario_id),
            "rows": int(group["rows"].iloc[0]),
            "columns": int(group["columns"].iloc[0]),
            "n_p": int(group["n_p"].iloc[0]),
            "n_q": int(group["n_q"].iloc[0]),
            "target_mi": float(group["target_mi"].iloc[0]),
            "replicates": len(group),
            "invalid_rate": float(np.mean(~group["valid"])),
            "fallback_rate": float(np.mean(group["route"] != "lugannani_rice")),
            "clipped_rate": float(group["tail_was_clipped"].mean()),
            "median_root_iterations": float(group["root_iterations"].median()),
            "median_saddlepoint_ms": float(
                1000.0 * group["saddlepoint_seconds"].median()
            ),
            "p95_saddlepoint_ms": float(
                1000.0 * group["saddlepoint_seconds"].quantile(0.95)
            ),
        }
        for method in ("wald_analytic", "influence_saddlepoint"):
            values = group[f"{method}_p"]
            valid = values[np.isfinite(values)]
            row[f"{method}_valid_n"] = len(valid)
            row[f"{method}_fpr_10"] = float(np.mean(valid <= 0.10))
            row[f"{method}_fpr_05"] = float(np.mean(valid <= 0.05))
        for route, count in group["route"].value_counts().items():
            row[f"route_{route}_rate"] = float(count / len(group))
        rows.append(row)
    return pd.DataFrame(rows).fillna(0.0)


def _aggregate(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method in ("wald_analytic", "influence_saddlepoint"):
        rates = summary[f"{method}_fpr_05"]
        rows.append(
            {
                "method": method,
                "scenarios": len(summary),
                "mean_absolute_fpr_error_05": float(
                    np.mean(np.abs(rates - 0.05))
                ),
                "median_absolute_fpr_error_05": float(
                    np.median(np.abs(rates - 0.05))
                ),
                "within_035_065": float(np.mean(rates.between(0.035, 0.065))),
                "minimum_fpr_05": float(rates.min()),
                "maximum_fpr_05": float(rates.max()),
            }
        )
    return pd.DataFrame(rows)


def _decision(summary: pd.DataFrame, aggregate: pd.DataFrame) -> dict[str, float | bool]:
    indexed = aggregate.set_index("method")
    wald_mae = float(
        indexed.loc["wald_analytic", "mean_absolute_fpr_error_05"]
    )
    saddle_mae = float(
        indexed.loc["influence_saddlepoint", "mean_absolute_fpr_error_05"]
    )
    wald_band = float(indexed.loc["wald_analytic", "within_035_065"])
    saddle_band = float(indexed.loc["influence_saddlepoint", "within_035_065"])
    new_bad = (
        summary["wald_analytic_fpr_05"].between(0.035, 0.065)
        & ~summary["influence_saddlepoint_fpr_05"].between(0.025, 0.075)
    )
    improvement = (wald_mae - saddle_mae) / wald_mae if wald_mae > 0 else 0.0
    return {
        "relative_mae_improvement": improvement,
        "in_band_change": saddle_band - wald_band,
        "new_bad_scenarios": int(new_bad.sum()),
        "maximum_invalid_rate": float(summary["invalid_rate"].max()),
        "passes_stage_2": bool(
            improvement >= 0.10
            and saddle_band >= wald_band - 0.02
            and not new_bad.any()
            and summary["invalid_rate"].max() == 0.0
        ),
    }


def _markdown_table(frame: pd.DataFrame) -> list[str]:
    headers = [str(column) for column in frame.columns]
    interpretation = (
        [
            "The smoke run is an implementation check only. The pass/fail rule is",
            "interpreted decisively only for the complete two-seed broad run.",
        ]
        if mode == "smoke"
        else [
            "This is the complete two-seed broad run. The frozen decision rule",
            "is interpreted decisively and stops the rejected refinement branch.",
        ]
    )
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        rendered = [
            f"{value:.5f}" if isinstance(value, (float, np.floating)) else str(value)
            for value in values
        ]
        lines.append("| " + " | ".join(rendered) + " |")
    return lines


def _write_report(
    output_dir: Path,
    mode: str,
    aggregate: pd.DataFrame,
    summary: pd.DataFrame,
    decision: dict[str, float | bool],
    elapsed: float,
) -> None:
    runtime = summary[
        ["median_saddlepoint_ms", "p95_saddlepoint_ms", "fallback_rate"]
    ].mean()
    lines = [
        "# Influence-Saddlepoint Validation",
        "",
        f"Mode: `{mode}`.",
        "",
        "## Calibration",
        "",
        *_markdown_table(aggregate),
        "",
        "## Frozen Decision Rule",
        "",
        f"- Relative MAE improvement: `{decision['relative_mae_improvement']:.3%}`",
        f"- Change in in-band proportion: `{decision['in_band_change']:.3%}`",
        f"- New bad scenarios: `{decision['new_bad_scenarios']}`",
        f"- Maximum invalid rate: `{decision['maximum_invalid_rate']:.3%}`",
        f"- Stage-2 pass: `{decision['passes_stage_2']}`",
        "",
        "## Runtime and Routes",
        "",
        f"- Mean scenario median runtime: `{runtime['median_saddlepoint_ms']:.3f} ms`",
        f"- Mean scenario p95 runtime: `{runtime['p95_saddlepoint_ms']:.3f} ms`",
        f"- Mean fallback rate: `{runtime['fallback_rate']:.3%}`",
        f"- Complete run wall time: `{elapsed:.2f} s`",
        "",
        *interpretation,
    ]
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenario_seeds = args.scenario_seeds or list(DEFAULT_SCENARIO_SEEDS)
    if args.mode == "smoke":
        scenario_seeds = scenario_seeds[:1]
        replicates = args.replicates or 100
        scenario_limit = args.scenario_limit or 6
    else:
        replicates = args.replicates or 2000
        scenario_limit = args.scenario_limit

    started = perf_counter()
    frames = []
    scenario_rows = []
    run_index = 0
    for scenario_seed in scenario_seeds:
        scenarios = generate_random_scenarios(scenario_seed)
        if scenario_limit is not None:
            positions = np.linspace(
                0, len(scenarios) - 1, scenario_limit, dtype=int
            )
            scenarios = [scenarios[position] for position in positions]
        for scenario in scenarios:
            seed = args.simulation_seed + run_index
            print(
                f"[{run_index + 1}] seed={scenario_seed} "
                f"{scenario.scenario_id}: {replicates} replicates",
                flush=True,
            )
            frames.append(
                _run_scenario(
                    scenario,
                    scenario_seed=scenario_seed,
                    replicates=replicates,
                    seed=seed,
                )
            )
            metadata = scenario_diagnostics(scenario)
            metadata["scenario_seed"] = scenario_seed
            metadata["probability_p_json"] = json.dumps(
                scenario.probability_p.tolist()
            )
            metadata["probability_q_json"] = json.dumps(
                scenario.probability_q.tolist()
            )
            scenario_rows.append(metadata)
            run_index += 1

    replicates_frame = pd.concat(frames, ignore_index=True)
    scenarios_frame = pd.DataFrame(scenario_rows)
    summary = _summarize(replicates_frame)
    aggregate = _aggregate(summary)
    decision = _decision(summary, aggregate)
    elapsed = perf_counter() - started

    replicates_frame.to_csv(
        args.output_dir / "refinement_replicates.csv.gz",
        index=False,
        compression="gzip",
    )
    scenarios_frame.to_csv(args.output_dir / "scenarios.csv", index=False)
    summary.to_csv(args.output_dir / "summary.csv", index=False)
    aggregate.to_csv(args.output_dir / "aggregate.csv", index=False)
    metadata = {
        "mode": args.mode,
        "scenario_seeds": scenario_seeds,
        "simulation_seed": args.simulation_seed,
        "replicates_per_scenario": replicates,
        "scenarios": len(summary),
        "elapsed_seconds": elapsed,
        "decision": decision,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_report(
        args.output_dir,
        args.mode,
        aggregate,
        summary,
        decision,
        elapsed,
    )
    print(aggregate.to_string(index=False), flush=True)
    print(json.dumps(decision, indent=2), flush=True)


if __name__ == "__main__":
    main()
