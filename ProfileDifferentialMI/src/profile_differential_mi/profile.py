"""Constrained multinomial profile tests for H0: I(P) = I(Q)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.optimize import brentq, minimize
from scipy.special import logsumexp, xlogy
from scipy.stats import chi2


@dataclass(frozen=True)
class ProfileTestResult:
    """Profile test statistics and numerical diagnostics for one table pair."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    observed_mi_p: float
    observed_mi_q: float
    observed_delta: float
    fitted_mi_p: float
    fitted_mi_q: float
    constraint_residual: float
    lr_statistic: float
    lr_p_value: float
    pearson_statistic: float
    pearson_p_value: float
    cr_2_3_statistic: float
    cr_2_3_p_value: float
    nll_unrestricted: float
    nll_constrained: float
    likelihood_gap: float
    starts_attempted: int
    starts_converged: int
    best_start_index: int
    optimizer_iterations: int
    optimizer_status: int
    optimizer_message: str
    kkt_residual: float
    relative_kkt_residual: float
    minimum_fitted_probability: float
    minimum_fitted_expected: float
    hit_logit_bound: bool
    trustworthy: bool
    elapsed_seconds: float
    fitted_probability_p: np.ndarray
    fitted_probability_q: np.ndarray

    def to_dict(self, *, include_probabilities: bool = False) -> dict:
        result = asdict(self)
        if not include_probabilities:
            del result["fitted_probability_p"]
            del result["fitted_probability_q"]
        return result


