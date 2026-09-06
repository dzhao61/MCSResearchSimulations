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
DEFAULT_DOCUMENT = PROJECT_ROOT / "docs" / "experiments" / "FINAL_EXPERIMENT_LANDSCAPE.md"
METHODS = ("normal_wald", "expanded_welch")
LABELS = {"normal_wald": "Normal Wald", "expanded_welch": "Expanded Welch"}
COLORS = {"normal_wald": "#1f4e79", "expanded_welch": "#b23a73"}
MARKERS = {"normal_wald": "o", "expanded_welch": "s"}
SHAPES = ("2x2", "2x3", "3x3", "3x5", "4x4", "4x8", "5x5", "8x8")
SKEWNESS = ("balanced", "mild", "strong", "ultra")
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
                axis.set_xlabel("Scaled MI difference e (absolute difference = eM)", fontsize=8)

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
        ("identical_distribution", "P and Q have the same distribution shape"),
        ("equal_mi_different_shape", "P and Q have different distribution shapes"),
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
        "checkerboard_and_cyclic": "alternating/repeating",
        "fixed_random_A_and_fixed_random_B": "fixed irregular",
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
            f"{shape} rejection curves for other arrangements of dependence",
            output_dir / f"interaction_{shape}.png",
        )


def _format_number_set(values: pd.Series) -> str:
    unique = sorted(values.dropna().unique())
    return r"$\{" + ", ".join(f"{value:g}" for value in unique) + r"\}$"


def _mi_details(frame: pd.DataFrame, row_definitions: list[tuple[str, dict[str, object]]]) -> str:
    details = []
    for label, filters in row_definitions:
        row = frame
        for column, value in filters.items():
            row = row[row[column].eq(value)]
        if row.empty:
            raise ValueError(f"No MI specification data for {label}: {filters}")
        mi_p = row["achieved_mi_p"].iloc[0]
        scales = row["shared_reachable_mi"].dropna().unique()
        if len(scales) != 1:
            raise ValueError(f"Expected one MI scale for {label}, got {scales}")
        details.append(
            f"{label}: $M\approx{scales[0]:.4g}$, $I(P)\approx{mi_p:.4g}$, "
            f"$e$ values {_format_number_set(row['relative_effect'])}"
        )
    return "<br>".join(details)


def _specification_table(
    shape: str,
    population_construction: str,
    horizontal_regimes: str,
    vertical_regimes: str,
    resulting_sample_sizes: str,
    mi_details: str,
) -> list[str]:
    table_shape = shape.replace("x", r"\times")
    return [
        "| Figure specification | Exact setting |",
        "| --- | --- |",
        f"| Table shape | ${table_shape}$ |",
        f"| Population construction | {population_construction} |",
        f"| Horizontal graph regime specifications (columns) | {horizontal_regimes} |",
        f"| Vertical graph regime specifications (rows) | {vertical_regimes} |",
        f"| Resulting sample sizes | {resulting_sample_sizes} |",
        f"| MI settings by vertical regime | {mi_details} |",
        "| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to "
        r"0.60; the corresponding absolute difference is $eM$ nats |",
        "| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; "
        "an invalid result counts as a non-rejection |",
        "| Methods | {Normal Wald, Expanded Welch} |",
        r"| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |",
        "| Reference line | Rejection rate 0.05 |",
        "| Validity notation | Filled marker: valid rate at least 0.90; "
        "hollow marker: valid rate below 0.90 |",
        "| Replicates | 10,000 independently simulated table pairs per plotted point |",
    ]


