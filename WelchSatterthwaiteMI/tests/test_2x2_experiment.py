from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_2x2_experiment import (  # noqa: E402
    _size_adjustment_thresholds,
    build_null_configurations,
    build_power_configurations,
    fixed_null_pairs,
    probability_table,
    simulate_configuration,
    solve_target_mi,
    summarize_null,
)
from differential_mi.distributions import mutual_information_probability  # noqa: E402


class TwoByTwoExperimentTests(unittest.TestCase):
    def test_probability_table_has_requested_margins(self) -> None:
        table = probability_table(0.2, 0.3, 0.04)
        np.testing.assert_allclose(table.sum(axis=1), [0.8, 0.2])
        np.testing.assert_allclose(table.sum(axis=0), [0.7, 0.3])
        self.assertAlmostEqual(float(table.sum()), 1.0)

    def test_target_solver_reaches_both_association_branches(self) -> None:
        positive, delta_positive = solve_target_mi(0.5, 0.5, 0.1, 1)
        negative, delta_negative = solve_target_mi(0.5, 0.5, 0.1, -1)
        self.assertGreater(delta_positive, 0.0)
        self.assertLess(delta_negative, 0.0)
        self.assertAlmostEqual(mutual_information_probability(positive), 0.1)
        self.assertAlmostEqual(mutual_information_probability(negative), 0.1)

    def test_fixed_null_cases_have_equal_mi_and_expected_order(self) -> None:
        pairs = fixed_null_pairs()
        self.assertEqual(tuple(pairs), tuple(f"N{i}" for i in range(8)))
        for pair in pairs.values():
            self.assertAlmostEqual(pair.mi_p, pair.mi_q, places=10)
        self.assertLess(
            min(pairs["N7"].probability_p.min(), pairs["N7"].probability_q.min()),
            min(pairs["N0"].probability_p.min(), pairs["N0"].probability_q.min()),
        )

    def test_configuration_builders_are_unique_and_keep_low_counts(self) -> None:
        null, infeasible = build_null_configurations()
        power = build_power_configurations()
        null_ids = [config.configuration_id for config in null]
        power_ids = [config.configuration_id for config in power]
        self.assertEqual(len(null_ids), len(set(null_ids)))
        self.assertEqual(len(power_ids), len(set(power_ids)))
        self.assertTrue(infeasible)
        self.assertLess(
            min(
                min(
                    config.n_p * config.pair.probability_p.min(),
                    config.n_q * config.pair.probability_q.min(),
                )
                for config in null
            ),
            0.01,
        )

    def test_simulation_summary_partitions_valid_null_decisions(self) -> None:
        config = build_null_configurations()[0][0]
        values, diagnostics, _ = simulate_configuration(
            config,
            replicates=100,
            blocks=2,
            base_seed=1234,
            stream="test",
        )
        rows, curves, mechanism = summarize_null(config, values, diagnostics)
        self.assertEqual(len(rows), 3)
        self.assertEqual(len(curves), 3 * 101)
        self.assertEqual(mechanism["replicates"], 100)
        for row in rows:
            self.assertEqual(
                row["false_positive_count_05"] + row["true_negative_count_05"],
                row["valid_count"],
            )
            self.assertEqual(
                row["invalid_shared_statistic_count"]
                + row["invalid_reference_count"],
                row["invalid_count"],
            )
            self.assertAlmostEqual(
                row["false_positive_rate_05"] + row["true_negative_rate_05"],
                1.0,
            )

    def test_size_adjustment_uses_only_method_valid_values(self) -> None:
        config = build_null_configurations()[0][0]
        values, _, _ = simulate_configuration(
            config,
            replicates=100,
            blocks=1,
            base_seed=5678,
            stream="threshold-test",
        )
        rows = _size_adjustment_thresholds(values)
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertGreaterEqual(row["p_value_threshold_for_five_percent"], 0.0)
            self.assertLessEqual(row["p_value_threshold_for_five_percent"], 1.0)


if __name__ == "__main__":
    unittest.main()
