from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from .exact_convolution import (
    StateSpaceTooLarge,
    estimate_convolution_complexity,
    exact_conditional_distribution,
)
from .models import Stratum
from .moments import AggregateMoments, aggregate_moments
from .saddlepoint import FactorizedConditionalCGF, SaddlepointResult
from .statistic import observed_g2


@dataclass(frozen=True)
class DeterministicTestResult:
    pvalue: float
    statistic: float
    route: str
    moments: AggregateMoments
    exact_state_count: int | None
    exact_state_upper_bound: int
    exact_transition_upper_bound: int
    saddlepoint: SaddlepointResult | None
    warning: str


def deterministic_pvalue(
    strata: Sequence[Stratum],
    *,
    statistic: float | None = None,
    exact_max_informative: int | None = None,
    exact_max_states: int = 100_000,
    exact_max_transitions: int = 100_000,
) -> DeterministicTestResult:
    """Route a binary sparse-CMI test without simulation or permutation."""

    strata_list = list(strata)
    value = observed_g2(strata_list) if statistic is None else float(statistic)
    moments = aggregate_moments(strata_list)
    complexity = estimate_convolution_complexity(
        strata_list,
        cap=max(exact_max_states, exact_max_transitions),
    )
    if moments.variance <= 0:
        return DeterministicTestResult(
            pvalue=1.0 if value <= moments.mean + 1e-10 else 0.0,
            statistic=value,
            route="degenerate",
            moments=moments,
            exact_state_count=1,
            exact_state_upper_bound=complexity.state_upper_bound,
            exact_transition_upper_bound=complexity.transition_upper_bound,
            saddlepoint=None,
            warning="conditional null has zero variance",
        )

    informative_allowed = (
        exact_max_informative is None
        or moments.informative_strata <= exact_max_informative
    )
    exact_is_bounded = (
        complexity.state_upper_bound <= exact_max_states
        and complexity.transition_upper_bound <= exact_max_transitions
    )
    if informative_allowed and exact_is_bounded:
        try:
            exact = exact_conditional_distribution(
                strata_list,
                max_states=exact_max_states,
            )
            return DeterministicTestResult(
                pvalue=exact.upper_tail(value),
                statistic=value,
                route="exact_convolution",
                moments=moments,
                exact_state_count=int(exact.values.size),
                exact_state_upper_bound=complexity.state_upper_bound,
                exact_transition_upper_bound=complexity.transition_upper_bound,
                saddlepoint=None,
                warning="",
            )
        except StateSpaceTooLarge:
            pass

    saddlepoint = FactorizedConditionalCGF(strata_list).upper_tail(value)
    warning = ""
    if saddlepoint.fallback:
        warning = f"saddlepoint used {saddlepoint.fallback}"
    return DeterministicTestResult(
        pvalue=saddlepoint.pvalue,
        statistic=value,
        route="saddlepoint",
        moments=moments,
        exact_state_count=None,
        exact_state_upper_bound=complexity.state_upper_bound,
        exact_transition_upper_bound=complexity.transition_upper_bound,
        saddlepoint=saddlepoint,
        warning=warning,
    )
