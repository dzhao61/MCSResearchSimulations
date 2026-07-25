from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy import stats
from scipy.special import gammaln


def _as_positive_int_array(values: Iterable[int], name: str) -> np.ndarray:
    arr = np.asarray(list(values), dtype=np.int64)
    arr = arr[arr > 0]
    if arr.size == 0:
        raise ValueError(f"{name} must contain at least one positive count")
    return arr


def _log_factorials(n: int) -> np.ndarray:
    return gammaln(np.arange(n + 1, dtype=np.float64) + 1.0)


def drop_empty_margins(table: np.ndarray) -> np.ndarray:
    counts = np.asarray(table, dtype=np.int64)
    row_mask = counts.sum(axis=1) > 0
    col_mask = counts.sum(axis=0) > 0
    return counts[row_mask][:, col_mask]


def g_statistic(table: np.ndarray) -> float:
    counts = drop_empty_margins(table)
    total = int(counts.sum())
    if total <= 0:
        return 0.0

    rows = counts.sum(axis=1, keepdims=True)
    cols = counts.sum(axis=0, keepdims=True)
    mask = counts > 0
    ratio = np.ones_like(counts, dtype=np.float64)
    np.divide(counts * total, rows * cols, out=ratio, where=mask)
    return float(2.0 * np.sum(np.where(mask, counts * np.log(ratio), 0.0)))


@dataclass(frozen=True)
class PValueResult:
    pvalue: float
    route: str
    support_count: int | None
    support_count_status: str
    elapsed_s: float
    saddlepoint_s_hat: float | None = None
    saddlepoint_w: float | None = None
    saddlepoint_u: float | None = None
    saddlepoint_k: float | None = None
    saddlepoint_k2: float | None = None
    saddlepoint_iterations: int | None = None
    saddlepoint_converged: bool | None = None
    saddlepoint_fallback: str = ""


@dataclass(frozen=True)
class SaddlepointTailResult:
    pvalue: float
    s_hat: float | None
    w: float | None
    u: float | None
    k: float | None
    k2: float | None
    iterations: int
    converged: bool
    fallback: str


@dataclass(frozen=True)
class TransitionLayer:
    """Typed transition arrays for one DP layer, sorted by destination state."""

    from_idx: np.ndarray
    to_idx: np.ndarray
    g_sum: np.ndarray
    log_denom: np.ndarray
    group_starts: np.ndarray
    group_lengths: np.ndarray
    group_index: np.ndarray
    group_to_idx: np.ndarray


