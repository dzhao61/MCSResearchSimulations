#!/usr/bin/env python3
"""Independently audit frozen joint-Edgeworth validation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


METHODS = (
    "wald_normal",
    "welch_n_minus_1",
    "if_satterthwaite",
    "joint_edgeworth",
)
EXPECTED_ROWS = {"broad": 144, "hard": 12, "strong": 144, "stress": 26}
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
    positive = probability > 0
    return float(
        np.sum(
            probability[positive]
            * np.log(probability[positive] / denominator[positive])
        )
    )


def _close(actual: float, expected: float, tolerance: float = 1e-12) -> bool:
    return bool(np.isfinite(actual) and abs(actual - expected) <= tolerance)


def main() -> None:
    args = parse_args()
    root = args.results_dir
    scenario = pd.read_csv(root / "scenario_summary.csv")
    populations = pd.read_csv(root / "scenarios.csv")
    aggregate = pd.read_csv(root / "method_summary.csv")
    power = pd.read_csv(root / "power_summary.csv")
    runtime = pd.read_csv(root / "runtime_summary.csv")
    metadata = json.loads((root / "run_metadata.json").read_text())

    checks: dict[str, bool] = {}
    checks["scenario_row_counts"] = (
        scenario.groupby("stage").size().to_dict() == EXPECTED_ROWS
    )
    checks["replicate_counts"] = all(
        np.all(
            scenario.loc[scenario["stage"].eq(stage), "replicates"]
            == count
        )
        for stage, count in EXPECTED_REPLICATES.items()
    )
    checks["scenario_keys_unique"] = not scenario["scenario_key"].duplicated().any()
    checks["simulation_seeds_unique"] = not scenario[
        "simulation_seed"
    ].duplicated().any()
    checks["power_seeds_disjoint"] = set(
        power["simulation_seed"].unique()
    ).isdisjoint(set(scenario["simulation_seed"]))
    checks["all_null_deltas_zero"] = (
        float(np.max(np.abs(scenario["true_delta"]))) < 2e-12
    )

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
    checks["populations_valid_and_satisfy_null"] = all(probability_checks)

    rate_checks = []
    for method in METHODS:
        valid_n = scenario[f"{method}_valid_n"]
        valid_rate = scenario[f"{method}_valid_rate"]
        rate_checks.append(
            np.allclose(
                valid_rate,
                valid_n / scenario["replicates"],
                rtol=0.0,
                atol=1e-14,
            )
        )
        for label, alpha in (("10", 0.10), ("05", 0.05)):
            rate = scenario[f"{method}_fpr_{label}"]
            low = scenario[f"{method}_fpr_{label}_low"]
            high = scenario[f"{method}_fpr_{label}_high"]
            error = scenario[f"{method}_error_{label}"]
            rejection_count = rate * valid_n
            rate_checks.extend(
                [
                    bool(rate.between(0.0, 1.0).all()),
                    bool(
                        (
                            np.abs(rejection_count - np.round(rejection_count))
                            < 1e-7
                        ).all()
                    ),
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
    checks["rates_validity_counts_and_intervals_consistent"] = all(rate_checks)

    aggregate_checks = []
    groups = list(scenario.groupby("stage", sort=False))
    groups.append(
        (
            "broad_balanced_design0",
            scenario[
                scenario["stage"].eq("broad")
                & scenario["design_index"].eq(0)
            ],
        )
    )
    for stage, group in groups:
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
                        float(
                            group[f"{method}_valid_n"].sum()
                            / group["replicates"].sum()
                        ),
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
    checks["aggregate_metrics_recompute"] = all(aggregate_checks)

    project_root = Path(__file__).resolve().parents[1]
    script_hash = hashlib.sha256(
        (project_root / "experiments" / "run_validation.py").read_bytes()
    ).hexdigest()
    method_hash = hashlib.sha256(
        (
            project_root
            / "src"
            / "joint_edgeworth_mi"
            / "method.py"
        ).read_bytes()
    ).hexdigest()
    checks["recorded_code_hashes_match"] = (
        script_hash == metadata["script_sha256"]
        and method_hash == metadata["method_sha256"]
    )
    checks["stored_decision_matches_criteria"] = (
        metadata["decision"]
        == (
            "GO"
            if all(metadata["decision_metrics"]["criteria"].values())
            else "NO-GO"
        )
    )
    checks["power_methods_complete"] = (
        set(power["method"]) == set(METHODS)
        and power.groupby("scenario_id")["method"].nunique().eq(len(METHODS)).all()
    )
    checks["runtime_finite_positive"] = bool(
        (
            runtime[
                [
                    "median_wald_normal_ms",
                    "median_welch_n_minus_1_ms",
                    "median_if_satterthwaite_ms",
                    "median_joint_edgeworth_ms",
                ]
            ]
            > 0
        ).all().all()
    )

    checks = {name: bool(passed) for name, passed in checks.items()}
    artifact_status = "PASS" if all(checks.values()) else "FAIL"
    invalid_audit_path = root / "invalid_case_audit.csv"
    sensitivity: dict[str, object] = {}
    scientific_method_status = "NOT_AUDITED"
    if invalid_audit_path.exists():
        invalid = pd.read_csv(invalid_audit_path)
        invalid = invalid.merge(
            scenario[["scenario_key", "design_index"]],
            on="scenario_key",
            how="left",
        )
        sensitivity_groups = {
            "broad": invalid[invalid["stage"].eq("broad")],
            "hard": invalid[invalid["stage"].eq("hard")],
            "strong": invalid[invalid["stage"].eq("strong")],
            "stress": invalid[invalid["stage"].eq("stress")],
            "broad_balanced_design0": invalid[
                invalid["stage"].eq("broad")
                & invalid["design_index"].eq(0)
            ],
        }
        sensitivity["normal_fallback_mae_05"] = {
            name: float(
                np.mean(
                    np.abs(
                        group["candidate_normal_fallback_fpr_05"] - 0.05
                    )
                )
            )
            for name, group in sensitivity_groups.items()
        }
        sensitivity["invalid_normal_rejection_fraction_05"] = {
            stage: float(
                np.sum(
                    group["invalid_normal_rejection_rate_05"].fillna(0.0)
                    * group["invalid_n"]
                )
                / group["invalid_n"].sum()
            )
            for stage, group in sensitivity_groups.items()
            if group["invalid_n"].sum() > 0
        }
        regular_selectivity = all(
            sensitivity["invalid_normal_rejection_fraction_05"][stage] > 0.95
            for stage in ("broad", "hard", "strong")
        )
        fallback_fails_core = (
            sensitivity["normal_fallback_mae_05"]["hard"]
            > 0.90
            * float(
                aggregate.loc[
                    aggregate["stage"].eq("hard")
                    & aggregate["method"].eq("welch_n_minus_1"),
                    "mean_absolute_fpr_error_05",
                ].iloc[0]
            )
            or sensitivity["normal_fallback_mae_05"]["broad"]
            > float(
                aggregate.loc[
                    aggregate["stage"].eq("broad")
                    & aggregate["method"].eq("welch_n_minus_1"),
                    "mean_absolute_fpr_error_05",
                ].iloc[0]
            )
            + 0.00025
        )
        scientific_method_status = (
            "NO-GO"
            if regular_selectivity and fallback_fails_core
            else "REQUIRES_REVIEW"
        )
        sensitivity["selective_invalidity_detected"] = regular_selectivity
        sensitivity["normal_fallback_fails_core_criteria"] = fallback_fails_core

    audit = {
        "status": artifact_status,
        "artifact_integrity_status": artifact_status,
        "scientific_method_status": scientific_method_status,
        "checks": checks,
        "recomputed": {
            "scenario_rows": len(scenario),
            "null_table_pairs": int(scenario["replicates"].sum()),
            "power_table_pairs": int(
                power.drop_duplicates("scenario_id")["replicates"].sum()
            ),
            "edgeworth_invalid_by_stage": {
                stage: int(
                    (
                        group["replicates"]
                        - group["joint_edgeworth_valid_n"]
                    ).sum()
                )
                for stage, group in scenario.groupby("stage")
            },
        },
        "post_hoc_sensitivity": sensitivity,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
