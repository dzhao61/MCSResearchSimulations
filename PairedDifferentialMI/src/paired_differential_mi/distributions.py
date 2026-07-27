"""Controlled paired categorical distributions for feasibility validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from scipy.optimize import brentq
from scipy.special import xlogy


def mutual_information_probability(probabilities: np.ndarray) -> float:
    """Return mutual information in nats for a positive probability table."""
    p = np.asarray(probabilities, dtype=float)
    if p.ndim != 2 or np.any(p < 0) or not np.isfinite(p).all():
        raise ValueError("Expected a finite nonnegative probability table.")
    p = p / p.sum()
    row = p.sum(axis=1)
    column = p.sum(axis=0)
    return float(
        np.sum(xlogy(p, p))
        - np.sum(xlogy(row, row))
        - np.sum(xlogy(column, column))
    )


def marginal_probabilities(size: int, regime: str) -> np.ndarray:
    """Construct balanced, mildly skewed, or strongly skewed margins."""
    if size < 2:
        raise ValueError("Alphabet size must be at least two.")
    if regime == "balanced":
        return np.full(size, 1.0 / size)
    dominant = {"mild": 0.70, "strong": 0.90}.get(regime)
    if dominant is None:
        raise ValueError(f"Unknown marginal regime: {regime}")
    result = np.full(size, (1.0 - dominant) / (size - 1))
    result[0] = dominant
    return result


def _interaction_pattern(rows: int, columns: int, pattern: str) -> np.ndarray:
    if pattern == "ordinal":
        return np.outer(
            np.linspace(-1.0, 1.0, rows),
            np.linspace(-1.0, 1.0, columns),
        )
    if pattern == "checkerboard":
        return np.outer(
            np.where(np.arange(rows) % 2 == 0, 1.0, -1.0),
            np.where(np.arange(columns) % 2 == 0, 1.0, -1.0),
        )
    if pattern == "cyclic":
        row_phase = 2.0 * np.pi * np.arange(rows) / rows
        column_phase = 2.0 * np.pi * np.arange(columns) / columns
        return np.cos(row_phase[:, None] - column_phase[None, :])
    raise ValueError(f"Unknown interaction pattern: {pattern}")


def _association_table(
    row: np.ndarray,
    column: np.ndarray,
    association: float,
    pattern: str,
) -> np.ndarray:
    """Use iterative proportional fitting to preserve requested margins."""
    row = np.asarray(row, dtype=float)
    column = np.asarray(column, dtype=float)
    interaction = _interaction_pattern(row.size, column.size, pattern)
    exponent = association * interaction
    kernel = np.exp(exponent - exponent.max())
    right = np.ones(column.size)
    table = np.outer(row, column)
    for _ in range(20_000):
        left = row / (kernel @ right)
        right = column / (kernel.T @ left)
        table = (left[:, None] * kernel) * right[None, :]
        error = max(
            np.max(np.abs(table.sum(axis=1) - row)),
            np.max(np.abs(table.sum(axis=0) - column)),
        )
        if error <= 1e-13:
            return table / table.sum()
    raise RuntimeError("Iterative proportional fitting did not converge.")


def table_with_target_mi(
    rows: int,
    columns: int,
    margin: str,
    target_mi: float,
    pattern: str,
) -> np.ndarray:
    """Construct a positive table with exact margins and target MI."""
    row = marginal_probabilities(rows, margin)
    column = marginal_probabilities(columns, margin)
    if target_mi <= 1e-12:
        return np.outer(row, column)

    def objective(association: float) -> float:
        return (
            mutual_information_probability(
                _association_table(row, column, association, pattern)
            )
            - target_mi
        )

    upper = 1.0
    while objective(upper) < 0 and upper < 256.0:
        upper *= 2.0
    if objective(upper) < 0:
        raise ValueError("Target MI is infeasible for the requested margins.")
    association = brentq(objective, 0.0, upper, xtol=1e-12, rtol=1e-13)
    result = _association_table(row, column, association, pattern)
    if abs(mutual_information_probability(result) - target_mi) > 1e-10:
        raise RuntimeError("Target-MI solver did not reach the target.")
    return result


def local_information(probabilities: np.ndarray) -> np.ndarray:
    """Return population local information for every flattened table cell."""
    p = np.asarray(probabilities, dtype=float)
    row = p.sum(axis=1)
    column = p.sum(axis=0)
    return (
        np.log(p)
        - np.log(row[:, None])
        - np.log(column[None, :])
    ).reshape(-1)


def _quantile_coupling(
    probability_a: np.ndarray,
    probability_b: np.ndarray,
    order_a: np.ndarray,
    order_b: np.ndarray,
) -> np.ndarray:
    """Couple categorical distributions by overlapping ordered quantiles."""
    pa = np.asarray(probability_a, dtype=float)
    pb = np.asarray(probability_b, dtype=float)
    result = np.zeros((pa.size, pb.size), dtype=float)
    remaining_a = pa[order_a].copy()
    remaining_b = pb[order_b].copy()
    index_a = 0
    index_b = 0
    tolerance = 1e-15
    while index_a < pa.size and index_b < pb.size:
        mass = min(remaining_a[index_a], remaining_b[index_b])
        result[order_a[index_a], order_b[index_b]] += mass
        remaining_a[index_a] -= mass
        remaining_b[index_b] -= mass
        if remaining_a[index_a] <= tolerance:
            index_a += 1
        if remaining_b[index_b] <= tolerance:
            index_b += 1
    result /= result.sum()
    return result


def paired_coupling(
    probability_a: np.ndarray,
    probability_b: np.ndarray,
    pairing: float,
) -> np.ndarray:
    """Preserve both condition tables while controlling score covariance.

    ``pairing=0`` gives independent conditions. Positive values mix toward
    comonotone local-information scores; negative values mix toward
    countermonotone scores.
    """
    if not -1.0 <= pairing <= 1.0:
        raise ValueError("pairing must lie between -1 and 1.")
    pa = np.asarray(probability_a, dtype=float).reshape(-1)
    pb = np.asarray(probability_b, dtype=float).reshape(-1)
    independent = np.outer(pa, pb)
    if pairing == 0:
        return independent

    score_a = local_information(probability_a)
    score_b = local_information(probability_b)
    order_a = np.argsort(score_a, kind="stable")
    order_b = np.argsort(score_b, kind="stable")
    if pairing < 0:
        order_b = order_b[::-1]
    extreme = _quantile_coupling(pa, pb, order_a, order_b)
    result = (1.0 - abs(pairing)) * independent + abs(pairing) * extreme
    result /= result.sum()
    return result


def coupling_diagnostics(
    probability_a: np.ndarray,
    probability_b: np.ndarray,
    coupling: np.ndarray,
) -> dict[str, float]:
    """Return exact population MI, margin, sparsity, and covariance checks."""
    pa = np.asarray(probability_a, dtype=float).reshape(-1)
    pb = np.asarray(probability_b, dtype=float).reshape(-1)
    score_a = local_information(probability_a)
    score_b = local_information(probability_b)
    mi_a = mutual_information_probability(probability_a)
    mi_b = mutual_information_probability(probability_b)
    centered_a = score_a - mi_a
    centered_b = score_b - mi_b
    variance_a = float(np.dot(pa, centered_a * centered_a))
    variance_b = float(np.dot(pb, centered_b * centered_b))
    covariance = float(
        np.sum(coupling * centered_a[:, None] * centered_b[None, :])
    )
    denominator = np.sqrt(variance_a * variance_b)
    return {
        "true_mi_a": mi_a,
        "true_mi_b": mi_b,
        "true_delta": mi_a - mi_b,
        "population_variance_a": variance_a,
        "population_variance_b": variance_b,
        "population_covariance": covariance,
        "population_score_correlation": (
            covariance / denominator if denominator > 0 else float("nan")
        ),
        "coupling_margin_error_a": float(
            np.max(np.abs(coupling.sum(axis=1) - pa))
        ),
        "coupling_margin_error_b": float(
            np.max(np.abs(coupling.sum(axis=0) - pb))
        ),
    }


@dataclass(frozen=True)
class PairedScenario:
    scenario_id: str
    regime: str
    rows: int
    columns: int
    n: int
    margin_a: str
    margin_b: str
    target_mi_a: float
    target_mi_b: float
    pairing: float
    pattern_a: str = "ordinal"
    pattern_b: str = "cyclic"

    def metadata(self) -> dict[str, str | int | float]:
        return asdict(self)

    def materialize(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
        probability_a = table_with_target_mi(
            self.rows,
            self.columns,
            self.margin_a,
            self.target_mi_a,
            self.pattern_a,
        )
        probability_b = table_with_target_mi(
            self.rows,
            self.columns,
            self.margin_b,
            self.target_mi_b,
            self.pattern_b,
        )
        coupling = paired_coupling(probability_a, probability_b, self.pairing)
        diagnostics = self.metadata()
        diagnostics.update(
            coupling_diagnostics(probability_a, probability_b, coupling)
        )
        expected_a = self.n * probability_a
        expected_b = self.n * probability_b
        diagnostics.update(
            {
                "min_expected_joint_a": float(expected_a.min()),
                "min_expected_joint_b": float(expected_b.min()),
                "expected_joint_below_1_a": float(np.mean(expected_a < 1)),
                "expected_joint_below_1_b": float(np.mean(expected_b < 1)),
                "expected_joint_below_5_a": float(np.mean(expected_a < 5)),
                "expected_joint_below_5_b": float(np.mean(expected_b < 5)),
                "condition_distribution_l1": float(
                    np.abs(probability_a - probability_b).sum()
                ),
            }
        )
        return probability_a, probability_b, coupling, diagnostics


def pilot_scenarios(profile: str = "pilot") -> list[PairedScenario]:
    """Return scenarios fixed in the feasibility protocol."""
    scenarios = [
        PairedScenario("regular_2x2_bal_n50_zero", "regular", 2, 2, 50, "balanced", "balanced", 0.10, 0.10, 0.0, "ordinal", "ordinal"),
        PairedScenario("regular_2x2_bal_n50_positive", "regular", 2, 2, 50, "balanced", "balanced", 0.10, 0.10, 0.8, "ordinal", "ordinal"),
        PairedScenario("regular_2x2_bal_n50_negative", "regular", 2, 2, 50, "balanced", "balanced", 0.10, 0.10, -0.8, "ordinal", "ordinal"),
        PairedScenario("regular_2x2_weak_n100_zero", "regular", 2, 2, 100, "balanced", "strong", 0.05, 0.05, 0.0),
        PairedScenario("regular_2x2_weak_n100_positive", "regular", 2, 2, 100, "balanced", "strong", 0.05, 0.05, 0.8),
        PairedScenario("regular_2x2_weak_n100_negative", "regular", 2, 2, 100, "balanced", "strong", 0.05, 0.05, -0.8),
        PairedScenario("regular_3x3_weak_n150_zero", "regular", 3, 3, 150, "balanced", "strong", 0.10, 0.10, 0.0),
        PairedScenario("regular_3x3_weak_n150_positive", "regular", 3, 3, 150, "balanced", "strong", 0.10, 0.10, 0.8),
        PairedScenario("regular_3x3_weak_n150_negative", "regular", 3, 3, 150, "balanced", "strong", 0.10, 0.10, -0.8),
        PairedScenario("regular_3x3_mild_strong_n300", "regular", 3, 3, 300, "mild", "strong", 0.10, 0.10, 0.8),
        PairedScenario("regular_5x5_bal_mild_n500", "regular", 5, 5, 500, "balanced", "mild", 0.15, 0.15, 0.8),
        PairedScenario("regular_5x5_mild_strong_n1000", "regular", 5, 5, 1000, "mild", "strong", 0.10, 0.10, 0.8),
        PairedScenario("sparse_3x3_strong_n50_zero", "sparse", 3, 3, 50, "strong", "strong", 0.05, 0.05, 0.0, "ordinal", "ordinal"),
        PairedScenario("sparse_3x3_strong_n50_positive", "sparse", 3, 3, 50, "strong", "strong", 0.05, 0.05, 0.8, "ordinal", "ordinal"),
        PairedScenario("sparse_5x5_strong_n150_zero", "sparse", 5, 5, 150, "strong", "strong", 0.10, 0.10, 0.0, "ordinal", "ordinal"),
        PairedScenario("sparse_5x5_strong_n150_positive", "sparse", 5, 5, 150, "strong", "strong", 0.10, 0.10, 0.8, "ordinal", "ordinal"),
        PairedScenario("sparse_5x5_mild_strong_n250", "sparse", 5, 5, 250, "mild", "strong", 0.10, 0.10, 0.8),
        PairedScenario("boundary_2x2_weak_n250", "boundary", 2, 2, 250, "balanced", "strong", 0.002, 0.002, 0.8),
        PairedScenario("boundary_3x3_weak_n500", "boundary", 3, 3, 500, "balanced", "strong", 0.005, 0.005, 0.8),
        PairedScenario("boundary_2x2_independence_n250", "boundary", 2, 2, 250, "balanced", "strong", 0.0, 0.0, 0.8),
        PairedScenario("power_2x2_n100", "power", 2, 2, 100, "balanced", "strong", 0.05, 0.10, 0.8),
        PairedScenario("power_3x3_n150", "power", 3, 3, 150, "balanced", "strong", 0.10, 0.15, 0.8),
        PairedScenario("power_5x5_n500", "power", 5, 5, 500, "mild", "strong", 0.10, 0.15, 0.8),
    ]
    if profile == "pilot":
        return scenarios
    if profile == "smoke":
        wanted = {
            "regular_2x2_bal_n50_positive",
            "regular_2x2_weak_n100_negative",
            "sparse_3x3_strong_n50_positive",
            "boundary_2x2_weak_n250",
            "power_2x2_n100",
        }
        return [scenario for scenario in scenarios if scenario.scenario_id in wanted]
    raise ValueError(f"Unknown profile: {profile}")
