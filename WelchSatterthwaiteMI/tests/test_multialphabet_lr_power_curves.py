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
from run_multialphabet_lr_power_curves import (  # noqa: E402
    BASE_MI,
    PLOTTED_METHODS,
    _simulate_configuration,
    build_curve_design,
)


class MultiAlphabetPowerCurveTests(unittest.TestCase):
    def test_curve_design_hits_each_target(self) -> None:
        for size in (3, 4, 5, 8):
            for regime in ("balanced", "mild", "strong", "ultra"):
                for difference in (0.0, 0.005, 0.02, 0.05):
                    design = build_curve_design(size, regime, difference)
                    self.assertAlmostEqual(
                        mutual_information_probability(design.probability_p),
                        BASE_MI,
                        places=10,
                    )
                    self.assertAlmostEqual(
                        mutual_information_probability(design.probability_q),
                        BASE_MI + difference,
                        places=10,
                    )
                    self.assertTrue(np.all(design.probability_p > 0.0))
                    self.assertTrue(np.all(design.probability_q > 0.0))

    def test_smoke_configuration_returns_three_methods(self) -> None:
        result = _simulate_configuration(
            (build_curve_design(3, "balanced", 0.01), 100, 3, 2026)
        )
        self.assertEqual(
            {row["method"] for row in result["rows"]},
            set(PLOTTED_METHODS),
        )
        self.assertTrue(all(row["replicates"] == 3 for row in result["rows"]))
        self.assertGreater(result["diagnostics"]["lr_valid_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
