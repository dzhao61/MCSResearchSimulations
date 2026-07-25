#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import chi2, norm

from sparse_cmi.approximations import edgeworth_pvalue, normal_pvalue
from sparse_cmi.models import Stratum
from sparse_cmi.moments import StratumMoments, stratum_moments
from sparse_cmi.permutation import monte_carlo_pvalue, sample_conditional_g2
from sparse_cmi.statistic import g2_for_a

ALPHAS = (0.10, 0.05, 0.01)
METHODS = (
    "normal",
    "edgeworth",
    "cornish_fisher",
    "chi2_nominal",
    "chi2_informative",
    "conditional_mc",
)


@dataclass(frozen=True)
class DGPConfiguration:
    name: str
    k: int
    average_n: int
    margin_pattern: str
    z_pattern: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Unconditional calibration of conditional sparse CMI tests."
    )
    parser.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    parser.add_argument("--replicates", type=int, default=5_000)
    parser.add_argument("--anchor-replicates", type=int, default=100)
    parser.add_argument("--anchor-samples", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=5030)
    parser.add_argument("--checkpoint-every", type=int, default=5)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def configurations(profile: str) -> list[DGPConfiguration]:
    if profile == "smoke":
        k_values = (10, 50)
        average_sizes = (5, 20)
    else:
        k_values = (5, 20, 100)
        average_sizes = (3, 5, 10, 20, 30)
    return [
        DGPConfiguration(
            name=f"k{k}_n{average_n}_{margin}_{z_pattern}",
            k=k,
            average_n=average_n,
            margin_pattern=margin,
            z_pattern=z_pattern,
        )
        for k in k_values
        for average_n in average_sizes
        for margin in ("balanced", "both_skew", "asymmetric", "heterogeneous")
        for z_pattern in ("fixed_equal", "random_uniform")
    ]


def marginal_probabilities(
    k: int,
    pattern: str,
) -> tuple[np.ndarray, np.ndarray]:
    if pattern == "balanced":
        return np.full(k, 0.5), np.full(k, 0.5)
    if pattern == "both_skew":
        return np.full(k, 0.1), np.full(k, 0.1)
    if pattern == "asymmetric":
        return np.full(k, 0.1), np.full(k, 0.5)
    if pattern == "heterogeneous":
        x_cycle = np.asarray((0.05, 0.10, 0.25, 0.50, 0.90))
        y_cycle = np.asarray((0.50, 0.90, 0.10, 0.25, 0.05))
        indices = np.arange(k)
        return x_cycle[indices % 5], y_cycle[(2 * indices + 1) % 5]
    raise ValueError(f"unknown margin pattern: {pattern}")


