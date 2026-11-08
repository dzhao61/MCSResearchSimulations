"""
Zero-inflated mixture null for discrete mutual information significance testing.

Model
-----
Under H₀ with binary marginals p, the rarest cell count n₁₁ ~ Poisson(λ),
λ = N·p².  The null distribution of T = 2N·I is a mixture:

    T ~ e^{-λ} · D₀  +  (1 - e^{-λ}) · D₁

where D₀ (n₁₁=0) is a near-zero spike and D₁ (n₁₁≥1) is chi²-like.

For significance testing only D₁ matters in the rejection region, giving:

    P(T > t | H₀)  ≈  (1 - e^{-λ}) · P( a_c·χ²(ν_c) > t )

Both the mixing weight (e^{-λ}) and the conditional parameters (ν_c, a_c) are
derived analytically from λ = N·p² estimated from the observed marginals.

This script:
  1. Generates the bootstrap null via JIDT (same method as baseline)
  2. Splits surrogates into D₀ (n₁₁=0) and D₁ (n₁₁≥1) components
  3. Fits ν_c(λ) and a_c(λ) from the conditional D₁ distribution
  4. Plots CDFs comparing:
       - Bootstrap ground truth (red)
       - Standard χ²(1) (green)
       - Moment-matched unconditional (orange, from Stage 1)
       - Zero-inflated model (purple)
  5. Plots the conditional ν_c and a_c vs λ to confirm they are well-behaved
"""

import os
import numpy as np
from scipy import stats, optimize
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

from jpype import startJVM, getDefaultJVMPath, JPackage, JArray, JInt, isJVMStarted

JIDT_JAR = os.environ.get(
    "JIDT_JAR",
    "/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/jidt/infodynamics.jar",
)
if not os.path.exists(JIDT_JAR):
    raise FileNotFoundError(f"JIDT jar not found at {JIDT_JAR}.")
if not isJVMStarted():
    startJVM(getDefaultJVMPath(), "-ea", f"-Djava.class.path={JIDT_JAR}")

MICalcDiscrete = JPackage("infodynamics.measures.discrete").MutualInformationCalculatorDiscrete


# ── Bootstrap null — returns (MI in bits, n₁₁ count) for each surrogate ───────

def bootstrap_null_with_counts(bias, N, repeats, rng):
    """
    Same fresh-draw method as baseline, but also records n₁₁ per surrogate
    so we can split into D₀ / D₁ components.
    Returns:
        mis_bits : (repeats,) float  — MI in bits
        n11      : (repeats,) int    — count of (X=1, Y=1) observations
    """
    calc = MICalcDiscrete(2)
    mis_bits = np.empty(repeats)
    n11      = np.empty(repeats, dtype=int)
    for s in range(repeats):
        x = (rng.random(N) < bias).astype(int)
        y = (rng.random(N) < bias).astype(int)
        n11[s] = int(np.sum((x == 1) & (y == 1)))
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mis_bits[s] = float(calc.computeAverageLocalOfObservations())
    return mis_bits, n11


# ── Moment matching (same as Stage 1) ────────────────────────────────────────

def fit_scaled_chi2(mis_bits, N):
    """Unconditional moment-matched ν and a (Stage 1 method, for comparison)."""
    T      = 2 * N * mis_bits * np.log(2)
    mu     = float(np.mean(T))
    sigma2 = float(np.var(T, ddof=1))
    nu     = 2 * mu**2 / sigma2
    a      = sigma2 / (2 * mu)
    return nu, a


def fit_scaled_chi2_conditional(mis_bits_d1, N):
    """Moment-matched ν_c and a_c from the D₁ (n₁₁≥1) conditional samples."""
    if len(mis_bits_d1) < 30:
        return np.nan, np.nan
    T      = 2 * N * mis_bits_d1 * np.log(2)
    mu     = float(np.mean(T))
    sigma2 = float(np.var(T, ddof=1))
    if sigma2 <= 0 or mu <= 0:
        return np.nan, np.nan
    nu = 2 * mu**2 / sigma2
    a  = sigma2 / (2 * mu)
    return nu, a


# ── Zero-inflated CDF ─────────────────────────────────────────────────────────

def zi_cdf(x_bits, N, lam, nu_c, a_c):
    """
    P(T ≤ t) under the zero-inflated model.
    x_bits : x-axis values in MI bits
    lam    : λ = N·p²
    nu_c, a_c : conditional chi² parameters
    """
    w  = 1 - np.exp(-lam)           # P(n₁₁ ≥ 1)
    t  = 2 * N * x_bits * np.log(2) # convert to chi² statistic
    # D₀ component: treated as a point mass at 0 (contributes e^{-λ} to CDF)
    # D₁ component: a_c · χ²(ν_c)
    cdf_d1 = stats.chi2.cdf(t / a_c, df=nu_c)
    # Overall CDF: e^{-λ} (mass at 0) + (1-e^{-λ}) · CDF_D1
    return np.exp(-lam) + w * cdf_d1


