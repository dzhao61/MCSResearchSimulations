#!/usr/bin/env python3
"""Parallel evaluation: constrained LR and studentized permutation vs Welch.

This is NOT part of the primary thesis evidence base (Expanded Welch is the
thesis's contribution, validated in ``run_supervisor_experiment.py``). It
answers a narrower, secondary question the student wants an answer to before
deciding whether to also propose the constrained likelihood-ratio (LR) test:
on the identical population-pair grid used for the main thesis validation,
how does LR compare to normal Wald and expanded Welch on calibration, and
what does it cost in wall-clock time? A studentized permutation test is
included as an independent nonparametric benchmark, since an analytic-only
comparison would be the weakest possible validation structure available in
this repository (see ``differential_mi.inference.compare_tables``, already
used elsewhere in this project and documented as its best-calibrated
reference method).

The scenario generators are imported directly from
``run_supervisor_experiment`` rather than reimplemented, so this script
evaluates the exact same population pairs as the thesis experiment (same
scenario seed, same margins, same target MI, same sample sizes) -- only the
per-replicate table draws and replicate counts differ, because LR's
per-replicate SLSQP fit and the permutation test's internal resampling are
both far more expensive than the closed-form Wald/Welch calculations. Within
one replicate, all four methods are evaluated on the identical simulated
table pair, so the comparison is paired.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import scipy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_supervisor_experiment import (  # noqa: E402
    DEFAULT_SCENARIO_SEED,
    REGIME_ORDER,
    REGIMES,
    SHAPES,
    _regime_for,
    _wilson,
    generate_adversarial_scenarios,
    generate_expected_count_stress_scenarios,
    generate_fixed_density_scenarios,
    generate_strong_null_scenarios,
)
from differential_mi.inference import compare_tables  # noqa: E402
from welch_differential_mi import (  # noqa: E402
    constrained_likelihood_ratio_test,
    differential_mi_pvalues,
)

ALPHA = 0.05
# LR requires a per-replicate constrained optimization (SLSQP with up to 5
# starts) and the permutation test requires per-replicate resampling, so
# both are far more expensive than the closed-form Wald/Welch calculations
# that the primary thesis experiment uses. Replicate counts are therefore
# scaled down by table size to keep total runtime tractable, in the same
# spirit as (and taken from measured timings comparable to) the constrained
# LR multi-alphabet validation elsewhere in this project. This asymmetry is
# a deliberate, disclosed trade-off for a secondary evaluation -- it is not
# appropriate for the primary thesis evidence, which uses a uniform
# replicate count per population pair for exactly this reason.
REPLICATES_BY_SHAPE = {
    "smoke": {
        (2, 2): 10,
        (2, 5): 10,
        (3, 3): 10,
        (3, 5): 8,
        (5, 5): 6,
        (8, 8): 4,
    },
    "full": {
        (2, 2): 300,
        (2, 5): 250,
        (3, 3): 200,
        (3, 5): 150,
        (5, 5): 100,
        (8, 8): 40,
    },
}
PERMUTATIONS_BY_PROFILE = {"smoke": 19, "full": 199}
DEFAULT_SIMULATION_SEED = 2_026_090_601


def _method_values(table_p: np.ndarray, table_q: np.ndarray) -> dict[str, np.ndarray]:
    """Vectorized Wald and expanded Welch p-values for one table pair."""
    return differential_mi_pvalues(
        table_p[None, :, :],
        table_q[None, :, :],
        include_expanded=True,
        include_unbiased_sensitivity=False,
    )


def _build_scenarios(scenario_seed: int, shape_limit: int | None) -> list:
    scenarios = generate_strong_null_scenarios(scenario_seed - 1)
    scenarios.extend(generate_fixed_density_scenarios(scenario_seed))
    scenarios.extend(generate_expected_count_stress_scenarios(scenario_seed + 1))
    scenarios.extend(generate_adversarial_scenarios(scenario_seed + 2))
    scenarios.sort(key=lambda scenario: (scenario.shape_index, scenario.design_index))
    if shape_limit is not None:
        scenarios = [
            scenario for scenario in scenarios if scenario.shape_index < shape_limit
        ]
    return scenarios


def _simulate_scenario(
    scenario,
    *,
    replicates: int,
    permutations: int,
    seed: int,
) -> list[dict]:
    rng = np.random.default_rng(seed)
    permutation_rng = np.random.default_rng(seed + 1)
    methods = ("normal_wald", "expanded_welch", "constrained_lr", "student_permutation")
    counts = {
        method: {"valid": 0, "rejections": 0, "runtimes": []} for method in methods
    }
    for _ in range(replicates):
        table_p = rng.multinomial(
            scenario.n_p, scenario.probability_p.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)
        table_q = rng.multinomial(
            scenario.n_q, scenario.probability_q.reshape(-1)
        ).reshape(scenario.rows, scenario.columns)

        start = perf_counter()
        wald_values = _method_values(table_p, table_q)
        wald_elapsed = perf_counter() - start
        if bool(wald_values["base_valid"][0]):
            counts["normal_wald"]["valid"] += 1
            counts["normal_wald"]["runtimes"].append(wald_elapsed)
            if float(wald_values["normal_p_value"][0]) <= ALPHA:
                counts["normal_wald"]["rejections"] += 1
        if bool(wald_values["expanded_valid"][0]):
            counts["expanded_welch"]["valid"] += 1
            counts["expanded_welch"]["runtimes"].append(wald_elapsed)
            if float(wald_values["expanded_welch_p_value"][0]) <= ALPHA:
                counts["expanded_welch"]["rejections"] += 1

        lr_result = constrained_likelihood_ratio_test(table_p, table_q)
        counts["constrained_lr"]["runtimes"].append(lr_result.elapsed_seconds)
        if lr_result.converged and np.isfinite(lr_result.p_value):
            counts["constrained_lr"]["valid"] += 1
            if lr_result.p_value <= ALPHA:
                counts["constrained_lr"]["rejections"] += 1

        permutation_start = perf_counter()
        permutation_result = compare_tables(
            table_p,
            table_q,
            permutations=permutations,
            rng=permutation_rng,
        )
        permutation_elapsed = perf_counter() - permutation_start
        counts["student_permutation"]["runtimes"].append(permutation_elapsed)
        if permutation_result.valid_studentization and np.isfinite(
            permutation_result.student_perm_analytic_p
        ):
            counts["student_permutation"]["valid"] += 1
            if permutation_result.student_perm_analytic_p <= ALPHA:
                counts["student_permutation"]["rejections"] += 1

    regime = _regime_for(scenario)
    rows = []
    for method in methods:
        valid = counts[method]["valid"]
        rejections = counts[method]["rejections"]
        runtimes = np.asarray(counts[method]["runtimes"])
        fpr = rejections / valid if valid else np.nan
        low, high = _wilson(rejections, valid)
        rows.append(
            {
                "scenario_id": scenario.scenario_id,
                "regime": regime,
                "regime_label": REGIMES[regime]["label"],
                "rows": scenario.rows,
                "columns": scenario.columns,
                "n_p": scenario.n_p,
                "n_q": scenario.n_q,
                "target_mi": scenario.target_mi,
                "method": method,
                "replicates": replicates,
                "valid_replicates": valid,
                "valid_rate": valid / replicates if replicates else np.nan,
                "fpr_05": fpr,
                "fpr_05_low": low,
                "fpr_05_high": high,
                "absolute_fpr_error_05": (
                    abs(fpr - ALPHA) if np.isfinite(fpr) else np.nan
                ),
                "median_runtime_ms": (
                    1_000.0 * float(np.median(runtimes)) if runtimes.size else np.nan
                ),
                "p95_runtime_ms": (
                    1_000.0 * float(np.quantile(runtimes, 0.95))
                    if runtimes.size
                    else np.nan
                ),
            }
        )
    return rows


def _aggregate(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for regime in (*REGIME_ORDER, "all"):
        frame = (
            results
            if regime == "all"
            else results[results["regime"].eq(regime)]
        )
        for method, group in frame.groupby("method", sort=False):
            rows.append(
                {
                    "regime": regime,
                    "regime_label": (
                        "All regimes" if regime == "all" else REGIMES[regime]["label"]
                    ),
                    "method": method,
                    "population_pairs": len(group),
                    "mean_valid_rate": float(group["valid_rate"].mean()),
                    "mean_fpr_05": float(group["fpr_05"].mean()),
                    "mean_absolute_fpr_error_05": float(
                        group["absolute_fpr_error_05"].mean()
                    ),
                    "median_runtime_ms": float(group["median_runtime_ms"].median()),
                    "p95_runtime_ms": float(group["p95_runtime_ms"].median()),
                }
            )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Secondary evaluation of constrained LR and studentized "
            "permutation against normal Wald and expanded Welch, on the "
            "same population-pair grid as the primary thesis experiment."
        )
    )
    parser.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "lr_permutation_comparison",
    )
    parser.add_argument("--scenario-seed", type=int, default=DEFAULT_SCENARIO_SEED)
    parser.add_argument(
        "--simulation-seed", type=int, default=DEFAULT_SIMULATION_SEED
    )
    parser.add_argument("--shape-limit", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    run_start = perf_counter()

    replicates_by_shape = REPLICATES_BY_SHAPE[args.profile]
    permutations = PERMUTATIONS_BY_PROFILE[args.profile]
    scenarios = _build_scenarios(args.scenario_seed, args.shape_limit)

    all_rows = []
    for index, scenario in enumerate(scenarios):
        replicates = replicates_by_shape[(scenario.rows, scenario.columns)]
        seed = int(
            np.random.SeedSequence(
                [args.simulation_seed, index]
            ).generate_state(1)[0]
        )
        scenario_rows = _simulate_scenario(
            scenario,
            replicates=replicates,
            permutations=permutations,
            seed=seed,
        )
        all_rows.extend(scenario_rows)
        print(
            f"[{index + 1}/{len(scenarios)}] "
            f"{REGIMES[_regime_for(scenario)]['label']}: "
            f"{scenario.scenario_id} ({replicates} replicates)",
            flush=True,
        )

    results = pd.DataFrame(all_rows)
    summary = _aggregate(results)

    results.to_csv(args.output_dir / "scenario_results.csv", index=False)
    summary.to_csv(args.output_dir / "regime_summary.csv", index=False)

    overall = summary[summary["regime"].eq("all")].set_index("method")
    lines = [
        "# Constrained LR and Studentized Permutation: Secondary Evaluation",
        "",
        "This is not part of the primary thesis evidence. Expanded Welch is",
        "validated on the full grid in `run_supervisor_experiment.py`; this",
        "script answers a narrower question -- how does the constrained LR",
        "test compare on accuracy and runtime, evaluated on the identical",
        "population-pair grid -- before deciding whether to also propose it.",
        "",
        f"Profile: `{args.profile}`. Replicate counts are scaled down by table",
        "size because LR's per-replicate constrained optimization and the",
        "permutation test's per-replicate resampling are far more expensive",
        "than the closed-form Wald/Welch calculations used elsewhere in this",
        "project; this is a disclosed trade-off appropriate only for this",
        "secondary comparison, not for primary evidence.",
        "",
        "## Overall calibration and runtime",
        "",
        "| Method | Mean FPR (0.05) | Mean absolute error | Mean valid rate |"
        " Median runtime (ms) | p95 runtime (ms) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for method, row in overall.iterrows():
        lines.append(
            f"| {method} | {row['mean_fpr_05']:.4f} | "
            f"{row['mean_absolute_fpr_error_05']:.4f} | "
            f"{row['mean_valid_rate']:.4f} | {row['median_runtime_ms']:.4f} | "
            f"{row['p95_runtime_ms']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Output map",
            "",
            "- `scenario_results.csv`: every population pair and method,",
            "  including runtime percentiles.",
            "- `regime_summary.csv`: regime-level aggregates; `all` rows give",
            "  the overall summary above.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    metadata = {
        "profile": args.profile,
        "replicates_by_shape": {
            f"{rows}x{columns}": count
            for (rows, columns), count in replicates_by_shape.items()
        },
        "permutations": permutations,
        "scenario_seed": args.scenario_seed,
        "simulation_seed": args.simulation_seed,
        "scenario_count": len(scenarios),
        "elapsed_seconds": perf_counter() - run_start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Results written to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
