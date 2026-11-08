# High-impact thesis improvement plan

30 October 2026 · Implemented, rebuilt and reviewed

Implementation and verification are recorded in [HIGH_IMPACT_REVISION_2026-10-30.md](HIGH_IMPACT_REVISION_2026-10-30.md). The original plan follows.

**Planning update, 31 October 2026.** The later prose work is consolidated in
[Research prose writing guidelines](RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md),
including a summary of the Chapters 5–7 revisions. The earlier-chapter pass is
specified in [Chapters 1–4 prose revision plan](CHAPTERS_1_4_PROSE_REVISION_PLAN_2026-10-31.md).
The guide now includes concrete before/after examples, paragraph and
display-placement lessons, and decisions about when to join, split, move,
delete or retain text. The plan prioritises Chapter 2 outside Section 2.3,
keeps Chapter 1 light, and protects the mathematical steps in Chapters 3–4.
The user subsequently authorised the Chapters 1–4 pass, which is now
implemented in the source with all literature coverage retained. See
[the revision record](CHAPTERS_1_4_PROSE_REVISION_2026-10-31.md) for the
changes and preservation checks. The requested rebuild now includes the
revisions and new abstract in the 107-page PDF. The completed
30 October plan below is retained as historical context; its appendix,
table and research-question references describe that earlier manuscript.

This plan selects three changes from the marking-rubric review, the comparison with all three sample theses, and the first-reader assessment of language and reading flow. Each addresses a specific difficulty in assessing the existing work and can be implemented using evidence already in the thesis.

The principal opportunity is to make the mathematical contribution and the empirical judgment easier to follow. The derivations, diagnostic experiments and qualifications are substantial strengths. The sample theses provide useful models for connecting a question to its evidence and conclusion; they do not justify adding experiments simply to make this thesis broader. Their exact marks and examiners' reports were unavailable, so they are qualitative references rather than numerical marking benchmarks.

The plan is deliberately limited to the following three packages. It does not require a new method, new experiments, a change of hypotheses or a reduction in derivation depth.

| Priority | Change | Main location | Relevant marking criteria |
| --- | --- | --- | --- |
| 1 | Finish interpreting each body of evidence before changing the comparison | Chapter 6, especially Sections 6.1.2 and 6.2.2 | Exposition and interpretation of findings; literary quality and presentation |
| 2 | Show the decisive calibration-validation evidence beside the calibrated-power conclusion | Section 6.3.2, supported by Appendix C | Measurable evaluation; critical interpretation; conclusions supported by findings |
| 3 | Give a direct, integrated judgment of what the proposed method contributes | Chapter 7, checked against the abstract and introduction | Original contribution; reflection; conclusions linked to the research questions and evidence |

## 1. Remove the main reading loops in Chapter 6

**Problem demonstrated in the current manuscript.** The chapter has explicit cross-references, but some discussions require the reader to leave a display, decode another comparison and then return to the earlier display. This creates avoidable memory demands even when individual sentences are clear. The highest-value changes are local changes to the order of existing material.

### Section 6.1.2: finish Figure 6.2 before developing Table 6.1

The current sequence explains the top row of Figure 6.2, introduces the numerical example and Table 6.1, defines the table's columns after the table, and then says “Returning to the bottom row of Figure 6.2.” The reader must retain the unfinished figure comparison while learning several table labels.

Reorder this passage so that it:

1. Introduces Figure 6.2 and identifies the two ratios and their common moment target.
2. Explains the population first-order comparison in the top row.
3. Explains the sample-based comparison in the bottom row, including the meaning of missing points and the effect of averaging a nonlinear ratio.
4. Introduces Table 6.1 with the existing concise column definitions before the table.
5. Uses the numerical example to connect the mean and sampling-variance errors to the degrees of freedom: at the specified 4 × 4, n = 1,000 setting, the first-order value for P is 15.30 compared with a moment target of 21.03.

The table then supplies a numerical explanation of a figure the reader has already understood. Preserve the distinct roles of the sampling-moment target, the population first-order value and the sample-based estimate. A target calculated from sampling moments must remain distinguishable from the estimated degrees of freedom used by the actual test.

### Section 6.2.2: complete the selected-setting diagnosis before moving to other checks

Tables 6.3 and 6.4 introduce estimation diagnostics and null rejection rates for selected settings. Their interpretation is interrupted by a return to the uniform-margin curves and a stronger-common-MI comparison, after which the text returns to the sparse rows of the earlier tables.

