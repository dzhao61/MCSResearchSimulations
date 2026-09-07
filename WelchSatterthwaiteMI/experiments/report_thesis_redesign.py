#!/usr/bin/env python3
"""Generate standardized figures and the reader-facing thesis experiment report."""

from __future__ import annotations

import json
import hashlib
import math
import re
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from thesis_redesign_core import ROOT

METHODS = {
    "normal_wald": ("Normal Wald", "#1f4e79", "o", "-"),
    "expanded_welch": ("Expanded Welch", "#b23a73", "s", "--"),
}
SECTION_ORDER = [
    "main", "baseline", "patterns", "imbalance", "broad_effect",
    "rectangular", "construction", "extreme", "rare_stress",
    "independence", "convergence",
]
SECTION_TITLES = {
    "main": "Main comparison",
    "baseline": "Baseline MI sensitivity",
    "patterns": "Where the cell probabilities change",
    "imbalance": "Unequal sample sizes and MI direction",
    "broad_effect": "Larger MI differences",
    "rectangular": "Rectangular tables",
    "construction": "Alternative population construction",
    "extreme": "Extreme skew and very small samples",
    "rare_stress": "Rare-cell stress check",
    "independence": "Exact independence boundary",
    "convergence": "Large-sample null behaviour",
}
SECTION_QUESTIONS = {
    "main": "How do the methods behave as table size, marginal skew and sample size change?",
    "baseline": "Does performance change when the populations begin closer to independence?",
    "patterns": "Does performance change when dependence is placed in common, rare or many cells?",
    "imbalance": "Does performance depend on which population has more data or greater MI?",
    "broad_effect": "Do the power curves continue across larger actual MI differences?",
    "rectangular": "Do the square-table conclusions extend to rectangular tables?",
    "construction": "Do conclusions change under a matched ordinal log-linear construction?",
    "extreme": "What happens under deliberately extreme marginal skew and very small samples?",
    "rare_stress": "What happens when the probability changes are concentrated in rare cells?",
    "independence": "What happens at the nonregular boundary where baseline MI is exactly zero?",
    "convergence": "Do null rejection rates approach 0.05 as the fixed populations receive more data?",
}
SECTION_LIMITS = {
    "main": (0.0, 0.02), "baseline": (0.0, 0.02), "patterns": (0.0, 0.002),
    "imbalance": (0.0, 0.02), "broad_effect": (0.0, 0.2),
    "rectangular": (0.0, 0.02), "construction": (0.0, 0.02),
    "extreme": (0.0, 0.0002), "rare_stress": (0.0, 0.0001),
    "independence": (0.0, 0.02),
}


def format_number(value: Any, rate: bool = False) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "NA"
    if rate:
        return f"{float(value):.4f}"
    number = float(value)
    if number == 0:
        return "0"
    if abs(number) < 0.0001 or abs(number) >= 10000:
        return f"{number:.4g}"
    return f"{number:.4g}"


def markdown_table(columns: list[str], rows: list[list[Any]]) -> list[str]:
    return [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
        *["| " + " | ".join(str(value) for value in row) + " |" for row in rows],
    ]


def vector_text(payload: str) -> str:
    values = np.asarray(json.loads(payload), dtype=float)
    if np.allclose(values, values[0], rtol=0, atol=1e-14):
        return f"({format_number(values[0])} repeated {len(values)} times)"
    if len(values) > 2 and np.allclose(values[1:], values[1], rtol=0, atol=1e-14):
        remainder = 1.0 - values[0]
        return (
            f"({format_number(values[0])}, {format_number(remainder)}/{len(values)-1} "
            f"repeated {len(values)-1} times)"
        )
    return "(" + ", ".join(format_number(value) for value in values) + ")"


