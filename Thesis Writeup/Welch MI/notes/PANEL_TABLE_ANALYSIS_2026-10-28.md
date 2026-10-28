# Panel and table analysis revision — 28 October 2026

## Reason for this pass

The user identified that explanations of selected shapes do not amount to analysis of all subplots or comparisons across table rows and columns. The earlier language, display and mechanism passes improved definitions and individual explanations, but their coverage judgements were too generous. This pass checks the seven results figures and all eighteen Chapter 6/Appendix C tables against the current manuscript and saved evidence. Definition tables need an explanation of their roles; empirical tables also need interpretation of their principal comparisons.

The preceding sources are preserved in `archive/before_panel_table_analysis_2026-10-28.zip`. Preserve the earlier reading-order edits, mathematical results, numerical tables, figure assets, inclusion rules and historical deliveries. Do not rebuild the PDF or run new experiments.

## Coverage and planned repairs

| Display | Comparisons to interpret | Repair |
| --- | --- | --- |
| Figure 6.1: six panels | All three rows for both P and Q; progression from 2 to 16 categories; peak/trough timing and large-sample recovery | Add the smaller-table contrast and compare columns. Explain why common MI does not give identical normalised errors. Retain the existing singleton and nonlinear-remainder mechanisms. |
| Figure 6.2: four panels | First-order versus sampled df, size ordering, P/Q comparison and missing early sample summaries | Connect size/column differences to the moment-ratio errors and explain why early gaps cannot be read as zero df. Retain the separate effects of mean error, variance error and averaging a nonlinear ratio. |
| Figure 6.3: six panels | Mean versus variance predictions for each population; identical local predictions versus different observations; low-MI plateaus, initial moment-target dip and subsequent rise; different df curves at larger MI | Explain each row and the column contrast, including the upper local df prediction at larger MI. Separate these results from Table 6.1's first-order variance comparisons. |
| Figure 6.4: four rates panels plus four validity strips | Uniform 2-by-2 trough, 4-by-4 excess-to-conservatism, 8-by-8 shoulder and later trough, 16-by-16 repeated crossings; validity and gap between methods | Replace the selective overview with panel-specific comparisons. Use saved variance/dependence diagnostics to explain broad changes; do not claim to identify every fluctuation. |
| Figure 6.5: four rates panels plus four validity strips | Different-skew small-table troughs, 8-by-8 transition, 16-by-16 elevated intermediate rates, validity and method separation | Compare each table size with its uniform counterpart, distinguish variance error from difference bias, and explain why narrowing method separation can coexist with poor calibration. |
| Figure 6.6: A/B/C | Monotone versus U-shaped power, magnitude and changing method gap, comparison at equal null-SD separation | Retain the tail-shift explanation; add the roles of residual bias and changing alternative sampling SD so a common horizontal scale is not mistaken for equal power. |
| Figure 6.7: A/B/C | Which curves move after calibration, persistent B dip, C stability and cross-panel power ranking | Explain the relative change in each test's threshold and distinguish a reversal in method ordering from removal of estimation error. Finish all panels before the sensitivity question. |
| Table 6.1 | Three MI levels, P/Q, moment ratios versus df | Interpret the trend across MI and explain why smaller mean ratios can coexist with lower absolute df. |
| Table 6.2 | Toward/away/tolerance groups | Draw the aggregate conclusion from their relative frequencies without treating the grid as a random population of use cases. |
| Tables 6.3–6.4 | A/B/C, both methods, matched sparse cases and larger samples | Make the equal variance error but different bias/rejection contrast explicit. Preserve the interpretation of each focus setting. |
| Table 6.5 | Stronger MI at A versus B; Wald versus Expanded Welch | Add the missing interpretation of both rows and relate the result to the narrower common-MI finding. |
| Table 6.6 | h=2 versus h=4, both fitting nulls, A/B/C and intervals | Explain growth of lower-null gains alongside their instability under upper-null calibration. |
| Table 6.7 | Variable/population definitions | Already covered by the question/table-construction sequence; no numerical trend exists to interpret. |
| Tables 6.8–6.9 | Month versus weekend, new versus returning, estimates/SE/T versus df/p-values | Existing interpretation covers both rows and methods; retain it. |
| Table C.1 | Ranges across n and reference coefficient 9 | Explain overcorrection at the smallest n and distinguish scaled error from absolute error. |
| Table C.2 | Means versus medians/percentiles/targets, P/Q and sample size | Add interpretation of asymmetry, relative spread, shared/different populations and recovery towards targets. |
| Table C.3 | Bias, variance error, dependence, skewness, combined df across settings | Distinguish displacement from asymmetry and connect changing diagnostics to convergence of test behaviour. |
| Table C.4 | A/B/C and fitted SD versus Monte Carlo SE | Explain implications for absolute alternative differences and precision of the fitted scale. |
| Table C.5 | Nominal versus calibrated power contrasts and interval sizes across A/B/C | Explain reversal, relative magnitude and small but precisely estimated C differences. |
| Table C.6 | Increasing separation versus changing fitting null, absolute power and method ordering | Interpret the different sensitivity at A/B/C, retaining the fixed-alternative comparison. |
| Table C.7 | Matching versus transferred calibration, both methods, both h values and A/B/C | Extend the A example to B/C and the larger separation. |
| Table C.8 | Both methods and both skew regimes | Explain why fewer rejections do not fix almost entirely wrong estimated direction under different skew. |
| Table C.9 | Both methods, raw/adjusted columns and all six comparisons | State which findings survive adjustment and whether method choice changes those decisions. |

