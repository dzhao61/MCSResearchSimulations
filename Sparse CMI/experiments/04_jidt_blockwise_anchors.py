#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest, chi2

from sparse_cmi.jidt import (
    DEFAULT_JIDT_JAR,
    jidt_conditional_significance,
    start_jidt_jvm,
)
from sparse_cmi.models import Stratum
from sparse_cmi.moments import aggregate_moments
from sparse_cmi.permutation import monte_carlo_pvalue, sample_conditional_g2
from sparse_cmi.routing import deterministic_pvalue
from sparse_cmi.simulation import (
    ValidationConfiguration,
    validation_configurations,
)
from sparse_cmi.statistic import g2_for_a, observed_g2


DEFAULT_ANCHORS = (
    "homogeneous_k20_n10_both_skew",
    "dominant_stratum_k100",
    "homogeneous_k10_n30_balanced",
    "homogeneous_k50_n30_both_skew",
    "homogeneous_k100_n30_balanced",
    "heterogeneous_k100_v1",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare the deterministic binary-CMI test to JIDT."
    )
    parser.add_argument("--permutations", type=int, default=1_000)
    parser.add_argument("--reference-samples", type=int, default=200_000)
    parser.add_argument("--candidate-samples", type=int, default=20_000)
    parser.add_argument("--target-quantile", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=5030)
    parser.add_argument("--jar-path", type=Path, default=DEFAULT_JIDT_JAR)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--anchors", nargs="*", default=list(DEFAULT_ANCHORS))
    return parser.parse_args()


def select_tail_table(
    configuration: ValidationConfiguration,
    *,
    samples: int,
    quantile: float,
    rng: np.random.Generator,
) -> tuple[Stratum, ...]:
    if samples <= 0:
        raise ValueError("candidate samples must be positive")
    if not 0 < quantile < 1:
        raise ValueError("target quantile must lie between zero and one")

    draws = np.empty(
        (samples, len(configuration.strata)),
        dtype=np.int32,
    )
    totals = np.zeros(samples, dtype=np.float64)
    for index, stratum in enumerate(configuration.strata):
        if stratum.support_width == 1:
            values = np.full(samples, stratum.support_min, dtype=np.int32)
        else:
            values = rng.hypergeometric(
                ngood=stratum.s,
                nbad=stratum.n - stratum.s,
                nsample=stratum.r,
                size=samples,
            ).astype(np.int32)
        draws[:, index] = values
        totals += np.asarray(
            g2_for_a(stratum.n, stratum.r, stratum.s, values)
        )

    target = float(np.quantile(totals, quantile, method="higher"))
    selected = int(np.argmin(np.abs(totals - target)))
    return tuple(
        Stratum(
            stratum.n,
            stratum.r,
            stratum.s,
            int(draws[selected, index]),
            stratum.label,
        )
        for index, stratum in enumerate(configuration.strata)
    )


def wilson_interval(pvalue: float, permutations: int) -> tuple[float, float]:
    exceedances = int(round(pvalue * permutations))
    interval = binomtest(exceedances, permutations).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    return float(interval.low), float(interval.high)


