"""Inspect saved Chapter 6 curves without modifying experiment outputs.

The optional support decomposition reconstructs the first recorded evaluation
chunk from its original streams, then checks its MI, variance and empty-cell
outputs against the saved records. It introduces no new evaluation samples.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr, t

import redesign_study as study
from redesign_report import select_case


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def describe(values):
    values=np.asarray(values)
    finite=values[np.isfinite(values)]
    if not len(finite):
        return {'count':0}
    return {'count':len(finite),'mean':float(finite.mean()),
            'sd':float(finite.std(ddof=1)),
            'quantiles':dict(zip(('p05','median','p95'),map(float,np.quantile(finite,[.05,.5,.95]))))}


def raw_diagnostics(config,records,population):
    delta=records['delta_corrected']; se2=records['squared_standard_error']
    vw=records['base_valid'].astype(bool); ve=records['expanded_valid'].astype(bool)
    rw=vw & (records['normal_p_value']<=.05)
    re=ve & (records['expanded_welch_p_value']<=.05)
    assert not np.any(re & ~rw)
    obsvar=float(np.var(delta,ddof=1))
    matched=np.isfinite(delta)&np.isfinite(records['standard_error'])
    centered=delta[matched]-delta[matched].mean()
    rms=np.sqrt(np.mean(se2[matched]))
    df=records['expanded_welch_degrees_of_freedom']
    result={'configuration_id':config['configuration_id'],
            'delta':describe(delta),'standard_error':describe(records['standard_error']),
            'bias':float(delta.mean()-config['true_delta']),
            'bias_sd':float((delta.mean()-config['true_delta'])/np.sqrt(obsvar)),
            'mean_se2_over_observed_variance':float(se2.mean()/obsvar),
            'centered_magnitude_se_spearman':float(spearmanr(abs(centered),records['standard_error'][matched]).statistic),
            'fixed_rms_se_tail_diagnostic':float(np.mean(abs(delta[matched])/rms>=norm.ppf(.975))),
            'statistic_on_wald_valid':describe(records['statistic'][vw]),
            'df_on_expanded_valid':describe(df[ve]),
            'student_cutoff_on_expanded_valid':describe(t.ppf(.975,df[ve])),
            'wald_rate':float(rw.mean()),'expanded_rate':float(re.mean()),
            'wald_valid_fraction':float(vw.mean()),'expanded_valid_fraction':float(ve.mean()),
            'wald_rejections_on_expanded_invalid':int(np.count_nonzero(rw & ~ve)),
            'wald_only_rejections_on_common_valid':int(np.count_nonzero(rw & ~re & ve)),
            'wald_positive_tail':int(np.count_nonzero(rw & (delta>0))),
            'wald_negative_tail':int(np.count_nonzero(rw & (delta<0))),
            'sides':{}}
    for side in 'pq':
        n=config['n_'+side]; v=records['influence_variance_'+side]
        tau=records['variance_influence_variance_'+side]
        nu=records['expanded_component_degrees_of_freedom_'+side]
        mi=records['plugin_mi_'+side]; valid=np.isfinite(nu)&(nu>0)
        target=2*v.mean()**2/np.var(v,ddof=1)
        pop=population[side]
        row={'v':describe(v),'tau2':describe(tau),'df':describe(nu[valid]),
             'zero_v_fraction':float(np.mean(v==0)),
             'df_valid_fraction':float(valid.mean()),
             'mean_occupied_cells':float(config['k']**2-records['empty_cells_'+side].mean()),
             'mean_occupied_rows':float(config['k']-records['empty_rows_'+side].mean()),
             'mean_occupied_columns':float(config['k']-records['empty_columns_'+side].mean()),
             'moment_target':float(target),
             'df_ratio_of_means_over_target':float(np.var(v,ddof=1)/(tau.mean()/n)),
             'mean_df_over_target':float(nu.mean()/target) if valid.all() else None,
             'mean_two_mi_over_mean_v':float(2*mi.mean()/v.mean()),
             'variance_two_mi_over_variance_v':float(np.var(2*mi,ddof=1)/np.var(v,ddof=1)),
             'mean_four_v_over_mean_tau2':float(4*v.mean()/tau.mean()),
             'mean_n_mi_over_mean_df':float(n*mi.mean()/nu.mean()) if valid.all() else None,
             'observed_G_variance_over_local_prediction':float(np.var(2*n*mi,ddof=1)/(2*((config['k']-1)**2+4*n*config['mi_'+side]))),
             'expected_occupied_cells':float(np.sum(-np.expm1(n*np.log1p(-pop))))}
        if valid.all():
            np.testing.assert_allclose(nu,2*n*v*v/tau,rtol=1e-12)
            row['mean_df_over_ratio_of_means']=float(nu.mean()/(2*n*v.mean()**2/tau.mean()))
        result['sides'][side]=row
    return result


def support_decomposition(base,config,populations):
    directory=base/'evaluation'/config['configuration_id']
    identity=json.loads((directory/'identity.json').read_text())
    count=min(study.CHUNK,identity['count'])
    path=directory/'chunk_000.npz'
    meta=json.loads(path.with_suffix('.json').read_text())
    assert sha(path)==meta['sha256'] and meta['count']==count
    with np.load(path,allow_pickle=False) as saved:
        result={'configuration_id':config['configuration_id'],'count':count,
                'existing_chunk_sha256':meta['sha256'],'sides':{}}
        for side in 'pq':
            p=populations[side];n=config['n_'+side]
            rng=np.random.default_rng(study.seed_for(identity['stream_phase'],config['configuration_id'],0,side))
            true_ell=np.log(p/(p.sum(axis=1)[:,None]*p.sum(axis=0)[None,:]))
            true_mi=np.sum(p*true_ell);true_v=np.sum(p*(true_ell-true_mi)**2)
            true_row=np.sum(p*true_ell,axis=1,keepdims=True)/p.sum(axis=1,keepdims=True)
            true_col=np.sum(p*true_ell,axis=0,keepdims=True)/p.sum(axis=0,keepdims=True)
            true_g=(true_ell-true_mi)**2-true_v+2*(true_ell-true_row-true_col+true_mi)
            np.testing.assert_allclose(np.sum(p*true_g),0,atol=1e-12)
            parts=[];linear_parts=[];tau_parts=[]
            totals={'isolated_singleton':0.,'other_singleton':0.,'repeated_cell':0.,
                    'isolated_singleton_count':0.,'singleton_count':0.,'fixed_weight_variance':0.,'variance':0.}
            for start in range(0,count,250):
                stop=min(count,start+250)
                counts=rng.multinomial(n,p.ravel(),size=stop-start).reshape(-1,*p.shape)
                rows=counts.sum(axis=2,keepdims=True);cols=counts.sum(axis=1,keepdims=True)
                weights=counts/n
                with np.errstate(divide='ignore',invalid='ignore'):
                    ell=np.where(counts>0,np.log(n*counts/(rows*cols)),0.)
                mi=np.sum(weights*ell,axis=(1,2))
                contributions=weights*(ell-mi[:,None,None])**2
                v=contributions.sum(axis=(1,2))
                np.testing.assert_allclose(mi,saved['plugin_mi_'+side][start:stop],rtol=1e-12,atol=1e-13)
                np.testing.assert_allclose(v,saved['influence_variance_'+side][start:stop],rtol=1e-12,atol=1e-13)
                np.testing.assert_array_equal((counts==0).sum(axis=(1,2)),saved['empty_cells_'+side][start:stop])
                isolated=(counts==1)&(rows==1)&(cols==1)
                np.testing.assert_allclose(ell[isolated],np.log(n),rtol=1e-12)
                masks={'isolated_singleton':isolated,'other_singleton':(counts==1)&~isolated,
                       'repeated_cell':counts>1}
                for label,mask in masks.items():totals[label]+=float(contributions[mask].sum())
                parts.append(np.column_stack([np.sum(np.where(mask,contributions,0),axis=(1,2)) for mask in masks.values()]))
                linear_parts.append(np.sum(weights*true_g,axis=(1,2)))
                row_p=rows/n;col_p=cols/n
                row_mean=np.divide(np.sum(weights*ell,axis=2,keepdims=True),row_p,out=np.zeros_like(row_p,dtype=float),where=row_p>0)
                col_mean=np.divide(np.sum(weights*ell,axis=1,keepdims=True),col_p,out=np.zeros_like(col_p,dtype=float),where=col_p>0)
                empirical_g=(ell-mi[:,None,None])**2-v[:,None,None]+2*(ell-row_mean-col_mean+mi[:,None,None])
                empirical_g-=np.sum(weights*empirical_g,axis=(1,2))[:,None,None]
                tau_contributions=weights*empirical_g**2
                np.testing.assert_allclose(tau_contributions.sum(axis=(1,2)),saved['variance_influence_variance_'+side][start:stop],rtol=1e-11,atol=1e-12)
                tau_parts.append(np.column_stack([np.sum(np.where(mask,tau_contributions,0),axis=(1,2)) for mask in masks.values()]))
                totals['isolated_singleton_count']+=int(isolated.sum())
                totals['singleton_count']+=int((counts==1).sum())
                true_sample_mean=np.sum(weights*true_ell,axis=(1,2))
                totals['fixed_weight_variance']+=float(np.sum(weights*(true_ell-true_sample_mean[:,None,None])**2))
                totals['variance']+=float(v.sum())
            np.testing.assert_allclose(sum(totals[k] for k in masks),totals['variance'],rtol=1e-12)
            result['sides'][side]={k:value/count for k,value in totals.items()}
            part=np.concatenate(parts);v=part.sum(axis=1);linear=np.concatenate(linear_parts)
            remainder=v-true_v-linear
            covariance=np.cov(part,rowvar=False,ddof=1)
            observed=np.var(v,ddof=1)
            var_l=np.var(linear,ddof=1);var_r=np.var(remainder,ddof=1)
            cov_lr=np.cov(linear,remainder,ddof=1)[0,1]
            np.testing.assert_allclose(var_l+var_r+2*cov_lr,observed,rtol=1e-12)
            result['sides'][side].update({'variance_contribution_groups':list(masks),
                'covariance_with_total_over_total_variance':(covariance.sum(axis=1)/observed).tolist(),
                'mean_tau2_contributions':np.concatenate(tau_parts).mean(axis=0).tolist(),
                'linear_variance_over_actual':float(var_l/observed),
                'remainder_variance_over_actual':float(var_r/observed),
                'twice_linear_remainder_covariance_over_actual':float(2*cov_lr/observed)})
    result['reconstructed_scalar_outputs_match_saved_chunk']=True
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',type=Path,default=study.OUTPUT)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--support-decomposition',action='store_true')
    args=parser.parse_args();base=args.results.resolve()
    if args.output.resolve().is_relative_to(base):
        raise ValueError('Write diagnostics outside the preserved experiment-results directory.')
    configs=pd.read_csv(base/'configurations.csv')
    displays=pd.read_csv(base/'displays.csv',keep_default_na=False)
    moments=pd.read_csv(base/'moments.csv')
    diagnostics=pd.read_csv(base/'diagnostics.csv')
    rates=pd.read_csv(base/'rates.csv')
    focus=pd.read_csv(base/'focus.csv')
    ids=set(displays[displays.study.eq('null')].configuration_id)
    broad=configs[configs.configuration_id.isin(ids)].merge(diagnostics,on='configuration_id')
    broad=broad.merge(rates[rates.denominator.eq('all')&rates.method.isin(['wald','expanded'])],on='configuration_id')
    chosen=set()
    for profile,k,ns in [('different_skew',16,[10,20,50,100,250,500,1000,2500,10000,50000]),
                         ('different_skew',4,[10,20,50,100,250,1000,10000]),
                         ('uniform',16,[10,20,50,100,250,500,1000,2500,10000]),
                         ('uniform',4,[20,100]),('uniform',2,[10,50,250,1000])]:
        chosen.update(select_case(configs,k,profile,n) for n in ns)
    association=set(displays[displays.study.eq('association')].configuration_id)
    near=configs[configs.configuration_id.isin(association)&configs.profile.eq('different_skew')&configs.n_p.eq(1000)]
    chosen.update(near.configuration_id);chosen.update(focus.configuration_id)
    raw=[]
    support=[]
    with np.load(base/'populations.npz',allow_pickle=False) as arrays:
        for i,key in enumerate(sorted(chosen)):
            c=configs[configs.configuration_id.eq(key)].iloc[0].to_dict()
            populations={side:arrays[c['pair_id']+'_'+side] for side in 'pq'}
            records=study.load_records(base,'evaluation',key)
            raw.append(raw_diagnostics(c,records,populations))
            if args.support_decomposition and c['k']==16 and c['profile']=='different_skew' and c['n_p'] in [10,20,50,100,250,1000,10000] and c['mi_p']==.02 and c['mi_q']==.02:
                support.append(support_decomposition(base,c,populations))
            if (i+1)%10==0:print(f'Checked saved records for {i+1}/{len(chosen)} settings',flush=True)
    numeric=moments[moments.configuration_id.isin(ids)].copy()
    relation=1/(numeric.mean_ratio**2*numeric.variance_ratio)
    np.testing.assert_allclose(relation,numeric.df_ratio,rtol=1e-11)
    value={'status':'diagnostics from saved evaluation records; no experiment outputs modified',
           'source_sha256':sha(__file__),
           'inputs_sha256':{name:sha(base/name) for name in ['configurations.csv','displays.csv','moments.csv','diagnostics.csv','rates.csv','focus.csv','populations.npz']},
           'broad_null':broad.to_dict('records'),'raw_diagnostics':raw,'support_decomposition':support,
           'population_df_ratio_identity_checked_rows':len(numeric)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    print(f'Wrote {len(raw)} saved-record diagnostics and {len(support)} verified support decompositions.',flush=True)


if __name__=='__main__':main()
