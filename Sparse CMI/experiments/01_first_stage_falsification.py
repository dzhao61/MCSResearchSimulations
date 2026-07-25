#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.stats import chi2, spearmanr

from sparse_cmi.approximations import (
    cornish_fisher_critical_value,
    edgeworth_pvalue,
    normal_pvalue,
)
from sparse_cmi.diagnostics import table_diagnostics
from sparse_cmi.exact_convolution import (
    StateSpaceTooLarge,
    exact_conditional_distribution,
)
from sparse_cmi.moments import aggregate_moments
from sparse_cmi.permutation import label_permutation_g2, sample_conditional_g2
from sparse_cmi.simulation import (
    ValidationConfiguration,
    validation_configurations,
)

ALPHAS = (0.10, 0.05, 0.01, 0.001)
METHODS = (
    "normal",
    "edgeworth",
    "cornish_fisher",
    "chi2_nominal",
    "chi2_informative",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Falsify or support the exact-cumulant sparse CMI proposal."
    )
    parser.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    parser.add_argument("--null-samples", type=int, default=20_000)
    parser.add_argument("--permutations", type=int, default=200)
    parser.add_argument("--seed", type=int, default=5030)
    parser.add_argument("--exact-max-states", type=int, default=100_000)
    parser.add_argument("--exact-max-informative", type=int, default=10)
    parser.add_argument("--max-configurations", type=int)
    parser.add_argument("--checkpoint-every", type=int, default=5)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def empirical_upper_tail_pvalues(values: np.ndarray) -> np.ndarray:
    rounded = np.round(np.asarray(values, dtype=np.float64), 12)
    _, inverse, counts = np.unique(
        rounded,
        return_inverse=True,
        return_counts=True,
    )
    tails = np.cumsum(counts[::-1])[::-1] / rounded.size
    return tails[inverse]


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.dot(np.asarray(values, dtype=float), weights))


def rejection_probability(
    pvalues: np.ndarray,
    alpha: float,
    weights: np.ndarray,
) -> float:
    return weighted_mean(np.asarray(pvalues) <= alpha, weights)


def monotonicity_violations(
    statistics: np.ndarray,
    pvalues: np.ndarray,
) -> int:
    order = np.argsort(statistics)
    sorted_statistics = statistics[order]
    sorted_pvalues = pvalues[order]
    distinct = np.diff(sorted_statistics) > 1e-10
    return int(np.count_nonzero(np.diff(sorted_pvalues)[distinct] > 1e-10))


