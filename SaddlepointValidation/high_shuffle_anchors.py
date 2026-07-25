from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

try:
    from .jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from .run_validation import configure_output
    from .saddlepoint_cgf import CondCGF, drop_empty_margins, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from run_validation import configure_output
    from saddlepoint_cgf import CondCGF, drop_empty_margins, g_statistic


def choose_anchors(results: pd.DataFrame, count: int) -> pd.DataFrame:
    candidates = results.copy()
    candidates = candidates.replace([np.inf, -np.inf], np.nan)
    candidates = candidates.dropna(subset=["table_json", "saddle_p", "chi2_nominal_p"])
    candidates["chi2_saddle_gap"] = np.abs(candidates["chi2_nominal_p"] - candidates["saddle_p"])
    candidates = candidates.sort_values("chi2_saddle_gap", ascending=False)
    return candidates.drop_duplicates(subset=["name"]).head(count)


def wilson_interval_from_pvalue(pvalue: float, shuffles: int) -> tuple[float, float, int]:
    k = int(round(float(np.clip(pvalue, 0.0, 1.0)) * shuffles))
    interval = stats.binomtest(k, shuffles).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    return float(interval.low), float(interval.high), k


def evaluate_anchor(
    row: pd.Series,
    shuffles: int,
    exact_table_limit: int,
    jar_path: str,
) -> dict[str, object]:
    table = np.asarray(json.loads(row["table_json"]), dtype=int)
    nonempty = drop_empty_margins(table)
    g_value = g_statistic(table)
    cgf = CondCGF.from_table(table, exact_table_limit=exact_table_limit)
    saddle = cgf.pvalue(g_value, method="auto")

    nominal_df = int((row["r"] - 1) * (row["c"] - 1))
    dynamic_df = max((nonempty.shape[0] - 1) * (nonempty.shape[1] - 1), 0)
    chi2_nominal_p = float(stats.chi2.sf(g_value, df=nominal_df))
    chi2_dynamic_p = 1.0 if dynamic_df <= 0 else float(stats.chi2.sf(g_value, df=dynamic_df))

    jidt = jidt_permutation_pvalue(
        table=table,
        r_nominal=int(row["r"]),
        c_nominal=int(row["c"]),
        shuffles=shuffles,
        jar_path=jar_path,
    )
    ci_low, ci_high, exceedance_count = wilson_interval_from_pvalue(jidt.pvalue, shuffles)
    return {
        "name": row["name"],
        "source_replicate": int(row["replicate"]),
        "r": int(row["r"]),
        "c": int(row["c"]),
        "n": int(row["n"]),
        "skewness": row["skewness"],
        "table_json": row["table_json"],
        "nonempty_table_json": json.dumps(nonempty.astype(int).tolist(), separators=(",", ":")),
        "g_statistic": g_value,
        "saddle_p": saddle.pvalue,
        "saddle_route": saddle.route,
        "support_count": saddle.support_count,
        "support_count_status": saddle.support_count_status,
        "chi2_nominal_p": chi2_nominal_p,
        "chi2_nominal_df": nominal_df,
        "chi2_dynamic_p": chi2_dynamic_p,
        "chi2_dynamic_df": dynamic_df,
        "jidt_p": jidt.pvalue,
        "jidt_shuffles": shuffles,
        "jidt_exceedance_count_approx": exceedance_count,
        "jidt_ci_low_95": ci_low,
        "jidt_ci_high_95": ci_high,
        "jidt_time_s": jidt.elapsed_s,
        "jidt_g_statistic": jidt.g_statistic,
        "jidt_g_abs_diff": abs(g_value - jidt.g_statistic),
        "saddle_inside_jidt_ci": bool(ci_low <= saddle.pvalue <= ci_high),
        "chi2_nominal_inside_jidt_ci": bool(ci_low <= chi2_nominal_p <= ci_high),
        "chi2_dynamic_inside_jidt_ci": bool(ci_low <= chi2_dynamic_p <= ci_high),
    }


def write_summary(output_dir: Path, anchors: pd.DataFrame, shuffles: int) -> None:
    lines = [
        "# High-Shuffle Anchor Summary",
        "",
        f"JIDT shuffles per anchor: `{shuffles}`.",
        "",
        "| name | saddle_p | chi2_nominal_p | chi2_dynamic_p | jidt_p | jidt_95_ci | saddle_in_ci | nominal_chi2_in_ci | dynamic_chi2_in_ci |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for _, row in anchors.iterrows():
        ci = f"[{row['jidt_ci_low_95']:.4g}, {row['jidt_ci_high_95']:.4g}]"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["name"]),
                    f"{row['saddle_p']:.4g}",
                    f"{row['chi2_nominal_p']:.4g}",
                    f"{row['chi2_dynamic_p']:.4g}",
                    f"{row['jidt_p']:.4g}",
                    ci,
                    str(bool(row["saddle_inside_jidt_ci"])),
                    str(bool(row["chi2_nominal_inside_jidt_ci"])),
                    str(bool(row["chi2_dynamic_inside_jidt_ci"])),
                ]
            )
            + " |"
        )
    (output_dir / "high_shuffle_anchor_summary.md").write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run high-shuffle JIDT anchors from a validation CSV.")
    parser.add_argument("--input-results", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--anchors", type=int, default=5)
    parser.add_argument("--shuffles", type=int, default=100_000)
    parser.add_argument("--exact-table-limit", type=int, default=1000)
    parser.add_argument("--jar-path", default=DEFAULT_JIDT_JAR)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = configure_output(args.output_dir)
    results = pd.read_csv(args.input_results)
    selected = choose_anchors(results, count=args.anchors)

    rows = []
    for index, row in selected.iterrows():
        print(f"[{len(rows) + 1}/{len(selected)}] {row['name']} replicate={row['replicate']}", flush=True)
        rows.append(
            evaluate_anchor(
                row=row,
                shuffles=args.shuffles,
                exact_table_limit=args.exact_table_limit,
                jar_path=args.jar_path,
            )
        )

    anchors = pd.DataFrame(rows)
    anchors.to_csv(output_dir / "high_shuffle_anchors.csv", index=False)
    write_summary(output_dir, anchors, shuffles=args.shuffles)
    print(anchors[["name", "saddle_p", "chi2_nominal_p", "chi2_dynamic_p", "jidt_p"]].to_string(index=False))
    print(f"Wrote outputs to {output_dir}", flush=True)


if __name__ == "__main__":
    main()
