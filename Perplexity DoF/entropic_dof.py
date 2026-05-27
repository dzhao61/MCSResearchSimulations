"""
Pathway 1 (Gemini): Entropic effective degrees of freedom for the MI null.

Replaces the rigid alphabet-size formula ν = (|X|-1)(|Y|-1) with one based on
perplexity 2^H, the effective alphabet size after accounting for skewed marginals:

    ν_eff = (2^H(X) - 1) * (2^H(Y) - 1)

For binary X, Y with biases p_X, p_Y:
    H(X) = -p_X log2 p_X - (1-p_X) log2 (1-p_X)
    2^H(X) ∈ [1, 2],  ν_eff ∈ [0, 1]
    p = 0.5 → H = 1, 2^H = 2, ν_eff = 1  (matches nominal χ²(1))
    p → 0  → H → 0, 2^H → 1, ν_eff → 0  (sharp χ² near 0)

Test: under H₀ generate tables with fixed marginals, compute T = 2N·MI·log(2),
and overlay χ²(ν_eff) on the empirical density + CDF.
"""

import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
RNG_SEED = 42
K = 20_000


# ─── Entropy / effective dof ──────────────────────────────────────────────────

def entropy_bits_binary(p):
    if p in (0.0, 1.0):
        return 0.0
    return float(-p * np.log2(p) - (1 - p) * np.log2(1 - p))


def nu_eff(p_X, p_Y):
    H_X = entropy_bits_binary(p_X)
    H_Y = entropy_bits_binary(p_Y)
    return (2**H_X - 1) * (2**H_Y - 1)


# ─── Bootstrap null ───────────────────────────────────────────────────────────

def mi_bits_from_counts(n, N):
    """Vectorised 2x2 MI in bits. n: (K, 4) [n00, n01, n10, n11] → (K,)."""
    P = n.reshape(-1, 2, 2) / N
    px = P.sum(axis=2, keepdims=True)
    py = P.sum(axis=1, keepdims=True)
    denom = px * py
    with np.errstate(divide="ignore", invalid="ignore"):
        log_term = np.where((P > 0) & (denom > 0),
                            np.log2(P / np.where(denom > 0, denom, 1.0)),
                            0.0)
    return (P * log_term).sum(axis=(1, 2))


def bootstrap_T(p_X, p_Y, N, K, rng):
    """Fresh independent X, Y per surrogate. Returns T = 2N·MI·log(2) in nats."""
    probs = [(1 - p_X) * (1 - p_Y),
             (1 - p_X) * p_Y,
             p_X * (1 - p_Y),
             p_X * p_Y]
    n = rng.multinomial(N, probs, size=K)
    mi_bits = mi_bits_from_counts(n, N)
    return 2 * N * mi_bits * np.log(2)


# ─── Configs ──────────────────────────────────────────────────────────────────

def make_configs():
    """
    3x3 grid: rows are skewness regimes, columns are N values.
    """
    rows = [
        dict(p_X=0.50, p_Y=0.50, tag="balanced"),
        dict(p_X=0.10, p_Y=0.10, tag="symmetric skewed"),
        dict(p_X=0.50, p_Y=0.10, tag="asymmetric"),
    ]
    Ns = [50, 200, 1000]
    cfgs = []
    for r in rows:
        for N in Ns:
            cfgs.append({**r, "N": N})
    return cfgs


# ─── Plots ────────────────────────────────────────────────────────────────────

def panel_title(cfg, nu_e):
    H_X = entropy_bits_binary(cfg["p_X"])
    H_Y = entropy_bits_binary(cfg["p_Y"])
    return (
        f"{cfg['tag']}: p_X={cfg['p_X']}, p_Y={cfg['p_Y']}, N={cfg['N']}\n"
        f"H(X)={H_X:.3f}, H(Y)={H_Y:.3f}  |  "
        f"$\\nu_{{eff}}$={nu_e:.4f}  vs  $\\nu_{{nom}}$=1"
    )


