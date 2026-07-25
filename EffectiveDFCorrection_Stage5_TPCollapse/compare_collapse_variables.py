"""
Stage 5: Compare collapse variables λ = N·min(π) vs λ_tp = N / Σ(1/π_xy).

Background:
  The Stage 4 multi-marginal test showed residuals cluster systematically by
  marginal shape when fit against λ = N·min(π). Switching to λ_tp = N / Σ(1/π_xy)
  (the inverse of the Treves-Panzeri sum) eliminated the cross-shape bias.

Goal:
  Re-analyse Stage 2 (binary symmetric), Stage 3 (binary asymmetric), Stage 4
  (3×3 symmetric "p,p,1-2p"), and Stage 4 multi-marginal data using λ_tp instead.
  Check whether:
    (a) A coefficients align across datasets (suggesting one universal rule),
    (b) The fit quality on each dataset stays comparable.

Theoretical anchor:
  Treves-Panzeri bias:  E[T] - ν₀ ≈ (1/(6N)) · Σ 1/π_xy = 1/(6 · λ_tp).
  So 1/(6 λ_tp) is the canonical bias scale across any (k×k, shape).
"""

import os
import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.cm as cm

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT   = os.path.dirname(os.path.abspath(__file__))

LAM_LO, LAM_HI = 0.5, 5.0


# ── λ_tp computation ──────────────────────────────────────────────────────────

def lam_tp_from_marginals(p_X_vec, p_Y_vec, N):
    pi = np.outer(p_X_vec, p_Y_vec)
    return N / (1.0 / pi).sum()


def add_lam_tp_binary(df, col_pX, col_pY):
    return df.assign(lam_tp=df.apply(
        lambda r: lam_tp_from_marginals(
            np.array([1 - r[col_pX], r[col_pX]]),
            np.array([1 - r[col_pY], r[col_pY]]),
            r["N"]
        ), axis=1
    ))


# Stage 4 multi-marginal shape → marginal vector
SHAPE_TO_MARG = {
    "uniform (1/3,1/3,1/3)":    np.array([1/3, 1/3, 1/3]),
    "bimodal (.45,.10,.45)":    np.array([0.45, 0.10, 0.45]),
    "rare-rare (.10,.10,.80)":  np.array([0.10, 0.10, 0.80]),
    "rare-rare (.05,.05,.90)":  np.array([0.05, 0.05, 0.90]),
    "asymmetric (.05,.25,.70)": np.array([0.05, 0.25, 0.70]),
    "one-rare (.05,.475,.475)": np.array([0.05, 0.475, 0.475]),
}


# ── Models ────────────────────────────────────────────────────────────────────

def m1(L, A):           return 1 + A / L
def m2(L, A, gamma):    return 1 + A / L**gamma

