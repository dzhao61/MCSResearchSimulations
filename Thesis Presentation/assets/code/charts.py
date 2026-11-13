"""Charts for the replanned Welch MI talk (5 November plan).

Every figure is drawn at the size it occupies on the slide, so point sizes match the
projected sizes. Data come from ../data (written by extract_data.py); images go to ../charts.
"""
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter, NullLocator
import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data") if os.path.isdir(os.path.join(HERE, "data")) else os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "charts") if os.path.isdir(os.path.join(HERE, "charts")) else os.path.join(HERE, "..", "charts")

for f in glob.glob(os.path.expanduser("~/.fonts/Lato-*.ttf")):
    font_manager.fontManager.addfont(f)

TEXT = "#4D4D4D"
GRID = "#EDEDED"
NAVY = "#1F3A5C"
ORANGE = "#E97132"
CHARCOAL = "#3A3A3A"
GREY = "#888888"
OK_BLUE, OK_ORANGE, OK_GREEN = "#0072B2", "#E69F00", "#009E73"
K_COLOURS = {2: "#3B6FA0", 4: "#C7792A", 8: "#2E8B6E", 16: "#A53648"}

plt.rcParams.update({
    "font.family": "Lato", "font.size": 13, "axes.labelsize": 13, "xtick.labelsize": 12,
    "ytick.labelsize": 12, "legend.fontsize": 12.5, "axes.edgecolor": "#B5B5B5", "axes.labelcolor": TEXT,
    "xtick.color": "#9A9A9A", "ytick.color": "#9A9A9A", "xtick.labelcolor": "#666666", "ytick.labelcolor": "#666666",
    "text.color": TEXT, "axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.minor.width": 0.6, "xtick.major.size": 3.5, "ytick.major.size": 3.5,
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 300,
    "mathtext.fontset": "custom", "mathtext.rm": "Lato", "mathtext.it": "Lato:italic", "mathtext.bf": "Lato:bold",
})

NS = [10, 20, 50, 100, 250, 500, 1000, 2500, 10000, 50000]
METHOD = {
    "normal_wald": dict(c=NAVY, ls="-", marker="o", filled=True, label="Wald"),
    "expanded_welch": dict(c=ORANGE, ls="--", marker="s", filled=False, label="Expanded Welch"),
}
GRID_METHOD = {
    "normal_wald": dict(ls="-", marker="o", filled=True, label="Wald"),
    "expanded_welch": dict(ls="--", marker="s", filled=False, label="Expanded Welch"),
}


def thousands(x, _p=None):
    return f"{int(round(x)):,}"


def n_axis(ax, labels=True):
    ax.set_xscale("log")
    ax.set_xlim(7, 72000)
    ax.xaxis.set_major_locator(FixedLocator([10, 100, 1000, 10000]))
    ax.xaxis.set_minor_locator(FixedLocator(NS))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(FuncFormatter(thousands) if labels else NullFormatter())
    ax.tick_params(axis="x", which="minor", length=2.5)


def pct(v, _p=None):
    return f"{v:g}%"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"))
    fig.savefig(os.path.join(OUT, name + ".svg"))
    plt.close(fig)


def line(ax, x, y, colour, ls, marker, filled, lo=None, hi=None, ms=5.5, lw=2.0, alpha=0.15):
    if lo is not None:
        ax.fill_between(x, lo, hi, color=colour, alpha=alpha, lw=0)
    ax.plot(x, y, ls=ls, color=colour, lw=lw, marker=marker, ms=ms, mfc=colour if filled else "white",
            mec=colour, mew=1.3)


