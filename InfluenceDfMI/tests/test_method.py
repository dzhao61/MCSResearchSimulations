"""Correctness tests for the MI-specific influence-df calculation."""

from __future__ import annotations

import unittest

import numpy as np
from numpy.testing import assert_allclose

from influence_df_mi import (
    differential_mi_pvalues,
    influence_df_test,
    variance_functional_influence,
)
from welch_differential_mi import (
    differential_mi_pvalues as legacy_differential_mi_pvalues,
)


class VarianceInfluenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.probability = np.array(
            [
                [0.21, 0.09, 0.10],
                [0.08, 0.18, 0.34],
            ]
        )

    def test_influence_matches_contamination_finite_difference(self) -> None:
        base = variance_functional_influence(self.probability)
        epsilon = 1e-7
        for row in range(self.probability.shape[0]):
            for column in range(self.probability.shape[1]):
                point_mass = np.zeros_like(self.probability)
                point_mass[row, column] = 1.0
                contaminated = (
                    (1.0 - epsilon) * self.probability
                    + epsilon * point_mass
                )
                finite_difference = (
                    variance_functional_influence(contaminated)["variance"]
                    - base["variance"]
                ) / epsilon
                self.assertAlmostEqual(
                    finite_difference,
                    base["influence"][row, column],
                    delta=5e-6,
                )

    def test_influence_has_probability_weighted_mean_zero(self) -> None:
        result = variance_functional_influence(self.probability)
        self.assertAlmostEqual(result["influence_mean"], 0.0, delta=1e-12)
        weighted_mean = np.sum(self.probability * result["influence"])
        self.assertAlmostEqual(weighted_mean, 0.0, delta=1e-12)

    def test_probability_scaling_does_not_change_diagnostics(self) -> None:
        probability = variance_functional_influence(self.probability)
        counts = variance_functional_influence(500.0 * self.probability)
        for key in ("mutual_information", "variance", "influence_variance"):
            self.assertAlmostEqual(probability[key], counts[key], delta=1e-14)
        assert_allclose(probability["influence"], counts["influence"], atol=1e-14)


class DifferentialMethodTests(unittest.TestCase):
    def setUp(self) -> None:
        self.table_p = np.array([[30, 7, 8], [9, 21, 25]])
        self.table_q = np.array([[42, 13, 15], [18, 31, 41]])

    def test_legacy_statistic_and_naive_welch_are_unchanged(self) -> None:
        candidate = differential_mi_pvalues(self.table_p, self.table_q)
        legacy = legacy_differential_mi_pvalues(self.table_p, self.table_q)
        pairs = (
            ("delta_corrected", "delta_corrected"),
            ("influence_variance_p", "influence_variance_p"),
            ("influence_variance_q", "influence_variance_q"),
            ("standard_error", "standard_error"),
            ("statistic", "statistic"),
            ("normal_p_value", "normal_p_value"),
            ("naive_welch_df", "welch_degrees_of_freedom"),
            ("naive_welch_p_value", "welch_p_value"),
        )
        for candidate_key, legacy_key in pairs:
            assert_allclose(
                candidate[candidate_key],
                legacy[legacy_key],
                rtol=0.0,
                atol=0.0,
            )
        self.assertEqual(bool(candidate["valid"]), bool(legacy["valid"]))

    def test_combined_df_matches_component_satterthwaite_formula(self) -> None:
        result = differential_mi_pvalues(self.table_p, self.table_q)
        a = float(result["variance_component_p"])
        b = float(result["variance_component_q"])
        component_formula = (a + b) ** 2 / (
            a**2 / float(result["component_df_p"])
            + b**2 / float(result["component_df_q"])
        )
        self.assertAlmostEqual(
            float(result["influence_welch_df"]),
            component_formula,
            delta=1e-12,
        )

    def test_scalar_and_batch_apis_agree(self) -> None:
        scalar = influence_df_test(self.table_p, self.table_q)
        batch_p = np.stack([self.table_p, 2 * self.table_p])
        batch_q = np.stack([self.table_q, 2 * self.table_q])
        batch = differential_mi_pvalues(batch_p, batch_q)
        for key in (
            "delta_corrected",
            "standard_error",
            "statistic",
            "normal_p_value",
            "naive_welch_df",
            "naive_welch_p_value",
            "influence_welch_df",
            "influence_welch_p_value",
        ):
            scalar_value = getattr(scalar, key)
            self.assertAlmostEqual(scalar_value, float(batch[key][0]), delta=1e-14)

    def test_group_swap_and_category_relabelling_are_invariant(self) -> None:
        original = differential_mi_pvalues(self.table_p, self.table_q)
        swapped = differential_mi_pvalues(self.table_q, self.table_p)
        relabelled = differential_mi_pvalues(
            self.table_p[::-1, ::-1],
            self.table_q[::-1, ::-1],
        )
        self.assertAlmostEqual(
            float(original["statistic"]),
            -float(swapped["statistic"]),
            delta=1e-14,
        )
        for key in (
            "standard_error",
            "normal_p_value",
            "naive_welch_df",
            "naive_welch_p_value",
            "influence_welch_df",
            "influence_welch_p_value",
        ):
            self.assertAlmostEqual(
                float(original[key]),
                float(swapped[key]),
                delta=1e-12,
            )
            self.assertAlmostEqual(
                float(original[key]),
                float(relabelled[key]),
                delta=1e-12,
            )

    def test_large_sample_reference_converges_to_normal(self) -> None:
        result = differential_mi_pvalues(
            10_000 * self.table_p,
            10_000 * self.table_q,
        )
        self.assertGreater(float(result["influence_welch_df"]), 100_000)
        self.assertAlmostEqual(
            float(result["influence_welch_p_value"]),
            float(result["normal_p_value"]),
            delta=1e-5,
        )

    def test_exact_independence_is_marked_first_order_invalid(self) -> None:
        independent = np.array([[25, 25], [25, 25]])
        result = differential_mi_pvalues(independent, independent)
        self.assertFalse(bool(result["valid"]))
        self.assertTrue(np.isnan(result["influence_welch_p_value"]))
        self.assertTrue(np.isnan(result["normal_p_value"]))

    def test_valid_p_values_are_probabilities(self) -> None:
        rng = np.random.default_rng(8231)
        probability_p = np.array([0.20, 0.05, 0.08, 0.17, 0.10, 0.40])
        probability_q = np.array([0.18, 0.08, 0.04, 0.20, 0.16, 0.34])
        tables_p = rng.multinomial(500, probability_p, size=100).reshape(100, 2, 3)
        tables_q = rng.multinomial(700, probability_q, size=100).reshape(100, 2, 3)
        result = differential_mi_pvalues(tables_p, tables_q)
        self.assertTrue(np.all(result["valid"]))
        for key in (
            "normal_p_value",
            "naive_welch_p_value",
            "influence_welch_p_value",
        ):
            self.assertTrue(np.all((result[key] >= 0.0) & (result[key] <= 1.0)))

    def test_malformed_tables_are_rejected(self) -> None:
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
