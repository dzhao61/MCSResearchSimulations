"""Protect matched scope, reuse, sampling and reporting of the same-skew extension."""

from __future__ import annotations

import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from focused_study_core import build_design, seed_for, simulate_chunk
from run_focused_study import audit_records, load_records, run_configuration
from run_large_table_construction_check import build_construction_design
from run_unequal_sample_check import build_allocation_design
from same_skew_extension_core import (
    DEFAULT_OUTPUT, DISPLAY_COUNTS, build_extended_design, combined_frames, extension_design,
)
from thesis_redesign_core import margin, mutual_information


class SameSkewExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs, cls.displays, cls.populations, cls.arrays, cls.origins = build_extended_design()
        cls.new, cls.new_displays, cls.new_populations, cls.new_arrays = extension_design()
        cls.lookup = {c["configuration_id"]: c for c in cls.configs}

    def test_exact_unique_scope(self):
        self.assertEqual(len(self.configs), 312)
        self.assertEqual(len(self.lookup), 312)
        self.assertEqual(len(self.populations), 104)
        self.assertEqual(len(self.new), 72)
        self.assertEqual(len({c["pair_id"] for c in self.new}), 36)
        self.assertEqual(len(self.configs)*20000, 6240000)
        self.assertEqual(Counter(d["study"] for d in self.displays), DISPLAY_COUNTS)
        self.assertEqual(Counter(d["study"] for d in self.new_displays),
                         {"association": 12, "detection": 48, "construction": 10, "allocation": 4})

    def test_original_configurations_and_populations_are_unchanged(self):
        base, _, populations, arrays = build_design()
        large, large_populations, large_arrays = build_construction_design()
        allocation, _, _ = build_allocation_design()
        originals = {c["configuration_id"]: c for c in base+large+allocation}
        self.assertEqual(len(originals), 240)
        self.assertTrue(set(originals).isdisjoint(c["configuration_id"] for c in self.new))
        self.assertEqual(len({c["pair_id"] for c in self.configs}-{c["pair_id"] for c in originals.values()}), 34)
        for key, config in originals.items():
            self.assertEqual(self.lookup[key], config)
        pair_lookup = {p["pair_id"]: p for p in self.populations}
        for p in populations+large_populations:
            self.assertEqual(pair_lookup[p["pair_id"]], p)
        for key, pair in {**arrays, **large_arrays}.items():
            for old, new in zip(pair, self.arrays[key], strict=True):
                np.testing.assert_array_equal(old, new)

    def test_new_populations_are_positive_feasible_and_have_correct_margins(self):
        for population in self.new_populations:
            self.assertEqual(population["profile"], "same_skew")
            for side, table in zip("pq", self.new_arrays[population["pair_id"]], strict=True):
                a = margin(population["k"], .8)
                self.assertTrue(np.all(table > 0))
                self.assertAlmostEqual(table.sum(), 1, places=12)
                np.testing.assert_allclose(table.sum(axis=0), a, atol=1e-12)
                np.testing.assert_allclose(table.sum(axis=1), a, atol=1e-12)
                self.assertAlmostEqual(mutual_information(table), population[f"mi_{side}"], places=12)
                self.assertLess(population[f"mi_{side}"], population[f"endpoint_mi_{side}"])

    def test_same_skew_equal_mi_tables_are_identical_but_alternatives_are_not(self):
        for c in self.configs:
            if c["profile"] != "same_skew":
                continue
            p, q = self.arrays[c["pair_id"]]
            if c["mi_p"] == c["mi_q"]:
                np.testing.assert_array_equal(p, q)
            else:
                self.assertFalse(np.array_equal(p, q))

    def test_all_five_comparisons_include_both_skew_regimes(self):
        for study in DISPLAY_COUNTS:
            selected = [self.lookup[d["configuration_id"]] for d in self.displays if d["study"] == study]
            signatures = {}
            for profile in ("same_skew", "different_skew"):
                signatures[profile] = {(c["k"], c["construction"], c["mi_p"], c["mi_q"], c["n_p"], c["n_q"])
                                       for c in selected if c["profile"] == profile}
            self.assertEqual(signatures["same_skew"], signatures["different_skew"], study)

    def test_shared_settings_are_not_resimulated(self):
        for study in ("association", "detection", "allocation"):
            selected = [self.lookup[d["configuration_id"]] for d in self.displays if d["study"] == study]
            for c in selected:
                if c["mi_p"] == c["mi_q"] == .02 and c["n_p"] == c["n_q"]:
                    self.assertEqual(self.origins[c["configuration_id"]], "focused_study")
        for c in self.new:
            self.assertEqual(c["replicates"], 20000)
            self.assertEqual(c["profile"], "same_skew")

    def test_independent_streams_and_batch_invariance(self):
        for construction, balanced in (("copying", True), ("copying", False), ("four_cell", True)):
            c = next(c for c in self.new if c["construction"] == construction
                     and (c["n_p"] == c["n_q"]) == balanced)
            pair = self.arrays[c["pair_id"]]
            self.assertNotEqual(seed_for("full", c["configuration_id"], 0, "p"),
                                seed_for("full", c["configuration_id"], 0, "q"))
            first = simulate_chunk(c, *pair, 0, 53, 53, "test")
            second = simulate_chunk(c, *pair, 0, 53, 7, "test")
            audit_records(c, first)
            for field in first:
                np.testing.assert_array_equal(first[field], second[field])

    def test_checkpoint_resume_and_provenance(self):
        c = self.new[0]
        pair = self.arrays[c["pair_id"]]
        with tempfile.TemporaryDirectory() as directory:
            task = (c, *pair, directory, 35, 7, "test", "same-skew-test")
            first = run_configuration(task)
            resumed = run_configuration(task)
            self.assertEqual(first["resumed_replicates"], 0)
            self.assertEqual(resumed["resumed_replicates"], 35)
            audit_records(c, load_records(Path(directory)/c["configuration_id"], 35))
            with self.assertRaises(RuntimeError):
                run_configuration((*task[:-1], "changed-source"))

    @unittest.skipUnless((DEFAULT_OUTPUT / "method_results.csv").exists(), "Full extension not yet run")
    def test_combined_evidence_has_no_duplicate_settings(self):
        frames = combined_frames()
        self.assertEqual(len(frames["method_results"]), 312*6)
        self.assertEqual(len(frames["paired_results"]), 312*2)
        self.assertEqual(len(frames["diagnostics"]), 312)
        for name, keys in (("method_results", ["configuration_id", "method", "denominator"]),
                           ("paired_results", ["configuration_id", "denominator"]),
                           ("diagnostics", ["configuration_id"])):
            self.assertFalse(frames[name].duplicated(keys).any())


if __name__ == "__main__":
    unittest.main()
