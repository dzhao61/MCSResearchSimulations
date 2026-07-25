from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

try:
    from .jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from .saddlepoint_cgf import CondCGF, drop_empty_margins, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from saddlepoint_cgf import CondCGF, drop_empty_margins, g_statistic


ALPHAS = (0.10, 0.05, 0.01)
SKEWNESS_LEVELS = ("balanced", "mild", "strong")
CGF_CACHE_MAXSIZE = 4096


@dataclass(frozen=True)
class Config:
    name: str
    r: int
    c: int
    n: int
    skewness: str
    p: tuple[float, ...]
    q: tuple[float, ...]


def configure_output(output_dir: str | os.PathLike[str]) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("MPLCONFIGDIR", str(path / ".mplcache"))
    os.environ.setdefault("XDG_CACHE_HOME", str(path / ".cache"))
    (path / ".mplcache").mkdir(exist_ok=True)
    (path / ".cache").mkdir(exist_ok=True)
    return path


def marginal(size: int, label: str) -> np.ndarray:
    if label == "balanced":
        return np.full(size, 1.0 / size)
    if label == "mild":
        dominant = 0.70
    elif label == "strong":
        dominant = 0.90
    else:
        raise ValueError(f"unknown skewness: {label}")

    values = np.full(size, (1.0 - dominant) / (size - 1))
    values[0] = dominant
    return values


def make_configs(profile: str) -> list[Config]:
    if profile == "quick":
        shapes = [(2, 2), (3, 3), (6, 3), (8, 3)]
        sample_sizes = [50, 120]
        skews = ["balanced", "strong"]
    elif profile == "focused":
        shapes = [(2, 2), (3, 3), (6, 3), (8, 3)]
        sample_sizes = [50]
        skews = list(SKEWNESS_LEVELS)
    elif profile == "standard":
        shapes = [(2, 2), (3, 2), (3, 3), (4, 3), (6, 3), (8, 3)]
        sample_sizes = [50, 120]
        skews = list(SKEWNESS_LEVELS)
    elif profile == "robust":
        shapes = [(2, 2), (3, 2), (3, 3), (4, 3), (6, 3), (8, 3), (10, 3)]
        sample_sizes = [30, 60, 120, 250]
        skews = list(SKEWNESS_LEVELS)
    else:
        raise ValueError("profile must be quick, focused, standard, or robust")

    configs: list[Config] = []
    for r, c in shapes:
        for n in sample_sizes:
            for skewness in skews:
                p = marginal(r, skewness)
                q = marginal(c, skewness)
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


def alpha_suffix(alpha: float) -> str:
    return f"{int(round(alpha * 100)):02d}"


def canonical_margin_key(table: np.ndarray) -> tuple[tuple[int, ...], tuple[int, ...]]:
    nonempty = drop_empty_margins(table)
    rows = nonempty.sum(axis=1).astype(int)
    cols = nonempty.sum(axis=0).astype(int)
    if cols.size > rows.size:
        rows, cols = cols, rows
    row_key = tuple(sorted((int(x) for x in rows if x > 0), reverse=True))
    col_key = tuple(sorted((int(x) for x in cols if x > 0), reverse=True))
    return row_key, col_key


@lru_cache(maxsize=CGF_CACHE_MAXSIZE)
def cached_cgf(
    row_key: tuple[int, ...],
    col_key: tuple[int, ...],
    exact_table_limit: int,
) -> CondCGF:
    return CondCGF(row_key, col_key, exact_table_limit=exact_table_limit)


def cgf_from_table_cached(table: np.ndarray, exact_table_limit: int) -> CondCGF:
    row_key, col_key = canonical_margin_key(table)
    return cached_cgf(row_key, col_key, exact_table_limit)


def config_checkpoint_path(output_dir: Path, config: Config) -> Path:
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    return checkpoint_dir / f"{config.name}.csv"


