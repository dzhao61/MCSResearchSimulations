from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from validate_scaled_chi_square import (  # noqa: E402
    _distribution_metrics,
    _moment_distribution,
    _population_component,
)


class ScaledChiSquareValidationTests(unittest.TestCase):
    def test_all_moment_models_match_requested_moments(self) -> None:
        target_mean = 1.7
        target_variance = 0.42
        for kind in ("chi2", "normal", "lognormal"):
            with self.subTest(kind=kind):
                distribution = _moment_distribution(
                    kind, target_mean, target_variance
                )
                self.assertAlmostEqual(distribution.mean(), target_mean)
                self.assertAlmostEqual(distribution.var(), target_variance)

    def test_distribution_metrics_recover_known_chi_squared_sample(self) -> None:
        rng = np.random.default_rng(731)
        distribution = _moment_distribution("chi2", 2.0, 0.8)
        sample = distribution.rvs(size=100_000, random_state=rng)
        metrics = _distribution_metrics(sample, distribution)
        self.assertLess(metrics["ks"], 0.01)
        self.assertLess(metrics["tail_abs_error_05"], 0.005)
        self.assertLess(metrics["tail_abs_error_01"], 0.003)

    def test_population_component_is_finite_and_positive(self) -> None:
        probability = np.array(
            [[0.34, 0.16], [0.11, 0.39]], dtype=float
        )
        variance, variance_if_variance, component_df = _population_component(
            probability, 200
        )
        self.assertGreater(variance, 0)
        self.assertGreater(variance_if_variance, 0)
        self.assertGreater(component_df, 0)
        self.assertAlmostEqual(
            component_df,
            2.0 * 200 * variance**2 / variance_if_variance,
        )


if __name__ == "__main__":
    unittest.main()
