"""Regression checks for the thesis's self-contained shopping application."""

import json
import unittest

import numpy as np
import pandas as pd

import run_exploration as study


THESIS = study.WORKSPACE / "Thesis Writeup" / "Welch MI"


class ShoppersApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = {
            item["id"]: item
            for item in study.comparisons(study.load_datasets(study.HERE / "raw"))
        }
        cls.saved = pd.read_csv(study.HERE / "results" / "full_data_results.csv").set_index("id")
        cls.chapter = (THESIS / "chapters_rewrite" / "06_results.tex").read_text()
        cls.application = cls.chapter.split("\\section{Application to Online Shopping Data}", 1)[1]

    def test_source_count_tables_and_reported_group_sizes(self):
        archived = {
            item["id"]: item
            for item in json.loads((study.HERE / "results" / "count_tables.json").read_text())
        }
        for identifier in ("shoppers_month", "shoppers_weekend"):
            item = self.items[identifier]
            np.testing.assert_array_equal(item["table_p"], archived[identifier]["table_p"])
            np.testing.assert_array_equal(item["table_q"], archived[identifier]["table_q"])
            self.assertEqual(int(item["table_p"].sum()), 1694)
            self.assertEqual(int(item["table_q"].sum()), 10551)
            self.assertEqual(item["excluded_group_rows"], 85)
            self.assertEqual(item["excluded_missing_predictor"], 0)
        month = self.items["shoppers_month"]
        self.assertEqual(month["table_p"].shape, (10, 2))
        self.assertEqual(np.count_nonzero(month["table_p"] == 0), 1)
        self.assertFalse(np.any(month["table_p"].sum(axis=1) == 0))
        np.testing.assert_array_equal(month["table_p"][month["levels"].index("Feb")], [1, 0])
        for group in ("table_p", "table_q"):
            self.assertTrue(np.all(self.items["shoppers_weekend"][group] > 0))

    def test_table_rows_match_independently_recomputed_values(self):
        for identifier, name in (("shoppers_month", "Month"), ("shoppers_weekend", "Weekend")):
            item = self.items[identifier]
            actual = study.full_result(item)
            for key in study.independent_values(item["table_p"], item["table_q"]):
                np.testing.assert_allclose(actual[key], self.saved.loc[identifier, key], rtol=1e-11, atol=1e-12)
            if identifier == "shoppers_month":
                normal = rf"\({actual['normal_p_value'] * 1e5:.2f}\times10^{{-5}}\)"
                expanded = rf"\({actual['expanded_welch_p_value'] * 1e4:.2f}\times10^{{-4}}\)"
            else:
                normal = f"{actual['normal_p_value']:.4f}"
                expanded = f"{actual['expanded_welch_p_value']:.4f}"
            expected = (
                f"{name} & {actual['corrected_mi_p']:.6f} & {actual['corrected_mi_q']:.6f} & "
                f"{actual['expanded_welch_degrees_of_freedom']:.2f} & {normal} & {expanded}"
            )
            self.assertIn(expected, self.application)
            self.assertIn(f"{actual['delta_corrected']:.6f}", self.application)
            self.assertIn(f"{actual['standard_error']:.6f}", self.application)
            self.assertIn(f"{actual['statistic']:.3f}", self.application)

    def test_holm_adjustment_keeps_original_six_comparison_family(self):
        self.assertEqual(len(self.saved), 6)
        for column in ("normal_p_value", "expanded_welch_p_value"):
            adjusted = study.holm(self.saved[column].tolist())
            index = self.saved.index.get_loc("shoppers_month")
            value = adjusted[index]
            saved_column = "wald_holm_p" if column == "normal_p_value" else "expanded_holm_p"
            self.assertAlmostEqual(value, self.saved.loc["shoppers_month", saved_column], places=12)
            self.assertIn(f"{value:.3g}", self.application)
            self.assertLess(value, study.ALPHA)
        self.assertIn("six comparisons across three public datasets", self.application)
        self.assertIn("\\citep{holm1979}", self.application)

    def test_application_stays_together_and_citations_are_defined(self):
        self.assertNotIn("\\subsection", self.application)
        self.assertNotIn("\\ref{chap:design}", self.application)
        self.assertNotIn("\\ref{app:", self.application)
        self.assertNotIn("subsample", self.application.lower())
        self.assertIn("\\label{tab:shoppers-application}", self.application)
        bibliography = (THESIS / "references.bib").read_text()
        self.assertIn("@misc{sakar2018,", bibliography)
        self.assertIn("10.24432/C5F88Q", bibliography)
        self.assertIn(study.SOURCES["Online Shoppers"]["page"], bibliography)
        self.assertIn("@article{holm1979,", bibliography)
        conclusion = (THESIS / "chapters_rewrite" / "08_conclusion.tex").read_text()
        self.assertNotIn("and a real-data application would", conclusion)


if __name__ == "__main__":
    unittest.main()
