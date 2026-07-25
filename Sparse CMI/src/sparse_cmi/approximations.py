from __future__ import annotations

import numpy as np
from scipy.stats import norm


def normal_pvalue(
    statistic: float | np.ndarray,
    mean: float | np.ndarray,
    variance: float | np.ndarray,
) -> float | np.ndarray:
    values, means, variances = np.broadcast_arrays(
        np.asarray(statistic, dtype=np.float64),
        np.asarray(mean, dtype=np.float64),
        np.asarray(variance, dtype=np.float64),
    )
    positive = variances > 0
    z_score = np.zeros_like(values)
    np.divide(
        values - means,
        np.sqrt(np.maximum(variances, 0.0)),
        out=z_score,
        where=positive,
    )
    result = np.where(
        positive,
        norm.sf(z_score),
        np.where(values <= means + 1e-12, 1.0, 0.0),
    )
    return float(result) if result.ndim == 0 else result


def edgeworth_pvalue(
    statistic: float | np.ndarray,
    mean: float | np.ndarray,
    variance: float | np.ndarray,
    skewness: float | np.ndarray,
) -> float | np.ndarray:
    values, means, variances, skewnesses = np.broadcast_arrays(
        np.asarray(statistic, dtype=np.float64),
        np.asarray(mean, dtype=np.float64),
        np.asarray(variance, dtype=np.float64),
        np.asarray(skewness, dtype=np.float64),
    )
    positive = variances > 0
    z_score = np.zeros_like(values)
    np.divide(
        values - means,
        np.sqrt(np.maximum(variances, 0.0)),
        out=z_score,
        where=positive,
    )
    cdf = norm.cdf(z_score) + (
        skewnesses / 6.0
    ) * (1.0 - z_score**2) * norm.pdf(z_score)
    result = np.where(
        positive,
        np.clip(1.0 - cdf, 0.0, 1.0),
        np.where(values <= means + 1e-12, 1.0, 0.0),
    )
    return float(result) if result.ndim == 0 else result


def cornish_fisher_critical_value(
    alpha: float,
    mean: float,
    variance: float,
    skewness: float,
) -> float:
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    if variance <= 0:
        return float("inf")
    z_score = float(norm.ppf(1.0 - alpha))
    correction = z_score + skewness * (z_score**2 - 1.0) / 6.0
    return float(mean + np.sqrt(variance) * correction)
