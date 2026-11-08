#!/usr/bin/env python3
"""Trace equal-MI test power across a common multi-alphabet effect grid."""

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
    mutual_information_probability,
    table_with_target_mi_from_interaction,
)
from run_multialphabet_lr_experiment import (  # noqa: E402
    ALPHA,
    BASE_MI,
    METHODS,
    PROFILE_REPLICATES,
    REGIME_LABELS,
    REGIMES,
    SAMPLE_SIZES,
    SHAPES,
    _wilson,
    build_population_design,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402
from welch_differential_mi.likelihood_ratio import (  # noqa: E402
    constrained_likelihood_ratio_test,
)


MI_DIFFERENCES = (0.0, 0.005, 0.01, 0.02, 0.035, 0.05)
INTERIOR_MI_DIFFERENCES = MI_DIFFERENCES[1:-1]
PLOTTED_METHODS = ("normal_wald", "expanded_welch", "constrained_lr")
METHOD_STYLES = {
    "normal_wald": {
        "label": "Normal Wald",
        "color": "#24557A",
        "linestyle": "-",
        "marker": "o",
        "markerfacecolor": "#24557A",
        "zorder": 1,
    },
    "expanded_welch": {
        "label": "Expanded Welch",
        "color": "#A23B72",
        "linestyle": "--",
        "marker": "s",
        "markerfacecolor": "white",
        "zorder": 2,
    },
    "constrained_lr": {
        "label": "Constrained LR",
        "color": "#D87928",
        "linestyle": ":",
        "marker": "^",
        "markerfacecolor": "white",
        "zorder": 3,
    },
}


@dataclass(frozen=True)
class CurveDesign:
    size: int
    regime: str
    mi_difference: float
    probability_p: np.ndarray
    probability_q: np.ndarray
    association_q: float


def _stable_seed(base_seed: int, *parts: object) -> int:
    value = "|".join(str(part) for part in (base_seed, *parts))
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "little")


def build_curve_design(size: int, regime: str, mi_difference: float) -> CurveDesign:
    """Construct one population pair at an exact MI difference."""
    if mi_difference < 0.0:
        raise ValueError("MI difference must be nonnegative.")
    base = build_population_design(size, regime)
    if np.isclose(mi_difference, 0.0):
        probability_q = base.probability_q_null
        association_q = base.association_q_null
    elif np.isclose(mi_difference, 0.05):
        probability_q = base.probability_q_alternative
        association_q = base.association_q_alternative
    else:
        row_q = base.probability_q_null.sum(axis=1)
        column_q = base.probability_q_null.sum(axis=0)
        probability_q, association_q = table_with_target_mi_from_interaction(
            row_q,
            column_q,
            BASE_MI + mi_difference,
            -interaction_pattern(size, size, "ordinal"),
        )

    achieved_difference = (
        mutual_information_probability(probability_q)
        - mutual_information_probability(base.probability_p)
    )
    if not np.isclose(achieved_difference, mi_difference, atol=1e-10, rtol=0.0):
        raise RuntimeError("Population construction missed its MI-difference target.")
    return CurveDesign(
        size=size,
        regime=regime,
        mi_difference=mi_difference,
        probability_p=base.probability_p,
        probability_q=probability_q,
        association_q=association_q,
    )


def _result_row(
    *,
    design: CurveDesign,
    sample_size: int,
    method: str,
    p_values: np.ndarray,
    valid: np.ndarray,
    replicates: int,
) -> dict:
    finite_valid = valid & np.isfinite(p_values)
    valid_count = int(np.count_nonzero(finite_valid))
    reject_count = int(np.count_nonzero(finite_valid & (p_values <= ALPHA)))
    rejection_rate = reject_count / valid_count if valid_count else np.nan
    wilson_low, wilson_high = _wilson(reject_count, valid_count)
    return {
        "configuration_id": (
            f"{design.size}x{design.size}_{design.regime}_n{sample_size}"
            f"_delta{design.mi_difference:g}"
        ),
        "shape": f"{design.size}x{design.size}",
        "alphabet_size": design.size,
        "regime": design.regime,
        "regime_label": REGIME_LABELS[design.regime],
        "sample_size_p": sample_size,
        "sample_size_q": sample_size,
        "true_mi_p": BASE_MI,
        "true_mi_q": BASE_MI + design.mi_difference,
        "true_mi_difference": design.mi_difference,
        "method": method,
        "method_label": METHOD_STYLES[method]["label"],
        "replicates": replicates,
        "valid_count": valid_count,
        "valid_rate": valid_count / replicates,
        "reject_count": reject_count,
        "rejection_rate": rejection_rate,
        "wilson_low": wilson_low,
        "wilson_high": wilson_high,
        "source": "curve_run",
    }


