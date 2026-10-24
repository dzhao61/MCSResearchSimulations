from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.stats import norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_critical_value_audit import (  # noqa: E402
    SAMPLE_SCALES,
    audit_configurations,
    implied_t_degrees_of_freedom,
)


class CriticalValueAuditTests(unittest.TestCase):
    def test_audit_grid_contains_only_scaled_null_cases(self) -> None:
        anchors, configurations = audit_configurations()
        self.assertEqual(len(configurations), len(anchors) * len(SAMPLE_SCALES))
        for config in configurations:
            self.assertAlmostEqual(config.true_delta, 0.0)
            self.assertAlmostEqual(config.effect_delta_i, 0.0)

    def test_implied_degrees_of_freedom_inverts_student_critical_value(self) -> None:
        target_df = 7.5
        critical = float(t.ppf(0.975, target_df))
        self.assertAlmostEqual(
            implied_t_degrees_of_freedom(critical),
            target_df,
            places=6,
        )
        self.assertTrue(
            np.isnan(implied_t_degrees_of_freedom(float(norm.ppf(0.975) - 0.1)))
        )


if __name__ == "__main__":
    unittest.main()
