"""Correctness tests for joint studentized Edgeworth MI inference."""

from __future__ import annotations

import unittest

import numpy as np
from numpy.testing import assert_allclose
from scipy.stats import norm

from influence_df_mi import differential_mi_pvalues as base_mi_pvalues
from joint_edgeworth_mi import (
    differential_mi_pvalues,
    joint_edgeworth_test,
    studentized_edgeworth_cdf,
)
from joint_edgeworth_mi.method import _joint_influence_moments


class InfluenceMomentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.probability = np.array(
            [
                [0.21, 0.09, 0.10],
                [0.08, 0.18, 0.34],
            ]
        )

    def test_both_influence_functions_match_finite_differences(self) -> None:
        base = _joint_influence_moments(self.probability)
        epsilon = 1e-7
        for row in range(self.probability.shape[0]):
            for column in range(self.probability.shape[1]):
                point_mass = np.zeros_like(self.probability)
                point_mass[row, column] = 1.0
                contaminated = (
                    (1.0 - epsilon) * self.probability
                    + epsilon * point_mass
                )
                changed = _joint_influence_moments(contaminated)
                mi_difference = (
                    changed["mutual_information"]
                    - base["mutual_information"]
                ) / epsilon
                variance_difference = (
                    changed["variance"] - base["variance"]
                ) / epsilon
                self.assertAlmostEqual(
                    mi_difference,
                    base["mi_influence"][row, column],
                    delta=5e-6,
                )
                self.assertAlmostEqual(
                    variance_difference,
                    base["variance_influence"][row, column],
                    delta=5e-6,
                )

    def test_influence_means_and_cross_moments(self) -> None:
        result = _joint_influence_moments(self.probability)
        self.assertAlmostEqual(result["mi_influence_mean"], 0.0, delta=1e-12)
        self.assertAlmostEqual(
            result["variance_influence_mean"],
            0.0,
            delta=1e-12,
        )
        direct_third = np.sum(
            self.probability * result["mi_influence"] ** 3
        )
        direct_covariance = np.sum(
            self.probability
            * result["mi_influence"]
            * result["variance_influence"]
        )
        self.assertAlmostEqual(
            result["third_moment"],
            direct_third,
            delta=1e-14,
        )
        self.assertAlmostEqual(
            result["covariance"],
            direct_covariance,
            delta=1e-14,
        )

    def test_probability_scaling_does_not_change_moments(self) -> None:
        probability = _joint_influence_moments(self.probability)
        counts = _joint_influence_moments(1000.0 * self.probability)
        for key in (
            "mutual_information",
            "variance",
            "third_moment",
            "covariance",
        ):
            self.assertAlmostEqual(probability[key], counts[key], delta=1e-14)


class EdgeworthFormulaTests(unittest.TestCase):
    def test_studentized_mean_special_case(self) -> None:
        skew = 0.1
        grid = np.linspace(-2.5, 2.5, 31)
        result = studentized_edgeworth_cdf(grid, skew, skew)
        expected_polynomial = skew * (1.0 + 2.0 * grid**2) / 6.0
        assert_allclose(
            result["correction"],
            norm.pdf(grid) * expected_polynomial,
            rtol=1e-14,
            atol=1e-15,
        )
        self.assertTrue(np.all(result["valid"]))

    def test_zero_cumulants_recover_normal_exactly(self) -> None:
        grid = np.linspace(-3.0, 3.0, 51)
        result = studentized_edgeworth_cdf(grid, 0.0, 0.0)
        assert_allclose(result["cdf"], norm.cdf(grid), rtol=0.0, atol=0.0)
        assert_allclose(
            result["p_value"],
            2.0 * norm.sf(np.abs(grid)),
            rtol=0.0,
            atol=2e-16,
        )

    def test_invalid_local_cdf_is_not_silently_clipped(self) -> None:
        result = studentized_edgeworth_cdf(3.0, 1.0, 1.0)
        self.assertFalse(result["valid"])
        self.assertTrue(np.isnan(result["cdf"]))
        self.assertTrue(np.isnan(result["p_value"]))