def evaluate_anchor(
    configuration: ValidationConfiguration,
    *,
    permutations: int,
    reference_samples: int,
    candidate_samples: int,
    target_quantile: float,
    rng: np.random.Generator,
    jar_path: Path,
) -> dict[str, object]:
    stage_seeds = rng.integers(
        0,
        np.iinfo(np.int64).max,
        size=3,
        dtype=np.int64,
    )
    candidate_rng, reference_rng, blockwise_rng = (
        np.random.default_rng(int(seed)) for seed in stage_seeds
    )
    strata = select_tail_table(
        configuration,
        samples=candidate_samples,
        quantile=target_quantile,
        rng=candidate_rng,
    )
    statistic = observed_g2(strata)

    router_repeats = 10
    started = time.perf_counter()
    routed = None
    for _ in range(router_repeats):
        routed = deterministic_pvalue(strata, statistic=statistic)
    router_seconds = (time.perf_counter() - started) / router_repeats
    assert routed is not None

    if routed.route == "exact_convolution":
        reference_p = routed.pvalue
        reference = "exact_convolution"
    else:
        reference_statistics = sample_conditional_g2(
            strata,
            samples=reference_samples,
            rng=reference_rng,
        )
        reference_p = monte_carlo_pvalue(statistic, reference_statistics)
        reference = "conditional_monte_carlo"

    blockwise = jidt_conditional_significance(
        strata,
        permutations=permutations,
        shuffle_mode="blockwise",
        rng=blockwise_rng,
        jar_path=jar_path,
    )
    default_global = jidt_conditional_significance(
        strata,
        permutations=permutations,
        shuffle_mode="default_global",
        jar_path=jar_path,
    )
    block_low, block_high = wilson_interval(
        blockwise.tie_corrected_pvalue,
        permutations,
    )

    moments = aggregate_moments(strata)
    chi2_nominal_p = float(chi2.sf(statistic, len(strata)))
    chi2_informative_p = (
        float(chi2.sf(statistic, moments.informative_strata))
        if moments.informative_strata
        else 1.0
    )
    return {
        "configuration": configuration.name,
        "family": configuration.family,
        "total_n": sum(item.n for item in strata),
        "strata": len(strata),
        "informative_strata": moments.informative_strata,
        "statistic_g2": statistic,
        "reference": reference,
        "reference_p": reference_p,
        "router_route": routed.route,
        "router_p": routed.pvalue,
        "router_seconds": router_seconds,
        "router_abs_error": abs(routed.pvalue - reference_p),
        "exact_state_count": routed.exact_state_count,
        "exact_state_upper_bound": routed.exact_state_upper_bound,
        "exact_transition_upper_bound": routed.exact_transition_upper_bound,
        "jidt_blockwise_p": blockwise.pvalue,
        "jidt_blockwise_tie_corrected_p": (
            blockwise.tie_corrected_pvalue
        ),
        "jidt_blockwise_ci_low": block_low,
        "jidt_blockwise_ci_high": block_high,
        "jidt_blockwise_seconds": blockwise.elapsed_seconds,
        "jidt_blockwise_abs_error": abs(
            blockwise.tie_corrected_pvalue - reference_p
        ),
        "jidt_default_global_p": default_global.pvalue,
        "jidt_default_global_tie_corrected_p": (
            default_global.tie_corrected_pvalue
        ),
        "jidt_default_global_seconds": default_global.elapsed_seconds,
        "jidt_default_abs_error": abs(default_global.pvalue - reference_p),
        "jidt_g2": blockwise.g2,
        "manual_jidt_g2_abs_difference": abs(statistic - blockwise.g2),
        "chi2_nominal_p": chi2_nominal_p,
        "chi2_nominal_abs_error": abs(chi2_nominal_p - reference_p),
        "chi2_informative_p": chi2_informative_p,
        "chi2_informative_abs_error": abs(
            chi2_informative_p - reference_p
        ),
        "speedup_vs_jidt_blockwise": (
            blockwise.elapsed_seconds / router_seconds
        ),
        "permutations": permutations,
        "jidt_pvalue_resolution": 1.0 / permutations,
    }


