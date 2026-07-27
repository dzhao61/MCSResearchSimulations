"""MI-specific influence-matched degrees of freedom for differential MI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.stats import norm, t

from differential_mi.statistics import plugin_mi


@dataclass(frozen=True)
class InfluenceDfResult:
    """Scalar differential-MI result with three analytic references."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    degrees_of_freedom_mi: int
    delta_corrected: float
    influence_variance_p: float
    influence_variance_q: float
    variance_if_variance_p: float
    variance_if_variance_q: float
    variance_component_p: float
    variance_component_q: float
    component_df_p: float
    component_df_q: float
    standard_error: float
    statistic: float
    normal_p_value: float
    naive_welch_df: float
    naive_welch_p_value: float
    influence_welch_df: float
    influence_welch_p_value: float
    valid: bool
    elapsed_seconds: float

    def to_dict(self) -> dict:
        return asdict(self)


def _validate_pair(
    table_p: np.ndarray,
    table_q: np.ndarray,
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


def variance_functional_influence(
    probabilities: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """Return V(P), its influence function, and Var(IF_V).

    The final two axes represent the joint alphabet. Leading axes, if present,
    are treated as independent batches. Inputs are normalized so this helper
    can be used with either probabilities or count tables.
    """
    values = np.asarray(probabilities, dtype=float)
    if values.ndim < 2 or np.any(~np.isfinite(values)) or np.any(values < 0):
        raise ValueError("Probabilities must be finite and nonnegative.")
    totals = values.sum(axis=(-2, -1), keepdims=True)
    if np.any(totals <= 0):
        raise ValueError("Every distribution must have positive total mass.")

    probability = values / totals
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
    second_moment = np.sum(probability * score**2, axis=(-2, -1))
    variance = np.maximum(second_moment - mean**2, 0.0)

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
    expanded_second = second_moment[..., None, None]
    influence = (
        score**2
        - expanded_second
        + 2.0
        * (
            score
            - row_score_mean[..., :, None]
            - column_score_mean[..., None, :]
            + expanded_mean
        )
        - 2.0 * expanded_mean * (score - expanded_mean)
    )
    influence_mean = np.sum(probability * influence, axis=(-2, -1))
    influence_variance = np.sum(
        probability * (influence - influence_mean[..., None, None]) ** 2,
        axis=(-2, -1),
    )
    influence_variance = np.maximum(influence_variance, 0.0)

    scalar = mean.ndim == 0
    return {
        "mutual_information": float(mean) if scalar else mean,
        "variance": float(variance) if scalar else variance,
        "second_moment": float(second_moment) if scalar else second_moment,
        "influence": influence,
        "influence_mean": float(influence_mean) if scalar else influence_mean,
        "influence_variance": (
            float(influence_variance) if scalar else influence_variance
        ),
    }


def _naive_welch_df(
    component_p: np.ndarray,
    component_q: np.ndarray,
    n_p: np.ndarray,
    n_q: np.ndarray,
) -> np.ndarray:
    numerator = (component_p + component_q) ** 2
    denominator = (
        component_p**2 / (n_p - 1.0)
        + component_q**2 / (n_q - 1.0)
    )
    return np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan, dtype=float),
        where=np.isfinite(denominator) & (denominator > 0),
    )


def _component_df(
    variance: np.ndarray,
    variance_if_variance: np.ndarray,
    sample_size: np.ndarray,
) -> np.ndarray:
    numerator = 2.0 * sample_size * variance**2
    return np.divide(
        numerator,
        variance_if_variance,
        out=np.full_like(numerator, np.nan, dtype=float),
        where=np.isfinite(variance_if_variance) & (variance_if_variance > 0),
    )


