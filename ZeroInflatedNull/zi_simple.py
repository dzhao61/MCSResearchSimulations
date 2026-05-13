"""
Simplified zero-inflated null for discrete MI significance testing.

Model (no free parameters)
--------------------------
P(T ≤ t | H₀) = e^{-λ} + (1 - e^{-λ}) · χ²_CDF(t, df=1)

where λ = N·p² is computed directly from the observed marginals.

The mixing weight e^{-λ} = P(n₁₁ = 0) is analytically exact under the
Poisson approximation for the rarest cell.  The conditional D₁ component
is approximated as χ²(1) (i.e. ν_c = 1, a_c = 1).

Critical value at level α:
    t_α = χ²_ppf( (1 - α - e^{-λ}) / (1 - e^{-λ}), df=1 )

This script compares:
  1. Bootstrap ground truth      (red)
  2. Standard χ²(1)              (green)
  3. Simplified ZI model         (purple)

and produces a calibration table: actual false-positive rate under each
model when the nominal level is α = 0.05.
"""

import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
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


# ── Bootstrap null ────────────────────────────────────────────────────────────

def bootstrap_null(bias, N, repeats, rng):
    calc = MICalcDiscrete(2)
    mis = np.empty(repeats)
    for s in range(repeats):
        x = (rng.random(N) < bias).astype(int)
        y = (rng.random(N) < bias).astype(int)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mis[s] = float(calc.computeAverageLocalOfObservations())
    return mis


# ── Simplified ZI CDF ─────────────────────────────────────────────────────────

def zi_simple_cdf(x_bits, N, lam):
    """P(T ≤ t) = e^{-λ} + (1-e^{-λ})·χ²_CDF(t, df=1).  No free parameters."""
    t = 2 * N * x_bits * np.log(2)
    return np.exp(-lam) + (1 - np.exp(-lam)) * stats.chi2.cdf(t, df=1)


def zi_simple_critical(alpha, lam):
    """
    Critical value (in chi² statistic) at level alpha under simplified ZI.
    Solves e^{-λ} + (1-e^{-λ})·χ²_CDF(t, 1) = 1 - alpha.
    Returns NaN when the equation has no solution (degenerate regime).
    """
    w = 1 - np.exp(-lam)
    if w <= 0:
        return np.nan
    p_cond = (1 - alpha - np.exp(-lam)) / w   # required conditional quantile
    if p_cond <= 0 or p_cond >= 1:
        return np.nan
    return stats.chi2.ppf(p_cond, df=1)


# ── Empirical false-positive rate ─────────────────────────────────────────────

def empirical_fpr(mis_bits, threshold_bits):
    """Fraction of surrogates exceeding threshold (both in bits)."""
    return float(np.mean(mis_bits > threshold_bits))


# ── CDF comparison plot ───────────────────────────────────────────────────────

