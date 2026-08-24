#!/usr/bin/env python3
"""Compare LR and baseline power after matching their null rejection rates."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_2x2_experiment import _seed, _wilson  # noqa: E402
from run_2x2_power_curves import (  # noqa: E402
    CANDIDATE_EFFECTS,
    CONFIGURATION_LABELS,
    _format_effect_axis,
    build_curve_configurations,
    selected_anchor_configurations,
)
from run_constrained_lr_full_curves import _simulate  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


BASELINES = {
    "normal_wald": {"p_value": "normal_p_value", "valid": "base_valid"},
    "expanded_welch": {
        "p_value": "expanded_welch_p_value",
        "valid": "expanded_valid",
    },
}
METHOD_LABELS = {
    "normal_wald": "Normal Wald (nominal)",
    "normal_wald_matched": "Normal Wald (size-matched)",
    "expanded_welch_matched": "Expanded Welch (size-matched)",
    "empirical_lr": "Oracle-calibrated LR",
}
METHOD_STYLES = {
    "normal_wald": {"color": "#24557A", "linestyle": ":"},
    "normal_wald_matched": {"color": "#24557A", "linestyle": "-"},
    "expanded_welch_matched": {"color": "#A23B72", "linestyle": "-"},
    "empirical_lr": {"color": "#228833", "linestyle": "--"},
}


def _conservative_threshold(p_values: np.ndarray, alpha: float = 0.05) -> float:
    values, counts = np.unique(np.asarray(p_values, dtype=float), return_counts=True)
    rates = np.cumsum(counts) / counts.sum()
    acceptable = values[rates <= alpha]
    return float(acceptable[-1]) if acceptable.size else -np.inf


def _development_thresholds(replicates: int, seed: int) -> pd.DataFrame:
    rows = []
    for anchor in selected_anchor_configurations():
        rng = np.random.default_rng(_seed(seed, "size_match_development", anchor.configuration_id))
        table_p = rng.multinomial(
            anchor.n_p,
            anchor.pair.probability_p.reshape(-1),
            size=replicates,
        ).reshape(replicates, 2, 2)
        table_q = rng.multinomial(
            anchor.n_q,
            anchor.pair.probability_q.reshape(-1),
            size=replicates,
        ).reshape(replicates, 2, 2)
        values = differential_mi_pvalues(table_p, table_q)
        for method, specification in BASELINES.items():
            valid = np.asarray(values[specification["valid"]], dtype=bool)
            p_values = np.asarray(values[specification["p_value"]], dtype=float)
            threshold = _conservative_threshold(p_values[valid])
            rows.append(
                {
                    "anchor_configuration_id": anchor.configuration_id,
                    "method": method,
                    "p_value_threshold": threshold,
                    "development_replicates": replicates,
                    "development_valid_count": int(np.count_nonzero(valid)),
                    "development_valid_rate": float(np.mean(valid)),
                    "development_rejection_rate": float(
                        np.mean(p_values[valid] <= threshold)
                    ),
                }
            )
    return pd.DataFrame(rows)


def _baseline_curves(
    thresholds: pd.DataFrame, replicates: int, seed: int
) -> pd.DataFrame:
    threshold_map = {
        (row.anchor_configuration_id, row.method): row.p_value_threshold
        for row in thresholds.itertuples()
    }
    configurations = build_curve_configurations(
        selected_anchor_configurations(),
        effects=CANDIDATE_EFFECTS,
        sample_scales=(1.0,),
    )
    rows = []
    for index, config in enumerate(configurations, start=1):
        table_p, table_q = _simulate(config, replicates, seed)
        values = differential_mi_pvalues(table_p, table_q)
        for method, specification in BASELINES.items():
            valid = np.asarray(values[specification["valid"]], dtype=bool)
            p_values = np.asarray(values[specification["p_value"]], dtype=float)
            threshold = threshold_map[(config.power_family, method)]
            rejected = valid & (p_values <= threshold)
            valid_count = int(np.count_nonzero(valid))
            reject_count = int(np.count_nonzero(rejected))
            rate = reject_count / valid_count if valid_count else np.nan
            low, high = _wilson(reject_count, valid_count)
            rows.append(
                {
                    "configuration_id": config.configuration_id,
                    "anchor_configuration_id": config.power_family,
                    "configuration_label": CONFIGURATION_LABELS[config.power_family],
                    "mi_difference": config.effect_delta_i,
                    "method": f"{method}_matched",
                    "method_label": METHOD_LABELS[f"{method}_matched"],
                    "p_value_threshold": threshold,
                    "replicates": replicates,
                    "valid_count": valid_count,
                    "valid_rate": valid_count / replicates,
                    "reject_count": reject_count,
                    "rejection_rate": rate,
                    "wilson_low": low,
                    "wilson_high": high,
                }
            )
        if index % 25 == 0 or index == len(configurations):
            print(f"Baseline configurations: {index}/{len(configurations)}", flush=True)
    return pd.DataFrame(rows)


def _plot(results: pd.DataFrame, output_dir: Path) -> None:
    figure, axes = plt.subplots(3, 5, figsize=(20, 11))
    flat_axes = axes.ravel()
    for axis, (anchor_id, label) in zip(
        flat_axes, CONFIGURATION_LABELS.items(), strict=False
    ):
        selected = results[results["anchor_configuration_id"].eq(anchor_id)]
        for method, style in METHOD_STYLES.items():
            curve = selected[selected["method"].eq(method)].sort_values("mi_difference")
            axis.plot(
                curve["mi_difference"],
                curve["rejection_rate"],
                marker="o",
                linewidth=1.6,
                markersize=3.5,
                label=METHOD_LABELS[method],
                **style,
            )
        axis.axhline(0.05, color="#555555", linestyle=":", linewidth=1)
        _format_effect_axis(axis, float(selected["mi_difference"].max()))
        upper = max(0.12, float(selected["rejection_rate"].max()) * 1.08)
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
        ncol=4,
        frameon=False,
    )
    figure.suptitle("2x2 power curves after matching null rejection rates", fontsize=16, y=0.995)
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    figure.savefig(output_dir / "SIZE_MATCHED_POWER_CURVES.png", dpi=180)
    plt.close(figure)


def _comparison(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for anchor_id, group in results.groupby("anchor_configuration_id", sort=False):
        wide = group.pivot(index="mi_difference", columns="method", values="rejection_rate")
        alternatives = wide[wide.index > 0]
        for baseline in ("normal_wald_matched", "expanded_welch_matched"):
            difference = alternatives["empirical_lr"] - alternatives[baseline]
            rows.append(
                {
                    "anchor_configuration_id": anchor_id,
                    "configuration_label": CONFIGURATION_LABELS[anchor_id],
                    "baseline": baseline,
                    "nonzero_effects": len(difference),
                    "mean_lr_power_difference": float(difference.mean()),
                    "median_lr_power_difference": float(difference.median()),
                    "lr_higher_count": int(np.count_nonzero(difference > 0)),
                    "lr_lower_count": int(np.count_nonzero(difference < 0)),
                    "lr_null_rate": float(wide.loc[0.0, "empirical_lr"]),
                    "baseline_null_rate": float(wide.loc[0.0, baseline]),
                }
            )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--development-replicates", type=int, default=50_000)
    parser.add_argument("--curve-replicates", type=int, default=5_000)
    parser.add_argument("--seed", type=int, default=2_026_082_702)
    parser.add_argument(
        "--lr-curves",
        type=Path,
        default=PROJECT_ROOT
        / "results"
        / "2x2_constrained_lr_full_curves"
        / "power_curves.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "2x2_lr_size_matched",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    thresholds = _development_thresholds(args.development_replicates, args.seed)
    baselines = _baseline_curves(thresholds, args.curve_replicates, 2_026_082_701)
    lr_curves = pd.read_csv(args.lr_curves)
    selected_lr = lr_curves[lr_curves["method"].eq("empirical_lr")].copy()
    nominal_wald = lr_curves[lr_curves["method"].eq("normal_wald")].copy()
    results = pd.concat([nominal_wald, baselines, selected_lr], ignore_index=True)
    comparison = _comparison(results)
    thresholds.to_csv(args.output_dir / "baseline_null_thresholds.csv", index=False)
    baselines.to_csv(args.output_dir / "size_matched_baseline_curves.csv", index=False)
    results.to_csv(args.output_dir / "combined_power_curves.csv", index=False)
    comparison.to_csv(args.output_dir / "configuration_comparison.csv", index=False)
    _plot(results, args.output_dir)
    metadata = {
        "seed": args.seed,
        "development_replicates_per_anchor": args.development_replicates,
        "curve_replicates_per_point": args.curve_replicates,
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "lr_curve_source": str(args.lr_curves),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(
        comparison.groupby("baseline", as_index=False)
        .agg(
            mean_lr_power_difference=("mean_lr_power_difference", "mean"),
            median_lr_power_difference=("median_lr_power_difference", "median"),
            lr_higher_points=("lr_higher_count", "sum"),
            lr_lower_points=("lr_lower_count", "sum"),
        )
        .to_string(index=False)
    )
    print(f"Elapsed: {metadata['elapsed_seconds']:.1f} seconds")


if __name__ == "__main__":
    main()
