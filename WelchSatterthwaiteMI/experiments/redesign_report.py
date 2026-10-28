"""Tables, plots and paired calibration uncertainty for the copied thesis."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from decimal import Decimal
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from report_ratio_tools import (comparison_curves, mean_df_over_moment_target,
    plain_log_tick, MEAN_LABEL, RATIO_ORIENTATION, VAR_AXIS_LABEL, DF_AXIS_LABEL)

import redesign_study as study
from report_formatting import decimal_text

LABELS={'wald':'Normal Wald','size':'Sample-size df','expanded':'Expanded Welch','reference':'Moment reference'}
COLOURS={'wald':'#28679b','size':'#b46c14','expanded':'#a53648','reference':'#34866f'}
STYLES={'wald':'-','size':'--','expanded':'-','reference':':'}
FIGURES=study.ROOT.parent/'Thesis Writeup/Welch MI/figures_rewrite'
# The full four-rule evidence is retained in the experimental supplement.
# Thesis displays compare the two tests only.
DISPLAY_METHODS=('wald','expanded')


def percentage_text(value):
    return decimal_text(Decimal(str(value))*100,places=2)+r'\%'


def significant_text(value,figures=3):
    x=Decimal(str(value))
    if x.is_zero(): return '0'
    return decimal_text(x,places=max(0,figures-1-x.adjusted()))


def calibration_grid(rates,null_ids,tolerance=.003):
    selected=rates[rates.denominator.eq('all')&rates.configuration_id.isin(null_ids)]
    rates_wide=selected.pivot(index='configuration_id',columns='method',values='rate')
    counts=selected.pivot(index='configuration_id',columns='method',values='count')
    rejected=selected.pivot(index='configuration_id',columns='method',values='rejected')
    if not (counts.wald.eq(counts.expanded).all() and counts.wald.nunique()==1):
        raise AssertionError('Grid comparison requires matched denominators')
    # Integer rejection counts retain exact equality at the tolerance boundary.
    target=study.ALPHA*counts.wald
    improvement=(rejected.wald-target).abs()-(rejected.expanded-target).abs()
    boundary=tolerance*counts.wald
    category=np.where(improvement>boundary,'toward',np.where(improvement < -boundary,'away','within'))
    grid=rates_wide[['wald','expanded']].copy()
    grid['improvement']=improvement/counts.wald
    grid['classification']=category
    summary=dict(settings=len(grid),tolerance_percentage_points=100*tolerance,
                 toward=int((category=='toward').sum()),away=int((category=='away').sum()),
                 within=int((category=='within').sum()),
                 toward_wald_above=int(((category=='toward')&grid.wald.gt(study.ALPHA)).sum()),
                 away_wald_below=int(((category=='away')&grid.wald.lt(study.ALPHA)).sum()))
    return grid.reset_index(),summary


def bootstrap_focus(task):
    output,label,focus,configurations,references,repetitions=task
    by_id={c['configuration_id']:c for c in configurations}
    selected=focus[focus.focus.eq(label)].sort_values('standardised_difference')
    null_key=selected.iloc[0].configuration_id
    ref=references[null_key]
    fit=study.load_records(output,'fit',null_key)
    fit_methods,_=study.method_values(fit,by_id[null_key],ref['nu_ref'])
    prepared=[]
    for row in selected.itertuples():
        r=study.load_records(output,'evaluation',row.configuration_id)
        methods,_=study.method_values(r,by_id[row.configuration_id],ref['nu_ref'])
        prepared.append((row.configuration_id,r,methods))
    rng=np.random.default_rng(study.seed_for('calibration-bootstrap',label,0,'paired'))
    draws=np.zeros((repetitions,len(prepared),4))
    n=len(fit['statistic']); k=int(study.ALPHA*n)
    fit_p={m:np.where(v,p,1.) for m,(p,v) in fit_methods.items()}
    absolute=np.where(fit['base_valid'],abs(fit['statistic']),-np.inf)
    codes=np.arange(16)
    membership=((codes[:,None] & (1<<np.arange(4)))>0).astype(float)
    for b in range(repetitions):
        indices=rng.integers(0,n,n)
        critical=np.partition(absolute[indices],n-k-1)[n-k-1]
        cuts={m:np.partition(fit_p[m][indices],k)[k] for m in ('size','expanded')}
        for j,(_,r,methods) in enumerate(prepared):
            code=np.zeros(len(r['statistic']),np.uint8)
            for bit,m in enumerate(study.METHODS):
                p,valid=methods[m]
                yes=valid & ((abs(r['statistic'])>critical) if m in ('wald','reference') else (p<cuts[m]))
                code |= yes.astype(np.uint8)<<bit
            counts=np.bincount(code,minlength=16)
            # Multinomial resampling of joint decisions preserves all paired contrasts.
            resampled=rng.multinomial(len(code),counts/len(code))
            draws[b,j]=resampled@membership/len(code)
    rows=[]
    for j,(key,_,_) in enumerate(prepared):
        for bit,m in enumerate(study.METHODS):
            low,high=np.quantile(draws[:,j,bit],[.025,.975])
            rows.append(dict(configuration_id=key,focus=label,method=m,low=low,high=high,
                             mcse=float(np.std(draws[:,j,bit],ddof=1)),bootstrap_repetitions=repetitions))
        for bit,m in enumerate(study.METHODS):
            if m=='expanded': continue
            difference=draws[:,j,2]-draws[:,j,bit]
            low,high=np.quantile(difference,[.025,.975])
            rows.append(dict(configuration_id=key,focus=label,method='expanded_minus_'+m,
                             low=low,high=high,mcse=float(np.std(difference,ddof=1)),
                             bootstrap_repetitions=repetitions))
    return rows


def save(fig,name,figures,bbox_inches='tight'):
    fig.savefig(figures/('focused_redesign_'+name+'.pdf'),bbox_inches=bbox_inches)
    plt.close(fig)


def table(path,columns,rows,flexible_first=False,group_header=None):
    alignment=(r'>{\raggedright\arraybackslash}X' if flexible_first else 'l')+'r'*(len(columns)-1)
    opening=(r'\begin{tabularx}{\textwidth}' if flexible_first else r'\begin{tabular}')
    lines=[opening+r'{@{}'+alignment+r'@{}}',r'\toprule']
    if group_header is not None:
        lines.extend(group_header)
    lines.extend([' & '.join(columns)+r'\\',r'\midrule'])
    lines += [' & '.join(map(str,row))+r'\\' for row in rows]
    lines += [r'\bottomrule',r'\end{tabularx}' if flexible_first else r'\end{tabular}']
    text='\n'.join(lines)+'\n'
    text=re.sub(r'(?<![\d.])-0(\.0+)(?![\d.])',r'0\1',text)
    path.write_text(text)


def case_display_label(label,side=None):
    """Expand display wording while retaining the existing evidence keys."""
    match=re.fullmatch(r'16, (same|different), ([\d,]+)',label)
    if match:
        profile,n=match.groups()
        number=n.replace(',',r'{,}')
        label=rf'\(16\times16\), {profile} skew\newline \(n={number}\)'
    if side is not None:
        label+=rf', \({side.upper()}\)'
    return label


def component_spread_table(figures,cases,moments):
    rows=[]
    for label,key in cases:
        for side in 'pq':
            measured=moments[moments.configuration_id.eq(key)&moments.side.eq(side)].iloc[0]
            rows.append([case_display_label(label,side),f'{measured.df_mean:.2f}',f'{measured.df_median:.2f}',
                         f'[{measured.df_p05:.2f}, {measured.df_p95:.2f}]',f'{measured.nu_mom:.2f}',f'{int(measured.df_valid_count):,}'])
    table(figures/'focused_redesign_component_spread.tex',
          ['Setting, population',r'\shortstack{Mean\\df}',r'\shortstack{Median\\df}',
           r'\shortstack{5th--95th\\percentiles}',r'\shortstack{Moment\\target}','Included'],
          rows,flexible_first=True)


def component_comparison_table(figures,selected):
    rows=[[f'{r["mi"]:g}, {r["side"].upper()}',f'{r["mean_ratio"]:.3f}',f'{r["variance_ratio"]:.3f}',
           f'{r["plugin_variance_ratio"]:.3f}',f'{r["df_mean"]:.2f}',f'{r["nu_mom"]:.2f}',f'{r["nu_fo"]:.2f}'] for r in selected]
    table(figures/'focused_redesign_components.tex',
          ['MI, pop.','Mean ratio',r'\shortstack{Var. ratio\\(pop.)}',
           r'\shortstack{Var. ratio\\(sample)}','Mean df','Moment df',r'\(\nu_{\mathrm{FO}}\)'],rows,
          group_header=[r'& \multicolumn{3}{c}{Moment ratios} & \multicolumn{3}{c}{Component df}\\',
                        r'\cmidrule(lr){2-4}\cmidrule(l){5-7}'])


def select_case(configs,k,profile,n,mi=.02,construction='copying',iq=None,nq=None):
    iq=mi if iq is None else iq; nq=n if nq is None else nq
    subset=configs[configs.k.eq(k)&configs.profile.eq(profile)&configs.n_p.eq(n)&configs.n_q.eq(nq)
                   &np.isclose(configs.mi_p,mi,atol=1e-12,rtol=0)&np.isclose(configs.mi_q,iq,atol=1e-12,rtol=0)
                   &configs.construction.eq(construction)]
    if len(subset)!=1: raise AssertionError('Case selection not unique')
    return subset.iloc[0].configuration_id


def testing_rule_figures(configs,displays,focus,raw,cal,boot,figures,methods=DISPLAY_METHODS):
    """Plot saved rejection rates; do not refit or resample any experiment."""
    null_ids=set(displays[displays.study.eq('null')].configuration_id)
    for profile in study.PROFILES:
        fig=plt.figure(figsize=(7.1,6.2))
        grid=fig.add_gridspec(2,2,hspace=.50,wspace=.28,left=.11,right=.98,top=.94,bottom=.16)
        first=None; panels=[]
        for position,k in enumerate((2,4,8,16)):
            pair=grid[position//2,position%2].subgridspec(2,1,height_ratios=[4,1],hspace=.10)
            ax=fig.add_subplot(pair[0]); validity_ax=fig.add_subplot(pair[1],sharex=ax)
            panels.append((ax,validity_ax))
            if first is None: first=ax
            data=configs[configs.configuration_id.isin(null_ids)&configs.profile.eq(profile)&configs.k.eq(k)].sort_values('n_p')
            for m in methods:
                y=[raw.loc[(key,m),'rate'] for key in data.configuration_id]
                lo=[raw.loc[(key,m),'low'] for key in data.configuration_id]
                hi=[raw.loc[(key,m),'high'] for key in data.configuration_id]
                ax.plot(data.n_p,y,color=COLOURS[m],ls=STYLES[m],label=LABELS[m],lw=1.3)
                ax.fill_between(data.n_p,lo,hi,color=COLOURS[m],alpha=.10)
            for m in ('wald','expanded'):
                validity=[raw.loc[(key,m),'valid_count']/100000 for key in data.configuration_id]
                validity_ax.plot(data.n_p,validity,color=COLOURS[m],lw=1.2)
            validity_ax.set_ylim(-.05,1.07);validity_ax.set_yticks([0,1]);validity_ax.tick_params(labelsize=8)
            validity_ax.set_ylabel('Valid',fontsize=9);validity_ax.set_xlabel('Sample size per population',fontsize=9)
            ax.tick_params(labelbottom=False)
            ax.axhline(.05,color='black',lw=.6); ax.set_xscale('log'); ax.set_title(f'{k} x {k}')
            ax.set_ylabel('False-positive rate')
        # Retain the canvas size, panel geometry and preceding margins. The full
        # validity label fits horizontally in the unused lower part of its strip.
        previous_legend=fig.legend(*first.get_legend_handles_labels(),loc='lower center',ncol=2)
        fig.canvas.draw()
        bounds=fig.get_tightbbox(fig.canvas.get_renderer()).padded(plt.rcParams['savefig.pad_inches'])
        previous_legend.remove()
        for ax,validity_ax in panels:
            ax.yaxis.set_major_formatter(FuncFormatter(lambda value,position:f'{100*value:g}%'))
            validity_ax.set_ylabel('Valid fraction',fontsize=9,rotation=0,ha='left',va='bottom')
            validity_ax.yaxis.set_label_coords(.02,.13)
        handles,labels=first.get_legend_handles_labels()
        fig.legend(handles+[Line2D([],[],color='black',lw=.6)],labels+['Nominal 5%'],
                   loc='lower center',ncol=3)
        save(fig,'null_'+profile,figures,bbox_inches=bounds)

    for calibrated in (False,True):
        fig,axes=plt.subplots(1,3,figsize=(7.1,3.1),sharey=True)
        source=cal if calibrated else raw
        for ax,label in zip(axes,study.FOCUS):
            selected=focus[focus.focus.eq(label)].sort_values('standardised_difference')
            for m in methods:
                if calibrated and m=='reference': continue
                y=[source.loc[(key,m),'rate'] for key in selected.configuration_id]
                ax.plot(selected.standardised_difference,y,color=COLOURS[m],ls=STYLES[m],label=LABELS[m])
                if calibrated:
                    low=[boot.loc[(key,m),'low'] for key in selected.configuration_id]
                    high=[boot.loc[(key,m),'high'] for key in selected.configuration_id]
                    ax.fill_between(selected.standardised_difference,low,high,color=COLOURS[m],alpha=.12)
            ax.axhline(.05,color='black',lw=.5); ax.set_title(label); ax.set_ylim(0,1)
            ax.set_xlabel(r'$-\Delta/\sigma_0$')
        axes[0].set_ylabel('Calibrated rejection rate' if calibrated else 'Nominal rejection rate')
        fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=len(methods) if not calibrated else 2)
        fig.tight_layout(rect=(0,.14,1,1)); save(fig,'power_calibrated' if calibrated else 'power',figures)



def report(output=study.OUTPUT,figures=FIGURES,bootstrap=1000,workers=3):
    output=Path(output); figures=Path(figures); figures.mkdir(parents=True,exist_ok=True)
    configs=pd.read_csv(output/'configurations.csv')
    # "null" is a study name, not a missing-value marker.
    displays=pd.read_csv(output/'displays.csv',keep_default_na=False)
    focus=pd.read_csv(output/'focus.csv')
    moments=pd.read_csv(output/'moments.csv')
    rates=pd.read_csv(output/'rates.csv')
    null_ids=set(displays[displays.study.eq('null')].configuration_id)
    grid,grid_summary=calibration_grid(rates,null_ids)
    if grid_summary['settings']!=120:
        raise AssertionError('Broad null grid changed')
    if grid_summary['toward_wald_above']!=grid_summary['toward']:
        raise AssertionError('Review manuscript statement about improvements above 5%')
    grid.to_csv(output/'calibration_grid_summary.csv',index=False)
    study.atomic_json(output/'calibration_grid_summary.json',grid_summary)
    upper_nominal_path=output/'calibration_sensitivity/nominal_upper_rates.csv'
    upper_nominal=pd.read_csv(upper_nominal_path).set_index(['focus','effect','method'])
    commands={'RedesignToward':str(grid_summary['toward']),
              'RedesignAway':str(grid_summary['away']),
              'RedesignAwayBelow':str(grid_summary['away_wald_below']),
              'RedesignWithin':str(grid_summary['within']),
              'RedesignGridTolerance':decimal_text(grid_summary['tolerance_percentage_points'],1)}
    for focus_label,effect in [('A',2.),('B',4.)]:
        commands['RedesignUpper'+focus_label+'MI']=decimal_text(upper_nominal.loc[(focus_label,effect,'wald'),'common_mi'],2)
        for method in ('wald','expanded'):
            commands['RedesignUpper'+focus_label+method.title()+'Rate']=percentage_text(upper_nominal.loc[(focus_label,effect,method),'rate'])
    (figures/'focused_redesign_reporting_values.tex').write_text(''.join(
        '\\newcommand{\\'+key+'}{'+value+'}\n' for key,value in commands.items()))
    raw=rates[rates.denominator.eq('all')].set_index(['configuration_id','method'])
    diagnostics=pd.read_csv(output/'diagnostics.csv').set_index('configuration_id')
    dependence_path=output/'calibration_sensitivity/dependence_diagnostics.csv'
    dependence=pd.read_csv(dependence_path).set_index('configuration_id')
    cal=pd.read_csv(output/'calibrated_rates.csv').set_index(['configuration_id','method'])
    refs=json.loads((output/'references.json').read_text())
    if 'plugin_variance_ratio_mcse' not in moments:
        uncertainty={}
        for key in configs.configuration_id:
            records=study.load_records(output,'evaluation',key)
            for side in 'pq':
                x=records['influence_variance_'+side]
                tx=records['variance_influence_variance_'+side]
                n=int(configs.loc[configs.configuration_id.eq(key),'n_'+side].iloc[0])
                mask=np.isfinite(x)&np.isfinite(tx)
                x=x[mask]; y=tx[mask]/n
                mean=x.mean(); variance=np.var(x,ddof=1); prediction=y.mean()
                influence=(y-prediction)/variance-prediction/variance**2*((x-mean)**2-variance)
                uncertainty[key,side]=study.mcse(influence)
        moments['plugin_variance_ratio_mcse']=[uncertainty[r.configuration_id,r.side] for r in moments.itertuples()]
        moments.to_csv(output/'moments.csv',index=False)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.labelsize':10,'legend.fontsize':9,'pdf.fonttype':42})
    if bootstrap:
        rows=[]
        with ProcessPoolExecutor(max_workers=workers) as pool:
            tasks=[(str(output),label,focus,configs.to_dict('records'),refs,bootstrap) for label in study.FOCUS]
            for f in as_completed([pool.submit(bootstrap_focus,t) for t in tasks]):
                rows.extend(f.result()); print('Completed focused calibration bootstrap',flush=True)
        pd.DataFrame(rows).to_csv(output/'calibration_bootstrap.csv',index=False)
    boot=pd.read_csv(output/'calibration_bootstrap.csv').set_index(['configuration_id','method'])

    for profile in study.PROFILES:
        ids=set(displays[displays.study.eq('null')].configuration_id)
        fig,axes=plt.subplots(3,2,figsize=(7.1,7.7),sharex=True,sharey='row')
        for col,side in enumerate('pq'):
            subset=moments[moments.configuration_id.isin(ids)&moments.profile.eq(profile)&moments.side.eq(side)]
            for k,colour in zip((2,4,8,16),('#376c9b','#bd7627','#30836e','#a74356')):
                data=subset[subset.k.eq(k)].sort_values('n')
                for row,kind in enumerate(('mean','variance','df')):
                    ax=axes[row,col]
                    point,low,high,sample=comparison_curves(data,kind)
                    ax.plot(data.n,point,marker='.',color=colour,label=f'{k} x {k}')
                    ax.fill_between(data.n,low,high,color=colour,alpha=.40)
                    if sample is not None:
                        ax.plot(data.n,sample,ls='--',color=colour,lw=1.1)
                    ax.set_xscale('log'); ax.set_yscale('log'); ax.axhline(1,color='black',lw=.6)
                    ax.yaxis.set_major_formatter(FuncFormatter(plain_log_tick))
                    ax.yaxis.set_minor_formatter(plt.NullFormatter())
            axes[0,col].set_title(side.upper())
            axes[2,col].set_xlabel('Sample size per population')
        profile_data=moments[moments.configuration_id.isin(ids)&moments.profile.eq(profile)]
        point,low,high,sample=comparison_curves(profile_data,'df')
        bounds=np.concatenate([low,high,sample])
        bounds=bounds[np.isfinite(bounds)&(bounds>0)]
        axes[2,0].set_ylim(bounds.min()*.85,bounds.max()*1.18)
        for row,label in enumerate(('$'+MEAN_LABEL+'$',VAR_AXIS_LABEL,DF_AXIS_LABEL)):
            axes[row,0].set_ylabel(label)
        handles,labels=axes[0,0].get_legend_handles_labels()
        fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.035),ncol=4)
        fig.legend([Line2D([0],[0],color='black'),Line2D([0],[0],color='black',ls='--')],
                   ['Using population prediction (middle/bottom)','Using mean sample prediction/df (middle/bottom)'],loc='lower center',ncol=2,fontsize=8)
        fig.tight_layout(rect=(0,.09,1,1)); save(fig,'moments_'+profile,figures)

    association_ids=set(displays[displays.study.eq('association')].configuration_id)
    for profile in study.PROFILES:
        for n in (100,1000,10000):
            fig,axes=plt.subplots(3,2,figsize=(7.1,7.5),sharex=True)
            for col,side in enumerate('pq'):
                data=moments[moments.configuration_id.isin(association_ids)&moments.profile.eq(profile)&moments.n.eq(n)&moments.side.eq(side)].sort_values('mi')
                for row,actual,pred,scale in [(0,'mean','a4_scaled_mean',n),(1,'variance','a4_scaled_variance',n*n)]:
                    axes[row,col].plot(data.mi,data[actual]*scale,'o-',color='#28679b',label='Observed')
                    axes[row,col].plot(data.mi,data[pred],'--',color='#b46c14',label='Local approximation')
                    if col == 0:
                        axes[row,col].legend(loc='upper left',fontsize=9,frameon=False)
                ax=axes[2,col]
                ax.fill_between(data.mi,data.df_p05,data.df_p95,color='#a53648',alpha=.12)
                ax.plot(data.mi,data.df_mean,'o-',color='#a53648',label='Mean estimated df')
                ax.plot(data.mi,data.df_median,':',color='#a53648',label='Median estimated df')
                ax.plot(data.mi,data.a4_df_mean,'--',color='#a53648',label='A.4 mean df')
                ax.plot(data.mi,data.nu_mom,'o-',color='#34866f',label='Moment df')
                ax.plot(data.mi,data.a4_df_mom,'--',color='#34866f',label='A.4 moment df')
                ax.plot(data.mi,data.nu_fo,':',color='black',label='First-order df')
                for row in range(3):
                    axes[row,col].set_xscale('log'); axes[row,col].set_yscale('log')
                    axes[row,col].yaxis.set_major_formatter(FuncFormatter(plain_log_tick))
                    axes[row,col].yaxis.set_minor_formatter(plt.NullFormatter())
                axes[0,col].set_title(side.upper()); axes[2,col].set_xlabel('Population MI (nats)')
            for row,label in enumerate((r'$n\,\mathbb{E}(\widehat V)$',r'$n^2\mathrm{Var}(\widehat V)$','Component degrees of freedom')):
                axes[row,0].set_ylabel(label)
            handles,labels=axes[2,0].get_legend_handles_labels()
            fig.legend(handles,labels,loc='lower center',ncol=3,fontsize=8)
            fig.tight_layout(rect=(0,.09,1,1)); save(fig,f'a4_{profile}_{n}',figures)

    fig,axes=plt.subplots(1,3,figsize=(7.1,3.2),sharey=True)
    for ax,profile in zip(axes,study.PROFILES):
        for n,colour in zip((100,1000,10000),('#28679b','#b46c14','#34866f')):
            for side,style in [('p','-'),('q','--')]:
                data=moments[moments.configuration_id.isin(association_ids)&moments.profile.eq(profile)&moments.n.eq(n)&moments.side.eq(side)].sort_values('mi')
                ax.plot(data.mi,data.scaled_mean_error,style,color=colour,label=f'n={n}, {side.upper()}')
                error=1.96*data.scaled_mean_error_mcse
                ax.fill_between(data.mi,data.scaled_mean_error-error,data.scaled_mean_error+error,color=colour,alpha=.08)
        ax.axhline(9,color='black',lw=.7); ax.set_xscale('log'); ax.set_title(profile.replace('_',' ')); ax.set_xlabel('MI (nats)')
    axes[0].set_ylabel('n times mean error in V estimate')
    fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=3,fontsize=8)
    fig.tight_layout(rect=(0,.16,1,1)); save(fig,'mean_bias',figures)

    testing_rule_figures(configs,displays,focus,raw,cal,boot,figures)

    for profile in ('same_skew','different_skew'):
        fig,axes=plt.subplots(2,2,figsize=(7.1,5.3),sharex=True)
        ids=set(displays[displays.study.eq('detection')].configuration_id)
        for ax,k in zip(axes.flat,(2,4,8,16)):
            for n,style in [(1000,'-'),(10000,'--')]:
                data=configs[configs.configuration_id.isin(ids)&configs.profile.eq(profile)&configs.k.eq(k)&configs.n_p.eq(n)].sort_values('mi_q')
                for m in ('wald','expanded'):
                    ax.plot(data.mi_q-data.mi_p,[raw.loc[(key,m),'rate'] for key in data.configuration_id],color=COLOURS[m],ls=style,label=f'{LABELS[m]}, n={n}')
            ax.set_title(f'{k} x {k}'); ax.set_xlabel(r'$-\Delta$ (nats)'); ax.set_ylabel('Rejection rate'); ax.set_ylim(0,1)
        fig.legend(*axes[0,0].get_legend_handles_labels(),loc='lower center',ncol=2,fontsize=8)
        fig.tight_layout(rect=(0,.1,1,1)); save(fig,'broad_power_'+profile,figures)

    cases=[(label,select_case(configs,*spec)) for label,spec in study.FOCUS.items()]
    cases += [(f'16, {"same" if profile=="same_skew" else "different"}, {n:,}',select_case(configs,16,profile,n))
              for profile in ('same_skew','different_skew') for n in (1000,10000)]
    rows=[]
    for label,key in cases:
        cells=[percentage_text(raw.loc[(key,m),'rate'])+' ['+
               decimal_text(Decimal(str(raw.loc[(key,m),'low']))*100,2)+', '+
               decimal_text(Decimal(str(raw.loc[(key,m),'high']))*100,2)+']' for m in DISPLAY_METHODS]
        rows.append([case_display_label(label)]+cells)
    table(figures/'focused_redesign_cases_rates.tex',
          ['Setting']+[LABELS[m] for m in DISPLAY_METHODS],rows,flexible_first=True)
    rows=[]
    for label,key in cases:
        d=diagnostics.loc[key]
        rows.append([case_display_label(label),f'{d.bias_sd:.3f}',f'{d.variance_ratio:.3f}',f'{dependence.loc[key,"centered_magnitude_spearman"]:.3f}',
                     f'{d.delta_skewness:.3f}',f'{d.df_median:.2f}'])
    table(figures/'focused_redesign_cases_diagnostics.tex',
          ['Setting','Bias/SD',r'\shortstack{Est./obs.\\variance}',r'\shortstack{Rank\\corr.}',
           'Skewness',r'\shortstack{Median\\combined df}'],rows,flexible_first=True)
    rows=[]
    for row in focus[focus.standardised_difference.isin([0,1,2,3,4])].sort_values(['focus','standardised_difference']).itertuples():
        rows.append([f'{row.focus}: {row.standardised_difference:g}',significant_text(row.difference_nats)]+
                    [percentage_text(cal.loc[(row.configuration_id,m),'rate']) for m in ('wald','expanded')])
    table(figures/'focused_redesign_calibrated_power.tex',['Setting: SD','Nats','Normal Wald','Expanded Welch'],rows)
    paired=pd.read_csv(output/'paired.csv')
    paired=paired[paired.denominator.eq('all')].set_index(['configuration_id','comparator'])
    rows=[]
    for row in focus[focus.standardised_difference.eq(2)].sort_values('focus').itertuples():
        for other in ('wald',):
            nominal=paired.loc[(row.configuration_id,other)]
            calibrated=cal.loc[(row.configuration_id,'expanded'),'rate']-cal.loc[(row.configuration_id,other),'rate']
            ci=boot.loc[(row.configuration_id,'expanded_minus_'+other)]
            label=row.focus
            rows.append([label,f'{100*nominal.difference:+.3f}',f'[{100*nominal.low:+.3f}, {100*nominal.high:+.3f}]',
                         f'{100*calibrated:+.3f}',f'[{100*ci.low:+.3f}, {100*ci.high:+.3f}]'])
    table(figures/'focused_redesign_power_contrasts.tex',['Setting','Nominal','95\\% interval','Calibrated','95\\% interval'],rows)
    rows=[]
    for label,key in cases[:3]:
        r=refs[key]
        rows.append([label,f'{r["null_sd"]:.6f}',f'{r["null_sd_mcse"]:.6f}'])
    table(figures/'focused_redesign_null_sd_fitting.tex',['Setting','Null SD (nats)',r'\shortstack{Monte Carlo SE\\(nats)}'],rows)
    component_spread_table(figures,cases,moments)
    for study_name in ('allocation','construction'):
        ids=set(displays[displays.study.eq(study_name)].configuration_id)
        selected=configs[configs.configuration_id.isin(ids)].sort_values(['k','profile','construction','mi_q','n_p'])
        if study_name=='construction': selected=selected[selected.mi_p.eq(selected.mi_q)]
        rows=[]
        for c in selected.itertuples():
            profile='Same' if c.profile=='same_skew' else 'Different'
            label=(f'{profile}, {c.n_p}/{c.n_q}, {abs(c.delta):.2f}' if study_name=='allocation' else
                   f'{c.k}, {profile}, {"copy" if c.construction=="copying" else "four"}, {c.n_p}')
            rows.append([label]+[f'{raw.loc[(c.configuration_id,m),"rate"]:.4f}' for m in DISPLAY_METHODS])
        table(figures/f'focused_redesign_{study_name}.tex',['Setting']+[LABELS[m] for m in DISPLAY_METHODS],rows)
    # A compact selection makes component-level numerical comparisons inspectable.
    selected=[]
    for mi in (.0001,.02,.05):
        key=select_case(configs,4,'different_skew',1000,mi=mi)
        selected.extend(moments[moments.configuration_id.eq(key)].to_dict('records'))
    component_comparison_table(figures,selected)
    evidence={'settings':len(configs),'fitting_settings':len(refs),'evaluation_pairs':len(configs)*100000,
              'fitting_pairs':len(refs)*100000,'focus_cases':dict(cases),
              'focus_null_sd':{label:refs[key]['null_sd'] for label,key in json.loads((output/'focus_nulls.json').read_text()).items()},
              'bootstrap_repetitions':int(boot.bootstrap_repetitions.iloc[0]),
              'display_methods':list(DISPLAY_METHODS)}
    study.atomic_json(figures/'focused_redesign_evidence.json',evidence)
    study.atomic_json(output/'report_summary.json',evidence)
    study.atomic_json(output/'report_provenance.json',{
        'source_sha256':study.sha(Path(__file__)),
        'ratio_tools_sha256':study.sha(Path(__file__).with_name('report_ratio_tools.py')),
        'display_ratio_orientation':RATIO_ORIENTATION,
        'interval_orientation':'same saved ratio and scale as the plotted values',
        'inputs':{name:study.sha(output/name) for name in ['protocol.json','configurations.csv','references.json','rates.csv','moments.csv','calibration_bootstrap.csv','audit.json']},
        'dependence_input_sha256':study.sha(dependence_path),
        'upper_nominal_input_sha256':study.sha(upper_nominal_path),
        'grid_summary':grid_summary,
        'null_display_settings':len(null_ids),'bootstrap_repetitions':int(boot.bootstrap_repetitions.iloc[0]),
              'display_methods':list(DISPLAY_METHODS)})
    print(json.dumps(evidence,indent=2),flush=True)


def render_testing_rule_displays(output=study.OUTPUT,figures=FIGURES):
    """Refresh only two-test views from existing CSV/JSON summaries."""
    output=Path(output);figures=Path(figures);figures.mkdir(parents=True,exist_ok=True)
    configs=pd.read_csv(output/'configurations.csv')
    displays=pd.read_csv(output/'displays.csv',keep_default_na=False)
    focus=pd.read_csv(output/'focus.csv')
    rates=pd.read_csv(output/'rates.csv')
    raw=rates[rates.denominator.eq('all')].set_index(['configuration_id','method'])
    cal=pd.read_csv(output/'calibrated_rates.csv').set_index(['configuration_id','method'])
    boot=pd.read_csv(output/'calibration_bootstrap.csv').set_index(['configuration_id','method'])
    diagnostics=pd.read_csv(output/'diagnostics.csv').set_index('configuration_id')
    dependence=pd.read_csv(output/'calibration_sensitivity/dependence_diagnostics.csv').set_index('configuration_id')
    refs=json.loads((output/'references.json').read_text())
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.labelsize':10,'legend.fontsize':9,'pdf.fonttype':42})
    testing_rule_figures(configs,displays,focus,raw,cal,boot,figures)
    cases=[(label,select_case(configs,*spec)) for label,spec in study.FOCUS.items()]
    cases += [(f'16, {"same" if profile=="same_skew" else "different"}, {n:,}',select_case(configs,16,profile,n))
              for profile in ('same_skew','different_skew') for n in (1000,10000)]
    rows=[]
    for label,key in cases:
        cells=[percentage_text(raw.loc[(key,m),'rate'])+' ['+
               decimal_text(Decimal(str(raw.loc[(key,m),'low']))*100,2)+', '+
               decimal_text(Decimal(str(raw.loc[(key,m),'high']))*100,2)+']' for m in DISPLAY_METHODS]
        rows.append([case_display_label(label)]+cells)
    table(figures/'focused_redesign_cases_rates.tex',
          ['Setting']+[LABELS[m] for m in DISPLAY_METHODS],rows,flexible_first=True)
    rows=[]
    for label,key in cases:
        d=diagnostics.loc[key]
        rows.append([case_display_label(label),f'{d.bias_sd:.3f}',f'{d.variance_ratio:.3f}',f'{dependence.loc[key,"centered_magnitude_spearman"]:.3f}',
                     f'{d.delta_skewness:.3f}',f'{d.df_median:.2f}'])
    table(figures/'focused_redesign_cases_diagnostics.tex',
          ['Setting','Bias/SD',r'\shortstack{Est./obs.\\variance}',r'\shortstack{Rank\\corr.}',
           'Skewness',r'\shortstack{Median\\combined df}'],rows,flexible_first=True)
    rows=[]
    for row in focus[focus.standardised_difference.isin([0,1,2,3,4])].sort_values(['focus','standardised_difference']).itertuples():
        rows.append([f'{row.focus}: {row.standardised_difference:g}',significant_text(row.difference_nats)]+
                    [percentage_text(cal.loc[(row.configuration_id,m),'rate']) for m in ('wald','expanded')])
    table(figures/'focused_redesign_calibrated_power.tex',['Setting: SD','Nats','Normal Wald','Expanded Welch'],rows)
    rows=[]
    for label,key in cases[:3]:
        r=refs[key]
        rows.append([label,f'{r["null_sd"]:.6f}',f'{r["null_sd_mcse"]:.6f}'])
    table(figures/'focused_redesign_null_sd_fitting.tex',['Setting','Null SD (nats)',r'\shortstack{Monte Carlo SE\\(nats)}'],rows)
    moments=pd.read_csv(output/'moments.csv')
    component_spread_table(figures,cases,moments)
    selected=[]
    for mi in (.0001,.02,.05):
        key=select_case(configs,4,'different_skew',1000,mi=mi)
        selected.extend(moments[moments.configuration_id.eq(key)].to_dict('records'))
    component_comparison_table(figures,selected)
    evidence_path=figures/'focused_redesign_evidence.json'
    if evidence_path.exists():
        evidence=json.loads(evidence_path.read_text())
        evidence['display_methods']=list(DISPLAY_METHODS)
        evidence_path.write_text(json.dumps(evidence,indent=2)+'\n')
    print('Updated two-test displays from saved summaries; no fitting or bootstrap draws.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=study.OUTPUT)
    p.add_argument('--figures',type=Path,default=FIGURES)
    p.add_argument('--bootstrap',type=int,default=1000)
    p.add_argument('--workers',type=int,default=3)
    p.add_argument('--displays-only',action='store_true',help='Update two-test views without fitting, resampling or writing results.')
    a=p.parse_args()
    if a.displays_only: render_testing_rule_displays(a.output,a.figures)
    else: report(a.output,a.figures,a.bootstrap,a.workers)
