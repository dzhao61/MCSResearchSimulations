#!/usr/bin/env python3
"""Independently audit the frozen influence-df validation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


METHODS = ("wald_normal", "welch_n_minus_1", "if_satterthwaite")
EXPECTED_STAGE_ROWS = {"broad": 144, "hard": 12, "strong": 144, "stress": 26}
EXPECTED_REPLICATES = {
    "broad": 5_000,
    "hard": 20_000,
    "strong": 5_000,
    "stress": 10_000,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def _mi(probability: np.ndarray) -> float:
    row = probability.sum(axis=1, keepdims=True)
    column = probability.sum(axis=0, keepdims=True)
    denominator = row * column
    mask = probability > 0
    return float(
        np.sum(
            probability[mask]
            * np.log(probability[mask] / denominator[mask])
        )
    )


def _close(actual: float, expected: float, tolerance: float = 1e-12) -> bool:
    return bool(np.isfinite(actual) and abs(actual - expected) <= tolerance)


def main() -> None:
    args = parse_args()
    results = args.results_dir
    scenario = pd.read_csv(results / "scenario_summary.csv")
    populations = pd.read_csv(results / "scenarios.csv")
    aggregate = pd.read_csv(results / "method_summary.csv")
    power = pd.read_csv(results / "power_summary.csv")
    runtime = pd.read_csv(results / "runtime_summary.csv")
    df_audit = pd.read_csv(results / "df_audit.csv")
    metadata = json.loads((results / "run_metadata.json").read_text())

    checks: dict[str, bool] = {}
    checks["scenario_row_counts"] = (
        scenario.groupby("stage").size().to_dict() == EXPECTED_STAGE_ROWS
    )
    checks["replicate_counts"] = all(
        np.all(
            scenario.loc[scenario["stage"].eq(stage), "replicates"]
            == expected
        )
        for stage, expected in EXPECTED_REPLICATES.items()
    )
    checks["scenario_keys_unique"] = not scenario["scenario_key"].duplicated().any()
    checks["simulation_seeds_unique"] = not scenario[
        "simulation_seed"
    ].duplicated().any()
    checks["power_seeds_disjoint"] = set(
        power["simulation_seed"].unique()
    ).isdisjoint(set(scenario["simulation_seed"]))
    checks["all_null_deltas_numerically_zero"] = (
        float(np.max(np.abs(scenario["true_delta"]))) < 2e-12
    )
    checks["regular_stage_valid_rates"] = all(
        float(
            scenario.loc[scenario["stage"].eq(stage), "valid_n"].sum()
            / scenario.loc[scenario["stage"].eq(stage), "replicates"].sum()
        )
        >= 0.995
        for stage in ("broad", "hard", "strong")
    )

    rate_checks = []
    for method in METHODS:
        for label, alpha in (("10", 0.10), ("05", 0.05)):
            rate = scenario[f"{method}_fpr_{label}"]
            low = scenario[f"{method}_fpr_{label}_low"]
            high = scenario[f"{method}_fpr_{label}_high"]
            error = scenario[f"{method}_error_{label}"]
            rejection_count = rate * scenario["valid_n"]
            rate_checks.extend(
                [
                    bool(rate.between(0.0, 1.0).all()),
                    bool((np.abs(rejection_count - np.round(rejection_count)) < 1e-7).all()),
                    bool(((low <= rate) & (rate <= high)).all()),
                    bool(
                        np.allclose(
                            error,
                            np.abs(rate - alpha),
                            rtol=0.0,
                            atol=1e-14,
                        )
                    ),
                ]
            )
    checks["rates_counts_intervals_and_errors_consistent"] = all(rate_checks)

    probability_checks = []
    for row in populations.loc[populations["stage"].ne("power")].itertuples():
        p = np.asarray(json.loads(row.probability_p_json), dtype=float)
        q = np.asarray(json.loads(row.probability_q_json), dtype=float)
        probability_checks.extend(
            [
                p.shape == (int(row.rows), int(row.columns)),
                q.shape == p.shape,
                _close(float(p.sum()), 1.0),
                _close(float(q.sum()), 1.0),
                bool(np.all(p >= 0.0) and np.all(q >= 0.0)),
                abs(_mi(p) - _mi(q)) < 2e-12,
            ]
        )
        if row.stage == "strong":
            probability_checks.append(bool(np.array_equal(p, q)))
    checks["saved_populations_valid_and_satisfy_null"] = all(probability_checks)

    aggregate_checks = []
    aggregate_groups = list(scenario.groupby("stage", sort=False))
    aggregate_groups.append(
        (
            "broad_balanced_design0",
            scenario[
                scenario["stage"].eq("broad")
                & scenario["design_index"].eq(0)
            ],
        )
    )
    for stage, group in aggregate_groups:
        for method in METHODS:
            stored = aggregate[
                aggregate["stage"].eq(stage)
                & aggregate["method"].eq(method)
            ].iloc[0]
            aggregate_checks.extend(
                [
                    int(stored["population_pairs"]) == len(group),
                    int(stored["table_pairs"]) == int(group["replicates"].sum()),
                    _close(
                        float(stored["aggregate_valid_rate"]),
                        float(group["valid_n"].sum() / group["replicates"].sum()),
                    ),
                    _close(
                        float(stored["mean_coverage_95"]),
                        float(group[f"{method}_coverage_95"].mean()),
                    ),
                ]
            )
            for label, alpha in (("10", 0.10), ("05", 0.05)):
                rates = group[f"{method}_fpr_{label}"]
                aggregate_checks.extend(
                    [
                        _close(
                            float(stored[f"mean_fpr_{label}"]),
                            float(rates.mean()),
                        ),
                        _close(
                            float(stored[f"mean_absolute_fpr_error_{label}"]),
                            float(np.mean(np.abs(rates - alpha))),
                        ),
                    ]
                )
    checks["aggregate_metrics_recompute_exactly"] = all(aggregate_checks)

    naive_df_error = float(
        np.median(
            np.abs(
                np.log(
                    df_audit["median_naive_total_df"]
                    / df_audit["empirical_total_df"]
                )
            )
        )
    )
    candidate_df_error = float(
        np.median(
            np.abs(
                np.log(
                    df_audit["median_if_total_df"]
                    / df_audit["empirical_total_df"]
                )
            )
        )
    )
    checks["df_audit_is_finite_positive"] = bool(
        np.isfinite(
            df_audit[
                [
                    "empirical_total_df",
                    "median_naive_total_df",
                    "median_if_total_df",
                    "population_if_total_df",
                ]
            ]
        ).all().all()
        and (
            df_audit[
                [
                    "empirical_total_df",
                    "median_naive_total_df",
                    "median_if_total_df",
                    "population_if_total_df",
                ]
            ]
            > 0
        ).all().all()
    )
    checks["df_error_improvement_recomputes"] = (
        candidate_df_error <= 0.5 * naive_df_error
    )
    checks["runtime_values_finite_positive"] = bool(
        np.isfinite(runtime.select_dtypes(include=[np.number])).all().all()
        and (
            runtime[
                [
                    "median_wald_normal_ms",
                    "median_welch_n_minus_1_ms",
                    "median_if_satterthwaite_ms",
                ]
            ]
            > 0
        ).all().all()
    )

    project_root = Path(__file__).resolve().parents[1]
    current_script_hash = hashlib.sha256(
        (project_root / "experiments" / "run_validation.py").read_bytes()
    ).hexdigest()
    current_method_hash = hashlib.sha256(
        (project_root / "src" / "influence_df_mi" / "method.py").read_bytes()
    ).hexdigest()
    checks["recorded_code_hashes_match"] = (
        current_script_hash == metadata["script_sha256"]
        and current_method_hash == metadata["method_sha256"]
    )

    stored_criteria = metadata["decision_metrics"]["criteria"]
    checks["stored_decision_matches_criteria"] = (
        metadata["decision"]
        == ("GO" if all(stored_criteria.values()) else "NO-GO")
    )
    checks["power_methods_complete"] = (
        power.groupby("scenario_id")["method"].nunique().eq(len(METHODS)).all()
        and set(power["method"]) == set(METHODS)
    )

    audit = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "recomputed": {
            "naive_median_absolute_log_df_error": naive_df_error,
            "candidate_median_absolute_log_df_error": candidate_df_error,
            "df_error_reduction": 1.0 - candidate_df_error / naive_df_error,
            "scenario_rows": len(scenario),
            "null_table_pairs": int(scenario["replicates"].sum()),
            "power_table_pairs": int(
                power.drop_duplicates("scenario_id")["replicates"].sum()
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
