"""Extend the nominal-power grid to gaps 0.005, 0.01 and 0.02 nats."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

import fixed_gap_power_study as base
from focused_study_core import construct_copying, digest, evaluate_tables
from differential_mi.statistics import influence_variance

OUTPUT = base.ROOT / "results/mi_gap_power_2026-11-01"
GAPS = (.005, .01, .02)


def fingerprint():
    return digest({"base": base.fingerprint(), "runner": base.sha(__file__),
                   "construction": base.sha(Path(__file__).with_name("thesis_redesign_core.py"))})


def build_design():
    originals, populations, arrays = base.build_design()
    configs = [{**c, "gap": .01, "record_source": "original"} for c in originals]
    for gap in (.005, .02):
        for original in list(populations.values()):
            if original["mi_q"] != .03:
                continue
            target = round(.02+gap, 12)
            spec = {key: original[key] for key in ["k", "profile", "mi_p", "construction"]}
            spec["mi_q"] = target
            pair_id = "pair_"+digest(spec)[:16]
            population = {**original, **spec, "pair_id": pair_id}
            a = np.array(original["margin_q"])
            q = construct_copying(a, target)
            population.update(variance_q=float(influence_variance(q.probability)),
                achieved_mi_q=q.achieved_mi, strength_q=q.strength, endpoint_mi_q=q.endpoint_mi,
                minimum_probability_q=float(q.probability.min()),
                normalization_error_q=q.normalization_error, row_margin_error_q=q.row_margin_error,
                column_margin_error_q=q.column_margin_error, probability_q=q.probability.tolist())
            populations[pair_id] = population
            arrays[pair_id] = (np.array(original["probability_p"]), q.probability)
            for n in base.SAMPLE_SIZES:
                configs.append(dict(configuration_id="setting_"+digest([pair_id,n,n])[:16],
                    pair_id=pair_id, **spec, n_p=n, n_q=n, delta=-gap,
                    replicates=base.REPLICATES, gap=gap, record_source="extension"))
    assert len(configs) == 360 and len(populations) == 36
    assert len({c["configuration_id"] for c in configs}) == 360
    return configs, populations, arrays


def write_manifest(output, configs, populations, count, smoke):
    identity = dict(master_seed=base.MASTER_SEED, alpha=.05, count=count,
        configurations=configs, source_fingerprint=fingerprint(),
        original_directory=str(base.OUTPUT.relative_to(base.ROOT.parent)),
        original_manifest_sha256=base.sha(base.OUTPUT/"manifest.json"),
        original_audit_sha256=base.sha(base.OUTPUT/"audit.json"), smoke=smoke)
    path=output/"manifest.json"
    if path.exists() and json.loads(path.read_text()) != identity:
        raise RuntimeError("Output belongs to a different extension/source version")
    base.atomic_json(path,identity)
    base.atomic_json(output/"populations.json",list(populations.values()))
    pd.DataFrame(configs).to_csv(output/"configurations.csv",index=False)
    return identity


def verify_original(configs, populations, arrays):
    manifest=json.loads((base.OUTPUT/"manifest.json").read_text())
    if manifest["source_fingerprint"] != base.fingerprint() or manifest["count"] != base.REPLICATES:
        raise RuntimeError("Original evidence fingerprint or repetition count changed")
    saved={p["pair_id"]:p for p in json.loads((base.OUTPUT/"populations.json").read_text())}
    rates=pd.read_csv(base.OUTPUT/"rates.csv")
    rates=rates[rates.denominator.eq("all")].set_index(["configuration_id","method"])
    audited=0
    for c in configs:
        if c["record_source"] != "original":continue
        assert populations[c["pair_id"]] == saved[c["pair_id"]]
        r, checks=base.load_records(base.OUTPUT,c,base.REPLICATES)
        assert checks == 8
        p,q=arrays[c["pair_id"]]
        rp=np.random.default_rng(base.seed_for(c["configuration_id"],0,"p"))
        rq=np.random.default_rng(base.seed_for(c["configuration_id"],0,"q"))
        cp=rp.multinomial(c["n_p"],p.ravel(),size=8).reshape(8,*p.shape)
        cq=rq.multinomial(c["n_q"],q.ravel(),size=8).reshape(8,*q.shape)
        calculated=evaluate_tables(cp,cq)
        base.check_scalar(cp,cq,calculated)
        for field in base.FIELDS:
            np.testing.assert_allclose(r[field][:8],calculated[field],rtol=2e-10,atol=1e-11,equal_nan=True)
        for name,valid,key in [("normal_wald","base_valid","normal_p_value"),
                               ("expanded_welch","expanded_valid","expanded_welch_p_value")]:
            rejected=int((r[valid]&(r[key]<=.05)).sum())
            assert rejected == int(rates.loc[(c["configuration_id"],name),"rejections"])
        audited+=8
    assert audited == 960
    return audited


def combine(output, configs, populations, arrays):
    checked=verify_original(configs,populations,arrays)
    keys={c["configuration_id"] for c in configs}
    metadata=pd.DataFrame(configs)[["configuration_id","gap","record_source"]]
    for name in ["rates.csv","paired.csv","diagnostics.csv"]:
        old=pd.read_csv(base.OUTPUT/name)
        new=pd.read_csv(output/name)
        both=pd.concat([old,new],ignore_index=True)
        assert set(both.configuration_id) == keys
        both=both.merge(metadata,on="configuration_id",validate="many_to_one")
        both.to_csv(output/("combined_"+name),index=False)
    rates=pd.read_csv(output/"combined_rates.csv")
    primary=rates[rates.denominator.eq("all")]
    assert len(primary)==720 and primary.replicates.eq(base.REPLICATES).all()
    assert not primary.duplicated(["configuration_id","method"]).any()
    np.testing.assert_allclose(primary.rejection_rate,primary.rejections/primary.replicates)
    pairs=pd.read_csv(output/"combined_paired.csv")
    pairs=pairs[pairs.denominator.eq("all")]
    assert len(pairs)==360 and pairs.only_expanded.eq(0).all()
    np.testing.assert_array_equal(pairs.only_wald+pairs.only_expanded+pairs.both_reject+pairs.neither_reject,base.REPLICATES)
    audit=dict(passed=True,settings=360,pairs=36000000,new_settings=240,new_pairs=24000000,
        reused_settings=120,reused_pairs=12000000,independently_reconstructed_pairs=checked+1920,
        original_manifest_sha256=base.sha(base.OUTPUT/"manifest.json"),
        checks=["full 120-setting grid at each of three gaps","positive target-MI populations",
                "all new and reused raw checkpoint hashes","reused populations and rates unchanged",
                "independent scalar reconstructions","validity/rejection nesting","paired counts and denominators"])
    base.atomic_json(output/"combined_audit.json",audit)
    print(json.dumps(audit),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=OUTPUT)
    parser.add_argument("--mode",choices=["preflight","smoke","full","combine"],default="preflight")
    parser.add_argument("--workers",type=int,default=3)
    args=parser.parse_args()
    configs,populations,arrays=build_design()
    new=[c for c in configs if c["record_source"]=="extension"]
    if args.mode=="smoke":
        new=[c for c in new if c["n_p"] in (10,1000,50000)]
    count=200 if args.mode=="smoke" else base.REPLICATES
    args.output.mkdir(parents=True,exist_ok=True)
    write_manifest(args.output,configs,populations,count,args.mode=="smoke")
    print(f'Design: 360 settings; {len(new)} new settings in this run; gaps {GAPS}',flush=True)
    if args.mode=="preflight":return
    if args.mode!="combine":
        tasks=[(str(args.output),c,*arrays[c["pair_id"]],count,500,fingerprint()) for c in new]
        execution=[]
        started=perf_counter()
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for future in as_completed([pool.submit(base.run_setting,task) for task in tasks]):
                execution.append(future.result())
                if len(execution)%10==0 or len(execution)==len(tasks):
                    print(f'Completed {len(execution)}/{len(tasks)} new settings',flush=True)
        pd.DataFrame(execution).to_csv(args.output/"execution.csv",index=False)
        print(f'New sampling finished in {perf_counter()-started:.1f}s',flush=True)
    base.aggregate(args.output,new,populations,count)
    if args.mode!="smoke":combine(args.output,configs,populations,arrays)


if __name__=="__main__":main()
