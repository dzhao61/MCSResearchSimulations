"""Regression checks for the manuscript's sample-size scope."""

import json
import re
import unittest

import pandas as pd

import make_figures as figures


class ReportedScopeTests(unittest.TestCase):
    def test_filter_requires_both_samples(self):
        rows = pd.DataFrame({"n_p": [1, 2, 5, 10, 10, 10, 20],
                             "n_q": [10, 10, 10, 1, 2, 5, 10]})
        retained = figures.reported_rows(rows)
        self.assertEqual(retained.index.tolist(), [6])
        self.assertEqual(len(rows), 7)

    def test_reported_counts_match_independent_selection(self):
        original = pd.read_csv(figures.RESULTS / "display_manifest.csv")
        expected = original.loc[(original.n_p >= 10) & (original.n_q >= 10)]
        pd.testing.assert_frame_equal(figures.DISPLAY, expected)
        self.assertEqual(len(figures.DISPLAY), 3626)
        self.assertEqual(figures.DISPLAY.configuration_id.nunique(), 2760)
        self.assertEqual(figures.DISPLAY.pair_id.nunique(), 534)
        self.assertEqual(figures.DISPLAY.configuration_id.nunique() * figures.REPLICATES,
                         55200000)
        self.assertEqual(len(original), 4001)
        self.assertEqual(original.configuration_id.nunique(), 3111)

    def test_saved_null_table_contains_only_retained_settings(self):
        table = (figures.HERE / "main_null_table.tex").read_text()
        keys = re.findall(
            r"\\\((\d+)\\times(\d+)\\\) & (Uniform|Same skew|Different skew) & (\d+) &",
            table,
        )
        self.assertEqual(len(keys), 84)
        self.assertEqual(len(set(keys)), 84)
        self.assertEqual({int(key[3]) for key in keys}, {10, 20, 50, 100, 250, 500, 1000})

    def test_saved_figures_use_only_retained_configurations(self):
        manifest = json.loads((figures.HERE / "figure_manifest.json").read_text())
        retained = set(figures.DISPLAY.configuration_id)
        self.assertEqual(len(manifest), 22)
        for record in manifest:
            self.assertLessEqual(set(record["configuration_ids"]), retained)

    def test_small_sample_macros_are_absent(self):
        macros = (figures.HERE / "evidence_values.tex").read_text()
        self.assertNotIn("MainFive", macros)
        self.assertNotIn("EightSparseFive", macros)


if __name__ == "__main__":
    unittest.main()