def grid_y(ax):
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- Slide 4
def slide04():
    fig, ax = plt.subplots(figsize=(5.9, 3.45))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.17)
    x = np.linspace(-4.6, 4.6, 1201)
    zc, tc = stats.norm.ppf(0.975), stats.t.ppf(0.975, 5)
    for sgn in (-1, 1):
        xs = x[sgn * x >= tc]
        ax.fill_between(xs, 0, stats.t.pdf(xs, 5), color=ORANGE, alpha=0.18, lw=0)
    ax.plot(x, stats.norm.pdf(x), color=NAVY, lw=2.2)
    ax.plot(x, stats.t.pdf(x, 5), color=ORANGE, lw=2.2, ls="--")
    for sgn in (-1, 1):
        ax.vlines(sgn * zc, 0, 0.30, color=NAVY, lw=1.2, ls=(0, (4, 3)))
        ax.vlines(sgn * tc, 0, 0.30, color=ORANGE, lw=1.2, ls=(0, (1, 2)))
        ax.text(sgn * zc, 0.315, f"{'−' if sgn < 0 else ''}1.96", color=NAVY, fontsize=12.5, fontweight="bold",
                ha="left" if sgn < 0 else "right")
        ax.text(sgn * tc, 0.315, f"{'−' if sgn < 0 else ''}2.57", color=ORANGE, fontsize=12.5, fontweight="bold",
                ha="right" if sgn < 0 else "left")
    ax.text(-4.5, 0.415, "Standard normal", color=NAVY, fontsize=13, fontweight="bold", ha="left")
    ax.text(4.5, 0.415, "Student t, 5 df", color=ORANGE, fontsize=13, fontweight="bold", ha="right")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(0, 0.45)
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_xticklabels(["−4", "−2", "0", "2", "4"])
    ax.set_xlabel("Standardised statistic T")
    save(fig, "slide04_reference_distributions")


# ---------------------------------------------------------------- Slide 7
def slide07():
    d = pd.read_csv(os.path.join(DATA, "slide07_variance_inputs_4x4.csv")).sort_values("n")
    assert list(d.n) == NS
    c = d[d.n == 1000].iloc[0]
    # top: mean ratio
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.95, bottom=0.08)
    ax.axhline(1, color="#AAAAAA", lw=1.0)
    line(ax, d.n, d.mean_ratio, CHARCOAL, "-", "o", True, d.mean_ratio - 1.96 * d.mean_ratio_mcse,
         d.mean_ratio + 1.96 * d.mean_ratio_mcse)
    ax.set_ylim(0, 5.5)
    ax.set_yticks([1, 3, 5])
    n_axis(ax, labels=False)
    grid_y(ax)
    ax.annotate("n = 1,000: +19%", xy=(1000, c.mean_ratio), xytext=(1900, 2.9), fontsize=13, fontweight="bold",
                color=CHARCOAL, arrowprops=dict(arrowstyle="-", color=CHARCOAL, lw=0.9, shrinkA=2, shrinkB=4))
    save(fig, "slide07_mean_ratio")
    # bottom: variance ratios
    fig, ax = plt.subplots(figsize=(6.4, 2.15))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.96, bottom=0.26)
    ax.axhline(1, color="#AAAAAA", lw=1.0)
    line(ax, d.n, d.variance_ratio, NAVY, "-", "o", True, d.variance_ratio - 1.96 * d.variance_ratio_mcse,
         d.variance_ratio + 1.96 * d.variance_ratio_mcse)
    line(ax, d.n, d.plugin_variance_ratio, ORANGE, "--", "s", False,
         d.plugin_variance_ratio - 1.96 * d.plugin_variance_ratio_mcse,
         d.plugin_variance_ratio + 1.96 * d.plugin_variance_ratio_mcse)
    ax.set_ylim(0.4, 1.75)
    ax.set_yticks([0.5, 1.0, 1.5])
    n_axis(ax)
    grid_y(ax)
    ax.set_xlabel("Observations per population, n (log scale)")
    ax.text(115, 1.6, "sample-based inputs", color=ORANGE, fontsize=13, fontweight="bold", va="center")
    ax.text(26, 0.55, "population-based inputs", color=NAVY, fontsize=13, fontweight="bold", va="center")
    ax.annotate("n = 1,000: −3%", xy=(1000, c.variance_ratio), xytext=(1900, 0.62), fontsize=13, fontweight="bold",
                color=NAVY, arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, shrinkA=2, shrinkB=4))
    save(fig, "slide07_variance_ratio")


