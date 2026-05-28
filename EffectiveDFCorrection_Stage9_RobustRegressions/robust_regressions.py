"""
Stage 9: High-volume effective-degrees-of-freedom regression lab.

Goal
----
Generate a broad simulation dataset for the MI null under independence and
fit many descriptor-based regressions for the effective-DF correction:

    T = 2N I(X;Y)  ~=  a * chi2(nu_eff)

For each simulated configuration we estimate:

    nu_eff = 2 * mean(T)^2 / var(T)
    a      = var(T) / (2 * mean(T))

and regress the normalized targets

    nu_norm = nu_eff / nu0,    nu0 = (kx - 1)(ky - 1)
    a

against sparsity and marginal-shape descriptors.

This stage is intentionally more empirical than Stages 2-8.  It is meant to
answer: "If we generate a lot of data from many regimes, what descriptors
actually predict the effective degrees of freedom robustly?"

The bootstrap is vectorized with numpy multinomial draws, so it can generate
much more data than the JIDT-per-surrogate loops.

Examples
--------
Small smoke test:

    python robust_regressions.py --mode smoke

Bigger run:

    python robust_regressions.py --mode full --bootstrap 5000 --resume

Fit existing data only:

    python robust_regressions.py --fit-only --data robust_regression_data.csv
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

OUT = os.path.dirname(os.path.abspath(__file__))

# The workspace is writable, but the user's home matplotlib/fontconfig cache may
# not be. Set this before importing pyplot so smoke/full runs work cleanly.
os.environ["XDG_CACHE_HOME"] = os.path.join(OUT, ".cache")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(OUT, ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

plt = None


MODE_DEFAULTS = {
    "smoke": dict(
        k_min=2,
        k_max=5,
        bootstrap=300,
        max_pairs_per_k=6,
        dirichlet_reps=0,
        lambda_targets="0.5,1,2,5",
    ),
    "medium": dict(
        k_min=2,
        k_max=10,
        bootstrap=2_000,
        max_pairs_per_k=14,
        dirichlet_reps=1,
        lambda_targets="0.1,0.2,0.35,0.5,0.75,1,1.5,2,3,5,8,12,20,30",
    ),
    "full": dict(
        k_min=2,
        k_max=18,
        bootstrap=5_000,
        max_pairs_per_k=30,
        dirichlet_reps=2,
        lambda_targets="0.1,0.15,0.25,0.35,0.5,0.65,0.8,1,1.25,1.6,2,2.5,3.2,4,5,7.5,10,15,22,30",
    ),
}


RIDGE_ALPHAS = [0.0, 1e-8, 1e-6, 1e-4, 1e-2, 1.0]
PHYSICAL_CONFIG_KEY = ["kx", "ky", "shape_x", "shape_y", "N", "lam_target"]


@dataclass(frozen=True)
class Shape:
    label: str
    family: str
    p: np.ndarray


def parse_lambda_targets(text: str) -> list[float]:
    return sorted({float(x.strip()) for x in text.split(",") if x.strip()})


def float_label(x: float) -> str:
    return f"{x:g}".replace(".", "p").replace("-", "m")


def entropy_bits(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def gini(p: np.ndarray) -> float:
    """Gini coefficient for a probability vector."""
    x = np.sort(np.asarray(p, dtype=float))
    n = len(x)
    if n == 0 or x.sum() <= 0:
        return np.nan
    return float((2 * np.arange(1, n + 1) @ x) / (n * x.sum()) - (n + 1) / n)


def vector_descriptors(p: np.ndarray, prefix: str) -> dict[str, float]:
    k = len(p)
    H = entropy_bits(p)
    perp = 2.0**H
    simpson = 1.0 / float(np.sum(p**2))
    return {
        f"{prefix}_k": float(k),
        f"{prefix}_H": H,
        f"{prefix}_H_norm": H / np.log2(k) if k > 1 else 1.0,
        f"{prefix}_perp": perp,
        f"{prefix}_perp_n": perp / k,
        f"{prefix}_simpson": simpson,
        f"{prefix}_simpson_n": simpson / k,
        f"{prefix}_min_p": float(p.min()),
        f"{prefix}_max_p": float(p.max()),
        f"{prefix}_k_min_p": float(k * p.min()),
        f"{prefix}_max_min_ratio": float(p.max() / max(p.min(), 1e-300)),
        f"{prefix}_gini": gini(p),
    }


def make_marginal_library(k: int, rng: np.random.Generator, dirichlet_reps: int) -> list[Shape]:
    shapes: list[Shape] = [Shape("uniform", "uniform", np.full(k, 1.0 / k))]

    for ratio in [0.8, 0.5, 0.2, 0.05]:
        p_rare = ratio / k
        rest = (1 - p_rare) / (k - 1)
        p = np.concatenate([[p_rare], np.full(k - 1, rest)])
        shapes.append(Shape(f"one_rare_{float_label(ratio)}", "one_rare", p))

    if k >= 4:
        p_rare = 0.3 / k
        rest = (1 - 2 * p_rare) / (k - 2)
        p = np.concatenate([[p_rare, p_rare], np.full(k - 2, rest)])
        shapes.append(Shape("two_rare_0p3", "two_rare", p))

    for alpha in [0.7, 1.0, 1.3]:
        ranks = np.arange(1, k + 1, dtype=float)
        p = ranks ** (-alpha)
        shapes.append(Shape(f"zipf_a{float_label(alpha)}", "zipf", p / p.sum()))

    for q in [0.6, 0.8]:
        ranks = np.arange(k, dtype=float)
        p = q**ranks
        shapes.append(Shape(f"geom_q{float_label(q)}", "geometric", p / p.sum()))

    # Random shapes add coverage, but avoid vanishingly tiny cells that would
    # demand astronomical N just to hit lambda_min ~= 1.
    for alpha in [0.3, 1.0]:
        accepted = 0
        attempts = 0
        while accepted < dirichlet_reps and attempts < 200:
            attempts += 1
            p = rng.dirichlet(np.full(k, alpha))
            if k * p.min() < 0.03:
                continue
            label = f"dirichlet_a{float_label(alpha)}_{accepted}"
            shapes.append(Shape(label, f"dirichlet_{float_label(alpha)}", p))
            accepted += 1

    return shapes


def select_shape_pairs(
    x_shapes: list[Shape],
    y_shapes: list[Shape],
    max_pairs: int,
    rng: np.random.Generator,
    same_alphabet: bool,
) -> list[tuple[Shape, Shape]]:
    pairs: list[tuple[Shape, Shape]] = []
    seen: set[tuple[str, str]] = set()

    def add(sx: Shape, sy: Shape) -> None:
        key = (sx.label, sy.label)
        if key not in seen:
            pairs.append((sx, sy))
            seen.add(key)

    x_by_label = {s.label: s for s in x_shapes}
    y_by_label = {s.label: s for s in y_shapes}

    if same_alphabet:
        for label in x_by_label:
            if label in y_by_label:
                add(x_by_label[label], y_by_label[label])

    uniform_x = x_by_label.get("uniform")
    uniform_y = y_by_label.get("uniform")
    if uniform_x is not None:
        for sy in y_shapes:
            add(uniform_x, sy)
    if uniform_y is not None:
        for sx in x_shapes:
            add(sx, uniform_y)

    priority_families = {"one_rare", "two_rare", "zipf", "geometric"}
    for sx in x_shapes:
        for sy in y_shapes:
            if sx.family in priority_families and sy.family in priority_families:
                if sx.family != sy.family:
                    add(sx, sy)
                if len(pairs) >= max_pairs:
                    return pairs[:max_pairs]

    all_pairs = [(sx, sy) for sx in x_shapes for sy in y_shapes]
    rng.shuffle(all_pairs)
    for sx, sy in all_pairs:
        add(sx, sy)
        if len(pairs) >= max_pairs:
            break

    return pairs[:max_pairs]


def bootstrap_moments(
    p_x: np.ndarray,
    p_y: np.ndarray,
    N: int,
    K: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    """Vectorized product-null bootstrap. T is returned in nats."""
    kx, ky = len(p_x), len(p_y)
    pi = np.outer(p_x, p_y).ravel()
    counts = rng.multinomial(N, pi, size=K)
    P = counts.reshape(K, kx, ky) / N
    px = P.sum(axis=2, keepdims=True)
    py = P.sum(axis=1, keepdims=True)
    denom = np.maximum(px * py, 1e-300)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_term = np.where(P > 0, np.log(P / denom), 0.0)
    T = 2 * N * (P * log_term).sum(axis=(1, 2))

    mu = float(T.mean())
    sigma2 = float(T.var(ddof=1))
    if sigma2 <= 0 or mu <= 0:
        nu = np.nan
        a = np.nan
    else:
        nu = 2 * mu**2 / sigma2
        a = sigma2 / (2 * mu)

    return {
        "mu": mu,
        "sigma2": sigma2,
        "nu": float(nu),
        "a": float(a),
        "T_q50": float(np.quantile(T, 0.50)),
        "T_q90": float(np.quantile(T, 0.90)),
        "T_q95": float(np.quantile(T, 0.95)),
        "T_q99": float(np.quantile(T, 0.99)),
    }


def pair_descriptors(p_x: np.ndarray, p_y: np.ndarray, N: int) -> dict[str, float]:
    kx, ky = len(p_x), len(p_y)
    pi = np.outer(p_x, p_y)
    expected = N * pi
    poisson_zero = np.exp(-np.minimum(expected, 700.0))
    poisson_singleton = expected * poisson_zero
    poisson_doubleton = 0.5 * expected**2 * poisson_zero
    Hx = entropy_bits(p_x)
    Hy = entropy_bits(p_y)
    cell_perp = 2.0 ** (Hx + Hy)
    cell_simpson = 1.0 / float(np.sum(pi**2))
    x_inv_p_sum = float(np.sum(1.0 / p_x))
    y_inv_p_sum = float(np.sum(1.0 / p_y))
    x_inv_p2_sum = float(np.sum(1.0 / (p_x**2)))
    y_inv_p2_sum = float(np.sum(1.0 / (p_y**2)))
    inv_pi_sum = float(np.sum(1.0 / pi))
    inv_sqrt_pi_sum = float(np.sum(1.0 / np.sqrt(pi)))
    bartlett_B = ((x_inv_p_sum - 1.0) * (y_inv_p_sum - 1.0)) / 6.0
    bartlett_C = (
        x_inv_p2_sum * y_inv_p2_sum
        - x_inv_p_sum * y_inv_p_sum
        - (x_inv_p2_sum - x_inv_p_sum)
        - (y_inv_p2_sum - y_inv_p_sum)
    ) / 6.0
    collision_prob = float(np.sum(pi**2))
    expected_collision_count = N * (N - 1.0) * collision_prob / 2.0
    nu0 = (kx - 1) * (ky - 1)
    q95_chi2 = float(stats.chi2.ppf(0.95, df=nu0)) if nu0 > 0 else np.nan
    q99_chi2 = float(stats.chi2.ppf(0.99, df=nu0)) if nu0 > 0 else np.nan

    out = {
        "kx": float(kx),
        "ky": float(ky),
        "k_cells": float(kx * ky),
        "nu0": float(nu0),
        "log_nu0": float(np.log(max(nu0, 1.0))),
        "log_k_cells": float(np.log(kx * ky)),
        "N": float(N),
        "pi_min": float(pi.min()),
        "pi_max": float(pi.max()),
        "pi_max_min_ratio": float(pi.max() / max(pi.min(), 1e-300)),
        "lam_min": float(expected.min()),
        "lam_tp": float(N / inv_pi_sum),
        "lam_sqrt_harm": float(N / inv_sqrt_pi_sum),
        "x_inv_p_sum": x_inv_p_sum,
        "y_inv_p_sum": y_inv_p_sum,
        "x_inv_p2_sum": x_inv_p2_sum,
        "y_inv_p2_sum": y_inv_p2_sum,
        "inv_pi_sum": inv_pi_sum,
        "inv_sqrt_pi_sum": inv_sqrt_pi_sum,
        "bartlett_B": float(bartlett_B),
        "bartlett_C": float(bartlett_C),
        "expected_mean": float(expected.mean()),
        "expected_sd": float(expected.std(ddof=0)),
        "expected_cv": float(expected.std(ddof=0) / max(expected.mean(), 1e-300)),
        "expected_zero_count": float(poisson_zero.sum()),
        "expected_singleton_count": float(poisson_singleton.sum()),
        "expected_doubleton_count": float(poisson_doubleton.sum()),
        "expected_le1_count": float(poisson_zero.sum() + poisson_singleton.sum()),
        "expected_le2_count": float(
            poisson_zero.sum() + poisson_singleton.sum() + poisson_doubleton.sum()
        ),
        "expected_nonempty_count": float(np.sum(1.0 - poisson_zero)),
        "expected_zero_frac": float(poisson_zero.mean()),
        "expected_singleton_frac": float(poisson_singleton.mean()),
        "expected_doubleton_frac": float(poisson_doubleton.mean()),
        "expected_le1_frac": float((poisson_zero + poisson_singleton).mean()),
        "expected_le2_frac": float((poisson_zero + poisson_singleton + poisson_doubleton).mean()),
        "n_cells_lt_0p5": int((expected < 0.5).sum()),
        "n_cells_lt_1": int((expected < 1.0).sum()),
        "n_cells_lt_5": int((expected < 5.0).sum()),
        "frac_cells_lt_0p5": float((expected < 0.5).mean()),
        "frac_cells_lt_1": float((expected < 1.0).mean()),
        "frac_cells_lt_5": float((expected < 5.0).mean()),
        "H_cell": Hx + Hy,
        "H_cell_norm": (Hx + Hy) / np.log2(kx * ky),
        "cell_perp": cell_perp,
        "cell_perp_n": cell_perp / (kx * ky),
        "cell_simpson": cell_simpson,
        "cell_simpson_n": cell_simpson / (kx * ky),
        "collision_prob": collision_prob,
        "expected_collision_count": float(expected_collision_count),
        "birthday_ratio": float(N / np.sqrt(cell_simpson)),
        "q95_chi2": q95_chi2,
        "q99_chi2": q99_chi2,
    }
    out.update(vector_descriptors(p_x, "x"))
    out.update(vector_descriptors(p_y, "y"))
    return out


def make_configs(args: argparse.Namespace, rng: np.random.Generator) -> list[dict]:
    lambda_targets = parse_lambda_targets(args.lambda_targets)
    configs: list[dict] = []
    k_pairs = [(k, k) for k in range(args.k_min, args.k_max + 1)]
    if args.include_rectangular:
        k_pairs.extend((k, k + 1) for k in range(args.k_min, args.k_max))

    for kx, ky in k_pairs:
        x_shapes = make_marginal_library(kx, rng, args.dirichlet_reps)
        y_shapes = make_marginal_library(ky, rng, args.dirichlet_reps)
        pairs = select_shape_pairs(
            x_shapes,
            y_shapes,
            args.max_pairs_per_k,
            rng,
            same_alphabet=(kx == ky),
        )

        for sx, sy in pairs:
            pi_min = float(sx.p.min() * sy.p.min())
            for lam_target in lambda_targets:
                raw_N = lam_target / pi_min
                if raw_N < args.min_N or raw_N > args.max_N:
                    continue
                N = int(round(raw_N))
                if N < args.min_N or N > args.max_N:
                    continue
                lam_actual = N * pi_min
                cfg_id = (
                    f"kx={kx}|ky={ky}|x={sx.label}|y={sy.label}|"
                    f"N={N}|K={args.bootstrap}"
                )
                configs.append(
                    dict(
                        config_id=cfg_id,
                        kx=kx,
                        ky=ky,
                        shape_x=sx,
                        shape_y=sy,
                        N=N,
                        lam_target=lam_target,
                        lam_actual=lam_actual,
                    )
                )

    return configs


def save_rows(rows: list[dict], path: str) -> None:
    if not rows:
        return
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)


def generate_data(args: argparse.Namespace) -> pd.DataFrame:
    data_path = os.path.join(args.out_dir, args.data)
    rng = np.random.default_rng(args.seed)
    configs = make_configs(args, rng)

    existing = pd.DataFrame()
    done_ids: set[str] = set()
    rows: list[dict] = []
    if args.resume and os.path.exists(data_path):
        existing = pd.read_csv(data_path)
        if "config_id" in existing:
            done_ids = set(existing["config_id"].astype(str))
        rows = existing.to_dict("records")
        print(f"Resume enabled: loaded {len(done_ids)} completed configs")

    configs = [cfg for cfg in configs if cfg["config_id"] not in done_ids]
    print(f"Configs to run: {len(configs)}")
    if not configs and rows:
        return pd.DataFrame(rows)

    t0 = time.time()
    for i, cfg in enumerate(configs, start=1):
        sx: Shape = cfg["shape_x"]
        sy: Shape = cfg["shape_y"]
        N = int(cfg["N"])
        start = time.time()
        moments = bootstrap_moments(sx.p, sy.p, N, args.bootstrap, rng)
        desc = pair_descriptors(sx.p, sy.p, N)
        nu0 = desc["nu0"]
        row = {
            "config_id": cfg["config_id"],
            "seed": args.seed,
            "bootstrap": args.bootstrap,
            "shape_x": sx.label,
            "shape_y": sy.label,
            "family_x": sx.family,
            "family_y": sy.family,
            "pair_family": f"{sx.family}|{sy.family}",
            "symmetric_shape": sx.label == sy.label and cfg["kx"] == cfg["ky"],
            "lam_target": cfg["lam_target"],
            **desc,
            **moments,
        }
        row["nu_norm"] = row["nu"] / nu0 if nu0 > 0 else np.nan
        row["q95_ratio_chi2"] = row["T_q95"] / row["q95_chi2"] if row["q95_chi2"] > 0 else np.nan
        row["q99_ratio_chi2"] = row["T_q99"] / row["q99_chi2"] if row["q99_chi2"] > 0 else np.nan
        rows.append(row)

        if i == 1 or i % args.progress_every == 0 or i == len(configs):
            elapsed = time.time() - t0
            rate = i / elapsed if elapsed > 0 else np.nan
            eta = (len(configs) - i) / rate if rate > 0 else 0.0
            print(
                f"[{i:5d}/{len(configs)}] k={cfg['kx']}x{cfg['ky']} "
                f"{sx.label} vs {sy.label} N={N} "
                f"lam_min={row['lam_min']:.3g} nu_norm={row['nu_norm']:.3g} "
                f"a={row['a']:.3g} ({time.time() - start:.2f}s, ETA {eta/60:.1f}m)",
                flush=True,
            )

        if args.checkpoint_every and i % args.checkpoint_every == 0:
            save_rows(rows, data_path)
            print(f"Checkpoint saved: {data_path}")

    save_rows(rows, data_path)
    print(f"Saved data: {data_path} ({len(rows)} rows)")
    return pd.DataFrame(rows)


def add_regression_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    eps = 1e-12
    d["inv_lam_min"] = 1.0 / np.maximum(d["lam_min"], eps)
    d["inv_lam_min_sq"] = d["inv_lam_min"] ** 2
    d["inv_sqrt_lam_min"] = 1.0 / np.sqrt(np.maximum(d["lam_min"], eps))
    d["inv_lam_tp"] = 1.0 / np.maximum(d["lam_tp"], eps)
    d["inv_sqrt_lam_tp"] = 1.0 / np.sqrt(np.maximum(d["lam_tp"], eps))
    d["inv_lam_sqrt_harm"] = 1.0 / np.maximum(d["lam_sqrt_harm"], eps)
    d["one_minus_H_cell_norm"] = 1.0 - d["H_cell_norm"]
    d["one_minus_cell_perp_n"] = 1.0 - d["cell_perp_n"]
    d["one_minus_cell_simpson_n"] = 1.0 - d["cell_simpson_n"]
    d["mean_k_min_p"] = 0.5 * (d["x_k_min_p"] + d["y_k_min_p"])
    d["min_k_min_p"] = np.minimum(d["x_k_min_p"], d["y_k_min_p"])
    d["mean_H_norm"] = 0.5 * (d["x_H_norm"] + d["y_H_norm"])
    d["min_H_norm"] = np.minimum(d["x_H_norm"], d["y_H_norm"])
    d["asym_H_norm"] = np.abs(d["x_H_norm"] - d["y_H_norm"])
    d["asym_min_p"] = np.abs(np.log(np.maximum(d["x_min_p"], eps)) - np.log(np.maximum(d["y_min_p"], eps)))
    d["n_lt1_norm_nu0"] = d["n_cells_lt_1"] / np.maximum(d["nu0"], 1.0)
    d["n_lt5_norm_nu0"] = d["n_cells_lt_5"] / np.maximum(d["nu0"], 1.0)

    # Weighted rarity terms matter when only one cell is extremely rare.  A raw
    # lambda_min feature overreacts in that regime; multiplying by the fraction
    # or normalized count of sparse cells lets the model distinguish "one tiny
    # corner" from "the whole table is under-sampled".
    d["inv_lam_min_x_frac_lt1"] = d["inv_lam_min"] * d["frac_cells_lt_1"]
    d["inv_lam_min_x_frac_lt5"] = d["inv_lam_min"] * d["frac_cells_lt_5"]
    d["inv_sqrt_lam_min_x_frac_lt1"] = d["inv_sqrt_lam_min"] * d["frac_cells_lt_1"]
    d["inv_sqrt_lam_min_x_frac_lt5"] = d["inv_sqrt_lam_min"] * d["frac_cells_lt_5"]
    d["inv_lam_min_x_n_lt1_norm_nu0"] = d["inv_lam_min"] * d["n_lt1_norm_nu0"]
    d["inv_lam_min_x_n_lt5_norm_nu0"] = d["inv_lam_min"] * d["n_lt5_norm_nu0"]
    d["inv_sqrt_lam_min_x_n_lt1_norm_nu0"] = d["inv_sqrt_lam_min"] * d["n_lt1_norm_nu0"]
    d["inv_sqrt_lam_min_x_n_lt5_norm_nu0"] = d["inv_sqrt_lam_min"] * d["n_lt5_norm_nu0"]

    interaction_sources = [
        "log_nu0",
        "log_k_cells",
        "one_minus_H_cell_norm",
        "one_minus_cell_perp_n",
        "one_minus_cell_simpson_n",
        "frac_cells_lt_0p5",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "expected_cv",
        "mean_k_min_p",
        "min_k_min_p",
        "mean_H_norm",
        "min_H_norm",
        "asym_H_norm",
        "asym_min_p",
    ]
    for col in interaction_sources:
        d[f"tp_x_{col}"] = d["inv_lam_tp"] * d[col]
        d[f"minlam_x_{col}"] = d["inv_lam_min"] * d[col]

    return d


FEATURE_SETS: dict[str, list[str]] = {
    "lambda_min": ["inv_lam_min"],
    "lambda_min_power": ["inv_lam_min", "inv_sqrt_lam_min", "inv_lam_min_sq"],
    "lambda_tp": ["inv_lam_tp"],
    "lambda_tp_power": ["inv_lam_tp", "inv_sqrt_lam_tp"],
    "tp_size": ["inv_lam_tp", "tp_x_log_nu0", "tp_x_log_k_cells"],
    "tp_entropy": [
        "inv_lam_tp",
        "tp_x_one_minus_H_cell_norm",
        "tp_x_one_minus_cell_perp_n",
        "tp_x_one_minus_cell_simpson_n",
    ],
    "tp_sparsity": [
        "inv_lam_tp",
        "tp_x_frac_cells_lt_0p5",
        "tp_x_frac_cells_lt_1",
        "tp_x_frac_cells_lt_5",
        "tp_x_expected_cv",
    ],
    "tp_shape_asymmetry": [
        "inv_lam_tp",
        "tp_x_mean_k_min_p",
        "tp_x_min_k_min_p",
        "tp_x_mean_H_norm",
        "tp_x_min_H_norm",
        "tp_x_asym_H_norm",
        "tp_x_asym_min_p",
    ],
    "mixed_sparsity": [
        "inv_lam_min",
        "inv_sqrt_lam_min",
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
    ],
    "weighted_frac_sparsity": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "inv_lam_min_x_frac_lt1",
        "inv_sqrt_lam_min_x_frac_lt1",
        "inv_lam_min_x_frac_lt5",
        "inv_sqrt_lam_min_x_frac_lt5",
    ],
    "weighted_count_sparsity": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
        "inv_lam_min_x_n_lt1_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt1_norm_nu0",
        "inv_lam_min_x_n_lt5_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt5_norm_nu0",
    ],
    "hybrid_weighted_sparsity": [
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "frac_cells_lt_1",
        "frac_cells_lt_5",
        "n_lt1_norm_nu0",
        "n_lt5_norm_nu0",
        "inv_lam_min_x_frac_lt1",
        "inv_sqrt_lam_min_x_frac_lt1",
        "inv_lam_min_x_n_lt1_norm_nu0",
        "inv_sqrt_lam_min_x_n_lt1_norm_nu0",
    ],
    "rich_interactions": [
        "inv_lam_min",
        "inv_sqrt_lam_min",
        "inv_lam_tp",
        "inv_sqrt_lam_tp",
        "inv_lam_sqrt_harm",
        "tp_x_log_nu0",
        "tp_x_log_k_cells",
        "tp_x_one_minus_H_cell_norm",
        "tp_x_one_minus_cell_perp_n",
        "tp_x_one_minus_cell_simpson_n",
        "tp_x_frac_cells_lt_0p5",
        "tp_x_frac_cells_lt_1",
        "tp_x_frac_cells_lt_5",
        "tp_x_expected_cv",
        "tp_x_mean_k_min_p",
        "tp_x_min_k_min_p",
        "tp_x_mean_H_norm",
        "tp_x_min_H_norm",
        "tp_x_asym_H_norm",
        "tp_x_asym_min_p",
    ],
}


def r2_score(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan


def fit_ridge_zero_asymptote(
    X: np.ndarray,
    y_delta: np.ndarray,
    alpha: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fit y = 1 + X beta, with feature scaling but no centering.

    No centering preserves the intended asymptote: when inverse-sparsity
    features go to zero, the correction goes to 1.
    """
    scale = np.sqrt(np.mean(X**2, axis=0))
    scale = np.where(scale > 0, scale, 1.0)
    Xs = X / scale
    lhs = Xs.T @ Xs + alpha * np.eye(Xs.shape[1])
    rhs = Xs.T @ y_delta
    beta_scaled = np.linalg.pinv(lhs) @ rhs
    beta = beta_scaled / scale
    pred_delta = X @ beta
    return beta, pred_delta, scale


