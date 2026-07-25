from __future__ import annotations

import math
import unittest

import numpy as np

from sparse_cmi.hypergeom import stratum_null
from sparse_cmi.models import Stratum
from sparse_cmi.moments import aggregate_moments, stratum_moments
from sparse_cmi.statistic import g2_for_a, observed_cmi_nats, observed_g2
from sparse_cmi.tables import build_binary_strata


class CoreTests(unittest.TestCase):
    def test_support_and_probabilities_match_combinatorics(self) -> None:
        stratum = Stratum(8, 3, 4, 1)
        null = stratum_null(stratum)
        expected = np.asarray(
            [
                math.comb(4, int(a))
                * math.comb(4, 3 - int(a))
                / math.comb(8, 3)
                for a in null.support
            ]
        )
        np.testing.assert_allclose(null.probabilities, expected, atol=1e-15)
        self.assertAlmostEqual(float(null.probabilities.sum()), 1.0, places=14)

    def test_independence_and_maximal_binary_association(self) -> None:
        self.assertAlmostEqual(g2_for_a(20, 10, 10, 5), 0.0, places=14)
        self.assertAlmostEqual(
            g2_for_a(20, 10, 10, 10),
            40.0 * math.log(2.0),
            places=12,
        )

    def test_raw_arrays_are_built_into_strata(self) -> None:
        x = [0, 1, 1, 0, 1]
        y = [1, 1, 0, 0, 1]
        z = ["a", "a", "a", "b", "b"]
        strata = build_binary_strata(x, y, z)
        self.assertEqual(
            strata,
            [
                Stratum(3, 2, 2, 1, "a"),
                Stratum(2, 1, 1, 1, "b"),
            ],
        )

    def test_moments_match_direct_weighted_calculation(self) -> None:
        stratum = Stratum(7, 3, 4, 2)
        null = stratum_null(stratum)
        moments = stratum_moments(stratum)
        mean = np.dot(null.probabilities, null.g_values)
        centered = null.g_values - mean
        self.assertAlmostEqual(moments.mean, float(mean), places=14)
        self.assertAlmostEqual(
            moments.variance,
            float(np.dot(null.probabilities, centered**2)),
            places=14,
        )
        self.assertAlmostEqual(
            moments.third_cumulant,
            float(np.dot(null.probabilities, centered**3)),
            places=14,
        )

    def test_degenerate_strata_have_zero_statistic_and_variance(self) -> None:
        for stratum in (
            Stratum(0, 0, 0, 0),
            Stratum(5, 0, 2, 0),
            Stratum(5, 3, 5, 3),
        ):
            self.assertEqual(observed_g2([stratum]), 0.0)
            self.assertEqual(stratum_moments(stratum).variance, 0.0)

    def test_cmi_nats_scaling(self) -> None:
        strata = [Stratum(20, 10, 10, 10)]
        self.assertAlmostEqual(observed_cmi_nats(strata), math.log(2.0), places=14)
        self.assertAlmostEqual(
            observed_g2(strata),
            2 * 20 * observed_cmi_nats(strata),
            places=14,
        )

    def test_swap_and_binary_relabel_invariance(self) -> None:
        original = Stratum(11, 4, 7, 3)
        swap_xy = Stratum(11, 7, 4, 3)
        relabel_x = Stratum(11, 7, 7, 4)
        relabel_y = Stratum(11, 4, 4, 1)
        statistics = [
            observed_g2([item])
            for item in (original, swap_xy, relabel_x, relabel_y)
        ]
        np.testing.assert_allclose(statistics, statistics[0], atol=1e-12)
        moments = [
            aggregate_moments([item])
            for item in (original, swap_xy, relabel_x, relabel_y)
        ]
        np.testing.assert_allclose(
            [item.mean for item in moments],
            moments[0].mean,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            [item.variance for item in moments],
            moments[0].variance,
            atol=1e-12,
        )


if __name__ == "__main__":
    unittest.main()

