#!/usr/bin/env python3
"""Compare all matched large-table constructions, including rejection direction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from audit_focused_study import audit
from focused_study_core import REPLICATES, ROOT
from report_focused_mechanisms import METHODS, direction_summary
from report_unequal_sample_check import rate_text
from run_focused_study import load_records
from run_large_table_construction_check import (
    DEFAULT_BASE, DEFAULT_OUTPUT, MI_PAIRS, SAMPLE_SIZES, audit_check,
)
from run_unequal_sample_check import checked_base_identity


def comparison_rows(base: Path, output: Path):
    rows = []
    for construction, directory in (("copying", base), ("four_cell", output)):
        configs = pd.read_csv(directory / "configuration_manifest.csv")
        methods = pd.read_csv(directory / "method_results.csv")
        methods = methods[methods.denominator.eq("all")].set_index(["configuration_id", "method"])
        diagnostics = pd.read_csv(directory / "diagnostics.csv").set_index("configuration_id")
        for mi_p, mi_q in MI_PAIRS:
            for n in SAMPLE_SIZES:
                selected = configs[
                    configs.k.eq(16) & configs.profile.eq("different_skew")
                    & configs.construction.eq(construction) & configs.mi_p.eq(mi_p)
                    & configs.mi_q.eq(mi_q) & configs.n_p.eq(n) & configs.n_q.eq(n)]
                if len(selected) != 1:
                    raise AssertionError("Large-table construction selection is not unique.")
                config = selected.iloc[0].to_dict()
                key = config["configuration_id"]
                records = load_records(directory / "records" / key, REPLICATES)
                diagnostic = diagnostics.loc[key].to_dict()
                delta = records["delta_corrected"]
                finite = np.isfinite(delta)
                np.testing.assert_allclose(diagnostic["difference_bias"],
                                           np.mean(delta[finite])-config["delta"], atol=1e-13)
                np.testing.assert_allclose(diagnostic["difference_bias"],
                                           diagnostic["bias_p"]-diagnostic["bias_q"], atol=1e-13)
                row = {"configuration_id": key, "construction": construction,
                       "mi_p": mi_p, "mi_q": mi_q, "n": n, "delta": config["delta"],
                       "diagnostics": diagnostic}
                for name, valid, p_value in METHODS:
                    method = "normal_wald" if name == "wald" else "expanded_welch"
                    row[name] = methods.loc[(key, method)].to_dict()
                    if config["delta"] != 0:
                        direction = direction_summary(delta, records[valid], records[p_value], config["delta"])
                        if (direction["rejections"] != row[name]["rejections"]
                                or direction["valid_count"] != row[name]["valid_replicates"]):
                            raise AssertionError("Direction counts disagree with method totals.")
                        row[name+"_direction"] = direction
                rows.append(row)
    return sorted(rows, key=lambda r: (r["mi_q"], r["n"], r["construction"] != "copying"))


def table_text(rows):
    labels = {"copying": "Copying", "four_cell": "Four-cell"}
    lines = [r"\begin{tabular}{@{}rlrrr@{}}", r"\toprule",
             r"\(n\) & Construction & Normal Wald & Expanded Welch & Valid W/E (\%)\\",
             r"\midrule"]
    for mi_q in (.02, .03):
        title = (r"\(I(P)=I(Q)=0.02\): false positives" if mi_q == .02 else
                 r"\(I(P)=0.02,\ I(Q)=0.03\): detection")
        lines.append(r"\multicolumn{5}{@{}l}{"+title+r"}\\")
        for row in rows:
            if row["mi_q"] == mi_q:
                validity = f"{100*row['wald']['valid_rate']:.1f}/{100*row['expanded']['valid_rate']:.1f}"
                lines.append(f"{row['n']:,} & {labels[row['construction']]} & "
                             f"{rate_text(row['wald'])} & {rate_text(row['expanded'])} & {validity}"+r"\\")
        lines.append(r"\midrule" if mi_q == .02 else r"\bottomrule")
    lines.extend([r"\end{tabular}", r"\par\medskip", r"\begin{tabular}{@{}rlrrrrr@{}}",
                  r"\toprule",
                  r"\(n\) & Construction & Bias & MCSE & Obs. SD & Est./obs. & Opposite W/E (\%)\\",
                  r"\midrule"])
    for mi_q in (.02, .03):
        title = r"\(I(P)=I(Q)=0.02\)" if mi_q == .02 else r"\(I(P)=0.02,\ I(Q)=0.03\)"
        lines.append(r"\multicolumn{7}{@{}l}{"+title+r"}\\")
        for row in rows:
            if row["mi_q"] != mi_q:
                continue
            diagnostic = row["diagnostics"]
            opposite = "---"
            if row["delta"] != 0:
                fractions = [row[name+"_direction"]["opposite_fraction_among_rejections"]
                             for name in ("wald", "expanded")]
                opposite = "/".join(f"{100*f:.2f}" if f is not None else "---" for f in fractions)
            lines.append(f"{row['n']:,} & {labels[row['construction']]} & "
                         f"{diagnostic['difference_bias']:+.5f} & {diagnostic['bias_mcse']:.5f} & "
                         f"{np.sqrt(diagnostic['observed_variance']):.5f} & "
                         f"{diagnostic['estimated_observed_ratio']:.2f} & {opposite}"+r"\\")
        lines.append(r"\midrule" if mi_q == .02 else r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)+"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-results", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--results", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--figures", type=Path, default=ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite")
    args = parser.parse_args()
    expected_base = checked_base_identity(args.base_results)
    identity = json.loads((args.results / "study_identity.json").read_text())
    if identity["comparison_source_identity"] != expected_base:
        raise AssertionError("Copying comparison does not match the extension's base study.")
    audit(args.base_results)
    audit_check(args.results)
    rows = comparison_rows(args.base_results, args.results)
    args.figures.mkdir(parents=True, exist_ok=True)
    (args.figures / "focused_large_construction_table.tex").write_text(table_text(rows))
    (args.figures / "focused_large_construction_evidence.json").write_text(
        json.dumps(rows, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
