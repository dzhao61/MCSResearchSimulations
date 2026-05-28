"""
Reconstruct exact Stage 9 descriptors without rerunning bootstraps.

The existing robust_regression_data.csv contains the expensive bootstrap
moments, but older rows did not store the exact analytic quantities needed by
Stage 12:

    Sx = sum_i 1/p_i, Sy = sum_j 1/q_j
    Bartlett B and C terms
    Poisson occupancy counts for zeros, singletons, and doubletons

Because Stage 9 generated the probability vectors deterministically from the
seed and mode settings, we can reconstruct the probability vectors for the
current data and merge these exact descriptors onto the existing bootstrap
results.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
STAGE9 = ROOT / "EffectiveDFCorrection_Stage9_RobustRegressions"
OUT = Path(__file__).resolve().parent

sys.path.insert(0, str(STAGE9))
import robust_regressions as rr  # noqa: E402


os.environ["XDG_CACHE_HOME"] = str(OUT / ".cache")
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)


EXACT_COLUMNS = [
    "x_inv_p_sum",
    "y_inv_p_sum",
    "x_inv_p2_sum",
    "y_inv_p2_sum",
    "bartlett_B",
    "bartlett_C",
    "expected_zero_count",
    "expected_singleton_count",
    "expected_doubleton_count",
    "expected_le1_count",
    "expected_le2_count",
    "expected_nonempty_count",
    "expected_zero_frac",
    "expected_singleton_frac",
    "expected_doubleton_frac",
    "expected_le1_frac",
    "expected_le2_frac",
    "collision_prob",
    "expected_collision_count",
    "birthday_ratio",
]

CHECK_COLUMNS = ["pi_min", "pi_max", "lam_min", "lam_tp", "cell_simpson"]


def mode_args(mode: str, seed: int) -> SimpleNamespace:
    defaults = rr.MODE_DEFAULTS[mode].copy()
    return SimpleNamespace(
        mode=mode,
        seed=seed,
        include_rectangular=False,
        min_N=10,
        max_N=20_000_000,
        **defaults,
    )


def descriptor_rows(mode: str, seed: int) -> list[dict]:
    args = mode_args(mode, seed)
    rng = np.random.default_rng(seed)
    rows = []
    for cfg in rr.make_configs(args, rng):
        sx = cfg["shape_x"]
        sy = cfg["shape_y"]
        desc = rr.pair_descriptors(sx.p, sy.p, int(cfg["N"]))
        row = {
            "config_id": cfg["config_id"],
            "descriptor_mode": mode,
            "descriptor_bootstrap": args.bootstrap,
        }
        for col in EXACT_COLUMNS + CHECK_COLUMNS:
            row[f"{col}_exact_check" if col in CHECK_COLUMNS else col] = desc[col]
        rows.append(row)
    return rows


def build_descriptors(modes: list[str], seed: int) -> pd.DataFrame:
    rows = []
    for mode in modes:
        mode_rows = descriptor_rows(mode, seed)
        print(f"Reconstructed {len(mode_rows)} descriptor rows for mode={mode}")
        rows.extend(mode_rows)
    return pd.DataFrame(rows).drop_duplicates("config_id", keep="last")


def validate_merge(enriched: pd.DataFrame) -> None:
    print("\n=== Reconstruction checks ===")
    for col in CHECK_COLUMNS:
        exact_col = f"{col}_exact_check"
        if col not in enriched or exact_col not in enriched:
            continue
        diff = np.abs(enriched[col].to_numpy(dtype=float) - enriched[exact_col].to_numpy(dtype=float))
        print(f"{col:<14} max_abs_diff={diff.max():.6g} median_abs_diff={np.median(diff):.6g}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        default=str(STAGE9 / "robust_regression_data.csv"),
        help="Existing Stage 9 data with bootstrap moments.",
    )
    parser.add_argument(
        "--out",
        default=str(OUT / "robust_regression_data_exact.csv"),
        help="Output CSV with exact descriptor columns merged in.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--modes",
        default="medium,full",
        help="Comma-separated Stage 9 modes to reconstruct.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data_path = Path(args.data)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    modes = [mode.strip() for mode in args.modes.split(",") if mode.strip()]
    descriptors = build_descriptors(modes, args.seed)

    missing = set(df["config_id"].astype(str)) - set(descriptors["config_id"].astype(str))
    if missing:
        sample = sorted(missing)[:5]
        raise RuntimeError(f"Could not reconstruct {len(missing)} config_ids; sample={sample}")

    drop_cols = [col for col in descriptors.columns if col in df.columns and col != "config_id"]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    enriched = df.merge(descriptors, on="config_id", how="left", validate="many_to_one")
    validate_merge(enriched)

    check_cols = [f"{col}_exact_check" for col in CHECK_COLUMNS]
    enriched = enriched.drop(columns=[col for col in check_cols if col in enriched])
    enriched.to_csv(out_path, index=False)
    print(f"\nSaved exact-descriptor data: {out_path} ({len(enriched)} rows)")


if __name__ == "__main__":
    main()
