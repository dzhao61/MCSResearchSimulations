"""Independent numerical checks of the thesis's variance sensitivity."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.stats import norm, t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT.parent / "DifferentialMI" / "src"))

from welch_differential_mi.welch import (
    _variance_influence_component_df,
    differential_mi_pvalues,
)


def mi_and_variance(probability: np.ndarray) -> tuple[float, float]:
    """Evaluate the population functionals without using the test implementation."""
    row = probability.sum(axis=1, keepdims=True)
    column = probability.sum(axis=0, keepdims=True)
    pointwise = np.log(probability / (row * column))
    mi = float(np.sum(probability * pointwise))
    variance = float(np.sum(probability * (pointwise - mi) ** 2))
    return mi, variance


def finite_difference_sensitivities(probability: np.ndarray) -> np.ndarray:
    epsilon = 1e-6
    sensitivities = np.zeros_like(probability)
    for cell in np.ndindex(probability.shape):
        point_mass = np.zeros_like(probability)
        point_mass[cell] = 1.0
        plus = (1.0 - epsilon) * probability + epsilon * point_mass
        minus = (1.0 + epsilon) * probability - epsilon * point_mass
        sensitivities[cell] = (
            mi_and_variance(plus)[1] - mi_and_variance(minus)[1]
        ) / (2.0 * epsilon)
    return sensitivities


def direct_expanded_values(table: np.ndarray) -> tuple[float, float, float, float]:
    """Independently substitute one table into the thesis equations."""
    probability = table / table.sum()
    mi, variance = mi_and_variance(probability)
    pointwise = np.log(
        probability
        / (
            probability.sum(axis=1, keepdims=True)
            * probability.sum(axis=0, keepdims=True)
        )
    )
    row_probability = probability.sum(axis=1)
    column_probability = probability.sum(axis=0)
    row_mean = np.sum(probability * pointwise, axis=1) / row_probability
    column_mean = np.sum(probability * pointwise, axis=0) / column_probability
    sensitivity = (
        (pointwise - mi) ** 2
        - variance
        + 2.0 * (pointwise - row_mean[:, None] - column_mean[None, :] + mi)
    )
    sensitivity_mean = float(np.sum(probability * sensitivity))
    tau_squared = float(
        np.sum(probability * (sensitivity - sensitivity_mean) ** 2)
    )
    component_df = 2.0 * table.sum() * variance**2 / tau_squared
    return mi, variance, tau_squared, component_df


class ThesisDerivationAudit(unittest.TestCase):
    def test_mi_influence_matches_direct_finite_differences(self) -> None:
        probability = np.array([[0.36, 0.14], [0.09, 0.41]])
        mi, _ = mi_and_variance(probability)
        row = probability.sum(axis=1, keepdims=True)
        column = probability.sum(axis=0, keepdims=True)
        expected = np.log(probability / (row * column)) - mi
        epsilon = 1e-6
        for cell in np.ndindex(probability.shape):
            point_mass = np.zeros_like(probability)
            point_mass[cell] = 1.0
            plus = (1.0 - epsilon) * probability + epsilon * point_mass
            minus = (1.0 + epsilon) * probability - epsilon * point_mass
            derivative = (mi_and_variance(plus)[0] - mi_and_variance(minus)[0]) / (2 * epsilon)
            self.assertAlmostEqual(derivative, float(expected[cell]), places=8)

    def test_variance_influence_matches_direct_finite_differences(self) -> None:
        for probability in (
            np.array([[0.36, 0.14], [0.09, 0.41]]),
            np.array(
                [[0.28, 0.09, 0.07], [0.08, 0.17, 0.06], [0.04, 0.10, 0.11]]
            ),
        ):
            with self.subTest(shape=probability.shape):
                probability = probability / probability.sum()
                _, variance = mi_and_variance(probability)
                sensitivity = finite_difference_sensitivities(probability)
                self.assertAlmostEqual(float(np.sum(probability * sensitivity)), 0.0, places=8)
                expected_tau_squared = float(np.sum(probability * sensitivity**2))
                sample_size = 1000.0
                component_df, tau_squared = _variance_influence_component_df(
                    probability * sample_size, np.asarray(variance)
                )
                self.assertAlmostEqual(
                    float(tau_squared), expected_tau_squared, delta=2e-8
                )
                self.assertAlmostEqual(
                    float(component_df),
                    2.0 * sample_size * variance**2 / expected_tau_squared,
                    places=6,
                )

    def test_positive_mi_variance_need_not_give_positive_sensitivity_variance(self) -> None:
        # The symmetric 2x2 family has an interior stationary point of V.
        strength = 0.8335565596009646
        probability = np.array(
            [
                [(1 + strength) / 4, (1 - strength) / 4],
                [(1 - strength) / 4, (1 + strength) / 4],
            ]
        )
        mi, variance = mi_and_variance(probability)
        sensitivity = finite_difference_sensitivities(probability)
        self.assertGreater(mi, 0.4)
        self.assertGreater(variance, 0.4)
        self.assertLess(float(np.sum(probability * sensitivity**2)), 1e-16)

    def test_independence_second_order_expansion(self) -> None:
        row = np.array([0.6, 0.4])
        column = np.array([0.5, 0.3, 0.2])
        probability = np.outer(row, column)
        direction = np.array([[0.08, -0.03, -0.01], [-0.04, 0.02, -0.02]])
        self.assertAlmostEqual(float(direction.sum()), 0.0)

        row_change = direction.sum(axis=1)
        column_change = direction.sum(axis=0)
        residual = (
            direction
            - column[None, :] * row_change[:, None]
            - row[:, None] * column_change[None, :]
        )
        entropy_hessian = float(
            np.sum(direction**2 / probability)
            - np.sum(row_change**2 / row)
            - np.sum(column_change**2 / column)
        )
        residual_form = float(np.sum(residual**2 / probability))
        self.assertAlmostEqual(entropy_hessian, residual_form, places=14)

        epsilon = 1e-4
        mi_zero = mi_and_variance(probability)[0]
        mi_plus = mi_and_variance(probability + epsilon * direction)[0]
        mi_minus = mi_and_variance(probability - epsilon * direction)[0]
        first_derivative = (mi_plus - mi_minus) / (2.0 * epsilon)
        second_derivative = (mi_plus - 2.0 * mi_zero + mi_minus) / epsilon**2
        self.assertAlmostEqual(first_derivative, 0.0, delta=1e-10)
        self.assertAlmostEqual(second_derivative, residual_form, delta=1e-7)

    def test_worked_example_matches_displayed_values(self) -> None:
        table_p = np.array([[35, 10, 5], [10, 20, 5], [5, 5, 10]], dtype=float)
        table_q = np.array([[30, 5, 5], [5, 30, 5], [5, 5, 10]], dtype=float)
        mi_p, variance_p, tau_p, df_p = direct_expanded_values(table_p)
        mi_q, variance_q, tau_q, df_q = direct_expanded_values(table_q)

        corrected_delta = (mi_p - 4.0 / (2.0 * table_p.sum())) - (
            mi_q - 4.0 / (2.0 * table_q.sum())
        )
        standard_error = np.sqrt(
            variance_p / table_p.sum() + variance_q / table_q.sum()
        )
        statistic = corrected_delta / standard_error
        normal_p = 2.0 * norm.sf(abs(statistic))
        component_p = variance_p / table_p.sum()
        component_q = variance_q / table_q.sum()
        combined_df = (component_p + component_q) ** 2 / (
            component_p**2 / df_p + component_q**2 / df_q
        )
        expanded_p = 2.0 * t.sf(abs(statistic), df=combined_df)

        displayed = (
            (mi_p, 0.13693),
            (mi_q, 0.25848),
            (corrected_delta, -0.12059),
            (variance_p, 0.27189),
            (variance_q, 0.43371),
            (standard_error, 0.08323),
            (statistic, -1.44898),
            (normal_p, 0.14734),
            (tau_p, 0.93212),
            (tau_q, 0.82035),
            (df_p, 16.65),
            (df_q, 45.86),
            (combined_df, 59.03),
            (expanded_p, 0.15264),
        )
        for actual, expected in displayed:
            places = 2 if abs(expected) >= 10 else 5
            self.assertAlmostEqual(actual, expected, places=places)

        implementation = differential_mi_pvalues(table_p, table_q)
        self.assertAlmostEqual(float(implementation["delta_corrected"]), corrected_delta)
        self.assertAlmostEqual(float(implementation["standard_error"]), standard_error)
        self.assertAlmostEqual(
            float(implementation["expanded_welch_degrees_of_freedom"]), combined_df
        )
        self.assertAlmostEqual(
            float(implementation["expanded_welch_p_value"]), expanded_p
        )

    def test_worked_population_pair_has_stated_margins_and_mi(self) -> None:
        probability_p = np.array(
            [
                [0.532729447578475, 0.16727055242152497],
                [0.16727055242152497, 0.13272944757847507],
            ]
        )
        probability_q = np.array(
            [
                [0.681745873125986, 0.11825412687401415],
                [0.11825412687401415, 0.0817458731259858],
            ]
        )
        np.testing.assert_allclose(probability_p.sum(axis=1), [0.7, 0.3])
        np.testing.assert_allclose(probability_p.sum(axis=0), [0.7, 0.3])
        np.testing.assert_allclose(probability_q.sum(axis=1), [0.8, 0.2])
        np.testing.assert_allclose(probability_q.sum(axis=0), [0.8, 0.2])
        self.assertAlmostEqual(mi_and_variance(probability_p)[0], 0.02, places=14)
        self.assertAlmostEqual(mi_and_variance(probability_q)[0], 0.03, places=14)


if __name__ == "__main__":
    unittest.main()
