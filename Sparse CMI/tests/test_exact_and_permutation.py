from __future__ import annotations

import itertools
import unittest

import numpy as np

from sparse_cmi.exact_convolution import exact_conditional_distribution
from sparse_cmi.hypergeom import stratum_null
from sparse_cmi.models import Stratum
from sparse_cmi.moments import aggregate_moments
from sparse_cmi.permutation import sample_conditional_g2


class ExactAndPermutationTests(unittest.TestCase):
    def test_convolution_matches_cartesian_product(self) -> None:
        strata = [Stratum(5, 2, 2, 1), Stratum(6, 2, 3, 1)]
        exact = exact_conditional_distribution(strata, max_states=1000)
        nulls = [stratum_null(item) for item in strata]
        brute: dict[float, float] = {}
        for indices in itertools.product(*(range(len(item.support)) for item in nulls)):
            value = round(
                sum(nulls[j].g_values[index] for j, index in enumerate(indices)),
                12,
            )
            probability = np.prod(
                [nulls[j].probabilities[index] for j, index in enumerate(indices)]
            )
            brute[value] = brute.get(value, 0.0) + float(probability)
        self.assertEqual(exact.values.size, len(brute))
        brute_values = np.asarray(sorted(brute))
        brute_probabilities = np.asarray([brute[value] for value in brute_values])
        np.testing.assert_allclose(exact.values, brute_values, atol=2e-12)
        np.testing.assert_allclose(
            exact.probabilities,
            brute_probabilities,
            atol=1e-14,
        )

    def test_aggregate_moments_match_exact_convolution(self) -> None:
        strata = [
            Stratum(5, 2, 2, 1),
            Stratum(6, 2, 3, 1),
            Stratum(4, 1, 2, 0),
        ]
        moments = aggregate_moments(strata)
        exact = exact_conditional_distribution(strata, max_states=5000)
        mean = float(np.dot(exact.probabilities, exact.values))
        variance = float(
            np.dot(exact.probabilities, (exact.values - mean) ** 2)
        )
        third = float(
            np.dot(exact.probabilities, (exact.values - mean) ** 3)
        )
        self.assertAlmostEqual(moments.mean, mean, places=10)
        self.assertAlmostEqual(moments.variance, variance, places=10)
        self.assertAlmostEqual(moments.third_cumulant, third, places=9)

    def test_direct_sampler_matches_exact_distribution(self) -> None:
        strata = [Stratum(5, 2, 2, 1)]
        exact = exact_conditional_distribution(strata)
        draws = sample_conditional_g2(
            strata,
            samples=200_000,
            rng=np.random.default_rng(12345),
        )
        for value, probability in zip(
            exact.values, exact.probabilities, strict=True
        ):
            empirical = np.mean(np.isclose(draws, value, atol=1e-10))
            self.assertLess(abs(empirical - probability), 0.005)

    def test_hypergeometric_is_observation_permutation_distribution(self) -> None:
        n, r, s = 6, 2, 3
        counts = {a: 0 for a in range(max(0, r + s - n), min(r, s) + 1)}
        for one_positions in itertools.combinations(range(n), s):
            y = np.zeros(n, dtype=int)
            y[list(one_positions)] = 1
            counts[int(y[:r].sum())] += 1
        total = sum(counts.values())
        stratum = Stratum(n, r, s, 1)
        null = stratum_null(stratum)
        empirical = np.asarray([counts[int(a)] / total for a in null.support])
        np.testing.assert_allclose(empirical, null.probabilities, atol=1e-15)


if __name__ == "__main__":
    unittest.main()
