#!/usr/bin/env python3
"""Compare analytic and jackknife MI centering on identical null tables."""

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
from scipy.stats import norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.statistics import jackknife_mi  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


ALPHAS = (0.10, 0.05, 0.01)
DEFAULT_SIMULATION_SEED = 2_026_080_502
METHODS = {
    "analytic_normal": "Analytic correction + Normal Wald",
    "analytic_simple": "Analytic correction + Simple Welch",
    "analytic_expanded": "Analytic correction + Expanded Welch",
    "jackknife_normal": "Jackknife correction + Normal Wald",
    "jackknife_simple": "Jackknife correction + Simple Welch",
    "jackknife_expanded": "Jackknife correction + Expanded Welch",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare analytic and jackknife MI bias correction on the fixed "
            "supervisor experiment populations."
        )
    )
    parser.add_argument(
        "--population-file",
        type=Path,
        default=(
            PROJECT_ROOT
            / "results"
            / "supervisor_practical"
            / "population_scenarios.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "jackknife_comparison",
    )
    parser.add_argument("--replicates", type=int, default=10_000)
    parser.add_argument("--batch-size", type=int, default=1_000)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    return parser.parse_args()


def _scenario_seeds(count: int, seed: int) -> list[int]:
    children = np.random.SeedSequence(seed).spawn(count)
    return [int(child.generate_state(1)[0]) for child in children]


def _simulate_scenario(
    scenario: pd.Series,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> tuple[list[dict], list[dict]]:
    rows = int(scenario["rows"])
    columns = int(scenario["columns"])
    n_p = int(scenario["n_p"])
    n_q = int(scenario["n_q"])
    probability_p = np.asarray(
        json.loads(scenario["probability_p_json"]), dtype=float
    )
    probability_q = np.asarray(
        json.loads(scenario["probability_q_json"]), dtype=float
    )
    true_delta = float(scenario["true_delta"])
    rng = np.random.default_rng(seed)

    counts = {
        method: {
            "valid": 0,
            "rejections": {alpha: 0 for alpha in ALPHAS},
        }
        for method in METHODS
    }
    centering = {
        "analytic": {"count": 0, "sum": 0.0, "square_sum": 0.0},
        "jackknife": {"count": 0, "sum": 0.0, "square_sum": 0.0},
    }
    standard_error_count = 0
    standard_error_sum = 0.0
    for start_index in range(0, replicates, batch_size):
        count = min(batch_size, replicates - start_index)
        table_p = rng.multinomial(
            n_p, probability_p.reshape(-1), size=count
        ).reshape(count, rows, columns)
        table_q = rng.multinomial(
            n_q, probability_q.reshape(-1), size=count
        ).reshape(count, rows, columns)

        values = differential_mi_pvalues(
            table_p,
            table_q,
            include_unbiased_sensitivity=False,
        )
        jackknife_delta = np.asarray(jackknife_mi(table_p)) - np.asarray(
            jackknife_mi(table_q)
        )

        standard_error = values["standard_error"]
        jackknife_statistic = np.divide(
            jackknife_delta,
            standard_error,
            out=np.full_like(jackknife_delta, np.nan, dtype=float),
            where=np.isfinite(standard_error) & (standard_error > 0),
        )
        jackknife_base_valid = (
            values["base_valid"]
            & np.isfinite(jackknife_delta)
            & np.isfinite(jackknife_statistic)
        )
        method_pvalues = {
            "analytic_normal": values["normal_p_value"],
            "analytic_simple": values["welch_p_value"],
            "analytic_expanded": values["expanded_welch_p_value"],
            "jackknife_normal": np.where(
                jackknife_base_valid,
                2.0 * norm.sf(np.abs(jackknife_statistic)),
                np.nan,
            ),
            "jackknife_simple": np.where(
                values["simple_valid"] & jackknife_base_valid,
                2.0
                * t.sf(
                    np.abs(jackknife_statistic),
                    df=values["welch_degrees_of_freedom"],
                ),
                np.nan,
            ),
            "jackknife_expanded": np.where(
                values["expanded_valid"] & jackknife_base_valid,
                2.0
                * t.sf(
                    np.abs(jackknife_statistic),
                    df=values["expanded_welch_degrees_of_freedom"],
                ),
                np.nan,
            ),
        }
        for method, pvalues in method_pvalues.items():
            valid = np.isfinite(pvalues)
            valid_pvalues = pvalues[valid]
            counts[method]["valid"] += int(valid_pvalues.size)
            for alpha in ALPHAS:
                counts[method]["rejections"][alpha] += int(
                    np.count_nonzero(valid_pvalues <= alpha)
                )

        base_valid = values["base_valid"]
        analytic_errors = values["delta_corrected"][base_valid] - true_delta
        jackknife_errors = jackknife_delta[jackknife_base_valid] - true_delta
        for name, errors in (
            ("analytic", analytic_errors),
            ("jackknife", jackknife_errors),
        ):
            centering[name]["count"] += int(errors.size)
            centering[name]["sum"] += float(np.sum(errors))
            centering[name]["square_sum"] += float(np.sum(errors**2))
        standard_error_count += int(np.count_nonzero(base_valid))
        standard_error_sum += float(np.sum(standard_error[base_valid]))

    common = {
        "scenario_id": scenario["scenario_id"],
        "regime": scenario["regime"],
        "regime_label": scenario["regime_label"],
        "variant": scenario["variant"],
        "rows": rows,
        "columns": columns,
        "n_p": n_p,
        "n_q": n_q,
        "target_mi": float(scenario["target_mi"]),
        "minimum_joint_expected_pair": float(
            scenario["minimum_joint_expected_pair"]
        ),
        "sample_size_ratio_q_to_p": float(
            scenario["sample_size_ratio_q_to_p"]
        ),
        "simulation_seed": seed,
        "replicates": replicates,
    }
    method_rows = []
    for method, label in METHODS.items():
        valid = counts[method]["valid"]
        row = {
            **common,
            "method": method,
            "method_label": label,
            "valid_replicates": valid,
            "valid_rate": valid / replicates,
        }
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            fpr = (
                counts[method]["rejections"][alpha] / valid
                if valid
                else np.nan
            )
            row[f"fpr_{suffix}"] = fpr
            row[f"absolute_fpr_error_{suffix}"] = abs(fpr - alpha)
        method_rows.append(row)

    mean_standard_error = (
        standard_error_sum / standard_error_count
        if standard_error_count
        else np.nan
    )
    centering_rows = []
    for correction, totals in centering.items():
        valid = totals["count"]
        mean_error = totals["sum"] / valid if valid else np.nan
        empirical_sd = (
            np.sqrt(
                max(
                    0.0,
                    (
                        totals["square_sum"]
                        - totals["sum"] ** 2 / valid
                    )
                    / (valid - 1),
                )
            )
            if valid > 1
            else np.nan
        )
        centering_rows.append(
            {
                **common,
                "correction": correction,
                "valid_replicates": valid,
                "mean_delta_error": mean_error,
                "mean_standard_error": mean_standard_error,
                "standardized_mean_bias": mean_error / mean_standard_error,
                "empirical_delta_sd": empirical_sd,
                "sd_to_mean_se_ratio": empirical_sd / mean_standard_error,
            }
        )
    return method_rows, centering_rows


def _summarize_methods(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (regime, regime_label, method, method_label), group in results.groupby(
        ["regime", "regime_label", "method", "method_label"], sort=False
    ):
        row = {
            "regime": regime,
            "regime_label": regime_label,
            "method": method,
            "method_label": method_label,
            "population_pairs": len(group),
            "mean_valid_rate": group["valid_rate"].mean(),
        }
        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            row[f"mean_fpr_{suffix}"] = group[f"fpr_{suffix}"].mean()
            row[f"mean_absolute_fpr_error_{suffix}"] = group[
                f"absolute_fpr_error_{suffix}"
            ].mean()
        rows.append(row)
    return pd.DataFrame(rows)


def _summarize_centering(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby(
            ["regime", "regime_label", "correction"], sort=False
        )
        .agg(
            population_pairs=("scenario_id", "size"),
            mean_absolute_standardized_bias=(
                "standardized_mean_bias",
                lambda values: np.mean(np.abs(values)),
            ),
            median_absolute_standardized_bias=(
                "standardized_mean_bias",
                lambda values: np.median(np.abs(values)),
            ),
            mean_sd_to_mean_se_ratio=("sd_to_mean_se_ratio", "mean"),
        )
        .reset_index()
    )


def _expanded_comparison(results: pd.DataFrame) -> pd.DataFrame:
    analytic = results[results["method"] == "analytic_expanded"].set_index(
        "scenario_id"
    )
    jackknife = results[results["method"] == "jackknife_expanded"].set_index(
        "scenario_id"
    )
    rows = []
    for alpha in ALPHAS:
        suffix = f"{int(round(alpha * 100)):02d}"
        analytic_error = analytic[f"absolute_fpr_error_{suffix}"]
        jackknife_error = jackknife[f"absolute_fpr_error_{suffix}"]
        difference = jackknife_error - analytic_error
        rows.append(
            {
                "alpha": alpha,
                "population_pairs": len(difference),
                "analytic_expanded_mean_absolute_fpr_error": (
                    analytic_error.mean()
                ),
                "jackknife_expanded_mean_absolute_fpr_error": (
                    jackknife_error.mean()
                ),
                "jackknife_minus_analytic_error": difference.mean(),
                "jackknife_wins": int(np.count_nonzero(difference < -1e-12)),
                "analytic_wins": int(np.count_nonzero(difference > 1e-12)),
                "ties": int(np.count_nonzero(np.abs(difference) <= 1e-12)),
            }
        )
    return pd.DataFrame(rows)


def _markdown(frame: pd.DataFrame, digits: int = 6) -> str:
    def format_value(value: object) -> str:
        if isinstance(value, (float, np.floating)):
            return "" if not np.isfinite(value) else f"{value:.{digits}f}"
        return str(value)

    header = "| " + " | ".join(frame.columns) + " |"
    separator = "| " + " | ".join("---" for _ in frame.columns) + " |"
    body = [
        "| " + " | ".join(format_value(value) for value in row) + " |"
        for row in frame.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *body])


def _write_report(
    output_dir: Path,
    comparison: pd.DataFrame,
    method_summary: pd.DataFrame,
    centering_summary: pd.DataFrame,
) -> None:
    overall_methods = (
        method_summary.groupby(["method", "method_label"], sort=False)
        .agg(
            mean_absolute_fpr_error_10=(
                "mean_absolute_fpr_error_10",
                "mean",
            ),
            mean_absolute_fpr_error_05=(
                "mean_absolute_fpr_error_05",
                "mean",
            ),
            mean_absolute_fpr_error_01=(
                "mean_absolute_fpr_error_01",
                "mean",
            ),
        )
        .reset_index()
    )
    report = [
        "# Jackknife Centering Comparison",
        "",
        "The experiment changes only the MI bias correction. The standard "
        "error and both Welch degrees-of-freedom calculations are identical "
        "for the analytic and jackknife versions, and every method is applied "
        "to the same simulated table pairs.",
        "",
        "## Expanded Welch comparison",
        "",
        _markdown(comparison),
        "",
        "## Overall method calibration",
        "",
        _markdown(overall_methods),
        "",
        "## Centering diagnostics by regime",
        "",
        _markdown(centering_summary),
        "",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.replicates <= 1 or args.batch_size <= 0:
        raise ValueError("Replicates must exceed one and batch size must be positive.")

    populations = pd.read_csv(args.population_file)
    required = {
        "scenario_id",
        "rows",
        "columns",
        "n_p",
        "n_q",
        "true_delta",
        "probability_p_json",
        "probability_q_json",
        "regime",
        "regime_label",
        "variant",
        "target_mi",
        "minimum_joint_expected_pair",
        "sample_size_ratio_q_to_p",
    }
    missing = required.difference(populations.columns)
    if missing:
        raise ValueError(f"Population file is missing columns: {sorted(missing)}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    seeds = _scenario_seeds(len(populations), args.simulation_seed)
    method_rows = []
    centering_rows = []
    start = perf_counter()
    for (_, scenario), seed in zip(populations.iterrows(), seeds):
        scenario_methods, scenario_centering = _simulate_scenario(
            scenario,
            replicates=args.replicates,
            batch_size=args.batch_size,
            seed=seed,
        )
        method_rows.extend(scenario_methods)
        centering_rows.extend(scenario_centering)

    scenario_results = pd.DataFrame(method_rows)
    centering_results = pd.DataFrame(centering_rows)
    method_summary = _summarize_methods(scenario_results)
    centering_summary = _summarize_centering(centering_results)
    comparison = _expanded_comparison(scenario_results)

    scenario_results.to_csv(args.output_dir / "scenario_results.csv", index=False)
    centering_results.to_csv(
        args.output_dir / "centering_diagnostics.csv", index=False
    )
    method_summary.to_csv(args.output_dir / "regime_summary.csv", index=False)
    centering_summary.to_csv(
        args.output_dir / "centering_summary.csv", index=False
    )
    comparison.to_csv(
        args.output_dir / "expanded_comparison.csv", index=False
    )
    _write_report(
        args.output_dir,
        comparison,
        method_summary,
        centering_summary,
    )

    metadata = {
        "population_file": str(args.population_file),
        "population_pairs": len(populations),
        "replicates_per_population": args.replicates,
        "batch_size": args.batch_size,
        "simulation_seed": args.simulation_seed,
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )

    print(comparison.to_string(index=False))
    print(f"Saved comparison to {args.output_dir}")


if __name__ == "__main__":
    main()
