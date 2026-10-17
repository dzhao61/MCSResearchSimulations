#!/usr/bin/env python3
"""Generate printed-size figures and manuscript tables from audited focused results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedFormatter, FixedLocator, LogFormatterMathtext

from focused_study_core import ROOT
from report_formatting import decimal_text

WIDTH = 148/25.4
METHODS = {"normal_wald": ("Normal Wald", "#194f78", "o", "-"),
           "expanded_welch": ("Expanded Welch", "#ba3778", "s", "--")}
PROFILE_NAMES = {"uniform": "Uniform", "same_skew": "Same skew", "different_skew": "Different skew"}


def configure_style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                         "axes.titlesize": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                         "ytick.labelsize": 8, "legend.fontsize": 8.5,
                         "lines.linewidth": 1.3, "lines.markersize": 3.4,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42})


def save(fig, directory, name):
    fig.savefig(directory / f"{name}.pdf")
    fig.savefig(directory / f"{name}.png", dpi=180)
    plt.close(fig)


def legend(fig):
    handles = [Line2D([], [], color=color, marker=marker, linestyle=style, label=label)
               for label, color, marker, style in METHODS.values()]
    fig.legend(handles=handles, loc="upper center", ncol=2, frameon=False,
               bbox_to_anchor=(.53, 1.0))


def draw_rate(ax, frame, x, maximum=1):
    for method, (_, color, marker, style) in METHODS.items():
        selected = frame[frame.method.eq(method)].sort_values(x)
        xx = selected[x].to_numpy()
        yy = selected.rejection_rate.to_numpy()
        ax.plot(xx, yy, style, color=color)
        ax.errorbar(xx, yy, yerr=np.stack((yy-selected.rejection_low, selected.rejection_high-yy)),
                    fmt="none", ecolor=color, elinewidth=.65, capsize=1.4, alpha=.75)
        for filled in (True, False):
            mask = selected.valid_rate.ge(.9).to_numpy() == filled
            ax.plot(xx[mask], yy[mask], linestyle="none", marker=marker, color=color,
                    markerfacecolor=color if filled else "white", markeredgewidth=.9)
    ax.axhline(.05, color=".45", linestyle=":", linewidth=.8)
    ax.grid(alpha=.15)
    ax.set_ylim(0, maximum)


def log_sample_axis(ax):
    ax.set_xscale("log")
    ax.set_xlim(8, 65000)
    ax.xaxis.set_major_locator(FixedLocator([10, 1000, 50000]))
    ax.xaxis.set_major_formatter(FixedFormatter([r"$10^1$", r"$10^3$", r"$5\times10^4$"]))


def null_figure(frame, cases, columns, output, name):
    rows = (len(cases)+columns-1)//columns
    fig = plt.figure(figsize=(WIDTH, .55+rows*2.2))
    grid = fig.add_gridspec(rows, columns, left=.115, right=.975, bottom=.105, top=.87,
                           hspace=.53, wspace=.32)
    for index, (k, profile) in enumerate(cases):
        row, column = divmod(index, columns)
        panel = grid[row, column].subgridspec(2, 1, height_ratios=[3, .65], hspace=.15)
        ax = fig.add_subplot(panel[0])
        va = fig.add_subplot(panel[1], sharex=ax)
        selected = frame[(frame.k==k)&(frame.profile==profile)]
        draw_rate(ax, selected, "n_p", .30)
        ax.set_title(f"{k} x {k}: {PROFILE_NAMES[profile]}")
        log_sample_axis(ax)
        ax.tick_params(labelbottom=False)
        ax.set_yticks([0, .1, .2, .3])
        if column == 0:
            ax.set_ylabel("False-positive rate")
            va.set_ylabel("Valid", fontsize=8)
        for method, (_, color, marker, style) in METHODS.items():
            part = selected[selected.method.eq(method)].sort_values("n_p")
            va.plot(part.n_p, part.valid_rate, color=color, marker=marker, linestyle=style)
        va.set_ylim(0, 1.05)
        va.set_yticks([0, 1])
        va.get_xticklabels()[-1].set_horizontalalignment("right")
        va.grid(alpha=.15)
        if row == rows-1:
            va.set_xlabel("Sample size per population", fontsize=8)
    legend(fig)
    save(fig, output, name)


def association_figure(rates, diagnostics, output):
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 4.45))
    fig.subplots_adjust(left=.13, right=.975, top=.87, bottom=.14, hspace=.4, wspace=.32)
    for column, n in enumerate((100, 1000)):
        draw_rate(axes[0, column], rates[rates.n_p.eq(n)], "mi_p", .06)
        axes[0, column].set_title(f"n = {n:,}")
        selected = diagnostics[diagnostics.n_p.eq(n)].sort_values("mi_p")
        ax = axes[1, column]
        ax.fill_between(selected.mi_p, selected.df_p05, selected.df_p95, color=".82")
        ax.plot(selected.mi_p, selected.df_median, color="#374f42", marker="o")
        ax.set_yscale("log")
        ax.set_ylim(2, 130)
        ax.grid(alpha=.15)
        ax.set_xlabel("Common population MI (nats)")
        for a in axes[:, column]:
            a.set_xscale("log")
            a.set_xlim(.00008, .065)
            a.xaxis.set_major_locator(FixedLocator([.0001, .001, .01]))
            a.xaxis.set_major_formatter(LogFormatterMathtext())
    axes[0, 0].set_ylabel("False-positive rate")
    axes[1, 0].set_ylabel("Degrees of freedom")
    legend(fig)
    save(fig, output, "focused_association")


def detection_sizes(frame, output, full=False):
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 4.9))
    fig.subplots_adjust(left=.12, right=.975, top=.83, bottom=.13, hspace=.65, wspace=.3)
    for k, ax in zip((2, 4, 8, 16), axes.ravel(), strict=True):
        for n in (1000, 10000):
            part = frame[(frame.k==k)&(frame.n_p==n)]
            for method, (_, color, _, style) in METHODS.items():
                selected = part[part.method.eq(method)].sort_values("difference")
                x, y = selected.difference, selected.rejection_rate
                alpha = .55 if n == 1000 else 1
                ax.plot(x, y, color=color, linestyle=style, marker="o" if n == 1000 else "^", alpha=alpha)
                ax.fill_between(x, selected.rejection_low, selected.rejection_high, color=color, alpha=.10)
        ax.set_xlim(0, .2 if full else .02)
        ax.set_xticks([0, .1, .2] if full else [0, .01, .02])
        ax.set_ylim(0, 1.02)
        ax.axhline(.05, color=".45", linestyle=":", linewidth=.8)
        ax.set_title(f"{k} x {k}")
        ax.grid(alpha=.15)
        ax.set_xlabel("|MI difference| (nats)")
    for ax in axes[:, 0]:
        ax.set_ylabel("Rejection rate")
    handles = []
    for n in (1000, 10000):
        for _, (label, color, _, style) in METHODS.items():
            handles.append(Line2D([], [], color=color, linestyle=style, marker="o" if n == 1000 else "^",
                                  alpha=.55 if n == 1000 else 1, label=f"{label}, n = {n:,}"))
    fig.legend(handles=handles, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(.53, 1))
    save(fig, output, "focused_detection_sizes_full" if full else "focused_detection_sizes")


def detection_margins(frame, output, full=False):
    fig, axes = plt.subplots(2, 3, figsize=(WIDTH, 4.45))
    fig.subplots_adjust(left=.11, right=.975, top=.87, bottom=.13, hspace=.45, wspace=.32)
    for row, n in enumerate((1000, 10000)):
        for column, profile in enumerate(PROFILE_NAMES):
            ax = axes[row, column]
            draw_rate(ax, frame[(frame.n_p==n)&(frame.profile==profile)], "difference")
            ax.set_title(f"{PROFILE_NAMES[profile]}\nn = {n:,}")
            ax.set_xlim(0, .2 if full else .02)
            ax.set_xticks([0, .1, .2] if full else [0, .01, .02])
            if column == 0:
                ax.set_ylabel("Rejection rate")
            if row == 1:
                ax.set_xlabel("|MI difference| (nats)", fontsize=8)
    legend(fig)
    save(fig, output, "focused_detection_margins_full" if full else "focused_detection_margins")


def write_null_table(frame, output):
    pivot = frame.pivot(index=["k", "profile", "n_p"], columns="method", values=["rejection_rate", "valid_rate"])
    lines = [r"\begin{longtable}{@{}llrrrrr@{}}",
             r"\caption{False-positive and valid-result rates for all 120 null settings.}\label{tab:all-main-null}\\",
             r"\toprule Size & Margins & \(n\) & Wald & Expanded & Valid W & Valid E\\\midrule\endfirsthead",
             r"\toprule Size & Margins & \(n\) & Wald & Expanded & Valid W & Valid E\\\midrule\endhead"]
    for k in (2, 4, 8, 16):
        for profile in PROFILE_NAMES:
            for n in (10, 20, 50, 100, 250, 500, 1000, 2500, 10000, 50000):
                row = pivot.loc[(k, profile, n)]
                lines.append(f"\\({k}\\times{k}\\) & {PROFILE_NAMES[profile]} & {n:,} & " +
                             " & ".join(decimal_text(row[(metric, method)]) for metric in ("rejection_rate", "valid_rate") for method in METHODS) + r"\\")
        lines.append(r"\midrule")
    lines.extend([r"\bottomrule", r"\end{longtable}"])
    (output / "focused_null_table.tex").write_text("\n".join(lines)+"\n")


def write_diagnostic_table(diagnostics, rates, output):
    selected = diagnostics[(diagnostics.k.isin([4, 16]))&(diagnostics.profile=="different_skew")
                           &(diagnostics.mi_p==.02)&(diagnostics.mi_q==.02)
                           &(diagnostics.n_p.isin([1000, 10000]))&(diagnostics.construction=="copying")].sort_values(["k", "n_p"])
    lines = [r"\begin{tabular}{@{}rrrrrr@{}}\toprule",
             r"Size & \(n\) & Bias & Observed SD & Estimated SD & Variance ratio\\\midrule"]
    for row in selected.itertuples():
        lines.append(f"\\({row.k}\\times{row.k}\\) & {row.n_p:,} & {row.difference_bias:.5f} & "
                     f"{np.sqrt(row.observed_variance):.5f} & {np.sqrt(row.mean_estimated_variance):.5f} & {row.estimated_observed_ratio:.3f}" + r"\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    (output / "focused_diagnostic_table.tex").write_text("\n".join(lines)+"\n")


def write_supporting_tables(diagnostics, rates, output):
    association = diagnostics[(diagnostics.k==4)&(diagnostics.profile=="different_skew")
                              &(diagnostics.mi_p==diagnostics.mi_q)&(diagnostics.n_p.isin([100,1000]))
                              &(diagnostics.construction=="copying")].sort_values(["n_p", "mi_p"])
    lines = [r"\begin{tabular}{@{}rrrrrr@{}}\toprule",
             r"\(n\) & MI & Bias & DF median [5th, 95th] & Est./obs. & Pop./obs.\\\midrule"]
    for r in association.itertuples():
        lines.append(f"{r.n_p:,} & {r.mi_p:g} & {r.difference_bias:.5f} & {r.df_median:.2f} [{r.df_p05:.2f}, {r.df_p95:.2f}] & {r.estimated_observed_ratio:.3f} & {r.first_order_observed_ratio:.3f}" + r"\\")
    lines.extend([r"\bottomrule\end{tabular}"])
    (output / "focused_association_table.tex").write_text("\n".join(lines)+"\n")
    large = diagnostics[(diagnostics.k.isin([4,16]))&(diagnostics.profile=="different_skew")
                        &(diagnostics.mi_p==.02)&(diagnostics.mi_q==.02)&(diagnostics.n_p==50000)
                        &(diagnostics.construction=="copying")].sort_values("k")
    lines = [r"\begin{tabular}{@{}rrrrr@{}}\toprule", r"Size & Bias & Est./obs. & Pop./obs. & DF median\\\midrule"]
    for r in large.itertuples():
        lines.append(f"\\({r.k}\\times{r.k}\\) & {r.difference_bias:.5f} & {r.estimated_observed_ratio:.3f} & {r.first_order_observed_ratio:.3f} & {r.df_median:.2f}" + r"\\")
    lines.extend([r"\bottomrule\end{tabular}"])
    (output / "focused_large_sample_table.tex").write_text("\n".join(lines)+"\n")
    selected = rates[(rates.k==4)&(rates.profile=="different_skew")&(rates.mi_p==.02)
                     &(rates.mi_q.isin([.02,.03]))&(rates.n_p.isin([1000,10000]))]
    pivot = selected.pivot(index=["construction", "n_p", "difference"], columns="method", values="rejection_rate")
    diag = diagnostics.set_index("configuration_id")
    lines = [r"\begin{tabular}{@{}lrrrrr@{}}\toprule",
             r"Construction & \(n\) & \(|\Delta|\) & Wald & Expanded & Bias\\\midrule"]
    for (construction, n, difference), row in pivot.iterrows():
        setting = selected[(selected.construction==construction)&(selected.n_p==n)&(selected.difference==difference)].iloc[0]
        bias = diag.loc[setting.configuration_id, "difference_bias"]
        lines.append(f"{'Copying' if construction=='copying' else 'Four-cell'} & {n:,} & {abs(difference):g} & {decimal_text(row.normal_wald)} & {decimal_text(row.expanded_welch)} & {bias:.5f}" + r"\\")
    lines.extend([r"\bottomrule\end{tabular}"])
    (output / "focused_construction_table.tex").write_text("\n".join(lines)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=ROOT / "results/focused_study")
    parser.add_argument("--figures", type=Path, default=ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite")
    args = parser.parse_args()
    if not json.loads((args.results / "verification.json").read_text())["all_pass"]:
        raise RuntimeError("Results have not passed their audit.")
    configs = pd.read_csv(args.results / "configuration_manifest.csv")
    displays = pd.read_csv(args.results / "display_manifest.csv", keep_default_na=False)
    rates = pd.read_csv(args.results / "method_results.csv")
    rates = rates[rates.denominator.eq("all")].merge(configs, on="configuration_id")
    rates["difference"] = rates.delta.abs()
    diagnostics = pd.read_csv(args.results / "diagnostics.csv").merge(configs, on="configuration_id")
    def study(frame, name):
        ids = displays.loc[displays.study.eq(name), "configuration_id"]
        expected = {"null": 120, "association": 14, "detection": 108, "construction": 4}[name]
        if ids.nunique() != expected:
            raise AssertionError(f"Incomplete display selection: {name}")
        return frame[frame.configuration_id.isin(ids)]
    args.figures.mkdir(parents=True, exist_ok=True)
    configure_style()
    null = study(rates, "null")
    null_figure(null, [(k, "different_skew") for k in (2, 4, 8, 16)], 2, args.figures, "focused_null_sizes")
    null_figure(null, [(k, p) for k in (4, 16) for p in PROFILE_NAMES], 3, args.figures, "focused_null_margins")
    null_figure(null, [(k, p) for k in (2, 8) for p in ("uniform", "same_skew")], 2, args.figures, "focused_null_remaining")
    association_figure(study(rates, "association"), study(diagnostics, "association"), args.figures)
    detection = study(rates, "detection")
    for full in (False, True):
        detection_sizes(detection[detection.profile.eq("different_skew")], args.figures, full)
        detection_margins(detection[detection.k.eq(4)], args.figures, full)
    write_null_table(null, args.figures)
    write_diagnostic_table(diagnostics, rates, args.figures)
    write_supporting_tables(diagnostics, rates, args.figures)
    print("Generated five main figures, three companion figures and five tables.")


if __name__ == "__main__":
    main()
