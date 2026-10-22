#!/usr/bin/env python3
"""Check variance-estimate stability and rejection direction in saved samples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from audit_focused_study import audit
from focused_study_core import ALPHA, REPLICATES, ROOT, seed_for
from run_focused_study import load_records

DEFAULT_RESULTS = ROOT / "results/focused_study"
STABILITY_SETTINGS = (
    (4, 1000, .0001), (4, 1000, .02), (4, 1000, .05),
    (4, 10000, .02), (16, 1000, .02), (16, 10000, .02),
)
DIRECTION_SETTINGS = ((1000, .03), (1000, .04), (10000, .03), (10000, .04))
METHODS = (
    ("wald", "base_valid", "normal_p_value"),
    ("expanded", "expanded_valid", "expanded_welch_p_value"),
)


def direction_summary(delta, valid, p_value, true_delta):
    delta, valid, p_value = np.asarray(delta), np.asarray(valid, bool), np.asarray(p_value)
    if delta.ndim != 1 or delta.shape != valid.shape or delta.shape != p_value.shape:
        raise ValueError("Direction records must be aligned one-dimensional arrays.")
    if not np.isfinite(true_delta) or true_delta == 0:
        raise ValueError("Direction requires a finite nonzero population difference.")
    rejected = valid & np.isfinite(delta) & np.isfinite(p_value) & (p_value <= ALPHA)
    opposite = rejected & ((delta > 0) if true_delta < 0 else (delta < 0))
    correct = rejected & ((delta < 0) if true_delta < 0 else (delta > 0))
    count = int(rejected.sum())
    return {
        "repetitions": len(delta), "valid_count": int(valid.sum()),
        "rejections": count, "correct_sign": int(correct.sum()),
        "opposite_sign": int(opposite.sum()), "zero_sign": int((rejected & (delta == 0)).sum()),
        "opposite_fraction_among_rejections": float(opposite.sum()/count) if count else None,
        "opposite_rate_all_repetitions": float(opposite.sum()/len(delta)) if len(delta) else None,
    }


def population_moments(probability):
    probability = np.asarray(probability, float)
    if probability.ndim != 2 or not np.isfinite(probability).all() or np.any(probability <= 0):
        raise ValueError("Population moments require a positive finite probability table.")
    np.testing.assert_allclose(probability.sum(), 1, atol=1e-12, rtol=0)
    rows = probability.sum(axis=1, keepdims=True)
    columns = probability.sum(axis=0, keepdims=True)
    pointwise = np.log(probability/(rows*columns))
    mi = np.sum(probability*pointwise)
    variance = np.sum(probability*(pointwise-mi)**2)
    row_mean = np.sum(probability*pointwise, axis=1, keepdims=True)/rows
    column_mean = np.sum(probability*pointwise, axis=0, keepdims=True)/columns
    sensitivity = (pointwise-mi)**2-variance+2*(pointwise-row_mean-column_mean+mi)
    sensitivity_mean = np.sum(probability*sensitivity)
    np.testing.assert_allclose(sensitivity_mean, 0, atol=1e-12, rtol=0)
    tau2 = np.sum(probability*(sensitivity-sensitivity_mean)**2)
    return {"mi": float(mi), "variance": float(variance), "tau2": float(tau2)}


def stability_summary(variance, tau2, population_tau2, sample_size):
    variance, tau2 = np.asarray(variance, float), np.asarray(tau2, float)
    if variance.ndim != 1 or variance.shape != tau2.shape:
        raise ValueError("Stability records must be aligned one-dimensional arrays.")
    if sample_size <= 0 or not np.isfinite(population_tau2) or population_tau2 < 0:
        raise ValueError("Invalid population prediction.")
    included = np.isfinite(variance) & np.isfinite(tau2)
    if np.any(variance[included] < 0) or np.any(tau2[included] < 0):
        raise ValueError("Variance quantities must be nonnegative.")
    v, t = variance[included], tau2[included]
    observed = float(np.var(v, ddof=1)) if len(v) > 1 else None
    population = float(population_tau2/sample_size)
    plugin = float(np.mean(t)/sample_size) if len(t) else None
    return {
        "repetitions": len(variance), "included_count": len(v),
        "observed_variance_of_variance": observed,
        "population_prediction": population, "mean_plugin_prediction": plugin,
        "population_observed_ratio": population/observed if observed and observed > 0 else None,
        "plugin_observed_ratio": plugin/observed if observed and observed > 0 else None,
    }


def bootstrap_intervals(variance, tau2, population_tau2, sample_size, seed, repetitions=1000):
    # Resample paired saved outputs, not observations or population count tables.
    if repetitions < 1:
        raise ValueError("Bootstrap repetition count must be positive.")
    variance, tau2 = np.asarray(variance, float), np.asarray(tau2, float)
    included = np.isfinite(variance) & np.isfinite(tau2)
    v, t = variance[included], tau2[included]
    if len(v) < 2 or np.var(v, ddof=1) <= 0:
        return {"repetitions": repetitions, "finite_repetitions": 0,
                "population_ratio_interval": None, "plugin_ratio_interval": None}
    rng = np.random.default_rng(seed)
    population, plugin = [], []
    for start in range(0, repetitions, 50):
        index = rng.integers(0, len(v), size=(min(50, repetitions-start), len(v)))
        observed = np.var(v[index], axis=1, ddof=1)
        finite = np.isfinite(observed) & (observed > 0)
        population.extend((population_tau2/sample_size/observed[finite]).tolist())
        plugin.extend((np.mean(t[index], axis=1)[finite]/sample_size/observed[finite]).tolist())
    return {
        "repetitions": repetitions, "finite_repetitions": len(population),
        "population_ratio_interval": np.quantile(population, [.025, .975]).tolist() if population else None,
        "plugin_ratio_interval": np.quantile(plugin, [.025, .975]).tolist() if plugin else None,
    }


def select(configurations, k, n, mi_p, mi_q):
    selected = configurations[
        configurations.k.eq(k) & configurations.n_p.eq(n) & configurations.n_q.eq(n)
        & configurations.mi_p.eq(mi_p) & configurations.mi_q.eq(mi_q)
        & configurations.profile.eq("different_skew") & configurations.construction.eq("copying")]
    if len(selected) != 1:
        raise AssertionError("Mechanism selection is not unique.")
    return selected.iloc[0].to_dict()


def build_evidence(results=DEFAULT_RESULTS, *, bootstrap_repetitions=1000):
    configurations = pd.read_csv(results / "configuration_manifest.csv")
    populations = {p["pair_id"]: p for p in json.loads((results / "population_definitions.json").read_text())}
    methods = pd.read_csv(results / "method_results.csv")
    methods = methods[methods.denominator.eq("all")].set_index(["configuration_id", "method"])
    stability, direction = [], []
    with np.load(results / "populations.npz", allow_pickle=False) as arrays:
        for k, n, mi in STABILITY_SETTINGS:
            config = select(configurations, k, n, mi, mi)
            key = config["configuration_id"]
            records = load_records(results / "records" / key, REPLICATES)
            for side in "pq":
                moments = population_moments(arrays[f"{config['pair_id']}_{side}"])
                stored = populations[config["pair_id"]]
                for field, value in moments.items():
                    stored_field = {"mi": "mi", "variance": "variance",
                                    "tau2": "variance_sensitivity_variance"}[field]
                    np.testing.assert_allclose(value, stored[f"{stored_field}_{side}"], atol=1e-13, rtol=1e-11)
                v, t = records[f"influence_variance_{side}"], records[f"variance_influence_variance_{side}"]
                seed = seed_for("mechanism-output-bootstrap", key, side)
                stability.append({"configuration_id": key, "k": k, "n": n, "mi": mi,
                                  "population": side.upper(), "population_moments": moments,
                                  **stability_summary(v, t, moments["tau2"], n),
                                  "monte_carlo_check": bootstrap_intervals(
                                      v, t, moments["tau2"], n, seed, bootstrap_repetitions),
                                  "bootstrap_seed": seed})
    for n, mi_q in DIRECTION_SETTINGS:
        config = select(configurations, 16, n, .02, mi_q)
        key = config["configuration_id"]
        records = load_records(results / "records" / key, REPLICATES)
        row = {"configuration_id": key, "k": 16, "n": n, "delta": config["delta"]}
        for name, valid, p_value in METHODS:
            summary = direction_summary(records["delta_corrected"], records[valid], records[p_value], config["delta"])
            reference = methods.loc[(key, "normal_wald" if name == "wald" else "expanded_welch")]
            if summary["rejections"] != reference.rejections or summary["valid_count"] != reference.valid_replicates:
                raise AssertionError("Direction counts disagree with audited method totals.")
            if summary["zero_sign"] != 0:
                raise AssertionError("A rejected difference has zero sign.")
            row[name] = summary
        direction.append(row)
    return {"stability_settings": 6, "direction_settings": 4,
            "replicates_per_setting": REPLICATES,
            "stability": stability, "direction": direction}


def stability_table(rows):
    lines = [r"\begin{tabular}{@{}rrrlrr@{}}", r"\toprule",
             r"Size & \(n\) & Common MI & Population & Pop./obs. & Plug-in/obs.\\",
             r"\midrule"]
    for index, row in enumerate(rows):
        if index and index % 2 == 0:
            lines.append(r"\addlinespace[2pt]")
        lines.append(f"\\({row['k']}\\times{row['k']}\\) & {row['n']:,} & {row['mi']:g} & "
                     f"{row['population']} & {row['population_observed_ratio']:.3f} & "
                     f"{row['plugin_observed_ratio']:.3f}"+r"\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    return "\n".join(lines)+"\n"


def direction_table(rows):
    lines = [r"\begin{tabular}{@{}rrrrrr@{}}", r"\toprule",
             r"& & \multicolumn{2}{c}{Normal Wald} & \multicolumn{2}{c}{Expanded Welch}\\",
             r"\cmidrule(lr){3-4}\cmidrule(l){5-6}",
             r"\(n\) & \(|\Delta|\) & Rejections & Opposite sign & Rejections & Opposite sign\\",
             r"\midrule"]
    for row in rows:
        lines.append(f"{row['n']:,} & {abs(row['delta']):g} & {row['wald']['rejections']:,} & "
                     f"{row['wald']['opposite_sign']:,} & {row['expanded']['rejections']:,} & "
                     f"{row['expanded']['opposite_sign']:,}"+r"\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    return "\n".join(lines)+"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--figures", type=Path, default=ROOT.parent / "Thesis Writeup/Welch MI/figures_rewrite")
    args = parser.parse_args()
    audit(args.results)
    evidence = build_evidence(args.results)
    args.figures.mkdir(parents=True, exist_ok=True)
    (args.figures / "focused_stability_table.tex").write_text(stability_table(evidence["stability"]))
    (args.figures / "focused_direction_table.tex").write_text(direction_table(evidence["direction"]))
    (args.figures / "focused_mechanism_evidence.json").write_text(json.dumps(evidence, indent=2, allow_nan=False)+"\n")
    print("Verified six stability settings and four direction settings; generated two supporting tables.")


if __name__ == "__main__":
    main()
