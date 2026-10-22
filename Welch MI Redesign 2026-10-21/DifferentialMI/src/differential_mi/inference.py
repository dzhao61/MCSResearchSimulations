"""Two-sample MI tests using influence-function studentization."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
from scipy.stats import norm, t

from .statistics import (
    analytic_bias_corrected_mi,
    influence_variance,
    jackknife_mi,
    plugin_mi,
)


@dataclass(frozen=True)
class AnalyticWaldResult:
    """Primary deterministic inference result for a difference in discrete MI."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    degrees_of_freedom: int
    mi_p_plugin: float
    mi_q_plugin: float
    bias_correction_p: float
    bias_correction_q: float
    mi_p_corrected: float
    mi_q_corrected: float
    delta_corrected: float
    influence_variance_p: float
    influence_variance_q: float
    standard_error: float
    z_statistic: float
    p_value: float
    confidence_level: float
    confidence_interval_low: float
    confidence_interval_high: float
    zero_fraction_p: float
    zero_fraction_q: float
    expected_below_1_fraction_p: float
    expected_below_1_fraction_q: float
    expected_below_5_fraction_p: float
    expected_below_5_fraction_q: float
    minimum_independence_expected_p: float
    minimum_independence_expected_q: float
    standardized_bias_difference: float
    numerically_computable: bool
    valid_first_order_calculation: bool
    elapsed_seconds: float

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class WelchSatterthwaiteResult:
    """Primary finite-df reference for analytic differential-MI inference."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    degrees_of_freedom: int
    mi_p_plugin: float
    mi_q_plugin: float
    bias_correction_p: float
    bias_correction_q: float
    mi_p_corrected: float
    mi_q_corrected: float
    delta_corrected: float
    influence_variance_p: float
    influence_variance_q: float
    variance_component_p: float
    variance_component_q: float
    standard_error: float
    statistic: float
    normal_p_value: float
    welch_degrees_of_freedom: float
    p_value: float
    confidence_level: float
    confidence_interval_low: float
    confidence_interval_high: float
    zero_fraction_p: float
    zero_fraction_q: float
    expected_below_1_fraction_p: float
    expected_below_1_fraction_q: float
    expected_below_5_fraction_p: float
    expected_below_5_fraction_q: float
    minimum_independence_expected_p: float
    minimum_independence_expected_q: float
    standardized_bias_difference: float
    numerically_computable: bool
    valid_first_order_calculation: bool
    elapsed_seconds: float

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class InfluenceSaddlepointResult:
    """Experimental empirical-saddlepoint result for a difference in MI."""

    rows: int
    columns: int
    n_p: int
    n_q: int
    delta_corrected: float
    standard_error: float
    wald_p_value: float
    saddlepoint_p_value: float
    lower_tail_probability: float
    upper_tail_probability: float
    route: str
    support_lower: float
    support_upper: float
    saddlepoint_root: float
    root_residual: float
    root_iterations: int
    cgf_at_root: float
    cgf_second_at_root: float
    lugannani_rice_w: float
    lugannani_rice_u: float
    tail_was_clipped: bool
    numerically_computable: bool
    valid_first_order_calculation: bool
    elapsed_seconds: float

    def to_dict(self) -> dict[str, float | int | bool | str]:
        return asdict(self)


@dataclass(frozen=True)
class ComparisonResult:
    n_p: int
    n_q: int
    mi_p_plugin: float
    mi_q_plugin: float
    mi_p_analytic: float
    mi_q_analytic: float
    mi_p_jackknife: float
    mi_q_jackknife: float
    delta_plugin: float
    delta_analytic: float
    delta_jackknife: float
    pooled_mi_plugin: float
    pooled_influence_variance: float
    standard_error: float
    z_plugin: float
    z_analytic: float
    z_jackknife: float
    wald_plugin_p: float
    wald_analytic_p: float
    wald_jackknife_p: float
    welch_satterthwaite_p: float
    welch_degrees_of_freedom: float
    naive_perm_plugin_p: float
    student_perm_plugin_p: float
    student_perm_analytic_p: float
    student_perm_jackknife_p: float
    valid_studentization: bool
    permutations: int
    deterministic_seconds: float
    permutation_seconds: float

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def _safe_z(delta: np.ndarray, standard_error: np.ndarray) -> np.ndarray:
    delta_values = np.asarray(delta, dtype=float)
    se_values = np.asarray(standard_error, dtype=float)
    return np.divide(
        delta_values,
        se_values,
        out=np.full_like(delta_values, np.nan),
        where=np.isfinite(se_values) & (se_values > 0),
    )


def _welch_satterthwaite_df(
    component_p: float,
    component_q: float,
    n_p: int,
    n_q: int,
) -> float:
    if n_p <= 1 or n_q <= 1:
        return float("nan")
    denominator = (
        component_p**2 / (n_p - 1.0)
        + component_q**2 / (n_q - 1.0)
    )
    if not np.isfinite(denominator) or denominator <= 0:
        return float("nan")
    return float((component_p + component_q) ** 2 / denominator)


def _monte_carlo_p(reference: np.ndarray, observed: float) -> float:
    valid = np.asarray(reference, dtype=float)
    valid = valid[np.isfinite(valid)]
    if valid.size == 0 or not np.isfinite(observed):
        return float("nan")
    return float((1 + np.count_nonzero(np.abs(valid) >= abs(observed))) / (valid.size + 1))


def _validated_table_pair(
    table_p: np.ndarray, table_q: np.ndarray
) -> tuple[np.ndarray, np.ndarray, int, int]:
    raw_p = np.asarray(table_p)
    raw_q = np.asarray(table_q)
    if raw_p.shape != raw_q.shape or raw_p.ndim != 2:
        raise ValueError("The two tables must have the same two-dimensional shape.")
    if min(raw_p.shape) < 2:
        raise ValueError("Each table dimension must contain at least two categories.")
    if np.iscomplexobj(raw_p) or np.iscomplexobj(raw_q):
        raise ValueError("Counts must be finite nonnegative integers.")
    try:
        numeric_p = np.asarray(raw_p, dtype=float)
        numeric_q = np.asarray(raw_q, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Counts must be finite nonnegative integers.") from error
    if (
        np.any(~np.isfinite(numeric_p))
        or np.any(~np.isfinite(numeric_q))
        or np.any(numeric_p != np.floor(numeric_p))
        or np.any(numeric_q != np.floor(numeric_q))
        or np.any(numeric_p > np.iinfo(np.int64).max)
        or np.any(numeric_q > np.iinfo(np.int64).max)
    ):
        raise ValueError("Counts must be finite nonnegative integers.")
    p = numeric_p.astype(np.int64)
    q = numeric_q.astype(np.int64)
    if np.any(p < 0) or np.any(q < 0):
        raise ValueError("Counts cannot be negative.")
    n_p = int(p.sum())
    n_q = int(q.sum())
    if min(n_p, n_q) <= 1:
        raise ValueError("Each group needs at least two observations.")
    return p, q, n_p, n_q


def _support_diagnostics(table: np.ndarray) -> tuple[float, float, float, float]:
    counts = np.asarray(table, dtype=float)
    total = counts.sum()
    expected = np.outer(counts.sum(axis=1), counts.sum(axis=0)) / total
    return (
        float(np.mean(counts == 0)),
        float(np.mean(expected < 1.0)),
        float(np.mean(expected < 5.0)),
        float(expected.min()),
    )


@dataclass(frozen=True)
class _InfluenceCGF:
    probability_p: np.ndarray
    score_p: np.ndarray
    probability_q: np.ndarray
    score_q: np.ndarray
    n_p: int
    n_q: int

    @property
    def support(self) -> tuple[float, float]:
        return (
            float(self.score_p.min() - self.score_q.max()),
            float(self.score_p.max() - self.score_q.min()),
        )

    def evaluate(self, t: float) -> tuple[float, float, float]:
        """Return K(t), K'(t), and K''(t) using stable exponential tilting."""
        scaled_p = t * self.score_p / self.n_p
        scaled_q = -t * self.score_q / self.n_q
        log_mgf_p = float(logsumexp(np.log(self.probability_p) + scaled_p))
        log_mgf_q = float(logsumexp(np.log(self.probability_q) + scaled_q))
        tilted_p = self.probability_p * np.exp(scaled_p - log_mgf_p)
        tilted_q = self.probability_q * np.exp(scaled_q - log_mgf_q)

        mean_p = float(np.dot(tilted_p, self.score_p))
        mean_q = float(np.dot(tilted_q, self.score_q))
        variance_p = float(
            np.dot(tilted_p, (self.score_p - mean_p) ** 2)
        )
        variance_q = float(
            np.dot(tilted_q, (self.score_q - mean_q) ** 2)
        )
        cgf = self.n_p * log_mgf_p + self.n_q * log_mgf_q
        first = mean_p - mean_q
        second = variance_p / self.n_p + variance_q / self.n_q
        return float(cgf), float(first), float(max(second, 0.0))


