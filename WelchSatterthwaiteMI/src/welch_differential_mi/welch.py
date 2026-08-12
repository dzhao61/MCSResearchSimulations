"""Finite-df references for bias-corrected differential-MI Wald inference."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.stats import norm, t

from differential_mi.statistics import influence_variance, plugin_mi

@dataclass(frozen=True)
class WelchResult:
    """Normal and finite-df inference for one pair of discrete tables."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    degrees_of_freedom_mi: int
    delta_corrected: float
    influence_variance_p: float
    influence_variance_q: float
    standard_error: float
    statistic: float
    normal_p_value: float
    welch_degrees_of_freedom: float
    welch_p_value: float
    expanded_welch_degrees_of_freedom: float
    expanded_welch_p_value: float
    unbiased_standard_error: float
    unbiased_statistic: float
    unbiased_welch_degrees_of_freedom: float
    unbiased_welch_p_value: float
    valid: bool
    expanded_valid: bool
    elapsed_seconds: float

    def to_dict(self) -> dict:
        return asdict(self)


def _validate_pair(
    table_p: np.ndarray, table_q: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(table_p)
    q = np.asarray(table_q)
    if p.ndim < 2 or q.shape != p.shape:
        raise ValueError("Tables must have matching shapes and at least two dimensions.")
    if min(p.shape[-2:]) < 2:
        raise ValueError("Both table dimensions must contain at least two categories.")
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
    totals_p = p_float.sum(axis=(-2, -1))
    totals_q = q_float.sum(axis=(-2, -1))
    if np.any(totals_p <= 1) or np.any(totals_q <= 1):
        raise ValueError("Every table must contain at least two observations.")
    return p_float, q_float


def _welch_df(
    component_p: np.ndarray,
    component_q: np.ndarray,
    n_p: np.ndarray,
    n_q: np.ndarray,
) -> np.ndarray:
    return _combine_df(
        component_p,
        component_q,
        n_p - 1.0,
        n_q - 1.0,
    )


def _combine_df(
    component_p: np.ndarray,
    component_q: np.ndarray,
    degrees_of_freedom_p: np.ndarray,
    degrees_of_freedom_q: np.ndarray,
) -> np.ndarray:
    numerator = (component_p + component_q) ** 2
    denominator = (
        component_p**2 / degrees_of_freedom_p
        + component_q**2 / degrees_of_freedom_q
    )
    return np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan, dtype=float),
        where=np.isfinite(denominator) & (denominator > 0),
    )