def kfold_predictions(
    X: np.ndarray,
    y_delta: np.ndarray,
    alpha: float,
    n_folds: int,
    rng: np.random.Generator,
) -> np.ndarray:
    n = len(y_delta)
    pred = np.full(n, np.nan)
    order = rng.permutation(n)
    folds = np.array_split(order, min(n_folds, n))
    for fold in folds:
        train = np.ones(n, dtype=bool)
        train[fold] = False
        beta, _, _ = fit_ridge_zero_asymptote(X[train], y_delta[train], alpha)
        pred[fold] = X[fold] @ beta
    return pred


def group_predictions(
    X: np.ndarray,
    y_delta: np.ndarray,
    groups: np.ndarray,
    alpha: float,
) -> np.ndarray:
    pred = np.full(len(y_delta), np.nan)
    unique = np.unique(groups)
    if len(unique) < 2:
        return pred
    for group in unique:
        test = groups == group
        train = ~test
        if train.sum() <= X.shape[1] or test.sum() == 0:
            continue
        beta, _, _ = fit_ridge_zero_asymptote(X[train], y_delta[train], alpha)
        pred[test] = X[test] @ beta
    return pred


def fit_regressions(df: pd.DataFrame, args: argparse.Namespace) -> tuple[pd.DataFrame, pd.DataFrame]:
    d = add_regression_features(df)
    d = d.replace([np.inf, -np.inf], np.nan)
    d = d.dropna(subset=["nu_norm", "a"])

    results: list[dict] = []
    prediction_frames: list[pd.DataFrame] = []
    rng = np.random.default_rng(args.seed + 10_000)

    for target in ["nu_norm", "a"]:
        y = d[target].to_numpy(dtype=float)
        y_delta = y - 1.0

        for feature_set, features in FEATURE_SETS.items():
            clean = d.dropna(subset=features + [target])
            if len(clean) < max(10, len(features) + 3):
                continue
            X = clean[features].to_numpy(dtype=float)
            y_clean = clean[target].to_numpy(dtype=float)
            y_delta_clean = y_clean - 1.0
            groups = clean["pair_family"].astype(str).to_numpy()

            best = None
            for alpha in RIDGE_ALPHAS:
                beta, pred_delta, _ = fit_ridge_zero_asymptote(X, y_delta_clean, alpha)
                pred = 1.0 + pred_delta
                train_r2 = r2_score(y_clean, pred)

                cv_delta = kfold_predictions(
                    X,
                    y_delta_clean,
                    alpha,
                    args.cv_folds,
                    rng,
                )
                cv_mask = np.isfinite(cv_delta)
                cv_r2 = r2_score(y_clean[cv_mask], 1.0 + cv_delta[cv_mask])

                group_delta = group_predictions(X, y_delta_clean, groups, alpha)
                group_mask = np.isfinite(group_delta)
                group_r2 = (
                    r2_score(y_clean[group_mask], 1.0 + group_delta[group_mask])
                    if group_mask.sum() >= 3
                    else np.nan
                )

                score = cv_r2 if np.isfinite(cv_r2) else train_r2
                if best is None or score > best["score"]:
                    best = dict(
                        score=score,
                        alpha=alpha,
                        beta=beta,
                        pred=pred,
                        train_r2=train_r2,
                        cv_r2=cv_r2,
                        group_r2=group_r2,
                    )

            if best is None:
                continue

            coef = {name: float(value) for name, value in zip(features, best["beta"])}
            results.append(
                dict(
                    target=target,
                    feature_set=feature_set,
                    n=len(clean),
                    n_features=len(features),
                    alpha=best["alpha"],
                    train_r2=best["train_r2"],
                    random_cv_r2=best["cv_r2"],
                    group_cv_r2=best["group_r2"],
                    features=",".join(features),
                    coefficients=json.dumps(coef, sort_keys=True),
                )
            )

            prediction_frames.append(
                pd.DataFrame(
                    {
                        "config_id": clean["config_id"].values,
                        "target": target,
                        "feature_set": feature_set,
                        "observed": y_clean,
                        "predicted": best["pred"],
                        "residual": y_clean - best["pred"],
                    }
                )
            )

    result_df = pd.DataFrame(results).sort_values(
        ["target", "random_cv_r2", "train_r2"],
        ascending=[True, False, False],
    )
    pred_df = pd.concat(prediction_frames, ignore_index=True) if prediction_frames else pd.DataFrame()

    result_path = os.path.join(args.out_dir, args.results)
    pred_path = os.path.join(args.out_dir, args.predictions)
    result_df.to_csv(result_path, index=False)
    pred_df.to_csv(pred_path, index=False)
    print(f"Saved regression results: {result_path}")
    print(f"Saved predictions: {pred_path}")
    return result_df, pred_df


