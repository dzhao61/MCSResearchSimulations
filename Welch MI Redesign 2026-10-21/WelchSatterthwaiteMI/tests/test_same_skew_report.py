"""Verify the matched-skew manuscript evidence and printed figure selections."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import report_same_skew_extension as report
from run_focused_study import load_records
from same_skew_extension_core import DEFAULT_OUTPUT, combined_frames, directories

THESIS = ROOT.parent / "Thesis Writeup/Welch MI"
EVIDENCE = THESIS / "figures_rewrite/focused_same_skew_evidence.json"


class FormattingTests(unittest.TestCase):
    def test_signed_bias_never_prints_negative_zero(self):
        self.assertEqual(report.bias_text(-.0000049), "0.00000")
        self.assertEqual(report.bias_text(.000005), "+0.00001")
        self.assertEqual(report.bias_text(-.000005), "-0.00001")


@unittest.skipUnless(EVIDENCE.exists(), "Separately supplied manuscript evidence is absent")
class SameSkewReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads(EVIDENCE.read_text())
        cls.lookup = {r["configuration_id"]: r for r in cls.rows}

    def test_evidence_covers_all_unique_settings_and_validity_denominators(self):
        self.assertEqual(len(self.rows), 312)
        self.assertEqual(len(self.lookup), 312)
        self.assertEqual(len([r for r in self.rows if r["origin"] == "same_skew_extension"]), 72)
        for r in self.rows:
            for name in ("wald", "expanded"):
                method = r[name]
                self.assertEqual(method["replicates"], 20000)
                self.assertAlmostEqual(method["rejection_rate"], method["rejections"]/20000)
                self.assertAlmostEqual(method["valid_rate"], method["valid_replicates"]/20000)
            self.assertEqual(r["diagnostics"]["degrees_of_freedom_count"], r["expanded"]["valid_replicates"])
            self.assertAlmostEqual(r["median_df_student_t_cutoff"], t.ppf(.975, r["diagnostics"]["df_median"]))

    def test_table_fragments_regenerate_exactly(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            for writer in (report.write_association_table, report.write_construction_table,
                           report.write_allocation_table, report.write_df_table):
                writer(self.rows, output)
            files = list(output.glob("*.tex"))
            self.assertEqual(len(files), 4)
            for path in files:
                text = path.read_text()
                self.assertEqual(text, (THESIS / "figures_rewrite" / path.name).read_text())
                self.assertNotIn("-0.00000", text)

    def test_mi_figure_has_both_regimes_at_each_sample_size(self):
        frames = combined_frames()
        ids = frames["displays"].loc[frames["displays"].study.eq("association"), "configuration_id"]
        rates = frames["method_results"].query("denominator == 'all'").merge(frames["configurations"], on="configuration_id")
        diagnostics = frames["diagnostics"].merge(frames["configurations"], on="configuration_id")
        with patch.object(report, "save") as save:
            report.configure_style()
            report.association_figure(rates[rates.configuration_id.isin(ids)],
                                      diagnostics[diagnostics.configuration_id.isin(ids)], Path("."))
            fig = save.call_args.args[0]
            self.assertEqual(len(fig.axes), 4)
            for ax, n in zip(fig.axes[:2], (100, 1000), strict=True):
                curves = ax.lines[:4]
                self.assertEqual(len(curves), 4)
                self.assertEqual({curve.get_marker() for curve in curves}, {"o", "^"})
                for curve in curves:
                    self.assertEqual(len(curve.get_xdata()), 7)
                    self.assertEqual(curve.get_markerfacecolor(), curve.get_color())
            for ax in fig.axes[2:]:
                self.assertEqual(len(ax.lines), 2)
                for curve in ax.lines:
                    self.assertEqual(len(curve.get_xdata()), 7)
            report.plt.close(fig)

    def test_sparse_same_skew_counts_and_direction_match_saved_records(self):
        selected = [r for r in self.rows if r["profile"] == "same_skew" and r["k"] == 16
                    and r["construction"] == "copying" and r["mi_q"] == .03 and r["n_p"] == 1000]
        self.assertEqual(len(selected), 1)
        r = selected[0]
        records = load_records(directories()[r["origin"]] / "records" / r["configuration_id"], 20000)
        for name, valid, p_value, total, opposite in (
            ("wald", "base_valid", "normal_p_value", 370, 14),
            ("expanded", "expanded_valid", "expanded_welch_p_value", 339, 12),
        ):
            mask = records[valid] & (records[p_value] <= .05)
            self.assertEqual(mask.sum(), total)
            self.assertEqual(np.count_nonzero(mask & (records["delta_corrected"] > 0)), opposite)
            self.assertEqual(r[name+"_direction"]["opposite_sign"], opposite)

    def test_redesign_preserves_matched_same_skew_coverage(self):
        fresh = ROOT / "results/approximation_redesign"
        configs = pd.read_csv(fresh / "configurations.csv")
        display = pd.read_csv(fresh / "displays.csv", keep_default_na=False)
        self.assertEqual(len(configs), 366)
        self.assertTrue(configs.replicates.eq(100000).all())
        for study, count in (("null", 120), ("association", 63), ("construction", 32), ("allocation", 12)):
            ids = set(display[display.study.eq(study)].configuration_id)
            self.assertEqual(len(ids), count)
            selected = configs[configs.configuration_id.isin(ids)]
            self.assertTrue(selected.profile.eq("same_skew").any())
            self.assertTrue(selected.profile.eq("different_skew").any())
        for name in ("focused_redesign_moments_same_skew", "focused_redesign_null_same_skew",
                     "focused_redesign_broad_power_same_skew", "focused_redesign_allocation"):
            self.assertIn(name, (THESIS / "appendices_rewrite/C_additional_results.tex").read_text())



if __name__ == "__main__":
    unittest.main()
