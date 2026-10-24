"""Verify the bounded jackknife diagnostic without changing the existing methods."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"experiments"))
import run_focused_jackknife_check as check
from differential_mi.statistics import jackknife_mi, plugin_mi
from focused_study_core import simulate_chunk


class JackknifeCalculationTests(unittest.TestCase):
    def test_literal_reference_matches_removing_every_observation(self):
        table = np.array([[4, 1, 0], [0, 1, 2], [0, 0, 0]])
        deletions = []
        for i, j in np.argwhere(table > 0):
            reduced = table.copy()
            reduced[i, j] -= 1
            deletions.extend([float(plugin_mi(reduced))]*int(table[i, j]))
        n = table.sum()
        expected = n*float(plugin_mi(table))-(n-1)*np.mean(deletions)
        self.assertAlmostEqual(check.literal_jackknife(table), expected, places=12)

    def test_vectorized_estimator_handles_zeros_singletons_and_empty_margins(self):
        tables = np.array([[[4, 1, 0], [0, 1, 2], [0, 0, 0]],
                           [[1, 0, 0], [0, 0, 1], [1, 1, 0]],
                           [[10, 0, 0], [0, 0, 0], [0, 0, 0]]])
        np.testing.assert_allclose(jackknife_mi(tables),
                                   [check.literal_jackknife(t) for t in tables], atol=1e-12)

    def test_large_table_matches_independent_definition(self):
        rng = np.random.default_rng(19)
        for n in (1000, 10000):
            table = rng.multinomial(n, np.full(256, 1/256)).reshape(16, 16)
            np.testing.assert_allclose(jackknife_mi(table), check.literal_jackknife(table),
                                       atol=3e-11, rtol=1e-9)

    def test_negative_jackknife_estimate_is_not_clipped(self):
        result = jackknife_mi(np.array([[2, 2], [2, 2]]))
        self.assertLess(result, 0)

    def test_sample_regeneration_matches_original_batched_sampler(self):
        config = {"configuration_id": "test_setting", "n_p": 1000, "n_q": 10000}
        p = np.array([[.4, .1], [.1, .4]])
        q = np.array([[.6, .1], [.1, .2]])
        counts_p, counts_q = check.original_counts(config, p, q, 2, 31)
        expected = simulate_chunk(config, p, q, 2, 31, 7, "full")
        actual = check.evaluate_tables(counts_p, counts_q)
        for key in expected:
            np.testing.assert_array_equal(actual[key], expected[key])

    def test_fixed_se_does_not_change_validity_or_denominator(self):
        valid, statistic, p_value = check.fixed_se_test([-.04, .04, np.nan, 0],
                                                       [.01, .01, .01, 0], [1, 0, 1, 1])
        np.testing.assert_array_equal(valid, [1, 0, 0, 0])
        self.assertEqual(statistic[0], -4)
        self.assertLess(p_value[0], .05)
        self.assertTrue(np.isnan(p_value[1:]).all())


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.config = {"configuration_id": "test", "n_p": 1000, "mi_p": .02,
                       "mi_q": .03, "delta": -.01}

    def test_all_repetitions_denominator_and_alternative_direction(self):
        row, *_ = check.estimator_summary(np.array([-.05, .05, -.005, .05]),
                                         [0, .1, .02, .1], [.05, .05, .025, .05],
                                         [.01]*4, [1, 1, 1, 0], self.config, "test")
        self.assertEqual(row["valid_count"], 3)
        self.assertEqual(row["rejection"]["count"], 2)
        self.assertEqual(row["rejection"]["rate"], .5)
        self.assertEqual(row["correct_direction"]["rate"], .25)
        self.assertEqual(row["opposite_direction"]["rate"], .25)
        self.assertEqual(row["opposite_fraction_among_rejections"], .5)
        self.assertAlmostEqual(row["bias"]["mean"], np.mean([-.04, .06, .005, .06]))

    def test_direction_is_not_assigned_under_equal_mi(self):
        config = {**self.config, "mi_q": .02, "delta": 0}
        row, *_ = check.estimator_summary(np.array([-.05, .05]), [-.02, .1], [.03, .05],
                                         [.01]*2, [1, 1], config, "test")
        self.assertIsNone(row["correct_direction"])
        self.assertIsNone(row["opposite_direction"])
        self.assertEqual(row["negative_mi_p"]["count"], 1)

    def test_paired_contrast_uses_the_same_samples(self):
        row = check.paired_summary(np.array([1., 2., 3., 4.]), np.array([2., 3., 4., 5.]),
                                   np.array([1, 0, 0, 0], bool),
                                   np.array([0, 1, 1, 0], bool), 0)
        self.assertEqual(row["bias_change_jackknife_minus_analytic"]["mean"], 1)
        contrast = row["rejection_change_jackknife_minus_analytic"]
        self.assertEqual(contrast["only_jackknife"], 2)
        self.assertEqual(contrast["only_analytic"], 1)
        self.assertEqual(contrast["estimate"], .25)

    def test_variance_ratio_interval_is_undefined_for_constant_estimates(self):
        self.assertIsNone(check.variance_ratio_interval([1, 1], [2, 2], 23))

    def test_scope_requires_exactly_one_match_per_planned_setting(self):
        rows = [{"configuration_id": f"setting_{n}_{mi_q}", "k": 16,
                 "profile": "different_skew", "construction": "copying",
                 "n_p": n, "n_q": n, "mi_p": .02, "mi_q": mi_q}
                for n, mi_q in check.SETTINGS]
        self.assertEqual(len(check.select_settings(pd.DataFrame(rows))), 4)
        with self.assertRaises(ValueError):
            check.select_settings(pd.DataFrame(rows[:-1]))
        with self.assertRaises(ValueError):
            check.select_settings(pd.DataFrame(rows+[rows[0]]))


class SavedDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = check.DEFAULT_OUTPUT/"evidence.json"
        if not path.exists():
            raise unittest.SkipTest("Optional diagnostic has not been run.")
        cls.evidence = json.loads(path.read_text())

    def test_scope_and_verified_original_samples(self):
        rows = self.evidence["estimators"]
        self.assertEqual(len(rows), 8)
        self.assertEqual({(r["n"], r["mi_q"]) for r in rows}, set(check.SETTINGS))
        self.assertTrue(all(r["repetitions"] == r["valid_count"] == 20000 for r in rows))
        verification = json.loads((check.DEFAULT_OUTPUT/"verification.json").read_text())
        self.assertTrue(verification["all_pass"])
        self.assertEqual(verification["original_sample_pairs_verified"], 80000)
        self.assertEqual(sum(r["literal_checks"] for r in verification["checks"]), 16)

    def test_saved_direction_counts_and_estimator_moments(self):
        rows = self.evidence["estimators"]
        self.assertEqual([r["rejection"]["count"] for r in rows],
                         [5044, 169, 2010, 549, 925, 1014, 13984, 13238])
        for row in rows:
            with np.load(check.DEFAULT_OUTPUT/f"{row['configuration_id']}.npz") as values:
                prefix = "analytic" if row["method"] == "analytic_normal" else "jackknife"
                delta = values[f"{prefix}_delta"]
                self.assertAlmostEqual(row["bias"]["mean"], float(delta.mean()-row["true_delta"]))
                self.assertAlmostEqual(row["observed_sd"], float(np.std(delta, ddof=1)))
                self.assertAlmostEqual(row["se_variance_ratio"],
                                       float(np.mean(values["standard_error"]**2)/np.var(delta, ddof=1)))
                if row["true_delta"] != 0:
                    opposite = values[f"{prefix}_rejected"] & (delta*row["true_delta"] < 0)
                    self.assertEqual(row["opposite_direction"]["count"], int(opposite.sum()))
        self.assertEqual([r["opposite_direction"]["count"] for r in rows if r["true_delta"] != 0],
                         [2009, 5, 0, 0])

    def test_small_difference_bias_does_not_imply_unbiased_individual_mi(self):
        rows = self.evidence["estimators"]
        sparse_jackknife = [r for r in rows if r["n"] == 1000 and r["method"] == "jackknife_fixed_se_normal"]
        for row in sparse_jackknife:
            self.assertGreater(row["bias_p"]["mean"], .03)
            self.assertGreater(row["bias_q"]["mean"], .03)
            self.assertLess(abs(row["bias"]["mean"]), .002)
            self.assertGreater(row["se_variance_ratio"], 1.6)


if __name__ == "__main__":
    unittest.main()
