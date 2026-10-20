# Sentence Review Batch

Status: all approved sentence-review edits 1-21 are included in the current
main PDF and delivery files. No approved edits in this batch remain pending.
Edits 1-14 were rebuilt on 18 October 2026; edits 15-16 were included in
the user-authorised 19 October rebuild alongside the matched same-skew
extension. Edits 17-21 were included in the subsequent user-requested
19 October clarity rebuild. The current main PDF and delivery files have
112 pages. Further sentence edits can continue source-only until the next
requested rebuild.
No historical working-draft source or PDF was changed.

## Applied And Rebuilt

1. Introduction: move the population definitions, hypotheses and accompanying
   explanation before the paragraph beginning "In practice, MI is estimated
   from observed data." Wording, equation and label unchanged. Approved and
   applied and rebuilt.
2. Introduction: replace the paragraph following the hypotheses with the
   user's explanation that equal MI does not require identical joint
   probability tables. Correct the spelling of "probability". Approved and
   applied and rebuilt.
3. Introduction, empirical contribution: replace the opening sentence with
   the approved description naming sample size, table size, category
   frequencies and population MI. Keep the remaining sentences unchanged.
   Approved, applied and rebuilt.
4. Introduction, empirical contribution: use "Supporting diagnostics assess"
   and "Additional supplementary checks look at further population
   constructions and sample allocation" as requested. Approved and applied;
   Included in the rebuilt PDF.
5. Introduction, practical contribution: replace the detailed results preview
   with the approved sentence about false-positive rates relative to the 5%
   level and estimation errors that make both tests unreliable. Approved and
   applied and rebuilt.
6. Introduction, scope and organisation: add topic sentences explicitly
   naming scope and organisation, and separate the data setup and sampling
   assumptions into clearer sentences. Preserve the derivation assumptions,
   zero-MI case, test settings and chapter references. Applied as requested;
   Included in the rebuilt PDF.
7. Introduction, organisation: introduce the online-shopping dataset as a
   real-world example illustrating both tests in its own sentence, separate
   from the description of the experimental results. Applied as requested;
   Included in the rebuilt PDF.
8. Background, Welch--Satterthwaite principle: add the approved opening
   explaining that the thesis adapts the mean-comparison principle to MI
   comparisons. Retain the citation, equations and subsequent explanation.
   Approved, applied and rebuilt.
9. Background, Welch--Satterthwaite principle: introduce the Student t
   distribution and its degrees of freedom before the equations, using the
   approved sentence about the standardised difference between sample means.
   Make the sample means and sample variances explicit, remove the later
   repeated introduction and retain the cutoff comparison and equations.
   Approved, applied and rebuilt.
10. Background, previous work and contribution: replace the paragraph about
    two successive sources of uncertainty with the approved direct statement
    of the MI variance calculation and its use in Expanded Welch. Keep the
    surrounding literature discussion unchanged. Approved and applied;
    Included in the rebuilt PDF.
11. Background, Welch--Satterthwaite principle: add a compact density plot
    comparing the standard normal distribution with Student t distributions
    with 3, 10 and 30 degrees of freedom. Place it before the MI-specific
    discussion, with a short caption and adjacent explanation of heavier
    tails, rejection cutoffs and convergence to the standard normal
    distribution. Figure generated and visually inspected; density values,
    tail behaviour, label bounds and cross-reference checked. Included in
    the rebuilt thesis and source archive; historical drafts unchanged.
12. Expanded Welch, choosing degrees of freedom: use the approved first
    sentence naming Normal Wald and Expanded Welch and linking their standard
    error to Chapter 3. Change "The new quantities are" to "The new variables
    being introduced are" and retain the final sentence. Approved and applied;
    Included in the rebuilt PDF.
13. Experimental design, opening paragraph: replace "when MI differs" with
    "when MI differs between the two populations" as requested. Applied;
    Included in the rebuilt PDF.
