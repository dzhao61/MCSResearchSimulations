from __future__ import annotations

import unittest

import numpy as np

from sparse_cmi import Stratum, test_sparse_cmi
from sparse_cmi.approximations import (
    cornish_fisher_critical_value,
    edgeworth_pvalue,
    normal_pvalue,
)
from sparse_cmi.simulation import validation_configurations


class ApiAndEdgeCaseTests(unittest.TestCase):
    def test_api_matches_exact_when_requested(self) -> None:
        result = test_sparse_cmi(
            [Stratum(5, 2, 2, 2), Stratum(6, 2, 3, 2)],
            exact_max_states=10_000,
        )
        self.assertIsNotNone(result.p_exact)
        self.assertIsNotNone(result.exact_state_count)
        self.assertGreaterEqual(result.p_exact, 0.0)
        self.assertLessEqual(result.p_exact, 1.0)
        self.assertEqual(result.informative_strata, 2)

    def test_zero_aggregate_variance_is_defined(self) -> None:
        result = test_sparse_cmi(
            [Stratum(3, 0, 1, 0), Stratum(4, 2, 4, 2)],
            exact_max_states=100,
        )
        self.assertEqual(result.variance, 0.0)
        self.assertEqual(result.p_normal, 1.0)
        self.assertEqual(result.p_edgeworth, 1.0)
        self.assertEqual(result.p_exact, 1.0)
        self.assertEqual(result.informative_strata, 0)
        self.assertTrue(np.isinf(result.cf_critical_value))

    def test_positive_constant_null_never_rejects(self) -> None:
        # With one X=1 and a balanced Y margin, both attainable tables have
        # the same positive G^2. The conditional p-value is still one.
        result = test_sparse_cmi(
            [Stratum(10, 1, 5, 0)],
            exact_max_states=100,
        )
        self.assertGreater(result.g2_observed, 0)
        self.assertEqual(result.variance, 0.0)
        self.assertEqual(result.p_normal, 1.0)
        self.assertEqual(result.p_edgeworth, 1.0)
        self.assertEqual(result.p_exact, 1.0)
        self.assertTrue(
            np.isinf(
                cornish_fisher_critical_value(
                    0.05,
                    result.mean,
                    result.variance,
                    result.skewness,
                )
            )
        )

    def test_approximation_pvalues_are_finite_and_bounded(self) -> None:
        statistics = np.linspace(0, 100, 1001)
        for values in (
            normal_pvalue(statistics, mean=5, variance=4),
            edgeworth_pvalue(statistics, mean=5, variance=4, skewness=1.2),
        ):
            self.assertTrue(np.all(np.isfinite(values)))
            self.assertTrue(np.all((values >= 0) & (values <= 1)))

    def test_approximations_broadcast_per_table_moments(self) -> None:
        statistics = np.asarray((0.0, 2.0, 5.0))
        means = np.asarray((0.0, 1.0, 4.0))
        variances = np.asarray((0.0, 1.0, 4.0))
        skewness = np.asarray((0.0, 0.5, 1.0))
        normal = normal_pvalue(statistics, means, variances)
        edgeworth = edgeworth_pvalue(
            statistics,
            means,
            variances,
            skewness,
        )
        self.assertEqual(normal.shape, statistics.shape)
        self.assertEqual(edgeworth.shape, statistics.shape)
        self.assertEqual(normal[0], 1.0)
        self.assertEqual(edgeworth[0], 1.0)
        self.assertTrue(np.all(np.isfinite(normal)))
        self.assertTrue(np.all(np.isfinite(edgeworth)))

    def test_invalid_stratum_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Stratum(5, 2, 2, 3)
        with self.assertRaises(ValueError):
            Stratum(-1, 0, 0, 0)

    def test_validation_grid_deduplicates_relabel_equivalents(self) -> None:
        configurations = validation_configurations("smoke")
        homogeneous = [
            item for item in configurations if item.family == "homogeneous"
        ]
        signatures = []
        for configuration in homogeneous:
            signatures.append(
                tuple(
                    (
                        item.n,
                        min(
                            min(item.r, item.n - item.r),
                            min(item.s, item.n - item.s),
                        ),
                        max(
                            min(item.r, item.n - item.r),
                            min(item.s, item.n - item.s),
                        ),
                    )
                    for item in configuration.strata
                )
            )
        self.assertEqual(len(signatures), len(set(signatures)))


if __name__ == "__main__":
    unittest.main()
