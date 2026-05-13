"""
Moment-matched chi-squared correction for the discrete MI null distribution.
Based on effectiveDF.md (Welch-Satterthwaite / moment-matching idea).

Same methodology as ChiSquaredExploration/null_chi2_fit.py:
  - JIDT bootstrap null: fresh independent X, Y drawn per surrogate
  - histogram(mis, 100) → normalise → cumsum → plot at bin centres
  - x-axis: MI in bits; chi^2 CDF evaluated at 2*N*MI*log(2)

Extension: on top of the standard chi^2(1) curve, adds the moment-matched
correction a·chi^2(nu_eff), where:
    nu  = 2*mu^2 / sigma^2      (effective degrees of freedom)
    a   = sigma^2 / (2*mu)      (scale factor)
    mu, sigma^2 estimated from the same bootstrap samples (in nats).

Also produces a diagnostic plot of nu_eff and a vs N for various p values.
"""

import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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


# ── Bootstrap null (identical to null_chi2_fit.py) ────────────────────────────

def bootstrap_null(bias, N, repeats, rng):
    """Fresh independent X, Y per surrogate — returns MI in bits."""
    calc = MICalcDiscrete(2)
    mis = np.empty(repeats)
    for s in range(repeats):
        x = (rng.random(N) < bias).astype(int)
        y = (rng.random(N) < bias).astype(int)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mis[s] = float(calc.computeAverageLocalOfObservations())
    return mis  # bits


# ── Moment matching ───────────────────────────────────────────────────────────

