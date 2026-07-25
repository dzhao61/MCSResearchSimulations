from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.stats import hypergeom

from .models import Stratum
from .statistic import g2_for_a


@dataclass(frozen=True)
class StratumNull:
    support: np.ndarray
    probabilities: np.ndarray
    g_values: np.ndarray


@lru_cache(maxsize=4096)
def _stratum_null_cached(n: int, r: int, s: int) -> StratumNull:
    support = np.arange(
        max(0, r + s - n),
        min(r, s) + 1,
        dtype=np.int64,
    )
    if n == 0:
        probabilities = np.ones(1, dtype=np.float64)
    else:
        probabilities = hypergeom.pmf(
            support,
            M=n,
            n=s,
            N=r,
        ).astype(np.float64)
        probability_sum = float(probabilities.sum())
        if not np.isfinite(probability_sum) or probability_sum <= 0:
            raise FloatingPointError("hypergeometric probabilities are invalid")
        probabilities /= probability_sum

    g_values = np.asarray(
        g2_for_a(n, r, s, support),
        dtype=np.float64,
    )
    support.setflags(write=False)
    probabilities.setflags(write=False)
    g_values.setflags(write=False)
    return StratumNull(support, probabilities, g_values)


def stratum_null(stratum: Stratum) -> StratumNull:
    """Return the cached exact conditional null for fixed stratum margins."""

    return _stratum_null_cached(stratum.n, stratum.r, stratum.s)
