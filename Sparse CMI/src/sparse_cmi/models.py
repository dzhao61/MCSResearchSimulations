from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Stratum:
    """Observed 2x2 table represented by its margins and top-left count."""

    n: int
    r: int
    s: int
    a_observed: int
    label: object | None = None

    def __post_init__(self) -> None:
        values = (self.n, self.r, self.s, self.a_observed)
        if any(not isinstance(value, int) for value in values):
            raise TypeError("n, r, s, and a_observed must be Python integers")
        if self.n < 0:
            raise ValueError("n must be non-negative")
        if not 0 <= self.r <= self.n or not 0 <= self.s <= self.n:
            raise ValueError("r and s must lie between 0 and n")
        lower = max(0, self.r + self.s - self.n)
        upper = min(self.r, self.s)
        if not lower <= self.a_observed <= upper:
            raise ValueError(
                f"a_observed={self.a_observed} is outside [{lower}, {upper}]"
            )

    @property
    def support_min(self) -> int:
        return max(0, self.r + self.s - self.n)

    @property
    def support_max(self) -> int:
        return min(self.r, self.s)

    @property
    def support_width(self) -> int:
        return self.support_max - self.support_min + 1


@dataclass(frozen=True)
class CMIResult:
    g2_observed: float
    cmi_nats: float
    mean: float
    variance: float
    third_cumulant: float
    fourth_cumulant: float
    skewness: float
    z_score: float
    p_normal: float
    p_edgeworth: float
    cf_critical_value: float
    p_chi2_nominal: float
    p_chi2_informative: float
    p_exact: float | None
    informative_strata: int
    total_strata: int
    lyapunov_ratio: float
    max_variance_share: float
    exact_state_count: int | None

