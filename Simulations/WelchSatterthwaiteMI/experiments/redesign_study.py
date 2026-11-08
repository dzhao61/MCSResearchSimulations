"""Independent 100,000-pair redesign: fitting, evaluation, calibration and audit."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import time

import numpy as np
import pandas as pd
from scipy.stats import norm, t, skew

from same_skew_extension_core import build_extended_design
from focused_study_core import (ROOT, PROFILES, COMMON_MI, TOLERANCES,
                                construct_copying, evaluate_tables, digest)
from thesis_redesign_core import margin
from report_focused_mechanisms import population_moments

OUTPUT = ROOT / 'results/approximation_redesign'
SEED = 20261021
REPLICATES = 100000
CHUNK = 10000
ALPHA = .05
METHODS = ('wald', 'size', 'expanded', 'reference')
FOCUS = {'A': (4, 'uniform', 20), 'B': (8, 'different_skew', 100),
         'C': (4, 'different_skew', 10000)}
EFFECTS = tuple(np.arange(0, 4.01, .5))


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')
    tmp.replace(path)


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def fingerprint():
    paths = [Path(__file__), Path(__file__).with_name('focused_study_core.py'),
             Path(__file__).with_name('same_skew_extension_core.py'),
             Path(__file__).with_name('thesis_redesign_core.py'),
             ROOT/'src/welch_differential_mi/welch.py',
             ROOT.parent/'DifferentialMI/src/differential_mi/statistics.py']
    return digest({str(p.relative_to(ROOT.parent)): sha(p) for p in paths})


def seed_for(phase, key, chunk, side):
    return int(digest([SEED, phase, key, chunk, side])[:16], 16)


def build_design(references=None):
    old, display, populations, arrays, _ = build_extended_design()
    configs = {c['configuration_id']: {**c, 'replicates': REPLICATES} for c in old}
    pairs = {p['pair_id']: p for p in populations}
    displays = {(r['study'], r['configuration_id']) for r in display if r['study'] != 'association'}

    def add(study, k, profile, ip, iq, n, nq=None, focus='', effect=None):
        nq = n if nq is None else nq
        spec = dict(k=k, profile=profile, mi_p=round(float(ip), 12),
                    mi_q=round(float(iq), 12), construction='copying')
        pair_id = 'pair_' + digest(spec)[:16]
        if pair_id not in pairs:
            row = {'pair_id': pair_id, **spec}
            tables = []
            for side, rho in zip('pq', PROFILES[profile]):
                a = margin(k, rho)
                result = construct_copying(a, spec['mi_'+side])
                moment = population_moments(result.probability)
                row.update({f'achieved_mi_{side}': moment['mi'],
                            f'variance_{side}': moment['variance'],
                            f'variance_sensitivity_variance_{side}': moment['tau2'],
                            f'minimum_probability_{side}': float(result.probability.min()),
                            f'margin_{side}': a.tolist(), f'strength_{side}': result.strength,
                            f'endpoint_mi_{side}': result.endpoint_mi})
                tables.append(result.probability)
            pairs[pair_id] = row
            arrays[pair_id] = tuple(tables)
        key = 'setting_' + digest([pair_id, n, nq])[:16]
        configs.setdefault(key, dict(configuration_id=key, pair_id=pair_id, **spec,
                                     n_p=n, n_q=nq, delta=spec['mi_p']-spec['mi_q'],
                                     replicates=REPLICATES))
        displays.add((study, key))
        if focus:
            focus_rows.append(dict(configuration_id=key, focus=focus,
                                   standardised_difference=float(effect),
                                   difference_nats=spec['mi_q']-spec['mi_p']))
        return key

    focus_rows = []
    for profile in PROFILES:
        for common in COMMON_MI:
            for n in (100, 1000, 10000):
                add('association', 4, profile, common, common, n)
    if len(configs) != 342:
        raise AssertionError('Base redesign scope changed')
    focus_nulls = {}
    for label, (k, profile, n) in FOCUS.items():
        key = add('focus', k, profile, .02, .02, n, focus=label, effect=0)
        focus_nulls[label] = key
        if references is not None:
            sd = references[key]['null_sd']
            for effect in EFFECTS[1:]:
                add('focus', k, profile, .02, .02+effect*sd, n,
                    focus=label, effect=effect)
    null_lookup = {}
    for c in configs.values():
        if c['mi_p'] == c['mi_q']:
            null_lookup[(c['k'], c['profile'], c['construction'], c['n_p'],
                         c['n_q'], c['mi_p'])] = c['configuration_id']
    if len(null_lookup) != 186:
        raise AssertionError('Null fitting scope changed')
    for c in configs.values():
        c['reference_id'] = null_lookup[(c['k'], c['profile'], c['construction'],
                                        c['n_p'], c['n_q'], c['mi_p'])]
        p, q = arrays[c['pair_id']]
        c['true_delta'] = population_moments(p)['mi']-population_moments(q)['mi']
    return (sorted(configs.values(), key=lambda c: c['configuration_id']),
            [dict(study=s, configuration_id=k) for s, k in sorted(displays)],
            pairs, arrays, focus_rows, focus_nulls)


def sample(config, p, q, phase, index, count, batch=250):
    rp = np.random.default_rng(seed_for(phase, config['configuration_id'], index, 'p'))
    rq = np.random.default_rng(seed_for(phase, config['configuration_id'], index, 'q'))
    parts = {}
    for start in range(0, count, batch):
        size = min(batch, count-start)
        cp = rp.multinomial(config['n_p'], p.ravel(), size=size).reshape(size, *p.shape)
        cq = rq.multinomial(config['n_q'], q.ravel(), size=size).reshape(size, *q.shape)
        for key, values in evaluate_tables(cp, cq).items():
            parts.setdefault(key, []).append(values)
    return {key: np.concatenate(values) for key, values in parts.items()}


def load_records(output, phase, key):
    directory = Path(output)/phase/key
    identity = json.loads((directory/'identity.json').read_text())
    parts = {}
    for index, offset in enumerate(range(0, identity['count'], CHUNK)):
        path = directory/f'chunk_{index:03d}.npz'
        meta = json.loads(path.with_suffix('.json').read_text())
        if sha(path) != meta['sha256'] or meta['count'] != min(CHUNK, identity['count']-offset):
            raise AssertionError('Corrupt chunk: '+str(path))
        with np.load(path, allow_pickle=False) as data:
            for field in data.files:
                if data[field].shape != (meta['count'],):
                    raise AssertionError('Malformed scalar records')
                parts.setdefault(field, []).append(data[field])
    return {k: np.concatenate(v) for k, v in parts.items()}


def run_task(task):
    output, phase, config, p, q, count, fp = task
    directory = Path(output)/phase/config['configuration_id']
    directory.mkdir(parents=True, exist_ok=True)
    stream_phase = 'pilot_'+phase if Path(output).name == 'pilot' else phase
    identity = {'config': config, 'phase': phase, 'stream_phase': stream_phase, 'count': count, 'source': fp,
                'seed': SEED, 'chunk': CHUNK}
    target = directory/'identity.json'
    if target.exists() and json.loads(target.read_text()) != identity:
        raise RuntimeError('Incompatible checkpoint '+str(directory))
    atomic_json(target, identity)
    started = time.perf_counter()
    for index, offset in enumerate(range(0, count, CHUNK)):
        path = directory/f'chunk_{index:03d}.npz'
        count_chunk = min(CHUNK, count-offset)
        if path.exists() and path.with_suffix('.json').exists():
            meta = json.loads(path.with_suffix('.json').read_text())
            if meta != {'sha256': sha(path), 'count': count_chunk}:
                raise RuntimeError('Corrupt checkpoint')
            continue
        records = sample(config, p, q, stream_phase, index, count_chunk)
        with path.with_suffix('.tmp').open('wb') as handle:
            np.savez_compressed(handle, **records)
        path.with_suffix('.tmp').replace(path)
        atomic_json(path.with_suffix('.json'), {'sha256': sha(path), 'count': count_chunk})
    return {'configuration_id': config['configuration_id'], 'phase': phase,
            'count': count, 'seconds': time.perf_counter()-started}


def execute(output, phase, configs, arrays, count, workers):
    tasks = [(str(output), phase, c, *arrays[c['pair_id']], count, fingerprint()) for c in configs]
    execution = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for future in as_completed([pool.submit(run_task, task) for task in tasks]):
            execution.append(future.result())
            if len(execution) % 10 == 0 or len(execution) == len(tasks):
                print(f'{phase}: {len(execution)}/{len(tasks)} settings', flush=True)
    pd.DataFrame(execution).to_csv(Path(output)/f'{phase}_execution.csv', index=False)


def mcse(influence):
    x = np.asarray(influence)
    return float(np.std(x, ddof=1)/np.sqrt(len(x)))


def moment_summary(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2 or np.any(x < 0):
        raise ValueError('Insufficient or negative variance records')
    mean = float(np.mean(x))
    variance = float(np.var(x, ddof=1))
    if variance <= 0 or mean <= 0:
        raise ValueError('Degenerate moment target')
    im = x-mean
    iv = im**2-variance
    nu = 2*mean**2/variance
    inu = 4*mean/variance*im-2*mean**2/variance**2*iv
    return {'count': len(x), 'zero_count': int((x == 0).sum()), 'mean': mean,
            'variance': variance, 'mean_mcse': mcse(im), 'variance_mcse': mcse(iv),
            'nu_mom': nu, 'nu_mom_mcse': mcse(inu)}


def method_values(records, config, reference_df):
    a = records['influence_variance_p']/config['n_p']
    b = records['influence_variance_q']/config['n_q']
    with np.errstate(divide='ignore', invalid='ignore'):
        df = (a+b)**2/(a*a/config['n_p']+b*b/config['n_q'])
    statistic = records['statistic']
    valid_base = records['base_valid'].astype(bool)
    size_p = 2*t.sf(np.abs(statistic), df)
    ref_p = 2*t.sf(np.abs(statistic), reference_df)
    values = {
        'wald': (records['normal_p_value'], valid_base),
        'size': (size_p, valid_base & np.isfinite(df) & (df > 0) & np.isfinite(size_p)),
        'expanded': (records['expanded_welch_p_value'], records['expanded_valid'].astype(bool)),
        'reference': (ref_p, valid_base & np.isfinite(ref_p)),
    }
    return values, df


def calibration_threshold(pvalues, valid):
    x = np.where(valid & np.isfinite(pvalues), pvalues, 1.)
    # Strict inequality excludes every tie at the boundary and never exceeds 5% in fitting.
    index = min(int(ALPHA*len(x)), len(x)-1)
    return float(np.partition(x, index)[index])


def calibrate(records, config, reference_df):
    methods, _ = method_values(records, config, reference_df)
    result = {m: calibration_threshold(*methods[m]) for m in METHODS}
    absolute = np.where(records['base_valid'], np.abs(records['statistic']), -np.inf)
    index = len(absolute)-int(ALPHA*len(absolute))-1
    result['absolute_t'] = float(np.partition(absolute, index)[index])
    return result


def decisions(records, config, reference, calibrated=False):
    methods, _ = method_values(records, config, reference['nu_ref'])
    out = {}
    for m, (p, valid) in methods.items():
        if calibrated and m in ('wald', 'reference'):
            out[m] = valid & (np.abs(records['statistic']) > reference['calibration']['absolute_t'])
        elif calibrated:
            out[m] = valid & (p < reference['calibration'][m])
        else:
            out[m] = valid & (p <= ALPHA)
    return methods, out


def fit_references(output, configs):
    references = {}
    for c in configs:
        r = load_records(output, 'fit', c['configuration_id'])
        components = {s: moment_summary(r['influence_variance_'+s]) for s in 'pq'}
        mean = sum(components[s]['mean']/c['n_'+s] for s in 'pq')
        variance = sum(components[s]['variance']/c['n_'+s]**2 for s in 'pq')
        nu = 2*mean**2/variance
        im = sum((r['influence_variance_'+s]-components[s]['mean'])/c['n_'+s] for s in 'pq')
        iv = sum(((r['influence_variance_'+s]-components[s]['mean'])**2-components[s]['variance'])/c['n_'+s]**2 for s in 'pq')
        inu = 4*mean/variance*im-2*mean**2/variance**2*iv
        delta = r['delta_corrected']
        sd = float(np.std(delta, ddof=1))
        direct = float(np.var(r['squared_standard_error'], ddof=1))
        references[c['configuration_id']] = {
            'nu_ref': nu, 'nu_ref_mcse': mcse(inu), 'components': components,
            'mean_squared_se': mean, 'variance_squared_se': variance,
            'direct_variance_squared_se': direct, 'direct_component_ratio': direct/variance,
            'null_sd': sd, 'null_sd_mcse': mcse(((delta-delta.mean())**2-sd**2)/(2*sd)),
            'calibration': calibrate(r, c, nu), 'count': len(delta)}
    atomic_json(Path(output)/'references.json', references)
    return references


def wilson(k, n):
    if not n:
        return (math.nan, math.nan)
    z = norm.ppf(.975)
    p = k/n
    centre = (p+z*z/(2*n))/(1+z*z/n)
    half = z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return float(centre-half), float(centre+half)


def corr(a, b):
    finite = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(a[finite], b[finite])[0, 1]) if finite.sum()>2 and np.std(a[finite])>0 and np.std(b[finite])>0 else math.nan


def aggregate(output, configs, pairs, arrays, references):
    rates, contrasts, moments, diagnostics, calibrated_rows = [], [], [], [], []
    for index, c in enumerate(configs):
        key = c['configuration_id']
        r = load_records(output, 'evaluation', key)
        reference = references[c['reference_id']]
        methods, reject = decisions(r, c, reference)
        _, calibrated = decisions(r, c, reference, calibrated=True)
        if not np.array_equal(calibrated['wald'], calibrated['reference']):
            raise AssertionError('Fixed-reference calibrated decisions disagree')
        all_mask = np.ones(len(r['statistic']), bool)
        common = np.logical_and.reduce([v for _, v in methods.values()])
        for m, (pvalues, valid) in methods.items():
            for denominator, mask in [('all', all_mask), ('method_valid', valid), ('common_valid', common)]:
                n = int(mask.sum())
                k = int((reject[m] & mask).sum())
                low, high = wilson(k, n)
                direction_wrong = int((reject[m] & mask & (r['delta_corrected']*c['true_delta'] < 0)).sum()) if c['true_delta'] else 0
                rates.append(dict(configuration_id=key, method=m, denominator=denominator,
                                  count=n, valid_count=int(valid.sum()), rejected=k,
                                  rate=k/n if n else math.nan, low=low, high=high,
                                  mcse=math.sqrt(k/n*(1-k/n)/n) if n else math.nan,
                                  wrong_direction=direction_wrong))
            k = int(calibrated[m].sum())
            low, high = wilson(k, len(all_mask))
            calibrated_rows.append(dict(configuration_id=key, method=m, count=len(all_mask),
                                        rejected=k, rate=k/len(all_mask), low=low, high=high))
        for other in ('wald', 'size', 'reference'):
            for label, mask in [('all', all_mask), ('common_valid', common)]:
                d = reject['expanded'][mask].astype(float)-reject[other][mask]
                se = mcse(d) if len(d)>1 else math.nan
                mean = float(d.mean()) if len(d) else math.nan
                contrasts.append(dict(configuration_id=key, comparator=other, denominator=label,
                                      difference=mean, mcse=se, low=mean-1.96*se, high=mean+1.96*se,
                                      only_expanded=int((d==1).sum()), only_comparator=int((d==-1).sum()), count=len(d)))
        for side, table in zip('pq', arrays[c['pair_id']]):
            pop = population_moments(table)
            x = r['influence_variance_'+side]
            tx = r['variance_influence_variance_'+side]
            measured = moment_summary(x)
            n = c['n_'+side]
            fo = 2*n*pop['variance']**2/pop['tau2']
            mean_ratio = measured['mean']/pop['variance']
            variance_ratio = (pop['tau2']/n)/measured['variance']
            df_ratio = fo/measured['nu_mom']
            np.testing.assert_allclose(df_ratio, mean_ratio**-2/variance_ratio, rtol=1e-12)
            nuhat = r['expanded_component_degrees_of_freedom_'+side]
            mask = np.isfinite(nuhat) & (nuhat > 0)
            d = (c['k']-1)**2
            kappa = 2*n*pop['mi']
            row = dict(configuration_id=key, side=side, k=c['k'], profile=c['profile'],
                       construction=c['construction'], n=n, mi=pop['mi'],
                       population_v=pop['variance'], population_tau2=pop['tau2'],
                       **measured, mean_ratio=mean_ratio,
                       mean_ratio_mcse=measured['mean_mcse']/pop['variance'],
                       variance_ratio=variance_ratio,
                       variance_ratio_mcse=variance_ratio*measured['variance_mcse']/measured['variance'],
                       plugin_variance_ratio=float(np.mean(tx[np.isfinite(tx)])/n/measured['variance']),
                       nu_fo=fo, df_ratio=df_ratio,
                       df_ratio_mcse=df_ratio*measured['nu_mom_mcse']/measured['nu_mom'],
                       scaled_mean_error=n*(measured['mean']-pop['variance']),
                       scaled_mean_error_mcse=n*measured['mean_mcse'],
                       df_valid_count=int(mask.sum()),
                       df_mean=float(np.mean(nuhat[mask])) if mask.any() else math.nan,
                       df_mean_mcse=mcse(nuhat[mask]) if mask.sum()>1 else math.nan,
                       df_median=float(np.median(nuhat[mask])) if mask.any() else math.nan,
                       df_p05=float(np.quantile(nuhat[mask], .05)) if mask.any() else math.nan,
                       df_p95=float(np.quantile(nuhat[mask], .95)) if mask.any() else math.nan,
                       a4_scaled_mean=d+kappa, a4_scaled_variance=2*(d+2*kappa),
                       a4_df_mean=(d+kappa)/2, a4_df_mom=(d+kappa)**2/(d+2*kappa))
            moments.append(row)
        delta = r['delta_corrected']
        finite = np.isfinite(delta) & np.isfinite(r['squared_standard_error'])
        x = delta[finite]
        v = float(np.var(x, ddof=1))
        df = r['expanded_welch_degrees_of_freedom']
        good_df = np.isfinite(df) & (df > 0)
        diagnostics.append(dict(configuration_id=key, bias=float(x.mean()-c['true_delta']),
                                bias_mcse=math.sqrt(v/len(x)), observed_variance=v,
                                bias_sd=float((x.mean()-c['true_delta'])/np.sqrt(v)),
                                variance_ratio=float(r['squared_standard_error'][finite].mean()/v),
                                delta_se_correlation=corr(delta, r['standard_error']),
                                squared_delta_variance_correlation=corr(delta**2,r['squared_standard_error']),
                                statistic_df_correlation=corr(np.abs(r['statistic']), df),
                                delta_skewness=float(skew(x, bias=False)),
                                df_median=float(np.median(df[good_df])) if good_df.any() else math.nan,
                                reference_df=reference['nu_ref'], reference_df_mcse=reference['nu_ref_mcse'],
                                lower_rejections=int((reject['reference'] & (delta<0)).sum()),
                                upper_rejections=int((reject['reference'] & (delta>0)).sum())))
        if (index+1)%30 == 0:
            print(f'Summarised {index+1}/{len(configs)}', flush=True)
    for name, rows in [('rates', rates), ('paired', contrasts), ('moments', moments),
                       ('diagnostics', diagnostics), ('calibrated_rates', calibrated_rows)]:
        pd.DataFrame(rows).to_csv(Path(output)/(name+'.csv'), index=False)


def independent_values(cp, cq, reference_df):
    summaries = []
    for counts in (cp, cq):
        n = counts.sum()
        p = counts/n
        rows, cols = p.sum(1), p.sum(0)
        score = np.zeros_like(p)
        nz = p>0
        score[nz] = np.log(p[nz]/np.outer(rows,cols)[nz])
        mi = float((p*score).sum())
        v = float((p*(score-mi)**2).sum())
        rm = np.divide((p*score).sum(1), rows, out=np.zeros_like(rows), where=rows>0)
        cm = np.divide((p*score).sum(0), cols, out=np.zeros_like(cols), where=cols>0)
        influence=(score-mi)**2-v+2*(score-rm[:,None]-cm[None,:]+mi)
        tau=float((p*(influence-(p*influence).sum())**2).sum())
        # Constant occupied-cell ratios have exactly zero score variance.
        # Verify the rational ratios with integers, independently of the production helper.
        occupied=np.argwhere(counts>0)
        ai,aj=occupied[0]
        row_counts=counts.sum(1); col_counts=counts.sum(0)
        constant=all(int(counts[i,j])*int(row_counts[ai])*int(col_counts[aj]) ==
                     int(counts[ai,aj])*int(row_counts[i])*int(col_counts[j]) for i,j in occupied)
        if constant:
            v=0.; tau=0.
        nu=2*n*v*v/tau if v>0 and tau>0 else math.nan
        summaries.append((mi-(p.shape[0]-1)*(p.shape[1]-1)/(2*n),v,tau,nu,n))
    a,b=summaries
    delta=a[0]-b[0]
    se=math.sqrt(a[1]/a[4]+b[1]/b[4])
    stat=delta/se if se>0 else math.nan
    size=(a[1]/a[4]+b[1]/b[4])**2/((a[1]/a[4])**2/a[4]+(b[1]/b[4])**2/b[4]) if se>0 else math.nan
    return summaries,delta,se,stat,size


def audit(output, configs, arrays, references):
    tested=0
    for phase in ('fit','evaluation'):
        for c in configs:
            if phase=='fit' and c['mi_p']!=c['mi_q']:
                continue
            key=c['configuration_id']
            r=load_records(output,phase,key)
            p,q=arrays[c['pair_id']]
            stream_phase=json.loads((Path(output)/phase/key/'identity.json').read_text())['stream_phase']
            rp=np.random.default_rng(seed_for(stream_phase,key,0,'p'))
            rq=np.random.default_rng(seed_for(stream_phase,key,0,'q'))
            cp=rp.multinomial(c['n_p'],p.ravel(),size=8).reshape(8,*p.shape)
            cq=rq.multinomial(c['n_q'],q.ravel(),size=8).reshape(8,*q.shape)
            for i in range(8):
                components,delta,se,stat,df=independent_values(cp[i],cq[i],references[c['reference_id']]['nu_ref'])
                for field,value in [('delta_corrected',delta),('standard_error',se),('statistic',stat)]:
                    np.testing.assert_allclose(r[field][i],value,atol=1e-11,rtol=2e-10,equal_nan=True)
                for side,component in zip('pq',components):
                    for field,value in [('influence_variance_',component[1]),('variance_influence_variance_',component[2]),('expanded_component_degrees_of_freedom_',component[3])]:
                        np.testing.assert_allclose(r[field+side][i],value,atol=2e-10,rtol=2e-9,equal_nan=True)
                tested+=1
            a=r['influence_variance_p']/c['n_p']
            b=r['influence_variance_q']/c['n_q']
            np.testing.assert_allclose(r['squared_standard_error'],a+b,atol=1e-15,rtol=1e-12)
            np.testing.assert_allclose(r['delta_corrected'],r['corrected_mi_p']-r['corrected_mi_q'],atol=1e-13)
            base=(np.isfinite(r['delta_corrected']) & ((r['influence_variance_p']+r['influence_variance_q'])>1e-14)
                  & np.isfinite(r['standard_error']) & (r['standard_error']>0) & np.isfinite(r['normal_p_value']))
            np.testing.assert_array_equal(base,r['base_valid'])
            edfp=r['expanded_component_degrees_of_freedom_p']; edfq=r['expanded_component_degrees_of_freedom_q']
            with np.errstate(invalid='ignore',divide='ignore'):
                edf=(a+b)**2/(a*a/edfp+b*b/edfq)
            np.testing.assert_allclose(edf,r['expanded_welch_degrees_of_freedom'],atol=1e-10,rtol=1e-10,equal_nan=True)
            expanded=base & np.isfinite(edfp)&(edfp>0)&np.isfinite(edfq)&(edfq>0)&np.isfinite(edf)&(edf>0)
            np.testing.assert_array_equal(expanded,r['expanded_valid'])
            np.testing.assert_allclose(r['normal_p_value'][base],2*norm.sf(np.abs(r['statistic'][base])),rtol=1e-12)
            np.testing.assert_allclose(r['expanded_welch_p_value'][expanded],2*t.sf(np.abs(r['statistic'][expanded]),edf[expanded]),rtol=1e-12)
    atomic_json(Path(output)/'audit.json',{'passed':True,'settings':len(configs),
                'independently_reconstructed_pairs':tested,'checks':['all chunk hashes and dimensions',
                'independent count reconstruction and scalar probability formulas','variance and difference identities',
                'component and combined degrees of freedom','validity masks','normal and Student t p-values']})
    print(f'Audit passed: {tested} independently reconstructed pairs',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['preflight','pilot','fit','evaluate','summarize','audit','all'])
    parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    output=args.output/'pilot' if args.mode=='pilot' else args.output
    output.mkdir(parents=True,exist_ok=True)
    reference_path=output/'references.json'
    refs=json.loads(reference_path.read_text()) if reference_path.exists() else None
    configs,displays,pairs,arrays,focus_rows,focus_nulls=build_design(refs)
    protocol={'seed':SEED,'replicates':REPLICATES,'fit_replicates':REPLICATES,'chunk':CHUNK,
              'source':fingerprint(),'python':platform.python_version(),'numpy':np.__version__,
              'phase_independence':True,'alpha':ALPHA,'methods':METHODS,
              'power_effects':EFFECTS,'scope':'312 existing settings plus complete MI sweep and SD-scaled power',
              'calibration':'strict p threshold; fixed normal and reference share empirical absolute T cutoff'}
    identity=output/'protocol.json'
    if identity.exists() and json.loads(identity.read_text())!=json.loads(json.dumps(protocol)):
        raise RuntimeError('Protocol changed; use a new output directory')
    atomic_json(identity,protocol)
    nulls=[c for c in configs if c['mi_p']==c['mi_q']]
    pd.DataFrame(configs).to_csv(output/'configurations.csv',index=False)
    pd.DataFrame(displays).to_csv(output/'displays.csv',index=False)
    atomic_json(output/'populations.json',pairs)
    with (output/'populations.npz').open('wb') as f:
        np.savez_compressed(f,**{f'{key}_{side}':a for key,value in arrays.items() for side,a in zip('pq',value)})
    print(f'{len(configs)} evaluation settings; {len(nulls)} independent fitting settings',flush=True)
    if args.mode=='preflight': return
    if args.mode=='pilot':
        execute(output,'fit',nulls,arrays,200,args.workers)
        refs=fit_references(output,nulls)
        configs,displays,pairs,arrays,focus_rows,focus_nulls=build_design(refs)
        execute(output,'evaluation',configs,arrays,200,args.workers)
        aggregate(output,configs,pairs,arrays,refs)
        audit(output,configs,arrays,refs)
        return
    if args.mode in ('fit','all'):
        execute(output,'fit',nulls,arrays,REPLICATES,args.workers)
        refs=fit_references(output,nulls)
        configs,displays,pairs,arrays,focus_rows,focus_nulls=build_design(refs)
    if args.mode in ('evaluate','all'):
        if refs is None: raise RuntimeError('Fit references first')
        execute(output,'evaluation',configs,arrays,REPLICATES,args.workers)
    pd.DataFrame(configs).to_csv(output/'configurations.csv',index=False)
    pd.DataFrame(displays).to_csv(output/'displays.csv',index=False)
    pd.DataFrame(focus_rows).to_csv(output/'focus.csv',index=False)
    atomic_json(output/'focus_nulls.json',focus_nulls)
    atomic_json(output/'populations.json',pairs)
    with (output/'populations.npz').open('wb') as f:
        np.savez_compressed(f,**{f'{key}_{side}':a for key,value in arrays.items() for side,a in zip('pq',value)})
    if args.mode in ('summarize','all'):
        aggregate(output,configs,pairs,arrays,refs)
    if args.mode in ('audit','all'):
        audit(output,configs,arrays,refs)


if __name__=='__main__':
    main()