# ---------------------------------------------------------------- Slide 8
def slide08():
    d = pd.read_csv(os.path.join(DATA, "slide08_B5_near_independence_df.csv")).sort_values("mi")
    assert len(d) == 7
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.97, bottom=0.14)
    ax.fill_between(d.mi, d.nu_mom - 1.96 * d.nu_mom_mcse, d.nu_mom + 1.96 * d.nu_mom_mcse, color=CHARCOAL, alpha=0.15,
                    lw=0)
    ax.fill_between(d.mi, d.df_mean - 1.96 * d.df_mean_mcse, d.df_mean + 1.96 * d.df_mean_mcse, color=ORANGE,
                    alpha=0.18, lw=0)
    ax.plot(d.mi, d.nu_mom, color=CHARCOAL, lw=2.0, marker="s", ms=6, mfc="white", mec=CHARCOAL, mew=1.3)
    ax.plot(d.mi, d.df_mean, color=ORANGE, lw=2.0, marker="o", ms=6)
    ax.plot(d.mi, d.nu_fo, color=NAVY, lw=1.8, ls=":", marker="^", ms=6, mfc="white", mec=NAVY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(6e-5, 0.09)
    ax.set_ylim(0.06, 90)
    ax.xaxis.set_major_locator(FixedLocator([1e-4, 1e-3, 1e-2]))
    ax.xaxis.set_minor_locator(FixedLocator(list(d.mi)))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
    ax.yaxis.set_major_locator(FixedLocator([0.1, 1, 10]))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
    ax.set_xlabel("Population MI, nats (log scale)")
    ax.set_ylabel("Component degrees of freedom (log scale)")
    grid_y(ax)
    ax.text(1.15e-4, 23.0, "target (measured from 100,000 samples)", color=CHARCOAL, fontsize=13, fontweight="bold")
    ax.text(1.15e-4, 3.6, "mean sample-based estimate", color=ORANGE, fontsize=13, fontweight="bold", va="top")
    ax.text(1.6e-3, 0.11, "population-based value", color=NAVY, fontsize=13, fontweight="bold")
    lo, hi = d.df_mean.iloc[0], d.nu_mom.iloc[0]
    ax.annotate("", xy=(1.45e-4, lo * 1.07), xytext=(1.45e-4, hi / 1.07),
                arrowprops=dict(arrowstyle="|-|,widthA=0.25,widthB=0.25", color=CHARCOAL, lw=1.0))
    ax.text(1.65e-4, (lo * hi) ** 0.5 * 1.05, "about half the target", color=CHARCOAL, fontsize=10.5, va="center")
    save(fig, "slide08_near_independence_df")


# ---------------------------------------------------------------- Slide 9: all 360 null settings
def paired(prefix):
    d = pd.concat([pd.read_csv(os.path.join(DATA, f"B_{prefix}_{p}.csv"))
                   for p in ["uniform", "same_skew", "different_skew"]])
    w = d[d.method == "normal_wald"].set_index("configuration_id")
    e = d[d.method == "expanded_welch"].set_index("configuration_id")
    x = w.join(e[["rejection_rate"]], rsuffix="_ew").rename(columns={"rejection_rate": "wald", "rejection_rate_ew": "ew"})
    assert len(x) == 360 and (x.ew <= x.wald + 1e-12).all()
    return x


def slide09():
    x = paired("null")
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    fig.subplots_adjust(left=0.18, right=0.97, top=0.97, bottom=0.14)
    lo, hi = 0.0005, 0.5
    assert x.wald.min() > lo and x.ew.min() > lo and x.wald.max() < hi
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.axvspan(0.05, hi, color=ORANGE, alpha=0.07, lw=0, zorder=0)
    ax.axvspan(lo, 0.05, color=NAVY, alpha=0.06, lw=0, zorder=0)
    ax.plot([lo, hi], [lo, hi], color="#9A9A9A", lw=1.0, zorder=1)
    ax.axvline(0.05, color="#555555", lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.axhline(0.05, color="#555555", lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.scatter(x.wald, x.ew, s=14, color=CHARCOAL, alpha=0.55, lw=0, zorder=2)
    ex = x[(x.k == 4) & (x.profile == "uniform") & (x.n_p == 20) & np.isclose(x.common_mi, 0.02)].iloc[0]
    bias = x[(x.k == 16) & (x.profile == "different_skew") & (x.n_p == 1000) & np.isclose(x.common_mi, 0.005)].iloc[0]
    assert round(ex.wald, 4) == 0.0835 and round(ex.ew, 4) == 0.049
    assert round(bias.wald, 4) == 0.3638 and round(bias.ew, 4) == 0.3438
    ax.scatter([ex.wald, bias.wald], [ex.ew, bias.ew], s=70, facecolors="none", edgecolors=ORANGE, lw=2.0, zorder=3)
    ax.annotate("8.35% to 4.90%", xy=(ex.wald, ex.ew), xytext=(0.0105, 0.0024), fontsize=11.5, color=CHARCOAL,
                arrowprops=dict(arrowstyle="-", color=CHARCOAL, lw=0.8, shrinkB=5))
    ax.annotate("36.38% to 34.38%", xy=(bias.wald, bias.ew), xytext=(0.06, 0.0033), fontsize=11.5, color=CHARCOAL,
                arrowprops=dict(arrowstyle="-", color=CHARCOAL, lw=0.8, shrinkB=5))
    pct_ticks = FuncFormatter(lambda v, _p: f"{v * 100:g}%")
    for a in (ax.xaxis, ax.yaxis):
        a.set_major_locator(FixedLocator([0.001, 0.01, 0.05, 0.2]))
        a.set_major_formatter(pct_ticks)
        a.set_minor_locator(NullLocator())
    ax.set_xlabel("Wald false-positive rate (log scale)")
    ax.set_ylabel("Expanded Welch false-positive rate\n(log scale)", linespacing=1.1)
    ax.text(0.0007, 0.25, "Wald too low", color=NAVY, fontsize=13, fontweight="bold", va="center")
    ax.text(0.47, 0.00075, "Wald too high", color="#B4501A", fontsize=13, fontweight="bold", ha="right")
    ax.text(0.0011, 0.00155, "no change", color="#8A8A8A", fontsize=10.5, rotation=40, rotation_mode="anchor")
    save(fig, "slide09_null_all_settings")


# ---------------------------------------------------------------- Slide 11: power lost across all settings
def slide11():
    x = paired("power")
    x["loss"] = (x.wald - x.ew) * 100
    g = x.groupby("n_p").loss
    med, mn, mx = g.median(), g.min(), g.max()
    assert list(med.index) == NS and (g.size() == 36).all()
    assert mx.loc[10000] < 0.32
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.97, bottom=0.14)
    ax.fill_between(med.index, mn, mx, color=ORANGE, alpha=0.16, lw=0)
    line(ax, med.index, med, ORANGE, "-", "o", True)
    ax.set_ylim(0, 14.5)
    ax.set_yticks([0, 5, 10])
    n_axis(ax)
    grid_y(ax)
    ax.set_xlabel("Observations per population, n (log scale)")
    ax.set_ylabel("Power lost (percentage points)")
    ax.text(14, 12.6, "range across the 36 settings at each n", color="#B4501A", fontsize=11.5)
    ax.text(26, 0.35, "median", color=ORANGE, fontsize=12.5, fontweight="bold")
    ax.annotate("n = 10,000: under 0.32\npoints in every setting", xy=(10000, mx.loc[10000]), xytext=(1300, 5.2),
                fontsize=12, color=CHARCOAL, arrowprops=dict(arrowstyle="-", color=CHARCOAL, lw=0.9, shrinkB=4))
    save(fig, "slide11_power_loss_all_settings")


# ---------------------------------------------------------------- Slide 12: wrong-direction rejections
def slide12():
    from matplotlib.colors import LinearSegmentedColormap
    d = pd.read_csv(os.path.join(DATA, "slide12_wrong_direction_all.csv"))
    assert len(d) == 360
    s = d[(d.profile == "different_skew") & np.isclose(d.gap, 0.01)].copy()
    s["share"] = s.expanded_positive_rejections / (s.expanded_positive_rejections + s.expanded_negative_rejections)
    z = s.pivot_table(index="k", columns="n_p", values="share")
    cell = s[(s.k == 16) & (s.n_p == 1000)].iloc[0]
    assert int(cell.expanded_positive_rejections) == 9659 and int(cell.expanded_negative_rejections) == 3
    ks = [16, 8, 4, 2]
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.17)
    cmap = LinearSegmentedColormap.from_list("wrong", ["#FFFFFF", "#F8DCCB", ORANGE, "#8A3A10"])
    ax.imshow(z.loc[ks, NS].values, aspect="auto", cmap=cmap, vmin=0, vmax=1)
    for i, k in enumerate(ks):
        for j, n in enumerate(NS):
            v = z.loc[k, n]
            ax.text(j, i, f"{v * 100:.0f}", ha="center", va="center", fontsize=11.5,
                    color="white" if v > 0.6 else CHARCOAL)
    ax.add_patch(plt.Rectangle((NS.index(1000) - 0.5, -0.5), 1, 1, fill=False, ec=NAVY, lw=2.6))
    ax.set_xticks(range(len(NS)))
    ax.set_xticklabels([thousands(n) for n in NS], rotation=40, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(ks)))
    ax.set_yticklabels([f"{k}×{k}" for k in ks])
    ax.tick_params(length=0)
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlabel("Observations per population, n")
    save(fig, "slide12_wrong_direction_heatmap")


