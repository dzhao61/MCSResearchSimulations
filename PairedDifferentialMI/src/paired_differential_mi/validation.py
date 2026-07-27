"""Simulation, summaries, and reporting for the paired feasibility pilot."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from .core import P_VALUE_COLUMNS, paired_bootstrap_t, paired_mi_tests
from .distributions import PairedScenario


def _interval(rejections: int, total: int) -> tuple[float, float]:
    if total == 0:
        return float("nan"), float("nan")
    result = binomtest(rejections, total).proportion_ci(method="wilson")
    return float(result.low), float(result.high)


def run_scenario(
    scenario: PairedScenario,
    *,
    replicates: int,
    seed: int,
) -> tuple[pd.DataFrame, dict]:
    """Run repeated samples from one exact paired population."""
    _, _, coupling, diagnostics = scenario.materialize()
    rng = np.random.default_rng(seed)
    cells = scenario.rows * scenario.columns
    paired_counts = rng.multinomial(
        scenario.n, coupling.reshape(-1), size=replicates
    ).reshape(replicates, cells, cells)
    start = perf_counter()
    result = paired_mi_tests(
        paired_counts,
        (scenario.rows, scenario.columns),
    )
    elapsed = perf_counter() - start
    frame = pd.DataFrame(result)
    frame.insert(0, "replicate", np.arange(replicates))
    frame.insert(0, "scenario_id", scenario.scenario_id)
    frame["regime"] = scenario.regime
    frame["true_delta"] = diagnostics["true_delta"]
    frame["zero_fraction_a"] = np.mean(
        paired_counts.sum(axis=2) == 0, axis=1
    )
    frame["zero_fraction_b"] = np.mean(
        paired_counts.sum(axis=1) == 0, axis=1
    )
    diagnostics["replicates"] = replicates
    diagnostics["scenario_seed"] = seed
    diagnostics["simulation_and_test_seconds"] = elapsed
    diagnostics["mean_test_microseconds"] = 1e6 * elapsed / replicates
    return frame, diagnostics


def summarize(
    replicates: pd.DataFrame, scenarios: pd.DataFrame
) -> pd.DataFrame:
    rows: list[dict] = []
    scenario_lookup = scenarios.set_index("scenario_id")
    for scenario_id, group in replicates.groupby("scenario_id", sort=False):
        metadata = scenario_lookup.loc[scenario_id]
        row = {
            "scenario_id": scenario_id,
            "regime": group["regime"].iloc[0],
            "replicates": len(group),
            "n": int(metadata["n"]),
            "rows": int(metadata["rows"]),
            "columns": int(metadata["columns"]),
            "true_delta": float(group["true_delta"].iloc[0]),
            "population_score_correlation": float(
                metadata["population_score_correlation"]
            ),
            "min_expected_joint": float(
                min(
                    metadata["min_expected_joint_a"],
                    metadata["min_expected_joint_b"],
                )
            ),
            "expected_joint_below_1": float(
                max(
                    metadata["expected_joint_below_1_a"],
                    metadata["expected_joint_below_1_b"],
                )
            ),
            "mean_zero_fraction": float(
                max(
                    group["zero_fraction_a"].mean(),
                    group["zero_fraction_b"].mean(),
                )
            ),
            "paired_wald_valid_rate": float(group["valid_paired_wald"].mean()),
            "jackknife_valid_rate": float(group["valid_jackknife"].mean()),
            "mean_delta_plugin_bias": float(
                (group["delta_plugin"] - group["true_delta"]).mean()
            ),
            "mean_delta_jackknife_bias": float(
                (group["jackknife_delta"] - group["true_delta"]).mean()
            ),
            "mean_paired_se": float(group["paired_standard_error"].mean()),
            "mean_unpaired_se": float(group["unpaired_standard_error"].mean()),
            "mean_se_ratio_paired_to_unpaired": float(
                np.nanmean(
                    group["paired_standard_error"]
                    / group["unpaired_standard_error"]
                )
            ),
            "mean_test_microseconds": float(metadata["mean_test_microseconds"]),
        }
        for column in P_VALUE_COLUMNS:
            valid = group[column].dropna()
            method = column.removesuffix("_p")
            for alpha in (0.10, 0.05):
                suffix = f"{int(100 * alpha):02d}"
                rejections = int(np.count_nonzero(valid <= alpha))
                low, high = _interval(rejections, len(valid))
                row[f"{method}_reject_{suffix}"] = (
                    rejections / len(valid) if len(valid) else float("nan")
                )
                row[f"{method}_reject_{suffix}_low"] = low
                row[f"{method}_reject_{suffix}_high"] = high
        rows.append(row)
    return pd.DataFrame(rows)


def run_bootstrap_anchors(
    scenarios: list[PairedScenario],
    *,
    tables_per_scenario: int,
    bootstrap_replicates: int,
    seed: int,
) -> pd.DataFrame:
    """Compare analytic and bootstrap p-values on selected null tables."""
    rng = np.random.default_rng(seed)
    rows: list[dict] = []
    for scenario in scenarios:
        _, _, coupling, diagnostics = scenario.materialize()
        cells = scenario.rows * scenario.columns
        tables = rng.multinomial(
            scenario.n,
            coupling.reshape(-1),
            size=tables_per_scenario,
        ).reshape(tables_per_scenario, cells, cells)
        for table_index, counts in enumerate(tables):
            analytic_start = perf_counter()
            analytic = paired_mi_tests(
                counts, (scenario.rows, scenario.columns)
            )
            analytic_seconds = perf_counter() - analytic_start
            bootstrap = paired_bootstrap_t(
                counts,
                (scenario.rows, scenario.columns),
                replicates=bootstrap_replicates,
                rng=rng,
            )
            rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "regime": scenario.regime,
                    "table_index": table_index,
                    "true_delta": diagnostics["true_delta"],
                    "paired_wald_normal_p": analytic["paired_wald_normal_p"],
                    "paired_wald_t_p": analytic["paired_wald_t_p"],
                    "paired_jackknife_t_p": analytic["paired_jackknife_t_p"],
                    "bootstrap_t_p": bootstrap.p_value,
                    "analytic_seconds": analytic_seconds,
                    "bootstrap_seconds": bootstrap.elapsed_seconds,
                    "bootstrap_valid_replicates": bootstrap.valid_replicates,
                    "bootstrap_requested_replicates": bootstrap_replicates,
                }
            )
    return pd.DataFrame(rows)


def _method_regime_summary(summary: pd.DataFrame) -> pd.DataFrame:
    null = summary[summary["regime"] != "power"].copy()
    rows: list[dict] = []
    for regime, group in null.groupby("regime", sort=False):
        for method in P_VALUE_COLUMNS:
            prefix = method.removesuffix("_p")
            rate = group[f"{prefix}_reject_05"]
            rows.append(
                {
                    "regime": regime,
                    "method": prefix,
                    "scenarios": len(group),
                    "mean_rejection_05": float(rate.mean()),
                    "mean_absolute_fpr_error_05": float(
                        np.abs(rate - 0.05).mean()
                    ),
                    "scenarios_in_035_065": float(
                        np.mean((rate >= 0.035) & (rate <= 0.065))
                    ),
                    "min_rejection_05": float(rate.min()),
                    "max_rejection_05": float(rate.max()),
                }
            )
    return pd.DataFrame(rows)


def write_report(
    output_dir: Path,
    summary: pd.DataFrame,
    method_summary: pd.DataFrame,
    bootstrap: pd.DataFrame,
) -> None:
    regular = method_summary[method_summary["regime"] == "regular"]
    sparse = method_summary[method_summary["regime"] == "sparse"]
    power = summary[summary["regime"] == "power"]
    bootstrap_speedup = (
        bootstrap["bootstrap_seconds"] / bootstrap["analytic_seconds"]
        if not bootstrap.empty
        else pd.Series(dtype=float)
    )

    def markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
        """Render a compact table without pandas' optional tabulate dependency."""
        header = "| " + " | ".join(columns) + " |"
        divider = "| " + " | ".join("---" for _ in columns) + " |"
        body = []
        for record in frame[columns].to_dict(orient="records"):
            values = []
            for column in columns:
                value = record[column]
                values.append(f"{value:.4f}" if isinstance(value, float) else str(value))
            body.append("| " + " | ".join(values) + " |")
        return "\n".join([header, divider, *body])

    def method_table(frame: pd.DataFrame) -> str:
        columns = [
            "method",
            "mean_absolute_fpr_error_05",
            "scenarios_in_035_065",
            "min_rejection_05",
            "max_rejection_05",
        ]
        return markdown_table(frame, columns)

    primary_regular = regular.loc[
        regular["method"] == "paired_jackknife_t"
    ].iloc[0]
    rule_1 = bool(
        primary_regular["mean_absolute_fpr_error_05"] <= 0.01
        and primary_regular["scenarios_in_035_065"] >= 0.80
    )
    sparse_wald = float(
        sparse.loc[
            sparse["method"] == "paired_wald_normal",
            "mean_absolute_fpr_error_05",
        ].iloc[0]
    )
    sparse_jackknife = float(
        sparse.loc[
            sparse["method"] == "paired_jackknife_t",
            "mean_absolute_fpr_error_05",
        ].iloc[0]
    )
    rule_3 = bool(
        sparse_jackknife <= 0.8 * sparse_wald
        or (sparse_wald <= 0.01 and sparse_jackknife <= sparse_wald + 0.005)
    )
    runtime_rule = bool(
        not bootstrap_speedup.empty
        and bootstrap_speedup.median() >= 10
        and summary["mean_test_microseconds"].median() < 1000
    )
    bootstrap_count = (
        int(bootstrap["bootstrap_requested_replicates"].iloc[0])
        if not bootstrap.empty
        else 0
    )
    decision = "PROCEED" if rule_1 else "NO-GO IN CURRENT FORM"

    lines = [
        "# Paired Differential-MI Feasibility Results",
        "",
        f"## Decision: **{decision}**",
        "",
        "The decision applies to the positive-MI paired weak-null direction. "
        "Boundary scenarios remain outside the supported scope.",
        "",
        "## Regular Positive-MI Calibration",
        "",
        method_table(regular),
        "",
        "## Sparse Calibration",
        "",
        method_table(sparse),
        "",
        "## Power Controls",
        "",
        markdown_table(
            power,
            [
                "scenario_id",
                "true_delta",
                "paired_wald_normal_reject_05",
                "paired_wald_t_reject_05",
                "paired_jackknife_t_reject_05",
            ],
        ),
        "",
        "## Bootstrap Anchors",
        "",
        (
            f"- Median deterministic latency: "
            f"`{1000 * bootstrap['analytic_seconds'].median():.3f} ms`."
            if not bootstrap.empty
            else "- Bootstrap anchors were not run."
        ),
        (
            f"- Median {bootstrap_count}-bootstrap latency: "
            f"`{bootstrap['bootstrap_seconds'].median():.3f} s`."
            if not bootstrap.empty
            else ""
        ),
        (
            f"- Median measured speedup: `{bootstrap_speedup.median():.1f}x`."
            if not bootstrap.empty
            else ""
        ),
        (
            f"- Median absolute jackknife-t versus bootstrap p-value "
            f"difference: "
            f"`{np.median(np.abs(bootstrap['paired_jackknife_t_p'] - bootstrap['bootstrap_t_p'])):.4f}`."
            if not bootstrap.empty
            else ""
        ),
        "",
        "## Pre-Specified Rules",
        "",
        f"- Rule 1, regular calibration: **{'PASS' if rule_1 else 'FAIL'}**.",
        f"- Rule 3, sparse refinement value: **{'PASS' if rule_3 else 'FAIL'}**.",
        f"- Rule 5, runtime: **{'PASS' if runtime_rule else 'FAIL'}**.",
        "",
        "Rules concerning pairing signs and the boundary are interpreted from "
        "the scenario-level table rather than reduced to one scalar.",
        "",
        "## Important Limits",
        "",
        "- Repeated simulation from the known paired population is the "
        "calibration truth; bootstrap agreement alone is not treated as proof.",
        "- The unpaired calculation is a diagnostic, not a valid competitor.",
        "- Exact and near independence are nonregular and remain outside the "
        "method claim.",
        "- This pilot establishes plausibility, not novelty or publication-ready "
        "validation.",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n")


def save_results(
    output_dir: Path,
    replicates: pd.DataFrame,
    scenarios: pd.DataFrame,
    summary: pd.DataFrame,
    bootstrap: pd.DataFrame,
    metadata: dict,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    method_summary = _method_regime_summary(summary)
    replicates.to_csv(output_dir / "replicates.csv.gz", index=False)
    scenarios.to_csv(output_dir / "scenarios.csv", index=False)
    summary.to_csv(output_dir / "summary.csv", index=False)
    method_summary.to_csv(output_dir / "method_summary.csv", index=False)
    bootstrap.to_csv(output_dir / "bootstrap_anchors.csv", index=False)
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    write_report(output_dir, summary, method_summary, bootstrap)
