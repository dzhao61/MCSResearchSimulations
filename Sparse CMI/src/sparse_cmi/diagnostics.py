from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from .models import Stratum
from .moments import AggregateMoments


@dataclass(frozen=True)
class TableDiagnostics:
    min_expected_count: float
    fraction_expected_below_1: float
    fraction_expected_below_5: float
    degenerate_fraction: float


def table_diagnostics(
    strata: Iterable[Stratum],
    moments: AggregateMoments,
) -> TableDiagnostics:
    strata_list = list(strata)
    expected: list[float] = []
    for item in strata_list:
        if item.n == 0:
            continue
        expected.extend(
            (
                item.r * item.s / item.n,
                item.r * (item.n - item.s) / item.n,
                (item.n - item.r) * item.s / item.n,
                (item.n - item.r) * (item.n - item.s) / item.n,
            )
        )
    expected_array = np.asarray(expected, dtype=np.float64)
    if expected_array.size:
        minimum = float(expected_array.min())
        below_1 = float(np.mean(expected_array < 1.0))
        below_5 = float(np.mean(expected_array < 5.0))
    else:
        minimum = 0.0
        below_1 = 1.0
        below_5 = 1.0
    total = max(1, moments.total_strata)
    return TableDiagnostics(
        min_expected_count=minimum,
        fraction_expected_below_1=below_1,
        fraction_expected_below_5=below_5,
        degenerate_fraction=1.0 - moments.informative_strata / total,
    )

