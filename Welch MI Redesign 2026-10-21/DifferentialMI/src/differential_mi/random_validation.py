"""Randomized regular-case scenarios and high-throughput validation helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from time import perf_counter

import numpy as np
import pandas as pd
from scipy.stats import binomtest, norm

from .distributions import (
    mutual_information_probability,
    random_interaction_pattern,
    table_with_target_mi_from_interaction,
)
from .inference import compare_tables
from .statistics import influence_variance, jackknife_mi, plugin_mi


DETERMINISTIC_METHODS = ("wald_plugin", "wald_analytic", "wald_jackknife")
PERMUTATION_METHODS = (
    "naive_perm_plugin",
    "student_perm_plugin",
    "student_perm_analytic",
    "student_perm_jackknife",
)


@dataclass(frozen=True)
class RandomScenario:
    """A fully materialized weak-null pair used by randomized validation."""

    scenario_id: str
    shape_index: int
    design_index: int
    rows: int
    columns: int
    n_p: int
    n_q: int
    target_mi: float
    margin_alpha_p: float
    margin_alpha_q: float
    association_p: float
    association_q: float
    generation_attempts: int
    probability_p: np.ndarray
    probability_q: np.ndarray

    def metadata(self) -> dict[str, int | float | str]:
        result = asdict(self)
        del result["probability_p"]
        del result["probability_q"]
        return result


SHAPES = (
    (2, 2),
    (2, 5),
    (3, 3),
    (3, 7),
    (4, 6),
    (5, 5),
    (5, 10),
    (8, 8),
    (8, 12),
    (10, 10),
    (10, 15),
    (20, 20),
)

# The six designs span nearly uniform through heterogeneous margins, equal
# and unequal sample sizes, and low through high per-cell sampling density.
DESIGNS = (
    # alpha_p, alpha_q, target MI, base n/cells, q:p ratio
    (50.0, 50.0, 0.03, 100, 1),
    (20.0, 5.0, 0.07, 50, 2),
    (5.0, 1.2, 0.15, 25, 4),
    (1.0, 0.5, 0.03, 200, 1),
    (10.0, 0.8, 0.07, 20, 2),
    (2.0, 20.0, 0.15, 10, 4),
)

# These positions are fixed before inspecting randomized calibration results.
ANCHOR_POSITIONS = frozenset(
    {
        (0, 0),
        (0, 2),
        (1, 1),
        (2, 4),
        (3, 3),
        (4, 5),
        (5, 2),
        (6, 1),
        (7, 4),
        (8, 0),
        (10, 5),
        (11, 2),
    }
)


def _dirichlet_margin(
    size: int, concentration: float, rng: np.random.Generator
) -> np.ndarray:
    for _ in range(2_000):
        margin = rng.dirichlet(np.full(size, concentration))
        if margin.min() >= 1e-4 and margin.max() <= 0.98:
            return margin
    raise RuntimeError("Could not draw a numerically usable random margin.")


def generate_random_scenarios(seed: int) -> list[RandomScenario]:
    """Generate the fixed broad grid of randomized equal-MI distribution pairs."""
    rng = np.random.default_rng(seed)
    scenarios: list[RandomScenario] = []
    for shape_index, (rows, columns) in enumerate(SHAPES):
        cells = rows * columns
        for design_index, design in enumerate(DESIGNS):
            alpha_p, alpha_q, target_mi, density, ratio = design
            n_p = max(120, cells * density)
            n_q = n_p * ratio

            last_error: Exception | None = None
            for attempt in range(1, 101):
                try:
                    row_p = _dirichlet_margin(rows, alpha_p, rng)
                    col_p = _dirichlet_margin(columns, alpha_p, rng)
                    row_q = _dirichlet_margin(rows, alpha_q, rng)
                    col_q = _dirichlet_margin(columns, alpha_q, rng)
                    interaction_p = random_interaction_pattern(rows, columns, rng)
                    interaction_q = random_interaction_pattern(rows, columns, rng)
                    probability_p, association_p = (
                        table_with_target_mi_from_interaction(
                            row_p,
                            col_p,
                            target_mi,
                            interaction_p,
                        )
                    )
                    probability_q, association_q = (
                        table_with_target_mi_from_interaction(
                            row_q,
                            col_q,
                            target_mi,
                            interaction_q,
                        )
                    )
                    if min(probability_p.min(), probability_q.min()) < 1e-12:
                        raise ValueError("Generated cell probability is too small.")
                    if np.abs(probability_p - probability_q).sum() < 0.05:
                        raise ValueError("Generated weak-null pair is too similar.")
                    if min(
                        float(influence_variance(probability_p)),
                        float(influence_variance(probability_q)),
                    ) < 1e-6:
                        raise ValueError("Generated influence variance is degenerate.")
                except (RuntimeError, ValueError) as error:
                    last_error = error
                    continue
                break
            else:
                raise RuntimeError(
                    f"Failed to generate shape={rows}x{columns}, "
                    f"design={design_index}: {last_error}"
                )

            scenarios.append(
                RandomScenario(
                    scenario_id=f"random_{rows}x{columns}_d{design_index}",
                    shape_index=shape_index,
                    design_index=design_index,
                    rows=rows,
                    columns=columns,
                    n_p=n_p,
                    n_q=n_q,
                    target_mi=target_mi,
                    margin_alpha_p=alpha_p,
                    margin_alpha_q=alpha_q,
                    association_p=association_p,
                    association_q=association_q,
                    generation_attempts=attempt,
                    probability_p=probability_p,
                    probability_q=probability_q,
                )
            )
    return scenarios


def scenario_diagnostics(scenario: RandomScenario) -> dict[str, int | float | str]:
    """Return population diagnostics and serializable scenario metadata."""
    p = scenario.probability_p
    q = scenario.probability_q
    expected_independence_p = scenario.n_p * np.outer(p.sum(axis=1), p.sum(axis=0))
    expected_independence_q = scenario.n_q * np.outer(q.sum(axis=1), q.sum(axis=0))
    pooled_weight = scenario.n_p / (scenario.n_p + scenario.n_q)
    pooled_mixture = pooled_weight * p + (1.0 - pooled_weight) * q
    result = scenario.metadata()
    result.update(
        {
            "true_mi_p": mutual_information_probability(p),
            "true_mi_q": mutual_information_probability(q),
            "true_delta": (
                mutual_information_probability(p)
                - mutual_information_probability(q)
            ),
            "distribution_l1": float(np.abs(p - q).sum()),
            "population_variance_p": float(influence_variance(p)),
            "population_variance_q": float(influence_variance(q)),
            "pooled_mixture_mi": mutual_information_probability(pooled_mixture),
            "pooled_mixture_variance": float(
                influence_variance(pooled_mixture)
            ),
            "min_probability_p": float(p.min()),
            "min_probability_q": float(q.min()),
            "min_joint_expected_p": float(scenario.n_p * p.min()),
            "min_joint_expected_q": float(scenario.n_q * q.min()),
            "independence_expected_below_1_p": float(
                np.mean(expected_independence_p < 1)
            ),
            "independence_expected_below_1_q": float(
                np.mean(expected_independence_q < 1)
            ),
            "independence_expected_below_5_p": float(
                np.mean(expected_independence_p < 5)
            ),
            "independence_expected_below_5_q": float(
                np.mean(expected_independence_q < 5)
            ),
            "is_permutation_anchor": (
                scenario.shape_index,
                scenario.design_index,
            )
            in ANCHOR_POSITIONS,
        }
    )
    return result


def strong_null_version(scenario: RandomScenario) -> RandomScenario:
    """Convert a weak-null scenario to a P=Q implementation-control scenario."""
    return replace(
        scenario,
        scenario_id=f"strong_{scenario.scenario_id.removeprefix('random_')}",
        margin_alpha_q=scenario.margin_alpha_p,
        association_q=scenario.association_p,
        probability_q=scenario.probability_p.copy(),
    )


def _sample_diagnostics(tables: np.ndarray) -> dict[str, np.ndarray]:
    counts = np.asarray(tables, dtype=float)
    totals = counts.sum(axis=(1, 2))
    row = counts.sum(axis=2)
    col = counts.sum(axis=1)
    expected = row[:, :, None] * col[:, None, :] / totals[:, None, None]
    return {
        "zero_fraction": np.mean(counts == 0, axis=(1, 2)),
        "independence_expected_min": expected.min(axis=(1, 2)),
        "independence_expected_below_1": np.mean(expected < 1, axis=(1, 2)),
        "independence_expected_below_5": np.mean(expected < 5, axis=(1, 2)),
        "nonempty_rows": np.count_nonzero(row, axis=1),
        "nonempty_columns": np.count_nonzero(col, axis=1),
    }


def _safe_two_sided_p(delta: np.ndarray, standard_error: np.ndarray) -> np.ndarray:
    z = np.divide(
        delta,
        standard_error,
        out=np.full_like(delta, np.nan, dtype=float),
        where=np.isfinite(standard_error) & (standard_error > 0),
    )
    return 2.0 * norm.sf(np.abs(z))


def run_deterministic_scenario(
    scenario: RandomScenario,
    *,
    replicates: int,
    seed: int,
) -> pd.DataFrame:
    """Run all deterministic methods in one vectorized multinomial batch."""
    rng = np.random.default_rng(seed)
    table_p = rng.multinomial(
        scenario.n_p, scenario.probability_p.reshape(-1), size=replicates
    ).reshape(replicates, scenario.rows, scenario.columns)
    table_q = rng.multinomial(
        scenario.n_q, scenario.probability_q.reshape(-1), size=replicates
    ).reshape(replicates, scenario.rows, scenario.columns)

    start = perf_counter()
    mi_plugin_p = np.asarray(plugin_mi(table_p))
    mi_plugin_q = np.asarray(plugin_mi(table_q))
    degrees_of_freedom = (scenario.rows - 1) * (scenario.columns - 1)
    mi_analytic_p = mi_plugin_p - degrees_of_freedom / (2.0 * scenario.n_p)
    mi_analytic_q = mi_plugin_q - degrees_of_freedom / (2.0 * scenario.n_q)
    mi_jackknife_p = np.asarray(jackknife_mi(table_p))
    mi_jackknife_q = np.asarray(jackknife_mi(table_q))
    variance_p = np.asarray(influence_variance(table_p))
    variance_q = np.asarray(influence_variance(table_q))
    standard_error = np.sqrt(
        variance_p / scenario.n_p + variance_q / scenario.n_q
    )

    delta_plugin = mi_plugin_p - mi_plugin_q
    delta_analytic = mi_analytic_p - mi_analytic_q
    delta_jackknife = mi_jackknife_p - mi_jackknife_q
    p_plugin = _safe_two_sided_p(delta_plugin, standard_error)
    p_analytic = _safe_two_sided_p(delta_analytic, standard_error)
    p_jackknife = _safe_two_sided_p(delta_jackknife, standard_error)
    deterministic_seconds = perf_counter() - start

    diagnostics_p = _sample_diagnostics(table_p)
    diagnostics_q = _sample_diagnostics(table_q)
    correction_difference = delta_jackknife - delta_analytic
    standardized_correction_difference = np.divide(
        np.abs(correction_difference),
        standard_error,
        out=np.full_like(standard_error, np.nan),
        where=standard_error > 0,
    )

    return pd.DataFrame(
        {
            "scenario_id": scenario.scenario_id,
            "replicate": np.arange(replicates),
            "replicate_seed": seed,
            "true_delta": scenario_diagnostics(scenario)["true_delta"],
            "delta_plugin": delta_plugin,
            "delta_analytic": delta_analytic,
            "delta_jackknife": delta_jackknife,
            "standard_error": standard_error,
            "variance_p": variance_p,
            "variance_q": variance_q,
            "wald_plugin_p": p_plugin,
            "wald_analytic_p": p_analytic,
            "wald_jackknife_p": p_jackknife,
            "zero_fraction_p": diagnostics_p["zero_fraction"],
            "zero_fraction_q": diagnostics_q["zero_fraction"],
            "independence_expected_min_p": diagnostics_p[
                "independence_expected_min"
            ],
            "independence_expected_min_q": diagnostics_q[
                "independence_expected_min"
            ],
            "independence_expected_below_1_p": diagnostics_p[
                "independence_expected_below_1"
            ],
            "independence_expected_below_1_q": diagnostics_q[
                "independence_expected_below_1"
            ],
            "independence_expected_below_5_p": diagnostics_p[
                "independence_expected_below_5"
            ],
            "independence_expected_below_5_q": diagnostics_q[
                "independence_expected_below_5"
            ],
            "nonempty_rows_p": diagnostics_p["nonempty_rows"],
            "nonempty_rows_q": diagnostics_q["nonempty_rows"],
            "nonempty_columns_p": diagnostics_p["nonempty_columns"],
            "nonempty_columns_q": diagnostics_q["nonempty_columns"],
            "jackknife_minus_analytic_delta": correction_difference,
            "standardized_correction_difference": standardized_correction_difference,
            "valid_studentization": (
                np.isfinite(standard_error)
                & (standard_error > 0)
                & np.isfinite(p_plugin)
                & np.isfinite(p_analytic)
                & np.isfinite(p_jackknife)
            ),
            "deterministic_batch_seconds": deterministic_seconds,
            "deterministic_microseconds_per_pair": (
                1e6 * deterministic_seconds / replicates
            ),
        }
    )


def run_permutation_anchor(
    scenario: RandomScenario,
    *,
    replicates: int,
    permutations: int,
    seed: int,
) -> pd.DataFrame:
    """Run the full deterministic and permutation comparison for one anchor."""
    rng = np.random.default_rng(seed)
    population_diagnostics = scenario_diagnostics(scenario)
    rows: list[dict] = []
    for replicate in range(replicates):
        table_p = rng.multinomial(
            scenario.n_p, scenario.probability_p.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q, scenario.probability_q.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)
        result = compare_tables(
            table_p, table_q, permutations=permutations, rng=rng
        ).to_dict()
        result.update(
            {
                "scenario_id": scenario.scenario_id,
                "replicate": replicate,
                "replicate_seed": seed,
                "pooled_population_mi": population_diagnostics["pooled_mixture_mi"],
                "pooled_population_variance": population_diagnostics[
                    "pooled_mixture_variance"
                ],
            }
        )
        rows.append(result)
    return pd.DataFrame(rows)


def _wilson_interval(rejections: int, total: int) -> tuple[float, float]:
    interval = binomtest(rejections, total).proportion_ci(
        confidence_level=0.95, method="wilson"
    )
    return float(interval.low), float(interval.high)


def summarize_deterministic(replicates: pd.DataFrame) -> pd.DataFrame:
    """Summarize deterministic calibration, coverage, bias, and diagnostics."""
    rows: list[dict] = []
    for scenario_id, group in replicates.groupby("scenario_id", sort=False):
        true_delta = float(group["true_delta"].iloc[0])
        row: dict[str, int | float | str] = {
            "scenario_id": scenario_id,
            "replicates": len(group),
            "valid_rate": float(group["valid_studentization"].mean()),
            "mean_zero_fraction_p": float(group["zero_fraction_p"].mean()),
            "mean_zero_fraction_q": float(group["zero_fraction_q"].mean()),
            "mean_expected_below_1_p": float(
                group["independence_expected_below_1_p"].mean()
            ),
            "mean_expected_below_1_q": float(
                group["independence_expected_below_1_q"].mean()
            ),
            "mean_expected_below_5_p": float(
                group["independence_expected_below_5_p"].mean()
            ),
            "mean_expected_below_5_q": float(
                group["independence_expected_below_5_q"].mean()
            ),
            "mean_standardized_correction_difference": float(
                group["standardized_correction_difference"].mean()
            ),
            "deterministic_microseconds_per_pair": float(
                group["deterministic_microseconds_per_pair"].iloc[0]
            ),
        }
        for method in DETERMINISTIC_METHODS:
            p_values = group[f"{method}_p"]
            delta = group[f"delta_{method.removeprefix('wald_')}"]
            valid = p_values.notna()
            for alpha in (0.10, 0.05):
                rejections = int(np.count_nonzero(p_values[valid] <= alpha))
                total = int(np.count_nonzero(valid))
                rate = rejections / total if total else float("nan")
                low, high = (
                    _wilson_interval(rejections, total)
                    if total
                    else (float("nan"), float("nan"))
                )
                suffix = f"{int(100 * alpha):02d}"
                row[f"{method}_fpr_{suffix}"] = rate
                row[f"{method}_fpr_{suffix}_low"] = low
                row[f"{method}_fpr_{suffix}_high"] = high
            row[f"{method}_bias"] = float(np.mean(delta - true_delta))
            row[f"{method}_rmse"] = float(
                np.sqrt(np.mean((delta - true_delta) ** 2))
            )
            row[f"{method}_coverage_95"] = float(
                np.mean(
                    (delta - 1.959963984540054 * group["standard_error"] <= true_delta)
                    & (
                        true_delta
                        <= delta + 1.959963984540054 * group["standard_error"]
                    )
                )
            )
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_permutation(replicates: pd.DataFrame) -> pd.DataFrame:
    """Summarize the pre-selected permutation anchor results."""
    methods = (*PERMUTATION_METHODS, *DETERMINISTIC_METHODS)
    rows: list[dict] = []
    for scenario_id, group in replicates.groupby("scenario_id", sort=False):
        row: dict[str, int | float | str] = {
            "scenario_id": scenario_id,
            "replicates": len(group),
            "permutations": int(group["permutations"].iloc[0]),
            "mean_deterministic_ms": float(
                1000 * group["deterministic_seconds"].mean()
            ),
            "mean_permutation_ms": float(
                1000 * group["permutation_seconds"].mean()
            ),
        }
        for method in methods:
            p_values = group[f"{method}_p"].dropna()
            for alpha in (0.10, 0.05):
                rejections = int(np.count_nonzero(p_values <= alpha))
                total = int(p_values.size)
                suffix = f"{int(100 * alpha):02d}"
                row[f"{method}_fpr_{suffix}"] = (
                    rejections / total if total else float("nan")
                )
        rows.append(row)
    return pd.DataFrame(rows)
