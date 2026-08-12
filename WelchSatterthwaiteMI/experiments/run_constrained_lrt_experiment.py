#!/usr/bin/env python3
"""Screen constrained equal-MI likelihood-ratio inference on 16 configs."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from welch_differential_mi import (  # noqa: E402
    constrained_likelihood_ratio_test,
    differential_mi_pvalues,
)

from run_supervisor_experiment import (  # noqa: E402
    DEFAULT_SCENARIO_SEED,
    DEFAULT_SIMULATION_SEED,
    DESIGN_TO_REGIME,
    REGIMES,
    generate_configuration_scenarios,
    _scenario_simulation_seeds,
)


ALPHAS = (0.10, 0.05, 0.01)
METHODS = {
    "normal_wald": ("Normal Wald", "normal_p_value", "base_valid"),
    "simple_welch": ("Simple Welch", "welch_p_value", "simple_valid"),
    "expanded_welch": (
        "Expanded Welch",
        "expanded_welch_p_value",
        "expanded_valid",
    ),
    "constrained_lrt": ("Constrained LRT", None, None),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=500)
    parser.add_argument("--population-replicates", type=int, default=10)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--audit-replicates", type=int, default=10)
    parser.add_argument("--multiple-starts", action="store_true")
    parser.add_argument("--scenario-start", type=int, default=0)
    parser.add_argument("--scenario-stop", type=int)
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "constrained_lrt_16_config",
    )
    return parser.parse_args()


def _scenario_metadata(scenario, seed: int, replicates: int) -> dict:
    condition = DESIGN_TO_REGIME[scenario.design_index]
    return {
        "scenario_id": scenario.scenario_id,
        "configuration_id": scenario.configuration_id,
        "rows": scenario.rows,
        "columns": scenario.columns,
        "condition": condition,
        "condition_label": REGIMES[condition]["label"],
        "n_p": scenario.n_p,
        "n_q": scenario.n_q,
        "population_replication": scenario.population_replication,
        "target_mi": scenario.target_mi,
        "simulation_seed": seed,
        "replicates": replicates,
    }


def _run_scenario(task) -> tuple[list[dict], np.ndarray, dict]:
    scenario, seed, replicates, audit_replicates, force_multiple_starts = task
    rng = np.random.default_rng(seed)
    table_p = rng.multinomial(
        scenario.n_p,
        scenario.probability_p.ravel(),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    table_q = rng.multinomial(
        scenario.n_q,
        scenario.probability_q.ravel(),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    analytic = differential_mi_pvalues(
        table_p,
        table_q,
        include_simple=True,
        include_expanded=True,
        include_unbiased_sensitivity=False,
    )
    p_values = np.full((len(METHODS), replicates), np.nan, dtype=float)
    for method_index, (method, (_, p_key, validity_key)) in enumerate(
        METHODS.items()
    ):
        if method == "constrained_lrt":
            continue
        valid = analytic[validity_key]
        p_values[method_index, valid] = analytic[p_key][valid]

    lrt_index = tuple(METHODS).index("constrained_lrt")
    converged = np.zeros(replicates, dtype=bool)
    fallback = np.zeros(replicates, dtype=bool)
    iterations = np.zeros(replicates, dtype=int)
    residuals = np.full(replicates, np.nan)
    elapsed = np.full(replicates, np.nan)
    audit_differences = []
    for index, (p, q) in enumerate(zip(table_p, table_q)):
        result = constrained_likelihood_ratio_test(
            p,
            q,
            multiple_starts=force_multiple_starts,
        )
        if not result.converged:
            fallback[index] = True
            result = constrained_likelihood_ratio_test(
                p,
                q,
                multiple_starts=True,
            )
        if index < audit_replicates and not force_multiple_starts:
            audited = constrained_likelihood_ratio_test(
                p,
                q,
                multiple_starts=True,
            )
            if result.converged and audited.converged:
                audit_differences.append(abs(result.statistic - audited.statistic))
        converged[index] = result.converged
        iterations[index] = result.iterations
        residuals[index] = result.constraint_residual
        elapsed[index] = result.elapsed_seconds
        if result.converged:
            p_values[lrt_index, index] = result.p_value

    common = _scenario_metadata(scenario, seed, replicates)
    rows = []
    for method_index, (method, (label, _, _)) in enumerate(METHODS.items()):
        values = p_values[method_index]
        valid = np.isfinite(values)
        row = {
            **common,
            "method": method,
            "method_label": label,
            "valid_replicates": int(np.count_nonzero(valid)),
            "valid_rate": float(np.mean(valid)),
        }
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            row[f"fpr_{suffix}"] = (
                float(np.mean(values[valid] <= alpha))
                if np.any(valid)
                else np.nan
            )
        rows.append(row)
    diagnostics = {
        **common,
        "lrt_convergence_rate": float(np.mean(converged)),
        "lrt_fallback_rate": float(np.mean(fallback)),
        "lrt_median_iterations": float(np.median(iterations[converged]))
        if np.any(converged)
        else np.nan,
        "lrt_max_constraint_residual": float(np.nanmax(residuals)),
        "lrt_mean_seconds_per_fit": float(np.nanmean(elapsed)),
        "audited_replicates": len(audit_differences),
        "audit_max_statistic_difference": float(max(audit_differences, default=np.nan)),
        "audit_mean_statistic_difference": float(np.mean(audit_differences))
        if audit_differences
        else np.nan,
    }
    return rows, p_values, diagnostics


def _aggregate(results: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    rows = []
    for keys, group in results.groupby(
        [*group_columns, "method", "method_label"],
        sort=False,
    ):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip([*group_columns, "method", "method_label"], keys))
        row["population_pairs"] = len(group)
        row["mean_valid_rate"] = float(group["valid_rate"].mean())
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            values = group[f"fpr_{suffix}"].to_numpy()
            row[f"mean_fpr_{suffix}"] = float(np.nanmean(values))
            row[f"configuration_mae_{suffix}"] = float(
                np.nanmean(np.abs(values - alpha))
            )
            row[f"population_sd_fpr_{suffix}"] = float(
                np.nanstd(values, ddof=1)
            )
        rows.append(row)
    return pd.DataFrame(rows)


def _overall(configuration: pd.DataFrame) -> pd.DataFrame:
    rows = []
    normal = configuration[configuration.method == "normal_wald"].set_index(
        "configuration_id"
    )
    for method, group in configuration.groupby("method", sort=False):
        indexed = group.set_index("configuration_id")
        row = {
            "method": method,
            "method_label": group.method_label.iloc[0],
            "configurations": len(group),
            "mean_valid_rate": float(group.mean_valid_rate.mean()),
        }
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            errors = np.abs(group[f"mean_fpr_{suffix}"] - alpha)
            normal_errors = np.abs(normal[f"mean_fpr_{suffix}"] - alpha)
            candidate_errors = np.abs(indexed[f"mean_fpr_{suffix}"] - alpha)
            row[f"mean_fpr_{suffix}"] = float(group[f"mean_fpr_{suffix}"].mean())
            row[f"configuration_mae_{suffix}"] = float(errors.mean())
            row[f"wins_vs_normal_{suffix}"] = int(
                np.count_nonzero(candidate_errors < normal_errors)
            )
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    if min(
        args.replicates,
        args.population_replicates,
        args.workers,
        args.audit_replicates,
    ) <= 0:
        raise ValueError("Replicate, worker, and audit counts must be positive.")
    start = perf_counter()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_scenarios = generate_configuration_scenarios(
        args.scenario_seed,
        args.population_replicates,
    )
    seeds = _scenario_simulation_seeds(all_scenarios, args.simulation_seed)
    scenario_stop = (
        len(all_scenarios)
        if args.scenario_stop is None
        else args.scenario_stop
    )
    if not 0 <= args.scenario_start < scenario_stop <= len(all_scenarios):
        raise ValueError("Scenario slice is outside the generated scenario list.")
    scenarios = all_scenarios[args.scenario_start : scenario_stop]
    tasks = [
        (
            scenario,
            seeds[scenario.scenario_id],
            args.replicates,
            min(args.audit_replicates, args.replicates),
            args.multiple_starts,
        )
        for scenario in scenarios
    ]
    outputs = {}
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(_run_scenario, task): task[0].scenario_id
            for task in tasks
        }
        for future in as_completed(futures):
            outputs[futures[future]] = future.result()

    result_rows = []
    diagnostics = []
    p_value_archive = np.full(
        (len(scenarios), len(METHODS), args.replicates),
        np.nan,
    )
    for index, scenario in enumerate(scenarios):
        rows, p_values, scenario_diagnostics = outputs[scenario.scenario_id]
        result_rows.extend(rows)
        diagnostics.append(scenario_diagnostics)
        p_value_archive[index] = p_values

    scenario_results = pd.DataFrame(result_rows)
    configuration = _aggregate(
        scenario_results,
        ["configuration_id", "rows", "columns", "condition", "condition_label", "n_p", "n_q"],
    )
    regime = _aggregate(
        scenario_results,
        ["condition", "condition_label"],
    )
    overall = _overall(configuration)
    optimizer_diagnostics = pd.DataFrame(diagnostics)

    scenario_results.to_csv(args.output_dir / "scenario_results.csv", index=False)
    configuration.to_csv(args.output_dir / "configuration_summary.csv", index=False)
    regime.to_csv(args.output_dir / "regime_summary.csv", index=False)
    overall.to_csv(args.output_dir / "overall_summary.csv", index=False)
    optimizer_diagnostics.to_csv(
        args.output_dir / "optimizer_diagnostics.csv",
        index=False,
    )
    np.savez_compressed(
        args.output_dir / "null_pvalues.npz",
        p_values=p_value_archive,
        scenario_ids=np.asarray([scenario.scenario_id for scenario in scenarios]),
        methods=np.asarray(tuple(METHODS)),
    )
    metadata = {
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "configuration_count": int(
            scenario_results["configuration_id"].nunique()
        ),
        "scenario_start": args.scenario_start,
        "scenario_stop": scenario_stop,
        "population_replicates": args.population_replicates,
        "scenarios": len(scenarios),
        "null_replicates_per_scenario": args.replicates,
        "total_table_pairs": len(scenarios) * args.replicates,
        "workers": args.workers,
        "audit_replicates_per_scenario": args.audit_replicates,
        "forced_multiple_starts": args.multiple_starts,
        "methods": list(METHODS),
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(overall.to_string(index=False))
    print("Optimizer diagnostics:")
    print(
        optimizer_diagnostics[
            [
                "lrt_convergence_rate",
                "lrt_fallback_rate",
                "lrt_mean_seconds_per_fit",
                "audit_max_statistic_difference",
            ]
        ]
        .mean()
        .to_string()
    )
    print(f"Saved results to {args.output_dir}")


if __name__ == "__main__":
    main()
