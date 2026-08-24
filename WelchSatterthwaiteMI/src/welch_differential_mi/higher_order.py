"""Experimental joint Cornish-Fisher calibration for differential MI."""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

from .welch import _validate_pair, differential_mi_pvalues


def _mi_variance_influence_moments(
    tables: np.ndarray,
) -> dict[str, np.ndarray]:
    """Return moments of the MI and MI-variance influence functions."""
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
    pointwise_information = log_probability - log_row - log_column

    mutual_information = np.sum(
        probability * pointwise_information,
        axis=(-2, -1),
    )
    mi_influence = pointwise_information - mutual_information[..., None, None]
    mi_variance = np.sum(
        probability * mi_influence**2,
        axis=(-2, -1),
    )
    mi_third_moment = np.sum(
        probability * mi_influence**3,
        axis=(-2, -1),
    )

    row_probability = row[..., 0]
    column_probability = column[..., 0, :]
    row_pointwise_mean = np.divide(
        np.sum(probability * pointwise_information, axis=-1),
        row_probability,
        out=np.zeros_like(row_probability),
        where=row_probability > 0,
    )
    column_pointwise_mean = np.divide(
        np.sum(probability * pointwise_information, axis=-2),
        column_probability,
        out=np.zeros_like(column_probability),
        where=column_probability > 0,
    )
    second_moment = mi_variance + mutual_information**2
    variance_influence = (
        pointwise_information**2
        - second_moment[..., None, None]
        + 2.0
        * (
            pointwise_information
            - row_pointwise_mean[..., :, None]
            - column_pointwise_mean[..., None, :]
            + mutual_information[..., None, None]
        )
        - 2.0 * mutual_information[..., None, None] * mi_influence
    )
    variance_influence_mean = np.sum(
        probability * variance_influence,
        axis=(-2, -1),
    )
    centered_variance_influence = (
        variance_influence - variance_influence_mean[..., None, None]
    )

    return {
        "mi_variance": mi_variance,
        "mi_third_moment": mi_third_moment,
        "mi_variance_influence_covariance": np.sum(
            probability * mi_influence * centered_variance_influence,
            axis=(-2, -1),
        ),
        "variance_influence_variance": np.sum(
            probability * centered_variance_influence**2,
            axis=(-2, -1),
        ),
    }


def joint_cornish_fisher_parameters(
    probability_p: np.ndarray,
    probability_q: np.ndarray,
    n_p: np.ndarray | float,
    n_q: np.ndarray | float,
    *,
    alpha: float = 0.05,
) -> dict[str, np.ndarray]:
    """Calculate joint-CF parameters from population-shaped probabilities."""
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie strictly between zero and one.")
    p = np.asarray(probability_p, dtype=float)
    q = np.asarray(probability_q, dtype=float)
    if p.ndim < 2 or q.shape != p.shape:
        raise ValueError("Probability tables must have matching shapes.")
    if np.any(~np.isfinite(p)) or np.any(~np.isfinite(q)):
        raise ValueError("Probabilities must be finite.")
    if np.any(p < 0.0) or np.any(q < 0.0):
        raise ValueError("Probabilities must be nonnegative.")
    p_total = p.sum(axis=(-2, -1), keepdims=True)
    q_total = q.sum(axis=(-2, -1), keepdims=True)
    if np.any(p_total <= 0.0) or np.any(q_total <= 0.0):
        raise ValueError("Probability tables must have positive mass.")
    p = p / p_total
    q = q / q_total
    n_p = np.asarray(n_p, dtype=float)
    n_q = np.asarray(n_q, dtype=float)
    if np.any(~np.isfinite(n_p)) or np.any(~np.isfinite(n_q)):
        raise ValueError("Sample sizes must be finite.")
    if np.any(n_p <= 1.0) or np.any(n_q <= 1.0):
        raise ValueError("Sample sizes must exceed one.")

    moments_p = _mi_variance_influence_moments(p)
    moments_q = _mi_variance_influence_moments(q)
    variance = moments_p["mi_variance"] / n_p + moments_q["mi_variance"] / n_q
    standard_deviation = np.sqrt(variance)
    numerator_third_cumulant = (
        moments_p["mi_third_moment"] / n_p**2
        - moments_q["mi_third_moment"] / n_q**2
    )
    numerator_variance_covariance = (
        moments_p["mi_variance_influence_covariance"] / n_p**2
        - moments_q["mi_variance_influence_covariance"] / n_q**2
    )
    denominator = standard_deviation**3
    mean_shift = np.divide(
        -0.5 * numerator_variance_covariance,
        denominator,
        out=np.full_like(variance, np.nan, dtype=float),
        where=np.isfinite(denominator) & (denominator > 0),
    )
    skewness = np.divide(
        numerator_third_cumulant - 3.0 * numerator_variance_covariance,
        denominator,
        out=np.full_like(variance, np.nan, dtype=float),
        where=np.isfinite(denominator) & (denominator > 0),
    )
    z_lower = float(norm.ppf(alpha / 2.0))
    z_upper = float(norm.ppf(1.0 - alpha / 2.0))
    lower_critical = mean_shift + z_lower + skewness * (z_lower**2 - 1.0) / 6.0
    upper_critical = mean_shift + z_upper + skewness * (z_upper**2 - 1.0) / 6.0
    valid = (
        np.isfinite(mean_shift)
        & np.isfinite(skewness)
        & np.isfinite(lower_critical)
        & np.isfinite(upper_critical)
        & (lower_critical < upper_critical)
    )
    return {
        "mean_shift": mean_shift,
        "skewness": skewness,
        "lower_critical": lower_critical,
        "upper_critical": upper_critical,
        "valid": valid,
    }


def joint_cornish_fisher_values(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    alpha: float = 0.05,
    base_values: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    """Estimate first-order joint Cornish-Fisher rejection boundaries.

    The expansion treats the MI difference and its estimated variance as a
    joint asymptotically linear pair. It estimates the resulting mean shift
    and skewness of the studentized statistic, then applies the first
    Cornish-Fisher quantile correction.
    """
    p, q = _validate_pair(table_p, table_q)
    if base_values is None:
        base_values = differential_mi_pvalues(
            p,
            q,
            include_simple=False,
            include_expanded=False,
            include_unbiased_sensitivity=False,
        )

    n_p = p.sum(axis=(-2, -1))
    n_q = q.sum(axis=(-2, -1))
    parameters = joint_cornish_fisher_parameters(
        p,
        q,
        n_p,
        n_q,
        alpha=alpha,
    )
    mean_shift = parameters["mean_shift"]
    skewness = parameters["skewness"]
    lower_critical = parameters["lower_critical"]
    upper_critical = parameters["upper_critical"]
    statistic = np.asarray(base_values["statistic"], dtype=float)
    base_valid = np.asarray(base_values["base_valid"], dtype=bool)
    valid = base_valid & parameters["valid"]
    rejected = valid & (
        (statistic < lower_critical) | (statistic > upper_critical)
    )
    return {
        "mean_shift": mean_shift,
        "skewness": skewness,
        "lower_critical": lower_critical,
        "upper_critical": upper_critical,
        "valid": valid,
        "rejected": rejected,
    }