def write_config_checkpoint(output_dir: Path, config: Config, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(config_checkpoint_path(output_dir, config), index=False)


def load_config_checkpoint(
    output_dir: Path,
    config: Config,
    expected_replicates: int,
    shuffles: int,
) -> list[dict[str, object]] | None:
    path = config_checkpoint_path(output_dir, config)
    if not path.exists():
        return None
    checkpoint = pd.read_csv(path)
    if len(checkpoint) != expected_replicates:
        return None
    if "shuffles" in checkpoint and checkpoint["shuffles"].notna().any():
        if int(checkpoint["shuffles"].dropna().iloc[0]) != shuffles:
            return None
    return checkpoint.to_dict("records")


def write_combined_checkpoint(output_dir: Path, rows: list[dict[str, object]]) -> None:
    if rows:
        pd.DataFrame(rows).to_csv(
            output_dir / "saddlepoint_validation_results.partial.csv",
            index=False,
        )


def evaluate_table(
    config: Config,
    table: np.ndarray,
    replicate: int,
    shuffles: int,
    run_jidt: bool,
    exact_table_limit: int,
    jar_path: str,
) -> dict[str, object]:
    n = int(table.sum())
    g_value = g_statistic(table)
    nonempty_table = drop_empty_margins(table)
    observed_r, observed_c = nonempty_table.shape
    dynamic_df = max((observed_r - 1) * (observed_c - 1), 0)
    row_totals = table.sum(axis=1).astype(int).tolist()
    col_totals = table.sum(axis=0).astype(int).tolist()
    nonempty_row_totals = nonempty_table.sum(axis=1).astype(int).tolist()
    nonempty_col_totals = nonempty_table.sum(axis=0).astype(int).tolist()

    saddle_start = time.perf_counter()
    try:
        cgf = cgf_from_table_cached(table, exact_table_limit=exact_table_limit)
        saddle = cgf.pvalue(g_value, method="auto")
        saddle_p = saddle.pvalue
        route = saddle.route
        support = saddle.support_count
        support_status = saddle.support_count_status
        saddle_elapsed = time.perf_counter() - saddle_start
        cgf_mean = cgf.K1(0.0)
        cgf_var = cgf.K2(0.0)
        saddlepoint_s_hat = saddle.saddlepoint_s_hat
        saddlepoint_w = saddle.saddlepoint_w
        saddlepoint_u = saddle.saddlepoint_u
        saddlepoint_k = saddle.saddlepoint_k
        saddlepoint_k2 = saddle.saddlepoint_k2
        saddlepoint_iterations = saddle.saddlepoint_iterations
        saddlepoint_converged = saddle.saddlepoint_converged
        saddlepoint_fallback = saddle.saddlepoint_fallback
        saddle_error = ""
    except Exception as exc:
        saddle_p = np.nan
        route = "error"
        support = np.nan
        support_status = "error"
        saddle_elapsed = time.perf_counter() - saddle_start
        cgf_mean = np.nan
        cgf_var = np.nan
        saddlepoint_s_hat = np.nan
        saddlepoint_w = np.nan
        saddlepoint_u = np.nan
        saddlepoint_k = np.nan
        saddlepoint_k2 = np.nan
        saddlepoint_iterations = np.nan
        saddlepoint_converged = np.nan
        saddlepoint_fallback = ""
        saddle_error = repr(exc)

    chi2_start = time.perf_counter()
    chi2_nominal_df = (config.r - 1) * (config.c - 1)
    chi2_nominal_p = float(stats.chi2.sf(g_value, df=chi2_nominal_df))
    chi2_dynamic_p = 1.0 if dynamic_df <= 0 else float(stats.chi2.sf(g_value, df=dynamic_df))
    chi2_elapsed = time.perf_counter() - chi2_start

    result: dict[str, object] = {
        **asdict(config),
        "replicate": replicate,
        "observed_N": n,
        "table_json": json.dumps(table.astype(int).tolist(), separators=(",", ":")),
        "nonempty_table_json": json.dumps(nonempty_table.astype(int).tolist(), separators=(",", ":")),
        "row_totals_json": json.dumps(row_totals, separators=(",", ":")),
        "col_totals_json": json.dumps(col_totals, separators=(",", ":")),
        "nonempty_row_totals_json": json.dumps(nonempty_row_totals, separators=(",", ":")),
        "nonempty_col_totals_json": json.dumps(nonempty_col_totals, separators=(",", ":")),
        "observed_r": observed_r,
        "observed_c": observed_c,
        "dynamic_df": dynamic_df,
        "g_statistic": g_value,
        "saddle_p": saddle_p,
        "saddle_route": route,
        "support_count": support,
        "support_count_status": support_status,
        "saddle_time_s": saddle_elapsed,
        "conditional_mean": cgf_mean,
        "conditional_variance": cgf_var,
        "saddlepoint_s_hat": saddlepoint_s_hat,
        "saddlepoint_w": saddlepoint_w,
        "saddlepoint_u": saddlepoint_u,
        "saddlepoint_k": saddlepoint_k,
        "saddlepoint_k2": saddlepoint_k2,
        "saddlepoint_iterations": saddlepoint_iterations,
        "saddlepoint_converged": saddlepoint_converged,
        "saddlepoint_fallback": saddlepoint_fallback,
        "saddle_error": saddle_error,
        "chi2_nominal_p": chi2_nominal_p,
        "chi2_nominal_df": chi2_nominal_df,
        "chi2_dynamic_p": chi2_dynamic_p,
        "chi2_dynamic_df": dynamic_df,
        "chi2_p": chi2_nominal_p,
        "chi2_df": chi2_nominal_df,
        "chi2_time_s": chi2_elapsed,
        "shuffles": shuffles,
        "jidt_p_floor": 1.0 / (shuffles + 1.0),
        "jidt_p": np.nan,
        "jidt_g_statistic": np.nan,
        "jidt_g_abs_diff": np.nan,
        "jidt_time_s": np.nan,
        "jidt_error": "",
    }

    if run_jidt:
        try:
            jidt = jidt_permutation_pvalue(
                table=table,
                r_nominal=config.r,
                c_nominal=config.c,
                shuffles=shuffles,
                jar_path=jar_path,
            )
            result["jidt_p"] = jidt.pvalue
            result["jidt_g_statistic"] = jidt.g_statistic
            result["jidt_g_abs_diff"] = abs(g_value - jidt.g_statistic)
            result["jidt_time_s"] = jidt.elapsed_s
        except Exception as exc:
            result["jidt_error"] = repr(exc)

    return result


def evaluate_config(
    config_index: int,
    config: Config,
    seed: int,
    replicates: int,
    jidt_replicates: int,
    shuffles: int,
    exact_table_limit: int,
    jar_path: str,
) -> list[dict[str, object]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, object]] = []
    for rep in range(replicates):
        table = sample_table(config, rng)
        row = evaluate_table(
            config=config,
            table=table,
            replicate=rep,
            shuffles=shuffles,
            run_jidt=rep < jidt_replicates,
            exact_table_limit=exact_table_limit,
            jar_path=jar_path,
        )
        row["config_index"] = config_index
        rows.append(row)
    return rows


