"""Pre-specified validation scenarios."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .distributions import (
    marginal_probabilities,
    mutual_information_probability,
    table_with_target_mi,
)


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    family: str
    rows: int
    columns: int
    n_p: int
    n_q: int
    margin_p: str
    margin_q: str
    target_mi_p: float
    target_mi_q: float
    regular: bool
    pattern_p: str = "ordinal"
    pattern_q: str = "ordinal"

    def to_dict(self) -> dict[str, str | int | float | bool]:
        return asdict(self)


def build_distributions(scenario: Scenario) -> tuple[np.ndarray, np.ndarray, dict]:
    row_p = marginal_probabilities(scenario.rows, scenario.margin_p)
    col_p = marginal_probabilities(scenario.columns, scenario.margin_p)
    row_q = marginal_probabilities(scenario.rows, scenario.margin_q)
    col_q = marginal_probabilities(scenario.columns, scenario.margin_q)

    probability_p, association_p = table_with_target_mi(
        row_p, col_p, scenario.target_mi_p, pattern=scenario.pattern_p
    )
    if scenario.family == "strong_null":
        probability_q = probability_p.copy()
        association_q = association_p
    else:
        probability_q, association_q = table_with_target_mi(
            row_q, col_q, scenario.target_mi_q, pattern=scenario.pattern_q
        )

    mi_p = mutual_information_probability(probability_p)
    mi_q = mutual_information_probability(probability_q)
    diagnostics = {
        "true_mi_p": mi_p,
        "true_mi_q": mi_q,
        "true_delta": mi_p - mi_q,
        "association_p": association_p,
        "association_q": association_q,
        "min_probability_p": float(probability_p.min()),
        "min_probability_q": float(probability_q.min()),
        "min_expected_p": float(scenario.n_p * probability_p.min()),
        "min_expected_q": float(scenario.n_q * probability_q.min()),
        "different_distributions_l1": float(np.abs(probability_p - probability_q).sum()),
    }
    return probability_p, probability_q, diagnostics


def all_scenarios() -> list[Scenario]:
    """Return broad null and power cases, including expected failure boundaries."""
    return [
        Scenario("strong_2x2_bal_100", "strong_null", 2, 2, 100, 100, "balanced", "balanced", 0.05, 0.05, True),
        Scenario("strong_3x3_strong_250", "strong_null", 3, 3, 250, 250, "strong", "strong", 0.10, 0.10, True),
        Scenario("strong_5x5_mild_500", "strong_null", 5, 5, 500, 500, "mild", "mild", 0.10, 0.10, True),
        Scenario("weak_2x2_bal_strong_100_100", "weak_null", 2, 2, 100, 100, "balanced", "strong", 0.05, 0.05, True),
        Scenario("weak_2x2_bal_strong_100_250", "weak_null", 2, 2, 100, 250, "balanced", "strong", 0.05, 0.05, True),
        Scenario("weak_3x3_bal_strong_200_200", "weak_null", 3, 3, 200, 200, "balanced", "strong", 0.10, 0.10, True),
        Scenario("weak_3x3_bal_strong_150_400", "weak_null", 3, 3, 150, 400, "balanced", "strong", 0.05, 0.05, True),
        Scenario("weak_5x5_bal_strong_500_500", "weak_null", 5, 5, 500, 500, "balanced", "strong", 0.10, 0.10, True),
        Scenario("weak_5x5_mild_strong_300_800", "weak_null", 5, 5, 300, 800, "mild", "strong", 0.10, 0.10, True),
        Scenario("weak_10x10_bal_strong_1000", "weak_null", 10, 10, 1000, 1000, "balanced", "strong", 0.10, 0.10, False),
        Scenario("near_2x2_bal_strong_500", "near_boundary", 2, 2, 500, 500, "balanced", "strong", 0.002, 0.002, False),
        Scenario("near_5x5_bal_strong_1000", "near_boundary", 5, 5, 1000, 1000, "balanced", "strong", 0.005, 0.005, False),
        Scenario("power_2x2_bal_strong_200", "power", 2, 2, 200, 200, "balanced", "strong", 0.05, 0.10, True),
        Scenario("power_3x3_bal_strong_300", "power", 3, 3, 300, 300, "balanced", "strong", 0.05, 0.10, True),
        Scenario("power_5x5_mild_strong_600", "power", 5, 5, 600, 600, "mild", "strong", 0.05, 0.10, True),
    ]


def adversarial_scenarios() -> list[Scenario]:
    """Post-protocol checks for rectangular tables and different interactions."""
    return [
        Scenario("adv_strong_3x5_cyclic_400", "strong_null", 3, 5, 400, 400, "mild", "mild", 0.08, 0.08, True, "cyclic", "cyclic"),
        Scenario("adv_weak_2x3_bal_strong_150_300", "weak_null", 2, 3, 150, 300, "balanced", "strong", 0.05, 0.05, True, "ordinal", "cyclic"),
        Scenario("adv_weak_3x5_bal_mild_300_600", "weak_null", 3, 5, 300, 600, "balanced", "mild", 0.08, 0.08, True, "cyclic", "checkerboard"),
        Scenario("adv_weak_5x10_mild_strong_1000_2000", "weak_null", 5, 10, 1000, 2000, "mild", "strong", 0.10, 0.10, False, "checkerboard", "cyclic"),
        Scenario("adv_weak_10x10_bal_mild_2000_4000", "weak_null", 10, 10, 2000, 4000, "balanced", "mild", 0.15, 0.15, True, "cyclic", "checkerboard"),
        Scenario("adv_weak_5x5_same_margin_structure", "weak_null", 5, 5, 600, 600, "mild", "mild", 0.10, 0.10, True, "ordinal", "cyclic"),
        Scenario("adv_weak_10x10_same_margin_structure", "weak_null", 10, 10, 2000, 2000, "strong", "strong", 0.10, 0.10, False, "ordinal", "cyclic"),
    ]


def power_curve_scenarios() -> list[Scenario]:
    """Post-protocol checks for power monotonicity in effect and sample size."""
    return [
        Scenario("curve_effect_d02_n300", "power", 3, 3, 300, 300, "balanced", "strong", 0.05, 0.07, True),
        Scenario("curve_effect_d05_n300", "power", 3, 3, 300, 300, "balanced", "strong", 0.05, 0.10, True),
        Scenario("curve_effect_d10_n300", "power", 3, 3, 300, 300, "balanced", "strong", 0.05, 0.15, True),
        Scenario("curve_sample_d05_n150", "power", 3, 3, 150, 150, "balanced", "strong", 0.05, 0.10, True),
        Scenario("curve_sample_d05_n600", "power", 3, 3, 600, 600, "balanced", "strong", 0.05, 0.10, True),
    ]


def scenarios_for_profile(profile: str) -> list[Scenario]:
    scenarios = all_scenarios()
    if profile == "smoke":
        wanted = {
            "strong_2x2_bal_100",
            "weak_2x2_bal_strong_100_250",
            "near_2x2_bal_strong_500",
            "power_2x2_bal_strong_200",
        }
        return [scenario for scenario in scenarios if scenario.scenario_id in wanted]
    if profile == "screen":
        return scenarios
    if profile == "decisive":
        wanted = {
            "strong_2x2_bal_100",
            "strong_3x3_strong_250",
            "strong_5x5_mild_500",
            "weak_2x2_bal_strong_100_100",
            "weak_2x2_bal_strong_100_250",
            "weak_3x3_bal_strong_200_200",
            "weak_3x3_bal_strong_150_400",
            "weak_5x5_bal_strong_500_500",
            "weak_5x5_mild_strong_300_800",
            "weak_10x10_bal_strong_1000",
            "near_2x2_bal_strong_500",
            "near_5x5_bal_strong_1000",
            "power_2x2_bal_strong_200",
            "power_3x3_bal_strong_300",
            "power_5x5_mild_strong_600",
        }
        return [scenario for scenario in scenarios if scenario.scenario_id in wanted]
    if profile == "adversarial":
        return adversarial_scenarios()
    if profile == "power_curve":
        return power_curve_scenarios()
    raise ValueError(f"Unknown profile: {profile}")
