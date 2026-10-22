"""Checks for the standalone practical-data exploration."""

import unittest
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

import run_exploration as study


class ExplorationTests(unittest.TestCase):
    def test_full_data_only_export_reproduces_and_rejects_mutations(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            study.full_application(output)
            study.full_application(output, verify_only=True)
            self.assertFalse((output / "records").exists())
            values = pd.read_csv(output / "full_data_results.csv")
            values.loc[0, "wald_holm_p"] = .12345
            values.to_csv(output / "full_data_results.csv", index=False)
            with self.assertRaises(AssertionError):
                study.full_application(output, verify_only=True)

    def test_exact_six_comparison_scope(self):
        self.assertEqual(len(study.SPECIFICATIONS), 6)
        self.assertEqual(len({row[0] for row in study.SPECIFICATIONS}), 6)
        self.assertEqual([row[1] for row in study.SPECIFICATIONS].count("Adult"), 2)
        self.assertEqual(study.SAMPLE_SIZES, (50, 100, 200, 500, 1000, 2000, 5000))

    def test_common_alphabet_keeps_empty_categories(self):
        frame = pd.DataFrame({"x": ["a", "a", "c"], "y": [False, True, True]})
        table = study.count_table(frame, "x", "y", ["a", "b", "c"])
        np.testing.assert_array_equal(table, [[1, 1], [0, 0], [0, 1]])

    def test_unknown_category_is_not_silently_dropped(self):
        frame = pd.DataFrame({"x": ["a", "c"], "y": [False, True]})
        with self.assertRaises(ValueError):
            study.count_table(frame, "x", "y", ["a", "b"])

    def test_holm_and_missing_result(self):
        np.testing.assert_allclose(study.holm([.01, .03, .04]), [.03, .06, .06])
        values = study.holm([.01, np.nan, .1])
        np.testing.assert_allclose(values[[0, 2]], [.03, .2])
        self.assertTrue(np.isnan(values[1]))

    def test_independent_formula_with_unequal_counts(self):
        p = np.array([[14, 3], [8, 9], [4, 2]])
        q = np.array([[25, 5], [12, 17], [3, 4]])
        expected = study.independent_values(p, q)
        actual = study.method_values(p, q)
        for name, value in expected.items():
            np.testing.assert_allclose(actual[name], value, rtol=1e-11, atol=1e-12)
        self.assertGreaterEqual(actual["expanded_welch_p_value"], actual["normal_p_value"])

    def test_independent_formula_with_empty_margin(self):
        p = np.array([[14, 3], [8, 9], [0, 0]])
        q = np.array([[25, 5], [12, 17], [3, 4]])
        expected = study.independent_values(p, q)
        actual = study.method_values(p, q)
        for name, value in expected.items():
            np.testing.assert_allclose(actual[name], value, rtol=1e-11, atol=1e-12)

    def test_group_streams_are_distinct_and_reproducible(self):
        first = study.rng_for("adult_education", 100, "P").integers(0, 10000, size=50)
        second = study.rng_for("adult_education", 100, "P").integers(0, 10000, size=50)
        other = study.rng_for("adult_education", 100, "Q").integers(0, 10000, size=50)
        np.testing.assert_array_equal(first, second)
        self.assertFalse(np.array_equal(first, other))

    def test_without_replacement_sampling_and_summary(self):
        population = np.array([[30, 8], [12, 20], [15, 5]])
        p = study.rng_for("test", 50, "P").multivariate_hypergeometric(population.ravel(), 50, size=100).reshape(100, 3, 2)
        q = study.rng_for("test", 50, "Q").multivariate_hypergeometric(population.ravel(), 50, size=100).reshape(100, 3, 2)
        self.assertTrue(np.all(p <= population))
        np.testing.assert_array_equal(p.sum(axis=(1, 2)), np.full(100, 50))
        values = study.method_values(p, q)
        summary = study.subsample_result("test", 50, p, q, values)
        self.assertEqual(summary["expanded_only"], 0)
        self.assertEqual(summary["repetitions"], 100)
        self.assertLessEqual(summary["expanded_rejections"], summary["wald_rejections"])

    def test_wilson_bounds_and_json_nonfinite_values(self):
        low, high = study.wilson(0, 5000)
        self.assertAlmostEqual(low, 0, places=12)
        self.assertGreater(high, 0)
        self.assertEqual(study.serializable({"value": np.nan, "array": np.array([1, np.inf])}),
                         {"value": None, "array": [1.0, None]})

    def test_real_data_preparation_counts_and_labels(self):
        frames = study.load_datasets(study.HERE / "raw")
        self.assertEqual(len(frames["Adult"]), 48842)
        self.assertEqual(len(frames["Online Shoppers"]), 12330)
        self.assertEqual(len(frames["Student Performance"]), 649)
        self.assertTrue(frames["Adult"].income.isin(["<=50K", ">50K"]).all())
        items = study.comparisons(frames)
        for item in items:
            self.assertEqual(item["table_p"].shape, item["table_q"].shape)
            self.assertGreater(item["table_p"].sum(), 50)
        self.assertEqual(items[0]["excluded_missing_predictor"], 0)
        self.assertGreater(items[1]["excluded_missing_predictor"], 0)
        self.assertEqual(items[2]["excluded_group_rows"], 85)
        self.assertEqual(items[4]["table_p"].sum()+items[4]["table_q"].sum(), 649)


if __name__ == "__main__":
    unittest.main()