def backup04():
    d = pd.read_csv(os.path.join(DATA, "B4_approximation_ratios.csv"))
    fs = 13
    fig, axes = plt.subplots(3, 2, figsize=(12.1, 5.3), sharex=True)
    fig.subplots_adjust(left=0.12, right=0.985, top=1 - 0.8 / 5.3, bottom=0.55 / 5.3, hspace=0.22, wspace=0.07)
    rows = [("mean_ratio", r"$E(\hat{V})\,/\,V$", (0.8, 15), [1, 2, 5, 10]),
            ("variance_ratio", "population-\nbased\ninputs", (0.1, 2.6), [0.2, 0.5, 1, 2]),
            ("plugin_variance_ratio", "sample-\nbased\ninputs", (0.1, 2.6), [0.2, 0.5, 1, 2])]
    for ri, (col, lab, ylim, yt) in enumerate(rows):
        for ci, side in enumerate(["p", "q"]):
            ax = axes[ri, ci]
            ax.axhline(1, color="#888888", lw=0.9)
            for k, colour in K_COLOURS.items():
                m = d[(d.side == side) & (d.k == k)].sort_values("n")
                assert list(m.n) == NS
                ax.plot(m.n, m[col], color=colour, lw=1.7, marker="o", ms=4)
            ax.set_yscale("log")
            ax.set_ylim(*ylim)
            ax.yaxis.set_major_locator(FixedLocator(yt))
            ax.yaxis.set_minor_locator(NullLocator())
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
            ax.tick_params(labelsize=fs - 1)
            n_axis(ax, labels=(ri == 2))
            grid_y(ax)
            if ci == 0:
                ax.set_ylabel(lab, fontsize=fs - 1, rotation=0, ha="right", va="center", labelpad=14)
            else:
                ax.tick_params(labelleft=False)
            if ri == 0:
                ax.set_title(["Population P: margins m", "Population Q: margins m"][ci] +
                             [r"$_k$(0.7)", r"$_k$(0.8)"][ci], fontsize=fs, fontweight="bold", color=TEXT, pad=6)
    for ax in axes[2]:
        ax.set_xlabel("Observations per population, n (log scale)", fontsize=fs)
    hs = [Line2D([], [], color=c, lw=2, marker="o", ms=4.5, label=f"{k}×{k}") for k, c in K_COLOURS.items()]
    leg = fig.legend(handles=[Line2D([], [], lw=0, label="Table size")] + hs, loc="upper left", bbox_to_anchor=(0.11, 1.0),
                     ncol=5, frameon=False, fontsize=fs, handlelength=1.8, columnspacing=1.4)
    leg.get_texts()[0].set_fontweight("bold")
    leg.legend_handles[0].set_visible(False)
    save(fig, "B4_approximation_ratios")


