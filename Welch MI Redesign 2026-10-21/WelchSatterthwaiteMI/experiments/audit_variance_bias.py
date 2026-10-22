#!/usr/bin/env python3
"""Diagnose variance bias and finite-df references for differential MI.

This is a post-hoc diagnostic, not a confirmatory validation runner. It uses
known population quantities to distinguish failures in the estimated standard
error from failures in the reference distribution.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.random_validation import (  # noqa: E402
    generate_random_scenarios,
)
from differential_mi.statistics import influence_variance  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


DEFAULT_DECISIVE_SCENARIOS = (
    PROJECT_ROOT / "results" / "decisive" / "scenarios.csv"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "variance_bias_audit"
DEFAULT_FRESH_SCENARIO_SEED = 2_026_080_301
DEFAULT_SIMULATION_SEED = 2_026_080_302
ALPHAS = (0.10, 0.05, 0.01)
HARD_SHAPES = frozenset({(2, 2), (2, 5), (3, 7), (4, 6), (5, 5), (5, 10)})


@dataclass(frozen=True)
class AuditScenario:
    source: str
    scenario_key: str
    scenario_id: str
    design_index: int
    rows: int
    columns: int
    n_p: int
    n_q: int
    probability_p: np.ndarray
    probability_q: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--decisive-scenarios",
        type=Path,
        default=DEFAULT_DECISIVE_SCENARIOS,
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--decisive-replicates", type=int, default=20_000)
    parser.add_argument("--fresh-replicates", type=int, default=10_000)
    parser.add_argument(
        "--fresh-scenario-seed",
        type=int,
        default=DEFAULT_FRESH_SCENARIO_SEED,
    )
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    return parser.parse_args()


def _from_decisive(path: Path) -> list[AuditScenario]:
    frame = pd.read_csv(path)
    frame = frame.loc[frame["stage"].eq("hard")].copy()
    scenarios = []
    for row in frame.itertuples(index=False):
        probability_p = np.asarray(json.loads(row.probability_p_json), dtype=float)
        probability_q = np.asarray(json.loads(row.probability_q_json), dtype=float)
        scenarios.append(
            AuditScenario(
                source="decisive_hard",
                scenario_key=str(row.scenario_key),
                scenario_id=str(row.scenario_id),
                design_index=int(row.design_index),
                rows=int(row.rows),
                columns=int(row.columns),
                n_p=int(row.n_p),
                n_q=int(row.n_q),
                probability_p=probability_p,
                probability_q=probability_q,
            )
        )
    return scenarios


def _fresh_scenarios(seed: int) -> list[AuditScenario]:
    result = []
    for scenario in generate_random_scenarios(seed):
        result.append(
            AuditScenario(
                source="fresh_holdout",
                scenario_key=f"fresh:{seed}:{scenario.scenario_id}",
                scenario_id=scenario.scenario_id,
                design_index=scenario.design_index,
                rows=scenario.rows,
                columns=scenario.columns,
                n_p=scenario.n_p,
                n_q=scenario.n_q,
                probability_p=scenario.probability_p,
                probability_q=scenario.probability_q,
            )
        )
    return result


def _score_moment_diagnostics(
    tables: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return local-kurtosis df, variance-functional IF df, and IF variance."""
    counts = np.asarray(tables, dtype=float)
    totals = counts.sum(axis=(-2, -1), keepdims=True)
    probability = counts / totals
    row = probability.sum(axis=-1, keepdims=True)
    column = probability.sum(axis=-2, keepdims=True)

    log_probability = np.zeros_like(probability)
    log_row = np.zeros_like(row)
    log_column = np.zeros_like(column)
    np.log(probability, out=log_probability, where=probability > 0)
    np.log(row, out=log_row, where=row > 0)
    np.log(column, out=log_column, where=column > 0)
    score = log_probability - log_row - log_column

    mean = np.sum(probability * score, axis=(-2, -1))
    centered = score - mean[..., None, None]
    variance = np.sum(probability * centered**2, axis=(-2, -1))
    fourth = np.sum(probability * centered**4, axis=(-2, -1))
    local_variance_if = fourth - variance**2

    row_numerator = np.sum(probability * score, axis=-1)
    column_numerator = np.sum(probability * score, axis=-2)
    row_probability = row[..., 0]
    column_probability = column[..., 0, :]
    row_score_mean = np.divide(
        row_numerator,
        row_probability,
        out=np.zeros_like(row_numerator),
        where=row_probability > 0,
    )
    column_score_mean = np.divide(
        column_numerator,
        column_probability,
        out=np.zeros_like(column_numerator),
        where=column_probability > 0,
    )
    second_moment = variance + mean**2
    variance_if = (
        score**2
        - second_moment[..., None, None]
        + 2.0
        * (
            score
            - row_score_mean[..., :, None]
            - column_score_mean[..., None, :]
            + mean[..., None, None]
        )
        - 2.0 * mean[..., None, None] * centered
    )
    variance_if_mean = np.sum(probability * variance_if, axis=(-2, -1))
    variance_if_variance = np.sum(
        probability
        * (variance_if - variance_if_mean[..., None, None]) ** 2,
        axis=(-2, -1),
    )

    sample_size = totals[..., 0, 0]
    numerator = 2.0 * sample_size * variance**2
    local_df = np.divide(
        numerator,
        local_variance_if,
        out=np.full_like(variance, np.nan),
        where=np.isfinite(local_variance_if) & (local_variance_if > 0),
    )
    variance_if_df = np.divide(
        numerator,
        variance_if_variance,
        out=np.full_like(variance, np.nan),
        where=np.isfinite(variance_if_variance) & (variance_if_variance > 0),
    )
    return local_df, variance_if_df, variance_if_variance


