"""Correctness tests for paired differential-MI calculations."""

from __future__ import annotations

import unittest

import numpy as np

from paired_differential_mi.core import (
    _jackknife_pseudovalues_flat,
    _plugin_mi_flat,
    paired_bootstrap_t,
    paired_mi_tests,
)
from paired_differential_mi.distributions import (
    coupling_diagnostics,
    paired_coupling,
    table_with_target_mi,
)


class PairedCoreTests(unittest.TestCase):
    def test_plugin_mi_known_tables(self) -> None:
        independent = np.array([[25, 25], [25, 25]]).reshape(1, -1)
        diagonal = np.array([[50, 0], [0, 50]]).reshape(1, -1)
        self.assertAlmostEqual(_plugin_mi_flat(independent, (2, 2))[0], 0.0)
        self.assertAlmostEqual(
            _plugin_mi_flat(diagonal, (2, 2))[0], np.log(2.0)
        )

    def test_fast_pseudovalues_match_brute_delete_one(self) -> None:
        table = np.array([[4, 2, 1], [3, 5, 2]])
        flat = table.reshape(1, -1)
        n = table.sum()
        full = _plugin_mi_flat(flat, table.shape)[0]
        fast = _jackknife_pseudovalues_flat(flat, table.shape)[0]
        for cell in np.flatnonzero(table):
            reduced = table.copy().reshape(-1)
            reduced[cell] -= 1
            leave_one_out = _plugin_mi_flat(
                reduced.reshape(1, -1), table.shape
            )[0]
            brute = n * full - (n - 1) * leave_one_out
            self.assertAlmostEqual(fast[cell], brute, places=12)

    def test_coupling_preserves_both_tables(self) -> None:
        pa = table_with_target_mi(3, 3, "balanced", 0.10, "ordinal")
        pb = table_with_target_mi(3, 3, "strong", 0.10, "cyclic")
        for pairing in (-0.8, 0.0, 0.8):
            coupling = paired_coupling(pa, pb, pairing)
            np.testing.assert_allclose(coupling.sum(axis=1), pa.reshape(-1))
            np.testing.assert_allclose(coupling.sum(axis=0), pb.reshape(-1))
            diagnostics = coupling_diagnostics(pa, pb, coupling)
            self.assertAlmostEqual(diagnostics["true_delta"], 0.0, places=10)

    def test_pairing_controls_covariance_sign(self) -> None:
        pa = table_with_target_mi(3, 3, "balanced", 0.10, "ordinal")
        pb = table_with_target_mi(3, 3, "strong", 0.10, "cyclic")
        negative = coupling_diagnostics(
            pa, pb, paired_coupling(pa, pb, -0.8)
        )
        zero = coupling_diagnostics(pa, pb, paired_coupling(pa, pb, 0.0))
        positive = coupling_diagnostics(
            pa, pb, paired_coupling(pa, pb, 0.8)
        )
        self.assertLess(negative["population_covariance"], 0)
        self.assertAlmostEqual(zero["population_covariance"], 0.0, places=14)
        self.assertGreater(positive["population_covariance"], 0)

    def test_paired_variance_matches_expanded_local_scores(self) -> None:
        counts = np.array(
            [
                [5, 1, 0, 1],
                [0, 4, 1, 0],
                [1, 0, 3, 1],
                [0, 1, 0, 6],
            ]
        )
        result = paired_mi_tests(counts, (2, 2))
        flat_a = counts.sum(axis=1)
        flat_b = counts.sum(axis=0)
        table_a = flat_a.reshape(2, 2)
        table_b = flat_b.reshape(2, 2)
        n = counts.sum()

        def local(table: np.ndarray) -> np.ndarray:
            row = table.sum(axis=1)
            column = table.sum(axis=0)
            values = np.zeros(4)
            for cell in np.flatnonzero(table):
                i, j = divmod(cell, 2)
                values[cell] = np.log(
                    table[i, j] * n / (row[i] * column[j])
                )
            return values

        local_a = local(table_a)
        local_b = local(table_b)
        expanded = []
        for a, b in np.argwhere(counts > 0):
            expanded.extend([local_a[a] - local_b[b]] * counts[a, b])
        expected = np.var(expanded, ddof=1) / n
        self.assertAlmostEqual(
            result["paired_standard_error"] ** 2, expected, places=14
        )

    def test_condition_swap_is_invariant(self) -> None:
        counts = np.array(
            [
                [5, 1, 0, 1],
                [0, 4, 1, 0],
                [1, 0, 3, 1],
                [0, 1, 0, 6],
            ]
        )
        forward = paired_mi_tests(counts, (2, 2))
        reverse = paired_mi_tests(counts.T, (2, 2))
        self.assertAlmostEqual(
            forward["delta_corrected"], -reverse["delta_corrected"]
        )
        self.assertAlmostEqual(
            forward["paired_wald_normal_p"],
            reverse["paired_wald_normal_p"],
        )
        self.assertAlmostEqual(
            forward["paired_jackknife_t_p"],
            reverse["paired_jackknife_t_p"],
        )

    def test_bootstrap_returns_valid_probability(self) -> None:
        counts = np.array(
            [
                [5, 1, 0, 1],
                [0, 4, 1, 0],
                [1, 0, 3, 1],
                [0, 1, 0, 6],
            ]
        )
        result = paired_bootstrap_t(
            counts,
            (2, 2),
            replicates=99,
            rng=np.random.default_rng(7),
        )
        self.assertTrue(0.0 <= result.p_value <= 1.0)
        self.assertGreater(result.valid_replicates, 90)


if __name__ == "__main__":
    unittest.main()
