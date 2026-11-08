"""Generate the supplementary mechanism report and thesis tables."""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def find_thesis():
    override = os.environ.get("WELCH_MI_THESIS_ROOT")
    candidates = ([Path(override).expanduser().resolve()] if override else [])
    candidates.extend([ROOT.parent / "Thesis Writeup/Welch MI", ROOT.parent])
    for candidate in candidates:
        if (candidate / "main.tex").is_file() and (candidate / "figures_rewrite").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate thesis source; set WELCH_MI_THESIS_ROOT")


THESIS = find_thesis()
OUT = ROOT / "results/thesis_mechanism_check"
FINAL = ROOT / "results/thesis_redesign"
FIG = THESIS / "figures_rewrite"
METHODS = ["normal_wald", "hutcheson_welch", "simple_welch", "kurtosis_welch", "expanded_welch"]
LABELS = ["Normal Wald", "Hutcheson-style", "Simple Welch", "Kurtosis only", "Expanded Welch"]


def local_moment_df(frame, interaction_df):
    """Evaluate the local component-df formula with the matching sample size."""
    sample_size = frame.n_p.where(frame.population.eq("p"), frame.n_q)
    return (
        (sample_size * frame.v + interaction_df) ** 2
        / (2 * sample_size * frame.v + interaction_df)
    )


def markdown(frame):
    lines = ["| " + " | ".join(frame.columns) + " |", "| " + " | ".join(["---"]*len(frame.columns)) + " |"]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(f"{x:.5g}" if isinstance(x, float) else str(x) for x in row) + " |")
    return "\n".join(lines)


