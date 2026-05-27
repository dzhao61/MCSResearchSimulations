"""
Stage 4 follow-up: does the collapse onto λ = N·min(p_X)·min(p_Y) survive
when MANY cells of the 3×3 table are sparse, not just the rarest one?

The Stage 4 grid used (p, p, 1-2p), which produces 4 rare cells (corners) and
5 well-populated cells. Here we sweep marginal shapes that vary the *number*
of rare cells (n_rare = # cells with expected count < 5), holding everything
else as analogous as possible:

  uniform     (1/3, 1/3, 1/3)    : all 9 cells equal — most cells sparse
  bimodal     (0.45, 0.10, 0.45) : middle state rare → 5 rare cells
  rare-rare   (0.1, 0.1, 0.8)    : Stage 4 pattern — 4 rare cells
  asymmetric  (0.05, 0.25, 0.7)  : single very-rare state — 3 rare cells
  one-rare    (0.05, 0.475, 0.475): one very-rare state — 5 cells of mid count

Test: plot ν_eff/ν₀ and a vs λ, coloured by marginal type. If curves overlay,
then "single λ" is sufficient. If they separate, then n_rare (or some other
sparsity descriptor) matters and the Stage 4 universal rule breaks.
"""

import os
import numpy as np
from scipy import optimize, stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

