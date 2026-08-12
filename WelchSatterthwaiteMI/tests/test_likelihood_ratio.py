from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

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


class ConstrainedLikelihoodRatioTests(unittest.TestCase):
    def test_analytic_gradients_match_finite_differences(self) -> None:
        logits = np.array([0.4, -0.7, 0.2, -0.3, 0.5])
        counts = np.array([12.0, 4.0, 8.0, 5.0, 10.0, 6.0])
        epsilon = 1e-6
        objective, objective_gradient, probability = (
            _multinomial_nll_and_gradient(logits, counts)
        )
        mi, mi_gradient = _mi_and_logit_gradient(probability, 2, 3)
        numerical_objective = np.empty_like(logits)
        numerical_mi = np.empty_like(logits)
        for index in range(logits.size):
            direction = np.zeros_like(logits)
            direction[index] = epsilon
            plus_objective = _multinomial_nll_and_gradient(
                logits + direction,
                counts,
            )[0]
            minus_objective = _multinomial_nll_and_gradient(
                logits - direction,
                counts,
            )[0]
            numerical_objective[index] = (
                plus_objective - minus_objective
            ) / (2.0 * epsilon)
            plus_probability = _softmax_reference(logits + direction)
            minus_probability = _softmax_reference(logits - direction)
            plus_mi = _mi_and_logit_gradient(plus_probability, 2, 3)[0]
            minus_mi = _mi_and_logit_gradient(minus_probability, 2, 3)[0]
            numerical_mi[index] = (plus_mi - minus_mi) / (2.0 * epsilon)
        self.assertTrue(np.isfinite(objective))
        self.assertTrue(np.isfinite(mi))
        np.testing.assert_allclose(
            objective_gradient,
            numerical_objective,
            rtol=1e-7,
            atol=1e-7,
        )
        np.testing.assert_allclose(
            mi_gradient,
            numerical_mi,
            rtol=1e-7,
            atol=1e-7,
        )

    def test_identical_positive_tables_have_zero_statistic(self) -> None:
        table = np.array([[18, 4], [6, 22]])
        result = constrained_likelihood_ratio_test(table, table)
        self.assertTrue(result.converged)
        self.assertLess(result.constraint_residual, 1e-9)
        self.assertLess(result.statistic, 1e-8)
        self.assertAlmostEqual(result.p_value, 1.0, places=6)

    def test_group_swap_and_relabelling_invariance(self) -> None:
        p = np.array([[38, 8, 4], [7, 25, 8], [4, 9, 17]])
        q = np.array([[55, 4, 6], [10, 37, 13], [6, 16, 33]])
        baseline = constrained_likelihood_ratio_test(p, q)
        swapped = constrained_likelihood_ratio_test(q, p)
        relabelled = constrained_likelihood_ratio_test(
            p[np.ix_([2, 0, 1], [1, 2, 0])],
            q[np.ix_([2, 0, 1], [1, 2, 0])],
        )
        for result in (baseline, swapped, relabelled):
            self.assertTrue(result.converged)
            self.assertLess(result.constraint_residual, 1e-8)
            self.assertGreaterEqual(result.statistic, 0.0)
        self.assertAlmostEqual(baseline.statistic, swapped.statistic, places=7)
        self.assertAlmostEqual(baseline.p_value, swapped.p_value, places=7)
        self.assertAlmostEqual(baseline.statistic, relabelled.statistic, places=7)
        self.assertAlmostEqual(baseline.p_value, relabelled.p_value, places=7)

    def test_invalid_inputs_are_rejected(self) -> None:
        valid = np.array([[4, 3], [2, 5]])
        with self.assertRaises(ValueError):
            constrained_likelihood_ratio_test(valid, np.ones((2, 3)))
        with self.assertRaises(ValueError):
            constrained_likelihood_ratio_test(valid + 0.5, valid)


if __name__ == "__main__":
    unittest.main()