def _write_document(results: pd.DataFrame, document: Path) -> None:
    primary = results[
        results["method"].eq("normal_wald")
        & np.isclose(results["nominal_alpha"], 0.05)
    ]
    lines = [
        "# Final Experiment Landscape: Normal Wald versus Expanded Welch",
        "",
        "## 1. Purpose",
        "",
        "This document presents the complete primary comparison of Normal Wald and",
        "Expanded Welch. Every panel represents one fixed experimental regime. No",
        "result is averaged across table shape, skewness, sample size, population",
        "construction, MI difference, sample-size ratio, or arrangement of dependence.",
        "",
        "The test is",
        "",
        "$$",
        "H_0:I(P)=I(Q)",
        r"\qquad\text{against}\qquad",
        "H_1:I(P)\\ne I(Q).",
        "$$",
        "",
        "## 2. How to read the figures",
        "",
        "The blue circular line is Normal Wald and the magenta square line is Expanded",
        "Welch. The horizontal axis is the scaled MI difference $e$. The zero-difference",
        "point gives the false-positive rate; positive differences give power. The dotted",
        "horizontal line marks the target rejection rate of 0.05 under the null.",
        "",
        "Every figure uses the same horizontal range of 0 to 0.60 and the same vertical",
        "range of 0 to 1. A filled marker means that at least 90% of replicates returned",
        "a valid statistic and $p$-value. A hollow marker means that the valid rate was",
        "below 90%.",
        "",
        "## 3. Population definitions",
        "",
        "A table's shape is its number of rows and columns. Skewness controls its",
        "margins: balanced margins are uniform, while mild, strong, and ultra margins",
        "have dominant probabilities 0.70, 0.90, and 0.95, respectively. There is no",
        "minimum expected-count requirement and no lower sample-size floor beyond the",
        "sample sizes stated in each subsection.",
        "",
        "The primary dependence arrangement places higher probability near matching",
        "ordered categories. The additional dependence experiments use the two",
        "arrangements defined explicitly in each subsection table. All observed tables",
        "are independent multinomial samples from fixed population tables $P$ and $Q$.",
        "",
        "$M$ is the smaller of the maximum MI values attainable by the fixed $P$ and",
        "$Q$ constructions. Every regime sets $I(P)=0.2M$ and",
        "$I(Q)=(0.2+e)M$. Therefore, the absolute MI difference is",
        r"$\lvert I(Q)-I(P)\rvert=eM$ nats. Scaling by $M$ places regimes with",
        "different attainable MI ranges on the same horizontal axis.",
        "",
        "## 4. Calibration and power across regimes",
        "",
        "Each figure combines calibration and power. Reading a curve from left to right",
        "shows the method's false-positive rate at zero difference and how often it",
        "detects progressively larger MI differences.",
        "",
        "### 4.1 Equal sample sizes and the primary dependence arrangement",
        "",
    ]

    power_rows = [
        ("balanced", {"skewness": "balanced"}),
        ("mild", {"skewness": "mild"}),
        ("strong", {"skewness": "strong"}),
        ("ultra", {"skewness": "ultra"}),
    ]
    relationships = (
        (
            "identical_distribution",
            "same distribution shape",
            "Same distribution shape: $P$ and $Q$ use the same margins and dependence "
            "arrangement; $I(Q)$ is increased according to the listed scaled MI settings",
        ),
        (
            "equal_mi_different_shape",
            "different distribution shapes",
            "Different distribution shapes: the largest row and column probabilities "
            "are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is "
            "increased according to the listed scaled MI settings",
        ),
    )
    subsection = 1
    for shape in SHAPES:
        for relationship, label, construction in relationships:
            frame = primary[
                primary["shape"].eq(shape)
                & primary["relationship"].eq(relationship)
                & primary["n_p"].eq(5)
                & primary["experiment"].isin(("calibration", "power"))
            ]
            stem = (
                "identical_distribution"
                if relationship == "identical_distribution"
                else "equal_mi_different_shape"
            )
            lines.extend(
                [
                    f"#### 4.1.{subsection} Shape {shape}: {label}",
                    "",
                    f"![{shape} rejection curves for {label}]"
                    f"(figures/final_experiment_landscape/power_{shape}_{stem}.png)",
                    "",
                    *_specification_table(
                        shape,
                        construction,
                        r"$\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$",
                        "{balanced (uniform margins), mild (dominant marginal probability "
                        "0.70), strong (0.90), ultra (0.95)}",
                        r"$\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), "
                        r"(100,100), (250,250), (500,500), (1000,1000)\}$",
                        _mi_details(frame, power_rows),
                    ),
                    "",
                ]
            )
            subsection += 1

    lines.extend(["### 4.2 Unequal sample sizes", ""])
    imbalance_rows = [
        (f"{skew}, $n_Q:n_P={ratio}:1$", {"skewness": skew, "sample_size_ratio_q_to_p": float(ratio)})
        for skew in ("strong", "ultra")
        for ratio in IMBALANCE_RATIOS
    ]
    for subsection, shape in enumerate(("2x2", "3x3", "5x5", "8x8"), start=1):
        frame = primary[
            primary["experiment"].eq("robustness_imbalance")
            & primary["shape"].eq(shape)
            & primary["n_p"].eq(5)
        ]
        lines.extend(
            [
                f"#### 4.2.{subsection} Shape {shape}",
                "",
                f"![{shape} rejection curves under unequal sample sizes]"
                f"(figures/final_experiment_landscape/imbalance_{shape}.png)",
                "",
                *_specification_table(
                    shape,
                    "Different distribution shapes: the largest row and column "
                    "probabilities are moved in $Q$, and its dependence arrangement is "
                    "reversed; $I(Q)$ is increased according to the listed scaled MI settings",
                    r"$\{n_P=5, 10, 20, 50, 100\}$",
                    r"$\{\text{strong}, n_Q:n_P=2:1;\ \text{strong}, 5:1;\ "
                    r"\text{strong}, 10:1;\ \text{ultra}, 2:1;\ \text{ultra}, 5:1;\ "
                    r"\text{ultra}, 10:1\}$",
                    "ratio 2:1: $\\{(5,10),(10,20),(20,40),(50,100),(100,200)\\}$; "
                    "ratio 5:1: $\\{(5,25),(10,50),(20,100),(50,250),(100,500)\\}$; "
                    "ratio 10:1: $\\{(5,50),(10,100),(20,200),(50,500),(100,1000)\\}$, "
                    "where each pair is $(n_P,n_Q)$",
                    _mi_details(frame, imbalance_rows),
                ),
                "",
            ]
        )

    lines.extend(["### 4.3 Other arrangements of dependence", ""])
    pair_labels = {
        "checkerboard_and_cyclic": "alternating/repeating",
        "fixed_random_A_and_fixed_random_B": "fixed irregular",
    }
    interaction_rows = [
        (
            f"{skew}, {pair_labels[pair]}",
            {"skewness": skew, "interaction_pair": pair},
        )
        for skew in ("balanced", "strong", "ultra")
        for pair in INTERACTION_PAIRS
    ]
    vertical_interactions = (
        "{balanced, alternating/repeating; balanced, fixed irregular; strong, "
        "alternating/repeating; strong, fixed irregular; ultra, "
        "alternating/repeating; ultra, fixed irregular}"
    )
    for subsection, shape in enumerate(("3x3", "3x5", "5x5", "8x8"), start=1):
        frame = primary[
            primary["experiment"].eq("robustness_interaction")
            & primary["shape"].eq(shape)
            & primary["n_p"].eq(5)
        ]
        lines.extend(
            [
                f"#### 4.3.{subsection} Shape {shape}",
                "",
                f"![{shape} rejection curves for other arrangements of dependence]"
                f"(figures/final_experiment_landscape/interaction_{shape}.png)",
                "",
                *_specification_table(
                    shape,
                    "Different distribution shapes. Alternating/repeating compares an "
                    "alternating high-low arrangement in $P$ with a repeating "
                    "shifted-diagonal arrangement in $Q$. Fixed irregular compares two "
                    "irregular arrangements generated once from fixed seeds and then held constant.",
                    r"$\{n_P=n_Q=5, 10, 20, 50, 100, 250\}$",
                    vertical_interactions,
                    r"$\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), "
                    r"(100,100), (250,250)\}$",
                    _mi_details(frame, interaction_rows),
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## 5. Briefing sequence",
            "",
            "1. Read the zero-difference point to assess false-positive control.",
            "2. Check whether the marker is hollow before interpreting a low rejection rate.",
            "3. Follow both curves to the right to compare power at the same scaled MI",
            "   differences $e$.",
            "4. Compare panels horizontally to change sample size while holding the row",
            "   regime fixed.",
            "5. Compare panels vertically to change skewness, imbalance, or dependence",
            "   arrangement while holding the column regime fixed.",
            "",
            "## 6. Reproducibility",
            "",
            "The figures and this document are generated by",
            "[`../../experiments/make_final_experiment_landscape.py`]"
            "(../../experiments/make_final_experiment_landscape.py)",
            "from",
            "[`../../results/detection_breakdown_sweep/cell_results.csv`]"
            "(../../results/detection_breakdown_sweep/cell_results.csv).",
            "The generator verifies the frozen configuration counts and rejects duplicate",
            "or incomplete curves rather than averaging them.",
        ]
    )
    document.parent.mkdir(parents=True, exist_ok=True)
    document.write_text("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--document", type=Path, default=DEFAULT_DOCUMENT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = pd.read_csv(args.results_dir / "cell_results.csv")
    _validate_source(results)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _power_curve_landscapes(results, args.output_dir)
    _imbalance_curve_landscapes(results, args.output_dir)
    _interaction_curve_landscapes(results, args.output_dir)
    _write_document(results, args.document)
    print(f"Wrote 24 exact-regime landscape figures to {args.output_dir}")
    print(f"Wrote the landscape document to {args.document}")


if __name__ == "__main__":
    main()