def evaluate_configuration(
    configuration: ValidationConfiguration,
    *,
    null_samples: int,
    permutations: int,
    rng: np.random.Generator,
    exact_max_states: int,
    exact_max_informative: int,
) -> list[dict[str, object]]:
    moment_start = time.perf_counter()
    moments = aggregate_moments(configuration.strata)
    moment_seconds = time.perf_counter() - moment_start
    diagnostics = table_diagnostics(configuration.strata, moments)

    exact = None
    exact_status = "not_attempted"
    exact_seconds = 0.0
    if moments.informative_strata <= exact_max_informative:
        exact_start = time.perf_counter()
        try:
            exact = exact_conditional_distribution(
                configuration.strata,
                max_states=exact_max_states,
            )
            exact_status = "available"
        except StateSpaceTooLarge:
            exact_status = f">{exact_max_states}"
        exact_seconds = time.perf_counter() - exact_start

    sample_start = time.perf_counter()
    sampled_statistics = sample_conditional_g2(
        configuration.strata,
        samples=null_samples,
        rng=rng,
    )
    sampling_seconds = time.perf_counter() - sample_start

    if exact is not None:
        statistics = exact.values
        weights = exact.probabilities
        truth_p = exact.upper_tail_array(statistics)
        reference = "exact_convolution"
        exact_state_count: int | None = int(exact.values.size)
    else:
        statistics = sampled_statistics
        weights = np.full(statistics.size, 1.0 / statistics.size)
        truth_p = empirical_upper_tail_pvalues(statistics)
        reference = "conditional_monte_carlo"
        exact_state_count = None

    normal_p = np.asarray(
        normal_pvalue(statistics, moments.mean, moments.variance)
    )
    edgeworth_p = np.asarray(
        edgeworth_pvalue(
            statistics,
            moments.mean,
            moments.variance,
            moments.skewness,
        )
    )
    nominal_df = len(configuration.strata)
    informative_df = moments.informative_strata
    chi_nominal_p = (
        chi2.sf(statistics, nominal_df)
        if nominal_df
        else np.ones_like(statistics)
    )
    chi_informative_p = (
        chi2.sf(statistics, informative_df)
        if informative_df
        else np.ones_like(statistics)
    )

    pvalue_arrays = {
        "normal": normal_p,
        "edgeworth": edgeworth_p,
        "chi2_nominal": chi_nominal_p,
        "chi2_informative": chi_informative_p,
    }
    pvalue_mae = {
        method: weighted_mean(np.abs(values - truth_p), weights)
        for method, values in pvalue_arrays.items()
    }
    tail_mask = truth_p <= 0.10
    if np.any(tail_mask):
        tail_weights = weights[tail_mask]
        tail_weights = tail_weights / tail_weights.sum()
        tail_mae = {
            method: weighted_mean(
                np.abs(values[tail_mask] - truth_p[tail_mask]),
                tail_weights,
            )
            for method, values in pvalue_arrays.items()
        }
        tail_max_error = {
            method: float(
                np.max(np.abs(values[tail_mask] - truth_p[tail_mask]))
            )
            for method, values in pvalue_arrays.items()
        }
    else:
        tail_mae = {method: 0.0 for method in pvalue_arrays}
        tail_max_error = {method: 0.0 for method in pvalue_arrays}

    permutation_seconds: float | None = None
    if permutations > 0:
        permutation_start = time.perf_counter()
        label_permutation_g2(
            configuration.strata,
            permutations=permutations,
            rng=rng,
        )
        permutation_seconds = time.perf_counter() - permutation_start

    common: dict[str, object] = {
        "configuration": configuration.name,
        "family": configuration.family,
        "description": configuration.description,
        "total_n": configuration.total_n,
        "total_strata": len(configuration.strata),
        "informative_strata": informative_df,
        "reference": reference,
        "exact_status": exact_status,
        "exact_state_count": exact_state_count,
        "mean": moments.mean,
        "variance": moments.variance,
        "skewness": moments.skewness,
        "fourth_cumulant": moments.fourth_cumulant,
        "lyapunov_ratio": moments.lyapunov_ratio,
        "max_variance_share": moments.max_variance_share,
        "total_support_width": moments.total_support_width,
        "min_expected_count": diagnostics.min_expected_count,
        "fraction_expected_below_1": diagnostics.fraction_expected_below_1,
        "fraction_expected_below_5": diagnostics.fraction_expected_below_5,
        "degenerate_fraction": diagnostics.degenerate_fraction,
        "moment_seconds": moment_seconds,
        "exact_seconds": exact_seconds,
        "reference_sampling_seconds": sampling_seconds,
        "permutation_seconds": permutation_seconds,
        "permutations": permutations,
        "runtime_speedup_vs_permutation": (
            permutation_seconds / moment_seconds
            if permutation_seconds is not None and moment_seconds > 0
            else None
        ),
        "normal_p_mae": pvalue_mae["normal"],
        "edgeworth_p_mae": pvalue_mae["edgeworth"],
        "chi2_nominal_p_mae": pvalue_mae["chi2_nominal"],
        "chi2_informative_p_mae": pvalue_mae["chi2_informative"],
        "normal_tail_p_mae": tail_mae["normal"],
        "edgeworth_tail_p_mae": tail_mae["edgeworth"],
        "chi2_nominal_tail_p_mae": tail_mae["chi2_nominal"],
        "chi2_informative_tail_p_mae": tail_mae["chi2_informative"],
        "normal_tail_max_error": tail_max_error["normal"],
        "edgeworth_tail_max_error": tail_max_error["edgeworth"],
        "chi2_nominal_tail_max_error": tail_max_error["chi2_nominal"],
        "chi2_informative_tail_max_error": tail_max_error["chi2_informative"],
        "normal_monotonicity_violations": monotonicity_violations(
            statistics, normal_p
        ),
        "edgeworth_monotonicity_violations": monotonicity_violations(
            statistics, edgeworth_p
        ),
    }

    rows: list[dict[str, object]] = []
    for alpha in ALPHAS:
        truth_fpr = rejection_probability(truth_p, alpha, weights)
        fprs = {
            method: rejection_probability(values, alpha, weights)
            for method, values in pvalue_arrays.items()
        }
        cf_threshold = cornish_fisher_critical_value(
            alpha,
            moments.mean,
            moments.variance,
            moments.skewness,
        )
        if moments.variance <= 0:
            fprs["cornish_fisher"] = 0.0
        else:
            fprs["cornish_fisher"] = weighted_mean(
                statistics >= cf_threshold - 1e-10,
                weights,
            )
        row = dict(common)
        row.update(
            {
                "alpha": alpha,
                "reference_fpr": truth_fpr,
                "normal_fpr": fprs["normal"],
                "edgeworth_fpr": fprs["edgeworth"],
                "cornish_fisher_fpr": fprs["cornish_fisher"],
                "chi2_nominal_fpr": fprs["chi2_nominal"],
                "chi2_informative_fpr": fprs["chi2_informative"],
            }
        )
        for method in METHODS:
            row[f"{method}_fpr_error_vs_reference"] = abs(
                fprs[method] - truth_fpr
            )
            row[f"{method}_size_distortion"] = abs(fprs[method] - alpha)
        rows.append(row)
    return rows