# ---------------------------------------------------------------- B6-B11
def grid_backup(path, key, colours, colour_title, ylims, ysteps, ylabel, name, five_line):
    d = pd.read_csv(os.path.join(DATA, path))
    fs = 13
    fig = plt.figure(figsize=(12.1, 5.3))
    outer = fig.add_gridspec(2, 2, left=0.06, right=0.985, top=1 - 0.62 / 5.3, bottom=0.55 / 5.3,
                             hspace=0.34, wspace=0.09)
    for idx, k in enumerate([2, 4, 8, 16]):
        r, c = divmod(idx, 2)
        inner = outer[r, c].subgridspec(2, 1, height_ratios=[3.4, 1], hspace=0.1)
        ax = fig.add_subplot(inner[0])
        axv = fig.add_subplot(inner[1], sharex=ax)
        for val, colour in colours.items():
            for method, st in GRID_METHOD.items():
                m = d[(d.k == k) & np.isclose(d[key], val) & (d.method == method)].sort_values("n_p")
                assert list(m.n_p) == NS
                line(ax, m.n_p, m.rejection_rate * 100, colour, st["ls"], st["marker"], st["filled"],
                     m.rejection_low * 100, m.rejection_high * 100, ms=3.8, lw=1.4, alpha=0.12)
                line(axv, m.n_p, m.valid_rate * 100, colour, st["ls"], st["marker"], st["filled"], ms=2.6, lw=1.0)
        ax.set_ylim(0, ylims[k])
        ax.set_yticks(np.arange(ysteps[k], ylims[k] + 0.1, ysteps[k]))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
        ax.tick_params(labelsize=fs - 1)
        grid_y(ax)
        if five_line:
            ax.axhline(5, color="#555555", lw=0.9, ls=(0, (2, 2)))
        n_axis(ax, labels=False)
        n_axis(axv, labels=(r == 1))
        axv.set_ylim(-12, 115)
        axv.set_yticks([0, 100])
        axv.tick_params(labelsize=fs - 2.5)
        axv.grid(axis="y", color=GRID, lw=0.8)
        axv.text(0.995, 0.42, "calculation success (%)", transform=axv.transAxes, ha="right", va="center", fontsize=fs - 3,
                 color="#666666", style="italic")
        ax.set_title(f"{k}×{k}", color=ORANGE, fontweight="bold", fontsize=fs, loc="left", pad=4)
        if r == 1:
            axv.set_xlabel("Observations per population, n (log scale)", fontsize=fs - 1)
    fig.text(0.01, 0.56, ylabel, rotation=90, ha="center", va="center", fontsize=fs)
    blank = Line2D([], [], lw=0, label=colour_title)
    hs = [blank] + [Line2D([], [], color=cv, lw=4, label={0.3: "0.30"}.get(v, f"{v:g}")) for v, cv in colours.items()]
    leg = fig.legend(handles=hs, loc="upper left", bbox_to_anchor=(0.0, 1.0), ncol=4, frameon=False, fontsize=fs,
                     handlelength=1.4, columnspacing=0.9, handletextpad=0.5)
    leg.get_texts()[0].set_fontweight("bold")
    leg.legend_handles[0].set_visible(False)
    mh = [Line2D([], [], color="#555555", lw=1.5, ls=st["ls"], marker=st["marker"], ms=5.5,
                 mfc="#555555" if st["filled"] else "white", mec="#555555", mew=1.2, label=st["label"])
          for st in GRID_METHOD.values()]
    fig.legend(handles=mh, loc="upper right", bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False, fontsize=fs,
               handlelength=2.2, columnspacing=1.0)
    save(fig, name)


