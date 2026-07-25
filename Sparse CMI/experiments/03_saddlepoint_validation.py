#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
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
from scipy.stats import chi2

from sparse_cmi.approximations import (
    cornish_fisher_critical_value,
    edgeworth_pvalue,
    normal_pvalue,
)
from sparse_cmi.exact_convolution import (
    StateSpaceTooLarge,
    estimate_convolution_complexity,
    exact_conditional_distribution,
)
from sparse_cmi.moments import aggregate_moments
from sparse_cmi.permutation import label_permutation_g2, sample_conditional_g2
from sparse_cmi.saddlepoint import FactorizedConditionalCGF
from sparse_cmi.simulation import (
    ValidationConfiguration,
    validation_configurations,
)

ALPHAS = (0.10, 0.05, 0.01, 0.001)
METHODS = (
    "normal",
    "edgeworth",
    "cornish_fisher",
    "saddlepoint",
    "router",
    "chi2_nominal",
    "chi2_informative",
)
NUMERICAL_FAILURE_FALLBACKS = frozenset(
    {
        "root_failure_edgeworth",
        "tilted_variance_edgeworth",
        "nonpositive_radicand_edgeworth",
        "invalid_lr_edgeworth",
    }
)
PILOT_CONFIGURATION_NAMES = frozenset(
    item.name for item in validation_configurations("smoke")
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the deterministic factorised-CGF sparse-CMI test."
    )
    parser.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    parser.add_argument("--null-samples", type=int, default=20_000)
    parser.add_argument("--permutations", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=5030)
    parser.add_argument("--exact-max-states", type=int, default=100_000)
    parser.add_argument("--exact-max-transitions", type=int, default=100_000)
    parser.add_argument("--exact-max-informative", type=int)
    parser.add_argument("--max-configurations", type=int)
    parser.add_argument("--checkpoint-every", type=int, default=5)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def validation_split(name: str) -> str:
    digest = hashlib.sha256(name.encode("utf-8")).digest()
    return "heldout" if digest[0] % 3 == 0 else "development"


