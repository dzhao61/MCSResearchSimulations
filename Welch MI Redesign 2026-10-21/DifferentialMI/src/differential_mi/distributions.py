"""Construct controlled discrete joint distributions for validation."""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
from scipy.special import xlogy


def marginal_probabilities(size: int, regime: str) -> np.ndarray:
    """Return balanced, mildly skewed, or strongly skewed probabilities."""
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


def mutual_information_probability(probabilities: np.ndarray) -> float:
    """Calculate discrete MI in nats from a joint probability table."""
    p = np.asarray(probabilities, dtype=float)
    if p.ndim != 2 or np.any(p < 0):
        raise ValueError("Expected a nonnegative two-dimensional table.")
    total = p.sum()
    if not np.isfinite(total) or total <= 0:
        raise ValueError("Probabilities must have positive finite mass.")
    p = p / total
    row = p.sum(axis=1)
    col = p.sum(axis=0)
    return float(
        np.sum(xlogy(p, p))
        - np.sum(xlogy(row, row))
        - np.sum(xlogy(col, col))
    )


def interaction_pattern(rows: int, columns: int, pattern: str) -> np.ndarray:
    """Return a non-additive interaction pattern for a log-linear table."""
    if pattern == "ordinal":
        row_score = np.linspace(-1.0, 1.0, rows)
        col_score = np.linspace(-1.0, 1.0, columns)
        return np.outer(row_score, col_score)
    if pattern == "checkerboard":
        row_score = np.where(np.arange(rows) % 2 == 0, 1.0, -1.0)
        col_score = np.where(np.arange(columns) % 2 == 0, 1.0, -1.0)
        return np.outer(row_score, col_score)
    if pattern == "cyclic":
        row_phase = 2.0 * np.pi * np.arange(rows) / rows
        column_phase = 2.0 * np.pi * np.arange(columns) / columns
        return np.cos(row_phase[:, None] - column_phase[None, :])
    raise ValueError(f"Unknown interaction pattern: {pattern}")


def random_interaction_pattern(
    rows: int, columns: int, rng: np.random.Generator
) -> np.ndarray:
    """Draw a standardized non-additive log-linear interaction matrix."""
    if rows < 2 or columns < 2:
        raise ValueError("Interaction dimensions must both be at least two.")
    interaction = rng.normal(size=(rows, columns))
    interaction = (
        interaction
        - interaction.mean(axis=1, keepdims=True)
        - interaction.mean(axis=0, keepdims=True)
        + interaction.mean()
    )
    scale = float(np.sqrt(np.mean(interaction * interaction)))
    if not np.isfinite(scale) or scale < 1e-12:
        raise RuntimeError("Random interaction pattern is numerically degenerate.")
    return interaction / scale


def association_table_from_interaction(
    row_marginal: np.ndarray,
    column_marginal: np.ndarray,
    association: float,
    interaction: np.ndarray,
    *,
    tolerance: float = 1e-13,
    max_iterations: int = 20_000,
) -> np.ndarray:
    """Build a positive table from arbitrary interactions and fixed margins."""
    row = np.asarray(row_marginal, dtype=float)
    col = np.asarray(column_marginal, dtype=float)
    pattern = np.asarray(interaction, dtype=float)
    if row.ndim != 1 or col.ndim != 1 or np.any(row <= 0) or np.any(col <= 0):
        raise ValueError("Margins must be positive one-dimensional vectors.")
    if pattern.shape != (row.size, col.size) or not np.all(np.isfinite(pattern)):
        raise ValueError("Interaction must be finite and match the margin dimensions.")
    row = row / row.sum()
    col = col / col.sum()

    exponent = association * pattern
    exponent -= np.max(exponent)
    kernel = np.exp(exponent)

    right = np.ones(col.size)
    table = np.outer(row, col)
    for _ in range(max_iterations):
        denominator_left = kernel @ right
        if np.any(denominator_left <= 0):
            break
        left = row / denominator_left
        denominator_right = kernel.T @ left
        if np.any(denominator_right <= 0):
            break
        right = col / denominator_right
        table = (left[:, None] * kernel) * right[None, :]
        error = max(
            np.max(np.abs(table.sum(axis=1) - row)),
            np.max(np.abs(table.sum(axis=0) - col)),
        )
        if error <= tolerance:
            return table / table.sum()
    raise RuntimeError("Iterative proportional fitting did not converge.")