def _simulate_configuration(
    task: tuple[CurveDesign, int, int, int],
) -> dict:
    design, sample_size, replicates, seed = task
    rng = np.random.default_rng(
        _stable_seed(
            seed,
            design.size,
            design.regime,
            sample_size,
            design.mi_difference,
        )
    )
    table_p = rng.multinomial(
        sample_size,
        design.probability_p.reshape(-1),
        size=replicates,
    ).reshape(replicates, design.size, design.size)
    table_q = rng.multinomial(
        sample_size,
        design.probability_q.reshape(-1),
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
        rows.append(
            _result_row(
                design=design,
                sample_size=sample_size,
                method=method,
                p_values=np.asarray(analytic[specification["p_value"]], dtype=float),
                valid=np.asarray(analytic[specification["valid"]], dtype=bool),
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
        _result_row(
            design=design,
            sample_size=sample_size,
            method="constrained_lr",
            p_values=lr_p_values,
            valid=lr_valid,
            replicates=replicates,
        )
    )

    expected = sample_size * np.concatenate(
        [design.probability_p.reshape(-1), design.probability_q.reshape(-1)]
    )
    valid_elapsed = lr_elapsed[np.isfinite(lr_elapsed)]
    valid_iterations = lr_iterations[np.isfinite(lr_iterations)]
    valid_residuals = lr_residuals[np.isfinite(lr_residuals)]
    diagnostics = {
        "configuration_id": rows[0]["configuration_id"],
        "alphabet_size": design.size,
        "regime": design.regime,
        "sample_size": sample_size,
        "true_mi_difference": design.mi_difference,
        "replicates": replicates,
        "minimum_expected_count": float(expected.min()),
        "fraction_expected_below_1": float(np.mean(expected < 1.0)),
        "fraction_expected_below_5": float(np.mean(expected < 5.0)),
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
    return {"rows": rows, "diagnostics": diagnostics}


def _load_endpoint_rows(path: Path, shapes: tuple[int, ...]) -> pd.DataFrame:
    """Convert the completed fixed-effect screen into curve endpoint rows."""
    existing = pd.read_csv(path)
    existing = existing[
        existing["alphabet_size"].isin(shapes)
        & existing["method"].isin(PLOTTED_METHODS)
    ].copy()
    existing["true_mi_difference"] = np.where(
        existing["stage"].eq("equal_mi_null"), 0.0, 0.05
    )
    existing = existing[
        existing["true_mi_difference"].isin((0.0, 0.05))
    ].copy()
    existing["true_mi_q"] = BASE_MI + existing["true_mi_difference"]
    existing["source"] = "fixed_effect_screen"
    columns = [
        "configuration_id",
        "shape",
        "alphabet_size",
        "regime",
        "regime_label",
        "sample_size_p",
        "sample_size_q",
        "true_mi_p",
        "true_mi_q",
        "true_mi_difference",
        "method",
        "method_label",
        "replicates",
        "valid_count",
        "valid_rate",
        "reject_count",
        "rejection_rate",
        "wilson_low",
        "wilson_high",
        "source",
    ]
    endpoints = existing[columns]
    expected_rows = len(shapes) * len(REGIMES) * 8 * 2 * len(PLOTTED_METHODS)
    if len(endpoints) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} endpoint rows in {path}, found {len(endpoints)}."
        )
    return endpoints


def _plot_alphabet(results: pd.DataFrame, output_dir: Path, size: int) -> None:
    panel_data = results[results["alphabet_size"].eq(size)]
    sample_sizes = SAMPLE_SIZES[size]
    figure, axes = plt.subplots(
        len(REGIMES),
        len(sample_sizes),
        figsize=(24, 12),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for row_index, regime in enumerate(REGIMES):
        for column_index, sample_size in enumerate(sample_sizes):
            axis = axes[row_index, column_index]
            selected = panel_data[
                panel_data["regime"].eq(regime)
                & panel_data["sample_size_p"].eq(sample_size)
            ]
            for method in PLOTTED_METHODS:
                curve = selected[selected["method"].eq(method)].sort_values(
                    "true_mi_difference"
                )
                style = METHOD_STYLES[method]
                axis.plot(
                    curve["true_mi_difference"],
                    curve["rejection_rate"],
                    color=style["color"],
                    linestyle=style["linestyle"],
                    marker=style["marker"],
                    markerfacecolor=style["markerfacecolor"],
                    linewidth=1.55,
                    markersize=3.4,
                    zorder=style["zorder"],
                    label=style["label"],
                )
            axis.axhline(ALPHA, color="#666666", linestyle="-.", linewidth=0.8)
            axis.set_xlim(MI_DIFFERENCES[0], MI_DIFFERENCES[-1])
            axis.set_ylim(0.0, 1.0)
            axis.set_xticks((0.0, 0.01, 0.02, 0.035, 0.05))
            axis.set_xticklabels(("0", ".01", ".02", ".035", ".05"), fontsize=7)
            axis.tick_params(axis="y", labelsize=7)
            axis.grid(alpha=0.16)
            if row_index == 0:
                axis.set_title(f"N = {sample_size}", fontsize=10)
            if column_index == 0:
                axis.set_ylabel(
                    f"{REGIME_LABELS[regime]}\nRejection rate",
                    fontsize=9,
                )
            if row_index == len(REGIMES) - 1:
                axis.set_xlabel("MI difference (nats)", fontsize=8)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.958),
        ncol=3,
        frameon=False,
    )
    figure.suptitle(
        f"{size}x{size} equal-MI test power curves (shared axes)",
        fontsize=16,
        y=0.995,
    )
    figure.text(
        0.5,
        0.925,
        (
            r"$I(P)=0.05$ nats; horizontal line = $\alpha=0.05$; "
            "each panel uses independently simulated table pairs"
        ),
        ha="center",
        fontsize=9,
        color="#555555",
    )
    figure.tight_layout(rect=(0.01, 0.02, 1, 0.89))
    figure.savefig(output_dir / f"POWER_CURVES_{size}x{size}.png", dpi=180)
    plt.close(figure)


