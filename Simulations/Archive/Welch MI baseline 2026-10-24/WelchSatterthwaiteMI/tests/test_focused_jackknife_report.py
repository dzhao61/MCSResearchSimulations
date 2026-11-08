"""Protect the compact table and bounded interpretation of the jackknife check."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT.parent/"Thesis Writeup/Welch MI"
sys.path.insert(0, str(ROOT/"experiments"))
import report_focused_jackknife_check as report
from report_formatting import decimal_text
from run_focused_jackknife_check import DEFAULT_OUTPUT


class JackknifeReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = report.checked_evidence(DEFAULT_OUTPUT)

    def test_table_contains_all_eight_rows_and_exact_rate_rounding(self):
        text = report.table_text(self.evidence)
        for row in self.evidence["estimators"]:
            expected = decimal_text(row['rejection']['count']/row['repetitions'])
            self.assertIn(expected+r"\\", text)
        self.assertEqual(text.count(" & Analytic & "), 4)
        self.assertEqual(text.count(" & Jackknife & "), 4)
        self.assertNotIn("-0.00 &", text)

    def test_exported_evidence_and_table_match_verified_records(self):
        figures = THESIS/"figures_rewrite"
        if not figures.exists():
            self.skipTest("Thesis source is a separate delivered archive.")
        self.assertEqual((figures/"focused_jackknife_table.tex").read_text(),
                         report.table_text(self.evidence))
        self.assertEqual(json.loads((figures/"focused_jackknife_evidence.json").read_text()),
                         self.evidence)

    def test_bias_variance_identity_and_rejection_direction(self):
        for row in self.evidence["estimators"]:
            self.assertAlmostEqual(row["bias"]["mean"], row["bias_p"]["mean"]-row["bias_q"]["mean"])
            expected_mse = row["bias"]["mean"]**2 + row["observed_sd"]**2*(20000-1)/20000
            self.assertAlmostEqual(row["rmse"]**2, expected_mse)
            if row["true_delta"] != 0:
                self.assertEqual(row["rejection"]["count"],
                                 row["correct_direction"]["count"]+row["opposite_direction"]["count"])

    def test_main_text_only_points_to_bounded_appendix_check(self):
        if not (THESIS/"main.tex").exists():
            self.skipTest("Thesis source is a separate delivered archive.")
        for chapter in ("05_experimental_design", "06_results"):
            self.assertIn(r"\ref{sec:jackknife-difference-check}",
                          (THESIS/f"chapters_rewrite/{chapter}.tex").read_text())
        for chapter in ("03_problem_baselines", "04_expanded_welch"):
            self.assertNotIn("jackknife", (THESIS/f"chapters_rewrite/{chapter}.tex").read_text().lower())
        results = (THESIS/"chapters_rewrite/06_results.tex").read_text()
        paragraph = next(part for part in results.split("\n\n")
                         if r"\ref{sec:jackknife-difference-check}" in part)
        paragraph = " ".join(paragraph.split())
        self.assertIn("Wald's analytic MI bias correction", paragraph)
        self.assertIn("existing standard error", paragraph)
        self.assertIn("standard normal distribution cutoff", paragraph)

    def test_appendix_prose_matches_record_based_biases_and_intervals(self):
        if not (THESIS/"main.tex").exists():
            self.skipTest("Thesis source is a separate delivered archive.")
        source = (THESIS/"appendices_rewrite/C_additional_results.tex").read_text()
        section = source.split(r"\label{sec:jackknife-difference-check}", 1)[1].split(
            r"\section{Power over the full MI-difference range}", 1)[0]
        rows = self.evidence["estimators"]
        for row in rows:
            if row["n"] == 1000 and row["method"] == "jackknife_fixed_se_normal":
                for side in "pq":
                    self.assertIn(f"{row[f'bias_{side}']['mean']:.5f}", section)
            if row["method"] == "jackknife_fixed_se_normal" and row["true_delta"] == 0:
                rate = row["rejection"]
                self.assertIn(decimal_text(rate['rate']), section)
                self.assertIn(f"[{decimal_text(rate['low'])}, {decimal_text(rate['high'])}]", section)
            if row["n"] == 1000:
                self.assertIn(f"{row['rmse']:.5f}", section)
        self.assertIn("biases largely cancel", section)
        self.assertIn("standard error still exceeds", section)


if __name__ == "__main__":
    unittest.main()