14. Experimental design: give each main study a paragraph explaining its
    comparison and purpose in Section 5.1. Consolidate table-size and
    category-frequency explanations in Section 5.2 and clarify equal-MI
    wording in the overview table and Section 5.3. Move the Morris citation
    to the chapter introduction. Preserve headings, numbering, parameter
    grids and supporting-check subsections. Approved and applied;
    Included in the rebuilt PDF.

## Applied In The 19 October Rebuild

15. Experimental design, Section 5.1: add the approved paragraph explaining
    the construction and sample-allocation checks before Table 5.1. State
    what changes and what stays fixed, and move the table-introduction
    sentence after the new explanation. Detailed procedures and parameter
    settings unchanged. Approved, applied and rebuilt.
16. Experimental design, Section 5.2: add the approved sentence beside the
    copying equation identifying it as a special case of Bocci, Carlini and
    Rapallo (2010), and add the bibliography entry. This attributes only the
    probability formula, not the target-MI search or the experimental design.
    Definition 3.4 in the author manuscript gives the exact match when
    alpha = 1 - lambda, r = c = a and D = diag(a):
    https://arxiv.org/pdf/0908.0232 . Publication metadata verified through
    DOI content negotiation at https://doi.org/10.1090/conm/516/10166 ;
    publisher-deposited Crossref metadata gives pages 61-73 (not 61-74).
    Approved, applied and rebuilt.

## Applied In The 19 October Clarity Rebuild

17. Experimental design, Sections 5.3.4 and 5.3.5: organise each into three
    paragraphs covering purpose, procedure and settings. State the question
    before the technical setup. Remove the results preview and vague
    "representative findings" wording. Retain the four-cell transfer,
    citation, matched controls, all parameter settings, outcome measures and
    reuse counts. Binary equivalence and unequal-sample correction details
    are already explained in Appendix B, so no new appendix material is
    needed. Experiments, headings, labels, grids and results are unchanged.
    Initially applied source-only; included in the requested clarity rebuild.
    All 15 targeted same-skew tests passed at the source-review stage.
18. Experimental design, Section 5.4: clarify that each repetition draws
    one count table from P and another independently from Q, then applies
    both tests to those same two tables. Remove the sentence referring back
    to the Chapter 3 and Chapter 4 calculations. Retain 20,000 independent
    multinomial pairs per setting and the fixed populations. Approved,
    applied and included in the clarity rebuild.
19. Experimental design, Section 5.4: replace the simulation-uncertainty
    paragraph with the approved explanation of confidence intervals, the
    approximate 4.7%-5.3% interval for an estimated 5% rate from 20,000
    repetitions, and comparisons using both tests' decisions on the same
    simulated pairs. Retain the Wilson citation and Appendix B.6 reference.
    Remove the main-text Monte Carlo standard error and paired-indicator
    terminology; calculation details remain in Appendix B.6. Included in
    the clarity rebuild.

20. Experimental design, Section 5.4: replace "Diagnostics of the shared
    estimates" with "Accuracy of the MI difference and standard error".
    Explain bias, standard-error accuracy and the population variance
    approximation in separate paragraphs. State how the variance ratio is
    calculated and what values above, below or equal to one mean. Give
    degrees of freedom and computational cost their own unnumbered headings.
    Retain degree-of-freedom summaries across all five comparisons and all
    timing settings. Detailed inclusion rules, percentile interpretation
    and empty-cell measures already appear in Appendix B; add a label to
    its existing diagnostics section for a precise reference. No experiment,
    equation, result or calculation rule changes. Included in the clarity
    rebuild.