def _write_report(
    output_dir: Path,
    results: pd.DataFrame,
    shapes: tuple[int, ...],
    replicate_map: dict[int, int],
    endpoint_results: Path | None,
) -> None:
    lines = [
        "# Multi-Alphabet Power Curves",
        "",
        "These figures compare Normal Wald, Expanded Welch, and the usable "
        "constrained likelihood-ratio test over the same MI-difference range.",
        "",
        "- Population MI: $I(P)=0.05$ nats.",
        "- Comparison MI: $I(Q)=0.05+\\Delta$ nats.",
        "- Common effects: $\\Delta\\in\\{0,0.005,0.01,0.02,0.035,0.05\\}$ nats.",
        "- Significance level: $\\alpha=0.05$.",
        "- Rows: balanced, mildly skewed, strongly skewed, and ultra-skewed margins.",
        "- Columns: exact sample size per population.",
        "- All panels and alphabet figures use the same axes.",
        f"- Replicates per point by alphabet: `{replicate_map}`.",
    ]
    if endpoint_results is not None:
        lines.append(
            f"- The $\\Delta=0$ and $0.05$ endpoints are reused from `{endpoint_results}`."
        )
    for size in shapes:
        lines.extend(
            [
                "",
                f"## {size}x{size}",
                "",
                f"![{size}x{size} power curves](POWER_CURVES_{size}x{size}.png)",
            ]
        )

    alternative = results[results["true_mi_difference"] > 0].copy()
    summary = (
        alternative.groupby("method_label", as_index=False)
        .agg(
            mean_rejection_rate=("rejection_rate", "mean"),
            median_rejection_rate=("rejection_rate", "median"),
            minimum_valid_rate=("valid_rate", "min"),
        )
        .sort_values("method_label")
    )
    lines.extend(["", "## Overall numerical summary", ""])
    lines.extend(
        [
            "| Method | Mean rejection rate | Median rejection rate | Minimum valid rate |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.method_label} | {row.mean_rejection_rate:.4f} | "
            f"{row.median_rejection_rate:.4f} | {row.minimum_valid_rate:.4f} |"
        )
    lines.extend(
        [
            "",
            "The averages are descriptive only. The individual panels are the primary "
            "result because calibration, power, and validity vary substantially by "
            "sample size and marginal regime.",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILE_REPLICATES, default="screen")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2_026_083_102)
    parser.add_argument("--replicates", type=int)
    parser.add_argument("--shape-limit", type=int)
    parser.add_argument(
        "--endpoint-results",
        type=Path,
        default=PROJECT_ROOT / "results" / "multialphabet_lr_screen" / "results.csv",
        help="Reuse the completed delta=0 and delta=0.05 screen endpoints.",
    )
    parser.add_argument(
        "--no-reuse-endpoints",
        action="store_true",
        help="Simulate all six effects instead of reusing the completed endpoints.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "multialphabet_lr_power_curves",
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

    reuse_endpoints = not args.no_reuse_endpoints
    effects_to_simulate = INTERIOR_MI_DIFFERENCES if reuse_endpoints else MI_DIFFERENCES
    designs = [
        build_curve_design(size, regime, mi_difference)
        for size in shapes
        for regime in REGIMES
        for mi_difference in effects_to_simulate
    ]
    tasks = [
        (design, sample_size, replicate_map[design.size], args.seed)
        for design in designs
        for sample_size in SAMPLE_SIZES[design.size]
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = perf_counter()
    completed = []
    if args.workers == 1:
        for index, task in enumerate(tasks, start=1):
            completed.append(_simulate_configuration(task))
            print(f"Configurations: {index}/{len(tasks)}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_simulate_configuration, task) for task in tasks]
            for index, future in enumerate(as_completed(futures), start=1):
                completed.append(future.result())
                if index % 8 == 0 or index == len(futures):
                    print(f"Configurations: {index}/{len(tasks)}", flush=True)

    simulated_results = pd.DataFrame(
        [row for item in completed for row in item["rows"]]
    )
    diagnostics = pd.DataFrame(
        [item["diagnostics"] for item in completed]
    )
    endpoint_path: Path | None = None
    if reuse_endpoints:
        endpoint_path = args.endpoint_results
        endpoints = _load_endpoint_rows(endpoint_path, shapes)
        results = pd.concat([endpoints, simulated_results], ignore_index=True)
    else:
        results = simulated_results

    results = results.sort_values(
        ["alphabet_size", "regime", "sample_size_p", "true_mi_difference", "method"]
    )
    diagnostics = diagnostics.sort_values(
        ["alphabet_size", "regime", "sample_size", "true_mi_difference"]
    )
    results.to_csv(args.output_dir / "power_curves.csv", index=False)
    diagnostics.to_csv(args.output_dir / "lr_diagnostics_interior.csv", index=False)
    for size in shapes:
        _plot_alphabet(results, args.output_dir, size)
    _write_report(args.output_dir, results, shapes, replicate_map, endpoint_path)

    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "workers": args.workers,
        "shapes": list(shapes),
        "regimes": list(REGIMES),
        "sample_sizes": {str(size): list(SAMPLE_SIZES[size]) for size in shapes},
        "mi_differences": list(MI_DIFFERENCES),
        "replicates_by_shape": replicate_map,
        "endpoint_results": str(endpoint_path) if endpoint_path is not None else None,
        "simulated_configuration_count": len(tasks),
        "simulated_table_pair_count": sum(task[2] for task in tasks),
        "elapsed_seconds": perf_counter() - started,
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