def _validated_tables(
    table_p: np.ndarray, table_q: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(table_p)
    q = np.asarray(table_q)
    if p.ndim != 2 or q.shape != p.shape or min(p.shape) < 2:
        raise ValueError("Tables must have the same two-dimensional shape.")
    if np.iscomplexobj(p) or np.iscomplexobj(q):
        raise ValueError("Counts must be finite nonnegative integers.")
    try:
        p_float = np.asarray(p, dtype=float)
        q_float = np.asarray(q, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Counts must be finite nonnegative integers.") from error
    for values in (p_float, q_float):
        if (
            np.any(~np.isfinite(values))
            or np.any(values < 0)
            or np.any(values != np.floor(values))
        ):
            raise ValueError("Counts must be finite nonnegative integers.")
    p_int = p_float.astype(np.int64)
    q_int = q_float.astype(np.int64)
    if min(int(p_int.sum()), int(q_int.sum())) <= 1:
        raise ValueError("Each table must contain at least two observations.")
    return p_int, q_int


def _mutual_information(probability: np.ndarray) -> float:
    p = np.asarray(probability, dtype=float)
    row = p.sum(axis=1)
    column = p.sum(axis=0)
    return float(
        np.sum(xlogy(p, p))
        - np.sum(xlogy(row, row))
        - np.sum(xlogy(column, column))
    )


def _mi_probability_gradient(probability: np.ndarray) -> np.ndarray:
    p = np.asarray(probability, dtype=float)
    row = p.sum(axis=1)
    column = p.sum(axis=0)
    return np.log(p) - np.log(row)[:, None] - np.log(column)[None, :] - 1.0


def _probability_to_reduced_logits(probability: np.ndarray) -> np.ndarray:
    flat = np.asarray(probability, dtype=float).reshape(-1)
    return np.log(flat[:-1]) - np.log(flat[-1])


def _reduced_logits_to_probability(
    logits: np.ndarray, shape: tuple[int, int]
) -> np.ndarray:
    full = np.concatenate((np.asarray(logits, dtype=float), np.zeros(1)))
    full -= logsumexp(full)
    return np.exp(full).reshape(shape)


def _mi_logit_gradient(probability: np.ndarray) -> np.ndarray:
    flat = np.asarray(probability, dtype=float).reshape(-1)
    gradient = _mi_probability_gradient(probability).reshape(-1)
    tangent_gradient = flat * (gradient - float(np.dot(flat, gradient)))
    return tangent_gradient[:-1]


def _split_probabilities(
    parameters: np.ndarray, shape: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray]:
    reduced_size = shape[0] * shape[1] - 1
    return (
        _reduced_logits_to_probability(parameters[:reduced_size], shape),
        _reduced_logits_to_probability(parameters[reduced_size:], shape),
    )


def _objective(
    parameters: np.ndarray,
    counts_p: np.ndarray,
    counts_q: np.ndarray,
) -> float:
    shape = counts_p.shape
    reduced_size = counts_p.size - 1
    logits_p = parameters[:reduced_size]
    logits_q = parameters[reduced_size:]
    nll_p = counts_p.sum() * logsumexp(np.append(logits_p, 0.0))
    nll_p -= float(np.dot(counts_p.reshape(-1)[:-1], logits_p))
    nll_q = counts_q.sum() * logsumexp(np.append(logits_q, 0.0))
    nll_q -= float(np.dot(counts_q.reshape(-1)[:-1], logits_q))
    return float(nll_p + nll_q)


def _objective_gradient(
    parameters: np.ndarray,
    counts_p: np.ndarray,
    counts_q: np.ndarray,
) -> np.ndarray:
    probability_p, probability_q = _split_probabilities(
        parameters, counts_p.shape
    )
    return np.concatenate(
        (
            counts_p.sum() * probability_p.reshape(-1)[:-1]
            - counts_p.reshape(-1)[:-1],
            counts_q.sum() * probability_q.reshape(-1)[:-1]
            - counts_q.reshape(-1)[:-1],
        )
    )


def _constraint(parameters: np.ndarray, shape: tuple[int, int]) -> float:
    probability_p, probability_q = _split_probabilities(parameters, shape)
    return _mutual_information(probability_p) - _mutual_information(probability_q)


def _constraint_gradient(
    parameters: np.ndarray, shape: tuple[int, int]
) -> np.ndarray:
    probability_p, probability_q = _split_probabilities(parameters, shape)
    return np.concatenate(
        (
            _mi_logit_gradient(probability_p),
            -_mi_logit_gradient(probability_q),
        )
    )


def _smoothed_probability(counts: np.ndarray, pseudocount: float) -> np.ndarray:
    values = np.asarray(counts, dtype=float) + pseudocount
    return values / values.sum()


def _independence_projection(probability: np.ndarray) -> np.ndarray:
    return np.outer(probability.sum(axis=1), probability.sum(axis=0))


def _mi_path_probability(
    probability: np.ndarray, target_mi: float
) -> np.ndarray:
    independence = _independence_projection(probability)
    endpoint_mi = _mutual_information(probability)
    if target_mi <= 1e-14:
        return independence
    if target_mi >= endpoint_mi - 1e-13:
        return probability

    def residual(weight: float) -> float:
        candidate = independence + weight * (probability - independence)
        return _mutual_information(candidate) - target_mi

    weight = brentq(residual, 0.0, 1.0, xtol=1e-13, rtol=1e-13)
    return independence + weight * (probability - independence)


def _feasible_starts(
    counts_p: np.ndarray,
    counts_q: np.ndarray,
    *,
    pseudocount: float,
    target_fractions: tuple[float, ...],
) -> list[np.ndarray]:
    probability_p = _smoothed_probability(counts_p, pseudocount)
    probability_q = _smoothed_probability(counts_q, pseudocount)
    common_maximum = min(
        _mutual_information(probability_p),
        _mutual_information(probability_q),
    )
    starts: list[np.ndarray] = []
    for fraction in target_fractions:
        target = max(1e-10, fraction * common_maximum)
        fitted_p = _mi_path_probability(probability_p, target)
        fitted_q = _mi_path_probability(probability_q, target)
        starts.append(
            np.concatenate(
                (
                    _probability_to_reduced_logits(fitted_p),
                    _probability_to_reduced_logits(fitted_q),
                )
            )
        )
    return starts


def _unrestricted_nll(counts: np.ndarray) -> float:
    total = float(counts.sum())
    return float(-np.sum(xlogy(counts, counts / total)))


def _power_divergence(
    observed: np.ndarray, expected: np.ndarray, power: float
) -> float:
    positive = observed > 0
    ratio_power = (observed[positive] / expected[positive]) ** power
    coefficient = 2.0 / (power * (power + 1.0))
    return float(
        coefficient * np.sum(observed[positive] * (ratio_power - 1.0))
    )


def profile_equal_mi_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    pseudocount: float = 0.5,
    target_fractions: tuple[float, ...] = (1.0, 0.75, 0.35),
    logit_bound: float = 30.0,
    max_iterations: int = 600,
    ftol: float = 1e-11,
    constraint_tolerance: float = 2e-7,
    relative_kkt_tolerance: float = 2e-4,
) -> ProfileTestResult:
    """Fit the equal-MI null and return three one-df profile tests.

    The pseudocount is used only to construct positive optimization starts. It
    is not added to the likelihood or the reported test statistics.
    """
    start_time = perf_counter()
    counts_p, counts_q = _validated_tables(table_p, table_q)
    if pseudocount <= 0 or logit_bound <= 0 or not target_fractions:
        raise ValueError("Optimization controls must be strictly positive.")
    if any(fraction <= 0 or fraction > 1 for fraction in target_fractions):
        raise ValueError("Every target fraction must lie in (0, 1].")

    shape = counts_p.shape
    starts = _feasible_starts(
        counts_p,
        counts_q,
        pseudocount=pseudocount,
        target_fractions=target_fractions,
    )
    bounds = [(-logit_bound, logit_bound)] * starts[0].size
    constraint = {
        "type": "eq",
        "fun": lambda value: _constraint(value, shape),
        "jac": lambda value: _constraint_gradient(value, shape),
    }

    candidates = []
    for index, initial in enumerate(starts):
        result = minimize(
            _objective,
            initial,
            args=(counts_p, counts_q),
            method="SLSQP",
            jac=_objective_gradient,
            bounds=bounds,
            constraints=(constraint,),
            options={
                "ftol": ftol,
                "maxiter": max_iterations,
                "disp": False,
            },
        )
        residual = abs(_constraint(result.x, shape))
        if np.isfinite(result.fun) and residual <= constraint_tolerance:
            candidates.append((float(result.fun), index, result))

    if candidates:
        _, best_start_index, best = min(candidates, key=lambda item: item[0])
    else:
        fallback_results = []
        for index, initial in enumerate(starts):
            fallback_results.append(
                (
                    abs(_constraint(initial, shape)),
                    _objective(initial, counts_p, counts_q),
                    index,
                    initial,
                )
            )
        _, fallback_nll, best_start_index, fallback = min(fallback_results)

        class _Fallback:
            x = fallback
            fun = fallback_nll
            success = False
            status = -1
            message = "No optimizer result met the constraint tolerance."
            nit = 0

        best = _Fallback()

    fitted_p, fitted_q = _split_probabilities(best.x, shape)
    fitted_mi_p = _mutual_information(fitted_p)
    fitted_mi_q = _mutual_information(fitted_q)
    constraint_residual = abs(fitted_mi_p - fitted_mi_q)

    nll_unrestricted = _unrestricted_nll(counts_p) + _unrestricted_nll(counts_q)
    nll_constrained = float(best.fun)
    likelihood_gap = nll_constrained - nll_unrestricted
    lr_statistic = max(0.0, 2.0 * likelihood_gap)

    expected_p = counts_p.sum() * fitted_p
    expected_q = counts_q.sum() * fitted_q
    pearson_statistic = float(
        np.sum((counts_p - expected_p) ** 2 / expected_p)
        + np.sum((counts_q - expected_q) ** 2 / expected_q)
    )
    cr_statistic = _power_divergence(counts_p, expected_p, 2.0 / 3.0)
    cr_statistic += _power_divergence(counts_q, expected_q, 2.0 / 3.0)
    cr_statistic = max(0.0, cr_statistic)

    objective_gradient = _objective_gradient(best.x, counts_p, counts_q)
    constraint_gradient = _constraint_gradient(best.x, shape)
    denominator = float(np.dot(constraint_gradient, constraint_gradient))
    multiplier = (
        -float(np.dot(objective_gradient, constraint_gradient)) / denominator
        if denominator > 0
        else 0.0
    )
    kkt_vector = objective_gradient + multiplier * constraint_gradient
    kkt_residual = float(np.linalg.norm(kkt_vector, ord=np.inf))
    objective_scale = max(
        1.0, float(np.linalg.norm(objective_gradient, ord=np.inf))
    )
    relative_kkt_residual = kkt_residual / objective_scale

    minimum_probability = float(min(fitted_p.min(), fitted_q.min()))
    minimum_expected = float(min(expected_p.min(), expected_q.min()))
    hit_logit_bound = bool(
        np.any(np.abs(best.x) >= logit_bound - 1e-5)
    )
    trustworthy = bool(
        best.success
        and np.isfinite(nll_constrained)
        and likelihood_gap >= -1e-6
        and constraint_residual <= constraint_tolerance
        and relative_kkt_residual <= relative_kkt_tolerance
    )

    observed_probability_p = counts_p / counts_p.sum()
    observed_probability_q = counts_q / counts_q.sum()
    observed_mi_p = _mutual_information(observed_probability_p)
    observed_mi_q = _mutual_information(observed_probability_q)
    return ProfileTestResult(
        rows=shape[0],
        columns=shape[1],
        n_p=int(counts_p.sum()),
        n_q=int(counts_q.sum()),
        observed_mi_p=observed_mi_p,
        observed_mi_q=observed_mi_q,
        observed_delta=observed_mi_p - observed_mi_q,
        fitted_mi_p=fitted_mi_p,
        fitted_mi_q=fitted_mi_q,
        constraint_residual=constraint_residual,
        lr_statistic=lr_statistic,
        lr_p_value=float(chi2.sf(lr_statistic, df=1)),
        pearson_statistic=pearson_statistic,
        pearson_p_value=float(chi2.sf(pearson_statistic, df=1)),
        cr_2_3_statistic=cr_statistic,
        cr_2_3_p_value=float(chi2.sf(cr_statistic, df=1)),
        nll_unrestricted=nll_unrestricted,
        nll_constrained=nll_constrained,
        likelihood_gap=likelihood_gap,
        starts_attempted=len(starts),
        starts_converged=len(candidates),
        best_start_index=best_start_index,
        optimizer_iterations=int(best.nit),
        optimizer_status=int(best.status),
        optimizer_message=str(best.message),
        kkt_residual=kkt_residual,
        relative_kkt_residual=relative_kkt_residual,
        minimum_fitted_probability=minimum_probability,
        minimum_fitted_expected=minimum_expected,
        hit_logit_bound=hit_logit_bound,
        trustworthy=trustworthy,
        elapsed_seconds=perf_counter() - start_time,
        fitted_probability_p=fitted_p,
        fitted_probability_q=fitted_q,
    )
