"""Experimental constrained likelihood-ratio test for equality of two MI values."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.optimize import minimize
from scipy.special import xlogy
from scipy.stats import chi2


@dataclass(frozen=True)
class ConstrainedLikelihoodRatioResult:
    """Result of one constrained equal-MI likelihood-ratio fit."""

    statistic: float
    p_value: float
    constrained_mi: float
    constraint_residual: float
    objective_gap: float
    iterations: int
    converged: bool
    starts_attempted: int
    elapsed_seconds: float


def _softmax_reference(logits: np.ndarray) -> np.ndarray:
    """Map K-1 free logits to K strictly positive probabilities."""
    complete = np.concatenate((np.asarray(logits, dtype=float), np.zeros(1)))
    shifted = complete - np.max(complete)
    weights = np.exp(shifted)
    return weights / np.sum(weights)


def _logits_from_probability(probability: np.ndarray) -> np.ndarray:
    values = np.asarray(probability, dtype=float)
    values = np.maximum(values, 1e-14)
    values /= np.sum(values)
    return np.log(values[:-1]) - np.log(values[-1])


def _mi_and_logit_gradient(
    probability: np.ndarray,
    rows: int,
    columns: int,
) -> tuple[float, np.ndarray]:
    table = np.asarray(probability, dtype=float).reshape(rows, columns)
    row = table.sum(axis=1, keepdims=True)
    column = table.sum(axis=0, keepdims=True)
    local_information = np.log(table) - np.log(row) - np.log(column)
    mi = float(np.sum(table * local_information))
    gradient = probability * (local_information.ravel() - mi)
    return mi, gradient[:-1]


def _multinomial_nll_and_gradient(
    logits: np.ndarray,
    counts: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray]:
    probability = _softmax_reference(logits)
    total = float(np.sum(counts))
    objective = float(-np.sum(xlogy(counts, probability)))
    gradient = total * probability[:-1] - counts[:-1]
    return objective, gradient, probability


def _unconstrained_nll(counts: np.ndarray) -> float:
    total = float(np.sum(counts))
    probability = counts / total
    return float(-np.sum(xlogy(counts, probability)))


def constrained_likelihood_ratio_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    tolerance: float = 1e-8,
    maximum_iterations: int = 500,
    multiple_starts: bool = True,
) -> ConstrainedLikelihoodRatioResult:
    """Test ``I(P) = I(Q)`` by constrained multinomial maximum likelihood.

    The reference distribution is the regular one-restriction asymptotic
    chi-squared distribution. No Bartlett correction or resampling calibration
    is applied in this experimental implementation.
    """
    start_time = perf_counter()
    p_table = np.asarray(table_p, dtype=float)
    q_table = np.asarray(table_q, dtype=float)
    if (
        p_table.ndim != 2
        or q_table.shape != p_table.shape
        or min(p_table.shape) < 2
        or np.any(~np.isfinite(p_table))
        or np.any(~np.isfinite(q_table))
        or np.any(p_table < 0)
        or np.any(q_table < 0)
        or np.any(p_table != np.floor(p_table))
        or np.any(q_table != np.floor(q_table))
        or np.sum(p_table) <= 1
        or np.sum(q_table) <= 1
    ):
        raise ValueError("Tables must be matching nonnegative integer count tables.")

    rows, columns = p_table.shape
    counts_p = p_table.ravel()
    counts_q = q_table.ravel()
    cells = counts_p.size
    free = cells - 1
    empirical_p = counts_p / np.sum(counts_p)
    empirical_q = counts_q / np.sum(counts_q)
    smoothed_p = (counts_p + 0.5) / (np.sum(counts_p) + 0.5 * cells)
    smoothed_q = (counts_q + 0.5) / (np.sum(counts_q) + 0.5 * cells)
    pooled = (counts_p + counts_q + 1e-10) / (
        np.sum(counts_p) + np.sum(counts_q) + 1e-10 * cells
    )
    average = (empirical_p + empirical_q + 1e-10) / (
        np.sum(empirical_p + empirical_q + 1e-10)
    )
    all_starts = (
        np.concatenate(
            (
                _logits_from_probability(smoothed_p),
                _logits_from_probability(smoothed_q),
            )
        ),
        np.tile(_logits_from_probability(pooled), 2),
        np.tile(_logits_from_probability(average), 2),
    )
    starts = all_starts if multiple_starts else all_starts[:1]

    def objective(parameters: np.ndarray) -> float:
        value_p, _, _ = _multinomial_nll_and_gradient(
            parameters[:free],
            counts_p,
        )
        value_q, _, _ = _multinomial_nll_and_gradient(
            parameters[free:],
            counts_q,
        )
        return value_p + value_q

    def objective_gradient(parameters: np.ndarray) -> np.ndarray:
        _, gradient_p, _ = _multinomial_nll_and_gradient(
            parameters[:free],
            counts_p,
        )
        _, gradient_q, _ = _multinomial_nll_and_gradient(
            parameters[free:],
            counts_q,
        )
        return np.concatenate((gradient_p, gradient_q))

    def constraint(parameters: np.ndarray) -> float:
        probability_p = _softmax_reference(parameters[:free])
        probability_q = _softmax_reference(parameters[free:])
        mi_p, _ = _mi_and_logit_gradient(probability_p, rows, columns)
        mi_q, _ = _mi_and_logit_gradient(probability_q, rows, columns)
        return mi_p - mi_q

    def constraint_gradient(parameters: np.ndarray) -> np.ndarray:
        probability_p = _softmax_reference(parameters[:free])
        probability_q = _softmax_reference(parameters[free:])
        _, gradient_p = _mi_and_logit_gradient(probability_p, rows, columns)
        _, gradient_q = _mi_and_logit_gradient(probability_q, rows, columns)
        return np.concatenate((gradient_p, -gradient_q))

    unrestricted_objective = _unconstrained_nll(counts_p) + _unconstrained_nll(
        counts_q
    )
    candidates = []
    for initial in starts:
        result = minimize(
            objective,
            initial,
            jac=objective_gradient,
            method="SLSQP",
            bounds=[(-32.0, 32.0)] * (2 * free),
            constraints={
                "type": "eq",
                "fun": constraint,
                "jac": constraint_gradient,
            },
            options={
                "ftol": min(1e-10, tolerance * 0.01),
                "maxiter": maximum_iterations,
                "disp": False,
            },
        )
        residual = float(abs(constraint(result.x)))
        objective_gap = float(result.fun - unrestricted_objective)
        if (
            result.success
            and np.isfinite(result.fun)
            and residual <= tolerance
            and objective_gap >= -max(tolerance, 1e-7)
        ):
            candidates.append((result, residual, max(objective_gap, 0.0)))

    if not candidates:
        return ConstrainedLikelihoodRatioResult(
            statistic=float("nan"),
            p_value=float("nan"),
            constrained_mi=float("nan"),
            constraint_residual=float("nan"),
            objective_gap=float("nan"),
            iterations=0,
            converged=False,
            starts_attempted=len(starts),
            elapsed_seconds=perf_counter() - start_time,
        )

    result, residual, objective_gap = min(candidates, key=lambda item: item[0].fun)
    probability_p = _softmax_reference(result.x[:free])
    constrained_mi, _ = _mi_and_logit_gradient(
        probability_p,
        rows,
        columns,
    )
    statistic = 2.0 * objective_gap
    return ConstrainedLikelihoodRatioResult(
        statistic=statistic,
        p_value=float(chi2.sf(statistic, df=1)),
        constrained_mi=constrained_mi,
        constraint_residual=residual,
        objective_gap=objective_gap,
        iterations=int(result.nit),
        converged=True,
        starts_attempted=len(starts),
        elapsed_seconds=perf_counter() - start_time,
    )
