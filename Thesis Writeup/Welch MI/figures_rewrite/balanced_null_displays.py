"""Render the balanced common-MI null grid and its compact mechanism table."""
from pathlib import Path
import argparse
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
RESULTS=HERE.parents[2]/"WelchSatterthwaiteMI/results/balanced_null_2026-11-01"
LEVELS={.005:"#0072b2",.02:"#e69f00",.30:"#009e73"}
METHODS={"normal_wald":("Normal Wald","-","o"),
         "expanded_welch":("Expanded Welch","--","s")}
CASES=[(4,"uniform",20),(16,"same_skew",1000),(16,"different_skew",1000)]


def generate(results=RESULTS,destination=HERE):
    audit=json.loads((results/"combined_audit.json").read_text())
    assert audit["passed"] and audit["settings"]==360 and audit["pairs"]==36000000
    rates=pd.read_csv(results/"combined_rates.csv")
    rates=rates[rates.denominator.eq("all")]
    assert len(rates)==720 and rates.replicates.eq(100000).all()
    np.testing.assert_allclose(rates.rejection_rate,rates.rejections/rates.replicates)
    ymax={k:float(max(.10,.05*np.ceil((rates[rates.k.eq(k)].rejection_high.max()+.005)/.05)))
          for k in [2,4,8,16]}
    plt.rcParams.update({"font.size":10,"axes.labelsize":10,"axes.titlesize":11,
        "legend.fontsize":9,"pdf.fonttype":42,"axes.spines.top":False,"axes.spines.right":False})
    evidence={"inputs_sha256":{name:hashlib.sha256((results/name).read_bytes()).hexdigest()
        for name in ["combined_rates.csv","combined_paired.csv","combined_diagnostics.csv","combined_audit.json"]},
        "ymax_by_size":ymax,"figures":{}}
    for profile in ["uniform","same_skew","different_skew"]:
        fig=plt.figure(figsize=(7.1,6.6))
        grid=fig.add_gridspec(2,2,hspace=.50,wspace=.28,left=.12,right=.98,top=.95,bottom=.22)
        ids=[]
        for position,k in enumerate([2,4,8,16]):
            pair=grid[position//2,position%2].subgridspec(2,1,height_ratios=[4,1],hspace=.10)
            ax=fig.add_subplot(pair[0]);valid=fig.add_subplot(pair[1],sharex=ax)
            subset=rates[rates.profile.eq(profile)&rates.k.eq(k)]
            assert len(subset)==60
            ids.extend(subset.configuration_id.unique().tolist())
            for common,colour in LEVELS.items():
                for method,(_,style,marker) in METHODS.items():
                    r=subset[np.isclose(subset.common_mi,common)&subset.method.eq(method)].sort_values("n_p")
                    assert len(r)==10 and not r.n_p.duplicated().any()
                    ax.plot(r.n_p,r.rejection_rate,color=colour,ls=style,marker=marker,
                        markerfacecolor=colour if method=="normal_wald" else "none",
                        markeredgewidth=.65,ms=3 if method=="normal_wald" else 5,lw=1.3)
                    ax.fill_between(r.n_p,r.rejection_low,r.rejection_high,color=colour,alpha=.08)
                    valid.plot(r.n_p,r.valid_rate,color=colour,ls=style,lw=1.1)
            ax.axhline(.05,color="black",ls=":",lw=.9,zorder=0)
            ax.set(xscale="log",ylim=(0,ymax[k]),title=rf"${k}\times{k}$",ylabel="False-positive rate")
            ax.set_yticks(np.arange(0,ymax[k]+.001,.05))
            ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
            ax.tick_params(labelbottom=False)
            valid.set(ylim=(-.05,1.07),yticks=[0,1],xlabel="Sample size per population")
            valid.tick_params(labelsize=8);valid.xaxis.label.set_size(9)
            valid.set_ylabel("Valid fraction",fontsize=9,rotation=0,ha="left",va="bottom")
            valid.yaxis.set_label_coords(.02,.13)
        common_handles=[Line2D([],[],color=colour,lw=1.5,label=f'{value:g}') for value,colour in LEVELS.items()]
        method_handles=[Line2D([],[],color="black",ls=style,marker=marker,
            ms=3 if method=="normal_wald" else 5,markeredgewidth=.65,
            markerfacecolor="black" if method=="normal_wald" else "none",label=label)
            for method,(label,style,marker) in METHODS.items()]
        method_handles.append(Line2D([],[],color="black",ls=":",lw=.9,label="Nominal 5%"))
        fig.legend(handles=common_handles,loc="lower center",bbox_to_anchor=(.5,.075),ncol=3,
            title="Common population MI (nats)",title_fontsize=9)
        fig.legend(handles=method_handles,loc="lower center",bbox_to_anchor=(.5,.015),ncol=3)
        name=f'balanced_null_{profile}.pdf';fig.savefig(destination/name,bbox_inches="tight");plt.close(fig)
        evidence["figures"][name]=dict(configurations=sorted(ids),common_mi=list(LEVELS),
            repetitions_per_setting=100000)
    diagnostics=pd.read_csv(results/"combined_diagnostics.csv")
    rows=[];case_ids=[]
    for k,profile,n in CASES:
        selected=diagnostics[diagnostics.k.eq(k)&diagnostics.profile.eq(profile)&diagnostics.n_p.eq(n)
            &np.isclose(diagnostics.common_mi,.02)]
        assert len(selected)==1
        d=selected.iloc[0];key=d.configuration_id;case_ids.append(key)
        case=rates[rates.configuration_id.eq(key)].set_index("method")
        assert case.valid_replicates.eq(100000).all()
        label={"uniform":"Uniform","same_skew":"Same skew","different_skew":"Different skew"}[profile]
        sample_size=f'{n:,}'.replace(',',r'{,}')
        rows.append([label+rf' \({k}\times{k}\), \(n={sample_size}\)',
            f'{d.difference_bias/np.sqrt(d.observed_variance):.3f}',f'{d.estimated_observed_ratio:.3f}',
            f'{100*case.loc["normal_wald","rejection_rate"]:.2f}',
            f'{100*case.loc["expanded_welch","rejection_rate"]:.2f}'])
    table=[r'\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}Xrrrr@{}}',r'\toprule',
           r'\textbf{Setting} & \textbf{Bias / SD} & \shortstack[r]{\textbf{Variance}\\\textbf{ratio}} & \shortstack[r]{\textbf{Normal Wald}\\\textbf{(\%)}} & \shortstack[r]{\textbf{Expanded Welch}\\\textbf{(\%)}}\\',r'\midrule']
    for index, row in enumerate(rows):
        if index:
            table.append(r'\addlinespace[0.35em]')
        table.append(' & '.join(row)+r'\\')
    table.extend([r'\bottomrule',r'\end{tabularx}'])
    (destination/"balanced_null_diagnostics.tex").write_text('\n'.join(table)+'\n')
    evidence["diagnostic_cases"]=case_ids;evidence["diagnostic_rows"]=rows
    (destination/"balanced_null_evidence.json").write_text(json.dumps(evidence,indent=2)+"\n")
    print(json.dumps({"rendered_settings":360,"diagnostic_rows":rows,"ymax_by_size":ymax}))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results",type=Path,default=RESULTS)
    parser.add_argument("--figures",type=Path,default=HERE)
    args=parser.parse_args();generate(args.results,args.figures)
