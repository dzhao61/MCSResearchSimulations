from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parent / "DifferentialMI/src"))

from differential_mi.statistics import influence_variance
from welch_differential_mi.welch import differential_mi_pvalues


def exactly_constant(table):
    row = table.sum(axis=1).astype(object)
    column = table.sum(axis=0).astype(object)
    a, b = np.argwhere(table > 0)[0]
    return all(int(table[i, j]) * int(row[a]) * int(column[b])
               == int(table[a, b]) * int(row[i]) * int(column[j])
               for i, j in np.argwhere(table > 0))


class NumericalDegeneracyTests(unittest.TestCase):
    def test_audited_residual_does_not_define_component_df(self):
        p = np.array([[1, 1], [4, 4]])
        q = np.array([[7, 0], [0, 3]])
        result = differential_mi_pvalues(p, q)
        self.assertEqual(result["influence_variance_p"], 0)
        self.assertEqual(result["variance_influence_variance_p"], 0)
        self.assertTrue(np.isnan(result["expanded_component_degrees_of_freedom_p"]))
        self.assertFalse(result["expanded_valid"])
        self.assertTrue(result["base_valid"])
        self.assertTrue(result["simple_valid"])

    def test_constant_nonzero_mi_and_empty_margins(self):
        for table in (np.diag([3, 3, 3]), np.array([[0, 0], [1, 9]]),
                      np.array([[0, 3, 3], [3, 0, 3], [3, 3, 0]])):
            with self.subTest(table=table.tolist()):
                self.assertTrue(exactly_constant(table))
                self.assertEqual(influence_variance(table), 0)
                result = differential_mi_pvalues(table, table)
                self.assertEqual(result["variance_influence_variance_p"], 0)
                self.assertFalse(result["expanded_valid"])

    def test_exhaustive_small_tables_are_label_invariant(self):
        tables = []
        for n in range(2, 21):
            for a in range(n + 1):
                for b in range(n - a + 1):
                    for c in range(n - a - b + 1):
                        tables.append([[a, b], [c, n - a - b - c]])
        p = np.asarray(tables)
        q = np.broadcast_to([[7, 1], [2, 8]], p.shape)
        baseline = differential_mi_pvalues(p, q)
        constant = np.array([exactly_constant(table) for table in p])
        np.testing.assert_array_equal(baseline["influence_variance_p"] == 0, constant)
        self.assertFalse(np.any(baseline["expanded_valid"][constant]))
        for left, right in ((p.swapaxes(-1, -2), q.swapaxes(-1, -2)),
                            (p[:, ::-1, :], q[:, ::-1, :]),
                            (p[:, :, ::-1], q[:, :, ::-1]), (q, p)):
            transformed = differential_mi_pvalues(left, right)
            for field in ("base_valid", "simple_valid", "expanded_valid"):
                np.testing.assert_array_equal(transformed[field], baseline[field])
            for field in ("normal_p_value", "expanded_welch_p_value"):
                np.testing.assert_allclose(transformed[field], baseline[field],
                                           atol=2e-13, rtol=2e-11, equal_nan=True)
                np.testing.assert_array_equal(transformed[field] <= .05, baseline[field] <= .05)

    def test_near_independence_is_not_rounded_to_zero(self):
        table = np.full((2, 2), 10**12, dtype=np.int64)
        table += [[1, -1], [-1, 1]]
        self.assertFalse(exactly_constant(table))
        variance = influence_variance(table)
        self.assertGreater(variance, 0)
        self.assertAlmostEqual(variance / 1e-24, 1, delta=3e-4)
        values = differential_mi_pvalues(table, np.array([[7, 1], [2, 8]]))
        self.assertTrue(values["expanded_valid"])

    def test_large_exact_counts_do_not_overflow_cross_products(self):
        table = np.array([[1, 1], [4, 4]], dtype=np.int64) * 2**40
        self.assertEqual(influence_variance(table), 0)

    def test_arbitrary_batch_shape_and_scalar_agree(self):
        p = np.array([[[1, 1], [4, 4]], [[4, 1], [2, 3]]]).reshape(1, 2, 2, 2)
        q = np.broadcast_to([[7, 0], [0, 3]], p.shape)
        batch = differential_mi_pvalues(p, q)
        for i in range(2):
            scalar = differential_mi_pvalues(p[0, i], q[0, i])
            for field in batch:
                np.testing.assert_allclose(batch[field][0, i], scalar[field], equal_nan=True)


if __name__ == "__main__":
    unittest.main()