def _influence_distribution(table: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    counts = np.asarray(table, dtype=float)
    total = float(counts.sum())
    probability = counts / total
    row = probability.sum(axis=1)
    column = probability.sum(axis=0)
    occupied_row, occupied_column = np.nonzero(counts)
    occupied_probability = probability[occupied_row, occupied_column]
    local_mi = (
        np.log(occupied_probability)
        - np.log(row[occupied_row])
        - np.log(column[occupied_column])
    )
    mean = float(np.dot(occupied_probability, local_mi))
    score = local_mi - mean
    return occupied_probability, score


def _build_influence_cgf(
    table_p: np.ndarray,
    table_q: np.ndarray,
    n_p: int,
    n_q: int,
) -> _InfluenceCGF:
    probability_p, score_p = _influence_distribution(table_p)
    probability_q, score_q = _influence_distribution(table_q)
    return _InfluenceCGF(
        probability_p=probability_p,
        score_p=score_p,
        probability_q=probability_q,
        score_q=score_q,
        n_p=n_p,
        n_q=n_q,
    )


def _normal_saddlepoint_fallback(
    x: float, standard_error: float
) -> tuple[float, float, float]:
    z = x / standard_error
    lower = float(norm.cdf(z))
    upper = float(norm.sf(z))
    return lower, upper, float(min(1.0, 2.0 * min(lower, upper)))


def _saddlepoint_root(
    cgf: _InfluenceCGF,
    x: float,
    variance: float,
) -> tuple[float, int, float]:
    """Find K'(t)=x with an adaptively expanded sign-correct bracket."""
    initial = max(1.0, abs(x) / variance)
    if x > 0:
        lower, upper = 0.0, initial
        for _ in range(80):
            if cgf.evaluate(upper)[1] >= x:
                break
            upper *= 2.0
        else:
            raise RuntimeError("Could not bracket the positive saddlepoint root.")
    else:
        lower, upper = -initial, 0.0
        for _ in range(80):
            if cgf.evaluate(lower)[1] <= x:
                break
            lower *= 2.0
        else:
            raise RuntimeError("Could not bracket the negative saddlepoint root.")

    root, result = brentq(
        lambda value: cgf.evaluate(value)[1] - x,
        lower,
        upper,
        xtol=1e-12,
        rtol=4.0 * np.finfo(float).eps,
        maxiter=100,
        full_output=True,
        disp=False,
    )
    residual = cgf.evaluate(float(root))[1] - x
    return float(root), int(result.iterations), float(residual)


def influence_saddlepoint_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    near_mean_z: float = 1e-2,
) -> InfluenceSaddlepointResult:
    """Approximate the corrected MI-difference tail by empirical saddlepoint.

    This experimental method applies a Lugannani-Rice approximation to the
    empirical influence-function sum. Explicit normal routes cover the
    singular near-mean expression, empirical support endpoints, and numerical
    failures.
    """
    if near_mean_z <= 0:
        raise ValueError("near_mean_z must be positive.")
    p, q, n_p, n_q = _validated_table_pair(table_p, table_q)
    start = perf_counter()
    rows, columns = p.shape
    degrees_of_freedom = (rows - 1) * (columns - 1)
    delta = float(
        plugin_mi(p)
        - degrees_of_freedom / (2.0 * n_p)
        - plugin_mi(q)
        + degrees_of_freedom / (2.0 * n_q)
    )
    variance = float(influence_variance(p) / n_p + influence_variance(q) / n_q)
    standard_error = float(np.sqrt(variance))
    valid = bool(np.isfinite(standard_error) and standard_error > 0)
    wald_p = (
        float(2.0 * norm.sf(abs(delta / standard_error)))
        if valid
        else float("nan")
    )
    cgf = _build_influence_cgf(p, q, n_p, n_q)
    support_lower, support_upper = cgf.support

    route = "invalid"
    saddlepoint_p = float("nan")
    lower_tail = float("nan")
    upper_tail = float("nan")
    root = float("nan")
    residual = float("nan")
    iterations = 0
    cgf_at_root = float("nan")
    cgf_second = float("nan")
    w = float("nan")
    u = float("nan")
    tail_was_clipped = False

    if valid:
        standardized = abs(delta) / standard_error
        support_tolerance = 1e-12 * max(
            1.0, abs(support_lower), abs(support_upper)
        )
        if standardized <= near_mean_z:
            route = "normal_near_mean"
            lower_tail, upper_tail, saddlepoint_p = _normal_saddlepoint_fallback(
                delta, standard_error
            )
        elif (
            delta <= support_lower + support_tolerance
            or delta >= support_upper - support_tolerance
        ):
            route = "normal_support_boundary"
            lower_tail, upper_tail, saddlepoint_p = _normal_saddlepoint_fallback(
                delta, standard_error
            )
        else:
            try:
                root, iterations, residual = _saddlepoint_root(
                    cgf, delta, variance
                )
                cgf_at_root, _, cgf_second = cgf.evaluate(root)
                deviance = 2.0 * (root * delta - cgf_at_root)
                if deviance <= 0.0 or cgf_second <= 0.0:
                    raise FloatingPointError("Invalid saddlepoint curvature.")
                w = float(np.copysign(np.sqrt(deviance), root))
                u = float(root * np.sqrt(cgf_second))
                if min(abs(w), abs(u)) <= 1e-8:
                    raise FloatingPointError("Unstable near-mean tail expression.")
                correction = float(norm.pdf(w) * (1.0 / w - 1.0 / u))
                raw_lower = float(norm.cdf(w) + correction)
                raw_upper = float(norm.sf(w) - correction)
                if not np.isfinite(raw_lower + raw_upper):
                    raise FloatingPointError("Nonfinite Lugannani-Rice tail.")
                if raw_lower < -0.01 or raw_upper < -0.01:
                    raise FloatingPointError("Invalid Lugannani-Rice tail.")
                lower_tail = float(np.clip(raw_lower, 0.0, 1.0))
                upper_tail = float(np.clip(raw_upper, 0.0, 1.0))
                tail_was_clipped = bool(
                    lower_tail != raw_lower or upper_tail != raw_upper
                )
                total = lower_tail + upper_tail
                if total <= 0:
                    raise FloatingPointError("Zero total tail probability.")
                lower_tail /= total
                upper_tail /= total
                saddlepoint_p = float(
                    np.clip(2.0 * min(lower_tail, upper_tail), 0.0, 1.0)
                )
                route = "lugannani_rice"
            except (RuntimeError, ValueError, FloatingPointError, OverflowError):
                route = "normal_numerical_fallback"
                lower_tail, upper_tail, saddlepoint_p = (
                    _normal_saddlepoint_fallback(delta, standard_error)
                )

    elapsed_seconds = perf_counter() - start
    return InfluenceSaddlepointResult(
        rows=rows,
        columns=columns,
        n_p=n_p,
        n_q=n_q,
        delta_corrected=delta,
        standard_error=standard_error,
        wald_p_value=wald_p,
        saddlepoint_p_value=saddlepoint_p,
        lower_tail_probability=lower_tail,
        upper_tail_probability=upper_tail,
        route=route,
        support_lower=support_lower,
        support_upper=support_upper,
        saddlepoint_root=root,
        root_residual=residual,
        root_iterations=iterations,
        cgf_at_root=cgf_at_root,
        cgf_second_at_root=cgf_second,
        lugannani_rice_w=w,
        lugannani_rice_u=u,
        tail_was_clipped=tail_was_clipped,
        numerically_computable=valid,
        valid_first_order_calculation=valid,
        elapsed_seconds=elapsed_seconds,
    )