def _population_variance_if_df(
    probability: np.ndarray,
    sample_size: int,
) -> float:
    _, component_df, _ = _score_moment_diagnostics(
        (probability * sample_size)[None, ...]
    )
    return float(component_df[0])


def _combine_df(
    component_p: np.ndarray,
    component_q: np.ndarray,
    df_p: np.ndarray,
    df_q: np.ndarray,
) -> np.ndarray:
    numerator = (component_p + component_q) ** 2
    denominator = component_p**2 / df_p + component_q**2 / df_q
    return np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan),
        where=np.isfinite(denominator) & (denominator > 0),
    )


def _empirical_df(values: np.ndarray) -> float:
    mean = float(np.mean(values))
    variance = float(np.var(values, ddof=1))
    return 2.0 * mean**2 / variance if variance > 0 else np.nan


def _fpr(p_values: np.ndarray, alpha: float) -> float:
    valid = np.isfinite(p_values)
    return float(np.mean(p_values[valid] <= alpha)) if np.any(valid) else np.nan


def _audit_scenario(
    scenario: AuditScenario,
    *,
    replicates: int,
    simulation_seed: int,
) -> dict[str, int | float | str]:
    rng = np.random.default_rng(simulation_seed)
    table_p = rng.multinomial(
        scenario.n_p,
        scenario.probability_p.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)
    table_q = rng.multinomial(
        scenario.n_q,
        scenario.probability_q.reshape(-1),
        size=replicates,
    ).reshape(replicates, scenario.rows, scenario.columns)

    values = differential_mi_pvalues(table_p, table_q)
    delta = values["delta_corrected"]
    variance_p = values["influence_variance_p"]
    variance_q = values["influence_variance_q"]
    component_p = variance_p / scenario.n_p
    component_q = variance_q / scenario.n_q
    estimated_se2 = component_p + component_q

    true_variance_p = float(influence_variance(scenario.probability_p))
    true_variance_q = float(influence_variance(scenario.probability_q))
    true_component_p = true_variance_p / scenario.n_p
    true_component_q = true_variance_q / scenario.n_q
    true_se2 = true_component_p + true_component_q

    local_df_p, variance_if_df_p, _ = _score_moment_diagnostics(table_p)
    local_df_q, variance_if_df_q, _ = _score_moment_diagnostics(table_q)
    local_total_df = _combine_df(
        component_p, component_q, local_df_p, local_df_q
    )
    variance_if_total_df = _combine_df(
        component_p,
        component_q,
        variance_if_df_p,
        variance_if_df_q,
    )
    statistic = values["statistic"]
    local_p = 2.0 * t.sf(np.abs(statistic), df=local_total_df)
    variance_if_p = 2.0 * t.sf(
        np.abs(statistic), df=variance_if_total_df
    )
    oracle_statistic = delta / np.sqrt(true_se2)
    oracle_p = 2.0 * norm.sf(np.abs(oracle_statistic))

    population_df_p = _population_variance_if_df(
        scenario.probability_p, scenario.n_p
    )
    population_df_q = _population_variance_if_df(
        scenario.probability_q, scenario.n_q
    )
    population_total_df = float(
        _combine_df(
            np.asarray(true_component_p),
            np.asarray(true_component_q),
            np.asarray(population_df_p),
            np.asarray(population_df_q),
        )
    )

    row: dict[str, int | float | str] = {
        "source": scenario.source,
        "scenario_key": scenario.scenario_key,
        "scenario_id": scenario.scenario_id,
        "design_index": scenario.design_index,
        "rows": scenario.rows,
        "columns": scenario.columns,
        "n_p": scenario.n_p,
        "n_q": scenario.n_q,
        "replicates": replicates,
        "simulation_seed": simulation_seed,
        "true_variance_p": true_variance_p,
        "mean_estimated_variance_p": float(np.mean(variance_p)),
        "estimated_to_true_variance_ratio_p": float(
            np.mean(variance_p) / true_variance_p
        ),
        "true_variance_q": true_variance_q,
        "mean_estimated_variance_q": float(np.mean(variance_q)),
        "estimated_to_true_variance_ratio_q": float(
            np.mean(variance_q) / true_variance_q
        ),
        "estimated_to_true_se2_ratio": float(np.mean(estimated_se2) / true_se2),
        "empirical_delta_variance_to_true_se2": float(
            np.var(delta, ddof=1) / true_se2
        ),
        "mean_corrected_delta_in_se_units": float(
            np.mean(delta) / np.sqrt(true_se2)
        ),
        "correlation_delta_estimated_se2": float(
            np.corrcoef(delta, estimated_se2)[0, 1]
        ),
        "empirical_component_df_p": _empirical_df(component_p),
        "population_variance_if_df_p": population_df_p,
        "median_plugin_variance_if_df_p": float(
            np.nanmedian(variance_if_df_p)
        ),
        "empirical_component_df_q": _empirical_df(component_q),
        "population_variance_if_df_q": population_df_q,
        "median_plugin_variance_if_df_q": float(
            np.nanmedian(variance_if_df_q)
        ),
        "empirical_total_df": _empirical_df(estimated_se2),
        "population_variance_if_total_df": population_total_df,
        "median_naive_total_df": float(
            np.nanmedian(values["welch_degrees_of_freedom"])
        ),
        "median_local_kurtosis_total_df": float(np.nanmedian(local_total_df)),
        "median_plugin_variance_if_total_df": float(
            np.nanmedian(variance_if_total_df)
        ),
        "studentized_abs_q95": float(np.nanquantile(np.abs(statistic), 0.95)),
        "studentized_abs_q99": float(np.nanquantile(np.abs(statistic), 0.99)),
    }
    methods = {
        "normal": values["normal_p_value"],
        "naive_welch": values["welch_p_value"],
        "local_kurtosis": local_p,
        "variance_if": variance_if_p,
        "oracle_variance_normal": oracle_p,
    }
    for alpha in ALPHAS:
        label = f"{int(round(alpha * 100)):02d}"
        for method, p_values in methods.items():
            fpr = _fpr(p_values, alpha)
            row[f"{method}_fpr_{label}"] = fpr
            row[f"{method}_error_{label}"] = abs(fpr - alpha)
    for method, p_values in methods.items():
        row[f"{method}_valid_rate"] = float(np.mean(np.isfinite(p_values)))
    return row


