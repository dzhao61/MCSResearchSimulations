#!/usr/bin/env python3
"""Go/no-go audit for joint Edgeworth and Cornish-Fisher calibration."""

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
from scipy.stats import kurtosis, norm, skew

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from run_2x2_experiment import _seed, _wilson  # noqa: E402
from run_2x2_power_curves import (  # noqa: E402
    CONFIGURATION_LABELS,
    SAMPLE_SCALES,
    build_curve_configurations,
    selected_anchor_configurations,
)
from welch_differential_mi.higher_order import (  # noqa: E402
    joint_cornish_fisher_parameters,
    joint_cornish_fisher_values,
)
from welch_differential_mi.welch import differential_mi_pvalues  # noqa: E402


ALPHA = 0.05
DEFAULT_REPLICATES = 20_000
DEFAULT_BLOCKS = 4
DEFAULT_SEED = 2_026_082_601


def audit_configurations():
    anchors = selected_anchor_configurations()
    configurations = build_curve_configurations(
        anchors,
        effects=(0.0,),
        sample_scales=SAMPLE_SCALES,
    )
    return anchors, configurations


def cornish_fisher_boundaries(
    values: np.ndarray,
    *,
    alpha: float = ALPHA,
) -> dict[str, tuple[float, float]]:
    """Estimate normal and Cornish-Fisher boundaries from one sample."""
    sample = np.asarray(values, dtype=float)
    sample = sample[np.isfinite(sample)]
    if sample.size < 4:
        raise ValueError("At least four finite values are required.")
    mean = float(np.mean(sample))
    standard_deviation = float(np.std(sample, ddof=1))
    sample_skewness = float(skew(sample, bias=False))
    excess_kurtosis = float(kurtosis(sample, fisher=True, bias=False))
    z = np.asarray([norm.ppf(alpha / 2.0), norm.ppf(1.0 - alpha / 2.0)])

    location_scale = mean + standard_deviation * z
    skew_cf = z + sample_skewness * (z**2 - 1.0) / 6.0
    four_moment_cf = (
        skew_cf
        + excess_kurtosis * (z**3 - 3.0 * z) / 24.0
        - sample_skewness**2 * (2.0 * z**3 - 5.0 * z) / 36.0
    )
    empirical = np.quantile(sample, [alpha / 2.0, 1.0 - alpha / 2.0])
    return {
        "location_scale": tuple(mean + standard_deviation * z),
        "cf_skew": tuple(mean + standard_deviation * skew_cf),
        "cf_four_moment": tuple(mean + standard_deviation * four_moment_cf),
        "empirical": tuple(empirical),
        "moments": (mean, standard_deviation, sample_skewness, excess_kurtosis),
    }


def _simulate(
    config,
    *,
    replicates: int,
    blocks: int,
    base_seed: int,
    stream: str,
    include_joint: bool,
) -> dict[str, np.ndarray]:
    if replicates < blocks or replicates % blocks != 0:
        raise ValueError("Replicates must be positive and divisible by blocks.")
    per_block = replicates // blocks
    pieces: dict[str, list[np.ndarray]] = {}

    for block in range(blocks):
        rng = np.random.default_rng(
            _seed(base_seed, stream, config.configuration_id, block)
        )
        table_p = rng.multinomial(
            config.n_p,
            config.pair.probability_p.reshape(-1),
            size=per_block,
        ).reshape(per_block, 2, 2)
        table_q = rng.multinomial(
            config.n_q,
            config.pair.probability_q.reshape(-1),
            size=per_block,
        ).reshape(per_block, 2, 2)
        base = differential_mi_pvalues(table_p, table_q)
        selected = {
            "statistic": base["statistic"],
            "base_valid": base["base_valid"],
            "normal_p_value": base["normal_p_value"],
            "simple_valid": base["simple_valid"],
            "simple_p_value": base["welch_p_value"],
            "expanded_valid": base["expanded_valid"],
            "expanded_p_value": base["expanded_welch_p_value"],
        }
        if include_joint:
            joint = joint_cornish_fisher_values(
                table_p,
                table_q,
                base_values=base,
            )
            selected.update(
                {
                    "joint_valid": joint["valid"],
                    "joint_rejected": joint["rejected"],
                    "joint_mean_shift": joint["mean_shift"],
                    "joint_skewness": joint["skewness"],
                    "joint_lower_critical": joint["lower_critical"],
                    "joint_upper_critical": joint["upper_critical"],
                }
            )
        for name, values in selected.items():
            pieces.setdefault(name, []).append(np.asarray(values))

    return {name: np.concatenate(values) for name, values in pieces.items()}


