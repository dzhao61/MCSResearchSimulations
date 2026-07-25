"""Vectorized estimators and influence-function calculations."""

from __future__ import annotations

import numpy as np
from scipy.special import xlogy


def _as_table_batch(tables: np.ndarray) -> np.ndarray:
    values = np.asarray(tables, dtype=float)
    if values.ndim < 2 or np.any(values < 0):
        raise ValueError("Tables must be nonnegative with at least two dimensions.")
    totals = values.sum(axis=(-2, -1))
    if np.any(totals <= 0):
        raise ValueError("Every table must contain at least one observation.")
    return values


def plugin_mi(tables: np.ndarray) -> np.ndarray | float:
    """Calculate plug-in MI in nats for one table or a batch of tables."""
    counts = _as_table_batch(tables)
    totals = counts.sum(axis=(-2, -1), keepdims=True)
    p = counts / totals
    row = p.sum(axis=-1)
    col = p.sum(axis=-2)
    result = (
        np.sum(xlogy(p, p), axis=(-2, -1))
        - np.sum(xlogy(row, row), axis=-1)
        - np.sum(xlogy(col, col), axis=-1)
    )
    return float(result) if result.ndim == 0 else result


def analytic_bias_corrected_mi(tables: np.ndarray) -> np.ndarray | float:
    """Subtract the leading full-support multinomial bias from plug-in MI."""
    counts = _as_table_batch(tables)
    totals = counts.sum(axis=(-2, -1))
    degrees_of_freedom = (counts.shape[-2] - 1) * (counts.shape[-1] - 1)
    result = np.asarray(plugin_mi(counts)) - degrees_of_freedom / (2.0 * totals)
    return float(result) if result.ndim == 0 else result


def _jackknife_entropy(counts: np.ndarray) -> np.ndarray:
    """Delete-one jackknife entropy for vectors on the final axis."""
    values = np.asarray(counts, dtype=float)
    totals = values.sum(axis=-1)
    if np.any(totals <= 1):
        raise ValueError("Jackknife entropy requires at least two observations.")

    f_counts = xlogy(values, values)
    sum_f = f_counts.sum(axis=-1)
    plugin = np.log(totals) - sum_f / totals

    reduced = np.maximum(values - 1.0, 0.0)
    change = xlogy(reduced, reduced) - f_counts
    weighted_change = np.sum(values * change, axis=-1) / totals
    mean_leave_one_out = (
        np.log(totals - 1.0) - (sum_f + weighted_change) / (totals - 1.0)
    )
    return totals * plugin - (totals - 1.0) * mean_leave_one_out


def jackknife_mi(tables: np.ndarray) -> np.ndarray | float:
    """Delete-one jackknife bias-corrected MI without clipping at zero."""
    counts = _as_table_batch(tables)
    leading_shape = counts.shape[:-2]
    joint = counts.reshape(*leading_shape, -1)
    row = counts.sum(axis=-1)
    col = counts.sum(axis=-2)
    result = (
        _jackknife_entropy(row)
        + _jackknife_entropy(col)
        - _jackknife_entropy(joint)
    )
    return float(result) if result.ndim == 0 else result


def influence_variance(tables: np.ndarray) -> np.ndarray | float:
    """Estimate Var[log(p_ij/(p_i p_j))] under each empirical table."""
    counts = _as_table_batch(tables)
    totals = counts.sum(axis=(-2, -1), keepdims=True)
    p = counts / totals
    row = p.sum(axis=-1, keepdims=True)
    col = p.sum(axis=-2, keepdims=True)

    log_p = np.zeros_like(p)
    log_row = np.zeros_like(row)
    log_col = np.zeros_like(col)
    np.log(p, out=log_p, where=p > 0)
    np.log(row, out=log_row, where=row > 0)
    np.log(col, out=log_col, where=col > 0)

    score = log_p - log_row - log_col
    mean = np.sum(p * score, axis=(-2, -1))
    second_moment = np.sum(p * score * score, axis=(-2, -1))
    result = np.maximum(second_moment - mean * mean, 0.0)
    return float(result) if result.ndim == 0 else result
