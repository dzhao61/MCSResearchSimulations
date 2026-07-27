#!/usr/bin/env python3
"""Run the pre-specified constrained-profile differential-MI pilot."""

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
from scipy.optimize import brentq
from scipy.special import xlogy
from scipy.stats import binomtest, norm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.inference import compare_tables
from differential_mi.random_validation import (
    RandomScenario,
    generate_random_scenarios,
    scenario_diagnostics,
)
from differential_mi.statistics import influence_variance, plugin_mi
from profile_differential_mi.profile import profile_equal_mi_test


EASY_SCENARIO_IDS = (
    "random_2x2_d0",
    "random_3x3_d0",
    "random_4x6_d0",
    "random_5x5_d0",
)
HARD_SCENARIO_IDS = (
    "random_2x5_d2",
    "random_3x3_d4",
    "random_4x6_d5",
    "random_5x10_d5",
)
METHOD_COLUMNS = {
    "wald_analytic": "wald_analytic_p",
    "profile_lr": "lr_p_value",
    "profile_pearson": "pearson_p_value",
    "profile_cr_2_3": "cr_2_3_p_value",
}
DEFAULT_SCENARIO_SEEDS = (2026072501, 2026072601)
DEFAULT_SIMULATION_SEED = 2026072701


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "screen", "focused"), default="smoke")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--power-replicates", type=int)
    parser.add_argument("--permutation-pairs", type=int)
    parser.add_argument("--permutations", type=int, default=999)
    parser.add_argument("--scenario-seed", type=int, action="append", dest="scenario_seeds")
    parser.add_argument("--simulation-seed", type=int, default=DEFAULT_SIMULATION_SEED)
    return parser.parse_args()


def _mi(probability: np.ndarray) -> float:
    p = np.asarray(probability, dtype=float)
    row = p.sum(axis=1)
    column = p.sum(axis=0)
    return float(
        np.sum(xlogy(p, p))
        - np.sum(xlogy(row, row))
        - np.sum(xlogy(column, column))
    )


def _lower_mi(probability: np.ndarray, target: float) -> np.ndarray:
    independence = np.outer(probability.sum(axis=1), probability.sum(axis=0))
    if target <= 0:
        return independence

    def residual(weight: float) -> float:
        candidate = independence + weight * (probability - independence)
        return _mi(candidate) - target

    weight = brentq(residual, 0.0, 1.0, xtol=1e-13, rtol=1e-13)
    return independence + weight * (probability - independence)


def _wald_analytic_p(table_p: np.ndarray, table_q: np.ndarray) -> float:
    n_p = int(table_p.sum())
    n_q = int(table_q.sum())
    degrees_of_freedom = (table_p.shape[0] - 1) * (table_p.shape[1] - 1)
    delta = (
        float(plugin_mi(table_p))
        - degrees_of_freedom / (2.0 * n_p)
        - float(plugin_mi(table_q))
        + degrees_of_freedom / (2.0 * n_q)
    )
    standard_error = np.sqrt(
        float(influence_variance(table_p)) / n_p
        + float(influence_variance(table_q)) / n_q
    )
    if not np.isfinite(standard_error) or standard_error <= 0:
        return float("nan")
    return float(2.0 * norm.sf(abs(delta / standard_error)))


