"""Place saved experiment summaries beside the questions answered in Chapter 6.

No simulations, moment estimates or bootstrap draws are recomputed. Supply
--results after extracting the experiment supplement to regenerate these files.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
DEFAULT_RESULTS = HERE.parents[2] / 'WelchSatterthwaiteMI/results/approximation_redesign'


def fixed(value, places):
    result = f'{value:.{places}f}'
    return result[1:] if result.startswith('-') and float(result) == 0 else result


def write_table(path, columns, rows, alignment=None):
    alignment = alignment or 'l' + 'r' * (len(columns)-1)
    path.write_text('\n'.join([
        r'\begin{tabular}{@{}' + alignment + r'@{}}', r'\toprule',
        ' & '.join(columns) + r'\\', r'\midrule',
        *[' & '.join(map(str, row)) + r'\\' for row in rows],
        r'\bottomrule', r'\end{tabular}', '']))


def generate(results, destination):
    configs = pd.read_csv(results/'configurations.csv')
    displays = pd.read_csv(results/'displays.csv', keep_default_na=False)
    moments = pd.read_csv(results/'moments.csv')
    diagnostics = pd.read_csv(results/'diagnostics.csv').set_index('configuration_id')
    rates = pd.read_csv(results/'rates.csv')
    rates = rates[rates.denominator.eq('all')].set_index(['configuration_id', 'method'])
    null_ids = set(displays[displays.study.eq('null')].configuration_id)
    association_ids = set(displays[displays.study.eq('association')].configuration_id)
    null_moments = moments[moments.configuration_id.isin(null_ids)]
    assert len(null_ids) == 120
    saved = {}

    def case(k, profile, n_p, n_q=None, mi_q=.02, construction='copying'):
        selected = configs[configs.k.eq(k) & configs.profile.eq(profile)
            & configs.n_p.eq(n_p) & configs.n_q.eq(n_p if n_q is None else n_q)
            & np.isclose(configs.mi_p, .02, rtol=0, atol=1e-12)
            & np.isclose(configs.mi_q, mi_q, rtol=0, atol=1e-12)
            & configs.construction.eq(construction)]
        assert len(selected) == 1, selected
        key = selected.iloc[0].configuration_id
        for method in ('wald', 'expanded', 'reference'):
            r = rates.loc[(key, method)]
            assert r['count'] == 100000 and r.valid_count == 100000
        return key

    def percent(key, method):
        return f'{100*rates.loc[(key, method), "rate"]:.2f}'

    ranges = []
    for n in (1000, 50000):
        d = null_moments[null_moments.n.eq(n)]
        assert len(d) == 24
        ranges.append([f'{n:,}', f'{d.mean_ratio.min():.3f}--{d.mean_ratio.max():.3f}',
                       f'{d.variance_ratio.min():.3f}--{d.variance_ratio.max():.3f}'])
    write_table(destination/'focused_redesign_moment_ranges.tex',
                [r'\(n\)', 'Mean ratio', 'Sampling-variance ratio'], ranges)
    saved['moment_ranges'] = ranges

    plt.rcParams.update({'font.size':10, 'axes.spines.top':False,
        'axes.spines.right':False, 'axes.labelsize':10, 'legend.fontsize':9,
        'pdf.fonttype':42})
    subset = null_moments[null_moments.profile.eq('different_skew')]
    colours = ('#376c9b','#bd7627','#30836e','#a74356')
    for group, fields, figsize in [('moment_predictions', ('mean_ratio','variance_ratio'), (7.1,5.4)),
                                  ('component_df', ('df_ratio',), (7.1,3.0))]:
        fig, axes = plt.subplots(len(fields), 2, figsize=figsize, sharex=True, squeeze=False)
        for col, side in enumerate('pq'):
            population = subset[subset.side.eq(side)]
            for k, colour in zip((2,4,8,16), colours):
                data = population[population.k.eq(k)].sort_values('n')
                for row, field in enumerate(fields):
                    ax = axes[row, col]
                    ax.plot(data.n, data[field], marker='.', color=colour, label=f'{k} x {k}')
                    error = data[field+'_mcse']
                    ax.fill_between(data.n, np.maximum(data[field]-1.96*error,1e-12),
                                    data[field]+1.96*error, color=colour, alpha=.10)
                    if field == 'variance_ratio':
                        ax.plot(data.n, data.plugin_variance_ratio, ls='--', color=colour, lw=1.1)
                    if field == 'df_ratio':
                        ratio = (data.df_mean/data.nu_mom).where(data.df_valid_count.eq(data['count']))
                        ax.plot(data.n, ratio, ls='--', color=colour, lw=1.1)
                    ax.set_xscale('log'); ax.set_yscale('log'); ax.axhline(1,color='black',lw=.6)
            axes[0,col].set_title('Population '+side.upper())
            axes[-1,col].set_xlabel('Sample size per population')
            if group == 'component_df':
                ratio = (population.df_mean/population.nu_mom).where(population.df_valid_count.eq(population['count']))
                bounds = np.concatenate([population.df_ratio-1.96*population.df_ratio_mcse,
                                         population.df_ratio+1.96*population.df_ratio_mcse,ratio])
                bounds = bounds[np.isfinite(bounds)&(bounds>0)]
                axes[0,col].set_ylim(bounds.min()*.85,bounds.max()*1.18)
        for row, field in enumerate(fields):
            axes[row,0].set_ylabel({'mean_ratio':r'Observed mean / $V$',
                'variance_ratio':r'Prediction / observed $\mathrm{Var}(\widehat V)$',
                'df_ratio':'df / moment target'}[field])
        handles, labels = axes[0,0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5,.055), ncol=4)
        style_labels = (['Population prediction (bottom row)','Mean sample prediction (bottom row)']
                        if group == 'moment_predictions' else ['Population first-order df','Mean estimated df'])
        fig.legend([Line2D([0],[0],color='black'),Line2D([0],[0],color='black',ls='--')],
                   style_labels, loc='lower center', ncol=2, fontsize=8)
        fig.tight_layout(rect=(0,.16 if group=='component_df' else .12,1,1))
        fig.savefig(destination/f'focused_redesign_{group}_different_skew.pdf',bbox_inches='tight')
        plt.close(fig)

    evidence = json.loads((destination/'focused_redesign_evidence.json').read_text())
    labels = ['A','B','C','16, same, 1,000','16, different, 1,000']
    rows = []
    for label in labels:
        d = diagnostics.loc[evidence['focus_cases'][label]]
        display_label = {'16, same, 1,000':r'\(16\times16\), same skew, \(n=1{,}000\)',
                         '16, different, 1,000':r'\(16\times16\), different skew, \(n=1{,}000\)'}.get(label,label)
        rows.append([display_label,fixed(d.bias_sd,3),fixed(d.variance_ratio,3)])
    write_table(destination/'focused_redesign_shared_estimates.tex',
                ['Setting','Bias / SD','Variance ratio'],rows)
    saved['shared_estimates'] = rows

    upper = pd.read_csv(results/'calibration_sensitivity/nominal_upper_rates.csv')
    rows = []
    for label, effect in [('A',2.),('B',4.)]:
        selected = upper[upper.focus.eq(label)&upper.effect.eq(effect)].set_index('method')
        assert selected['count'].eq(100000).all()
        values = []
        for method in ('wald','expanded'):
            r = selected.loc[method]
            values.append(f'{100*r.rate:.2f} [{100*r.low:.2f}, {100*r.high:.2f}]')
        rows.append([label,f'{selected.loc["wald","common_mi"]:.4f}',*values])
    write_table(destination/'focused_redesign_stronger_null.tex',
                ['Setting','Common MI (nats)','Normal Wald','Expanded Welch'],rows)
    saved['stronger_null'] = rows

    rows = []
    for profile in ('different_skew','same_skew'):
        for construction in ('copying','four_cell'):
            key = case(16,profile,1000,construction=construction)
            rows.append(['Different skew' if profile=='different_skew' else 'Same skew',
                         'Copying' if construction=='copying' else 'Four-cell transfer',
                         f'{diagnostics.loc[key,"bias"]:.5f}',
                         *[percent(key,m) for m in ('wald','expanded','reference')]])
    write_table(destination/'focused_redesign_construction_summary.tex',
                ['Margins','Construction',r'\shortstack{Bias\\(nats)}',
                 r'\shortstack{Normal\\Wald}',r'\shortstack{Expanded\\Welch}',r'\shortstack{Moment\\reference}'],rows,'llrrrr')
    saved['construction'] = rows

    rows = []
    for n_p,n_q in ((1000,1000),(400,1600),(1600,400)):
        key = case(4,'different_skew',n_p,n_q,mi_q=.03)
        d = diagnostics.loc[key]
        rows.append([f'{n_p:,}',f'{n_q:,}',f'{np.sqrt(d.observed_variance):.5f}',
                     f'{d.df_median:.2f}',percent(key,'wald'),percent(key,'expanded')])
    write_table(destination/'focused_redesign_allocation_summary.tex',
                [r'\(n_P\)',r'\(n_Q\)',r'\shortstack{Observed SD\\(nats)}',
                 r'\shortstack{Median expanded\\degrees of freedom}',
                 r'\shortstack{Normal\\Wald}',r'\shortstack{Expanded\\Welch}'],rows,'rrrrrr')
    saved['allocation'] = rows

    rows = []
    for n in (100,1000,10000):
        d = moments[moments.configuration_id.isin(association_ids)&moments.n.eq(n)]
        assert len(d)==42
        rows.append([f'{n:,}',f'{d.scaled_mean_error.min():.2f}--{d.scaled_mean_error.max():.2f}'])
    write_table(destination/'focused_redesign_scaled_mean_error.tex',
                [r'\(n\)',r'Range of \(n\{\E\Vhat-V\}\)'],rows)
    saved['scaled_mean_error'] = rows

    rows = []
    for method,label in [('wald','Normal Wald'),('expanded','Expanded Welch'),('reference','Moment reference')]:
        cells=[]
        for profile in ('different_skew','same_skew'):
            key = case(16,profile,1000,mi_q=.03)
            r = rates.loc[(key,method)]
            cells.append(f'{int(r.wrong_direction):,} / {int(r.rejected):,}')
        rows.append([label,*cells])
    write_table(destination/'focused_redesign_rejection_direction.tex',
                ['Method','Different skew','Same skew'],rows)
    saved['rejection_direction'] = rows
    saved['inputs_sha256'] = {name:hashlib.sha256((results/name).read_bytes()).hexdigest()
        for name in ('configurations.csv','displays.csv','moments.csv','diagnostics.csv','rates.csv','calibration_sensitivity/nominal_upper_rates.csv')}
    (destination/'focused_results_display_evidence.json').write_text(json.dumps(saved,indent=2)+'\n')
    print(json.dumps(saved,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',type=Path,default=DEFAULT_RESULTS)
    parser.add_argument('--figures',type=Path,default=HERE)
    args=parser.parse_args()
    generate(args.results,args.figures)
