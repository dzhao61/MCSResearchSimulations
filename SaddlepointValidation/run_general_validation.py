from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
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


SKEWNESS_LEVELS = ("balanced", "mild", "strong")
ROBUST_SKEWNESS_LEVELS = (
    "balanced",
    "slight",
    "mild",
    "strong",
    "extreme",
    "zipf_mild",
    "zipf_strong",
)
ALPHAS = (0.10, 0.05, 0.01)


@dataclass(frozen=True)
class Config:
    name: str
    r: int
    c: int
    n: int
    skewness: str
    p: tuple[float, ...]
    q: tuple[float, ...]


def marginal(size: int, label: str) -> np.ndarray:
    if label == "balanced":
        return np.full(size, 1.0 / size)
    if label == "slight":
        dominant = 0.50
    elif label == "mild":
        dominant = 0.70
    elif label == "strong":
        dominant = 0.90
    elif label == "extreme":
        dominant = 0.98
    elif label == "zipf_mild":
        ranks = np.arange(1, size + 1, dtype=np.float64)
        values = 1.0 / np.power(ranks, 1.1)
        return values / values.sum()
    elif label == "zipf_strong":
        ranks = np.arange(1, size + 1, dtype=np.float64)
        values = 1.0 / np.power(ranks, 2.0)
        return values / values.sum()
    else:
        raise ValueError(f"unknown skewness: {label}")

    values = np.full(size, (1.0 - dominant) / (size - 1))
    values[0] = dominant
    return values


def make_configs(profile: str) -> list[Config]:
    if profile == "smoke":
        specs = [
            (8, 3, 50, "strong"),
            (20, 3, 10_000, "strong"),
            (50, 10, 100_000, "mild"),
            (80, 80, 100_000, "balanced"),
        ]
    elif profile == "targeted":
        specs = []
        for skewness in SKEWNESS_LEVELS:
            specs.extend(
                [
                    (8, 3, 50, skewness),
                    (20, 3, 10_000, skewness),
                    (50, 10, 100_000, skewness),
                    (80, 80, 100_000, skewness),
                ]
            )
    elif profile == "large":
        specs = [
            (20, 3, 2_000_000, "strong"),
            (50, 10, 2_000_000, "mild"),
            (80, 80, 1_000_000, "balanced"),
        ]
    elif profile == "empirical_robust":
        specs = []
        for skewness in SKEWNESS_LEVELS:
            for n in (50, 1_000, 10_000, 100_000):
                specs.extend(
                    [
                        (2, 2, n, skewness),
                        (8, 3, n, skewness),
                        (20, 3, n, skewness),
                        (50, 10, n, skewness),
                        (80, 20, n, skewness),
                        (80, 80, n, skewness),
                    ]
                )
    elif profile == "empirical_large":
        specs = []
        for skewness in SKEWNESS_LEVELS:
            specs.extend(
                [
                    (20, 3, 1_000_000, skewness),
                    (50, 10, 1_000_000, skewness),
                    (80, 80, 1_000_000, skewness),
                ]
            )
    elif profile == "empirical_stress":
        specs = []
        for skewness in ROBUST_SKEWNESS_LEVELS:
            for n in (1_000, 10_000, 100_000, 1_000_000):
                specs.extend(
                    [
                        (20, 20, n, skewness),
                        (50, 20, n, skewness),
                        (80, 80, n, skewness),
                        (100, 50, n, skewness),
                        (100, 100, n, skewness),
                    ]
                )
    elif profile == "empirical_mega_anchors":
        specs = []
        for skewness in ("balanced", "mild", "strong", "extreme", "zipf_strong"):
            specs.extend(
                [
                    (50, 20, 2_000_000, skewness),
                    (100, 50, 2_000_000, skewness),
                    (100, 100, 2_000_000, skewness),
                ]
            )
    elif profile == "empirical_calibration":
        specs = [
            (20, 20, 1_000, "balanced"),
            (20, 20, 1_000, "strong"),
            (20, 20, 1_000, "zipf_strong"),
            (50, 20, 10_000, "balanced"),
            (50, 20, 10_000, "strong"),
            (50, 20, 10_000, "extreme"),
            (80, 80, 10_000, "zipf_mild"),
            (80, 80, 10_000, "zipf_strong"),
            (100, 50, 100_000, "strong"),
            (100, 50, 100_000, "extreme"),
            (50, 20, 10_000, "balanced", "strong"),
            (50, 20, 10_000, "strong", "zipf_strong"),
        ]
    elif profile == "empirical_balanced_controls":
        specs = [
            (5, 5, 1_000, "balanced"),
            (10, 10, 10_000, "balanced"),
            (20, 20, 10_000, "balanced"),
            (50, 20, 50_000, "balanced"),
            (50, 50, 250_000, "balanced"),
            (100, 50, 500_000, "balanced"),
        ]
    else:
        raise ValueError(
            "profile must be smoke, targeted, large, empirical_robust, empirical_large, "
            "empirical_stress, empirical_mega_anchors, empirical_calibration, "
            "or empirical_balanced_controls"
        )

    configs: list[Config] = []
    for spec in specs:
        if len(spec) == 4:
            r, c, n, skewness = spec
            p_label = skewness
            q_label = skewness
        elif len(spec) == 5:
            r, c, n, p_label, q_label = spec
            skewness = f"x_{p_label}_y_{q_label}"
        else:
            raise ValueError(f"invalid config spec: {spec!r}")
        p = marginal(r, p_label)
        q = marginal(c, q_label)
        configs.append(
            Config(
                name=f"{r}x{c}_N{n}_{skewness}",
                r=r,
                c=c,
                n=n,
                skewness=skewness,
                p=tuple(float(x) for x in p),
                q=tuple(float(x) for x in q),
            )
        )
    return configs


