"""Design coverage and numerical/evidence checks for the fixed-gap power study."""
import json
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
from scipy.stats import binomtest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import fixed_gap_power_study as study
from focused_study_core import evaluate_tables


class FixedGapPowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs, cls.pops, cls.arrays = study.build_design()

    def test_grid_matches_submitted_broad_null_grid(self):
        root = study.ROOT / "results/approximation_redesign"
        old = pd.read_csv(root / "configurations.csv")
        display = pd.read_csv(root / "displays.csv", keep_default_na=False)
        ids = set(display[display.study.eq("null")].configuration_id)
        null = old[old.configuration_id.isin(ids)]
        self.assertEqual(len(null), 120)
        expected = set(zip(null.k, null.profile, null.n_p, null.n_q))
        actual = {(c["k"], c["profile"], c["n_p"], c["n_q"]) for c in self.configs}
        self.assertEqual(len(actual), 120)
        self.assertEqual(actual, expected)
        self.assertTrue(all(c["mi_p"] == .02 and c["mi_q"] == .03 and
                            c["delta"] == -.01 for c in self.configs))

    def test_population_targets_and_margins(self):
        for pop in self.pops.values():
            for side in "pq":
                p = np.array(pop["probability_" + side])
                self.assertTrue((p > 0).all())
                np.testing.assert_allclose(p.sum(0), pop["margin_" + side], atol=1e-12)
                np.testing.assert_allclose(p.sum(1), pop["margin_" + side], atol=1e-12)
                self.assertAlmostEqual(pop["achieved_mi_" + side], pop["mi_" + side], places=10)

    def test_sampling_streams_and_batches(self):
        c = next(c for c in self.configs if c["k"] == 16 and c["n_p"] == 1000)
        for side, p in zip("pq", self.arrays[c["pair_id"]], strict=True):
            seed = study.seed_for(c["configuration_id"], 0, side)
            rng = np.random.default_rng(seed)
            a = rng.multinomial(c["n_p"], p.ravel(), size=32)
            rng = np.random.default_rng(seed)
            b = np.concatenate([rng.multinomial(c["n_p"], p.ravel(), size=8) for _ in range(4)])
            np.testing.assert_array_equal(a, b)
        self.assertNotEqual(study.seed_for(c["configuration_id"], 0, "p"),
                            study.seed_for(c["configuration_id"], 0, "q"))
        self.assertNotEqual(study.seed_for(c["configuration_id"], 0, "p"),
                            study.seed_for(c["configuration_id"], 1, "p"))

    def test_scalar_check_covers_sparse_and_constant_score_tables(self):
        p = np.array([[[3, 0], [0, 3]], [[3, 1], [2, 0]], [[1, 2], [1, 2]]])
        q = np.array([[[2, 0], [1, 3]], [[0, 4], [2, 0]], [[3, 1], [1, 1]]])
        self.assertEqual(study.check_scalar(p, q, evaluate_tables(p, q)), 3)

    def test_complete_saved_rates_and_wilson_intervals(self):
        if not (study.OUTPUT / "audit.json").exists():
            self.skipTest("Full study has not run")
        audit = json.loads((study.OUTPUT / "audit.json").read_text())
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["pairs"], 12000000)
        self.assertEqual(audit["independently_reconstructed_pairs"], 960)
        rates = pd.read_csv(study.OUTPUT / "rates.csv")
        rates = rates[rates.denominator.eq("all")]
        self.assertEqual(len(rates), 240)
        for row in rates.itertuples():
            interval = binomtest(row.rejections, row.replicates).proportion_ci(method="wilson")
            self.assertAlmostEqual(row.rejection_low, interval.low, places=12)
            self.assertAlmostEqual(row.rejection_high, interval.high, places=12)
        pairs = pd.read_csv(study.OUTPUT / "paired.csv")
        pairs = pairs[pairs.denominator.eq("all")]
        self.assertTrue(pairs.only_expanded.eq(0).all())
        np.testing.assert_array_equal(pairs.only_wald + pairs.only_expanded +
                                     pairs.both_reject + pairs.neither_reject, 100000)

    def test_new_manuscript_numerical_anchors_match_evidence(self):
        thesis = study.ROOT.parent / "Thesis Writeup/Welch MI"
        source = thesis / "chapters_rewrite/06_results.tex"
        if not source.exists() or not (study.OUTPUT / "audit.json").exists():
            self.skipTest("Manuscript or completed study is absent")
        text = source.read_text()
        rates = pd.read_csv(study.OUTPUT / "rates.csv")
        rates = rates[rates.denominator.eq("all") & rates.method.eq("expanded_welch")]
        for profile, k, n in [("uniform", 2, 10000), ("uniform", 16, 10000),
                              ("same_skew", 16, 10000), ("same_skew", 16, 1000),
                              ("different_skew", 16, 1000), ("different_skew", 16, 2500)]:
            row, = rates[rates.profile.eq(profile) & rates.k.eq(k) & rates.n_p.eq(n)].to_dict("records")
            self.assertIn(f'{100*row["rejection_rate"]:.2f}\\%', text)
        diag = pd.read_csv(study.OUTPUT / "diagnostics.csv")
        row, = diag[diag.profile.eq("different_skew") & diag.k.eq(16) & diag.n_p.eq(1000)].to_dict("records")
        self.assertIn(f'{row["difference_bias"]:.4f}', text)
        self.assertIn(f'+{row["difference_bias"]-.01:.4f}', text)
        self.assertGreater(row["expanded_positive_rejections"] /
                           (row["expanded_positive_rejections"]+row["expanded_negative_rejections"]), .999)
        pairs = pd.read_csv(study.OUTPUT / "paired.csv")
        pairs = pairs[pairs.denominator.eq("all")]
        self.assertLess(100*pairs[pairs.n_p.eq(10000)].difference.max(), .32)
        self.assertGreater(rates[rates.n_p.eq(50000)].rejection_rate.min(), .999)


if __name__ == "__main__":
    unittest.main()
