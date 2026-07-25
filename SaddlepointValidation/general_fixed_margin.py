from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from scipy import stats
from scipy.stats import random_table

try:
    from .saddlepoint_cgf import drop_empty_margins, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from saddlepoint_cgf import drop_empty_margins, g_statistic


@dataclass(frozen=True)
class GeneralApproxResult:
    observed_g: float
    gamma_p: float
    empirical_p: float
    mu: float
    variance: float
    gamma_shape: float
    gamma_scale: float
    samples: int
    elapsed_s: float
    error: str = ""


def g_statistics_batch(tables: np.ndarray) -> np.ndarray:
    counts = np.asarray(tables, dtype=np.float64)
    if counts.ndim == 2:
        counts = counts[None, :, :]
    totals = counts.sum(axis=(1, 2), keepdims=True)
    rows = counts.sum(axis=2, keepdims=True)
    cols = counts.sum(axis=1, keepdims=True)
    expected = np.zeros_like(counts, dtype=np.float64)
    np.divide(rows * cols, totals, out=expected, where=totals > 0)
    mask = counts > 0
    terms = np.zeros_like(counts, dtype=np.float64)
    terms[mask] = counts[mask] * np.log(counts[mask] / expected[mask])
    return 2.0 * terms.sum(axis=(1, 2))


def sample_fixed_margin_g(
    table: np.ndarray,
    samples: int,
    rng: np.random.Generator,
    batch_size: int = 10_000,
) -> np.ndarray:
    counts = drop_empty_margins(table)
    rows = counts.sum(axis=1).astype(np.int64)
    cols = counts.sum(axis=0).astype(np.int64)
    rv = random_table(rows, cols)
    values = np.empty(samples, dtype=np.float64)
    pos = 0
    while pos < samples:
        size = min(batch_size, samples - pos)
        sampled = rv.rvs(size=size, random_state=rng)
        values[pos : pos + size] = g_statistics_batch(sampled)
        pos += size
    return values


def fixed_margin_gamma_approx(
    table: np.ndarray,
    samples: int = 10_000,
    seed: int | None = None,
    batch_size: int = 10_000,
) -> GeneralApproxResult:
    start = time.perf_counter()
    observed_g = float("nan")
    try:
        rng = np.random.default_rng(seed)
        observed_g = g_statistic(table)
        null_g = sample_fixed_margin_g(
            table=table,
            samples=samples,
            rng=rng,
            batch_size=batch_size,
        )
        mu = float(null_g.mean())
        variance = float(null_g.var(ddof=1 if samples > 1 else 0))

        # The fixed-margin null is discrete. Sparse tables often put large mass on
        # exactly the observed G value, so include numerical ties in the upper tail
        # to match JIDT's permutation p-value convention.
        tie_tol = max(1e-12, 1e-12 * max(abs(observed_g), float(np.max(np.abs(null_g)))))
        empirical_p = float((np.count_nonzero(null_g >= observed_g - tie_tol) + 1) / (samples + 1))

        if not np.isfinite(mu) or not np.isfinite(variance) or mu < 0 or variance < 0:
            raise ValueError(f"invalid null moments: mu={mu}, variance={variance}")
        if mu == 0 or variance == 0:
            return GeneralApproxResult(
                observed_g=observed_g,
                gamma_p=empirical_p,
                empirical_p=empirical_p,
                mu=mu,
                variance=variance,
                gamma_shape=float("nan"),
                gamma_scale=float("nan"),
                samples=samples,
                elapsed_s=time.perf_counter() - start,
            )

        shape = mu * mu / variance
        scale = variance / mu
        gamma_p = float(stats.gamma(a=shape, scale=scale).sf(observed_g))
        return GeneralApproxResult(
            observed_g=observed_g,
            gamma_p=float(np.clip(gamma_p, 0.0, 1.0)),
            empirical_p=empirical_p,
            mu=mu,
            variance=variance,
            gamma_shape=float(shape),
            gamma_scale=float(scale),
            samples=samples,
            elapsed_s=time.perf_counter() - start,
        )
    except Exception as exc:
        return GeneralApproxResult(
            observed_g=observed_g,
            gamma_p=float("nan"),
            empirical_p=float("nan"),
            mu=float("nan"),
            variance=float("nan"),
            gamma_shape=float("nan"),
            gamma_scale=float("nan"),
            samples=samples,
            elapsed_s=time.perf_counter() - start,
            error=repr(exc),
        )