def summarize(results: pd.DataFrame, shuffles: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    config_cols = ["name", "r", "c", "n", "skewness"]
    rows = []
    for keys, group in results.groupby(config_cols, dropna=False):
        row = dict(zip(config_cols, keys))
        row["replicates"] = int(len(group))
        row["jidt_replicates"] = int(group["jidt_p"].notna().sum())
        row["saddle_error_count"] = int((group["saddle_route"] == "error").sum())
        row["saddle_exact_fraction"] = float((group["saddle_route"] == "exact").mean())
        row["support_censored_fraction"] = float(group["support_count_status"].astype(str).str.startswith(">").mean())
        row["median_support_count"] = float(pd.to_numeric(group["support_count"], errors="coerce").median())
        row["median_saddle_time_s"] = float(group["saddle_time_s"].median())
        row["median_chi2_time_s"] = float(group["chi2_time_s"].median())
        row["median_jidt_time_s"] = float(group["jidt_time_s"].dropna().median()) if group["jidt_p"].notna().any() else np.nan
        row["max_jidt_g_abs_diff"] = float(group["jidt_g_abs_diff"].dropna().max()) if group["jidt_g_abs_diff"].notna().any() else np.nan

        jidtd = group.dropna(subset=["jidt_p", "saddle_p", "chi2_nominal_p", "chi2_dynamic_p"])
        if len(jidtd):
            floor = 1.0 / (shuffles + 1.0)
            row["mae_saddle_vs_jidt"] = float(np.mean(np.abs(jidtd["saddle_p"] - jidtd["jidt_p"])))
            row["mae_chi2_nominal_vs_jidt"] = float(np.mean(np.abs(jidtd["chi2_nominal_p"] - jidtd["jidt_p"])))
            row["mae_chi2_dynamic_vs_jidt"] = float(np.mean(np.abs(jidtd["chi2_dynamic_p"] - jidtd["jidt_p"])))
            row["mae_chi2_vs_jidt"] = row["mae_chi2_nominal_vs_jidt"]
            row["log10_mae_saddle_vs_jidt"] = float(
                np.mean(np.abs(np.log10(jidtd["saddle_p"].clip(lower=floor)) - np.log10(jidtd["jidt_p"].clip(lower=floor))))
            )
            row["log10_mae_chi2_nominal_vs_jidt"] = float(
                np.mean(np.abs(np.log10(jidtd["chi2_nominal_p"].clip(lower=floor)) - np.log10(jidtd["jidt_p"].clip(lower=floor))))
            )
            row["log10_mae_chi2_dynamic_vs_jidt"] = float(
                np.mean(np.abs(np.log10(jidtd["chi2_dynamic_p"].clip(lower=floor)) - np.log10(jidtd["jidt_p"].clip(lower=floor))))
            )
            row["log10_mae_chi2_vs_jidt"] = row["log10_mae_chi2_nominal_vs_jidt"]
            row["saddle_closer_than_chi2_nominal_fraction"] = float(
                np.mean(np.abs(jidtd["saddle_p"] - jidtd["jidt_p"]) <= np.abs(jidtd["chi2_nominal_p"] - jidtd["jidt_p"]))
            )
            row["saddle_closer_than_chi2_dynamic_fraction"] = float(
                np.mean(np.abs(jidtd["saddle_p"] - jidtd["jidt_p"]) <= np.abs(jidtd["chi2_dynamic_p"] - jidtd["jidt_p"]))
            )
            row["saddle_closer_to_jidt_fraction"] = row["saddle_closer_than_chi2_nominal_fraction"]
        else:
            row["mae_saddle_vs_jidt"] = np.nan
            row["mae_chi2_nominal_vs_jidt"] = np.nan
            row["mae_chi2_dynamic_vs_jidt"] = np.nan
            row["mae_chi2_vs_jidt"] = np.nan
            row["log10_mae_saddle_vs_jidt"] = np.nan
            row["log10_mae_chi2_nominal_vs_jidt"] = np.nan
            row["log10_mae_chi2_dynamic_vs_jidt"] = np.nan
            row["log10_mae_chi2_vs_jidt"] = np.nan
            row["saddle_closer_than_chi2_nominal_fraction"] = np.nan
            row["saddle_closer_than_chi2_dynamic_fraction"] = np.nan
            row["saddle_closer_to_jidt_fraction"] = np.nan

        for alpha in ALPHAS:
            suffix = alpha_suffix(alpha)
            row[f"fpr_saddle_{suffix}"] = float(np.mean(group["saddle_p"] <= alpha))
            row[f"fpr_chi2_nominal_{suffix}"] = float(np.mean(group["chi2_nominal_p"] <= alpha))
            row[f"fpr_chi2_dynamic_{suffix}"] = float(np.mean(group["chi2_dynamic_p"] <= alpha))
            row[f"fpr_chi2_{suffix}"] = row[f"fpr_chi2_nominal_{suffix}"]
            row[f"fpr_jidt_{suffix}"] = float(np.mean(group["jidt_p"].dropna() <= alpha)) if group["jidt_p"].notna().any() else np.nan
        rows.append(row)

    summary = pd.DataFrame(rows)

    def nanmean_or_nan(values: pd.Series | np.ndarray) -> float:
        finite = pd.Series(values).dropna()
        return float(finite.mean()) if len(finite) else np.nan

    overall_rows = []
    for alpha in ALPHAS:
        suffix = alpha_suffix(alpha)
        jidt_abs_error = np.abs(summary[f"fpr_jidt_{suffix}"] - alpha)
        jidt_within = np.abs(summary[f"fpr_jidt_{suffix}"] - alpha) <= 0.2 * alpha
        jidt_mask = summary[f"fpr_jidt_{suffix}"].notna()
        if jidt_mask.any():
            jidt_within_value = float(jidt_within[jidt_mask].mean())
        else:
            jidt_within_value = np.nan
        overall_rows.append(
            {
                "alpha": alpha,
                "saddle_mean_abs_calibration_error": float(np.mean(np.abs(summary[f"fpr_saddle_{suffix}"] - alpha))),
                "chi2_nominal_mean_abs_calibration_error": float(np.mean(np.abs(summary[f"fpr_chi2_nominal_{suffix}"] - alpha))),
                "chi2_dynamic_mean_abs_calibration_error": float(np.mean(np.abs(summary[f"fpr_chi2_dynamic_{suffix}"] - alpha))),
                "chi2_mean_abs_calibration_error": float(np.mean(np.abs(summary[f"fpr_chi2_nominal_{suffix}"] - alpha))),
                "jidt_mean_abs_calibration_error": nanmean_or_nan(jidt_abs_error),
                "saddle_within_20pct_fraction": float(np.mean(np.abs(summary[f"fpr_saddle_{suffix}"] - alpha) <= 0.2 * alpha)),
                "chi2_nominal_within_20pct_fraction": float(np.mean(np.abs(summary[f"fpr_chi2_nominal_{suffix}"] - alpha) <= 0.2 * alpha)),
                "chi2_dynamic_within_20pct_fraction": float(np.mean(np.abs(summary[f"fpr_chi2_dynamic_{suffix}"] - alpha) <= 0.2 * alpha)),
                "chi2_within_20pct_fraction": float(np.mean(np.abs(summary[f"fpr_chi2_nominal_{suffix}"] - alpha) <= 0.2 * alpha)),
                "jidt_within_20pct_fraction": jidt_within_value,
            }
        )
    overall = pd.DataFrame(overall_rows)
    return summary, overall


def make_plots(results: pd.DataFrame, summary: pd.DataFrame, output_dir: Path) -> None:
    import matplotlib.pyplot as plt

    jidtd = results.dropna(subset=["jidt_p", "saddle_p", "chi2_nominal_p", "chi2_dynamic_p"])
    if len(jidtd):
        fig, ax = plt.subplots(figsize=(6.4, 6.2))
        ax.scatter(jidtd["jidt_p"], jidtd["saddle_p"], s=24, alpha=0.75, label="Saddlepoint/Exact")
        ax.scatter(jidtd["jidt_p"], jidtd["chi2_nominal_p"], s=24, alpha=0.50, label="Chi-squared nominal")
        ax.scatter(jidtd["jidt_p"], jidtd["chi2_dynamic_p"], s=24, alpha=0.50, label="Chi-squared dynamic")
        ax.plot([0, 1], [0, 1], color="black", linewidth=1, linestyle="--")
        ax.set_xlabel("JIDT permutation p-value")
        ax.set_ylabel("Analytical p-value")
        ax.set_title("P-value agreement against JIDT shuffling")
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "pvalue_scatter_vs_jidt.png", dpi=160)
        plt.close(fig)

    labels = summary["name"].tolist()
    x = np.arange(len(labels))
    width = 0.20
    fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.35), 5.2))
    ax.bar(x - 1.5 * width, summary["fpr_saddle_05"], width, label="Saddlepoint/Exact")
    ax.bar(x - 0.5 * width, summary["fpr_chi2_nominal_05"], width, label="Chi-squared nominal")
    ax.bar(x + 0.5 * width, summary["fpr_chi2_dynamic_05"], width, label="Chi-squared dynamic")
    ax.bar(x + 1.5 * width, summary["fpr_jidt_05"], width, label="JIDT shuffle")
    ax.axhline(0.05, color="black", linestyle="--", linewidth=1)
    ax.set_ylabel("False positive rate at alpha=0.05")
    ax.set_title("Null calibration by configuration")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=65, ha="right", fontsize=8)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "fpr_alpha05_by_config.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    timing = [
        summary["median_saddle_time_s"].median(),
        summary["median_chi2_time_s"].median(),
        summary["median_jidt_time_s"].median(),
    ]
    ax.bar(["Saddlepoint/Exact", "Chi-squared", "JIDT shuffle"], timing)
    ax.set_yscale("log")
    ax.set_ylabel("Median seconds per table (log scale)")
    ax.set_title("Per-table runtime")
    fig.tight_layout()
    fig.savefig(output_dir / "runtime_comparison.png", dpi=160)
    plt.close(fig)


