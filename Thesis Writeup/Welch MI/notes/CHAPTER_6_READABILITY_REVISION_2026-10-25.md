# Chapter 6 readability revision — 25 October 2026

## Scope and preservation

The reader approved a targeted readability revision to Chapter 6: lead with findings, make the mean comparison explicit, keep bias interpretation beside the evidence, shorten repeated explanations in the power section, and make only light changes to the construction/allocation and application sections.

The preceding 98-page manuscript and active manuscript/source/figure inputs are preserved in `archive/before_chapter6_readability_revision_2026-10-25.zip`. Chapter and section order are unchanged. No manuscript chapter or appendix outside Chapter 6 was edited.

## Changes

- Section 6.1 separates the numerical findings from the figure guide. It explicitly distinguishes the observed sampling mean of the variance estimator from V(P), which the first-order calculation uses to approximate that mean. The worked P/Q comparison explains why substituting the smaller population coefficient lowers the numerator of the moment-matching formula.
- Population first-order approximation error and the additional error from using sampled proportions remain distinct. The near-independence comparison identifies P explicitly and names sampling-variance predictions when describing errors in opposite directions.
- Section 6.2 leads with the conditional false-positive result and the full 120-setting classification. Validity information is beside the plot guide. The two broad null figures finish before the detailed case subsection.
- The small-sample and sparse-table cases retain every rejection rate, variance/bias diagnostic and limitation. Bias cancellation is explained in the matched same-skew null comparison, where it accounts for the different results.
- Section 6.3 explains B's initial decline in nominal rejection once, identifying how increasing I(Q) initially offsets positive estimation bias and lowers the absolute statistic. The calibrated comparison states briefly that the decline persists. Calibration-population sensitivity, all paired intervals and the limits of the two-null check remain explicit.
- Section 6.4 leads with the allocation result and names Expanded Welch as the method whose median degrees of freedom fall.
- Section 6.5 retains the data source, selection of six comparisons, group/sample counts, categorical construction, sparse-cell details, bias corrections, both worked statistics, test outcomes and Holm-adjusted results. Repeated descriptions of the two tests and redundant interpretation are shortened. Non-rejection remains distinguished from equality; the unknown population moment target remains a limitation.

## Preservation and validation

- All five figure blocks, four table blocks and two displayed equation blocks remain byte-identical, including captions, dimensions and typography. All figure assets are unchanged.
- Every distinct numerical literal in the previous Chapter 6 source remains, and the citation sequence and section/subsection headings are unchanged. No estimates, simulation results or uncertainty calculations were recomputed.
- Before updating internal records, source/asset hashes confirm that only Chapter 6 and the thesis README changed among the snapshotted inputs, together with the rebuilt PDF after packaging. Chapter 5 and the protected theory remain unchanged.
- All five manuscript-consistency tests and eight packaging tests pass.
- The final main build has no LaTeX warnings, undefined references or overfull/underfull boxes.
- Physical pages 4–8 and 51–64 were rendered and visually reviewed, including the plot/table sequence, application and transition to Chapter 7. A float barrier keeps the broad null plots before the detailed case subsection. The month paragraph keeps the method name together across a page break.
- The manuscript remains 98 pages with 60 pages of main text; Chapter 6 remains 13 pages. Prose is slightly shorter; numerical evidence and scientific qualifications are retained.

Full delivery checksum/inventory checks pass. The extracted source archive builds independently without warnings and produces identical PDF text. These completed checks are recorded in the root verification file. No experiments, bootstrap sampling or Git commit were requested or performed.
