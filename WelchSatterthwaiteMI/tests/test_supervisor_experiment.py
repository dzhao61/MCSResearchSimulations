from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_supervisor_experiment import (
    _margin_is_near_balanced,
    _margin_is_strongly_skewed,
    _sample_sizes_in_expected_band,
    _widespread_sparsity_sample_sizes,
)


class ExpectedCountDesignTests(unittest.TestCase):
    def test_highly_sparse_band_holds_for_both_populations(self) -> None:
        sample_sizes = _sample_sizes_in_expected_band(
            0.01,
            0.005,
            ratio=1,
            lower=1.0,
            upper=5.0,
        )
        self.assertIsNotNone(sample_sizes)
        n_p, n_q = sample_sizes
        self.assertGreaterEqual(n_p * 0.01, 1.0)
        self.assertLess(n_p * 0.01, 5.0)
        self.assertGreaterEqual(n_q * 0.005, 1.0)
        self.assertLess(n_q * 0.005, 5.0)

    def test_ultra_sparse_band_preserves_requested_ratio(self) -> None:
        sample_sizes = _sample_sizes_in_expected_band(
            0.003,
            0.002,
            ratio=4,
            lower=0.2,
            upper=1.0,
        )
        self.assertIsNotNone(sample_sizes)
        n_p, n_q = sample_sizes
        self.assertEqual(n_q, 4 * n_p)
        self.assertGreater(n_p * 0.003, 0.0)
        self.assertLess(n_p * 0.003, 1.0)
        self.assertGreater(n_q * 0.002, 0.0)
        self.assertLess(n_q * 0.002, 1.0)

    def test_returns_none_when_integer_sample_sizes_cannot_fit(self) -> None:
        sample_sizes = _sample_sizes_in_expected_band(
            0.1,
            0.1,
            ratio=1,
            lower=0.2,
            upper=1.0,
        )
        self.assertIsNone(sample_sizes)

    def test_widespread_sparsity_rule_controls_many_cells(self) -> None:
        probability_p = np.array([[0.95, 0.035], [0.01, 0.005]])
        probability_q = np.array([[0.94, 0.045], [0.01, 0.005]])
        sample_sizes = _widespread_sparsity_sample_sizes(
            probability_p,
            probability_q,
            ratio=1,
        )
        self.assertIsNotNone(sample_sizes)
        n_p, n_q = sample_sizes
        for expected in (n_p * probability_p, n_q * probability_q):
            self.assertGreaterEqual(float(np.mean(expected < 1.0)), 0.25)
            self.assertLessEqual(float(np.mean(expected < 1.0)), 0.50)
            self.assertGreaterEqual(float(np.mean(expected < 5.0)), 0.50)

    def test_shape_mismatch_margin_rules_are_distinct(self) -> None:
        balanced = np.array([0.34, 0.33, 0.33])
        skewed = np.array([0.80, 0.15, 0.05])
        self.assertTrue(_margin_is_near_balanced(balanced))
        self.assertFalse(_margin_is_near_balanced(skewed))
        self.assertTrue(_margin_is_strongly_skewed(skewed))
        self.assertFalse(_margin_is_strongly_skewed(balanced))


if __name__ == "__main__":
    unittest.main()