def analytic_wald_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    confidence_level: float = 0.95,
) -> AnalyticWaldResult:
    """Test equality of two discrete MI values using the normal comparator.

    The calculation uses natural logarithms, the classical full-support
    first-order bias correction, and the empirical influence-function
    variance. It reports diagnostics but does not silently route unsupported
    boundary cases to another method.
    """
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie strictly between zero and one.")
    p, q, n_p, n_q = _validated_table_pair(table_p, table_q)
    start = perf_counter()
    rows, columns = p.shape
    degrees_of_freedom = (rows - 1) * (columns - 1)
    mi_p_plugin = float(plugin_mi(p))
    mi_q_plugin = float(plugin_mi(q))
    bias_correction_p = degrees_of_freedom / (2.0 * n_p)
    bias_correction_q = degrees_of_freedom / (2.0 * n_q)
    mi_p_corrected = mi_p_plugin - bias_correction_p
    mi_q_corrected = mi_q_plugin - bias_correction_q
    delta_corrected = mi_p_corrected - mi_q_corrected
    variance_p = float(influence_variance(p))
    variance_q = float(influence_variance(q))
    standard_error = float(np.sqrt(variance_p / n_p + variance_q / n_q))
    z_statistic = float(
        _safe_z(np.asarray(delta_corrected), np.asarray(standard_error))
    )
    valid = bool(
        np.isfinite(z_statistic)
        and np.isfinite(standard_error)
        and standard_error > 0
    )
    p_value = (
        float(2.0 * norm.sf(abs(z_statistic))) if valid else float("nan")
    )
    critical = float(norm.ppf((1.0 + confidence_level) / 2.0))
    confidence_interval_low = (
        float(delta_corrected - critical * standard_error)
        if valid
        else float("nan")
    )
    confidence_interval_high = (
        float(delta_corrected + critical * standard_error)
        if valid
        else float("nan")
    )
    support_p = _support_diagnostics(p)
    support_q = _support_diagnostics(q)
    standardized_bias_difference = (
        float(abs(bias_correction_p - bias_correction_q) / standard_error)
        if valid
        else float("nan")
    )
    elapsed_seconds = perf_counter() - start
    return AnalyticWaldResult(
        rows=rows,
        columns=columns,
        n_p=n_p,
        n_q=n_q,
        degrees_of_freedom=degrees_of_freedom,
        mi_p_plugin=mi_p_plugin,
        mi_q_plugin=mi_q_plugin,
        bias_correction_p=bias_correction_p,
        bias_correction_q=bias_correction_q,
        mi_p_corrected=mi_p_corrected,
        mi_q_corrected=mi_q_corrected,
        delta_corrected=delta_corrected,
        influence_variance_p=variance_p,
        influence_variance_q=variance_q,
        standard_error=standard_error,
        z_statistic=z_statistic,
        p_value=p_value,
        confidence_level=confidence_level,
        confidence_interval_low=confidence_interval_low,
        confidence_interval_high=confidence_interval_high,
        zero_fraction_p=support_p[0],
        zero_fraction_q=support_q[0],
        expected_below_1_fraction_p=support_p[1],
        expected_below_1_fraction_q=support_q[1],
        expected_below_5_fraction_p=support_p[2],
        expected_below_5_fraction_q=support_q[2],
        minimum_independence_expected_p=support_p[3],
        minimum_independence_expected_q=support_q[3],
        standardized_bias_difference=standardized_bias_difference,
        numerically_computable=valid,
        valid_first_order_calculation=valid,
        elapsed_seconds=elapsed_seconds,
    )


