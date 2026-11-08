from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.stats import norm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.statistics import influence_variance
from welch_differential_mi.higher_order import (
    _mi_variance_influence_moments,
    joint_cornish_fisher_values,
)
from run_joint_cornish_fisher_audit import cornish_fisher_boundaries


class HigherOrderTests(unittest.TestCase):
    def test_mi_variance_matches_existing_estimator(self) -> None:
        tables = np.array(
            [
                [[30, 10], [8, 52]],
                [[12, 3], [7, 28]],
            ]
        )
        moments = _mi_variance_influence_moments(tables)
        np.testing.assert_allclose(
            moments["mi_variance"],
            influence_variance(tables),
            rtol=1e-13,
            atol=1e-13,
        )

    def test_identical_groups_recover_normal_boundaries(self) -> None:
        table = np.array([[30, 10], [8, 52]])
        result = joint_cornish_fisher_values(table, table)
        self.assertAlmostEqual(float(result["mean_shift"]), 0.0, places=13)
        self.assertAlmostEqual(float(result["skewness"]), 0.0, places=13)
        self.assertAlmostEqual(
            float(result["lower_critical"]),
            float(norm.ppf(0.025)),
            places=13,
        )
        self.assertAlmostEqual(
            float(result["upper_critical"]),
            float(norm.ppf(0.975)),
            places=13,
        )

    def test_swapping_groups_reflects_the_boundaries(self) -> None:
        p = np.array([[30, 10], [8, 52]])
        q = np.array([[15, 5], [13, 67]])
        forward = joint_cornish_fisher_values(p, q)
        reverse = joint_cornish_fisher_values(q, p)
        self.assertAlmostEqual(
            float(forward["mean_shift"]),
            -float(reverse["mean_shift"]),
        )
        self.assertAlmostEqual(
            float(forward["skewness"]),
            -float(reverse["skewness"]),
        )
        self.assertAlmostEqual(
            float(forward["lower_critical"]),
            -float(reverse["upper_critical"]),
        )
        self.assertAlmostEqual(
            float(forward["upper_critical"]),
            -float(reverse["lower_critical"]),
        )

    def test_correction_vanishes_with_sample_size(self) -> None:
        p = np.array([[30, 10], [8, 52]])
        q = np.array([[15, 5], [13, 67]])
        small = joint_cornish_fisher_values(p, q)
        large = joint_cornish_fisher_values(100 * p, 100 * q)
        self.assertLess(
            abs(float(large["mean_shift"])),
            abs(float(small["mean_shift"])),
        )
        self.assertLess(
            abs(float(large["skewness"])),
            abs(float(small["skewness"])),
        )

    def test_alpha_must_be_a_probability(self) -> None:
        table = np.array([[30, 10], [8, 52]])
        with self.assertRaises(ValueError):
            joint_cornish_fisher_values(table, table, alpha=0.0)

    def test_split_sample_boundaries_are_ordered(self) -> None:
        sample = np.array([-2.0, -1.0, -0.5, 0.0, 0.1, 0.8, 1.3, 2.4])
        result = cornish_fisher_boundaries(sample)
        for name in ("location_scale", "cf_skew", "cf_four_moment", "empirical"):
            self.assertLess(result[name][0], result[name][1])
        np.testing.assert_allclose(
            result["empirical"],
            np.quantile(sample, [0.025, 0.975]),
        )


if __name__ == "__main__":
    unittest.main()