def _variance_influence_component_df(
    table: np.ndarray,
    influence_variance_value: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate component df from the MI-variance influence function."""
    component_df, influence_variance, _, _ = _joint_influence_moments(
        table,
        influence_variance_value,
    )
    return component_df, influence_variance


def _joint_influence_moments(
    table: np.ndarray,
    influence_variance_value: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return variance-IF df, variance, MI skew moment, and cross-moment."""
    counts = np.asarray(table, dtype=float)
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
    variance = np.asarray(influence_variance_value, dtype=float)
    second_moment = variance + mean**2

    row_probability = row[..., 0]
    column_probability = column[..., 0, :]
    row_score_mean = np.divide(
        np.sum(probability * score, axis=-1),
        row_probability,
        out=np.zeros_like(row_probability),
        where=row_probability > 0,
    )
    column_score_mean = np.divide(
        np.sum(probability * score, axis=-2),
        column_probability,
        out=np.zeros_like(column_probability),
        where=column_probability > 0,
    )
    variance_influence = (
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
    influence_mean = np.sum(
        probability * variance_influence,
        axis=(-2, -1),
    )
    influence_variance = np.sum(
        probability
        * (variance_influence - influence_mean[..., None, None]) ** 2,
        axis=(-2, -1),
    )
    third_moment = np.sum(
        probability * centered**3,
        axis=(-2, -1),
    )
    cross_moment = np.sum(
        probability
        * centered
        * (variance_influence - influence_mean[..., None, None]),
        axis=(-2, -1),
    )

    sample_size = totals[..., 0, 0]
    numerator = 2.0 * sample_size * variance**2
    component_df = np.divide(
        numerator,
        influence_variance,
        out=np.full_like(variance, np.nan, dtype=float),
        where=np.isfinite(influence_variance) & (influence_variance > 0),
    )
    return component_df, influence_variance, third_moment, cross_moment


def _edgeworth_cdf(
    statistic: np.ndarray,
    baseline_cdf: np.ndarray,
    standardized_third_cumulant: np.ndarray,
    studentization_covariance: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply the first-order correction for a generally studentized pivot."""
    statistic = np.asarray(statistic, dtype=float)
    adjustment = (
        standardized_third_cumulant * (1.0 - statistic**2) / 6.0
        + studentization_covariance * statistic**2 / 2.0
    )
    cdf = np.asarray(baseline_cdf, dtype=float) + norm.pdf(statistic) * adjustment
    return cdf, adjustment


def joint_influence_pvalues(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> dict[str, np.ndarray]:
    """Experimental joint-influence corrections for differential MI.

    The first-order CDF correction accounts for both numerator skewness and
    covariance between the MI difference and its estimated squared standard
    error. The normal version isolates this correction; the Welch version adds
    it to the existing expanded finite-df reference.
    """
    p, q = _validate_pair(table_p, table_q)
    base = differential_mi_pvalues(
        p,
        q,
        include_simple=True,
        include_expanded=True,
        include_unbiased_sensitivity=False,
    )
    totals_p = p.sum(axis=(-2, -1))
    totals_q = q.sum(axis=(-2, -1))
    variance_p = base["influence_variance_p"]
    variance_q = base["influence_variance_q"]
    _, _, third_moment_p, cross_moment_p = _joint_influence_moments(
        p,
        variance_p,
    )
    _, _, third_moment_q, cross_moment_q = _joint_influence_moments(
        q,
        variance_q,
    )

    standard_error = base["standard_error"]
    standard_error_cubed = standard_error**3
    third_cumulant = (
        third_moment_p / totals_p**2 - third_moment_q / totals_q**2
    )
    numerator_denominator_covariance = (
        cross_moment_p / totals_p**2 - cross_moment_q / totals_q**2
    )
    standardized_third_cumulant = np.divide(
        third_cumulant,
        standard_error_cubed,
        out=np.full_like(standard_error, np.nan, dtype=float),
        where=np.isfinite(standard_error_cubed) & (standard_error_cubed > 0),
    )
    studentization_covariance = np.divide(
        numerator_denominator_covariance,
        standard_error_cubed,
        out=np.full_like(standard_error, np.nan, dtype=float),
        where=np.isfinite(standard_error_cubed) & (standard_error_cubed > 0),
    )

    statistic = base["statistic"]
    normal_cdf, edgeworth_adjustment = _edgeworth_cdf(
        statistic,
        norm.cdf(statistic),
        standardized_third_cumulant,
        studentization_covariance,
    )
    expanded_df = base["expanded_welch_degrees_of_freedom"]
    expanded_cdf, _ = _edgeworth_cdf(
        statistic,
        t.cdf(statistic, df=expanded_df),
        standardized_third_cumulant,
        studentization_covariance,
    )

    moment_valid = (
        base["base_valid"]
        & np.isfinite(standardized_third_cumulant)
        & np.isfinite(studentization_covariance)
        & np.isfinite(edgeworth_adjustment)
    )
    edgeworth_valid = (
        moment_valid
        & np.isfinite(normal_cdf)
        & (normal_cdf >= 0.0)
        & (normal_cdf <= 1.0)
    )
    joint_welch_valid = (
        moment_valid
        & base["expanded_valid"]
        & np.isfinite(expanded_cdf)
        & (expanded_cdf >= 0.0)
        & (expanded_cdf <= 1.0)
    )
    edgeworth_p = 2.0 * np.minimum(normal_cdf, 1.0 - normal_cdf)
    joint_welch_p = 2.0 * np.minimum(expanded_cdf, 1.0 - expanded_cdf)

    return {
        **base,
        "mi_third_moment_p": third_moment_p,
        "mi_third_moment_q": third_moment_q,
        "mi_variance_cross_moment_p": cross_moment_p,
        "mi_variance_cross_moment_q": cross_moment_q,
        "standardized_third_cumulant": standardized_third_cumulant,
        "studentization_covariance": studentization_covariance,
        "edgeworth_adjustment": edgeworth_adjustment,
        "edgeworth_normal_cdf": normal_cdf,
        "edgeworth_normal_p_value": np.where(
            edgeworth_valid,
            edgeworth_p,
            np.nan,
        ),
        "joint_influence_welch_cdf": expanded_cdf,
        "joint_influence_welch_p_value": np.where(
            joint_welch_valid,
            joint_welch_p,
            np.nan,
        ),
        "edgeworth_valid": edgeworth_valid,
        "joint_influence_welch_valid": joint_welch_valid,
    }


def differential_mi_pvalues(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    include_simple: bool = True,
    include_expanded: bool = True,
    include_unbiased_sensitivity: bool = True,
) -> dict[str, np.ndarray]:
    """Vectorized normal and Welch p-values for one pair or table batches."""
    p, q = _validate_pair(table_p, table_q)
    totals_p = p.sum(axis=(-2, -1))
    totals_q = q.sum(axis=(-2, -1))
    rows, columns = p.shape[-2:]
    mi_df = (rows - 1) * (columns - 1)

    delta = (
        np.asarray(plugin_mi(p))
        - mi_df / (2.0 * totals_p)
        - np.asarray(plugin_mi(q))
        + mi_df / (2.0 * totals_q)
    )
    variance_p = np.asarray(influence_variance(p))
    variance_q = np.asarray(influence_variance(q))

    component_p = variance_p / totals_p
    component_q = variance_q / totals_q
    standard_error = np.sqrt(component_p + component_q)
    statistic = np.divide(
        delta,
        standard_error,
        out=np.full_like(delta, np.nan, dtype=float),
        where=np.isfinite(standard_error) & (standard_error > 0),
    )
    normal_p = 2.0 * norm.sf(np.abs(statistic))
    if include_simple:
        welch_df = _welch_df(component_p, component_q, totals_p, totals_q)
        welch_p = 2.0 * t.sf(np.abs(statistic), df=welch_df)
    else:
        welch_df = np.full_like(delta, np.nan, dtype=float)
        welch_p = np.full_like(delta, np.nan, dtype=float)

    if include_expanded:
        expanded_df_p, variance_influence_variance_p = (
            _variance_influence_component_df(p, variance_p)
        )
        expanded_df_q, variance_influence_variance_q = (
            _variance_influence_component_df(q, variance_q)
        )
        expanded_df = _combine_df(
            component_p,
            component_q,
            expanded_df_p,
            expanded_df_q,
        )
        expanded_p = 2.0 * t.sf(np.abs(statistic), df=expanded_df)
    else:
        expanded_df_p = np.full_like(delta, np.nan, dtype=float)
        expanded_df_q = np.full_like(delta, np.nan, dtype=float)
        variance_influence_variance_p = np.full_like(
            delta, np.nan, dtype=float
        )
        variance_influence_variance_q = np.full_like(
            delta, np.nan, dtype=float
        )
        expanded_df = np.full_like(delta, np.nan, dtype=float)
        expanded_p = np.full_like(delta, np.nan, dtype=float)

    if include_unbiased_sensitivity:
        unbiased_component_p = variance_p / (totals_p - 1.0)
        unbiased_component_q = variance_q / (totals_q - 1.0)
        unbiased_standard_error = np.sqrt(
            unbiased_component_p + unbiased_component_q
        )
        unbiased_statistic = np.divide(
            delta,
            unbiased_standard_error,
            out=np.full_like(delta, np.nan, dtype=float),
            where=np.isfinite(unbiased_standard_error)
            & (unbiased_standard_error > 0),
        )
        unbiased_df = _welch_df(
            unbiased_component_p,
            unbiased_component_q,
            totals_p,
            totals_q,
        )
        unbiased_p = 2.0 * t.sf(
            np.abs(unbiased_statistic),
            df=unbiased_df,
        )
    else:
        unbiased_standard_error = np.full_like(delta, np.nan, dtype=float)
        unbiased_statistic = np.full_like(delta, np.nan, dtype=float)
        unbiased_df = np.full_like(delta, np.nan, dtype=float)
        unbiased_p = np.full_like(delta, np.nan, dtype=float)
    first_order_variance_valid = (
        variance_p + variance_q
    ) > 1e-14
    base_valid = (
        np.isfinite(delta)
        & first_order_variance_valid
        & np.isfinite(standard_error)
        & (standard_error > 0)
        & np.isfinite(normal_p)
    )
    simple_valid = (
        base_valid
        & np.isfinite(welch_df)
        & (welch_df > 0)
        & np.isfinite(welch_p)
    )
    valid = simple_valid if include_simple else base_valid
    expanded_valid = (
        base_valid
        & np.isfinite(expanded_df_p)
        & (expanded_df_p > 0)
        & np.isfinite(expanded_df_q)
        & (expanded_df_q > 0)
        & np.isfinite(expanded_df)
        & (expanded_df > 0)
        & np.isfinite(expanded_p)
    )
    normal_p = np.where(base_valid, normal_p, np.nan)
    welch_p = np.where(valid, welch_p, np.nan)
    expanded_p = np.where(expanded_valid, expanded_p, np.nan)
    unbiased_p = np.where(
        valid & np.isfinite(unbiased_p),
        unbiased_p,
        np.nan,
    )
    return {
        "delta_corrected": delta,
        "influence_variance_p": variance_p,
        "influence_variance_q": variance_q,
        "standard_error": standard_error,
        "statistic": statistic,
        "normal_p_value": normal_p,
        "welch_degrees_of_freedom": welch_df,
        "welch_p_value": welch_p,
        "expanded_component_degrees_of_freedom_p": expanded_df_p,
        "expanded_component_degrees_of_freedom_q": expanded_df_q,
        "variance_influence_variance_p": variance_influence_variance_p,
        "variance_influence_variance_q": variance_influence_variance_q,
        "expanded_welch_degrees_of_freedom": expanded_df,
        "expanded_welch_p_value": expanded_p,
        "unbiased_standard_error": unbiased_standard_error,
        "unbiased_statistic": unbiased_statistic,
        "unbiased_welch_degrees_of_freedom": unbiased_df,
        "unbiased_welch_p_value": unbiased_p,
        "base_valid": base_valid,
        "valid": valid,
        "simple_valid": simple_valid,
        "expanded_valid": expanded_valid,
    }


def welch_satterthwaite_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> WelchResult:
    """Return scalar normal and Welch inference for two count tables."""
    start = perf_counter()
    p, q = _validate_pair(table_p, table_q)
    if p.ndim != 2:
        raise ValueError("The scalar API expects exactly two-dimensional tables.")
    values = differential_mi_pvalues(p, q)
    rows, columns = p.shape
    return WelchResult(
        rows=rows,
        columns=columns,
        n_p=int(p.sum()),
        n_q=int(q.sum()),
        degrees_of_freedom_mi=(rows - 1) * (columns - 1),
        delta_corrected=float(values["delta_corrected"]),
        influence_variance_p=float(values["influence_variance_p"]),
        influence_variance_q=float(values["influence_variance_q"]),
        standard_error=float(values["standard_error"]),
        statistic=float(values["statistic"]),
        normal_p_value=float(values["normal_p_value"]),
        welch_degrees_of_freedom=float(values["welch_degrees_of_freedom"]),
        welch_p_value=float(values["welch_p_value"]),
        expanded_welch_degrees_of_freedom=float(
            values["expanded_welch_degrees_of_freedom"]
        ),
        expanded_welch_p_value=float(values["expanded_welch_p_value"]),
        unbiased_standard_error=float(values["unbiased_standard_error"]),
        unbiased_statistic=float(values["unbiased_statistic"]),
        unbiased_welch_degrees_of_freedom=float(
            values["unbiased_welch_degrees_of_freedom"]
        ),
        unbiased_welch_p_value=float(values["unbiased_welch_p_value"]),
        valid=bool(values["valid"]),
        expanded_valid=bool(values["expanded_valid"]),
        elapsed_seconds=perf_counter() - start,
    )
