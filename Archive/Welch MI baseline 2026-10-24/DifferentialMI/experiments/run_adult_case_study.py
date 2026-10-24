#!/usr/bin/env python3
"""Run the pre-specified UCI Adult differential-MI case study."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.inference import analytic_wald_test, compare_tables


COLUMNS = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education_num",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
    "native_country",
    "income",
]

EDUCATION = [
    "Preschool",
    "1st-4th",
    "5th-6th",
    "7th-8th",
    "9th",
    "10th",
    "11th",
    "12th",
    "HS-grad",
    "Some-college",
    "Assoc-voc",
    "Assoc-acdm",
    "Bachelors",
    "Masters",
    "Prof-school",
    "Doctorate",
]

INCOME = ["<=50K", ">50K"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PROJECT_ROOT / "external" / "adult",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--permutations", type=int, default=9_999)
    parser.add_argument("--seed", type=int, default=2026072505)
    return parser.parse_args()


def _load_data(data_dir: Path) -> pd.DataFrame:
    options = {
        "names": COLUMNS,
        "skipinitialspace": True,
        "na_values": "?",
    }
    training = pd.read_csv(data_dir / "adult.data", **options)
    testing = pd.read_csv(data_dir / "adult.test", skiprows=1, **options)
    data = pd.concat([training, testing], ignore_index=True)
    data["income"] = data["income"].str.rstrip(".")
    return data


def _table(data: pd.DataFrame, sex: str) -> np.ndarray:
    subset = data.loc[data["sex"] == sex]
    counts = pd.crosstab(subset["education"], subset["income"])
    return counts.reindex(index=EDUCATION, columns=INCOME, fill_value=0).to_numpy(
        dtype=int
    )


def _chi_square_independence(table: np.ndarray) -> tuple[float, float]:
    degrees_of_freedom = (table.shape[0] - 1) * (table.shape[1] - 1)
    mi_nats = analytic_wald_test(table, table).mi_p_plugin
    statistic = 2.0 * table.sum() * mi_nats
    return float(statistic), float(chi2.sf(statistic, degrees_of_freedom))


def _write_tables(
    output_dir: Path, female: np.ndarray, male: np.ndarray
) -> None:
    records = []
    for group, table in (("Female", female), ("Male", male)):
        for row, education in enumerate(EDUCATION):
            for column, income in enumerate(INCOME):
                records.append(
                    {
                        "group": group,
                        "education": education,
                        "income": income,
                        "count": int(table[row, column]),
                    }
                )
    pd.DataFrame(records).to_csv(
        output_dir / "education_income_tables.csv", index=False
    )


def _write_report(output_dir: Path, result: dict) -> None:
    wald = result["analytic_wald"]
    comparison = result["permutation_comparison"]
    diagnostics_supported = (
        wald["influence_variance_p"] > 0
        and wald["influence_variance_q"] > 0
        and max(wald["expected_below_5_fraction_p"], wald["expected_below_5_fraction_q"])
        <= 0.20
    )
    lines = [
        "# UCI Adult Differential-MI Case Study",
        "",
        "## Question",
        "",
        "Does the education-income mutual information differ between female and",
        "male records in this dataset?",
        "",
        "## Result",
        "",
        f"- Female sample size: `{wald['n_p']}`",
        f"- Male sample size: `{wald['n_q']}`",
        f"- Female corrected MI: `{wald['mi_p_corrected']:.6f}` nats",
        f"- Male corrected MI: `{wald['mi_q_corrected']:.6f}` nats",
        f"- Corrected difference, Female - Male: `{wald['delta_corrected']:.6f}` nats",
        f"- Standard error: `{wald['standard_error']:.6f}`",
        (
            f"- 95% confidence interval: "
            f"`[{wald['confidence_interval_low']:.6f}, "
            f"{wald['confidence_interval_high']:.6f}]`"
        ),
        f"- Analytic Wald p-value: `{wald['p_value']:.6g}`",
        f"- Raw permutation p-value: `{comparison['naive_perm_plugin_p']:.6g}`",
        (
            f"- Studentized analytic permutation p-value: "
            f"`{comparison['student_perm_analytic_p']:.6g}`"
        ),
        "",
        "## Diagnostics",
        "",
        (
            f"- Zero-cell fractions: female `{wald['zero_fraction_p']:.3f}`, "
            f"male `{wald['zero_fraction_q']:.3f}`"
        ),
        (
            f"- Expected-count-below-5 fractions: female "
            f"`{wald['expected_below_5_fraction_p']:.3f}`, male "
            f"`{wald['expected_below_5_fraction_q']:.3f}`"
        ),
        (
            f"- Minimum expected counts: female "
            f"`{wald['minimum_independence_expected_p']:.3f}`, male "
            f"`{wald['minimum_independence_expected_q']:.3f}`"
        ),
        f"- Pooled-mixture MI: `{comparison['pooled_mi_plugin']:.6f}` nats",
        (
            f"- Pooled influence variance: "
            f"`{comparison['pooled_influence_variance']:.6f}`"
        ),
        f"- Simple support screen passed: `{diagnostics_supported}`",
        "",
        "## Runtime",
        "",
        f"- Analytic Wald: `{1000 * wald['elapsed_seconds']:.3f} ms`",
        (
            f"- {comparison['permutations']} table permutations: "
            f"`{comparison['permutation_seconds']:.3f} s`"
        ),
        "",
        "## Important Boundary",
        "",
        "The two within-group chi-square p-values test independence of education",
        "and income separately. They do not test whether the two MI values are",
        "equal. The analysis is descriptive, unweighted, and not causal.",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data = _load_data(args.data_dir)
    primary = data.dropna(subset=["education", "income", "sex"])
    female = _table(primary, "Female")
    male = _table(primary, "Male")
    wald = analytic_wald_test(female, male)
    comparison = compare_tables(
        female,
        male,
        permutations=args.permutations,
        rng=np.random.default_rng(args.seed),
    )
    female_chi2 = _chi_square_independence(female)
    male_chi2 = _chi_square_independence(male)
    result = {
        "dataset": {
            "source": "UCI Adult",
            "doi": "10.24432/C5XW20",
            "rows_loaded": len(data),
            "rows_analyzed": len(primary),
            "rows_excluded": len(data) - len(primary),
            "fnlwgt_used": False,
        },
        "analysis": {
            "row_variable": "education",
            "column_variable": "income",
            "group_variable": "sex",
            "group_p": "Female",
            "group_q": "Male",
            "permutations": args.permutations,
            "seed": args.seed,
        },
        "analytic_wald": wald.to_dict(),
        "permutation_comparison": comparison.to_dict(),
        "female_chi_square_independence": {
            "statistic": female_chi2[0],
            "p_value": female_chi2[1],
        },
        "male_chi_square_independence": {
            "statistic": male_chi2[0],
            "p_value": male_chi2[1],
        },
    }
    _write_tables(args.output_dir, female, male)
    (args.output_dir / "case_study_results.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_report(args.output_dir, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