class CondCGF:
    """Exact conditional CGF for G = 2N*MI under fixed margins."""

    def __init__(
        self,
        row_totals: Iterable[int],
        col_totals: Iterable[int],
        exact_table_limit: int = 20_000,
    ) -> None:
        rows = _as_positive_int_array(row_totals, "row_totals")
        cols = _as_positive_int_array(col_totals, "col_totals")
        if int(rows.sum()) != int(cols.sum()):
            raise ValueError("row and column totals must have the same sum")

        # Make the smaller alphabet the column side, because DP state grows with columns.
        if cols.size > rows.size:
            rows, cols = cols, rows

        self.rows = np.sort(rows)[::-1].astype(np.int64)
        self.cols = np.sort(cols)[::-1].astype(np.int64)
        self.n = int(self.rows.sum())
        self.r = int(self.rows.size)
        self.c = int(self.cols.size)
        self.exact_table_limit = exact_table_limit
        self.logfact = _log_factorials(self.n)
        self._constant = (
            float(self.logfact[self.rows].sum())
            + float(self.logfact[self.cols].sum())
            - float(self.logfact[self.n])
        )
        self._allocations = [self._row_allocations(int(row)) for row in self.rows]
        self._state_layers, self._transition_layers = self._build_transition_layers()
        self._cache: dict[float, tuple[float, float, float]] = {}
        self._support_count: int | None = None

    @staticmethod
    def from_table(table: np.ndarray, exact_table_limit: int = 20_000) -> "CondCGF":
        counts = drop_empty_margins(table)
        return CondCGF(
            counts.sum(axis=1),
            counts.sum(axis=0),
            exact_table_limit=exact_table_limit,
        )

    def _cell_contribution(self, row_total: int, col_total: int, k: int) -> float:
        if k <= 0:
            return 0.0
        return float(2.0 * k * math.log((k * self.n) / (row_total * col_total)))

    def _row_allocations(self, row_total: int) -> list[tuple[tuple[int, ...], float, float]]:
        allocations: list[tuple[tuple[int, ...], float, float]] = []
        current = [0] * self.c

        def rec(pos: int, remaining: int) -> None:
            if pos == self.c - 1:
                if 0 <= remaining <= self.cols[pos]:
                    current[pos] = remaining
                    values = tuple(current)
                    g_sum = sum(
                        self._cell_contribution(row_total, int(col), int(k))
                        for col, k in zip(self.cols, values)
                    )
                    log_denom = float(sum(self.logfact[k] for k in values))
                    allocations.append((values, g_sum, log_denom))
                return

            max_k = min(int(self.cols[pos]), remaining)
            for k in range(max_k + 1):
                current[pos] = k
                rec(pos + 1, remaining - k)

        rec(0, row_total)
        return allocations

    def _build_transition_layers(
        self,
    ) -> tuple[
        list[dict[tuple[int, ...], int]],
        list[TransitionLayer],
    ]:
        state_layers: list[dict[tuple[int, ...], int]] = [
            {tuple(int(x) for x in self.cols): 0}
        ]
        transition_layers: list[TransitionLayer] = []

        for allocs in self._allocations:
            current = state_layers[-1]
            next_states: dict[tuple[int, ...], int] = {}
            from_values: list[int] = []
            to_values: list[int] = []
            g_values: list[float] = []
            log_denom_values: list[float] = []
            for state, from_idx in current.items():
                for alloc, g_sum, log_denom in allocs:
                    if not all(k <= u for k, u in zip(alloc, state)):
                        continue
                    new_state = tuple(u - k for u, k in zip(state, alloc))
                    to_idx = next_states.get(new_state)
                    if to_idx is None:
                        to_idx = len(next_states)
                        next_states[new_state] = to_idx
                    from_values.append(from_idx)
                    to_values.append(to_idx)
                    g_values.append(g_sum)
                    log_denom_values.append(log_denom)
            state_layers.append(next_states)
            transition_layers.append(
                self._make_transition_layer(
                    from_values,
                    to_values,
                    g_values,
                    log_denom_values,
                )
            )

        return state_layers, transition_layers

    @staticmethod
    def _make_transition_layer(
        from_values: list[int],
        to_values: list[int],
        g_values: list[float],
        log_denom_values: list[float],
    ) -> TransitionLayer:
        from_idx = np.asarray(from_values, dtype=np.int64)
        to_idx = np.asarray(to_values, dtype=np.int64)
        g_sum = np.asarray(g_values, dtype=np.float64)
        log_denom = np.asarray(log_denom_values, dtype=np.float64)

        if to_idx.size:
            order = np.argsort(to_idx, kind="mergesort")
            from_idx = from_idx[order]
            to_idx = to_idx[order]
            g_sum = g_sum[order]
            log_denom = log_denom[order]
            group_starts = np.flatnonzero(
                np.r_[True, to_idx[1:] != to_idx[:-1]]
            ).astype(np.int64)
            group_lengths = np.diff(
                np.r_[group_starts, np.asarray([to_idx.size], dtype=np.int64)]
            ).astype(np.int64)
            group_index = np.repeat(
                np.arange(group_starts.size, dtype=np.int64), group_lengths
            )
            group_to_idx = to_idx[group_starts]
        else:
            group_starts = np.empty(0, dtype=np.int64)
            group_lengths = np.empty(0, dtype=np.int64)
            group_index = np.empty(0, dtype=np.int64)
            group_to_idx = np.empty(0, dtype=np.int64)

        return TransitionLayer(
            from_idx=from_idx,
            to_idx=to_idx,
            g_sum=g_sum,
            log_denom=log_denom,
            group_starts=group_starts,
            group_lengths=group_lengths,
            group_index=group_index,
            group_to_idx=group_to_idx,
        )

    def support_count(self, limit: int | None = None) -> int:
        if self._support_count is not None:
            return self._support_count

        if limit is not None:
            cap = int(limit) + 1
            counts_array = np.array([1], dtype=np.int64)
            for layer_index, layer in enumerate(self._transition_layers):
                next_counts = np.zeros(
                    len(self._state_layers[layer_index + 1]), dtype=np.int64
                )
                np.add.at(next_counts, layer.to_idx, counts_array[layer.from_idx])
                np.minimum(next_counts, cap, out=next_counts)
                counts_array = next_counts
                if int(counts_array.sum()) > limit:
                    return cap

            terminal_idx = self._state_layers[-1].get(tuple([0] * self.c))
            self._support_count = (
                int(counts_array[terminal_idx]) if terminal_idx is not None else 0
            )
            return self._support_count

        counts = [1]
        for layer_index, layer in enumerate(self._transition_layers):
            next_counts = [0] * len(self._state_layers[layer_index + 1])
            for from_idx, to_idx in zip(layer.from_idx.tolist(), layer.to_idx.tolist()):
                next_counts[to_idx] += counts[from_idx]
            counts = next_counts

        terminal_idx = self._state_layers[-1].get(tuple([0] * self.c))
        self._support_count = int(counts[terminal_idx]) if terminal_idx is not None else 0
        return self._support_count

    def support_count_with_status(self, limit: int | None = None) -> tuple[int | None, str]:
        count = self.support_count(limit=limit)
        if limit is not None and count > limit:
            return None, f">{limit}"
        return count, "exact"

    def K_moments(self, s: float) -> tuple[float, float, float]:
        key = round(float(s), 14)
        if key in self._cache:
            return self._cache[key]

        # Each state stores log total weight, tilted mean of accumulated T, and raw second moment.
        log_z = np.array([0.0], dtype=np.float64)
        mean = np.array([0.0], dtype=np.float64)
        raw2 = np.array([0.0], dtype=np.float64)

        for layer_index, layer in enumerate(self._transition_layers):
            next_size = len(self._state_layers[layer_index + 1])
            next_log_z = np.full(next_size, -np.inf, dtype=np.float64)
            next_mean = np.zeros(next_size, dtype=np.float64)
            next_raw2 = np.zeros(next_size, dtype=np.float64)

            if layer.from_idx.size:
                prev_mean = mean[layer.from_idx]
                cand_log_z = log_z[layer.from_idx] + s * layer.g_sum - layer.log_denom
                cand_mean = prev_mean + layer.g_sum
                cand_raw2 = (
                    raw2[layer.from_idx]
                    + 2.0 * layer.g_sum * prev_mean
                    + layer.g_sum * layer.g_sum
                )

                max_log = np.maximum.reduceat(cand_log_z, layer.group_starts)
                weights = np.exp(cand_log_z - max_log[layer.group_index])
                sum_weights = np.add.reduceat(weights, layer.group_starts)
                next_log_z[layer.group_to_idx] = max_log + np.log(sum_weights)
                next_mean[layer.group_to_idx] = (
                    np.add.reduceat(weights * cand_mean, layer.group_starts)
                    / sum_weights
                )
                next_raw2[layer.group_to_idx] = (
                    np.add.reduceat(weights * cand_raw2, layer.group_starts)
                    / sum_weights
                )

            log_z, mean, raw2 = next_log_z, next_mean, next_raw2

        terminal_idx = self._state_layers[-1].get(tuple([0] * self.c))
        if terminal_idx is None or not np.isfinite(log_z[terminal_idx]):
            raise RuntimeError("DP ended without a zero-capacity terminal state")

        final_log_w = float(log_z[terminal_idx])
        final_mean = float(mean[terminal_idx])
        final_raw2 = float(raw2[terminal_idx])
        variance = max(0.0, final_raw2 - final_mean * final_mean)
        result = (final_log_w + self._constant, final_mean, variance)
        self._cache[key] = result
        return result

    def K(self, s: float) -> float:
        return self.K_moments(s)[0]

    def K1(self, s: float) -> float:
        return self.K_moments(s)[1]

    def K2(self, s: float) -> float:
        return self.K_moments(s)[2]

    def exact_distribution(self, max_tables: int | None = None) -> tuple[np.ndarray, np.ndarray]:
        limit = self.exact_table_limit if max_tables is None else max_tables
        count = self.support_count(limit=limit)
        if count > limit:
            raise ValueError(f"support has more than {limit} tables")

        stats_values: list[float] = []
        log_probs: list[float] = []

        def rec(row_idx: int, state: tuple[int, ...], t_sum: float, log_denom: float) -> None:
            if row_idx == self.r:
                if all(u == 0 for u in state):
                    stats_values.append(t_sum)
                    log_probs.append(self._constant - log_denom)
                return

            for alloc, g_sum, alloc_log_denom in self._allocations[row_idx]:
                if all(k <= u for k, u in zip(alloc, state)):
                    new_state = tuple(u - k for u, k in zip(state, alloc))
                    rec(row_idx + 1, new_state, t_sum + g_sum, log_denom + alloc_log_denom)

        rec(0, tuple(int(x) for x in self.cols), 0.0, 0.0)
        probs = np.exp(np.asarray(log_probs, dtype=np.float64))
        total = probs.sum()
        if total > 0:
            probs = probs / total
        return np.asarray(stats_values, dtype=np.float64), probs

    def exact_pvalue(self, t: float, midp: bool = False) -> float:
        values, probs = self.exact_distribution()
        tol = 1e-10
        if midp:
            greater = probs[values > t + tol].sum()
            equal = probs[np.abs(values - t) <= tol].sum()
            return self._clip_probability(float(greater + 0.5 * equal))
        return self._clip_probability(float(probs[values >= t - tol].sum()))

    @staticmethod
    def _clip_probability(value: float) -> float:
        if not np.isfinite(value):
            return np.nan
        return float(np.clip(value, 0.0, 1.0))

    @staticmethod
    def _normal_upper_tail(t: float, mean: float, variance: float) -> float:
        if variance <= 0.0:
            return 1.0 if t <= mean else 0.0
        z = (t - mean) / math.sqrt(variance)
        return float(stats.norm.sf(z))

    def saddlepoint_tail(self, t: float) -> SaddlepointTailResult:
        mean = self.K1(0.0)
        variance = self.K2(0.0)
        if variance <= 1e-14:
            return SaddlepointTailResult(
                pvalue=1.0 if t <= mean else 0.0,
                s_hat=None,
                w=None,
                u=None,
                k=None,
                k2=variance,
                iterations=0,
                converged=True,
                fallback="degenerate_variance",
            )

        sd = math.sqrt(variance)
        normal_p = self._normal_upper_tail(t, mean, variance)
        if abs(t - mean) <= 1e-6 * max(1.0, sd):
            return SaddlepointTailResult(
                pvalue=normal_p,
                s_hat=0.0,
                w=0.0,
                u=0.0,
                k=0.0,
                k2=variance,
                iterations=0,
                converged=True,
                fallback="near_mean_normal",
            )

        if t > mean:
            lo, hi = 0.0, 1.0
            while self.K1(hi) < t:
                hi *= 2.0
                if hi > 256:
                    return SaddlepointTailResult(
                        pvalue=0.0,
                        s_hat=hi,
                        w=None,
                        u=None,
                        k=None,
                        k2=None,
                        iterations=0,
                        converged=False,
                        fallback="right_bracket_exhausted",
                    )
        else:
            lo, hi = -1.0, 0.0
            while self.K1(lo) > t:
                lo *= 2.0
                if lo < -256:
                    return SaddlepointTailResult(
                        pvalue=1.0,
                        s_hat=lo,
                        w=None,
                        u=None,
                        k=None,
                        k2=None,
                        iterations=0,
                        converged=False,
                        fallback="left_bracket_exhausted",
                    )

        s_hat = 0.5 * (lo + hi)
        converged = False
        iterations = 0
        for iterations in range(1, 25):
            _, tilted_mean, tilted_var = self.K_moments(s_hat)
            err = tilted_mean - t
            if abs(err) <= 1e-8 * max(1.0, abs(t)):
                converged = True
                break

            if tilted_mean < t:
                lo = s_hat
            else:
                hi = s_hat

            if tilted_var > 1e-14:
                proposal = s_hat - err / tilted_var
                if lo < proposal < hi:
                    s_hat = proposal
                    continue
            s_hat = 0.5 * (lo + hi)

        k_hat, _, k2_hat = self.K_moments(s_hat)
        if k2_hat <= 1e-14:
            return SaddlepointTailResult(
                pvalue=normal_p,
                s_hat=s_hat,
                w=None,
                u=None,
                k=k_hat,
                k2=k2_hat,
                iterations=iterations,
                converged=converged,
                fallback="tilted_variance_normal",
            )

        signed = 1.0 if s_hat >= 0 else -1.0
        radicand = max(0.0, 2.0 * (s_hat * t - k_hat))
        w = signed * math.sqrt(radicand)
        u = s_hat * math.sqrt(k2_hat)

        if abs(w) < 1e-5 or abs(u) < 1e-8:
            return SaddlepointTailResult(
                pvalue=normal_p,
                s_hat=s_hat,
                w=w,
                u=u,
                k=k_hat,
                k2=k2_hat,
                iterations=iterations,
                converged=converged,
                fallback="small_w_or_u_normal",
            )

        cdf = stats.norm.cdf(w) + stats.norm.pdf(w) * (1.0 / w - 1.0 / u)
        upper = 1.0 - cdf
        direct_upper = stats.norm.sf(w) + stats.norm.pdf(w) * (1.0 / u - 1.0 / w)
        p = direct_upper if t >= mean else upper
        fallback = ""

        if not np.isfinite(p) or p < 0.0 or p > 1.0:
            p = normal_p
            fallback = "invalid_lr_normal"
        elif t < mean - 0.25 * sd and p < 0.5:
            p = normal_p
            fallback = "left_tail_guard_normal"

        return SaddlepointTailResult(
            pvalue=self._clip_probability(p),
            s_hat=s_hat,
            w=w,
            u=u,
            k=k_hat,
            k2=k2_hat,
            iterations=iterations,
            converged=converged,
            fallback=fallback,
        )

    def saddlepoint_pvalue(self, t: float) -> float:
        return self.saddlepoint_tail(t).pvalue

    def pvalue(self, t: float, method: str = "auto", midp: bool = False) -> PValueResult:
        start = time.perf_counter()
        support: int | None = None
        support_status = "not_checked"
        if method not in {"auto", "exact", "saddlepoint"}:
            raise ValueError("method must be one of: auto, exact, saddlepoint")

        route = method
        if method == "auto":
            support, support_status = self.support_count_with_status(limit=self.exact_table_limit)
            route = "exact" if support_status == "exact" and support is not None else "saddlepoint"

        if route == "exact":
            if support is None:
                support, support_status = self.support_count_with_status(limit=self.exact_table_limit)
            p = self.exact_pvalue(t, midp=midp)
            tail = None
        else:
            if support is None:
                support, support_status = self.support_count_with_status(limit=self.exact_table_limit)
            tail = self.saddlepoint_tail(t)
            p = tail.pvalue

        return PValueResult(
            pvalue=float(p),
            route=route,
            support_count=support,
            support_count_status=support_status,
            elapsed_s=time.perf_counter() - start,
            saddlepoint_s_hat=None if tail is None else tail.s_hat,
            saddlepoint_w=None if tail is None else tail.w,
            saddlepoint_u=None if tail is None else tail.u,
            saddlepoint_k=None if tail is None else tail.k,
            saddlepoint_k2=None if tail is None else tail.k2,
            saddlepoint_iterations=None if tail is None else tail.iterations,
            saddlepoint_converged=None if tail is None else tail.converged,
            saddlepoint_fallback="" if tail is None else tail.fallback,
        )
