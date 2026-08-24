from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_2x2_power_curves import (  # noqa: E402
    CANDIDATE_EFFECTS,
    SAMPLE_SCALES,
    build_curve_configurations,
    selected_anchor_configurations,
)


class TwoByTwoPowerCurveTests(unittest.TestCase):
    def test_grid_preserves_anchor_margins_and_sample_ratio(self) -> None:
        anchors = selected_anchor_configurations()
        anchor_by_id = {anchor.configuration_id: anchor for anchor in anchors}
        configurations = build_curve_configurations(anchors)
        self.assertIn(1.0, CANDIDATE_EFFECTS)
        self.assertTrue(any(config.effect_delta_i == 0.5 for config in configurations))
        self.assertFalse(any(config.effect_delta_i == 1.0 for config in configurations))
        self.assertGreater(
            len(configurations),
            len(anchors) * 5 * len(SAMPLE_SCALES),
        )
        for config in configurations:
            anchor = anchor_by_id[config.power_family]
            self.assertEqual(
                (
                    config.pair.u_p,
                    config.pair.v_p,
                    config.pair.u_q,
                    config.pair.v_q,
                ),
                (
                    anchor.pair.u_p,
                    anchor.pair.v_p,
                    anchor.pair.u_q,
                    anchor.pair.v_q,
                ),
            )
            self.assertAlmostEqual(
                config.pair.mi_q - config.pair.mi_p,
                config.effect_delta_i,
            )
            self.assertLessEqual(config.pair.mi_p, math.log(2.0))
            self.assertLessEqual(config.pair.mi_q, math.log(2.0))
            self.assertIn(config.effect_delta_i, CANDIDATE_EFFECTS)
            self.assertIn(config.n_p / anchor.n_p, SAMPLE_SCALES)
            self.assertAlmostEqual(config.n_p / config.n_q, anchor.n_p / anchor.n_q)

        for anchor in anchors:
            effects = {
                config.effect_delta_i
                for config in configurations
                if config.power_family == anchor.configuration_id
            }
            self.assertTrue({0.0, 1e-5, 1e-4, 1e-3, 5e-3}.issubset(effects))


if __name__ == "__main__":
    unittest.main()
