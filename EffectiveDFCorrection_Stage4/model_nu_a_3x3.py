"""
Stage 4: Does the Stage 2/3 framework generalise to 3×3 contingency tables?

Same machinery as Stage 3 (Welch-Satterthwaite moment-matching, M1–M4 fit
on λ ∈ [0.5, 5]) but the alphabet is now |X|=|Y|=3.

Key differences from binary:
  - JIDT MICalcDiscrete(3)
  - Marginals are 3-vectors: p_X = (p_X[0], p_X[1], p_X[2])
  - Nominal df is ν₀ = (k-1)² = 4 → χ²(4), not χ²(1)
  - We fit ν_eff / ν₀ (normalised) so the same M1–M4 with asymptote 1 apply,
    and the fitted A coefficients are directly comparable to Stage 2/3.
  - λ = N · min(p_X) · min(p_Y)   (rarest expected cell count)

Grid uses symmetric "rare-pair-plus-bulk" marginals p_X = p_Y = (p, p, 1-2p),
so the rarest cells (there are FOUR equal-prob rarest cells: (0,0), (0,1),
(1,0), (1,1)) each have expected count Np² = λ. This is a direct analogue of
the binary case where there is ONE rarest cell at Np².
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

# ── Setup ─────────────────────────────────────────────────────────────────────
K_ALPHABET = 3
NU0 = (K_ALPHABET - 1) ** 2      # = 4 for 3×3

LAM_LO = 0.5
LAM_HI = 5.0

LOG_SCALE = True


# ── Bootstrap ─────────────────────────────────────────────────────────────────

def bootstrap_moments(p_X, p_Y, N, K, rng):
    """Return (mu, sigma2) of T = 2N·I in nats. p_X, p_Y are length-3 prob vectors."""
    calc = MICalcDiscrete(K_ALPHABET)
    T = np.empty(K)
    for s in range(K):
        x = rng.choice(K_ALPHABET, size=N, p=p_X)
        y = rng.choice(K_ALPHABET, size=N, p=p_Y)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mi_bits = float(calc.computeAverageLocalOfObservations())
        T[s] = 2 * N * mi_bits * np.log(2)
    return float(T.mean()), float(T.var(ddof=1))


# ── Candidate models (asymptote 1 since we fit ν/ν₀) ──────────────────────────

def m1(lam, A):           return 1 + A / lam
def m2(lam, A, gamma):    return 1 + A / lam**gamma
def m3(lam, A, B):        return 1 + A / (lam + B)
def m4(lam, A, B):        return 1 + A / lam + B / lam**2

MODELS = {
    "M1: 1 + A/λ":         (m1, [1.0]),
    "M2: 1 + A/λ^γ":       (m2, [1.0, 0.8]),
    "M3: 1 + A/(λ+B)":     (m3, [1.0, 0.5]),
    "M4: 1 + A/λ + B/λ²":  (m4, [1.0, 0.1]),
}


def fit_model(func, p0, lam, y):
    try:
        popt, _ = optimize.curve_fit(func, lam, y, p0=p0, maxfev=10000)
        y_pred = func(lam, *popt)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - y.mean())**2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
        return popt, r2
    except Exception:
        return None, np.nan


# ── Data generation ───────────────────────────────────────────────────────────

def symmetric_marginal(p):
    """Returns the 3-vector (p, p, 1-2p) for p ∈ (0, 1/3]."""
    if p > 1/3 + 1e-9:
        raise ValueError(f"p={p} > 1/3 not allowed for symmetric marginal")
    return np.array([p, p, 1 - 2*p])


def make_grid():
    """
    Symmetric grid: p_X = p_Y = (p, p, 1-2p), sweep p and N.
    Rarest cells (0,0), (0,1), (1,0), (1,1) each have expected count Np².
    """
    p_values = [1/3, 0.25, 0.15, 0.10, 0.05, 0.03]
    N_values = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 1500, 2500, 5000]
    return p_values, N_values


def generate_data(p_values, N_values, K, rng):
    rows = []
    for p in p_values:
        marg = symmetric_marginal(p)
        for N in N_values:
            lam = N * marg.min() * marg.min()
            if lam < 0.02 or lam > 30:
                continue   # outside the range of interest
            print(f"  p={p:.4f}, marg=({marg[0]:.3f},{marg[1]:.3f},{marg[2]:.3f}), "
                  f"N={N:5d}, λ={lam:.3f} ...", flush=True)
            mu, sigma2 = bootstrap_moments(marg, marg, N, K, rng)
            nu  = 2 * mu**2 / sigma2 if sigma2 > 0 else np.nan
            a   = sigma2 / (2 * mu)  if mu > 0     else np.nan
            rows.append(dict(
                p=p, p0=marg[0], p1=marg[1], p2=marg[2],
                N=N, lam=lam, mu=mu, sigma2=sigma2,
                nu=nu, a=a, nu_norm=nu / NU0
            ))
    return pd.DataFrame(rows)


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_fits(df, fits_nu, fits_a):
    lam_curve = (np.logspace(np.log10(LAM_LO * 0.9), np.log10(LAM_HI * 1.5), 300)
                 if LOG_SCALE else
                 np.linspace(LAM_LO * 0.9, LAM_HI * 1.5, 300))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors_model = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3"]
    p_colors = cm.viridis(np.linspace(0.1, 0.9, df["p"].nunique()))

    for col_idx, (target, fits, ylabel, title) in enumerate([
        ("nu_norm", fits_nu, r"$\nu_{eff} / \nu_0$",
         r"$\nu_{eff} / \nu_0$ vs $\lambda$  ($\nu_0 = (k-1)^2 = 4$)"),
        ("a",      fits_a,  "Scale factor $a$", r"$a$ vs $\lambda$"),
    ]):
        ax_data = axes[0][col_idx]
        ax_res  = axes[1][col_idx]

        for (p_val, grp), col in zip(df.groupby("p"), p_colors):
            ax_data.scatter(grp["lam"], grp[target], color=col, s=30,
                            zorder=5, label=f"p={p_val:.3g}")

        best_r2, best_name = -np.inf, None
        for (name, (popt, r2)), col in zip(fits.items(), colors_model):
            if popt is None:
                continue
            func = MODELS[name][0]
            y_curve = func(lam_curve, *popt)
            ax_data.plot(lam_curve, y_curve, color=col, linewidth=1.8,
                         label=f"{name}  R²={r2:.4f}")
            if r2 > best_r2:
                best_r2, best_name = r2, name

        ax_data.axhline(1.0, color="green", linestyle="--", linewidth=1.2,
                        label=r"nominal $\chi^2(\nu_0)$")
        ax_data.axvspan(LAM_LO, LAM_HI, alpha=0.06, color="grey",
                        label="Fitting region")
        if LOG_SCALE:
            ax_data.set_xscale("log")
        ax_data.set_ylabel(ylabel, fontsize=11)
        ax_data.set_title(title, fontsize=12, fontweight="bold")
        ax_data.legend(fontsize=7, loc="upper right")
        ax_data.grid(True, alpha=0.2, linestyle="--")

        if best_name:
            func = MODELS[best_name][0]
            popt = fits[best_name][0]
            df_fit = df[(df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)]
            resid = df_fit[target] - func(df_fit["lam"].values, *popt)
            ax_res.scatter(df_fit["lam"], resid, s=25, color="#333333", zorder=5)
            ax_res.axhline(0, color="red", linewidth=1.2)
            if LOG_SCALE:
                ax_res.set_xscale("log")
            ax_res.set_xlabel(r"$\lambda = N \cdot \min(p_X) \cdot \min(p_Y)$", fontsize=11)
            ax_res.set_ylabel("Residual", fontsize=11)
            ax_res.set_title(f"Residuals: best model = {best_name}", fontsize=11)
            ax_res.grid(True, alpha=0.2, linestyle="--")

    fig.suptitle(
        r"Stage 4 (3×3): fitting $\nu_{eff}/\nu_0$ and $a$"
        f"\nλ ∈ [{LAM_LO}, {LAM_HI}], symmetric marginals $(p, p, 1-2p)$",
        fontsize=13
    )
    plt.tight_layout()
    plt.savefig("model_fits_3x3.png", dpi=150, bbox_inches="tight")
    print("Saved: model_fits_3x3.png")
    plt.show()


def print_summary(fits_nu, fits_a, stage_compare):
    print("\n=== Stage 4 (3×3) model fit summary ===")
    print(f"{'Model':<24}  {'R²(ν/ν₀)':>9}  {'R²(a)':>8}  "
          f"{'params(ν/ν₀)':<30}  {'params(a)'}")
    print("-" * 110)
    for name in MODELS:
        popt_nu, r2_nu = fits_nu.get(name, (None, np.nan))
        popt_a,  r2_a  = fits_a.get(name,  (None, np.nan))
        p_nu = ", ".join(f"{v:+.4f}" for v in popt_nu) if popt_nu is not None else "failed"
        p_a  = ", ".join(f"{v:+.4f}" for v in popt_a)  if popt_a  is not None else "failed"
        print(f"{name:<24}  {r2_nu:>9.5f}  {r2_a:>8.5f}  {p_nu:<30}  {p_a}")
    if stage_compare:
        print()
        print("Stage 3 (binary, λ ∈ [0.5, 5]) for comparison:")
        for line in stage_compare:
            print("  " + line)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)

    p_values, N_values = make_grid()
    K = 3_000

    print(f"Bootstrap K={K} samples per config")
    print(f"Grid: {len(p_values)} p values × {len(N_values)} N values "
          f"(configs with λ ∉ [0.02, 30] skipped)\n")

    df = generate_data(p_values, N_values, K, rng)
    df.to_csv("nu_a_data_3x3.csv", index=False)
    print(f"\nGenerated {len(df)} data points. Saved: nu_a_data_3x3.csv")

    mask = (df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)
    df_fit = df[mask]
    lam_fit = df_fit["lam"].values
    print(f"\nFitting on {mask.sum()} points with λ ∈ [{LAM_LO}, {LAM_HI}]")

    fits_nu, fits_a = {}, {}
    for name, (func, p0) in MODELS.items():
        fits_nu[name] = fit_model(func, p0, lam_fit, df_fit["nu_norm"].values)
        fits_a[name]  = fit_model(func, p0, lam_fit, df_fit["a"].values)

    stage3 = [
        "M1: 1 + A/λ            R²(ν)=0.633  A_ν=+0.4524    R²(a)=0.601  A_a=-0.2006",
        "M2: 1 + A/λ^γ          R²(ν)=0.633  A_ν=+0.4526, γ=0.9985    R²(a)=0.667  A_a=-0.1680, γ=1.5361",
    ]
    print_summary(fits_nu, fits_a, stage3)
    plot_fits(df, fits_nu, fits_a)


if __name__ == "__main__":
    main()
