#!/usr/bin/env python3
"""Confirm selected multi-alphabet LR calibration findings at higher precision."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))
sys.path.insert(0, str(REPOSITORY_ROOT / "DifferentialMI" / "src"))

from run_multialphabet_lr_experiment import (  # noqa: E402
    ALPHA,
    NULL_STAGE,
    _simulate_stage,
    build_population_design,
)


CONFIGURATIONS = (
    (3, "balanced", 250, "ordinary control"),
    (3, "ultra", 25, "screening LR loss"),
    (5, "balanced", 50, "screening LR gain"),
    (5, "ultra", 50, "screening LR loss"),
    (8, "mild", 25, "largest screening LR gain"),
    (8, "strong", 50, "screening LR gain"),
)


def _run_configuration(task: tuple[int, str, int, str, int, int]) -> dict:
    size, regime, sample_size, purpose, replicates, seed = task
    rows, diagnostics = _simulate_stage(
        build_population_design(size, regime),
        sample_size=sample_size,
        stage=NULL_STAGE,
        replicates=replicates,
        seed=seed,
    )
    for row in rows:
        row["selection_purpose"] = purpose
    diagnostics["selection_purpose"] = purpose
    return {"rows": rows, "diagnostics": diagnostics}


def _write_report(output_dir: Path, results: pd.DataFrame) -> None:
    lines = [
        "# Focused Multi-Alphabet LR Confirmation",
        "",
        "This run re-evaluates six exact null configurations selected before the",
        "confirmatory simulation. They include an ordinary control and screening",
        "cases in which constrained LR appeared either better or worse than Wald.",
        f"All tests use $\\alpha={ALPHA:.2f}$.",
        "",
        "| Shape | Regime | N | Purpose | Method | FPR | 95% interval | Valid rate |",
        "| --- | --- | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    ordered = results.sort_values(
        ["alphabet_size", "regime", "sample_size_p", "method"]
    )
    for row in ordered.itertuples(index=False):
        lines.append(
            f"| {row.shape} | {row.regime_label} | {row.sample_size_p} | "
            f"{row.selection_purpose} | {row.method_label} | "
            f"{row.rejection_rate:.4f} | "
            f"[{row.wilson_low:.4f}, {row.wilson_high:.4f}] | "
            f"{row.valid_rate:.4f} |"
        )
    lines.extend(
        [
            "",
            "The intervals quantify simulation uncertainty only. They do not",
            "represent variation over different population tables within a regime.",
        ]
    )
    (output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=2_000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2_026_090_101)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "multialphabet_lr_confirmatory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.replicates < 1 or args.workers < 1:
        raise ValueError("Replicates and workers must be positive.")
    tasks = [
        (*configuration, args.replicates, args.seed)
        for configuration in CONFIGURATIONS
    ]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = perf_counter()
    completed = []
    if args.workers == 1:
        for index, task in enumerate(tasks, start=1):
            completed.append(_run_configuration(task))
            print(f"Configurations: {index}/{len(tasks)}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(_run_configuration, task) for task in tasks]
            for index, future in enumerate(as_completed(futures), start=1):
                completed.append(future.result())
                print(f"Configurations: {index}/{len(tasks)}", flush=True)

    results = pd.DataFrame(
        [row for item in completed for row in item["rows"]]
    ).sort_values(["alphabet_size", "regime", "sample_size_p", "method"])
    diagnostics = pd.DataFrame(
        [item["diagnostics"] for item in completed]
    ).sort_values(["alphabet_size", "regime", "sample_size"])
    results.to_csv(args.output_dir / "results.csv", index=False)
    diagnostics.to_csv(args.output_dir / "lr_diagnostics.csv", index=False)
    _write_report(args.output_dir, results)
    metadata = {
        "replicates": args.replicates,
        "workers": args.workers,
        "seed": args.seed,
        "configurations": [list(item) for item in CONFIGURATIONS],
        "table_pair_count": args.replicates * len(CONFIGURATIONS),
        "elapsed_seconds": perf_counter() - started,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Completed in {metadata['elapsed_seconds']:.1f} seconds", flush=True)


if __name__ == "__main__":
    main()