def _summarize(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    methods = (
        "normal",
        "naive_welch",
        "local_kurtosis",
        "variance_if",
        "oracle_variance_normal",
    )
    groups = [(source, group) for source, group in frame.groupby("source", sort=False)]
    fresh_hard = frame.loc[
        frame["source"].eq("fresh_holdout")
        & frame["design_index"].eq(5)
        & pd.Series(
            list(zip(frame["rows"], frame["columns"])),
            index=frame.index,
        ).isin(HARD_SHAPES)
    ]
    groups.append(("fresh_holdout_hard", fresh_hard))
    for source, group in groups:
        for alpha in ALPHAS:
            label = f"{int(round(alpha * 100)):02d}"
            normal_error = group[f"normal_error_{label}"]
            for method in methods:
                error = group[f"{method}_error_{label}"]
                rows.append(
                    {
                        "source": source,
                        "alpha": alpha,
                        "method": method,
                        "scenarios": len(group),
                        "mean_fpr": float(group[f"{method}_fpr_{label}"].mean()),
                        "mean_absolute_fpr_error": float(error.mean()),
                        "median_absolute_fpr_error": float(error.median()),
                        "mean_valid_rate": float(
                            group[f"{method}_valid_rate"].mean()
                        ),
                        "improved_vs_normal": int((error < normal_error).sum()),
                        "worsened_vs_normal": int((error > normal_error).sum()),
                        "tied_vs_normal": int((error == normal_error).sum()),
                    }
                )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    if args.decisive_replicates <= 1 or args.fresh_replicates <= 1:
        raise ValueError("replicate counts must exceed one")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    decisive = _from_decisive(args.decisive_scenarios)
    fresh = _fresh_scenarios(args.fresh_scenario_seed)
    scenarios = decisive + fresh
    child_sequences = np.random.SeedSequence(args.simulation_seed).spawn(
        len(scenarios)
    )
    rows = []
    for index, (scenario, child) in enumerate(zip(scenarios, child_sequences)):
        simulation_seed = int(child.generate_state(1)[0])
        replicates = (
            args.decisive_replicates
            if scenario.source == "decisive_hard"
            else args.fresh_replicates
        )
        rows.append(
            _audit_scenario(
                scenario,
                replicates=replicates,
                simulation_seed=simulation_seed,
            )
        )
        print(
            f"[{index + 1}/{len(scenarios)}] "
            f"{scenario.source}:{scenario.scenario_key}",
            flush=True,
        )

    scenario_frame = pd.DataFrame(rows)
    summary_frame = _summarize(scenario_frame)
    scenario_frame.to_csv(args.output_dir / "scenario_audit.csv", index=False)
    summary_frame.to_csv(args.output_dir / "method_summary.csv", index=False)
    metadata = {
        "post_hoc_diagnostic": True,
        "decisive_scenarios": str(args.decisive_scenarios),
        "decisive_replicates": args.decisive_replicates,
        "fresh_replicates": args.fresh_replicates,
        "fresh_scenario_seed": args.fresh_scenario_seed,
        "simulation_seed": args.simulation_seed,
        "decisive_scenario_count": len(decisive),
        "fresh_scenario_count": len(fresh),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\nMethod summary", flush=True)
    print(summary_frame.to_string(index=False), flush=True)
    print("\nVariance-ratio summary", flush=True)
    print(
        scenario_frame.groupby("source")
        .agg(
            scenarios=("scenario_key", "size"),
            mean_se2_ratio=("estimated_to_true_se2_ratio", "mean"),
            min_se2_ratio=("estimated_to_true_se2_ratio", "min"),
            max_se2_ratio=("estimated_to_true_se2_ratio", "max"),
            mean_delta_variance_ratio=(
                "empirical_delta_variance_to_true_se2",
                "mean",
            ),
            mean_delta_se2_correlation=(
                "correlation_delta_estimated_se2",
                "mean",
            ),
        )
        .to_string(),
        flush=True,
    )


if __name__ == "__main__":
    main()
