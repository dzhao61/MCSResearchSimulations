from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_detection_breakdown_sweep import (
    _simulate_configuration,
    construct_all_populations,
    construct_population,
    dominant_margin,
    entropy_mi_upper_bound,
    generate_configuration_manifest,
    paired_difference_interval,
    parse_shape,
    reachable_path_maximum,
    stable_seed,
    sustained_frontier,
)


PROTOCOL_PATH = PROJECT_ROOT / "experiments" / "FINAL_PROTOCOL.json"


def load_protocol() -> dict:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


class ManifestTests(unittest.TestCase):
    def test_full_manifest_has_all_declared_cells_without_duplicates(self) -> None:
        manifest = generate_configuration_manifest(load_protocol(), "full")
        self.assertEqual(len(manifest), 5_672)
        self.assertTrue(manifest["configuration_id"].is_unique)
        self.assertEqual(
            manifest.groupby("experiment").size().to_dict(),
            {
                "calibration": 1_152,
                "power": 3_584,
                "robustness_imbalance": 360,
                "robustness_interaction": 576,
            },
        )

    def test_frozen_manifest_matches_protocol_expansion(self) -> None:
        generated = generate_configuration_manifest(load_protocol(), "full")
        frozen = pd.read_csv(
            PROJECT_ROOT / "experiments" / "FINAL_CONFIGURATION_MANIFEST.csv"
        )
        pd.testing.assert_frame_equal(frozen, generated, check_dtype=False)

    def test_calibration_and_power_use_separate_sample_grids(self) -> None:
        protocol = load_protocol()
        manifest = generate_configuration_manifest(protocol, "full")
        calibration = sorted(
            manifest.loc[manifest["experiment"].eq("calibration"), "n_p"].unique()
        )
        power = sorted(
            manifest.loc[manifest["experiment"].eq("power"), "n_p"].unique()
        )
        self.assertEqual(calibration, protocol["experiment_2_calibration"]["sample_sizes"])
        self.assertEqual(power, protocol["experiment_3_power"]["sample_sizes"])

    def test_smoke_manifest_uses_declared_development_profile(self) -> None:
        manifest = generate_configuration_manifest(load_protocol(), "smoke")
        primary = manifest[manifest["experiment"].isin(["calibration", "power"])]
        self.assertEqual(set(primary["shape"]), {"2x2", "3x5"})
        self.assertEqual(set(primary["skewness"]), {"balanced", "ultra"})
        self.assertTrue((manifest["replicates"] == 200).all())


class PopulationConstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol = load_protocol()

    def test_entropy_upper_bound_for_uniform_rectangular_table(self) -> None:
        row = np.full(2, 0.5)
        column = np.full(3, 1 / 3)
        self.assertAlmostEqual(entropy_mi_upper_bound(row, column), np.log(2))

    def test_reachable_range_is_monotone(self) -> None:
        row = dominant_margin(3, "balanced")
        column = dominant_margin(5, "strong")
        interaction = np.outer(np.linspace(-1, 1, 3), np.linspace(-1, 1, 5))
        maximum, _, trace = reachable_path_maximum(
            row, column, interaction, [0, 0.25, 0.5, 1, 2], 1e-10
        )
        achieved = [point["mi"] for point in trace]
        self.assertGreater(maximum, 0)
        self.assertTrue(np.all(np.diff(achieved) >= -1e-10))

    def test_identical_null_is_exactly_identical(self) -> None:
        metadata, probability_p, probability_q = construct_population(
            ("2x2", "balanced", "identical_distribution", "primary", 0.0),
            self.protocol,
        )
        np.testing.assert_array_equal(probability_p, probability_q)
        self.assertEqual(metadata["absolute_mi_difference"], 0)

    def test_different_shape_null_has_equal_mi_but_different_tables(self) -> None:
        metadata, probability_p, probability_q = construct_population(
            ("2x2", "balanced", "equal_mi_different_shape", "primary", 0.0),
            self.protocol,
        )
        self.assertLessEqual(metadata["absolute_mi_difference"], 1e-10)
        self.assertGreater(metadata["l1_distance"], 1e-8)
        self.assertFalse(np.allclose(probability_p, probability_q))

    def test_target_is_within_frozen_reachable_buffer(self) -> None:
        metadata, _, _ = construct_population(
            ("3x5", "ultra", "equal_mi_different_shape", "primary", 0.6),
            self.protocol,
        )
        self.assertLessEqual(
            metadata["target_mi_q"], 0.8 * metadata["shared_reachable_mi"] + 1e-10
        )
        self.assertLessEqual(
            abs(metadata["achieved_mi_q"] - metadata["target_mi_q"]), 1e-10
        )

    def test_square_and_rectangular_shapes_parse(self) -> None:
        self.assertEqual(parse_shape("5x5"), (5, 5))
        self.assertEqual(parse_shape("4x8"), (4, 8))

    def test_value_and_runtime_construction_failures_are_recorded(self) -> None:
        manifest = pd.DataFrame(
            [
                {
                    "shape": "2x2",
                    "skewness": "balanced",
                    "relationship": "identical_distribution",
                    "interaction_pair": "primary",
                    "relative_effect": 0.0,
                },
                {
                    "shape": "3x3",
                    "skewness": "strong",
                    "relationship": "equal_mi_different_shape",
                    "interaction_pair": "primary",
                    "relative_effect": 0.0,
                },
            ]
        )
        with patch(
            "run_detection_breakdown_sweep.construct_population",
            side_effect=[ValueError("bad target"), RuntimeError("IPF failure")],
        ):
            populations, definitions, failures = construct_all_populations(
                manifest, self.protocol
            )
        self.assertFalse(populations)
        self.assertTrue(definitions.empty)
        self.assertEqual(set(failures["error_type"]), {"ValueError", "RuntimeError"})


