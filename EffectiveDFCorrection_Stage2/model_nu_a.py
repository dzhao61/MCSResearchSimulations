"""
Stage 2: Fit ν_eff(λ) and a(λ) as closed-form functions of λ = N·p².

Theoretical motivation
----------------------
T = 2N·I under H₀ has:
  E[T]   = 1 + f(p)/N + O(N⁻²)
  Var[T] = 2 + g(p)/N + O(N⁻²)

For small p the rarest cell (1,1) dominates with probability π₁₁ = p², giving:
  f(p) ≈ 1/p²  →  E[T] ≈ 1 + 1/(N·p²) = 1 + 1/λ
  g(p) ≈ C/p²  →  Var[T] ≈ 2 + C/λ

So the leading-order models for ν and a are both of the form 1 + const/λ.
We try several generalisations to check goodness of fit:

  M1 (1-param, theory):    1 + A/λ
  M2 (2-param, power):     1 + A/λ^γ          (γ=1 recovers M1)
  M3 (2-param, shifted):   1 + A/(λ + B)       (avoids λ→0 singularity)
  M4 (2-param, 2nd order): 1 + A/λ + B/λ²     (next asymptotic term)

Fitting is restricted to λ ∈ [LAM_LO, LAM_HI] where the chi²(ν) family is
appropriate and the curves collapse cleanly.
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

# ── Fitting regime ────────────────────────────────────────────────────────────
LAM_LO = 0.5    # below this: point-mass regime, chi²(ν) is wrong family
LAM_HI = 50.0   # above this: correction is trivial (ν≈1, a≈1)


# ── Bootstrap ─────────────────────────────────────────────────────────────────

def bootstrap_moments(p, N, K, rng):
    """Return (mu, sigma2) of T = 2N·I in nats via JIDT."""
    calc = MICalcDiscrete(2)
    T = np.empty(K)
    for s in range(K):
        x = (rng.random(N) < p).astype(int)
        y = (rng.random(N) < p).astype(int)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mi_bits = float(calc.computeAverageLocalOfObservations())
        T[s] = 2 * N * mi_bits * np.log(2)     # nats
    return float(T.mean()), float(T.var(ddof=1))


# ── Candidate models ──────────────────────────────────────────────────────────
# All have asymptote 1 as λ→∞ (correct for both ν and a).

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
    """Fit func to (lam, y) data, return (params, r2)."""
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

def generate_data(p_values, N_values, K, rng):
    rows = []
    for p in p_values:
        for N in N_values:
            lam = N * p**2
            print(f"  p={p}, N={N:4d}, λ={lam:.3f} ...", flush=True)
            mu, sigma2 = bootstrap_moments(p, N, K, rng)
            nu  = 2 * mu**2 / sigma2
            a   = sigma2 / (2 * mu)
            rows.append(dict(p=p, N=N, lam=lam, mu=mu, sigma2=sigma2, nu=nu, a=a))
    return pd.DataFrame(rows)


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_fits(df, fits_nu, fits_a):
    lam_curve = np.logspace(np.log10(LAM_LO * 0.9), np.log10(LAM_HI * 1.5), 300)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors_model = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3"]
    p_colors = cm.viridis(np.linspace(0.1, 0.9, df["p"].nunique()))

    for col_idx, (target, fits, ylabel, title) in enumerate([
        ("nu",  fits_nu, r"$\nu_{eff}$",   r"$\nu_{eff}$ vs $\lambda$"),
        ("a",   fits_a,  "Scale factor $a$", r"$a$ vs $\lambda$"),
    ]):
        ax_data = axes[0][col_idx]
        ax_res  = axes[1][col_idx]

        # ── Scatter: data points coloured by p
        for (p_val, grp), col in zip(df.groupby("p"), p_colors):
            ax_data.scatter(grp["lam"], grp[target], color=col, s=30,
                            zorder=5, label=f"p={p_val}")

        # ── Fitted curves
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
                        label="χ²(1) nominal")
        ax_data.axvspan(LAM_LO, LAM_HI, alpha=0.06, color="grey",
                        label="Fitting region")
        ax_data.set_xscale("log")
        ax_data.set_xlabel(r"$\lambda = N \cdot p^2$", fontsize=11)
        ax_data.set_ylabel(ylabel, fontsize=11)
        ax_data.set_title(title, fontsize=12, fontweight="bold")
        ax_data.legend(fontsize=7, loc="upper right")
        ax_data.grid(True, alpha=0.2, linestyle="--")

        # ── Residual plot (best model)
        if best_name:
            func = MODELS[best_name][0]
            popt = fits[best_name][0]
            df_fit = df[(df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)]
            resid = df_fit[target] - func(df_fit["lam"].values, *popt)
            ax_res.scatter(df_fit["lam"], resid, s=25, color="#333333", zorder=5)
            ax_res.axhline(0, color="red", linewidth=1.2)
            ax_res.set_xscale("log")
            ax_res.set_xlabel(r"$\lambda = N \cdot p^2$", fontsize=11)
            ax_res.set_ylabel("Residual", fontsize=11)
            ax_res.set_title(f"Residuals: best model = {best_name}", fontsize=11)
            ax_res.grid(True, alpha=0.2, linestyle="--")

    fig.suptitle(
        r"Fitting $\nu_{eff}(\lambda)$ and $a(\lambda)$ — shaded = fitting region"
        f"\nλ ∈ [{LAM_LO}, {LAM_HI}]",
        fontsize=13
    )
    plt.tight_layout()
    plt.savefig("model_fits.png", dpi=150, bbox_inches="tight")
    print("Saved: model_fits.png")
    plt.show()


def print_summary(fits_nu, fits_a):
    print("\n=== Model fit summary ===")
    print(f"{'Model':<26}  {'R²(ν)':>8}  {'R²(a)':>8}  {'params(ν)'}")
    print("-" * 65)
    for name in MODELS:
        popt_nu, r2_nu = fits_nu.get(name, (None, np.nan))
        popt_a,  r2_a  = fits_a.get(name,  (None, np.nan))
        param_str = str([f"{v:.4f}" for v in popt_nu]) if popt_nu is not None else "failed"
        print(f"{name:<26}  {r2_nu:>8.5f}  {r2_a:>8.5f}  {param_str}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)

    p_values = [0.5, 0.3, 0.2, 0.1, 0.07, 0.05, 0.03, 0.02, 0.01]
    N_values = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000]
    K = 3_000   # bootstrap samples per (p, N) point

    print("Generating data grid...")
    df = generate_data(p_values, N_values, K, rng)
    df.to_csv("nu_a_data.csv", index=False)
    print(f"\nGenerated {len(df)} data points. Saved: nu_a_data.csv")
    print(df[["p", "N", "lam", "mu", "sigma2", "nu", "a"]].round(4).to_string())

    # Filter to fitting regime
    mask = (df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)
    df_fit = df[mask]
    lam_fit = df_fit["lam"].values
    print(f"\nFitting on {mask.sum()} points with λ ∈ [{LAM_LO}, {LAM_HI}]")

    # Fit all models for ν and a
    fits_nu, fits_a = {}, {}
    for name, (func, p0) in MODELS.items():
        fits_nu[name] = fit_model(func, p0, lam_fit, df_fit["nu"].values)
        fits_a[name]  = fit_model(func, p0, lam_fit, df_fit["a"].values)

    print_summary(fits_nu, fits_a)
    plot_fits(df, fits_nu, fits_a)


if __name__ == "__main__":
    main()
