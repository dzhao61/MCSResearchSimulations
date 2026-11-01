"""Render three MI-gap magnitudes across the complete nominal-power grid."""
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
RESULTS=HERE.parents[2]/"WelchSatterthwaiteMI/results/mi_gap_power_2026-11-01"
GAPS={.005:"#0072b2", .01:"#e69f00", .02:"#009e73"}
METHODS={"normal_wald":("Normal Wald","-","o"),
         "expanded_welch":("Expanded Welch","--","s")}


def generate(results=RESULTS,destination=HERE):
    audit=json.loads((results/"combined_audit.json").read_text())
    assert audit["passed"] and audit["settings"]==360 and audit["pairs"]==36000000
    rates=pd.read_csv(results/"combined_rates.csv")
    rates=rates[rates.denominator.eq("all")]
    assert len(rates)==720 and rates.replicates.eq(100000).all()
    np.testing.assert_allclose(rates.rejection_rate,rates.rejections/rates.replicates)
    plt.rcParams.update({"font.size":10,"axes.labelsize":10,"axes.titlesize":11,
        "legend.fontsize":9,"pdf.fonttype":42,"axes.spines.top":False,"axes.spines.right":False})
    evidence={"inputs_sha256":{name:hashlib.sha256((results/name).read_bytes()).hexdigest()
        for name in ["combined_rates.csv","combined_paired.csv","combined_diagnostics.csv","combined_audit.json"]},
        "figures":{}}
    for profile in ["uniform","same_skew","different_skew"]:
        fig=plt.figure(figsize=(7.1,6.6))
        grid=fig.add_gridspec(2,2,hspace=.50,wspace=.28,left=.11,right=.98,top=.95,bottom=.22)
        ids=[]
        for position,k in enumerate([2,4,8,16]):
            pair=grid[position//2,position%2].subgridspec(2,1,height_ratios=[4,1],hspace=.10)
            ax=fig.add_subplot(pair[0]);valid=fig.add_subplot(pair[1],sharex=ax)
            subset=rates[rates.profile.eq(profile)&rates.k.eq(k)]
            assert len(subset)==60
            ids.extend(subset.configuration_id.unique().tolist())
            for gap,colour in GAPS.items():
                for method,(label,style,marker) in METHODS.items():
                    r=subset[np.isclose(subset.gap,gap)&subset.method.eq(method)].sort_values("n_p")
                    assert len(r)==10 and not r.n_p.duplicated().any()
                    ax.plot(r.n_p,r.rejection_rate,color=colour,ls=style,marker=marker,
                        markerfacecolor=colour if method=="normal_wald" else "white",
                        markeredgewidth=.65,ms=3,lw=1.3)
                    ax.fill_between(r.n_p,r.rejection_low,r.rejection_high,color=colour,alpha=.08)
                    valid.plot(r.n_p,r.valid_rate,color=colour,ls=style,lw=1.1)
            ax.set(xscale="log",ylim=(-.025,1.025),title=rf"${k}\times{k}$",ylabel="Power")
            ax.set_yticks([0,.25,.5,.75,1]);ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
            ax.tick_params(labelbottom=False)
            valid.set(ylim=(-.05,1.07),yticks=[0,1],xlabel="Sample size per population")
            valid.tick_params(labelsize=8);valid.xaxis.label.set_size(9)
            valid.set_ylabel("Valid fraction",fontsize=9,rotation=0,ha="left",va="bottom")
            valid.yaxis.set_label_coords(.02,.13)
        gap_handles=[Line2D([],[],color=colour,lw=1.5,label=f'{gap:g}') for gap,colour in GAPS.items()]
        method_handles=[Line2D([],[],color="black",ls=style,marker=marker,ms=3,
            markerfacecolor="black" if method=="normal_wald" else "white",label=label)
            for method,(label,style,marker) in METHODS.items()]
        fig.legend(handles=gap_handles,loc="lower center",bbox_to_anchor=(.5,.075),ncol=3,
            title=r"MI-gap magnitude $|\Delta|$ (nats)",title_fontsize=9)
        fig.legend(handles=method_handles,loc="lower center",bbox_to_anchor=(.5,.015),ncol=2)
        name=f'mi_gap_power_{profile}.pdf'
        fig.savefig(destination/name,bbox_inches="tight");plt.close(fig)
        evidence["figures"][name]=dict(configurations=sorted(ids),gaps=list(GAPS),
            target_mi_p=.02,target_mi_q=[.025,.03,.04],repetitions_per_setting=100000)
    (destination/"mi_gap_power_evidence.json").write_text(json.dumps(evidence,indent=2)+"\n")
    print("Rendered all 360 settings across three MI gaps and margin figures.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results",type=Path,default=RESULTS)
    parser.add_argument("--figures",type=Path,default=HERE)
    args=parser.parse_args();generate(args.results,args.figures)
