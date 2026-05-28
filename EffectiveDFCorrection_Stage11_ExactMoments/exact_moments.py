"""
Stage 11: Brute-force exact moments for the MI null.

For small N, enumerate every possible contingency table under the product
multinomial null and compute exact moments of

    T = 2N * I_hat(X;Y)   (nats).

This gives noise-free targets for:

    E[T], Var[T], nu_eff = 2 E[T]^2 / Var[T], a = Var[T] / (2 E[T])

The main payoff is to separate true finite-sample corrections from bootstrap
noise, and to test closed/asymptotic equations.  In particular, the entropy
bias expansion gives the first-order mean equation:

    E[T] = nu0 + ((Sx - 1)(Sy - 1)) / (6N) + O(N^-2)

where

    nu0 = (kx - 1)(ky - 1)
    Sx  = sum_i 1 / p_i
    Sy  = sum_j 1 / q_j

For the variance, this script fits exact values to candidate first-order
corrections:

    Var[T] = 2 nu0 + C(p, q) / N + O(N^-2)

and reports which descriptors explain C(p, q).
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import gammaln


OUT = Path(__file__).resolve().parent


def compositions(n: int, k: int):
    """Yield all k-part nonnegative integer vectors summing to n."""
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, k - 1):
            yield (first,) + rest


def mi_stat_from_counts(counts: np.ndarray) -> float:
    """Return T = 2N I_hat in nats for a contingency table."""
    N = int(counts.sum())
    if N == 0:
        return 0.0
    row = counts.sum(axis=1, keepdims=True)
    col = counts.sum(axis=0, keepdims=True)
    mask = counts > 0
    # T = 2 sum n_ij log(n_ij N / (n_i. n_.j))
    ratio = np.zeros_like(counts, dtype=float)
    ratio[mask] = counts[mask] * N / (row @ col)[mask]
    return float(2.0 * np.sum(counts[mask] * np.log(ratio[mask])))


def exact_moments(p_x: np.ndarray, p_y: np.ndarray, N: int) -> dict[str, float]:
    """Exact multinomial moments by enumerating all kx*ky cell-count vectors."""
    p_x = np.asarray(p_x, dtype=float)
    p_y = np.asarray(p_y, dtype=float)
    pi = np.outer(p_x, p_y).ravel()
    kx, ky = len(p_x), len(p_y)
    m = kx * ky

    log_fact_N = gammaln(N + 1)
    log_pi = np.log(pi)
    total_prob = 0.0
    mean = 0.0
    second = 0.0
    n_tables = 0

    for comp in compositions(N, m):
        n = np.array(comp, dtype=int)
        logp = log_fact_N - np.sum(gammaln(n + 1)) + float(n @ log_pi)
        prob = math.exp(logp)
        table = n.reshape(kx, ky)
        T = mi_stat_from_counts(table)
        total_prob += prob
        mean += prob * T
        second += prob * T * T
        n_tables += 1

    # Renormalize tiny floating error from exp/log summation.
    mean /= total_prob
    second /= total_prob
    var = second - mean * mean
    return {
        "N": N,
        "n_tables": n_tables,
        "prob_sum": total_prob,
        "mu": mean,
        "sigma2": var,
        "nu": 2 * mean * mean / var if var > 0 else np.nan,
        "a": var / (2 * mean) if mean > 0 else np.nan,
    }


def descriptors(p_x: np.ndarray, p_y: np.ndarray, N: int) -> dict[str, float]:
    p_x = np.asarray(p_x, dtype=float)
    p_y = np.asarray(p_y, dtype=float)
    pi = np.outer(p_x, p_y)
    expected = N * pi
    kx, ky = len(p_x), len(p_y)
    nu0 = (kx - 1) * (ky - 1)
    Sx = float(np.sum(1.0 / p_x))
    Sy = float(np.sum(1.0 / p_y))
    mean_c1 = (Sx - 1.0) * (Sy - 1.0) / 6.0
    return {
        "kx": kx,
        "ky": ky,
        "nu0": nu0,
        "Sx": Sx,
        "Sy": Sy,
        "Sxy": Sx * Sy,
        "mean_c1": mean_c1,
        "mean_order1": nu0 + mean_c1 / N,
        "lam_min": float(expected.min()),
        "lam_tp": float(N / np.sum(1.0 / pi)),
        "frac_lt1": float((expected < 1).mean()),
        "frac_lt5": float((expected < 5).mean()),
        "n_lt1": int((expected < 1).sum()),
        "n_lt5": int((expected < 5).sum()),
        "inv_lam_min": float(1.0 / expected.min()),
        "inv_lam_tp": float(np.sum(1.0 / pi) / N),
    }


def binary_grid() -> list[tuple[str, np.ndarray, np.ndarray, list[int]]]:
    configs = []
    pairs = [
        ("b_sym_0p5", [0.5, 0.5], [0.5, 0.5]),
        ("b_sym_0p2", [0.8, 0.2], [0.8, 0.2]),
        ("b_sym_0p1", [0.9, 0.1], [0.9, 0.1]),
        ("b_asym_0p5_0p1", [0.5, 0.5], [0.9, 0.1]),
        ("b_asym_0p2_0p05", [0.8, 0.2], [0.95, 0.05]),
    ]
    Ns = [8, 10, 12, 15, 20, 30, 40, 60, 80, 120]
    for label, px, py in pairs:
        configs.append((label, np.array(px), np.array(py), Ns))
    return configs


def ternary_grid() -> list[tuple[str, np.ndarray, np.ndarray, list[int]]]:
    configs = []
    pairs = [
        ("t_uniform", [1 / 3, 1 / 3, 1 / 3], [1 / 3, 1 / 3, 1 / 3]),
        ("t_rare_rare_0p1", [0.1, 0.1, 0.8], [0.1, 0.1, 0.8]),
        ("t_one_rare_0p05", [0.05, 0.475, 0.475], [0.05, 0.475, 0.475]),
        ("t_asym", [0.05, 0.25, 0.7], [0.1, 0.45, 0.45]),
    ]
    Ns = [6, 8, 10, 12, 15, 18]
    for label, px, py in pairs:
        configs.append((label, np.array(px), np.array(py), Ns))
    return configs


def generate_exact_grid(include_ternary: bool) -> pd.DataFrame:
    rows = []
    configs = binary_grid()
    if include_ternary:
        configs += ternary_grid()

    for label, p_x, p_y, Ns in configs:
        for N in Ns:
            desc = descriptors(p_x, p_y, N)
            print(
                f"{label:<20} N={N:3d} k={len(p_x)}x{len(p_y)} "
                f"tables={math.comb(N + len(p_x) * len(p_y) - 1, len(p_x) * len(p_y) - 1):>8d}",
                flush=True,
            )
            moments = exact_moments(p_x, p_y, N)
            rows.append(
                {
                    "config": label,
                    "p_x": ",".join(f"{v:.12g}" for v in p_x),
                    "p_y": ",".join(f"{v:.12g}" for v in p_y),
                    **desc,
                    **moments,
                }
            )
    df = pd.DataFrame(rows)
    df["mean_resid_order1"] = df["mu"] - df["mean_order1"]
    df["mean_c1_emp"] = df["N"] * (df["mu"] - df["nu0"])
    df["var_c1_emp"] = df["N"] * (df["sigma2"] - 2 * df["nu0"])
    df["nu_norm"] = df["nu"] / df["nu0"]
    return df


def fit_variance_correction(df: pd.DataFrame) -> pd.DataFrame:
    """Fit Var[T] - 2nu0 = C/N to candidate descriptors."""
    rows = []
    d = df[df["nu0"] > 0].copy()
    y = d["var_c1_emp"].to_numpy(float)
    candidates = {
        "mean_c1": ["mean_c1"],
        "Sxy": ["Sxy"],
        "Sx+Sy+Sxy": ["Sx", "Sy", "Sxy"],
        "mean_c1+nu0": ["mean_c1", "nu0"],
        "sparse_geom": ["mean_c1", "frac_lt1", "frac_lt5", "inv_lam_min", "inv_lam_tp"],
    }
    for name, features in candidates.items():
        X = d[features].to_numpy(float)
        X = np.column_stack([np.ones(len(X)), X])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        pred = X @ beta
        ss_res = float(np.sum((y - pred) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        rows.append(
            {
                "model": name,
                "features": "intercept," + ",".join(features),
                "r2": 1 - ss_res / ss_tot,
                "rmse": float(np.sqrt(np.mean((y - pred) ** 2))),
                "coefficients": ",".join(f"{v:.8g}" for v in beta),
            }
        )
    return pd.DataFrame(rows).sort_values("r2", ascending=False)


def summarize_mean(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for config, grp in df.groupby("config"):
        rows.append(
            {
                "config": config,
                "n": len(grp),
                "nu0": grp["nu0"].iloc[0],
                "mean_c1_theory": grp["mean_c1"].iloc[0],
                "mean_c1_emp_lastN": grp.sort_values("N")["mean_c1_emp"].iloc[-1],
                "max_abs_mean_order1_error": float(grp["mean_resid_order1"].abs().max()),
                "lastN_mean_order1_error": grp.sort_values("N")["mean_resid_order1"].iloc[-1],
            }
        )
    return pd.DataFrame(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default=str(OUT))
    parser.add_argument("--include-ternary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = generate_exact_grid(args.include_ternary)
    var_fit = fit_variance_correction(df)
    mean_summary = summarize_mean(df)

    data_path = out_dir / "exact_moment_grid.csv"
    var_path = out_dir / "variance_correction_fits.csv"
    mean_path = out_dir / "mean_equation_summary.csv"
    df.to_csv(data_path, index=False)
    var_fit.to_csv(var_path, index=False)
    mean_summary.to_csv(mean_path, index=False)

    print(f"\nSaved exact grid: {data_path}")
    print(f"Saved variance fits: {var_path}")
    print(f"Saved mean summary: {mean_path}")

    print("\n=== Mean equation summary ===")
    print(mean_summary.to_string(index=False))
    print("\n=== Variance correction fits: Var[T] = 2nu0 + C/N ===")
    print(var_fit.to_string(index=False))


if __name__ == "__main__":
    main()
