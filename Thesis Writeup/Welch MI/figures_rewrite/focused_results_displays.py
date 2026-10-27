"""Place saved experiment summaries beside the questions answered in Chapter 6.

No simulations, moment estimates or bootstrap draws are recomputed. Supply
--results after extracting the experiment supplement to regenerate these files.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


def approximation_figure(subset, group):
    """Separate population calculations from their sample-based counterparts."""
    from report_ratio_tools import (comparison_curves, plain_log_tick,
        MEAN_LABEL, VAR_POP_LABEL, VAR_SAMPLE_LABEL, DF_POP_LABEL, DF_SAMPLE_LABEL)
    from matplotlib.ticker import FuncFormatter, LogLocator
    rows = ([('mean',False,MEAN_LABEL),('variance',False,VAR_POP_LABEL),
             ('variance',True,VAR_SAMPLE_LABEL)] if group=='moment_predictions'
            else [('df',False,DF_POP_LABEL),('df',True,DF_SAMPLE_LABEL)])
    fig, axes = plt.subplots(len(rows),2,figsize=(7.1,6.8 if len(rows)==3 else 4.9),
                             sharex=True,sharey='row',squeeze=False)
    bounds=[]
    colours=('#376c9b','#bd7627','#30836e','#a74356')
    for col,side in enumerate('pq'):
        population=subset[subset.side.eq(side)]
        for k,colour in zip((2,4,8,16),colours):
            data=population[population.k.eq(k)].sort_values('n')
            for row,(kind,sampled,label) in enumerate(rows):
                point,low,high,sample=comparison_curves(data,kind)
                values=sample if sampled else point
                ax=axes[row,col]
                ax.plot(data.n,values,marker='.',color=colour,label=f'{k} x {k}')
                if not sampled:
                    ax.fill_between(data.n,low,high,color=colour,alpha=.40)
                if kind!='mean':
                    bounds.extend([values] if sampled else [low,high])
        for row,(_,_,label) in enumerate(rows):
            ax=axes[row,col]
            ax.set_xscale('log');ax.set_yscale('log');ax.axhline(1,color='black',lw=.6)
            ax.yaxis.set_major_locator(LogLocator(base=10,subs=(1,2,5)))
            ax.yaxis.set_major_formatter(FuncFormatter(plain_log_tick))
            ax.yaxis.set_minor_formatter(plt.NullFormatter())
            if col==0:ax.set_ylabel('$'+label+'$',fontsize=12.5)
        axes[0,col].set_title('Population '+side.upper())
        axes[-1,col].set_xlabel('Sample size per population')
    # The two versions of a quantity use the same scale across both populations.
    bounds=np.concatenate(bounds);bounds=bounds[np.isfinite(bounds)&(bounds>0)]
    for row,(kind,_,_) in enumerate(rows):
        if kind!='mean':axes[row,0].set_ylim(bounds.min()*.85,bounds.max()*1.18)
    fig.legend(*axes[0,0].get_legend_handles_labels(),loc='lower center',
               bbox_to_anchor=(.5,.01),ncol=4,fontsize=10)
    fig.tight_layout(rect=(0,.085 if len(rows)==3 else .12,1,1))
    return fig


def near_independence_figure(data, detailed=False):
    """Show the key mean-df mechanism, retaining full diagnostics on request."""
    from report_ratio_tools import plain_log_tick
    from matplotlib.ticker import FuncFormatter
    fig,axes=plt.subplots(3,2,figsize=(7.1,7.5 if detailed else 7.2),
                          sharex=True,sharey='row')
    for col,side in enumerate('pq'):
        d=data[data.side.eq(side)].sort_values('mi')
        for row,actual,pred,scale in [(0,'mean','a4_scaled_mean',d.n),
                                      (1,'variance','a4_scaled_variance',d.n**2)]:
            axes[row,col].plot(d.mi,d[actual]*scale,'o-',color='#28679b',label='Observed')
            axes[row,col].plot(d.mi,d[pred],'--',color='#b46c14',label='Near-independence prediction')
            if col==0:axes[row,col].legend(loc='upper left',fontsize=9,frameon=False)
        ax=axes[2,col]
        if detailed:ax.fill_between(d.mi,d.df_p05,d.df_p95,color='#a53648',alpha=.12)
        ax.plot(d.mi,d.df_mean,'o-',color='#a53648',label='Mean estimated df')
        ax.plot(d.mi,d.a4_df_mean,'--',color='#a53648',label='Near-independence prediction of mean df')
        ax.plot(d.mi,d.nu_mom,'o-',color='#34866f',label='Moment target')
        ax.plot(d.mi,d.nu_fo,':',color='black',label='Population first-order df')
        if detailed:
            ax.plot(d.mi,d.df_median,':',color='#a53648',label='Median estimated df')
            ax.plot(d.mi,d.a4_df_mom,'--',color='#34866f',label='Near-independence moment target')
        for row in range(3):
            axes[row,col].set_xscale('log');axes[row,col].set_yscale('log')
            axes[row,col].yaxis.set_major_formatter(FuncFormatter(plain_log_tick))
            axes[row,col].yaxis.set_minor_formatter(plt.NullFormatter())
        axes[0,col].set_title('Population '+side.upper())
        axes[2,col].set_xlabel('Population MI (nats)')
    for row,label in enumerate((r'$n\,\mathbb{E}(\widehat V)$',
                                r'$n^2\mathrm{Var}(\widehat V)$','Component degrees\nof freedom')):
        axes[row,0].set_ylabel(label)
    fig.legend(*axes[2,0].get_legend_handles_labels(),loc='lower center',ncol=2,fontsize=9)
    if detailed:
        profile={'uniform':'Uniform margins','same_skew':'Same-skew margins','different_skew':'Different-skew margins'}[data.profile.iloc[0]]
        fig.suptitle(f'{int(data.k.iloc[0])} x {int(data.k.iloc[0])}; {profile}; n={int(data.n.iloc[0]):,}',fontsize=10)
    fig.tight_layout(rect=(0,.17 if detailed else .13,1,.96 if detailed else 1))
    return fig


def generate(results, destination, diagnostics_destination=None):
    sys.path.insert(0, str(results.resolve().parents[1]/'experiments'))
    from report_ratio_tools import RATIO_ORIENTATION
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
        for method in ('wald', 'expanded'):
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
                [r'\(n\)', 'Mean ratio', 'Predicted / observed variance'], ranges)
    saved['moment_ranges'] = ranges

    plt.rcParams.update({'font.size':10, 'axes.spines.top':False,
        'axes.spines.right':False, 'axes.labelsize':10, 'legend.fontsize':9,
        'pdf.fonttype':42})
    subset = null_moments[null_moments.profile.eq('different_skew')]
    for group in ('moment_predictions','component_df'):
        fig=approximation_figure(subset,group)
        fig.savefig(destination/f'focused_redesign_{group}_different_skew.pdf',bbox_inches='tight')
        plt.close(fig)
    near=moments[moments.configuration_id.isin(association_ids)
        &moments.profile.eq('different_skew')&moments.n.eq(1000)]
    assert len(near)==14 and near.df_valid_count.eq(near['count']).all()
    fig=near_independence_figure(near)
    fig.savefig(destination/'focused_redesign_near_independence_different_skew_1000.pdf',bbox_inches='tight')
    plt.close(fig)
    if diagnostics_destination is not None:
        diagnostics_destination.mkdir(parents=True,exist_ok=True)
        for profile in ('uniform','same_skew','different_skew'):
            for n in (100,1000,10000):
                data=moments[moments.configuration_id.isin(association_ids)
                    &moments.profile.eq(profile)&moments.n.eq(n)]
                assert len(data)==14
                fig=near_independence_figure(data,detailed=True)
                fig.savefig(diagnostics_destination/f'near_independence_{profile}_{n}_full.pdf',bbox_inches='tight')
                plt.close(fig)
    saved['figure_rows']={'moment_predictions':['mean','population variance prediction','average sample variance prediction'],
        'component_df':['population first-order df','mean estimated df']}
    saved['near_independence_curves']=['mean estimated df','near-independence prediction of mean df',
                                      'moment target','population first-order df']

    evidence = json.loads((destination/'focused_redesign_evidence.json').read_text())
    labels = ['A','B','C','16, same, 1,000','16, different, 1,000']
    rows = []
    for label in labels:
        d = diagnostics.loc[evidence['focus_cases'][label]]
        display_label = {'16, same, 1,000':r'\(16\times16\), same skew, \(n=1{,}000\)',
                         '16, different, 1,000':r'\(16\times16\), different skew, \(n=1{,}000\)'}.get(label,label)
        rows.append([display_label,fixed(d.bias_sd,3),fixed(d.variance_ratio,3)])
    write_table(destination/'focused_redesign_shared_estimates.tex',
                ['Setting','Bias / SD',r'\(\E(\SEhat^2)/\Var(\Deltahat)\)'],rows)
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
                         *[percent(key,m) for m in ('wald','expanded')]])
    write_table(destination/'focused_redesign_construction_summary.tex',
                ['Margins','Construction',r'\shortstack{Bias\\(nats)}',
                 r'\shortstack{Normal\\Wald}',r'\shortstack{Expanded\\Welch}'],rows,'llrrr')
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
    for method,label in [('wald','Normal Wald'),('expanded','Expanded Welch')]:
        cells=[]
        for profile in ('different_skew','same_skew'):
            key = case(16,profile,1000,mi_q=.03)
            r = rates.loc[(key,method)]
            cells.append(f'{int(r.wrong_direction):,} / {int(r.rejected):,}')
        rows.append([label,*cells])
    write_table(destination/'focused_redesign_rejection_direction.tex',
                ['Method','Different skew','Same skew'],rows)
    saved['rejection_direction'] = rows
    saved['ratio_orientation'] = RATIO_ORIENTATION
    saved['inputs_sha256'] = {name:hashlib.sha256((results/name).read_bytes()).hexdigest()
        for name in ('configurations.csv','displays.csv','moments.csv','diagnostics.csv','rates.csv','calibration_sensitivity/nominal_upper_rates.csv')}
    (destination/'focused_results_display_evidence.json').write_text(json.dumps(saved,indent=2)+'\n')
    print(json.dumps(saved,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',type=Path,default=DEFAULT_RESULTS)
    parser.add_argument('--figures',type=Path,default=HERE)
    parser.add_argument('--diagnostics',type=Path,help='Also write the nine full near-independence diagnostics here.')
    args=parser.parse_args()
    generate(args.results,args.figures,args.diagnostics)
