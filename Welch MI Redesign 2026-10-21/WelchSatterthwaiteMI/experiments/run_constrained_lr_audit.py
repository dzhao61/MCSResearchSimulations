#!/usr/bin/env python3
"""Audit a constrained likelihood-ratio test for equality of two discrete MIs."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
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
    selected_anchor_configurations,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402
from welch_differential_mi.likelihood_ratio import (  # noqa: E402
    constrained_likelihood_ratio_test,
)


ALPHAS = (0.10, 0.05, 0.01)
SAMPLE_SCALES = (0.5, 1.0, 2.0)
METHOD_LABELS = {
    "normal_wald": "Normal Wald",
    "simple_welch": "Simple Welch",
    "expanded_welch": "Expanded Welch",
    "constrained_lr": "Constrained LR (chi-squared)",
}
PROFILE_SETTINGS = {
    "smoke": {"replicates": 100, "scales": (1.0,)},
    "screen": {"replicates": 2_000, "scales": (1.0,)},
    "confirmatory": {
        "replicates": 5_000,
        "scales": SAMPLE_SCALES,
    },
}


def build_configurations(scales: tuple[float, ...]) -> list[Configuration]:
    configurations: list[Configuration] = []
    for anchor in selected_anchor_configurations():
        for scale in scales:
            n_p = max(2, int(round(anchor.n_p * scale)))
            n_q = max(2, int(round(anchor.n_q * scale)))
            configurations.append(
                replace(
                    anchor,
                    configuration_id=f"LR_{anchor.configuration_id}_scale{scale:g}",
                    experiment="CONSTRAINED_LR",
                    n_p=n_p,
                    n_q=n_q,
                    power_family=anchor.configuration_id,
                )
            )
    return configurations


def _simulate_tables(
    config: Configuration, replicates: int, seed: int, stream: str
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(_seed(seed, stream, config.configuration_id))
    table_p = rng.multinomial(
        config.n_p, config.pair.probability_p.reshape(-1), size=replicates
    ).reshape(replicates, 2, 2)
    table_q = rng.multinomial(
        config.n_q, config.pair.probability_q.reshape(-1), size=replicates
    ).reshape(replicates, 2, 2)
    return table_p, table_q


def _fit_lr_batch(
    table_p: np.ndarray, table_q: np.ndarray
) -> tuple[np.ndarray, dict[str, float]]:
    statistics = np.full(len(table_p), np.nan)
    residuals = np.full(len(table_p), np.nan)
    elapsed = np.full(len(table_p), np.nan)
    iterations = np.full(len(table_p), np.nan)
    retries = 0
    audit_differences: list[float] = []

    for index, (counts_p, counts_q) in enumerate(zip(table_p, table_q, strict=True)):
        result = constrained_likelihood_ratio_test(counts_p, counts_q)
        if not result.converged:
            retries += 1
        if result.converged:
            statistics[index] = result.statistic
            residuals[index] = result.constraint_residual
            elapsed[index] = result.elapsed_seconds
            iterations[index] = result.iterations

        if index % 200 == 0 and result.converged:
            repeated = constrained_likelihood_ratio_test(counts_p, counts_q)
            if repeated.converged:
                audit_differences.append(abs(result.statistic - repeated.statistic))

    valid = np.isfinite(statistics)
    diagnostics = {
        "lr_valid_count": int(np.count_nonzero(valid)),
        "lr_valid_rate": float(np.mean(valid)),
        "lr_retry_count": retries,
        "lr_median_elapsed_ms": float(np.nanmedian(elapsed) * 1_000.0),
        "lr_p99_elapsed_ms": float(np.nanquantile(elapsed, 0.99) * 1_000.0),
        "lr_max_constraint_residual": float(np.nanmax(residuals)),
        "lr_median_iterations": float(np.nanmedian(iterations)),
        "lr_full_start_audit_count": len(audit_differences),
        "lr_full_start_max_statistic_difference": (
            max(audit_differences) if audit_differences else np.nan
        ),
    }
    return statistics, diagnostics


def _row(
    config: Configuration,
    method: str,
    alpha: float,
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
        "sample_scale": config.n_p
        / selected_anchor_configurations_by_id()[config.power_family].n_p,
        "n_p": config.n_p,
        "n_q": config.n_q,
        "mi_p": config.pair.mi_p,
        "mi_q": config.pair.mi_q,
        "minimum_expected_count": min(
            config.n_p * float(np.min(config.pair.probability_p)),
            config.n_q * float(np.min(config.pair.probability_q)),
        ),
        "method": method,
        "method_label": METHOD_LABELS[method],
        "alpha": alpha,
        "replicates": len(valid),
        "valid_count": valid_count,
        "valid_rate": valid_count / len(valid),
        "reject_count": reject_count,
        "false_positive_rate": rate,
        "absolute_fpr_error": abs(rate - alpha),
        "wilson_low": low,
        "wilson_high": high,
    }


def selected_anchor_configurations_by_id() -> dict[str, Configuration]:
    return {config.configuration_id: config for config in selected_anchor_configurations()}


def _run_configuration(task: tuple[Configuration, int, int]) -> dict:
    config, replicates, seed = task
    start = perf_counter()
    validation_p, validation_q = _simulate_tables(
        config, replicates, seed, "validation"
    )
    validation_lr, validation_diagnostics = _fit_lr_batch(validation_p, validation_q)
    validation_values = differential_mi_pvalues(validation_p, validation_q)

    rows: list[dict] = []

    for alpha in ALPHAS:
        chi_threshold = float(chi2.ppf(1.0 - alpha, df=1))
        for method, specification in METHODS.items():
            valid = np.asarray(validation_values[specification["valid"]], dtype=bool)
            p_values = np.asarray(
                validation_values[specification["p_value"]], dtype=float
            )
            rows.append(_row(config, method, alpha, p_values <= alpha, valid))

        valid_lr = np.isfinite(validation_lr)
        rows.append(
            _row(
                config,
                "constrained_lr",
                alpha,
                validation_lr >= chi_threshold,
                valid_lr,
            )
        )

    diagnostics = {
        "configuration_id": config.configuration_id,
        "configuration_label": CONFIGURATION_LABELS[config.power_family],
        "n_p": config.n_p,
        "n_q": config.n_q,
        "wall_seconds": perf_counter() - start,
        **{f"validation_{key}": value for key, value in validation_diagnostics.items()},
    }
    return {"rows": rows, "diagnostics": diagnostics}


def _summarize(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (method, alpha), group in results.groupby(["method", "alpha"], sort=False):
        errors = group["absolute_fpr_error"].to_numpy()
        rows.append(
            {
                "method": method,
                "method_label": METHOD_LABELS[method],
                "alpha": alpha,
                "configurations": len(group),
                "mean_absolute_fpr_error": float(np.mean(errors)),
                "median_absolute_fpr_error": float(np.median(errors)),
                "maximum_absolute_fpr_error": float(np.max(errors)),
                "mean_fpr": float(group["false_positive_rate"].mean()),
                "minimum_valid_rate": float(group["valid_rate"].min()),
            }
        )
    return pd.DataFrame(rows)


def _plot(results: pd.DataFrame, output_dir: Path) -> None:
    selected = results[np.isclose(results["alpha"], 0.05)].copy()
    methods = ("normal_wald", "expanded_welch", "constrained_lr")
    figure, axis = plt.subplots(figsize=(10.5, 6.0))
    x = np.arange(len(selected["configuration_id"].unique()))
    width = 0.19
    for offset, method in enumerate(methods):
        method_rows = selected[selected["method"].eq(method)].sort_values(
            ["sample_scale", "anchor_configuration_id"]
        )
        axis.bar(
            x + (offset - 1.5) * width,
            method_rows["absolute_fpr_error"],
            width=width,
            label=METHOD_LABELS[method],
        )
    axis.set_ylabel(r"Absolute FPR error at $\alpha=0.05$")
    axis.set_xlabel("Fixed 2x2 configurations")
    axis.set_xticks([])
    axis.grid(axis="y", alpha=0.2)
    axis.legend(frameon=False, ncol=2)
    figure.tight_layout()
    figure.savefig(output_dir / "CALIBRATION_ERROR.png", dpi=180)
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile", choices=tuple(PROFILE_SETTINGS), default="screen"
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2_026_082_601)
    parser.add_argument("--replicates", type=int)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT
        / "results"
        / "2x2_constrained_lr_confirmatory_fullstarts",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = PROFILE_SETTINGS[args.profile]
    replicates = args.replicates or settings["replicates"]
    configurations = build_configurations(settings["scales"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = perf_counter()

    tasks = [(config, replicates, args.seed) for config in configurations]
    completed = []
    if args.workers == 1:
        completed = [_run_configuration(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_run_configuration, task) for task in tasks]
            for future in as_completed(futures):
                completed.append(future.result())

    result_rows = [row for result in completed for row in result["rows"]]
    diagnostic_rows = [result["diagnostics"] for result in completed]
    results = pd.DataFrame(result_rows).sort_values(
        ["sample_scale", "anchor_configuration_id", "alpha", "method"]
    )
    diagnostics = pd.DataFrame(diagnostic_rows).sort_values("configuration_id")
    summary = _summarize(results)
    results.to_csv(args.output_dir / "configuration_results.csv", index=False)
    diagnostics.to_csv(args.output_dir / "optimizer_diagnostics.csv", index=False)
    summary.to_csv(args.output_dir / "method_summary.csv", index=False)
    _plot(results, args.output_dir)

    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "replicates_per_configuration": replicates,
        "configuration_count": len(configurations),
        "workers": args.workers,
        "elapsed_seconds": perf_counter() - started,
        "python": platform.python_version(),
        "candidate": "constrained multinomial LR for I(P)=I(Q)",
        "candidate_reference": "chi-squared with one degree of freedom",
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(f"Elapsed: {metadata['elapsed_seconds']:.1f} seconds")


if __name__ == "__main__":
    main()
