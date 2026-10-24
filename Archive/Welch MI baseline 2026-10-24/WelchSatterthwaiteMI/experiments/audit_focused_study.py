#!/usr/bin/env python3
"""Independently recalculate focused-study results and regenerate sampled inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, t

from focused_study_core import (
    ALPHA, CHUNK_SIZE, MASTER_SEED, REPLICATES, ROOT, SCHEMA_VERSION,
    build_design, digest, evaluate_tables, seed_for, source_fingerprint,
)
from run_focused_study import atomic_json, file_hash, load_records


def close(a, b):
    np.testing.assert_allclose(a, b, atol=1e-13, rtol=1e-11, equal_nan=True)


def independent_interval(successes, total):
    if total == 0:
        return np.nan, np.nan
    estimate = successes/total
    z = norm.ppf(.975)
    center = (estimate+z*z/(2*total))/(1+z*z/total)
    half = z*np.sqrt(estimate*(1-estimate)/total+z*z/(4*total**2))/(1+z*z/total)
    return center-half, center+half


def authenticate_base_design(output: Path, identity: dict) -> None:
    """Authenticate experimental labels, populations and checkpoint provenance."""
    configs, displays, populations, arrays = build_design()
    expected = {"schema": SCHEMA_VERSION, "master_seed": MASTER_SEED,
                "source": source_fingerprint(), "phase": "full", "count": REPLICATES,
                "chunk_size": CHUNK_SIZE, "design_digest": digest([configs, populations]),
                "alpha": ALPHA}
    if any(identity.get(key) != value for key, value in expected.items()):
        raise AssertionError("Focused-study identity differs from the planned design.")
    for filename, rows in (("configuration_manifest.csv", configs),
                           ("display_manifest.csv", displays)):
        saved = pd.read_csv(output / filename, keep_default_na=False, float_precision="round_trip")
        pd.testing.assert_frame_equal(saved, pd.DataFrame(rows), check_dtype=False, check_exact=True)
    if json.loads((output / "population_definitions.json").read_text()) != populations:
        raise AssertionError("Population definitions differ from the planned design.")
    with np.load(output / "populations.npz", allow_pickle=False) as stored:
        expected_keys = {f"{key}_{side}" for key in arrays for side in "pq"}
        if set(stored.files) != expected_keys:
            raise AssertionError("Population array identifiers differ from the design.")
        for key, pair in arrays.items():
            for side, probability in zip("pq", pair, strict=True):
                np.testing.assert_array_equal(stored[f"{key}_{side}"], probability)
    for config in configs:
        metadata = json.loads((output / "records" / config["configuration_id"] / "identity.json").read_text())
        if metadata != {"configuration": config, "count": REPLICATES, "phase": "full",
                        "fingerprint": digest(identity), "chunk_size": CHUNK_SIZE}:
            raise AssertionError("Checkpoint identity differs from its setting or run.")


def audit(output: Path, *, expected_settings: int = 232, expected_pairs: int = 68):
    identity = json.loads((output / "study_identity.json").read_text())
    if identity["phase"] != "full" or identity["count"] != 20000 or identity["source"] != source_fingerprint():
        raise AssertionError("Unexpected run identity or scientific source changed.")
    if expected_settings == 232 and expected_pairs == 68:
        authenticate_base_design(output, identity)
    configs = pd.read_csv(output / "configuration_manifest.csv")
    populations = {p["pair_id"]: p for p in json.loads((output / "population_definitions.json").read_text())}
    methods = pd.read_csv(output / "method_results.csv").set_index(["configuration_id", "method", "denominator"])
    paired = pd.read_csv(output / "paired_results.csv").set_index(["configuration_id", "denominator"])
    diagnostics = pd.read_csv(output / "diagnostics.csv").set_index("configuration_id")
    if (len(configs) != expected_settings or len(populations) != expected_pairs
            or len(methods) != expected_settings*6 or len(paired) != expected_settings*2):
        raise AssertionError("Unexpected summary counts.")
    with np.load(output / "populations.npz", allow_pickle=False) as arrays:
        for config in configs.to_dict("records"):
            key = config["configuration_id"]
            records = load_records(output / "records" / key, 20000)
            for side in "pq":
                probability = arrays[f"{config['pair_id']}_{side}"]
                population = populations[config["pair_id"]]
                close(probability.sum(), 1)
                close(probability.sum(axis=0), population[f"margin_{side}"])
                close(probability.sum(axis=1), population[f"margin_{side}"])
                if not np.all(probability > 0):
                    raise AssertionError("Nonpositive population cell.")
                row_margin = probability.sum(axis=1, keepdims=True)
                column_margin = probability.sum(axis=0, keepdims=True)
                score = np.log(probability/(row_margin*column_margin))
                mi = np.sum(probability*score)
                variance = np.sum(probability*(score-mi)**2)
                row_score = np.sum(probability*score, axis=1, keepdims=True)/row_margin
                column_score = np.sum(probability*score, axis=0, keepdims=True)/column_margin
                sensitivity = (score-mi)**2-variance+2*(score-row_score-column_score+mi)
                sensitivity_variance = np.sum(probability*(sensitivity-np.sum(probability*sensitivity))**2)
                close(mi, population[f"mi_{side}"])
                close(variance, population[f"variance_{side}"])
                close(sensitivity_variance, population[f"variance_sensitivity_variance_{side}"])
            # Regenerate actual count tables independently of the chunk runner.
            p = arrays[f"{config['pair_id']}_p"]
            q = arrays[f"{config['pair_id']}_q"]
            rng_p = np.random.default_rng(seed_for("full", key, 0, "p"))
            rng_q = np.random.default_rng(seed_for("full", key, 0, "q"))
            sampled_p = rng_p.multinomial(config["n_p"], p.ravel(), size=17).reshape(17, *p.shape)
            sampled_q = rng_q.multinomial(config["n_q"], q.ravel(), size=17).reshape(17, *q.shape)
            calculated = evaluate_tables(sampled_p, sampled_q)
            for field in calculated:
                close(calculated[field], records[field][:17])
            statistic = records["delta_corrected"]/np.where(records["standard_error"] > 0, records["standard_error"], np.nan)
            close(statistic, records["statistic"])
            close(records["squared_standard_error"], records["standard_error"]**2)
            close(records["squared_standard_error"],
                  records["influence_variance_p"]/config["n_p"]
                  + records["influence_variance_q"]/config["n_q"])
            with np.errstate(divide="ignore", invalid="ignore"):
                df_p = 2*config["n_p"]*records["influence_variance_p"]**2/records["variance_influence_variance_p"]
                df_q = 2*config["n_q"]*records["influence_variance_q"]**2/records["variance_influence_variance_q"]
                component_p = records["influence_variance_p"]/config["n_p"]
                component_q = records["influence_variance_q"]/config["n_q"]
                combined = (component_p+component_q)**2/(component_p**2/df_p+component_q**2/df_q)
            good = records["expanded_valid"]
            close(df_p[good], records["expanded_component_degrees_of_freedom_p"][good])
            close(df_q[good], records["expanded_component_degrees_of_freedom_q"][good])
            close(combined[good], records["expanded_welch_degrees_of_freedom"][good])
            w = records["base_valid"]
            close(2*norm.sf(np.abs(statistic[w])), records["normal_p_value"][w])
            close(2*t.sf(np.abs(statistic[good]), df=combined[good]), records["expanded_welch_p_value"][good])
            wr = w & (records["normal_p_value"] <= .05)
            er = good & (records["expanded_welch_p_value"] <= .05)
            if np.any(er & ~wr):
                raise AssertionError("Expanded rejection outside Wald rejection.")
            common = w & good
            for method, valid, rejected in (("normal_wald", w, wr), ("expanded_welch", good, er)):
                for denominator, mask in (("all", np.ones(20000, bool)), ("method_valid", valid), ("common_valid", common)):
                    row = methods.loc[(key, method, denominator)]
                    count = mask.sum()
                    successes = np.count_nonzero(rejected & mask)
                    close(row.replicates, count)
                    close(row.rejections, successes)
                    close(row.valid_replicates, np.count_nonzero(valid & mask))
                    close(row.rejection_rate, successes/count if count else np.nan)
                    close(row.valid_rate, np.count_nonzero(valid & mask)/count if count else np.nan)
                    close(row.rejection_mcse, np.sqrt(row.rejection_rate*(1-row.rejection_rate)/count) if count else np.nan)
                    close([row.rejection_low, row.rejection_high], independent_interval(successes, count))
                    close([row.valid_low, row.valid_high], independent_interval(np.count_nonzero(valid & mask), count))
            for denominator, mask in (("all", np.ones(20000, bool)), ("common_valid", common)):
                d = wr[mask].astype(float)-er[mask].astype(float)
                row = paired.loc[(key, denominator)]
                close(row.replicates, len(d))
                close(row.only_wald, np.count_nonzero(d == 1))
                close(row.only_expanded, np.count_nonzero(d == -1))
                close(row.both_reject, np.count_nonzero(wr & er & mask))
                close(row.neither_reject, np.count_nonzero(~wr & ~er & mask))
                close(row.difference, np.mean(d) if len(d) > 1 else np.nan)
                close(row.mcse, np.std(d, ddof=1)/np.sqrt(len(d)) if len(d) > 1 else np.nan)
                close(row.low, row.difference-1.96*row.mcse)
                close(row.high, row.difference+1.96*row.mcse)
            row = diagnostics.loc[key]
            d = records["delta_corrected"]
            finite = np.isfinite(d)
            matched = finite & np.isfinite(records["squared_standard_error"])
            close(row.finite_difference_count, finite.sum())
            close(row.matched_variance_count, matched.sum())
            close(row.difference_bias, d[finite].mean()-config["delta"])
            close(row.observed_variance, np.var(d[finite], ddof=1))
            close(row.bias_mcse, np.std(d[finite], ddof=1)/np.sqrt(finite.sum()))
            close(row.mean_estimated_variance, records["squared_standard_error"][matched].mean())
            close(row.matched_observed_variance, np.var(d[matched], ddof=1))
            close(row.estimated_observed_ratio, records["squared_standard_error"][matched].mean()/np.var(d[matched], ddof=1))
            first = populations[config["pair_id"]]["variance_p"]/config["n_p"] + populations[config["pair_id"]]["variance_q"]/config["n_q"]
            close(row.first_order_variance, first)
            close(row.first_order_observed_ratio, first/np.var(d[finite], ddof=1))
            for column, quantile in (("df_p05", .05), ("df_median", .5), ("df_p95", .95)):
                close(row[column], np.quantile(records["expanded_welch_degrees_of_freedom"][good], quantile) if good.any() else np.nan)
            close(row.degrees_of_freedom_count, good.sum())
            for side in "pq":
                close(row[f"bias_{side}"], np.mean(records[f"corrected_mi_{side}"])-populations[config["pair_id"]][f"mi_{side}"])
                for item in ("cells", "rows", "columns"):
                    close(row[f"mean_empty_{item}_{side}"], np.mean(records[f"empty_{item}_{side}"]))
    result = {"all_pass": True, "settings": expected_settings, "population_pairs": expected_pairs,
              "table_pairs": expected_settings*20000, "regenerated_input_pairs": expected_settings*17,
              "checks": ["population positivity, total, margins, MI, variance and sensitivity", "all raw checksums and counts",
                         "regenerated count inputs match saved outputs", "independent statistic and df algebra",
                         "normal and Student t distribution p-values", "rejection and validity denominators",
                         "Wilson intervals", "paired indicator contrasts and intervals", "bias and variance masks",
                         "degrees-of-freedom validity mask and percentiles"],
              "input_sha256": {name: file_hash(output / name) for name in (
                  "study_identity.json", "configuration_manifest.csv", "population_definitions.json",
                  "populations.npz", "method_results.csv", "paired_results.csv", "diagnostics.csv")}}
    if expected_settings == 232 and expected_pairs == 68:
        result["checks"].append("exact design, display mapping, population arrays and checkpoint identities")
        result["input_sha256"]["display_manifest.csv"] = file_hash(output / "display_manifest.csv")
    atomic_json(output / "independent_audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=ROOT / "results/focused_study")
    audit(parser.parse_args().results)
