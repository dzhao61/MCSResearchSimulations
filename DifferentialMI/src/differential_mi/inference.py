"""Two-sample MI tests using influence-function studentization."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.stats import norm

from .statistics import (
    analytic_bias_corrected_mi,
    influence_variance,
    jackknife_mi,
    plugin_mi,
)


@dataclass(frozen=True)
class ComparisonResult:
    n_p: int
    n_q: int
    mi_p_plugin: float
    mi_q_plugin: float
    mi_p_analytic: float
    mi_q_analytic: float
    mi_p_jackknife: float
    mi_q_jackknife: float
    delta_plugin: float
    delta_analytic: float
    delta_jackknife: float
    pooled_mi_plugin: float
    pooled_influence_variance: float
    standard_error: float
    z_plugin: float
    z_analytic: float
    z_jackknife: float
    wald_plugin_p: float
    wald_analytic_p: float
    wald_jackknife_p: float
    naive_perm_plugin_p: float
    student_perm_plugin_p: float
    student_perm_analytic_p: float
    student_perm_jackknife_p: float
    valid_studentization: bool
    permutations: int
    deterministic_seconds: float
    permutation_seconds: float

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def _safe_z(delta: np.ndarray, standard_error: np.ndarray) -> np.ndarray:
    delta_values = np.asarray(delta, dtype=float)
    se_values = np.asarray(standard_error, dtype=float)
    return np.divide(
        delta_values,
        se_values,
        out=np.full_like(delta_values, np.nan),
        where=np.isfinite(se_values) & (se_values > 0),
    )


def _monte_carlo_p(reference: np.ndarray, observed: float) -> float:
    valid = np.asarray(reference, dtype=float)
    valid = valid[np.isfinite(valid)]
    if valid.size == 0 or not np.isfinite(observed):
        return float("nan")
    return float((1 + np.count_nonzero(np.abs(valid) >= abs(observed))) / (valid.size + 1))


def compare_tables(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    permutations: int,
    rng: np.random.Generator,
) -> ComparisonResult:
    """Compare MI from two count tables and return all pilot methods."""
    p = np.asarray(table_p, dtype=np.int64)
    q = np.asarray(table_q, dtype=np.int64)
    if p.shape != q.shape or p.ndim != 2:
        raise ValueError("The two tables must have the same two-dimensional shape.")
    if np.any(p < 0) or np.any(q < 0):
        raise ValueError("Counts cannot be negative.")
    n_p = int(p.sum())
    n_q = int(q.sum())
    if min(n_p, n_q) <= 1:
        raise ValueError("Each group needs at least two observations.")

    deterministic_start = perf_counter()
    mi_p_plugin = float(plugin_mi(p))
    mi_q_plugin = float(plugin_mi(q))
    mi_p_analytic = float(analytic_bias_corrected_mi(p))
    mi_q_analytic = float(analytic_bias_corrected_mi(q))
    mi_p_jackknife = float(jackknife_mi(p))
    mi_q_jackknife = float(jackknife_mi(q))
    delta_plugin = mi_p_plugin - mi_q_plugin
    delta_analytic = mi_p_analytic - mi_q_analytic
    delta_jackknife = mi_p_jackknife - mi_q_jackknife
    pooled_mi_plugin = float(plugin_mi(p + q))
    pooled_influence_variance = float(influence_variance(p + q))
    var_p = float(influence_variance(p))
    var_q = float(influence_variance(q))
    standard_error = float(np.sqrt(var_p / n_p + var_q / n_q))
    z_plugin = float(_safe_z(np.asarray(delta_plugin), np.asarray(standard_error)))
    z_analytic = float(
        _safe_z(np.asarray(delta_analytic), np.asarray(standard_error))
    )
    z_jackknife = float(
        _safe_z(np.asarray(delta_jackknife), np.asarray(standard_error))
    )
    wald_plugin_p = (
        float(2.0 * norm.sf(abs(z_plugin))) if np.isfinite(z_plugin) else float("nan")
    )
    wald_analytic_p = (
        float(2.0 * norm.sf(abs(z_analytic)))
        if np.isfinite(z_analytic)
        else float("nan")
    )
    wald_jackknife_p = (
        float(2.0 * norm.sf(abs(z_jackknife)))
        if np.isfinite(z_jackknife)
        else float("nan")
    )
    deterministic_seconds = perf_counter() - deterministic_start

    permutation_start = perf_counter()
    pooled_flat = (p + q).reshape(-1)
    perm_p_flat = rng.multivariate_hypergeometric(
        pooled_flat, n_p, size=permutations
    )
    perm_p = perm_p_flat.reshape(permutations, *p.shape)
    perm_q = (pooled_flat[None, :] - perm_p_flat).reshape(permutations, *q.shape)

    perm_plugin_delta = plugin_mi(perm_p) - plugin_mi(perm_q)
    naive_perm_plugin_p = _monte_carlo_p(perm_plugin_delta, delta_plugin)

    perm_analytic_delta = analytic_bias_corrected_mi(
        perm_p
    ) - analytic_bias_corrected_mi(perm_q)
    perm_jackknife_delta = jackknife_mi(perm_p) - jackknife_mi(perm_q)
    perm_var_p = influence_variance(perm_p)
    perm_var_q = influence_variance(perm_q)
    perm_se = np.sqrt(perm_var_p / n_p + perm_var_q / n_q)
    perm_z_plugin = _safe_z(perm_plugin_delta, perm_se)
    perm_z_analytic = _safe_z(perm_analytic_delta, perm_se)
    perm_z_jackknife = _safe_z(perm_jackknife_delta, perm_se)
    student_perm_plugin_p = _monte_carlo_p(perm_z_plugin, z_plugin)
    student_perm_analytic_p = _monte_carlo_p(perm_z_analytic, z_analytic)
    student_perm_jackknife_p = _monte_carlo_p(perm_z_jackknife, z_jackknife)
    permutation_seconds = perf_counter() - permutation_start

    return ComparisonResult(
        n_p=n_p,
        n_q=n_q,
        mi_p_plugin=mi_p_plugin,
        mi_q_plugin=mi_q_plugin,
        mi_p_analytic=mi_p_analytic,
        mi_q_analytic=mi_q_analytic,
        mi_p_jackknife=mi_p_jackknife,
        mi_q_jackknife=mi_q_jackknife,
        delta_plugin=delta_plugin,
        delta_analytic=delta_analytic,
        delta_jackknife=delta_jackknife,
        pooled_mi_plugin=pooled_mi_plugin,
        pooled_influence_variance=pooled_influence_variance,
        standard_error=standard_error,
        z_plugin=z_plugin,
        z_analytic=z_analytic,
        z_jackknife=z_jackknife,
        wald_plugin_p=wald_plugin_p,
        wald_analytic_p=wald_analytic_p,
        wald_jackknife_p=wald_jackknife_p,
        naive_perm_plugin_p=naive_perm_plugin_p,
        student_perm_plugin_p=student_perm_plugin_p,
        student_perm_analytic_p=student_perm_analytic_p,
        student_perm_jackknife_p=student_perm_jackknife_p,
        valid_studentization=bool(
            np.isfinite(z_plugin)
            and np.isfinite(z_jackknife)
            and standard_error > 0
        ),
        permutations=permutations,
        deterministic_seconds=deterministic_seconds,
        permutation_seconds=permutation_seconds,
    )
