"""Vectorized estimators and influence-function calculations."""

from __future__ import annotations

import numpy as np
from scipy.special import xlogy


def _as_table_batch(tables: np.ndarray) -> np.ndarray:
    if np.iscomplexobj(tables):
        raise ValueError("Tables must be finite and nonnegative.")
    values = np.asarray(tables, dtype=float)
    if values.ndim < 2 or np.any(~np.isfinite(values)) or np.any(values < 0):
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


def _constant_score_tables(counts: np.ndarray, score: np.ndarray) -> np.ndarray:
    """Identify exactly constant occupied-cell scores, without a variance floor."""
    flat = counts.reshape(-1, counts.shape[-2], counts.shape[-1])
    occupied = flat > 0
    flat_score = score.reshape(flat.shape)
    low = np.min(np.where(occupied, flat_score, np.inf), axis=(-2, -1))
    high = np.max(np.where(occupied, flat_score, -np.inf), axis=(-2, -1))
    # Only near-constant scores need an exact integer cross-product check.
    candidates = high - low <= 32 * np.finfo(float).eps * np.maximum(1, np.abs(high))
    constant = np.zeros(len(flat), dtype=bool)
    for index in np.flatnonzero(candidates):
        table = flat[index]
        if np.all(table == np.floor(table)):
            # Products contain three counts. Use Python integers above the
            # int64-safe total, rather than overflow or a floating tolerance.
            dtype = np.int64 if table.sum() <= 2**21 - 1 else object
            integers = (table.astype(dtype) if dtype is np.int64
                        else np.frompyfunc(int, 1, 1)(table))
            row = integers.sum(axis=-1)
            column = integers.sum(axis=-2)
            a, b = np.argwhere(occupied[index])[0]
            constant[index] = np.all(
                (integers * row[a] * column[b]
                 == integers[a, b] * row[:, None] * column[None, :])
                | ~occupied[index]
            )
        else:
            constant[index] = high[index] == low[index]
    return constant.reshape(counts.shape[:-2])


def _centered_mi_score(tables: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return empirical weights and stably centred pointwise MI values."""
    counts = _as_table_batch(tables)
    totals = counts.sum(axis=(-2, -1), keepdims=True)
    p = counts / totals
    row = counts.sum(axis=-1, keepdims=True)
    column = counts.sum(axis=-2, keepdims=True)
    ratio = np.divide(counts * totals, row * column,
                      out=np.ones_like(counts), where=counts > 0)
    score = np.log(ratio)
    constant = _constant_score_tables(counts, score)
    anchor = np.min(np.where(counts > 0, score, np.inf), axis=(-2, -1), keepdims=True)
    shifted = score - anchor
    centered = shifted - np.sum(p * shifted, axis=(-2, -1), keepdims=True)
    centered = np.where(constant[..., None, None], 0.0, centered)
    return p, centered


def influence_variance(tables: np.ndarray) -> np.ndarray | float:
    """Estimate Var[log(p_ij/(p_i p_j))] under each empirical table."""
    probability, centered = _centered_mi_score(tables)
    result = np.sum(probability * centered**2, axis=(-2, -1))
    return float(result) if result.ndim == 0 else result