def write_summary(results: pd.DataFrame, output_path: Path) -> None:
    lines = [
        "# JIDT Blockwise Anchor Comparison",
        "",
        (
            "JIDT blockwise orderings preserve both binary margins inside "
            "every conditioning stratum. JIDT's default global shuffle is "
            "reported separately and is not the same null in heterogeneous "
            "strata."
        ),
        "",
        "| Configuration | N | Route | Reference p | Router p | JIDT "
        "blockwise p (corrected) | JIDT raw p | JIDT default raw p | "
        "Router ms | JIDT blockwise ms | Speedup |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results.itertuples(index=False):
        lines.append(
            f"| {row.configuration} | {row.total_n} | {row.router_route} | "
            f"{row.reference_p:.5f} | {row.router_p:.5f} | "
            f"{row.jidt_blockwise_tie_corrected_p:.5f} | "
            f"{row.jidt_blockwise_p:.5f} | "
            f"{row.jidt_default_global_p:.5f} | "
            f"{1e3 * row.router_seconds:.3f} | "
            f"{1e3 * row.jidt_blockwise_seconds:.3f} | "
            f"{row.speedup_vs_jidt_blockwise:.1f}x |"
        )

    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            (
                f"- Median speedup versus JIDT blockwise permutation: "
                f"{results['speedup_vs_jidt_blockwise'].median():.1f}x."
            ),
            (
                f"- Median absolute p-value error: router "
                f"{results['router_abs_error'].median():.5f}, JIDT blockwise "
                f"{results['jidt_blockwise_abs_error'].median():.5f}, "
                f"chi-square nominal "
                f"{results['chi2_nominal_abs_error'].median():.5f}."
            ),
            (
                f"- Maximum manual-versus-JIDT `G^2` difference: "
                f"{results['manual_jidt_g2_abs_difference'].max():.3e}."
            ),
            (
                "- JIDT Monte Carlo p-values use `count / permutations`; with "
                f"{int(results['permutations'].iloc[0]):,} permutations their "
                f"resolution is {results['jidt_pvalue_resolution'].iloc[0]:g}."
            ),
            (
                "- JIDT's raw p-value uses an exact floating-point `>=` "
                "comparison. The corrected column recomputes the rank from "
                "JIDT's own surrogate values with a `G^2` tolerance of "
                "`1e-10`, so mathematically tied tables are counted together."
            ),
            (
                "- Runtime is a steady-state comparison: JVM startup and a "
                "small JIT warmup are excluded; JIDT ordering construction "
                "and conversion are included. Router time is the mean of ten "
                "complete calls."
            ),
            (
                "- Explicit blockwise orderings use the recorded NumPy seed. "
                "JIDT's default-global overload owns its RNG and is retained "
                "as a non-reproducible diagnostic baseline only."
            ),
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.output_dir is None:
        output_dir = (
            Path(__file__).resolve().parents[1]
            / "results"
            / f"jidt_anchors_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
    else:
        output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    available = {
        item.name: item for item in validation_configurations("full")
    }
    missing = sorted(set(args.anchors) - set(available))
    if missing:
        raise ValueError(f"unknown anchor configurations: {missing}")

    start_jidt_jvm(args.jar_path)
    warmup = [Stratum(4, 2, 2, 1, 0), Stratum(4, 2, 2, 1, 1)]
    jidt_conditional_significance(
        warmup,
        permutations=10,
        shuffle_mode="blockwise",
        rng=np.random.default_rng(args.seed),
        jar_path=args.jar_path,
    )

    seeds = np.random.SeedSequence(args.seed).spawn(len(args.anchors))
    rows = []
    started = time.perf_counter()
    for index, (name, seed) in enumerate(
        zip(args.anchors, seeds, strict=True),
        start=1,
    ):
        rows.append(
            evaluate_anchor(
                available[name],
                permutations=args.permutations,
                reference_samples=args.reference_samples,
                candidate_samples=args.candidate_samples,
                target_quantile=args.target_quantile,
                rng=np.random.default_rng(seed),
                jar_path=args.jar_path,
            )
        )
        print(f"[{index}/{len(args.anchors)}] {name}", flush=True)

    elapsed = time.perf_counter() - started
    results = pd.DataFrame(rows)
    results.to_csv(output_dir / "jidt_anchor_results.csv", index=False)
    write_summary(results, output_dir / "summary.md")
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": sys.argv,
        "seed": args.seed,
        "permutations": args.permutations,
        "reference_samples": args.reference_samples,
        "candidate_samples": args.candidate_samples,
        "target_quantile": args.target_quantile,
        "elapsed_seconds": elapsed,
        "jidt_jar": str(args.jar_path),
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "pandas": pd.__version__,
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