Group the existing explanations of A, B, C and the sparse same-skew/different-skew cases with Tables 6.3 and 6.4. Finish the comparison of difference bias, squared-standard-error accuracy and rejection before moving to the uniform-curve mechanism and the stronger-common-MI check. Keep each explanation close to the evidence that supports it, while allowing the two complementary tables to be read together.

The explanations of the uniform-table trough and numerator–standard-error dependence are scientifically useful. Their location should support the progression of the argument; they should not be removed as tangents. The stronger-common-MI comparison should then develop the separate question of whether the improvement at common MI 0.02 persists as the common MI changes.

### Preserve the distinctions that make the mathematics readable

These edits must preserve the names of the quantities being compared. Chapter 6 moves between the mean of the estimated MI variance, the sampling variance of that estimate, and the sampling variance of the estimated MI difference. Those are different statistical objects. In the relocated paragraphs, name the relevant quantity whenever a shortened reference such as “the variance” could reasonably refer to more than one of them.

The opening of Section 6.2.2 already explains this distinction well. Retain it. The 28 October improvements to Sections 6.1.3 and 6.3.2 also already group their figure explanations more coherently; preserve that progress. This package is a targeted repair of the remaining loops, not another chapter-wide rewrite.

**Acceptance checks**

- A reader can finish both rows of Figure 6.2 before starting the detailed table comparison.
- Table 6.1's column meanings are available before its first detailed reading.
- The selected-setting diagnoses in Section 6.2.2 form a complete comparison before the text changes to the other checks.
- Every moved explanation retains its evidence, qualifications and relevant reference. No causal claim becomes stronger through removal of context.
- Numerical values, equations, figure assets, statistical definitions and scientific conclusions are preserved.

## 2. Put calibration validation beside the power interpretation

**Problem demonstrated in the current manuscript.** Section 6.3.2 already shows that the apparent calibrated-power advantage can reverse when the fitting null changes. It also correctly states that matching rejection at one equal-MI setting does not ensure matching elsewhere. However, the numerical evidence showing the size of that failure remains in Appendix C. A central qualification of the power comparison therefore depends on an appendix lookup.

After interpreting Table 6.6, add one compact, quantitative example from the existing independent null-validation results. Use setting A at two null SDs, because it connects directly to the reported change from a 3.58-percentage-point power gain under lower-null calibration to a 0.76-point loss under upper-null calibration.

The existing cross-null table gives the following rates:

| Fitting null | Evaluation null | Normal Wald rejection | Expanded Welch rejection |
| --- | --- | --- | --- |
| Lower | Lower | 4.93% | 4.99% |
| Lower | Upper | 11.20% | 13.71% |
| Upper | Upper | 4.87% | 4.84% |
| Upper | Lower | 1.63% | 0.79% |

Use these values in a short paragraph or compact display, whichever fits the surrounding discussion more clearly. Keep the full cross-null table in Appendix C. Explain that the alternative samples are held fixed while the fitted thresholds change, and that approximately equal false-positive rates at the fitting null can become substantially different rates at another equal-MI null.

This makes the inferential consequence concrete: a power comparison matched at one specified null is conditional on that calibration choice. It does not establish a stable advantage across the complete equal-MI null. The evidence also shows why changing the fitting null can materially alter the comparison. Avoid implying that these two validation settings exhaust the composite null or provide a calibration procedure for unknown application populations.

**Acceptance checks**

- The reader can understand the scale and meaning of calibration sensitivity from the main discussion alone.
- Every quoted rate agrees with `focused_redesign_sensitivity_cross_null.tex`; the power contrasts agree with Table 6.6.
- Fitting null, evaluation null and fixed alternative remain explicitly distinguishable.
- The text connects the validation rates to the interpretation of power without claiming that they prove a unique cause of every power difference.
- The addition replaces any overlapping general explanation so that it strengthens the evidence rather than adding repeated caveats.

## 3. End with an integrated assessment of the contribution

**Problem demonstrated in the current manuscript.** The introduction and conclusion already identify the contribution and report the limitations accurately. The remaining opportunity is to make the final judgment easier to extract from the detailed RQ-by-RQ recap. An examiner should be able to identify what the derivation achieved, what the evaluation established and what practical judgment follows, without reconstructing that synthesis across several subsections.

Revise the conclusion locally around one explicit assessment linking the following findings:

1. **What the derivation supplies.** The observation-level sensitivity accounts for changes in cell probabilities, margins and pointwise MI. Its variance yields an MI-specific first-order approximation used in the degrees-of-freedom construction. This is a substantive mathematical and methodological contribution even though it does not establish an exact Student t reference distribution.
2. **What the empirical evaluation establishes.** Moment approximation and sample substitution can each affect the resulting degrees of freedom. Near independence, quadratic sampling contributions matter. A false-positive rate close to 5% can also reflect compensation between errors, so good rejection performance at a selected setting does not by itself validate the moment approximation.
3. **What judgment follows for the method.** Expanded Welch improves false-positive rates in selected tested settings, but can increase conservatism elsewhere; its calibrated-power advantage depends on the fitting null; and changing the cutoff leaves bias and standard-error errors in the shared statistic unresolved. The present evidence supports those setting-specific findings rather than a general replacement of Normal Wald.

Develop these as a connected argument. Use the existing results and cross-references, replace overlapping recap, and keep the answers to both research questions identifiable. Where A or B is essential to the concluding argument, give a brief description of the setting rather than relying solely on the letter and a table lookup several chapters earlier.

Then check the abstract and introduction against the revised assessment. They already contain appropriately bounded claims; change them only if needed for consistency. Keep the online-shopping application in its established role: it demonstrates calculation and interpretation on observed data, while the simulations evaluate error rates under known populations. Its unknown population quantities cannot establish which simulated reliability regime applies.

This package adopts the most useful lesson from the three sample theses: make the scientific question, evidence and resulting judgment form a clear progression. It does not require a more favourable result, a stronger novelty claim or an unsupported practitioner decision rule.

**Acceptance checks**

- A reader can state the original contribution and the empirical judgment after reading the conclusion once.
- The assessment answers the stated research questions and cites the findings that justify it.
- Method construction, approximation accuracy and test calibration remain distinct claims.
- The conclusion is decisive about the tested settings and appropriately bounded about untested populations.
- The abstract, contribution list, results and conclusion agree; additional synthesis replaces repetition.

## Implementation order and completion standard

Implement Package 1 first, because it improves the path through the evidence. Implement Package 2 next, then write Package 3 against that clarified discussion. Review each revised passage with its preceding and following paragraphs to check that moving text has not introduced an undefined reference or an interrupted explanation elsewhere.

Preserve Section 2.3 as the derivation benchmark, the substantive intermediate algebra in Chapter 4, all necessary assumptions, citations and reproducibility details. Avoid global terminology replacement, blanket sentence shortening, new notation and figure redesign. None is needed to deliver these three improvements.

Source checks should confirm that labels and references resolve and that every numerical claim retains its supporting evidence. When a PDF rebuild is explicitly requested, inspect the affected pages for the actual order of text and displays, readable table placement and any new layout gaps. Source order alone cannot establish the final reading order of floating tables.

The plan is complete when the three acceptance-check sets are satisfied. Broader simulation families, extra comparator methods, new applications, expanded literature surveys and cosmetic polishing are outside this plan: the current reviews do not establish that their benefit would justify the additional scope and risk. No mark increase is assigned to individual edits; the intended gains are clearer exposition, more accessible evaluation evidence and a better-supported final judgment under the supplied marking criteria.

## Review basis and implementation references

- Current manuscript: `../main.pdf`, especially printed pages 48–50, 57–59, 61–64 and 67–70. Page numbers will change after future builds; section numbers and labels are the primary references.
- Main source: `../chapters_rewrite/06_results.tex` and `../chapters_rewrite/07_conclusions.tex`.
- Calibration evidence: `../figures_rewrite/focused_redesign_calibration_sensitivity.tex`, `../figures_rewrite/focused_redesign_sensitivity_cross_null.tex` and `../appendices_rewrite/C_additional_results.tex`.
- Existing reading-order work: `CHAPTER_6_READING_ORDER_2026-10-28.md`; retain the completed improvements described there.
- Assessment basis: the supplied *18CP Research Pathway Project Marking Rubric V3* and the prior comparison with the Riley Jones, Grace Yan and Michael Fang sample theses. The rubric supplies assessment criteria; the sample documents supply reference examples, not instructions for this project.

The three packages have been implemented and the requested PDF rebuild is complete. The affected pages were inspected, and the PDF, source archive and checksums were refreshed. The existing experiment supplement was reused after checking its input inventory, sizes and modification times.
