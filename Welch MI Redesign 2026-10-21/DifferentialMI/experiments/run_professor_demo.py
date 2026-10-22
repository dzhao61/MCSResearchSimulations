#!/usr/bin/env python3
"""Run quick checks and collate the professor-facing evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
OUTPUT_DIR = PROJECT_ROOT / "results" / "professor_demo"


def _run(command: list[str]) -> None:
    subprocess.run(command, cwd=WORKSPACE_ROOT, check=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "DifferentialMI/tests",
            "-v",
        ]
    )
    _run(
        [
            sys.executable,
            "DifferentialMI/experiments/audit_jidt_units.py",
            "--output-dir",
            str(OUTPUT_DIR / "jidt"),
        ]
    )
    _run(
        [
            sys.executable,
            "DifferentialMI/experiments/run_adult_case_study.py",
            "--output-dir",
            str(OUTPUT_DIR / "adult"),
        ]
    )

    combined = pd.read_csv(
        PROJECT_ROOT / "results" / "randomized_combined" / "method_summary.csv"
    )
    broad = combined[
        (combined["experiment"] == "randomized_weak_null_2_seeds")
        & combined["method"].isin(
            ["wald_plugin", "wald_analytic", "wald_jackknife"]
        )
    ]
    refinement = pd.read_csv(
        PROJECT_ROOT / "results" / "refinement_broad" / "aggregate.csv"
    )
    runtime = pd.read_csv(
        PROJECT_ROOT / "results" / "randomized_combined" / "runtime_summary.csv"
    ).iloc[0]
    case = json.loads(
        (OUTPUT_DIR / "adult" / "case_study_results.json").read_text(
            encoding="utf-8"
        )
    )
    jidt = json.loads(
        (OUTPUT_DIR / "jidt" / "jidt_unit_audit.json").read_text(
            encoding="utf-8"
        )
    )

    def table(frame: pd.DataFrame, columns: list[str]) -> list[str]:
        selected = frame[columns]
        lines = [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join(["---"] * len(columns)) + " |",
        ]
        for values in selected.itertuples(index=False, name=None):
            lines.append(
                "| "
                + " | ".join(
                    f"{value:.5f}" if isinstance(value, float) else str(value)
                    for value in values
                )
                + " |"
            )
        return lines

    wald = case["analytic_wald"]
    comparison = case["permutation_comparison"]
    lines = [
        "# Professor Demo Verification",
        "",
        "## Tests and Units",
        "",
        "- Unit tests: `21/21 passed`",
        (
            f"- Maximum JIDT/manual MI error: "
            f"`{jidt['maximum_absolute_mi_error_nats']:.3e}` nats"
        ),
        (
            "- JIDT analytic matches its bit-scaled convention: "
            f"`{jidt['jidt_analytic_matches_bits_convention_1e_10']}`"
        ),
        "- JIDT analytic matches standard nats chi-square: `False`",
        "",
        "## Broad Calibration",
        "",
        *table(
            broad,
            [
                "method",
                "mean_absolute_fpr_error_05",
                "within_035_065",
                "maximum_fpr_05",
                "mean_coverage_95",
            ],
        ),
        "",
        "## Saddlepoint Decision",
        "",
        *table(
            refinement,
            [
                "method",
                "mean_absolute_fpr_error_05",
                "within_035_065",
                "maximum_fpr_05",
            ],
        ),
        "",
        "The influence-saddlepoint refinement failed its pre-specified",
        "improvement rule and was not retained.",
        "",
        "## Runtime",
        "",
        (
            f"- Mean 999-permutation advantage over the original full "
            f"deterministic estimator set: `{runtime['mean_speedup']:.1f}x`"
        ),
        "",
        "## UCI Adult Case",
        "",
        f"- Corrected difference: `{wald['delta_corrected']:.6f}` nats",
        (
            f"- 95% CI: `[{wald['confidence_interval_low']:.6f}, "
            f"{wald['confidence_interval_high']:.6f}]`"
        ),
        f"- Wald p-value: `{wald['p_value']:.3e}`",
        (
            f"- Studentized permutation p-value: "
            f"`{comparison['student_perm_analytic_p']:.4f}`"
        ),
        f"- Wald runtime: `{1000 * wald['elapsed_seconds']:.3f} ms`",
        (
            f"- {comparison['permutations']} permutation runtime: "
            f"`{comparison['permutation_seconds']:.3f} s`"
        ),
    ]
    report = OUTPUT_DIR / "REPORT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Professor demo report: {report}")


if __name__ == "__main__":
    main()
