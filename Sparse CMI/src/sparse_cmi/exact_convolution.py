from __future__ import annotations

from collections.abc import Iterable
from collections import defaultdict
from dataclasses import dataclass
import math

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
        indices = np.searchsorted(
            values,
            np.asarray(statistics) - tolerance,
            side="left",
        )
        result = np.zeros_like(np.asarray(statistics), dtype=np.float64)
        valid = indices < values.size
        result[valid] = tails[indices[valid]]
        return result


@dataclass(frozen=True)
class ConvolutionComplexity:
    state_upper_bound: int
    transition_upper_bound: int
    informative_components: int


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


def _group_components(
    components: list[dict[float, float]],
) -> list[list[dict[float, float]]]:
    grouped: dict[tuple[float, ...], list[dict[float, float]]] = defaultdict(list)
    for component in components:
        if len(component) > 1:
            grouped[tuple(component)].append(component)
    groups = list(grouped.values())
    groups.sort(
        key=lambda group: (
            math.comb(
                len(group) + len(group[0]) - 1,
                len(group[0]) - 1,
            ),
            len(group[0]),
        )
    )
    return groups


def estimate_convolution_complexity(
    strata: Iterable[Stratum],
    *,
    rounding_decimals: int = 12,
    cap: int | None = None,
) -> ConvolutionComplexity:
    """Bound exact states and transition work using repeated supports."""

    components = [
        _collapsed_stratum(stratum, rounding_decimals) for stratum in strata
    ]
    groups = _group_components(components)
    state_bound = 1
    transition_bound = 0
    informative = 0
    saturated = cap + 1 if cap is not None else None

    for group in groups:
        repetitions = len(group)
        support_size = len(group[0])
        informative += repetitions
        for index in range(1, repetitions + 1):
            within_group_states = math.comb(
                index + support_size - 2,
                support_size - 1,
            )
            transition_bound += (
                state_bound * within_group_states * support_size
            )
            if saturated is not None and transition_bound >= saturated:
                transition_bound = saturated
        group_states = math.comb(
            repetitions + support_size - 1,
            support_size - 1,
        )
        state_bound *= group_states
        if saturated is not None and state_bound >= saturated:
            state_bound = saturated

    return ConvolutionComplexity(
        state_upper_bound=state_bound,
        transition_upper_bound=transition_bound,
        informative_components=informative,
    )


def exact_conditional_distribution(
    strata: Iterable[Stratum],
    *,
    max_states: int = 250_000,
    rounding_decimals: int = 12,
) -> ExactDistribution:
    """Numerically convolve the finite conditional distributions."""

    components = [
        _collapsed_stratum(stratum, rounding_decimals) for stratum in strata
    ]
    constant = sum(
        next(iter(component))
        for component in components
        if len(component) == 1
    )
    ordered_components = [
        component
        for group in _group_components(components)
        for component in group
    ]

    states: dict[float, float] = {round(constant, rounding_decimals): 1.0}
    for component in ordered_components:
        if len(states) * len(component) > max_states * 4:
            raise StateSpaceTooLarge(
                "intermediate convolution exceeds the transition-work guard"
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
