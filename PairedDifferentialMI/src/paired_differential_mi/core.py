"""Deterministic paired differential-MI statistics and bootstrap reference."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.special import xlogy
from scipy.stats import norm, t


P_VALUE_COLUMNS = (
    "paired_wald_normal_p",
    "paired_wald_t_p",
    "paired_jackknife_t_p",
    "unpaired_wald_normal_p",
)


def _as_batch(
    paired_counts: np.ndarray,
    shape_a: tuple[int, int],
    shape_b: tuple[int, int],
) -> tuple[np.ndarray, bool]:
    counts = np.asarray(paired_counts)
    single = counts.ndim == 2
    if single:
        counts = counts[None, ...]
    expected = (shape_a[0] * shape_a[1], shape_b[0] * shape_b[1])
    if counts.ndim != 3 or counts.shape[-2:] != expected:
        raise ValueError(f"paired_counts must end in shape {expected}.")
    if (
        not np.issubdtype(counts.dtype, np.integer)
        or np.any(counts < 0)
        or np.any(counts.sum(axis=(1, 2)) <= 1)
    ):
        raise ValueError("Every paired table needs at least two integer counts.")
    totals = counts.sum(axis=(1, 2))
    if np.any(totals != totals[0]):
        raise ValueError("All tables in a batch must have the same sample size.")
    return counts.astype(np.int64, copy=False), single


def _plugin_mi_flat(counts: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    table = np.asarray(counts, dtype=float).reshape(counts.shape[0], *shape)
    totals = table.sum(axis=(1, 2))
    row = table.sum(axis=2)
    column = table.sum(axis=1)
    numerator = (
        np.sum(xlogy(table, table), axis=(1, 2))
        - np.sum(xlogy(row, row), axis=1)
        - np.sum(xlogy(column, column), axis=1)
        + xlogy(totals, totals)
    )
    return numerator / totals


def _local_information_flat(
    counts: np.ndarray, shape: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray]:
    table = np.asarray(counts, dtype=float).reshape(counts.shape[0], *shape)
    totals = table.sum(axis=(1, 2))
    row = table.sum(axis=2)
    column = table.sum(axis=1)
    local = np.zeros_like(table)
    denominator = row[:, :, None] * column[:, None, :]
    ratio = np.divide(
        table * totals[:, None, None],
        denominator,
        out=np.ones_like(table),
        where=(table > 0) & (denominator > 0),
    )
    np.log(ratio, out=local, where=table > 0)
    mi = np.sum(table * local, axis=(1, 2)) / totals
    return local.reshape(table.shape[0], -1), mi


def _f(value: np.ndarray) -> np.ndarray:
    return xlogy(value, value)


def _jackknife_pseudovalues_flat(
    counts: np.ndarray, shape: tuple[int, int]
) -> np.ndarray:
    """Return the MI delete-one pseudo-value associated with each cell."""
    table = np.asarray(counts, dtype=float).reshape(counts.shape[0], *shape)
    totals = table.sum(axis=(1, 2))
    row = table.sum(axis=2)
    column = table.sum(axis=1)
    reduced_joint = np.maximum(table - 1.0, 0.0)
    reduced_row = np.maximum(row - 1.0, 0.0)
    reduced_column = np.maximum(column - 1.0, 0.0)
    common = _f(totals) - _f(totals - 1.0)
    pseudo = (
        _f(table)
        - _f(reduced_joint)
        + _f(reduced_row)[:, :, None]
        - _f(row)[:, :, None]
        + _f(reduced_column)[:, None, :]
        - _f(column)[:, None, :]
        + common[:, None, None]
    )
    pseudo[table <= 0] = 0.0
    return pseudo.reshape(table.shape[0], -1)


def _safe_statistic(
    estimate: np.ndarray, standard_error: np.ndarray
) -> np.ndarray:
    return np.divide(
        estimate,
        standard_error,
        out=np.full_like(estimate, np.nan, dtype=float),
        where=np.isfinite(standard_error) & (standard_error > 0),
    )


def paired_mi_tests(
    paired_counts: np.ndarray,
    shape_a: tuple[int, int],
    shape_b: tuple[int, int] | None = None,
) -> dict[str, np.ndarray | float]:
    """Calculate paired Wald, jackknife-t, and unpaired diagnostic tests.

    The input axes represent condition-A joint cells and condition-B joint
    cells. Keeping this full paired table is necessary to estimate covariance.
    """
    if shape_b is None:
        shape_b = shape_a
    counts, single = _as_batch(paired_counts, shape_a, shape_b)
    start = perf_counter()
    batch_size = counts.shape[0]
    n = int(counts[0].sum())
    flat_a = counts.sum(axis=2)
    flat_b = counts.sum(axis=1)

    local_a, mi_a = _local_information_flat(flat_a, shape_a)
    local_b, mi_b = _local_information_flat(flat_b, shape_b)
    degrees_a = (shape_a[0] - 1) * (shape_a[1] - 1)
    degrees_b = (shape_b[0] - 1) * (shape_b[1] - 1)
    correction_a = degrees_a / (2.0 * n)
    correction_b = degrees_b / (2.0 * n)
    delta_plugin = mi_a - mi_b
    delta_corrected = delta_plugin - correction_a + correction_b

    probabilities = counts / n
    marginal_a = flat_a / n
    marginal_b = flat_b / n
    score_a = local_a - mi_a[:, None]
    score_b = local_b - mi_b[:, None]
    bessel = n / (n - 1.0)
    variance_a = bessel * np.sum(marginal_a * score_a * score_a, axis=1)
    variance_b = bessel * np.sum(marginal_b * score_b * score_b, axis=1)
    covariance = bessel * np.einsum(
        "bij,bi,bj->b", probabilities, score_a, score_b, optimize=True
    )
    paired_variance = np.maximum(
        variance_a + variance_b - 2.0 * covariance, 0.0
    )
    paired_se = np.sqrt(paired_variance / n)
    unpaired_se = np.sqrt(np.maximum(variance_a + variance_b, 0.0) / n)
    paired_statistic = _safe_statistic(delta_corrected, paired_se)
    unpaired_statistic = _safe_statistic(delta_corrected, unpaired_se)

    pseudo_a = _jackknife_pseudovalues_flat(flat_a, shape_a)
    pseudo_b = _jackknife_pseudovalues_flat(flat_b, shape_b)
    pseudo_difference = pseudo_a[:, :, None] - pseudo_b[:, None, :]
    jackknife_delta = np.sum(probabilities * pseudo_difference, axis=(1, 2))
    jackknife_variance = bessel * np.sum(
        probabilities
        * (pseudo_difference - jackknife_delta[:, None, None]) ** 2,
        axis=(1, 2),
    )
    jackknife_se = np.sqrt(np.maximum(jackknife_variance, 0.0) / n)
    jackknife_statistic = _safe_statistic(jackknife_delta, jackknife_se)

    result: dict[str, np.ndarray | float] = {
        "mi_a_plugin": mi_a,
        "mi_b_plugin": mi_b,
        "delta_plugin": delta_plugin,
        "delta_corrected": delta_corrected,
        "paired_if_variance": paired_variance,
        "variance_a": variance_a,
        "variance_b": variance_b,
        "covariance": covariance,
        "paired_standard_error": paired_se,
        "unpaired_standard_error": unpaired_se,
        "paired_wald_statistic": paired_statistic,
        "paired_wald_normal_p": 2.0 * norm.sf(np.abs(paired_statistic)),
        "paired_wald_t_p": 2.0 * t.sf(np.abs(paired_statistic), df=n - 1),
        "jackknife_delta": jackknife_delta,
        "jackknife_standard_error": jackknife_se,
        "jackknife_statistic": jackknife_statistic,
        "paired_jackknife_t_p": 2.0
        * t.sf(np.abs(jackknife_statistic), df=n - 1),
        "unpaired_wald_normal_p": 2.0 * norm.sf(np.abs(unpaired_statistic)),
        "valid_paired_wald": np.isfinite(paired_statistic) & (paired_se > 0),
        "valid_jackknife": np.isfinite(jackknife_statistic) & (jackknife_se > 0),
        "elapsed_seconds": np.full(
            batch_size, (perf_counter() - start) / batch_size
        ),
    }
    if single:
        return {
            key: (
                bool(value[0])
                if np.asarray(value).dtype == bool
                else float(value[0])
            )
            for key, value in result.items()
        }
    return result


@dataclass(frozen=True)
class BootstrapResult:
    p_value: float
    observed_statistic: float
    valid_replicates: int
    requested_replicates: int
    elapsed_seconds: float


def paired_bootstrap_t(
    paired_counts: np.ndarray,
    shape_a: tuple[int, int],
    shape_b: tuple[int, int] | None = None,
    *,
    replicates: int = 999,
    rng: np.random.Generator,
) -> BootstrapResult:
    """Studentized nonparametric bootstrap of complete paired units."""
    if replicates <= 0:
        raise ValueError("replicates must be positive.")
    if shape_b is None:
        shape_b = shape_a
    counts, single = _as_batch(paired_counts, shape_a, shape_b)
    if not single:
        raise ValueError("Bootstrap accepts one paired table at a time.")
    counts = counts[0]
    n = int(counts.sum())
    start = perf_counter()
    observed = paired_mi_tests(counts, shape_a, shape_b)
    observed_delta = float(observed["jackknife_delta"])
    observed_statistic = float(observed["jackknife_statistic"])
    bootstrap = rng.multinomial(
        n, counts.reshape(-1) / n, size=replicates
    ).reshape(replicates, *counts.shape)
    reference = paired_mi_tests(bootstrap, shape_a, shape_b)
    reference_statistic = np.divide(
        np.asarray(reference["jackknife_delta"]) - observed_delta,
        np.asarray(reference["jackknife_standard_error"]),
        out=np.full(replicates, np.nan),
        where=np.asarray(reference["jackknife_standard_error"]) > 0,
    )
    valid = reference_statistic[np.isfinite(reference_statistic)]
    p_value = (
        float(
            (1 + np.count_nonzero(np.abs(valid) >= abs(observed_statistic)))
            / (valid.size + 1)
        )
        if np.isfinite(observed_statistic) and valid.size
        else float("nan")
    )
    return BootstrapResult(
        p_value=p_value,
        observed_statistic=observed_statistic,
        valid_replicates=int(valid.size),
        requested_replicates=replicates,
        elapsed_seconds=perf_counter() - start,
    )
