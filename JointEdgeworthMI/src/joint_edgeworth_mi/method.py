"""Joint studentized Edgeworth inference for differential mutual information."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.stats import norm

from influence_df_mi import differential_mi_pvalues as base_mi_pvalues


@dataclass(frozen=True)
class JointEdgeworthResult:
    """Scalar differential-MI result with a joint Edgeworth reference."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    degrees_of_freedom_mi: int
    delta_corrected: float
    standard_error: float
    statistic: float
    normal_p_value: float
    naive_welch_p_value: float
    influence_welch_p_value: float
    mi_third_moment_p: float
    mi_third_moment_q: float
    mi_variance_covariance_p: float
    mi_variance_covariance_q: float
    numerator_third_cumulant: float
    numerator_variance_covariance: float
    standardized_third_cumulant: float
    standardized_variance_covariance: float
    edgeworth_correction: float
    edgeworth_cdf: float
    edgeworth_density_factor: float
    edgeworth_p_value: float
    base_valid: bool
    edgeworth_valid: bool
    elapsed_seconds: float

    def to_dict(self) -> dict:
        return asdict(self)


def _joint_influence_moments(
    values: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """Calculate MI and variance-functional influence cross-moments."""
    counts = np.asarray(values, dtype=float)
    if counts.ndim < 2 or np.any(~np.isfinite(counts)) or np.any(counts < 0):
        raise ValueError("Values must be finite and nonnegative.")
    totals = counts.sum(axis=(-2, -1), keepdims=True)
    if np.any(totals <= 0):
        raise ValueError("Every distribution must have positive total mass.")
    probability = counts / totals
    row_mass = probability.sum(axis=-1)
    column_mass = probability.sum(axis=-2)

    log_probability = np.zeros_like(probability)
    log_row = np.zeros_like(row_mass)
    log_column = np.zeros_like(column_mass)
    np.log(probability, out=log_probability, where=probability > 0)
    np.log(row_mass, out=log_row, where=row_mass > 0)
    np.log(column_mass, out=log_column, where=column_mass > 0)
    score = log_probability - log_row[..., :, None] - log_column[..., None, :]

    mean = np.sum(probability * score, axis=(-2, -1))
    centered_score = score - mean[..., None, None]
    variance = np.sum(
        probability * centered_score**2,
        axis=(-2, -1),
    )
    third_moment = np.sum(
        probability * centered_score**3,
        axis=(-2, -1),
    )
    second_moment = np.sum(probability * score**2, axis=(-2, -1))

    row_score_sum = np.sum(probability * score, axis=-1)
    column_score_sum = np.sum(probability * score, axis=-2)
    row_score_mean = np.divide(
        row_score_sum,
        row_mass,
        out=np.zeros_like(row_score_sum),
        where=row_mass > 0,
    )
    column_score_mean = np.divide(
        column_score_sum,
        column_mass,
        out=np.zeros_like(column_score_sum),
        where=column_mass > 0,
    )
    expanded_mean = mean[..., None, None]
    variance_influence = (
        score**2
        - second_moment[..., None, None]
        + 2.0
        * (
            score
            - row_score_mean[..., :, None]
            - column_score_mean[..., None, :]
            + expanded_mean
        )
        - 2.0 * expanded_mean * (score - expanded_mean)
    )
    covariance = np.sum(
        probability * centered_score * variance_influence,
        axis=(-2, -1),
    )
    variance_influence_mean = np.sum(
        probability * variance_influence,
        axis=(-2, -1),
    )

    scalar = mean.ndim == 0
    result: dict[str, np.ndarray | float] = {
        "mutual_information": mean,
        "variance": np.maximum(variance, 0.0),
        "mi_influence": centered_score,
        "variance_influence": variance_influence,
        "mi_influence_mean": np.sum(
            probability * centered_score,
            axis=(-2, -1),
        ),
        "variance_influence_mean": variance_influence_mean,
        "third_moment": third_moment,
        "covariance": covariance,
    }
    if scalar:
        for key in (
            "mutual_information",
            "variance",
            "mi_influence_mean",
            "variance_influence_mean",
            "third_moment",
            "covariance",
        ):
            result[key] = float(result[key])
    return result


def studentized_edgeworth_cdf(
    statistic: np.ndarray | float,
    standardized_third_cumulant: np.ndarray | float,
    standardized_variance_covariance: np.ndarray | float,
) -> dict[str, np.ndarray | float]:
    """Evaluate the first joint studentized-Edgeworth CDF correction."""
    x = np.asarray(statistic, dtype=float)
    skew = np.asarray(standardized_third_cumulant, dtype=float)
    covariance = np.asarray(standardized_variance_covariance, dtype=float)
    correction_polynomial = (
        skew * (1.0 - x**2) / 6.0
        + covariance * x**2 / 2.0
    )
    correction = norm.pdf(x) * correction_polynomial
    raw_cdf = norm.cdf(x) + correction
    a0 = skew / 6.0
    a2 = -skew / 6.0 + covariance / 2.0
    density_factor = 1.0 + (2.0 * a2 - a0) * x - a2 * x**3
    valid = (
        np.isfinite(x)
        & np.isfinite(skew)
        & np.isfinite(covariance)
        & np.isfinite(correction)
        & np.isfinite(raw_cdf)
        & (raw_cdf >= 0.0)
        & (raw_cdf <= 1.0)
        & np.isfinite(density_factor)
        & (density_factor > 0.0)
    )
    cdf = np.where(valid, np.clip(raw_cdf, 0.0, 1.0), np.nan)
    p_value = np.where(
        valid,
        np.clip(2.0 * np.minimum(cdf, 1.0 - cdf), 0.0, 1.0),
        np.nan,
    )
    scalar = x.ndim == 0 and skew.ndim == 0 and covariance.ndim == 0
    return {
        "correction": float(correction) if scalar else correction,
        "raw_cdf": float(raw_cdf) if scalar else raw_cdf,
        "cdf": float(cdf) if scalar else cdf,
        "density_factor": float(density_factor) if scalar else density_factor,
        "p_value": float(p_value) if scalar else p_value,
        "valid": bool(valid) if scalar else valid,
    }


def differential_mi_pvalues(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> dict[str, np.ndarray]:
    """Calculate legacy references and the joint Edgeworth p-value."""
    base = base_mi_pvalues(table_p, table_q)
    p = np.asarray(table_p, dtype=float)
    q = np.asarray(table_q, dtype=float)
    n_p = p.sum(axis=(-2, -1))
    n_q = q.sum(axis=(-2, -1))

    moments_p = _joint_influence_moments(p)
    moments_q = _joint_influence_moments(q)
    third_p = np.asarray(moments_p["third_moment"])
    third_q = np.asarray(moments_q["third_moment"])
    covariance_p = np.asarray(moments_p["covariance"])
    covariance_q = np.asarray(moments_q["covariance"])

    numerator_third_cumulant = third_p / n_p**2 - third_q / n_q**2
    numerator_variance_covariance = (
        covariance_p / n_p**2 - covariance_q / n_q**2
    )
    squared_standard_error = np.asarray(base["standard_error"]) ** 2
    scaling = squared_standard_error**1.5
    standardized_third_cumulant = np.divide(
        numerator_third_cumulant,
        scaling,
        out=np.full_like(numerator_third_cumulant, np.nan, dtype=float),
        where=np.isfinite(scaling) & (scaling > 0),
    )
    standardized_variance_covariance = np.divide(
        numerator_variance_covariance,
        scaling,
        out=np.full_like(numerator_variance_covariance, np.nan, dtype=float),
        where=np.isfinite(scaling) & (scaling > 0),
    )
    edgeworth = studentized_edgeworth_cdf(
        base["statistic"],
        standardized_third_cumulant,
        standardized_variance_covariance,
    )
    base_valid = np.asarray(base["valid"], dtype=bool)
    edgeworth_valid = base_valid & np.asarray(edgeworth["valid"], dtype=bool)
    edgeworth_p = np.where(
        edgeworth_valid,
        np.asarray(edgeworth["p_value"]),
        np.nan,
    )

    return {
        **base,
        "mi_third_moment_p": third_p,
        "mi_third_moment_q": third_q,
        "mi_variance_covariance_p": covariance_p,
        "mi_variance_covariance_q": covariance_q,
        "numerator_third_cumulant": numerator_third_cumulant,
        "numerator_variance_covariance": numerator_variance_covariance,
        "standardized_third_cumulant": standardized_third_cumulant,
        "standardized_variance_covariance": (
            standardized_variance_covariance
        ),
        "edgeworth_correction": np.asarray(edgeworth["correction"]),
        "edgeworth_cdf": np.asarray(edgeworth["cdf"]),
        "edgeworth_density_factor": np.asarray(edgeworth["density_factor"]),
        "edgeworth_p_value": edgeworth_p,
        "base_valid": base_valid,
        "edgeworth_valid": edgeworth_valid,
        "valid": edgeworth_valid,
    }


def joint_edgeworth_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> JointEdgeworthResult:
    """Return scalar joint-Edgeworth inference for two count tables."""
    start = perf_counter()
    p = np.asarray(table_p)
    q = np.asarray(table_q)
    if p.ndim != 2 or q.ndim != 2:
        raise ValueError("The scalar API expects exactly two-dimensional tables.")
    values = differential_mi_pvalues(p, q)
    rows, columns = p.shape
    return JointEdgeworthResult(
        rows=rows,
        columns=columns,
        n_p=int(p.sum()),
        n_q=int(q.sum()),
        degrees_of_freedom_mi=(rows - 1) * (columns - 1),
        delta_corrected=float(values["delta_corrected"]),
        standard_error=float(values["standard_error"]),
        statistic=float(values["statistic"]),
        normal_p_value=float(values["normal_p_value"]),
        naive_welch_p_value=float(values["naive_welch_p_value"]),
        influence_welch_p_value=float(values["influence_welch_p_value"]),
        mi_third_moment_p=float(values["mi_third_moment_p"]),
        mi_third_moment_q=float(values["mi_third_moment_q"]),
        mi_variance_covariance_p=float(
            values["mi_variance_covariance_p"]
        ),
        mi_variance_covariance_q=float(
            values["mi_variance_covariance_q"]
        ),
        numerator_third_cumulant=float(
            values["numerator_third_cumulant"]
        ),
        numerator_variance_covariance=float(
            values["numerator_variance_covariance"]
        ),
        standardized_third_cumulant=float(
            values["standardized_third_cumulant"]
        ),
        standardized_variance_covariance=float(
            values["standardized_variance_covariance"]
        ),
        edgeworth_correction=float(values["edgeworth_correction"]),
        edgeworth_cdf=float(values["edgeworth_cdf"]),
        edgeworth_density_factor=float(values["edgeworth_density_factor"]),
        edgeworth_p_value=float(values["edgeworth_p_value"]),
        base_valid=bool(values["base_valid"]),
        edgeworth_valid=bool(values["edgeworth_valid"]),
        elapsed_seconds=perf_counter() - start,
    )
