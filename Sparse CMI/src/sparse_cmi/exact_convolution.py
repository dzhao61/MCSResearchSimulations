from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

import numpy as np

from .hypergeom import stratum_null
from .models import Stratum


class StateSpaceTooLarge(RuntimeError):
    pass


@dataclass(frozen=True)
class ExactDistribution:
    values: np.ndarray
    probabilities: np.ndarray

    def upper_tail(self, statistic: float, tolerance: float = 1e-10) -> float:
        return float(self.probabilities[self.values >= statistic - tolerance].sum())

    def upper_tail_array(
        self,
        statistics: np.ndarray,
        tolerance: float = 1e-10,
    ) -> np.ndarray:
        order = np.argsort(self.values)
        values = self.values[order]
        probabilities = self.probabilities[order]
        tails = np.cumsum(probabilities[::-1])[::-1]
        indices = np.searchsorted(values, np.asarray(statistics) - tolerance, side="left")
        result = np.zeros_like(np.asarray(statistics), dtype=np.float64)
        valid = indices < values.size
        result[valid] = tails[indices[valid]]
        return result


def _collapsed_stratum(
    stratum: Stratum,
    rounding_decimals: int,
) -> dict[float, float]:
    null = stratum_null(stratum)
    collapsed: dict[float, float] = {}
    for value, probability in zip(null.g_values, null.probabilities, strict=True):
        key = round(float(value), rounding_decimals)
        collapsed[key] = collapsed.get(key, 0.0) + float(probability)
    return collapsed


def exact_conditional_distribution(
    strata: Iterable[Stratum],
    *,
    max_states: int = 250_000,
    rounding_decimals: int = 12,
) -> ExactDistribution:
    """Numerically convolve the finite conditional distributions."""

    states: dict[float, float] = {0.0: 1.0}
    for stratum in strata:
        component = _collapsed_stratum(stratum, rounding_decimals)
        if len(states) * len(component) > max_states * 4:
            raise StateSpaceTooLarge(
                "intermediate convolution is certain to exceed max_states"
            )
        updated: dict[float, float] = {}
        for left_value, left_probability in states.items():
            for right_value, right_probability in component.items():
                key = round(left_value + right_value, rounding_decimals)
                updated[key] = (
                    updated.get(key, 0.0)
                    + left_probability * right_probability
                )
        if len(updated) > max_states:
            raise StateSpaceTooLarge(
                f"convolution exceeded max_states={max_states}"
            )
        states = updated

    values = np.fromiter(states.keys(), dtype=np.float64)
    probabilities = np.fromiter(states.values(), dtype=np.float64)
    probabilities /= probabilities.sum()
    order = np.argsort(values)
    return ExactDistribution(values[order], probabilities[order])

