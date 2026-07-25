"""
Stage 8: Robust formula for A_ν(k, skew) via a dense (k, shape, N) grid.

Design:
  - 8 marginal shape families (uniform, four levels of one-rare skew, plus
    two-rare bimodal, Zipf, and geometric decay) covering k·min(p) from ~0.05
    to 1.0.
  - k ∈ {3, 4, ..., 15} (13 alphabet sizes).
  - For each (k, shape) sweep N to cover λ_min ∈ [0.1, 30].
  - K = 5000 bootstrap surrogates per config, using vectorised numpy
    multinomial sampling + vectorised MI (no JIDT-per-sample loop).

Analysis:
  - Per (k, shape): fit ν − ν₀ = A_ν/λ_tp and a − 1 = B_a/λ_tp.
  - Fit A_ν = f(k, descriptor) and B_a = f(k, descriptor) for several
    descriptors and functional forms.
  - Leave-one-shape-out cross-validation to check robustness.
"""

import os
import time
import itertools
import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
K_BOOTSTRAP = 5_000
LAM_LO, LAM_HI = 0.5, 5.0


# ── Vectorised MI bootstrap (no JIDT) ─────────────────────────────────────────

def bootstrap_moments(p_X, p_Y, N, K, rng):
    pi = np.outer(p_X, p_Y).flatten()
    counts = rng.multinomial(N, pi, size=K)
    k_X, k_Y = len(p_X), len(p_Y)
    P = counts.reshape(K, k_X, k_Y) / N
    px = P.sum(axis=2, keepdims=True)
    py = P.sum(axis=1, keepdims=True)
    denom = np.maximum(px * py, 1e-300)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_term = np.where((P > 0) & (px * py > 0),
                            np.log2(P / denom), 0.0)
    mi_bits = (P * log_term).sum(axis=(1, 2))
    T = 2 * N * mi_bits * np.log(2)
    return float(T.mean()), float(T.var(ddof=1))


# ── Shape families ───────────────────────────────────────────────────────────

def make_marginal(k, shape):
    if shape == "uniform":
        return np.full(k, 1.0 / k)
    if shape.startswith("one_rare_"):
        # one_rare_X: rarest state = X/k, rest equal
        # k·min(p) = X
        ratio = float(shape.split("_")[-1])
        p_rare = ratio / k
        return np.concatenate([[p_rare], np.full(k - 1, (1 - p_rare) / (k - 1))])
    if shape == "two_rare":
        # two rare states each at 0.3/k, rest equal → k·min(p) = 0.3
        if k < 4:
            return None
        p_rare = 0.3 / k
        rest = (1 - 2 * p_rare) / (k - 2)
        return np.concatenate([[p_rare, p_rare], np.full(k - 2, rest)])
    if shape == "zipf":
        # p_i ∝ 1/i
        ranks = np.arange(1, k + 1)
        p = 1.0 / ranks
        return p / p.sum()
    if shape == "geometric":
        # p_i ∝ 0.6^i
        ranks = np.arange(k)
        p = 0.6 ** ranks
        return p / p.sum()
    raise ValueError(shape)


SHAPES = [
    "uniform",
    "one_rare_0.8",
    "one_rare_0.5",
    "one_rare_0.2",
    "one_rare_0.05",
    "two_rare",
    "zipf",
    "geometric",
]


# ── Descriptors ──────────────────────────────────────────────────────────────

def descriptors(p):
    p_pos = p[p > 0]
    H = float(-np.sum(p_pos * np.log2(p_pos)))
    k = len(p)
    pmin = float(p.min())
    return dict(
        H=H,
        H_norm=H / np.log2(k) if k > 1 else 1.0,
        perp=2.0 ** H,
        perp_n=(2.0 ** H) / k,
        simpson=1.0 / float(np.sum(p ** 2)),
        simpson_n=(1.0 / float(np.sum(p ** 2))) / k,
        k_min_p=k * pmin,
        log_k_min_p=np.log(k * pmin),
    )


# ── Data generation ──────────────────────────────────────────────────────────

