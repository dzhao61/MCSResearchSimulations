"""Generate thesis figures from the accepted supervisor-practical results."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "WelchSatterthwaiteMI" / "results" / "supervisor_practical"
OUTPUT = Path(__file__).resolve().parent

METHOD_COLORS = {
    "normal_wald": "#2f6f91",
    "simple_welch": "#d97724",
    "expanded_welch": "#2e8067",
}
REGIME_COLORS = {
    "Well sampled": "#3d6f8e",
    "Moderate": "#d69a2d",
    "Highly skewed and sparse": "#2f8a68",
    "Ultra-skewed and sparse": "#b85c4b",
    "Widespread sparsity": "#765a94",
}


def configure() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.6,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUTPUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUTPUT / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


def scenario_calibration() -> None:
    data = pd.read_csv(RESULTS / "scenario_results.csv")
    values = data.pivot(
        index=["scenario_id", "regime_label"],
        columns="method",
        values="absolute_fpr_error_05",
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.55), sharex=True, sharey=True)
    comparisons = [
        ("simple_welch", "Simple Welch"),
        ("expanded_welch", "Expanded Welch"),
    ]
    limit = 1.08 * values[["normal_wald", "simple_welch", "expanded_welch"]].max().max()

    for axis, (method, label) in zip(axes, comparisons, strict=True):
        for regime, group in values.groupby("regime_label", sort=False):
            axis.scatter(
                group["normal_wald"],
                group[method],
                s=28,
                alpha=0.82,
                color=REGIME_COLORS[regime],
                edgecolor="white",
                linewidth=0.35,
                label=regime,
            )
        axis.plot([0, limit], [0, limit], color="#555555", linestyle="--", linewidth=1)
        improved = int((values[method] < values["normal_wald"]).sum())
        tied = int(np.isclose(values[method], values["normal_wald"]).sum())
        axis.set_title(f"{label}: improved in {improved}/60 scenarios")
        axis.set_xlabel("Normal Wald absolute FPR error")
        axis.set_xlim(0, limit)
        axis.set_ylim(0, limit)
        axis.set_aspect("equal", adjustable="box")
        if tied:
            axis.text(0.98, 0.04, f"ties: {tied}", transform=axis.transAxes, ha="right")

    axes[0].set_ylabel("Comparator absolute FPR error")
    handles, labels = axes[1].get_legend_handles_labels()
    fig.suptitle("Scenario-level calibration at nominal $\\alpha=0.05$", y=0.99, fontsize=12)
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.93),
        ncol=3,
        frameon=False,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.82))
    save(fig, "scenario_calibration_comparison")


def degrees_of_freedom() -> None:
    data = pd.read_csv(RESULTS / "scenario_results.csv")
    values = data.pivot(
        index=["scenario_id", "regime_label"],
        columns="method",
        values="median_effective_df",
    ).reset_index()

    fig, axis = plt.subplots(figsize=(5.25, 4.25))
    for regime, group in values.groupby("regime_label", sort=False):
        axis.scatter(
            group["simple_welch"],
            group["expanded_welch"],
            s=31,
            alpha=0.82,
            color=REGIME_COLORS[regime],
            edgecolor="white",
            linewidth=0.35,
            label=regime,
        )
    finite = values[["simple_welch", "expanded_welch"]].to_numpy()
    lower = np.nanmin(finite) * 0.8
    upper = np.nanmax(finite) * 1.25
    axis.plot([lower, upper], [lower, upper], color="#555555", linestyle="--", linewidth=1)
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlim(lower, upper)
    axis.set_ylim(lower, upper)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("Simple Welch median effective df")
    axis.set_ylabel("Expanded Welch median effective df")
    axis.set_title("MI-specific degrees of freedom are usually smaller")
    axis.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    save(fig, "effective_df_comparison")


def power_comparison() -> None:
    data = pd.read_csv(RESULTS / "power_summary.csv")
    order = [
        "curve_effect_d02_n300",
        "curve_sample_d05_n150",
        "curve_effect_d05_n300",
        "curve_sample_d05_n600",
        "curve_effect_d10_n300",
    ]
    labels = [
        "$|\\Delta|=.02$\n$n=300$",
        "$|\\Delta|=.05$\n$n=150$",
        "$|\\Delta|=.05$\n$n=300$",
        "$|\\Delta|=.05$\n$n=600$",
        "$|\\Delta|=.10$\n$n=300$",
    ]
    methods = ["normal_wald", "simple_welch", "expanded_welch"]
    method_labels = ["Normal Wald", "Simple Welch", "Expanded Welch"]
    pivot = data.pivot(index="scenario_id", columns="method", values="power_05").loc[order]

    x = np.arange(len(order))
    width = 0.23
    fig, axis = plt.subplots(figsize=(7.25, 3.7))
    for offset, method, label in zip((-1, 0, 1), methods, method_labels, strict=True):
        axis.bar(
            x + offset * width,
            pivot[method],
            width,
            color=METHOD_COLORS[method],
            label=label,
        )
    axis.set_xticks(x, labels)
    axis.set_ylim(0, 0.82)
    axis.set_ylabel("Rejection probability at $\\alpha=0.05$")
    axis.set_title("Power across effect sizes and sample sizes")
    axis.legend(frameon=False, ncol=3, loc="upper left")
    fig.tight_layout()
    save(fig, "power_comparison")


def main() -> None:
    configure()
    scenario_calibration()
    degrees_of_freedom()
    power_comparison()


if __name__ == "__main__":
    main()
