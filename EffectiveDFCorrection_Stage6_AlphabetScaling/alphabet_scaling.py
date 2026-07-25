"""
Stage 6: Does A_k (the slope of ν − ν₀ vs 1/λ_tp) follow a clean function of k?

Setup:
  - Uniform marginals p_X = p_Y = (1/k, ..., 1/k) at each k ∈ {2, ..., 12}.
  - Bootstrap T = 2N·MI under H₀ at a range of N.
  - λ_min = N · min(π) · min(π) = N / k²  (rarest cell expected count).
  - λ_tp  = N / Σ(1/π_xy) = N / k⁴  (Treves-Panzeri scaling parameter).
  - Per k: fit  ν − ν₀ = A_ν / λ_tp  and  a − 1 = B_a / λ_tp  on λ_min ∈ [0.5, 5].
  - Test candidate functional forms for A_k vs k: linear, power, log, etc.
"""

import os
import numpy as np
import pandas as pd
from scipy import optimize
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

OUT = os.path.dirname(os.path.abspath(__file__))
K_BOOTSTRAP = 3_000
LAM_LO, LAM_HI = 0.5, 5.0


# ── Bootstrap (uniform marginals: rng.integers is faster than rng.choice) ─────

def bootstrap_moments_uniform(k, N, K, rng):
    calc = MICalcDiscrete(k)
    T = np.empty(K)
    for s in range(K):
        x = rng.integers(0, k, size=N)
        y = rng.integers(0, k, size=N)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mi_bits = float(calc.computeAverageLocalOfObservations())
        T[s] = 2 * N * mi_bits * np.log(2)
    return float(T.mean()), float(T.var(ddof=1))


# ── Data generation ───────────────────────────────────────────────────────────

def generate_data(k_values, K, rng):
    rows = []
    # For each k, sweep λ_min over [0.1, 30] with extra density in [0.5, 5]
    lam_targets = np.unique(np.round(np.concatenate([
        np.logspace(np.log10(0.1), np.log10(0.5),  4),
        np.logspace(np.log10(0.5), np.log10(5.0), 12),
        np.logspace(np.log10(5.0), np.log10(30.0), 4),
    ]), 3))
    for k in k_values:
        nu0 = (k - 1) ** 2
        Ns = sorted(set(int(round(L * k * k)) for L in lam_targets if L * k * k >= 10))
        for N in Ns:
            lam_min = N / k**2
            lam_tp  = N / k**4
            print(f"  k={k:2d}  N={N:6d}  λ_min={lam_min:6.3f}  λ_tp={lam_tp:.5g}",
                  flush=True)
            mu, sigma2 = bootstrap_moments_uniform(k, N, K, rng)
            nu = 2 * mu**2 / sigma2 if sigma2 > 0 else np.nan
            a  = sigma2 / (2 * mu)  if mu > 0     else np.nan
            rows.append(dict(k=k, nu0=nu0, N=N,
                             lam_min=lam_min, lam_tp=lam_tp,
                             mu=mu, sigma2=sigma2,
                             nu=nu, a=a))
    return pd.DataFrame(rows)


# ── Per-k fit: ν − ν₀ = A/λ_tp  (linear through origin) ───────────────────────

def fit_per_k(df):
    rows = []
    for k in sorted(df["k"].unique()):
        d = df[(df["k"] == k) & (df["lam_min"] >= LAM_LO) & (df["lam_min"] <= LAM_HI)]
        if len(d) < 3:
            continue
        nu0 = (k - 1) ** 2
        x   = 1.0 / d["lam_tp"].values
        y_nu = d["nu"].values - nu0
        y_a  = d["a"].values - 1.0

        A_nu = float((x * y_nu).sum() / (x * x).sum())
        A_a  = float((x * y_a ).sum() / (x * x).sum())

        r2_nu = 1 - ((y_nu - A_nu * x) ** 2).sum() / ((y_nu - y_nu.mean()) ** 2).sum()
        r2_a  = 1 - ((y_a  - A_a  * x) ** 2).sum() / ((y_a  - y_a.mean())  ** 2).sum()

        rows.append(dict(k=k, n=len(d), nu0=nu0, A_nu=A_nu, A_a=A_a,
                         r2_nu=r2_nu, r2_a=r2_a))
    return pd.DataFrame(rows)


# ── Functional-form search for A_k vs k ───────────────────────────────────────

CANDIDATES = {
    "A = c · 1":            lambda kv, c: c * np.ones_like(kv, dtype=float),
    "A = c · k":            lambda kv, c: c * kv,
    "A = c · (k − 1)":      lambda kv, c: c * (kv - 1),
    "A = c · k²":           lambda kv, c: c * kv**2,
    "A = c · (k − 1)²":     lambda kv, c: c * (kv - 1)**2,
    "A = c · log(k)":       lambda kv, c: c * np.log(kv),
    "A = c · k log(k)":     lambda kv, c: c * kv * np.log(kv),
    "A = c · k³":           lambda kv, c: c * kv**3,
    "A = c · (k − 1) k":    lambda kv, c: c * (kv - 1) * kv,
}


def fit_A_vs_k(fits, label):
    k     = fits["k"].values
    A_nu  = fits["A_nu"].values
    A_a   = fits["A_a"].values

    def r2(y, yhat): return 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)

    print(f"\n=== Functional form for {label} vs k ===")
    print(f"{'Model':<24} {'coef (A_ν)':>12} {'R²(A_ν)':>9}  "
          f"{'coef (A_a)':>12} {'R²(A_a)':>9}")
    print("-" * 80)
    for name, func in CANDIDATES.items():
        try:
            (c_nu,), _ = optimize.curve_fit(func, k.astype(float), A_nu, p0=[0.1])
            (c_a, ), _ = optimize.curve_fit(func, k.astype(float), A_a,  p0=[-0.1])
            r2_nu = r2(A_nu, func(k.astype(float), c_nu))
            r2_a  = r2(A_a,  func(k.astype(float), c_a))
            print(f"{name:<24} {c_nu:>+12.4f} {r2_nu:>9.4f}  "
                  f"{c_a:>+12.4f} {r2_a:>9.4f}")
        except Exception:
            print(f"{name:<24} fit failed")