class AggregationTests(unittest.TestCase):
    def test_seed_is_stable_and_configuration_specific(self) -> None:
        first = stable_seed(123, "configuration-a")
        self.assertEqual(first, stable_seed(123, "configuration-a"))
        self.assertNotEqual(first, stable_seed(123, "configuration-b"))

    def test_sustained_frontier_requires_three_consecutive_points(self) -> None:
        sizes = [2, 5, 10, 20, 50]
        self.assertEqual(
            sustained_frontier(sizes, [True, False, True, True, True]), 10
        )
        self.assertIsNone(
            sustained_frontier(sizes, [True, False, True, True, False])
        )

    def test_paired_interval_uses_discordant_counts(self) -> None:
        difference, standard_error, low, high = paired_difference_interval(20, 5, 100)
        self.assertAlmostEqual(difference, 0.15)
        self.assertGreater(standard_error, 0)
        self.assertLess(low, difference)
        self.assertGreater(high, difference)

    def test_simulation_reports_all_three_denominators_and_pair_counts(self) -> None:
        protocol = load_protocol()
        metadata, probability_p, probability_q = construct_population(
            ("2x2", "balanced", "identical_distribution", "primary", 0.0),
            protocol,
        )
        configuration = {
            "configuration_id": "unit-simulation",
            "experiment": "calibration",
            "shape": "2x2",
            "rows": 2,
            "columns": 2,
            "skewness": "balanced",
            "relationship": "identical_distribution",
            "interaction_pair": "primary",
            "n_p": 50,
            "n_q": 50,
            "sample_size_ratio_q_to_p": 1.0,
            "relative_effect": 0.0,
            "replicates": 200,
            "structural_breakdown": False,
            "simulation_seed": stable_seed(123, "unit-simulation"),
            "population_id": metadata["population_id"],
            "target_mi_p": metadata["target_mi_p"],
            "target_mi_q": metadata["target_mi_q"],
            "achieved_mi_p": metadata["achieved_mi_p"],
            "achieved_mi_q": metadata["achieved_mi_q"],
            "shared_reachable_mi": metadata["shared_reachable_mi"],
            "absolute_mi_difference": metadata["absolute_mi_difference"],
            "population_l1_distance": metadata["l1_distance"],
        }
        output = _simulate_configuration(
            {
                "configuration": configuration,
                "probability_p": probability_p,
                "probability_q": probability_q,
                "alphas": [0.1, 0.05, 0.01],
                "batch_size": 100,
            }
        )
        self.assertEqual(len(output["cell_rows"]), 9)
        self.assertEqual(len(output["paired_rows"]), 9)
        for row in output["cell_rows"]:
            self.assertIn("unconditional_rejection_rate", row)
            self.assertIn("conditional_rejection_rate", row)
            self.assertIn("common_valid_rejection_rate", row)
            self.assertLessEqual(row["rejections"], row["valid_replicates"])
        for row in output["paired_rows"]:
            self.assertEqual(
                row["both_reject"]
                + row["neither_rejects"]
                + row["only_method_a_rejects"]
                + row["only_method_b_rejects"],
                200,
            )


if __name__ == "__main__":
    unittest.main()