def safe_spearman(left: pd.Series, right: pd.Series) -> float:
    valid = left.notna() & right.notna()
    if valid.sum() < 3 or left[valid].nunique() < 2 or right[valid].nunique() < 2:
        return float("nan")
    return float(spearmanr(left[valid], right[valid]).statistic)


def decision_summary(results: pd.DataFrame) -> dict[str, object]:
    alpha_05 = results[np.isclose(results["alpha"], 0.05)].copy()
    sparse = alpha_05[
        (alpha_05["fraction_expected_below_5"] >= 0.5)
        & (alpha_05["informative_strata"] > 0)
    ]
    normal_beats_chi_rate = float(
        np.mean(
            sparse["normal_fpr_error_vs_reference"]
            < sparse["chi2_informative_fpr_error_vs_reference"]
        )
    )
    normal_p_beats_chi_rate = float(
        np.mean(
            sparse["normal_p_mae"] < sparse["chi2_informative_p_mae"]
        )
    )
    edgeworth_beats_normal_rate = float(
        np.mean(
            sparse["edgeworth_fpr_error_vs_reference"]
            < sparse["normal_fpr_error_vs_reference"]
        )
    )
    edgeworth_tail_p_beats_normal_rate = float(
        np.mean(
            sparse["edgeworth_tail_p_mae"] < sparse["normal_tail_p_mae"]
        )
    )
    sparse_tail_levels = results[
        (results["fraction_expected_below_5"] >= 0.5)
        & (results["informative_strata"] > 0)
        & (results["alpha"] <= 0.05)
    ]
    edgeworth_tail_fpr_nonworse_rate = float(
        np.mean(
            sparse_tail_levels["edgeworth_fpr_error_vs_reference"]
            <= sparse_tail_levels["normal_fpr_error_vs_reference"] + 1e-12
        )
    )
    normal_tail_fpr_error = float(
        sparse_tail_levels["normal_fpr_error_vs_reference"].mean()
    )
    edgeworth_tail_fpr_error = float(
        sparse_tail_levels["edgeworth_fpr_error_vs_reference"].mean()
    )

    diagnostic_correlations = {
        diagnostic: safe_spearman(
            alpha_05[diagnostic],
            alpha_05["normal_tail_p_mae"],
        )
        for diagnostic in (
            "lyapunov_ratio",
            "max_variance_share",
            "skewness",
            "informative_strata",
        )
    }
    finite_correlations = [
        abs(value)
        for value in diagnostic_correlations.values()
        if np.isfinite(value)
    ]
    best_diagnostic_correlation = max(finite_correlations, default=0.0)
    speedup = float(
        alpha_05["runtime_speedup_vs_permutation"].dropna().median()
    )

    criteria = {
        "normal_beats_chi_sparse": (
            normal_beats_chi_rate >= 0.60
            and normal_p_beats_chi_rate >= 0.60
        ),
        "skewness_correction_broadly_helps": (
            edgeworth_tail_p_beats_normal_rate >= 0.60
            and edgeworth_tail_fpr_nonworse_rate >= 0.80
            and edgeworth_tail_fpr_error <= 0.90 * normal_tail_fpr_error
        ),
        "diagnostics_predict_error": best_diagnostic_correlation >= 0.30,
        "faster_than_permutation": speedup >= 10.0,
    }
    if all(criteria.values()):
        verdict = "PROCEED"
    elif (
        criteria["normal_beats_chi_sparse"]
        and criteria["faster_than_permutation"]
    ):
        verdict = "NARROW_OR_REVISE"
    else:
        verdict = "PIVOT"

    return {
        "verdict": verdict,
        "criteria": criteria,
        "normal_beats_chi_sparse_rate": normal_beats_chi_rate,
        "normal_p_beats_chi_sparse_rate": normal_p_beats_chi_rate,
        "edgeworth_beats_normal_sparse_rate": edgeworth_beats_normal_rate,
        "edgeworth_tail_p_beats_normal_sparse_rate": (
            edgeworth_tail_p_beats_normal_rate
        ),
        "edgeworth_tail_fpr_nonworse_rate": edgeworth_tail_fpr_nonworse_rate,
        "normal_mean_tail_fpr_error": normal_tail_fpr_error,
        "edgeworth_mean_tail_fpr_error": edgeworth_tail_fpr_error,
        "diagnostic_correlations": diagnostic_correlations,
        "best_abs_diagnostic_correlation": best_diagnostic_correlation,
        "median_runtime_speedup": speedup,
        "sparse_configuration_count": int(sparse.shape[0]),
    }