def _rate(rejected: np.ndarray, valid: np.ndarray) -> tuple[float, float, float, float]:
    usable = np.asarray(valid, dtype=bool)
    decisions = np.asarray(rejected, dtype=bool)
    valid_count = int(np.count_nonzero(usable))
    reject_count = int(np.count_nonzero(decisions & usable))
    low, high = _wilson(reject_count, valid_count)
    rate = reject_count / valid_count if valid_count else np.nan
    return rate, float(np.mean(usable)), low, high


def _constant_boundary_rate(
    statistic: np.ndarray,
    valid: np.ndarray,
    boundaries: tuple[float, float],
) -> tuple[float, float, float, float]:
    lower, upper = boundaries
    rejected = (statistic < lower) | (statistic > upper)
    return _rate(rejected, valid)


def summarize_configuration(config, anchor, development, validation) -> dict:
    development_valid = np.asarray(development["base_valid"], dtype=bool)
    development_statistic = np.asarray(development["statistic"], dtype=float)
    boundaries = cornish_fisher_boundaries(
        development_statistic[development_valid]
    )
    base_valid = np.asarray(validation["base_valid"], dtype=bool)
    statistic = np.asarray(validation["statistic"], dtype=float)
    population_joint = joint_cornish_fisher_parameters(
        config.pair.probability_p,
        config.pair.probability_q,
        config.n_p,
        config.n_q,
    )

    row = {
        "anchor_configuration_id": anchor.configuration_id,
        "configuration_label": CONFIGURATION_LABELS[anchor.configuration_id],
        "configuration_id": config.configuration_id,
        "sample_scale": config.n_p / anchor.n_p,
        "n_p": config.n_p,
        "n_q": config.n_q,
        "development_replicates": len(development_valid),
        "validation_replicates": len(base_valid),
    }
    methods = {
        "normal_wald": _rate(
            np.asarray(validation["normal_p_value"]) <= ALPHA,
            base_valid,
        ),
        "simple_welch": _rate(
            np.asarray(validation["simple_p_value"]) <= ALPHA,
            np.asarray(validation["simple_valid"], dtype=bool),
        ),
        "expanded_welch": _rate(
            np.asarray(validation["expanded_p_value"]) <= ALPHA,
            np.asarray(validation["expanded_valid"], dtype=bool),
        ),
        "plugin_joint_cf": _rate(
            np.asarray(validation["joint_rejected"], dtype=bool),
            np.asarray(validation["joint_valid"], dtype=bool),
        ),
        "population_joint_cf": _constant_boundary_rate(
            statistic,
            base_valid,
            (
                float(population_joint["lower_critical"]),
                float(population_joint["upper_critical"]),
            ),
        ),
    }
    for name in ("location_scale", "cf_skew", "cf_four_moment", "empirical"):
        methods[f"split_{name}"] = _constant_boundary_rate(
            statistic,
            base_valid,
            boundaries[name],
        )

    for method, (rate, valid_rate, low, high) in methods.items():
        row[f"{method}_rejection_rate"] = rate
        row[f"{method}_valid_rate"] = valid_rate
        row[f"{method}_wilson_low"] = low
        row[f"{method}_wilson_high"] = high
        row[f"{method}_absolute_error"] = abs(rate - ALPHA)

    mean, standard_deviation, sample_skewness, excess_kurtosis = boundaries["moments"]
    row.update(
        {
            "development_mean": mean,
            "development_sd": standard_deviation,
            "development_skewness": sample_skewness,
            "development_excess_kurtosis": excess_kurtosis,
            "plugin_joint_mean_shift_median": float(
                np.nanmedian(validation["joint_mean_shift"])
            ),
            "plugin_joint_skewness_median": float(
                np.nanmedian(validation["joint_skewness"])
            ),
            "population_joint_mean_shift": float(population_joint["mean_shift"]),
            "population_joint_skewness": float(population_joint["skewness"]),
            "population_joint_lower_critical": float(
                population_joint["lower_critical"]
            ),
            "population_joint_upper_critical": float(
                population_joint["upper_critical"]
            ),
        }
    )
    for name in ("location_scale", "cf_skew", "cf_four_moment", "empirical"):
        row[f"split_{name}_lower_critical"] = boundaries[name][0]
        row[f"split_{name}_upper_critical"] = boundaries[name][1]
    return row


