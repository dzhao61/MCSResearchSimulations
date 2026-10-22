#!/usr/bin/env python3
"""Create exact-configuration presentation figures for the 2x2 experiment."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


METHODS = ("normal_wald", "simple_welch", "expanded_welch")
COLORS = {
    "normal_wald": "#22577a",
    "simple_welch": "#d97706",
    "expanded_welch": "#A23B72",
}
LABELS = {
    "normal_wald": "Normal Wald",
    "simple_welch": "Simple Welch",
    "expanded_welch": "Expanded Welch",
}
NULL_LABELS = {
    "C1_N0_n10": "Identical balanced, 10:10",
    "C1_N0_n50": "Identical balanced, 50:50",
    "C1_N0_n1000": "Identical balanced, 1000:1000",
    "C1_N3_n50": "One skewed population, 50:50",
    "C1_N6_n100": "Sparse/opposite association, 100:100",
    "C1_N6_n200": "Sparse/opposite association, 200:200",
    "C1_N7_n1000": "Ultra-rare categories, 1000:1000",
    "C2_N0_np20_nq200": "Identical balanced, 20:200",
    "C2_N3_np500_nq50": "One skewed population, 500:50",
    "C2_N5_np200_nq2000": "Extreme rare categories, 200:2000",
    "C3_C3_same_balanced_i0p005_n1000": "Near independence, MI=.005, 1000:1000",
    "C4_C4_s0p1_i0p0001_n100": "Rare-cell ladder, s=.1, MI=.0001, 100:100",
    "C4_C4_s0p05_i0p0001_n500": "Rare-cell ladder, s=.05, MI=.0001, 500:500",
}
POWER_LABELS = {
    f"PM_{configuration_id}_di0p005": label
    for configuration_id, label in NULL_LABELS.items()
}

def plot_null(input_dir: Path, output_dir: Path) -> None:
    frame = pd.read_csv(input_dir / "null_summary.csv")
    order = [configuration_id for configuration_id in NULL_LABELS if configuration_id in set(frame["configuration_id"])]
    positions = np.arange(len(order), dtype=float)
    offsets = dict(zip(METHODS, (-0.20, 0.0, 0.20), strict=True))

    figure, (calibration_axis, validity_axis) = plt.subplots(
        1,
        2,
        figsize=(14, 8),
        sharey=True,
        gridspec_kw={"width_ratios": [1.2, 1.0]},
    )
    for method in METHODS:
        selected = (
            frame[frame["method"].eq(method)]
            .set_index("configuration_id")
            .loc[order]
        )
        y = positions + offsets[method]
        rate = selected["false_positive_rate_05"].to_numpy()
        low = selected["fpr_wilson_low_05"].to_numpy()
        high = selected["fpr_wilson_high_05"].to_numpy()
        calibration_axis.errorbar(
            rate,
            y,
            xerr=np.vstack((rate - low, high - rate)),
            fmt="o",
            markersize=5,
            capsize=2,
            color=COLORS[method],
            label=LABELS[method],
        )
        validity_axis.scatter(
            selected["valid_rate"],
            y,
            s=28,
            color=COLORS[method],
        )

    calibration_axis.axvline(0.05, color="#333333", linestyle=":", linewidth=1.5)
    calibration_axis.set_xlabel("False-positive rate at nominal alpha = 0.05")
    calibration_axis.set_ylabel("Configuration")
    calibration_axis.legend(frameon=False, loc="lower right")
    calibration_axis.grid(axis="x", alpha=0.2)

    validity_axis.axvline(1.0, color="#333333", linestyle=":", linewidth=1.5)
    validity_axis.set_xlabel("Valid-result rate")
    validity_axis.set_xlim(-0.02, 1.03)
    validity_axis.grid(axis="x", alpha=0.2)

    calibration_axis.set_yticks(positions)
    calibration_axis.set_yticklabels([NULL_LABELS[value] for value in order])
    calibration_axis.invert_yaxis()
    figure.suptitle("2x2 confirmatory null results (50,000 replicates per row)")
    figure.tight_layout()
    figure.savefig(output_dir / "CONFIRM_null_calibration_and_validity.png", dpi=180)
    plt.close(figure)


def plot_power(input_dir: Path, output_dir: Path) -> None:
    frame = pd.read_csv(input_dir / "power_summary.csv")
    order = [configuration_id for configuration_id in POWER_LABELS if configuration_id in set(frame["configuration_id"])]
    positions = np.arange(len(order), dtype=float)
    offsets = dict(zip(METHODS, (-0.20, 0.0, 0.20), strict=True))
    figure, power_axis = plt.subplots(figsize=(10.5, 7.2))
    for method in METHODS:
        selected = (
            frame[frame["method"].eq(method)]
            .set_index("configuration_id")
            .loc[order]
        )
        y = positions + offsets[method]
        rate = selected["true_positive_rate_05"].to_numpy()
        low = selected["rejection_wilson_low_05"].to_numpy()
        high = selected["rejection_wilson_high_05"].to_numpy()
        power_axis.errorbar(
            rate,
            y,
            xerr=np.vstack((rate - low, high - rate)),
            fmt="o",
            markersize=5,
            capsize=2,
            color=COLORS[method],
            label=LABELS[method],
        )

    power_axis.set_xlabel("Detection power at p <= 0.05")
    power_axis.set_ylabel("Configuration")
    power_axis.grid(axis="x", alpha=0.2)
    power_axis.legend(frameon=False, loc="lower right")
    power_axis.set_yticks(positions)
    power_axis.set_yticklabels([POWER_LABELS[value] for value in order])
    power_axis.invert_yaxis()
    figure.suptitle("2x2 detection power (50,000 replicates per configuration)")
    figure.tight_layout()
    figure.savefig(output_dir / "CONFIRM_detection_power.png", dpi=180)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir or args.input_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_null(args.input_dir, output_dir)
    plot_power(args.input_dir, output_dir)


if __name__ == "__main__":
    main()