def backups_grid():
    lims = {2: 25, 4: 25, 8: 30, 16: 40}
    steps = {2: 10, 4: 10, 8: 10, 16: 20}
    mi = {0.005: OK_BLUE, 0.02: OK_ORANGE, 0.3: OK_GREEN}
    gaps = {0.005: OK_BLUE, 0.01: OK_ORANGE, 0.02: OK_GREEN}
    for i, prof in enumerate(["uniform", "same_skew", "different_skew"]):
        grid_backup(f"B_null_{prof}.csv", "common_mi", mi, "Shared MI (nats)", lims, steps, "False-positive rate (%)",
                    f"B{6 + i}_null_{prof}", True)
        grid_backup(f"B_power_{prof}.csv", "gap", gaps, "MI gap (nats)", {k: 100 for k in lims},
                    {k: 50 for k in lims}, "Power (%)", f"B{10 + i}_power_{prof}", False)


# ---------------------------------------------------------------- Slide 5 (schematic, no data)
def slide05():
    """Schematic spread of the variance estimate over repeated samples. No simulation data."""
    fig, ax = plt.subplots(figsize=(3.45, 1.85))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.2)
    fig.patch.set_alpha(0)                       # transparent, so the slide panel shows through
    ax.patch.set_alpha(0)
    x = np.linspace(0, 4.2, 801)
    y = stats.gamma.pdf(x, 6, scale=0.25)
    ax.fill_between(x, 0, y, color=ORANGE, alpha=0.14, lw=0)
    ax.plot(x, y, color=ORANGE, lw=2.0)
    v = 1.5                                      # the mean, near V(P)
    ax.vlines(v, 0, y.max() * 1.08, color=NAVY, lw=1.3, ls=(0, (4, 3)))
    ax.text(v + 0.06, y.max() * 1.02, r"$V(P)$", color=NAVY, fontsize=12.5, fontweight="bold", ha="left")
    for xs in (0.86, 1.12, 1.36, 1.58, 1.85, 2.3):
        ax.plot([xs], [-0.035], marker="o", ms=4.2, color=ORANGE, clip_on=False)
    h = y.max() * 0.42
    lo, hi = v - 0.61, v + 0.61                  # one standard deviation either side
    ax.annotate("", xy=(lo, h), xytext=(hi, h), arrowprops=dict(arrowstyle="<->", color=CHARCOAL, lw=1.1))
    ax.text(v - 0.1, h + 0.03, "spread", color=CHARCOAL, fontsize=12, va="bottom", ha="right")
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 4.2)
    ax.set_ylim(-0.07, y.max() * 1.2)
    ax.spines["bottom"].set_position(("data", -0.07))
    ax.set_xlabel("Each dot: one sample’s estimate", labelpad=4)
    save(fig, "slide05_vhat_spread")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    slide04()
    slide05()
    slide07()
    slide08()
    slide09()
    slide11()
    slide12()
    backup04()
    backups_grid()
    print(sorted(f for f in os.listdir(OUT) if f.endswith(".png")))
