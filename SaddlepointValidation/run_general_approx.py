from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

try:
    from .general_fixed_margin import fixed_margin_gamma_approx
    from .jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from .saddlepoint_cgf import drop_empty_margins, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from general_fixed_margin import fixed_margin_gamma_approx
    from jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from saddlepoint_cgf import drop_empty_margins, g_statistic


def marginal(size: int, skewness: str) -> np.ndarray:
    if skewness == "balanced":
        return np.full(size, 1.0 / size)
    if skewness == "mild":
        dominant = 0.70
    elif skewness == "strong":
        dominant = 0.90
    else:
        raise ValueError(f"unknown skewness: {skewness}")
    values = np.full(size, (1.0 - dominant) / (size - 1))
    values[0] = dominant
    return values


def sample_table(
    r: int,
    c: int,
    n: int,
    skewness: str,
    rng: np.random.Generator,
) -> np.ndarray:
    probs = np.outer(marginal(r, skewness), marginal(c, skewness)).ravel()
    return rng.multinomial(n, probs).reshape(r, c)


def evaluate_case(args: argparse.Namespace) -> dict[str, object]:
    rng = np.random.default_rng(args.seed)
    table = sample_table(args.r, args.c, args.n, args.skewness, rng)
    nonempty = drop_empty_margins(table)
    observed_r, observed_c = nonempty.shape
    dynamic_df = max((observed_r - 1) * (observed_c - 1), 0)
    g_value = g_statistic(table)
    gamma = fixed_margin_gamma_approx(
        table=table,
        samples=args.samples,
        seed=args.seed + 1,
        batch_size=args.batch_size,
    )
    nominal_df = (args.r - 1) * (args.c - 1)
    row = {
        "name": args.name,
        "r": args.r,
        "c": args.c,
        "N": args.n,
        "skewness": args.skewness,
        "observed_r": observed_r,
        "observed_c": observed_c,
        "dynamic_df": dynamic_df,
        "g_statistic": g_value,
        "gamma_fixed_margin_p": gamma.gamma_p,
        "empirical_fixed_margin_p": gamma.empirical_p,
        "gamma_mu": gamma.mu,
        "gamma_variance": gamma.variance,
        "gamma_shape": gamma.gamma_shape,
        "gamma_scale": gamma.gamma_scale,
        "gamma_samples": gamma.samples,
        "gamma_time_s": gamma.elapsed_s,
        "gamma_error": gamma.error,
        "chi2_nominal_p": float(stats.chi2.sf(g_value, df=nominal_df)),
        "chi2_dynamic_p": 1.0 if dynamic_df <= 0 else float(stats.chi2.sf(g_value, df=dynamic_df)),
        "jidt_p": np.nan,
        "jidt_time_s": np.nan,
        "jidt_g_abs_diff": np.nan,
        "jidt_error": "",
    }
    if args.jidt_shuffles > 0:
        try:
            jidt = jidt_permutation_pvalue(
                table=table,
                r_nominal=args.r,
                c_nominal=args.c,
                shuffles=args.jidt_shuffles,
                jar_path=args.jar_path,
            )
            row["jidt_p"] = jidt.pvalue
            row["jidt_time_s"] = jidt.elapsed_s
            row["jidt_g_abs_diff"] = abs(jidt.g_statistic - g_value)
        except Exception as exc:
            row["jidt_error"] = repr(exc)
    return row


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="General fixed-margin table-sampling gamma approximation benchmark."
    )
    parser.add_argument("--name", default="general_case")
    parser.add_argument("--r", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--skewness", choices=["balanced", "mild", "strong"], required=True)
    parser.add_argument("--samples", type=int, default=10_000)
    parser.add_argument("--batch-size", type=int, default=10_000)
    parser.add_argument("--jidt-shuffles", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260706)
    parser.add_argument("--jar-path", default=DEFAULT_JIDT_JAR)
    parser.add_argument("--output", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    row = evaluate_case(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(output, index=False)
    print(pd.DataFrame([row]).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