def fit_and_r2(func, p0, x, y):
    popt, _ = optimize.curve_fit(func, x, y, p0=p0, maxfev=10000)
    yhat = func(x, *popt)
    ss_res = np.sum((y - yhat)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return popt, r2


# ── Load all datasets ─────────────────────────────────────────────────────────

def load_all():
    # Stage 2: binary symmetric
    df2 = pd.read_csv(os.path.join(ROOT, "EffectiveDFCorrection_Stage2",
                                   "nu_a_data.csv"))
    df2 = add_lam_tp_binary(df2.rename(columns={"p": "p_X"})
                                .assign(p_Y=lambda d: d["p_X"]),
                            "p_X", "p_Y")
    df2["nu_norm"] = df2["nu"]                     # ν₀ = 1 for 2×2
    df2["dataset"] = "Stage 2 (2×2 symmetric)"

    # Stage 3: binary asymmetric
    df3 = pd.read_csv(os.path.join(ROOT, "EffectiveDFCorrection_Stage3",
                                   "nu_a_data_asym.csv"))
    df3 = add_lam_tp_binary(df3, "p_X", "p_Y")
    df3["nu_norm"] = df3["nu"]
    df3["dataset"] = "Stage 3 (2×2 asymmetric)"

    # Stage 4: 3×3 symmetric (p, p, 1-2p)
    df4 = pd.read_csv(os.path.join(ROOT, "EffectiveDFCorrection_Stage4",
                                   "nu_a_data_3x3.csv"))
    df4["lam_tp"] = df4.apply(
        lambda r: lam_tp_from_marginals(
            np.array([r["p0"], r["p1"], r["p2"]]),
            np.array([r["p0"], r["p1"], r["p2"]]),
            r["N"]
        ), axis=1
    )
    df4["dataset"] = "Stage 4 (3×3, p,p,1-2p)"

    # Stage 4 multi-marginal
    df4mm = pd.read_csv(os.path.join(ROOT, "EffectiveDFCorrection_Stage4",
                                     "multi_marginal_data.csv"))
    df4mm["lam_tp"] = df4mm.apply(
        lambda r: lam_tp_from_marginals(
            SHAPE_TO_MARG[r["shape"]], SHAPE_TO_MARG[r["shape"]], r["N"]
        ), axis=1
    )
    df4mm["dataset"] = "Stage 4 multi-marginal"

    return df2, df3, df4, df4mm


# ── Compare fits ──────────────────────────────────────────────────────────────

def compare_fits(df, label):
    """
    Fit M1 on the SAME points (selected by physical regime λ ∈ [0.5, 5]) against
    both x = λ and x = λ_tp. This isolates the question 'which variable explains
    the data better?' from 'which range of points are we using?'.
    """
    m = (df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)
    if m.sum() < 5:
        print(f"\n--- {label} --- too few points ({m.sum()}) in λ ∈ [{LAM_LO}, {LAM_HI}]")
        return []
    sub = df.loc[m]

    print(f"\n--- {label} (selecting {m.sum()} points with λ ∈ [{LAM_LO}, {LAM_HI}]) ---")
    print(f"{'collapse var':<22} {'A_ν':>8} {'R²(ν)':>7} {'A_a':>8} {'R²(a)':>7}")
    rows = []
    for x_col, x_label in [("lam", "λ = N·min(π)"),
                           ("lam_tp", "λ_tp = N/Σ(1/π)")]:
        popt_nu, r2_nu = fit_and_r2(m1, [0.3], sub[x_col], sub["nu_norm"])
        popt_a,  r2_a  = fit_and_r2(m1, [-0.2], sub[x_col], sub["a"])
        print(f"{x_label:<22} {popt_nu[0]:>+8.4f} {r2_nu:>7.4f} {popt_a[0]:>+8.4f} {r2_a:>7.4f}")
        rows.append((x_label, popt_nu[0], r2_nu, popt_a[0], r2_a))
    return rows


# ── Pool everything ───────────────────────────────────────────────────────────

def pool_fit(dfs, label):
    pooled = pd.concat(dfs, ignore_index=True)
    m = (pooled["lam"] >= LAM_LO) & (pooled["lam"] <= LAM_HI)
    sub = pooled.loc[m]
    print(f"\n=== Pooled fit across {label} ({len(sub)} points with λ ∈ [{LAM_LO}, {LAM_HI}]) ===")
    print(f"{'collapse var':<22} {'A_ν':>8} {'R²(ν)':>7} {'A_a':>8} {'R²(a)':>7}")
    for x_col, x_label in [("lam", "λ = N·min(π)"),
                           ("lam_tp", "λ_tp = N/Σ(1/π)")]:
        popt_nu, r2_nu = fit_and_r2(m1, [0.3], sub[x_col], sub["nu_norm"])
        popt_a,  r2_a  = fit_and_r2(m1, [-0.2], sub[x_col], sub["a"])
        print(f"{x_label:<22} {popt_nu[0]:>+8.4f} {r2_nu:>7.4f} {popt_a[0]:>+8.4f} {r2_a:>7.4f}")
    return pooled


# ── Plot ──────────────────────────────────────────────────────────────────────

def plot_comparison(dfs):
    """Two-panel figure: ν_norm vs λ (left) and vs λ_tp (right), colored by dataset."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    labels = [d["dataset"].iloc[0] for d in dfs]

    for row_idx, (target, ylabel) in enumerate([
        ("nu_norm", r"$\nu_{eff}/\nu_0$"),
        ("a",       r"scale $a$"),
    ]):
        for col_idx, (x_col, x_label) in enumerate([
            ("lam",    r"$\lambda = N \cdot \min(\pi)$"),
            ("lam_tp", r"$\lambda_{tp} = N / \sum 1/\pi_{xy}$"),
        ]):
            ax = axes[row_idx][col_idx]
            for df, col, lab in zip(dfs, colors, labels):
                ax.scatter(df[x_col], df[target], color=col, s=18,
                           alpha=0.55, label=lab, edgecolors="none")

            # Overlay M1 pooled fit in the fitting region
            pooled = pd.concat(dfs, ignore_index=True)
            m = (pooled[x_col] >= LAM_LO) & (pooled[x_col] <= LAM_HI)
            p0 = [0.3] if target == "nu_norm" else [-0.2]
            popt, r2 = fit_and_r2(m1, p0, pooled.loc[m, x_col], pooled.loc[m, target])
            x_curve = np.logspace(np.log10(LAM_LO * 0.9), np.log10(LAM_HI * 1.1), 200)
            ax.plot(x_curve, m1(x_curve, *popt),
                    color="black", linewidth=2.0, linestyle="--",
                    label=f"pooled M1: A={popt[0]:+.3f}, R²={r2:.3f}")

            ax.axhline(1.0, color="green", linestyle="--", linewidth=0.8, alpha=0.5)
            ax.axvspan(LAM_LO, LAM_HI, alpha=0.08, color="grey")
            ax.set_xscale("log")
            ax.set_xlim(0.05, 60)
            ax.set_xlabel(x_label, fontsize=11)
            ax.set_ylabel(ylabel, fontsize=11)
            ax.grid(True, alpha=0.2, linestyle="--")
            if row_idx == 0 and col_idx == 1:
                ax.legend(fontsize=7.5, loc="upper right")

            ax.set_title(f"{ylabel} vs {x_label}", fontsize=10)

    fig.suptitle(
        r"Stage 5: collapse variable comparison — $\lambda$ (left) vs $\lambda_{tp}$ (right)"
        "\nFour datasets pooled. If $\\lambda_{tp}$ is the right variable, the right column"
        " collapses better than the left.",
        fontsize=12, y=1.00
    )
    plt.tight_layout()
    out = os.path.join(OUT, "collapse_comparison.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {out}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    df2, df3, df4, df4mm = load_all()

    compare_fits(df2,  "Stage 2 (2×2 symmetric)")
    compare_fits(df3,  "Stage 3 (2×2 asymmetric)")
    compare_fits(df4,  "Stage 4 (3×3 p,p,1-2p)")
    compare_fits(df4mm,"Stage 4 multi-marginal (3×3 varied shapes)")

    pool_fit([df2, df3, df4, df4mm], "all 4 datasets")
    pool_fit([df2, df3],             "binary only")
    pool_fit([df4, df4mm],           "3×3 only")

    plot_comparison([df2, df3, df4, df4mm])


if __name__ == "__main__":
    main()
