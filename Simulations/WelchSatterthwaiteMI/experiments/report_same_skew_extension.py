#!/usr/bin/env python3
"""Report both skew regimes using authenticated, deduplicated study evidence."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, LogFormatterMathtext
import numpy as np
import pandas as pd
from scipy.stats import t

from focused_study_core import REPLICATES, ROOT
from report_focused_mechanisms import direction_summary
from report_focused_study import METHODS, WIDTH, configure_style, detection_sizes, save
from report_formatting import decimal_text
from run_focused_study import atomic_json, load_records
from run_same_skew_extension import audit_extension
from same_skew_extension_core import (
    DEFAULT_OUTPUT, build_extended_design, combined_frames, directories,
)

PROFILES = {"same_skew": ("Same skew", "o", "#476858"),
            "different_skew": ("Different skew", "^", "#9a653e")}


def association_figure(rates, diagnostics, output):
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 4.65))
    fig.subplots_adjust(left=.13, right=.975, top=.82, bottom=.13, hspace=.43, wspace=.32)
    for column, n in enumerate((100, 1000)):
        upper, lower = axes[:, column]
        for profile, (_, marker, df_color) in PROFILES.items():
            for method, (_, color, _, style) in METHODS.items():
                part = rates[rates.n_p.eq(n) & rates.profile.eq(profile) & rates.method.eq(method)].sort_values("mi_p")
                x = part.mi_p.to_numpy()
                upper.plot(x, part.rejection_rate, color=color, linestyle=style, marker=marker,
                           markerfacecolor=color)
                upper.fill_between(x, part.rejection_low, part.rejection_high, color=color, alpha=.07)
            part = diagnostics[diagnostics.n_p.eq(n) & diagnostics.profile.eq(profile)].sort_values("mi_p")
            lower.fill_between(part.mi_p, part.df_p05, part.df_p95, color=df_color, alpha=.12)
            lower.plot(part.mi_p, part.df_median, color=df_color, marker=marker,
                       linestyle="-" if profile == "same_skew" else "--")
        upper.set_title(f"n = {n:,}")
        upper.axhline(.05, color=".45", linestyle=":", linewidth=.8)
        upper.set_ylim(0, .06)
        lower.set_yscale("log")
        lower.set_ylim(1.5, 140)
        lower.set_xlabel("MI in both populations (nats)")
        for ax in (upper, lower):
            ax.set_xscale("log")
            ax.set_xlim(.00008, .065)
            ax.xaxis.set_major_locator(FixedLocator([.0001, .001, .01]))
            ax.xaxis.set_major_formatter(LogFormatterMathtext())
            ax.grid(alpha=.15)
    axes[0, 0].set_ylabel("False-positive rate")
    axes[1, 0].set_ylabel("Degrees of freedom")
    method_handles = [Line2D([], [], color=color, linestyle=style, label=label)
                      for label, color, _, style in METHODS.values()]
    profile_handles = [Line2D([], [], color=color, marker=marker, linestyle="none", label=label)
                       for label, marker, color in PROFILES.values()]
    fig.legend(handles=method_handles, loc="upper center", bbox_to_anchor=(.53, 1.0), ncol=2, frameon=False)
    fig.legend(handles=profile_handles, loc="upper center", bbox_to_anchor=(.53, .935), ncol=2, frameon=False)
    save(fig, output, "focused_association_skew_comparison")


def make_evidence(output):
    frames = combined_frames(output)
    configs, displays, _, _, origins = build_extended_design()
    methods = frames["method_results"].query("denominator == 'all'").set_index(["configuration_id", "method"])
    diagnostics = frames["diagnostics"].set_index("configuration_id")
    membership = {}
    for row in displays:
        membership.setdefault(row["configuration_id"], []).append(row["study"])
    evidence = []
    for config in configs:
        key = config["configuration_id"]
        diagnostic = diagnostics.loc[key].to_dict()
        row = {**config, "studies": membership[key], "origin": origins[key],
               "diagnostics": diagnostic,
               "median_df_student_t_cutoff": float(t.ppf(.975, diagnostic["df_median"])),
               "wald": methods.loc[(key, "normal_wald")].to_dict(),
               "expanded": methods.loc[(key, "expanded_welch")].to_dict()}
        if config["delta"] != 0:
            records = load_records(directories(output)[origins[key]] / "records" / key, REPLICATES)
            for name, valid, p_value in (("wald", "base_valid", "normal_p_value"),
                                        ("expanded", "expanded_valid", "expanded_welch_p_value")):
                row[name+"_direction"] = direction_summary(
                    records["delta_corrected"], records[valid], records[p_value], config["delta"])
                if row[name+"_direction"]["rejections"] != row[name]["rejections"]:
                    raise AssertionError("Direction counts disagree with rejection totals.")
        evidence.append(row)
    return frames, evidence


def rate(row, name):
    return decimal_text(row[name]["rejection_rate"])


def bias_text(value):
    rounded = decimal_text(value, 5)
    return "+"+rounded if float(rounded) > 0 else rounded


def write_association_table(rows, output):
    selected = sorted((r for r in rows if "association" in r["studies"] and r["profile"] == "same_skew"),
                      key=lambda r: (r["n_p"], r["mi_p"]))
    lines = [r"\begin{tabular}{@{}rrrrrr@{}}\toprule",
             r"\(n\) & MI & Wald & Expanded & DF median [5th, 95th] & Est./obs.\\\midrule"]
    for r in selected:
        d = r["diagnostics"]
        lines.append(f"{r['n_p']:,} & {r['mi_p']:g} & {rate(r, 'wald')} & {rate(r, 'expanded')} & "
                     f"{d['df_median']:.2f} [{d['df_p05']:.2f}, {d['df_p95']:.2f}] & {d['estimated_observed_ratio']:.3f}"+r"\\")
    lines.append(r"\bottomrule\end{tabular}")
    (output / "focused_same_association_table.tex").write_text("\n".join(lines)+"\n")


def write_construction_table(rows, output):
    selected = sorted((r for r in rows if "construction" in r["studies"] and r["profile"] == "same_skew"),
                      key=lambda r: (r["k"], r["n_p"], r["mi_q"], r["construction"]))
    lines = [r"\begin{tabular}{@{}rrlrrrrr@{}}\toprule",
             r"Size & \(n\) & Construction & \(|\Delta|\) & Wald & Expanded & Bias & DF\\\midrule"]
    for r in selected:
        d = r["diagnostics"]
        label = "Copying" if r["construction"] == "copying" else "Four-cell"
        lines.append(f"\\({r['k']}\\times{r['k']}\\) & {r['n_p']:,} & {label} & {abs(r['delta']):g} & "
                     f"{rate(r, 'wald')} & {rate(r, 'expanded')} & {bias_text(d['difference_bias'])} & {d['df_median']:.2f}"+r"\\")
    lines.append(r"\bottomrule\end{tabular}")
    (output / "focused_same_construction_table.tex").write_text("\n".join(lines)+"\n")


def write_allocation_table(rows, output):
    selected = sorted((r for r in rows if "allocation" in r["studies"] and r["profile"] == "same_skew"),
                      key=lambda r: (r["mi_q"], r["n_p"]))
    lines = [r"\begin{tabular}{@{}rrrrrrrr@{}}\toprule",
             r"\(n_P\) & \(n_Q\) & \(|\Delta|\) & Wald & Expanded & Bias & Est./obs. & DF\\\midrule"]
    for r in selected:
        d = r["diagnostics"]
        lines.append(f"{r['n_p']:,} & {r['n_q']:,} & {abs(r['delta']):g} & {rate(r, 'wald')} & "
                     f"{rate(r, 'expanded')} & {bias_text(d['difference_bias'])} & {d['estimated_observed_ratio']:.3f} & "
                     f"{d['df_median']:.2f}"+r"\\")
    lines.append(r"\bottomrule\end{tabular}")
    (output / "focused_same_allocation_table.tex").write_text("\n".join(lines)+"\n")


def write_df_table(rows, output):
    selected = sorted((r for r in rows if r["k"] in (4, 16) and r["profile"] in PROFILES
                       and r["mi_p"] == r["mi_q"] == .02 and r["construction"] == "copying"
                       and r["n_p"] == r["n_q"] and r["n_p"] in (1000, 10000)),
                      key=lambda r: (r["k"], r["profile"], r["n_p"]))
    lines = [r"\begin{tabular}{@{}rlrrrr@{}}\toprule",
             r"Size & Margins & \(n\) & DF median [5th, 95th] & Cutoff & Est./obs.\\\midrule"]
    for r in selected:
        d = r["diagnostics"]
        lines.append(f"\\({r['k']}\\times{r['k']}\\) & {PROFILES[r['profile']][0]} & {r['n_p']:,} & "
                     f"{d['df_median']:.2f} [{d['df_p05']:.2f}, {d['df_p95']:.2f}] & "
                     f"{r['median_df_student_t_cutoff']:.3f} & {d['estimated_observed_ratio']:.3f}"+r"\\")
    lines.append(r"\bottomrule\end{tabular}")
    (output / "focused_df_structure_table.tex").write_text("\n".join(lines)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--figures", type=Path, default=ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite")
    args = parser.parse_args()
    audit_extension(args.results)
    frames, evidence = make_evidence(args.results)
    args.figures.mkdir(parents=True, exist_ok=True)
    configure_style()
    configs = frames["configurations"]
    rates = frames["method_results"].query("denominator == 'all'").merge(configs, on="configuration_id")
    rates["difference"] = rates.delta.abs()
    diagnostics = frames["diagnostics"].merge(configs, on="configuration_id")
    displays = frames["displays"]
    ids = displays.loc[displays.study.eq("association"), "configuration_id"]
    association_figure(rates[rates.configuration_id.isin(ids)], diagnostics[diagnostics.configuration_id.isin(ids)], args.figures)
    ids = displays.loc[displays.study.eq("detection"), "configuration_id"]
    same_power = rates[rates.configuration_id.isin(ids) & rates.profile.eq("same_skew")]
    for full in (False, True):
        # Reuse the established power layout without replacing the original files.
        import tempfile
        with tempfile.TemporaryDirectory() as scratch:
            detection_sizes(same_power, Path(scratch), full)
            original = "focused_detection_sizes_full" if full else "focused_detection_sizes"
            target = "focused_same_detection_sizes_full" if full else "focused_same_detection_sizes"
            for suffix in (".pdf", ".png"):
                (args.figures / (target+suffix)).write_bytes((Path(scratch) / (original+suffix)).read_bytes())
    write_association_table(evidence, args.figures)
    write_construction_table(evidence, args.figures)
    write_allocation_table(evidence, args.figures)
    write_df_table(evidence, args.figures)
    atomic_json(args.figures / "focused_same_skew_evidence.json", evidence)
    print("Generated matched MI figure, same-skew power figures, four tables and complete evidence.")


if __name__ == "__main__":
    main()
