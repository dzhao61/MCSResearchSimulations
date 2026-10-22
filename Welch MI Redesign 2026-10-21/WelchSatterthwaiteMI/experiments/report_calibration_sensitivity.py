"""Joint calibration uncertainty, cross-null validation, and magnitude diagnostics."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import redesign_study as study
import calibration_sensitivity as sensitivity
from redesign_report import FIGURES, table, select_case


def prepared(records, config, reference):
    values,_=study.method_values(records,config,reference['nu_ref'])
    return dict(absolute=np.where(records['base_valid'],abs(records['statistic']),-np.inf),
                size=np.where(values['size'][1],values['size'][0],1.),
                expanded=np.where(values['expanded'][1],values['expanded'][0],1.))


def cutoffs(data, indices=None):
    n=len(data['absolute']); k=int(study.ALPHA*n)
    x=data if indices is None else {f:v[indices] for f,v in data.items()}
    return dict(absolute_t=float(np.partition(x['absolute'],n-k-1)[n-k-1]),
                **{m:float(np.partition(x[m],k)[k]) for m in ('size','expanded')})


def reject(data, cuts):
    # Invalid records have absolute=-inf or p=1 and remain non-rejections.
    w=data['absolute']>cuts['absolute_t']
    return np.column_stack([w,data['size']<cuts['size'],data['expanded']<cuts['expanded'],w])


def resample_joint(decisions, rng):
    """Resample rows of paired decisions by their joint bit pattern."""
    width=decisions.shape[1]
    codes=(decisions.astype(np.uint16)*(1<<np.arange(width))).sum(1).astype(int)
    counts=np.bincount(codes,minlength=1<<width)
    membership=((np.arange(1<<width)[:,None] & (1<<np.arange(width)))>0)
    return rng.multinomial(len(codes),counts/len(codes))@membership/len(codes)


def bootstrap_focus(task):
    base,output,label,repetitions=task
    base,output=Path(base),Path(output)
    cases,_=sensitivity.design(base); cases=[c for c in cases if c['focus']==label]
    configs=pd.read_csv(base/'configurations.csv').set_index('configuration_id').to_dict('index')
    refs=json.loads((base/'references.json').read_text())
    upper_refs=json.loads((output/'references.json').read_text())
    lower_id=cases[0]['lower_id']; lower_ref=refs[lower_id]
    lower_fit=prepared(study.load_records(base,'fit',lower_id),configs[lower_id],lower_ref)
    ready=[]
    for c in cases:
        upper_ref=upper_refs[c['configuration_id']]
        upper_fit=prepared(study.load_records(output,'fit',c['configuration_id']),c,upper_ref)
        alt=prepared(study.load_records(base,'evaluation',c['alternative_id']),configs[c['alternative_id']],lower_ref)
        ready.append((c,upper_fit,alt))
    n=len(lower_fit['absolute'])
    rng=np.random.default_rng(study.seed_for('upper-null-joint-bootstrap',label,0,'paired'))
    draws=np.empty((repetitions,len(ready),8))
    for b in range(repetitions):
        # The lower fitting sample is shared by the 2-SD and 4-SD comparisons.
        lower_cuts=cutoffs(lower_fit,rng.integers(0,n,n))
        for j,(c,upper_fit,alt) in enumerate(ready):
            upper_cuts=cutoffs(upper_fit,rng.integers(0,len(upper_fit['absolute']),len(upper_fit['absolute'])))
            joint=np.column_stack([reject(alt,lower_cuts),reject(alt,upper_cuts)])
            draws[b,j]=resample_joint(joint,rng)
    rows=[]
    for j,(c,upper_fit,alt) in enumerate(ready):
        point=np.r_[reject(alt,lower_ref['calibration']).mean(0),
                    reject(alt,upper_refs[c['configuration_id']]['calibration']).mean(0)]
        common=dict(configuration_id=c['configuration_id'],alternative_id=c['alternative_id'],focus=label,
                    effect=c['effect'],upper_mi=c['mi_q'],bootstrap_repetitions=repetitions,count=len(alt['absolute']))
        quantities=[]
        for i,location in enumerate(('lower','upper')):
            for k,m in enumerate(study.METHODS):
                quantities.append((location,m,point[4*i+k],draws[:,j,4*i+k]))
            for k,m in enumerate(study.METHODS):
                if m!='expanded':
                    quantities.append((location,'expanded_minus_'+m,point[4*i+2]-point[4*i+k],draws[:,j,4*i+2]-draws[:,j,4*i+k]))
        for k,m in enumerate(study.METHODS):
            if m!='expanded':
                quantities.append(('upper_minus_lower','expanded_minus_'+m,
                                   (point[6]-point[4+k])-(point[2]-point[k]),
                                   (draws[:,j,6]-draws[:,j,4+k])-(draws[:,j,2]-draws[:,j,k])))
        for location,quantity,value,values in quantities:
            low,high=np.quantile(values,[.025,.975])
            rows.append(dict(**common,calibration=location,quantity=quantity,estimate=value,
                             low=low,high=high,mcse=float(np.std(values,ddof=1))))
    return rows


def cross_null_rates(base,output,cases):
    configs=pd.read_csv(base/'configurations.csv').set_index('configuration_id').to_dict('index')
    lower_refs=json.loads((base/'references.json').read_text())
    upper_refs=json.loads((output/'references.json').read_text())
    rows=[]
    for c in cases:
        for location,root,key,config in [('lower',base,c['lower_id'],configs[c['lower_id']]),
                                          ('upper',output,c['configuration_id'],c)]:
            records=study.load_records(root,'evaluation',key)
            data=prepared(records,config,lower_refs[c['lower_id']])
            methods,_=study.method_values(records,config,lower_refs[c['lower_id']]['nu_ref'])
            for calibration,ref in [('lower',lower_refs[c['lower_id']]),('upper',upper_refs[c['configuration_id']])]:
                decisions=reject(data,ref['calibration'])
                for i,m in enumerate(study.METHODS):
                    k=int(decisions[:,i].sum()); n=len(decisions)
                    low,high=study.wilson(k,n)
                    rows.append(dict(focus=c['focus'],effect=c['effect'],null_location=location,
                                     calibration=calibration,method=m,rejected=k,count=n,rate=k/n,low=low,high=high))
                    rows[-1]['valid_count']=int(methods[m][1].sum())
    return pd.DataFrame(rows)


def dependence(base,output):
    configs=pd.read_csv(base/'configurations.csv')
    cases=[(label,select_case(configs,*spec)) for label,spec in study.FOCUS.items()]
    cases += [(f'16, {"same" if profile=="same_skew" else "different"}, {n:,}',select_case(configs,16,profile,n))
              for profile in ('same_skew','different_skew') for n in (1000,10000)]
    cases += [('2, same, 100',select_case(configs,2,'same_skew',100))]
    rows=[]
    for label,key in cases:
        r=study.load_records(base,'evaluation',key)
        mask=np.isfinite(r['delta_corrected'])&np.isfinite(r['standard_error'])
        delta=r['delta_corrected'][mask]; se=r['standard_error'][mask]
        rows.append(dict(setting=label,configuration_id=key,count=int(mask.sum()),
                         excluded_count=int((~mask).sum()),sampling_mean=float(delta.mean()),
                         centered_magnitude_spearman=float(spearmanr(abs(delta-delta.mean()),se).statistic)))
    pd.DataFrame(rows).to_csv(output/'dependence_diagnostics.csv',index=False)


def write_tables(output,figures):
    power=pd.read_csv(output/'power.csv')
    gains=power[power.quantity.eq('expanded_minus_wald')].set_index(['focus','effect','calibration'])
    rows=[]
    for label in study.FOCUS:
        for effect in (2.,4.):
            lo,hi=[gains.loc[(label,effect,p)] for p in ('lower','upper')]
            rows.append([f'{label}: {effect:g}',f'{lo.upper_mi:.4f}',
                         f'{100*lo.estimate:+.2f} [{100*lo.low:+.2f}, {100*lo.high:+.2f}]',
                         f'{100*hi.estimate:+.2f} [{100*hi.low:+.2f}, {100*hi.high:+.2f}]'])
    table(figures/'focused_redesign_calibration_sensitivity.tex',
          ['Setting: SD','Upper MI','Lower-null gain (pp)','Upper-null gain (pp)'],rows)
    rows=[]
    values=power[power.quantity.isin(study.METHODS)].set_index(['focus','effect','calibration','quantity'])
    for label in study.FOCUS:
        for effect in (2.,4.):
            for location in ('lower','upper'):
                rows.append([f'{label}: {effect:g}, {location}']+
                            [f'{values.loc[(label,effect,location,m),"estimate"]:.4f}' for m in ('wald','size','expanded')])
    table(figures/'focused_redesign_sensitivity_power_full.tex',['Setting: SD, null','Wald/ref.','Size df','Expanded'],rows)
    cross=pd.read_csv(output/'cross_null_rates.csv').set_index(['focus','effect','calibration','null_location','method'])
    rows=[]
    for label in study.FOCUS:
        for effect in (2.,4.):
            for calibration in ('lower','upper'):
                for location in ('lower','upper'):
                    rows.append([f'{label}: {effect:g}',calibration,location]+
                                [f'{cross.loc[(label,effect,calibration,location,m),"rate"]:.4f}' for m in ('wald','size','expanded')])
    table(figures/'focused_redesign_sensitivity_cross_null.tex',
          ['Setting: SD','Fitting null','Evaluation null','Wald/ref.','Size df','Expanded'],rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,default=study.OUTPUT)
    parser.add_argument('--output',type=Path,default=sensitivity.OUTPUT)
    parser.add_argument('--figures',type=Path,default=FIGURES)
    parser.add_argument('--bootstrap',type=int,default=1000)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args(); sensitivity.audit(args.output,args.base)
    args.figures.mkdir(parents=True,exist_ok=True)
    if args.bootstrap:
        rows=[]
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for future in as_completed([pool.submit(bootstrap_focus,(str(args.base),str(args.output),label,args.bootstrap)) for label in study.FOCUS]):
                rows.extend(future.result()); print('Completed sensitivity bootstrap focus',flush=True)
        pd.DataFrame(rows).sort_values(['focus','effect','calibration','quantity']).to_csv(args.output/'power.csv',index=False)
    cases,_=sensitivity.design(args.base)
    cross_null_rates(args.base,args.output,cases).to_csv(args.output/'cross_null_rates.csv',index=False)
    dependence(args.base,args.output)
    write_tables(args.output,args.figures)
    study.atomic_json(args.output/'report_provenance.json',dict(
        report_sha256=study.sha(Path(__file__)),base_report_sha256=study.sha(Path(__file__).with_name('redesign_report.py')),
        inputs={name:study.sha(args.output/name) for name in ['protocol.json','references.json','audit.json','power.csv','cross_null_rates.csv','dependence_diagnostics.csv']},
        uncertainty='Joint fitting-sample and paired evaluation bootstrap for power; conditional Wilson intervals for cross-null rates',
        bootstrap_repetitions=int(pd.read_csv(args.output/'power.csv').bootstrap_repetitions.iloc[0])))


if __name__=='__main__': main()
