# Chapter 5 presentation revision — 25 October 2026

## Scope

The reader requested more tables, lists and equations where verbal descriptions obscure parameter settings or calculations. This pass changes Chapter 5 presentation, preserving the experiment, four comparison rules, numerical results and theoretical chapters. The earlier suggestion to remove the sample-size degrees-of-freedom comparator remains pending; this pass does not implement it.

The complete pre-edit thesis sources, figures and 96-page PDF are preserved in `archive/before_chapter5_visual_revision_2026-10-25.zip`. The baseline archive and historical working drafts are unchanged.

## Changes

- Display the existing four-category margin example in Section 5.1.
- Add Table 5.2 with the sample-size and near-independence grids. State the shared margin regimes and equal sample sizes beside the table.
- Display the component sampling-moment target and show explicitly which mean-to-target ratio is being interpreted.
- Add fitted null standard deviations to the three focus settings in Table 5.3. Define the standard deviation before the table.
- Display the focused power construction: the fixed lower MI, nine separation values and resulting signed difference.
- Add Table 5.4 showing the fixed alternative and its lower and upper equal-MI calibration populations. Preserve independent fitting and validation, common alternative samples and cross-null checks.
- List the three sampling roles, giving the common batch size once.
- Add Table 5.5 with rejection rate, valid-result fraction, MI-difference bias, variance ratio and rejection direction. Explain inclusion rules and interpretation beside the table.
- Remove prose that merely repeats these displays. Preserve interval definitions, uncertainty from paired comparisons and cutoff fitting, pointwise interpretation and the practical tolerance.

Table 5.1 remains the margin table. Chapter 5 now contains five tables, up from two. Normal text size and existing page dimensions are preserved. The manuscript is 97 pages, one page longer than the pre-edit version; main text is 59 pages.

## Scientific checks

Parameter grids and power/calibration constructions were checked against Appendix B. The six-decimal focus standard deviations agree with the existing generated reference-fitting table: 0.154967, 0.065138 and 0.003175. The new moment-target display restates Appendix B.7. Original displayed equations and the margin table remain unchanged, apart from equation numbering after the added display. The original citation sequence is retained.

An input-hash comparison confirms that only Chapter 5 and the thesis README changed among the snapshotted manuscript/source/figure inputs. No estimators, experiment code, sampled results or plots changed; no experiments were rerun.

## Validation

- All five existing manuscript-consistency tests passed.
- The final manuscript builds without LaTeX warnings, overfull boxes, underfull boxes or undefined references.
- Rendered physical pages 4–8 and 42–50 were inspected for contents/list entries, table widths, equation readability, page flow and the transition to Chapter 6. The sampling list continues on the following page; all three numbered items stay together. The final interval paragraph stays together.
- Full delivery packaging and checksum/inventory verification passed. An independent build of the extracted source archive passed without warnings and produced identical PDF text. The root verification file records these checks.

Root README and compatibility README page counts were updated. The thesis README records this pass separately from the earlier Section 5.1 rewrite. No Git commit was requested.