class DifferentialMethodTests(unittest.TestCase):
    def setUp(self) -> None:
        self.table_p = np.array([[30, 7, 8], [9, 21, 25]])
        self.table_q = np.array([[42, 13, 15], [18, 31, 41]])

    def test_all_comparators_are_exactly_unchanged(self) -> None:
        candidate = differential_mi_pvalues(self.table_p, self.table_q)
        base = base_mi_pvalues(self.table_p, self.table_q)
        keys = (
            "delta_corrected",
            "influence_variance_p",
            "influence_variance_q",
            "standard_error",
            "statistic",
            "normal_p_value",
            "naive_welch_df",
            "naive_welch_p_value",
            "influence_welch_df",
            "influence_welch_p_value",
        )
        for key in keys:
            assert_allclose(candidate[key], base[key], rtol=0.0, atol=0.0)
        self.assertEqual(
            bool(candidate["base_valid"]),
            bool(base["valid"]),
        )

    def test_group_swap_and_category_relabelling_are_invariant(self) -> None:
        original = differential_mi_pvalues(self.table_p, self.table_q)
        swapped = differential_mi_pvalues(self.table_q, self.table_p)
        relabelled = differential_mi_pvalues(
            self.table_p[::-1, ::-1],
            self.table_q[::-1, ::-1],
        )
        signed_keys = (
            "statistic",
            "numerator_third_cumulant",
            "numerator_variance_covariance",
            "standardized_third_cumulant",
            "standardized_variance_covariance",
        )
        for key in signed_keys:
            self.assertAlmostEqual(
                float(original[key]),
                -float(swapped[key]),
                delta=1e-13,
            )
        invariant_keys = (
            "standard_error",
            "normal_p_value",
            "naive_welch_p_value",
            "influence_welch_p_value",
            "edgeworth_p_value",
        )
        for key in invariant_keys:
            self.assertAlmostEqual(
                float(original[key]),
                float(swapped[key]),
                delta=1e-13,
            )
            self.assertAlmostEqual(
                float(original[key]),
                float(relabelled[key]),
                delta=1e-13,
            )

    def test_identical_tables_with_equal_n_recover_normal(self) -> None:
        result = differential_mi_pvalues(self.table_p, self.table_p)
        self.assertAlmostEqual(
            float(result["standardized_third_cumulant"]),
            0.0,
            delta=1e-15,
        )
        self.assertAlmostEqual(
            float(result["standardized_variance_covariance"]),
            0.0,
            delta=1e-15,
        )
        self.assertEqual(
            float(result["edgeworth_p_value"]),
            float(result["normal_p_value"]),
        )

    def test_standardized_corrections_shrink_at_large_n(self) -> None:
        original = differential_mi_pvalues(self.table_p, self.table_q)
        scaled = differential_mi_pvalues(
            100 * self.table_p,
            100 * self.table_q,
        )
        for key in (
            "standardized_third_cumulant",
            "standardized_variance_covariance",
        ):
            self.assertAlmostEqual(
                float(scaled[key]),
                float(original[key]) / 10.0,
                delta=1e-13,
            )

    def test_scalar_and_batch_apis_agree(self) -> None:
        scalar = joint_edgeworth_test(self.table_p, self.table_q)
        batch = differential_mi_pvalues(
            np.stack([self.table_p, 2 * self.table_p]),
            np.stack([self.table_q, 2 * self.table_q]),
        )
        for key in (
            "delta_corrected",
            "standard_error",
            "statistic",
            "normal_p_value",
            "naive_welch_p_value",
            "influence_welch_p_value",
            "standardized_third_cumulant",
            "standardized_variance_covariance",
            "edgeworth_cdf",
            "edgeworth_p_value",
        ):
            self.assertAlmostEqual(
                getattr(scalar, key),
                float(batch[key][0]),
                delta=1e-14,
            )

    def test_valid_p_values_are_probabilities(self) -> None:
        rng = np.random.default_rng(7739)
        probability_p = np.array([0.20, 0.05, 0.08, 0.17, 0.10, 0.40])
        probability_q = np.array([0.18, 0.08, 0.04, 0.20, 0.16, 0.34])
        tables_p = rng.multinomial(500, probability_p, size=200).reshape(200, 2, 3)
        tables_q = rng.multinomial(700, probability_q, size=200).reshape(200, 2, 3)
        result = differential_mi_pvalues(tables_p, tables_q)
        valid = result["edgeworth_valid"]
        self.assertGreater(float(np.mean(valid)), 0.995)
        self.assertTrue(
            np.all(
                (result["edgeworth_p_value"][valid] >= 0.0)
                & (result["edgeworth_p_value"][valid] <= 1.0)
            )
        )

    def test_degenerate_and_malformed_tables_are_rejected(self) -> None:
        independent = np.array([[25, 25], [25, 25]])
        degenerate = differential_mi_pvalues(independent, independent)
        self.assertFalse(bool(degenerate["edgeworth_valid"]))
        self.assertTrue(np.isnan(degenerate["edgeworth_p_value"]))

        invalid_pairs = (
            (np.array([1, 2]), np.array([1, 2])),
            (np.ones((2, 2)), np.ones((3, 2))),
            (np.array([[1, -1], [1, 1]]), np.ones((2, 2))),
            (np.array([[1.5, 1], [1, 1]]), np.ones((2, 2))),
            (np.array([[1, np.nan], [1, 1]]), np.ones((2, 2))),
            (np.array([[1, 0], [0, 0]]), np.ones((2, 2))),
        )
        for table_p, table_q in invalid_pairs:
            with self.subTest(table_p=table_p, table_q=table_q):
                with self.assertRaises(ValueError):
                    differential_mi_pvalues(table_p, table_q)


if __name__ == "__main__":
    unittest.main()
