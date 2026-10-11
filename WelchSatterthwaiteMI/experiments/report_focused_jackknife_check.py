#!/usr/bin/env python3
"""Export the bounded jackknife diagnostic as a compact manuscript table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from focused_study_core import ALPHA, REPLICATES, ROOT
from run_focused_jackknife_check import (
    DEFAULT_OUTPUT, SETTINGS, fixed_se_test, protocol_for, select_settings,
)


def checked_evidence(results: Path) -> dict:
    evidence = json.loads((results/"evidence.json").read_text())
    verification = json.loads((results/"verification.json").read_text())
    configurations = select_settings(pd.read_csv(ROOT/"results/focused_study/configuration_manifest.csv"))
    if evidence["protocol"] != protocol_for(ROOT/"results/focused_study", configurations):
        raise AssertionError("Diagnostic provenance no longer matches the original study.")
    if not verification["all_pass"] or verification["original_sample_pairs_verified"] != 80000:
        raise AssertionError("Jackknife sample verification is incomplete.")
    rows = evidence["estimators"]
    expected = {(n, mi_q, method) for n, mi_q in SETTINGS
                for method in ("analytic_normal", "jackknife_fixed_se_normal")}
    actual = {(row["n"], row["mi_q"], row["method"]) for row in rows}
    if actual != expected or len(rows) != 8:
        raise AssertionError("Report must include all four paired settings.")
    for row in rows:
        with np.load(results/f"{row['configuration_id']}.npz", allow_pickle=False) as values:
            name = "analytic" if row["method"] == "analytic_normal" else "jackknife"
            delta = values[name+"_delta"]
            valid, _, p_value = fixed_se_test(delta, values["standard_error"], values["base_valid"])
            rejected = valid & (p_value <= ALPHA)
            if len(delta) != REPLICATES or int(valid.sum()) != row["valid_count"]:
                raise AssertionError("Diagnostic repetition count or validity changed.")
            np.testing.assert_array_equal(rejected, values[name+"_rejected"])
            np.testing.assert_allclose(row["bias"]["mean"], delta.mean()-row["true_delta"], atol=1e-13)
            np.testing.assert_allclose(row["observed_sd"], np.std(delta, ddof=1), atol=1e-13)
            np.testing.assert_allclose(row["se_variance_ratio"],
                                       np.mean(values["standard_error"]**2)/np.var(delta, ddof=1), atol=1e-13)
            if int(rejected.sum()) != row["rejection"]["count"]:
                raise AssertionError("Saved rejection total changed.")
    return evidence


def table_text(evidence: dict) -> str:
    lines = [r"\begin{tabular}{@{}rrlrrrr@{}}", r"\toprule",
             r"\(n\) & \(\Delta\) & Correction & Bias & Obs. SD & Est./obs. & \shortstack{Rejection\\(\%)}\\",
             r"\midrule"]
    rows = evidence["estimators"]
    for n, mi_q in SETTINGS:
        for method, label in (("analytic_normal", "Analytic"), ("jackknife_fixed_se_normal", "Jackknife")):
            row, = [r for r in rows if r["n"] == n and r["mi_q"] == mi_q and r["method"] == method]
            lines.append(f"{n:,} & {row['true_delta']:.2f} & {label} & "
                         f"{row['bias']['mean']:+.5f} & {row['observed_sd']:.5f} & "
                         f"{row['se_variance_ratio']:.2f} & {100*row['rejection']['rate']:.3f}"+r"\\")
        lines.append(r"\bottomrule" if (n, mi_q) == SETTINGS[-1] else r"\midrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)+"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--figures", type=Path, default=ROOT.parent/"Thesis Writeup/Welch MI/figures_rewrite")
    args = parser.parse_args()
    evidence = checked_evidence(args.results)
    args.figures.mkdir(parents=True, exist_ok=True)
    (args.figures/"focused_jackknife_table.tex").write_text(table_text(evidence))
    (args.figures/"focused_jackknife_evidence.json").write_text(json.dumps(evidence, indent=2, allow_nan=False)+"\n")
    print("Exported all four jackknife comparisons from verified saved records.")


if __name__ == "__main__":
    main()
