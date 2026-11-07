"""Check the shopping application and preserve the saved exploratory results."""

import json
import unittest

import numpy as np
import pandas as pd

import run_exploration as study


THESIS = study.WORKSPACE / "Thesis Writeup" / "Welch MI"


@unittest.skipUnless(THESIS.exists(), "Thesis source is supplied separately from the experiment supplement.")
class ShoppersApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = {
            item["id"]: item
            for item in study.comparisons(study.load_datasets(study.HERE / "raw"))
        }
        saved = study.HERE / "results" / "full_data_results.csv"
        if not saved.exists():
            saved = study.HERE / "thesis_application" / "full_data_results.csv"
        cls.saved = pd.read_csv(saved).set_index("id")
        cls.chapter = (THESIS / "chapters_rewrite" / "06_results.tex").read_text()
        cls.application = cls.chapter.split(r"\label{sec:shoppers-application}", 1)[1]

    def test_source_count_tables_and_reported_group_sizes(self):
        saved = study.HERE / "results" / "count_tables.json"
        if not saved.exists():
            saved = study.HERE / "thesis_application" / "count_tables.json"
        archived = {
            item["id"]: item
            for item in json.loads(saved.read_text())
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
            estimates = (
                f"{name} & {actual['corrected_mi_p']:.6f} & {actual['corrected_mi_q']:.6f} & "
                f"{actual['delta_corrected']:.6f} & {actual['standard_error']:.6f} & {actual['statistic']:.3f}"
            )
            decisions = (
                f"{name} & {actual['expanded_welch_degrees_of_freedom']:.2f} & {normal} & {expanded}"
            )
            self.assertIn(estimates, self.application)
            self.assertIn(decisions, self.application)
            self.assertIn(f"{actual['delta_corrected']:.6f}", self.application)
            self.assertIn(f"{actual['standard_error']:.6f}", self.application)
            self.assertIn(f"{actual['statistic']:.3f}", self.application)

    def test_saved_exploratory_adjustment_keeps_original_family(self):
        self.assertEqual(len(self.saved), 6)
        for column in ("normal_p_value", "expanded_welch_p_value"):
            adjusted = study.holm(self.saved[column].tolist())
            index = self.saved.index.get_loc("shoppers_month")
            value = adjusted[index]
            saved_column = "wald_holm_p" if column == "normal_p_value" else "expanded_holm_p"
            self.assertAlmostEqual(value, self.saved.loc["shoppers_month", saved_column], places=12)
            self.assertLess(value, study.ALPHA)

    def test_saved_p_values_match_all_six_source_comparisons(self):
        results = {identifier: study.full_result(item) for identifier, item in self.items.items()}
        identifiers = list(results)
        for column, saved_column in (
            ("normal_p_value", "wald_holm_p"),
            ("expanded_welch_p_value", "expanded_holm_p"),
        ):
            raw = np.array([results[identifier][column] for identifier in identifiers])
            np.testing.assert_allclose(raw, self.saved.loc[identifiers, column], rtol=1e-12, atol=0)
            order = np.argsort(raw)
            values = np.empty_like(raw)
            running = 0.0
            for rank, index in enumerate(order):
                running = max(running, (len(raw) - rank) * raw[index])
                values[index] = min(running, 1.0)
            np.testing.assert_allclose(values, self.saved.loc[identifiers, saved_column], rtol=1e-12, atol=0)

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
        conclusion = (THESIS / "chapters_rewrite" / "07_conclusions.tex").read_text()
        self.assertNotIn("and a real-data application would", conclusion)


if __name__ == "__main__":
    unittest.main()
