from __future__ import annotations

import argparse
import math

import numpy as np

try:
    from .jidt_utils import jidt_permutation_pvalue
    from .saddlepoint_cgf import CondCGF, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from jidt_utils import jidt_permutation_pvalue
    from saddlepoint_cgf import CondCGF, g_statistic


def assert_close(name: str, actual: float, expected: float, tol: float = 1e-10) -> None:
    if not math.isfinite(actual) or abs(actual - expected) > tol:
        raise AssertionError(f"{name}: actual={actual}, expected={expected}, tol={tol}")


def check_exact_moments() -> None:
    tables = [
        np.array([[5, 5], [5, 5]], dtype=int),
        np.array([[7, 3, 1], [2, 4, 1]], dtype=int),
        np.array([[5, 0, 2], [1, 3, 4], [2, 1, 2]], dtype=int),
    ]
    for idx, table in enumerate(tables, start=1):
        cgf = CondCGF.from_table(table, exact_table_limit=200_000)
        values, probs = cgf.exact_distribution(max_tables=200_000)
        mean = float(np.sum(values * probs))
        variance = float(np.sum((values - mean) ** 2 * probs))
        assert_close(f"table {idx} K(0)", cgf.K(0.0), 0.0, tol=1e-10)
        assert_close(f"table {idx} K1(0)", cgf.K1(0.0), mean, tol=1e-10)
        assert_close(f"table {idx} K2(0)", cgf.K2(0.0), variance, tol=1e-10)
        assert_close(f"table {idx} probability sum", float(probs.sum()), 1.0, tol=1e-10)


def check_left_of_mean_regression() -> None:
    cgf = CondCGF([20, 15, 15], [20, 15, 15], exact_table_limit=10)
    mean = cgf.K1(0.0)
    t = max(0.1, mean - 2.0 * math.sqrt(cgf.K2(0.0)))
    result = cgf.pvalue(t, method="saddlepoint")
    if not math.isfinite(result.pvalue) or not (0.5 < result.pvalue <= 1.0):
        raise AssertionError(
            f"left-of-mean p-value should be large and finite; t={t}, mean={mean}, result={result}"
        )


def check_saddlepoint_monotonicity() -> None:
    cgf = CondCGF([18, 17, 15], [20, 16, 14], exact_table_limit=10)
    mean = cgf.K1(0.0)
    sd = math.sqrt(cgf.K2(0.0))
    grid = np.linspace(max(0.01, mean - 2.5 * sd), mean + 2.5 * sd, 17)
    pvalues = np.array([cgf.pvalue(float(t), method="saddlepoint").pvalue for t in grid])
    if np.any(~np.isfinite(pvalues)):
        raise AssertionError(f"non-finite saddlepoint p-values: {pvalues}")
    if np.any((pvalues < -1e-12) | (pvalues > 1.0 + 1e-12)):
        raise AssertionError(f"out-of-range saddlepoint p-values: {pvalues}")
    if np.any(np.diff(pvalues) > 1e-8):
        raise AssertionError(f"saddlepoint p-values are not monotone decreasing: {pvalues}")


def check_jidt_statistic() -> None:
    table = np.array([[18, 2], [3, 7]], dtype=int)
    manual_g = g_statistic(table)
    jidt = jidt_permutation_pvalue(table, r_nominal=2, c_nominal=2, shuffles=10)
    assert_close("JIDT G statistic", jidt.g_statistic, manual_g, tol=1e-10)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run saddlepoint validation correctness checks.")
    parser.add_argument("--skip-jidt", action="store_true", help="Skip the JIDT bridge statistic check.")
    args = parser.parse_args()

    check_exact_moments()
    check_left_of_mean_regression()
    check_saddlepoint_monotonicity()
    if not args.skip_jidt:
        check_jidt_statistic()
    print("All saddlepoint validation checks passed.")


if __name__ == "__main__":
    main()