def sample_table(config: Config, rng: np.random.Generator) -> np.ndarray:
    probs = np.outer(np.asarray(config.p), np.asarray(config.q)).ravel()
    return rng.multinomial(config.n, probs).reshape(config.r, config.c)


def evaluate_table(
    config: Config,
    table: np.ndarray,
    replicate: int,
    samples: int,
    batch_size: int,
    seed: int,
    jidt_shuffles: int,
    jar_path: str,
) -> dict[str, object]:
    nonempty = drop_empty_margins(table)
    observed_r, observed_c = nonempty.shape
    dynamic_df = max((observed_r - 1) * (observed_c - 1), 0)
    g_value = g_statistic(table)
    mi_nats = g_value / (2.0 * int(table.sum())) if int(table.sum()) > 0 else 0.0
    mi_bits = mi_nats / np.log(2.0)
    jidt_bits_scaled_statistic = g_value / np.log(2.0)
    gamma = fixed_margin_gamma_approx(
        table=table,
        samples=samples,
        seed=seed,
        batch_size=batch_size,
    )
    nominal_df = (config.r - 1) * (config.c - 1)
    row: dict[str, object] = {
        **asdict(config),
        "replicate": replicate,
        "observed_r": observed_r,
        "observed_c": observed_c,
        "dynamic_df": dynamic_df,
        "table_json": json.dumps(table.astype(int).tolist(), separators=(",", ":")),
        "row_totals_json": json.dumps(table.sum(axis=1).astype(int).tolist(), separators=(",", ":")),
        "col_totals_json": json.dumps(table.sum(axis=0).astype(int).tolist(), separators=(",", ":")),
        "g_statistic": g_value,
        "mi_nats_observed": float(mi_nats),
        "mi_bits_observed": float(mi_bits),
        "gamma_fixed_margin_p": gamma.gamma_p,
        "empirical_fixed_margin_p": gamma.empirical_p,
        "gamma_mu": gamma.mu,
        "gamma_variance": gamma.variance,
        "gamma_shape": gamma.gamma_shape,
        "gamma_scale": gamma.gamma_scale,
        "gamma_samples": gamma.samples,
        "gamma_time_s": gamma.elapsed_s,
        "empirical_table_time_s": gamma.elapsed_s,
        "gamma_error": gamma.error,
        "chi2_nominal_p": float(stats.chi2.sf(g_value, df=nominal_df)),
        "chi2_dynamic_p": 1.0 if dynamic_df <= 0 else float(stats.chi2.sf(g_value, df=dynamic_df)),
        "jidt_analytic_bits_nominal_p": float(stats.chi2.sf(jidt_bits_scaled_statistic, df=nominal_df)),
        "jidt_analytic_bits_nominal_statistic": float(jidt_bits_scaled_statistic),
        "jidt_p": np.nan,
        "jidt_time_s": np.nan,
        "jidt_g_abs_diff": np.nan,
        "jidt_error": "",
    }
    if jidt_shuffles > 0:
        try:
            jidt = jidt_permutation_pvalue(
                table=table,
                r_nominal=config.r,
                c_nominal=config.c,
                shuffles=jidt_shuffles,
                jar_path=jar_path,
            )
            row["jidt_p"] = jidt.pvalue
            row["jidt_time_s"] = jidt.elapsed_s
            row["jidt_g_abs_diff"] = abs(jidt.g_statistic - g_value)
        except Exception as exc:
            row["jidt_error"] = repr(exc)
    return row


