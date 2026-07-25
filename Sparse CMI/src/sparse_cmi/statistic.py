from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from .models import Stratum


def g2_for_a(n: int, r: int, s: int, a: int | np.ndarray) -> float | np.ndarray:
    """Likelihood-ratio G^2 for attainable top-left cell count(s)."""

    a_array = np.asarray(a, dtype=np.float64)
    if n == 0:
        result = np.zeros_like(a_array)
        return float(result) if result.ndim == 0 else result

    observed = np.stack(
        (
            a_array,
            r - a_array,
            s - a_array,
            n - r - s + a_array,
        ),
        axis=-1,
    )
    expected = np.asarray(
        (
            r * s / n,
            r * (n - s) / n,
            (n - r) * s / n,
            (n - r) * (n - s) / n,
        ),
        dtype=np.float64,
    )

    positive = observed > 0
    if np.any(positive & (expected <= 0)):
        raise ValueError("positive observed count has zero expected count")
    terms = np.zeros_like(observed)
    np.divide(observed, expected, out=terms, where=positive)
    np.log(terms, out=terms, where=positive)
    terms = np.where(positive, observed * terms, 0.0)
    result = 2.0 * terms.sum(axis=-1)
    if result.ndim == 0:
        return float(result)
    return result


def observed_g2(strata: Iterable[Stratum]) -> float:
    return float(
        sum(g2_for_a(item.n, item.r, item.s, item.a_observed) for item in strata)
    )


def observed_cmi_nats(strata: Iterable[Stratum]) -> float:
    strata_list = list(strata)
    total_n = sum(item.n for item in strata_list)
    if total_n == 0:
        return 0.0
    return observed_g2(strata_list) / (2.0 * total_n)