def ordered_unique(values: pd.Series) -> list[Any]:
    return list(dict.fromkeys(values.tolist()))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def human_figure_title(frame: pd.DataFrame, section: str, figure_key: str) -> str:
    shape = ordered_unique(frame["shape"])[0]
    profile = ordered_unique(frame["profile"])[0].replace("_", " ")
    if section == "main":
        return f"{shape}: {figure_key.rsplit('_', 1)[-1]} sample sizes"
    if section == "baseline":
        return f"{shape}: {profile} margins"
    if section == "patterns":
        return f"{shape}: locations of probability changes"
    if section == "imbalance":
        group = "1" if figure_key.endswith("_a") else "2"
        return f"{shape}: {profile} margins, sample allocations group {group}"
    if section == "broad_effect":
        return f"{shape}: {profile} margins, broad MI range"
    if section == "rectangular":
        return f"{shape}: {profile} margins"
    if section == "construction":
        baseline = format_number(frame["baseline_mi"].iloc[0])
        return f"{shape}: {profile} margins, baseline MI {baseline}"
    if section == "extreme":
        return f"{shape}: extreme margins, {figure_key.rsplit('_', 1)[-1]} sample sizes"
    if section == "rare_stress":
        return f"{shape}: common- and rare-cell changes, {figure_key.rsplit('_', 1)[-1]} sample sizes"
    if section == "independence":
        return f"{shape}: exact independence baseline"
    if section == "convergence" and "_rare_" in figure_key:
        return f"{shape}: rare-cell null convergence"
    return f"{shape}: null convergence"


def draw_figure(
    frame: pd.DataFrame,
    path: Path,
    section: str,
    title: str,
    y_limits: tuple[float, float] = (0.0, 1.0),
) -> None:
    row_keys = ordered_unique(frame["row_key"])
    column_keys = ordered_unique(frame["column_key"])
    figure, axes = plt.subplots(
        len(row_keys), len(column_keys),
        figsize=(4.1 * len(column_keys), 3.15 * len(row_keys)),
        sharex=True, sharey=True, squeeze=False,
    )
    for row_index, row_key in enumerate(row_keys):
        for column_index, column_key in enumerate(column_keys):
            axis = axes[row_index, column_index]
            panel = frame[frame["row_key"].eq(row_key) & frame["column_key"].eq(column_key)]
            x_column = "x_value"
            for method, (label, color, marker, linestyle) in METHODS.items():
                values = panel[panel["method"].eq(method)].sort_values(x_column)
                if values.empty:
                    continue
                axis.plot(
                    values[x_column], values["unconditional_rejection_rate"],
                    color=color, marker=marker, linestyle=linestyle, linewidth=1.6,
                    markersize=4, label=label, zorder=3,
                )
                axis.fill_between(
                    values[x_column], values["wilson_95_low"], values["wilson_95_high"],
                    color=color, alpha=0.10, zorder=1,
                )
                bad = values[values["valid_rate"] < 0.9]
                axis.scatter(
                    bad[x_column], bad["unconditional_rejection_rate"], marker=marker,
                    facecolors="white", edgecolors=color, s=28, zorder=4,
                )
                if len(values) and (values["valid_rate"] == 0).all():
                    axis.text(0.5, 0.85 if method == "normal_wald" else 0.72,
                              f"{label}: no valid results", transform=axis.transAxes,
                              ha="center", fontsize=7, color=color)
            axis.axhline(0.05, color="#777777", linestyle=":", linewidth=1)
            axis.set_ylim(*y_limits)
            if section == "convergence":
                axis.set_xscale("log")
                axis.set_xlim(1000, 50000)
                axis.set_xticks([1000, 2500, 10000, 50000])
                axis.get_xaxis().set_major_formatter(plt.ScalarFormatter())
                axis.set_xlabel("Sample size per population")
            else:
                axis.set_xlim(*SECTION_LIMITS[section])
                ticks = sorted(panel["x_value"].unique())
                axis.set_xticks(ticks)
                axis.set_xticklabels([format_number(value) for value in ticks], rotation=35, ha="right")
                axis.set_xlabel("Actual MI difference (nats)")
            axis.tick_params(axis="x", labelbottom=True)
            if row_index == 0:
                label = panel["column_label"].iloc[0] if not panel.empty else str(column_key)
                axis.set_title(label, fontsize=9)
            if column_index == 0:
                label = panel["row_label"].iloc[0] if not panel.empty else str(row_key)
                axis.set_ylabel(f"{label}\nRejection rate", fontsize=9)
            axis.grid(alpha=0.18)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.suptitle(title, y=0.995, fontsize=13)
    if handles:
        figure.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.968),
                      ncol=2, frameon=False)
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def specification_rows(frame: pd.DataFrame, populations: pd.DataFrame, section: str) -> list[list[str]]:
    row_specs = []
    for row_key in ordered_unique(frame["row_key"]):
        record = frame[frame["row_key"].eq(row_key)].iloc[0]
        population = populations[populations["pair_id"].eq(record["pair_id"])].iloc[0]
        row_specs.append(
            f"{record['row_label']}: P row {vector_text(population['row_margin_p_json'])}, "
            f"P column {vector_text(population['column_margin_p_json'])}; "
            f"Q row {vector_text(population['row_margin_q_json'])}, "
            f"Q column {vector_text(population['column_margin_q_json'])}"
        )
    changes = []
    for row_key in ordered_unique(frame["row_key"]):
        record = frame[frame["row_key"].eq(row_key)].iloc[0]
        if record["constructor"] == "loglinear":
            rule = "ordinal log-linear scores from -1 to 1, with row and column multipliers preserving the stated margins"
        elif record["pattern"] == "first":
            rule = "add at (1,1),(2,2) and subtract at (1,2),(2,1)"
        elif record["pattern"] == "rare":
            rule = "the same four signs in the last two rows and last two columns"
        else:
            rule = "spread changes H_ij=s_i s_j using equally spaced scores s from -1 to 1"
        changes.append(f"{record['row_label']}: {rule}, for both P and Q")
    baselines = ", ".join(format_number(value) for value in sorted(frame["baseline_mi"].unique()))
    differences = ", ".join(format_number(value) for value in sorted(frame["mi_difference"].unique()))
    directions = ", ".join(value.replace("_", " ") for value in ordered_unique(frame["mi_direction"]))
    columns = ", ".join(ordered_unique(frame["column_label"]))
    if section == "convergence":
        horizontal = "Equal sample size from 1,000 to 50,000 on a log scale; fixed listed ticks"
    else:
        low, high = SECTION_LIMITS[section]
        horizontal = f"Actual MI difference in nats, fixed from {format_number(low)} to {format_number(high)}"
    return [
        ["Table size", ", ".join(ordered_unique(frame["shape"]))],
        ["Horizontal graph regime specifications (columns)", columns],
        ["Vertical graph regime specifications (rows)", "; ".join(row_specs)],
        ["Probability changes", "; ".join(changes)],
        ["MI settings", f"Baseline MI {{{baselines}}}; direction {{{directions}}}; actual differences {{{differences}}} nats"],
        ["Horizontal axis within each graph", horizontal],
        ["Vertical axis within each graph", "Unconditional rejection rate from 0 to 1; invalid results count as non-rejections"],
        ["Replicates", f"{int(frame['replicates'].iloc[0]):,} per unique point"],
    ]