def collapsed_reference(
    statistics: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    rounded = np.round(np.asarray(statistics, dtype=np.float64), 12)
    values, counts = np.unique(rounded, return_counts=True)
    return values, counts.astype(np.float64) / rounded.size


def upper_tails(weights: np.ndarray) -> np.ndarray:
    return np.cumsum(weights[::-1])[::-1]


def rejection_probability(
    pvalues: np.ndarray,
    alpha: float,
    weights: np.ndarray,
) -> float:
    return float(np.dot(pvalues <= alpha, weights))


def threshold_fpr(
    values: np.ndarray,
    weights: np.ndarray,
    alpha: float,
    cgf: FactorizedConditionalCGF,
) -> tuple[float, float | None, int, int, int]:
    """Use monotonicity to find the first attainable saddlepoint rejection."""

    cache: dict[int, tuple[float, str]] = {}

    def evaluate(index: int) -> tuple[float, str]:
        if index not in cache:
            result = cgf.upper_tail(float(values[index]))
            cache[index] = (result.pvalue, result.fallback)
        return cache[index]

    def diagnostics() -> tuple[int, int]:
        guardrails = sum(bool(item[1]) for item in cache.values())
        failures = sum(
            item[1] in NUMERICAL_FAILURE_FALLBACKS for item in cache.values()
        )
        return guardrails, failures

    if evaluate(values.size - 1)[0] > alpha:
        guardrails, failures = diagnostics()
        return 0.0, None, len(cache), guardrails, failures
    if evaluate(0)[0] <= alpha:
        guardrails, failures = diagnostics()
        return 1.0, float(values[0]), len(cache), guardrails, failures

    lower = 0
    upper = values.size - 1
    while upper - lower > 1:
        middle = (lower + upper) // 2
        if evaluate(middle)[0] <= alpha:
            upper = middle
        else:
            lower = middle
    fpr = float(weights[upper:].sum())
    guardrails, failures = diagnostics()
    return fpr, float(values[upper]), len(cache), guardrails, failures


def quantile_error_metrics(
    values: np.ndarray,
    weights: np.ndarray,
    truth_pvalues: np.ndarray,
    cgf: FactorizedConditionalCGF,
) -> dict[str, object]:
    cdf = np.cumsum(weights)
    quantiles = np.linspace(0.001, 0.999, 199)
    indices = np.unique(np.searchsorted(cdf, quantiles, side="left"))
    indices = np.clip(indices, 0, values.size - 1)
    results = [cgf.upper_tail(float(values[index])) for index in indices]
    fallback_reasons = Counter(
        item.fallback for item in results if item.fallback
    )
    saddlepoint_pvalues = np.asarray([item.pvalue for item in results])
    truth = truth_pvalues[indices]
    tail = truth <= 0.10
    return {
        "saddlepoint_quantile_p_mae": float(
            np.mean(np.abs(saddlepoint_pvalues - truth))
        ),
        "saddlepoint_tail_quantile_p_mae": float(
            np.mean(np.abs(saddlepoint_pvalues[tail] - truth[tail]))
            if np.any(tail)
            else 0.0
        ),
        "saddlepoint_quantile_max_error": float(
            np.max(np.abs(saddlepoint_pvalues - truth))
        ),
        "saddlepoint_quantile_monotonicity_violations": int(
            np.count_nonzero(np.diff(saddlepoint_pvalues) > 1e-9)
        ),
        "saddlepoint_quantile_evaluations": int(indices.size),
        "saddlepoint_quantile_fallbacks": int(
            sum(bool(item.fallback) for item in results)
        ),
        "saddlepoint_quantile_numerical_failures": int(
            sum(
                item.fallback in NUMERICAL_FAILURE_FALLBACKS
                for item in results
            )
        ),
        "saddlepoint_quantile_guardrail_reasons": json.dumps(
            fallback_reasons,
            sort_keys=True,
        ),
    }


def evaluate_configuration(
    configuration: ValidationConfiguration,
    *,
    null_samples: int,
    permutations: int,
    rng: np.random.Generator,
    exact_max_states: int,
    exact_max_transitions: int,
    exact_max_informative: int | None,
) -> list[dict[str, object]]:
    moments_started = time.perf_counter()
    moments = aggregate_moments(configuration.strata)
    moments_seconds = time.perf_counter() - moments_started
    complexity_started = time.perf_counter()
    complexity = estimate_convolution_complexity(
        configuration.strata,
        cap=max(exact_max_states, exact_max_transitions),
    )
    complexity_seconds = time.perf_counter() - complexity_started

    exact = None
    exact_seconds = 0.0
    informative_allowed = (
        exact_max_informative is None
        or moments.informative_strata <= exact_max_informative
    )
    exact_is_bounded = (
        complexity.state_upper_bound <= exact_max_states
        and complexity.transition_upper_bound <= exact_max_transitions
    )
    if informative_allowed and exact_is_bounded:
        started = time.perf_counter()
        try:
            exact = exact_conditional_distribution(
                configuration.strata,
                max_states=exact_max_states,
            )
        except StateSpaceTooLarge:
            pass
        exact_seconds = time.perf_counter() - started

    sampled = sample_conditional_g2(
        configuration.strata,
        samples=null_samples,
        rng=rng,
    )
    if exact is not None:
        values = exact.values
        weights = exact.probabilities
        reference = "exact_convolution"
        exact_state_count: int | None = int(values.size)
    else:
        values, weights = collapsed_reference(sampled)
        reference = "conditional_monte_carlo"
        exact_state_count = None
    truth_pvalues = upper_tails(weights)

    cgf_started = time.perf_counter()
    cgf = FactorizedConditionalCGF(configuration.strata)
    cgf_build_seconds = time.perf_counter() - cgf_started
    quantile_metrics = quantile_error_metrics(
        values,
        weights,
        truth_pvalues,
        cgf,
    )

    normal_p = np.asarray(normal_pvalue(values, moments.mean, moments.variance))
    edgeworth_p = np.asarray(
        edgeworth_pvalue(
            values,
            moments.mean,
            moments.variance,
            moments.skewness,
        )
    )
    nominal_p = chi2.sf(values, len(configuration.strata))
    informative_p = (
        chi2.sf(values, moments.informative_strata)
        if moments.informative_strata
        else np.ones_like(values)
    )

    cdf = np.cumsum(weights)
    benchmark_index = int(np.searchsorted(cdf, 0.95, side="left"))
    benchmark_index = min(benchmark_index, values.size - 1)
    pvalue_repeats = 10
    pvalue_started = time.perf_counter()
    for _ in range(pvalue_repeats):
        cgf.upper_tail(float(values[benchmark_index]))
    saddlepoint_pvalue_seconds = (
        time.perf_counter() - pvalue_started
    ) / pvalue_repeats

    permutation_seconds: float | None = None
    if permutations > 0:
        permutation_started = time.perf_counter()
        label_permutation_g2(
            configuration.strata,
            permutations=permutations,
            rng=rng,
        )
        permutation_seconds = time.perf_counter() - permutation_started

    exact_router = exact is not None
    router_route = "exact_convolution" if exact_router else "saddlepoint"
    router_seconds = (
        moments_seconds + complexity_seconds + exact_seconds
        if exact_router
        else (
            moments_seconds
            + complexity_seconds
            + cgf_build_seconds
            + saddlepoint_pvalue_seconds
        )
    )

    common: dict[str, object] = {
        "configuration": configuration.name,
        "family": configuration.family,
        "split": validation_split(configuration.name),
        "seen_in_router_pilot": (
            configuration.name in PILOT_CONFIGURATION_NAMES
        ),
        "total_n": configuration.total_n,
        "total_strata": len(configuration.strata),
        "informative_strata": moments.informative_strata,
        "lyapunov_ratio": moments.lyapunov_ratio,
        "max_variance_share": moments.max_variance_share,
        "skewness": moments.skewness,
        "reference": reference,
        "exact_state_count": exact_state_count,
        "exact_state_upper_bound": complexity.state_upper_bound,
        "exact_transition_upper_bound": complexity.transition_upper_bound,
        "router_route": router_route,
        "moments_seconds": moments_seconds,
        "complexity_seconds": complexity_seconds,
        "exact_seconds": exact_seconds,
        "cgf_build_seconds": cgf_build_seconds,
        "cgf_components": cgf.component_count,
        "cgf_unique_components": cgf.unique_component_count,
        "saddlepoint_pvalue_seconds": saddlepoint_pvalue_seconds,
        "router_seconds": router_seconds,
        "permutation_seconds": permutation_seconds,
        "runtime_speedup_vs_permutation": (
            permutation_seconds / router_seconds
            if permutation_seconds is not None and router_seconds > 0
            else None
        ),
        **quantile_metrics,
    }

    rows: list[dict[str, object]] = []
    for alpha in ALPHAS:
        truth_fpr = rejection_probability(truth_pvalues, alpha, weights)
        normal_fpr = rejection_probability(normal_p, alpha, weights)
        edgeworth_fpr = rejection_probability(edgeworth_p, alpha, weights)
        nominal_fpr = rejection_probability(nominal_p, alpha, weights)
        informative_fpr = rejection_probability(informative_p, alpha, weights)
        cf_threshold = cornish_fisher_critical_value(
            alpha,
            moments.mean,
            moments.variance,
            moments.skewness,
        )
        cf_fpr = float(weights[values >= cf_threshold - 1e-10].sum())
        (
            saddle_fpr,
            saddle_threshold,
            evaluations,
            guardrails,
            numerical_failures,
        ) = threshold_fpr(values, weights, alpha, cgf)
        router_fpr = truth_fpr if exact_router else saddle_fpr
        fprs = {
            "normal": normal_fpr,
            "edgeworth": edgeworth_fpr,
            "cornish_fisher": cf_fpr,
            "saddlepoint": saddle_fpr,
            "router": router_fpr,
            "chi2_nominal": nominal_fpr,
            "chi2_informative": informative_fpr,
        }
        row = dict(common)
        row.update(
            {
                "alpha": alpha,
                "reference_fpr": truth_fpr,
                "saddlepoint_threshold": saddle_threshold,
                "saddlepoint_threshold_evaluations": evaluations,
                "saddlepoint_threshold_guardrails": guardrails,
                "saddlepoint_threshold_numerical_failures": numerical_failures,
            }
        )
        for method, fpr in fprs.items():
            row[f"{method}_fpr"] = fpr
            row[f"{method}_fpr_error_vs_reference"] = abs(fpr - truth_fpr)
            row[f"{method}_size_distortion"] = abs(fpr - alpha)
        rows.append(row)
    return rows


def write_summary(
    results: pd.DataFrame,
    output_path: Path,
    args: argparse.Namespace,
) -> None:
    heldout = results[results["split"] == "heldout"]
    heldout_05 = heldout[np.isclose(heldout["alpha"], 0.05)]
    saddle_only_05 = heldout_05[heldout_05["router_route"] == "saddlepoint"]
    speedups = heldout_05["runtime_speedup_vs_permutation"].dropna()
    speedup = float(speedups.median()) if not speedups.empty else None
    exact_routes = int(
        heldout_05["router_route"].eq("exact_convolution").sum()
    )
    total_heldout = int(heldout_05.shape[0])

    def append_error_table(
        lines: list[str],
        subset: pd.DataFrame,
    ) -> None:
        lines.extend(
            [
                "| Alpha | Normal | Edgeworth | Cornish-Fisher | Raw "
                "saddlepoint | Deterministic router | Chi2 nominal | "
                "Chi2 informative |",
                "|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for alpha in ALPHAS:
            alpha_subset = subset[np.isclose(subset["alpha"], alpha)]
            errors = [
                alpha_subset[f"{method}_fpr_error_vs_reference"].mean()
                for method in METHODS
            ]
            lines.append(
                f"| {alpha:g} | "
                + " | ".join(f"{value:.5f}" for value in errors)
                + " |"
            )

    lines = [
        "# Deterministic Sparse-CMI Saddlepoint Validation",
        "",
        (
            f"Profile `{args.profile}` evaluated "
            f"{results['configuration'].nunique()} configurations. The "
            "development/held-out split is a stable hash of the configuration "
            "name and is independent of method performance."
        ),
        "",
        "## Held-out calibration",
        "",
        "Mean absolute rejection-rate error versus the conditional reference:",
        "",
    ]
    append_error_table(lines, heldout)

    confirmation = results[~results["seen_in_router_pilot"]]
    if not confirmation.empty:
        lines.extend(
            [
                "",
                "## Post-pilot confirmation set",
                "",
                (
                    f"These {confirmation['configuration'].nunique()} "
                    "configurations were absent from the smoke grid used to "
                    "correct the router. Mean absolute rejection-rate error:"
                ),
                "",
            ]
        )
        append_error_table(lines, confirmation)

    lines.extend(
        [
            "",
            "## Route coverage",
            "",
            (
                f"Exact convolution handled {exact_routes}/{total_heldout} "
                "held-out configurations; the remainder used saddlepoint."
            ),
            (
                f"Median held-out speedup versus {args.permutations:,} literal "
                f"within-stratum permutations was {speedup:.1f}x."
                if speedup is not None
                else "No held-out permutation timing was available."
            ),
            "",
            "## Saddlepoint-only held-out cases at alpha=0.05",
            "",
        ]
    )
    if saddle_only_05.empty:
        lines.append(
            "No held-out configuration in this run required the saddlepoint "
            "route; use a larger profile before judging its calibration."
        )
    else:
        lines.extend(
            [
                "| Method | Mean FPR error | Maximum FPR error |",
                "|---|---:|---:|",
            ]
        )
        for method in (
            "edgeworth",
            "cornish_fisher",
            "saddlepoint",
            "chi2_nominal",
        ):
            values = saddle_only_05[f"{method}_fpr_error_vs_reference"]
            lines.append(
                f"| {method} | {values.mean():.5f} | {values.max():.5f} |"
            )

    numerical_failures = int(
        heldout_05["saddlepoint_threshold_numerical_failures"].sum()
    )
    quantile_failures = int(
        heldout_05["saddlepoint_quantile_numerical_failures"].sum()
    )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            (
                f"- Numerical failures: {numerical_failures} during critical-"
                f"value searches and {quantile_failures} across p-value "
                "diagnostic quantiles."
            ),
            (
                "- Raw saddlepoint and routed results are reported separately. "
                "Exact routing cannot be used to conceal saddlepoint failures."
            ),
            (
                "- Exact routing requires guaranteed upper bounds of at most "
                f"{args.exact_max_states:,} states and "
                f"{args.exact_max_transitions:,} transitions"
                + (
                    f", plus `informative_strata <= "
                    f"{args.exact_max_informative}`."
                    if args.exact_max_informative is not None
                    else "."
                )
            ),
            (
                "- Monte Carlo reference rows have finite resolution; alpha "
                "0.001 remains exploratory unless exact convolution is available."
            ),
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def make_figure(results: pd.DataFrame, output_dir: Path) -> None:
    heldout = results[
        (results["split"] == "heldout") & np.isclose(results["alpha"], 0.05)
    ]
    methods = (
        "normal",
        "edgeworth",
        "cornish_fisher",
        "saddlepoint",
        "router",
        "chi2_nominal",
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.boxplot(
        [
            heldout[f"{method}_fpr_error_vs_reference"].to_numpy()
            for method in methods
        ],
        tick_labels=[method.replace("_", "\n") for method in methods],
    )
    ax.set_ylabel("Absolute FPR error vs conditional reference")
    ax.set_title("Held-out deterministic-method calibration at alpha=0.05")
    fig.tight_layout()
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figure_dir / "heldout_fpr_error_alpha_05.png", dpi=160)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    configurations = validation_configurations(args.profile)
    if args.max_configurations is not None:
        configurations = configurations[: args.max_configurations]
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = (
            Path(__file__).resolve().parents[1]
            / "results"
            / f"saddlepoint_{args.profile}_{timestamp}"
        )
    else:
        output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    seeds = np.random.SeedSequence(args.seed).spawn(len(configurations))
    rows: list[dict[str, object]] = []
    checkpoint = output_dir / "saddlepoint_results.partial.csv"
    started = time.perf_counter()
    for index, (configuration, seed) in enumerate(
        zip(configurations, seeds, strict=True),
        start=1,
    ):
        rows.extend(
            evaluate_configuration(
                configuration,
                null_samples=args.null_samples,
                permutations=args.permutations,
                rng=np.random.default_rng(seed),
                exact_max_states=args.exact_max_states,
                exact_max_transitions=args.exact_max_transitions,
                exact_max_informative=args.exact_max_informative,
            )
        )
        print(
            f"[{index:>3}/{len(configurations)}] {configuration.name}",
            flush=True,
        )
        if index % args.checkpoint_every == 0:
            pd.DataFrame(rows).to_csv(checkpoint, index=False)

    elapsed = time.perf_counter() - started
    results = pd.DataFrame(rows)
    results.to_csv(output_dir / "saddlepoint_results.csv", index=False)
    if checkpoint.exists():
        checkpoint.unlink()
    write_summary(results, output_dir / "summary.md", args)
    make_figure(results, output_dir)
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": sys.argv,
        "profile": args.profile,
        "seed": args.seed,
        "null_samples": args.null_samples,
        "permutations": args.permutations,
        "exact_max_states": args.exact_max_states,
        "exact_max_transitions": args.exact_max_transitions,
        "exact_max_informative": args.exact_max_informative,
        "configuration_count": len(configurations),
        "elapsed_seconds": elapsed,
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
    print(f"\nResults: {output_dir}")
    print(f"Elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
