"""Generate publication figures from the frozen validation outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = ARTICLE_DIR.parent
FIGURE_DIR = ARTICLE_DIR / "figures"

NAVY = "#17324d"
BLUE = "#2f6f8f"
ORANGE = "#d97828"
GOLD = "#e2b44a"
GREEN = "#3d8061"
GREY = "#68737d"
LIGHT = "#eef2f3"


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.bbox": "tight",
        }
    )


def method_overview() -> None:
    fig, ax = plt.subplots(figsize=(7.1, 2.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        (0.01, "Independent\ncount tables", NAVY),
        (0.21, "Plug-in MI\n$\\widehat I_P,\\widehat I_Q$", BLUE),
        (0.41, "Bias-corrected\nMI difference", GREEN),
        (0.61, "Influence\nstandard error", ORANGE),
        (0.81, "Welch-type\n$t_\\nu$ p-value", NAVY),
    ]
    width = 0.17
    for x, label, colour in boxes:
        patch = plt.Rectangle(
            (x, 0.36),
            width,
            0.34,
            facecolor=colour,
            edgecolor="none",
            linewidth=0,
        )
        ax.add_patch(patch)
        ax.text(
            x + width / 2,
            0.53,
            label,
            color="white",
            ha="center",
            va="center",
            fontsize=8.1,
            fontweight="bold",
        )

    for x in (0.18, 0.38, 0.58, 0.78):
        ax.annotate(
            "",
            xy=(x + 0.025, 0.53),
            xytext=(x, 0.53),
            arrowprops={"arrowstyle": "-|>", "color": GREY, "lw": 1.4},
        )

    ax.text(
        0.5,
        0.16,
        "$H_0:I(P)=I(Q)$ while allowing $P\\ne Q$",
        ha="center",
        va="center",
        color=NAVY,
        fontsize=10,
        fontweight="bold",
    )
    fig.savefig(FIGURE_DIR / "method_overview.pdf")
    plt.close(fig)


def evidence_summary() -> None:
    decisive = pd.read_csv(
        PROJECT_DIR / "results" / "decisive" / "method_summary.csv"
    )
    holdout = pd.read_csv(
        PROJECT_DIR / "results" / "adversarial_holdout" / "method_summary.csv"
    )
    runtime = pd.read_csv(
        PROJECT_DIR / "results" / "decisive" / "runtime_summary.csv"
    )
    permutation = pd.read_csv(
        PROJECT_DIR / "results" / "decisive" / "permutation_summary.csv"
    )

    stages = ["broad", "hard", "stress"]
    labels = ["Decisive\nbroad", "Decisive\nhard", "Decisive\nstress"]
    normal_mae = []
    welch_mae = []
    for stage in stages:
        subset = decisive[decisive["stage"] == stage].set_index("method")
        normal_mae.append(
            subset.loc["wald_normal", "mean_absolute_fpr_error_05"]
        )
        welch_mae.append(
            subset.loc["welch_reference", "mean_absolute_fpr_error_05"]
        )

    holdout_rows = [
        ("fresh_broad", "Holdout\nbroad"),
        ("frozen_hard_design", "Holdout\nhard"),
        ("fresh_strong_null", "Holdout\nstrong null"),
    ]
    for stage, label in holdout_rows:
        row = holdout[holdout["stage"] == stage].iloc[0]
        labels.append(label)
        normal_mae.append(row["normal_mae_05"])
        welch_mae.append(row["welch_mae_05"])

    normal_ms = float(runtime["median_normal_ms"].median())
    welch_ms = float(runtime["median_welch_ms"].median())
    permutation_ms = float(permutation["mean_permutation_ms"].median())

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(7.1, 3.15),
        gridspec_kw={"width_ratios": [2.15, 1]},
    )

    x = np.arange(len(labels))
    width = 0.36
    axes[0].bar(
        x - width / 2,
        normal_mae,
        width,
        color=BLUE,
        label="Normal Wald",
    )
    axes[0].bar(
        x + width / 2,
        welch_mae,
        width,
        color=ORANGE,
        label="BCW-DMI",
    )
    axes[0].set_ylabel("Mean absolute FPR error at $\\alpha=0.05$")
    axes[0].set_xticks(x, labels)
    axes[0].tick_params(axis="x", rotation=18)
    axes[0].legend(frameon=False, ncol=2, loc="upper left")
    axes[0].set_title("Calibration across decisive and holdout grids")
    axes[0].grid(axis="y", color=LIGHT, linewidth=0.8)
    axes[0].set_axisbelow(True)

    methods = ["Normal\nWald", "BCW-DMI", "Permutation\n(999)"]
    times = [normal_ms, welch_ms, permutation_ms]
    bars = axes[1].bar(methods, times, color=[BLUE, ORANGE, GREEN])
    axes[1].set_yscale("log")
    axes[1].set_ylabel("Median time per table pair (ms, log scale)")
    axes[1].set_title("Computational cost")
    axes[1].grid(axis="y", color=LIGHT, linewidth=0.8, which="both")
    axes[1].set_axisbelow(True)
    for bar, value in zip(bars, times, strict=True):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value * 1.12,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.tight_layout(w_pad=1.7)
    fig.savefig(FIGURE_DIR / "evidence_summary.pdf")
    plt.close(fig)


def degrees_of_freedom_audit() -> None:
    audit = pd.read_csv(
        PROJECT_DIR
        / "results"
        / "adversarial_holdout"
        / "variance_component_audit.csv"
    )
    naive = audit["median_naive_total_df"].to_numpy()
    empirical = audit["empirical_total_df"].to_numpy()
    predicted = audit["if_predicted_total_df"].to_numpy()

    fig, ax = plt.subplots(figsize=(3.45, 2.8))
    ax.scatter(
        naive,
        empirical,
        s=42,
        color=ORANGE,
        edgecolor="white",
        linewidth=0.5,
        label="Empirical moment df",
        zorder=3,
    )
    ax.scatter(
        naive,
        predicted,
        s=42,
        color=GREEN,
        marker="s",
        edgecolor="white",
        linewidth=0.5,
        label="Variance-IF prediction",
        zorder=3,
    )
    limit_low = min(20.0, empirical.min() * 0.8)
    limit_high = naive.max() * 1.25
    ax.plot(
        [limit_low, limit_high],
        [limit_low, limit_high],
        color=GREY,
        linestyle="--",
        linewidth=1,
        label="Identity",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(limit_low, limit_high)
    ax.set_ylim(limit_low, limit_high)
    ax.set_xlabel("Implemented naive total df")
    ax.set_ylabel("Audited total df")
    ax.set_title("Variance-component qualification")
    ax.grid(color=LIGHT, linewidth=0.8, which="both")
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "df_audit.pdf")
    plt.close(fig)


if __name__ == "__main__":
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    _style()
    method_overview()
    evidence_summary()
    degrees_of_freedom_audit()
