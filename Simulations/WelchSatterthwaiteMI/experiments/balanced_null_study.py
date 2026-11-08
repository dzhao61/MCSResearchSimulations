"""Balanced null grid at common MI 0.005, 0.02 and 0.30 nats."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

import fixed_gap_power_study as base
import redesign_study as original
from focused_study_core import construct_copying, digest, summarize, evaluate_tables
from thesis_redesign_core import margin
from differential_mi.statistics import influence_variance

OUTPUT=base.ROOT/"results/balanced_null_2026-11-01"
COMMON_MI=(.005,.02,.30)
DIAGNOSTIC_CASES=((4,"uniform",20),(16,"same_skew",1000),(16,"different_skew",1000))


def fingerprint():
    return digest({"runner":base.sha(__file__),"base":base.fingerprint(),
        "original":original.fingerprint(),
        "construction":base.sha(Path(__file__).with_name("thesis_redesign_core.py"))})


def build_design():
    configs,populations,arrays=[],{},{}
    for common in COMMON_MI:
        for k in base.SIZES:
            for profile,dominant in base.PROFILES.items():
                spec=dict(k=k,profile=profile,mi_p=common,mi_q=common,construction="copying")
                pair_id="pair_"+digest(spec)[:16]
                pop=dict(pair_id=pair_id,**spec);tables=[]
                for side,rho in zip("pq",dominant,strict=True):
                    a=margin(k,rho);result=construct_copying(a,common)
                    pop.update({f"variance_{side}":float(influence_variance(result.probability)),
                        f"achieved_mi_{side}":result.achieved_mi,f"strength_{side}":result.strength,
                        f"endpoint_mi_{side}":result.endpoint_mi,
                        f"minimum_probability_{side}":float(result.probability.min()),
                        f"normalization_error_{side}":result.normalization_error,
                        f"row_margin_error_{side}":result.row_margin_error,
                        f"column_margin_error_{side}":result.column_margin_error,
                        f"margin_{side}":a.tolist(),f"probability_{side}":result.probability.tolist()})
                    tables.append(result.probability)
                populations[pair_id]=pop;arrays[pair_id]=tuple(tables)
                for n in base.SAMPLE_SIZES:
                    configs.append(dict(configuration_id="setting_"+digest([pair_id,n,n])[:16],
                        pair_id=pair_id,**spec,n_p=n,n_q=n,delta=0.,replicates=base.REPLICATES,
                        common_mi=common,record_source="original" if common==.02 else "extension"))
    assert len(configs)==360 and len(populations)==36
    assert len({c["configuration_id"] for c in configs})==360
    return configs,populations,arrays


def original_ids():
    displays=pd.read_csv(original.OUTPUT/"displays.csv",keep_default_na=False)
    return set(displays[displays.study.eq("null")].configuration_id)


def summarise_original(configs,populations,arrays):
    expected=original_ids()
    selected=[c for c in configs if c["record_source"]=="original"]
    assert {c["configuration_id"] for c in selected}==expected and len(selected)==120
    saved_rates=pd.read_csv(original.OUTPUT/"rates.csv")
    saved_rates=saved_rates[saved_rates.denominator.eq("all")].set_index(["configuration_id","method"])
    methods,pairs,diagnostics,checksums=[],[],[],{}
    with np.load(original.OUTPUT/"populations.npz",allow_pickle=False) as saved:
        for c in selected:
            key=c["configuration_id"];directory=original.OUTPUT/"evaluation"/key
            identity=json.loads((directory/"identity.json").read_text())
            assert identity["source"]==original.fingerprint()
            assert identity["count"]==base.REPLICATES and identity["seed"]==original.SEED
            assert identity["stream_phase"]=="evaluation"
            checksums[key]=base.sha(directory/"identity.json")
            p,q=arrays[c["pair_id"]]
            for side,table in zip("pq",(p,q),strict=True):
                np.testing.assert_allclose(table,saved[c["pair_id"]+"_"+side],atol=1e-15,rtol=0)
            records=original.load_records(original.OUTPUT,"evaluation",key)
            rp=np.random.default_rng(original.seed_for("evaluation",key,0,"p"))
            rq=np.random.default_rng(original.seed_for("evaluation",key,0,"q"))
            cp=rp.multinomial(c["n_p"],p.ravel(),size=8).reshape(8,*p.shape)
            cq=rq.multinomial(c["n_q"],q.ravel(),size=8).reshape(8,*q.shape)
            calculated=evaluate_tables(cp,cq);base.check_scalar(cp,cq,calculated)
            for field in base.FIELDS:
                np.testing.assert_allclose(records[field][:8],calculated[field],rtol=2e-10,atol=1e-11,equal_nan=True)
            m,paired,d=summarize(c,populations[c["pair_id"]],records)
            metadata={k:c[k] for k in ["configuration_id","k","profile","n_p","n_q","mi_p","mi_q"]}
            for method,old_name in [("normal_wald","wald"),("expanded_welch","expanded")]:
                row=next(row for row in m if row["method"]==method and row["denominator"]=="all")
                old=saved_rates.loc[(key,old_name)]
                assert row["rejections"]==int(old.rejected) and row["valid_replicates"]==int(old.valid_count)
            methods.extend({**metadata,**row} for row in m)
            pairs.extend({**metadata,**row} for row in paired)
            diagnostics.append({**metadata,**d})
    return methods,pairs,diagnostics,checksums


def combine(output,configs,populations,arrays):
    m,p,d,checksums=summarise_original(configs,populations,arrays)
    metadata=pd.DataFrame(configs)[["configuration_id","common_mi","record_source"]]
    for name,rows in [("rates.csv",m),("paired.csv",p),("diagnostics.csv",d)]:
        both=pd.concat([pd.DataFrame(rows),pd.read_csv(output/name)],ignore_index=True)
        assert set(both.configuration_id)==set(metadata.configuration_id)
        both=both.merge(metadata,on="configuration_id",validate="many_to_one")
        both.to_csv(output/("combined_"+name),index=False)
    rates=pd.read_csv(output/"combined_rates.csv");rates=rates[rates.denominator.eq("all")]
    assert len(rates)==720 and rates.replicates.eq(100000).all()
    np.testing.assert_allclose(rates.rejection_rate,rates.rejections/rates.replicates)
    assert not rates.duplicated(["configuration_id","method"]).any()
    pairs=pd.read_csv(output/"combined_paired.csv");pairs=pairs[pairs.denominator.eq("all")]
    assert len(pairs)==360 and pairs.only_expanded.eq(0).all()
    np.testing.assert_array_equal(pairs.only_wald+pairs.only_expanded+pairs.both_reject+pairs.neither_reject,100000)
    audit=dict(passed=True,settings=360,pairs=36000000,new_settings=240,new_pairs=24000000,
        reused_settings=120,reused_pairs=12000000,independently_reconstructed_pairs=2880,
        original_identity_sha256=checksums,
        checks=["balanced 120-setting grid at each common MI","positive targets and fixed margins",
                "all new and reused raw hashes","original source and seed identities",
                "original arrays and rejection/validity counts unchanged",
                "independent scalar formulas","paired decisions and denominators"])
    base.atomic_json(output/"combined_audit.json",audit)
    print(json.dumps({k:v for k,v in audit.items() if k!="original_identity_sha256"}),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=OUTPUT)
    parser.add_argument("--mode",choices=["preflight","smoke","full","combine"],default="preflight")
    parser.add_argument("--workers",type=int,default=3)
    args=parser.parse_args();configs,populations,arrays=build_design()
    assert {c["configuration_id"] for c in configs if c["record_source"]=="original"}==original_ids()
    new=[c for c in configs if c["record_source"]=="extension"]
    if args.mode=="smoke":new=[c for c in new if c["n_p"] in (10,1000,50000)]
    count=200 if args.mode=="smoke" else base.REPLICATES
    args.output.mkdir(parents=True,exist_ok=True)
    identity=dict(configurations=configs,count=count,source_fingerprint=fingerprint(),
        common_mi=list(COMMON_MI),master_seed=base.MASTER_SEED,original_seed=original.SEED,
        original_configurations_sha256=base.sha(original.OUTPUT/"configurations.csv"),
        original_rates_sha256=base.sha(original.OUTPUT/"rates.csv"),smoke=args.mode=="smoke")
    path=args.output/"manifest.json"
    if path.exists() and json.loads(path.read_text())!=identity:raise RuntimeError("Incompatible null-grid output")
    base.atomic_json(path,identity);base.atomic_json(args.output/"populations.json",list(populations.values()))
    pd.DataFrame(configs).to_csv(args.output/"configurations.csv",index=False)
    print(f'Design: 360 settings; common MI {COMMON_MI}; {len(new)} new settings in this run',flush=True)
    if args.mode=="preflight":return
    if args.mode!="combine":
        started=perf_counter();execution=[]
        tasks=[(str(args.output),c,*arrays[c["pair_id"]],count,500,fingerprint()) for c in new]
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for future in as_completed([pool.submit(base.run_setting,task) for task in tasks]):
                execution.append(future.result())
                if len(execution)%10==0 or len(execution)==len(tasks):
                    print(f'Completed {len(execution)}/{len(tasks)} new null settings',flush=True)
        pd.DataFrame(execution).to_csv(args.output/"execution.csv",index=False)
        print(f'New null sampling finished in {perf_counter()-started:.1f}s',flush=True)
    base.aggregate(args.output,new,populations,count)
    if args.mode!="smoke":combine(args.output,configs,populations,arrays)


if __name__=="__main__":main()