def differential_mi_pvalues(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> dict[str, np.ndarray]:
    """Calculate normal, naive-Welch, and MI-specific finite-df p-values."""
    p, q = _validate_pair(table_p, table_q)
    n_p = p.sum(axis=(-2, -1))
    n_q = q.sum(axis=(-2, -1))
    rows, columns = p.shape[-2:]
    mi_df = (rows - 1) * (columns - 1)

    delta = (
        np.asarray(plugin_mi(p))
        - mi_df / (2.0 * n_p)
        - np.asarray(plugin_mi(q))
        + mi_df / (2.0 * n_q)
    )
    diagnostics_p = variance_functional_influence(p)
    diagnostics_q = variance_functional_influence(q)
    variance_p = np.asarray(diagnostics_p["variance"])
    variance_q = np.asarray(diagnostics_q["variance"])
    variance_if_variance_p = np.asarray(diagnostics_p["influence_variance"])
    variance_if_variance_q = np.asarray(diagnostics_q["influence_variance"])

    component_p = variance_p / n_p
    component_q = variance_q / n_q
    standard_error = np.sqrt(component_p + component_q)
    statistic = np.divide(
        delta,
        standard_error,
        out=np.full_like(delta, np.nan, dtype=float),
        where=np.isfinite(standard_error) & (standard_error > 0),
    )

    normal_p = 2.0 * norm.sf(np.abs(statistic))
    naive_df = _naive_welch_df(component_p, component_q, n_p, n_q)
    naive_p = 2.0 * t.sf(np.abs(statistic), df=naive_df)

    component_df_p = _component_df(variance_p, variance_if_variance_p, n_p)
    component_df_q = _component_df(variance_q, variance_if_variance_q, n_q)
    # This is algebraically identical to the component Satterthwaite formula,
    # but remains stable when one component is zero.
    estimated_component_variance = (
        variance_if_variance_p / n_p**3
        + variance_if_variance_q / n_q**3
    )
    influence_df = np.divide(
        2.0 * (component_p + component_q) ** 2,
        estimated_component_variance,
        out=np.full_like(delta, np.nan, dtype=float),
        where=np.isfinite(estimated_component_variance)
        & (estimated_component_variance > 0),
    )
    influence_p = 2.0 * t.sf(np.abs(statistic), df=influence_df)

    valid = (
        np.isfinite(delta)
        & np.isfinite(standard_error)
        & (standard_error > 0)
        & ((variance_p + variance_q) > 1e-14)
        & np.isfinite(naive_df)
        & (naive_df > 0)
        & np.isfinite(influence_df)
        & (influence_df > 0)
        & np.isfinite(normal_p)
        & np.isfinite(naive_p)
        & np.isfinite(influence_p)
    )
    normal_p = np.where(valid, np.clip(normal_p, 0.0, 1.0), np.nan)
    naive_p = np.where(valid, np.clip(naive_p, 0.0, 1.0), np.nan)
    influence_p = np.where(valid, np.clip(influence_p, 0.0, 1.0), np.nan)

    return {
        "delta_corrected": delta,
        "influence_variance_p": variance_p,
        "influence_variance_q": variance_q,
        "variance_if_variance_p": variance_if_variance_p,
        "variance_if_variance_q": variance_if_variance_q,
        "variance_component_p": component_p,
        "variance_component_q": component_q,
        "component_df_p": component_df_p,
        "component_df_q": component_df_q,
        "standard_error": standard_error,
        "statistic": statistic,
        "normal_p_value": normal_p,
        "naive_welch_df": naive_df,
        "naive_welch_p_value": naive_p,
        "influence_welch_df": influence_df,
        "influence_welch_p_value": influence_p,
        "valid": valid,
    }


def influence_df_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> InfluenceDfResult:
    """Return scalar MI-specific influence-df inference for two count tables."""
    start = perf_counter()
    p, q = _validate_pair(table_p, table_q)
    if p.ndim != 2:
        raise ValueError("The scalar API expects exactly two-dimensional tables.")
    values = differential_mi_pvalues(p, q)
    rows, columns = p.shape
    return InfluenceDfResult(
        rows=rows,
        columns=columns,
        n_p=int(p.sum()),
        n_q=int(q.sum()),
        degrees_of_freedom_mi=(rows - 1) * (columns - 1),
        delta_corrected=float(values["delta_corrected"]),
        influence_variance_p=float(values["influence_variance_p"]),
        influence_variance_q=float(values["influence_variance_q"]),
        variance_if_variance_p=float(values["variance_if_variance_p"]),
        variance_if_variance_q=float(values["variance_if_variance_q"]),
        variance_component_p=float(values["variance_component_p"]),
        variance_component_q=float(values["variance_component_q"]),
        component_df_p=float(values["component_df_p"]),
        component_df_q=float(values["component_df_q"]),
        standard_error=float(values["standard_error"]),
        statistic=float(values["statistic"]),
        normal_p_value=float(values["normal_p_value"]),
        naive_welch_df=float(values["naive_welch_df"]),
        naive_welch_p_value=float(values["naive_welch_p_value"]),
        influence_welch_df=float(values["influence_welch_df"]),
        influence_welch_p_value=float(values["influence_welch_p_value"]),
        valid=bool(values["valid"]),
        elapsed_seconds=perf_counter() - start,
    )
