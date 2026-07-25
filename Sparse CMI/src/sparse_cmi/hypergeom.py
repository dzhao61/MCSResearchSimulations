from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import hypergeom

from .models import Stratum
from .statistic import g2_for_a


@dataclass(frozen=True)
class StratumNull:
    support: np.ndarray
    probabilities: np.ndarray
    g_values: np.ndarray


def stratum_null(stratum: Stratum) -> StratumNull:
    """Return the exact conditional null for one fixed-margin stratum."""

    support = np.arange(
        stratum.support_min,
        stratum.support_max + 1,
        dtype=np.int64,
    )
    if stratum.n == 0:
        probabilities = np.ones(1, dtype=np.float64)
    else:
        probabilities = hypergeom.pmf(
            support,
            M=stratum.n,
            n=stratum.s,
            N=stratum.r,
        ).astype(np.float64)
        probability_sum = float(probabilities.sum())
        if not np.isfinite(probability_sum) or probability_sum <= 0:
            raise FloatingPointError("hypergeometric probabilities are invalid")
        probabilities /= probability_sum

    g_values = np.asarray(
        g2_for_a(stratum.n, stratum.r, stratum.s, support),
        dtype=np.float64,
    )
    return StratumNull(support, probabilities, g_values)