def generate_data(k_values, K, rng):
    rows = []
    t0 = time.time()
    lam_targets = np.unique(np.round(np.concatenate([
        np.logspace(np.log10(0.1), np.log10(0.5),  4),
        np.logspace(np.log10(0.5), np.log10(5.0), 12),
        np.logspace(np.log10(5.0), np.log10(30.0), 4),
    ]), 3))

    cfg_idx = 0
    n_configs_est = 0
    for k in k_values:
        for shape in SHAPES:
            p = make_marginal(k, shape)
            if p is None:
                continue
            pi_min = p.min() * p.min()
            Ns = sorted(set(int(round(L / pi_min)) for L in lam_targets
                            if L / pi_min >= 10))
            n_configs_est += len(Ns)
    print(f"Estimated {n_configs_est} configs total\n")

    for k in k_values:
        nu0 = (k - 1) ** 2
        for shape in SHAPES:
            p = make_marginal(k, shape)
            if p is None:
                continue
            desc = descriptors(p)
            pi_min = p.min() * p.min()
            sum_inv_pi = float(np.sum(1.0 / np.outer(p, p)))
            Ns = sorted(set(int(round(L / pi_min)) for L in lam_targets
                            if L / pi_min >= 10))
            for N in Ns:
                lam_min = N * pi_min
                lam_tp = N / sum_inv_pi
                t_start = time.time()
                mu, sigma2 = bootstrap_moments(p, p, N, K, rng)
                dt = time.time() - t_start
                nu = 2 * mu**2 / sigma2 if sigma2 > 0 else np.nan
                a  = sigma2 / (2 * mu)  if mu > 0     else np.nan
                cfg_idx += 1
                if cfg_idx % 20 == 0 or cfg_idx == 1:
                    elapsed = time.time() - t0
                    rate = cfg_idx / elapsed
                    eta = (n_configs_est - cfg_idx) / rate if rate > 0 else 0
                    print(f"  [{cfg_idx:4d}/{n_configs_est}] "
                          f"k={k:2d} {shape:<16} N={N:7d}  λ_min={lam_min:6.3f}  "
                          f"({dt:.2f}s, ETA {eta/60:.1f}min)", flush=True)
                rows.append(dict(k=k, shape=shape, nu0=nu0, N=N,
                                 lam_min=lam_min, lam_tp=lam_tp,
                                 mu=mu, sigma2=sigma2, nu=nu, a=a,
                                 **desc))
    print(f"\nTotal time: {(time.time() - t0)/60:.2f} min")
    return pd.DataFrame(rows)


# ── Per (k, shape) fit ───────────────────────────────────────────────────────

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
        first = d.iloc[0]
        rows.append(dict(
            k=k, shape=shape, n=len(d), nu0=nu0,
            A_nu=A_nu, A_a=A_a, r2_nu=r2_nu, r2_a=r2_a,
            H=first["H"], H_norm=first["H_norm"],
            perp=first["perp"], perp_n=first["perp_n"],
            simpson=first["simpson"], simpson_n=first["simpson_n"],
            k_min_p=first["k_min_p"], log_k_min_p=first["log_k_min_p"],
        ))
    return pd.DataFrame(rows).sort_values(["shape", "k"]).reset_index(drop=True)


# ── Model fitting ────────────────────────────────────────────────────────────

MODEL_FORMS = {
    "log(k)·d (mul)":          (lambda kv, dv, c: c * np.log(kv) * dv,           [0.3]),
    "log(k)·d^α (pow)":         (lambda kv, dv, c, a: c * np.log(kv) * dv ** a,   [0.3, 1.5]),
    "log(k)·d^α + b (pow+b)":   (lambda kv, dv, c, a, b: c * np.log(kv) * dv ** a + b, [0.3, 1.5, 0.0]),
    "c1·log(k) + c2·d (add)":   (lambda kv, dv, c1, c2: c1*np.log(kv) + c2*dv,    [0.3, 0.0]),
    "log(k)·(d+b) (mul+b)":     (lambda kv, dv, c, b: c * np.log(kv) * (dv + b),  [0.3, 0.0]),
    "log(k)^p·d^α":             (lambda kv, dv, c, p, a: c * np.log(kv)**p * dv**a, [0.3, 1.0, 1.5]),
}


def r2(y, yhat):
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else np.nan


