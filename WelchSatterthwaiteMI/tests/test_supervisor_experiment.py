from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_supervisor_experiment import (
    CALIBRATION_ALPHAS,
    CONFIGURATIONS,
    MAXIMUM_SAMPLE_SIZE,
    MINIMUM_SAMPLE_SIZE,
    SHAPES,
    _aggregate_rejection_calibration,
    _configuration_sample_sizes,
    _fixed_margin,
    _wilson,
    _wilson_many,
    generate_configuration_scenarios,
)
from differential_mi.distributions import mutual_information_probability


class ConfigurationDesignTests(unittest.TestCase):
    def test_calibration_grid_covers_lower_tail_in_thousandths(self) -> None:
        self.assertEqual(len(CALIBRATION_ALPHAS), 101)
        self.assertEqual(CALIBRATION_ALPHAS[0], 0.0)
        self.assertEqual(CALIBRATION_ALPHAS[-1], 0.1)
        self.assertIn(0.01, CALIBRATION_ALPHAS)
        self.assertIn(0.05, CALIBRATION_ALPHAS)

    def test_vectorized_wilson_matches_scalar_calculation(self) -> None:
        counts = np.array([0, 5, 25, 50])
        low, high = _wilson_many(counts, 100)
        for index, count in enumerate(counts):
            expected_low, expected_high = _wilson(int(count), 100)
            self.assertAlmostEqual(low[index], expected_low)
            self.assertAlmostEqual(high[index], expected_high)

    def test_rejection_calibration_aggregation_retains_spread(self) -> None:
        rows = []
        for scenario_id, rates in (
            ("scenario_a", (0.0, 0.04)),
            ("scenario_b", (0.0, 0.06)),
        ):
            for alpha, rate in zip((0.0, 0.05), rates):
                rows.append(
                    {
                        "scenario_id": scenario_id,
                        "regime": "balanced_control",
                        "regime_label": "Balanced control",
                        "method": "normal_wald",
                        "method_label": "Normal Wald",
                        "nominal_alpha": alpha,
                        "rejection_rate": rate,
                        "absolute_calibration_error": abs(rate - alpha),
                    }
                )
        summary = _aggregate_rejection_calibration(pd.DataFrame(rows))
        at_five_percent = summary[summary["nominal_alpha"].eq(0.05)].iloc[0]
        self.assertEqual(at_five_percent["population_pairs"], 2)
        self.assertAlmostEqual(at_five_percent["mean_rejection_rate"], 0.05)
        self.assertLess(
            at_five_percent["p10_rejection_rate"],
            at_five_percent["p90_rejection_rate"],
        )

    def test_fixed_margin_templates_are_exact(self) -> None:
        balanced = _fixed_margin(5, None, 3)
        moderate = _fixed_margin(5, 0.70, 2)
        strong = _fixed_margin(5, 0.90, 4)
        np.testing.assert_allclose(balanced, np.full(5, 0.20))
        self.assertAlmostEqual(moderate[2], 0.70)
        np.testing.assert_allclose(np.delete(moderate, 2), 0.075)
        self.assertAlmostEqual(strong[4], 0.90)
        np.testing.assert_allclose(np.delete(strong, 4), 0.025)

    def test_all_16_sample_size_formulas_are_exact_and_bounded(self) -> None:
        expected = {
            (2, 2): ((100, 100), (50, 50), (50, 50), (50, 250)),
            (3, 3): ((135, 135), (72, 72), (50, 50), (50, 250)),
            (5, 5): ((375, 375), (200, 200), (75, 75), (75, 375)),
            (8, 8): ((960, 960), (512, 512), (192, 192), (192, 960)),
        }
        for shape in SHAPES:
            cells = shape[0] * shape[1]
            actual = []
            for design in CONFIGURATIONS.values():
                sample_sizes = _configuration_sample_sizes(
                    cells,
                    density=design["density"],
                    ratio=design["sample_size_ratio"],
                    minimum_n=design["minimum_n"],
                )
                actual.append(sample_sizes)
                self.assertGreaterEqual(sample_sizes[0], MINIMUM_SAMPLE_SIZE)
                self.assertLessEqual(sample_sizes[1], MAXIMUM_SAMPLE_SIZE)
            self.assertEqual(tuple(actual), expected[shape])

    def test_generator_materializes_each_design_cell_and_seed(self) -> None:
        scenarios = generate_configuration_scenarios(2026080501, 1)
        self.assertEqual(len(scenarios), 16)
        self.assertEqual(
            len({scenario.configuration_id for scenario in scenarios}),
            16,
        )
        self.assertEqual(len({scenario.population_seed for scenario in scenarios}), 16)
        for scenario in scenarios:
            self.assertAlmostEqual(scenario.probability_p.sum(), 1.0)
            self.assertAlmostEqual(scenario.probability_q.sum(), 1.0)
            self.assertAlmostEqual(
                mutual_information_probability(scenario.probability_p),
                0.10,
                places=11,
            )
            self.assertAlmostEqual(
                mutual_information_probability(scenario.probability_q),
                0.10,
                places=11,
            )
            self.assertGreater(
                np.abs(scenario.probability_p - scenario.probability_q).sum(),
                0.05,
            )
            self.assertGreaterEqual(scenario.n_p, MINIMUM_SAMPLE_SIZE)
            self.assertLessEqual(scenario.n_q, MAXIMUM_SAMPLE_SIZE)

if __name__ == "__main__":
    unittest.main()