def welch_satterthwaite_test(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    confidence_level: float = 0.95,
) -> WelchSatterthwaiteResult:
    """Apply the prospective primary reference to differential-MI inference.

    The estimate, first-order bias correction, influence variance, standard
    error, and statistic are identical to :func:`analytic_wald_test`. Only
    the normal reference is replaced by a Student t reference whose effective
    degrees of freedom use the Welch-Satterthwaite variance-component
    approximation.

    This is an empirically calibrated finite-sample approximation, not an
    exact t test. In particular, the empirical MI influence variances are not
    ordinary sample variances from fixed Gaussian observations, so assigning
    each component ``n_i - 1`` degrees of freedom is a heuristic rather than
    a derived moment match for the plug-in variance functional.
    """
    start = perf_counter()
    normal = analytic_wald_test(
        table_p,
        table_q,
        confidence_level=confidence_level,
    )
    component_p = normal.influence_variance_p / normal.n_p
    component_q = normal.influence_variance_q / normal.n_q
    welch_degrees_of_freedom = _welch_satterthwaite_df(
        component_p,
        component_q,
        normal.n_p,
        normal.n_q,
    )
    valid = bool(
        normal.influence_variance_p + normal.influence_variance_q > 1e-14
        and normal.numerically_computable
        and np.isfinite(welch_degrees_of_freedom)
        and welch_degrees_of_freedom > 0
    )
    normal_p_value = normal.p_value if valid else float("nan")
    p_value = (
        float(2.0 * t.sf(abs(normal.z_statistic), df=welch_degrees_of_freedom))
        if valid
        else float("nan")
    )
    critical = (
        float(
            t.ppf(
                (1.0 + confidence_level) / 2.0,
                df=welch_degrees_of_freedom,
            )
        )
        if valid
        else float("nan")
    )
    confidence_interval_low = (
        float(normal.delta_corrected - critical * normal.standard_error)
        if valid
        else float("nan")
    )
    confidence_interval_high = (
        float(normal.delta_corrected + critical * normal.standard_error)
        if valid
        else float("nan")
    )
    elapsed_seconds = perf_counter() - start
    return WelchSatterthwaiteResult(
        rows=normal.rows,
        columns=normal.columns,
        n_p=normal.n_p,
        n_q=normal.n_q,
        degrees_of_freedom=normal.degrees_of_freedom,
        mi_p_plugin=normal.mi_p_plugin,
        mi_q_plugin=normal.mi_q_plugin,
        bias_correction_p=normal.bias_correction_p,
        bias_correction_q=normal.bias_correction_q,
        mi_p_corrected=normal.mi_p_corrected,
        mi_q_corrected=normal.mi_q_corrected,
        delta_corrected=normal.delta_corrected,
        influence_variance_p=normal.influence_variance_p,
        influence_variance_q=normal.influence_variance_q,
        variance_component_p=component_p,
        variance_component_q=component_q,
        standard_error=normal.standard_error,
        statistic=normal.z_statistic,
        normal_p_value=normal_p_value,
        welch_degrees_of_freedom=welch_degrees_of_freedom,
        p_value=p_value,
        confidence_level=confidence_level,
        confidence_interval_low=confidence_interval_low,
        confidence_interval_high=confidence_interval_high,
        zero_fraction_p=normal.zero_fraction_p,
        zero_fraction_q=normal.zero_fraction_q,
        expected_below_1_fraction_p=normal.expected_below_1_fraction_p,
        expected_below_1_fraction_q=normal.expected_below_1_fraction_q,
        expected_below_5_fraction_p=normal.expected_below_5_fraction_p,
        expected_below_5_fraction_q=normal.expected_below_5_fraction_q,
        minimum_independence_expected_p=normal.minimum_independence_expected_p,
        minimum_independence_expected_q=normal.minimum_independence_expected_q,
        standardized_bias_difference=normal.standardized_bias_difference,
        numerically_computable=valid,
        valid_first_order_calculation=valid,
        elapsed_seconds=elapsed_seconds,
    )