def _run_scenario(
    scenario: RandomScenario,
    *,
    scenario_seed: int,
    simulation_seed: int,
    replicates: int,
    power_replicates: int,
    permutation_pairs: int,
    permutations: int,
) -> tuple[list[dict], list[dict], list[dict]]:
    rng = np.random.default_rng(simulation_seed)
    null_rows: list[dict] = []
    runtime_rows: list[dict] = []
    for replicate in range(replicates):
        table_p = rng.multinomial(
            scenario.n_p, scenario.probability_p.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q, scenario.probability_q.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)

        wald_start = perf_counter()
        wald_p = _wald_analytic_p(table_p, table_q)
        wald_seconds = perf_counter() - wald_start
        profile = profile_equal_mi_test(table_p, table_q)
        row = {
            "scenario_seed": scenario_seed,
            "scenario_id": scenario.scenario_id,
            "scenario_key": f"{scenario_seed}:{scenario.scenario_id}",
            "subset": (
                "easy"
                if scenario.scenario_id in EASY_SCENARIO_IDS
                else "hard"
            ),
            "replicate": replicate,
            "simulation_seed": simulation_seed,
            "wald_analytic_p": wald_p,
            "wald_elapsed_seconds": wald_seconds,
            "zero_fraction_p": float(np.mean(table_p == 0)),
            "zero_fraction_q": float(np.mean(table_q == 0)),
            "table_p_json": json.dumps(table_p.tolist(), separators=(",", ":")),
            "table_q_json": json.dumps(table_q.tolist(), separators=(",", ":")),
        }
        row.update(profile.to_dict())
        null_rows.append(row)

        if replicate < permutation_pairs:
            permutation_rng = np.random.default_rng(
                np.random.SeedSequence(
                    [simulation_seed, replicate, 99173]
                )
            )
            permutation = compare_tables(
                table_p,
                table_q,
                permutations=permutations,
                rng=permutation_rng,
            )
            runtime_rows.append(
                {
                    "scenario_seed": scenario_seed,
                    "scenario_id": scenario.scenario_id,
                    "scenario_key": f"{scenario_seed}:{scenario.scenario_id}",
                    "subset": row["subset"],
                    "replicate": replicate,
                    "profile_seconds": profile.elapsed_seconds,
                    "wald_seconds": wald_seconds,
                    "permutation_seconds": permutation.permutation_seconds,
                    "permutations": permutations,
                    "student_perm_analytic_p": permutation.student_perm_analytic_p,
                }
            )

    power_rows: list[dict] = []
    if power_replicates > 0:
        population_se = np.sqrt(
            float(influence_variance(scenario.probability_p)) / scenario.n_p
            + float(influence_variance(scenario.probability_q)) / scenario.n_q
        )
        target_difference = min(
            0.6 * scenario.target_mi,
            2.0 * population_se,
        )
        alternative_q = _lower_mi(
            scenario.probability_q,
            scenario.target_mi - target_difference,
        )
        achieved_difference = _mi(scenario.probability_p) - _mi(alternative_q)
        for replicate in range(power_replicates):
            table_p = rng.multinomial(
                scenario.n_p, scenario.probability_p.reshape(-1)
            ).reshape(scenario.rows, scenario.columns)
            table_q = rng.multinomial(
                scenario.n_q, alternative_q.reshape(-1)
            ).reshape(scenario.rows, scenario.columns)
            profile = profile_equal_mi_test(table_p, table_q)
            row = {
                "scenario_seed": scenario_seed,
                "scenario_id": scenario.scenario_id,
                "scenario_key": f"{scenario_seed}:{scenario.scenario_id}",
                "subset": (
                    "easy"
                    if scenario.scenario_id in EASY_SCENARIO_IDS
                    else "hard"
                ),
                "replicate": replicate,
                "true_delta": achieved_difference,
                "wald_analytic_p": _wald_analytic_p(table_p, table_q),
            }
            row.update(profile.to_dict())
            power_rows.append(row)
    return null_rows, runtime_rows, power_rows


def _wilson(rejections: int, total: int) -> tuple[float, float]:
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=0.95, method="wilson"
    )
    return float(interval.low), float(interval.high)


