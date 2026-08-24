from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.stats import chi2

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from welch_differential_mi.likelihood_ratio import (
    _mi_and_logit_gradient,
    _multinomial_nll_and_gradient,
    _softmax_reference,
    constrained_likelihood_ratio_test,
)


def _finite_difference(function, values: np.ndarray, step: float = 1e-6) -> np.ndarray:
    result = np.empty_like(values)
    for index in range(values.size):
        upper = values.copy()
        lower = values.copy()
        upper[index] += step
        lower[index] -= step
        result[index] = (function(upper) - function(lower)) / (2.0 * step)
    return result


class ConstrainedLikelihoodRatioTests(unittest.TestCase):
    def test_analytic_gradients_match_finite_differences(self) -> None:
        logits = np.array([0.4, -0.7, 0.2])
        counts = np.array([17.0, 5.0, 9.0, 31.0])
        _, nll_gradient = _multinomial_nll_and_gradient(logits, counts)
        numerical_nll = _finite_difference(
            lambda value: _multinomial_nll_and_gradient(value, counts)[0], logits
        )
        probability = _softmax_reference(logits)
        _, mi_gradient = _mi_and_logit_gradient(probability, 2, 2)
        numerical_mi = _finite_difference(
            lambda value: _mi_and_logit_gradient(
                _softmax_reference(value), 2, 2
            )[0],
            logits,
        )
        np.testing.assert_allclose(nll_gradient, numerical_nll, rtol=1e-7, atol=1e-7)
        np.testing.assert_allclose(mi_gradient, numerical_mi, rtol=1e-7, atol=1e-8)

    def test_identical_positive_tables_have_zero_statistic(self) -> None:
        table = np.array([[30, 10], [8, 52]])
        result = constrained_likelihood_ratio_test(table, table)
        self.assertTrue(result.converged)
        self.assertLess(result.constraint_residual, 1e-7)
        self.assertLess(result.statistic, 1e-7)
        self.assertAlmostEqual(result.p_value, 1.0, places=7)

    def test_group_swap_and_relabelling_invariance(self) -> None:
        table_p = np.array([[30, 10], [8, 52]])
        table_q = np.array([[12, 8], [19, 41]])
        base = constrained_likelihood_ratio_test(table_p, table_q)
        swapped = constrained_likelihood_ratio_test(table_q, table_p)
        relabelled = constrained_likelihood_ratio_test(
            table_p[::-1, ::-1], table_q[::-1, ::-1]
        )
        for result in (base, swapped, relabelled):
            self.assertTrue(result.converged)
            self.assertLess(result.constraint_residual, 1e-7)
            self.assertGreaterEqual(result.statistic, 0.0)
        self.assertAlmostEqual(base.statistic, swapped.statistic, places=7)
        self.assertAlmostEqual(base.statistic, relabelled.statistic, places=7)
        self.assertAlmostEqual(base.p_value, chi2.sf(base.statistic, 1), places=13)

    def test_scaling_counts_scales_the_likelihood_ratio(self) -> None:
        table_p = np.array([[30, 10], [8, 52]])
        table_q = np.array([[12, 8], [19, 41]])
        base = constrained_likelihood_ratio_test(table_p, table_q)
        scaled = constrained_likelihood_ratio_test(4 * table_p, 4 * table_q)
        self.assertTrue(base.converged and scaled.converged)
        self.assertAlmostEqual(scaled.statistic, 4.0 * base.statistic, places=5)

    def test_full_start_set_avoids_sparse_local_optimum(self) -> None:
        table_p = np.array([[988, 5], [7, 0]])
        table_q = np.array([[989, 9], [2, 0]])
        partial = constrained_likelihood_ratio_test(
            table_p, table_q, maximum_starts=3
        )
        full = constrained_likelihood_ratio_test(table_p, table_q)
        self.assertTrue(partial.converged and full.converged)
        self.assertLess(full.statistic, partial.statistic - 0.05)
        self.assertLess(full.constraint_residual, 1e-8)

    def test_invalid_inputs_are_rejected(self) -> None:
        table = np.array([[4, 2], [3, 5]])
        with self.assertRaises(ValueError):
            constrained_likelihood_ratio_test(table, np.ones((3, 3)))
        with self.assertRaises(ValueError):
            constrained_likelihood_ratio_test(table, np.array([[1, -1], [2, 3]]))
        with self.assertRaises(ValueError):
            constrained_likelihood_ratio_test(table, np.array([[1.5, 1], [2, 3]]))


if __name__ == "__main__":
    unittest.main()
