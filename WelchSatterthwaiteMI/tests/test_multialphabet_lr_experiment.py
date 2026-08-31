from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.distributions import mutual_information_probability  # noqa: E402
from run_multialphabet_lr_experiment import (  # noqa: E402
    ALTERNATIVE_MI,
    NULL_STAGE,
    BASE_MI,
    _simulate_stage,
    _stable_seed,
    build_population_design,
)


class MultiAlphabetExperimentTests(unittest.TestCase):
    def test_population_design_hits_targets_and_changes_shape(self) -> None:
        for size in (3, 4, 5, 8):
            for regime in ("balanced", "mild", "strong", "ultra"):
                design = build_population_design(size, regime)
                for probability in (
                    design.probability_p,
                    design.probability_q_null,
                    design.probability_q_alternative,
                ):
                    self.assertEqual(probability.shape, (size, size))
                    self.assertAlmostEqual(float(probability.sum()), 1.0, places=12)
                    self.assertTrue(np.all(probability > 0.0))
                self.assertAlmostEqual(
                    mutual_information_probability(design.probability_p),
                    BASE_MI,
                    places=10,
                )
                self.assertAlmostEqual(
                    mutual_information_probability(design.probability_q_null),
                    BASE_MI,
                    places=10,
                )
                self.assertAlmostEqual(
                    mutual_information_probability(design.probability_q_alternative),
                    ALTERNATIVE_MI,
                    places=10,
                )
                self.assertGreater(
                    np.abs(
                        design.probability_p - design.probability_q_null
                    ).sum(),
                    0.05,
                )

    def test_seed_is_stable_and_configuration_specific(self) -> None:
        seed = _stable_seed(2026, 3, "balanced", 50, "null")
        self.assertEqual(seed, _stable_seed(2026, 3, "balanced", 50, "null"))
        self.assertNotEqual(seed, _stable_seed(2026, 3, "balanced", 75, "null"))

    def test_small_3x3_stage_returns_all_methods(self) -> None:
        rows, diagnostics = _simulate_stage(
            build_population_design(3, "balanced"),
            sample_size=100,
            stage=NULL_STAGE,
            replicates=4,
            seed=2026,
        )
        self.assertEqual(
            {row["method"] for row in rows},
            {"normal_wald", "expanded_welch", "constrained_lr"},
        )
        self.assertTrue(all(row["replicates"] == 4 for row in rows))
        self.assertGreater(diagnostics["lr_valid_rate"], 0.0)
        self.assertGreaterEqual(diagnostics["minimum_expected_count"], 0.0)


if __name__ == "__main__":
    unittest.main()
