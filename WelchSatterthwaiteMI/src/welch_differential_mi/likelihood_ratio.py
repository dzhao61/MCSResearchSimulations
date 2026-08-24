"""Constrained likelihood-ratio inference for equality of two discrete MIs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.optimize import minimize
from scipy.special import xlogy
from scipy.stats import chi2


@dataclass(frozen=True)
class ConstrainedLikelihoodRatioResult:
    """Result of fitting two multinomials under the constraint I(P) = I(Q)."""

    statistic: float
    p_value: float
    constrained_mi: float
    constraint_residual: float
    objective_gap: float
    iterations: int
    converged: bool
    starts_attempted: int
    elapsed_seconds: float

    def to_dict(self) -> dict:
        return asdict(self)


def _validate_table_pair(
    table_p: np.ndarray, table_q: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(table_p)
    q = np.asarray(table_q)
    if p.ndim != 2 or q.shape != p.shape or min(p.shape) < 2:
        raise ValueError("Tables must be matching two-dimensional contingency tables.")
    if np.iscomplexobj(p) or np.iscomplexobj(q):
        raise ValueError("Counts must be finite nonnegative integers.")
    try:
        p_float = np.asarray(p, dtype=float)
        q_float = np.asarray(q, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Counts must be finite nonnegative integers.") from error
    for table in (p_float, q_float):
        if (
            np.any(~np.isfinite(table))
            or np.any(table < 0)
            or np.any(table != np.floor(table))
            or table.sum() <= 0
        ):
            raise ValueError("Counts must be finite nonnegative integers with positive totals.")
    return p_float, q_float


def _softmax_reference(logits: np.ndarray) -> np.ndarray:
    """Map K-1 logits to K probabilities, using the final cell as reference."""
    extended = np.append(np.asarray(logits, dtype=float), 0.0)
    shifted = extended - np.max(extended)
    exponential = np.exp(shifted)
    return exponential / exponential.sum()


def _logits_from_probability(probability: np.ndarray) -> np.ndarray:
    values = np.asarray(probability, dtype=float).reshape(-1)
    values = np.maximum(values, 1e-14)
    values /= values.sum()
    return np.log(values[:-1]) - np.log(values[-1])


def _mi_and_logit_gradient(
    probability: np.ndarray, rows: int, columns: int
) -> tuple[float, np.ndarray]:
    """Return MI and its derivative with respect to reference-cell logits."""
    table = np.asarray(probability, dtype=float).reshape(rows, columns)
    row = table.sum(axis=1, keepdims=True)
    column = table.sum(axis=0, keepdims=True)
    pointwise_information = np.log(table) - np.log(row) - np.log(column)
    mutual_information = float(np.sum(table * pointwise_information))
    full_gradient = table.reshape(-1) * (
        pointwise_information.reshape(-1) - mutual_information
    )
    return mutual_information, full_gradient[:-1]


def _multinomial_nll_and_gradient(
    logits: np.ndarray, counts: np.ndarray
) -> tuple[float, np.ndarray]:
    probability = _softmax_reference(logits)
    flat_counts = np.asarray(counts, dtype=float).reshape(-1)
    objective = float(-np.sum(xlogy(flat_counts, probability)))
    gradient = flat_counts.sum() * probability[:-1] - flat_counts[:-1]
    return objective, gradient


def _unconstrained_nll(counts: np.ndarray) -> float:
    flat_counts = np.asarray(counts, dtype=float).reshape(-1)
    probability = flat_counts / flat_counts.sum()
    return float(-np.sum(xlogy(flat_counts, probability)))


def _starting_values(counts_p: np.ndarray, counts_q: np.ndarray) -> list[np.ndarray]:
    size = counts_p.size

    def smooth(counts: np.ndarray) -> np.ndarray:
        values = counts.reshape(-1) + 0.5
        return values / values.sum()

    observed_p = smooth(counts_p)
    observed_q = smooth(counts_q)
    pooled = (counts_p.reshape(-1) + counts_q.reshape(-1) + 0.5)
    pooled /= pooled.sum()
    uniform = np.full(size, 1.0 / size)

    probability_pairs = (
        (observed_p, observed_q),
        (pooled, pooled),
        (observed_p, observed_p),
        (observed_q, observed_q),
        (uniform, uniform),
    )
    starts: list[np.ndarray] = []
    for probability_p, probability_q in probability_pairs:
        candidate = np.concatenate(
            [
                _logits_from_probability(probability_p),
                _logits_from_probability(probability_q),
            ]
        )
        if not any(np.allclose(candidate, existing) for existing in starts):
            starts.append(candidate)
    return starts


def constrained_likelihood_ratio_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    tolerance: float = 1e-8,
    maximum_iterations: int = 500,
    multiple_starts: bool = True,
    maximum_starts: int | None = None,
) -> ConstrainedLikelihoodRatioResult:
    """Test I(P) = I(Q) by constrained multinomial maximum likelihood.

    The reference p-value uses the regular asymptotic chi-squared distribution
    with one degree of freedom. Calibration near independence or a probability
    boundary must be assessed empirically because regularity can fail there.
    """
    start_time = perf_counter()
    counts_p, counts_q = _validate_table_pair(table_p, table_q)
    if (
        tolerance <= 0
        or maximum_iterations < 1
        or (maximum_starts is not None and maximum_starts < 1)
    ):
        raise ValueError("Tolerance, iterations, and starts must be positive.")

    rows, columns = counts_p.shape
    parameter_count = counts_p.size - 1
    unconstrained_nll = _unconstrained_nll(counts_p) + _unconstrained_nll(counts_q)

    def objective(parameters: np.ndarray) -> float:
        value_p, _ = _multinomial_nll_and_gradient(
            parameters[:parameter_count], counts_p
        )
        value_q, _ = _multinomial_nll_and_gradient(
            parameters[parameter_count:], counts_q
        )
        return value_p + value_q

    def objective_gradient(parameters: np.ndarray) -> np.ndarray:
        _, gradient_p = _multinomial_nll_and_gradient(
            parameters[:parameter_count], counts_p
        )
        _, gradient_q = _multinomial_nll_and_gradient(
            parameters[parameter_count:], counts_q
        )
        return np.concatenate([gradient_p, gradient_q])

    def equality_constraint(parameters: np.ndarray) -> float:
        probability_p = _softmax_reference(parameters[:parameter_count])
        probability_q = _softmax_reference(parameters[parameter_count:])
        mi_p, _ = _mi_and_logit_gradient(probability_p, rows, columns)
        mi_q, _ = _mi_and_logit_gradient(probability_q, rows, columns)
        return mi_p - mi_q

    def equality_jacobian(parameters: np.ndarray) -> np.ndarray:
        probability_p = _softmax_reference(parameters[:parameter_count])
        probability_q = _softmax_reference(parameters[parameter_count:])
        _, gradient_p = _mi_and_logit_gradient(probability_p, rows, columns)
        _, gradient_q = _mi_and_logit_gradient(probability_q, rows, columns)
        return np.concatenate([gradient_p, -gradient_q])

    starts = _starting_values(counts_p, counts_q)
    if not multiple_starts:
        starts = starts[:1]
    elif maximum_starts is not None:
        starts = starts[:maximum_starts]
    constraint = {"type": "eq", "fun": equality_constraint, "jac": equality_jacobian}
    bounds = [(-32.0, 32.0)] * (2 * parameter_count)
    candidates = []
    for initial in starts:
        fitted = minimize(
            objective,
            initial,
            method="SLSQP",
            jac=objective_gradient,
            bounds=bounds,
            constraints=constraint,
            options={"ftol": tolerance, "maxiter": maximum_iterations, "disp": False},
        )
        residual = abs(float(equality_constraint(fitted.x)))
        objective_gap = float(fitted.fun - unconstrained_nll)
        acceptable = (
            fitted.success
            and np.isfinite(fitted.fun)
            and residual <= max(10.0 * tolerance, 1e-7)
            and objective_gap >= -max(10.0 * tolerance, 1e-7)
        )
        if acceptable:
            candidates.append((float(fitted.fun), residual, fitted, objective_gap))

    elapsed = perf_counter() - start_time
    if not candidates:
        return ConstrainedLikelihoodRatioResult(
            statistic=np.nan,
            p_value=np.nan,
            constrained_mi=np.nan,
            constraint_residual=np.nan,
            objective_gap=np.nan,
            iterations=0,
            converged=False,
            starts_attempted=len(starts),
            elapsed_seconds=elapsed,
        )

    _, residual, fitted, objective_gap = min(candidates, key=lambda item: item[0])
    objective_gap = max(0.0, objective_gap)
    if objective_gap <= tolerance:
        objective_gap = 0.0
    statistic = 2.0 * objective_gap
    probability_p = _softmax_reference(fitted.x[:parameter_count])
    constrained_mi, _ = _mi_and_logit_gradient(probability_p, rows, columns)
    return ConstrainedLikelihoodRatioResult(
        statistic=statistic,
        p_value=float(chi2.sf(statistic, df=1)),
        constrained_mi=constrained_mi,
        constraint_residual=residual,
        objective_gap=objective_gap,
        iterations=int(fitted.nit),
        converged=True,
        starts_attempted=len(starts),
        elapsed_seconds=elapsed,
    )
