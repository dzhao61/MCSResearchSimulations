from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import math

import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
from scipy.stats import norm

from .approximations import edgeworth_pvalue
from .hypergeom import stratum_null
from .models import Stratum


@dataclass(frozen=True)
class SaddlepointResult:
    pvalue: float
    s_hat: float | None
    w: float | None
    u: float | None
    k_hat: float | None
    k2_hat: float | None
    iterations: int
    converged: bool
    fallback: str
    support_min: float
    support_max: float


@dataclass(frozen=True)
class _CGFComponent:
    g_values: np.ndarray
    log_probabilities: np.ndarray
    minimum: float
    maximum: float
    minimum_mass: float
    maximum_mass: float
    multiplicity: int = 1


class FactorizedConditionalCGF:
    """Exact conditional CGF for a sum of binary-CMI stratum statistics."""

    def __init__(self, strata: Iterable[Stratum]) -> None:
        self.strata = tuple(strata)
        raw_components = tuple(
            self._component_from_stratum(stratum) for stratum in self.strata
        )
        self._components = self._group_components(raw_components)
        self.component_count = len(raw_components)
        self.unique_component_count = len(self._components)
        self.support_min = float(
            sum(
                component.multiplicity * component.minimum
                for component in self._components
            )
        )
        self.support_max = float(
            sum(
                component.multiplicity * component.maximum
                for component in self._components
            )
        )
        self.minimum_mass = float(
            math.prod(
                component.minimum_mass**component.multiplicity
                for component in self._components
            )
        )
        self.maximum_mass = float(
            math.prod(
                component.maximum_mass**component.multiplicity
                for component in self._components
            )
        )

        _, self.mean, self.variance = self.evaluate(0.0)
        self.third_cumulant = 0.0
        for component in self._components:
            probabilities = np.exp(component.log_probabilities)
            component_mean = float(np.dot(probabilities, component.g_values))
            self.third_cumulant += component.multiplicity * float(
                np.dot(
                    probabilities,
                    (component.g_values - component_mean) ** 3,
                )
            )
        self.skewness = (
            self.third_cumulant / self.variance**1.5
            if self.variance > 0
            else 0.0
        )

    @staticmethod
    def _component_from_stratum(stratum: Stratum) -> _CGFComponent:
        null = stratum_null(stratum)
        probabilities = np.array(
            null.probabilities,
            dtype=np.float64,
            copy=True,
        )
        probabilities /= probabilities.sum()
        g_values = np.asarray(null.g_values, dtype=np.float64)
        minimum = float(g_values.min())
        maximum = float(g_values.max())
        tolerance = 1e-12 * max(1.0, abs(minimum), abs(maximum))
        minimum_mass = float(probabilities[g_values <= minimum + tolerance].sum())
        maximum_mass = float(probabilities[g_values >= maximum - tolerance].sum())
        return _CGFComponent(
            g_values=g_values,
            log_probabilities=np.log(probabilities),
            minimum=minimum,
            maximum=maximum,
            minimum_mass=minimum_mass,
            maximum_mass=maximum_mass,
        )

    @staticmethod
    def _group_components(
        components: tuple[_CGFComponent, ...],
    ) -> tuple[_CGFComponent, ...]:
        grouped: dict[tuple[bytes, bytes], _CGFComponent] = {}
        multiplicities: dict[tuple[bytes, bytes], int] = {}
        for component in components:
            key = (
                component.g_values.tobytes(),
                component.log_probabilities.tobytes(),
            )
            grouped.setdefault(key, component)
            multiplicities[key] = multiplicities.get(key, 0) + 1
        return tuple(
            _CGFComponent(
                g_values=component.g_values,
                log_probabilities=component.log_probabilities,
                minimum=component.minimum,
                maximum=component.maximum,
                minimum_mass=component.minimum_mass,
                maximum_mass=component.maximum_mass,
                multiplicity=multiplicities[key],
            )
            for key, component in grouped.items()
        )

    def evaluate(self, s: float) -> tuple[float, float, float]:
        """Return K(s), K'(s), and K''(s) using stable exponential tilting."""

        if not np.isfinite(s):
            raise ValueError("s must be finite")
        k_value = 0.0
        first = 0.0
        second = 0.0
        for component in self._components:
            log_weights = (
                component.log_probabilities + float(s) * component.g_values
            )
            log_normalizer = float(logsumexp(log_weights))
            weights = np.exp(log_weights - log_normalizer)
            tilted_mean = float(np.dot(weights, component.g_values))
            centered = component.g_values - tilted_mean
            tilted_variance = float(np.dot(weights, centered**2))
            k_value += component.multiplicity * log_normalizer
            first += component.multiplicity * tilted_mean
            second += component.multiplicity * max(0.0, tilted_variance)
        return float(k_value), float(first), float(second)

    def _fallback_pvalue(self, statistic: float) -> float:
        return float(
            edgeworth_pvalue(
                statistic,
                self.mean,
                self.variance,
                self.skewness,
            )
        )

    def _root(self, statistic: float) -> tuple[float, int]:
        if statistic > self.mean:
            lower = 0.0
            upper = max(1.0, (statistic - self.mean) / self.variance)
            for _ in range(60):
                if self.evaluate(upper)[1] >= statistic:
                    break
                upper *= 2.0
            else:
                raise RuntimeError("failed to bracket the right saddlepoint")
        else:
            upper = 0.0
            lower = min(-1.0, (statistic - self.mean) / self.variance)
            for _ in range(60):
                if self.evaluate(lower)[1] <= statistic:
                    break
                lower *= 2.0
            else:
                raise RuntimeError("failed to bracket the left saddlepoint")

        root, details = brentq(
            lambda value: self.evaluate(value)[1] - statistic,
            lower,
            upper,
            xtol=1e-12,
            rtol=1e-12,
            maxiter=100,
            full_output=True,
            disp=False,
        )
        if not details.converged:
            raise RuntimeError("saddlepoint root did not converge")
        return float(root), int(details.iterations)

    def upper_tail(self, statistic: float) -> SaddlepointResult:
        """Approximate P(G^2 >= statistic) with Lugannani-Rice."""

        value = float(statistic)
        scale = max(1.0, abs(self.support_min), abs(self.support_max))
        tolerance = 1e-11 * scale

        if value <= self.support_min + tolerance:
            return SaddlepointResult(
                pvalue=1.0,
                s_hat=None,
                w=None,
                u=None,
                k_hat=None,
                k2_hat=None,
                iterations=0,
                converged=True,
                fallback="exact_lower_endpoint",
                support_min=self.support_min,
                support_max=self.support_max,
            )
        if value > self.support_max + tolerance:
            return SaddlepointResult(
                pvalue=0.0,
                s_hat=None,
                w=None,
                u=None,
                k_hat=None,
                k2_hat=None,
                iterations=0,
                converged=True,
                fallback="outside_upper_support",
                support_min=self.support_min,
                support_max=self.support_max,
            )
        if value >= self.support_max - tolerance:
            return SaddlepointResult(
                pvalue=self.maximum_mass,
                s_hat=None,
                w=None,
                u=None,
                k_hat=None,
                k2_hat=None,
                iterations=0,
                converged=True,
                fallback="exact_upper_endpoint",
                support_min=self.support_min,
                support_max=self.support_max,
            )
        if self.variance <= 64 * np.finfo(float).eps:
            return SaddlepointResult(
                pvalue=1.0 if value <= self.mean + tolerance else 0.0,
                s_hat=None,
                w=None,
                u=None,
                k_hat=None,
                k2_hat=self.variance,
                iterations=0,
                converged=True,
                fallback="degenerate_variance",
                support_min=self.support_min,
                support_max=self.support_max,
            )

        standard_deviation = math.sqrt(self.variance)
        if abs(value - self.mean) <= 1e-5 * max(1.0, standard_deviation):
            return SaddlepointResult(
                pvalue=self._fallback_pvalue(value),
                s_hat=0.0,
                w=0.0,
                u=0.0,
                k_hat=0.0,
                k2_hat=self.variance,
                iterations=0,
                converged=True,
                fallback="near_mean_edgeworth",
                support_min=self.support_min,
                support_max=self.support_max,
            )

        try:
            s_hat, iterations = self._root(value)
            k_hat, _, k2_hat = self.evaluate(s_hat)
        except (RuntimeError, ValueError, FloatingPointError, OverflowError):
            return SaddlepointResult(
                pvalue=self._fallback_pvalue(value),
                s_hat=None,
                w=None,
                u=None,
                k_hat=None,
                k2_hat=None,
                iterations=0,
                converged=False,
                fallback="root_failure_edgeworth",
                support_min=self.support_min,
                support_max=self.support_max,
            )

        if k2_hat <= 64 * np.finfo(float).eps:
            return SaddlepointResult(
                pvalue=self._fallback_pvalue(value),
                s_hat=s_hat,
                w=None,
                u=None,
                k_hat=k_hat,
                k2_hat=k2_hat,
                iterations=iterations,
                converged=False,
                fallback="tilted_variance_edgeworth",
                support_min=self.support_min,
                support_max=self.support_max,
            )

        radicand = 2.0 * (s_hat * value - k_hat)
        if radicand <= 0:
            return SaddlepointResult(
                pvalue=self._fallback_pvalue(value),
                s_hat=s_hat,
                w=None,
                u=None,
                k_hat=k_hat,
                k2_hat=k2_hat,
                iterations=iterations,
                converged=False,
                fallback="nonpositive_radicand_edgeworth",
                support_min=self.support_min,
                support_max=self.support_max,
            )

        w_value = math.copysign(math.sqrt(radicand), s_hat)
        u_value = s_hat * math.sqrt(k2_hat)
        if abs(w_value) < 1e-7 or abs(u_value) < 1e-10:
            return SaddlepointResult(
                pvalue=self._fallback_pvalue(value),
                s_hat=s_hat,
                w=w_value,
                u=u_value,
                k_hat=k_hat,
                k2_hat=k2_hat,
                iterations=iterations,
                converged=True,
                fallback="small_w_or_u_edgeworth",
                support_min=self.support_min,
                support_max=self.support_max,
            )

        pvalue = float(
            norm.sf(w_value)
            + norm.pdf(w_value) * (1.0 / u_value - 1.0 / w_value)
        )
        fallback = ""
        if (
            not np.isfinite(pvalue)
            or pvalue < 0.0
            or pvalue > 1.0
        ):
            pvalue = self._fallback_pvalue(value)
            fallback = "invalid_lr_edgeworth"

        return SaddlepointResult(
            pvalue=float(np.clip(pvalue, 0.0, 1.0)),
            s_hat=s_hat,
            w=w_value,
            u=u_value,
            k_hat=k_hat,
            k2_hat=k2_hat,
            iterations=iterations,
            converged=True,
            fallback=fallback,
            support_min=self.support_min,
            support_max=self.support_max,
        )

    def upper_tail_array(self, statistics: np.ndarray) -> np.ndarray:
        values = np.asarray(statistics, dtype=np.float64)
        result = np.empty_like(values)
        iterator = np.nditer(
            [values, result],
            op_flags=[["readonly"], ["writeonly"]],
        )
        for input_value, output_value in iterator:
            output_value[...] = self.upper_tail(float(input_value)).pvalue
        return result


def saddlepoint_pvalue(
    strata: Iterable[Stratum],
    statistic: float,
) -> SaddlepointResult:
    return FactorizedConditionalCGF(strata).upper_tail(statistic)
