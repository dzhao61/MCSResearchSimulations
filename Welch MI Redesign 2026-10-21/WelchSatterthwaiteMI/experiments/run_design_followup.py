"""Run and report the documented follow-up without changing the frozen results."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from run_detection_breakdown_sweep import (
    _simulate_configuration, stable_seed, table_with_target_mi_from_interaction,
)
from make_final_experiment_landscape import marginal_specification

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/detection_breakdown_sweep"
OUT = ROOT / "results/design_followup"
DOC = ROOT / "docs/experiments/archive/EXPERIMENTAL_RESULTS.md"
FIG = ROOT / "docs/experiments/figures/design_followup"
PROTOCOL = Path(__file__).with_name("DESIGN_FOLLOWUP_PROTOCOL.json")
METHODS = {"normal_wald": ("Normal Wald", "#1f4e79", "o"),
           "expanded_welch": ("Expanded Welch", "#b23a73", "s")}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mi(a):
    marginal = a.sum(1)[:, None] * a.sum(0)[None, :]
    positive = a > 0
    return float(np.sum(a[positive] * np.log(a[positive] / marginal[positive])))


def retarget(row, side, target):
    return table_with_target_mi_from_interaction(
        np.array(json.loads(row[f"row_margin_{side}_json"])),
        np.array(json.loads(row[f"column_margin_{side}_json"])),
        target, np.array(json.loads(row[f"interaction_matrix_{side}_json"])),
        mi_tolerance=1e-11, max_association=128,
    )[0]


def build(protocol):
    populations = pd.read_csv(SOURCE / "population_definitions.csv")
    original = pd.read_csv(SOURCE / "cell_results.csv")
    tasks, definitions = [], []
    def source(shape, skew, effect=0):
        x = populations[(populations['shape'] == shape) & (populations.skewness == skew)
                        & (populations.relative_effect == effect)
                        & (populations.interaction_pair == 'primary')
                        & (populations.relationship == 'equal_mi_different_shape')]
        assert len(x) == 1
        return x.iloc[0]

    def add(block, shape, skew, b, effect, scale, p, q, np_, nq_, ratio=1):
        pid = f'{block}_{shape}_{skew}_b{b:g}_e{effect:g}'
        cid = f'{pid}_np{np_}_nq{nq_}'
        ip, iq = mi(p), mi(q)
        assert abs(ip - b * scale) < 1e-10 and abs(iq - (b + effect) * scale) < 1e-10
        for a in (p, q):
            assert np.isfinite(a).all() and (a >= 0).all() and abs(a.sum()-1) < 1e-10
        if block == 'heterogeneous_margins':
            # Different sorted margins rule out equivalence through category relabelling.
            assert not np.allclose(np.sort(p.sum(1)), np.sort(q.sum(1)), atol=1e-8)
        row = dict(configuration_id=cid, population_id=pid, experiment=block, shape=shape,
                   rows=p.shape[0], columns=p.shape[1], skewness=skew,
                   relationship='equal_mi_different_shape', interaction_pair='primary',
                   n_p=np_, n_q=nq_, sample_size_ratio_q_to_p=nq_/np_, allocation_ratio=ratio,
                   relative_effect=effect, baseline_fraction=b, shared_reachable_mi=scale,
                   target_mi_p=b*scale, target_mi_q=(b+effect)*scale,
                   achieved_mi_p=ip, achieved_mi_q=iq, absolute_mi_difference=abs(iq-ip),
                   structural_breakdown=min(np_,nq_)<max(p.shape),
                   replicates=protocol['replicates'], simulation_seed=stable_seed(protocol['master_seed'],cid))
        tasks.append(dict(configuration=row, probability_p=p, probability_q=q,
                          alphas=protocol['alphas'], batch_size=2000))
        definitions.append(dict(population_id=pid, probability_p_json=json.dumps(p.tolist()),
                                probability_q_json=json.dumps(q.tolist()), M=scale, I_p=ip,I_q=iq))

    h=protocol['heterogeneous_margins']
    for shape in h['shapes']:
        a,c=source(shape,'balanced'),source(shape,'mild')
        scale=min(a.shared_reachable_mi,c.shared_reachable_mi)
        p=retarget(a,'p',.2*scale)
        for e in h['effects']:
            q=retarget(c,'q',(.2+e)*scale)
            for n in h['sample_sizes']: add('heterogeneous_margins',shape,'balanced_vs_mild',.2,e,scale,p,q,n,n)
    h=protocol['baseline_sensitivity']
    for shape in h['shapes']:
        for skew in h['skewness']:
            a=source(shape,skew); scale=a.shared_reachable_mi
            for b in h['baseline_fractions']:
                p=retarget(a,'p',b*scale)
                for e in h['effects']:
                    q=retarget(a,'q',(b+e)*scale)
                    for n in h['sample_sizes']: add('baseline_sensitivity',shape,skew,b,e,scale,p,q,n,n)
    previous=original[(original.experiment=='robustness_imbalance') &
                      (original.method=='normal_wald') & (original.nominal_alpha==.05)]
    for _,r in previous.iterrows():
        a=source(r['shape'],r.skewness,r.relative_effect)
        p,q=(np.array(json.loads(a[f'probability_{s}_json'])) for s in ('p','q'))
        add('allocation_reversal',r['shape'],r.skewness,.2,r.relative_effect,
            a.shared_reachable_mi,p,q,int(r.n_q),int(r.n_p),int(r.n_q/r.n_p))
    h=protocol['convergence']
    for shape in h['shapes']:
        for skew in h['skewness']:
            a=source(shape,skew)
            p,q=(np.array(json.loads(a[f'probability_{s}_json'])) for s in ('p','q'))
            for n in h['sample_sizes']: add('convergence',shape,skew,.2,0,a.shared_reachable_mi,p,q,n,n)
    manifest=pd.DataFrame([t['configuration'] for t in tasks])
    assert len(manifest)==protocol['new_configuration_count'] and manifest.configuration_id.is_unique
    return tasks,manifest,pd.DataFrame(definitions).drop_duplicates('population_id')


def table(frame):
    cols=['n_p','n_q','relative_effect','method','unconditional_rejection_rate',
          'wilson_95_low','wilson_95_high','valid_rate','conditional_rejection_rate',
          'minimum_true_expected_p','minimum_true_expected_q']
    headings=['nP','nQ','e','Method','Rejection rate','95% lower','95% upper',
              'Valid rate','Rejection rate among valid results','Minimum expected count P','Minimum expected count Q']
    lines=['| '+' | '.join(headings)+' |','| '+' | '.join(['---']*len(cols))+' |']
    for values in frame[cols].itertuples(index=False,name=None):
        values=list(values);values[3]=METHODS[values[3]][0]
        lines.append('| '+' | '.join(f'{v:.4g}' if isinstance(v,float) else str(v) for v in values)+' |')
    return lines


def report(results, document):
    FIG.mkdir(parents=True,exist_ok=True)
    old=pd.read_csv(SOURCE/'cell_results.csv')
    old=old[(old.nominal_alpha==.05)&old.method.isin(METHODS)].copy()
    current=results[(results.nominal_alpha==.05)&results.method.isin(METHODS)].copy()
    lines=['# Follow-up Experiments: Wald and Expanded Welch','',
           'These additions were specified after reviewing the original experiment. Each panel is one fixed regime; no rates are averaged across regimes.', '',
           'The curves show operational rejection rates: invalid outputs count as non-rejections. At zero MI difference this is the false-positive rate; at positive differences it is power. Shading shows pointwise 95% Wilson Monte Carlo intervals. Hollow markers indicate validity below 90%. Each point uses 10,000 table pairs.', '',
           'Expanded Welch uses the same statistic with a heavier-tailed reference, so it can only reduce rejection relative to Wald. A benefit requires improved null calibration together with useful power and adequate validity.', '',
           'The effect axis is e, with absolute MI difference eM. M is a numerical scale demonstrated by the original probe grid, not a theoretical maximum. Within each baseline comparison, M, margins, and dependence arrangements stay fixed; I(P)=bM and I(Q)=(b+e)M. All rejection and validity rates are listed as fractions beneath the figures.', '',
           'The heterogeneous-margin block uses uniform margins for P and one dominant category of probability 0.70 for Q. Remaining marginal probabilities are equal. Other blocks use the saved ordinal/negative-ordinal constructions with balanced, strong (0.90), or ultra (0.95) margins.', '',
           '[Protocol](../../experiments/DESIGN_FOLLOWUP_PROTOCOL.json) | [Full results](../../results/design_followup/cell_results.csv) | [Paired comparisons](../../results/design_followup/paired_method_results.csv) | [Exact populations](../../results/design_followup/population_definitions.csv)', '']
    groups=current.groupby(['experiment','shape','skewness','baseline_fraction','allocation_ratio'],sort=False)
    for index,((block,shape,skew,b,ratio),frame) in enumerate(groups,1):
        frame=frame.copy(); frame['allocation']='equal samples'
        if block=='allocation_reversal':
            frame['allocation']='P larger'
            prior=old[(old.experiment=='robustness_imbalance')&(old['shape']==shape)&
                      (old.skewness==skew)&(old.sample_size_ratio_q_to_p==ratio)].copy()
            prior['allocation']='Q larger';frame=pd.concat([prior,frame],ignore_index=True)
        if block=='convergence':
            prior=old[(old.experiment=='calibration')&(old['shape']==shape)&(old.skewness==skew)&
                      (old.relationship=='equal_mi_different_shape')&(old.n_p==1000)].copy()
            prior['allocation']='equal samples';frame=pd.concat([prior,frame],ignore_index=True)
        frame['smaller_n']=frame[['n_p','n_q']].min(axis=1)
        allocations=list(frame.allocation.unique()); ns=sorted(frame.smaller_n.unique())
        convergence=block=='convergence'
        fig,axes=plt.subplots(len(allocations),1 if convergence else len(ns),
                              figsize=(7 if convergence else 3.4*len(ns),3.1*len(allocations)),squeeze=False,sharex=True,sharey=True)
        for i,allocation in enumerate(allocations):
            for j,n in enumerate([None] if convergence else ns):
                ax=axes[i,j]; panel=frame[frame.allocation==allocation]
                if n is not None: panel=panel[panel.smaller_n==n]
                x='n_p' if convergence else 'relative_effect'
                for method,(label,color,marker) in METHODS.items():
                    r=panel[panel.method==method].sort_values(x)
                    ax.plot(r[x],r.unconditional_rejection_rate,label=label,color=color,marker=marker,markersize=3)
                    ax.fill_between(r[x],r.wilson_95_low,r.wilson_95_high,color=color,alpha=.15)
                    invalid=r.valid_rate<.9
                    ax.scatter(r.loc[invalid,x],r.loc[invalid,'unconditional_rejection_rate'],
                               marker=marker,facecolors='white',edgecolors=color,s=16,zorder=4)
                ax.axhline(.05,color='gray',linestyle=':',linewidth=1);ax.set_ylim(0,1)
                if convergence: ax.set_xscale('log');ax.set_xticks(ns,labels=[str(int(v)) for v in ns])
                else: ax.set_xlim(0,.6)
                first=panel.iloc[0]
                ax.set_title('Equal sample sizes' if convergence else f'nP={int(first.n_p)}, nQ={int(first.n_q)}',fontsize=10)
                ax.set_xlabel('Sample size per group (log scale)' if convergence else 'Scaled MI difference e')
                ax.set_ylabel('Rejection rate');ax.grid(alpha=.2)
        block_labels={'heterogeneous_margins':'Different margins',
                      'baseline_sensitivity':'Baseline MI sensitivity',
                      'allocation_reversal':'Reversed sample allocation',
                      'convergence':'Large-sample null calibration'}
        title=f'{block_labels[block]}: {shape}, {skew.replace("_"," ")}, b={b:g}'
        if block=='allocation_reversal':title+=f', ratio={ratio:g}:1'
        fig.suptitle(title,fontsize=11);handles,labels=axes[0,0].get_legend_handles_labels()
        fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=2,frameon=False)
        fig.tight_layout(rect=(0,0,1,.86))
        filename=f'{index:02d}_{block}_{shape}_{skew}_b{b:g}_r{ratio:g}.png'
        fig.savefig(FIG/filename,dpi=150);plt.close(fig)
        first=frame.iloc[0];scale=float(first.shared_reachable_mi)
        rows=['| Specification | Setting |','| --- | --- |',f'| Table shape | {shape} |',
              '| Population construction | Ordinal arrangement for P and reversed ordinal for Q |',
              f'| Horizontal graph regime specifications (columns) | '+('{single graph, n in '+str([int(v) for v in ns])+'}' if convergence else '{'+', '.join('smaller n='+str(int(v)) for v in ns)+'}')+' |',
              '| Vertical graph regime specifications (rows) | {'+', '.join(allocations)+'}.<br>'+
                  marginal_specification(shape, skew)+
                  '. These are row/column totals, not cell probabilities; they stay fixed across all panels and MI differences in this figure. |',
              f'| MI settings (nats) | M approximately {scale:.4g}; b={b:g}; I(P) approximately {b*scale:.4g}; e in '+str(sorted(frame.relative_effect.unique().tolist()))+'; I(Q)=(b+e)M |',
              '| Axes | '+('n from 1000 to 50000, log scale' if convergence else 'e from 0 to 0.6')+'; rejection rate from 0 to 1 |',
              '| Replicates | 10,000 independent table pairs per point |']
        lines.extend([f'## {index}. {title}','',f'![{title}](figures/design_followup/{filename})','',*rows,'',
                      '<details><summary>Exact rejection rates, intervals, validity and expected counts</summary>','',
                      *table(frame.sort_values(['n_p','n_q','relative_effect','method'])),'','</details>',''])
    document.write_text('\n'.join(lines)+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report-only',action='store_true');args=parser.parse_args()
    protocol=json.loads(PROTOCOL.read_text());OUT.mkdir(parents=True,exist_ok=True)
    if not args.report_only:
        start=perf_counter()
        try: tasks,manifest,populations=build(protocol)
        except Exception as error:
            (OUT/'preflight_failure.json').write_text(json.dumps({'error':str(error)},indent=2));raise
        manifest.to_csv(OUT/'configuration_manifest.csv',index=False)
        populations.to_csv(OUT/'population_definitions.csv',index=False)
        (OUT/'protocol.json').write_text(PROTOCOL.read_text())
        inputs=[PROTOCOL,Path(__file__),SOURCE/'population_definitions.csv',SOURCE/'cell_results.csv',
                Path(__file__).with_name('run_detection_breakdown_sweep.py'),ROOT/'src/welch_differential_mi/welch.py',
                ROOT.parent/'DifferentialMI/src/differential_mi/statistics.py',
                ROOT.parent/'DifferentialMI/src/differential_mi/distributions.py']
        metadata={'input_sha256':{str(p.relative_to(ROOT.parent)):digest(p) for p in inputs},
                  'status':'preflight_complete', 'seed':protocol['master_seed'], 'configurations':len(tasks)}
        (OUT/'run_metadata.json').write_text(json.dumps(metadata,indent=2))
        print(f'Preflight passed: {len(tasks)} configurations; protocol and inputs recorded.',flush=True)
        cells,paired=[],[]
        for i,task in enumerate(tasks,1):
            result=_simulate_configuration(task);cells.extend(result['cell_rows']);paired.extend(result['paired_rows'])
            if i%40==0:print(f'{i}/{len(tasks)} completed',flush=True)
        results=pd.DataFrame(cells);pairs=pd.DataFrame(paired)
        results.to_csv(OUT/'cell_results.csv',index=False);pairs.to_csv(OUT/'paired_method_results.csv',index=False)
        metadata.update(status='complete',elapsed_seconds=perf_counter()-start,table_pairs=int(manifest.replicates.sum()))
        (OUT/'run_metadata.json').write_text(json.dumps(metadata,indent=2))
    results=pd.read_csv(OUT/'cell_results.csv')
    assert len(results)==protocol['new_configuration_count']*9
    assert not results.duplicated(['configuration_id','method','nominal_alpha']).any()
    assert np.allclose(results.unconditional_rejection_rate,results.rejections/results.replicates)
    assert (results.rejections<=results.valid_replicates).all()
    assert np.max(abs(results.achieved_mi_p-results.target_mi_p))<1e-10
    assert np.max(abs(results.achieved_mi_q-results.target_mi_q))<1e-10
    counts=results.pivot(index=['configuration_id','nominal_alpha'],columns='method',values='rejections')
    assert (counts.expanded_welch<=counts.normal_wald).all()
    (OUT/'verification.json').write_text(json.dumps({'all_pass':True,'configurations':protocol['new_configuration_count'],
        'checks':['unique complete result grid','rejection denominators','valid counts','target MI','Expanded rejection subset']},indent=2))
    from make_experimental_results import write_combined
    write_combined(DOC, followup=results)
    print(f'Verified results; wrote {DOC}',flush=True)


if __name__=='__main__':
    main()