def compare_tables(
    table_p: np.ndarray,
    table_q: np.ndarray,
    *,
    permutations: int,
    rng: np.random.Generator,
) -> ComparisonResult:
    """Compare MI from two count tables and return all pilot methods."""
    if not isinstance(permutations, (int, np.integer)) or permutations <= 0:
        raise ValueError("permutations must be a positive integer.")
    p, q, n_p, n_q = _validated_table_pair(table_p, table_q)

    deterministic_start = perf_counter()
    mi_p_plugin = float(plugin_mi(p))
    mi_q_plugin = float(plugin_mi(q))
    mi_p_analytic = float(analytic_bias_corrected_mi(p))
    mi_q_analytic = float(analytic_bias_corrected_mi(q))
    mi_p_jackknife = float(jackknife_mi(p))
    mi_q_jackknife = float(jackknife_mi(q))
    delta_plugin = mi_p_plugin - mi_q_plugin
    delta_analytic = mi_p_analytic - mi_q_analytic
    delta_jackknife = mi_p_jackknife - mi_q_jackknife
    pooled_mi_plugin = float(plugin_mi(p + q))
    pooled_influence_variance = float(influence_variance(p + q))
    var_p = float(influence_variance(p))
    var_q = float(influence_variance(q))
    standard_error = float(np.sqrt(var_p / n_p + var_q / n_q))
    z_plugin = float(_safe_z(np.asarray(delta_plugin), np.asarray(standard_error)))
    z_analytic = float(
        _safe_z(np.asarray(delta_analytic), np.asarray(standard_error))
    )
    z_jackknife = float(
        _safe_z(np.asarray(delta_jackknife), np.asarray(standard_error))
    )
    wald_plugin_p = (
        float(2.0 * norm.sf(abs(z_plugin))) if np.isfinite(z_plugin) else float("nan")
    )
    wald_analytic_p = (
        float(2.0 * norm.sf(abs(z_analytic)))
        if np.isfinite(z_analytic)
        else float("nan")
    )
    wald_jackknife_p = (
        float(2.0 * norm.sf(abs(z_jackknife)))
        if np.isfinite(z_jackknife)
        else float("nan")
    )
    component_p = var_p / n_p
    component_q = var_q / n_q
    welch_degrees_of_freedom = _welch_satterthwaite_df(
        component_p,
        component_q,
        n_p,
        n_q,
    )
    welch_satterthwaite_p = (
        float(2.0 * t.sf(abs(z_analytic), df=welch_degrees_of_freedom))
        if (
            var_p + var_q > 1e-14
            and np.isfinite(z_analytic)
            and np.isfinite(welch_degrees_of_freedom)
        )
        else float("nan")
    )
    deterministic_seconds = perf_counter() - deterministic_start

    permutation_start = perf_counter()
    pooled_flat = (p + q).reshape(-1)
    perm_p_flat = rng.multivariate_hypergeometric(
        pooled_flat, n_p, size=permutations
    )
    perm_p = perm_p_flat.reshape(permutations, *p.shape)
    perm_q = (pooled_flat[None, :] - perm_p_flat).reshape(permutations, *q.shape)

    perm_plugin_delta = plugin_mi(perm_p) - plugin_mi(perm_q)
    naive_perm_plugin_p = _monte_carlo_p(perm_plugin_delta, delta_plugin)

    perm_analytic_delta = analytic_bias_corrected_mi(
        perm_p
    ) - analytic_bias_corrected_mi(perm_q)
    perm_jackknife_delta = jackknife_mi(perm_p) - jackknife_mi(perm_q)
    perm_var_p = influence_variance(perm_p)
    perm_var_q = influence_variance(perm_q)
    perm_se = np.sqrt(perm_var_p / n_p + perm_var_q / n_q)
    perm_z_plugin = _safe_z(perm_plugin_delta, perm_se)
    perm_z_analytic = _safe_z(perm_analytic_delta, perm_se)
    perm_z_jackknife = _safe_z(perm_jackknife_delta, perm_se)
    student_perm_plugin_p = _monte_carlo_p(perm_z_plugin, z_plugin)
    student_perm_analytic_p = _monte_carlo_p(perm_z_analytic, z_analytic)
    student_perm_jackknife_p = _monte_carlo_p(perm_z_jackknife, z_jackknife)
    permutation_seconds = perf_counter() - permutation_start

    return ComparisonResult(
        n_p=n_p,
        n_q=n_q,
        mi_p_plugin=mi_p_plugin,
        mi_q_plugin=mi_q_plugin,
        mi_p_analytic=mi_p_analytic,
        mi_q_analytic=mi_q_analytic,
        mi_p_jackknife=mi_p_jackknife,
        mi_q_jackknife=mi_q_jackknife,
        delta_plugin=delta_plugin,
        delta_analytic=delta_analytic,
        delta_jackknife=delta_jackknife,
        pooled_mi_plugin=pooled_mi_plugin,
        pooled_influence_variance=pooled_influence_variance,
        standard_error=standard_error,
        z_plugin=z_plugin,
        z_analytic=z_analytic,
        z_jackknife=z_jackknife,
        wald_plugin_p=wald_plugin_p,
        wald_analytic_p=wald_analytic_p,
        wald_jackknife_p=wald_jackknife_p,
        welch_satterthwaite_p=welch_satterthwaite_p,
        welch_degrees_of_freedom=welch_degrees_of_freedom,
        naive_perm_plugin_p=naive_perm_plugin_p,
        student_perm_plugin_p=student_perm_plugin_p,
        student_perm_analytic_p=student_perm_analytic_p,
        student_perm_jackknife_p=student_perm_jackknife_p,
        valid_studentization=bool(
            np.isfinite(z_plugin)
            and np.isfinite(z_jackknife)
            and standard_error > 0
        ),
        permutations=permutations,
        deterministic_seconds=deterministic_seconds,
        permutation_seconds=permutation_seconds,
    )
