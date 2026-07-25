from __future__ import annotations

import argparse
import json
import signal
import time
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from .saddlepoint_cgf import CondCGF, g_statistic
except ImportError:  # pragma: no cover - supports direct script execution
    from jidt_utils import DEFAULT_JIDT_JAR, jidt_permutation_pvalue
    from saddlepoint_cgf import CondCGF, g_statistic


class SaddleTimeout(Exception):
    pass


def _timeout_handler(signum: int, frame: object) -> None:
    raise SaddleTimeout()


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


def sample_table(r: int, c: int, n: int, skewness: str, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    probs = np.outer(marginal(r, skewness), marginal(c, skewness)).ravel()
    return rng.multinomial(n, probs).reshape(r, c)


def run_case(args: argparse.Namespace) -> dict[str, object]:
    table = sample_table(args.r, args.c, args.n, args.skewness, args.seed)
    g_value = g_statistic(table)

    saddle_status = "skipped" if args.skip_saddle else "ok"
    saddle_p = np.nan
    saddle_route = ""
    saddle_time_s = np.nan
    if not args.skip_saddle:
        signal.signal(signal.SIGALRM, _timeout_handler)
        try:
            signal.alarm(args.saddle_timeout_s)
            saddle_start = time.perf_counter()
            cgf = CondCGF.from_table(table, exact_table_limit=args.exact_table_limit)
            saddle = cgf.pvalue(g_value, method="auto")
            saddle_time_s = time.perf_counter() - saddle_start
            saddle_p = saddle.pvalue
            saddle_route = saddle.route
        except SaddleTimeout:
            saddle_status = f"timeout_{args.saddle_timeout_s}s"
        except Exception as exc:
            saddle_status = repr(exc)
        finally:
            signal.alarm(0)

    print(
        f"running JIDT: {args.name}, N={args.n}, shape={args.r}x{args.c}, "
        f"shuffles={args.shuffles}",
        flush=True,
    )
    jidt = jidt_permutation_pvalue(
        table=table,
        r_nominal=args.r,
        c_nominal=args.c,
        shuffles=args.shuffles,
        jar_path=args.jar_path,
    )

    return {
        "name": args.name,
        "r": args.r,
        "c": args.c,
        "N": args.n,
        "skewness": args.skewness,
        "seed": args.seed,
        "shuffles": args.shuffles,
        "table_json": json.dumps(table.astype(int).tolist(), separators=(",", ":")),
        "g_statistic": g_value,
        "saddle_status": saddle_status,
        "saddle_route": saddle_route,
        "saddle_p": saddle_p,
        "saddle_time_s": saddle_time_s,
        "jidt_p": jidt.pvalue,
        "jidt_time_s": jidt.elapsed_s,
        "jidt_g_statistic": jidt.g_statistic,
        "jidt_g_abs_diff": abs(jidt.g_statistic - g_value),
        "jidt_over_saddle": (
            np.nan
            if not np.isfinite(saddle_time_s) or saddle_time_s <= 0
            else jidt.elapsed_s / saddle_time_s
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one long JIDT benchmark case.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--r", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--skewness", choices=["balanced", "mild", "strong"], required=True)
    parser.add_argument("--seed", type=int, default=20260706)
    parser.add_argument("--shuffles", type=int, required=True)
    parser.add_argument("--saddle-timeout-s", type=int, default=30)
    parser.add_argument("--skip-saddle", action="store_true")
    parser.add_argument("--exact-table-limit", type=int, default=1000)
    parser.add_argument("--jar-path", default=DEFAULT_JIDT_JAR)
    parser.add_argument("--output", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    row = run_case(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(output, index=False)
    print(pd.DataFrame([row]).drop(columns=["table_json"]).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