def summarize(results: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    jidt_analytic_col = (
        "jidt_analytic_bits_nominal_p"
        if "jidt_analytic_bits_nominal_p" in results
        else "jidt_analytic_nominal_p"
    )
    config_cols = ["name", "r", "c", "n", "skewness"]
    rows = []
    for keys, group in results.groupby(config_cols, dropna=False):
        row = dict(zip(config_cols, keys))
        row["replicates"] = int(len(group))
        row["gamma_error_count"] = int(group["gamma_error"].astype(str).ne("").sum())
        row["jidt_error_count"] = int(group["jidt_error"].astype(str).ne("").sum())
        row["median_gamma_time_s"] = float(group["gamma_time_s"].median())
        row["median_empirical_table_time_s"] = float(group["empirical_table_time_s"].median())
        row["median_jidt_time_s"] = (
            float(group["jidt_time_s"].dropna().median())
            if group["jidt_time_s"].notna().any()
            else np.nan
        )
        row["median_empirical_speedup_vs_jidt"] = (
            float((group["jidt_time_s"] / group["empirical_table_time_s"]).dropna().median())
            if group["jidt_time_s"].notna().any()
            else np.nan
        )
        row["median_gamma_speedup_vs_jidt"] = (
            float((group["jidt_time_s"] / group["gamma_time_s"]).dropna().median())
            if group["jidt_time_s"].notna().any()
            else np.nan
        )
        row["median_abs_gamma_vs_empirical"] = float(
            np.median(np.abs(group["gamma_fixed_margin_p"] - group["empirical_fixed_margin_p"]))
        )
        row["median_abs_chi2_dynamic_vs_empirical"] = float(
            np.median(np.abs(group["chi2_dynamic_p"] - group["empirical_fixed_margin_p"]))
        )
        jidtd = group.dropna(subset=["jidt_p"])
        if len(jidtd):
            row["median_abs_gamma_vs_jidt"] = float(
                np.median(np.abs(jidtd["gamma_fixed_margin_p"] - jidtd["jidt_p"]))
            )
            row["median_abs_empirical_vs_jidt"] = float(
                np.median(np.abs(jidtd["empirical_fixed_margin_p"] - jidtd["jidt_p"]))
            )
            row["median_abs_chi2_nominal_vs_jidt"] = float(
                np.median(np.abs(jidtd["chi2_nominal_p"] - jidtd["jidt_p"]))
            )
            row["median_abs_chi2_dynamic_vs_jidt"] = float(
                np.median(np.abs(jidtd["chi2_dynamic_p"] - jidtd["jidt_p"]))
            )
            row["median_abs_jidt_analytic_nominal_vs_jidt"] = float(
                np.median(np.abs(jidtd[jidt_analytic_col] - jidtd["jidt_p"]))
            )
            row["empirical_closer_than_chi2_nominal_fraction"] = float(
                np.mean(
                    np.abs(jidtd["empirical_fixed_margin_p"] - jidtd["jidt_p"])
                    <= np.abs(jidtd["chi2_nominal_p"] - jidtd["jidt_p"])
                )
            )
            row["empirical_closer_than_chi2_dynamic_fraction"] = float(
                np.mean(
                    np.abs(jidtd["empirical_fixed_margin_p"] - jidtd["jidt_p"])
                    <= np.abs(jidtd["chi2_dynamic_p"] - jidtd["jidt_p"])
                )
            )
            row["gamma_closer_than_chi2_dynamic_fraction"] = float(
                np.mean(
                    np.abs(jidtd["gamma_fixed_margin_p"] - jidtd["jidt_p"])
                    <= np.abs(jidtd["chi2_dynamic_p"] - jidtd["jidt_p"])
                )
            )
            row["empirical_closer_than_jidt_analytic_nominal_fraction"] = float(
                np.mean(
                    np.abs(jidtd["empirical_fixed_margin_p"] - jidtd["jidt_p"])
                    <= np.abs(jidtd[jidt_analytic_col] - jidtd["jidt_p"])
                )
            )
        else:
            row["median_abs_gamma_vs_jidt"] = np.nan
            row["median_abs_empirical_vs_jidt"] = np.nan
            row["median_abs_chi2_nominal_vs_jidt"] = np.nan
            row["median_abs_chi2_dynamic_vs_jidt"] = np.nan
            row["median_abs_jidt_analytic_nominal_vs_jidt"] = np.nan
            row["empirical_closer_than_chi2_nominal_fraction"] = np.nan
            row["empirical_closer_than_chi2_dynamic_fraction"] = np.nan
            row["gamma_closer_than_chi2_dynamic_fraction"] = np.nan
            row["empirical_closer_than_jidt_analytic_nominal_fraction"] = np.nan

        for alpha in ALPHAS:
            suffix = f"{int(round(alpha * 100)):02d}"
            row[f"fpr_empirical_{suffix}"] = float(np.mean(group["empirical_fixed_margin_p"] <= alpha))
            row[f"fpr_gamma_{suffix}"] = float(np.mean(group["gamma_fixed_margin_p"] <= alpha))
            row[f"fpr_chi2_nominal_{suffix}"] = float(np.mean(group["chi2_nominal_p"] <= alpha))
            row[f"fpr_chi2_dynamic_{suffix}"] = float(np.mean(group["chi2_dynamic_p"] <= alpha))
            row[f"fpr_jidt_analytic_nominal_{suffix}"] = float(
                np.mean(group[jidt_analytic_col] <= alpha)
            )
            row[f"fpr_jidt_{suffix}"] = (
                float(np.mean(group["jidt_p"].dropna() <= alpha))
                if group["jidt_p"].notna().any()
                else np.nan
            )
        rows.append(row)
    summary = pd.DataFrame(rows)

    overall = pd.DataFrame(
        [
            {
                "configs": int(len(summary)),
                "rows": int(len(results)),
                "median_gamma_time_s": float(results["gamma_time_s"].median()),
                "median_empirical_table_time_s": float(results["empirical_table_time_s"].median()),
                "median_jidt_time_s": (
                    float(results["jidt_time_s"].dropna().median())
                    if results["jidt_time_s"].notna().any()
                    else np.nan
                ),
                "median_empirical_speedup_vs_jidt": (
                    float((results["jidt_time_s"] / results["empirical_table_time_s"]).dropna().median())
                    if results["jidt_time_s"].notna().any()
                    else np.nan
                ),
                "median_gamma_speedup_vs_jidt": (
                    float((results["jidt_time_s"] / results["gamma_time_s"]).dropna().median())
                    if results["jidt_time_s"].notna().any()
                    else np.nan
                ),
                "median_abs_gamma_vs_empirical": float(
                    np.median(np.abs(results["gamma_fixed_margin_p"] - results["empirical_fixed_margin_p"]))
                ),
                "median_abs_chi2_dynamic_vs_empirical": float(
                    np.median(np.abs(results["chi2_dynamic_p"] - results["empirical_fixed_margin_p"]))
                ),
                "median_abs_gamma_vs_jidt": (
                    float(
                        np.median(
                            np.abs(
                                results.dropna(subset=["jidt_p"])["gamma_fixed_margin_p"]
                                - results.dropna(subset=["jidt_p"])["jidt_p"]
                            )
                        )
                    )
                    if results["jidt_p"].notna().any()
                    else np.nan
                ),
                "median_abs_chi2_dynamic_vs_jidt": (
                    float(
                        np.median(
                            np.abs(
                                results.dropna(subset=["jidt_p"])["chi2_dynamic_p"]
                                - results.dropna(subset=["jidt_p"])["jidt_p"]
                            )
                        )
                    )
                    if results["jidt_p"].notna().any()
                    else np.nan
                ),
                "median_abs_jidt_analytic_nominal_vs_jidt": (
                    float(
                        np.median(
                            np.abs(
                                results.dropna(subset=["jidt_p"])[jidt_analytic_col]
                                - results.dropna(subset=["jidt_p"])["jidt_p"]
                            )
                        )
                    )
                    if results["jidt_p"].notna().any()
                    else np.nan
                ),
                "median_abs_jidt_analytic_bits_nominal_vs_jidt": (
                    float(
                        np.median(
                            np.abs(
                                results.dropna(subset=["jidt_p"])[jidt_analytic_col]
                                - results.dropna(subset=["jidt_p"])["jidt_p"]
                            )
                        )
                    )
                    if results["jidt_p"].notna().any()
                    else np.nan
                ),
                "median_abs_empirical_vs_jidt": (
                    float(
                        np.median(
                            np.abs(
                                results.dropna(subset=["jidt_p"])["empirical_fixed_margin_p"]
                                - results.dropna(subset=["jidt_p"])["jidt_p"]
                            )
                        )
                    )
                    if results["jidt_p"].notna().any()
                    else np.nan
                ),
                "median_abs_chi2_nominal_vs_jidt": (
                    float(
                        np.median(
                            np.abs(
                                results.dropna(subset=["jidt_p"])["chi2_nominal_p"]
                                - results.dropna(subset=["jidt_p"])["jidt_p"]
                            )
                        )
                    )
                    if results["jidt_p"].notna().any()
                    else np.nan
                ),
            }
        ]
    )
    return summary, overall


def write_markdown(output_dir: Path, summary: pd.DataFrame, overall: pd.DataFrame) -> None:
    def fmt(x: object) -> str:
        if pd.isna(x):
            return ""
        if isinstance(x, float):
            return f"{x:.4g}"
        return str(x)

    lines = [
        "# General Fixed-Margin Gamma Validation",
        "",
        "This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.",
        "",
        "## Overall",
        "| metric | value |",
        "| --- | ---: |",
    ]
    for col, val in overall.iloc[0].items():
        lines.append(f"| `{col}` | {fmt(val)} |")

    display_cols = [
        "name",
        "replicates",
        "median_gamma_time_s",
        "median_jidt_time_s",
        "median_empirical_speedup_vs_jidt",
        "median_gamma_speedup_vs_jidt",
        "median_abs_empirical_vs_jidt",
        "median_abs_gamma_vs_empirical",
        "median_abs_gamma_vs_jidt",
        "median_abs_chi2_nominal_vs_jidt",
        "median_abs_chi2_dynamic_vs_jidt",
        "median_abs_jidt_analytic_nominal_vs_jidt",
        "empirical_closer_than_chi2_dynamic_fraction",
        "empirical_closer_than_jidt_analytic_nominal_fraction",
        "gamma_closer_than_chi2_dynamic_fraction",
    ]
    lines += [
        "",
        "## Per Configuration",
        "| " + " | ".join(display_cols) + " |",
        "| " + " | ".join(["---"] * len(display_cols)) + " |",
    ]
    for _, row in summary[display_cols].iterrows():
        lines.append("| " + " | ".join(fmt(row[col]) for col in display_cols) + " |")

    lines += [
        "",
        "## Interpretation Notes",
        "- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.",
        "- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.",
        "- `chi2_*` columns use the standard likelihood-ratio statistic `2N * MI_nats`.",
        "- `jidt_analytic_bits_nominal_p` reproduces JIDT's built-in analytic convention: nominal df and `2N * MI_bits`.",
        "- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.",
        "- JIDT p-values have Monte Carlo noise and resolution around `1 / shuffles`; finite-sample p-value conventions may differ by about `1 / shuffles`.",
    ]
    (output_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the general fixed-margin gamma approximation.")
    parser.add_argument(
        "--profile",
        choices=[
            "smoke",
            "targeted",
            "large",
            "empirical_robust",
            "empirical_large",
            "empirical_stress",
            "empirical_mega_anchors",
            "empirical_calibration",
            "empirical_balanced_controls",
        ],
        default="smoke",
    )
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--samples", type=int, default=5_000)
    parser.add_argument("--batch-size", type=int, default=10_000)
    parser.add_argument("--jidt-shuffles", type=int, default=1000)
    parser.add_argument(
        "--jidt-replicates",
        type=int,
        default=None,
        help="Run JIDT for only the first N replicates per configuration. Defaults to all replicates.",
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=1,
        help="Write the partial results CSV every N completed rows.",
    )
    parser.add_argument("--seed", type=int, default=20260706)
    parser.add_argument("--jar-path", default=DEFAULT_JIDT_JAR)
    parser.add_argument("--output-dir", default="SaddlepointValidation/outputs/general_validation")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    configs = make_configs(args.profile)
    jidt_replicates = args.replicates if args.jidt_replicates is None else args.jidt_replicates
    seed_seq = np.random.SeedSequence(args.seed)
    child_seeds = seed_seq.spawn(len(configs) * args.replicates)
    rng = np.random.default_rng(args.seed)
    rows = []
    seed_pos = 0
    for config_index, config in enumerate(configs, start=1):
        print(f"[{config_index}/{len(configs)}] {config.name}", flush=True)
        for rep in range(args.replicates):
            table = sample_table(config, rng)
            eval_seed = int(child_seeds[seed_pos].generate_state(1, dtype=np.uint32)[0])
            seed_pos += 1
            rows.append(
                evaluate_table(
                    config=config,
                    table=table,
                    replicate=rep,
                    samples=args.samples,
                    batch_size=args.batch_size,
                    seed=eval_seed,
                    jidt_shuffles=args.jidt_shuffles if rep < jidt_replicates else 0,
                    jar_path=args.jar_path,
                )
            )
            if args.checkpoint_every > 0 and len(rows) % args.checkpoint_every == 0:
                pd.DataFrame(rows).to_csv(output_dir / "general_validation_results.partial.csv", index=False)

    results = pd.DataFrame(rows)
    results.to_csv(output_dir / "general_validation_results.csv", index=False)
    summary, overall = summarize(results)
    summary.to_csv(output_dir / "general_validation_summary.csv", index=False)
    overall.to_csv(output_dir / "overall_summary.csv", index=False)
    write_markdown(output_dir, summary, overall)
    metadata = {
        "profile": args.profile,
        "replicates": args.replicates,
        "samples": args.samples,
        "batch_size": args.batch_size,
        "jidt_shuffles": args.jidt_shuffles,
        "jidt_replicates": jidt_replicates,
        "seed": args.seed,
        "config_count": len(configs),
        "rows": len(results),
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(overall.to_string(index=False), flush=True)
    print(f"Wrote outputs to {output_dir}", flush=True)


if __name__ == "__main__":
    main()
