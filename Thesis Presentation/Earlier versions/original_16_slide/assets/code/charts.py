"""Presentation charts for the Welch MI talk.

Each figure is drawn at the exact size it occupies on the slide, so font
sizes in points match the projected sizes. Data come from ./data, written
by extract_data.py.
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
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "charts")

for f in glob.glob(os.path.expanduser("~/.fonts/Lato-*.ttf")):
    font_manager.fontManager.addfont(f)

TEXT = "#333333"
GRID = "#E6E6E6"
ORANGE = "#ED7D31"
NAVY = "#1F3A5C"
BLUE, OKORANGE, GREEN = "#0072B2", "#E69F00", "#009E73"
CRIMSON, MOMGREEN = "#A53648", "#34866F"

plt.rcParams.update({
    "font.family": "Lato",
    "font.size": 20,
    "axes.labelsize": 20,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "legend.fontsize": 20,
    "axes.edgecolor": "#888888",
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "text.color": TEXT,
    "axes.linewidth": 1.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 300,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Lato",
    "mathtext.it": "Lato:italic",
    "mathtext.bf": "Lato:bold",
})

NS = [10, 20, 50, 100, 250, 500, 1000, 2500, 10000, 50000]
MI_COLOURS = {0.005: BLUE, 0.02: OKORANGE, 0.3: GREEN}
GAP_COLOURS = {0.005: BLUE, 0.01: OKORANGE, 0.02: GREEN}
METHOD_STYLE = {
    "normal_wald": dict(ls="-", marker="o", filled=True, label="Normal Wald"),
    "expanded_welch": dict(ls="--", marker="s", filled=False, label="Expanded Welch"),
}


def thousands(x, _pos=None):
    return f"{int(round(x)):,}"


def n_axis(ax, labels=True):
    ax.set_xscale("log")
    ax.set_xlim(7, 72000)
    ax.xaxis.set_major_locator(FixedLocator([10, 100, 1000, 10000]))
    ax.xaxis.set_minor_locator(FixedLocator(NS))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(FuncFormatter(thousands) if labels else NullFormatter())
    ax.tick_params(axis="x", which="minor", length=4)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"))
    fig.savefig(os.path.join(OUT, name + ".svg"))
    plt.close(fig)


def method_line(ax, x, y, colour, method, lo=None, hi=None, ms=8, lw=2.4):
    st = METHOD_STYLE[method]
    if lo is not None:
        ax.fill_between(x, lo, hi, color=colour, alpha=0.16, lw=0)
    ax.plot(x, y, ls=st["ls"], color=colour, lw=lw, marker=st["marker"], ms=ms,
            mfc=colour if st["filled"] else "white", mec=colour, mew=1.8)


def method_handles(colour="#333333"):
    return [Line2D([], [], color=colour, lw=2.4, ls=s["ls"], marker=s["marker"], ms=9,
                   mfc=colour if s["filled"] else "white", mec=colour, mew=1.8, label=s["label"])
            for s in METHOD_STYLE.values()]


def colour_handles(colours, fmt):
    return [Line2D([], [], color=c, lw=7, label=fmt(v)) for v, c in colours.items()]


def legend_row(fig, colours, colour_title, y, x0, fs, methods=False, hl=2.2, cs=1.0):
    blank = Line2D([], [], lw=0, label=colour_title)
    handles = [blank] + colour_handles(colours, lambda v: f"{v:g}")
    if methods:
        handles += [Line2D([], [], lw=0, label=" ")] + method_handles()
    leg = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(x0, y), ncol=len(handles),
                     frameon=False, fontsize=fs, handlelength=hl, columnspacing=cs, handletextpad=0.5)
    leg.get_texts()[0].set_fontweight("bold")
    leg.legend_handles[0].set_visible(False)
    if methods:
        leg.legend_handles[4].set_visible(False)
    return leg


def method_legend(ax, fs, loc="upper left", anchor=(0.0, 1.02)):
    leg = ax.legend(handles=method_handles(), loc=loc, bbox_to_anchor=anchor, frameon=False,
                    fontsize=fs, handlelength=2.6, borderaxespad=0.2, labelspacing=0.35)
    return leg


def rate_chart(df, key, colours, w, h, ymax, ylabel, colour_title, name, five_line,
               ytick_step, annotate=None, fs=20):
    """Rejection-rate chart with a validity strip below the main axes and a legend row on top."""
    fig, (ax, axv) = plt.subplots(2, 1, figsize=(w, h), sharex=True,
                                  gridspec_kw={"height_ratios": [4.0, 1.0], "hspace": 0.14})
    fig.subplots_adjust(left=0.085, right=0.985, top=1 - 0.62 / h, bottom=0.88 / h)
    for val, colour in colours.items():
        for method in METHOD_STYLE:
            d = df[np.isclose(df[key], val) & (df.method == method)].sort_values("n_p")
            assert list(d.n_p) == NS
            method_line(ax, d.n_p, d.rejection_rate * 100, colour, method,
                        d.rejection_low * 100, d.rejection_high * 100)
            method_line(axv, d.n_p, d.valid_rate * 100, colour, method,
                        d.valid_low * 100, d.valid_high * 100, ms=6, lw=1.8)
    ax.set_ylim(0, ymax)
    ax.set_yticks(np.arange(0, ymax + 0.1, ytick_step))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color=GRID, lw=1)
    ax.set_axisbelow(True)
    if five_line:
        ax.axhline(5, color="#222222", lw=1.6, ls=(0, (2, 2)))
        ax.text(7.6, 5.7, "5% target", ha="left", va="bottom", fontsize=fs - 2, color="#222222")
    if annotate:
        annotate(ax)
    n_axis(ax, labels=False)
    n_axis(axv)
    axv.set_ylim(-10, 112)
    axv.set_yticks([0, 100])
    axv.set_ylabel("Valid (%)", fontsize=fs - 2)
    axv.grid(axis="y", color=GRID, lw=1)
    axv.set_xlabel("Observations per population, n (log scale)")
    fig.align_ylabels([ax, axv])
    legend_row(fig, colours, colour_title, 1.0, 0.075, fs)
    method_legend(ax, fs)
    save(fig, name)


# ---------------------------------------------------------------- Slide 5
def slide05():
    w, h = 7.05, 3.15
    fig, ax = plt.subplots(figsize=(w, h))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.27)
    x = np.linspace(-5, 5, 1201)
    zc, tc = stats.norm.ppf(0.975), stats.t.ppf(0.975, 3)
    ax.plot(x, stats.norm.pdf(x), color=ORANGE, lw=3)
    ax.plot(x, stats.t.pdf(x, 3), color=NAVY, lw=3, ls="--")
    for c, col in [(zc, ORANGE), (tc, NAVY)]:
        for s in (-1, 1):
            ax.vlines(s * c, 0, 0.075, color=col, lw=3)
    ax.text(0.95, 0.315, "Standard normal", color=ORANGE, fontsize=20, fontweight="bold", ha="left")
    ax.text(1.75, 0.165, "Student t, 3 df", color=NAVY, fontsize=20, fontweight="bold", ha="left")
    ax.set_xticks([-tc, -zc, 0, zc, tc])
    ax.set_xticklabels(["−3.18", "−1.96", "0", "1.96", "3.18"])
    for lab, col in zip(ax.get_xticklabels(), [NAVY, ORANGE, TEXT, ORANGE, NAVY]):
        lab.set_color(col)
        lab.set_fontweight("bold" if col != TEXT else "normal")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(0, 0.45)
    ax.set_xlabel("Two-sided 5% cutoffs")
    save(fig, "slide05_reference_distributions")


# ---------------------------------------------------------------- Slide 8
def slide08():
    d = pd.read_csv(os.path.join(DATA, "slide08_variance_inputs.csv")).sort_values("n")
    assert list(d.n) == NS
    w, h = 5.95, 3.75
    specs = [
        ("slide08_mean_ratio", [("mean_ratio", "mean_ratio_mcse", CRIMSON, "-", "o", "Mean estimate")],
         (0.9, 20), [1, 2, 5, 10, 20]),
        ("slide08_variance_ratio", [("variance_ratio", "variance_ratio_mcse", "#222222", ":", "s", "Population inputs"),
                                    ("plugin_variance_ratio", "plugin_variance_ratio_mcse", CRIMSON, "-", "o",
                                     "Sample-based inputs")],
         (0.1, 4), [0.1, 0.2, 0.5, 1, 2, 4]),
    ]
    for name, series, ylim, yt in specs:
        fig, ax = plt.subplots(figsize=(w, h))
        fig.subplots_adjust(left=0.15, right=0.97, top=0.96, bottom=0.21)
        ax.axhline(1, color="#888888", lw=1.6)
        for col, mc, colour, ls, mk, lab in series:
            lo, hi = d[col] - 1.96 * d[mc], d[col] + 1.96 * d[mc]
            ax.fill_between(d.n, lo.clip(lower=1e-3), hi, color=colour, alpha=0.16, lw=0)
            ax.plot(d.n, d[col], color=colour, ls=ls, lw=2.6, marker=mk, ms=8,
                    mfc=colour if mk == "o" else "white", mec=colour, mew=1.8, label=lab)
        ax.set_yscale("log")
        ax.set_ylim(*ylim)
        ax.yaxis.set_major_locator(FixedLocator(yt))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
        n_axis(ax)
        ax.set_xlabel("Observations, n (log scale)")
        ax.grid(axis="y", color=GRID, lw=1)
        ax.set_axisbelow(True)
        if len(series) > 1:
            ax.text(22, 2.75, "Sample-based inputs", color=CRIMSON, fontsize=20, fontweight="bold")
            ax.text(700, 0.36, "Population inputs", color="#222222", fontsize=20, fontweight="bold")
        save(fig, name)


# ---------------------------------------------------------------- Slide 9
def slide09():
    d = pd.read_csv(os.path.join(DATA, "slide09_near_independence_df.csv")).sort_values("mi")
    assert len(d) == 7
    w, h = 8.3, 4.85
    fig, ax = plt.subplots(figsize=(w, h))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.97, bottom=0.17)
    ax.fill_between(d.mi, d.df_mean - 1.96 * d.df_mean_mcse, d.df_mean + 1.96 * d.df_mean_mcse,
                    color=CRIMSON, alpha=0.18, lw=0)
    ax.fill_between(d.mi, d.nu_mom - 1.96 * d.nu_mom_mcse, d.nu_mom + 1.96 * d.nu_mom_mcse,
                    color=MOMGREEN, alpha=0.18, lw=0)
    ax.plot(d.mi, d.nu_mom, color=MOMGREEN, lw=2.8, marker="s", ms=8, mfc="white", mec=MOMGREEN, mew=1.8)
    ax.plot(d.mi, d.df_mean, color=CRIMSON, lw=2.8, marker="o", ms=8)
    ax.plot(d.mi, d.nu_fo, color="#111111", lw=2.6, ls=":", marker="^", ms=8, mfc="white", mec="#111111")
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
    ax.set_ylabel("Component degrees of freedom")
    ax.grid(axis="y", color=GRID, lw=1)
    ax.set_axisbelow(True)
    ax.text(1.3e-4, 15.5, "Sampling-moment target", color=MOMGREEN, fontsize=20, fontweight="bold")
    ax.text(1.15e-4, 3.6, "Mean estimated\ncomponent df", color=CRIMSON, fontsize=20, fontweight="bold",
            va="top", linespacing=1.1)
    ax.text(5.6e-4, 0.12, "Population first-order value", color="#111111", fontsize=20, fontweight="bold")
    save(fig, "slide09_near_independence_df")


# ---------------------------------------------------------------- Slide 11
def slide11():
    d = pd.read_csv(os.path.join(DATA, "slide11_null_16x16_different_skew.csv"))

    def note(ax):
        ax.annotate("Common MI 0.005, n = 1,000\nWald 36.38%\nExpanded Welch 34.38%",
                    xy=(1000, 36.381), xytext=(3300, 27.5), fontsize=20, ha="left", va="center",
                    bbox=dict(boxstyle="round,pad=0.35,rounding_size=0.2", fc="#FFF1E8", ec="#F5C6A7", lw=1.2),
                    arrowprops=dict(arrowstyle="-", color="#555555", lw=1.4, shrinkA=0, shrinkB=6))

    rate_chart(d, "common_mi", MI_COLOURS, 12.2, 4.75, 40, "False positives (%)",
               "Common population MI (nats)", "slide11_null_rates", True, 10, annotate=note)


# ---------------------------------------------------------------- Slide 12
def slide12():
    d = pd.read_csv(os.path.join(DATA, "slide12_power_4x4_uniform.csv"))
    rate_chart(d, "gap", GAP_COLOURS, 12.2, 4.2, 100, "Power (%)",
               "MI-gap magnitude (nats)", "slide12_power", False, 25)


# ---------------------------------------------------------------- Slide 13
def slide13():
    d = pd.read_csv(os.path.join(DATA, "slide13_power_16x16_different_skew_gap001.csv"))
    w, h = 8.05, 4.9
    fig, (ax, axv) = plt.subplots(2, 1, figsize=(w, h), sharex=True,
                                  gridspec_kw={"height_ratios": [4.2, 1.0], "hspace": 0.12})
    fig.subplots_adjust(left=0.12, right=0.97, top=0.97, bottom=0.17)
    for method in METHOD_STYLE:
        m = d[d.method == method].sort_values("n_p")
        assert list(m.n_p) == NS
        method_line(ax, m.n_p, m.rejection_rate * 100, OKORANGE, method, m.rejection_low * 100,
                    m.rejection_high * 100)
        method_line(axv, m.n_p, m.valid_rate * 100, OKORANGE, method, m.valid_low * 100,
                    m.valid_high * 100, ms=6, lw=1.8)
    ax.axvline(1000, color="#888888", lw=1.4, ls=(0, (3, 3)))
    ax.text(1150, 88, "n = 1,000", fontsize=19, color="#555555", va="center")
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Power (%)")
    ax.grid(axis="y", color=GRID, lw=1)
    ax.set_axisbelow(True)
    ax.legend(handles=method_handles(OKORANGE), loc="upper left", frameon=False, fontsize=19,
              handlelength=2.6, title="MI gap 0.01 nats", title_fontsize=19, alignment="left")
    ax.get_legend().get_title().set_fontweight("bold")
    n_axis(ax, labels=False)
    n_axis(axv)
    axv.set_ylim(-8, 108)
    axv.set_yticks([0, 100])
    axv.set_ylabel("Valid (%)", fontsize=18)
    axv.yaxis.set_label_coords(-0.085, 0.5)
    axv.grid(axis="y", color=GRID, lw=1)
    axv.set_xlabel("Observations per population, n (log scale)")
    save(fig, "slide13_direction_power")


# ---------------------------------------------------------------- Backups B6-B9
def backup_grid(path, key, colours, legend_title, ylims, ylabel, name, five_line, steps):
    d = pd.read_csv(os.path.join(DATA, path))
    fs = 18
    fig, axes = plt.subplots(2, 2, figsize=(12.2, 5.15), sharex=True)
    fig.subplots_adjust(left=0.075, right=0.985, top=1 - 0.95 / 5.15, bottom=0.75 / 5.15, hspace=0.32, wspace=0.12)
    for ax, k in zip(axes.flat, [2, 4, 8, 16]):
        for val, colour in colours.items():
            for method in METHOD_STYLE:
                m = d[(d.k == k) & np.isclose(d[key], val) & (d.method == method)].sort_values("n_p")
                assert list(m.n_p) == NS
                method_line(ax, m.n_p, m.rejection_rate * 100, colour, method,
                            m.rejection_low * 100, m.rejection_high * 100, ms=6, lw=2)
        ax.set_ylim(0, ylims[k])
        ax.set_yticks(np.arange(0, ylims[k] + 0.1, steps[k]))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}"))
        ax.tick_params(labelsize=fs)
        ax.grid(axis="y", color=GRID, lw=1)
        ax.set_axisbelow(True)
        if five_line:
            ax.axhline(5, color="#222222", lw=1.4, ls=(0, (2, 2)))
        n_axis(ax, labels=True)
        ax.set_title(f"{k}×{k}", color=ORANGE, fontweight="bold", fontsize=19, loc="left", pad=6)
    for ax in axes[0]:
        ax.tick_params(labelbottom=False)
    for ax in axes[1]:
        ax.set_xlabel("Observations per population, n (log scale)", fontsize=fs)
    fig.supylabel(ylabel, fontsize=fs, x=0.012)
    legend_row(fig, colours, legend_title, 1.0, 0.0, fs, hl=1.4, cs=0.8)
    fig.legend(handles=method_handles(), loc="upper right", bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False,
               fontsize=fs, handlelength=2.2, columnspacing=1.0, handletextpad=0.5)
    save(fig, name)


def backups():
    null_lims = {2: 25, 4: 25, 8: 30, 16: 40}
    null_steps = {2: 5, 4: 5, 8: 10, 16: 10}
    for prof, tag in [("uniform", "b06"), ("same_skew", "b07"), ("different_skew", "b08")]:
        backup_grid(f"backup_null_{prof}.csv", "common_mi", MI_COLOURS,
                    "Common MI (nats)", null_lims, "False-positive rate (%)",
                    f"{tag}_null_{prof}", True, null_steps)
    backup_grid("backup_power_same_skew.csv", "gap", GAP_COLOURS, "MI gap (nats)",
                {k: 100 for k in (2, 4, 8, 16)}, "Power (%)", "b09_power_same_skew", False,
                {k: 25 for k in (2, 4, 8, 16)})


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    slide05()
    slide08()
    slide09()
    slide11()
    slide12()
    slide13()
    backups()
    print(sorted(os.listdir(OUT)))