def ordered_frame(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    row_order = {value: index for index, value in enumerate(ordered_unique(frame["row_key"]))}
    column_order = {value: index for index, value in enumerate(ordered_unique(frame["column_key"]))}
    result["_row_order"] = result["row_key"].map(row_order)
    result["_column_order"] = result["column_key"].map(column_order)
    return result.sort_values(["_row_order", "_column_order", "x_value", "method"])


def null_rows(frame: pd.DataFrame) -> list[list[str]]:
    null = frame[np.isclose(frame["mi_difference"], 0)].copy()
    rows = []
    for record in ordered_frame(null).itertuples():
        rows.append([
            record.row_label, record.column_label, format_number(record.x_value), record.method_label,
            format_number(record.unconditional_rejection_rate, True),
            format_number(record.valid_rate, True),
        ])
    return rows


def detail_rows(frame: pd.DataFrame, section: str) -> list[list[str]]:
    rows = []
    ordered = ordered_frame(frame)
    for record in ordered.itertuples():
        x_value = int(record.x_value) if section == "convergence" else format_number(record.x_value)
        rows.append([
            record.row_label, record.column_label, str(x_value), record.method_label,
            format_number(record.unconditional_rejection_rate, True),
            f"[{format_number(record.wilson_95_low, True)}, {format_number(record.wilson_95_high, True)}]",
            format_number(record.valid_rate, True),
            format_number(record.conditional_rejection_rate, True),
            format_number(record.minimum_true_expected_p),
            format_number(record.minimum_true_expected_q),
        ])
    return rows


def worked_example(populations: pd.DataFrame) -> list[str]:
    frame = populations[
        populations["shape"].eq("2x2")
        & populations["profile"].eq("different_skew")
        & populations["constructor"].eq("additive")
        & populations["pattern"].eq("first")
        & np.isclose(populations["target_mi_p"], 0.02)
        & np.isclose(populations["target_mi_q"], 0.03)
    ]
    if frame.empty:
        return []
    row = frame.iloc[0]
    p, q = np.array(json.loads(row["probability_p_json"])), np.array(json.loads(row["probability_q_json"]))
    matrix = lambda values: "<br>".join("[" + ", ".join(format_number(value) for value in line) + "]" for line in values)
    return [
        "### A concrete population pair", "",
        "For a 2x2 different-skew example, the construction fixes the following populations before sampling:", "",
        *markdown_table(
            ["Population", "Joint probability table", "Row probabilities", "Column probabilities", "MI (nats)"],
            [
                ["P", matrix(p), vector_text(row["row_margin_p_json"]), vector_text(row["column_margin_p_json"]), format_number(row["achieved_mi_p"])],
                ["Q", matrix(q), vector_text(row["row_margin_q_json"]), vector_text(row["column_margin_q_json"]), format_number(row["achieved_mi_q"])],
            ],
        ), "",
        "Their true MI difference is 0.01 nats. Repeated multinomial samples make the estimated MI, variance and rejection decision random; they do not change this x-axis value.", "",
    ]


def runtime_section(output: Path, section_number: int) -> list[str]:
    path = output / "runtime_summary.csv"
    if not path.exists():
        return []
    frame = pd.read_csv(path)
    rows = []
    for record in frame.sort_values(["shape", "profile", "n_p", "mi_difference", "method"]).itertuples():
        rows.append([
            record.shape, record.profile.replace("_", " "), f"({record.n_p}, {record.n_q})",
            format_number(record.mi_difference), record.method.replace("_", " "),
            format_number(record.median_microseconds),
            f"[{format_number(record.q1_microseconds)}, {format_number(record.q3_microseconds)}]",
            format_number(record.expanded_to_wald_ratio), format_number(record.valid_rate, True),
        ])
    return [
        f"## {section_number}. Runtime", "",
        "Complete scalar test calls were timed on the same 200 saved input pairs per exact regime. Wald calls omit Expanded-Welch calculations; Expanded-Welch calls include the shared statistic plus its degrees-of-freedom calculation.", "",
        *markdown_table(
            ["Shape", "Margins", "(nP,nQ)", "MI difference", "Method", "Median us", "IQR us", "Expanded/Wald", "Valid"], rows
        ), "",
    ]


def overall_summary(
    display: pd.DataFrame,
    results: pd.DataFrame,
    output: Path,
    section_number: int,
) -> list[str]:
    merged = display.merge(results, on="configuration_id", suffixes=("", "_result"))
    main = merged[merged["section"].eq("main") & np.isclose(merged["mi_difference"], 0)]
    pivot = main.pivot(
        index=["configuration_id", "n_p"], columns="method",
        values="unconditional_rejection_rate",
    ).reset_index()
    pivot["wald_error"] = np.abs(pivot["normal_wald"] - 0.05)
    pivot["expanded_error"] = np.abs(pivot["expanded_welch"] - 0.05)
    small = pivot[pivot["n_p"].isin([5, 10, 20])]
    large = pivot[pivot["n_p"].isin([500, 1000])]
    expanded_small = int((small["expanded_error"] < small["wald_error"]).sum())
    wald_small = int((small["wald_error"] < small["expanded_error"]).sum())
    expanded_large = int((large["expanded_error"] < large["wald_error"]).sum())
    wald_large = int((large["wald_error"] < large["expanded_error"]).sum())
    power = merged[merged["section"].eq("main") & (merged["mi_difference"] > 0)]
    power_pivot = power.pivot(
        index="configuration_id", columns="method", values="unconditional_rejection_rate"
    )
    power_gap = power_pivot["normal_wald"] - power_pivot["expanded_welch"]
    convergence = merged[
        merged["section"].eq("convergence") & merged["n_p"].eq(50000)
    ]
    regular = convergence[np.isclose(convergence["baseline_mi"], 0.02)]
    near = convergence[np.isclose(convergence["baseline_mi"], 0.0001)]
    runtime = pd.read_csv(output / "runtime_summary.csv")
    ratios = runtime.drop_duplicates(
        ["shape", "profile", "n_p", "n_q", "mi_difference"]
    )["expanded_to_wald_ratio"]
    main_1000 = main[main["n_p"].eq(1000)]
    return [
        f"## {section_number}. Overall findings", "",
        "The complete regime-by-regime results support a conditional conclusion, not a universal ranking:", "",
        f"- Among the 36 main null regimes with n in {{5,10,20}}, Expanded Welch was closer to 0.05 in {expanded_small}, while Wald was closer in {wald_small}. The n=2 cases were ties only because neither method returned a valid result.",
        f"- Among the 24 main null regimes with n in {{500,1000}}, Wald was closer in {wald_large} and Expanded Welch in {expanded_large}. At n=1,000, Wald false-positive rates ranged from {main_1000[main_1000['method'].eq('normal_wald')]['unconditional_rejection_rate'].min():.4f} to {main_1000[main_1000['method'].eq('normal_wald')]['unconditional_rejection_rate'].max():.4f}; Expanded Welch ranged from {main_1000[main_1000['method'].eq('expanded_welch')]['unconditional_rejection_rate'].min():.4f} to {main_1000[main_1000['method'].eq('expanded_welch')]['unconditional_rejection_rate'].max():.4f}.",
        f"- On every common-valid input, Expanded Welch used the same statistic with a no-smaller p-value. Across nonzero main points its unconditional rejection rate was therefore never higher; the largest observed Wald-minus-Expanded difference was {power_gap.max():.4f}.",
        f"- At baseline MI 0.02 and n=50,000, both methods were close to nominal across all main null populations: Wald ranged from {regular[regular['method'].eq('normal_wald')]['unconditional_rejection_rate'].min():.4f} to {regular[regular['method'].eq('normal_wald')]['unconditional_rejection_rate'].max():.4f}, and Expanded Welch from {regular[regular['method'].eq('expanded_welch')]['unconditional_rejection_rate'].min():.4f} to {regular[regular['method'].eq('expanded_welch')]['unconditional_rejection_rate'].max():.4f}.",
        f"- Near independence, baseline MI 0.0001 remained conservative at n=50,000: Wald ranged from {near[near['method'].eq('normal_wald')]['unconditional_rejection_rate'].min():.4f} to {near[near['method'].eq('normal_wald')]['unconditional_rejection_rate'].max():.4f}, and Expanded Welch from {near[near['method'].eq('expanded_welch')]['unconditional_rejection_rate'].min():.4f} to {near[near['method'].eq('expanded_welch')]['unconditional_rejection_rate'].max():.4f}. This shows that sample size alone is not an adequate description of the approximation regime.",
        f"- Expanded Welch took {ratios.median():.2f} times the Wald runtime at the median across the 60 timed regimes (range {ratios.min():.2f} to {ratios.max():.2f}).", "",
        "Taken together, the study does not support Expanded Welch as a general replacement for Normal Wald. Its heavier-tailed reference can usefully reduce liberal rejection in some small-sample regimes, but it can also become unnecessarily conservative, fail more often, and lose power. The exact population construction still matters in larger tables, so conclusions should be attached to the stated regimes rather than presented as a universal rule.", "",
    ]


def build_report(protocol_path: Path, output: Path) -> Path:
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    required = ["display_manifest.csv", "population_definitions.csv", "cell_results.csv"]
    missing = [name for name in required if not (output / name).exists()]
    if missing:
        raise FileNotFoundError(f"Report inputs are missing: {missing}")
    display = pd.read_csv(output / "display_manifest.csv", keep_default_na=False)
    display["row_label"] = display["row_label"].replace(
        {"first": "first four-cell block", "rare": "last (rare) four-cell block"}
    )
    populations = pd.read_csv(output / "population_definitions.csv")
    results = pd.read_csv(output / "cell_results.csv")
    merged = display.merge(results, on="configuration_id", how="left", validate="many_to_many", suffixes=("", "_result"))
    if merged["method"].isna().any():
        raise RuntimeError("At least one displayed configuration has no result.")
    profile = json.loads((output / "preflight_summary.json").read_text())["profile"]
    full = profile == "full"
    figure_root = ROOT / "docs/experiments/figures/thesis_redesign" if full else output / "figures"
    image_prefix = "figures/thesis_redesign" if full else "figures"
    report_path = ROOT / "docs/experiments/THESIS_EXPERIMENTS.md" if full else output / "SMOKE_REPORT.md"

    lines = [
        "# Thesis Experiments: Normal Wald and Expanded Welch" if full else "# Thesis Redesign Smoke Report",
        "",
        ("This report compares Normal Wald and Expanded Welch for the two-sided test of equal population MI. "
         f"Every unique point uses {int(results['replicates'].iloc[0]):,} independently sampled table pairs at alpha=0.05. "
         "Both methods receive the same sampled tables, and no regimes are averaged together."), "",
        "## 1. How to read this document", "",
        "At an MI difference of zero, a curve reports the false-positive rate under H0; the target is 0.05. At a positive MI difference, it reports power under H1. Read calibration, power and validity together: liberal null rejection can inflate apparent power, while invalid outputs can make unconditional rejection appear artificially low.", "",
        "The x-axis is the true population MI difference fixed during construction, not a random difference estimated from the samples. The main and focused sections use separate stated ranges in nats so very small effects remain visible. A hollow marker means fewer than 90% of results were valid.", "",
        "'Minimum expected count' means the minimum population expected cell count, not the expected value of the smallest observed cell count.", "",
        "### Roadmap", "",
        "1. The main comparison maps table size, margins and sample size.",
        "2. Focused comparisons vary baseline MI, changed cells, sample imbalance, effect range, table shape and population construction.",
        "3. Limit checks examine extreme sparsity, exact independence and large-sample null behaviour.",
        "4. Runtime and reproducibility records follow the statistical results.", "",
        "## 2. How the fixed populations are built", "",
        "For each population, begin with the independence table B_ij=a_i b_j formed from its stated row and column probabilities. The main construction adds t to cells (1,1) and (2,2), and subtracts t from (1,2) and (2,1). These changes sum to zero in every affected row and column, so the margins remain fixed. A one-dimensional numerical solve chooses t so the table has the exact requested MI.", "",
        "For baseline B and plotted difference Delta, the usual direction sets I(P)=B and I(Q)=B+Delta. The reverse-direction experiment instead sets I(P)=B+Delta and I(Q)=B. The tables are constructed once and held fixed before sampling.", "",
        *worked_example(populations),
    ]
    section_number = 3
    for section in SECTION_ORDER:
        section_frame = merged[merged["section"].eq(section)]
        if section_frame.empty:
            continue
        lines.extend([f"## {section_number}. {SECTION_TITLES[section]}", "", SECTION_QUESTIONS[section], ""])
        for figure_index, figure_key in enumerate(ordered_unique(section_frame["figure_key"]), 1):
            frame = section_frame[section_frame["figure_key"].eq(figure_key)].copy()
            title = human_figure_title(frame, section, figure_key)
            filename = figure_key + ".png"
            draw_figure(frame, figure_root / filename, section, title)
            images = [f"![{title}]({image_prefix}/{filename})", ""]
            if section == "convergence":
                zoom_filename = figure_key + "_zoom.png"
                draw_figure(
                    frame, figure_root / zoom_filename, section,
                    title + ": calibration zoom", y_limits=(0.0, 0.1),
                )
                images.extend([
                    "The companion graph uses the same results with the rejection-rate axis limited to 0.1.", "",
                    f"![{title}: calibration zoom]({image_prefix}/{zoom_filename})", "",
                ])
            lines.extend([
                f"### {section_number}.{figure_index} {title}", "",
                SECTION_QUESTIONS[section], "",
                *images,
                *markdown_table(["Specification", "Setting"], specification_rows(frame, populations, section)), "",
                "Null-point rejection and validity:", "",
                *markdown_table(["Vertical regime", "Horizontal regime", "x", "Method", "Rejection", "Valid"], null_rows(frame)), "",
                "<details><summary>Every plotted rate, interval, validity and minimum expected count</summary>", "",
                *markdown_table(
                    ["Vertical regime", "Horizontal regime", "x", "Method", "Rejection", "95% interval", "Valid", "Conditional", "Min expected P", "Min expected Q"],
                    detail_rows(frame, section),
                ), "", "</details>", "",
            ])
        section_number += 1
    if full and (output / "runtime_summary.csv").exists():
        lines.extend(overall_summary(display, results, output, section_number))
        section_number += 1
    runtime_lines = runtime_section(output, section_number)
    lines.extend(runtime_lines)
    if runtime_lines:
        section_number += 1
    lines.extend([
        f"## {section_number}. Reproducibility", "",
        f"The manifest contains {results['configuration_id'].nunique():,} unique simulated configurations and {len(display):,} display points. Reused configurations were simulated once and referenced in multiple prespecified sections.", "",
        "- [Executable protocol](../../experiments/THESIS_REDESIGN_PROTOCOL.json)",
        "- [Unique configuration manifest](../../results/thesis_redesign/configuration_manifest.csv)",
        "- [Display-to-configuration map](../../results/thesis_redesign/display_manifest.csv)",
        "- [Full-precision population tables](../../results/thesis_redesign/population_definitions.csv)",
        "- [Per-method results](../../results/thesis_redesign/cell_results.csv)",
        "- [Paired method results](../../results/thesis_redesign/paired_method_results.csv)",
        "- [Verification record](../../results/thesis_redesign/verification.json)",
        "- [Runtime results](../../results/thesis_redesign/runtime_summary.csv)",
        "- [Run metadata and source hashes](../../results/thesis_redesign/run_metadata.json)",
        "- [Report verification](../../results/thesis_redesign/report_verification.json)",
        "- [Report and reporter hashes](../../results/thesis_redesign/report_metadata.json)", "",
        "The report presents the complete prespecified landscape before interpretation. It does not average regimes or use result-dependent thresholds.", "",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    if full:
        (output / "REPORT.md").write_text(
            "# Thesis Experiment Report\n\nSee [the reader-facing report](../../docs/experiments/THESIS_EXPERIMENTS.md).\n",
            encoding="utf-8",
        )
    image_links = re.findall(r"!\[[^]]*\]\(([^)]+)\)", report_path.read_text(encoding="utf-8"))
    expected_figures = int(display["figure_key"].nunique()) + int(
        display.loc[display["section"].eq("convergence"), "figure_key"].nunique()
    )
    checks = {
        "expected_figure_count": len(image_links) == expected_figures,
        "all_referenced_figures_exist": all((report_path.parent / link).exists() for link in image_links),
        "every_display_point_has_two_method_rows": len(merged) == 2 * len(display),
        "no_missing_result_rows": not merged["method"].isna().any(),
    }
    checks["all_pass"] = all(checks.values())
    (output / "report_verification.json").write_text(
        json.dumps(checks, indent=2) + "\n", encoding="utf-8"
    )
    if not checks["all_pass"]:
        raise RuntimeError("Generated report failed verification.")
    report_metadata = {
        "report_sha256": file_sha256(report_path),
        "reporter_sha256": file_sha256(Path(__file__)),
        "primary_figures": int(display["figure_key"].nunique()),
        "companion_calibration_zooms": int(
            display.loc[display["section"].eq("convergence"), "figure_key"].nunique()
        ),
    }
    (output / "report_metadata.json").write_text(
        json.dumps(report_metadata, indent=2) + "\n", encoding="utf-8"
    )
    return report_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=Path(__file__).with_name("THESIS_REDESIGN_PROTOCOL.json"))
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results/thesis_redesign")
    arguments = parser.parse_args()
    print(build_report(arguments.protocol.resolve(), arguments.output_dir.resolve()))
