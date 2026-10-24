from __future__ import annotations

import json
import sys
import unittest
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from thesis_redesign_core import (  # noqa: E402
    build_manifests,
    change_matrix,
    construct_additive,
    margin,
    mutual_information,
    simulate_configuration,
    smoke_configuration_ids,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


def protocol() -> dict:
    return json.loads((ROOT / "experiments/THESIS_REDESIGN_PROTOCOL.json").read_text())


class ConstructionTests(unittest.TestCase):
    def test_change_matrices_preserve_margins(self) -> None:
        for shape in [(2, 2), (3, 5), (8, 8)]:
            for pattern in ["first", "rare", "spread"]:
                matrix = change_matrix(*shape, pattern)
                np.testing.assert_allclose(matrix.sum(axis=0), 0, atol=1e-14)
                np.testing.assert_allclose(matrix.sum(axis=1), 0, atol=1e-14)

    def test_additive_constructor_matches_tiny_and_regular_targets(self) -> None:
        rules = protocol()["population_tolerances"]
        row, column = margin(8, 0.999), margin(8, 0.999)
        for target in [0, 1e-5, 2.1e-4]:
            result = construct_additive(row, column, target, "first", rules)
            self.assertTrue(np.all(result.probability > 0))
            self.assertLessEqual(abs(result.achieved_mi - target), 1e-12 + 1e-8 * target)
            np.testing.assert_allclose(result.probability.sum(axis=1), row, atol=1e-12)
            np.testing.assert_allclose(result.probability.sum(axis=0), column, atol=1e-12)

    def test_direct_mi_is_zero_at_independence(self) -> None:
        row, column = margin(3, 0.7), margin(5, 0.8)
        self.assertLess(abs(mutual_information(np.outer(row, column))), 1e-15)

    def test_binary_table_is_independently_determined_by_one_cell(self) -> None:
        rules = protocol()["population_tolerances"]
        row, column = margin(2, 0.7), margin(2, 0.8)
        result = construct_additive(row, column, 0.02, "first", rules)
        x = result.probability[0, 0]
        rebuilt = np.array([[x, row[0] - x], [column[0] - x, 1 - row[0] - column[0] + x]])
        np.testing.assert_allclose(rebuilt, result.probability, atol=1e-14)
        self.assertAlmostEqual(mutual_information(rebuilt), 0.02, places=11)

    def test_additive_mi_is_monotone_and_curvature_identity_holds(self) -> None:
        row, column = margin(5, 0.7), margin(5, 0.8)
        h = change_matrix(5, 5, "first")
        base = np.outer(row, column)
        endpoint = float(np.min(base[h < 0] / -h[h < 0]))
        points = np.linspace(0, 0.8 * endpoint, 21)
        values = np.array([mutual_information(base + point * h) for point in points])
        self.assertTrue(np.all(np.diff(values) > 0))
        point = 0.3 * endpoint
        step = endpoint * 1e-4
        finite = (
            mutual_information(base + (point + step) * h)
            - 2 * mutual_information(base + point * h)
            + mutual_information(base + (point - step) * h)
        ) / step**2
        analytic = np.sum(h * h / (base + point * h))
        self.assertAlmostEqual(finite / analytic, 1.0, places=5)


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.display, cls.configurations, cls.populations, cls.arrays = build_manifests(protocol())

    def test_full_design_is_feasible_and_deduplicated(self) -> None:
        self.assertGreater(len(self.display), len(self.configurations))
        self.assertTrue(self.display["display_id"].is_unique)
        self.assertTrue(self.configurations["configuration_id"].is_unique)
        self.assertFalse(self.display["configuration_id"].isna().any())
        self.assertTrue((self.populations[["minimum_probability_p", "minimum_probability_q"]] > 0).all().all())

    def test_main_section_has_exact_declared_grid(self) -> None:
        main = self.display[self.display["section"].eq("main")]
        self.assertEqual(len(main), 4 * 3 * 9 * 6)
        self.assertEqual(set(main["mi_difference"]), {0, .001, .002, .005, .01, .02})

    def test_smoke_selection_covers_every_section(self) -> None:
        selected = smoke_configuration_ids(self.display)
        sections = set(self.display[self.display["configuration_id"].isin(selected)]["section"])
        self.assertEqual(sections, set(self.display["section"]))

    def test_n_one_is_recorded_as_invalid_not_an_exception(self) -> None:
        row = self.configurations[self.configurations["n_p"].eq(1)].iloc[0].to_dict()
        row["replicates"] = 10
        p, q = self.arrays[row["pair_id"]]
        result = simulate_configuration(
            {"configuration": row, "probability_p": p, "probability_q": q,
             "alpha": .05, "batch_size": 5}
        )
        self.assertEqual({entry["valid_rate"] for entry in result["cell_rows"]}, {0})
        self.assertEqual(result["paired_rows"][0]["neither_rejects"], 10)

    def test_constructed_inputs_obey_swap_and_relabelling_invariance(self) -> None:
        row = self.configurations[
            self.configurations["shape"].eq("3x3") & self.configurations["n_p"].eq(100)
        ].iloc[0]
        p, q = self.arrays[row["pair_id"]]
        rng = np.random.default_rng(12)
        count_p = rng.multinomial(100, p.ravel()).reshape(3, 3)
        count_q = rng.multinomial(100, q.ravel()).reshape(3, 3)
        original = differential_mi_pvalues(count_p, count_q, include_simple=False)
        swapped = differential_mi_pvalues(count_q, count_p, include_simple=False)
        permuted = differential_mi_pvalues(count_p[[2, 0, 1]][:, [1, 2, 0]], count_q[[2, 0, 1]][:, [1, 2, 0]], include_simple=False)
        self.assertAlmostEqual(float(original["statistic"]), -float(swapped["statistic"]), places=12)
        self.assertAlmostEqual(float(original["normal_p_value"]), float(permuted["normal_p_value"]), places=12)
        self.assertAlmostEqual(float(original["expanded_welch_p_value"]), float(permuted["expanded_welch_p_value"]), places=12)

    def test_vector_batch_matches_scalar_and_degenerate_tables_do_not_warn(self) -> None:
        tables_p = np.array([[[5, 0], [0, 5]], [[10, 0], [0, 0]]])
        tables_q = np.array([[[4, 1], [1, 4]], [[10, 0], [0, 0]]])
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            batch = differential_mi_pvalues(tables_p, tables_q, include_simple=False)
        for index in range(2):
            scalar = differential_mi_pvalues(tables_p[index], tables_q[index], include_simple=False)
            for key in ["statistic", "normal_p_value", "expanded_welch_p_value"]:
                np.testing.assert_allclose(batch[key][index], scalar[key], equal_nan=True)


if __name__ == "__main__":
    unittest.main()