def association_table(
    row_marginal: np.ndarray,
    column_marginal: np.ndarray,
    association: float,
    *,
    pattern: str = "ordinal",
    tolerance: float = 1e-13,
    max_iterations: int = 20_000,
) -> np.ndarray:
    """Build a positive log-linear table with exactly prescribed margins."""
    row = np.asarray(row_marginal, dtype=float)
    col = np.asarray(column_marginal, dtype=float)
    return association_table_from_interaction(
        row,
        col,
        association,
        interaction_pattern(row.size, col.size, pattern),
        tolerance=tolerance,
        max_iterations=max_iterations,
    )


def table_with_target_mi_from_interaction(
    row_marginal: np.ndarray,
    column_marginal: np.ndarray,
    target_mi: float,
    interaction: np.ndarray,
    *,
    mi_tolerance: float = 1e-12,
    max_association: float = 128.0,
) -> tuple[np.ndarray, float]:
    """Solve for association strength using an arbitrary interaction matrix."""
    if target_mi < 0:
        raise ValueError("Target MI cannot be negative.")
    row = np.asarray(row_marginal, dtype=float)
    col = np.asarray(column_marginal, dtype=float)
    if target_mi <= mi_tolerance:
        table = np.outer(row, col)
        return table / table.sum(), 0.0

    def objective(association: float) -> float:
        table = association_table_from_interaction(
            row, col, association, interaction
        )
        return mutual_information_probability(table) - target_mi

    upper = 0.5
    upper_value = objective(upper)
    while upper_value < 0 and upper < max_association:
        upper *= 2.0
        upper_value = objective(upper)
    if upper_value < 0:
        raise ValueError("Target MI is infeasible for the requested margins.")

    association = float(
        brentq(objective, 0.0, upper, xtol=mi_tolerance, rtol=1e-13)
    )
    table = association_table_from_interaction(
        row, col, association, interaction
    )
    achieved = mutual_information_probability(table)
    if abs(achieved - target_mi) > 10 * mi_tolerance:
        raise RuntimeError("Target-MI solver did not reach the requested value.")
    return table, association


def table_with_target_mi(
    row_marginal: np.ndarray,
    column_marginal: np.ndarray,
    target_mi: float,
    *,
    pattern: str = "ordinal",
    mi_tolerance: float = 1e-12,
) -> tuple[np.ndarray, float]:
    """Solve for a positive table having the requested margins and MI."""
    if target_mi < 0:
        raise ValueError("Target MI cannot be negative.")
    if target_mi <= mi_tolerance:
        table = np.outer(row_marginal, column_marginal)
        return table / table.sum(), 0.0

    def objective(association: float) -> float:
        table = association_table(
            row_marginal, column_marginal, association, pattern=pattern
        )
        return mutual_information_probability(table) - target_mi

    upper = 1.0
    while objective(upper) < 0 and upper < 256:
        upper *= 2.0
    if upper >= 256 and objective(upper) < 0:
        raise ValueError("Target MI is infeasible for the requested margins.")

    association = float(
        brentq(objective, 0.0, upper, xtol=mi_tolerance, rtol=1e-13)
    )
    table = association_table(
        row_marginal, column_marginal, association, pattern=pattern
    )
    achieved = mutual_information_probability(table)
    if abs(achieved - target_mi) > 10 * mi_tolerance:
        raise RuntimeError("Target-MI solver did not reach the requested value.")
    return table, association
