"""
Recreates checkMiDiscreteNullDistribution.m (JIDT wiki/NullDistributions) in Python,
extended to overlay chi^2(k) CDFs at several degrees of freedom.

Key detail from the Octave source (line 29 comment): useToolkit=false is the correct
default. Using computeSignificance() fixes the marginals exactly, which restricts the
number of distinct MI values and produces a stepped CDF. Instead we draw fresh
independent X, Y for every surrogate — exactly as the Octave code does in its loop.

X-axis: MI in bits (matching the wiki). Chi^2 CDF is evaluated at 2*N*MI*log(2),
the standard chi^2 statistic for a 2x2 table.
"""

import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ── JIDT setup ────────────────────────────────────────────────────────────────

from jpype import startJVM, getDefaultJVMPath, JPackage, JArray, JInt, isJVMStarted

JIDT_JAR = os.environ.get(
    "JIDT_JAR",
    "/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/jidt/infodynamics.jar",
)
if not os.path.exists(JIDT_JAR):
    raise FileNotFoundError(
        f"JIDT jar not found at {JIDT_JAR}. "
        "Set the JIDT_JAR environment variable or edit the constant above."
    )

if not isJVMStarted():
    startJVM(getDefaultJVMPath(), "-ea", f"-Djava.class.path={JIDT_JAR}")

MICalcDiscrete = JPackage("infodynamics.measures.discrete").MutualInformationCalculatorDiscrete


def bootstrap_null(bias1, bias2, N, repeats, rng):
    """
    Direct translation of the Octave loop (useToolkit=false):
      for s = 1:repeats
        x = (rand(1,N) < bias1)*1;
        y = (rand(1,N) < bias2)*1;
        mis(s) = miCalc.computeAverageLocalOfObservations();
      end
    Returns MI values in bits.
    """
    calc = MICalcDiscrete(2)
    mis = np.empty(repeats)
    for s in range(repeats):
        x = (rng.random(N) < bias1).astype(int)
        y = (rng.random(N) < bias2).astype(int)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mis[s] = float(calc.computeAverageLocalOfObservations())
    return mis   # bits


# ── Plotting ──────────────────────────────────────────────────────────────────

CANDIDATE_DFS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]


def plot_pdf(configs, surrogates_dict):
    colors = cm.plasma(np.linspace(0.05, 0.85, len(CANDIDATE_DFS)))
    n_cols = 4
    n_rows = (len(configs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.2 * n_cols, 4.2 * n_rows), squeeze=False)

    for i, cfg in enumerate(configs):
        ax = axes[i // n_cols][i % n_cols]
        mis = surrogates_dict[cfg["label"]]   # in bits
        N   = cfg["N"]

        counts, edges = np.histogram(mis, bins=100)
        pdfX = (edges[:-1] + edges[1:]) / 2
        bin_width = edges[1] - edges[0]
        pdfY = counts / len(mis) / bin_width    # density (area sums to 1)

        ax.plot(pdfX, pdfY, color="red", linewidth=2.5,
                label="Bootstrapped null", zorder=4)

        # chi^2 PDFs: d/dx chi2cdf(2*N*x*log(2), df) = chi2pdf(2*N*x*log(2), df) * 2*N*log(2)
        stat = 2 * N * pdfX * np.log(2)
        jacobian = 2 * N * np.log(2)
        for df_val, col in zip(CANDIDATE_DFS, colors):
            pdf_vals = stats.chi2.pdf(stat, df=df_val) * jacobian
            if df_val == 1.0:
                ax.plot(pdfX, pdf_vals, color="green", linewidth=2.2,
                        label=fr"$\chi^2$(1) — theoretic", zorder=5)
            else:
                ax.plot(pdfX, pdf_vals, color=col, linewidth=1.4, alpha=0.85,
                        label=fr"$\chi^2$({df_val})", zorder=3)

        # Cap y-axis at the bootstrapped null peak to prevent singularities dominating
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
        r"Bootstrapped null PDF of MI vs $\chi^2(k)$ analytic — binary X, Y",
        fontsize=13, y=1.01
    )
    plt.tight_layout()
    plt.savefig("null_chi2_fit_pdf.png", dpi=150, bbox_inches="tight")
    print("Saved: null_chi2_fit_pdf.png")
    plt.show()


def plot_cdf(configs, surrogates_dict):
    """
    Matches the Octave plot exactly:
      - hist(mis, 100) → normalise → cumsum → plot at bin centres
      - chi2cdf(2*N*pdfX*log(2), df) overlaid for each candidate df
      - blue horizontal line at CDF = 0.95
    """
    colors = cm.plasma(np.linspace(0.05, 0.85, len(CANDIDATE_DFS)))
    n_cols = 4
    n_rows = (len(configs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.2 * n_cols, 4.2 * n_rows), squeeze=False)

    for i, cfg in enumerate(configs):
        ax = axes[i // n_cols][i % n_cols]
        mis = surrogates_dict[cfg["label"]]   # in bits
        N   = cfg["N"]

        # ── Octave: [pdfY, pdfX] = hist(mis, 100)
        counts, edges = np.histogram(mis, bins=100)
        pdfX = (edges[:-1] + edges[1:]) / 2        # bin centres
        pdfY = counts / len(mis)                    # normalise sum to 1
        cdfY = np.cumsum(pdfY)                      # empirical CDF

        ax.plot(pdfX, cdfY, color="red", linewidth=2.5,
                label="Bootstrapped null", zorder=4)

        # ── chi^2(df) CDFs: chi2cdf(2*N*pdfX*log(2), df)
        stat = 2 * N * pdfX * np.log(2)            # convert MI bits → chi^2 statistic
        for df_val, col in zip(CANDIDATE_DFS, colors):
            if df_val == 1.0:
                ax.plot(pdfX, stats.chi2.cdf(stat, df=df_val),
                        color="green", linewidth=2.2,
                        label=fr"$\chi^2$(1) — theoretic", zorder=5)
            else:
                ax.plot(pdfX, stats.chi2.cdf(stat, df=df_val),
                        color=col, linewidth=1.4, alpha=0.85,
                        label=fr"$\chi^2$({df_val})", zorder=3)

        # ── α = 0.05 line (blue, like the wiki)
        ax.axhline(0.95, color="blue", linewidth=1.5, alpha=0.7,
                   label="α=0.05 (CDF=0.95)")

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
        r"Bootstrapped null CDF of MI vs $\chi^2(k)$ analytic — binary X, Y"
        "\nBlue line = α=0.05 threshold",
        fontsize=13, y=1.01
    )
    plt.tight_layout()
    plt.savefig("null_chi2_fit_cdf.png", dpi=150, bbox_inches="tight")
    print("Saved: null_chi2_fit_cdf.png")
    plt.show()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
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
    rng = np.random.default_rng(42)

    surrogates_dict = {}
    print("Generating bootstrapped nulls (fresh X,Y draws per surrogate)...")
    for cfg in configs:
        p = cfg["p"]
        print(f"  {cfg['label']}...", flush=True)
        surrogates_dict[cfg["label"]] = bootstrap_null(p, p, cfg["N"], repeats, rng)
        mis = surrogates_dict[cfg["label"]]
        print(f"    mean={mis.mean():.4f} bits  n_unique={len(np.unique(mis.round(8)))}")

    print("\nPlotting PDFs...")
    plot_pdf(configs, surrogates_dict)

    print("Plotting CDFs...")
    plot_cdf(configs, surrogates_dict)


if __name__ == "__main__":
    main()
