#!/usr/bin/env python3
"""Trace fixed-threshold detection across MI effects and sample sizes."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_2x2_experiment import (  # noqa: E402
    METHODS,
    Configuration,
    _configuration,
    _metadata,
    _token,
    _wilson,
    build_null_configurations,
    make_pair,
    simulate_configuration,
)


CANDIDATE_EFFECTS = (
    0.0,
    1e-5,
    1e-4,
    1e-3,
    5e-3,
    1e-2,
    2e-2,
    5e-2,
    1e-1,
    2e-1,
    5e-1,
    1.0,
)
SAMPLE_SCALES = (0.5, 1.0, 2.0)
DEFAULT_SEED = 2_026_082_401
DEFAULT_SELECTION = PROJECT_ROOT / "experiments" / "2x2_confirmatory_selection.json"

COLORS = {
    "normal_wald": "#24557A",
    "simple_welch": "#D87928",
    "expanded_welch": "#A23B72",
}
SCALE_COLORS = {
    0.5: "#4477AA",
    1.0: "#CC6677",
    2.0: "#228833",
}

CONFIGURATION_LABELS = {
    "C1_N0_n10": "Balanced, very small sample",
    "C1_N0_n50": "Balanced, moderate sample",
    "C1_N0_n1000": "Balanced, large sample",
    "C1_N3_n50": "One skewed population",
    "C1_N6_n100": "Sparse, smaller sample",
    "C1_N6_n200": "Sparse, larger sample",
    "C1_N7_n1000": "Ultra-rare categories",
    "C2_N0_np20_nq200": "Balanced, unequal samples",
    "C2_N3_np500_nq50": "Skewed, unequal samples",
    "C2_N5_np200_nq2000": "Rare and highly unequal",
    "C3_C3_same_balanced_i0p005_n1000": "Near independence",
    "C4_C4_s0p1_i0p0001_n100": "Rare-cell case A",
    "C4_C4_s0p05_i0p0001_n500": "Rare-cell case B",
}


def selected_anchor_configurations(path: Path = DEFAULT_SELECTION) -> list[Configuration]:
    selection = json.loads(path.read_text(encoding="utf-8"))
    selected_ids = selection["null_configuration_ids"]
    available = {
        config.configuration_id: config
        for config in build_null_configurations()[0]
    }
    missing = [
        configuration_id
        for configuration_id in selected_ids
        if configuration_id not in available
    ]
    if missing:
        raise ValueError(f"Unknown null configuration IDs: {missing}")
    return [available[configuration_id] for configuration_id in selected_ids]


def build_curve_configurations(
    anchors: list[Configuration],
    *,
    effects: tuple[float, ...] = CANDIDATE_EFFECTS,
    sample_scales: tuple[float, ...] = SAMPLE_SCALES,
) -> list[Configuration]:
    configurations: list[Configuration] = []
    for anchor in anchors:
        source = anchor.pair
        for sample_scale in sample_scales:
            n_p = int(round(anchor.n_p * sample_scale))
            n_q = int(round(anchor.n_q * sample_scale))
            if n_p < 2 or n_q < 2:
                raise ValueError("Scaled sample sizes must both be at least two.")
            for effect in effects:
                try:
                    pair = make_pair(
                        f"CURVE_{anchor.configuration_id}_di{_token(effect)}",
                        f"Power curve for {source.purpose}",
                        (source.u_p, source.v_p),
                        (source.u_q, source.v_q),
                        source.mi_p,
                        source.mi_q + effect,
                        directions=(source.direction_p, source.direction_q),
                    )
                except ValueError:
                    # Fixed margins place a genuine upper bound on attainable MI.
                    continue
                config = _configuration(
                    "CURVE",
                    pair,
                    n_p,
                    n_q,
                    f"scale{_token(sample_scale)}",
                    effect_delta_i=effect,
                    power_family=anchor.configuration_id,
                    calibration_key=None,
                )
                configurations.append(config)
    identifiers = [config.configuration_id for config in configurations]
    if len(identifiers) != len(set(identifiers)):
        raise RuntimeError("Power-curve configuration identifiers are not unique.")
    return configurations


def _summarize(
    config: Configuration,
    values: dict[str, np.ndarray],
    diagnostics: dict[str, np.ndarray],
    anchor: Configuration,
) -> list[dict]:
    metadata = _metadata(config)
    sample_scale = config.n_p / anchor.n_p
    delta = np.asarray(values["delta_corrected"], dtype=float)
    standard_error = np.asarray(values["standard_error"], dtype=float)
    finite_delta = delta[np.isfinite(delta)]
    finite_standard_error = standard_error[np.isfinite(standard_error)]
    mean_delta = float(np.mean(finite_delta)) if finite_delta.size else np.nan
    mean_standard_error = (
        float(np.mean(finite_standard_error))
        if finite_standard_error.size
        else np.nan
    )
    rms_standard_error = (
        float(np.sqrt(np.mean(finite_standard_error**2)))
        if finite_standard_error.size
        else np.nan
    )
    rows: list[dict] = []
    for method, specification in METHODS.items():
        valid = np.asarray(values[specification["valid"]], dtype=bool)
        p_values = np.asarray(values[specification["p_value"]], dtype=float)
        valid_count = int(np.count_nonzero(valid))
        reject_count = int(np.count_nonzero(valid & (p_values <= 0.05)))
        rejection_rate = reject_count / valid_count if valid_count else np.nan
        low, high = _wilson(reject_count, valid_count)
        degrees_of_freedom = specification["df"]
        if degrees_of_freedom is None:
            median_df = np.nan
        else:
            df_values = np.asarray(values[degrees_of_freedom], dtype=float)
            usable_df = df_values[valid & np.isfinite(df_values)]
            median_df = float(np.median(usable_df)) if usable_df.size else np.nan
        rows.append(
            {
                "anchor_configuration_id": anchor.configuration_id,
                "configuration_label": CONFIGURATION_LABELS[anchor.configuration_id],
                "configuration_id": config.configuration_id,
                "sample_scale": sample_scale,
                "baseline_n_p": anchor.n_p,
                "baseline_n_q": anchor.n_q,
                "n_p": config.n_p,
                "n_q": config.n_q,
                "mi_p": config.pair.mi_p,
                "mi_q": config.pair.mi_q,
                "true_delta_p_minus_q": config.true_delta,
                "mi_difference": config.effect_delta_i,
                "minimum_expected_count": metadata["minimum_expected_either"],
                "mean_delta_corrected": mean_delta,
                "mean_delta_error": mean_delta - config.true_delta,
                "sd_delta_corrected": (
                    float(np.std(finite_delta, ddof=1))
                    if finite_delta.size > 1
                    else np.nan
                ),
                "mean_standard_error": mean_standard_error,
                "rms_standard_error": rms_standard_error,
                "method": method,
                "method_label": specification["label"],
                "replicates": len(valid),
                "valid_count": valid_count,
                "valid_rate": float(np.mean(valid)),
                "reject_count": reject_count,
                "rejection_rate": rejection_rate,
                "rejection_wilson_low": low,
                "rejection_wilson_high": high,
                "median_degrees_of_freedom": median_df,
                "p_any_zero_cell_rate": float(np.mean(diagnostics["p_any_zero_cell"])),
                "q_any_zero_cell_rate": float(np.mean(diagnostics["q_any_zero_cell"])),
                "p_empty_margin_rate": float(np.mean(diagnostics["p_empty_margin"])),
                "q_empty_margin_rate": float(np.mean(diagnostics["q_empty_margin"])),
            }
        )
    return rows


def _plot_overview(
    summary: pd.DataFrame,
    output_dir: Path,
    *,
    filename: str,
    title: str,
    effect_cap: float | None = None,
    logarithmic: bool = False,
) -> None:
    baseline = summary[np.isclose(summary["sample_scale"], 1.0)]
    figure, axes = plt.subplots(3, 5, figsize=(20, 11))
    flat_axes = axes.ravel()
    for axis, (anchor_id, label) in zip(flat_axes, CONFIGURATION_LABELS.items(), strict=False):
        selected = baseline[baseline["anchor_configuration_id"].eq(anchor_id)]
        if effect_cap is not None:
            selected = selected[selected["mi_difference"] <= effect_cap]
        for method, specification in METHODS.items():
            method_rows = selected[selected["method"].eq(method)].sort_values("mi_difference")
            axis.plot(
                method_rows["mi_difference"],
                method_rows["rejection_rate"],
                marker="o",
                linewidth=1.6,
                markersize=3.5,
                color=COLORS[method],
                label=specification["label"],
            )
        axis.axhline(0.05, color="#555555", linestyle=":", linewidth=1)
        _format_effect_axis(
            axis,
            float(selected["mi_difference"].max()),
            logarithmic=logarithmic,
        )
        upper = max(0.12, float(selected["rejection_rate"].max()) * 1.12)
        axis.set_ylim(0.0, min(1.0, upper))
        axis.set_title(label, fontsize=10)
        axis.grid(alpha=0.18)
    for axis in flat_axes[len(CONFIGURATION_LABELS) :]:
        axis.set_visible(False)
    for axis in flat_axes:
        if axis.get_visible():
            axis.set_xlabel(r"MI difference $|I(P)-I(Q)|$ (nats)")
    for axis in axes[:, 0]:
        axis.set_ylabel("Rejection rate")
    handles, labels = flat_axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=3,
        frameon=False,
    )
    figure.suptitle(
        title,
        fontsize=16,
        y=0.995,
    )
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    figure.savefig(output_dir / filename, dpi=180)
    plt.close(figure)


def _effect_tick_label(value: float, _position: int) -> str:
    if np.isclose(value, 0.0):
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.0e}"
    return f"{value:g}"


def _format_effect_axis(
    axis: plt.Axes,
    maximum: float,
    *,
    logarithmic: bool = False,
) -> None:
    axis.set_xlim(0.0, maximum * 1.04)
    if logarithmic:
        ticks = [0.0, 1e-5, 1e-4, 1e-3, 1e-2]
        ticks = [value for value in ticks if value <= maximum]
        if not np.isclose(ticks[-1], maximum):
            ticks.append(maximum)
        axis.set_xscale("symlog", linthresh=1e-5)
        axis.set_xticks(ticks)
    else:
        axis.set_xscale("linear")
        axis.xaxis.set_major_locator(
            MaxNLocator(nbins=6, steps=[1, 2, 2.5, 5, 10])
        )
    axis.xaxis.set_major_formatter(FuncFormatter(_effect_tick_label))
    axis.tick_params(axis="x", labelrotation=30)


def _plot_cases(summary: pd.DataFrame, output_dir: Path) -> None:
    case_dir = output_dir / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    for anchor_id, label in CONFIGURATION_LABELS.items():
        selected = summary[summary["anchor_configuration_id"].eq(anchor_id)]
        figure, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
        method_axes = dict(zip(METHODS, axes.ravel()[:3], strict=True))
        for method, axis in method_axes.items():
            method_rows = selected[selected["method"].eq(method)]
            for sample_scale in SAMPLE_SCALES:
                curve = method_rows[np.isclose(method_rows["sample_scale"], sample_scale)].sort_values(
                    "mi_difference"
                )
                n_p = int(curve["n_p"].iloc[0])
                n_q = int(curve["n_q"].iloc[0])
                axis.plot(
                    curve["mi_difference"],
                    curve["rejection_rate"],
                    marker="o",
                    color=SCALE_COLORS[sample_scale],
                    label=rf"$n_P:n_Q={n_p}:{n_q}$",
                )
            axis.axhline(0.05, color="#555555", linestyle=":", linewidth=1)
            _format_effect_axis(axis, float(method_rows["mi_difference"].max()))
            axis.set_title(METHODS[method]["label"])
            axis.set_ylabel("Rejection rate")
            axis.grid(alpha=0.18)

        validity_axis = axes.ravel()[3]
        expanded = selected[selected["method"].eq("expanded_welch")]
        for sample_scale in SAMPLE_SCALES:
            curve = expanded[np.isclose(expanded["sample_scale"], sample_scale)].sort_values(
                "mi_difference"
            )
            n_p = int(curve["n_p"].iloc[0])
            n_q = int(curve["n_q"].iloc[0])
            validity_axis.plot(
                curve["mi_difference"],
                curve["valid_rate"],
                marker="o",
                color=SCALE_COLORS[sample_scale],
                label=rf"$n_P:n_Q={n_p}:{n_q}$",
            )
        validity_axis.set_title("Expanded Welch validity")
        _format_effect_axis(validity_axis, float(expanded["mi_difference"].max()))
        validity_axis.set_ylabel("Valid-result rate")
        validity_axis.set_ylim(-0.02, 1.02)
        validity_axis.grid(alpha=0.18)
        validity_axis.legend(frameon=False, loc="best")
        for axis in axes[-1, :]:
            axis.set_xlabel(r"MI difference $|I(P)-I(Q)|$ (nats)")
        figure.suptitle(label, fontsize=15)
        figure.tight_layout(rect=(0, 0, 1, 0.96))
        figure.savefig(case_dir / f"{anchor_id}.png", dpi=170)
        plt.close(figure)


def _script_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--selection-file", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--replicates", type=int, default=50_000)
    parser.add_argument("--blocks", type=int, default=5)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.replicates % args.blocks != 0:
        raise ValueError("Replicates must be divisible by blocks.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = args.output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    anchors = selected_anchor_configurations(args.selection_file)
    configurations = build_curve_configurations(anchors)
    anchor_by_id = {anchor.configuration_id: anchor for anchor in anchors}
    start = perf_counter()
    rows: list[dict] = []
    for index, config in enumerate(configurations, start=1):
        anchor = anchor_by_id[config.power_family]
        values, diagnostics, _ = simulate_configuration(
            config,
            replicates=args.replicates,
            blocks=args.blocks,
            base_seed=args.seed,
            stream="power_curve",
        )
        rows.extend(_summarize(config, values, diagnostics, anchor))
        if index % 25 == 0 or index == len(configurations):
            print(f"Power-curve configurations: {index}/{len(configurations)}", flush=True)

    summary = pd.DataFrame(rows)
    design = summary.drop_duplicates("configuration_id")[
        [
            "anchor_configuration_id",
            "configuration_label",
            "configuration_id",
            "sample_scale",
            "baseline_n_p",
            "baseline_n_q",
            "n_p",
            "n_q",
            "mi_p",
            "mi_q",
            "true_delta_p_minus_q",
            "mi_difference",
            "minimum_expected_count",
        ]
    ]
    design.to_csv(args.output_dir / "configurations.csv", index=False)
    summary.to_csv(args.output_dir / "power_curves.csv", index=False)
    _plot_overview(
        summary,
        figure_dir,
        filename="POWER_CURVES_overview.png",
        title="2x2 fixed-threshold power curves: full feasible range",
    )
    _plot_overview(
        summary,
        figure_dir,
        filename="POWER_CURVES_small_effects.png",
        title="2x2 fixed-threshold power curves: small-effect detail",
        effect_cap=0.05,
        logarithmic=True,
    )
    _plot_cases(summary, figure_dir)

    metadata = {
        "seed": args.seed,
        "replicates_per_configuration": args.replicates,
        "blocks": args.blocks,
        "anchors": len(anchors),
        "sample_scales": list(SAMPLE_SCALES),
        "candidate_mi_differences": list(CANDIDATE_EFFECTS),
        "binary_mi_upper_bound_nats": float(np.log(2.0)),
        "requested_configurations": (
            len(anchors) * len(SAMPLE_SCALES) * len(CANDIDATE_EFFECTS)
        ),
        "simulated_configurations": len(configurations),
        "omitted_infeasible_configurations": (
            len(anchors) * len(SAMPLE_SCALES) * len(CANDIDATE_EFFECTS)
            - len(configurations)
        ),
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "script_sha256": _script_sha256(),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
