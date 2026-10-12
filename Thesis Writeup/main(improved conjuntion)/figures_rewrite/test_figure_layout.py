"""Regression checks for printed figure geometry, typography and data."""

import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np

import make_figures as figures


class FigureLayoutTests(unittest.TestCase):
    def setUp(self):
        self.rows = figures.subset(
            "main", shape="2x2", profile="uniform", n_p=100, n_q=100,
        )

    def tearDown(self):
        plt.close("all")

    def check_typography(self, fig):
        for ax in fig.axes:
            self.assertEqual(ax.title.get_fontsize(), 9)
            for label in (ax.xaxis.label, ax.yaxis.label):
                if label.get_text():
                    self.assertEqual(label.get_fontsize(), 9)
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                self.assertEqual(tick.get_fontsize(), 8)
            for line in ax.lines[:2]:
                self.assertEqual(line.get_linewidth(), 1.25)
                self.assertEqual(line.get_markersize(), 3.5)
        for legend in fig.legends:
            for label in legend.get_texts():
                self.assertEqual(label.get_fontsize(), 9)
        figures.check_layout(fig)

    def test_fixed_physical_dimensions(self):
        for rows_count in (1, 2):
            for columns, width_mm in ((1, 85), (2, 116), (3, 142)):
                with self.subTest(rows=rows_count, columns=columns):
                    fig, axes = figures.figure_axes(rows_count, columns)
                    self.assertAlmostEqual(fig.get_figwidth() * 25.4, width_mm)
                    for ax in axes.flat:
                        printed_height = ax.get_position().height * fig.get_figheight() * 25.4
                        self.assertAlmostEqual(printed_height, 34)

    def test_exported_pdf_dimensions(self):
        records = json.loads((figures.HERE / "figure_manifest.json").read_text())
        self.assertEqual(len(records), 22)
        for record in records:
            name = Path(record["file"]).name
            with self.subTest(figure=name):
                if name.startswith("broad_"):
                    width_mm, height_mm = 85, 67
                elif name.startswith(("imbalance_", "rectangular_", "construction_", "convergence")):
                    width_mm, height_mm = 116, 117
                else:
                    width_mm, height_mm = 142, 117
                box = re.search(
                    rb"/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]",
                    (figures.HERE / name).read_bytes(),
                )
                self.assertIsNotNone(box)
                self.assertAlmostEqual(float(box[1]) * 25.4 / 72, width_mm, places=5)
                self.assertAlmostEqual(float(box[2]) * 25.4 / 72, height_mm, places=5)

    def test_latex_preserves_native_sizes(self):
        for relative in ("chapters_rewrite/06_results.tex", "appendices_rewrite/C_additional_results.tex"):
            source = (figures.HERE.parent / relative).read_text()
            self.assertNotRegex(source, r"\\includegraphics\[")

    def test_comparison_templates_share_typography(self):
        for columns in (1, 2, 3):
            with self.subTest(columns=columns):
                panels = [(f"Panel {i + 1}", self.rows) for i in range(columns)]
                with patch.object(figures, "save") as save:
                    figures.grid("test", panels, zoom=None if columns == 1 else 0.15)
                self.check_typography(save.call_args.args[1])

    def test_convergence_uses_the_same_template(self):
        with patch.object(figures, "save") as save:
            figures.convergence()
        fig = save.call_args.args[1]
        self.assertAlmostEqual(fig.get_figwidth() * 25.4, 116)
        self.check_typography(fig)

    def test_draw_preserves_both_method_curves(self):
        fig, axes = figures.figure_axes(1, 1)
        ax = axes[0, 0]
        figures.draw(ax, self.rows)
        for line, method in zip(ax.lines[:2], ("normal_wald", "expanded_welch")):
            expected = self.rows.loc[self.rows.method.eq(method)].sort_values("x_value")
            np.testing.assert_array_equal(line.get_xdata(), expected.x_value)
            np.testing.assert_array_equal(line.get_ydata(), expected.unconditional_rejection_rate)
        np.testing.assert_array_equal(ax.lines[2].get_ydata(), [0.05, 0.05])
        self.assertEqual(ax.get_ylim(), (0, 1))

    def test_small_difference_labels_fit(self):
        rows = figures.subset(
            "extreme", shape="3x3", dominant_p=0.999,
            dominant_q=0.9995, n_p=100, n_q=100,
        )
        with patch.object(figures, "save") as save:
            figures.grid("test", [("P 0.999\nQ 0.9995", rows)] * 3)
        self.check_typography(save.call_args.args[1])

    def test_layout_rejects_clipped_labels(self):
        fig, axes = figures.figure_axes(1, 1)
        axes[0, 0].set_xlabel("A label too long for this fixed figure canvas " * 3)
        with self.assertRaisesRegex(ValueError, "outside the fixed canvas"):
            figures.check_layout(fig)

    def test_layout_rejects_crowded_ticks(self):
        fig, axes = figures.figure_axes(1, 3)
        ax = axes[0, 0]
        ax.set_xticks(np.linspace(0, 1, 15))
        ax.set_xticklabels(["0.0001"] * 15)
        with self.assertRaisesRegex(ValueError, "Overlapping x-axis"):
            figures.check_layout(fig)


if __name__ == "__main__":
    unittest.main()