def _summarize_null(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scenario_key, group in frame.groupby("scenario_key", sort=False):
        row = {
            "scenario_key": scenario_key,
            "scenario_seed": int(group["scenario_seed"].iloc[0]),
            "scenario_id": group["scenario_id"].iloc[0],
            "subset": group["subset"].iloc[0],
            "replicates": len(group),
            "trustworthy_rate": float(group["trustworthy"].mean()),
            "hit_logit_bound_rate": float(group["hit_logit_bound"].mean()),
            "mean_constraint_residual": float(group["constraint_residual"].mean()),
            "maximum_constraint_residual": float(group["constraint_residual"].max()),
            "mean_relative_kkt_residual": float(group["relative_kkt_residual"].mean()),
            "maximum_relative_kkt_residual": float(group["relative_kkt_residual"].max()),
            "mean_zero_fraction_p": float(group["zero_fraction_p"].mean()),
            "mean_zero_fraction_q": float(group["zero_fraction_q"].mean()),
            "mean_profile_seconds": float(group["elapsed_seconds"].mean()),
            "median_profile_seconds": float(group["elapsed_seconds"].median()),
            "mean_wald_seconds": float(group["wald_elapsed_seconds"].mean()),
        }
        for method, column in METHOD_COLUMNS.items():
            valid = group[column].notna()
            if method.startswith("profile"):
                valid &= group["trustworthy"]
            values = group.loc[valid, column]
            row[f"{method}_valid_rate"] = float(valid.mean())
            for alpha_label, alpha in (("10", 0.10), ("05", 0.05)):
                rejections = int((values <= alpha).sum())
                rate = rejections / len(values) if len(values) else float("nan")
                low, high = (
                    _wilson(rejections, len(values))
                    if len(values)
                    else (float("nan"), float("nan"))
                )
                row[f"{method}_fpr_{alpha_label}"] = rate
                row[f"{method}_fpr_{alpha_label}_low"] = low
                row[f"{method}_fpr_{alpha_label}_high"] = high
        rows.append(row)
    return pd.DataFrame(rows)


def _method_summary(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for subset in ("easy", "hard", "all"):
        selected = summary if subset == "all" else summary[summary["subset"] == subset]
        for method in METHOD_COLUMNS:
            row = {
                "subset": subset,
                "method": method,
                "scenarios": len(selected),
                "mean_valid_rate": float(selected[f"{method}_valid_rate"].mean()),
            }
            for alpha_label, alpha in (("10", 0.10), ("05", 0.05)):
                rates = selected[f"{method}_fpr_{alpha_label}"]
                row[f"mean_absolute_fpr_error_{alpha_label}"] = float(
                    np.mean(np.abs(rates - alpha))
                )
                row[f"mean_fpr_{alpha_label}"] = float(rates.mean())
                row[f"minimum_fpr_{alpha_label}"] = float(rates.min())
                row[f"maximum_fpr_{alpha_label}"] = float(rates.max())
            rows.append(row)
    return pd.DataFrame(rows)


def _power_summary(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    rows = []
    for method, column in METHOD_COLUMNS.items():
        valid = frame[column].notna()
        if method.startswith("profile"):
            valid &= frame["trustworthy"]
        rows.append(
            {
                "method": method,
                "replicates": int(valid.sum()),
                "valid_rate": float(valid.mean()),
                "rejection_rate_05": float((frame.loc[valid, column] <= 0.05).mean()),
                "mean_true_delta": float(frame.loc[valid, "true_delta"].mean()),
            }
        )
    return pd.DataFrame(rows)


def _runtime_summary(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    rows = []
    for subset in ("easy", "hard", "all"):
        selected = frame if subset == "all" else frame[frame["subset"] == subset]
        rows.append(
            {
                "subset": subset,
                "pairs": len(selected),
                "median_wald_ms": 1000.0 * float(selected["wald_seconds"].median()),
                "median_profile_ms": 1000.0 * float(selected["profile_seconds"].median()),
                "median_permutation_ms": 1000.0
                * float(selected["permutation_seconds"].median()),
                "profile_over_permutation": float(
                    np.median(
                        selected["profile_seconds"]
                        / selected["permutation_seconds"]
                    )
                ),
            }
        )
    return pd.DataFrame(rows)


def _markdown_table(frame: pd.DataFrame, digits: int) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, (float, np.floating)):
                rendered.append(f"{value:.{digits}f}")
            else:
                rendered.append(str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def _scenario_frame(entries: list[tuple[int, RandomScenario]]) -> pd.DataFrame:
    rows = []
    for scenario_seed, scenario in entries:
        row = scenario_diagnostics(scenario)
        row["scenario_seed"] = scenario_seed
        row["scenario_key"] = f"{scenario_seed}:{scenario.scenario_id}"
        row["subset"] = (
            "easy" if scenario.scenario_id in EASY_SCENARIO_IDS else "hard"
        )
        row["probability_p_json"] = json.dumps(scenario.probability_p.tolist())
        row["probability_q_json"] = json.dumps(scenario.probability_q.tolist())
        rows.append(row)
    return pd.DataFrame(rows)


def _write_report(
    output_dir: Path,
    method_summary: pd.DataFrame,
    runtime_summary: pd.DataFrame,
    power_summary: pd.DataFrame,
    trustworthy_rate: float,
) -> None:
    hard = method_summary[method_summary["subset"] == "hard"].set_index("method")
    easy = method_summary[method_summary["subset"] == "easy"].set_index("method")
    profile_methods = [name for name in METHOD_COLUMNS if name.startswith("profile")]
    selected_method = min(
        profile_methods,
        key=lambda name: hard.loc[name, "mean_absolute_fpr_error_05"],
    )
    wald_hard = float(hard.loc["wald_analytic", "mean_absolute_fpr_error_05"])
    profile_hard = float(hard.loc[selected_method, "mean_absolute_fpr_error_05"])
    improvement = (
        (wald_hard - profile_hard) / wald_hard if wald_hard > 0 else float("-inf")
    )
    easy_degradation = float(
        easy.loc[selected_method, "mean_absolute_fpr_error_05"]
        - easy.loc["wald_analytic", "mean_absolute_fpr_error_05"]
    )
    runtime_all = runtime_summary[runtime_summary["subset"] == "all"].iloc[0]
    runtime_pass = bool(runtime_all["profile_over_permutation"] < 1.0)
    power_pass = True
    if not power_summary.empty:
        power = power_summary.set_index("method")
        power_pass = bool(
            power.loc[selected_method, "rejection_rate_05"]
            >= power.loc["wald_analytic", "rejection_rate_05"] - 0.10
        )
    criteria = {
        "hard_calibration_improvement_at_least_20pct": improvement >= 0.20,
        "easy_mae_degradation_at_most_0_005": easy_degradation <= 0.005,
        "trustworthy_fit_rate_at_least_0_995": trustworthy_rate >= 0.995,
        "median_faster_than_999_permutations": runtime_pass,
        "power_not_more_than_0_10_below_wald": power_pass,
    }
    decision = "GO" if all(criteria.values()) else "NO-GO"

    method_table = _markdown_table(
        method_summary[
            [
                "subset",
                "method",
                "mean_absolute_fpr_error_05",
                "mean_fpr_05",
                "mean_valid_rate",
            ]
        ],
        5,
    )
    runtime_table = _markdown_table(runtime_summary, 3)
    power_table = (
        _markdown_table(power_summary, 4)
        if not power_summary.empty
        else "Power was not run in this profile."
    )
    criterion_lines = [
        f"- [{'x' if passed else ' '}] `{name}`"
        for name, passed in criteria.items()
    ]
    lines = [
        "# Constrained-Profile Go/No-Go Result",
        "",
        f"## Decision: {decision}",
        "",
        f"The best hard-subset profile method was `{selected_method}`. Its alpha=0.05",
        f"FPR MAE was `{profile_hard:.5f}` versus `{wald_hard:.5f}` for the",
        f"bias-corrected Wald baseline, a relative improvement of `{improvement:.1%}`.",
        f"Its easy-subset MAE change was `{easy_degradation:+.5f}`.",
        "",
        *criterion_lines,
        "",
        "This decision applies to the pilot protocol only. Monte Carlo uncertainty",
        "and any failed criterion must be considered before making a thesis claim.",
        "",
        "## Calibration",
        "",
        method_table,
        "",
        "## Runtime",
        "",
        runtime_table,
        "",
        "The permutation comparator is the existing optimized table-level",
        "studentized differential-MI permutation implementation with 999 draws.",
        "JIDT does not provide this two-sample equal-MI test.",
        "",
        "## Power",
        "",
        power_table,
        "",
        "## Numerical Audit",
        "",
        f"Overall trustworthy constrained-fit rate: `{trustworthy_rate:.5f}`.",
        "Boundary hits are retained as diagnostics because multinomial MLEs can",
        "legitimately lie on the simplex boundary; separate tests check statistic",
        "stability as the numerical logit bound changes.",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    settings = {
        "smoke": (12, 4, 2),
        "screen": (100, 20, 5),
        "focused": (1000, 100, 10),
    }
    defaults = settings[args.profile]
    replicates = args.replicates or defaults[0]
    power_replicates = (
        args.power_replicates
        if args.power_replicates is not None
        else defaults[1]
    )
    permutation_pairs = (
        args.permutation_pairs
        if args.permutation_pairs is not None
        else defaults[2]
    )
    scenario_seeds = args.scenario_seeds or list(DEFAULT_SCENARIO_SEEDS)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    selected_ids = set(EASY_SCENARIO_IDS + HARD_SCENARIO_IDS)
    entries: list[tuple[int, RandomScenario]] = []
    for scenario_seed in scenario_seeds:
        entries.extend(
            (scenario_seed, scenario)
            for scenario in generate_random_scenarios(scenario_seed)
            if scenario.scenario_id in selected_ids
        )
    scenarios = _scenario_frame(entries)
    scenarios.to_csv(args.output_dir / "scenarios.csv", index=False)

    child_seeds = np.random.SeedSequence(args.simulation_seed).spawn(len(entries))
    jobs = [
        (
            scenario,
            scenario_seed,
            int(child.generate_state(1)[0]),
        )
        for (scenario_seed, scenario), child in zip(entries, child_seeds)
    ]
    null_rows: list[dict] = []
    runtime_rows: list[dict] = []
    power_rows: list[dict] = []
    run_start = perf_counter()
    if args.workers == 1:
        for completed, (scenario, scenario_seed, simulation_seed) in enumerate(
            jobs, 1
        ):
            scenario_null, scenario_runtime, scenario_power = _run_scenario(
                scenario,
                scenario_seed=scenario_seed,
                simulation_seed=simulation_seed,
                replicates=replicates,
                power_replicates=power_replicates,
                permutation_pairs=permutation_pairs,
                permutations=args.permutations,
            )
            null_rows.extend(scenario_null)
            runtime_rows.extend(scenario_runtime)
            power_rows.extend(scenario_power)
            key = f"{scenario_seed}:{scenario.scenario_id}"
            print(f"[{completed}/{len(jobs)}] {key}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    _run_scenario,
                    scenario,
                    scenario_seed=scenario_seed,
                    simulation_seed=simulation_seed,
                    replicates=replicates,
                    power_replicates=power_replicates,
                    permutation_pairs=permutation_pairs,
                    permutations=args.permutations,
                ): f"{scenario_seed}:{scenario.scenario_id}"
                for scenario, scenario_seed, simulation_seed in jobs
            }
            completed = 0
            for future in as_completed(futures):
                key = futures[future]
                scenario_null, scenario_runtime, scenario_power = future.result()
                null_rows.extend(scenario_null)
                runtime_rows.extend(scenario_runtime)
                power_rows.extend(scenario_power)
                completed += 1
                print(f"[{completed}/{len(futures)}] {key}", flush=True)

    null_frame = pd.DataFrame(null_rows)
    runtime_frame = pd.DataFrame(runtime_rows)
    power_frame = pd.DataFrame(power_rows)
    null_frame.to_csv(
        args.output_dir / "null_replicates.csv.gz",
        index=False,
        compression="gzip",
    )
    runtime_frame.to_csv(args.output_dir / "runtime_pairs.csv", index=False)
    if not power_frame.empty:
        power_frame.to_csv(
            args.output_dir / "power_replicates.csv.gz",
            index=False,
            compression="gzip",
        )

    null_summary = _summarize_null(null_frame)
    null_summary = scenarios.merge(
        null_summary,
        on=["scenario_key", "scenario_seed", "scenario_id", "subset"],
    )
    methods = _method_summary(null_summary)
    runtimes = _runtime_summary(runtime_frame)
    powers = _power_summary(power_frame)
    null_summary.to_csv(args.output_dir / "null_summary.csv", index=False)
    methods.to_csv(args.output_dir / "method_summary.csv", index=False)
    runtimes.to_csv(args.output_dir / "runtime_summary.csv", index=False)
    if not powers.empty:
        powers.to_csv(args.output_dir / "power_summary.csv", index=False)

    trustworthy_rate = float(null_frame["trustworthy"].mean())
    _write_report(
        args.output_dir,
        methods,
        runtimes,
        powers,
        trustworthy_rate,
    )
    metadata = {
        "profile": args.profile,
        "scenario_seeds": scenario_seeds,
        "simulation_seed": args.simulation_seed,
        "replicates_per_scenario": replicates,
        "power_replicates_per_scenario": power_replicates,
        "permutation_pairs_per_scenario": permutation_pairs,
        "permutations": args.permutations,
        "workers": args.workers,
        "scenarios": len(entries),
        "elapsed_seconds": perf_counter() - run_start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
