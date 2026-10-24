from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from focused_study_core import (
    COMMON_MI, DIFFERENCES, PROFILES, SAMPLE_SIZES, TOLERANCES,
    build_design, construct_copying, evaluate_tables, margin, mutual_information,
    seed_for, simulate_chunk, summarize,
)
from thesis_redesign_core import construct_additive
from run_focused_study import audit_records, load_records, run_configuration
from welch_differential_mi import differential_mi_pvalues


class FocusedDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs, cls.displays, cls.populations, cls.arrays = build_design()

    def test_counts_and_reuse(self):
        self.assertEqual(len(self.configs), 232)
        self.assertEqual(len(self.populations), 68)
        self.assertEqual(len(self.displays), 246)
        self.assertEqual(len({c["configuration_id"] for c in self.configs}), 232)
        for study, count in (("null", 120), ("association", 14), ("detection", 108), ("construction", 4)):
            self.assertEqual(sum(d["study"] == study for d in self.displays), count)
        null_ids = {d["configuration_id"] for d in self.displays if d["study"] == "null"}
        for study, overlaps in (("association", 2), ("detection", 12)):
            ids = {d["configuration_id"] for d in self.displays if d["study"] == study}
            self.assertEqual(len(ids & null_ids), overlaps)

    def test_exact_grids(self):
        lookup = {c["configuration_id"]: c for c in self.configs}
        for study, field, expected in (("null", "n_p", SAMPLE_SIZES), ("association", "mi_p", COMMON_MI)):
            records = [lookup[d["configuration_id"]] for d in self.displays if d["study"] == study]
            self.assertEqual({c[field] for c in records}, set(expected))
        detected = [lookup[d["configuration_id"]] for d in self.displays if d["study"] == "detection"]
        self.assertEqual({-c["delta"] for c in detected}, set(DIFFERENCES))
        self.assertEqual({c["n_p"] for c in detected}, {1000, 10000})
        self.assertTrue(all(c["n_p"] == c["n_q"] >= 10 for c in self.configs))

    def test_positive_populations_match_margins_and_mi(self):
        for record in self.populations:
            p, q = self.arrays[record["pair_id"]]
            for side, table in zip("pq", (p, q), strict=True):
                self.assertTrue(np.all(table > 0))
                self.assertLess(abs(table.sum()-1), 1e-12)
                np.testing.assert_allclose(table.sum(axis=1), record[f"margin_{side}"], atol=1e-12)
                np.testing.assert_allclose(table.sum(axis=0), record[f"margin_{side}"], atol=1e-12)
                self.assertLess(abs(mutual_information(table)-record[f"mi_{side}"]), 1e-12+1e-8*record[f"mi_{side}"])
                self.assertGreater(record[f"variance_{side}"], 0)
                self.assertGreater(record[f"variance_sensitivity_variance_{side}"], 0)

    def test_identical_and_distinct_nulls(self):
        for record in self.populations:
            if record["mi_p"] != record["mi_q"]:
                continue
            p, q = self.arrays[record["pair_id"]]
            if record["profile"] == "different_skew":
                self.assertFalse(np.allclose(p, q))
            else:
                np.testing.assert_array_equal(p, q)

    def test_copying_endpoints_and_binary_equivalence(self):
        for k in (2, 4, 8, 16):
            for rho in (None, .7, .8):
                a = margin(k, rho)
                zero = construct_copying(a, 0)
                np.testing.assert_allclose(zero.probability, np.outer(a, a), atol=1e-15)
                self.assertAlmostEqual(zero.endpoint_mi, -np.sum(a*np.log(a)))
                with self.assertRaises(ValueError):
                    construct_copying(a, zero.endpoint_mi)
                if k == 2:
                    copied = construct_copying(a, .03)
                    transferred = construct_additive(a, a, .03, "first", TOLERANCES)
                    np.testing.assert_allclose(copied.probability, transferred.probability, atol=1e-13)
                    self.assertAlmostEqual(transferred.strength, copied.strength*a[0]*a[1], places=12)

    def test_copying_mi_is_monotone(self):
        a = margin(16, .8)
        points = [mutual_information((1-lam)*np.outer(a, a)+lam*np.diag(a)) for lam in np.linspace(0, 1, 21)]
        self.assertTrue(np.all(np.diff(points) > 0))

    def test_copying_rejects_invalid_margins_and_targets(self):
        for a, target in ((np.array([.7, .2]), .02), (np.array([1., 0.]), .02),
                          (np.array([.5, .5]), -1), (np.array([.5, .5]), np.nan)):
            with self.assertRaises(ValueError):
                construct_copying(a, target)

    def setting(self):
        c = next(c for c in self.configs if c["k"] == 4 and c["profile"] == "different_skew"
                 and c["n_p"] == 1000 and c["delta"] == 0 and c["construction"] == "copying")
        population = next(p for p in self.populations if p["pair_id"] == c["pair_id"])
        return c, population, self.arrays[c["pair_id"]]

    def test_batch_size_invariance_and_separate_phases(self):
        c, _, (p, q) = self.setting()
        a = simulate_chunk(c, p, q, 0, 43, 43, "test")
        b = simulate_chunk(c, p, q, 0, 43, 7, "test")
        for key in a:
            np.testing.assert_array_equal(a[key], b[key])
        other = simulate_chunk(c, p, q, 0, 43, 43, "pilot")
        self.assertFalse(np.array_equal(a["delta_corrected"], other["delta_corrected"]))
        self.assertNotEqual(seed_for("test", c["configuration_id"], 0, "p"), seed_for("test", c["configuration_id"], 0, "q"))

    def test_checkpoint_resume_and_corruption_detection(self):
        c, _, (p, q) = self.setting()
        with tempfile.TemporaryDirectory() as temp:
            task = (c, p, q, temp, 31, 7, "test", "fingerprint")
            first = run_configuration(task)
            second = run_configuration((c, p, q, temp, 31, 31, "test", "fingerprint"))
            self.assertEqual(first["resumed_replicates"], 0)
            self.assertEqual(second["resumed_replicates"], 31)
            directory = Path(temp) / c["configuration_id"]
            values = load_records(directory, 31)
            audit_records(c, values)
            with self.assertRaises(RuntimeError):
                run_configuration((c, p, q, temp, 32, 7, "test", "fingerprint"))
            path = directory / "chunk_000.npz"
            path.write_bytes(b"corrupt")
            with self.assertRaises(RuntimeError):
                run_configuration(task)

    def test_summary_denominators_variance_and_bias(self):
        c, population, (p, q) = self.setting()
        records = simulate_chunk(c, p, q, 0, 100, 20, "test")
        methods, paired, diagnostic = summarize(c, population, records)
        self.assertAlmostEqual(diagnostic["observed_variance"], np.var(records["delta_corrected"], ddof=1))
        self.assertAlmostEqual(diagnostic["mean_estimated_variance"], np.mean(records["standard_error"]**2))
        self.assertAlmostEqual(diagnostic["difference_bias"], diagnostic["bias_p"]-diagnostic["bias_q"])
        self.assertEqual(diagnostic["degrees_of_freedom_count"], records["expanded_valid"].sum())
        for row in methods:
            self.assertLessEqual(row["rejections"], row["valid_replicates"])
            self.assertAlmostEqual(row["rejection_rate"], row["rejections"]/row["replicates"])
        self.assertTrue(all(row["only_expanded"] == 0 for row in paired))

    def test_scalar_and_batched_tests_unchanged_including_empty_tables(self):
        p = np.array([[[5, 0], [0, 5]], [[10, 0], [0, 0]], [[3, 2], [1, 4]]])
        q = np.array([[[4, 1], [1, 4]], [[10, 0], [0, 0]], [[1, 4], [2, 3]]])
        records = evaluate_tables(p, q)
        for i in range(3):
            scalar = differential_mi_pvalues(p[i], q[i], include_simple=False, include_unbiased_sensitivity=False)
            for key in ("delta_corrected", "base_valid", "expanded_valid", "normal_p_value", "expanded_welch_p_value"):
                np.testing.assert_allclose(records[key][i], scalar[key], equal_nan=True)
        self.assertEqual(records["empty_cells_p"][1], 3)
        self.assertEqual(records["empty_rows_p"][1], 1)
        self.assertEqual(records["empty_columns_p"][1], 1)
        self.assertFalse(records["base_valid"][1])
        self.assertGreater(records["normal_invalid_reasons"][1], 0)

    def test_invalid_tests_retain_finite_zero_variance_diagnostics(self):
        c, population, _ = self.setting()
        c = {**c, "n_p": 10, "n_q": 10}
        tables = np.zeros((2, 4, 4), dtype=int)
        tables[:, 0, 0] = 10
        records = evaluate_tables(tables, tables)
        methods, paired, diagnostic = summarize(c, population, records)
        self.assertEqual(diagnostic["finite_difference_count"], 2)
        self.assertEqual(diagnostic["matched_variance_count"], 2)
        self.assertEqual(diagnostic["observed_variance"], 0)
        self.assertEqual(diagnostic["mean_estimated_variance"], 0)
        self.assertTrue(np.isnan(diagnostic["estimated_observed_ratio"]))
        self.assertEqual(diagnostic["degrees_of_freedom_count"], 0)
        self.assertTrue(np.isnan(diagnostic["df_median"]))
        for row in methods:
            if row["denominator"] == "all":
                self.assertEqual(row["rejection_rate"], 0)
                self.assertEqual(row["valid_rate"], 0)
            else:
                self.assertEqual(row["replicates"], 0)
                self.assertTrue(np.isnan(row["rejection_rate"]))


if __name__ == "__main__":
    unittest.main()