def write_summary(
    results: pd.DataFrame,
    decision: dict[str, object],
    output_path: Path,
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Sparse CMI First-Stage Falsification Summary",
        "",
        f"**Decision: `{decision['verdict']}`**",
        "",
        (
            f"Profile `{args.profile}` evaluated "
            f"{results['configuration'].nunique()} configurations with "
            f"{args.null_samples:,} conditional-null draws per configuration "
            f"and {args.permutations:,} literal label permutations for runtime."
        ),
        "",
        "## Decision criteria",
        "",
        "| Criterion | Pass | Evidence |",
        "|---|---:|---:|",
        (
            "| Exact-moment normal beats informative-df chi-square in sparse cases "
            f"| {decision['criteria']['normal_beats_chi_sparse']} "
            f"| FPR: {decision['normal_beats_chi_sparse_rate']:.1%}; "
            f"p-value: {decision['normal_p_beats_chi_sparse_rate']:.1%} |"
        ),
        (
            "| Edgeworth broadly improves on exact-moment normal "
            f"| {decision['criteria']['skewness_correction_broadly_helps']} "
            f"| upper-tail p-value: "
            f"{decision['edgeworth_tail_p_beats_normal_sparse_rate']:.1%}; "
            f"tail FPR non-worse: "
            f"{decision['edgeworth_tail_fpr_nonworse_rate']:.1%} |"
        ),
        (
            "| Observable diagnostics predict normal tail error "
            f"| {decision['criteria']['diagnostics_predict_error']} "
            f"| best absolute Spearman rho: "
            f"{decision['best_abs_diagnostic_correlation']:.3f} |"
        ),
        (
            "| Exact-moment calculation is at least 10x faster than permutation "
            f"| {decision['criteria']['faster_than_permutation']} "
            f"| median speedup: {decision['median_runtime_speedup']:.1f}x |"
        ),
        "",
        "## Calibration",
        "",
        (
            "Mean absolute rejection-rate error relative to the attainable "
            "exact/Monte Carlo conditional reference:"
        ),
        "",
        "| Alpha | Normal | Edgeworth | Cornish-Fisher | Chi2 nominal | Chi2 informative |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for alpha in ALPHAS:
        subset = results[np.isclose(results["alpha"], alpha)]
        values = [
            subset[f"{method}_fpr_error_vs_reference"].mean()
            for method in METHODS
        ]
        lines.append(
            f"| {alpha:g} | "
            + " | ".join(f"{value:.5f}" for value in values)
            + " |"
        )

    lines.extend(
        [
            "",
            "## Reliability diagnostics",
            "",
            "| Diagnostic | Spearman rho with normal upper-tail p-value error |",
            "|---|---:|",
        ]
    )
    for name, correlation in decision["diagnostic_correlations"].items():
        lines.append(f"| {name} | {correlation:.3f} |")

    exact_count = results.loc[
        np.isclose(results["alpha"], 0.05), "reference"
    ].value_counts()
    lines.extend(
        [
            "",
            "## Reference coverage",
            "",
            *[
                f"- `{name}`: {int(count)} configurations"
                for name, count in exact_count.items()
            ],
            "",
            "## Interpretation guardrails",
            "",
            (
                "- `PROCEED` is only an empirical first-stage result. Novelty and "
                "the conditional Berry-Esseen theorem remain separate gates."
            ),
            (
                "- `NARROW_OR_REVISE` means exact centring/scaling may be useful "
                "but the proposed first-order skewness correction is not yet "
                "reliable enough to defend."
            ),
            (
                "- Exact conditional p-values are discrete and conservative. "
                "Approximation errors are therefore reported against both their "
                "attainable reference size and nominal alpha in the CSV."
            ),
            (
                "- Edgeworth is judged on upper-tail accuracy at alpha <= 0.05. "
                "Its whole-distribution p-value MAE is still recorded because "
                "a tail improvement can coexist with poorer central p-values."
            ),
            (
                "- Conditional Monte Carlo configurations should be rerun with "
                "more draws before publication, especially at alpha=0.001."
            ),
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def make_figures(results: pd.DataFrame, output_dir: Path) -> None:
    alpha_05 = results[np.isclose(results["alpha"], 0.05)].copy()
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    data = [
        alpha_05[f"{method}_fpr_error_vs_reference"].to_numpy()
        for method in METHODS
    ]
    ax.boxplot(data, tick_labels=[name.replace("_", "\n") for name in METHODS])
    ax.set_ylabel("Absolute rejection-rate error vs conditional reference")
    ax.set_title("Calibration error at alpha=0.05")
    fig.tight_layout()
    fig.savefig(figure_dir / "calibration_error_alpha_05.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 7))
    x = np.maximum(alpha_05["chi2_informative_p_mae"], 1e-8)
    y = np.maximum(alpha_05["normal_p_mae"], 1e-8)
    scatter = ax.scatter(
        x,
        y,
        c=alpha_05["lyapunov_ratio"],
        cmap="viridis",
        alpha=0.8,
    )
    limits = [min(x.min(), y.min()), max(x.max(), y.max())]
    ax.plot(limits, limits, color="black", linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Informative-df chi-square p-value MAE")
    ax.set_ylabel("Exact-moment normal p-value MAE")
    ax.set_title("Points below the line favour exact-moment normal")
    fig.colorbar(scatter, ax=ax, label="Lyapunov ratio")
    fig.tight_layout()
    fig.savefig(figure_dir / "normal_vs_chi2_pvalue_error.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        alpha_05["lyapunov_ratio"],
        alpha_05["normal_tail_p_mae"],
        c=alpha_05["max_variance_share"],
        cmap="magma",
        alpha=0.8,
    )
    ax.set_xlabel("Lyapunov ratio")
    ax.set_ylabel("Normal upper-tail p-value MAE")
    ax.set_title("Does the theoretical diagnostic predict tail error?")
    fig.tight_layout()
    fig.savefig(figure_dir / "diagnostic_tail_error.png", dpi=160)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    if args.null_samples <= 0:
        raise ValueError("--null-samples must be positive")
    if args.permutations < 0:
        raise ValueError("--permutations must be non-negative")

    configurations = validation_configurations(args.profile)
    if args.max_configurations is not None:
        configurations = configurations[: args.max_configurations]

    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = (
            Path(__file__).resolve().parents[1]
            / "results"
            / f"{args.profile}_{timestamp}"
        )
    else:
        output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    seed_sequence = np.random.SeedSequence(args.seed)
    child_seeds = seed_sequence.spawn(len(configurations))
    rows: list[dict[str, object]] = []
    checkpoint_path = output_dir / "configuration_results.partial.csv"

    started = time.perf_counter()
    for index, (configuration, child_seed) in enumerate(
        zip(configurations, child_seeds, strict=True),
        start=1,
    ):
        rows.extend(
            evaluate_configuration(
                configuration,
                null_samples=args.null_samples,
                permutations=args.permutations,
                rng=np.random.default_rng(child_seed),
                exact_max_states=args.exact_max_states,
                exact_max_informative=args.exact_max_informative,
            )
        )
        print(
            f"[{index:>3}/{len(configurations)}] {configuration.name}",
            flush=True,
        )
        if index % args.checkpoint_every == 0:
            pd.DataFrame(rows).to_csv(checkpoint_path, index=False)

    elapsed = time.perf_counter() - started
    results = pd.DataFrame(rows)
    results_path = output_dir / "configuration_results.csv"
    results.to_csv(results_path, index=False)
    if checkpoint_path.exists():
        checkpoint_path.unlink()

    decision = decision_summary(results)
    write_summary(results, decision, output_dir / "summary.md", args)
    make_figures(results, output_dir)

    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": sys.argv,
        "profile": args.profile,
        "seed": args.seed,
        "null_samples": args.null_samples,
        "permutations": args.permutations,
        "exact_max_states": args.exact_max_states,
        "exact_max_informative": args.exact_max_informative,
        "configuration_count": len(configurations),
        "elapsed_seconds": elapsed,
        "decision": decision,
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "pandas": pd.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    print(f"\nDecision: {decision['verdict']}")
    print(f"Results: {output_dir}")
    print(f"Elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