# ── Plot ──────────────────────────────────────────────────────────────────────

def plot_results(df, fits):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    k_vals = sorted(df["k"].unique())
    colors = cm.viridis(np.linspace(0.05, 0.95, len(k_vals)))

    # Panel 1: (ν - ν₀) vs 1/λ_tp, coloured by k
    ax = axes[0][0]
    for k_val, col in zip(k_vals, colors):
        d = df[(df["k"] == k_val) & (df["lam_min"] >= LAM_LO) & (df["lam_min"] <= LAM_HI)]
        if len(d) == 0: continue
        nu0 = (k_val - 1) ** 2
        x = 1.0 / d["lam_tp"]
        ax.scatter(x, d["nu"] - nu0, color=col, s=30, label=f"k={k_val}")
    ax.set_xlabel(r"$1 / \lambda_{tp}$  (= $k^4 / N$ for uniform)")
    ax.set_ylabel(r"$\nu - \nu_0$")
    ax.set_title(r"$\nu - \nu_0$ vs $1/\lambda_{tp}$, fitting region only")
    ax.set_xscale("log"); ax.set_yscale("symlog", linthresh=0.5)
    ax.grid(True, alpha=0.2); ax.legend(fontsize=7, ncol=2, loc="upper left")

    # Panel 2: (a - 1) vs 1/λ_tp
    ax = axes[0][1]
    for k_val, col in zip(k_vals, colors):
        d = df[(df["k"] == k_val) & (df["lam_min"] >= LAM_LO) & (df["lam_min"] <= LAM_HI)]
        if len(d) == 0: continue
        x = 1.0 / d["lam_tp"]
        ax.scatter(x, d["a"] - 1, color=col, s=30, label=f"k={k_val}")
    ax.set_xlabel(r"$1 / \lambda_{tp}$")
    ax.set_ylabel(r"$a - 1$")
    ax.set_title(r"$a - 1$ vs $1/\lambda_{tp}$, fitting region only")
    ax.set_xscale("log")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=7, ncol=2, loc="lower left")

    # Panel 3: A_ν vs k  with best 3 candidate fits overlaid
    ax = axes[1][0]
    k = fits["k"].values.astype(float)
    A_nu = fits["A_nu"].values
    ax.scatter(k, A_nu, color="red", s=80, zorder=5, label="empirical $A_\\nu$")
    kk = np.linspace(k.min(), k.max(), 200)
    candidates_to_plot = ["A = c · k", "A = c · k²", "A = c · k log(k)", "A = c · k³"]
    overlay_colors = ["#1f77b4", "#2ca02c", "#9467bd", "#8c564b"]
    for name, col in zip(candidates_to_plot, overlay_colors):
        func = CANDIDATES[name]
        try:
            (c,), _ = optimize.curve_fit(func, k, A_nu, p0=[0.1])
            ax.plot(kk, func(kk, c), color=col, linewidth=1.7, alpha=0.8,
                    label=f"{name}  c={c:+.4f}")
        except Exception:
            pass
    ax.set_xlabel("k (alphabet size)")
    ax.set_ylabel(r"$A_\nu$")
    ax.set_title(r"$A_\nu(k)$: per-k slope of $\nu - \nu_0$ vs $1/\lambda_{tp}$")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=8, loc="upper left")

    # Panel 4: A_a (= B_a) vs k
    ax = axes[1][1]
    A_a = fits["A_a"].values
    ax.scatter(k, A_a, color="blue", s=80, zorder=5, label="empirical $B_a$")
    for name, col in zip(candidates_to_plot, overlay_colors):
        func = CANDIDATES[name]
        try:
            (c,), _ = optimize.curve_fit(func, k, A_a, p0=[-0.1])
            ax.plot(kk, func(kk, c), color=col, linewidth=1.7, alpha=0.8,
                    label=f"{name}  c={c:+.4f}")
        except Exception:
            pass
    ax.set_xlabel("k (alphabet size)")
    ax.set_ylabel(r"$B_a$")
    ax.set_title(r"$B_a(k)$: per-k slope of $a - 1$ vs $1/\lambda_{tp}$")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=8, loc="lower left")

    fig.suptitle(
        r"Stage 6: how do $A_\nu$ and $B_a$ scale with alphabet size $k$?"
        "\n(uniform marginals, fitting region $\\lambda_{min} \\in [0.5, 5]$)",
        fontsize=13
    )
    plt.tight_layout()
    out = os.path.join(OUT, "alphabet_scaling.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {out}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)
    k_values = list(range(2, 13))

    print(f"Bootstrap K={K_BOOTSTRAP} per config, k ∈ {k_values}")
    df = generate_data(k_values, K_BOOTSTRAP, rng)
    df.to_csv(os.path.join(OUT, "alphabet_scaling_data.csv"), index=False)
    print(f"\nGenerated {len(df)} data points.")

    fits = fit_per_k(df)
    fits.to_csv(os.path.join(OUT, "alphabet_scaling_fits.csv"), index=False)
    print("\n=== Per-k fits (ν − ν₀ = A_ν/λ_tp, a − 1 = B_a/λ_tp) ===")
    print(fits.to_string(index=False))

    fit_A_vs_k(fits, "A_ν / B_a")
    plot_results(df, fits)


if __name__ == "__main__":
    main()
