"""Check manuscript citations and displayed values against the saved evidence."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT.parent / "Thesis Writeup/Welch MI"
sys.path.insert(0, str(ROOT / "experiments"))
from report_formatting import decimal_text


class ThesisConsistencyTests(unittest.TestCase):
    def test_new_identical_population_diagnostics_match_saved_results(self):
        output = ROOT / "results/focused_study"
        configs = pd.read_csv(output / "configuration_manifest.csv")
        diagnostics = pd.read_csv(output / "diagnostics.csv").merge(configs, on="configuration_id")
        for k, n, ratio in ((8, 100, .84), (16, 250, .77)):
            row, = diagnostics[
                diagnostics.k.eq(k) & diagnostics.n_p.eq(n)
                & diagnostics.profile.eq("uniform") & diagnostics.mi_p.eq(.02)
                & diagnostics.mi_q.eq(.02) & diagnostics.construction.eq("copying")
            ].to_dict("records")
            self.assertEqual(round(row["estimated_observed_ratio"], 2), ratio)
            self.assertLess(abs(row["difference_bias"]), 2*row["bias_mcse"])
            self.assertEqual(row["matched_variance_count"], 20000)

    def test_concrete_false_positive_improvements_have_full_validity(self):
        output = ROOT / "results/focused_study"
        configs = pd.read_csv(output / "configuration_manifest.csv")
        rates = pd.read_csv(output / "method_results.csv")
        rates = rates[rates.denominator.eq("all")].merge(configs, on="configuration_id")
        for k, profile, n, expected in (
            (4, "uniform", 20, {"normal_wald": "0.0813", "expanded_welch": "0.0470"}),
            (8, "different_skew", 100, {"normal_wald": "0.0706", "expanded_welch": "0.0518"}),
        ):
            selected = rates[rates.k.eq(k) & rates.n_p.eq(n) & rates.profile.eq(profile)
                             & rates.mi_p.eq(.02) & rates.mi_q.eq(.02)
                             & rates.construction.eq("copying")]
            self.assertEqual(len(selected), 2)
            for row in selected.itertuples():
                self.assertEqual(decimal_text(row.rejection_rate), expected[row.method])
                self.assertEqual(row.valid_replicates, 20000)

    def test_prose_matches_source_derived_rounding(self):
        output = ROOT / "results/focused_study"
        configs = pd.read_csv(output / "configuration_manifest.csv")
        rates = pd.read_csv(output / "method_results.csv")
        rates = rates[rates.denominator.eq("all")].merge(configs, on="configuration_id")
        selected = rates[(rates.k == 8) & rates.profile.eq("uniform")
                         & rates.n_p.eq(100) & rates.mi_p.eq(.02)
                         & rates.mi_q.eq(.02) & rates.method.eq("normal_wald")
                         & rates.construction.eq("copying")]
        self.assertEqual(len(selected), 1)
        row = selected.iloc[0]
        self.assertEqual(row.rejections, 1473)
        self.assertEqual(row.replicates_x, row.replicates_y)
        rate = decimal_text(row.rejections / row.replicates_x)
        appendix = (THESIS / "appendices_rewrite/C_additional_results.tex").read_text()
        self.assertIn(f"give rates\n{rate} and 0.0651", appendix)

        diagnostics = pd.read_csv(output / "diagnostics.csv").merge(configs, on="configuration_id")
        selected = diagnostics[(diagnostics.k == 16)
                               & diagnostics.profile.eq("different_skew")
                               & diagnostics.n_p.eq(1000) & diagnostics.mi_p.eq(.02)
                               & diagnostics.mi_q.eq(.02)
                               & diagnostics.construction.eq("copying")]
        self.assertEqual(len(selected), 1)
        sd = f"{np.sqrt(selected.iloc[0].observed_variance):.5f}"
        results = (THESIS / "chapters_rewrite/06_results.tex").read_text()
        self.assertIn(f"observed SD of approximately {sd}", results)

    def test_active_citations_have_unique_bibliography_entries(self):
        bibliography = (THESIS / "references.bib").read_text()
        keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)", bibliography)
        self.assertEqual(len(keys), len(set(keys)))
        sources = [THESIS / "main.tex"]
        for directory in ("frontmatter", "chapters_rewrite", "appendices_rewrite"):
            sources.extend((THESIS / directory).glob("*.tex"))
        cited = set()
        for source in sources:
            for group in re.findall(r"\\cite\w*\*?(?:\[[^]]*\]){0,2}\{([^}]+)\}",
                                    source.read_text()):
                cited.update(key.strip() for key in group.split(","))
        self.assertTrue(cited)
        self.assertFalse(cited - set(keys), f"Undefined citations: {cited - set(keys)}")


if __name__ == "__main__":
    unittest.main()