def table(caption, label, header, rows, spec):
    return ("\\begin{table}[htbp]\n\\centering\\small\n\\caption{"+caption+"}\n"
            "\\label{"+label+"}\n\\begin{tabular}{"+spec+"}\n\\toprule\n"+header+
            "\\\\\n\\midrule\n"+"\n".join(rows)+"\n\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def main():
    display = pd.read_csv(FINAL / "display_manifest.csv")
    cells = pd.read_csv(FINAL / "cell_results.csv")
    rates = pd.read_csv(OUT / "ablation_rates.csv")
    diag = pd.read_csv(OUT / "denominator_diagnostics.csv")
    components = pd.read_csv(OUT / "component_diagnostics.csv")
    main_null = display.loc[display.section.eq("main") & display.mi_difference.eq(0)]
    assert len(main_null) == 108
    joined = main_null.merge(cells, on="configuration_id", suffixes=("", "_result"))
    lines = [r"\begingroup\footnotesize", r"\setlength{\tabcolsep}{4pt}",
        r"\begin{longtable}{@{}llrrrrr@{}}",
        r"\caption{All 108 main null regimes in the frozen run. Each rate uses all 20,000 replicates. V denotes the fraction with a valid result. Uniform and same-skew profiles have $P=Q$; different-skew profiles have $P\ne Q$ with equal MI.}\label{tab:all-main-null}\\",
        r"\toprule Shape & Margins & $n$ & Wald & V & Expanded & V\\\midrule\endfirsthead",
        r"\toprule Shape & Margins & $n$ & Wald & V & Expanded & V\\\midrule\endhead"]
    for keys, group in joined.groupby(["shape", "profile", "n_p"], sort=True):
        s, p, n = keys
        w = group[group.method.eq("normal_wald")].iloc[0]
        e = group[group.method.eq("expanded_welch")].iloc[0]
        lines.append(f"{s} & {p.replace('_',' ')} & {n} & {w.unconditional_rejection_rate:.4f} & {w.valid_rate:.4f} & {e.unconditional_rejection_rate:.4f} & {e.valid_rate:.4f} \\")
        lines[-1] += "\\"
    lines += [r"\bottomrule\end{longtable}", r"\endgroup"]
    (FIG / "main_null_table.tex").write_text("\n".join(lines)+"\n")
    weak_rows = []
    for p in ["uniform", "same_skew", "different_skew"]:
        group = joined[joined.profile.eq(p)]
        for m in ["normal_wald", "expanded_welch"]:
            g = group[group.method.eq(m)]
            r = g.unconditional_rejection_rate
            weak_rows.append(dict(profile=p, method=m, regimes=len(g),
                below=int((r<.025).sum()), inside=int(r.between(.025,.075).sum()),
                above=int((r>.075).sum()), low_valid=int((g.valid_rate<.9).sum()),
                minimum_valid=float(g.valid_rate.min())))
    pd.DataFrame(weak_rows).to_csv(OUT / "null_profile_summary.csv", index=False)
    d = diag[(diag["shape"]=="3x3") & diag.profile.eq("different_skew") & diag.target_mi_p.eq(.02)
             & diag.n_p.eq(diag.n_q) & diag.n_p.isin([100,1000])].sort_values("n_p")
    rows = [f"{r.n_p} & {r.mean_se2_over_empirical_var:.2f} & {r.normal_wald_rate:.4f} & {r.independent_mc_sd_rate:.4f} & {r.population_first_order_sd_rate:.4f} \\\\" for r in d.itertuples()]
    text = table("Denominator diagnostic for the additive first-block $3\\times3$ different-skew null, $I(P)=I(Q)=0.02$. $R$ is mean estimated squared SE divided by independently estimated sampling variance. MC SD uses that independent finite-sample SD; first-order SD uses the population influence variance. Each pilot and evaluation uses 20,000 independent replicates.",
                 "tab:denominator-check",r"$n$ & $R$ & Wald & MC SD & First-order SD",rows,"rrrrr")
    c = components[components.configuration_id.isin(d.configuration_id)].copy()
    shape_dims = c["shape"].str.extract(r"(?P<rows>\d+)x(?P<cols>\d+)").astype(int)
    interaction_df = (shape_dims.rows - 1) * (shape_dims.cols - 1)
    c["local_moment_df"] = local_moment_df(c, interaction_df)
    c = c.sort_values(["n_p", "population"])
    rows = [f"{r.n_p} & {r.population.upper()} & {r.mean_vhat_over_v:.2f} & {r.population_first_order_df:.2f} & {r.local_moment_df:.2f} & {r.median_plugin_df:.2f} & {r.empirical_moment_df:.2f} \\\\" for r in c.itertuples()]
    text += table("Variance and component-df diagnostics for the same populations. First order is $2nV^2/\\tau^2$; local moments is $(nV+d)^2/(2nV+d)$; plug-in is the median first-order estimate over evaluation tables; MC is $2\\overline{\\widehat V}^{2}/s^2_{\\widehat V}$ from the independent pilot.",
                  "tab:component-check",r"$n$ & Population & $\E\widehat V/V$ & First order & Local moments & Plug-in & MC",rows,"rlrrrrr")
    (FIG / "mechanism_tables.tex").write_text(text)
    for shape in ["2x2", "3x3", "5x5", "8x8"]:
        fig, axes = plt.subplots(3, 3, figsize=(10, 8), sharex=True, sharey=True)
        for i, profile in enumerate(["uniform", "same_skew", "different_skew"]):
            for j, n in enumerate([10,100,1000]):
                ax = axes[i,j]
                sel = rates[rates.section.eq("main") & rates["shape"].eq(shape) & rates.profile.eq(profile) & rates.n_p.eq(n)]
                for m, label, color, marker, style in zip(METHODS,LABELS,["#184a70","#7a5195","#d67816","#348354","#b03c78"],["o","D","v","^","s"],["-","--","--","-.",":"]):
                    r=sel[sel.method.eq(m)].sort_values("target_mi_q")
                    x=r.target_mi_q-r.target_mi_p
                    ax.plot(x,r.rate,label=label,color=color,marker=marker,linestyle=style,markersize=3)
                    low=r.valid_rate<.9
                    ax.scatter(x[low],r.rate[low],facecolors="white",edgecolors=color,s=20,zorder=4)
                ax.axhline(.05,color="gray",linestyle=":",linewidth=.7)
                ax.set(xlim=(0,.02),ylim=(0,.15),title=f"{profile.replace('_',' ')}, $n={n}$")
                ax.grid(alpha=.15)
                if j==0: ax.set_ylabel("Rejection rate")
                if i==2: ax.set_xlabel("MI difference (nats)")
        handles,labels=axes[0,0].get_legend_handles_labels()
        fig.legend(handles,labels,loc="upper center",ncol=5,frameon=False)
        fig.tight_layout(rect=(0,0,1,.96))
        fig.savefig(OUT / f"ablation_{shape}.pdf",bbox_inches="tight")
        if shape=="3x3": fig.savefig(FIG / "mechanism_ablation.pdf",bbox_inches="tight")
        plt.close(fig)
    overview = ["# Supplementary mechanism checks", "", "This is a post-protocol diagnostic study, separate from the frozen confirmatory run.", "",
        "## Design", "", "The saved tables supply all populations. There are 809 unique configurations: the complete main grid, the 3x3 different-skew baseline and imbalance checks, and the 3x3/8x8 convergence checks. Every configuration uses 20,000 new evaluation pairs; every null also uses an independent 20,000-pair pilot. Seeds and source hashes are in metadata.json.", "",
        "All five reference variants share the corrected numerator and plug-in standard error. The Hutcheson-style MI analogue uses n per component, following Hutcheson's information-theoretic Satterthwaite assignment. Simple Welch uses n-1 per component. Kurtosis-only Welch freezes the pointwise scores when differentiating the variance. Expanded Welch differentiates the complete functional. The separate observed-support sensitivity changes the numerator correction to (occupied cells - occupied rows - occupied columns + 1)/(2n). It is not a validated replacement.", "",
        "Across the 809 configurations, Hutcheson-style and Simple Welch have identical rejection rates in 494 cases. Their mean absolute difference is 0.00047 and their largest difference is 0.01235, in the 5x5 uniform n=5 alternative with target MI values 0.020 and 0.022.", "",
        "## Denominator diagnostic", "", markdown(d), "",
        "The MC SD is estimated from the independent pilot at the known null population. It is an explanatory reference, unavailable from a single real dataset. It leaves numerator bias and non-normal shape intact, but removes the random denominator and its dependence on the numerator together. It therefore does not isolate mean variance bias alone. The population first-order SD omits quadratic sampling variation and is not the finite-sample true SD.", "",
        "## Component degrees of freedom", "", markdown(c), "",
        "The empirical moment df validates approximation quality; finite-difference tests only validate the derivative. These are component dfs, distinct from the combined two-sample df.", "",
        "## Complete evidence", "", "- ablation_rates.csv: every selected regime, all six arms, rejection counts, validity, MC standard errors and paired differences from Wald.",
        "- denominator_diagnostics.csv: all selected nulls and both population-SD diagnostics.",
        "- component_diagnostics.csv: both populations at every selected null, variance ratios and three empirical or first-order df definitions; the local-moment column in the thesis table is calculated from the recorded population V, n and table dimension.",
        "- selected_displays.csv: exact selected settings and frozen configuration identifiers.",
        "- ablation_2x2.pdf through ablation_8x8.pdf: main curves, rows = margin profiles, columns = n=10,100,1000. All axes use MI difference 0--0.02 and rejection 0--0.15; larger rates are outside this calibration zoom and remain in the CSV. Hollow markers mean validity below 90%.", "",
        "## Strong and weak nulls", "", markdown(pd.DataFrame(weak_rows)), "",
        "These descriptive bins use the wide interval [0.025,0.075]; being inside is not proof of nominal calibration. They accompany all 108 exact main-null rates in the thesis appendix. Same-margin nulls here have P=Q; different-skew nulls have equal MI but P!=Q."]
    (OUT / "REPORT.md").write_text("\n".join(overview)+"\n")
    print("Generated all 108 main-null rows, mechanism tables, four ablation figures and report.")


if __name__ == "__main__": main()
