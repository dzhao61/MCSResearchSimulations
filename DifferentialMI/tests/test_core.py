from __future__ import annotations

import unittest
import sys
from pathlib import Path

import numpy as np
from scipy.stats import multivariate_hypergeom

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.distributions import (
    association_table,
    association_table_from_interaction,
    marginal_probabilities,
    mutual_information_probability,
    random_interaction_pattern,
    table_with_target_mi,
    table_with_target_mi_from_interaction,
)
from differential_mi.inference import (
    _build_influence_cgf,
    analytic_wald_test,
    compare_tables,
    influence_saddlepoint_test,
)
from differential_mi.statistics import (
    analytic_bias_corrected_mi,
    influence_variance,
    jackknife_mi,
    plugin_mi,
)


def brute_force_jackknife_mi(table: np.ndarray) -> float:
    estimate = float(plugin_mi(table))
    leave_one_out = []
    for row, column in zip(*np.nonzero(table)):
        reduced = table.copy()
        reduced[row, column] -= 1
        leave_one_out.extend(
            [float(plugin_mi(reduced))] * int(table[row, column])
        )
    n = int(table.sum())
    return n * estimate - (n - 1) * float(np.mean(leave_one_out))


class CoreTests(unittest.TestCase):
    def test_known_mi_tables(self) -> None:
        independent = np.array([[25, 25], [25, 25]])
        diagonal = np.array([[50, 0], [0, 50]])
        self.assertLess(abs(plugin_mi(independent)), 1e-14)
        self.assertLess(abs(plugin_mi(diagonal) - np.log(2.0)), 1e-14)

    def test_association_table_preserves_margins(self) -> None:
        row = marginal_probabilities(5, "strong")
        col = marginal_probabilities(3, "mild")
        table = association_table(row, col, 2.0)
        np.testing.assert_allclose(table.sum(axis=1), row, atol=1e-12)
        np.testing.assert_allclose(table.sum(axis=0), col, atol=1e-12)
        self.assertTrue(np.all(table > 0))
        cyclic = association_table(row, col, 1.5, pattern="cyclic")
        np.testing.assert_allclose(cyclic.sum(axis=1), row, atol=1e-12)
        np.testing.assert_allclose(cyclic.sum(axis=0), col, atol=1e-12)

    def test_equal_mi_solver(self) -> None:
        balanced = marginal_probabilities(3, "balanced")
        strong = marginal_probabilities(3, "strong")
        p, _ = table_with_target_mi(balanced, balanced, 0.08)
        q, _ = table_with_target_mi(strong, strong, 0.08)
        self.assertGreater(np.abs(p - q).sum(), 0.5)
        self.assertLess(abs(mutual_information_probability(p) - 0.08), 1e-10)
        self.assertLess(abs(mutual_information_probability(q) - 0.08), 1e-10)

    def test_random_interaction_equal_mi_solver(self) -> None:
        rng = np.random.default_rng(19)
        row = rng.dirichlet(np.full(4, 2.0))
        col = rng.dirichlet(np.full(6, 1.0))
        interaction = random_interaction_pattern(4, 6, rng)
        table = association_table_from_interaction(row, col, 0.8, interaction)
        np.testing.assert_allclose(table.sum(axis=1), row, atol=1e-12)
        np.testing.assert_allclose(table.sum(axis=0), col, atol=1e-12)
        solved, _ = table_with_target_mi_from_interaction(
            row, col, 0.05, interaction
        )
        self.assertLess(abs(mutual_information_probability(solved) - 0.05), 1e-10)

    def test_analytic_bias_correction(self) -> None:
        table = np.array([[20, 5, 4], [3, 10, 8]])
        expected = plugin_mi(table) - (2 - 1) * (3 - 1) / (2 * table.sum())
        self.assertLess(abs(analytic_bias_corrected_mi(table) - expected), 1e-14)
        batch = np.stack([table, table + 1])
        expected_batch = plugin_mi(batch) - 1.0 / batch.sum(axis=(1, 2))
        np.testing.assert_allclose(
            analytic_bias_corrected_mi(batch), expected_batch, atol=1e-14
        )

    def test_influence_function_matches_contamination_derivative(self) -> None:
        margin = marginal_probabilities(3, "mild")
        probability, _ = table_with_target_mi(margin, margin, 0.10)
        row, column = 0, 1
        baseline = mutual_information_probability(probability)
        influence = (
            np.log(
                probability[row, column]
                / (probability[row].sum() * probability[:, column].sum())
            )
            - baseline
        )
        epsilon = 1e-7
        contaminated = (1.0 - epsilon) * probability
        contaminated[row, column] += epsilon
        derivative = (
            mutual_information_probability(contaminated) - baseline
        ) / epsilon
        self.assertLess(abs(derivative - influence), 2e-5)

    def test_influence_variance_matches_multinomial_delta_method(self) -> None:
        rng = np.random.default_rng(29)
        probability = rng.dirichlet(np.full(12, 2.0)).reshape(3, 4)
        row = probability.sum(axis=1)
        col = probability.sum(axis=0)
        gradient = (
            np.log(probability)
            - np.log(row)[:, None]
            - np.log(col)[None, :]
            - 1.0
        ).reshape(-1)
        flat = probability.reshape(-1)
        multinomial_covariance = np.diag(flat) - np.outer(flat, flat)
        delta_variance = float(
            gradient @ multinomial_covariance @ gradient
        )
        self.assertLess(
            abs(delta_variance - influence_variance(probability)), 1e-12
        )

    def test_mi_hessian_implies_classical_leading_bias(self) -> None:
        rng = np.random.default_rng(31)
        probability = rng.dirichlet(np.full(12, 3.0)).reshape(3, 4)
        flat = probability.reshape(-1)
        covariance = np.diag(flat) - np.outer(flat, flat)
        row = probability.sum(axis=1)
        col = probability.sum(axis=0)
        hessian = np.zeros((flat.size, flat.size))
        for i in range(probability.shape[0]):
            for j in range(probability.shape[1]):
                first = i * probability.shape[1] + j
                for k in range(probability.shape[0]):
                    for ell in range(probability.shape[1]):
                        second = k * probability.shape[1] + ell
                        hessian[first, second] = (
                            (1.0 / probability[i, j] if first == second else 0.0)
                            - (1.0 / row[i] if i == k else 0.0)
                            - (1.0 / col[j] if j == ell else 0.0)
                        )
        second_order_bias_coefficient = 0.5 * float(
            np.sum(hessian * covariance)
        )
        expected = 0.5 * (probability.shape[0] - 1) * (
            probability.shape[1] - 1
        )
        self.assertLess(abs(second_order_bias_coefficient - expected), 1e-12)

    def test_influence_variance_is_zero_at_exact_independence(self) -> None:
        table = np.array([[10, 20], [20, 40]])
        self.assertLess(influence_variance(table), 1e-14)

    def test_vectorized_jackknife_matches_literal_leave_one_out(self) -> None:
        table = np.array([[8, 3, 1], [2, 6, 4]])
        self.assertLess(
            abs(jackknife_mi(table) - brute_force_jackknife_mi(table)), 1e-12
        )
        batch = np.stack([table, table + 1])
        vectorized = jackknife_mi(batch)
        expected = np.array([brute_force_jackknife_mi(item) for item in batch])
        np.testing.assert_allclose(vectorized, expected, atol=1e-12)

    def test_permutation_comparison_returns_valid_probabilities(self) -> None:
        p = np.array([[30, 10], [10, 50]])
        q = np.array([[60, 5], [15, 20]])
        result = compare_tables(p, q, permutations=99, rng=np.random.default_rng(7))
        for value in (
            result.naive_perm_plugin_p,
            result.student_perm_plugin_p,
            result.student_perm_analytic_p,
            result.student_perm_jackknife_p,
            result.wald_plugin_p,
            result.wald_analytic_p,
            result.wald_jackknife_p,
        ):
            self.assertTrue(np.isfinite(value))
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)
        self.assertGreater(result.standard_error, 0)
        self.assertGreaterEqual(result.pooled_mi_plugin, 0)
        self.assertGreaterEqual(result.pooled_influence_variance, 0)
        with self.assertRaises(ValueError):
            compare_tables(p, q, permutations=0, rng=np.random.default_rng(7))

    def test_primary_analytic_wald_api(self) -> None:
        p = np.array([[30, 10, 5], [10, 35, 10]])
        q = np.array([[80, 10, 5], [20, 60, 25]])
        result = analytic_wald_test(p, q, confidence_level=0.90)
        degrees_of_freedom = (p.shape[0] - 1) * (p.shape[1] - 1)
        self.assertEqual(result.degrees_of_freedom, degrees_of_freedom)
        self.assertAlmostEqual(
            result.mi_p_corrected,
            plugin_mi(p) - degrees_of_freedom / (2 * p.sum()),
        )
        self.assertAlmostEqual(
            result.delta_corrected,
            result.mi_p_corrected - result.mi_q_corrected,
        )
        self.assertTrue(result.valid_first_order_calculation)
        self.assertGreaterEqual(result.p_value, 0)
        self.assertLessEqual(result.p_value, 1)
        self.assertLess(
            result.confidence_interval_low, result.confidence_interval_high
        )
        self.assertEqual(result.confidence_level, 0.90)

    def test_primary_wald_is_invariant_to_category_relabelling(self) -> None:
        p = np.array([[12, 5, 3], [4, 18, 8], [7, 2, 11]])
        q = np.array([[20, 4, 6], [3, 15, 12], [8, 5, 7]])
        baseline = analytic_wald_test(p, q)
        row_order = [2, 0, 1]
        column_order = [1, 2, 0]
        relabelled = analytic_wald_test(
            p[np.ix_(row_order, column_order)],
            q[np.ix_(row_order, column_order)],
        )
        self.assertAlmostEqual(baseline.delta_corrected, relabelled.delta_corrected)
        self.assertAlmostEqual(baseline.standard_error, relabelled.standard_error)
        self.assertAlmostEqual(baseline.p_value, relabelled.p_value)

    def test_primary_wald_is_invariant_to_group_swap(self) -> None:
        p = np.array([[30, 10, 5], [10, 35, 10]])
        q = np.array([[80, 10, 5], [20, 60, 25]])
        baseline = analytic_wald_test(p, q)
        swapped = analytic_wald_test(q, p)
        self.assertAlmostEqual(baseline.delta_corrected, -swapped.delta_corrected)
        self.assertAlmostEqual(baseline.standard_error, swapped.standard_error)
        self.assertAlmostEqual(baseline.p_value, swapped.p_value)
        self.assertTrue(baseline.numerically_computable)

    def test_primary_wald_rejects_invalid_inputs(self) -> None:
        valid = np.array([[3, 2], [1, 4]])
        with self.assertRaises(ValueError):
            analytic_wald_test(valid, np.ones((2, 3), dtype=int))
        with self.assertRaises(ValueError):
            analytic_wald_test(valid, valid, confidence_level=1.0)
        with self.assertRaises(ValueError):
            analytic_wald_test(valid.astype(float) + 0.5, valid)
        with self.assertRaises(ValueError):
            analytic_wald_test(
                np.array([[3.0, np.nan], [1.0, 4.0]]), valid
            )
        with self.assertRaises(ValueError):
            analytic_wald_test(valid.astype(complex) + 1j, valid)
        with self.assertRaises(ValueError):
            analytic_wald_test(np.array([[3, 2, 1]]), np.array([[4, 1, 1]]))

    def test_influence_cgf_matches_wald_first_two_cumulants(self) -> None:
        p = np.array([[30, 10, 5], [10, 35, 10]])
        q = np.array([[80, 10, 5], [20, 60, 25]])
        cgf = _build_influence_cgf(p, q, int(p.sum()), int(q.sum()))
        value, first, second = cgf.evaluate(0.0)
        expected = influence_variance(p) / p.sum() + influence_variance(q) / q.sum()
        self.assertLess(abs(value), 1e-12)
        self.assertLess(abs(first), 1e-12)
        self.assertLess(abs(second - expected), 1e-12)

    def test_influence_saddlepoint_is_finite_and_invariant(self) -> None:
        p = np.array([[12, 5, 3], [4, 18, 8], [7, 2, 11]])
        q = np.array([[20, 4, 6], [3, 15, 12], [8, 5, 7]])
        baseline = influence_saddlepoint_test(p, q)
        swapped = influence_saddlepoint_test(q, p)
        relabelled = influence_saddlepoint_test(
            p[np.ix_([2, 0, 1], [1, 2, 0])],
            q[np.ix_([2, 0, 1], [1, 2, 0])],
        )
        self.assertTrue(baseline.valid_first_order_calculation)
        self.assertTrue(np.isfinite(baseline.saddlepoint_p_value))
        self.assertGreaterEqual(baseline.saddlepoint_p_value, 0.0)
        self.assertLessEqual(baseline.saddlepoint_p_value, 1.0)
        self.assertAlmostEqual(
            baseline.saddlepoint_p_value, swapped.saddlepoint_p_value
        )
        self.assertAlmostEqual(
            baseline.saddlepoint_p_value, relabelled.saddlepoint_p_value
        )
        self.assertAlmostEqual(
            baseline.lower_tail_probability + baseline.upper_tail_probability,
            1.0,
        )

    def test_influence_saddlepoint_records_near_mean_fallback(self) -> None:
        p = np.array([[30, 8], [7, 25]])
        result = influence_saddlepoint_test(p, p)
        self.assertEqual(result.route, "normal_near_mean")
        self.assertAlmostEqual(result.saddlepoint_p_value, 1.0)

    def test_influence_saddlepoint_near_mean_regression(self) -> None:
        p = np.array([[300, 120, 80], [100, 250, 150], [50, 170, 280]])
        q = np.array([[300, 119, 80], [101, 250, 150], [50, 170, 280]])
        result = influence_saddlepoint_test(p, q)
        self.assertEqual(result.route, "normal_near_mean")
        self.assertAlmostEqual(result.saddlepoint_p_value, result.wald_p_value)
        self.assertGreater(result.saddlepoint_p_value, 0.99)

    def test_influence_saddlepoint_rejects_invalid_option(self) -> None:
        table = np.array([[30, 8], [7, 25]])
        with self.assertRaises(ValueError):
            influence_saddlepoint_test(table, table, near_mean_z=0.0)

    def test_table_permutation_probabilities_equal_label_counts(self) -> None:
        pooled = np.array([2, 1, 1])
        possible = np.array(
            [
                [2, 0, 0],
                [1, 1, 0],
                [1, 0, 1],
                [0, 1, 1],
            ]
        )
        # The four count tables arise from 1, 2, 2, and 1 of the six possible
        # choices of two individually labelled observations.
        label_permutation_probabilities = np.array([1, 2, 2, 1]) / 6
        table_probabilities = multivariate_hypergeom.pmf(
            possible, m=pooled, n=2
        )
        np.testing.assert_allclose(
            table_probabilities, label_permutation_probabilities, atol=1e-14
        )


if __name__ == "__main__":
    unittest.main()
