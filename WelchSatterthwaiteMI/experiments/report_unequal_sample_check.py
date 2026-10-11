#!/usr/bin/env python3
"""Generate the supporting allocation table from independently audited results."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import numpy as np
import pandas as pd

from focused_study_core import ROOT
from run_unequal_sample_check import ALLOCATIONS, DEFAULT_OUTPUT, MI_PAIRS, audit_check


def comparison_rows(output: Path):
    configurations = pd.read_csv(output / "configuration_manifest.csv")
    methods = pd.read_csv(output / "method_results.csv")
    methods = methods[methods.denominator.eq("all")].set_index(["configuration_id", "method"])
    diagnostics = pd.read_csv(output / "diagnostics.csv").set_index("configuration_id")
    rows = []
    for mi_p, mi_q in MI_PAIRS:
        for n_p, n_q in ALLOCATIONS:
            selected = configurations[configurations.mi_p.eq(mi_p) & configurations.mi_q.eq(mi_q)
                                      & configurations.n_p.eq(n_p) & configurations.n_q.eq(n_q)]
            if len(selected) != 1:
                raise AssertionError("Allocation table selection is not unique.")
            key = selected.iloc[0].configuration_id
            rows.append({"configuration_id": key, "mi_p": mi_p, "mi_q": mi_q,
                         "n_p": n_p, "n_q": n_q,
                         "wald": methods.loc[(key, "normal_wald")].to_dict(),
                         "expanded": methods.loc[(key, "expanded_welch")].to_dict(),
                         "diagnostics": diagnostics.loc[key].to_dict()})
    return rows


def rate_text(row):
    rate = Decimal(str(row["rejection_rate"])).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    return f"{rate} [{row['rejection_low']:.4f}, {row['rejection_high']:.4f}]"


def table_text(rows):
    lines = [r"\begin{tabular}{@{}lrrr@{}}", r"\toprule",
             r"\((n_P,n_Q)\) & Normal Wald & Expanded Welch & Valid W/E (\%)\\",
             r"\midrule"]
    for target in (.02, .03):
        title = (r"\(I(P)=I(Q)=0.02\): false positives" if target == .02 else
                 r"\(I(P)=0.02,\ I(Q)=0.03\): power")
        lines.append(r"\multicolumn{4}{@{}l}{"+title+r"}\\")
        for row in rows:
            if row["mi_q"] != target:
                continue
            validity = f"{100*row['wald']['valid_rate']:.1f}/{100*row['expanded']['valid_rate']:.1f}"
            lines.append(f"\\(({row['n_p']},{row['n_q']})\\) & {rate_text(row['wald'])} & "
                         f"{rate_text(row['expanded'])} & {validity}"+r"\\")
        lines.append(r"\midrule" if target == .02 else r"\bottomrule")
    lines.extend([r"\end{tabular}", r"\par\medskip", r"\begin{tabular}{@{}lrrrr@{}}",
                  r"\toprule", r"\((n_P,n_Q)\) & Difference bias & Observed SD & Est./obs. & Median DF\\",
                  r"\midrule"])
    for target in (.02, .03):
        title = (r"\(I(P)=I(Q)=0.02\)" if target == .02 else r"\(I(P)=0.02,\ I(Q)=0.03\)")
        lines.append(r"\multicolumn{5}{@{}l}{"+title+r"}\\")
        for row in rows:
            if row["mi_q"] != target:
                continue
            diagnostic = row["diagnostics"]
            lines.append(f"\\(({row['n_p']},{row['n_q']})\\) & {diagnostic['difference_bias']:+.5f} & "
                         f"{np.sqrt(diagnostic['observed_variance']):.5f} & "
                         f"{diagnostic['estimated_observed_ratio']:.2f} & {diagnostic['df_median']:.2f}"+r"\\")
        lines.append(r"\midrule" if target == .02 else r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)+"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--figures", type=Path, default=ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite")
    args = parser.parse_args()
    audit_check(args.results)
    rows = comparison_rows(args.results)
    args.figures.mkdir(parents=True, exist_ok=True)
    (args.figures / "focused_allocation_table.tex").write_text(table_text(rows))
    (args.figures / "focused_allocation_evidence.json").write_text(json.dumps(rows, indent=2)+"\n")


if __name__ == "__main__":
    main()
