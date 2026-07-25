from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats
from scipy.stats import random_table
from scipy.stats.contingency import chi2_contingency

try:
    from .general_fixed_margin import g_statistics_batch
    from .jidt_utils import DEFAULT_JIDT_JAR, init_jvm, table_to_observations
    from .saddlepoint_cgf import drop_empty_margins, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from general_fixed_margin import g_statistics_batch
    from jidt_utils import DEFAULT_JIDT_JAR, init_jvm, table_to_observations
    from saddlepoint_cgf import drop_empty_margins, g_statistic


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


def enumerate_fixed_margin_tables(rows: np.ndarray, cols: np.ndarray):
    rows = tuple(int(x) for x in rows)
    cols = tuple(int(x) for x in cols)
    r, c = len(rows), len(cols)
    table = np.zeros((r, c), dtype=np.int64)

    def row_vectors(max_values: list[int], total: int):
        current: list[int] = []

        def rec(j: int, remaining: int):
            if j == c - 1:
                if 0 <= remaining <= max_values[j]:
                    yield current + [remaining]
                return
            for value in range(min(max_values[j], remaining) + 1):
                current.append(value)
                yield from rec(j + 1, remaining - value)
                current.pop()

        yield from rec(0, total)

    def rec_row(i: int, remaining_cols: list[int]):
        if i == r - 1:
            if sum(remaining_cols) == rows[i]:
                table[i, :] = remaining_cols
                yield table.copy()
            return

        for vec in row_vectors(remaining_cols, rows[i]):
            table[i, :] = vec
            next_cols = [col - value for col, value in zip(remaining_cols, vec)]
            yield from rec_row(i + 1, next_cols)

    yield from rec_row(0, list(cols))


def fixed_margin_log_probability(table: np.ndarray) -> float:
    table = np.asarray(table, dtype=np.int64)
    rows = table.sum(axis=1)
    cols = table.sum(axis=0)
    n = int(table.sum())
    value = sum(math.lgamma(int(x) + 1) for x in rows)
    value += sum(math.lgamma(int(x) + 1) for x in cols)
    value -= math.lgamma(n + 1)
    value -= sum(math.lgamma(int(x) + 1) for x in table.ravel())
    return value


def exact_tail_probability(rows: np.ndarray, cols: np.ndarray, observed_g: float) -> tuple[float, int]:
    tables = list(enumerate_fixed_margin_tables(rows, cols))
    log_probs = np.array([fixed_margin_log_probability(table) for table in tables])
    probs = np.exp(log_probs - log_probs.max())
    probs /= probs.sum()
    g_values = np.array([g_statistic(table) for table in tables])
    tie_tol = max(1e-12, 1e-12 * max(abs(observed_g), float(np.max(np.abs(g_values)))))
    tail = float(probs[g_values >= observed_g - tie_tol].sum())
    return tail, len(tables)


def check_fixed_margin_sampler(seed: int = 20260706) -> CheckResult:
    rng = np.random.default_rng(seed)
    cases = [
        (np.array([3, 2]), np.array([2, 3]), np.array([[2, 1], [0, 2]])),
        (np.array([2, 2]), np.array([1, 1, 2]), np.array([[1, 0, 1], [0, 1, 1]])),
        (
            np.array([2, 2, 1]),
            np.array([1, 2, 2]),
            np.array([[1, 0, 1], [0, 1, 1], [0, 1, 0]]),
        ),
    ]
    details = []
    for rows, cols, observed in cases:
        observed_g = g_statistic(observed)
        exact_p, support = exact_tail_probability(rows, cols, observed_g)
        draws = random_table(rows, cols).rvs(size=20_000, random_state=rng)
        sampled_g = g_statistics_batch(draws)
        tie_tol = max(1e-12, 1e-12 * max(abs(observed_g), float(np.max(np.abs(sampled_g)))))
        sampled_p = (np.count_nonzero(sampled_g >= observed_g - tie_tol) + 1) / (len(sampled_g) + 1)
        diff = abs(exact_p - sampled_p)
        details.append(
            f"rows={rows.tolist()} cols={cols.tolist()} support={support} "
            f"exact={exact_p:.6g} sampled={sampled_p:.6g} diff={diff:.6g}"
        )
        if diff > 0.02:
            return CheckResult("fixed-margin sampler exactness", False, "; ".join(details))
    return CheckResult("fixed-margin sampler exactness", True, "; ".join(details))


