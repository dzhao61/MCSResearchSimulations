"""Post-review diagnostics; never modifies the frozen confirmatory results."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, t

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT.parent / "DifferentialMI" / "src")]
from differential_mi.statistics import plugin_mi
from welch_differential_mi.welch import differential_mi_pvalues, _combine_df


def population_moments(p):
    ell = np.log(p / (p.sum(1)[:, None] * p.sum(0)[None, :]))
    mi = float(np.sum(p * ell))
    v = float(np.sum(p * (ell - mi)**2))
    row = np.sum(p * ell, 1) / p.sum(1)
    col = np.sum(p * ell, 0) / p.sum(0)
    g = (ell - mi)**2 - v + 2 * (ell - row[:, None] - col[None, :] + mi)
    tau = float(np.sum(p * g**2))
    return mi, v, tau


def kurtosis_df(counts, v):
    p = counts / counts.sum((-2, -1))[:, None, None]
    independent = p.sum(-1)[:, :, None] * p.sum(-2)[:, None, :]
    ell = np.zeros_like(p)
    np.log(np.divide(p, independent, out=np.ones_like(p), where=p > 0), out=ell)
    mi = np.sum(p * ell, (-2, -1))
    g = (ell - mi[:, None, None])**2 - v[:, None, None]
    tau = np.sum(p * g**2, (-2, -1))
    with np.errstate(divide="ignore", invalid="ignore"):
        return 2 * counts.sum((-2, -1)) * v**2 / tau


def support_correction(counts):
    occupied = (counts > 0).sum((-2, -1))
    rows = (counts.sum(-1) > 0).sum(-1)
    cols = (counts.sum(-2) > 0).sum(-1)
    return (occupied - rows - cols + 1) / (2 * counts.sum((-2, -1)))


def simulate(config, population, replicates, phase):
    seed = int.from_bytes(hashlib.sha256(
        f"mechanism-v1:{config.configuration_id}:{phase}".encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    p, q = [np.array(json.loads(population[f"probability_{x}_json"])) for x in ("p", "q")]
    blocks = []
    for start in range(0, replicates, 1000):
        size = min(1000, replicates - start)
        a = rng.multinomial(int(config.n_p), p.ravel(), size).reshape((size, *p.shape))
        b = rng.multinomial(int(config.n_q), q.ravel(), size).reshape((size, *q.shape))
        r = differential_mi_pvalues(a, b, include_unbiased_sensitivity=False)
        vp, vq = r["influence_variance_p"], r["influence_variance_q"]
        hdf = _combine_df(vp/config.n_p, vq/config.n_q, config.n_p, config.n_q)
        hvalid = r["base_valid"] & np.isfinite(hdf) & (hdf > 0)
        hp = np.where(hvalid, 2*t.sf(np.abs(r["statistic"]), hdf), np.nan)
        dp, dq = kurtosis_df(a, vp), kurtosis_df(b, vq)
        df = _combine_df(vp/config.n_p, vq/config.n_q, dp, dq)
        valid = r["base_valid"] & np.isfinite(dp) & (dp > 0) & np.isfinite(dq) & (dq > 0) & np.isfinite(df) & (df > 0)
        kp = np.where(valid, 2*t.sf(np.abs(r["statistic"]), df), np.nan)
        ip, iq = np.asarray(plugin_mi(a)), np.asarray(plugin_mi(b))
        observed_delta = ip - support_correction(a) - iq + support_correction(b)
        with np.errstate(divide="ignore", invalid="ignore"):
            sp = np.where(r["base_valid"], 2*norm.sf(np.abs(observed_delta/r["standard_error"])), np.nan)
        blocks.append(pd.DataFrame({
            "delta": r["delta_corrected"], "se2": r["standard_error"]**2,
            "vp": vp, "vq": vq, "ip": ip, "iq": iq,
            "dfp": r["expanded_component_degrees_of_freedom_p"],
            "dfq": r["expanded_component_degrees_of_freedom_q"],
            "df": r["expanded_welch_degrees_of_freedom"],
            "normal_wald": r["normal_p_value"], "hutcheson_welch": hp,
            "simple_welch": r["welch_p_value"],
            "kurtosis_welch": kp, "expanded_welch": r["expanded_welch_p_value"],
            "observed_support_wald": sp,
        }))
    return pd.concat(blocks, ignore_index=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=20000)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    source = ROOT / "results/thesis_redesign"
    output = ROOT / ("results/thesis_mechanism_smoke" if args.smoke else "results/thesis_mechanism_check")
    output.mkdir(parents=True, exist_ok=True)
    display = pd.read_csv(source / "display_manifest.csv")
    chosen = display.loc[
        display.section.eq("main")
        | (display.section.eq("baseline") & display["shape"].eq("3x3") & display.profile.eq("different_skew"))
        | (display.section.eq("imbalance") & display["shape"].eq("3x3") & display.profile.eq("different_skew"))
        | (display.section.eq("convergence") & display["shape"].isin(["3x3", "8x8"]))
    ].drop_duplicates("configuration_id")
    if args.smoke:
        chosen = chosen.head(2)
    configs = pd.read_csv(source / "configuration_manifest.csv").set_index("configuration_id", drop=False)
    populations = pd.read_csv(source / "population_definitions.csv").set_index("pair_id")
    chosen.to_csv(output / "selected_displays.csv", index=False)
    methods = ["normal_wald", "hutcheson_welch", "simple_welch", "kurtosis_welch", "expanded_welch", "observed_support_wald"]
    rates, components, diagnostics = [], [], []
    for index, selected in enumerate(chosen.itertuples()):
        c = configs.loc[selected.configuration_id]
        pop = populations.loc[c.pair_id]
        draws = simulate(c, pop, args.replicates, "evaluation")
        info = {key: c[key] for key in ["configuration_id", "pair_id", "shape", "profile", "n_p", "n_q", "target_mi_p", "target_mi_q"]}
        info["section"] = selected.section
        for method in methods:
            valid = draws[method].notna().to_numpy()
            reject = draws[method].lt(.05).to_numpy() & valid
            paired = reject.astype(float) - draws.normal_wald.lt(.05).to_numpy()
            rates.append(dict(info, method=method, replicates=args.replicates,
                rejected=int(reject.sum()), valid=int(valid.sum()), rate=reject.mean(),
                valid_rate=valid.mean(), rate_mcse=np.sqrt(reject.mean()*(1-reject.mean())/args.replicates),
                paired_minus_wald=paired.mean(), paired_mcse=paired.std(ddof=1)/np.sqrt(args.replicates)))
        if np.isclose(c.target_mi_p, c.target_mi_q, atol=1e-14, rtol=0):
            pilot = simulate(c, pop, args.replicates, "independent-pilot")
            oracle_sd = pilot.delta.std(ddof=1)
            v0 = 0.
            for side in ("p", "q"):
                p = np.array(json.loads(pop[f"probability_{side}_json"]))
                mi, v, tau = population_moments(p)
                n = c[f"n_{side}"]
                v0 += v/n
                ev = pilot[f"v{side}"]
                ev_var = ev.var(ddof=1)
                finite_df = draws[f"df{side}"].replace([np.inf, -np.inf], np.nan)
                components.append(dict(info, population=side, mi=mi, v=v, tau2=tau,
                    mean_vhat=ev.mean(), var_vhat=ev_var,
                    mean_vhat_over_v=ev.mean()/v, n_var_ihat_over_v=n*pilot[f"i{side}"].var(ddof=1)/v,
                    population_first_order_df=2*n*v*v/tau,
                    empirical_moment_df=2*ev.mean()**2/ev_var if ev_var > 0 else np.nan,
                    median_plugin_df=finite_df.median(),
                    first_order_var_ratio=ev_var/(tau/n) if tau > 0 else np.nan))
            delta_sd = draws.delta.std(ddof=1)
            se2_sd = draws.se2.std(ddof=1)
            numerator_se2_correlation = (
                draws.delta.corr(draws.se2) if delta_sd > 0 and se2_sd > 0 else np.nan
            )
            diagnostics.append(dict(info, replicates=args.replicates,
                pilot_sd=oracle_sd, standardized_bias=draws.delta.mean()/oracle_sd,
                mean_se2_over_empirical_var=draws.se2.mean()/oracle_sd**2,
                empirical_var_over_first_order=oracle_sd**2/v0,
                normal_wald_rate=draws.normal_wald.lt(.05).mean(),
                independent_mc_sd_rate=(np.abs(draws.delta)/oracle_sd > norm.ppf(.975)).mean(),
                population_first_order_sd_rate=(np.abs(draws.delta)/np.sqrt(v0) > norm.ppf(.975)).mean(),
                median_combined_df=draws.df.replace([np.inf,-np.inf],np.nan).median(),
                numerator_se2_correlation=numerator_se2_correlation))
        if index % 25 == 0:
            print(f"Completed {index+1}/{len(chosen)} configurations", flush=True)
    pd.DataFrame(rates).to_csv(output / "ablation_rates.csv", index=False)
    pd.DataFrame(components).to_csv(output / "component_diagnostics.csv", index=False)
    pd.DataFrame(diagnostics).to_csv(output / "denominator_diagnostics.csv", index=False)
    metadata = dict(status="post-review explanatory follow-up", seed_scheme="SHA256 mechanism-v1:configuration_id:phase, first 8 bytes",
        replicates_per_phase=args.replicates, configurations=len(chosen), pilot_is_independent=True,
        source_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ["protocol.json", "configuration_manifest.csv", "population_definitions.csv"]},
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2)+"\n")
    print(output, flush=True)


if __name__ == "__main__":
    main()