## Writing and evidence rules

- Inspect every panel and every empirical row/column grouping. Discuss a shared mechanism once, with explicit links to the panels it explains. Give distinct patterns their own explanation.
- State the trend, comparison and scientific consequence. Use only numerical anchors needed to establish scale; do not transcribe curves or table rows into prose.
- Keep target quantities explicit. Different MI populations need not have the same variance, and equal null-SD separation need not give equal alternative sampling variation.
- Use algebra for direct consequences and saved diagnostics for supported explanations. Report unresolved attribution plainly rather than inventing a cause or a precise turning-point explanation.
- Put detailed interpretation next to the display in ordinary body text. Keep short captions, existing figures and readable table sizes. Preserve the results-to-diagnostics progression and existing calibration question sequence.
- Validate additions against saved summaries and the previously verified repetition diagnostics. Compare all protected numerical and scientific assets, run relevant existing consistency checks, and reread for flow. Leave final page layout to the next requested build.

## Completion and verification

Implemented in Chapter 6 and Appendix C on 28 October 2026. All seven results figures were rendered and inspected alongside their data and adjacent explanations: 38 individual panels including the validity strips. The eighteen Chapter 6/Appendix C tables were reviewed by scientific comparison, including which tables contain definitions rather than empirical trends. The unchanged application interpretation already covers both questions and testing rules.

The revision gives each table-size panel an explicit reading, compares both population columns and all moment/df rows, interprets the distinct power paths and changing method gaps, and follows comparisons across MI, sample size, fitting null and uncertainty summaries. The saved diagnostics also support the newly explicit comparison of alternative sampling SDs across A/B/C. No new experiment or display was added. Shared mechanisms are explained once where possible; minor finite-sample fluctuations are not assigned unique causes without evidence.

Rereading removed duplicated discussion of the component-df dip and unnecessary framing. The chapter still finishes interpreting all three calibrated-power panels before introducing calibration sensitivity. Captions, figure/table blocks, settings, equations and numerical cells are unchanged. This is a substantive expansion of analysis: Chapter 6 increases from 4,645 to 5,960 whitespace-delimited source words and Appendix C from 1,201 to 2,040. These counts include mathematical notation and are not PDF page estimates.

- **43 saved-evidence trend checks pass**, covering moment peaks and recovery, the timing of P/Q differences, the MI-sweep targets, validity, variance-error direction, nominal/calibrated power and alternative sampling variation. The checks use saved summaries and the previously verified scalar-record diagnostics, with no new random draws.
- **12 existing tests pass:** five manuscript consistency and seven ratio/display tests. Paragraph style and whitespace checks pass.
- All 31 active TeX inputs pass brace, environment, math-delimiter and reference checks: 157 unique labels and 187 references. Displayed equations, figure/table blocks, labels and citation sequences in the edited sources are unchanged.
- The other 105 baseline source/figure assets, all 7,381 result summaries and the ten protected PDF/delivery files are unchanged. The main PDF retains its preceding SHA-256 hash.

Evidence and machine-readable checks are in `notes/PANEL_TABLE_ANALYSIS_EVIDENCE_2026-10-28.json` and `notes/PANEL_TABLE_ANALYSIS_CHECKS_2026-10-28.json`. The source revision is complete. The PDF and delivery packages await an explicit rebuild request, when the longer analysis will require a page-flow review.

## Subsequent requested build

The user subsequently requested the rebuild. The reviewed 106-page PDF and complete delivery set are current; the preceding source-only completion record describes the state before that request. Formatting fixes and independent archive verification are recorded in `notes/PANEL_TABLE_PDF_BUILD_2026-10-28.md`.
