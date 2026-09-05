from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_supervisor_experiment import (
    BRADLEY_LIBERAL_LOWER,
    BRADLEY_LIBERAL_UPPER,
    CALIBRATION_ALPHAS,
    MAXIMUM_SAMPLE_SIZE,
    MINIMUM_SAMPLE_SIZE,
    RandomScenario,
    _aggregate_rejection_calibration,
    _build_power_alternative,
    _fixed_density_sample_sizes,
    _sample_sizes_in_expected_band,
    _simulate_null_scenario,
    _wilson,
    _wilson_many,
    _widespread_sparsity_sample_sizes,
    generate_strong_null_scenarios,
)
from differential_mi.distributions import table_with_target_mi


class ExpectedCountDesignTests(unittest.TestCase):
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
                        "regime": "well_sampled",
                        "regime_label": "Well sampled",
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
        self.assertGreaterEqual(n_p, MINIMUM_SAMPLE_SIZE)
        self.assertLessEqual(n_q, MAXIMUM_SAMPLE_SIZE)

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

    def test_fixed_density_sizes_respect_global_bounds(self) -> None:
        n_p, n_q = _fixed_density_sample_sizes(
            64,
            density=6,
            ratio=2,
        )
        self.assertEqual((n_p, n_q), (384, 768))
        self.assertGreaterEqual(n_p, MINIMUM_SAMPLE_SIZE)
        self.assertLessEqual(n_q, MAXIMUM_SAMPLE_SIZE)

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

def _make_scenario(target_mi: float = 0.10, rows: int = 2, columns: int = 2) -> RandomScenario:
    """Build a small deterministic RandomScenario for targeted unit tests."""
    row = np.full(rows, 1.0 / rows)
    column = np.full(columns, 1.0 / columns)
    probability_p, association_p = table_with_target_mi(row, column, target_mi)
    return RandomScenario(
        scenario_id="unit_test_scenario",
        shape_index=0,
        design_index=0,
        rows=rows,
        columns=columns,
        n_p=200,
        n_q=200,
        target_mi=target_mi,
        margin_alpha_p=50.0,
        margin_alpha_q=50.0,
        association_p=association_p,
        association_q=association_p,
        generation_attempts=1,
        probability_p=probability_p,
        probability_q=probability_p.copy(),
    )


class StrongNullTests(unittest.TestCase):
    def test_strong_null_scenarios_have_identical_populations(self) -> None:
        scenarios = generate_strong_null_scenarios(2_026_000_001)
        self.assertGreater(len(scenarios), 0)
        for scenario in scenarios:
            np.testing.assert_array_equal(
                scenario.probability_p, scenario.probability_q
            )
            self.assertAlmostEqual(scenario.association_p, scenario.association_q)
            self.assertGreaterEqual(scenario.n_p, MINIMUM_SAMPLE_SIZE)
            self.assertLessEqual(scenario.n_q, MAXIMUM_SAMPLE_SIZE)


class ThreeDenominatorReportingTests(unittest.TestCase):
    def test_common_valid_and_unconditional_rates_bound_the_conditional_rate(
        self,
    ) -> None:
        scenario = _make_scenario()
        rows, _, _ = _simulate_null_scenario(
            scenario, replicates=400, batch_size=100, seed=2_026_000_002
        )
        for row in rows:
            self.assertLessEqual(row["common_valid_replicates"], row["replicates"])
            for label in ("10", "05", "01"):
                # Unconditional divides the same numerator by a denominator
                # that is at least as large, so it can never exceed the
                # conditional rate.
                self.assertLessEqual(
                    row[f"unconditional_fpr_{label}"] + 1e-12,
                    row[f"fpr_{label}"] + 1e-12,
                )
                self.assertIsInstance(row[f"adequate_size_control_{label}"], bool)

    def test_bradley_liberal_interval_is_symmetric_around_nominal(self) -> None:
        self.assertLess(BRADLEY_LIBERAL_LOWER, 1.0)
        self.assertGreater(BRADLEY_LIBERAL_UPPER, 1.0)


class PowerAlternativeTests(unittest.TestCase):
    def test_alternative_hits_the_relative_effect_target(self) -> None:
        scenario = _make_scenario(target_mi=0.10)
        rng = np.random.default_rng(2_026_000_003)
        probability_q_alt, _, target_mi_alt = _build_power_alternative(
            scenario, relative_effect=0.5, rng=rng
        )
        self.assertAlmostEqual(target_mi_alt, 0.15, places=6)
        self.assertAlmostEqual(float(probability_q_alt.sum()), 1.0, places=10)

    def test_infeasible_target_raises_with_a_reason(self) -> None:
        scenario = _make_scenario(target_mi=0.10)
        rng = np.random.default_rng(2_026_000_004)
        with self.assertRaises(ValueError):
            _build_power_alternative(scenario, relative_effect=1_000.0, rng=rng)


if __name__ == "__main__":
    unittest.main()
