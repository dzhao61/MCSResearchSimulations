from __future__ import annotations

import unittest

import numpy as np

from sparse_cmi.jidt import (
    blockwise_jidt_orderings,
    jidt_reconstructed_condition_indices,
    strata_to_observations,
)
from sparse_cmi.models import Stratum


class JIDTOrderingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.strata = [
            Stratum(5, 2, 3, 1),
            Stratum(7, 5, 2, 2),
            Stratum(4, 1, 1, 0),
        ]

    def test_observation_reconstruction_preserves_tables(self) -> None:
        x_values, y_values, z_values = strata_to_observations(self.strata)
        self.assertEqual(x_values.size, sum(item.n for item in self.strata))
        for z_index, stratum in enumerate(self.strata):
            mask = z_values == z_index
            self.assertEqual(int(mask.sum()), stratum.n)
            self.assertEqual(int(x_values[mask].sum()), stratum.r)
            self.assertEqual(int(y_values[mask].sum()), stratum.s)
            self.assertEqual(
                int(np.dot(x_values[mask], y_values[mask])),
                stratum.a_observed,
            )

    def test_blockwise_orderings_never_cross_condition_groups(self) -> None:
        groups = jidt_reconstructed_condition_indices(self.strata)
        orderings = blockwise_jidt_orderings(
            self.strata,
            permutations=100,
            rng=np.random.default_rng(5030),
        )
        expected = np.arange(orderings.shape[1])
        for ordering in orderings:
            np.testing.assert_array_equal(np.sort(ordering), expected)
            for indices in groups:
                np.testing.assert_array_equal(
                    np.sort(ordering[indices]),
                    indices,
                )


if __name__ == "__main__":
    unittest.main()