# ── Empirical CDF helper (JIDT/Octave method) ─────────────────────────────────

def empirical_cdf(mis_bits, n_bins=100):
    """histogram → normalise → cumsum at bin centres."""
    counts, edges = np.histogram(mis_bits, bins=n_bins)
    pdfX = (edges[:-1] + edges[1:]) / 2
    cdfY = np.cumsum(counts / len(mis_bits))
    return pdfX, cdfY


# ── Main CDF comparison plot ──────────────────────────────────────────────────

def plot_cdf_comparison(configs, data):
    n_cols = 4
    n_rows = (len(configs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.5 * n_cols, 4.5 * n_rows), squeeze=False)

    for i, cfg in enumerate(configs):
        ax  = axes[i // n_cols][i % n_cols]
        lbl = cfg["label"]
        N   = cfg["N"]
        p   = cfg["p"]
        lam = N * p**2

        mis_bits = data[lbl]["mis_bits"]
        n11      = data[lbl]["n11"]
        nu_c     = data[lbl]["nu_c"]
        a_c      = data[lbl]["a_c"]
        nu_unc   = data[lbl]["nu_unc"]
        a_unc    = data[lbl]["a_unc"]

        pdfX, cdfY = empirical_cdf(mis_bits)
        stat = 2 * N * pdfX * np.log(2)

        # Bootstrap ground truth
        ax.plot(pdfX, cdfY, color="red", linewidth=2.5,
                label="Bootstrap null", zorder=4)

        # Standard χ²(1)
        ax.plot(pdfX, stats.chi2.cdf(stat, df=1),
                color="green", linewidth=2.0,
                label=r"$\chi^2(1)$ standard", zorder=3)

        # Unconditional moment-matched (Stage 1)
        if not (np.isnan(nu_unc) or np.isnan(a_unc)):
            ax.plot(pdfX, stats.chi2.cdf(stat / a_unc, df=nu_unc),
                    color="darkorange", linewidth=2.0, linestyle="--",
                    label=fr"Uncond. $a\cdot\chi^2(\nu)$  ν={nu_unc:.2f}", zorder=4)

        # Zero-inflated model
        if not (np.isnan(nu_c) or np.isnan(a_c)):
            ax.plot(pdfX, zi_cdf(pdfX, N, lam, nu_c, a_c),
                    color="purple", linewidth=2.0, linestyle="-.",
                    label=fr"ZI model  ν_c={nu_c:.2f}, a_c={a_c:.2f}", zorder=5)

        # α = 0.05 line
        ax.axhline(0.95, color="blue", linewidth=1.2, alpha=0.6, label="α=0.05")

        # Annotate mixing weight
        w = 1 - np.exp(-lam)
        ax.text(0.03, 0.97, f"λ={lam:.2f}\nw={w:.3f}", transform=ax.transAxes,
                fontsize=8, va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

        ax.set_xlim(0, pdfX.max())
        ax.set_ylim(0, 1.02)
        ax.set_title(lbl, fontsize=11, fontweight="bold")
        ax.set_xlabel("MI (bits)", fontsize=10)
        ax.set_ylabel("CDF", fontsize=10)
        ax.grid(True, alpha=0.20, linestyle="--")
        if i == 0:
            ax.legend(fontsize=7, loc="lower right", framealpha=0.9)

    for j in range(len(configs), n_rows * n_cols):
        axes[j // n_cols][j % n_cols].set_visible(False)

    fig.suptitle(
        "CDF comparison: bootstrap vs χ²(1) vs unconditional moment-match vs zero-inflated model\n"
        "Purple = ZI model  |  Red = ground truth  |  Blue line = α=0.05",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.savefig("zi_cdf_comparison.png", dpi=150, bbox_inches="tight")
    print("Saved: zi_cdf_comparison.png")
    plt.show()


# ── Conditional ν_c and a_c vs λ ──────────────────────────────────────────────

def plot_conditional_params(p_values, N_values, repeats, rng):
    """
    Show ν_c and a_c from the D₁ conditional distribution vs λ.
    These should be much smoother and more monotone than the unconditional ones.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    colors = cm.viridis(np.linspace(0.1, 0.9, len(p_values)))

    rows = []
    for p, col in zip(p_values, colors):
        lams, nus_c, a_cs, nus_u, a_us, ws = [], [], [], [], [], []
        for N in N_values:
            lam = N * p**2
            mis_bits, n11 = bootstrap_null_with_counts(p, N, repeats, rng)

            # Split into D₀ / D₁
            mask_d1    = n11 >= 1
            mis_bits_d1 = mis_bits[mask_d1]
            w_emp      = mask_d1.mean()   # empirical P(n₁₁ ≥ 1)
            w_theory   = 1 - np.exp(-lam)

            nu_c, a_c   = fit_scaled_chi2_conditional(mis_bits_d1, N)
            nu_u, a_u   = fit_scaled_chi2(mis_bits, N)

            lams.append(lam);  nus_c.append(nu_c);  a_cs.append(a_c)
            nus_u.append(nu_u); a_us.append(a_u);   ws.append(w_emp)
            rows.append(dict(p=p, N=N, lam=lam, nu_c=nu_c, a_c=a_c,
                             nu_u=nu_u, a_u=a_u,
                             w_emp=w_emp, w_theory=w_theory))
            print(f"  p={p}, N={N:4d}  λ={lam:.3f}  "
                  f"w={w_emp:.3f}(emp)/{w_theory:.3f}(theory)  "
                  f"ν_c={nu_c:.3f}  a_c={a_c:.3f}  "
                  f"ν_u={nu_u:.3f}  a_u={a_u:.3f}", flush=True)

        # Conditional (solid)
        ax1.plot(lams, nus_c, color=col, linewidth=2.0, marker="o",
                 markersize=5, label=f"p={p} (cond.)")
        ax2.plot(lams, a_cs,  color=col, linewidth=2.0, marker="o",
                 markersize=5, label=f"p={p} (cond.)")
        # Unconditional (dashed, same colour)
        ax1.plot(lams, nus_u, color=col, linewidth=1.2, marker="s",
                 markersize=4, linestyle="--", alpha=0.5)
        ax2.plot(lams, a_us,  color=col, linewidth=1.2, marker="s",
                 markersize=4, linestyle="--", alpha=0.5)

    for ax, ylabel, title in [
        (ax1, r"$\nu_c$",           r"Conditional $\nu_c$ vs $\lambda$"),
        (ax2, "Conditional $a_c$",  r"Conditional $a_c$ vs $\lambda$"),
    ]:
        ax.axhline(1.0, color="green", linestyle="--", linewidth=1.5,
                   label="χ²(1) nominal")
        ax.set_xscale("log")
        ax.set_xlabel(r"$\lambda = N \cdot p^2$", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, alpha=0.25, linestyle="--")

    fig.suptitle(
        r"Conditional ($n_{11} \geq 1$) parameters vs $\lambda$  —  "
        "solid = conditional, dashed = unconditional\n"
        r"Conditional curves should be smoother and monotone",
        fontsize=12
    )
    plt.tight_layout()
    plt.savefig("conditional_params_vs_lambda.png", dpi=150, bbox_inches="tight")
    print("Saved: conditional_params_vs_lambda.png")

    df = pd.DataFrame(rows)
    df.to_csv("conditional_params.csv", index=False)
    print("Saved: conditional_params.csv")
    plt.show()
    return df


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)

    configs = [
        dict(p=0.50, N=1000, label="p=0.50, N=1000"),
        dict(p=0.50, N=200,  label="p=0.50, N=200"),
        dict(p=0.50, N=50,   label="p=0.50, N=50"),
        dict(p=0.50, N=20,   label="p=0.50, N=20"),
        dict(p=0.10, N=500,  label="p=0.10, N=500"),
        dict(p=0.10, N=100,  label="p=0.10, N=100"),
        dict(p=0.10, N=50,   label="p=0.10, N=50"),
        dict(p=0.05, N=200,  label="p=0.05, N=200"),
        dict(p=0.05, N=100,  label="p=0.05, N=100"),
        dict(p=0.05, N=50,   label="p=0.05, N=50"),
        dict(p=0.05, N=20,   label="p=0.05, N=20"),
        dict(p=0.01, N=500,  label="p=0.01, N=500"),
    ]

    repeats = 10_000

    # ── Generate bootstrap nulls + n₁₁ counts
    print("Generating bootstrap nulls with cell counts...")
    data = {}
    for cfg in configs:
        p, N, lbl = cfg["p"], cfg["N"], cfg["label"]
        lam = N * p**2
        print(f"  {lbl}...", flush=True)
        mis_bits, n11 = bootstrap_null_with_counts(p, N, repeats, rng)

        mask_d1 = n11 >= 1
        w_emp   = mask_d1.mean()

        nu_c, a_c = fit_scaled_chi2_conditional(mis_bits[mask_d1], N)
        nu_u, a_u = fit_scaled_chi2(mis_bits, N)

        print(f"    λ={lam:.3f}  w={w_emp:.3f}  "
              f"ν_c={nu_c:.3f}  a_c={a_c:.3f}  "
              f"ν_u={nu_u:.3f}  a_u={a_u:.3f}")

        data[lbl] = dict(mis_bits=mis_bits, n11=n11,
                         nu_c=nu_c, a_c=a_c,
                         nu_unc=nu_u, a_unc=a_u)

    # ── CDF comparison
    print("\nPlotting CDF comparison...")
    plot_cdf_comparison(configs, data)

    # ── Conditional params vs λ
    print("\nPlotting conditional parameters vs λ...")
    plot_conditional_params(
        p_values=[0.5, 0.3, 0.1, 0.05, 0.02, 0.01],
        N_values=[10, 20, 50, 100, 200, 500, 1000],
        repeats=5_000,
        rng=rng,
    )


if __name__ == "__main__":
    main()