def plot_best_predictions(results: pd.DataFrame, predictions: pd.DataFrame, args: argparse.Namespace) -> None:
    global plt
    if results.empty or predictions.empty:
        return
    if plt is None:
        try:
            import matplotlib.pyplot as _plt
            plt = _plt
        except Exception as exc:  # pragma: no cover - plotting is optional
            print(f"Skipping plot; matplotlib import failed: {exc}")
            return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, target in zip(axes, ["nu_norm", "a"]):
        sub_results = results[results["target"] == target]
        if sub_results.empty:
            ax.set_visible(False)
            continue
        best = sub_results.iloc[0]
        sub = predictions[
            (predictions["target"] == target)
            & (predictions["feature_set"] == best["feature_set"])
        ]
        ax.scatter(sub["observed"], sub["predicted"], s=24, alpha=0.65)
        lo = float(min(sub["observed"].min(), sub["predicted"].min()))
        hi = float(max(sub["observed"].max(), sub["predicted"].max()))
        ax.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1.0)
        ax.set_xlabel("observed")
        ax.set_ylabel("predicted")
        ax.set_title(
            f"{target}: {best['feature_set']}\n"
            f"CV R2={best['random_cv_r2']:.3f}, group R2={best['group_cv_r2']:.3f}"
        )
        ax.grid(True, alpha=0.25, linestyle="--")

    fig.suptitle("Stage 9 robust regressions: best observed vs predicted")
    plt.tight_layout()
    out = os.path.join(args.out_dir, "robust_regression_best_predictions.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot: {out}")