def fit_scaled_chi2(mis_bits, N):
    """
    Estimate nu_eff and scale factor a from bootstrap samples.
    T = 2*N*I_nats = 2*N*MI_bits*log(2)  ~  a * chi^2(nu)
    """
    T = 2 * N * mis_bits * np.log(2)          # convert to chi^2 statistic (nats)
    mu     = float(np.mean(T))
    sigma2 = float(np.var(T, ddof=1))
    nu = 2 * mu**2 / sigma2
    a  = sigma2 / (2 * mu)
    return nu, a


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_cdf(configs, surrogates_dict):
    n_cols = 4
    n_rows = (len(configs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.2 * n_cols, 4.2 * n_rows), squeeze=False)

    for i, cfg in enumerate(configs):
        ax  = axes[i // n_cols][i % n_cols]
        mis = surrogates_dict[cfg["label"]]     # bits
        N   = cfg["N"]

        # ── Histogram → normalise → cumsum  (JIDT/Octave method)
        counts, edges = np.histogram(mis, bins=100)
        pdfX = (edges[:-1] + edges[1:]) / 2
        cdfY = np.cumsum(counts / len(mis))
        stat = 2 * N * pdfX * np.log(2)        # MI bits → chi^2 statistic

        # Bootstrap null (red)
        ax.plot(pdfX, cdfY, color="red", linewidth=2.5,
                label="Bootstrap null", zorder=4)

        # Standard chi^2(1) (green)
        ax.plot(pdfX, stats.chi2.cdf(stat, df=1),
                color="green", linewidth=2.0,
                label=r"$\chi^2(1)$ standard", zorder=5)

        # Moment-matched a·chi^2(nu_eff) (orange dashed)
        nu, a = fit_scaled_chi2(mis, N)
        ax.plot(pdfX, stats.chi2.cdf(stat / a, df=nu),
                color="darkorange", linewidth=2.0, linestyle="--", zorder=5,
                label=fr"$a\cdot\chi^2(\nu_{{eff}})$  ν={nu:.2f}, a={a:.2f}")

        # α = 0.05 line (blue)
        ax.axhline(0.95, color="blue", linewidth=1.2, alpha=0.6, label="α=0.05")

        ax.set_xlim(0, pdfX.max())
        ax.set_ylim(0, 1.02)
        ax.set_title(cfg["label"], fontsize=11, fontweight="bold")
        ax.set_xlabel("MI (bits)", fontsize=10)
        ax.set_ylabel("CDF", fontsize=10)
        ax.grid(True, alpha=0.20, linestyle="--")
        if i == 0:
            ax.legend(fontsize=7.5, loc="lower right", framealpha=0.9)

    for j in range(len(configs), n_rows * n_cols):
        axes[j // n_cols][j % n_cols].set_visible(False)

    fig.suptitle(
        r"CDF: Bootstrap null vs $\chi^2(1)$ vs moment-matched $a\cdot\chi^2(\nu_{eff})$"
        "\nRed = bootstrap | Green = standard χ²(1) | Orange = corrected",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.savefig("effective_df_cdf.png", dpi=150, bbox_inches="tight")
    print("Saved: effective_df_cdf.png")
    plt.show()


def plot_pdf(configs, surrogates_dict):
    n_cols = 4
    n_rows = (len(configs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.2 * n_cols, 4.2 * n_rows), squeeze=False)

    for i, cfg in enumerate(configs):
        ax  = axes[i // n_cols][i % n_cols]
        mis = surrogates_dict[cfg["label"]]
        N   = cfg["N"]

        counts, edges = np.histogram(mis, bins=100)
        pdfX      = (edges[:-1] + edges[1:]) / 2
        bin_width = edges[1] - edges[0]
        pdfY      = counts / len(mis) / bin_width

        stat     = 2 * N * pdfX * np.log(2)
        jacobian = 2 * N * np.log(2)

        ax.plot(pdfX, pdfY, color="red", linewidth=2.5,
                label="Bootstrap null", zorder=4)

        ax.plot(pdfX, stats.chi2.pdf(stat, df=1) * jacobian,
                color="green", linewidth=2.0,
                label=r"$\chi^2(1)$ standard", zorder=5)

        nu, a = fit_scaled_chi2(mis, N)
        ax.plot(pdfX, stats.chi2.pdf(stat / a, df=nu) * jacobian / a,
                color="darkorange", linewidth=2.0, linestyle="--", zorder=5,
                label=fr"$a\cdot\chi^2(\nu_{{eff}})$  ν={nu:.2f}")

        ax.set_xlim(0, pdfX.max())
        ax.set_ylim(0, pdfY.max() * 1.3)
        ax.set_title(cfg["label"], fontsize=11, fontweight="bold")
        ax.set_xlabel("MI (bits)", fontsize=10)
        ax.set_ylabel("density", fontsize=10)
        ax.grid(True, alpha=0.20, linestyle="--")
        if i == 0:
            ax.legend(fontsize=7.5, loc="upper right", framealpha=0.9)

    for j in range(len(configs), n_rows * n_cols):
        axes[j // n_cols][j % n_cols].set_visible(False)

    fig.suptitle(
        r"PDF: Bootstrap null vs $\chi^2(1)$ vs moment-matched $a\cdot\chi^2(\nu_{eff})$",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.savefig("effective_df_pdf.png", dpi=150, bbox_inches="tight")
    print("Saved: effective_df_pdf.png")
    plt.show()


def plot_nu_vs_lambda(p_values, N_values, repeats, rng):
    """
    Plot nu_eff and a against lambda = N*p^2 (minimum expected cell count).
    If all (p, N) combinations collapse onto a single curve, nu and a are
    functions of lambda alone — giving an analytical correction formula.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    colors = cm.viridis(np.linspace(0.1, 0.9, len(p_values)))

    for p, col in zip(p_values, colors):
        lambdas, nus, a_vals = [], [], []
        for N in N_values:
            lam = N * p**2                          # min expected cell count
            mis = bootstrap_null(p, N, repeats, rng)
            nu, a = fit_scaled_chi2(mis, N)
            lambdas.append(lam)
            nus.append(nu)
            a_vals.append(a)
            print(f"  p={p}, N={N}: lambda={lam:.2f}  nu={nu:.3f}  a={a:.3f}")
        ax1.plot(lambdas, nus,    color=col, linewidth=2, marker="o", markersize=5, label=f"p={p}")
        ax2.plot(lambdas, a_vals, color=col, linewidth=2, marker="o", markersize=5, label=f"p={p}")

    for ax, ylabel, title in [
        (ax1, r"$\nu_{eff}$",     r"$\nu_{eff}$ vs $\lambda = N p^2$"),
        (ax2, "Scale factor $a$", r"$a$ vs $\lambda = N p^2$"),
    ]:
        ax.axhline(1.0, color="green", linestyle="--", linewidth=1.5, label="χ²(1) nominal")
        ax.set_xscale("log")
        ax.set_xlabel(r"$\lambda = N \cdot p^2$ (min expected cell count)", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.25, linestyle="--")
        ax.axvline(5, color="grey", linestyle=":", linewidth=1.2, alpha=0.7,
                   label="λ=5 (rule of thumb)")

    fig.suptitle(
        r"If curves collapse: $\nu_{eff}$ and $a$ are functions of $\lambda = Np^2$ alone"
        "\n→ analytical correction without bootstrap",
        fontsize=12
    )
    plt.tight_layout()
    plt.savefig("nu_eff_vs_lambda.png", dpi=150, bbox_inches="tight")
    print("Saved: nu_eff_vs_lambda.png")
    plt.show()



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

    print("Generating bootstrap nulls...")
    surrogates_dict = {}
    for cfg in configs:
        print(f"  {cfg['label']}...", flush=True)
        surrogates_dict[cfg["label"]] = bootstrap_null(cfg["p"], cfg["N"], repeats, rng)

    print("\nPlotting CDFs...")
    plot_cdf(configs, surrogates_dict)

    print("Plotting PDFs...")
    plot_pdf(configs, surrogates_dict)

    print("\nPlotting nu_eff vs lambda diagnostic...")
    plot_nu_vs_lambda(
        p_values=[0.5, 0.3, 0.1, 0.05, 0.02, 0.01],
        N_values=[10, 20, 50, 100, 200, 500, 1000],
        repeats=2_000,
        rng=rng,
    )


if __name__ == "__main__":
    main()
