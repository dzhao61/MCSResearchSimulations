#!/usr/bin/env python3
"""Cross-check local JIDT MI units and analytic significance calculations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jpype
import jpype.imports
import numpy as np
import pandas as pd
from scipy.stats import chi2

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from differential_mi.statistics import plugin_mi


DEFAULT_JAR = Path(
    "/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/"
    "jidt/infodynamics.jar"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, default=DEFAULT_JAR)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--random-tables", type=int, default=30)
    parser.add_argument("--seed", type=int, default=2026072504)
    return parser.parse_args()


def _observations(table: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rows, columns = table.shape
    x_parts = []
    y_parts = []
    for row in range(rows):
        for column in range(columns):
            count = int(table[row, column])
            if count:
                x_parts.append(np.full(count, row, dtype=np.int32))
                y_parts.append(np.full(count, column, dtype=np.int32))
    return np.concatenate(x_parts), np.concatenate(y_parts)


def _audit_table(table: np.ndarray, calculator_class: object) -> dict[str, float | int]:
    rows, columns = table.shape
    x, y = _observations(table)
    calculator = calculator_class(rows, columns, 0)
    calculator.initialise()
    calculator.addObservations(
        jpype.JArray(jpype.JInt)(x.tolist()),
        jpype.JArray(jpype.JInt)(y.tolist()),
    )
    jidt_bits = float(calculator.computeAverageLocalOfObservations())
    jidt_nats = jidt_bits * np.log(2.0)
    manual_nats = float(plugin_mi(table))
    statistic = 2.0 * int(table.sum()) * manual_nats
    jidt_bits_statistic = 2.0 * int(table.sum()) * jidt_bits
    degrees_of_freedom = (rows - 1) * (columns - 1)
    scipy_p = float(chi2.sf(statistic, degrees_of_freedom))
    scipy_jidt_bits_p = float(chi2.sf(jidt_bits_statistic, degrees_of_freedom))
    jidt_analytic = calculator.computeSignificance()
    return {
        "rows": rows,
        "columns": columns,
        "sample_size": int(table.sum()),
        "manual_mi_nats": manual_nats,
        "jidt_mi_bits": jidt_bits,
        "jidt_mi_nats": jidt_nats,
        "absolute_mi_error_nats": abs(jidt_nats - manual_nats),
        "g_statistic": statistic,
        "jidt_bits_statistic": jidt_bits_statistic,
        "degrees_of_freedom": degrees_of_freedom,
        "scipy_chi2_p": scipy_p,
        "scipy_jidt_bits_p": scipy_jidt_bits_p,
        "jidt_analytic_p": float(jidt_analytic.pValue),
        "jidt_vs_standard_p_difference": float(jidt_analytic.pValue) - scipy_p,
        "jidt_bits_convention_p_error": abs(
            float(jidt_analytic.pValue) - scipy_jidt_bits_p
        ),
    }


def main() -> None:
    args = parse_args()
    if not args.jar.is_file():
        raise FileNotFoundError(args.jar)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[str(args.jar)])
    from infodynamics.measures.discrete import MutualInformationCalculatorDiscrete

    tables = [
        np.array([[25, 25], [25, 25]], dtype=int),
        np.array([[50, 0], [0, 50]], dtype=int),
        np.array([[18, 2], [5, 25]], dtype=int),
        np.array([[8, 1, 4], [2, 11, 3]], dtype=int),
    ]
    rng = np.random.default_rng(args.seed)
    shapes = ((2, 2), (2, 5), (3, 3), (4, 7), (10, 10))
    for index in range(args.random_tables):
        rows, columns = shapes[index % len(shapes)]
        probabilities = rng.dirichlet(np.full(rows * columns, 0.7))
        table = rng.multinomial(200 + 13 * index, probabilities).reshape(
            rows, columns
        )
        tables.append(table)

    records = [
        _audit_table(table, MutualInformationCalculatorDiscrete)
        for table in tables
    ]
    frame = pd.DataFrame(records)
    frame.to_csv(args.output_dir / "jidt_unit_audit.csv", index=False)
    result = {
        "jar": str(args.jar),
        "tables": len(frame),
        "maximum_absolute_mi_error_nats": float(
            frame["absolute_mi_error_nats"].max()
        ),
        "maximum_absolute_jidt_vs_standard_p_difference": float(
            np.abs(frame["jidt_vs_standard_p_difference"]).max()
        ),
        "maximum_jidt_bits_convention_p_error": float(
            frame["jidt_bits_convention_p_error"].max()
        ),
        "mi_matches_1e_10": bool(
            frame["absolute_mi_error_nats"].max() <= 1e-10
        ),
        "jidt_analytic_matches_bits_convention_1e_10": bool(
            frame["jidt_bits_convention_p_error"].max() <= 1e-10
        ),
        "jidt_analytic_matches_standard_nats_chi2": False,
        "constructor": "MutualInformationCalculatorDiscrete(r, c, 0)",
        "jidt_output_unit": "bits",
        "manual_output_unit": "nats",
    }
    (args.output_dir / "jidt_unit_audit.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