def fit_models_for_target(fits, target_col, descriptors_to_try):
    """For each descriptor, fit each model form. Return ranked results."""
    results = []
    k_arr = fits["k"].values.astype(float)
    y     = fits[target_col].values
    for desc in descriptors_to_try:
        d_arr = fits[desc].values
        for name, (func, p0) in MODEL_FORMS.items():
            try:
                def wrapped(X, *args):
                    kv, dv = X
                    return func(kv, dv, *args)
                popt, _ = optimize.curve_fit(wrapped, (k_arr, d_arr), y, p0=p0, maxfev=20000)
                pred = wrapped((k_arr, d_arr), *popt)
                r = r2(y, pred)
                results.append(dict(
                    target=target_col, descriptor=desc, model=name,
                    params=[float(v) for v in popt], r2=r
                ))
            except Exception:
                pass
    return sorted(results, key=lambda x: -x["r2"])


def loo_shape_cv(fits, target_col, desc, model_form):
    """Leave-one-shape-out cross-validation. Returns dict shape → held-out R²."""
    func, p0 = MODEL_FORMS[model_form]
    cv = {}
    for held_shape in fits["shape"].unique():
        train = fits[fits["shape"] != held_shape]
        test  = fits[fits["shape"] == held_shape]
        if len(test) < 2:
            continue
        try:
            def wrapped(X, *args):
                kv, dv = X
                return func(kv, dv, *args)
            popt, _ = optimize.curve_fit(
                wrapped,
                (train["k"].values.astype(float), train[desc].values),
                train[target_col].values, p0=p0, maxfev=20000
            )
            pred = wrapped((test["k"].values.astype(float), test[desc].values), *popt)
            r = r2(test[target_col].values, pred)
            cv[held_shape] = r
        except Exception:
            cv[held_shape] = np.nan
    return cv


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_summary(fits, best_nu, best_a):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    shape_colors = dict(zip(SHAPES, plt.cm.tab10.colors))

    # Panel 1: A_ν observed vs predicted under best model
    desc_nu = best_nu["descriptor"]
    func_nu, _ = MODEL_FORMS[best_nu["model"]]
    pred_nu = func_nu(fits["k"].values.astype(float),
                      fits[desc_nu].values, *best_nu["params"])
    ax = axes[0][0]
    for shape, col in shape_colors.items():
        m = fits["shape"] == shape
        if m.sum() == 0: continue
        ax.scatter(fits.loc[m, "A_nu"], pred_nu[m], color=col, s=80,
                   label=shape, edgecolors="k", linewidths=0.4)
    lims = [min(fits["A_nu"].min(), pred_nu.min()),
            max(fits["A_nu"].max(), pred_nu.max())]
    ax.plot(lims, lims, "k--", linewidth=1)
    ax.set_xlabel("observed $A_\\nu$"); ax.set_ylabel("predicted $A_\\nu$")
    ax.set_title(f"$A_\\nu$ — best: {best_nu['model']}, desc={desc_nu}\n"
                 f"R² = {best_nu['r2']:.4f}")
    ax.legend(fontsize=7, loc="upper left"); ax.grid(True, alpha=0.2)

    # Panel 2: B_a observed vs predicted
    desc_a = best_a["descriptor"]
    func_a, _ = MODEL_FORMS[best_a["model"]]
    pred_a = func_a(fits["k"].values.astype(float),
                    fits[desc_a].values, *best_a["params"])
    ax = axes[0][1]
    for shape, col in shape_colors.items():
        m = fits["shape"] == shape
        if m.sum() == 0: continue
        ax.scatter(fits.loc[m, "A_a"], pred_a[m], color=col, s=80,
                   label=shape, edgecolors="k", linewidths=0.4)
    lims = [min(fits["A_a"].min(), pred_a.min()),
            max(fits["A_a"].max(), pred_a.max())]
    ax.plot(lims, lims, "k--", linewidth=1)
    ax.set_xlabel("observed $B_a$"); ax.set_ylabel("predicted $B_a$")
    ax.set_title(f"$B_a$ — best: {best_a['model']}, desc={desc_a}\n"
                 f"R² = {best_a['r2']:.4f}")
    ax.legend(fontsize=7, loc="upper left"); ax.grid(True, alpha=0.2)

    # Panel 3: A_ν vs k by shape (with model curves overlaid)
    ax = axes[1][0]
    kk = np.linspace(3, fits["k"].max(), 100)
    for shape, col in shape_colors.items():
        s = fits[fits["shape"] == shape].sort_values("k")
        if len(s) == 0: continue
        ax.plot(s["k"], s["A_nu"], "o-", color=col, label=shape, markersize=6)
        # Overlay model
        d_val = s[desc_nu].iloc[0]  # constant per shape (within mild dependence)
        ax.plot(kk, func_nu(kk, np.full_like(kk, d_val), *best_nu["params"]),
                color=col, linestyle="--", alpha=0.5)
    ax.set_xlabel("k"); ax.set_ylabel("$A_\\nu$")
    ax.set_title(f"$A_\\nu(k)$ by shape (lines = model)")
    ax.legend(fontsize=7); ax.grid(True, alpha=0.2)

    # Panel 4: descriptor value vs A_ν, all (k, shape) — global view
    ax = axes[1][1]
    sc = ax.scatter(fits[desc_nu], fits["A_nu"], c=fits["k"],
                    cmap="viridis", s=80, edgecolors="k", linewidths=0.4)
    plt.colorbar(sc, ax=ax, label="k")
    ax.set_xlabel(desc_nu); ax.set_ylabel("$A_\\nu$")
    ax.set_title(f"$A_\\nu$ vs {desc_nu} (colour = k)")
    ax.grid(True, alpha=0.2)

    fig.suptitle("Stage 8: robust 2D formula for $A_\\nu$ and $B_a$",
                 fontsize=13)
    plt.tight_layout()
    out = os.path.join(OUT, "robust_fit.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)
    k_values = list(range(3, 16))

    print(f"Stage 8: bootstrap K={K_BOOTSTRAP}, shapes = {SHAPES}, k ∈ {k_values}\n")
    df = generate_data(k_values, K_BOOTSTRAP, rng)
    df.to_csv(os.path.join(OUT, "robust_fit_data.csv"), index=False)
    print(f"\nGenerated {len(df)} data points.")

    fits = fit_per_k_shape(df)
    fits.to_csv(os.path.join(OUT, "robust_fit_per_k_shape.csv"), index=False)
    print(f"\n{len(fits)} (k, shape) fit rows.")
    print("\n=== Per (k, shape) fit quality (R² of underlying 1/λ_tp fit) ===")
    for shape in SHAPES:
        s = fits[fits["shape"] == shape]
        if len(s) > 0:
            print(f"  {shape:<16}: n={len(s):2d}, mean R²(ν) = {s['r2_nu'].mean():.3f}, "
                  f"mean R²(a) = {s['r2_a'].mean():.3f}")

    descriptors_to_try = ["H_norm", "perp_n", "simpson_n", "k_min_p"]

    print("\n=== Best models for A_ν ===")
    ranked_nu = fit_models_for_target(fits, "A_nu", descriptors_to_try)
    for r in ranked_nu[:10]:
        print(f"  R²={r['r2']:.4f}  desc={r['descriptor']:<10}  "
              f"model={r['model']:<28}  params={[f'{v:+.4f}' for v in r['params']]}")

    print("\n=== Best models for B_a ===")
    ranked_a = fit_models_for_target(fits, "A_a", descriptors_to_try)
    for r in ranked_a[:10]:
        print(f"  R²={r['r2']:.4f}  desc={r['descriptor']:<10}  "
              f"model={r['model']:<28}  params={[f'{v:+.4f}' for v in r['params']]}")

    best_nu = ranked_nu[0]
    best_a  = ranked_a[0]

    print(f"\n=== Leave-one-shape-out CV on best A_ν model ({best_nu['model']}, "
          f"{best_nu['descriptor']}) ===")
    cv = loo_shape_cv(fits, "A_nu", best_nu["descriptor"], best_nu["model"])
    for shape, r in cv.items():
        print(f"  held-out {shape:<16}: R² = {r:+.4f}")

    print(f"\n=== Leave-one-shape-out CV on best B_a model ({best_a['model']}, "
          f"{best_a['descriptor']}) ===")
    cv = loo_shape_cv(fits, "A_a", best_a["descriptor"], best_a["model"])
    for shape, r in cv.items():
        print(f"  held-out {shape:<16}: R² = {r:+.4f}")

    plot_summary(fits, best_nu, best_a)


if __name__ == "__main__":
    main()
