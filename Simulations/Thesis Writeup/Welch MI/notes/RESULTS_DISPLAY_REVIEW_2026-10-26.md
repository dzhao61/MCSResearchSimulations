# Results displays and evidence placement — 26 October 2026

## Approved scope and preservation

The reader approved splitting the moment figure, displaying the broad-grid ranges in a compact table, shortening duplicated numerical prose, and checking the other results sections for the same issue. The review covers every results subsection in Chapter 6 and all four sections of Appendix C. Chapter 7 interprets evidence already presented and does not require a second set of result displays.

The preceding 99-page main PDF, active manuscript and figure inputs, thesis README and root verification record are preserved in `archive/before_results_display_revision_2026-10-26.zip`. This includes the already-approved simulation-repetition wording. Historical drafts and archives are unchanged.

## Audit and resulting evidence placement

| Passage | Accompanying evidence and action |
| --- | --- |
| 6.1.1 Mean and sampling-variance predictions | Figure 6.1 now contains the first two rows of the previous moment plot. Table 6.2 displays the quoted ranges at n=1,000 and 50,000 across all table sizes, margin regimes and both populations. The text distinguishes this complete-grid summary from the different-skew figure and interprets the ratios. |
| 6.1.2 Consequences for degrees of freedom | Figure 6.2 contains the previous bottom row, with the same saved ratios, uncertainty bands and positivity/finite-value rule. Table 6.3 remains the numerical component comparison. It is kept before its column explanations. Appendix Table C.2 is explicitly cited for the additional focus-setting examples. |
| 6.1.3 Near independence | Figure 6.3 retains the observed moments and Appendix A.4 predictions. An explicit reference to Table 6.3 connects the population and sample-based variance ratios to their numerical evidence. |
| 6.2 Broad false-positive comparison | Table 6.4 displays the 120-setting classification with the existing 0.3-percentage-point tolerance. Figures 6.4–6.5 retain the null rates and validity panels. Definitions and interval conventions remain beside this evidence. |
| 6.2.1 Selected null cases | Table 6.5 adds a compact subset of the saved bias/SD and variance-ratio diagnostics; Appendix C retains the fuller diagnostic table. Table 6.6 retains all seven original rate rows and intervals. Table 6.7 adds the previously prose-only higher-common-MI comparison of A and B, using the saved upper-null rates and Wilson intervals. The general all-repetitions denominator includes invalid outputs as non-rejections. The all-valid statement still applies specifically to the original seven cases, not the higher-MI cases. |
| 6.3.1 Nominal power | Figure 6.6 already accompanies the power curves, including B's initial decline. The paired contrasts remain in Appendix Table C.5 for precise numerical comparisons; their pairing is explained in the main text. |
| 6.3.2 Calibrated power | The existing calibrated-power figure moves from Appendix C to the main discussion as Figure 6.7, without changing its data, size or bands. Table 6.8 retains lower/upper-null power contrasts and joint bootstrap intervals. Appendix C retains full absolute rates and cross-null validation. |
| 6.4 Association construction | Table 6.9 adds the existing copying/four-cell comparison at 16×16 and n=1,000 under both skew regimes, showing difference bias and rejection rates for both tests and the moment reference. The prose explains the contrast rather than repeating every cell. |
| 6.4 Sample allocation | Table 6.10 adds the three allocations at fixed P, Q and total sample size 2,000, with the observed SD, median Expanded Welch degrees of freedom, and both tests' power. The alternative's MI values, units and percentage scale are explicit. |
| 6.5 Shopping application | Table 6.11 already accompanies both MI estimates, degrees of freedom and p-values. The worked statistic and interpretation are retained; Appendix Table C.9 supports the Holm adjustment. |
| C.1 Component diagnostics | Table C.1 replaces the three prose-only scaled-mean-error ranges. Tables C.2–C.4 retain component spread, shared-estimator diagnostics and reference fitting. |
| C.2 Calibration sensitivity | Tables C.5–C.7 retain the paired contrasts, absolute power and cross-null validation. The moved calibrated graph is referenced in Chapter 6 rather than duplicated. |
| C.3 Rejection direction | Table C.8 replaces the wrong-direction/rejection counts in prose, preserving all previous counts and adding the saved same-skew moment-reference count. The bias-shift equation, n=10,000 result and interpretation remain. |
| C.4 Multiple testing | Table C.9 retains all raw and Holm-adjusted p-values. The dataset definitions and adjustment procedure remain; the introduction is shortened. |

## Reproduction and scientific preservation

`figures_rewrite/focused_results_displays.py` produces the two separated plots and seven new data-table files directly from saved CSV summaries. The null-grid classification table uses the existing reporting macros. The helper accepts `--results` for an extracted experiment supplement. Its evidence JSON records all selected table values and input hashes. It does not run the experiment, refit references, or draw bootstrap samples.

All 11,878 snapshotted files in `WelchSatterthwaiteMI/results/approximation_redesign/` outside the pilot directory were verified unchanged by SHA-256, including the existing calibrated intervals and the higher-MI nominal rates. Every preceding figure/table asset is unchanged; new assets have separate names. Existing displayed equations and citation sequences are preserved. Only Chapter 6 and Appendix C change among the manuscript chapters/appendices. The protected derivation and scientific qualifications remain intact. Quoted values moved into tables retain the same underlying evidence, with table precision explicit; redundant rounded approximations need not also remain in prose.

No experiment, calibration fitting or bootstrap sampling was rerun. No Git commit was requested or performed.

## Layout and validation

The manuscript is 102 pages, compared with 99 before this revision. Main text is 63 pages, compared with 61; Chapter 6 is 16 pages, compared with 14. Appendix C remains six pages. The list of tables gains one page. Existing dense figure sizes are preserved, and the separated moment panels remain readable at full text width. Captions stay short; settings and interpretation remain in body text.

All five existing thesis-consistency tests and eight packaging tests pass. Source preservation and scientific evidence hash checks pass. The main build has no LaTeX warnings, unresolved references, or overfull/underfull boxes. Physical pages 4–9, 52–67 and 92–97 were rendered and visually reviewed, with the updated Chapter 6 pages reviewed again after the final placement and prose changes.

The delivery package and checksums were refreshed, and package verification passes. Main, build and delivery PDFs are byte-identical. The extracted source archive builds independently without warnings and produces identical PDF text. These completed checks are recorded in the root verification file.
