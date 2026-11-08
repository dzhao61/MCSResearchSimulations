"""Protect the four-setting construction scope and its matched comparison."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from focused_study_core import build_design, digest, seed_for, simulate_chunk, summarize
from report_focused_mechanisms import population_moments
from report_large_table_construction_check import comparison_rows, table_text
from run_focused_study import audit_records, load_records, run_configuration
from run_large_table_construction_check import (
    DEFAULT_BASE, DEFAULT_OUTPUT, MI_PAIRS, SAMPLE_SIZES, build_construction_design,
)
from run_unequal_sample_check import build_allocation_design
from thesis_redesign_core import margin, mutual_information


class LargeConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs, cls.populations, cls.arrays = build_construction_design()

    def test_exact_scope_and_no_original_setting_changes(self):
        base, _, pairs, _ = build_design()
        self.assertEqual(len(self.configs), 4)
        self.assertEqual(len(self.populations), 2)
        self.assertEqual({(c["mi_p"], c["mi_q"]) for c in self.configs}, set(MI_PAIRS))
        self.assertEqual({c["n_p"] for c in self.configs}, set(SAMPLE_SIZES))
        self.assertTrue({c["configuration_id"] for c in base}.isdisjoint(
            c["configuration_id"] for c in self.configs))
        self.assertTrue({p["pair_id"] for p in pairs}.isdisjoint(p["pair_id"] for p in self.populations))
        for c in self.configs:
            self.assertEqual(c["n_p"], c["n_q"])
            self.assertEqual(c["k"], 16)
            self.assertEqual(c["profile"], "different_skew")
            self.assertEqual(c["construction"], "four_cell")
            self.assertEqual(c["replicates"], 20000)
            self.assertEqual(c["configuration_id"], "setting_"+digest([c["pair_id"], c["n_p"], c["n_q"]])[:16])

    def test_only_first_four_cells_change_and_populations_remain_positive(self):
        change = np.zeros((16, 16))
        change[:2, :2] = [[1, -1], [-1, 1]]
        for population in self.populations:
            for side, rho, table in zip("pq", (.7, .8), self.arrays[population["pair_id"]], strict=True):
                a = margin(16, rho)
                np.testing.assert_allclose(table, np.outer(a, a)+population[f"strength_{side}"]*change,
                                           atol=1e-15, rtol=0)
                self.assertTrue(np.all(table > 0))
                np.testing.assert_allclose(table.sum(axis=0), a, atol=1e-12)
                np.testing.assert_allclose(table.sum(axis=1), a, atol=1e-12)
                self.assertAlmostEqual(mutual_information(table), population[f"mi_{side}"], places=12)
                self.assertLess(population[f"mi_{side}"], population[f"endpoint_mi_{side}"])

    def test_independent_population_moments(self):
        for population in self.populations:
            for side, table in zip("pq", self.arrays[population["pair_id"]], strict=True):
                moments = population_moments(table)
                for field, stored in (("mi", "mi"), ("variance", "variance"),
                                      ("tau2", "variance_sensitivity_variance")):
                    self.assertAlmostEqual(moments[field], population[f"{stored}_{side}"], places=12)

    def test_copying_comparisons_match_controls_but_not_association(self):
        base, _, populations, arrays = build_design()
        lookup = {p["pair_id"]: p for p in populations}
        for c in self.configs:
            matched = [b for b in base if b["k"] == 16 and b["profile"] == c["profile"]
                       and b["construction"] == "copying" and b["mi_p"] == c["mi_p"]
                       and b["mi_q"] == c["mi_q"] and b["n_p"] == c["n_p"]]
            self.assertEqual(len(matched), 1)
            original = matched[0]
            population = next(p for p in self.populations if p["pair_id"] == c["pair_id"])
            for side, new, old in zip("pq", self.arrays[c["pair_id"]], arrays[original["pair_id"]], strict=True):
                np.testing.assert_array_equal(population[f"margin_{side}"], lookup[original["pair_id"]][f"margin_{side}"])
                self.assertFalse(np.allclose(new, old))
            self.assertNotEqual(seed_for("full", c["configuration_id"], 0, "p"),
                                seed_for("full", original["configuration_id"], 0, "p"))

    def test_batching_resume_and_checkpoint_validation(self):
        c = self.configs[0]
        p, q = self.arrays[c["pair_id"]]
        a = simulate_chunk(c, p, q, 0, 43, 43, "test")
        b = simulate_chunk(c, p, q, 0, 43, 7, "test")
        for key in a:
            np.testing.assert_array_equal(a[key], b[key])
        audit_records(c, a)
        with tempfile.TemporaryDirectory() as temp:
            first = run_configuration((c, p, q, temp, 43, 7, "test", "construction-test"))
            second = run_configuration((c, p, q, temp, 43, 43, "test", "construction-test"))
            self.assertEqual(first["resumed_replicates"], 0)
            self.assertEqual(second["resumed_replicates"], 43)
            stored = load_records(Path(temp)/c["configuration_id"], 43)
            for key in a:
                np.testing.assert_array_equal(stored[key], a[key])
            with self.assertRaises(RuntimeError):
                run_configuration((c, p, q, temp, 43, 43, "test", "different-identity"))

    def test_summary_bias_and_paired_subset(self):
        populations = {p["pair_id"]: p for p in self.populations}
        for c in self.configs:
            records = simulate_chunk(c, *self.arrays[c["pair_id"]], 0, 100, 20, "test")
            _, paired, diagnostic = summarize(c, populations[c["pair_id"]], records)
            self.assertAlmostEqual(diagnostic["difference_bias"], diagnostic["bias_p"]-diagnostic["bias_q"])
            self.assertTrue(all(row["only_expanded"] == 0 for row in paired))
            self.assertEqual(diagnostic["finite_difference_count"], 100)

    def test_combined_scope_without_duplicate_balanced_settings(self):
        base, _, populations, _ = build_design()
        allocation, _, _ = build_allocation_design()
        ids = {c["configuration_id"] for c in base+allocation+self.configs}
        pair_ids = {c["pair_id"] for c in base+allocation+self.configs}
        self.assertEqual(len(ids), 240)
        self.assertEqual(len(pair_ids), 70)
        self.assertEqual(len(ids)*20000, 4800000)

    def test_all_matched_rows_reported_with_saved_counts(self):
        rows = comparison_rows(DEFAULT_BASE, DEFAULT_OUTPUT)
        self.assertEqual(len(rows), 8)
        expected = {("copying", 1000, .02): (5044, 4804),
                    ("copying", 10000, .02): (925, 905),
                    ("copying", 1000, .03): (2010, 1906),
                    ("copying", 10000, .03): (13984, 13935),
                    ("four_cell", 1000, .02): (6189, 5954),
                    ("four_cell", 10000, .02): (998, 982),
                    ("four_cell", 1000, .03): (2494, 2351),
                    ("four_cell", 10000, .03): (12646, 12593)}
        for row in rows:
            w, e = expected[(row["construction"], row["n"], row["mi_q"])]
            self.assertEqual(row["wald"]["rejections"], w)
            self.assertEqual(row["expanded"]["rejections"], e)
            self.assertEqual(row["wald"]["valid_replicates"], 20000)
            self.assertEqual(row["expanded"]["valid_replicates"], 20000)
            self.assertEqual(row["diagnostics"]["matched_variance_count"], 20000)

    def test_direction_counts_and_denominators_are_independently_recomputed(self):
        rows = comparison_rows(DEFAULT_BASE, DEFAULT_OUTPUT)
        for row in rows:
            if row["delta"] == 0:
                self.assertNotIn("wald_direction", row)
                self.assertNotIn("expanded_direction", row)
                continue
            directory = DEFAULT_BASE if row["construction"] == "copying" else DEFAULT_OUTPUT
            records = load_records(directory / "records" / row["configuration_id"], 20000)
            for name, valid, p_value in (("wald", "base_valid", "normal_p_value"),
                                         ("expanded", "expanded_valid", "expanded_welch_p_value")):
                mask = records[valid] & (records[p_value] <= .05)
                opposite = np.count_nonzero(mask & (records["delta_corrected"] > 0))
                direction = row[name+"_direction"]
                self.assertEqual(direction["opposite_sign"], opposite)
                self.assertAlmostEqual(direction["opposite_fraction_among_rejections"], opposite/mask.sum())
                self.assertEqual(direction["correct_sign"], 1 if row["n"] == 1000 else mask.sum())
                self.assertEqual(direction["zero_sign"], 0)

    def test_diagnostic_values_and_added_interpretation(self):
        rows = comparison_rows(DEFAULT_BASE, DEFAULT_OUTPUT)
        selected = {(r["construction"], r["n"], r["mi_q"]): r for r in rows}
        null = selected[("four_cell", 1000, .02)]["diagnostics"]
        alternative = selected[("four_cell", 1000, .03)]["diagnostics"]
        self.assertEqual(f"{null['difference_bias']:.5f}", "0.03145")
        self.assertEqual(f"{alternative['difference_bias']:.5f}", "0.03136")
        self.assertEqual(f"{-.01+alternative['difference_bias']:.5f}", "0.02136")
        for row in rows:
            d = row["diagnostics"]
            self.assertAlmostEqual(d["bias_mcse"], np.sqrt(d["observed_variance"]/20000), places=12)
            self.assertAlmostEqual(d["difference_bias"], d["bias_p"]-d["bias_q"], places=12)
        source = ROOT.parent / "Thesis Writeup/Welch MI"
        if source.exists():
            design = (source / "chapters_rewrite/05_experimental_design.tex").read_text()
            self.assertIn("104 population pairs and 312 distinct settings", design)
            self.assertIn("6,240,000 table pairs", design)
            result = (source / "chapters_rewrite/06_results.tex").read_text()
            for value in ("0.03145", "0.3095", "0.2977", "2,493 of 2,494", "2,350 of 2,351"):
                self.assertIn(value, result)

    def test_generated_table_contains_all_comparisons_and_precise_rounding(self):
        rows = comparison_rows(DEFAULT_BASE, DEFAULT_OUTPUT)
        generated = table_text(rows)
        self.assertEqual(generated.count("100.0/100.0"), 8)
        self.assertIn("0.3095 [", generated)
        self.assertIn("0.1176 [", generated)
        self.assertIn("99.96/99.96", generated)
        self.assertIn("0.00011", generated)
        path = ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite/focused_large_construction_table.tex"
        if path.exists():
            self.assertEqual(path.read_text(), generated)


if __name__ == "__main__":
    unittest.main()
