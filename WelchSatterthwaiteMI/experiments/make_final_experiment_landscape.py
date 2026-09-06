#!/usr/bin/env python3
"""Create the exact-cell Wald-versus-Expanded-Welch landscape atlas."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = PROJECT_ROOT / "results" / "detection_breakdown_sweep"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "docs" / "experiments" / "figures" / "final_experiment_landscape"
)
METHODS = ("normal_wald", "expanded_welch")
LABELS = {"normal_wald": "Normal Wald", "expanded_welch": "Expanded Welch"}
COLORS = {"normal_wald": "#1f4e79", "expanded_welch": "#b23a73"}
MARKERS = {"normal_wald": "o", "expanded_welch": "s"}
SHAPES = ("2x2", "2x3", "3x3", "3x5", "4x4", "4x8", "5x5", "8x8")
SKEWNESS = ("balanced", "mild", "strong", "ultra")
CALIBRATION_N = (2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50, 75, 100, 150, 250, 500, 1000)
POWER_N = (5, 10, 20, 50, 100, 250, 500, 1000)
EFFECTS = (0.0, 0.01, 0.025, 0.05, 0.10, 0.20, 0.40, 0.60)
IMBALANCE_RATIOS = (2, 5, 10)
IMBALANCE_EFFECTS = (0.0, 0.10, 0.40)
INTERACTION_EFFECTS = (0.0, 0.10, 0.40, 0.60)
INTERACTION_PAIRS = (
    "checkerboard_and_cyclic",
    "fixed_random_A_and_fixed_random_B",
)
EXPECTED_PRIMARY_CELLS = {
    "calibration": 1152,
    "power": 3584,
    "robustness_imbalance": 360,
    "robustness_interaction": 576,
}


def _label_effect(value: float) -> str:
    return "0" if np.isclose(value, 0.0) else f"{value:g}"


def _validate_source(results: pd.DataFrame) -> None:
    primary = results[
        results["method"].eq("normal_wald")
        & np.isclose(results["nominal_alpha"], 0.05)
    ]
    actual = primary.groupby("experiment").size().to_dict()
    if actual != EXPECTED_PRIMARY_CELLS:
        raise ValueError(
            f"Frozen primary-cell counts changed: expected {EXPECTED_PRIMARY_CELLS}, got {actual}"
        )
    if set(primary["replicates"].unique()) != {10_000}:
        raise ValueError("The landscape expects 10,000 replicates in every primary cell")
    if primary["configuration_id"].nunique() != sum(EXPECTED_PRIMARY_CELLS.values()):
        raise ValueError("Primary configuration identifiers are not one-to-one")


def _calibration_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    relationships = (
        ("identical_distribution", "Identical-distribution null: P = Q"),
        ("equal_mi_different_shape", "Equal-MI, different-shape null: P differs from Q"),
    )
    for relationship, label in relationships:
        frame = results[
            results["experiment"].eq("calibration")
            & results["relationship"].eq(relationship)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ]
        figure, axes = plt.subplots(
            len(SKEWNESS),
            len(SHAPES),
            figsize=(3.0 * len(SHAPES), 2.35 * len(SKEWNESS)),
            sharex=True,
            sharey=True,
        )
        for row_index, skew in enumerate(SKEWNESS):
            for column_index, shape in enumerate(SHAPES):
                axis = axes[row_index, column_index]
                panel = frame[frame["skewness"].eq(skew) & frame["shape"].eq(shape)]
                for method in METHODS:
                    line = panel[panel["method"].eq(method)].sort_values("n_p")
                    if tuple(line["n_p"]) != CALIBRATION_N:
                        raise ValueError(f"Incomplete calibration curve for {relationship}/{shape}/{skew}/{method}")
                    axis.plot(
                        line["n_p"],
                        line["unconditional_rejection_rate"],
                        color=COLORS[method],
                        linewidth=1.6,
                    )
                    valid = line["valid_rate"].ge(0.90)
                    axis.scatter(
                        line.loc[valid, "n_p"],
                        line.loc[valid, "unconditional_rejection_rate"],
                        color=COLORS[method],
                        marker=MARKERS[method],
                        s=16,
                        linewidths=0.7,
                        zorder=3,
                    )
                    axis.scatter(
                        line.loc[~valid, "n_p"],
                        line.loc[~valid, "unconditional_rejection_rate"],
                        facecolors="white",
                        edgecolors=COLORS[method],
                        marker=MARKERS[method],
                        s=21,
                        linewidths=1.1,
                        zorder=3,
                    )
                axis.axhline(0.05, color="#666666", linestyle=":", linewidth=0.9)
                axis.set_xscale("log")
                axis.set_xlim(1.8, 1100)
                axis.set_ylim(-0.02, 1.02)
                axis.grid(color="#dddddd", linewidth=0.55, alpha=0.65)
                axis.tick_params(labelsize=7)
                if row_index == 0:
                    axis.set_title(shape, fontsize=9)
                if column_index == 0:
                    axis.set_ylabel(f"{skew}\nFalse-positive rate", fontsize=8)
                if row_index == len(SKEWNESS) - 1:
                    axis.set_xlabel("Equal sample size n", fontsize=8)

        legend = [
            Line2D(
                [0],
                [0],
                color=COLORS[method],
                marker=MARKERS[method],
                linewidth=1.8,
                markersize=5,
                label=LABELS[method],
            )
            for method in METHODS
        ]
        legend.append(
            Line2D(
                [0],
                [0],
                color="#555555",
                marker="o",
                markerfacecolor="white",
                linewidth=0,
                markersize=5,
                label="Hollow point: validity below 0.90",
            )
        )
        figure.legend(
            legend,
            [item.get_label() for item in legend],
            loc="upper center",
            bbox_to_anchor=(0.5, 0.965),
            ncol=3,
            frameon=False,
        )
        figure.suptitle(f"Calibration at alpha = 0.05\n{label}", fontsize=14, weight="bold", y=1.0)
        figure.tight_layout(rect=(0, 0, 1, 0.92))
        figure.savefig(
            output_dir / f"calibration_{relationship}.png",
            dpi=180,
            bbox_inches="tight",
        )
        plt.close(figure)


def _plot_rejection_curve(axis: plt.Axes, panel: pd.DataFrame, method: str) -> None:
    line = panel[panel["method"].eq(method)].sort_values("relative_effect")
    if tuple(line["relative_effect"].round(6)) != tuple(
        sorted(line["relative_effect"].round(6))
    ):
        raise ValueError("Relative effects are not ordered")
    axis.plot(
        line["relative_effect"],
        line["unconditional_rejection_rate"],
        color=COLORS[method],
        linewidth=1.6,
        zorder=2,
    )
    valid = line["valid_rate"].ge(0.90)
    axis.scatter(
        line.loc[valid, "relative_effect"],
        line.loc[valid, "unconditional_rejection_rate"],
        color=COLORS[method],
        marker=MARKERS[method],
        s=17,
        linewidths=0.7,
        zorder=3,
    )
    axis.scatter(
        line.loc[~valid, "relative_effect"],
        line.loc[~valid, "unconditional_rejection_rate"],
        facecolors="white",
        edgecolors=COLORS[method],
        marker=MARKERS[method],
        s=22,
        linewidths=1.1,
        zorder=3,
    )


def _curve_grid(
    frame: pd.DataFrame,
    row_values: list[tuple[object, ...]],
    row_columns: tuple[str, ...],
    row_labels: list[str],
    column_values: tuple[int, ...],
    column_name: str,
    column_heading: str,
    expected_effects: tuple[float, ...],
    title: str,
    output: Path,
) -> None:
    figure, axes = plt.subplots(
        len(row_values),
        len(column_values),
        figsize=(3.0 * len(column_values), 2.35 * len(row_values)),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for row_index, (row_value, row_label) in enumerate(zip(row_values, row_labels)):
        for column_index, column_value in enumerate(column_values):
            axis = axes[row_index, column_index]
            mask = frame[column_name].eq(column_value)
            for field, value in zip(row_columns, row_value):
                mask &= frame[field].eq(value)
            panel = frame[mask]
            for method in METHODS:
                method_panel = panel[panel["method"].eq(method)]
                actual_effects = tuple(method_panel["relative_effect"].sort_values().round(6))
                if actual_effects != tuple(np.round(expected_effects, 6)):
                    raise ValueError(
                        f"Incomplete curve for {row_value}, {column_name}={column_value}, "
                        f"{method}: {actual_effects}"
                    )
                _plot_rejection_curve(axis, panel, method)
            axis.axhline(0.05, color="#666666", linestyle=":", linewidth=0.9)
            axis.set_xlim(-0.015, 0.615)
            axis.set_ylim(-0.02, 1.02)
            axis.grid(color="#dddddd", linewidth=0.55, alpha=0.65)
            axis.tick_params(labelsize=7)
            if row_index == 0:
                axis.set_title(f"{column_heading} = {column_value}", fontsize=9)
            if column_index == 0:
                axis.set_ylabel(f"{row_label}\nRejection rate", fontsize=8)
            if row_index == len(row_values) - 1:
                axis.set_xlabel("Relative MI difference e (Delta MI = eM)", fontsize=8)

    legend = [
        Line2D(
            [0],
            [0],
            color=COLORS[method],
            marker=MARKERS[method],
            linewidth=1.8,
            markersize=5,
            label=LABELS[method],
        )
        for method in METHODS
    ]
    legend.append(
        Line2D(
            [0],
            [0],
            color="#555555",
            marker="o",
            markerfacecolor="white",
            linewidth=0,
            markersize=5,
            label="Hollow point: validity below 0.90",
        )
    )
    figure.legend(
        legend,
        [item.get_label() for item in legend],
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=3,
        frameon=False,
    )
    figure.suptitle(title, fontsize=14, weight="bold", y=1.0)
    figure.tight_layout(rect=(0, 0, 1, 0.92))
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def _power_curve_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    relationships = (
        ("identical_distribution", "Same population path"),
        ("equal_mi_different_shape", "Different population paths with equal baseline MI"),
    )
    for shape in SHAPES:
        for relationship, relationship_label in relationships:
            positive = results[
                results["experiment"].eq("power")
                & results["shape"].eq(shape)
                & results["relationship"].eq(relationship)
                & results["method"].isin(METHODS)
                & np.isclose(results["nominal_alpha"], 0.05)
            ]
            null = results[
                results["experiment"].eq("calibration")
                & results["shape"].eq(shape)
                & results["relationship"].eq(relationship)
                & results["n_p"].isin(POWER_N)
                & results["method"].isin(METHODS)
                & np.isclose(results["nominal_alpha"], 0.05)
            ]
            frame = pd.concat([null, positive], ignore_index=True)
            _curve_grid(
                frame,
                [(skew,) for skew in SKEWNESS],
                ("skewness",),
                list(SKEWNESS),
                POWER_N,
                "n_p",
                "nP = nQ",
                EFFECTS,
                f"{shape} rejection curves\n{relationship_label}",
                output_dir / f"power_{shape}_{relationship}.png",
            )


def _imbalance_curve_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    for shape in ("2x2", "3x3", "5x5", "8x8"):
        frame = results[
            results["experiment"].eq("robustness_imbalance")
            & results["shape"].eq(shape)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ]
        row_values = [
            (skew, float(ratio))
            for skew in ("strong", "ultra")
            for ratio in IMBALANCE_RATIOS
        ]
        row_labels = [
            f"{skew}, nQ:nP={ratio}:1"
            for skew in ("strong", "ultra")
            for ratio in IMBALANCE_RATIOS
        ]
        _curve_grid(
            frame,
            row_values,
            ("skewness", "sample_size_ratio_q_to_p"),
            row_labels,
            (5, 10, 20, 50, 100),
            "n_p",
            "nP",
            IMBALANCE_EFFECTS,
            f"{shape} rejection curves under unequal sample sizes",
            output_dir / f"imbalance_{shape}.png",
        )


def _interaction_curve_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    pair_labels = {
        "checkerboard_and_cyclic": "checker/cyclic",
        "fixed_random_A_and_fixed_random_B": "fixed random",
    }
    for shape in ("3x3", "3x5", "5x5", "8x8"):
        frame = results[
            results["experiment"].eq("robustness_interaction")
            & results["shape"].eq(shape)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ]
        row_values = [
            (skew, pair)
            for skew in ("balanced", "strong", "ultra")
            for pair in INTERACTION_PAIRS
        ]
        row_labels = [
            f"{skew}, {pair_labels[pair]}"
            for skew in ("balanced", "strong", "ultra")
            for pair in INTERACTION_PAIRS
        ]
        _curve_grid(
            frame,
            row_values,
            ("skewness", "interaction_pair"),
            row_labels,
            (5, 10, 20, 50, 100, 250),
            "n_p",
            "nP = nQ",
            INTERACTION_EFFECTS,
            f"{shape} rejection curves under alternative interaction patterns",
            output_dir / f"interaction_{shape}.png",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = pd.read_csv(args.results_dir / "cell_results.csv")
    _validate_source(results)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _calibration_landscapes(results, args.output_dir)
    _power_curve_landscapes(results, args.output_dir)
    _imbalance_curve_landscapes(results, args.output_dir)
    _interaction_curve_landscapes(results, args.output_dir)
    print(f"Wrote 26 exact-regime landscape figures to {args.output_dir}")


if __name__ == "__main__":
    main()
