#!/usr/bin/env python3
"""Trace constrained-LR power over the full feasible 2x2 MI range."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
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
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_2x2_experiment import METHODS, Configuration, _seed, _wilson  # noqa: E402
from run_2x2_power_curves import (  # noqa: E402
    CANDIDATE_EFFECTS,
    CONFIGURATION_LABELS,
    _format_effect_axis,
    build_curve_configurations,
    selected_anchor_configurations,
)
from run_constrained_lr_audit import _fit_lr_batch  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


METHOD_LABELS = {
    "normal_wald": "Normal Wald",
    "simple_welch": "Simple Welch",
    "expanded_welch": "Expanded Welch",
    "constrained_lr": "Constrained LR",
    "bartlett_lr": "Oracle Bartlett LR",
    "empirical_lr": "Oracle-calibrated LR",
}
METHOD_STYLES = {
    "normal_wald": {"color": "#24557A", "linestyle": "-"},
    "expanded_welch": {"color": "#A23B72", "linestyle": "-"},
    "constrained_lr": {"color": "#D87928", "linestyle": "-"},
    "empirical_lr": {"color": "#228833", "linestyle": "--"},
}
PLOTTED_METHODS = tuple(METHOD_STYLES)


def _thresholds(path: Path) -> dict[str, dict[str, float]]:
    values = pd.read_csv(path)
    values = values[
        np.isclose(values["alpha"], 0.05)
        & values["configuration_id"].str.endswith("scale1")
    ]
    return {
        row.configuration_id.removeprefix("LR_").removesuffix("_scale1"): {
            "bartlett": float(row.bartlett_threshold),
            "empirical": float(row.empirical_threshold),
        }
        for row in values.itertuples()
    }


def _simulate(config: Configuration, replicates: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(_seed(seed, "lr_full_curve", config.configuration_id))
    table_p = rng.multinomial(
        config.n_p, config.pair.probability_p.reshape(-1), size=replicates
    ).reshape(replicates, 2, 2)
    table_q = rng.multinomial(
        config.n_q, config.pair.probability_q.reshape(-1), size=replicates
    ).reshape(replicates, 2, 2)
    return table_p, table_q


def _row(
    config: Configuration,
    method: str,
    rejected: np.ndarray,
    valid: np.ndarray,
) -> dict:
    valid_count = int(np.count_nonzero(valid))
    reject_count = int(np.count_nonzero(rejected & valid))
    rate = reject_count / valid_count if valid_count else np.nan
    low, high = _wilson(reject_count, valid_count)
    return {
        "configuration_id": config.configuration_id,
        "anchor_configuration_id": config.power_family,
        "configuration_label": CONFIGURATION_LABELS[config.power_family],
        "n_p": config.n_p,
        "n_q": config.n_q,
        "mi_p": config.pair.mi_p,
        "mi_q": config.pair.mi_q,
        "mi_difference": config.effect_delta_i,
        "minimum_expected_count": min(
            config.n_p * float(np.min(config.pair.probability_p)),
            config.n_q * float(np.min(config.pair.probability_q)),
        ),
        "method": method,
        "method_label": METHOD_LABELS[method],
        "replicates": len(valid),
        "valid_count": valid_count,
        "valid_rate": valid_count / len(valid),
        "reject_count": reject_count,
        "rejection_rate": rate,
        "wilson_low": low,
        "wilson_high": high,
    }


def _run_configuration(
    task: tuple[Configuration, int, int, dict[str, dict[str, float]]]
) -> dict:
    config, replicates, seed, thresholds = task
    table_p, table_q = _simulate(config, replicates, seed)
    values = differential_mi_pvalues(table_p, table_q)
    lr_statistic, diagnostics = _fit_lr_batch(table_p, table_q)
    rows = []
    for method, specification in METHODS.items():
        valid = np.asarray(values[specification["valid"]], dtype=bool)
        p_value = np.asarray(values[specification["p_value"]], dtype=float)
        rows.append(_row(config, method, p_value <= 0.05, valid))

    valid_lr = np.isfinite(lr_statistic)
    anchor_thresholds = thresholds[config.power_family]
    for method, threshold in (
        ("constrained_lr", float(chi2.ppf(0.95, 1))),
        ("bartlett_lr", anchor_thresholds["bartlett"]),
        ("empirical_lr", anchor_thresholds["empirical"]),
    ):
        rows.append(_row(config, method, lr_statistic >= threshold, valid_lr))
    return {
        "rows": rows,
        "diagnostics": {"configuration_id": config.configuration_id, **diagnostics},
    }


def _plot(
    results: pd.DataFrame,
    output_dir: Path,
    *,
    filename: str,
    effect_cap: float | None = None,
    logarithmic: bool = False,
) -> None:
    figure, axes = plt.subplots(3, 5, figsize=(20, 11))
    flat_axes = axes.ravel()
    for axis, (anchor_id, label) in zip(
        flat_axes, CONFIGURATION_LABELS.items(), strict=False
    ):
        selected = results[results["anchor_configuration_id"].eq(anchor_id)]
        if effect_cap is not None:
            selected = selected[selected["mi_difference"] <= effect_cap]
        for method in PLOTTED_METHODS:
            curve = selected[selected["method"].eq(method)].sort_values("mi_difference")
            axis.plot(
                curve["mi_difference"],
                curve["rejection_rate"],
                marker="o",
                linewidth=1.6,
                markersize=3.5,
                label=METHOD_LABELS[method],
                **METHOD_STYLES[method],
            )
        axis.axhline(0.05, color="#555555", linestyle=":", linewidth=1)
        _format_effect_axis(
            axis, float(selected["mi_difference"].max()), logarithmic=logarithmic
        )
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
    figure.suptitle(
        "2x2 constrained-LR power curves: full feasible range",
        fontsize=16,
        y=0.995,
    )
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    figure.savefig(output_dir / filename, dpi=180)
    plt.close(figure)


def _configuration_summary(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for anchor_id, group in results.groupby("anchor_configuration_id", sort=False):
        wide = group.pivot(index="mi_difference", columns="method", values="rejection_rate")
        alternatives = wide[wide.index > 0]
        for candidate in ("constrained_lr", "empirical_lr"):
            for baseline in ("normal_wald", "expanded_welch"):
                difference = alternatives[candidate] - alternatives[baseline]
                rows.append(
                    {
                        "anchor_configuration_id": anchor_id,
                        "configuration_label": CONFIGURATION_LABELS[anchor_id],
                        "candidate": candidate,
                        "baseline": baseline,
                        "feasible_nonzero_effects": len(difference),
                        "mean_power_difference": float(difference.mean()),
                        "median_power_difference": float(difference.median()),
                        "candidate_higher_count": int(np.count_nonzero(difference > 0)),
                        "candidate_lower_count": int(np.count_nonzero(difference < 0)),
                        "candidate_null_rejection_rate": float(wide.loc[0.0, candidate]),
                        "baseline_null_rejection_rate": float(wide.loc[0.0, baseline]),
                    }
                )
    return pd.DataFrame(rows)


def _compare_existing(results: pd.DataFrame, path: Path) -> pd.DataFrame:
    existing = pd.read_csv(path)
    existing = existing[
        np.isclose(existing["sample_scale"], 1.0)
        & existing["method"].isin(METHODS)
    ][["anchor_configuration_id", "mi_difference", "method", "rejection_rate"]]
    current = results[results["method"].isin(METHODS)][
        ["anchor_configuration_id", "mi_difference", "method", "rejection_rate"]
    ]
    merged = current.merge(
        existing,
        on=["anchor_configuration_id", "mi_difference", "method"],
        suffixes=("_current_5000", "_existing_50000"),
    )
    merged["absolute_difference"] = abs(
        merged["rejection_rate_current_5000"]
        - merged["rejection_rate_existing_50000"]
    )
    return merged


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=5_000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2_026_082_701)
    parser.add_argument(
        "--thresholds",
        type=Path,
        default=PROJECT_ROOT
        / "results"
        / "2x2_constrained_lr_confirmatory_fullstarts"
        / "null_thresholds.csv",
    )
    parser.add_argument(
        "--existing-curves",
        type=Path,
        default=PROJECT_ROOT / "results" / "2x2_power_curves" / "power_curves.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "2x2_constrained_lr_full_curves",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    configurations = build_curve_configurations(
        selected_anchor_configurations(),
        effects=CANDIDATE_EFFECTS,
        sample_scales=(1.0,),
    )
    thresholds = _thresholds(args.thresholds)
    tasks = [(config, args.replicates, args.seed, thresholds) for config in configurations]
    start = perf_counter()
    completed = []
    if args.workers == 1:
        completed = [_run_configuration(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_run_configuration, task) for task in tasks]
            for index, future in enumerate(as_completed(futures), start=1):
                completed.append(future.result())
                if index % 10 == 0 or index == len(futures):
                    print(f"Configurations: {index}/{len(futures)}", flush=True)

    results = pd.DataFrame(
        [row for result in completed for row in result["rows"]]
    ).sort_values(["anchor_configuration_id", "mi_difference", "method"])
    diagnostics = pd.DataFrame(
        [result["diagnostics"] for result in completed]
    ).sort_values("configuration_id")
    configuration_summary = _configuration_summary(results)
    consistency = _compare_existing(results, args.existing_curves)
    results.to_csv(args.output_dir / "power_curves.csv", index=False)
    diagnostics.to_csv(args.output_dir / "optimizer_diagnostics.csv", index=False)
    configuration_summary.to_csv(
        args.output_dir / "configuration_summary.csv", index=False
    )
    consistency.to_csv(args.output_dir / "existing_curve_consistency.csv", index=False)
    _plot(results, args.output_dir, filename="FULL_FEASIBLE_POWER_CURVES.png")
    _plot(
        results,
        args.output_dir,
        filename="SMALL_EFFECT_POWER_CURVES.png",
        effect_cap=0.05,
        logarithmic=True,
    )
    metadata = {
        "seed": args.seed,
        "replicates_per_configuration": args.replicates,
        "configuration_count": len(configurations),
        "candidate_effects": CANDIDATE_EFFECTS,
        "workers": args.workers,
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "threshold_source": str(args.thresholds),
        "existing_curve_source": str(args.existing_curves),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(
        configuration_summary.groupby(["candidate", "baseline"], as_index=False)
        .agg(
            mean_power_difference=("mean_power_difference", "mean"),
            median_power_difference=("median_power_difference", "median"),
            higher_points=("candidate_higher_count", "sum"),
            lower_points=("candidate_lower_count", "sum"),
        )
        .to_string(index=False)
    )
    print(
        "Existing 50k-curve consistency: median abs difference "
        f"{consistency['absolute_difference'].median():.4f}, "
        f"maximum {consistency['absolute_difference'].max():.4f}"
    )
    print(f"Elapsed: {metadata['elapsed_seconds']:.1f} seconds")


if __name__ == "__main__":
    main()
