# Chapter 6 ratio and notation audit — 26 October 2026

The review covers all results subsections in Chapter 6, generated displays and their definitions, interpretation and reporting dependencies. The preceding manuscript and reporting sources are preserved in `archive/before_observed_prediction_ratios_2026-10-26.zip`. Historical archives are unchanged.

## Display convention

| Quantity | Displayed ratio | Meaning above one |
| --- | --- | --- |
| Mean variance coefficient | E(Vhat) / V | The population prediction is too low |
| Sampling variance, population prediction | Var(Vhat) / (tau²/n) | The population prediction is too low |
| Sampling variance, sample prediction | Var(Vhat) / (E(tauhat²)/n) | The average sample prediction is too low |
| Component degrees of freedom | nu_mom / nu, or nu_mom / E(nuhat) | The approximation is too low |
| Shared squared standard error | Var(Deltahat) / E(SEhat²) | The average estimated difference variance is too low |

The component-df plot requires all estimates to be positive and finite before displaying the unconditional mean comparison. Other conditional numerical summaries retain their included counts. A zero numerator or denominator leaves a reciprocal comparison undefined.

All reciprocals use unrounded source values. For an original positive confidence interval [L,U], the reciprocal band is [1/U,1/L]. The transformed band retains approximate coverage and can be asymmetric. Intervals crossing zero are rejected rather than displayed as falsely bounded bands. The maximum relative half-width for Figure 6.1 remains below 1.3% after inversion.

## Changes and dependencies

- Figure 6.1 retains observed/predicted means and reverses the sampling-variance ratios, including the dashed sample-based curve and confidence bands. Figure 6.2 uses moment target / approximation. Both use symbolic ratio definitions and ordinary decimal y-axis ticks; the agreement value is labelled 1.
- The uniform and same-skew companion plots use the same convention. Near-independence plot labels use n E(Vhat) and n² Var(Vhat) and distinguish the local approximation.
- Component tables, shared-estimator diagnostics and their Appendix C counterparts use the new ratios. The unprinted range table is also updated, without reintroducing it into the manuscript.
- Section 6.1 explains each direction before its numerical example. The 16×16 P example at n=1,000 now has observed/population-prediction variance ratio 1.32 and observed/mean-sample-prediction ratio 0.599. The corresponding 4×4 example has ratios 1.031 and 1.034. Near-independence examples and df target/mean comparisons are recomputed from the original data.
- Chapter 5 definitions, Chapter 7 interpretations and Appendix B validity rules, algebraic decomposition and uncertainty calculation agree with the displayed ratios. Chapter 7 now explicitly names tau²(P)/n_P and Var(Vhat(P)) near independence.
- The positive power axes represent −Delta/sigma_0, since Delta=I(P)−I(Q) is negative in these alternatives. Companion unstandardised axes use −Delta. Test statistics, decision rules and rates are unchanged.
- Bias/SD, rejection and validity proportions, paired power differences and near-independence moment levels answer different questions and retain their existing definitions.
- `report_ratio_tools.py` centralises transformations, mathematical labels, interval handling and df inclusion rules. Both reporters use it. The experiment supplement includes the module and its tests and explains the unchanged historical orientation of the raw CSV fields.

## Verification

The complete 228-test experiment suite and all eight packaging tests pass. Tests check reciprocal endpoint ordering and asymmetry, incomplete df summaries, original unrounded plotted values, the df decomposition identity, the Monte Carlo width bound, power-axis sign and decimal tick labels.

Of 11,878 pre-edit saved result files, 11,877 are byte-identical. Only reporting provenance changes to record the current reporter and ratio tools. No simulation output, summary CSV, fitting result, bootstrap sample or scientific calculation is changed. Chapters 2–4 and Appendix A are preserved.

Final packaging, independent source build and rendered-page checks are recorded in the workspace `REDESIGN_VERIFICATION.json` after completion.

The rebuilt delivery contains 103 pages (64 pages of main text; Chapter 6 is 17 pages). The packaged source builds independently without warnings and produces identical extracted PDF text. The delivery check verifies all PDF, source and experiment supplement entries and checksums. Regenerating the added result displays from the packaged helper and packaged summaries reproduces all ten outputs: tables/evidence are byte-identical and the two figure renders are pixel-identical. Front matter, Chapter 6 and affected pages in Chapter 5, Chapter 7 and Appendices B–C have been visually reviewed. No layout/font-size compression was introduced to force the previous page count.
