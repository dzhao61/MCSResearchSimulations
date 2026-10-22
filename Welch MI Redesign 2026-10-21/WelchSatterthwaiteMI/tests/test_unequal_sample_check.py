"""Protect the supporting allocation scope and unequal-sample calculations."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from focused_study_core import build_design, digest, evaluate_tables, simulate_chunk, summarize
from run_focused_study import audit_records, load_records, run_configuration
from run_unequal_sample_check import ALLOCATIONS, MI_PAIRS, build_allocation_design
from run_focused_study import file_hash
from report_unequal_sample_check import comparison_rows, rate_text, table_text


class AllocationCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs, cls.populations, cls.arrays = build_allocation_design()

    def test_exact_scope_constant_total_and_existing_balanced_ids(self):
        base, _, _, _ = build_design()
        base_ids = {c["configuration_id"] for c in base}
        self.assertEqual(len(self.configs), 6)
        self.assertEqual(len(self.populations), 2)
        self.assertEqual({(c["n_p"], c["n_q"]) for c in self.configs}, set(ALLOCATIONS))
        self.assertEqual({(c["mi_p"], c["mi_q"]) for c in self.configs}, set(MI_PAIRS))
        self.assertEqual(sum(c["configuration_id"] in base_ids for c in self.configs), 2)
        for c in self.configs:
            self.assertEqual(c["n_p"]+c["n_q"], 2000)
            self.assertEqual(c["replicates"], 20000)
            self.assertEqual(c["k"], 4)
            self.assertEqual(c["profile"], "different_skew")
            self.assertEqual(c["construction"], "copying")
            self.assertEqual(c["configuration_id"], "setting_"+digest([c["pair_id"], c["n_p"], c["n_q"]])[:16])

    def test_populations_do_not_change_with_allocation(self):
        _, _, original_populations, original_arrays = build_design()
        lookup = {p["pair_id"]: p for p in original_populations}
        for p in self.populations:
            self.assertEqual(p, lookup[p["pair_id"]])
            for actual, expected in zip(self.arrays[p["pair_id"]], original_arrays[p["pair_id"]], strict=True):
                np.testing.assert_array_equal(actual, expected)
        self.assertEqual({p["margin_p"][0] for p in self.populations}, {.7})
        self.assertEqual({p["margin_q"][0] for p in self.populations}, {.8})

    def test_correction_does_not_cancel_and_reverses_with_allocation(self):
        base = np.array([[70, 10, 10, 10], [10, 50, 20, 20],
                         [10, 20, 50, 20], [10, 20, 20, 50]])
        self.assertEqual(base.sum(), 400)
        for p, q, correction in ((base, base*4, -.0084375), (base*4, base, .0084375)):
            values = evaluate_tables(p[None], q[None])
            self.assertAlmostEqual(values["plugin_mi_p"][0]-values["plugin_mi_q"][0], 0)
            self.assertAlmostEqual(values["delta_corrected"][0], correction)
            expected = (values["influence_variance_p"]/p.sum()
                        + values["influence_variance_q"]/q.sum())
            np.testing.assert_allclose(values["squared_standard_error"], expected)

    def test_unequal_sampling_batching_and_checkpoint_audit(self):
        c = next(c for c in self.configs if c["n_p"] == 400 and c["delta"] == -.01)
        p, q = self.arrays[c["pair_id"]]
        a = simulate_chunk(c, p, q, 0, 43, 43, "test")
        b = simulate_chunk(c, p, q, 0, 43, 7, "test")
        for key in a:
            np.testing.assert_array_equal(a[key], b[key])
        audit_records(c, a)
        with tempfile.TemporaryDirectory() as temp:
            first = run_configuration((c, p, q, temp, 43, 7, "test", "allocation-test"))
            second = run_configuration((c, p, q, temp, 43, 43, "test", "allocation-test"))
            self.assertEqual(first["resumed_replicates"], 0)
            self.assertEqual(second["resumed_replicates"], 43)
            records = load_records(Path(temp)/c["configuration_id"], 43)
            for key in a:
                np.testing.assert_array_equal(records[key], a[key])
            metadata_path = Path(temp)/c["configuration_id"]/"identity.json"
            metadata = json.loads(metadata_path.read_text())
            metadata["configuration"]["n_q"] = 1000
            metadata_path.write_text(json.dumps(metadata))
            with self.assertRaises(RuntimeError):
                run_configuration((c, p, q, temp, 43, 7, "test", "allocation-test"))

    def test_summary_uses_both_sample_sizes_and_corrected_bias(self):
        populations = {p["pair_id"]: p for p in self.populations}
        for c in self.configs:
            p, q = self.arrays[c["pair_id"]]
            records = simulate_chunk(c, p, q, 0, 100, 20, "test")
            _, paired, summary = summarize(c, populations[c["pair_id"]], records)
            pop = populations[c["pair_id"]]
            self.assertAlmostEqual(summary["first_order_variance"], pop["variance_p"]/c["n_p"]+pop["variance_q"]/c["n_q"])
            self.assertAlmostEqual(summary["difference_bias"], summary["bias_p"]-summary["bias_q"])
            self.assertEqual(summary["matched_variance_count"], 100)
            self.assertTrue(all(row["only_expanded"] == 0 for row in paired))

    def test_saved_balanced_chunks_are_identical_to_original(self):
        for c in self.configs:
            if c["n_p"] != c["n_q"]:
                continue
            source = ROOT / "results/focused_study/records" / c["configuration_id"]
            target = ROOT / "results/unequal_sample_check/records" / c["configuration_id"]
            self.assertEqual(file_hash(source/"identity.json"), file_hash(target/"identity.json"))
            for path in source.glob("chunk_*"):
                self.assertEqual(file_hash(path), file_hash(target/path.name))

    def test_report_includes_all_allocations_with_checked_rates(self):
        rows = comparison_rows(ROOT / "results/unequal_sample_check")
        self.assertEqual(len(rows), 6)
        expected = {(1000,1000,.02): (788,662), (400,1600,.02): (926,612),
                    (1600,400,.02): (908,503), (1000,1000,.03): (2264,2026),
                    (400,1600,.03): (2589,1994), (1600,400,.03): (1079,680)}
        for row in rows:
            w, e = expected[(row["n_p"], row["n_q"], row["mi_q"])]
            self.assertEqual(row["wald"]["rejections"], w)
            self.assertEqual(row["expanded"]["rejections"], e)
            self.assertEqual(row["wald"]["valid_replicates"], 20000)
            self.assertEqual(row["expanded"]["valid_replicates"], 20000)
        self.assertEqual(table_text(rows).count("100.0/100.0"), 6)
        self.assertTrue(rate_text(rows[-1]["wald"]).startswith("0.0540"))

    def test_allocation_report_matches_generated_table(self):
        rows = comparison_rows(ROOT / "results/unequal_sample_check")
        generated = ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite/focused_allocation_table.tex"
        if generated.exists():
            self.assertEqual(generated.read_text(), table_text(rows))
        for row in rows:
            diagnostic = row["diagnostics"]
            self.assertAlmostEqual(diagnostic["difference_bias"], diagnostic["bias_p"]-diagnostic["bias_q"])
            self.assertEqual(diagnostic["matched_variance_count"], 20000)
            self.assertEqual(diagnostic["degrees_of_freedom_count"], 20000)


if __name__ == "__main__":
    unittest.main()
