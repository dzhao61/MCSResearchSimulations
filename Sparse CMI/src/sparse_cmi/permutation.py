from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from .hypergeom import stratum_null
from .models import Stratum


def sample_conditional_g2(
    strata: Iterable[Stratum],
    samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample the fixed-margin null directly in table space."""

    if samples <= 0:
        raise ValueError("samples must be positive")
    result = np.zeros(samples, dtype=np.float64)
    for stratum in strata:
        null = stratum_null(stratum)
        if stratum.support_width == 1:
            result += null.g_values[0]
            continue
        draws = rng.hypergeometric(
            ngood=stratum.s,
            nbad=stratum.n - stratum.s,
            nsample=stratum.r,
            size=samples,
        )
        result += null.g_values[draws - stratum.support_min]
    return result


def label_permutation_g2(
    strata: Iterable[Stratum],
    permutations: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Literal within-stratum permutation of Y labels against fixed X labels."""

    if permutations <= 0:
        raise ValueError("permutations must be positive")
    strata_list = list(strata)
    lookup = [stratum_null(item) for item in strata_list]
    y_labels = [
        np.concatenate(
            (
                np.ones(item.s, dtype=np.int8),
                np.zeros(item.n - item.s, dtype=np.int8),
            )
        )
        for item in strata_list
    ]

    result = np.zeros(permutations, dtype=np.float64)
    for index in range(permutations):
        total = 0.0
        for stratum, null, labels in zip(
            strata_list, lookup, y_labels, strict=True
        ):
            if stratum.support_width == 1:
                total += float(null.g_values[0])
                continue
            a_value = int(rng.permutation(labels)[: stratum.r].sum())
            total += float(null.g_values[a_value - stratum.support_min])
        result[index] = total
    return result


def monte_carlo_pvalue(
    observed: float,
    null_statistics: np.ndarray,
) -> float:
    exceedances = int(np.count_nonzero(null_statistics >= observed - 1e-10))
    return (exceedances + 1.0) / (null_statistics.size + 1.0)

