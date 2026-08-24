#!/usr/bin/env python3
"""Measure power of the constrained MI likelihood-ratio test."""

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
    CONFIGURATION_LABELS,
    build_curve_configurations,
    selected_anchor_configurations,
)
from run_constrained_lr_audit import _fit_lr_batch  # noqa: E402
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


METHOD_LABELS = {
    "normal_wald": "Normal Wald",
    "simple_welch": "Simple Welch",
    "expanded_welch": "Expanded Welch",
    "constrained_lr": "Constrained LR (chi-squared)",
    "bartlett_lr": "Constrained LR (oracle Bartlett)",
    "empirical_lr": "Constrained LR (split empirical)",
}
EFFECTS = (0.005, 0.05)
SAMPLE_SCALES = (0.5, 1.0, 2.0)


def _simulate(config: Configuration, replicates: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(_seed(seed, "power", config.configuration_id))
    table_p = rng.multinomial(
        config.n_p, config.pair.probability_p.reshape(-1), size=replicates
    ).reshape(replicates, 2, 2)
    table_q = rng.multinomial(
        config.n_q, config.pair.probability_q.reshape(-1), size=replicates
    ).reshape(replicates, 2, 2)
    return table_p, table_q


def _power_row(
    config: Configuration,
    method: str,
    rejected: np.ndarray,
    valid: np.ndarray,
) -> dict:
    anchors = {
        anchor.configuration_id: anchor for anchor in selected_anchor_configurations()
    }
    anchor = anchors[config.power_family]
    valid_count = int(np.count_nonzero(valid))
    reject_count = int(np.count_nonzero(rejected & valid))
    power = reject_count / valid_count if valid_count else np.nan
    low, high = _wilson(reject_count, valid_count)
    return {
        "configuration_id": config.configuration_id,
        "anchor_configuration_id": config.power_family,
        "configuration_label": CONFIGURATION_LABELS[config.power_family],
        "sample_scale": config.n_p / anchor.n_p,
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
        "power": power,
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

    anchor = next(
        anchor
        for anchor in selected_anchor_configurations()
        if anchor.configuration_id == config.power_family
    )
    scale = config.n_p / anchor.n_p
    null_id = f"LR_{config.power_family}_scale{scale:g}"
    critical = thresholds[null_id]
    rows = []
    for method, specification in METHODS.items():
        valid = np.asarray(values[specification["valid"]], dtype=bool)
        p_value = np.asarray(values[specification["p_value"]], dtype=float)
        rows.append(_power_row(config, method, p_value <= 0.05, valid))

    valid_lr = np.isfinite(lr_statistic)
    rows.append(
        _power_row(
            config,
            "constrained_lr",
            lr_statistic >= chi2.ppf(0.95, 1),
            valid_lr,
        )
    )
    rows.append(
        _power_row(
            config,
            "bartlett_lr",
            lr_statistic >= critical["bartlett_threshold"],
            valid_lr,
        )
    )
    rows.append(
        _power_row(
            config,
            "empirical_lr",
            lr_statistic >= critical["empirical_threshold"],
            valid_lr,
        )
    )
    return {"rows": rows, "diagnostics": {"configuration_id": config.configuration_id, **diagnostics}}


def _read_thresholds(path: Path) -> dict[str, dict[str, float]]:
    data = pd.read_csv(path)
    data = data[np.isclose(data["alpha"], 0.05)]
    return {
        row.configuration_id: {
            "bartlett_threshold": float(row.bartlett_threshold),
            "empirical_threshold": float(row.empirical_threshold),
        }
        for row in data.itertuples()
    }


def _summary(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby(["mi_difference", "method", "method_label"], as_index=False)
        .agg(
            configurations=("configuration_id", "nunique"),
            mean_power=("power", "mean"),
            median_power=("power", "median"),
            minimum_valid_rate=("valid_rate", "min"),
        )
        .sort_values(["mi_difference", "method"])
    )


def _paired_differences(
    results: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    wide = results.pivot(index="configuration_id", columns="method", values="power")
    metadata = results.drop_duplicates("configuration_id").set_index("configuration_id")
    rows = []
    for candidate in ("constrained_lr", "bartlett_lr", "empirical_lr"):
        for baseline in ("normal_wald", "expanded_welch"):
            difference = wide[candidate] - wide[baseline]
            rows.append(
                {
                    "candidate": candidate,
                    "baseline": baseline,
                    "mean_power_difference": float(difference.mean()),
                    "median_power_difference": float(difference.median()),
                    "candidate_higher_count": int(np.count_nonzero(difference > 0)),
                    "candidate_lower_count": int(np.count_nonzero(difference < 0)),
                    "configurations": len(difference),
                }
            )
    detailed = wide.reset_index().merge(
        metadata[["configuration_label", "sample_scale", "mi_difference"]].reset_index(),
        on="configuration_id",
    )
    return detailed, pd.DataFrame(rows)


def _plot(results: pd.DataFrame, output_dir: Path) -> None:
    methods = ("normal_wald", "expanded_welch", "constrained_lr", "bartlett_lr")
    figure, axes = plt.subplots(1, 2, figsize=(11.5, 5.0), sharex=True, sharey=True)
    for axis, effect in zip(axes, EFFECTS, strict=True):
        selected = results[np.isclose(results["mi_difference"], effect)]
        for method in methods:
            values = selected[selected["method"].eq(method)]["power"].sort_values()
            axis.plot(
                np.linspace(0.0, 1.0, len(values)),
                values,
                marker="o",
                markersize=2.5,
                linewidth=1.3,
                label=METHOD_LABELS[method],
            )
        axis.set_title(f"MI difference = {effect:g} nats")
        axis.set_xlabel("Configuration quantile")
        axis.grid(alpha=0.2)
    axes[0].set_ylabel("Nominal power at alpha = 0.05")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.87))
    figure.savefig(output_dir / "POWER_DISTRIBUTION.png", dpi=180)
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=5_000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2_026_082_602)
    parser.add_argument(
        "--thresholds",
        type=Path,
        default=PROJECT_ROOT
        / "results"
        / "2x2_constrained_lr_confirmatory_fullstarts"
        / "null_thresholds.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "2x2_constrained_lr_power_fullstarts",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    thresholds = _read_thresholds(args.thresholds)
    configurations = build_curve_configurations(
        selected_anchor_configurations(),
        effects=EFFECTS,
        sample_scales=SAMPLE_SCALES,
    )
    tasks = [(config, args.replicates, args.seed, thresholds) for config in configurations]
    start = perf_counter()
    completed = []
    if args.workers == 1:
        completed = [_run_configuration(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_run_configuration, task) for task in tasks]
            for future in as_completed(futures):
                completed.append(future.result())

    results = pd.DataFrame(
        [row for result in completed for row in result["rows"]]
    ).sort_values(["mi_difference", "sample_scale", "anchor_configuration_id", "method"])
    diagnostics = pd.DataFrame(
        [result["diagnostics"] for result in completed]
    ).sort_values("configuration_id")
    summary = _summary(results)
    results.to_csv(args.output_dir / "configuration_power.csv", index=False)
    diagnostics.to_csv(args.output_dir / "optimizer_diagnostics.csv", index=False)
    summary.to_csv(args.output_dir / "method_power_summary.csv", index=False)
    detailed, paired_summary = _paired_differences(results)
    detailed.to_csv(args.output_dir / "paired_configuration_power.csv", index=False)
    paired_summary.to_csv(args.output_dir / "paired_power_summary.csv", index=False)
    _plot(results, args.output_dir)
    metadata = {
        "seed": args.seed,
        "replicates_per_configuration": args.replicates,
        "configuration_count": len(configurations),
        "effects": EFFECTS,
        "sample_scales": SAMPLE_SCALES,
        "workers": args.workers,
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "null_threshold_source": str(args.thresholds),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(paired_summary.to_string(index=False))
    print(f"Elapsed: {metadata['elapsed_seconds']:.1f} seconds")


if __name__ == "__main__":
    main()
