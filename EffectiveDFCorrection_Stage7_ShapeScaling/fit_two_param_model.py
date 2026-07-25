"""
Stage 7b: build a formula A_ν = f(k, skew_descriptor) using the Stage 7 data.

We have ~30 (k, shape) points across uniform, mild_skew, strong_skew, k ∈ [2, 12].
The Stage 7 fits gave A_ν per (k, shape). Now we fit a 2-parameter model to
those A_ν values jointly, with several candidate skew descriptors:

  H        = marginal entropy of p (bits)
  H_norm   = H / log₂(k)            (1 for uniform, < 1 for skewed)
  perp     = 2^H = perplexity        (effective alphabet size)
  perp_n   = perp / k                (1 for uniform, < 1 for skewed)
  simpson  = 1 / Σ p_i²              (Simpson effective alphabet)
  simpson_n = simpson / k            (1 for uniform, < 1 for skewed)
  k_min_p  = k · min(p)              (1 for uniform, < 1 for skewed)

Models tried for each descriptor d:
  M_add:   A = c1·log(k) + c2·d
  M_mul:   A = c·log(k)·d
  M_pow:   A = c·log(k)·d^α          (3-param)
  M_logd:  A = c·log(d)
  M_d_alone: A = c·d

Plus a few standalone forms:
  A = c·H                            ("entropy-alone")
  A = c·log(perp)                    ("perplexity-alone")

Best model = highest R² across all (k, shape) points (excluding k=2 if needed,
since Stage 7 noted k=2 was unreliable).
"""

import os
import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))


def make_marginal(k, shape):
    if shape == "uniform":
        return np.ones(k) / k
    if shape == "mild_skew":
        p_rare = 1 / (2 * k)
        return np.concatenate([[p_rare], np.full(k - 1, (1 - p_rare) / (k - 1))])
    if shape == "strong_skew":
        p_rare = 1 / (5 * k)
        return np.concatenate([[p_rare], np.full(k - 1, (1 - p_rare) / (k - 1))])
    raise ValueError(shape)


def descriptors(k, shape):
    p = make_marginal(k, shape)
    p_pos = p[p > 0]
    H = float(-np.sum(p_pos * np.log2(p_pos)))
    perp = 2.0 ** H
    simpson = 1.0 / float(np.sum(p ** 2))
    return dict(
        H=H,
        H_norm=H / np.log2(k) if k > 1 else 1.0,
        perp=perp,
        perp_n=perp / k,
        simpson=simpson,
        simpson_n=simpson / k,
        k_min_p=k * p.min(),
    )


def r2(y, yhat):
    return 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)


# ── Models ────────────────────────────────────────────────────────────────────

def f_add(X, c1, c2):
    kv, dv = X
    return c1 * np.log(kv) + c2 * dv

def f_mul(X, c):
    kv, dv = X
    return c * np.log(kv) * dv

def f_pow(X, c, a):
    kv, dv = X
    return c * np.log(kv) * dv ** a

def f_log_d(d, c):
    return c * np.log(d)

def f_d_alone(d, c):
    return c * d


def fit_one(model_func, X, A, p0):
    try:
        popt, _ = optimize.curve_fit(model_func, X, A, p0=p0, maxfev=20000)
        r = r2(A, model_func(X, *popt))
        return popt, r
    except Exception as e:
        return None, np.nan


# ── Main analysis ────────────────────────────────────────────────────────────