def write_markdown_summary(
    output_dir: Path,
    summary: pd.DataFrame,
    overall: pd.DataFrame,
    profile: str,
    shuffles: int,
    reps: int,
    jidt_reps: int,
) -> None:
    def markdown_table(df: pd.DataFrame) -> str:
        text_df = df.copy()
        for col in text_df.columns:
            if pd.api.types.is_float_dtype(text_df[col]):
                text_df[col] = text_df[col].map(lambda x: "" if pd.isna(x) else f"{x:.4g}")
        headers = list(text_df.columns)
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        for _, row in text_df.iterrows():
            lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
        return "\n".join(lines)

    best = summary.sort_values("saddle_closer_to_jidt_fraction", ascending=False).head(5)
    worst_chi2 = summary.assign(
        chi2_err=(summary["fpr_chi2_05"] - 0.05).abs(),
        saddle_err=(summary["fpr_saddle_05"] - 0.05).abs(),
    ).sort_values("chi2_err", ascending=False).head(5)
    median_saddle_time = summary["median_saddle_time_s"].median()
    median_jidt_time = summary["median_jidt_time_s"].median()
    median_chi2_time = summary["median_chi2_time_s"].median()
    slow_vs_jidt = summary[
        summary["median_jidt_time_s"].notna()
        & (summary["median_saddle_time_s"] > summary["median_jidt_time_s"])
    ].sort_values("median_saddle_time_s", ascending=False)
    slow_note = (
        f"Saddlepoint/exact is slower than this low-shuffle JIDT setting on `{len(slow_vs_jidt)}` "
        f"of `{summary['median_jidt_time_s'].notna().sum()}` configurations with JIDT timings. "
        "The advantage being tested here is deterministic fixed-margin tail resolution and agreement "
        "with high-shuffle anchors, not beating tiny-shuffle JIDT on every dense balanced table."
    )

    lines = [
        "# Saddlepoint MI Validation Summary",
        "",
        f"Profile: `{profile}`. Null replicates per configuration: `{reps}`. JIDT-shuffled replicates per configuration: `{jidt_reps}`. JIDT shuffles per p-value: `{shuffles}`.",
        "",
        "## Overall Calibration",
        markdown_table(overall),
        "",
        "## JIDT Agreement",
        f"Median fraction of tables where saddlepoint/exact was closer to JIDT than nominal chi-squared: `{summary['saddle_closer_than_chi2_nominal_fraction'].median():.3f}`.",
        f"Median fraction of tables where saddlepoint/exact was closer to JIDT than dynamic chi-squared: `{summary['saddle_closer_than_chi2_dynamic_fraction'].median():.3f}`.",
        f"Median absolute p-value error versus JIDT: saddlepoint/exact `{summary['mae_saddle_vs_jidt'].median():.4f}`, nominal chi-squared `{summary['mae_chi2_nominal_vs_jidt'].median():.4f}`, dynamic chi-squared `{summary['mae_chi2_dynamic_vs_jidt'].median():.4f}`.",
        "",
        "## Strongest Saddlepoint Wins Against JIDT",
        markdown_table(best[["name", "saddle_closer_than_chi2_nominal_fraction", "saddle_closer_than_chi2_dynamic_fraction", "mae_saddle_vs_jidt", "mae_chi2_nominal_vs_jidt", "mae_chi2_dynamic_vs_jidt"]]),
        "",
        "## Worst Nominal Chi-Squared Calibration Cases At Alpha 0.05",
        markdown_table(worst_chi2[["name", "fpr_saddle_05", "fpr_chi2_nominal_05", "fpr_chi2_dynamic_05", "fpr_jidt_05", "saddle_err", "chi2_err"]]),
        "",
        "## Runtime",
        f"Median per-table times: saddlepoint/exact `{median_saddle_time:.4g}s`, nominal/dynamic chi-squared `{median_chi2_time:.4g}s`, low-shuffle JIDT `{median_jidt_time:.4g}s`.",
        slow_note,
        markdown_table(slow_vs_jidt[["name", "median_saddle_time_s", "median_jidt_time_s"]].head(5)),
        "",
        "## Notes",
        "The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small. Nominal chi-squared uses configured alphabet size; dynamic chi-squared uses observed nonempty rows and columns.",
        "",
    ]
    (output_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate conditional-CGF saddlepoint MI p-values.")
    parser.add_argument("--output-dir", default="SaddlepointValidation/outputs/standard")
    parser.add_argument("--profile", choices=["quick", "focused", "standard", "robust"], default="standard")
    parser.add_argument("--replicates", type=int, default=20)
    parser.add_argument("--jidt-replicates", type=int, default=10)
    parser.add_argument("--shuffles", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260705)
    parser.add_argument("--exact-table-limit", type=int, default=20_000)
    parser.add_argument("--jar-path", default=DEFAULT_JIDT_JAR)
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes for per-configuration evaluation.",
    )
    parser.add_argument(
        "--parallel-jidt",
        action="store_true",
        help="Allow JIDT permutation calls inside worker processes. By default, JIDT keeps the run serial.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse complete per-configuration checkpoint CSVs in the output directory.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = configure_output(args.output_dir)
    configs = make_configs(args.profile)

    seed_sequence = np.random.SeedSequence(args.seed)
    config_seeds = [
        int(child.generate_state(1, dtype=np.uint32)[0])
        for child in seed_sequence.spawn(len(configs))
    ]

    rows: list[dict[str, object]] = []
    pending: list[tuple[int, Config, int]] = []
    for config_index, (config, config_seed) in enumerate(
        zip(configs, config_seeds, strict=True), start=1
    ):
        if args.resume:
            checkpoint_rows = load_config_checkpoint(
                output_dir=output_dir,
                config=config,
                expected_replicates=args.replicates,
                shuffles=args.shuffles,
            )
            if checkpoint_rows is not None:
                for row in checkpoint_rows:
                    row.setdefault("config_index", config_index)
                rows.extend(checkpoint_rows)
                print(
                    f"[{config_index}/{len(configs)}] {config.name} resumed from checkpoint",
                    flush=True,
                )
                continue
        pending.append((config_index, config, config_seed))

    can_parallelize = args.workers > 1 and (
        args.jidt_replicates == 0 or args.parallel_jidt
    )
    if args.workers > 1 and not can_parallelize:
        print(
            "Parallel workers requested, but JIDT replicates are enabled. "
            "Running serially to avoid multiple unmanaged JVMs; pass --parallel-jidt "
            "if you explicitly want one JVM per worker process.",
            flush=True,
        )

    if can_parallelize:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    evaluate_config,
                    config_index,
                    config,
                    config_seed,
                    args.replicates,
                    args.jidt_replicates,
                    args.shuffles,
                    args.exact_table_limit,
                    args.jar_path,
                ): (config_index, config)
                for config_index, config, config_seed in pending
            }
            for future in as_completed(futures):
                config_index, config = futures[future]
                print(f"[{config_index}/{len(configs)}] {config.name}", flush=True)
                config_rows = future.result()
                write_config_checkpoint(output_dir, config, config_rows)
                rows.extend(config_rows)
                write_combined_checkpoint(output_dir, rows)
    else:
        for config_index, config, config_seed in pending:
            print(f"[{config_index}/{len(configs)}] {config.name}", flush=True)
            config_rows = evaluate_config(
                config_index=config_index,
                config=config,
                seed=config_seed,
                replicates=args.replicates,
                jidt_replicates=args.jidt_replicates,
                shuffles=args.shuffles,
                exact_table_limit=args.exact_table_limit,
                jar_path=args.jar_path,
            )
            write_config_checkpoint(output_dir, config, config_rows)
            rows.extend(config_rows)
            write_combined_checkpoint(output_dir, rows)

    results = pd.DataFrame(rows)
    if "config_index" in results and "replicate" in results:
        results = results.sort_values(["config_index", "replicate"]).reset_index(
            drop=True
        )
    results.to_csv(output_dir / "saddlepoint_validation_results.csv", index=False)
    summary, overall = summarize(results, shuffles=args.shuffles)
    summary.to_csv(output_dir / "saddlepoint_validation_summary.csv", index=False)
    overall.to_csv(output_dir / "overall_summary.csv", index=False)
    make_plots(results, summary, output_dir)
    write_markdown_summary(
        output_dir=output_dir,
        summary=summary,
        overall=overall,
        profile=args.profile,
        shuffles=args.shuffles,
        reps=args.replicates,
        jidt_reps=args.jidt_replicates,
    )
    metadata = {
        "profile": args.profile,
        "replicates": args.replicates,
        "jidt_replicates": args.jidt_replicates,
        "shuffles": args.shuffles,
        "seed": args.seed,
        "exact_table_limit": args.exact_table_limit,
        "workers": args.workers,
        "parallel_jidt": bool(args.parallel_jidt),
        "resume": bool(args.resume),
        "cgf_cache_maxsize": CGF_CACHE_MAXSIZE,
        "cgf_cache_info": cached_cgf.cache_info()._asdict(),
        "config_count": len(configs),
        "result_rows": len(results),
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(overall.to_string(index=False), flush=True)
    print(f"Wrote outputs to {output_dir}", flush=True)


if __name__ == "__main__":
    main()