def plot_cdf_comparison(configs, data, alpha=0.05):
    n_cols = 4
    n_rows = (len(configs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.5 * n_cols, 4.5 * n_rows), squeeze=False)

    for i, cfg in enumerate(configs):
        ax  = axes[i // n_cols][i % n_cols]
        N, p, lbl = cfg["N"], cfg["p"], cfg["label"]
        lam = N * p**2

        mis = data[lbl]
        counts, edges = np.histogram(mis, bins=100)
        pdfX = (edges[:-1] + edges[1:]) / 2
        cdfY = np.cumsum(counts / len(mis))
        stat = 2 * N * pdfX * np.log(2)

        ax.plot(pdfX, cdfY,
                color="red", linewidth=2.5, label="Bootstrap null", zorder=4)
        ax.plot(pdfX, stats.chi2.cdf(stat, df=1),
                color="green", linewidth=2.0, label=r"$\chi^2(1)$", zorder=3)
        ax.plot(pdfX, zi_simple_cdf(pdfX, N, lam),
                color="purple", linewidth=2.0, linestyle="-.",
                label=fr"ZI-simple  λ={lam:.2f}", zorder=5)

        ax.axhline(1 - alpha, color="blue", linewidth=1.2,
                   alpha=0.6, label=f"α={alpha}")

        w = 1 - np.exp(-lam)
        ax.text(0.03, 0.97, f"λ={lam:.2f}\nw={w:.3f}",
                transform=ax.transAxes, fontsize=8, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

        ax.set_xlim(0, pdfX.max())
        ax.set_ylim(0, 1.02)
        ax.set_title(lbl, fontsize=11, fontweight="bold")
        ax.set_xlabel("MI (bits)", fontsize=10)
        ax.set_ylabel("CDF", fontsize=10)
        ax.grid(True, alpha=0.20, linestyle="--")
        if i == 0:
            ax.legend(fontsize=8, loc="lower right", framealpha=0.9)

    for j in range(len(configs), n_rows * n_cols):
        axes[j // n_cols][j % n_cols].set_visible(False)

    fig.suptitle(
        "Simplified ZI model: e^{-λ}·δ(0) + (1-e^{-λ})·χ²(1)  —  no free parameters\n"
        "Purple = ZI-simple  |  Red = bootstrap ground truth  |  Blue = α=0.05",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.savefig("zi_simple_cdf.png", dpi=150, bbox_inches="tight")
    print("Saved: zi_simple_cdf.png")
    plt.show()


# ── Calibration table ─────────────────────────────────────────────────────────

def calibration_table(configs, data, alpha=0.05):
    """
    For each config, compare:
      - Actual FPR of χ²(1) critical value (should be α if model is correct)
      - Actual FPR of ZI-simple critical value
    A well-calibrated model gives FPR ≈ α.
    """
    rows = []
    for cfg in configs:
        N, p, lbl = cfg["N"], cfg["p"], cfg["label"]
        lam = N * p**2
        mis = data[lbl]

        # Critical values (in bits)
        t_chi2_stat = stats.chi2.ppf(1 - alpha, df=1)
        t_zi_stat   = zi_simple_critical(alpha, lam)

        t_chi2_bits = t_chi2_stat / (2 * N * np.log(2))
        t_zi_bits   = t_zi_stat   / (2 * N * np.log(2)) if not np.isnan(t_zi_stat) else np.nan

        fpr_chi2 = empirical_fpr(mis, t_chi2_bits)
        fpr_zi   = empirical_fpr(mis, t_zi_bits) if not np.isnan(t_zi_bits) else np.nan

        rows.append(dict(
            config=lbl,
            lam=lam,
            w=1 - np.exp(-lam),
            t_chi2=t_chi2_bits,
            t_zi=t_zi_bits,
            fpr_chi2=fpr_chi2,
            fpr_zi=fpr_zi,
        ))
        print(f"  {lbl:22s}  λ={lam:6.3f}  "
              f"FPR χ²(1)={fpr_chi2:.4f}  FPR ZI-simple={fpr_zi:.4f}"
              f"  (nominal α={alpha})")

    df = pd.DataFrame(rows)
    df.to_csv("zi_simple_calibration.csv", index=False)
    print("Saved: zi_simple_calibration.csv")
    return df


# ── Calibration plot ──────────────────────────────────────────────────────────

def plot_calibration(df, alpha=0.05):
    fig, ax = plt.subplots(figsize=(9, 5))

    lams = df["lam"].values
    ax.plot(lams, df["fpr_chi2"], color="green", marker="o", linewidth=2,
            markersize=6, label=r"$\chi^2(1)$ FPR")
    ax.plot(lams, df["fpr_zi"],   color="purple", marker="s", linewidth=2,
            markersize=6, linestyle="-.", label="ZI-simple FPR")
    ax.axhline(alpha, color="blue", linewidth=1.5, linestyle="--",
               label=f"nominal α = {alpha}")

    ax.set_xscale("log")
    ax.set_xlabel(r"$\lambda = N \cdot p^2$", fontsize=12)
    ax.set_ylabel("Actual false-positive rate", fontsize=12)
    ax.set_title(
        r"Calibration at $\alpha=0.05$: actual FPR under each model"
        "\nGood calibration = points on the blue line",
        fontsize=12, fontweight="bold"
    )
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.25, linestyle="--")

    plt.tight_layout()
    plt.savefig("zi_simple_calibration.png", dpi=150, bbox_inches="tight")
    print("Saved: zi_simple_calibration.png")
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
    data = {}
    for cfg in configs:
        print(f"  {cfg['label']}...", flush=True)
        data[cfg["label"]] = bootstrap_null(cfg["p"], cfg["N"], repeats, rng)

    print("\nPlotting CDF comparison...")
    plot_cdf_comparison(configs, data)

    print("\nCalibration table (FPR at α=0.05):")
    df = calibration_table(configs, data)

    print("\nPlotting calibration...")
    plot_calibration(df)

    print("\nSummary:")
    print(df[["config", "lam", "fpr_chi2", "fpr_zi"]].to_string(index=False))


if __name__ == "__main__":
    main()
