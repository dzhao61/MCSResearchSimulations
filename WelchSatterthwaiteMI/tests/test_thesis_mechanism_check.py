"""Integrity checks for the post-review explanatory follow-up."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "thesis_mechanism_check"
SOURCE = ROOT / "results" / "thesis_redesign"


class ThesisMechanismCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rates = pd.read_csv(RESULTS / "ablation_rates.csv")
        cls.components = pd.read_csv(RESULTS / "component_diagnostics.csv")
        cls.diagnostics = pd.read_csv(RESULTS / "denominator_diagnostics.csv")
        cls.selected = pd.read_csv(RESULTS / "selected_displays.csv")
        cls.metadata = json.loads((RESULTS / "metadata.json").read_text())

    def test_complete_unique_selection(self) -> None:
        self.assertEqual(self.metadata["configurations"], 809)
        self.assertEqual(self.selected.configuration_id.nunique(), 809)
        self.assertEqual(len(self.rates), 809 * 6)
        self.assertEqual(self.diagnostics.configuration_id.nunique(), 169)
        self.assertEqual(len(self.components), 2 * 169)
        self.assertTrue(self.rates.replicates.eq(20000).all())

    def test_sources_are_the_frozen_inputs(self) -> None:
        for name, expected in self.metadata["source_sha256"].items():
            actual = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected)

    def test_rates_and_validity_are_well_formed(self) -> None:
        self.assertTrue(self.rates.rate.between(0, 1).all())
        self.assertTrue(self.rates.valid_rate.between(0, 1).all())
        self.assertTrue((self.rates.rejected <= self.rates.valid).all())
        self.assertTrue((self.rates.valid <= self.rates.replicates).all())
        self.assertTrue(np.isfinite(self.rates.rate_mcse).all())

    def test_reference_only_methods_are_nested_within_wald(self) -> None:
        pivot = self.rates.pivot(
            index="configuration_id", columns="method", values="rate"
        )
        for method in ("hutcheson_welch", "simple_welch", "kurtosis_welch", "expanded_welch"):
            self.assertTrue((pivot[method] <= pivot.normal_wald + 1e-15).all())
        self.assertTrue(
            (pivot.simple_welch <= pivot.hutcheson_welch + 1e-15).all()
        )

    def test_reported_anchor_values(self) -> None:
        row = self.diagnostics.loc[
            self.diagnostics.configuration_id.eq("config_f67e74127a56dc37")
        ].iloc[0]
        self.assertAlmostEqual(row.normal_wald_rate, 0.01660)
        self.assertAlmostEqual(row.independent_mc_sd_rate, 0.05510)
        self.assertAlmostEqual(row.population_first_order_sd_rate, 0.09760)
        self.assertAlmostEqual(row.mean_se2_over_empirical_var, 1.169852, places=6)
        self.assertAlmostEqual(row.empirical_var_over_first_order, 1.424926, places=6)


if __name__ == "__main__":
    unittest.main()
