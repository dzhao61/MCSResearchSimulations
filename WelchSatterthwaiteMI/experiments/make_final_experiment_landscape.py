#!/usr/bin/env python3
"""Create the exact-cell Wald-versus-Expanded-Welch landscape atlas."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = PROJECT_ROOT / "results" / "detection_breakdown_sweep"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "docs" / "experiments" / "figures" / "final_experiment_landscape"
)
METHODS = ("normal_wald", "expanded_welch")
LABELS = {"normal_wald": "Normal Wald", "expanded_welch": "Expanded Welch"}
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


def _matrix(
    frame: pd.DataFrame,
    method: str,
    row_order: list[str],
    column: str,
    column_order: tuple[float | int, ...],
    value: str,
) -> np.ndarray:
    subset = frame[frame["method"].eq(method)]
    duplicate = subset.duplicated(["landscape_row", column], keep=False)
    if duplicate.any():
        examples = subset.loc[duplicate, ["landscape_row", column]].head().to_dict("records")
        raise ValueError(f"Duplicate landscape cells: {examples}")
    pivot = subset.pivot(index="landscape_row", columns=column, values=value)
    pivot = pivot.reindex(index=row_order, columns=column_order)
    if pivot.isna().any().any():
        missing = int(pivot.isna().sum().sum())
        raise ValueError(f"Landscape is missing {missing} values for {method}/{value}")
    return pivot.to_numpy(dtype=float)


def _heatmap(
    figure: plt.Figure,
    axis: plt.Axes,
    values: np.ndarray,
    title: str,
    row_labels: list[str],
    column_labels: list[str],
    *,
    cmap: str,
    norm: mcolors.Normalize,
    colorbar_label: str,
    show_rows: bool,
) -> None:
    image = axis.imshow(values, aspect="auto", interpolation="nearest", cmap=cmap, norm=norm)
    axis.set_title(title, fontsize=11, weight="bold")
    axis.set_xticks(np.arange(len(column_labels)), column_labels, rotation=45, ha="right")
    axis.set_yticks(np.arange(len(row_labels)))
    axis.set_yticklabels(row_labels if show_rows else [])
    axis.tick_params(axis="both", labelsize=7, length=0)
    axis.set_xticks(np.arange(-0.5, len(column_labels), 1), minor=True)
    axis.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
    axis.grid(which="minor", color="white", linewidth=0.25, alpha=0.45)
    axis.tick_params(which="minor", bottom=False, left=False)
    colorbar = figure.colorbar(image, ax=axis, fraction=0.046, pad=0.025, extend="both")
    colorbar.ax.tick_params(labelsize=7)
    colorbar.set_label(colorbar_label, fontsize=8)


def _landscape_figure(
    frame: pd.DataFrame,
    row_order: list[str],
    row_labels: list[str],
    column: str,
    column_order: tuple[float | int, ...],
    column_labels: list[str],
    title: str,
    output: Path,
    *,
    calibration: bool,
) -> None:
    rejection = {
        method: _matrix(
            frame,
            method,
            row_order,
            column,
            column_order,
            "unconditional_rejection_rate",
        )
        for method in METHODS
    }
    validity = {
        method: _matrix(frame, method, row_order, column, column_order, "valid_rate")
        for method in METHODS
    }
    difference = rejection["expanded_welch"] - rejection["normal_wald"]
    difference_limit = max(float(np.max(np.abs(difference))), 0.01)

    height = max(9.0, 3.4 + 0.27 * len(row_labels))
    figure = plt.figure(figsize=(18, height), layout="constrained")
    grid = figure.add_gridspec(2, 3, height_ratios=(1.0, 1.0))
    axes = np.array(
        [
            [figure.add_subplot(grid[0, index]) for index in range(3)],
            [figure.add_subplot(grid[1, index]) for index in range(3)],
        ]
    )

    if calibration:
        rejection_norm: mcolors.Normalize = mcolors.TwoSlopeNorm(
            vmin=0.0, vcenter=0.05, vmax=0.25
        )
        rejection_label = "False-positive rate (values above 0.25 saturate)"
        rejection_cmap = "RdYlBu_r"
    else:
        rejection_norm = mcolors.Normalize(vmin=0.0, vmax=1.0)
        rejection_label = "Rejection rate"
        rejection_cmap = "viridis"

    _heatmap(
        figure,
        axes[0, 0],
        rejection["normal_wald"],
        "Normal Wald: rejection",
        row_labels,
        column_labels,
        cmap=rejection_cmap,
        norm=rejection_norm,
        colorbar_label=rejection_label,
        show_rows=True,
    )
    _heatmap(
        figure,
        axes[0, 1],
        rejection["expanded_welch"],
        "Expanded Welch: rejection",
        row_labels,
        column_labels,
        cmap=rejection_cmap,
        norm=rejection_norm,
        colorbar_label=rejection_label,
        show_rows=False,
    )
    _heatmap(
        figure,
        axes[0, 2],
        difference,
        "Expanded minus Wald rejection",
        row_labels,
        column_labels,
        cmap="coolwarm",
        norm=mcolors.TwoSlopeNorm(
            vmin=-difference_limit, vcenter=0.0, vmax=difference_limit
        ),
        colorbar_label="Difference in rejection rate",
        show_rows=False,
    )
    for index, method in enumerate(METHODS):
        _heatmap(
            figure,
            axes[1, index],
            validity[method],
            f"{LABELS[method]}: validity",
            row_labels,
            column_labels,
            cmap="cividis",
            norm=mcolors.Normalize(vmin=0.0, vmax=1.0),
            colorbar_label="Valid-result rate",
            show_rows=index == 0,
        )
    axes[1, 2].axis("off")
    axes[1, 2].text(
        0.05,
        0.92,
        "Reading key",
        transform=axes[1, 2].transAxes,
        fontsize=12,
        weight="bold",
        va="top",
    )
    note = (
        "Each heatmap cell is one exact configuration.\n\n"
        "Top row: unconditional rejection rates; invalid\n"
        "outputs count as non-rejections.\n\n"
        "Difference panel: red means Expanded Welch\n"
        "rejects more; blue means it rejects less.\n\n"
        "Bottom row: probability of returning a finite\n"
        "statistic and p-value."
    )
    if calibration:
        note += "\n\nIn the rejection maps, 0.05 is the null target."
    axes[1, 2].text(
        0.05,
        0.80,
        note,
        transform=axes[1, 2].transAxes,
        fontsize=10,
        linespacing=1.4,
        va="top",
    )
    figure.suptitle(title, fontsize=16, weight="bold")
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def _calibration_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    relationships = (
        ("identical_distribution", "Identical-distribution null: P = Q"),
        ("equal_mi_different_shape", "Equal-MI, different-shape null: P differs from Q"),
    )
    row_order = [f"{shape}|{skew}" for shape in SHAPES for skew in SKEWNESS]
    row_labels = [f"{shape} | {skew}" for shape in SHAPES for skew in SKEWNESS]
    for relationship, label in relationships:
        frame = results[
            results["experiment"].eq("calibration")
            & results["relationship"].eq(relationship)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ].copy()
        frame["landscape_row"] = frame["shape"] + "|" + frame["skewness"]
        _landscape_figure(
            frame,
            row_order,
            row_labels,
            "n_p",
            CALIBRATION_N,
            [str(value) for value in CALIBRATION_N],
            f"Calibration landscape at alpha = 0.05\n{label}",
            output_dir / f"calibration_{relationship}.png",
            calibration=True,
        )


def _power_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    relationship_labels = {
        "identical_distribution": "same",
        "equal_mi_different_shape": "different",
    }
    for shape in SHAPES:
        positive = results[
            results["experiment"].eq("power")
            & results["shape"].eq(shape)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ].copy()
        null = results[
            results["experiment"].eq("calibration")
            & results["shape"].eq(shape)
            & results["n_p"].isin(POWER_N)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ].copy()
        frame = pd.concat([null, positive], ignore_index=True)
        frame["relationship_short"] = frame["relationship"].map(relationship_labels)
        frame["landscape_row"] = (
            frame["relationship_short"]
            + "|"
            + frame["skewness"]
            + "|"
            + frame["n_p"].astype(str)
        )
        row_order = [
            f"{relationship}|{skew}|{sample_size}"
            for relationship in ("same", "different")
            for skew in SKEWNESS
            for sample_size in POWER_N
        ]
        row_labels = [
            f"{relationship} | {skew} | n={sample_size}"
            for relationship in ("same", "different")
            for skew in SKEWNESS
            for sample_size in POWER_N
        ]
        _landscape_figure(
            frame,
            row_order,
            row_labels,
            "relative_effect",
            EFFECTS,
            [_label_effect(value) for value in EFFECTS],
            f"Power landscape at alpha = 0.05: {shape}",
            output_dir / f"power_{shape}.png",
            calibration=False,
        )


def _imbalance_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    for effect in IMBALANCE_EFFECTS:
        frame = results[
            results["experiment"].eq("robustness_imbalance")
            & np.isclose(results["relative_effect"], effect)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ].copy()
        frame["landscape_row"] = (
            frame["shape"]
            + "|"
            + frame["skewness"]
            + "|"
            + frame["sample_size_ratio_q_to_p"].astype(int).astype(str)
        )
        row_order = [
            f"{shape}|{skew}|{ratio}"
            for shape in ("2x2", "3x3", "5x5", "8x8")
            for skew in ("strong", "ultra")
            for ratio in IMBALANCE_RATIOS
        ]
        row_labels = [
            f"{shape} | {skew} | ratio={ratio}:1"
            for shape in ("2x2", "3x3", "5x5", "8x8")
            for skew in ("strong", "ultra")
            for ratio in IMBALANCE_RATIOS
        ]
        _landscape_figure(
            frame,
            row_order,
            row_labels,
            "n_p",
            (5, 10, 20, 50, 100),
            ["5", "10", "20", "50", "100"],
            f"Sample-imbalance landscape at alpha = 0.05: relative effect e = {_label_effect(effect)}",
            output_dir / f"imbalance_effect_{_label_effect(effect).replace('.', '_')}.png",
            calibration=np.isclose(effect, 0.0),
        )


def _interaction_landscapes(results: pd.DataFrame, output_dir: Path) -> None:
    pair_labels = {
        "checkerboard_and_cyclic": "checker/cyclic",
        "fixed_random_A_and_fixed_random_B": "fixed random",
    }
    for effect in INTERACTION_EFFECTS:
        frame = results[
            results["experiment"].eq("robustness_interaction")
            & np.isclose(results["relative_effect"], effect)
            & results["method"].isin(METHODS)
            & np.isclose(results["nominal_alpha"], 0.05)
        ].copy()
        frame["pair_short"] = frame["interaction_pair"].map(pair_labels)
        frame["landscape_row"] = (
            frame["shape"] + "|" + frame["skewness"] + "|" + frame["pair_short"]
        )
        row_order = [
            f"{shape}|{skew}|{pair_labels[pair]}"
            for shape in ("3x3", "3x5", "5x5", "8x8")
            for skew in ("balanced", "strong", "ultra")
            for pair in INTERACTION_PAIRS
        ]
        row_labels = [
            f"{shape} | {skew} | {pair_labels[pair]}"
            for shape in ("3x3", "3x5", "5x5", "8x8")
            for skew in ("balanced", "strong", "ultra")
            for pair in INTERACTION_PAIRS
        ]
        _landscape_figure(
            frame,
            row_order,
            row_labels,
            "n_p",
            (5, 10, 20, 50, 100, 250),
            ["5", "10", "20", "50", "100", "250"],
            f"Interaction-pattern landscape at alpha = 0.05: relative effect e = {_label_effect(effect)}",
            output_dir / f"interaction_effect_{_label_effect(effect).replace('.', '_')}.png",
            calibration=np.isclose(effect, 0.0),
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
    _power_landscapes(results, args.output_dir)
    _imbalance_landscapes(results, args.output_dir)
    _interaction_landscapes(results, args.output_dir)
    print(f"Wrote 17 exact-cell landscape figures to {args.output_dir}")


if __name__ == "__main__":
    main()