def main():
    fits = pd.read_csv(os.path.join(OUT, "shape_scaling_fits.csv"))
    # Compute all descriptors
    for c in ["H", "H_norm", "perp", "perp_n", "simpson", "simpson_n", "k_min_p"]:
        fits[c] = fits.apply(lambda r: descriptors(int(r["k"]), r["shape"])[c], axis=1)

    # Drop k=2 — Stage 7 noted small-n unreliability
    df = fits[fits["k"] >= 3].copy()
    print(f"Fitting on {len(df)} (k, shape) points with k ≥ 3\n")

    k = df["k"].values.astype(float)
    A = df["A_nu"].values

    print(f"{'descriptor':<10} {'model':<20} {'params':<35} {'R²':>8}")
    print("-" * 80)

    # 1-D baseline: A = c · log(k)  (Stage 6 reference)
    popt, r = fit_one(lambda kv, c: c * np.log(kv), k, A, [0.3])
    print(f"{'-':<10} {'c · log(k)':<20} {str([f'{v:+.4f}' for v in popt]):<35} {r:>8.4f}")

    # 1-D: A = c · H
    popt, r = fit_one(f_d_alone, df["H"].values, A, [0.1])
    print(f"{'H':<10} {'c · H':<20} {str([f'{v:+.4f}' for v in popt]):<35} {r:>8.4f}")
    popt, r = fit_one(f_log_d, df["H"].values, A, [0.1])
    print(f"{'H':<10} {'c · log(H)':<20} {str([f'{v:+.4f}' for v in popt]):<35} {r:>8.4f}")

    print()
    # 2-D models for each descriptor
    for desc in ["H", "H_norm", "perp", "perp_n", "simpson", "simpson_n", "k_min_p"]:
        d = df[desc].values
        X = (k, d)
        popt_a, r_a = fit_one(f_add, X, A, [0.3, 0.0])
        popt_m, r_m = fit_one(f_mul, X, A, [0.3])
        popt_p, r_p = fit_one(f_pow, X, A, [0.3, 1.0])
        print(f"{desc:<10} {'add: c1·log(k)+c2·d':<20} "
              f"{str([f'{v:+.4f}' for v in popt_a]):<35} {r_a:>8.4f}")
        print(f"{desc:<10} {'mul: c·log(k)·d':<20} "
              f"{str([f'{v:+.4f}' for v in popt_m]):<35} {r_m:>8.4f}")
        print(f"{desc:<10} {'pow: c·log(k)·d^α':<20} "
              f"{str([f'{v:+.4f}' for v in popt_p]):<35} {r_p:>8.4f}")
        print()

    # ── Pick the best 2-param model and plot
    print("\n=== Selecting best 2-param model ===")
    best_r, best = -np.inf, None
    for desc in ["H", "H_norm", "perp", "perp_n", "simpson", "simpson_n", "k_min_p"]:
        d = df[desc].values
        for name, func, p0 in [("add", f_add, [0.3, 0.0]),
                                ("mul", f_mul, [0.3])]:
            popt, r_val = fit_one(func, (k, d), A, p0)
            if r_val > best_r:
                best_r, best = r_val, (desc, name, func, popt)
    desc, name, func, popt = best
    print(f"Best 2-param: descriptor={desc}, model={name}, "
          f"params={[f'{v:+.4f}' for v in popt]}, R²={best_r:.4f}")

    # Visualise the fit
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    shape_colors = {"uniform": "#1f77b4", "mild_skew": "#ff7f0e", "strong_skew": "#d62728"}

    # Left: predicted vs observed
    pred = func((k, df[desc].values), *popt)
    ax = axes[0]
    for shape, col in shape_colors.items():
        m = df["shape"] == shape
        ax.scatter(A[m], pred[m], color=col, s=80, label=shape,
                   edgecolors="k", linewidths=0.5)
    lims = [min(A.min(), pred.min()), max(A.max(), pred.max())]
    ax.plot(lims, lims, "k--", linewidth=1, alpha=0.5)
    ax.set_xlabel("observed $A_\\nu$")
    ax.set_ylabel("predicted $A_\\nu$")
    ax.set_title(f"Best fit: {desc}, {name}\nR² = {best_r:.4f}")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=9)

    # Right: heatmap of model surface over (k, descriptor)
    ax = axes[1]
    k_grid = np.linspace(3, 12, 50)
    d_grid = np.linspace(df[desc].min(), df[desc].max(), 50)
    KK, DD = np.meshgrid(k_grid, d_grid)
    ZZ = func((KK, DD), *popt)
    cs = ax.contourf(KK, DD, ZZ, levels=20, cmap="viridis")
    plt.colorbar(cs, ax=ax, label="$A_\\nu$ predicted")
    for shape, col in shape_colors.items():
        m = df["shape"] == shape
        ax.scatter(df.loc[m, "k"], df.loc[m, desc], color=col, s=100,
                   edgecolors="white", linewidths=1.5, label=shape, zorder=5)
    ax.set_xlabel("k")
    ax.set_ylabel(desc)
    ax.set_title(f"Model surface")
    ax.legend(fontsize=9, loc="best")

    fig.suptitle(f"Best 2-parameter model for $A_\\nu(k, {desc})$", fontsize=12)
    plt.tight_layout()
    out = os.path.join(OUT, "two_param_fit.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
