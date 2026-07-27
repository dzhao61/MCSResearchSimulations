from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.optimize import approx_fprime

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.distributions import (
    marginal_probabilities,
    table_with_target_mi,
)
from profile_differential_mi.profile import (
    _constraint,
    _constraint_gradient,
    _objective,
    _objective_gradient,
    profile_equal_mi_test,
)


class ProfileTests(unittest.TestCase):
    def test_analytic_derivatives_match_finite_differences(self) -> None:
        p = np.array([[19, 5, 3], [4, 14, 7]])
        q = np.array([[31, 7, 5], [6, 18, 9]])
        rng = np.random.default_rng(11)
        parameters = rng.normal(scale=0.7, size=2 * (p.size - 1))
        numeric_objective = approx_fprime(
            parameters, lambda value: _objective(value, p, q), 1e-7
        )
        analytic_objective = _objective_gradient(parameters, p, q)
        np.testing.assert_allclose(
            analytic_objective, numeric_objective, atol=2e-5, rtol=2e-5
        )
        numeric_constraint = approx_fprime(
            parameters, lambda value: _constraint(value, p.shape), 1e-7
        )
        analytic_constraint = _constraint_gradient(parameters, p.shape)
        np.testing.assert_allclose(
            analytic_constraint, numeric_constraint, atol=2e-7, rtol=2e-5
        )

    def test_equal_tables_give_zero_statistics(self) -> None:
        table = np.array([[30, 8, 3], [6, 25, 5], [2, 7, 20]])
        result = profile_equal_mi_test(table, table)
        self.assertTrue(result.trustworthy)
        self.assertLess(result.constraint_residual, 1e-9)
        self.assertLess(result.lr_statistic, 1e-8)
        self.assertLess(result.pearson_statistic, 1e-8)
        self.assertLess(result.cr_2_3_statistic, 1e-8)
        self.assertGreater(result.lr_p_value, 0.999)

    def test_fit_respects_constraint_and_likelihood_order(self) -> None:
        p = np.array([[38, 8, 4], [7, 25, 8], [4, 9, 17]])
        q = np.array([[55, 4, 6], [10, 37, 13], [6, 16, 33]])
        result = profile_equal_mi_test(p, q)
        self.assertTrue(result.trustworthy, result.optimizer_message)
        self.assertLess(result.constraint_residual, 2e-7)
        self.assertGreaterEqual(result.likelihood_gap, -1e-7)
        for value in (
            result.lr_p_value,
            result.pearson_p_value,
            result.cr_2_3_p_value,
        ):
            self.assertTrue(np.isfinite(value))
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_invariant_to_group_swap_and_category_relabelling(self) -> None:
        p = np.array([[38, 8, 4], [7, 25, 8], [4, 9, 17]])
        q = np.array([[55, 4, 6], [10, 37, 13], [6, 16, 33]])
        baseline = profile_equal_mi_test(p, q)
        swapped = profile_equal_mi_test(q, p)
        row_order = [2, 0, 1]
        column_order = [1, 2, 0]
        relabelled = profile_equal_mi_test(
            p[np.ix_(row_order, column_order)],
            q[np.ix_(row_order, column_order)],
        )
        self.assertTrue(baseline.trustworthy)
        self.assertTrue(swapped.trustworthy)
        self.assertTrue(relabelled.trustworthy)
        for name in ("lr_statistic", "pearson_statistic", "cr_2_3_statistic"):
            self.assertAlmostEqual(
                getattr(baseline, name), getattr(swapped, name), places=7
            )
            self.assertAlmostEqual(
                getattr(baseline, name), getattr(relabelled, name), places=7
            )

    def test_sparse_zero_cell_tables_are_explicitly_supported(self) -> None:
        p = np.array([[18, 0, 1], [0, 7, 0], [2, 0, 3]])
        q = np.array([[35, 1, 0], [2, 13, 1], [0, 1, 6]])
        result = profile_equal_mi_test(p, q)
        self.assertTrue(np.isfinite(result.lr_statistic))
        self.assertTrue(np.isfinite(result.constraint_residual))
        self.assertGreater(result.minimum_fitted_probability, 0)

    def test_sparse_statistics_are_stable_across_logit_bounds(self) -> None:
        p = np.array([[28, 0, 2], [1, 16, 0], [0, 2, 7]])
        q = np.array([[54, 2, 0], [3, 29, 2], [0, 4, 13]])
        lower = profile_equal_mi_test(p, q, logit_bound=24.0)
        upper = profile_equal_mi_test(p, q, logit_bound=36.0)
        self.assertTrue(lower.trustworthy)
        self.assertTrue(upper.trustworthy)
        for name in ("lr_statistic", "pearson_statistic", "cr_2_3_statistic"):
            self.assertAlmostEqual(
                getattr(lower, name), getattr(upper, name), places=6
            )

    def test_population_equal_mi_pair_has_feasible_profile_fit(self) -> None:
        balanced = marginal_probabilities(3, "balanced")
        skewed = marginal_probabilities(3, "mild")
        probability_p, _ = table_with_target_mi(balanced, balanced, 0.08)
        probability_q, _ = table_with_target_mi(skewed, skewed, 0.08)
        p = np.rint(10_000 * probability_p).astype(int)
        q = np.rint(10_000 * probability_q).astype(int)
        result = profile_equal_mi_test(p, q)
        self.assertTrue(result.trustworthy, result.optimizer_message)
        self.assertLess(result.constraint_residual, 2e-7)

    def test_invalid_inputs_are_rejected(self) -> None:
        valid = np.array([[3, 2], [1, 4]])
        with self.assertRaises(ValueError):
            profile_equal_mi_test(valid, np.ones((2, 3), dtype=int))
        with self.assertRaises(ValueError):
            profile_equal_mi_test(valid.astype(float) + 0.5, valid)
        with self.assertRaises(ValueError):
            profile_equal_mi_test(valid, valid, pseudocount=0)


if __name__ == "__main__":
    unittest.main()
