from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.inference import analytic_wald_test
from welch_differential_mi.welch import (
    _welch_df,
    differential_mi_pvalues,
    welch_satterthwaite_test,
)


class WelchTests(unittest.TestCase):
    def test_normal_component_matches_frozen_wald(self) -> None:
        p = np.array([[30, 10, 5], [10, 35, 10]])
        q = np.array([[80, 10, 5], [20, 60, 25]])
        expected = analytic_wald_test(p, q)
        result = welch_satterthwaite_test(p, q)
        self.assertAlmostEqual(result.delta_corrected, expected.delta_corrected)
        self.assertAlmostEqual(result.standard_error, expected.standard_error)
        self.assertAlmostEqual(result.statistic, expected.z_statistic)
        self.assertAlmostEqual(result.normal_p_value, expected.p_value)

    def test_equal_contributions_recover_pooled_degrees_of_freedom(self) -> None:
        n = np.asarray(50.0)
        result = _welch_df(
            np.asarray(0.2),
            np.asarray(0.2),
            n,
            n,
        )
        self.assertAlmostEqual(float(result), 2.0 * (n - 1.0))

    def test_finite_df_p_value_is_not_smaller_than_normal(self) -> None:
        p = np.array([[18, 2], [3, 17]])
        q = np.array([[60, 5], [8, 47]])
        result = welch_satterthwaite_test(p, q)
        self.assertTrue(result.valid)
        self.assertGreaterEqual(result.welch_p_value, result.normal_p_value)
        self.assertGreaterEqual(
            result.unbiased_welch_p_value,
            result.normal_p_value,
        )
        self.assertTrue(result.expanded_valid)
        self.assertGreaterEqual(
            result.expanded_welch_p_value,
            result.normal_p_value,
        )

    def test_method_validity_is_separate_at_unstable_support(self) -> None:
        # Both tables have well-defined, positive first-order MI variance, but
        # q's checkerboard zero pattern makes its variance-of-variance
        # (the expanded-method component df) degenerate.
        p = np.array([[13, 2, 6], [0, 13, 11]])
        q = np.array([[0, 13, 13], [13, 0, 13]])
        values = differential_mi_pvalues(p, q)
        self.assertGreater(float(values["influence_variance_p"]), 0.0)
        self.assertGreater(float(values["influence_variance_q"]), 0.0)
        self.assertTrue(values["base_valid"])
        self.assertTrue(values["simple_valid"])
        self.assertFalse(values["expanded_valid"])
        self.assertTrue(np.isfinite(values["normal_p_value"]))
        self.assertTrue(np.isnan(values["expanded_welch_p_value"]))

    def test_group_swap_and_relabelling_invariance(self) -> None:
        p = np.array([[38, 8, 4], [7, 25, 8], [4, 9, 17]])
        q = np.array([[55, 4, 6], [10, 37, 13], [6, 16, 33]])
        baseline = welch_satterthwaite_test(p, q)
        swapped = welch_satterthwaite_test(q, p)
        relabelled = welch_satterthwaite_test(
            p[np.ix_([2, 0, 1], [1, 2, 0])],
            q[np.ix_([2, 0, 1], [1, 2, 0])],
        )
        self.assertAlmostEqual(baseline.delta_corrected, -swapped.delta_corrected)
        for name in (
            "standard_error",
            "welch_degrees_of_freedom",
            "welch_p_value",
            "expanded_welch_degrees_of_freedom",
            "expanded_welch_p_value",
            "unbiased_welch_p_value",
        ):
            self.assertAlmostEqual(getattr(baseline, name), getattr(swapped, name))
            self.assertAlmostEqual(
                getattr(baseline, name),
                getattr(relabelled, name),
            )

    def test_large_sample_converges_to_normal_reference(self) -> None:
        p = np.array([[300_000, 100_000], [80_000, 520_000]])
        q = np.array([[410_000, 90_000], [120_000, 380_000]])
        result = welch_satterthwaite_test(p, q)
        self.assertGreater(result.welch_degrees_of_freedom, 500_000)
        self.assertLess(abs(result.welch_p_value - result.normal_p_value), 1e-6)
        self.assertTrue(result.expanded_valid)
        self.assertGreater(result.expanded_welch_degrees_of_freedom, 100_000)
        self.assertLess(
            abs(result.expanded_welch_p_value - result.normal_p_value),
            1e-5,
        )

    def test_vectorized_batch_matches_scalar_results(self) -> None:
        p = np.array(
            [
                [[30, 5], [8, 27]],
                [[25, 10], [5, 30]],
            ]
        )
        q = np.array(
            [
                [[60, 10], [15, 55]],
                [[50, 20], [10, 60]],
            ]
        )
        batch = differential_mi_pvalues(p, q)
        for index in range(2):
            scalar = welch_satterthwaite_test(p[index], q[index])
            self.assertAlmostEqual(
                batch["welch_p_value"][index],
                scalar.welch_p_value,
            )
            self.assertAlmostEqual(
                batch["unbiased_welch_p_value"][index],
                scalar.unbiased_welch_p_value,
            )
            self.assertAlmostEqual(
                batch["expanded_welch_p_value"][index],
                scalar.expanded_welch_p_value,
            )
    def test_optional_calibrations_do_not_change_normal_result(self) -> None:
        p = np.array([[30, 5], [8, 27]])
        q = np.array([[60, 10], [15, 55]])
        complete = differential_mi_pvalues(p, q)
        normal_only = differential_mi_pvalues(
            p,
            q,
            include_simple=False,
            include_expanded=False,
            include_unbiased_sensitivity=False,
        )
        self.assertTrue(normal_only["valid"])
        self.assertAlmostEqual(
            float(normal_only["normal_p_value"]),
            float(complete["normal_p_value"]),
        )
        self.assertTrue(np.isnan(normal_only["welch_p_value"]))
        self.assertTrue(np.isnan(normal_only["expanded_welch_p_value"]))

    def test_degenerate_independence_is_reported_invalid(self) -> None:
        table = np.array([[10, 20], [20, 40]])
        result = welch_satterthwaite_test(table, table)
        self.assertFalse(result.valid)
        self.assertTrue(np.isnan(result.welch_p_value))

    def test_one_sided_degenerate_variance_is_reported_invalid(self) -> None:
        """A single zero-variance side must invalidate the pair, not just the mean."""
        p = np.array([[0, 0], [12, 38]])
        q = np.array([[9, 26], [8, 7]])
        values = differential_mi_pvalues(p, q)
        self.assertAlmostEqual(float(values["influence_variance_p"]), 0.0)
        self.assertGreater(float(values["influence_variance_q"]), 0.0)
        self.assertFalse(values["base_valid"])
        self.assertTrue(np.isnan(values["normal_p_value"]))

    def test_invalid_inputs_are_rejected(self) -> None:
        valid = np.array([[3, 2], [1, 4]])
        with self.assertRaises(ValueError):
            welch_satterthwaite_test(valid, np.ones((2, 3), dtype=int))
        with self.assertRaises(ValueError):
            welch_satterthwaite_test(valid.astype(float) + 0.5, valid)
        with self.assertRaises(ValueError):
            welch_satterthwaite_test(np.array([[4, 2]]), np.array([[3, 3]]))


if __name__ == "__main__":
    unittest.main()
