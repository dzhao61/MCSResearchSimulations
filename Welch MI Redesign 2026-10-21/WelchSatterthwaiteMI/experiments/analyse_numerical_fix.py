#!/usr/bin/env python3
"""Measure the correction against preserved results on unchanged inputs."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from focused_study_core import CHUNK_SIZE, REPLICATES, ROOT, evaluate_tables
from run_focused_jackknife_check import original_counts
from run_focused_study import atomic_json, load_records

ARCHIVE = ROOT / "results/archive_before_numerical_fix_20261017"
OUTPUT = ROOT / "docs/history/NUMERICAL_FIX_2026-10-17"


def exact_constant(tables):
    """Independent integer reference for the checked n <= 250 inputs."""
    row, column = tables.sum(axis=-1), tables.sum(axis=-2)
    flat_index = (tables > 0).reshape(len(tables), -1).argmax(axis=-1)
    i, j = np.unravel_index(flat_index, tables.shape[-2:])
    batch = np.arange(len(tables))
    reference = tables[batch, i, j]
    return np.all((tables * row[batch, i, None, None] * column[batch, j, None, None]
                   == reference[:, None, None] * row[:, :, None] * column[:, None, :])
                  | (tables == 0), axis=(-2, -1))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    seen, changed, counts = set(), [], []
    zero_errors = transpose_validity = transpose_rejections = exact_checked = 0
    removed_validity = removed_rejections = new_validity = 0
    unchanged_input_fields = ("delta_corrected", "plugin_mi_p", "plugin_mi_q",
                              "corrected_mi_p", "corrected_mi_q", "empty_cells_p",
                              "empty_cells_q", "empty_rows_p", "empty_rows_q",
                              "empty_columns_p", "empty_columns_q")
    for name in ("focused_study", "unequal_sample_check", "large_table_construction_check"):
        old, new = ARCHIVE / name, ROOT / "results" / name
        old_configs = pd.read_csv(old / "configuration_manifest.csv", float_precision="round_trip")
        configs = pd.read_csv(new / "configuration_manifest.csv", float_precision="round_trip")
        pd.testing.assert_frame_equal(old_configs, configs, check_exact=True)
        with np.load(old / "populations.npz") as before, np.load(new / "populations.npz") as after:
            assert set(before.files) == set(after.files)
            for key in before.files:
                np.testing.assert_array_equal(before[key], after[key])
        rates_before = pd.read_csv(old / "method_results.csv")
        rates_after = pd.read_csv(new / "method_results.csv")
        for config in configs.to_dict("records"):
            key = config["configuration_id"]
            if key in seen:
                continue
            seen.add(key)
            before = load_records(old / "records" / key, REPLICATES)
            after = load_records(new / "records" / key, REPLICATES)
            for field in unchanged_input_fields:
                np.testing.assert_array_equal(before[field], after[field])
            np.testing.assert_array_equal(before["base_valid"], after["base_valid"])
            np.testing.assert_array_equal(before["normal_p_value"] <= .05, after["normal_p_value"] <= .05)
            lost = before["expanded_valid"] & ~after["expanded_valid"]
            gained = ~before["expanded_valid"] & after["expanded_valid"]
            old_reject = before["expanded_welch_p_value"] <= .05
            new_reject = after["expanded_welch_p_value"] <= .05
            removed_validity += int(lost.sum())
            new_validity += int(gained.sum())
            removed_rejections += int((old_reject & ~new_reject).sum())
            if config["n_p"] <= 250 and config["n_q"] <= 250:
                exact = []
                with np.load(new / "populations.npz") as arrays:
                    p, q = (arrays[f"{config['pair_id']}_{side}"] for side in "pq")
                    for index, offset in enumerate(range(0, REPLICATES, CHUNK_SIZE)):
                        pp, qq = original_counts(config, p, q, index, CHUNK_SIZE)
                        degenerate = exact_constant(pp) | exact_constant(qq)
                        exact.append(degenerate)
                        sl = slice(offset, offset + CHUNK_SIZE)
                        zero_errors += int(np.count_nonzero(degenerate & after["expanded_valid"][sl]))
                        transpose = evaluate_tables(pp.swapaxes(-1, -2), qq.swapaxes(-1, -2))
                        transpose_validity += int(np.count_nonzero(transpose["expanded_valid"] != after["expanded_valid"][sl]))
                        transpose_rejections += int(np.count_nonzero((transpose["expanded_welch_p_value"] <= .05) != new_reject[sl]))
                        exact_checked += len(pp)
                expected_loss = before["expanded_valid"] & np.concatenate(exact)
                np.testing.assert_array_equal(lost, expected_loss)
            if np.any(lost | gained | (old_reject != new_reject)):
                row = {**config, "old_valid": int(before["expanded_valid"].sum()),
                       "new_valid": int(after["expanded_valid"].sum()),
                       "old_rejections": int(old_reject.sum()), "new_rejections": int(new_reject.sum()),
                       "old_rate": float(old_reject.mean()), "new_rate": float(new_reject.mean()),
                       "marker_changed": (before["expanded_valid"].mean() < .9) != (after["expanded_valid"].mean() < .9)}
                changed.append(row)
            for denominator in ("all", "method_valid", "common_valid"):
                a = rates_before[(rates_before.configuration_id == key) & (rates_before.denominator == denominator)]
                b = rates_after[(rates_after.configuration_id == key) & (rates_after.denominator == denominator)]
                counts.append({"configuration_id": key, "denominator": denominator,
                               "rejections_before": int(a.rejections.sum()), "rejections_after": int(b.rejections.sum())})
    assert len(seen) == 240
    assert zero_errors == transpose_validity == transpose_rejections == new_validity == 0
    frame = pd.DataFrame(changed).sort_values(["k", "profile", "n_p"])
    frame.to_csv(OUTPUT / "affected_settings.csv", index=False)
    practical = ROOT.parent / "PracticalMIExploration"
    old_full = pd.read_csv(practical / "results_before_numerical_fix_20261017/full_data_results.csv")
    new_full = pd.read_csv(practical / "results/full_data_results.csv")
    for column in ("normal_p_value", "expanded_welch_p_value", "wald_holm_p", "expanded_holm_p"):
        np.testing.assert_allclose(old_full[column], new_full[column], rtol=1e-11, atol=1e-13)
        np.testing.assert_array_equal(old_full[column] <= .05, new_full[column] <= .05)
    old_subset = pd.read_csv(practical / "results_before_numerical_fix_20261017/subsample_results.csv")
    new_subset = pd.read_csv(practical / "results/subsample_results.csv")
    subset = old_subset.merge(new_subset, on=["id", "n_each"], suffixes=("_old", "_new"))
    subset.to_csv(OUTPUT / "practical_subset_comparison.csv", index=False)
    evidence = {"settings": len(seen), "sampled_table_pairs": len(seen)*REPLICATES,
                "changed_expanded_settings": len(frame), "removed_valid_outputs": removed_validity,
                "removed_rejections": removed_rejections, "new_valid_outputs": new_validity,
                "all_wald_validity_and_decisions_unchanged": True,
                "all_input_mi_and_support_records_identical": True,
                "all_population_arrays_identical": True,
                "independent_small_sample_pairs": exact_checked,
                "exact_zero_marked_valid_after_fix": zero_errors,
                "transpose_validity_disagreements_after_fix": transpose_validity,
                "transpose_rejection_disagreements_after_fix": transpose_rejections,
                "validity_markers_changed": int(frame.marker_changed.sum()),
                "full_data_application_and_Holm_decisions_unchanged": True}
    atomic_json(OUTPUT / "evidence.json", evidence)
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
