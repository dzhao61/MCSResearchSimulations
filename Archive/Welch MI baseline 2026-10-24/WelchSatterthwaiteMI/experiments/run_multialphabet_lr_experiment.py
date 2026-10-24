#!/usr/bin/env python3
"""Evaluate equal-MI inference from 3x3 through 8x8 tables."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.distributions import (  # noqa: E402
    interaction_pattern,
    marginal_probabilities,
    mutual_information_probability,
    table_with_target_mi_from_interaction,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402
from welch_differential_mi.likelihood_ratio import (  # noqa: E402
    constrained_likelihood_ratio_test,
)


ALPHA = 0.05
BASE_MI = 0.05
ALTERNATIVE_MI = 0.10
NULL_STAGE = "equal_mi_null"
ALTERNATIVE_STAGE = "alternative"
SHAPES = (3, 4, 5, 8)
REGIMES = ("balanced", "mild", "strong", "ultra")
COMMON_SAMPLE_SIZES = (25, 50, 75, 100, 150, 250, 500, 1_000)
SAMPLE_SIZES = {size: COMMON_SAMPLE_SIZES for size in SHAPES}
PROFILE_REPLICATES = {
    "smoke": {3: 20, 4: 15, 5: 10, 8: 5},
    "screen": {3: 1_000, 4: 750, 5: 500, 8: 250},
    "confirmatory": {3: 5_000, 4: 2_500, 5: 1_500, 8: 500},
}
METHODS = {
    "normal_wald": {
        "label": "Normal Wald",
        "p_value": "normal_p_value",
        "valid": "base_valid",
        "color": "#24557A",
        "linestyle": "-",
        "marker": "o",
    },
    "expanded_welch": {
        "label": "Expanded Welch",
        "p_value": "expanded_welch_p_value",
        "valid": "expanded_valid",
        "color": "#A23B72",
        "linestyle": "--",
        "marker": "s",
    },
    "constrained_lr": {
        "label": "Constrained LR",
        "p_value": None,
        "valid": None,
        "color": "#D87928",
        "linestyle": ":",
        "marker": "^",
    },
}
REGIME_LABELS = {
    "balanced": "Balanced margins",
    "mild": "Mildly skewed margins",
    "strong": "Strongly skewed margins",
    "ultra": "Ultra-skewed margins",
}


@dataclass(frozen=True)
class PopulationDesign:
    size: int
    regime: str
    probability_p: np.ndarray
    probability_q_null: np.ndarray
    probability_q_alternative: np.ndarray
    association_p: float
    association_q_null: float
    association_q_alternative: float


def _stable_seed(base_seed: int, *parts: object) -> int:
    text = "|".join(str(part) for part in (base_seed, *parts))
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "little")


def build_population_design(size: int, regime: str) -> PopulationDesign:
    """Build a deterministic weak-null pair and a matched alternative."""
    if regime == "ultra":
        margin_p = np.concatenate(
            ([0.95], np.repeat(0.05 / (size - 1), size - 1))
        )
    else:
        margin_p = marginal_probabilities(size, regime)
    margin_q_row = np.roll(margin_p, 1)
    margin_q_column = np.roll(margin_p, -1)
    interaction = interaction_pattern(size, size, "ordinal")

    probability_p, association_p = table_with_target_mi_from_interaction(
        margin_p,
        margin_p,
        BASE_MI,
        interaction,
    )
    probability_q_null, association_q_null = table_with_target_mi_from_interaction(
        margin_q_row,
        margin_q_column,
        BASE_MI,
        -interaction,
    )
    probability_q_alternative, association_q_alternative = (
        table_with_target_mi_from_interaction(
            margin_q_row,
            margin_q_column,
            ALTERNATIVE_MI,
            -interaction,
        )
    )

    achieved = (
        mutual_information_probability(probability_p),
        mutual_information_probability(probability_q_null),
        mutual_information_probability(probability_q_alternative),
    )
    expected = (BASE_MI, BASE_MI, ALTERNATIVE_MI)
    if not np.allclose(achieved, expected, atol=1e-10, rtol=0.0):
        raise RuntimeError("Population construction missed its MI target.")
    return PopulationDesign(
        size=size,
        regime=regime,
        probability_p=probability_p,
        probability_q_null=probability_q_null,
        probability_q_alternative=probability_q_alternative,
        association_p=association_p,
        association_q_null=association_q_null,
        association_q_alternative=association_q_alternative,
    )


def build_population_designs(
    shapes: tuple[int, ...] = SHAPES,
) -> list[PopulationDesign]:
    return [
        build_population_design(size, regime)
        for size in shapes
        for regime in REGIMES
    ]


def _wilson(successes: int, total: int) -> tuple[float, float]:
    if total == 0:
        return np.nan, np.nan
    z = 1.959963984540054
    rate = successes / total
    denominator = 1.0 + z * z / total
    centre = (rate + z * z / (2.0 * total)) / denominator
    half_width = (
        z
        * np.sqrt(rate * (1.0 - rate) / total + z * z / (4.0 * total**2))
        / denominator
    )
    return centre - half_width, centre + half_width


def _method_row(
    *,
    design: PopulationDesign,
    sample_size: int,
    stage: str,
    method: str,
    p_values: np.ndarray,
    valid: np.ndarray,
    replicates: int,
) -> dict:
    finite_valid = valid & np.isfinite(p_values)
    valid_count = int(np.count_nonzero(finite_valid))
    rejected = finite_valid & (p_values <= ALPHA)
    reject_count = int(np.count_nonzero(rejected))
    rate = reject_count / valid_count if valid_count else np.nan
    low, high = _wilson(reject_count, valid_count)
    return {
        "configuration_id": f"{design.size}x{design.size}_{design.regime}_n{sample_size}",
        "shape": f"{design.size}x{design.size}",
        "alphabet_size": design.size,
        "cells": design.size**2,
        "regime": design.regime,
        "regime_label": REGIME_LABELS[design.regime],
        "sample_size_p": sample_size,
        "sample_size_q": sample_size,
        "observations_per_cell": sample_size / design.size**2,
        "stage": stage,
        "true_mi_p": BASE_MI,
        "true_mi_q": BASE_MI if stage == NULL_STAGE else ALTERNATIVE_MI,
        "true_mi_difference": (
            0.0 if stage == NULL_STAGE else ALTERNATIVE_MI - BASE_MI
        ),
        "method": method,
        "method_label": METHODS[method]["label"],
        "replicates": replicates,
        "valid_count": valid_count,
        "valid_rate": valid_count / replicates,
        "reject_count": reject_count,
        "rejection_rate": rate,
        "wilson_low": low,
        "wilson_high": high,
        "absolute_calibration_error": (
            abs(rate - ALPHA) if stage == NULL_STAGE else np.nan
        ),
    }


def _simulate_stage(
    design: PopulationDesign,
    sample_size: int,
    stage: str,
    replicates: int,
    seed: int,
) -> tuple[list[dict], dict]:
    probability_q = (
        design.probability_q_null
        if stage == NULL_STAGE
        else design.probability_q_alternative
    )
    rng = np.random.default_rng(
        _stable_seed(seed, design.size, design.regime, sample_size, stage)
    )
    table_p = rng.multinomial(
        sample_size,
        design.probability_p.reshape(-1),
        size=replicates,
    ).reshape(replicates, design.size, design.size)
    table_q = rng.multinomial(
        sample_size,
        probability_q.reshape(-1),
        size=replicates,
    ).reshape(replicates, design.size, design.size)

    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        analytic = differential_mi_pvalues(
            table_p,
            table_q,
            include_simple=False,
            include_unbiased_sensitivity=False,
        )
    rows = []
    for method in ("normal_wald", "expanded_welch"):
        specification = METHODS[method]
        p_values = np.asarray(analytic[specification["p_value"]], dtype=float)
        valid = np.asarray(analytic[specification["valid"]], dtype=bool)
        rows.append(
            _method_row(
                design=design,
                sample_size=sample_size,
                stage=stage,
                method=method,
                p_values=p_values,
                valid=valid,
                replicates=replicates,
            )
        )

    lr_p_values = np.full(replicates, np.nan)
    lr_elapsed = np.full(replicates, np.nan)
    lr_iterations = np.full(replicates, np.nan)
    lr_residuals = np.full(replicates, np.nan)
    for index in range(replicates):
        result = constrained_likelihood_ratio_test(table_p[index], table_q[index])
        if result.converged:
            lr_p_values[index] = float(chi2.sf(result.statistic, df=1))
            lr_elapsed[index] = result.elapsed_seconds
            lr_iterations[index] = result.iterations
            lr_residuals[index] = result.constraint_residual
    lr_valid = np.isfinite(lr_p_values)
    rows.append(
        _method_row(
            design=design,
            sample_size=sample_size,
            stage=stage,
            method="constrained_lr",
            p_values=lr_p_values,
            valid=lr_valid,
            replicates=replicates,
        )
    )

    probability_p = design.probability_p
    combined_probabilities = np.concatenate(
        [probability_p.reshape(-1), probability_q.reshape(-1)]
    )
    expected = sample_size * combined_probabilities
    valid_elapsed = lr_elapsed[np.isfinite(lr_elapsed)]
    valid_iterations = lr_iterations[np.isfinite(lr_iterations)]
    valid_residuals = lr_residuals[np.isfinite(lr_residuals)]
    diagnostics = {
        "configuration_id": f"{design.size}x{design.size}_{design.regime}_n{sample_size}",
        "shape": f"{design.size}x{design.size}",
        "alphabet_size": design.size,
        "regime": design.regime,
        "sample_size": sample_size,
        "stage": stage,
        "replicates": replicates,
        "minimum_expected_count": float(expected.min()),
        "fraction_expected_below_1": float(np.mean(expected < 1.0)),
        "fraction_expected_below_5": float(np.mean(expected < 5.0)),
        "mean_observed_zero_cell_fraction_p": float(np.mean(table_p == 0)),
        "mean_observed_zero_cell_fraction_q": float(np.mean(table_q == 0)),
        "lr_valid_rate": float(np.mean(lr_valid)),
        "lr_median_elapsed_ms": (
            float(np.median(valid_elapsed) * 1_000.0)
            if valid_elapsed.size
            else np.nan
        ),
        "lr_p90_elapsed_ms": (
            float(np.quantile(valid_elapsed, 0.90) * 1_000.0)
            if valid_elapsed.size
            else np.nan
        ),
        "lr_median_iterations": (
            float(np.median(valid_iterations)) if valid_iterations.size else np.nan
        ),
        "lr_max_constraint_residual": (
            float(np.max(valid_residuals)) if valid_residuals.size else np.nan
        ),
    }
    return rows, diagnostics


def _run_task(task: tuple[PopulationDesign, int, int, int]) -> dict:
    design, sample_size, replicates, seed = task
    start = perf_counter()
    rows = []
    diagnostics = []
    for stage in (NULL_STAGE, ALTERNATIVE_STAGE):
        stage_rows, stage_diagnostics = _simulate_stage(
            design,
            sample_size,
            stage,
            replicates,
            seed,
        )
        rows.extend(stage_rows)
        diagnostics.append(stage_diagnostics)
    return {
        "rows": rows,
        "diagnostics": diagnostics,
        "wall_seconds": perf_counter() - start,
    }


def _configuration_rows(designs: list[PopulationDesign]) -> list[dict]:
    rows = []
    for design in designs:
        for sample_size in SAMPLE_SIZES[design.size]:
            p = design.probability_p
            q0 = design.probability_q_null
            q1 = design.probability_q_alternative
            rows.append(
                {
                    "configuration_id": (
                        f"{design.size}x{design.size}_{design.regime}_n{sample_size}"
                    ),
                    "shape": f"{design.size}x{design.size}",
                    "alphabet_size": design.size,
                    "cells": design.size**2,
                    "regime": design.regime,
                    "regime_label": REGIME_LABELS[design.regime],
                    "sample_size_p": sample_size,
                    "sample_size_q": sample_size,
                    "observations_per_cell": sample_size / design.size**2,
                    "true_mi_p": mutual_information_probability(p),
                    "true_mi_q_null": mutual_information_probability(q0),
                    "true_mi_q_alternative": mutual_information_probability(q1),
                    "minimum_expected_count_null": sample_size
                    * min(float(p.min()), float(q0.min())),
                    "fraction_expected_below_1_null": float(
                        np.mean(
                            sample_size
                            * np.concatenate([p.reshape(-1), q0.reshape(-1)])
                            < 1.0
                        )
                    ),
                    "fraction_expected_below_5_null": float(
                        np.mean(
                            sample_size
                            * np.concatenate([p.reshape(-1), q0.reshape(-1)])
                            < 5.0
                        )
                    ),
                    "probability_p_json": json.dumps(p.tolist()),
                    "probability_q_null_json": json.dumps(q0.tolist()),
                    "probability_q_alternative_json": json.dumps(q1.tolist()),
                    "association_p": design.association_p,
                    "association_q_null": design.association_q_null,
                    "association_q_alternative": design.association_q_alternative,
                }
            )
    return rows


def _plot_metric(
    results: pd.DataFrame,
    output_dir: Path,
    *,
    stage: str,
    filename: str,
) -> None:
    selected = results[results["stage"].eq(stage)]
    shapes = tuple(sorted(selected["alphabet_size"].unique()))
    figure, axes = plt.subplots(
        len(shapes),
        len(REGIMES),
        figsize=(5 * len(REGIMES), 3.7 * len(shapes)),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for row_index, size in enumerate(shapes):
        for column_index, regime in enumerate(REGIMES):
            axis = axes[row_index, column_index]
            panel = selected[
                selected["alphabet_size"].eq(size)
                & selected["regime"].eq(regime)
            ]
            for method, specification in METHODS.items():
                curve = panel[panel["method"].eq(method)].sort_values("sample_size_p")
                axis.plot(
                    curve["sample_size_p"],
                    curve["rejection_rate"],
                    color=specification["color"],
                    linestyle=specification["linestyle"],
                    marker=specification["marker"],
                    markerfacecolor=(
                        specification["color"] if method == "normal_wald" else "white"
                    ),
                    linewidth=1.6,
                    markersize=4,
                    label=specification["label"],
                )
            if stage == NULL_STAGE:
                axis.axhline(ALPHA, color="#555555", linestyle="-.", linewidth=1)
            axis.set_xscale("log")
            axis.grid(alpha=0.18)
            if row_index == 0:
                axis.set_title(REGIME_LABELS[regime])
            if column_index == 0:
                axis.set_ylabel(f"{size}x{size}\nRejection rate")
            if row_index == len(shapes) - 1:
                axis.set_xlabel("Sample size per population")
    if stage == NULL_STAGE:
        upper = min(1.0, max(0.12, float(selected["rejection_rate"].max()) * 1.10))
        title = "False-positive calibration under equal MI (shared axes)"
    else:
        upper = 1.0
        title = "Power for a 0.05-nat MI difference (shared axes)"
    axes[0, 0].set_ylim(0.0, upper)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.975),
        ncol=3,
        frameon=False,
    )
    figure.suptitle(title, fontsize=16, y=0.995)
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    figure.savefig(output_dir / filename, dpi=180)
    plt.close(figure)


def _plot_runtime(diagnostics: pd.DataFrame, output_dir: Path) -> None:
    selected = diagnostics[diagnostics["stage"].eq(NULL_STAGE)]
    shapes = tuple(sorted(selected["alphabet_size"].unique()))
    columns = min(2, len(shapes))
    rows = int(np.ceil(len(shapes) / columns))
    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(6 * columns, 4.5 * rows),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for axis, size in zip(axes.ravel(), shapes):
        panel = selected[selected["alphabet_size"].eq(size)]
        for regime in REGIMES:
            curve = panel[panel["regime"].eq(regime)].sort_values("sample_size")
            axis.plot(
                curve["sample_size"],
                curve["lr_median_elapsed_ms"],
                marker="o",
                label=REGIME_LABELS[regime],
            )
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_title(f"{size}x{size}")
        axis.grid(alpha=0.18)
        axis.set_xlabel("Sample size per population")
        axis.set_ylabel("Median LR time per table pair (ms)")
    for axis in axes.ravel()[len(shapes) :]:
        axis.set_visible(False)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=4,
        frameon=False,
    )
    figure.suptitle("Constrained-LR runtime", fontsize=16, y=0.995)
    figure.tight_layout(rect=(0, 0, 1, 0.91))
    figure.savefig(output_dir / "LR_RUNTIME.png", dpi=180)
    plt.close(figure)


def _markdown_table(frame: pd.DataFrame) -> str:
    headers = list(frame.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in values) + " |")
    return "\n".join(lines)


def _write_report(
    output_dir: Path,
    results: pd.DataFrame,
    diagnostics: pd.DataFrame,
    profile: str,
    replicate_map: dict[int, int],
) -> None:
    shapes = tuple(sorted(results["alphabet_size"].unique()))
    lines = [
        "# Multi-Alphabet Constrained-LR Experiment",
        "",
        "This experiment extends the equal-MI comparison from binary tables to "
        "larger alphabets. Every row below is one exact population pair and sample "
        "size; no result is averaged across configurations.",
        "",
        "## Design",
        "",
        f"- Profile: `{profile}`.",
        f"- Replicates by shape: `{replicate_map}` for each null and alternative.",
        f"- Null: $I(P)=I(Q)={BASE_MI:.2f}$ nats.",
        f"- Alternative: $I(P)={BASE_MI:.2f}$ and $I(Q)={ALTERNATIVE_MI:.2f}$ nats.",
        f"- Decision threshold: $\\alpha={ALPHA:.2f}$.",
        "- Margins: balanced or one category with probability 0.70, 0.90, or 0.95.",
        "- The two populations use opposite ordinal association patterns and shifted margins.",
        "",
        "![Calibration](CALIBRATION_BY_SAMPLE_SIZE.png)",
        "",
        "![Power](POWER_BY_SAMPLE_SIZE.png)",
        "",
        "![Runtime](LR_RUNTIME.png)",
        "",
        "## Exact Results",
        "",
        "FPR is the null rejection rate and power is the alternative rejection rate, both at 0.05.",
    ]
    null = results[results["stage"].eq(NULL_STAGE)]
    power = results[results["stage"].eq(ALTERNATIVE_STAGE)]
    for size in shapes:
        lines.extend(["", f"### {size}x{size}", ""])
        for regime in REGIMES:
            rows = []
            for sample_size in SAMPLE_SIZES[size]:
                diagnostic = diagnostics[
                    diagnostics["alphabet_size"].eq(size)
                    & diagnostics["regime"].eq(regime)
                    & diagnostics["sample_size"].eq(sample_size)
                    & diagnostics["stage"].eq(NULL_STAGE)
                ].iloc[0]
                row = {
                    "n": sample_size,
                    "n/cell": f"{sample_size / size**2:.2f}",
                    "min E": f"{diagnostic['minimum_expected_count']:.3g}",
                    "cells E<1": f"{diagnostic['fraction_expected_below_1']:.2f}",
                }
                for method in METHODS:
                    null_rate = null[
                        null["alphabet_size"].eq(size)
                        & null["regime"].eq(regime)
                        & null["sample_size_p"].eq(sample_size)
                        & null["method"].eq(method)
                    ]["rejection_rate"].iloc[0]
                    power_rate = power[
                        power["alphabet_size"].eq(size)
                        & power["regime"].eq(regime)
                        & power["sample_size_p"].eq(sample_size)
                        & power["method"].eq(method)
                    ]["rejection_rate"].iloc[0]
                    short = {
                        "normal_wald": "Wald",
                        "expanded_welch": "Expanded",
                        "constrained_lr": "LR",
                    }[method]
                    row[f"{short} FPR"] = f"{null_rate:.3f}"
                    row[f"{short} power"] = f"{power_rate:.3f}"
                rows.append(row)
            lines.extend([f"**{REGIME_LABELS[regime]}**", "", _markdown_table(pd.DataFrame(rows)), ""])
    lines.extend(
        [
            "## Files",
            "",
            "- `configurations.csv`: exact probabilities and sampling diagnostics.",
            "- `results.csv`: one row per configuration, stage, and method.",
            "- `lr_diagnostics.csv`: validity, runtime, iterations, and constraint residuals.",
            "- `run_metadata.json`: profile, seeds, software versions, and elapsed time.",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILE_REPLICATES, default="screen")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2_026_083_101)
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--shape-limit", type=int)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "multialphabet_lr_screen",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.workers < 1 or (args.replicates is not None and args.replicates < 1):
        raise ValueError("Workers and replicates must be positive.")
    shapes = SHAPES[: args.shape_limit] if args.shape_limit else SHAPES
    replicate_map = dict(PROFILE_REPLICATES[args.profile])
    if args.replicates is not None:
        replicate_map = {size: args.replicates for size in SHAPES}
    designs = build_population_designs(shapes)
    tasks = [
        (design, sample_size, replicate_map[design.size], args.seed)
        for design in designs
        for sample_size in SAMPLE_SIZES[design.size]
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    completed = []
    if args.workers == 1:
        for index, task in enumerate(tasks, start=1):
            completed.append(_run_task(task))
            print(f"Configurations: {index}/{len(tasks)}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_run_task, task) for task in tasks]
            for index, future in enumerate(as_completed(futures), start=1):
                completed.append(future.result())
                print(f"Configurations: {index}/{len(tasks)}", flush=True)

    configurations = pd.DataFrame(_configuration_rows(designs)).sort_values(
        ["alphabet_size", "regime", "sample_size_p"]
    )
    results = pd.DataFrame(
        [row for item in completed for row in item["rows"]]
    ).sort_values(["alphabet_size", "regime", "sample_size_p", "stage", "method"])
    diagnostics = pd.DataFrame(
        [row for item in completed for row in item["diagnostics"]]
    ).sort_values(["alphabet_size", "regime", "sample_size", "stage"])
    configurations.to_csv(args.output_dir / "configurations.csv", index=False)
    results.to_csv(args.output_dir / "results.csv", index=False)
    diagnostics.to_csv(args.output_dir / "lr_diagnostics.csv", index=False)
    _plot_metric(
        results,
        args.output_dir,
        stage=NULL_STAGE,
        filename="CALIBRATION_BY_SAMPLE_SIZE.png",
    )
    _plot_metric(
        results,
        args.output_dir,
        stage=ALTERNATIVE_STAGE,
        filename="POWER_BY_SAMPLE_SIZE.png",
    )
    _plot_runtime(diagnostics, args.output_dir)
    _write_report(args.output_dir, results, diagnostics, args.profile, replicate_map)
    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "workers": args.workers,
        "shapes": list(shapes),
        "regimes": list(REGIMES),
        "sample_sizes": {str(key): list(value) for key, value in SAMPLE_SIZES.items()},
        "replicates_by_shape": replicate_map,
        "base_mi": BASE_MI,
        "alternative_mi": ALTERNATIVE_MI,
        "alpha": ALPHA,
        "configuration_count": len(tasks),
        "table_pair_count": sum(2 * task[2] for task in tasks),
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Completed in {metadata['elapsed_seconds']:.1f} seconds", flush=True)


if __name__ == "__main__":
    main()
