"""Protect saved-sample mechanism analyses without changing either test."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import report_focused_mechanisms as report


class MechanismCalculationTests(unittest.TestCase):
    def test_negative_true_difference(self):
        summary = report.direction_summary([-2, 2, -1, 1], [True]*4, [.01, .05, .2, .01], -.1)
        self.assertEqual(summary["rejections"], 3)
        self.assertEqual(summary["correct_sign"], 1)
        self.assertEqual(summary["opposite_sign"], 2)
        self.assertAlmostEqual(summary["opposite_fraction_among_rejections"], 2/3)
        self.assertEqual(summary["opposite_rate_all_repetitions"], .5)

    def test_positive_true_difference_reverses_classification(self):
        summary = report.direction_summary([-2, 2], [True]*2, [.01]*2, .1)
        self.assertEqual(summary["opposite_sign"], 1)
        self.assertEqual(summary["correct_sign"], 1)

    def test_invalid_and_nonfinite_outputs_are_not_rejections(self):
        summary = report.direction_summary([1, 1, np.nan, 1], [False, True, True, True],
                                           [.01, np.nan, .01, .01], -.1)
        self.assertEqual(summary["rejections"], 1)
        self.assertEqual(summary["opposite_sign"], 1)

    def test_no_rejections_has_no_conditional_fraction(self):
        summary = report.direction_summary([1, -1], [True]*2, [.5]*2, -.1)
        self.assertIsNone(summary["opposite_fraction_among_rejections"])
        self.assertEqual(summary["opposite_rate_all_repetitions"], 0)

    def test_direction_is_undefined_at_the_null(self):
        with self.assertRaises(ValueError):
            report.direction_summary([1], [True], [.01], 0)

    def test_stability_keeps_finite_zeros_and_uses_a_matched_subset(self):
        summary = report.stability_summary([0, 2, np.nan, 10], [0, 4, 5, np.nan], 6, 2)
        self.assertEqual(summary["included_count"], 2)
        self.assertEqual(summary["observed_variance_of_variance"], 2)
        self.assertEqual(summary["population_observed_ratio"], 1.5)
        self.assertEqual(summary["plugin_observed_ratio"], .5)

    def test_constant_variance_records_do_not_define_a_ratio(self):
        summary = report.stability_summary([1, 1], [2, 2], 2, 10)
        self.assertIsNone(summary["population_observed_ratio"])
        self.assertIsNone(summary["plugin_observed_ratio"])
        self.assertEqual(report.bootstrap_intervals([1, 1], [2, 2], 2, 10, 5)["finite_repetitions"], 0)

    def test_population_moments_match_independence_and_implementation(self):
        independent = np.outer([.7, .3], [.7, .3])
        self.assertAlmostEqual(report.population_moments(independent)["tau2"], 0)
        probability = .8*independent+.2*np.diag([.7, .3])
        moments = report.population_moments(probability)
        from welch_differential_mi.welch import _variance_influence_component_df
        _, expected_tau = _variance_influence_component_df(probability, np.asarray(moments["variance"]))
        self.assertAlmostEqual(moments["tau2"], float(expected_tau))

    def test_bootstrap_resamples_variance_and_sensitivity_together(self):
        v, t = np.array([0., 1., 2., 4., 8.]), np.array([1., 2., 4., 8., 16.])
        index = np.random.default_rng(23).integers(0, len(v), size=(25, len(v)))
        observed = np.var(v[index], axis=1, ddof=1)
        finite = observed > 0
        expected = np.quantile(np.mean(t[index], axis=1)[finite]/10/observed[finite], [.025, .975])
        summary = report.bootstrap_intervals(v, t, 4, 10, 23, repetitions=25)
        np.testing.assert_array_equal(summary["plugin_ratio_interval"], expected)
        self.assertEqual(summary["finite_repetitions"], int(finite.sum()))


class SavedMechanismTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = report.build_evidence()

    def test_exact_scope_and_all_finite_inclusion(self):
        rows = self.evidence["stability"]
        self.assertEqual(len(rows), 12)
        self.assertEqual(len(self.evidence["direction"]), 4)
        self.assertEqual({(r["k"], r["n"], r["mi"]) for r in rows}, set(report.STABILITY_SETTINGS))
        self.assertTrue(all(r["included_count"] == 20000 for r in rows))
        self.assertTrue(all(r["monte_carlo_check"]["finite_repetitions"] == 1000 for r in rows))
        self.assertTrue(all(r[m]["valid_count"] == 20000 for r in self.evidence["direction"]
                            for m in ("wald", "expanded")))

    def test_verified_direction_counts(self):
        actual = [(r["wald"]["rejections"], r["wald"]["opposite_sign"],
                   r["expanded"]["rejections"], r["expanded"]["opposite_sign"])
                  for r in self.evidence["direction"]]
        self.assertEqual(actual, [(2010, 2009, 1906, 1905), (725, 713, 680, 669),
                                  (13984, 0, 13935, 0), (19863, 0, 19862, 0)])
        for row in self.evidence["direction"]:
            for method in ("wald", "expanded"):
                result = row[method]
                self.assertEqual(result["rejections"], result["correct_sign"]+result["opposite_sign"])

    def test_stability_ratios_and_precision_support_the_interpretation(self):
        rows = self.evidence["stability"]
        for row in rows:
            if row["mi"] == .0001:
                self.assertLess(row["population_observed_ratio"], .06)
                self.assertGreater(row["plugin_observed_ratio"], 1.9)
                self.assertGreater(row["monte_carlo_check"]["plugin_ratio_interval"][0], 1.8)
            if row["k"] == 4 and row["n"] == 10000:
                self.assertLess(abs(row["population_observed_ratio"]-1), .03)
                self.assertLess(abs(row["plugin_observed_ratio"]-1), .03)
        tiny = [r for r in rows if r["mi"] == .0001]
        np.testing.assert_array_equal(np.round([r["population_observed_ratio"] for r in tiny], 3), [.047, .051])
        np.testing.assert_array_equal(np.round([r["plugin_observed_ratio"] for r in tiny], 3), [1.950, 2.093])

    def test_generated_tables_and_evidence_are_reproducible(self):
        figures = ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite"
        if not figures.exists():
            self.skipTest("Thesis source is a separate delivered archive.")
        self.assertEqual((figures/"focused_stability_table.tex").read_text(),
                         report.stability_table(self.evidence["stability"]))
        self.assertEqual((figures/"focused_direction_table.tex").read_text(),
                         report.direction_table(self.evidence["direction"]))
        self.assertEqual(json.loads((figures/"focused_mechanism_evidence.json").read_text()), self.evidence)


if __name__ == "__main__":
    unittest.main()
