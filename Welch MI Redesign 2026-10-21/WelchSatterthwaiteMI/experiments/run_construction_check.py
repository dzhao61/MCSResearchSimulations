"""Independent additive constructions and matched log-linear controls."""
from pathlib import Path
import argparse
import hashlib
import json
from time import perf_counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.special import xlogy

from run_detection_breakdown_sweep import (
    _simulate_configuration, stable_seed, association_table_from_interaction,
    table_with_target_mi_from_interaction, interaction_pattern,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/construction_check'
DOC = ROOT / 'docs/experiments/CONSTRUCTION_CHECK.md'
FIG = DOC.parent / 'figures/construction_check'
METHODS = {'normal_wald': ('Normal Wald', '#1f4e79', 'o'),
           'expanded_welch': ('Expanded Welch', '#b23a73', 's')}
PROTOCOL = {
    'purpose': 'Exploratory sensitivity to population construction, specified before this run',
    'sizes': [2, 3, 5, 8], 'profiles': ['uniform', 'different_skew'],
    'families': ['common', 'rare', 'spread'],
    'sample_pairs': [[10, 10], [50, 50], [250, 250], [1000, 1000], [50, 500], [500, 50]],
    'effects': [0, .1, .3, .6], 'baseline_fraction': .2,
    'replicates': 10000, 'master_seed': 2026090807, 'alpha': .05,
    'additive_endpoint_fraction': .95,
    'probes': [0, .25, .5, 1, 2, 4, 8, 16, 32, 64, 128],
    'target_rule': 'I(P)=0.2M; I(Q)=(0.2+e)M; M is minimum reachable MI across both constructions and populations',
    'profiles_detail': 'Uniform: P and Q uniform; different_skew: P first row/column .7, Q .8; other categories equal',
    'two_by_two_rule': 'Only common family: common, rare and spread directions coincide in 2x2',
    'scope': 'Controls use the current ordinal log-linear family with newly matched targets; these are new runs, not reused original rates',
}


def mi(a):
    return float(xlogy(a, a).sum() - xlogy(a.sum(1), a.sum(1)).sum()
                 - xlogy(a.sum(0), a.sum(0)).sum())


def margin(k, dominant):
    if dominant is None:
        return np.full(k, 1/k)
    a = np.full(k, (1-dominant)/(k-1)); a[0] = dominant
    return a


def direction(k, family):
    if family == 'spread':
        scores = np.linspace(-1, 1, k)
        scores -= scores.mean()
        return np.outer(scores, scores)
    h = np.zeros((k, k))
    start = 0 if family == 'common' else k-2
    h[start:start+2, start:start+2] = [[1, -1], [-1, 1]]
    return h


def additive_path(marg, h):
    base = np.outer(marg, marg)
    bound = float(np.min(base[h < 0]/(-h[h < 0])))
    endpoint = PROTOCOL['additive_endpoint_fraction'] * bound
    assert np.max(np.abs(h.sum(0))) < 1e-12
    assert np.max(np.abs(h.sum(1))) < 1e-12
    return base, endpoint


def additive(marg, h, target):
    base, endpoint = additive_path(marg, h)
    fraction = brentq(lambda z: mi(base+z*endpoint*h)-target, 0, 1, xtol=1e-13)
    return base+fraction*endpoint*h, fraction*endpoint


def log_limit(marg, h):
    achieved = 0.
    for strength in PROTOCOL['probes']:
        try:
            current = mi(association_table_from_interaction(marg, marg, strength, h))
        except (ValueError, RuntimeError):
            break
        assert current >= achieved-1e-10
        achieved = current
    return achieved


def direct_binary_check():
    old = pd.read_csv(ROOT/'results/detection_breakdown_sweep/population_definitions.csv')
    rows = []
    for _, record in old[old['shape']=='2x2'].iterrows():
        for side in ['p', 'q']:
            table = np.array(json.loads(record[f'probability_{side}_json']))
            r, c = table.sum(1)[0], table.sum(0)[0]
            independent = r*c
            endpoint = min(r, c) if table[0, 0] >= independent else max(0, r+c-1)
            def make(z):
                x = independent + z*(endpoint-independent)
                return np.maximum([[x, r-x], [c-x, 1-r-c+x]], 0)
            target = mi(table)
            z = brentq(lambda z: mi(make(z))-target, 0, 1, xtol=1e-13)
            rebuilt = make(z)
            error = float(np.max(np.abs(rebuilt-table)))
            assert error < 1e-9, (record.population_id, error)
            rows.append(dict(population_id=record.population_id, side=side,
                             max_cell_error=error, mi_error=abs(mi(rebuilt)-target)))
    return pd.DataFrame(rows)


def build():
    tasks, populations = [], []
    for k in PROTOCOL['sizes']:
        ordinal = interaction_pattern(k, k, 'ordinal')
        for profile in PROTOCOL['profiles']:
            mp = margin(k, None if profile=='uniform' else .7)
            mq = margin(k, None if profile=='uniform' else .8)
            limits = [log_limit(m, ordinal) for m in [mp, mq]]
            for family in (['common'] if k==2 else PROTOCOL['families']):
                h = direction(k, family)
                caps = [mi(base+endpoint*h) for base, endpoint in
                        [additive_path(m, h) for m in [mp, mq]]]
                scale = min(caps+limits)
                assert scale > 1e-10
                for constructor in ['additive', 'loglinear']:
                    for e in PROTOCOL['effects']:
                        ip, iq = .2*scale, (.2+e)*scale
                        tables, strengths = [], []
                        for marg, target in [(mp, ip), (mq, iq)]:
                            if constructor=='additive':
                                a, strength = additive(marg, h, target)
                            else:
                                a, strength = table_with_target_mi_from_interaction(
                                    marg, marg, target, ordinal, mi_tolerance=1e-12)
                            assert (a > 0).all() and abs(a.sum()-1) < 1e-12
                            assert np.max(np.abs(a.sum(0)-marg)) < 1e-11
                            assert np.max(np.abs(a.sum(1)-marg)) < 1e-11
                            assert abs(mi(a)-target) < 1e-10
                            tables.append(a); strengths.append(strength)
                        p, q = tables
                        if profile=='different_skew':
                            assert not np.allclose(np.sort(p.sum(0)), np.sort(q.sum(0)))
                        pid = f'{k}x{k}_{profile}_{family}_{constructor}_e{e:g}'
                        populations.append(dict(population_id=pid, shape=f'{k}x{k}',
                            profile=profile, family=family, constructor=constructor, e=e, M=scale,
                            I_p=mi(p), I_q=mi(q), strength_p=strengths[0], strength_q=strengths[1],
                            row_margin_p_json=json.dumps(mp.tolist()), row_margin_q_json=json.dumps(mq.tolist()),
                            direction_json=json.dumps((h if constructor=='additive' else ordinal).tolist()),
                            probability_p_json=json.dumps(p.tolist()), probability_q_json=json.dumps(q.tolist())))
                        for n_p, n_q in PROTOCOL['sample_pairs']:
                            cid = f'{pid}_np{n_p}_nq{n_q}'
                            # Matching binary populations use the same simulation stream as a numerical control.
                            seed_id = cid.replace(constructor, 'shared') if k==2 else cid
                            row = dict(configuration_id=cid, population_id=pid, shape=f'{k}x{k}',
                                rows=k, columns=k, experiment='construction_check', profile=profile,
                                family=family, constructor=constructor, relationship=profile,
                                n_p=n_p, n_q=n_q, relative_effect=e, shared_reachable_mi=scale,
                                achieved_mi_p=mi(p), achieved_mi_q=mi(q), absolute_mi_difference=iq-ip,
                                target_mi_p=ip, target_mi_q=iq, replicates=PROTOCOL['replicates'],
                                simulation_seed=stable_seed(PROTOCOL['master_seed'], seed_id))
                            tasks.append(dict(configuration=row, probability_p=p, probability_q=q,
                                              alphas=[.05], batch_size=2000))
    manifest = pd.DataFrame([t['configuration'] for t in tasks])
    assert len(manifest)==960 and manifest.configuration_id.is_unique
    return tasks, manifest, pd.DataFrame(populations)


def markdown_table(frame):
    lines = ['| '+' | '.join(frame.columns)+' |', '| '+' | '.join(['---']*len(frame.columns))+' |']
    for row in frame.itertuples(index=False, name=None):
        lines.append('| '+' | '.join(f'{v:.4g}' if isinstance(v, float) else str(v) for v in row)+' |')
    return lines


def comparisons(results):
    frame = results[results.method.isin(METHODS)].copy()
    keys = ['shape', 'profile', 'family', 'constructor', 'n_p', 'n_q', 'relative_effect']
    w = frame[frame.method=='normal_wald'].set_index(keys)
    t = frame[frame.method=='expanded_welch'].set_index(keys)
    out = w[['achieved_mi_p', 'achieved_mi_q', 'absolute_mi_difference']].copy()
    for name, source in [('wald', w), ('welch', t)]:
        out[name+'_rejection'] = source.unconditional_rejection_rate
        out[name+'_valid'] = source.valid_rate
    out['welch_minus_wald'] = out.welch_rejection-out.wald_rejection
    return out.reset_index()


def report(results, audit):
    FIG.mkdir(parents=True, exist_ok=True)
    frame = results[results.method.isin(METHODS)]
    comp = comparisons(results)
    comp.to_csv(OUT/'method_comparison.csv', index=False)
    lines = [
        '# Population Construction Check', '',
        'This separate exploratory check compares additive probability tables with matched ordinal log-linear controls. Each point uses 10,000 pairs at alpha=0.05. Both methods receive the same sampled tables. Every regime is reported separately.', '',
        '## 1. Construction and purpose', '',
        'The additive family is R(t)=r c^T+tH. In common-cell cases H adds to cells (1,1),(2,2) and subtracts from (1,2),(2,1). Rare-cell cases apply that block to the last two rows and columns. Spread cases use H=ss^T with equally spaced scores s from -1 to 1. Every row and column of H sums to zero, preserving the margins. With uniform margins the common/rare labels indicate positions, not differences in rarity.', '',
        'For each population t_max=min(r_i c_j/(-H_ij)) over negative H entries. We search only up to 0.95 t_max, keeping probabilities positive; this is a construction endpoint, not an expected-count filter. The log-linear control uses the current ordinal fitting procedure with the same margins. It is a new matched control, not a replay of the original different-shape experiment.', '',
        'Within each shape/profile/family, M is the minimum reachable MI across P, Q and both constructors. We set I(P)=0.2M and I(Q)=(0.2+e)M. Targets, margins and sample sizes match across constructors; M and absolute differences can differ across families. This tests construction sensitivity, not a pure causal effect of cell location. Changing dependence can still change sparsity.', '',
        'Uniform profile: every row and column has probability 1/k in both populations. Different-skew profile: P has first-row and first-column probability 0.7, Q has 0.8; each remaining marginal probability is 0.3/(k-1) or 0.2/(k-1). Thus the different-skew null has equal positive MI with different margins. At the uniform null P=Q. The common/rare/spread directions coincide for 2x2, so only one is included there. For larger uniform tables common and rare blocks are category-relabelling controls, not distinct kinds of rarity.', '',
        'There are 960 configurations and 9.6 million simulated pairs. The binary constructor controls deliberately use the same random streams, so those cross-constructor comparisons are duplicates for validation. Larger-table cross-constructor comparisons use independent streams. No sampled count tables are retained; saved records contain fixed probabilities, rejection counts, uncertainty and diagnostics.', '',
        'The four-cell additive benchmark is adapted from [Berrett and Samworth (2021), Section 3.2](https://arxiv.org/pdf/2101.10880), also used by [Castro-Prado et al. (2026), Section 4.1](https://onlinelibrary.wiley.com/doi/10.1002/bimj.70129). Targeting equal positive MI and the spread direction here are our adaptations for comparing two populations.', '',
        '## 2. Independent binary reconstruction', '',
        'For every saved original 2x2 population we independently solve for x in [[x,r-x],[c-x,1-r-c+x]], using its margins, MI and association direction. This avoids proportional fitting.', '',
        f'Reconstructed {len(audit)} saved tables; largest cell-probability difference {audit.max_cell_error.max():.3g}; largest MI discrepancy {audit.mi_error.max():.3g}. This validates the binary constructor, not the null-reference distribution of either test.', '',
        '## 3. Calibration and power by exact regime', '',
        'Each figure has additive construction in the top row and matched log-linear construction below. Columns use (nP,nQ)={(10,10),(50,50),(250,250),(1000,1000),(50,500),(500,50)}. Blue circles are Wald; magenta squares are Expanded Welch. Axes are shared: e from 0 to 0.6 and rejection from 0 to 1. At e=0 the target is 0.05; positive e gives power. Shading is a pointwise 95% Wilson interval. Hollow markers flag valid rate below 90%. Invalid results count as non-rejections, and exact valid and conditional rates are shown below each figure.', '',
    ]
    for index, ((shape, profile, family), group) in enumerate(frame.groupby(['shape','profile','family'], sort=False), 1):
        fig, axes = plt.subplots(2, 6, figsize=(19, 6), sharex=True, sharey=True)
        for i, constructor in enumerate(['additive', 'loglinear']):
            for j, (np_, nq_) in enumerate(PROTOCOL['sample_pairs']):
                ax = axes[i,j]
                panel = group[(group.constructor==constructor)&(group.n_p==np_)&(group.n_q==nq_)]
                for method, (label, color, marker) in METHODS.items():
                    values = panel[panel.method==method].sort_values('relative_effect')
                    ax.plot(values.relative_effect, values.unconditional_rejection_rate, label=label,
                            color=color, marker=marker, markersize=3)
                    ax.fill_between(values.relative_effect, values.wilson_95_low, values.wilson_95_high,
                                    color=color, alpha=.15)
                    bad = values[values.valid_rate<.9]
                    ax.scatter(bad.relative_effect, bad.unconditional_rejection_rate,
                               marker=marker, facecolors='white', edgecolors=color, s=20, zorder=4)
                ax.axhline(.05, color='gray', linestyle=':')
                ax.set(xlim=(0,.6), ylim=(0,1), xticks=[0,.1,.3,.6],
                       title=f'{constructor}: nP={np_}, nQ={nq_}', xlabel='Scaled MI difference e')
                if j==0: ax.set_ylabel('Rejection rate')
                ax.grid(alpha=.2)
        fig.suptitle(f'{shape}, {profile}, {family} changes', y=.995)
        fig.legend(*axes[0,0].get_legend_handles_labels(), loc='upper center', bbox_to_anchor=(.5,.965), ncol=2)
        fig.tight_layout(rect=(0,0,1,.9))
        filename = f'{shape}_{profile}_{family}.png'
        fig.savefig(FIG/filename, dpi=140); plt.close(fig)
        first = group.iloc[0]
        cols = ['constructor','n_p','n_q','relative_effect','absolute_mi_difference','method',
                'unconditional_rejection_rate','wilson_95_low','wilson_95_high','valid_rate',
                'conditional_rejection_rate','minimum_true_expected_p','minimum_true_expected_q']
        detail = group.sort_values(['constructor','n_p','n_q','relative_effect','method'])[cols].copy()
        detail.columns = ['Construction','nP','nQ','e','MI difference','Method','Rejection',
                          '95% low','95% high','Valid','Conditional rejection','Min expected P','Min expected Q']
        k = int(shape.split('x')[0])
        marg_text = (f'P and Q: each row and column has probability 1/{k}' if profile=='uniform' else
                     f'P: row 1 and column 1 each have probability 0.7, every other row/column 0.3/{k-1}; '
                     f'Q: row 1 and column 1 each have probability 0.8, every other row/column 0.2/{k-1}')
        block_text = ({'common':'Rows 1,2 and columns 1,2: add t to the block diagonal, subtract t off diagonal',
                       'rare':f'Rows {k-1},{k} and columns {k-1},{k}: add t to the block diagonal, subtract t off diagonal',
                       'spread':f'H=ss^T, s={np.linspace(-1,1,k).round(4).tolist()} (equally spaced scores; displayed rounded)'}[family])
        lines += [f'### 3.{index}. {shape}: {profile}, {family}', '',
            f'![{shape} {profile} {family}](figures/construction_check/{filename})', '',
            '| Specification | Setting |', '| --- | --- |',
            f'| Table shape | {shape} |',
            '| Horizontal graph regime specifications (columns) | (nP,nQ)={(10,10),(50,50),(250,250),(1000,1000),(50,500),(500,50)} |',
            '| Vertical graph regime specifications (rows) | Top: additive probability changes; bottom: ordinal log-linear control. Each panel plots both Wald and Expanded Welch. |',
            f'| Fixed margins for both constructors | {marg_text} |',
            f'| Additive direction in P and Q | {block_text} |',
            '| Log-linear direction in P and Q | Products of equally spaced row/column scores from -1 to 1; ordinal in both populations |',
            f'| MI settings | M={first.shared_reachable_mi:.5g} nats; I(P)={first.achieved_mi_p:.5g} nats; I(Q)=I(P)+eM; e={{0,0.1,0.3,0.6}} |',
            '| Axes | e from 0 to 0.6; rejection rate from 0 to 1 |',
            '| Replicates | 10,000 per point |', '',
            '<details><summary>Every plotted rate, validity and minimum expected count</summary>', '',
            *markdown_table(detail), '', '</details>', '']
    examples = []
    for shape, profile, family, np_, nq_ in [
        ('5x5','uniform','common',50,50),
        ('3x3','different_skew','rare',250,250),
        ('5x5','different_skew','common',500,50),
    ]:
        group = comp[(comp['shape']==shape)&(comp.profile==profile)&(comp.family==family)
                     &(comp.n_p==np_)&(comp.n_q==nq_)]
        for constructor in ['additive','loglinear']:
            rows = group[group.constructor==constructor].set_index('relative_effect')
            null, alternative = rows.loc[0], rows.loc[.6]
            examples.append({'Regime':f'{shape}, {profile}, {family}, nP={np_}, nQ={nq_}',
                'Construction':constructor, 'I(P)':null.achieved_mi_p,
                'Positive MI difference':alternative.absolute_mi_difference,
                'Null Wald':null.wald_rejection, 'Null Welch':null.welch_rejection,
                'Power Wald':alternative.wald_rejection, 'Power Welch':alternative.welch_rejection})
    lines += ['## 4. What the check establishes', '',
        'The independent binary reconstruction and identical binary rejection counts give no evidence that proportional fitting is responsible for the earlier results. The larger-table results show sensitivity to population construction even after matching margins, baseline MI, MI difference and sample sizes. The effect is therefore not described fully by MI and margins alone.', '',
        'Expanded Welch still has both benefits and costs under the additive family: it improves some inflated false-positive rates, but can substantially overcorrect and lose power. This check does not establish that either method is uniformly preferable. The following examples illustrate those different outcomes; the complete landscape and all exact rates appear above.', '',
        *markdown_table(pd.DataFrame(examples)), '',
        'The null columns have target 0.05. Power columns use e=0.6 with the absolute difference shown. In these illustrative endpoints, both methods have at least 99.99% validity; their differences are not explained by large numbers of invalid outputs. The 5x5 unequal-sample example also has decreasing rejection as the MI difference grows. Improved null calibration there does not imply useful detection power.', '',
        'For the thesis, retain multiple constructions and describe advantages by regime. The four effect points are a sensitivity check, not a finely resolved power study. Targets differ between families because rare-cell changes permit smaller MI ranges; comparisons between constructors within each figure are the matched comparisons.', '',
        '## 5. Records', '',
        '[Protocol](../../results/construction_check/protocol.json) | '
        '[Exact populations](../../results/construction_check/population_definitions.csv) | '
        '[All results](../../results/construction_check/cell_results.csv) | '
        '[Method comparisons](../../results/construction_check/method_comparison.csv) | '
        '[Paired results](../../results/construction_check/paired_method_results.csv) | '
        '[Verification](../../results/construction_check/verification.json)', '',
        'Run `python experiments/run_construction_check.py --report-only` to rebuild this document from saved results.', '']
    DOC.write_text('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report-only', action='store_true')
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    if args.report_only:
        report(pd.read_csv(OUT/'cell_results.csv'), pd.read_csv(OUT/'binary_reconstruction.csv'))
        return
    start = perf_counter()
    audit = direct_binary_check()
    tasks, manifest, populations = build()
    print(f'Preflight: {len(tasks)} configurations; {len(audit)} binary reconstructions passed.', flush=True)
    if args.smoke:
        for family in ['common','rare','spread']:
            task = next(t for t in tasks if t['configuration']['shape']=='3x3'
                        and t['configuration']['family']==family
                        and t['configuration']['profile']=='different_skew')
            task = {**task, 'configuration': {**task['configuration'], 'replicates': 500}}
            result = _simulate_configuration(task)
            assert all(r['rejections']<=r['valid_replicates']<=500 for r in result['cell_rows'])
        print('Smoke passed for all three additive constructions.', flush=True)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'protocol.json').write_text(json.dumps(PROTOCOL, indent=2)+'\n')
    manifest.to_csv(OUT/'configuration_manifest.csv', index=False)
    populations.to_csv(OUT/'population_definitions.csv', index=False)
    audit.to_csv(OUT/'binary_reconstruction.csv', index=False)
    inputs = [Path(__file__), Path(__file__).with_name('run_detection_breakdown_sweep.py'),
              ROOT/'src/welch_differential_mi/welch.py',
              ROOT.parent/'DifferentialMI/src/differential_mi/distributions.py',
              ROOT.parent/'DifferentialMI/src/differential_mi/statistics.py']
    metadata = dict(status='running', input_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
    (OUT/'run_metadata.json').write_text(json.dumps(metadata, indent=2))
    cells, pairs = [], []
    sim_start = perf_counter()
    for i, task in enumerate(tasks, 1):
        result = _simulate_configuration(task)
        cells.extend(result['cell_rows']); pairs.extend(result['paired_rows'])
        if i%80==0: print(f'{i}/{len(tasks)} complete', flush=True)
    results = pd.DataFrame(cells)
    assert len(results)==len(tasks)*3
    assert (results.rejections<=results.valid_replicates).all()
    comp = comparisons(results)
    assert (comp.welch_minus_wald<=0).all()
    binary = comp[comp['shape']=='2x2'].pivot(index=['profile','family','n_p','n_q','relative_effect'],
                                           columns='constructor', values=['wald_rejection','welch_rejection'])
    binary_difference = float(np.max(np.abs(binary.xs('additive',axis=1,level=1)-binary.xs('loglinear',axis=1,level=1))))
    assert binary_difference == 0
    results.to_csv(OUT/'cell_results.csv', index=False)
    pd.DataFrame(pairs).to_csv(OUT/'paired_method_results.csv', index=False)
    verification = dict(configurations=len(tasks), simulated_pairs=len(tasks)*PROTOCOL['replicates'],
        result_rows=len(results), binary_max_rate_difference=binary_difference,
        binary_reconstruction_max_cell_error=float(audit.max_cell_error.max()),
        probability_margin_target_checks=True, rejection_denominators_checked=True,
        expanded_rejections_subset_of_wald=True)
    (OUT/'verification.json').write_text(json.dumps(verification, indent=2))
    metadata.update(status='complete', simulation_seconds=perf_counter()-sim_start,
                    total_seconds_before_reporting=perf_counter()-start)
    (OUT/'run_metadata.json').write_text(json.dumps(metadata, indent=2))
    report(results, audit)
    print(f'Completed; report: {DOC}', flush=True)


if __name__ == '__main__':
    main()
