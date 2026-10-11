"""Verify the focused figure data, printed geometry and label bounds."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, t

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import report_focused_study as report


class FocusedReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        output = ROOT / "results/focused_study"
        configs = pd.read_csv(output / "configuration_manifest.csv")
        cls.displays = pd.read_csv(output / "display_manifest.csv", keep_default_na=False)
        rates = pd.read_csv(output / "method_results.csv")
        cls.rates = rates[rates.denominator.eq("all")].merge(configs, on="configuration_id")
        cls.rates["difference"] = -cls.rates.delta
        cls.diagnostics = pd.read_csv(output / "diagnostics.csv").merge(configs, on="configuration_id")
        report.configure_style()

    def select(self, frame, name):
        ids = self.displays.loc[self.displays.study.eq(name), "configuration_id"]
        return frame[frame.configuration_id.isin(ids)]

    def test_null_csv_name_is_not_interpreted_as_missing(self):
        self.assertEqual(self.displays[self.displays.study.eq("null")].configuration_id.nunique(), 120)
        self.assertEqual(len(self.select(self.rates, "null")), 240)

    def check_figure(self, fig):
        self.assertAlmostEqual(fig.get_figwidth()*25.4, 148)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bounds = fig.bbox
        for ax in fig.axes:
            box = ax.get_tightbbox(renderer)
            self.assertGreaterEqual(box.x0, bounds.x0-1)
            self.assertGreaterEqual(box.y0, bounds.y0-1)
            self.assertLessEqual(box.x1, bounds.x1+1)
            self.assertLessEqual(box.y1, bounds.y1+1)
            self.assertEqual(ax.xaxis.label.get_fontsize() in (8, 9), True)
            if ax.get_xlabel():
                label_box = ax.xaxis.label.get_window_extent(renderer)
                for other in fig.axes:
                    if (other is not ax and other.get_title()
                            and other.get_position().y1 < ax.get_position().y0):
                        title_box = other.title.get_window_extent(renderer)
                        self.assertFalse(label_box.overlaps(title_box),
                                         "Upper-panel axis label overlaps lower-panel title.")
        plt.close(fig)

    def test_all_main_and_companion_figure_bounds(self):
        null = self.select(self.rates, "null")
        figures = []
        with patch.object(report, "save", side_effect=lambda fig, *_: figures.append(fig)):
            report.null_figure(null, [(k,"different_skew") for k in (2,4,8,16)], 2, Path("."), "test")
            report.null_figure(null, [(k,p) for k in (4,16) for p in report.PROFILE_NAMES], 3, Path("."), "test")
            report.null_figure(null, [(k,p) for k in (2,8) for p in ("uniform","same_skew")], 2, Path("."), "test")
            report.association_figure(self.select(self.rates,"association"), self.select(self.diagnostics,"association"), Path("."))
            for full in (False, True):
                detection = self.select(self.rates,"detection")
                report.detection_sizes(detection[detection.profile.eq("different_skew")], Path("."), full)
                report.detection_margins(detection[detection.k.eq(4)], Path("."), full)
        self.assertEqual(len(figures), 8)
        for fig in figures:
            self.check_figure(fig)

    def test_rates_plotted_without_rescaling_or_smoothing(self):
        frame = self.select(self.rates,"association")
        frame = frame[frame.n_p.eq(1000)]
        fig, ax = plt.subplots()
        report.draw_rate(ax, frame, "mi_p", .06)
        for method, (_, color, _, _) in report.METHODS.items():
            expected = frame[frame.method.eq(method)].sort_values("mi_p")
            line = next(line for line in ax.lines if line.get_color() == color and len(line.get_xdata()) == 7
                        and line.get_linestyle() != "None")
            np.testing.assert_array_equal(line.get_xdata(), expected.mi_p)
            np.testing.assert_array_equal(line.get_ydata(), expected.rejection_rate)
        plt.close(fig)

    def test_worked_bias_offsets_match_saved_diagnostics(self):
        frame = self.diagnostics
        frame = frame[frame.k.eq(16) & frame.profile.eq("different_skew")
                      & frame.n_p.eq(1000) & frame.mi_p.eq(.02)
                      & frame.mi_q.isin([.02, .03, .04])
                      & frame.construction.eq("copying")].sort_values("mi_q")
        self.assertEqual(len(frame), 3)
        np.testing.assert_allclose(frame.bias_p-frame.bias_q, frame.difference_bias,
                                   atol=1e-14, rtol=1e-12)
        np.testing.assert_array_equal(np.round(frame.difference_bias, 5),
                                      [.02960, .03061, .03164])
        np.testing.assert_array_equal(np.round(frame.delta+frame.difference_bias, 5),
                                      [.02960, .02061, .01164])

    def test_median_df_cutoff_examples(self):
        frame = self.select(self.diagnostics, "association")
        frame = frame[frame.n_p.eq(1000) & frame.mi_p.isin([.0001, .05])].sort_values("mi_p")
        self.assertEqual(len(frame), 2)
        degrees = np.round(frame.df_median.to_numpy(), 2)
        np.testing.assert_array_equal(degrees, [8.62, 78.24])
        cutoffs = t.ppf(.975, degrees)
        np.testing.assert_array_equal(np.round(cutoffs, 3), [2.277, 1.991])
        self.assertEqual(round(norm.ppf(.975), 3), 1.960)
        self.assertGreater(2.1, norm.ppf(.975))
        self.assertLess(2.1, cutoffs[0])
        self.assertGreater(2.1, cutoffs[1])

    def test_margin_precision_example(self):
        frame = self.diagnostics
        frame = frame[frame.k.eq(4) & frame.n_p.eq(10000)
                      & frame.mi_p.eq(.02) & frame.mi_q.eq(.03)
                      & frame.construction.eq("copying")].set_index("profile")
        frame = frame.loc[["uniform", "same_skew", "different_skew"]]
        np.testing.assert_array_equal(np.round(np.sqrt(frame.observed_variance), 5),
                                      [.00327, .00364, .00361])
        self.assertTrue((frame.difference_bias.abs() < .00005).all())
        np.testing.assert_allclose(np.sqrt(frame.mean_estimated_variance),
                                   np.sqrt(frame.observed_variance), rtol=.01)

    def test_construction_table_displays_zero_without_a_minus_sign(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            report.write_supporting_tables(self.diagnostics, self.rates, output)
            table = (output / "focused_construction_table.tex").read_text()
        self.assertNotIn(" & -0 & ", table)
        self.assertEqual(table.count(" & 0 & "), 4)

if __name__ == "__main__":
    unittest.main()
