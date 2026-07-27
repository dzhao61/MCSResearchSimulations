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
    unbiased_standard_error: float
    unbiased_statistic: float
    unbiased_welch_degrees_of_freedom: float
    unbiased_welch_p_value: float
    valid: bool
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


def differential_mi_pvalues(
    table_p: np.ndarray,
    table_q: np.ndarray,
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
    welch_df = _welch_df(component_p, component_q, totals_p, totals_q)
    welch_p = 2.0 * t.sf(np.abs(statistic), df=welch_df)

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
    first_order_variance_valid = (
        variance_p + variance_q
    ) > 1e-14
    valid = (
        np.isfinite(delta)
        & first_order_variance_valid
        & np.isfinite(standard_error)
        & (standard_error > 0)
        & np.isfinite(welch_df)
        & (welch_df > 0)
        & np.isfinite(normal_p)
        & np.isfinite(welch_p)
        & np.isfinite(unbiased_p)
    )
    normal_p = np.where(valid, normal_p, np.nan)
    welch_p = np.where(valid, welch_p, np.nan)
    unbiased_p = np.where(valid, unbiased_p, np.nan)
    return {
        "delta_corrected": delta,
        "influence_variance_p": variance_p,
        "influence_variance_q": variance_q,
        "standard_error": standard_error,
        "statistic": statistic,
        "normal_p_value": normal_p,
        "welch_degrees_of_freedom": welch_df,
        "welch_p_value": welch_p,
        "unbiased_standard_error": unbiased_standard_error,
        "unbiased_statistic": unbiased_statistic,
        "unbiased_welch_degrees_of_freedom": unbiased_df,
        "unbiased_welch_p_value": unbiased_p,
        "valid": valid,
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
        unbiased_standard_error=float(values["unbiased_standard_error"]),
        unbiased_statistic=float(values["unbiased_statistic"]),
        unbiased_welch_degrees_of_freedom=float(
            values["unbiased_welch_degrees_of_freedom"]
        ),
        unbiased_welch_p_value=float(values["unbiased_welch_p_value"]),
        valid=bool(values["valid"]),
        elapsed_seconds=perf_counter() - start,
    )
