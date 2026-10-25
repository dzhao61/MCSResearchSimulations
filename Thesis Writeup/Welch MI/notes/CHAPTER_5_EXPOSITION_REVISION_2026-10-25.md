# Chapter 5 exposition revision — 25 October 2026

## Scope and preservation

The reader requested that the rest of Chapter 5 follow the explanatory approach of the improved Section 5.1: establish the question, explain the mechanism, introduce notation when needed, show the calculation, and then generalise to the experiment settings.

Only Sections 5.2–5.5 have been rewritten. The chapter introduction and Section 5.1 remain byte-identical to the preceding version. The main comparison remains Expanded Welch versus Normal Wald, with the fixed moment reference as a supporting diagnostic. The removed sample-size comparator stays in the supplement.

The preceding 97-page manuscript and its active sources and assets are preserved in `archive/before_chapter5_exposition_revision_2026-10-25.zip`.

## Changes

- Section 5.2 starts with repeated count tables from one fixed population and sample size. It distinguishes the pointwise-MI variance being estimated from the sampling variance of that estimate. The sensitivity variance is introduced before its equation, and the observed benchmarks are explained before the parameter grids.
- The component sampling-moment target is connected to the mean and sampling variance measured across repetitions. Population first-order predictions and sample-estimated degrees of freedom are compared separately with that target. Conditional summaries identify the included fraction.
- Section 5.3 defines false-positive measurement before explaining the two tests' different cutoffs. The fixed moment diagnostic now displays its combined-denominator target and explains independent fitting and holding the fitted degrees of freedom fixed.
- Section 5.4 introduces power before the focused settings. It explains the null SD scale and gives a concrete setting C alternative: two fitted null SDs are about 0.00635 nats, giving I(P) = 0.02, I(Q) about 0.02635 and a signed difference about -0.00635 nats.
- Nominal power, empirical cutoff fitting and sensitivity to the calibration population are introduced in sequence. A three-step list distinguishes fitting, fixing the thresholds and independent evaluation. Lower- and upper-null definitions are kept together in a separate paragraph beside their table.
- The same baseline fitting batch supplies the null SD, fixed moment reference and curve's calibrated cutoffs. This agrees with the recorded fitting procedure; no additional batch is implied.
- Broader MI differences, association construction and sample allocation are listed as three distinct supporting comparisons, with their existing settings preserved.
- Section 5.5 explains why P and Q draws are independent while the methods' outcomes are paired. It explains variance ratios, estimated direction and the separate sources of interval uncertainty.

The five existing tables and every original displayed equation are retained unchanged. One combined-reference equation restates Appendix B.7. The chapter and section order, figure dimensions, typography and page dimensions are unchanged. The revised remainder has 1,704 whitespace-delimited source words versus 1,240 previously, including the unchanged table/equation source. The thesis is 98 pages, one page longer; its main text is 60 pages.

## Verification

- All five manuscript-consistency tests and eight packaging tests pass.
- The pre-edit source comparison confirms that the chapter introduction and all of Section 5.1 are unchanged. All original displayed equations, table blocks and citation order are preserved.
- The new combined-reference formula agrees with Appendix B.7. The worked alternative agrees with the saved setting C null SD. The source of the SD, moment reference and cutoffs was checked against the unchanged fitting code.
- No other manuscript chapter, appendix, figure, bibliography, estimator, experiment script or result was edited. No simulations or bootstrap calculations were rerun.
- The main build has no LaTeX warnings, undefined references or overfull/underfull boxes.
- Physical pages 4–8 and 45–51 were rendered and visually reviewed. Tables and equations remain legible and within the text margins; the final interval paragraph fits on the last design page. The transition to Chapter 6 and contents/table/figure lists were checked.

Full packaging and checksum/inventory checks pass. The extracted source archive builds independently without warnings and produces identical PDF text. These completed checks are recorded in the root verification file. No Git commit was requested.
