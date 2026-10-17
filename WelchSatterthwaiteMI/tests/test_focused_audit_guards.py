from __future__ import annotations

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import report_focused_study as reporter
from audit_focused_study import authenticate_base_design
from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, SCHEMA_VERSION,
    build_design, digest, source_fingerprint,
)
from run_focused_study import atomic_json


class FocusedAuditGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name)
        configs, displays, populations, arrays = build_design()
        self.configs = configs
        self.identity = {"schema": SCHEMA_VERSION, "master_seed": MASTER_SEED,
                         "source": source_fingerprint(), "phase": "full", "count": REPLICATES,
                         "chunk_size": CHUNK_SIZE, "design_digest": digest([configs, populations]),
                         "alpha": ALPHA}
        pd.DataFrame(configs).to_csv(self.output / "configuration_manifest.csv", index=False)
        pd.DataFrame(displays).to_csv(self.output / "display_manifest.csv", index=False)
        atomic_json(self.output / "population_definitions.json", populations)
        np.savez_compressed(self.output / "populations.npz", **{
            f"{key}_{side}": p for key, pair in arrays.items() for side, p in zip("pq", pair)})
        for config in configs:
            directory = self.output / "records" / config["configuration_id"]
            directory.mkdir(parents=True)
            atomic_json(directory / "identity.json", {
                "configuration": config, "count": REPLICATES, "phase": "full",
                "fingerprint": digest(self.identity), "chunk_size": CHUNK_SIZE})

    def test_authentic_design_passes(self):
        authenticate_base_design(self.output, self.identity)

    def test_changed_profile_target_identifier_or_display_fails(self):
        for filename, column, replacement in (
            ("configuration_manifest.csv", "profile", "invented_skew"),
            ("configuration_manifest.csv", "mi_q", .12345),
            ("configuration_manifest.csv", "configuration_id", "different_setting"),
            ("display_manifest.csv", "study", "invented_study"),
        ):
            path = self.output / filename
            original = path.read_bytes()
            frame = pd.read_csv(path, keep_default_na=False, float_precision="round_trip")
            frame.loc[0, column] = replacement
            frame.to_csv(path, index=False)
            with self.subTest(column=column), self.assertRaises(AssertionError):
                authenticate_base_design(self.output, self.identity)
            path.write_bytes(original)

    def test_wrong_digest_or_checkpoint_provenance_fails(self):
        with self.assertRaises(AssertionError):
            authenticate_base_design(self.output, {**self.identity, "design_digest": "changed"})
        path = self.output / "records" / self.configs[0]["configuration_id"] / "identity.json"
        value = json.loads(path.read_text())
        value["fingerprint"] = "different_run"
        atomic_json(path, value)
        with self.assertRaises(AssertionError):
            authenticate_base_design(self.output, self.identity)

    def test_population_array_or_definition_mutation_fails(self):
        definitions = self.output / "population_definitions.json"
        original = definitions.read_bytes()
        values = json.loads(original)
        values[0]["mi_p"] = .12345
        atomic_json(definitions, values)
        with self.assertRaises(AssertionError):
            authenticate_base_design(self.output, self.identity)
        definitions.write_bytes(original)
        path = self.output / "populations.npz"
        with np.load(path) as stored:
            arrays = {key: stored[key].copy() for key in stored.files}
        arrays[next(iter(arrays))][0, 0] += 1e-8
        np.savez_compressed(path, **arrays)
        with self.assertRaises(AssertionError):
            authenticate_base_design(self.output, self.identity)

    def test_reporter_rejects_changed_csv_despite_stored_success_flag(self):
        source = ROOT / "results/focused_study"
        if not (source / "method_results.csv").exists():
            self.skipTest("Saved focused-study evidence not supplied.")
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for path in source.iterdir():
                if path.is_file():
                    shutil.copyfile(path, output / path.name)
            (output / "records").symlink_to(source / "records", target_is_directory=True)
            atomic_json(output / "verification.json", {"all_pass": True})
            figures = output / "figures"
            for filename, column in (("diagnostics.csv", "difference_bias"),
                                     ("method_results.csv", "valid_rate")):
                path = output / filename
                original = path.read_bytes()
                frame = pd.read_csv(path)
                frame.loc[0, column] = .12345
                frame.to_csv(path, index=False)
                with patch.object(sys, "argv", ["report", "--results", str(output), "--figures", str(figures)]):
                    with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(AssertionError):
                        reporter.main()
                self.assertFalse(figures.exists())
                path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
