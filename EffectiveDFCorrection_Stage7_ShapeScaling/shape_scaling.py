"""
Stage 7: Does A_ν depend on marginal shape on top of alphabet size?

Stage 6 found A_ν ≈ 0.30·log(k) for UNIFORM marginals. Question: does this
hold for non-uniform marginals, or is shape another axis?

For each k ∈ {2, ..., 12}, run three shape families (p_X = p_Y, same shape):
  uniform     : (1/k, ..., 1/k)
  mild_skew   : ( 1/(2k),  rest equal )   ← rarest state at half-density
  strong_skew : ( 1/(5k),  rest equal )   ← rarest state at 1/5-density

For each (k, shape): fit ν − ν₀ = A_ν/λ_tp on λ_min ∈ [0.5, 5].
Then plot A_ν vs k coloured by shape — overlapping lines = "k only";
separate lines = "shape matters too".

Also record marginal entropy H(p) — if A_ν tracks H, that's the deeper variable.
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


# ── Marginal shape families ───────────────────────────────────────────────────

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


def entropy_bits(p):
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


# ── Bootstrap ─────────────────────────────────────────────────────────────────

def bootstrap_moments(k, p_marg, N, K, rng):
    calc = MICalcDiscrete(k)
    cdf = np.cumsum(p_marg)
    T = np.empty(K)
    for s in range(K):
        x = np.searchsorted(cdf, rng.random(N))
        y = np.searchsorted(cdf, rng.random(N))
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mi_bits = float(calc.computeAverageLocalOfObservations())
        T[s] = 2 * N * mi_bits * np.log(2)
    return float(T.mean()), float(T.var(ddof=1))


# ── Data generation ───────────────────────────────────────────────────────────

def generate_data(k_values, shapes, K, rng):
    rows = []
    lam_targets = np.unique(np.round(np.concatenate([
        np.logspace(np.log10(0.1), np.log10(0.5),  4),
        np.logspace(np.log10(0.5), np.log10(5.0), 12),
        np.logspace(np.log10(5.0), np.log10(30.0), 4),
    ]), 3))
    for k in k_values:
        nu0 = (k - 1) ** 2
        for shape in shapes:
            p = make_marginal(k, shape)
            H = entropy_bits(p)
            pi_min = p.min() * p.min()
            sum_inv_pi = float(np.sum(1.0 / np.outer(p, p)))
            # N values to cover λ_min ∈ [0.1, 30]
            Ns = sorted(set(int(round(L / pi_min)) for L in lam_targets
                            if L / pi_min >= 10))
            for N in Ns:
                lam_min = N * pi_min
                lam_tp  = N / sum_inv_pi
                print(f"  k={k:2d} {shape:<12} N={N:6d}  "
                      f"λ_min={lam_min:6.3f}  λ_tp={lam_tp:.5g}  H={H:.3f}",
                      flush=True)
                mu, sigma2 = bootstrap_moments(k, p, N, K, rng)
                nu = 2 * mu**2 / sigma2 if sigma2 > 0 else np.nan
                a  = sigma2 / (2 * mu)  if mu > 0     else np.nan
                rows.append(dict(
                    k=k, shape=shape, nu0=nu0, entropy=H, N=N,
                    lam_min=lam_min, lam_tp=lam_tp,
                    mu=mu, sigma2=sigma2, nu=nu, a=a,
                ))
    return pd.DataFrame(rows)


# ── Per (k, shape) fit ────────────────────────────────────────────────────────

def fit_per_k_shape(df):
    rows = []
    for (k, shape), d in df.groupby(["k", "shape"]):
        d = d[(d["lam_min"] >= LAM_LO) & (d["lam_min"] <= LAM_HI)]
        if len(d) < 3:
            continue
        nu0 = (k - 1) ** 2
        x = 1.0 / d["lam_tp"].values
        y_nu = d["nu"].values - nu0
        y_a  = d["a"].values - 1.0
        A_nu = float((x * y_nu).sum() / (x * x).sum())
        A_a  = float((x * y_a ).sum() / (x * x).sum())
        r2_nu = 1 - ((y_nu - A_nu * x)**2).sum() / ((y_nu - y_nu.mean())**2).sum()
        r2_a  = 1 - ((y_a  - A_a  * x)**2).sum() / ((y_a  - y_a.mean()) **2).sum()
        rows.append(dict(
            k=k, shape=shape, n=len(d), entropy=d["entropy"].iloc[0], nu0=nu0,
            A_nu=A_nu, A_a=A_a, r2_nu=r2_nu, r2_a=r2_a
        ))
    return pd.DataFrame(rows).sort_values(["shape", "k"]).reset_index(drop=True)


# ── Test functional forms ────────────────────────────────────────────────────

CANDIDATES_K = {
    "A = c · log(k)":  lambda kv, c: c * np.log(kv),
    "A = c · k":       lambda kv, c: c * kv,
    "A = c · (k − 1)": lambda kv, c: c * (kv - 1),
}

CANDIDATES_H = {
    "A = c · H":          lambda H, c: c * H,
    "A = c · H + d":      lambda H, c, d: c * H + d,
}


def fit_models(fits):
    def r2(y, yhat): return 1 - np.sum((y - yhat)**2) / np.sum((y - y.mean())**2)

    print("\n=== A_ν as function of k (per shape) ===")
    print(f"{'shape':<14} {'model':<22} {'c (and d)':<22} {'R²'}")
    for shape in fits["shape"].unique():
        s = fits[fits["shape"] == shape]
        k = s["k"].values.astype(float)
        A = s["A_nu"].values
        for name, func in CANDIDATES_K.items():
            try:
                popt, _ = optimize.curve_fit(func, k, A, p0=[0.3])
                r = r2(A, func(k, *popt))
                params = ", ".join(f"{v:+.4f}" for v in popt)
                print(f"{shape:<14} {name:<22} {params:<22} {r:>.4f}")
            except Exception:
                pass
        print()

    print("=== A_ν as function of entropy H (all shapes pooled per k? No — pooled all) ===")
    H = fits["entropy"].values
    A = fits["A_nu"].values
    for name, func in CANDIDATES_H.items():
        p0 = [0.3] if "+ d" not in name else [0.3, 0.0]
        try:
            popt, _ = optimize.curve_fit(func, H, A, p0=p0)
            r = r2(A, func(H, *popt))
            params = ", ".join(f"{v:+.4f}" for v in popt)
            print(f"{'(pooled all)':<14} {name:<22} {params:<22} {r:>.4f}")
        except Exception:
            pass

    print("\n=== Combined: A_ν = a·log(k) + b·H + c ===")
    k = fits["k"].values.astype(float)
    H = fits["entropy"].values
    A = fits["A_nu"].values
    def combo(X, a, b, c):
        kv, hv = X
        return a * np.log(kv) + b * hv + c
    popt, _ = optimize.curve_fit(combo, (k, H), A, p0=[0.3, 0.0, 0.0])
    r = r2(A, combo((k, H), *popt))
    print(f"  fit: A = {popt[0]:+.4f}·log(k) + {popt[1]:+.4f}·H + {popt[2]:+.4f}    R² = {r:.4f}")


# ── Plot ──────────────────────────────────────────────────────────────────────

def plot_results(df, fits):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    shape_colors = {"uniform": "#1f77b4", "mild_skew": "#ff7f0e", "strong_skew": "#d62728"}

    # Panel 1: A_ν vs k per shape
    ax = axes[0][0]
    for shape, col in shape_colors.items():
        s = fits[fits["shape"] == shape].sort_values("k")
        ax.plot(s["k"], s["A_nu"], "o-", color=col, label=shape, markersize=7)
    # Stage 6 reference (uniform)
    kk = np.linspace(2, 12, 100)
    ax.plot(kk, 0.304 * np.log(kk), color="black", linestyle="--",
            linewidth=1.5, alpha=0.7, label="Stage 6: 0.30·log(k)")
    ax.set_xlabel("k (alphabet size)")
    ax.set_ylabel(r"$A_\nu$ (slope of $\nu - \nu_0$ vs $1/\lambda_{tp}$)")
    ax.set_title(r"$A_\nu(k)$ by shape — do the lines overlap?")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=9)

    # Panel 2: A_a vs k per shape
    ax = axes[0][1]
    for shape, col in shape_colors.items():
        s = fits[fits["shape"] == shape].sort_values("k")
        ax.plot(s["k"], s["A_a"], "s-", color=col, label=shape, markersize=7)
    ax.axhline(0, color="green", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("k")
    ax.set_ylabel(r"$B_a$ (slope of $a - 1$ vs $1/\lambda_{tp}$)")
    ax.set_title(r"$B_a(k)$ by shape")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=9)

    # Panel 3: A_ν vs entropy H
    ax = axes[1][0]
    for shape, col in shape_colors.items():
        s = fits[fits["shape"] == shape].sort_values("entropy")
        ax.scatter(s["entropy"], s["A_nu"], color=col, s=80,
                   label=shape, edgecolors="k", linewidths=0.5)
        # Annotate with k
        for _, row in s.iterrows():
            ax.annotate(f"k={int(row['k'])}", (row["entropy"], row["A_nu"]),
                        fontsize=7, alpha=0.7, xytext=(4, 3), textcoords="offset points")
    # Fit pooled A vs H
    H = fits["entropy"].values
    A = fits["A_nu"].values
    fit_H = np.polyfit(H, A, 1)
    Hp = np.linspace(H.min(), H.max(), 100)
    ax.plot(Hp, np.polyval(fit_H, Hp), "k--", linewidth=1.5, alpha=0.7,
            label=f"linear: A = {fit_H[0]:+.3f}·H + {fit_H[1]:+.3f}")
    ax.set_xlabel(r"marginal entropy $H(p)$ (bits)")
    ax.set_ylabel(r"$A_\nu$")
    ax.set_title(r"$A_\nu$ vs $H(p)$ — does entropy collapse everything?")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=9)

    # Panel 4: residuals from log(k) fit, coloured by shape
    ax = axes[1][1]
    k_arr = fits["k"].values.astype(float)
    A_arr = fits["A_nu"].values
    # Fit pooled across all shapes: A = c · log(k)
    c_logk, _ = optimize.curve_fit(lambda kv, c: c * np.log(kv), k_arr, A_arr, p0=[0.3])
    pred = c_logk[0] * np.log(k_arr)
    for shape, col in shape_colors.items():
        m = fits["shape"] == shape
        ax.scatter(fits.loc[m, "k"], A_arr[m] - pred[m],
                   color=col, s=80, label=shape, edgecolors="k", linewidths=0.5)
    ax.axhline(0, color="red", linewidth=1.2)
    ax.set_xlabel("k")
    ax.set_ylabel(r"residual: $A_\nu - $" + f"{c_logk[0]:.3f}·log(k)")
    ax.set_title(f"Residual from pooled A = {c_logk[0]:.3f}·log(k) fit\n"
                 f"non-zero clustering by shape ⇒ shape matters beyond k")
    ax.grid(True, alpha=0.2); ax.legend(fontsize=9)

    fig.suptitle(
        r"Stage 7: does $A_\nu \approx 0.30 \log(k)$ hold for non-uniform marginals?",
        fontsize=13
    )
    plt.tight_layout()
    out = os.path.join(OUT, "shape_scaling.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {out}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)
    k_values = list(range(2, 13))
    shapes = ["uniform", "mild_skew", "strong_skew"]

    print(f"Bootstrap K={K_BOOTSTRAP}, k ∈ {k_values}, shapes = {shapes}\n")
    df = generate_data(k_values, shapes, K_BOOTSTRAP, rng)
    df.to_csv(os.path.join(OUT, "shape_scaling_data.csv"), index=False)
    print(f"\nGenerated {len(df)} data points.\n")

    fits = fit_per_k_shape(df)
    fits.to_csv(os.path.join(OUT, "shape_scaling_fits.csv"), index=False)
    print("=== Per (k, shape) fits ===")
    print(fits.to_string(index=False))

    fit_models(fits)
    plot_results(df, fits)


if __name__ == "__main__":
    main()