def plot_pdf(configs, samples):
    n_rows, n_cols = 3, 3
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.2 * n_cols, 3.9 * n_rows),
                             squeeze=False)
    for i, cfg in enumerate(configs):
        ax = axes[i // n_cols][i % n_cols]
        T = samples[i]
        nu_e = nu_eff(cfg["p_X"], cfg["p_Y"])

        # x range: 99.5th percentile clip so the heavy tail doesn't compress the body
        xmax = max(8.0, float(np.percentile(T, 99.5)))

        # Empirical histogram (density)
        ax.hist(T, bins=80, range=(0, xmax), density=True,
                color="#bbbbbb", edgecolor="#666666", linewidth=0.4,
                label="empirical")

        # Overlay support — start above 0 to avoid the ν<1 singularity ruining ylim
        xs = np.linspace(0.02, xmax, 500)
        ax.plot(xs, stats.chi2.pdf(xs, df=1), color="green", linewidth=2.0,
                label=r"$\chi^2(1)$ nominal")
        ax.plot(xs, stats.chi2.pdf(xs, df=nu_e), color="darkorange", linewidth=2.0,
                linestyle="--", label=fr"$\chi^2(\nu_{{eff}})$")

        ax.set_title(panel_title(cfg, nu_e), fontsize=9)
        ax.set_xlim(0, xmax)
        # cap y at ~3x the histogram peak so the chi² singularity at 0 doesn't dominate
        counts, _ = np.histogram(T, bins=80, range=(0, xmax), density=True)
        ax.set_ylim(0, max(counts) * 1.5 if max(counts) > 0 else 1.0)
        ax.set_xlabel(r"$T = 2N \cdot I$ (nats)", fontsize=9)
        ax.set_ylabel("density", fontsize=9)
        ax.grid(True, alpha=0.2, linestyle="--")
        if i == 0:
            ax.legend(fontsize=8, loc="upper right")

    fig.suptitle(
        r"Pathway 1: empirical PDF vs $\chi^2(\nu_{eff})$ with "
        r"$\nu_{eff} = (2^{H(X)}-1)(2^{H(Y)}-1)$",
        fontsize=12
    )
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "entropic_dof_pdf.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


def plot_cdf(configs, samples):
    n_rows, n_cols = 3, 3
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(5.2 * n_cols, 3.9 * n_rows),
                             squeeze=False)
    for i, cfg in enumerate(configs):
        ax = axes[i // n_cols][i % n_cols]
        T = samples[i]
        nu_e = nu_eff(cfg["p_X"], cfg["p_Y"])

        xmax = max(8.0, float(np.percentile(T, 99.5)))

        # Empirical CDF: sort + rank
        T_sorted = np.sort(T)
        cdf_emp = np.arange(1, len(T) + 1) / len(T)
        ax.plot(T_sorted, cdf_emp, color="red", linewidth=2.5,
                label="empirical", zorder=4)

        xs = np.linspace(0, xmax, 500)
        ax.plot(xs, stats.chi2.cdf(xs, df=1), color="green", linewidth=2.0,
                label=r"$\chi^2(1)$ nominal")
        ax.plot(xs, stats.chi2.cdf(xs, df=nu_e), color="darkorange",
                linewidth=2.0, linestyle="--",
                label=fr"$\chi^2(\nu_{{eff}})$")

        ax.axhline(0.95, color="blue", linewidth=1.0, alpha=0.5,
                   linestyle=":", label="α=0.05")

        ax.set_title(panel_title(cfg, nu_e), fontsize=9)
        ax.set_xlim(0, xmax)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel(r"$T = 2N \cdot I$ (nats)", fontsize=9)
        ax.set_ylabel("CDF", fontsize=9)
        ax.grid(True, alpha=0.2, linestyle="--")
        if i == 0:
            ax.legend(fontsize=8, loc="lower right")

    fig.suptitle(
        r"Pathway 1: empirical CDF vs $\chi^2(\nu_{eff})$ with "
        r"$\nu_{eff} = (2^{H(X)}-1)(2^{H(Y)}-1)$",
        fontsize=12
    )
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "entropic_dof_cdf.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ─── Summary table ────────────────────────────────────────────────────────────

def print_summary(configs, samples):
    print("\n=== Calibration check at α=0.05 ===")
    print(f"{'config':<40} {'ν_eff':>8} {'q95_χ²(1)':>10} {'q95_χ²(νeff)':>12} {'q95_emp':>9} "
          f"{'FPR_χ²(1)':>10} {'FPR_χ²(νeff)':>13}")
    print("-" * 110)
    for cfg, T in zip(configs, samples):
        nu_e = nu_eff(cfg["p_X"], cfg["p_Y"])
        q95_nom = stats.chi2.ppf(0.95, df=1)
        q95_eff = stats.chi2.ppf(0.95, df=nu_e)
        q95_emp = float(np.percentile(T, 95))
        fpr_nom = float((T > q95_nom).mean())
        fpr_eff = float((T > q95_eff).mean())
        tag = f"{cfg['tag']}: p=({cfg['p_X']},{cfg['p_Y']}), N={cfg['N']}"
        print(f"{tag:<40} {nu_e:>8.4f} {q95_nom:>10.3f} {q95_eff:>12.3f} {q95_emp:>9.3f} "
              f"{fpr_nom:>10.4f} {fpr_eff:>13.4f}")
    print("\nNominal target: FPR = 0.05.  Closer to 0.05 = better calibration.")


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(RNG_SEED)
    configs = make_configs()
    print(f"Bootstrap K={K} samples per config across {len(configs)} configs...")
    samples = []
    for cfg in configs:
        print(f"  {cfg['tag']}: p_X={cfg['p_X']}, p_Y={cfg['p_Y']}, N={cfg['N']}")
        samples.append(bootstrap_T(cfg["p_X"], cfg["p_Y"], cfg["N"], K, rng))
    plot_pdf(configs, samples)
    plot_cdf(configs, samples)
    print_summary(configs, samples)
    print("Done.")


if __name__ == "__main__":
    main()