def print_top_results(results: pd.DataFrame, n: int = 6) -> None:
    if results.empty:
        print("No regression results.")
        return
    for target in ["nu_norm", "a"]:
        sub = results[results["target"] == target].head(n)
        if sub.empty:
            continue
        print(f"\n=== Top models for {target} ===")
        print(
            sub[
                [
                    "feature_set",
                    "n",
                    "n_features",
                    "alpha",
                    "train_r2",
                    "random_cv_r2",
                    "group_cv_r2",
                ]
            ].to_string(index=False)
        )


def dedupe_highest_bootstrap(df: pd.DataFrame) -> pd.DataFrame:
    if not set(PHYSICAL_CONFIG_KEY + ["bootstrap"]).issubset(df.columns):
        return df
    before = len(df)
    out = (
        df.sort_values(["bootstrap"])
        .drop_duplicates(PHYSICAL_CONFIG_KEY, keep="last")
        .reset_index(drop=True)
    )
    removed = before - len(out)
    if removed:
        print(f"Deduped physical configs: removed {removed} lower-bootstrap duplicate rows")
    return out


def apply_mode_defaults(args: argparse.Namespace) -> argparse.Namespace:
    defaults = MODE_DEFAULTS[args.mode]
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    return args


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=sorted(MODE_DEFAULTS), default="smoke")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default=OUT)
    parser.add_argument("--data", default="robust_regression_data.csv")
    parser.add_argument("--results", default="robust_regression_results.csv")
    parser.add_argument("--predictions", default="robust_regression_predictions.csv")

    parser.add_argument("--k-min", type=int)
    parser.add_argument("--k-max", type=int)
    parser.add_argument("--bootstrap", type=int)
    parser.add_argument("--max-pairs-per-k", type=int)
    parser.add_argument("--dirichlet-reps", type=int)
    parser.add_argument("--lambda-targets")
    parser.add_argument("--min-N", type=int, default=10)
    parser.add_argument("--max-N", type=int, default=20_000_000)
    parser.add_argument("--include-rectangular", action="store_true")

    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--fit-only", action="store_true")
    parser.add_argument("--generate-only", action="store_true")
    parser.add_argument(
        "--dedupe-highest-bootstrap",
        action="store_true",
        help="Before fitting, keep only the highest-bootstrap row for each physical config.",
    )
    parser.add_argument("--checkpoint-every", type=int, default=50)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--cv-folds", type=int, default=5)
    parser.add_argument("--no-plot", action="store_true")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = apply_mode_defaults(parser.parse_args())
    os.makedirs(args.out_dir, exist_ok=True)

    data_path = os.path.join(args.out_dir, args.data)
    if args.fit_only:
        df = pd.read_csv(data_path)
        print(f"Loaded existing data: {data_path} ({len(df)} rows)")
    else:
        print(
            f"Stage 9 mode={args.mode}, k={args.k_min}..{args.k_max}, "
            f"K={args.bootstrap}, max_pairs_per_k={args.max_pairs_per_k}"
        )
        df = generate_data(args)

    if args.generate_only:
        return

    if args.dedupe_highest_bootstrap:
        df = dedupe_highest_bootstrap(df)

    results, predictions = fit_regressions(df, args)
    print_top_results(results)
    if not args.no_plot:
        plot_best_predictions(results, predictions, args)


if __name__ == "__main__":
    main()