def check_jidt_explicit_permutations() -> CheckResult:
    init_jvm(DEFAULT_JIDT_JAR)
    from infodynamics.measures.discrete import MutualInformationCalculatorDiscrete
    from jpype.types import JArray, JInt

    table = np.array([[3, 1, 0], [1, 2, 1], [0, 1, 1]], dtype=np.int64)
    r, c = table.shape
    n = int(table.sum())
    x, y = table_to_observations(table)
    calc = MutualInformationCalculatorDiscrete(r, c, 0)
    calc.initialise()
    calc.addObservations(x.tolist(), y.tolist())
    actual_bits = float(calc.computeAverageLocalOfObservations())

    permutations = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        [1, 0, 3, 2, 5, 4, 7, 6, 9, 8],
        [2, 3, 4, 5, 6, 7, 8, 9, 0, 1],
        [0, 2, 4, 6, 8, 1, 3, 5, 7, 9],
    ]
    java_int_array = JArray(JInt)
    java_int_matrix = JArray(java_int_array)
    java_permutations = java_int_matrix([java_int_array(p) for p in permutations])
    distribution = calc.computeSignificance(java_permutations)
    jidt_values = np.array([float(value) for value in distribution.distribution])

    i_counts = table.sum(axis=1).astype(int)
    j_counts = table.sum(axis=0).astype(int)
    i_values = np.concatenate([np.full(count, i, dtype=int) for i, count in enumerate(i_counts)])
    j_values = np.concatenate([np.full(count, j, dtype=int) for j, count in enumerate(j_counts)])
    manual_values = []
    for permutation in permutations:
        surrogate = np.zeros_like(table)
        np.add.at(surrogate, (i_values[np.array(permutation)], j_values), 1)
        manual_values.append(g_statistic(surrogate) / (2.0 * n * np.log(2.0)))
    manual_values = np.array(manual_values)
    manual_p = float(np.mean(manual_values >= actual_bits))

    max_diff = float(np.max(np.abs(jidt_values - manual_values)))
    p_diff = abs(float(distribution.pValue) - manual_p)
    passed = max_diff < 1e-12 and p_diff < 1e-12
    detail = (
        f"max surrogate MI diff={max_diff:.3g}; "
        f"JIDT p={float(distribution.pValue):.6g}; manual p={manual_p:.6g}; p diff={p_diff:.3g}"
    )
    return CheckResult("JIDT explicit permutation reproduction", passed, detail)


def check_jidt_analytic_units() -> CheckResult:
    init_jvm(DEFAULT_JIDT_JAR)
    from infodynamics.measures.discrete import MutualInformationCalculatorDiscrete

    cases = [
        np.array([[10, 0], [0, 10]], dtype=np.int64),
        np.array([[8, 2], [3, 7]], dtype=np.int64),
        np.array([[980, 3, 2], [4, 1, 0], [8, 0, 2]], dtype=np.int64),
    ]
    details = []
    for table in cases:
        r, c = table.shape
        n = int(table.sum())
        x, y = table_to_observations(table)
        calc = MutualInformationCalculatorDiscrete(r, c, 0)
        calc.initialise()
        calc.addObservations(x.tolist(), y.tolist())
        mi_bits = float(calc.computeAverageLocalOfObservations())
        analytic = calc.computeSignificance()
        df = (r - 1) * (c - 1)
        p_bits = float(stats.chi2.sf(2.0 * n * mi_bits, df))
        p_nats = float(stats.chi2.sf(2.0 * n * mi_bits * np.log(2.0), df))
        diff_bits = abs(float(analytic.pValue) - p_bits)
        details.append(
            f"shape={r}x{c} JIDT={float(analytic.pValue):.6g} "
            f"bits={p_bits:.6g} nats={p_nats:.6g} diff_bits={diff_bits:.3g}"
        )
        if diff_bits > 1e-12:
            return CheckResult("JIDT analytic unit convention", False, "; ".join(details))
    return CheckResult("JIDT analytic unit convention", True, "; ".join(details))


def check_standard_chi_square_against_scipy() -> CheckResult:
    tables = [
        np.array([[5, 5], [5, 5]], dtype=np.int64),
        np.array([[8, 2], [3, 7]], dtype=np.int64),
        np.array([[12, 3, 1], [4, 7, 0], [1, 2, 5]], dtype=np.int64),
    ]
    details = []
    for table in tables:
        counts = drop_empty_margins(table)
        g_value = g_statistic(counts)
        df = (counts.shape[0] - 1) * (counts.shape[1] - 1)
        p_value = float(stats.chi2.sf(g_value, df))
        scipy_result = chi2_contingency(counts, correction=False, lambda_="log-likelihood")
        stat_diff = abs(float(scipy_result.statistic) - g_value)
        p_diff = abs(float(scipy_result.pvalue) - p_value)
        details.append(
            f"shape={counts.shape[0]}x{counts.shape[1]} stat_diff={stat_diff:.3g} p_diff={p_diff:.3g}"
        )
        if stat_diff > 1e-10 or p_diff > 1e-12:
            return CheckResult("standard chi-square consistency", False, "; ".join(details))
    return CheckResult("standard chi-square consistency", True, "; ".join(details))


def main() -> None:
    checks = [
        check_fixed_margin_sampler(),
        check_jidt_explicit_permutations(),
        check_jidt_analytic_units(),
        check_standard_chi_square_against_scipy(),
    ]
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}", flush=True)
    if not all(check.passed for check in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
