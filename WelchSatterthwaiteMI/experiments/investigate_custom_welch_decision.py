#!/usr/bin/env python3
"""Cross sample allocation and population shape to audit Custom Welch routing."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

from differential_mi.random_validation import (  # noqa: E402
    RandomScenario,
    generate_random_scenarios,
    scenario_diagnostics,
)
from run_supervisor_experiment import (  # noqa: E402
    DEFAULT_SCENARIO_SEED,
    REGIMES,
    _regime_for,
    generate_adversarial_scenarios,
    generate_expected_count_stress_scenarios,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402


ALPHAS = (0.05, 0.01)
RATIOS = (1, 2, 3, 4, 6, 10, 20)
AUDIT_SHAPES = ((2, 2), (3, 3), (4, 6), (5, 10), (10, 10), (20, 20))
COHORT_SEEDS = {
    "development": DEFAULT_SCENARIO_SEED,
    "holdout": DEFAULT_SCENARIO_SEED + 10_000,
}
SIMULATION_SEED = 2_026_080_601
BOOTSTRAP_SEED = 2_026_080_602


@dataclass(frozen=True)
class Allocation:
    cohort: str
    scenario: RandomScenario
    ratio: int
    smaller_group: str
    n_p: int
    n_q: int
    seed: int

    @property
    def allocation_id(self) -> str:
        return (
            f"{self.cohort}__{self.scenario.scenario_id}"
            f"__r{self.ratio}__{self.smaller_group}"
        )


RULE_LABELS = {
    "normal": "Always Normal Wald",
    "expanded_no_fallback": "Always Expanded Welch",
    "expanded_fallback": "Expanded with Wald fallback",
    "ratio_ge_2": "Expanded if ratio >= 2",
    "ratio_ge_3": "Expanded if ratio >= 3",
    "ratio_ge_4": "Expanded if ratio >= 4",
    "ratio_ge_6": "Expanded if ratio >= 6",
    "ratio_ge_10": "Expanded if ratio >= 10",
    "ratio_ge_4_margin_ge_1": "Ratio >= 4 and minimum margin >= 1",
    "ratio_ge_4_margin_ge_2": "Ratio >= 4 and minimum margin >= 2",
    "ratio_ge_4_margin_ge_5": "Ratio >= 4 and minimum margin >= 5",
    "ratio_ge_4_small_share_ge_50": "Ratio >= 4 and smaller-sample share >= 0.50",
    "ratio_ge_4_small_share_ge_60": "Ratio >= 4 and smaller-sample share >= 0.60",
    "ratio_ge_4_small_share_ge_70": "Ratio >= 4 and smaller-sample share >= 0.70",
    "ratio_ge_4_margin_ge_2_share_ge_50": (
        "Ratio >= 4, minimum margin >= 2, and smaller-sample share >= 0.50"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=3_000)
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "custom_decision_audit",
    )
    parser.add_argument(
        "--shape-limit",
        type=int,
        help="Use the first N audit shapes for a smoke run.",
    )
    return parser.parse_args()


def _cohort_scenarios(seed: int, shape_limit: int | None) -> list[RandomScenario]:
    scenarios = generate_random_scenarios(seed)
    scenarios.extend(generate_expected_count_stress_scenarios(seed + 1))
    scenarios.extend(generate_adversarial_scenarios(seed + 2))
    shapes = AUDIT_SHAPES[:shape_limit] if shape_limit else AUDIT_SHAPES
    selected = [
        scenario
        for scenario in scenarios
        if (scenario.rows, scenario.columns) in shapes
    ]
    expected = len(shapes) * 18
    if len(selected) != expected:
        raise RuntimeError(f"Expected {expected} scenarios, found {len(selected)}.")
    return selected


def _allocations(shape_limit: int | None) -> list[Allocation]:
    specifications: list[tuple[str, RandomScenario, int, str, int, int]] = []
    for cohort, cohort_seed in COHORT_SEEDS.items():
        for scenario in _cohort_scenarios(cohort_seed, shape_limit):
            n_small = min(scenario.n_p, scenario.n_q)
            specifications.append(
                (cohort, scenario, 1, "equal", n_small, n_small)
            )
            for ratio in RATIOS[1:]:
                specifications.extend(
                    (
                        (
                            cohort,
                            scenario,
                            ratio,
                            "p",
                            n_small,
                            ratio * n_small,
                        ),
                        (
                            cohort,
                            scenario,
                            ratio,
                            "q",
                            ratio * n_small,
                            n_small,
                        ),
                    )
                )
    children = np.random.SeedSequence(SIMULATION_SEED).spawn(len(specifications))
    return [
        Allocation(
            cohort=cohort,
            scenario=scenario,
            ratio=ratio,
            smaller_group=smaller_group,
            n_p=n_p,
            n_q=n_q,
            seed=int(child.generate_state(1)[0]),
        )
        for (
            cohort,
            scenario,
            ratio,
            smaller_group,
            n_p,
            n_q,
        ), child in zip(specifications, children)
    ]


def _minimum_observed_margin(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> np.ndarray:
    minima = (
        table_p.sum(axis=-1).min(axis=-1),
        table_p.sum(axis=-2).min(axis=-1),
        table_q.sum(axis=-1).min(axis=-1),
        table_q.sum(axis=-2).min(axis=-1),
    )
    return np.minimum.reduce(minima)


def _routes(
    ratio: int,
    minimum_margin: np.ndarray,
    smaller_sample_share: np.ndarray,
) -> dict[str, np.ndarray]:
    size = minimum_margin.size
    always = np.ones(size, dtype=bool)
    never = np.zeros(size, dtype=bool)
    ratio_routes = {
        f"ratio_ge_{threshold}": (
            always if ratio >= threshold else never
        )
        for threshold in (2, 3, 4, 6, 10)
    }
    ratio_ge_4 = ratio >= 4
    return {
        "normal": never,
        "expanded_fallback": always,
        **ratio_routes,
        "ratio_ge_4_margin_ge_1": ratio_ge_4 & (minimum_margin >= 1),
        "ratio_ge_4_margin_ge_2": ratio_ge_4 & (minimum_margin >= 2),
        "ratio_ge_4_margin_ge_5": ratio_ge_4 & (minimum_margin >= 5),
        "ratio_ge_4_small_share_ge_50": (
            ratio_ge_4 & (smaller_sample_share >= 0.50)
        ),
        "ratio_ge_4_small_share_ge_60": (
            ratio_ge_4 & (smaller_sample_share >= 0.60)
        ),
        "ratio_ge_4_small_share_ge_70": (
            ratio_ge_4 & (smaller_sample_share >= 0.70)
        ),
        "ratio_ge_4_margin_ge_2_share_ge_50": (
            ratio_ge_4
            & (minimum_margin >= 2)
            & (smaller_sample_share >= 0.50)
        ),
    }


def _allocation_metadata(allocation: Allocation) -> dict:
    scenario = allocation.scenario
    diagnostics = scenario_diagnostics(scenario)
    probability_p = scenario.probability_p
    probability_q = scenario.probability_q
    expected_margins = (
        allocation.n_p * probability_p.sum(axis=1).min(),
        allocation.n_p * probability_p.sum(axis=0).min(),
        allocation.n_q * probability_q.sum(axis=1).min(),
        allocation.n_q * probability_q.sum(axis=0).min(),
    )
    component_p = diagnostics["population_variance_p"] / allocation.n_p
    component_q = diagnostics["population_variance_q"] / allocation.n_q
    if allocation.n_p <= allocation.n_q:
        smaller_component = component_p
    else:
        smaller_component = component_q
    return {
        "cohort": allocation.cohort,
        "allocation_id": allocation.allocation_id,
        "scenario_id": scenario.scenario_id,
        "regime": _regime_for(scenario),
        "regime_label": REGIMES[_regime_for(scenario)]["label"],
        "rows": scenario.rows,
        "columns": scenario.columns,
        "design_index": scenario.design_index,
        "ratio": allocation.ratio,
        "smaller_group": allocation.smaller_group,
        "n_p": allocation.n_p,
        "n_q": allocation.n_q,
        "seed": allocation.seed,
        "true_delta": diagnostics["true_delta"],
        "population_variance_p": diagnostics["population_variance_p"],
        "population_variance_q": diagnostics["population_variance_q"],
        "population_smaller_sample_variance_share": (
            smaller_component / (component_p + component_q)
        ),
        "minimum_expected_cell": min(
            allocation.n_p * float(probability_p.min()),
            allocation.n_q * float(probability_q.min()),
        ),
        "minimum_expected_margin": float(min(expected_margins)),
    }


def _simulate_allocation(
    allocation: Allocation,
    *,
    replicates: int,
    batch_size: int,
) -> list[dict]:
    scenario = allocation.scenario
    rng = np.random.default_rng(allocation.seed)
    counters = {
        rule: {
            "valid": 0,
            "expanded_route": 0,
            "rejections": {alpha: 0 for alpha in ALPHAS},
        }
        for rule in RULE_LABELS
    }
    observed_diagnostics = {
        "expanded_valid": 0,
        "empty_margin": 0,
        "minimum_margin_sum": 0.0,
        "smaller_share_sum": 0.0,
        "smaller_share_count": 0,
        "base_valid": 0,
        "delta_error_sum": 0.0,
        "delta_error_square_sum": 0.0,
        "standard_error_sum": 0.0,
    }

    for start in range(0, replicates, batch_size):
        count = min(batch_size, replicates - start)
        table_p = rng.multinomial(
            allocation.n_p,
            scenario.probability_p.reshape(-1),
            size=count,
        ).reshape(count, scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            allocation.n_q,
            scenario.probability_q.reshape(-1),
            size=count,
        ).reshape(count, scenario.rows, scenario.columns)
        values = differential_mi_pvalues(
            table_p,
            table_q,
            include_simple=False,
            include_expanded=True,
            include_unbiased_sensitivity=False,
        )
        base_valid = values["base_valid"]
        expanded_valid = values["expanded_valid"]
        minimum_margin = _minimum_observed_margin(table_p, table_q)
        component_p = values["influence_variance_p"] / allocation.n_p
        component_q = values["influence_variance_q"] / allocation.n_q
        if allocation.n_p <= allocation.n_q:
            smaller_component = component_p
        else:
            smaller_component = component_q
        smaller_share = np.divide(
            smaller_component,
            component_p + component_q,
            out=np.full_like(smaller_component, np.nan),
            where=(component_p + component_q) > 0,
        )
        routes = _routes(allocation.ratio, minimum_margin, smaller_share)

        true_delta = float(scenario_diagnostics(scenario)["true_delta"])
        delta_error = values["delta_corrected"][base_valid] - true_delta
        standard_error = values["standard_error"][base_valid]
        observed_diagnostics["base_valid"] += int(np.count_nonzero(base_valid))
        observed_diagnostics["delta_error_sum"] += float(np.sum(delta_error))
        observed_diagnostics["delta_error_square_sum"] += float(
            np.sum(delta_error**2)
        )
        observed_diagnostics["standard_error_sum"] += float(
            np.sum(standard_error)
        )

        observed_diagnostics["expanded_valid"] += int(
            np.count_nonzero(expanded_valid)
        )
        observed_diagnostics["empty_margin"] += int(
            np.count_nonzero(minimum_margin == 0)
        )
        observed_diagnostics["minimum_margin_sum"] += float(
            np.sum(minimum_margin)
        )
        observed_diagnostics["smaller_share_sum"] += float(
            np.nansum(smaller_share)
        )
        observed_diagnostics["smaller_share_count"] += int(
            np.count_nonzero(np.isfinite(smaller_share))
        )

        for rule in RULE_LABELS:
            if rule == "expanded_no_fallback":
                valid = expanded_valid
                use_expanded = expanded_valid
                p_values = values["expanded_welch_p_value"]
            else:
                route = routes[rule]
                valid = base_valid
                use_expanded = route & expanded_valid & base_valid
                p_values = np.where(
                    use_expanded,
                    values["expanded_welch_p_value"],
                    values["normal_p_value"],
                )
            counters[rule]["valid"] += int(np.count_nonzero(valid))
            counters[rule]["expanded_route"] += int(
                np.count_nonzero(use_expanded)
            )
            valid_p = p_values[valid]
            for alpha in ALPHAS:
                counters[rule]["rejections"][alpha] += int(
                    np.count_nonzero(valid_p <= alpha)
                )

    base_valid_count = observed_diagnostics["base_valid"]
    mean_delta_error = (
        observed_diagnostics["delta_error_sum"] / base_valid_count
        if base_valid_count
        else np.nan
    )
    empirical_delta_sd = (
        np.sqrt(
            max(
                0.0,
                (
                    observed_diagnostics["delta_error_square_sum"]
                    - observed_diagnostics["delta_error_sum"] ** 2
                    / base_valid_count
                )
                / (base_valid_count - 1),
            )
        )
        if base_valid_count > 1
        else np.nan
    )
    mean_standard_error = (
        observed_diagnostics["standard_error_sum"] / base_valid_count
        if base_valid_count
        else np.nan
    )
    common = {
        **_allocation_metadata(allocation),
        "replicates": replicates,
        "expanded_valid_rate": (
            observed_diagnostics["expanded_valid"] / replicates
        ),
        "empty_margin_rate": observed_diagnostics["empty_margin"] / replicates,
        "mean_observed_minimum_margin": (
            observed_diagnostics["minimum_margin_sum"] / replicates
        ),
        "mean_estimated_smaller_sample_variance_share": (
            observed_diagnostics["smaller_share_sum"]
            / observed_diagnostics["smaller_share_count"]
            if observed_diagnostics["smaller_share_count"]
            else np.nan
        ),
        "mean_delta_error": mean_delta_error,
        "empirical_delta_sd": empirical_delta_sd,
        "mean_standard_error": mean_standard_error,
        "absolute_bias_over_empirical_sd": (
            abs(mean_delta_error) / empirical_delta_sd
            if empirical_delta_sd > 0
            else np.nan
        ),
        "mean_se_over_empirical_sd": (
            mean_standard_error / empirical_delta_sd
            if empirical_delta_sd > 0
            else np.nan
        ),
    }
    rows = []
    for rule, label in RULE_LABELS.items():
        valid = counters[rule]["valid"]
        row = {
            **common,
            "rule": rule,
            "rule_label": label,
            "valid_rate": valid / replicates,
            "expanded_route_rate": (
                counters[rule]["expanded_route"] / valid if valid else np.nan
            ),
        }
        for alpha in ALPHAS:
            suffix = f"{int(alpha * 100):02d}"
            fpr = (
                counters[rule]["rejections"][alpha] / valid
                if valid
                else np.nan
            )
            row[f"fpr_{suffix}"] = fpr
            row[f"absolute_error_{suffix}"] = abs(fpr - alpha)
            row[f"relative_error_{suffix}"] = abs(fpr - alpha) / alpha
        row["selection_score"] = float(
            np.mean([row["relative_error_05"], row["relative_error_01"]])
        )
        rows.append(row)
    return rows


def _aggregate(results: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    rows = []
    for keys, group in results.groupby(group_columns, sort=False, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_columns, keys))
        row.update(
            {
                "configurations": len(group),
                "mean_valid_rate": float(group["valid_rate"].mean()),
                "mean_expanded_route_rate": float(
                    group["expanded_route_rate"].mean()
                ),
                "mean_selection_score": float(group["selection_score"].mean()),
            }
        )
        for alpha in ALPHAS:
            suffix = f"{int(alpha * 100):02d}"
            errors = group[f"absolute_error_{suffix}"]
            row[f"mean_fpr_{suffix}"] = float(group[f"fpr_{suffix}"].mean())
            row[f"mean_absolute_error_{suffix}"] = float(errors.mean())
            row[f"median_absolute_error_{suffix}"] = float(errors.median())
            row[f"p90_absolute_error_{suffix}"] = float(
                errors.quantile(0.90)
            )
            row[f"maximum_absolute_error_{suffix}"] = float(errors.max())
        rows.append(row)
    return pd.DataFrame(rows)


def _oracle_summary(results: pd.DataFrame) -> pd.DataFrame:
    eligible = results[results["rule"].isin(("normal", "expanded_fallback"))]
    rows = []
    for cohort, group in eligible.groupby("cohort"):
        pivot = group.pivot(
            index="allocation_id",
            columns="rule",
            values="selection_score",
        )
        rows.append(
            {
                "cohort": cohort,
                "configurations": len(pivot),
                "mean_oracle_selection_score": float(pivot.min(axis=1).mean()),
                "oracle_selects_expanded_fraction": float(
                    (pivot["expanded_fallback"] < pivot["normal"]).mean()
                ),
            }
        )
    return pd.DataFrame(rows)


def _domain_subset(results: pd.DataFrame, domain: str) -> pd.DataFrame:
    if domain == "all":
        return results
    if domain == "exclude_support_instability":
        return results[~results["regime"].eq("support_instability")]
    if domain == "regular_support":
        return results[
            ~results["regime"].isin(
                ("support_instability", "widespread_sparse")
            )
        ]
    raise ValueError(f"Unknown domain: {domain}")


def _domain_summary(results: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for domain in ("all", "exclude_support_instability", "regular_support"):
        part = _aggregate(
            _domain_subset(results, domain),
            ["cohort", "rule", "rule_label"],
        )
        part.insert(1, "domain", domain)
        parts.append(part)
    return pd.concat(parts, ignore_index=True)


def _paired_rule_comparisons(results: pd.DataFrame) -> pd.DataFrame:
    comparisons = (
        ("ratio_ge_4", "normal"),
        ("ratio_ge_2", "normal"),
        ("ratio_ge_2", "ratio_ge_4"),
        ("expanded_fallback", "ratio_ge_2"),
    )
    metrics = (
        "selection_score",
        "absolute_error_05",
        "absolute_error_01",
    )
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    rows = []
    for cohort in COHORT_SEEDS:
        cohort_results = results[results["cohort"].eq(cohort)]
        for domain in (
            "all",
            "exclude_support_instability",
            "regular_support",
        ):
            domain_results = _domain_subset(cohort_results, domain)
            metadata = domain_results[
                ["allocation_id", "scenario_id"]
            ].drop_duplicates("allocation_id")
            for candidate, reference in comparisons:
                for metric in metrics:
                    pivot = domain_results[
                        domain_results["rule"].isin((candidate, reference))
                    ].pivot(
                        index="allocation_id",
                        columns="rule",
                        values=metric,
                    )
                    difference = (
                        pivot[candidate] - pivot[reference]
                    ).rename("difference")
                    clusters = metadata.merge(
                        difference,
                        left_on="allocation_id",
                        right_index=True,
                    ).groupby("scenario_id")["difference"].mean()
                    bootstrap = rng.choice(
                        clusters.to_numpy(),
                        size=(10_000, len(clusters)),
                        replace=True,
                    ).mean(axis=1)
                    rows.append(
                        {
                            "cohort": cohort,
                            "domain": domain,
                            "candidate": candidate,
                            "reference": reference,
                            "metric": metric,
                            "population_clusters": len(clusters),
                            "mean_paired_difference": float(clusters.mean()),
                            "ci95_low": float(np.quantile(bootstrap, 0.025)),
                            "ci95_high": float(np.quantile(bootstrap, 0.975)),
                            "candidate_better_fraction": float(
                                (difference < 0).mean()
                            ),
                            "tied_fraction": float((difference == 0).mean()),
                        }
                    )
    return pd.DataFrame(rows)


def _markdown(frame: pd.DataFrame, digits: int = 5) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, (float, np.floating)):
                rendered.append(
                    "NA" if not np.isfinite(value) else f"{value:.{digits}f}"
                )
            else:
                rendered.append(str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def _plot_thresholds(rule_summary: pd.DataFrame, output_dir: Path) -> None:
    thresholds = (2, 3, 4, 6, 10)
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    colors = {"development": "#355070", "holdout": "#A33B20"}
    for axis, alpha in zip(axes, ALPHAS):
        suffix = f"{int(alpha * 100):02d}"
        for cohort, color in colors.items():
            group = rule_summary[
                rule_summary["cohort"].eq(cohort)
                & rule_summary["rule"].isin(
                    [f"ratio_ge_{threshold}" for threshold in thresholds]
                )
            ].set_index("rule")
            values = [
                group.loc[
                    f"ratio_ge_{threshold}",
                    f"mean_absolute_error_{suffix}",
                ]
                for threshold in thresholds
            ]
            axis.plot(
                thresholds,
                values,
                marker="o",
                linewidth=2,
                color=color,
                label=cohort.title(),
            )
        axis.set_title(f"Nominal alpha = {alpha:.2f}")
        axis.set_xlabel("Sample-size ratio threshold")
        axis.set_ylabel("Mean absolute FPR error")
        axis.set_xticks(thresholds)
        axis.grid(alpha=0.2)
    axes[0].legend(frameon=False)
    figure.suptitle("Custom Welch ratio-threshold sensitivity")
    figure.tight_layout()
    figure.savefig(output_dir / "threshold_sensitivity.png", dpi=180)
    plt.close(figure)


def _write_report(
    output_dir: Path,
    *,
    results: pd.DataFrame,
    rule_summary: pd.DataFrame,
    domain_summary: pd.DataFrame,
    paired_comparisons: pd.DataFrame,
    oracle: pd.DataFrame,
    settings: dict,
) -> None:
    key_rules = (
        "normal",
        "expanded_no_fallback",
        "expanded_fallback",
        "ratio_ge_2",
        "ratio_ge_3",
        "ratio_ge_4",
        "ratio_ge_6",
        "ratio_ge_10",
        "ratio_ge_4_margin_ge_2",
        "ratio_ge_4_margin_ge_5",
        "ratio_ge_4_small_share_ge_50",
        "ratio_ge_4_small_share_ge_60",
        "ratio_ge_4_margin_ge_2_share_ge_50",
    )
    summary_view = rule_summary[rule_summary["rule"].isin(key_rules)][
        [
            "cohort",
            "rule_label",
            "mean_absolute_error_05",
            "mean_absolute_error_01",
            "p90_absolute_error_05",
            "mean_valid_rate",
            "mean_expanded_route_rate",
            "mean_selection_score",
        ]
    ].rename(
        columns={
            "cohort": "Cohort",
            "rule_label": "Decision rule",
            "mean_absolute_error_05": "MAE 0.05",
            "mean_absolute_error_01": "MAE 0.01",
            "p90_absolute_error_05": "P90 error 0.05",
            "mean_valid_rate": "Valid rate",
            "mean_expanded_route_rate": "Expanded route",
            "mean_selection_score": "Relative-error score",
        }
    )
    domain_view = domain_summary[
        domain_summary["cohort"].eq("holdout")
        & domain_summary["rule"].isin(
            (
                "normal",
                "expanded_fallback",
                "ratio_ge_2",
                "ratio_ge_4",
                "ratio_ge_4_margin_ge_2",
                "ratio_ge_4_small_share_ge_50",
            )
        )
    ][
        [
            "domain",
            "rule_label",
            "mean_absolute_error_05",
            "mean_absolute_error_01",
            "p90_absolute_error_05",
            "mean_selection_score",
        ]
    ].rename(
        columns={
            "domain": "Domain",
            "rule_label": "Decision rule",
            "mean_absolute_error_05": "MAE 0.05",
            "mean_absolute_error_01": "MAE 0.01",
            "p90_absolute_error_05": "P90 error 0.05",
            "mean_selection_score": "Relative-error score",
        }
    )
    paired_view = paired_comparisons[
        paired_comparisons["cohort"].eq("holdout")
        & paired_comparisons["metric"].eq("selection_score")
    ][
        [
            "domain",
            "candidate",
            "reference",
            "mean_paired_difference",
            "ci95_low",
            "ci95_high",
            "candidate_better_fraction",
        ]
    ].rename(
        columns={
            "domain": "Domain",
            "candidate": "Candidate",
            "reference": "Reference",
            "mean_paired_difference": "Paired difference",
            "ci95_low": "95% CI low",
            "ci95_high": "95% CI high",
            "candidate_better_fraction": "Candidate better",
        }
    )
    holdout = rule_summary[rule_summary["cohort"].eq("holdout")].set_index(
        "rule"
    )
    current = holdout.loc["ratio_ge_4"]
    normal = holdout.loc["normal"]
    expanded = holdout.loc["expanded_fallback"]
    threshold_rules = [f"ratio_ge_{value}" for value in (2, 3, 4, 6, 10)]
    best_development = (
        rule_summary[
            rule_summary["cohort"].eq("development")
            & rule_summary["rule"].isin(threshold_rules)
        ]
        .sort_values("mean_selection_score")
        .iloc[0]
    )
    best_holdout = (
        rule_summary[
            rule_summary["cohort"].eq("holdout")
            & rule_summary["rule"].isin(threshold_rules)
        ]
        .sort_values("mean_selection_score")
        .iloc[0]
    )
    lines = [
        "# Custom Welch Decision Audit",
        "",
        "## Question",
        "",
        "Does the current rule, Expanded Welch at sample-size ratios of at",
        "least 4 and normal Wald otherwise, generalize when population shape,",
        "sparsity, ratio, and allocation direction are crossed rather than",
        "confounded?",
        "",
        "## Design",
        "",
        f"The audit used `{settings['replicates']:,}` null replicates for each",
        f"of `{settings['allocations']:,}` allocation configurations. It crossed",
        "the same equal-MI population pair with ratios 1, 2, 3, 4, 6, 10, and",
        "20, assigning the smaller sample to both P and Q. Six table shapes and",
        "all nine regimes were included. A development cohort and a separately",
        "generated holdout cohort used different population-generation seeds.",
        "",
        "All routing rules fall back to normal Wald when Expanded Welch is",
        "undefined, except the explicitly labelled no-fallback baseline. The",
        "selection score averages relative FPR error at alpha 0.05 and 0.01,",
        "giving the two levels equal weight.",
        "",
        "## Main Results",
        "",
        _markdown(summary_view),
        "",
        "## Interpretation",
        "",
        f"- On holdout, the current ratio-4 rule had MAE "
        f"`{current['mean_absolute_error_05']:.5f}` at alpha 0.05 and "
        f"`{current['mean_absolute_error_01']:.5f}` at alpha 0.01.",
        f"- Holdout normal-Wald MAE was "
        f"`{normal['mean_absolute_error_05']:.5f}` and "
        f"`{normal['mean_absolute_error_01']:.5f}`; expanded-with-fallback MAE "
        f"was `{expanded['mean_absolute_error_05']:.5f}` and "
        f"`{expanded['mean_absolute_error_01']:.5f}`.",
        f"- The best ratio threshold on development was "
        f"`{best_development['rule_label']}`. The best threshold when inspected "
        f"post hoc on holdout was `{best_holdout['rule_label']}`.",
        "- Agreement between those thresholds supports a stable ratio decision;",
        "  disagreement indicates that a sharp cutoff is not yet reliable.",
        "- Support and variance-share guards are shown in the same table. A guard",
        "  is useful only if it improves holdout error, not merely development",
        "  error.",
        "",
        "## Domain Sensitivity",
        "",
        "The all-regime average includes a support-instability boundary where",
        "neither first-order reference is calibrated. The restricted summaries",
        "show whether routing conclusions survive after that known failure domain",
        "is removed. `regular_support` additionally removes widespread sparsity.",
        "",
        _markdown(domain_view),
        "",
        "Negative paired differences favour the candidate. Confidence intervals",
        "use a cluster bootstrap over population pairs, keeping the thirteen",
        "allocations of each population together.",
        "",
        _markdown(paired_view),
        "",
        "The oracle table is not an implementable method. It chooses the better",
        "reference after observing each configuration's simulated calibration and",
        "therefore measures only the maximum room available for routing.",
        "",
        _markdown(oracle),
        "",
        "## Evidence Status",
        "",
        "The holdout populations are independent of the development populations,",
        "but this remains a simulation study using the same generator family.",
        "Any revised rule selected after reading this report needs another frozen",
        "confirmation run. Data-dependent support and variance-share guards also",
        "need particular caution because their route can be correlated with the",
        "test statistic.",
        "",
        "## Files",
        "",
        "- `configuration_results.csv`: every allocation-rule result.",
        "- `rule_summary.csv`: aggregate decision-rule comparison.",
        "- `domain_summary.csv`: all, support-excluded, and regular-support views.",
        "- `paired_rule_comparisons.csv`: clustered paired uncertainty estimates.",
        "- `ratio_summary.csv`: results separated by sample-size ratio.",
        "- `regime_summary.csv`: results separated by generating regime.",
        "- `oracle_summary.csv`: unattainable scenario-level routing benchmark.",
        "- `threshold_sensitivity.png`: development and holdout threshold curves.",
    ]
    (output_dir / "REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    if args.replicates <= 0 or args.batch_size <= 0:
        raise ValueError("Replicates and batch size must be positive.")
    if args.shape_limit is not None and not 1 <= args.shape_limit <= len(
        AUDIT_SHAPES
    ):
        raise ValueError("shape-limit is outside the available audit shapes.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    allocations = _allocations(args.shape_limit)
    rows = []
    for index, allocation in enumerate(allocations, start=1):
        if index == 1 or index % 25 == 0 or index == len(allocations):
            print(
                f"[{index}/{len(allocations)}] {allocation.cohort}: "
                f"{allocation.scenario.scenario_id}, ratio={allocation.ratio}, "
                f"smaller={allocation.smaller_group}",
                flush=True,
            )
        rows.extend(
            _simulate_allocation(
                allocation,
                replicates=args.replicates,
                batch_size=args.batch_size,
            )
        )
    results = pd.DataFrame(rows)
    rule_summary = _aggregate(results, ["cohort", "rule", "rule_label"])
    ratio_summary = _aggregate(
        results,
        ["cohort", "ratio", "rule", "rule_label"],
    )
    regime_summary = _aggregate(
        results,
        ["cohort", "regime", "regime_label", "rule", "rule_label"],
    )
    domain_summary = _domain_summary(results)
    paired_comparisons = _paired_rule_comparisons(results)
    oracle = _oracle_summary(results)

    results.to_csv(args.output_dir / "configuration_results.csv", index=False)
    rule_summary.to_csv(args.output_dir / "rule_summary.csv", index=False)
    ratio_summary.to_csv(args.output_dir / "ratio_summary.csv", index=False)
    regime_summary.to_csv(args.output_dir / "regime_summary.csv", index=False)
    domain_summary.to_csv(args.output_dir / "domain_summary.csv", index=False)
    paired_comparisons.to_csv(
        args.output_dir / "paired_rule_comparisons.csv",
        index=False,
    )
    oracle.to_csv(args.output_dir / "oracle_summary.csv", index=False)
    _plot_thresholds(rule_summary, args.output_dir)
    settings = {
        "replicates": args.replicates,
        "batch_size": args.batch_size,
        "shape_limit": args.shape_limit,
        "allocations": len(allocations),
        "population_pairs_per_cohort": len(allocations)
        // (2 * len(RATIOS) - 1)
        // len(COHORT_SEEDS),
        "ratios": RATIOS,
        "audit_shapes": (
            AUDIT_SHAPES[: args.shape_limit]
            if args.shape_limit
            else AUDIT_SHAPES
        ),
        "cohort_seeds": COHORT_SEEDS,
        "simulation_seed": SIMULATION_SEED,
        "elapsed_seconds": perf_counter() - start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(settings, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_report(
        args.output_dir,
        results=results,
        rule_summary=rule_summary,
        domain_summary=domain_summary,
        paired_comparisons=paired_comparisons,
        oracle=oracle,
        settings=settings,
    )
    print(f"Results written to {args.output_dir}")


if __name__ == "__main__":
    main()
