"""Check manuscript citations and displayed values against the saved evidence."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT.parent / "Thesis Writeup/Welch MI"


class ThesisConsistencyTests(unittest.TestCase):
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
        rate = f"{row.rejections / row.replicates_x:.4f}"
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
