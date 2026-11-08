#!/usr/bin/env python3
"""Diagnose why the differential-MI Wald statistic is miscalibrated."""

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
from scipy.optimize import brentq
from scipy.stats import kurtosis, norm, skew, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from run_2x2_experiment import _wilson, simulate_configuration  # noqa: E402
from run_2x2_power_curves import (  # noqa: E402
    CONFIGURATION_LABELS,
    SAMPLE_SCALES,
    build_curve_configurations,
    selected_anchor_configurations,
)


ALPHA = 0.05
DEFAULT_REPLICATES = 200_000
DEFAULT_BLOCKS = 10
DEFAULT_SEED = 2_026_082_501
SCALE_COLORS = {
    0.5: "#4477AA",
    1.0: "#CC6677",
    2.0: "#228833",
}


def audit_configurations():
    """Return the 13 selected null cases at three sample-size scales."""
    anchors = selected_anchor_configurations()
    return anchors, build_curve_configurations(
        anchors,
        effects=(0.0,),
        sample_scales=SAMPLE_SCALES,
    )


def implied_t_degrees_of_freedom(
    critical_value: float,
    *,
    alpha: float = ALPHA,
) -> float:
    """Find the constant Student df matching a two-sided critical value."""
    normal_critical = float(norm.ppf(1.0 - alpha / 2.0))
    if not np.isfinite(critical_value) or critical_value <= normal_critical:
        return np.nan

    def objective(degrees_of_freedom: float) -> float:
        return float(t.ppf(1.0 - alpha / 2.0, degrees_of_freedom) - critical_value)

    return float(brentq(objective, 0.05, 1e8, xtol=1e-10, rtol=1e-10))


def _correlation(x: np.ndarray, y: np.ndarray) -> float:
    usable = np.isfinite(x) & np.isfinite(y)
    if np.count_nonzero(usable) < 3:
        return np.nan
    x_usable = x[usable]
    y_usable = y[usable]
    if np.std(x_usable) == 0.0 or np.std(y_usable) == 0.0:
        return np.nan
    return float(np.corrcoef(x_usable, y_usable)[0, 1])


def _calibration_requirement(
    rejection_count: int,
    valid_count: int,
    *,
    alpha: float = ALPHA,
) -> tuple[str, float, float]:
    low, high = _wilson(rejection_count, valid_count)
    if low > alpha:
        requirement = "larger_than_normal_critical_value"
    elif high < alpha:
        requirement = "smaller_than_normal_critical_value"
    else:
        requirement = "normal_critical_value_adequate"
    return requirement, low, high


def summarize_configuration(config, anchor, values: dict[str, np.ndarray]) -> dict:
    base_valid = np.asarray(values["base_valid"], dtype=bool)
    delta = np.asarray(values["delta_corrected"], dtype=float)[base_valid]
    standard_error = np.asarray(values["standard_error"], dtype=float)[base_valid]
    statistic = np.asarray(values["statistic"], dtype=float)[base_valid]

    valid_count = int(statistic.size)
    normal_reject_count = int(np.count_nonzero(np.abs(statistic) >= norm.ppf(0.975)))
    requirement, normal_low, normal_high = _calibration_requirement(
        normal_reject_count,
        valid_count,
    )

    mean_delta = float(np.mean(delta))
    sd_delta = float(np.std(delta, ddof=1))
    mean_statistic = float(np.mean(statistic))
    sd_statistic = float(np.std(statistic, ddof=1))
    mean_standard_error = float(np.mean(standard_error))
    rms_standard_error = float(np.sqrt(np.mean(standard_error**2)))
    empirical_critical = float(np.quantile(np.abs(statistic), 1.0 - ALPHA))

    centered_statistic = (delta - mean_delta) / standard_error
    oracle_standardized_delta = (delta - mean_delta) / sd_delta
    location_scale_corrected_statistic = (
        statistic - mean_statistic
    ) / sd_statistic

    simple_valid = np.asarray(values["simple_valid"], dtype=bool)
    expanded_valid = np.asarray(values["expanded_valid"], dtype=bool)
    simple_p = np.asarray(values["welch_p_value"], dtype=float)
    expanded_p = np.asarray(values["expanded_welch_p_value"], dtype=float)
    expanded_df = np.asarray(
        values["expanded_welch_degrees_of_freedom"],
        dtype=float,
    )
    usable_expanded_df = expanded_df[expanded_valid & np.isfinite(expanded_df)]
    expanded_critical_values = t.ppf(0.975, usable_expanded_df)

    return {
        "anchor_configuration_id": anchor.configuration_id,
        "configuration_label": CONFIGURATION_LABELS[anchor.configuration_id],
        "configuration_id": config.configuration_id,
        "sample_scale": config.n_p / anchor.n_p,
        "n_p": config.n_p,
        "n_q": config.n_q,
        "replicates": len(base_valid),
        "base_valid_rate": float(np.mean(base_valid)),
        "expanded_valid_rate": float(np.mean(expanded_valid)),
        "normal_critical_value": float(norm.ppf(0.975)),
        "empirical_critical_value": empirical_critical,
        "implied_constant_t_df": implied_t_degrees_of_freedom(empirical_critical),
        "calibration_requirement": requirement,
        "normal_rejection_rate": normal_reject_count / valid_count,
        "normal_rejection_wilson_low": normal_low,
        "normal_rejection_wilson_high": normal_high,
        "simple_welch_rejection_rate": float(np.mean(simple_p[simple_valid] <= ALPHA)),
        "expanded_welch_rejection_rate": float(
            np.mean(expanded_p[expanded_valid] <= ALPHA)
        ),
        "expanded_df_median": float(np.median(usable_expanded_df)),
        "expanded_critical_median": float(np.median(expanded_critical_values)),
        "mean_delta_corrected": mean_delta,
        "sd_delta_corrected": sd_delta,
        "bias_in_sd_units": mean_delta / sd_delta,
        "mean_standard_error": mean_standard_error,
        "rms_standard_error": rms_standard_error,
        "sd_to_rms_se_ratio": sd_delta / rms_standard_error,
        "mean_statistic": mean_statistic,
        "sd_statistic": sd_statistic,
        "statistic_skewness": float(skew(statistic, bias=False)),
        "statistic_excess_kurtosis": float(kurtosis(statistic, fisher=True, bias=False)),
        "centered_studentized_critical_value": float(
            np.quantile(np.abs(centered_statistic), 1.0 - ALPHA)
        ),
        "oracle_shape_critical_value": float(
            np.quantile(np.abs(oracle_standardized_delta), 1.0 - ALPHA)
        ),
        "location_scale_corrected_statistic_critical_value": float(
            np.quantile(
                np.abs(location_scale_corrected_statistic),
                1.0 - ALPHA,
            )
        ),
        "statistic_lower_025_quantile": float(np.quantile(statistic, 0.025)),
        "statistic_upper_975_quantile": float(np.quantile(statistic, 0.975)),
        "delta_se_correlation": _correlation(delta, standard_error),
        "absolute_delta_se_correlation": _correlation(
            np.abs(delta),
            standard_error,
        ),
    }


