from __future__ import annotations

import unittest

import numpy as np

from sparse_cmi.exact_convolution import exact_conditional_distribution
from sparse_cmi.models import Stratum
from sparse_cmi.moments import aggregate_moments
from sparse_cmi.routing import deterministic_pvalue
from sparse_cmi.saddlepoint import FactorizedConditionalCGF


class SaddlepointTests(unittest.TestCase):
    def test_cgf_derivatives_at_zero_match_exact_cumulants(self) -> None:
        strata = [
            Stratum(5, 2, 2, 1),
            Stratum(7, 2, 4, 1),
            Stratum(10, 3, 6, 2),
        ]
        cgf = FactorizedConditionalCGF(strata)
        moments = aggregate_moments(strata)
        k_value, first, second = cgf.evaluate(0.0)
        self.assertAlmostEqual(k_value, 0.0, places=13)
        self.assertAlmostEqual(first, moments.mean, places=12)
        self.assertAlmostEqual(second, moments.variance, places=12)
        self.assertAlmostEqual(
            cgf.third_cumulant,
            moments.third_cumulant,
            places=11,
        )

    def test_identical_cgf_components_are_grouped_exactly(self) -> None:
        strata = [Stratum(10, 5, 5, 2) for _ in range(100)]
        cgf = FactorizedConditionalCGF(strata)
        moments = aggregate_moments(strata)
        self.assertEqual(cgf.component_count, 100)
        self.assertEqual(cgf.unique_component_count, 1)
        k_value, first, second = cgf.evaluate(0.25)
        single = FactorizedConditionalCGF(strata[:1])
        single_k, single_first, single_second = single.evaluate(0.25)
        self.assertAlmostEqual(k_value, 100 * single_k, places=11)
        self.assertAlmostEqual(first, 100 * single_first, places=11)
        self.assertAlmostEqual(second, 100 * single_second, places=11)
        self.assertAlmostEqual(cgf.mean, moments.mean, places=11)
        self.assertAlmostEqual(cgf.variance, moments.variance, places=11)

    def test_left_of_mean_upper_tail_is_large(self) -> None:
        strata = [Stratum(10, 5, 5, 2) for _ in range(20)]
        cgf = FactorizedConditionalCGF(strata)
        statistic = cgf.mean - 1.5 * np.sqrt(cgf.variance)
        result = cgf.upper_tail(float(statistic))
        self.assertTrue(np.isfinite(result.pvalue))
        self.assertGreater(result.pvalue, 0.5)
        self.assertLessEqual(result.pvalue, 1.0)

    def test_valid_left_of_mean_lr_value_is_not_rejected_by_guardrail(self) -> None:
        strata = [Stratum(10, 5, 5, 2) for _ in range(5)]
        cgf = FactorizedConditionalCGF(strata)
        result = cgf.upper_tail(5.465736224491)
        self.assertEqual(result.fallback, "")
        self.assertTrue(np.isfinite(result.pvalue))
        self.assertGreaterEqual(result.pvalue, 0.0)
        self.assertLessEqual(result.pvalue, 1.0)

    def test_upper_endpoint_probability_is_exact(self) -> None:
        strata = [Stratum(5, 2, 2, 1), Stratum(6, 2, 3, 1)]
        cgf = FactorizedConditionalCGF(strata)
        exact = exact_conditional_distribution(strata)
        expected = exact.upper_tail(cgf.support_max)
        result = cgf.upper_tail(cgf.support_max)
        self.assertEqual(result.fallback, "exact_upper_endpoint")
        self.assertAlmostEqual(result.pvalue, expected, places=13)

    def test_pvalues_are_finite_bounded_and_monotone(self) -> None:
        strata = [Stratum(10, 3, 6, 2) for _ in range(20)]
        cgf = FactorizedConditionalCGF(strata)
        grid = np.linspace(cgf.support_min, cgf.support_max, 101)
        pvalues = cgf.upper_tail_array(grid)
        self.assertTrue(np.all(np.isfinite(pvalues)))
        self.assertTrue(np.all((pvalues >= 0.0) & (pvalues <= 1.0)))
        self.assertTrue(np.all(np.diff(pvalues) <= 1e-9))

    def test_positive_constant_null_returns_one(self) -> None:
        cgf = FactorizedConditionalCGF([Stratum(10, 1, 5, 0)])
        self.assertEqual(cgf.variance, 0.0)
        self.assertEqual(cgf.upper_tail(cgf.mean).pvalue, 1.0)

    def test_deterministic_router_uses_exact_for_small_support(self) -> None:
        strata = [Stratum(5, 2, 2, 2) for _ in range(5)]
        result = deterministic_pvalue(strata)
        self.assertEqual(result.route, "exact_convolution")
        self.assertIsNotNone(result.exact_state_count)
        self.assertIsNone(result.saddlepoint)

    def test_router_uses_exact_for_many_repeated_low_support_strata(self) -> None:
        strata = [Stratum(10, 5, 5, 2) for _ in range(20)]
        result = deterministic_pvalue(strata)
        self.assertEqual(result.route, "exact_convolution")
        self.assertEqual(result.exact_state_upper_bound, 231)
        self.assertLessEqual(result.exact_transition_upper_bound, 100_000)

    def test_deterministic_router_uses_saddlepoint_for_many_strata(self) -> None:
        strata = [Stratum(30, 15, 15, 8) for _ in range(20)]
        result = deterministic_pvalue(strata)
        self.assertEqual(result.route, "saddlepoint")
        self.assertIsNone(result.exact_state_count)
        self.assertIsNotNone(result.saddlepoint)
        self.assertTrue(0.0 <= result.pvalue <= 1.0)


if __name__ == "__main__":
    unittest.main()