METHOD_LABELS = {
    "normal_wald": "Normal Wald",
    "simple_welch": "Simple Welch",
    "expanded_welch": "Expanded Welch",
    "plugin_joint_cf": "Plug-in joint CF",
    "population_joint_cf": "Population-moment joint CF",
    "split_location_scale": "Split-sample location-scale",
    "split_cf_skew": "Split-sample CF (skew)",
    "split_cf_four_moment": "Split-sample CF (four moments)",
    "split_empirical": "Split-sample empirical threshold",
}


def method_summary(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method, label in METHOD_LABELS.items():
        errors = results[f"{method}_absolute_error"]
        rows.append(
            {
                "method": method,
                "method_label": label,
                "mean_absolute_fpr_error": float(errors.mean()),
                "median_absolute_fpr_error": float(errors.median()),
                "maximum_absolute_fpr_error": float(errors.max()),
                "configurations_within_0.01": int(np.count_nonzero(errors <= 0.01)),
                "configurations_within_0.02": int(np.count_nonzero(errors <= 0.02)),
                "mean_valid_rate": float(results[f"{method}_valid_rate"].mean()),
            }
        )
    return pd.DataFrame(rows)


def _plot_results(results: pd.DataFrame, output_path: Path) -> None:
    identifiers = list(CONFIGURATION_LABELS)
    labels = list(CONFIGURATION_LABELS.values())
    methods = (
        "normal_wald",
        "expanded_welch",
        "plugin_joint_cf",
        "population_joint_cf",
        "split_location_scale",
        "split_cf_four_moment",
        "split_empirical",
    )
    colors = (
        "#4477AA",
        "#AA3377",
        "#228833",
        "#66CCEE",
        "#CCBB44",
        "#EE7733",
        "#666666",
    )
    figure, axes = plt.subplots(3, 1, figsize=(17, 14), sharex=True)
    x = np.arange(len(identifiers))
    for axis, scale in zip(axes, SAMPLE_SCALES, strict=True):
        selected = results[np.isclose(results["sample_scale"], scale)]
        selected = selected.set_index("anchor_configuration_id").loc[identifiers]
        for method, color in zip(methods, colors, strict=True):
            axis.plot(
                x,
                selected[f"{method}_rejection_rate"],
                marker="o",
                linewidth=1.5,
                color=color,
                label=METHOD_LABELS[method],
            )
        axis.axhline(ALPHA, color="#111111", linestyle=":", linewidth=1.2)
        axis.set_title(f"Sample-size scale {scale:g}")
        axis.set_ylabel("False-positive rate")
        axis.grid(alpha=0.2)
    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels(labels, rotation=35, ha="right")
    handles, legend_labels = axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.985),
        ncol=4,
        frameon=False,
    )
    figure.suptitle("Joint Cornish-Fisher calibration audit", y=0.998)
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--blocks", type=int, default=DEFAULT_BLOCKS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    anchors, configurations = audit_configurations()
    anchor_by_id = {anchor.configuration_id: anchor for anchor in anchors}
    start = perf_counter()
    rows = []
    for index, config in enumerate(configurations, start=1):
        development = _simulate(
            config,
            replicates=args.replicates,
            blocks=args.blocks,
            base_seed=args.seed,
            stream="joint_cf_development",
            include_joint=False,
        )
        validation = _simulate(
            config,
            replicates=args.replicates,
            blocks=args.blocks,
            base_seed=args.seed,
            stream="joint_cf_validation",
            include_joint=True,
        )
        rows.append(
            summarize_configuration(
                config,
                anchor_by_id[config.power_family],
                development,
                validation,
            )
        )
        print(f"Joint-CF configurations: {index}/{len(configurations)}", flush=True)

    results = pd.DataFrame(rows)
    methods = method_summary(results)
    results.to_csv(args.output_dir / "configuration_results.csv", index=False)
    methods.to_csv(args.output_dir / "method_summary.csv", index=False)
    results[np.isclose(results["sample_scale"], 1.0)].to_csv(
        args.output_dir / "baseline_results.csv",
        index=False,
    )
    _plot_results(results, args.output_dir / "JOINT_CF_AUDIT.png")

    metadata = {
        "seed": args.seed,
        "development_replicates_per_configuration": args.replicates,
        "validation_replicates_per_configuration": args.replicates,
        "blocks": args.blocks,
        "configurations": len(configurations),
        "alpha": ALPHA,
        "elapsed_seconds": perf_counter() - start,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(methods.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