def generate_null_tables(
    configuration: DGPConfiguration,
    replicates: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    total_n = configuration.k * configuration.average_n
    if configuration.z_pattern == "fixed_equal":
        n_values = np.full(
            (replicates, configuration.k),
            configuration.average_n,
            dtype=np.int64,
        )
    elif configuration.z_pattern == "random_uniform":
        n_values = rng.multinomial(
            total_n,
            np.full(configuration.k, 1.0 / configuration.k),
            size=replicates,
        )
    else:
        raise ValueError(f"unknown Z pattern: {configuration.z_pattern}")

    p_x, p_y = marginal_probabilities(
        configuration.k,
        configuration.margin_pattern,
    )
    p11 = p_x * p_y
    p10 = p_x * (1.0 - p_y)
    p01 = (1.0 - p_x) * p_y

    # Sequential binomials generate multinomial 2x2 cells and accept a
    # different stratum size on every replicate.
    a_values = rng.binomial(n_values, p11)
    remaining = n_values - a_values
    p10_conditional = p10 / (1.0 - p11)
    b_values = rng.binomial(remaining, p10_conditional)
    remaining -= b_values
    p01_conditional = p01 / (p01 + (1.0 - p_x) * (1.0 - p_y))
    c_values = rng.binomial(remaining, p01_conditional)
    r_values = a_values + b_values
    s_values = a_values + c_values
    return n_values, r_values, s_values, a_values


def aggregate_replicates(
    n_values: np.ndarray,
    r_values: np.ndarray,
    s_values: np.ndarray,
    a_values: np.ndarray,
) -> dict[str, np.ndarray]:
    replicates, k = n_values.shape
    statistic = np.zeros(replicates)
    mean = np.zeros(replicates)
    variance = np.zeros(replicates)
    third = np.zeros(replicates)
    absolute_third = np.zeros(replicates)
    max_stratum_variance = np.zeros(replicates)
    informative = np.zeros(replicates, dtype=np.int64)
    moment_cache: dict[tuple[int, int, int], StratumMoments] = {}

    for z_index in range(k):
        margins = np.column_stack(
            (
                n_values[:, z_index],
                r_values[:, z_index],
                s_values[:, z_index],
            )
        )
        unique_margins, inverse = np.unique(
            margins,
            axis=0,
            return_inverse=True,
        )
        for group_index, (n, r, s) in enumerate(unique_margins):
            mask = inverse == group_index
            key = (int(n), int(r), int(s))
            moments = moment_cache.get(key)
            if moments is None:
                lower = max(0, int(r + s - n))
                moments = stratum_moments(
                    Stratum(int(n), int(r), int(s), lower)
                )
                moment_cache[key] = moments
            statistic[mask] += np.asarray(
                g2_for_a(
                    int(n),
                    int(r),
                    int(s),
                    a_values[mask, z_index],
                )
            )
            mean[mask] += moments.mean
            variance[mask] += moments.variance
            third[mask] += moments.third_cumulant
            absolute_third[mask] += moments.absolute_third_central
            if moments.variance > 0:
                informative[mask] += 1
                max_stratum_variance[mask] = np.maximum(
                    max_stratum_variance[mask],
                    moments.variance,
                )

    positive_variance = variance > 0
    skewness = np.zeros(replicates)
    lyapunov = np.zeros(replicates)
    max_variance_share = np.zeros(replicates)
    skewness[positive_variance] = (
        third[positive_variance] / variance[positive_variance] ** 1.5
    )
    lyapunov[positive_variance] = (
        absolute_third[positive_variance] / variance[positive_variance] ** 1.5
    )
    max_variance_share[positive_variance] = (
        max_stratum_variance[positive_variance] / variance[positive_variance]
    )
    return {
        "statistic": statistic,
        "mean": mean,
        "variance": variance,
        "skewness": skewness,
        "informative": informative,
        "lyapunov": lyapunov,
        "max_variance_share": max_variance_share,
    }


def pvalue_arrays(
    aggregate: dict[str, np.ndarray],
    nominal_df: int,
) -> dict[str, np.ndarray]:
    statistic = aggregate["statistic"]
    mean = aggregate["mean"]
    variance = aggregate["variance"]
    skewness = aggregate["skewness"]
    normal_p = np.asarray(normal_pvalue(statistic, mean, variance))
    edgeworth_p = np.asarray(
        edgeworth_pvalue(statistic, mean, variance, skewness)
    )
    nominal_p = chi2.sf(statistic, nominal_df)
    informative_p = np.ones_like(statistic)
    positive_df = aggregate["informative"] > 0
    informative_p[positive_df] = chi2.sf(
        statistic[positive_df],
        aggregate["informative"][positive_df],
    )
    return {
        "normal": normal_p,
        "edgeworth": edgeworth_p,
        "chi2_nominal": nominal_p,
        "chi2_informative": informative_p,
    }


def conditional_mc_anchors(
    configuration: DGPConfiguration,
    n_values: np.ndarray,
    r_values: np.ndarray,
    s_values: np.ndarray,
    a_values: np.ndarray,
    approximation_pvalues: dict[str, np.ndarray],
    *,
    anchor_replicates: int,
    anchor_samples: int,
    rng: np.random.Generator,
) -> dict[str, object]:
    count = min(anchor_replicates, n_values.shape[0])
    indices = np.linspace(0, n_values.shape[0] - 1, count, dtype=int)
    conditional_pvalues = np.empty(count)
    started = time.perf_counter()
    for output_index, replicate_index in enumerate(indices):
        strata = [
            Stratum(
                int(n_values[replicate_index, z]),
                int(r_values[replicate_index, z]),
                int(s_values[replicate_index, z]),
                int(a_values[replicate_index, z]),
                z,
            )
            for z in range(configuration.k)
        ]
        null_statistics = sample_conditional_g2(
            strata,
            samples=anchor_samples,
            rng=rng,
        )
        conditional_pvalues[output_index] = monte_carlo_pvalue(
            float(approximation_pvalues["statistic"][replicate_index]),
            null_statistics,
        )
    elapsed = time.perf_counter() - started
    result: dict[str, object] = {
        "conditional_mc_seconds": elapsed,
        "conditional_mc_seconds_per_table": elapsed / count,
        "conditional_mc_anchor_count": count,
        "conditional_mc_samples": anchor_samples,
        "conditional_mc_pvalues": conditional_pvalues,
        "anchor_indices": indices,
    }
    for method in (
        "normal",
        "edgeworth",
        "chi2_nominal",
        "chi2_informative",
    ):
        result[f"{method}_anchor_p_mae"] = float(
            np.mean(
                np.abs(
                    approximation_pvalues[method][indices]
                    - conditional_pvalues
                )
            )
        )
    return result


def evaluate_configuration(
    configuration: DGPConfiguration,
    *,
    replicates: int,
    anchor_replicates: int,
    anchor_samples: int,
    rng: np.random.Generator,
) -> list[dict[str, object]]:
    n_values, r_values, s_values, a_values = generate_null_tables(
        configuration,
        replicates,
        rng,
    )
    method_started = time.perf_counter()
    aggregate = aggregate_replicates(n_values, r_values, s_values, a_values)
    pvalues = pvalue_arrays(aggregate, configuration.k)
    method_seconds = time.perf_counter() - method_started
    pvalues["statistic"] = aggregate["statistic"]
    anchors = conditional_mc_anchors(
        configuration,
        n_values,
        r_values,
        s_values,
        a_values,
        pvalues,
        anchor_replicates=anchor_replicates,
        anchor_samples=anchor_samples,
        rng=rng,
    )

    common: dict[str, object] = {
        "configuration": configuration.name,
        "k": configuration.k,
        "average_n": configuration.average_n,
        "total_n": configuration.k * configuration.average_n,
        "margin_pattern": configuration.margin_pattern,
        "z_pattern": configuration.z_pattern,
        "replicates": replicates,
        "mean_informative_strata": float(np.mean(aggregate["informative"])),
        "mean_lyapunov_ratio": float(np.mean(aggregate["lyapunov"])),
        "mean_max_variance_share": float(
            np.mean(aggregate["max_variance_share"])
        ),
        "zero_variance_fraction": float(np.mean(aggregate["variance"] <= 0)),
        "method_seconds": method_seconds,
        "method_seconds_per_table": method_seconds / replicates,
        "conditional_mc_seconds_per_table": anchors[
            "conditional_mc_seconds_per_table"
        ],
        "runtime_speedup_vs_conditional_mc": (
            anchors["conditional_mc_seconds_per_table"]
            / (method_seconds / replicates)
        ),
        "conditional_mc_anchor_count": anchors["conditional_mc_anchor_count"],
        "conditional_mc_samples": anchor_samples,
        "normal_anchor_p_mae": anchors["normal_anchor_p_mae"],
        "edgeworth_anchor_p_mae": anchors["edgeworth_anchor_p_mae"],
        "chi2_nominal_anchor_p_mae": anchors["chi2_nominal_anchor_p_mae"],
        "chi2_informative_anchor_p_mae": anchors[
            "chi2_informative_anchor_p_mae"
        ],
    }

    rows: list[dict[str, object]] = []
    positive_variance = aggregate["variance"] > 0
    sqrt_variance = np.sqrt(np.maximum(aggregate["variance"], 0))
    for alpha in ALPHAS:
        z_score = norm.ppf(1.0 - alpha)
        cf_threshold = aggregate["mean"] + sqrt_variance * (
            z_score
            + aggregate["skewness"] * (z_score**2 - 1.0) / 6.0
        )
        cf_reject = positive_variance & (
            aggregate["statistic"] >= cf_threshold
        )
        conditional_anchor_fpr = float(
            np.mean(anchors["conditional_mc_pvalues"] <= alpha)
        )
        fprs = {
            "normal": float(np.mean(pvalues["normal"] <= alpha)),
            "edgeworth": float(np.mean(pvalues["edgeworth"] <= alpha)),
            "cornish_fisher": float(np.mean(cf_reject)),
            "chi2_nominal": float(
                np.mean(pvalues["chi2_nominal"] <= alpha)
            ),
            "chi2_informative": float(
                np.mean(pvalues["chi2_informative"] <= alpha)
            ),
            "conditional_mc": conditional_anchor_fpr,
        }
        row = dict(common)
        row.update({"alpha": alpha})
        for method, fpr in fprs.items():
            row[f"{method}_fpr"] = fpr
            row[f"{method}_size_distortion"] = abs(fpr - alpha)
        rows.append(row)
    return rows


def write_summary(
    results: pd.DataFrame,
    output_path: Path,
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Sparse CMI Unconditional Calibration Summary",
        "",
        (
            f"Evaluated {results['configuration'].nunique()} data-generating "
            f"configurations with {args.replicates:,} independent null datasets "
            "per configuration. Every replicate regenerated the observed "
            "stratum margins."
        ),
        "",
        "## Mean absolute size distortion",
        "",
        "| Alpha | Normal | Edgeworth | Cornish-Fisher | Chi2 nominal | Chi2 informative | Conditional MC anchors |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for alpha in ALPHAS:
        subset = results[np.isclose(results["alpha"], alpha)]
        values = [
            subset[f"{method}_size_distortion"].mean()
            for method in METHODS
        ]
        lines.append(
            f"| {alpha:g} | "
            + " | ".join(f"{value:.5f}" for value in values)
            + " |"
        )

    alpha_05 = results[np.isclose(results["alpha"], 0.05)]
    lines.extend(
        [
            "",
            "## Conditional Monte Carlo p-value anchors",
            "",
            "Mean absolute p-value difference on held-out observed tables:",
            "",
            "| Method | Mean MAE | Median MAE |",
            "|---|---:|---:|",
        ]
    )
    for method in (
        "normal",
        "edgeworth",
        "chi2_nominal",
        "chi2_informative",
    ):
        values = alpha_05[f"{method}_anchor_p_mae"]
        lines.append(
            f"| {method} | {values.mean():.5f} | {values.median():.5f} |"
        )

    lines.extend(
        [
            "",
            "## Runtime",
            "",
            (
                f"Median per-table speedup over a {args.anchor_samples:,}-draw "
                "conditional table Monte Carlo test: "
                f"{alpha_05['runtime_speedup_vs_conditional_mc'].median():.1f}x."
            ),
            "",
            "## Guardrails",
            "",
            (
                "- Conditional Monte Carlo FPR uses only the configured anchor "
                "replicates and is therefore noisier than the approximation and "
                "chi-square FPR estimates."
            ),
            (
                "- Approximation runtime is vectorized batch throughput with a "
                "cache shared across repeated margin patterns. Use the fixed-"
                "margin runner's literal permutation benchmark for the stronger "
                "one-table runtime comparison."
            ),
            (
                "- This validates repeated-sampling calibration under i.i.d. "
                "binary CMI nulls. It does not validate transfer entropy or "
                "temporally dependent observations."
            ),
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.replicates <= 0 or args.anchor_replicates <= 0:
        raise ValueError("replicate counts must be positive")
    if args.anchor_samples <= 0:
        raise ValueError("--anchor-samples must be positive")

    all_configurations = configurations(args.profile)
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = (
            Path(__file__).resolve().parents[1]
            / "results"
            / f"unconditional_{args.profile}_{timestamp}"
        )
    else:
        output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    children = np.random.SeedSequence(args.seed).spawn(len(all_configurations))
    rows: list[dict[str, object]] = []
    checkpoint = output_dir / "unconditional_results.partial.csv"
    started = time.perf_counter()
    for index, (configuration, seed) in enumerate(
        zip(all_configurations, children, strict=True),
        start=1,
    ):
        rows.extend(
            evaluate_configuration(
                configuration,
                replicates=args.replicates,
                anchor_replicates=args.anchor_replicates,
                anchor_samples=args.anchor_samples,
                rng=np.random.default_rng(seed),
            )
        )
        print(
            f"[{index:>3}/{len(all_configurations)}] {configuration.name}",
            flush=True,
        )
        if index % args.checkpoint_every == 0:
            pd.DataFrame(rows).to_csv(checkpoint, index=False)

    elapsed = time.perf_counter() - started
    results = pd.DataFrame(rows)
    results.to_csv(output_dir / "unconditional_results.csv", index=False)
    if checkpoint.exists():
        checkpoint.unlink()
    write_summary(results, output_dir / "summary.md", args)
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": sys.argv,
        "profile": args.profile,
        "seed": args.seed,
        "replicates": args.replicates,
        "anchor_replicates": args.anchor_replicates,
        "anchor_samples": args.anchor_samples,
        "configuration_count": len(all_configurations),
        "elapsed_seconds": elapsed,
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