def _plot_audit(summary: pd.DataFrame, output_path: Path) -> None:
    labels = list(CONFIGURATION_LABELS.values())
    identifiers = list(CONFIGURATION_LABELS)
    x = np.arange(len(labels))
    figure, axes = plt.subplots(2, 2, figsize=(18, 11), sharex=True)

    panels = (
        ("empirical_critical_value", "Empirical 5% critical value", norm.ppf(0.975)),
        ("normal_rejection_rate", "Wald false-positive rate", ALPHA),
        ("sd_to_rms_se_ratio", r"Empirical SD / RMS estimated SE", 1.0),
        (
            "location_scale_corrected_statistic_critical_value",
            "Critical value after recentering and rescaling T",
            norm.ppf(0.975),
        ),
    )
    for axis, (column, title, reference) in zip(axes.ravel(), panels, strict=True):
        for sample_scale in SAMPLE_SCALES:
            selected = summary[np.isclose(summary["sample_scale"], sample_scale)]
            selected = selected.set_index("anchor_configuration_id").loc[identifiers]
            axis.plot(
                x,
                selected[column],
                marker="o",
                linewidth=1.7,
                color=SCALE_COLORS[sample_scale],
                label=f"sample scale {sample_scale:g}",
            )
        axis.axhline(reference, color="#555555", linestyle=":", linewidth=1.2)
        axis.set_title(title)
        axis.grid(alpha=0.2)

    for axis in axes[-1, :]:
        axis.set_xticks(x)
        axis.set_xticklabels(labels, rotation=38, ha="right")
    handles, legend_labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=3,
        frameon=False,
    )
    figure.suptitle("Why the differential-MI Wald statistic is miscalibrated", y=0.995)
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def _script_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--blocks", type=int, default=DEFAULT_BLOCKS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.replicates % args.blocks != 0:
        raise ValueError("Replicates must be divisible by blocks.")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    anchors, configurations = audit_configurations()
    anchor_by_id = {anchor.configuration_id: anchor for anchor in anchors}
    start = perf_counter()
    rows = []
    for index, config in enumerate(configurations, start=1):
        values, _, _ = simulate_configuration(
            config,
            replicates=args.replicates,
            blocks=args.blocks,
            base_seed=args.seed,
            stream="critical_value_audit",
        )
        rows.append(
            summarize_configuration(
                config,
                anchor_by_id[config.power_family],
                values,
            )
        )
        print(f"Critical-value configurations: {index}/{len(configurations)}", flush=True)

    summary = pd.DataFrame(rows)
    summary.to_csv(args.output_dir / "critical_value_audit.csv", index=False)
    summary[np.isclose(summary["sample_scale"], 1.0)].to_csv(
        args.output_dir / "baseline_critical_value_audit.csv",
        index=False,
    )
    _plot_audit(summary, args.output_dir / "CRITICAL_VALUE_AUDIT.png")

    metadata = {
        "seed": args.seed,
        "replicates_per_configuration": args.replicates,
        "blocks": args.blocks,
        "configurations": len(configurations),
        "sample_scales": list(SAMPLE_SCALES),
        "alpha": ALPHA,
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
