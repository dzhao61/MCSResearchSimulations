#!/usr/bin/env python3
"""Compare expanded Welch with von Davier's corrected df combination."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from scipy.stats import t

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from differential_mi.random_validation import (  # noqa: E402
    generate_random_scenarios,
)
from differential_mi.scenarios import (  # noqa: E402
    build_distributions,
    power_curve_scenarios,
)
from welch_differential_mi import differential_mi_pvalues  # noqa: E402

from run_supervisor_experiment import (  # noqa: E402
    ALPHAS,
    DEFAULT_SCENARIO_SEED,
    DEFAULT_SIMULATION_SEED,
    REGIMES,
    _markdown,
    _population_metadata,
    _regime_for,
    generate_adversarial_scenarios,
    generate_expected_count_stress_scenarios,
)


METHODS = {
    "expanded_welch": "Expanded Welch",
    "corrected_expanded_welch": "Corrected expanded Welch",
}

PROFILE_SETTINGS = {
    "smoke": {
        "null_replicates": 500,
        "power_replicates": 1_000,
        "batch_size": 250,
        "shape_limit": 3,
    },
    "full": {
        "null_replicates": 10_000,
        "power_replicates": 10_000,
        "batch_size": 1_000,
        "shape_limit": None,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILE_SETTINGS, default="smoke")
    parser.add_argument("--null-replicates", type=int)
    parser.add_argument("--power-replicates", type=int)
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=DEFAULT_SIMULATION_SEED,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "corrected_satterthwaite_check",
    )
    return parser.parse_args()


def corrected_combined_df(
    component_p: np.ndarray,
    component_q: np.ndarray,
    degrees_of_freedom_p: np.ndarray,
    degrees_of_freedom_q: np.ndarray,
) -> np.ndarray:
    """Apply the fourth-moment correction to the combined component df."""
    numerator = (component_p + component_q) ** 2
    denominator = (
        component_p**2 / (degrees_of_freedom_p + 2.0)
        + component_q**2 / (degrees_of_freedom_q + 2.0)
    )
    ratio = np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan, dtype=float),
        where=np.isfinite(denominator) & (denominator > 0),
    )
    return ratio - 2.0


def method_values(
    table_p: np.ndarray,
    table_q: np.ndarray,
) -> dict[str, dict[str, np.ndarray]]:
    values = differential_mi_pvalues(
        table_p,
        table_q,
        include_simple=False,
        include_expanded=True,
        include_unbiased_sensitivity=False,
    )
    n_p = table_p.sum(axis=(-2, -1))
    n_q = table_q.sum(axis=(-2, -1))
    component_p = values["influence_variance_p"] / n_p
    component_q = values["influence_variance_q"] / n_q
    corrected_df = corrected_combined_df(
        component_p,
        component_q,
        values["expanded_component_degrees_of_freedom_p"],
        values["expanded_component_degrees_of_freedom_q"],
    )
    corrected_p = 2.0 * t.sf(np.abs(values["statistic"]), df=corrected_df)
    corrected_valid = (
        values["expanded_valid"]
        & np.isfinite(corrected_df)
        & (corrected_df > 0)
        & np.isfinite(corrected_p)
    )
    return {
        "expanded_welch": {
            "p": values["expanded_welch_p_value"],
            "df": values["expanded_welch_degrees_of_freedom"],
            "valid": values["expanded_valid"],
        },
        "corrected_expanded_welch": {
            "p": np.where(corrected_valid, corrected_p, np.nan),
            "df": np.where(corrected_valid, corrected_df, np.nan),
            "valid": corrected_valid,
        },
    }


def build_null_scenarios(seed: int, shape_limit: int | None) -> list:
    scenarios = generate_random_scenarios(seed)
    scenarios.extend(generate_expected_count_stress_scenarios(seed + 1))
    scenarios.extend(generate_adversarial_scenarios(seed + 2))
    scenarios.sort(key=lambda scenario: (scenario.shape_index, scenario.design_index))
    if shape_limit is not None:
        scenarios = [
            scenario
            for scenario in scenarios
            if scenario.shape_index < shape_limit
        ]
    return scenarios


def simulate_null(
    scenarios: list,
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> pd.DataFrame:
    children = np.random.SeedSequence(seed).spawn(len(scenarios))
    rows: list[dict] = []
    for index, (scenario, child) in enumerate(zip(scenarios, children)):
        rng = np.random.default_rng(int(child.generate_state(1)[0]))
        counts = {
            method: {
                "valid": 0,
                "rejections": {alpha: 0 for alpha in ALPHAS},
                "df": [],
            }
            for method in METHODS
        }
        for start in range(0, replicates, batch_size):
            count = min(batch_size, replicates - start)
            table_p = rng.multinomial(
                scenario.n_p,
                scenario.probability_p.reshape(-1),
                size=count,
            ).reshape(count, scenario.rows, scenario.columns)
            table_q = rng.multinomial(
                scenario.n_q,
                scenario.probability_q.reshape(-1),
                size=count,
            ).reshape(count, scenario.rows, scenario.columns)
            values = method_values(table_p, table_q)
            for method in METHODS:
                valid = values[method]["valid"]
                p_values = values[method]["p"][valid]
                degrees_of_freedom = values[method]["df"][valid]
                counts[method]["valid"] += int(np.count_nonzero(valid))
                counts[method]["df"].append(degrees_of_freedom)
                for alpha in ALPHAS:
                    counts[method]["rejections"][alpha] += int(
                        np.count_nonzero(p_values <= alpha)
                    )

        metadata = _population_metadata(scenario)
        for method, label in METHODS.items():
            valid_count = counts[method]["valid"]
            degrees_of_freedom = np.concatenate(counts[method]["df"])
            row = {
                **metadata,
                "method": method,
                "method_label": label,
                "replicates": replicates,
                "valid_rate": valid_count / replicates,
                "median_df": float(np.median(degrees_of_freedom)),
            }
            for alpha in ALPHAS:
                suffix = f"{alpha:.2f}".replace("0.", "")
                fpr = counts[method]["rejections"][alpha] / valid_count
                row[f"fpr_{suffix}"] = fpr
                row[f"absolute_error_{suffix}"] = abs(fpr - alpha)
            rows.append(row)
        print(f"[{index + 1}/{len(scenarios)}] {scenario.scenario_id}", flush=True)
    return pd.DataFrame(rows)


def aggregate_null(scenario_results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (regime, method), group in scenario_results.groupby(
        ["regime", "method"], sort=False
    ):
        row = {
            "regime": regime,
            "regime_label": REGIMES[regime]["label"],
            "method": method,
            "method_label": METHODS[method],
            "scenarios": len(group),
            "mean_valid_rate": group["valid_rate"].mean(),
            "median_df": group["median_df"].median(),
        }
        for alpha in ALPHAS:
            suffix = f"{alpha:.2f}".replace("0.", "")
            row[f"mean_fpr_{suffix}"] = group[f"fpr_{suffix}"].mean()
            row[f"mean_absolute_error_{suffix}"] = group[
                f"absolute_error_{suffix}"
            ].mean()
        rows.append(row)
    return pd.DataFrame(rows)


def simulate_power(
    *,
    replicates: int,
    batch_size: int,
    seed: int,
) -> pd.DataFrame:
    scenarios = power_curve_scenarios()
    children = np.random.SeedSequence(seed).spawn(len(scenarios))
    rows = []
    for scenario, child in zip(scenarios, children):
        probability_p, probability_q, diagnostics = build_distributions(scenario)
        rng = np.random.default_rng(int(child.generate_state(1)[0]))
        counts = {
            method: {"valid": 0, "rejections": 0, "df": []}
            for method in METHODS
        }
        for start in range(0, replicates, batch_size):
            count = min(batch_size, replicates - start)
            table_p = rng.multinomial(
                scenario.n_p,
                probability_p.reshape(-1),
                size=count,
            ).reshape(count, scenario.rows, scenario.columns)
            table_q = rng.multinomial(
                scenario.n_q,
                probability_q.reshape(-1),
                size=count,
            ).reshape(count, scenario.rows, scenario.columns)
            values = method_values(table_p, table_q)
            for method in METHODS:
                valid = values[method]["valid"]
                counts[method]["valid"] += int(np.count_nonzero(valid))
                counts[method]["rejections"] += int(
                    np.count_nonzero(values[method]["p"][valid] <= 0.05)
                )
                counts[method]["df"].append(values[method]["df"][valid])
        for method, label in METHODS.items():
            valid_count = counts[method]["valid"]
            rows.append(
                {
                    **scenario.to_dict(),
                    **diagnostics,
                    "method": method,
                    "method_label": label,
                    "replicates": replicates,
                    "valid_rate": valid_count / replicates,
                    "power_05": counts[method]["rejections"] / valid_count,
                    "median_df": float(
                        np.median(np.concatenate(counts[method]["df"]))
                    ),
                }
            )
    return pd.DataFrame(rows)


def write_report(
    output_dir: Path,
    scenario_results: pd.DataFrame,
    regime_summary: pd.DataFrame,
    power_summary: pd.DataFrame,
    elapsed_seconds: float,
) -> None:
    error_columns = [
        f"absolute_error_{alpha:.2f}".replace("0.", "")
        for alpha in ALPHAS
    ]
    overall = scenario_results.groupby("method")[error_columns].mean()
    current = overall.loc["expanded_welch"]
    corrected = overall.loc["corrected_expanded_welch"]
    relative_changes = 100.0 * (corrected - current) / current

    pivot = scenario_results.pivot(
        index="scenario_id",
        columns="method",
        values=error_columns,
    )
    wins = {}
    for column in error_columns:
        current_error = pivot[(column, "expanded_welch")]
        corrected_error = pivot[(column, "corrected_expanded_welch")]
        wins[column] = {
            "corrected_better": int((corrected_error < current_error).sum()),
            "current_better": int((corrected_error > current_error).sum()),
            "tied": int((corrected_error == current_error).sum()),
        }

    power_pivot = power_summary.pivot(
        index="scenario_id", columns="method", values="power_05"
    )
    power_change = (
        power_pivot["corrected_expanded_welch"]
        - power_pivot["expanded_welch"]
    )
    lines = [
        "# Corrected Satterthwaite Check",
        "",
        "This experiment changes only the final combination of the two expanded",
        "component degrees of freedom. The corrected candidate uses",
        "",
        "$$",
        "\\widehat\\nu_{\\mathrm{corrected}}=",
        "\\frac{(C_P+C_Q)^2}",
        "{C_P^2/(\\widehat\\nu_V(P)+2)+C_Q^2/(\\widehat\\nu_V(Q)+2)}-2,",
        "$$",
        "",
        "where $C_P=\\widehat V(P)/n_P$ and",
        "$C_Q=\\widehat V(Q)/n_Q$. The MI difference and standard error are",
        "identical for both methods.",
        "",
        "## Overall null calibration",
        "",
        "| Alpha | Current MAE | Corrected MAE | Relative change | Corrected/current/tied scenarios |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for alpha, column in zip(ALPHAS, error_columns):
        result = wins[column]
        lines.append(
            f"| {alpha:.2f} | {current[column]:.5f} | "
            f"{corrected[column]:.5f} | {relative_changes[column]:+.1f}% | "
            f"{result['corrected_better']}/{result['current_better']}/"
            f"{result['tied']} |"
        )
    lines.extend(
        [
            "",
            "A negative relative change means that the correction reduced mean",
            "absolute false-positive-rate error.",
            "",
            "## Power",
            "",
            f"Mean alpha-0.05 power change: `{power_change.mean():+.5f}`. ",
            f"Range across alternatives: `{power_change.min():+.5f}` to ",
            f"`{power_change.max():+.5f}`.",
            "",
            "## Regime detail",
            "",
            _markdown(regime_summary, digits=5),
            "",
            f"Elapsed time: `{elapsed_seconds:.2f}` seconds.",
            "",
            "Source: Matthias von Davier (2026), *A Corrected Welch",
            "Satterthwaite Equation*, arXiv:2602.20912.",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    args = parse_args()
    settings = dict(PROFILE_SETTINGS[args.profile])
    for name in ("null_replicates", "power_replicates", "batch_size"):
        value = getattr(args, name)
        if value is not None:
            settings[name] = value
    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    scenarios = build_null_scenarios(
        args.scenario_seed,
        settings["shape_limit"],
    )
    scenario_results = simulate_null(
        scenarios,
        replicates=settings["null_replicates"],
        batch_size=settings["batch_size"],
        seed=args.simulation_seed,
    )
    regime_summary = aggregate_null(scenario_results)
    power_summary = simulate_power(
        replicates=settings["power_replicates"],
        batch_size=settings["batch_size"],
        seed=args.simulation_seed + 10_001,
    )
    elapsed_seconds = perf_counter() - start

    scenario_results.to_csv(args.output_dir / "scenario_results.csv", index=False)
    regime_summary.to_csv(args.output_dir / "regime_summary.csv", index=False)
    power_summary.to_csv(args.output_dir / "power_summary.csv", index=False)
    metadata = {
        "profile": args.profile,
        "settings": settings,
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "scenario_count": len(scenarios),
        "elapsed_seconds": elapsed_seconds,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    write_report(
        args.output_dir,
        scenario_results,
        regime_summary,
        power_summary,
        elapsed_seconds,
    )


if __name__ == "__main__":
    main()
