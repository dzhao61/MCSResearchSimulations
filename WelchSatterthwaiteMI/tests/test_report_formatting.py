"""Protect decimal ties and agreement between the manuscript rate tables."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from report_formatting import decimal_text, rate_interval_text


class ReportFormattingTests(unittest.TestCase):
    def test_rate_ties_round_half_up(self):
        for value, expected in ((.07365, "0.0737"), (.03825, "0.0383"),
                                (.04625, "0.0463"), (.04525, "0.0453"),
                                (.99095, "0.9910"), (.04895, "0.0490"),
                                (.00845, "0.0085")):
            with self.subTest(value=value):
                self.assertEqual(decimal_text(value), expected)

    def test_negative_zero_and_requested_precision(self):
        self.assertEqual(decimal_text(-0.0), "0.0000")
        self.assertEqual(decimal_text(-.00001), "0.0000")
        self.assertEqual(decimal_text(-.00005), "-0.0001")
        self.assertEqual(decimal_text(.00845, 5), "0.00845")

    def test_intervals_share_rate_rounding(self):
        row = dict(rejection_rate=.04625, rejection_low=.03825, rejection_high=.04895)
        self.assertEqual(rate_interval_text(row), "0.0463 [0.0383, 0.0490]")


if __name__ == "__main__":
    unittest.main()
