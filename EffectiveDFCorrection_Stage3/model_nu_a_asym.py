"""
Stage 3: Fit ν_eff(λ) and a(λ) when p_X ≠ p_Y (asymmetric marginals).

Same machinery as Stage 2 (M1–M4 candidate models, Welch-Satterthwaite
moment-matching, fitting on λ ∈ [LAM_LO, LAM_HI]) but the bootstrap now
draws X and Y from independent Bernoullis with separate biases:

    x ~ Bernoulli(p_X)
    y ~ Bernoulli(p_Y)

λ is defined as the rarest expected cell count:
    λ = N · p_X · p_Y     (for p_X, p_Y ≤ 0.5)

Open question: does the ν(λ), a(λ) collapse from Stage 2 still hold when
p_X ≠ p_Y, or do the curves branch by asymmetry ratio r = p_X / p_Y?
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
# Target region = descending side of the ν peak (peak sits at λ ≈ 0.5).
# Beyond λ ≈ 5 the correction is trivial (ν ≈ a ≈ 1).
LAM_LO = 0.5
LAM_HI = 5.0

LOG_SCALE = True


# ── Bootstrap (only line that materially differs from Stage 2) ────────────────

def bootstrap_moments(p_X, p_Y, N, K, rng):
    """Return (mu, sigma2) of T = 2N·I in nats via JIDT, with p_X ≠ p_Y."""
    calc = MICalcDiscrete(2)
    T = np.empty(K)
    for s in range(K):
        x = (rng.random(N) < p_X).astype(int)
        y = (rng.random(N) < p_Y).astype(int)
        calc.initialise()
        calc.addObservations(JArray(JInt)(x.tolist()), JArray(JInt)(y.tolist()))
        mi_bits = float(calc.computeAverageLocalOfObservations())
        T[s] = 2 * N * mi_bits * np.log(2)
    return float(T.mean()), float(T.var(ddof=1))


# ── Candidate models (identical to Stage 2) ───────────────────────────────────

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


# ── Data generation: 2D (p_X, p_Y) grid ───────────────────────────────────────

def make_pair_grid():
    """
    Pairs (p_X, p_Y) chosen to span both λ AND asymmetry ratio r = p_X/p_Y.
    Restricting to p ≤ 0.5 so the rarest cell is always (1,1) → λ = N·p_X·p_Y.

    Designed to cover r ∈ {1, 2, 5, 10, 25}, with several pairs per ratio so
    that for each ratio we sweep λ via N.
    """
    base = [0.5, 0.3, 0.2, 0.1, 0.05, 0.02]
    pairs = set()
    # r = 1 (symmetric — reproduces Stage 2 as sanity check)
    for p in base:
        pairs.add((p, p))
    # r = 2
    for p in base:
        if p / 2 >= 0.005:
            pairs.add((p, p / 2))
    # r = 5
    for p in [0.5, 0.3, 0.1, 0.05]:
        if p / 5 >= 0.005:
            pairs.add((p, p / 5))
    # r = 10
    for p in [0.5, 0.3, 0.1]:
        if p / 10 >= 0.005:
            pairs.add((p, p / 10))
    # r = 25
    for p in [0.5, 0.3]:
        if p / 25 >= 0.005:
            pairs.add((p, p / 25))
    # Ensure p_X >= p_Y by convention (since the asymmetric pair (a, b) and (b, a)
    # give the same null distribution by X↔Y symmetry).
    return sorted({(max(a, b), min(a, b)) for (a, b) in pairs})


def generate_data(pairs, N_values, K, rng):
    rows = []
    for (p_X, p_Y) in pairs:
        ratio = p_X / p_Y
        for N in N_values:
            lam = N * p_X * p_Y
            print(f"  p_X={p_X:.3f}, p_Y={p_Y:.3f} (r={ratio:5.2f}), "
                  f"N={N:4d}, λ={lam:.3f} ...", flush=True)
            mu, sigma2 = bootstrap_moments(p_X, p_Y, N, K, rng)
            nu = 2 * mu**2 / sigma2
            a  = sigma2 / (2 * mu)
            rows.append(dict(p_X=p_X, p_Y=p_Y, ratio=ratio,
                             N=N, lam=lam,
                             mu=mu, sigma2=sigma2, nu=nu, a=a))
    return pd.DataFrame(rows)


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_fits(df, fits_nu, fits_a):
    lam_curve = (np.logspace(np.log10(LAM_LO * 0.9), np.log10(LAM_HI * 1.5), 300)
                 if LOG_SCALE else
                 np.linspace(LAM_LO * 0.9, LAM_HI * 1.5, 300))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors_model = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3"]

    # Colour by asymmetry ratio so we can see whether the curves branch by r.
    unique_ratios = sorted(df["ratio"].unique())
    r_colors = cm.plasma(np.linspace(0.05, 0.95, len(unique_ratios)))
    ratio_to_color = dict(zip(unique_ratios, r_colors))

    for col_idx, (target, fits, ylabel, title) in enumerate([
        ("nu",  fits_nu, r"$\nu_{eff}$",   r"$\nu_{eff}$ vs $\lambda$"),
        ("a",   fits_a,  "Scale factor $a$", r"$a$ vs $\lambda$"),
    ]):
        ax_data = axes[0][col_idx]
        ax_res  = axes[1][col_idx]

        # Scatter coloured by ratio (key diagnostic: do colours separate?)
        for r_val in unique_ratios:
            grp = df[df["ratio"] == r_val]
            ax_data.scatter(grp["lam"], grp[target],
                            color=ratio_to_color[r_val], s=30,
                            zorder=5, label=f"r={r_val:g}")

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
        if LOG_SCALE:
            ax_data.set_xscale("log")
        ax_data.set_ylabel(ylabel, fontsize=11)
        ax_data.set_title(title, fontsize=12, fontweight="bold")
        ax_data.legend(fontsize=6.5, loc="upper right", ncol=2)
        ax_data.grid(True, alpha=0.2, linestyle="--")

        if best_name:
            func = MODELS[best_name][0]
            popt = fits[best_name][0]
            df_fit = df[(df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)]
            resid = df_fit[target] - func(df_fit["lam"].values, *popt)
            for r_val in unique_ratios:
                m = df_fit["ratio"] == r_val
                ax_res.scatter(df_fit.loc[m, "lam"], resid[m],
                               color=ratio_to_color[r_val], s=25, zorder=5)
            ax_res.axhline(0, color="red", linewidth=1.2)
            if LOG_SCALE:
                ax_res.set_xscale("log")
            ax_res.set_xlabel(r"$\lambda = N \cdot p_X \cdot p_Y$", fontsize=11)
            ax_res.set_ylabel("Residual", fontsize=11)
            ax_res.set_title(f"Residuals: best model = {best_name} "
                             f"(coloured by ratio r)", fontsize=11)
            ax_res.grid(True, alpha=0.2, linestyle="--")

    fig.suptitle(
        r"Stage 3 (asymmetric): fitting $\nu_{eff}(\lambda)$ and $a(\lambda)$"
        f"\nλ ∈ [{LAM_LO}, {LAM_HI}], colour = asymmetry ratio r = $p_X/p_Y$",
        fontsize=13
    )
    plt.tight_layout()
    plt.savefig("model_fits_asym.png", dpi=150, bbox_inches="tight")
    print("Saved: model_fits_asym.png")
    plt.show()


def print_summary(fits_nu, fits_a):
    print("\n=== Model fit summary (asymmetric data) ===")
    print(f"{'Model':<26}  {'R²(ν)':>8}  {'R²(a)':>8}  {'params(ν)':<30}  {'params(a)'}")
    print("-" * 110)
    for name in MODELS:
        popt_nu, r2_nu = fits_nu.get(name, (None, np.nan))
        popt_a,  r2_a  = fits_a.get(name,  (None, np.nan))
        p_nu = ", ".join(f"{v:+.4f}" for v in popt_nu) if popt_nu is not None else "failed"
        p_a  = ", ".join(f"{v:+.4f}" for v in popt_a)  if popt_a  is not None else "failed"
        print(f"{name:<26}  {r2_nu:>8.5f}  {r2_a:>8.5f}  {p_nu:<30}  {p_a}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)

    pairs = make_pair_grid()
    N_values = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000]
    K = 3_000

    print(f"Pairs to bootstrap: {len(pairs)} × {len(N_values)} N values = "
          f"{len(pairs) * len(N_values)} configs, K={K} each\n")
    for (px, py) in pairs:
        print(f"  ({px:.3f}, {py:.3f})  r={px/py:.2f}")
    print()

    print("Generating data grid (this will take a while)...")
    df = generate_data(pairs, N_values, K, rng)
    df.to_csv("nu_a_data_asym.csv", index=False)
    print(f"\nGenerated {len(df)} data points. Saved: nu_a_data_asym.csv")

    mask = (df["lam"] >= LAM_LO) & (df["lam"] <= LAM_HI)
    df_fit = df[mask]
    lam_fit = df_fit["lam"].values
    print(f"\nFitting on {mask.sum()} points with λ ∈ [{LAM_LO}, {LAM_HI}]")

    fits_nu, fits_a = {}, {}
    for name, (func, p0) in MODELS.items():
        fits_nu[name] = fit_model(func, p0, lam_fit, df_fit["nu"].values)
        fits_a[name]  = fit_model(func, p0, lam_fit, df_fit["a"].values)

    print_summary(fits_nu, fits_a)
    plot_fits(df, fits_nu, fits_a)


if __name__ == "__main__":
    main()