21. Results, Chapter 6: apply the approved independent clarity review.
    Distinguish the sampling variance of the MI difference from the
    variability of the estimated MI variance used in Expanded Welch's
    degrees of freedom, with separate unnumbered headings. Explain which
    effects come from the estimates used by both tests and which come from
    Expanded Welch's Student t distribution. State the signed MI difference
    before interpreting the falling power curve, replace ambiguous shorthand
    with named quantities, and group the construction, sample-allocation and
    jackknife checks after the main power comparisons. Consolidate repeated
    validity statements and simplify the application explanation. Preserve
    the numbered headings, labels, displayed equations, figure blocks,
    table blocks and citation keys exactly. Numerical claims checked against
    the saved evidence; no results or experimental settings changed. All
    207 Welch pipeline tests and 6 application tests pass. Included in the
    clarity rebuild. During layout verification, keep Equations 6.2-6.3 and
    their introductory sentence together; mathematical content and equation
    numbers are unchanged.

## Verification Of The 18 October Rebuild

- Both the active manuscript and a fresh extraction of the source archive
  compile without LaTeX warnings or unresolved references; their extracted
  PDF text matches exactly.
- Visually inspected the affected introduction, background, degrees-of-freedom
  and experimental-design pages, plus contents and figure/table lists.
- All 46 cited reference keys resolve. Chapter 5 headings, labels, equations
  and parameter grids are unchanged; all text from the power-study subsection
  onward is unchanged in that source chapter.
- Results, discussion, conclusion, appendices and bibliography have identical
  extracted text to the previous PDF apart from page numbering.
- All 8 packaging tests pass, and the delivery consistency check passes.
- Historical working-draft source and PDF hashes match their pre-build values.
- Build logs and temporary checks are under
  `/private/tmp/welch-review-batch-20261018-tevxcf/`.

## Verification Of The 19 October Rebuild

- The separate same-skew extension plan records the approved experimental
  scope and its results. All original settings and scientific methods remain
  unchanged; the additions give 312 settings and 104 population pairs.
- The main manuscript and a fresh extraction of its source archive compile
  without final LaTeX warnings or unresolved references. Their extracted
  text matches exactly. All 47 cited keys resolve, including Bocci et al.
- The affected design, results, discussion, conclusion, appendix, contents
  and list pages were rendered and visually inspected. New plots and tables
  fit within the margins. The current PDF has 112 pages: three additional
  main-text pages and six additional appendix pages versus the prior PDF.
- All 251 scientific/application tests and 8 packaging tests pass. The new
  and original results pass the independent audits, and current delivery
  PDF, source archive, experiment supplement and checksums agree.
- Historical working-draft hashes remain unchanged. The previous main PDF
  and source archive are retained in
  `archive/before_same_skew_extension_2026-10-19/`.
- QA logs and rendered pages are under `/private/tmp/welch-same-skew-*`.

## Verification Of The 19 October Clarity Rebuild

- Rebuilt the main manuscript with approved edits 17-21 and refreshed the
  delivery PDF, source archive, experiment supplement and checksums.
- The main build and a fresh extraction of the final source archive compile
  without LaTeX warnings or unresolved references. Their extracted PDF text
  matches exactly. All 47 cited keys have bibliography entries.
- Visually inspected PDF pages 45-65 (printed pages 37-57), including the
  revised experimental-design and results pages, equations, figures, tables
  and transition into Chapter 7. Also inspected the contents and figure/table
  lists. Kept the two-line bias calculation with its introductory sentence
  after the first render revealed an awkward page split.
- The thesis remains 112 pages. Compared with the previous delivery, text
  changes are confined to the approved Chapter 5 and Chapter 6 revisions and
  the updated page number for Figure 6.5 in the figure list. Other chapters,
  appendices, bibliography and scientific results are unchanged.
- All 207 Welch pipeline tests, 6 application tests and 8 packaging tests
  pass. The final delivery consistency check passes.
- All historical working-draft source and PDF hashes match their pre-build
  values. No historical draft was rebuilt or replaced.
- Build logs, clean-source extraction and rendered-page checks are under
  `/private/tmp/welch-rebuild-20261019-Xs9pO7/`.