from model_nu_a_3x3 import (
    bootstrap_moments, NU0, K_ALPHABET, LAM_LO, LAM_HI, MODELS, fit_model
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
RNG_SEED = 42
K = 3_000

# ── Marginal shapes to test (p_X = p_Y for symmetry) ──────────────────────────

MARGINAL_SHAPES = {
    "uniform (1/3,1/3,1/3)":    np.array([1/3, 1/3, 1/3]),
    "bimodal (.45,.10,.45)":    np.array([0.45, 0.10, 0.45]),
    "rare-rare (.10,.10,.80)":  np.array([0.10, 0.10, 0.80]),
    "rare-rare (.05,.05,.90)":  np.array([0.05, 0.05, 0.90]),
    "asymmetric (.05,.25,.70)": np.array([0.05, 0.25, 0.70]),
    "one-rare (.05,.475,.475)": np.array([0.05, 0.475, 0.475]),
}

N_VALUES = [10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 1500, 3000]


def describe_marginal(p_X, p_Y, N):
    """Return descriptors: lambda (rarest cell), n_rare (cells w/ exp count <5), n_zero (<1)."""
    cell_expected = N * np.outer(p_X, p_Y)
    lam = cell_expected.min()
    n_rare = int((cell_expected < 5).sum())
    n_very_rare = int((cell_expected < 1).sum())
    return lam, n_rare, n_very_rare


def generate_data(rng):
    rows = []
    for label, marg in MARGINAL_SHAPES.items():
        for N in N_VALUES:
            lam, n_rare, n_very_rare = describe_marginal(marg, marg, N)
            if lam < 0.02 or lam > 30:
                continue
            print(f"  {label:<30} N={N:5d}  λ={lam:.3f}  "
                  f"n_rare(<5)={n_rare}  n_very_rare(<1)={n_very_rare}",
                  flush=True)
            mu, sigma2 = bootstrap_moments(marg, marg, N, K, rng)
            nu = 2 * mu**2 / sigma2 if sigma2 > 0 else np.nan
            a  = sigma2 / (2 * mu)  if mu > 0     else np.nan
            rows.append(dict(
                shape=label, N=N, lam=lam,
                n_rare=n_rare, n_very_rare=n_very_rare,
                mu=mu, sigma2=sigma2,
                nu=nu, a=a, nu_norm=nu / NU0
            ))
    return pd.DataFrame(rows)


def plot_overlay(df, fits_nu, fits_a):
    lam_curve = np.logspace(np.log10(0.05), np.log10(30), 300)

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    shape_colors = cm.tab10(np.linspace(0, 1, len(MARGINAL_SHAPES)))
    shape_to_color = dict(zip(MARGINAL_SHAPES.keys(), shape_colors))

    for col_idx, (target, fits, ylabel, title) in enumerate([
        ("nu_norm", fits_nu, r"$\nu_{eff}/\nu_0$",
         r"$\nu_{eff}/\nu_0$ vs $\lambda$ — coloured by marginal shape"),
        ("a",      fits_a,  "Scale factor $a$",
         r"$a$ vs $\lambda$ — coloured by marginal shape"),
    ]):
        ax_data = axes[0][col_idx]
        ax_res  = axes[1][col_idx]

        for shape_label in MARGINAL_SHAPES:
            grp = df[df["shape"] == shape_label]
            ax_data.scatter(grp["lam"], grp[target],
                            color=shape_to_color[shape_label], s=35,
                            zorder=5, label=shape_label, edgecolors="k", linewidths=0.3)

        # Overlay Stage 4 M2 fit as reference
        best_popt, best_r2 = max(fits.values(), key=lambda x: x[1] if x[0] is not None else -1)
        # Use M2 specifically
        m2_popt, m2_r2 = fits["M2: 1 + A/λ^γ"]
        func = MODELS["M2: 1 + A/λ^γ"][0]
        ax_data.plot(lam_curve, func(lam_curve, *m2_popt),
                     color="black", linewidth=2.2, linestyle="--",
                     label=f"M2 pooled fit R²={m2_r2:.3f}")

        ax_data.axhline(1.0, color="green", linestyle="--", linewidth=1.0, alpha=0.6)
        ax_data.axvspan(LAM_LO, LAM_HI, alpha=0.08, color="grey",
                        label="Fitting region [0.5, 5]")
        ax_data.set_xscale("log")
        ax_data.set_ylabel(ylabel, fontsize=11)
        ax_data.set_title(title, fontsize=11)
        ax_data.legend(fontsize=7, loc="upper right")
        ax_data.grid(True, alpha=0.2, linestyle="--")

        # Residuals from pooled M2 fit, coloured by marginal
        df_fit = df[(df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)]
        resid = df_fit[target] - func(df_fit["lam"].values, *m2_popt)
        for shape_label in MARGINAL_SHAPES:
            m = df_fit["shape"] == shape_label
            ax_res.scatter(df_fit.loc[m, "lam"], resid[m],
                           color=shape_to_color[shape_label], s=30, zorder=5,
                           edgecolors="k", linewidths=0.3, label=shape_label)
        ax_res.axhline(0, color="red", linewidth=1.2)
        ax_res.set_xscale("log")
        ax_res.set_xlabel(r"$\lambda = N \cdot \min(p_X) \cdot \min(p_Y)$", fontsize=11)
        ax_res.set_ylabel("Residual from pooled M2", fontsize=11)
        ax_res.set_title(f"Residuals coloured by shape — do they cluster?",
                         fontsize=11)
        ax_res.grid(True, alpha=0.2, linestyle="--")

    fig.suptitle(
        r"Stage 4 follow-up: do different marginal shapes collapse onto same $\lambda$?",
        fontsize=13
    )
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "multi_marginal_test.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


def per_shape_summary(df):
    print("\n=== Mean residual per marginal shape (fitting region only) ===")
    d = df[(df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)]
    func = MODELS["M2: 1 + A/λ^γ"][0]

    # Fit pooled M2 on all shapes
    popt_nu, _ = optimize.curve_fit(func, d["lam"], d["nu_norm"], p0=[0.5, 1.0])
    popt_a,  _ = optimize.curve_fit(func, d["lam"], d["a"],       p0=[-0.2, 1.5])

    print(f"Pooled M2 fit: ν_norm: A={popt_nu[0]:+.4f}, γ={popt_nu[1]:.4f}")
    print(f"                a:      A={popt_a[0]:+.4f}, γ={popt_a[1]:.4f}\n")

    print(f"{'shape':<30} {'n':>3} {'⟨resid ν⟩':>12} {'⟨resid a⟩':>12} "
          f"{'mean n_rare':>12}")
    print("-" * 75)
    for shape_label in MARGINAL_SHAPES:
        m = d["shape"] == shape_label
        if m.sum() == 0:
            continue
        resid_nu = (d.loc[m, "nu_norm"].values
                    - func(d.loc[m, "lam"].values, *popt_nu))
        resid_a  = (d.loc[m, "a"].values
                    - func(d.loc[m, "lam"].values, *popt_a))
        print(f"{shape_label:<30} {m.sum():>3} {resid_nu.mean():>+12.4f} "
              f"{resid_a.mean():>+12.4f} {d.loc[m, 'n_rare'].mean():>12.2f}")

    # Test whether n_rare predicts residual
    log_n_rare = np.log(d["n_rare"].clip(lower=1).values)
    resid_nu = (d["nu_norm"].values - func(d["lam"].values, *popt_nu))
    resid_a  = (d["a"].values       - func(d["lam"].values, *popt_a))
    slope_nu, _, r_nu, p_nu, _ = stats.linregress(log_n_rare, resid_nu)
    slope_a,  _, r_a,  p_a,  _ = stats.linregress(log_n_rare, resid_a)
    print("\nDoes log(n_rare) explain residual variance after the λ-fit?")
    print(f"  ν residuals: slope={slope_nu:+.4f}/decade, R²={r_nu**2:.4f}, p={p_nu:.2e}")
    print(f"  a residuals: slope={slope_a:+.4f}/decade, R²={r_a**2:.4f}, p={p_a:.2e}")


def main():
    rng = np.random.default_rng(RNG_SEED)
    print(f"Bootstrap K={K} samples per config; {len(MARGINAL_SHAPES)} marginal shapes\n")
    df = generate_data(rng)
    df.to_csv("multi_marginal_data.csv", index=False)
    print(f"\nGenerated {len(df)} data points. Saved: multi_marginal_data.csv\n")

    # Fit pooled M1–M4 across all shapes (in fitting region)
    mask = (df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)
    df_fit = df[mask]
    lam_fit = df_fit["lam"].values
    print(f"Fitting on {mask.sum()} pooled points (λ ∈ [{LAM_LO}, {LAM_HI}])")
    fits_nu, fits_a = {}, {}
    for name, (func, p0) in MODELS.items():
        fits_nu[name] = fit_model(func, p0, lam_fit, df_fit["nu_norm"].values)
        fits_a[name]  = fit_model(func, p0, lam_fit, df_fit["a"].values)

    print("\n=== Pooled fit (all shapes together) ===")
    print(f"{'Model':<24}  {'R²(ν/ν₀)':>10}  {'R²(a)':>8}")
    for name in MODELS:
        popt_nu, r2_nu = fits_nu.get(name, (None, np.nan))
        popt_a,  r2_a  = fits_a.get(name,  (None, np.nan))
        print(f"{name:<24}  {r2_nu:>10.5f}  {r2_a:>8.5f}")

    per_shape_summary(df)
    plot_overlay(df, fits_nu, fits_a)


if __name__ == "__main__":
    main()
