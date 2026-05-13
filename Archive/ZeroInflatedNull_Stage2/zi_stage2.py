"""
ZI Stage 2: Compare Option 1 (ZI + D₁ bootstrap fit) and Option 2 (two-regime).

Option 1 — ZI with conditional fit (no free analytical params, bootstrap-estimated ν_c, a_c):
    p-value = (1 - e^{-λ}) · P(a_c·χ²(ν_c) > t)
    ν_c, a_c fitted by moment-matching on D₁ surrogates (n₁₁ ≥ 1) only.
    Mixing weight e^{-λ} is analytically exact.

Option 2 — Two-regime:
    if λ ≥ 5:  use χ²(1) directly  (already well-calibrated there)
    if λ < 5:  use Option 1

Both options are compared against:
  - χ²(1) standard baseline
  - ZI-simple (previous stage, no free params, uses χ²(1) for conditional — fails at small λ)

Calibration is measured as actual FPR at nominal α = 0.05 against the full bootstrap null.
FPR closest to α = best-calibrated model.

Outputs
-------
  zi_stage2_cdf.png         — 12-panel CDF overlay (5 curves per panel)
  zi_stage2_calibration.png — FPR vs λ for all 4 models
  zi_stage2_calibration.csv — full numerical results
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


# ── Bootstrap (records n₁₁ per surrogate) ────────────────────────────────────

def bootstrap_null_with_counts(bias, N, repeats, rng):
    """Fresh draws; returns (mis_bits, n11) arrays of length repeats."""
    calc = MICalcDiscrete(2)
    mis  = np.empty(repeats)
    n11  = np.empty(repeats, dtype=int)
    for s in range(repeats):
        x = (rng.random(N) < bias).astype(int)
        y = (rng.random(N) < bias).astype(int)
        n11[s] = int(np.sum((x == 1) & (y == 1)))
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mis[s] = float(calc.computeAverageLocalOfObservations())
    return mis, n11


# ── Conditional moment-matching (D₁ only) ────────────────────────────────────

def fit_scaled_chi2_conditional(mis_bits_d1, N):
    """
    Fit ν_c and a_c from D₁ (n₁₁ ≥ 1) surrogates via moment-matching.
    Returns (nan, nan) if too few samples or degenerate moments.
    """
    if len(mis_bits_d1) < 50:
        return np.nan, np.nan
    T      = 2 * N * mis_bits_d1 * np.log(2)
    mu     = float(np.mean(T))
    sigma2 = float(np.var(T, ddof=1))
    if sigma2 <= 0 or mu <= 0:
        return np.nan, np.nan
    nu = 2 * mu**2 / sigma2
    a  = sigma2 / (2 * mu)
    return nu, a


# ── CDF functions ─────────────────────────────────────────────────────────────

def zi_simple_cdf(x_bits, N, lam):
    """ZI-simple: e^{-λ} + (1-e^{-λ})·χ²_CDF(t, df=1).  No free params."""
    t = 2 * N * x_bits * np.log(2)
    return np.exp(-lam) + (1 - np.exp(-lam)) * stats.chi2.cdf(t, df=1)


def zi_cdf_opt1(x_bits, N, lam, nu_c, a_c):
    """Option 1 CDF: e^{-λ} + (1-e^{-λ})·χ²_CDF(t/a_c, df=ν_c)."""
    t = 2 * N * x_bits * np.log(2)
    return np.exp(-lam) + (1 - np.exp(-lam)) * stats.chi2.cdf(t / a_c, df=nu_c)


# ── Critical value functions ──────────────────────────────────────────────────

def zi_simple_critical(alpha, N, lam):
    """Critical value (MI bits) under ZI-simple at level alpha. Returns nan if degenerate."""
    w = 1 - np.exp(-lam)
    if w <= 0:
        return np.nan
    p_cond = (1 - alpha - np.exp(-lam)) / w
    if p_cond <= 0 or p_cond >= 1:
        return np.nan
    t_stat = stats.chi2.ppf(p_cond, df=1)
    return t_stat / (2 * N * np.log(2))


def zi_critical_opt1(alpha, N, lam, nu_c, a_c):
    """
    Critical value (MI bits) under Option 1 at level alpha.
    Inverts: e^{-λ} + (1-e^{-λ})·χ²_CDF(t/a_c, ν_c) = 1 - alpha
    Returns nan if degenerate or parameters missing.
    """
    if np.isnan(nu_c) or np.isnan(a_c):
        return np.nan
    w = 1 - np.exp(-lam)
    if w <= 0:
        return np.nan
    p_cond = (1 - alpha - np.exp(-lam)) / w
    if p_cond <= 0 or p_cond >= 1:
        return np.nan
    t_stat = a_c * stats.chi2.ppf(p_cond, df=nu_c)
    return t_stat / (2 * N * np.log(2))


def two_regime_critical(alpha, N, lam, nu_c, a_c, threshold=5.0):
    """
    Option 2: χ²(1) if λ ≥ threshold, else Option 1.
    Returns critical value in MI bits.
    """
    if lam >= threshold:
        return stats.chi2.ppf(1 - alpha, df=1) / (2 * N * np.log(2))
    return zi_critical_opt1(alpha, N, lam, nu_c, a_c)


# ── FPR helper ────────────────────────────────────────────────────────────────

def empirical_fpr(mis_bits, threshold_bits):
    """Fraction of surrogates exceeding threshold. nan threshold → nan FPR."""
    if threshold_bits is None or np.isnan(threshold_bits):
        return np.nan
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
        lam  = N * p**2
        d    = data[lbl]

        mis  = d["mis_bits"]
        nu_c = d["nu_c"]
        a_c  = d["a_c"]

        # Empirical CDF at bin centres
        counts, edges = np.histogram(mis, bins=100)
        pdfX = (edges[:-1] + edges[1:]) / 2
        cdfY = np.cumsum(counts / len(mis))

        # Bootstrap ground truth
        ax.plot(pdfX, cdfY,
                color="red", linewidth=2.5, label="Bootstrap null", zorder=5)

        # χ²(1)
        stat = 2 * N * pdfX * np.log(2)
        ax.plot(pdfX, stats.chi2.cdf(stat, df=1),
                color="green", linewidth=2.0, label=r"$\chi^2(1)$", zorder=3)

        # ZI-simple (reference)
        ax.plot(pdfX, zi_simple_cdf(pdfX, N, lam),
                color="purple", linewidth=1.8, linestyle="-.",
                label="ZI-simple", zorder=3)

        # Option 1
        if not (np.isnan(nu_c) or np.isnan(a_c)):
            ax.plot(pdfX, zi_cdf_opt1(pdfX, N, lam, nu_c, a_c),
                    color="royalblue", linewidth=2.0, linestyle="--",
                    label=fr"Opt1  ν_c={nu_c:.2f}, a_c={a_c:.2f}", zorder=4)

        # Option 2 (same CDF as Opt1 for λ<5, same as χ²(1) for λ≥5)
        if lam >= 5.0:
            ax.plot(pdfX, stats.chi2.cdf(stat, df=1),
                    color="darkorange", linewidth=2.0, linestyle=":",
                    label="Opt2 (=χ²(1), λ≥5)", zorder=4)
        elif not (np.isnan(nu_c) or np.isnan(a_c)):
            ax.plot(pdfX, zi_cdf_opt1(pdfX, N, lam, nu_c, a_c),
                    color="darkorange", linewidth=2.0, linestyle=":",
                    label="Opt2 (=Opt1, λ<5)", zorder=4)

        ax.axhline(1 - alpha, color="grey", linewidth=1.2,
                   alpha=0.7, linestyle="--", label=f"α={alpha}")

        w = 1 - np.exp(-lam)
        ax.text(0.03, 0.97,
                f"λ={lam:.2f}  w={w:.3f}\nν_c={nu_c:.3f}  a_c={a_c:.3f}",
                transform=ax.transAxes, fontsize=7.5, va="top",
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
        "CDF comparison — all four models vs bootstrap ground truth\n"
        "Red=bootstrap  Green=χ²(1)  Purple=ZI-simple  Blue=Opt1  Orange=Opt2",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.savefig("zi_stage2_cdf.png", dpi=150, bbox_inches="tight")
    print("Saved: zi_stage2_cdf.png")
    plt.show()


# ── Calibration table ─────────────────────────────────────────────────────────

def calibration_table(configs, data, alpha=0.05):
    rows = []
    for cfg in configs:
        N, p, lbl = cfg["N"], cfg["p"], cfg["label"]
        lam  = N * p**2
        d    = data[lbl]
        mis  = d["mis_bits"]
        nu_c = d["nu_c"]
        a_c  = d["a_c"]

        t_chi2      = stats.chi2.ppf(1 - alpha, df=1) / (2 * N * np.log(2))
        t_zi_simple = zi_simple_critical(alpha, N, lam)
        t_opt1      = zi_critical_opt1(alpha, N, lam, nu_c, a_c)
        t_opt2      = two_regime_critical(alpha, N, lam, nu_c, a_c)

        fpr_chi2      = empirical_fpr(mis, t_chi2)
        fpr_zi_simple = empirical_fpr(mis, t_zi_simple)
        fpr_opt1      = empirical_fpr(mis, t_opt1)
        fpr_opt2      = empirical_fpr(mis, t_opt2)

        rows.append(dict(
            config=lbl, lam=lam, w=1 - np.exp(-lam),
            nu_c=nu_c, a_c=a_c,
            fpr_chi2=fpr_chi2, fpr_zi_simple=fpr_zi_simple,
            fpr_opt1=fpr_opt1, fpr_opt2=fpr_opt2,
        ))
        print(f"  {lbl:22s}  λ={lam:6.3f}  "
              f"χ²(1)={fpr_chi2:.4f}  ZI-simple={fpr_zi_simple:.4f}  "
              f"Opt1={fpr_opt1:.4f}  Opt2={fpr_opt2:.4f}  "
              f"(nominal {alpha})", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv("zi_stage2_calibration.csv", index=False)
    print("Saved: zi_stage2_calibration.csv")
    return df


# ── Calibration plot ──────────────────────────────────────────────────────────

def plot_calibration(df, alpha=0.05):
    fig, ax = plt.subplots(figsize=(10, 5))

    lams = df["lam"].values

    ax.plot(lams, df["fpr_chi2"],      color="green",      marker="o",
            linewidth=2.0, markersize=7, label=r"$\chi^2(1)$")
    ax.plot(lams, df["fpr_zi_simple"], color="purple",     marker="s",
            linewidth=1.8, markersize=7, linestyle="-.", label="ZI-simple")
    ax.plot(lams, df["fpr_opt1"],      color="royalblue",  marker="D",
            linewidth=2.0, markersize=7, linestyle="--",  label="Option 1 (ZI + D₁ fit)")
    ax.plot(lams, df["fpr_opt2"],      color="darkorange", marker="^",
            linewidth=2.0, markersize=7, linestyle=":",   label="Option 2 (two-regime, λ_thresh=5)")

    ax.axhline(alpha, color="blue", linewidth=1.8, linestyle="--",
               label=f"nominal α = {alpha}")
    ax.axvline(5.0,   color="grey", linewidth=1.2, linestyle=":",
               alpha=0.7, label="λ=5 threshold")

    ax.set_xscale("log")
    ax.set_xlabel(r"$\lambda = N \cdot p^2$", fontsize=12)
    ax.set_ylabel("Actual false-positive rate", fontsize=12)
    ax.set_title(
        r"Calibration at $\alpha=0.05$: FPR for all four models"
        "\nIdeal = points on the blue dashed line",
        fontsize=12, fontweight="bold"
    )
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, alpha=0.25, linestyle="--")
    plt.tight_layout()
    plt.savefig("zi_stage2_calibration.png", dpi=150, bbox_inches="tight")
    print("Saved: zi_stage2_calibration.png")
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

    # 20,000 repeats to ensure stable D₁ estimates even at small λ
    # (e.g. λ=0.05 → ~980 D₁ samples out of 20,000)
    repeats = 20_000

    print("Generating bootstrap nulls with cell counts (repeats=20,000)...")
    data = {}
    for cfg in configs:
        p, N, lbl = cfg["p"], cfg["N"], cfg["label"]
        lam = N * p**2
        print(f"  {lbl}  (λ={lam:.3f})...", flush=True)

        mis_bits, n11 = bootstrap_null_with_counts(p, N, repeats, rng)
        mask_d1   = n11 >= 1
        mis_d1    = mis_bits[mask_d1]
        n_d1      = mask_d1.sum()

        nu_c, a_c = fit_scaled_chi2_conditional(mis_d1, N)
        print(f"    D₁ samples: {n_d1}/{repeats}  "
              f"ν_c={nu_c:.3f}  a_c={a_c:.3f}", flush=True)

        data[lbl] = dict(mis_bits=mis_bits, n11=n11, nu_c=nu_c, a_c=a_c)

    print("\nCalibration table (FPR at α=0.05):")
    df = calibration_table(configs, data)

    print("\nPlotting calibration...")
    plot_calibration(df)

    print("\nPlotting CDF comparison...")
    plot_cdf_comparison(configs, data)

    print("\nFull summary:")
    print(df[["config", "lam", "fpr_chi2", "fpr_zi_simple",
              "fpr_opt1", "fpr_opt2"]].to_string(index=False))


if __name__ == "__main__":
    main()
