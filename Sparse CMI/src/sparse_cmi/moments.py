from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

import numpy as np

from .hypergeom import StratumNull, stratum_null
from .models import Stratum


@dataclass(frozen=True)
class StratumMoments:
    mean: float
    variance: float
    third_cumulant: float
    fourth_cumulant: float
    absolute_third_central: float
    support_width: int


@dataclass(frozen=True)
class AggregateMoments:
    mean: float
    variance: float
    third_cumulant: float
    fourth_cumulant: float
    skewness: float
    lyapunov_ratio: float
    max_variance_share: float
    informative_strata: int
    total_strata: int
    total_support_width: int


def moments_from_null(null: StratumNull) -> StratumMoments:
    mean = float(np.dot(null.probabilities, null.g_values))
    centered = null.g_values - mean
    variance = float(np.dot(null.probabilities, centered**2))
    third = float(np.dot(null.probabilities, centered**3))
    fourth_central = float(np.dot(null.probabilities, centered**4))
    absolute_third = float(np.dot(null.probabilities, np.abs(centered) ** 3))

    scale = max(1.0, abs(mean))
    if variance < 64 * np.finfo(float).eps * scale * scale:
        variance = 0.0
        third = 0.0
        fourth_central = 0.0
        absolute_third = 0.0

    return StratumMoments(
        mean=mean,
        variance=variance,
        third_cumulant=third,
        fourth_cumulant=fourth_central - 3.0 * variance**2,
        absolute_third_central=absolute_third,
        support_width=int(null.support.size),
    )


def stratum_moments(stratum: Stratum) -> StratumMoments:
    return moments_from_null(stratum_null(stratum))


def aggregate_moments(strata: Iterable[Stratum]) -> AggregateMoments:
    strata_list = list(strata)
    individual = [stratum_moments(item) for item in strata_list]
    mean = float(sum(item.mean for item in individual))
    variance = float(sum(item.variance for item in individual))
    third = float(sum(item.third_cumulant for item in individual))
    fourth = float(sum(item.fourth_cumulant for item in individual))
    informative = sum(item.variance > 0 for item in individual)

    if variance > 0:
        skewness = third / variance**1.5
        lyapunov = (
            sum(item.absolute_third_central for item in individual)
            / variance**1.5
        )
        max_share = max((item.variance for item in individual), default=0.0) / variance
    else:
        skewness = 0.0
        lyapunov = 0.0
        max_share = 0.0

    return AggregateMoments(
        mean=mean,
        variance=variance,
        third_cumulant=third,
        fourth_cumulant=fourth,
        skewness=float(skewness),
        lyapunov_ratio=float(lyapunov),
        max_variance_share=float(max_share),
        informative_strata=informative,
        total_strata=len(strata_list),
        total_support_width=sum(item.support_width for item in individual),
    )

