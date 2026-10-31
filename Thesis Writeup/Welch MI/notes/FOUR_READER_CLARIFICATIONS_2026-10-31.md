# Four reader clarifications

Implemented on 31 October 2026 following the user's approval of four
focused changes. The immediately preceding sources, including the pending
local definition of h, are preserved in
`archive/before_four_reader_clarifications_2026-10-31.zip`.

## Changes

1. **Variance terminology.** Definitions, transitions, contribution
   statements and relevant headings identify V(P) and its estimate as
   pointwise-MI variances. The Introduction explains the cell-level
   variation and the division by sample size before discussing the
   sampling variability needed for degrees of freedom. Chapter 3 connects
   that distinction to the standard error; Chapter 6 names the variance
   being predicted and uses “squared standard error” where that is the
   actual quantity. Ordinary Welch and Bayesian variance terminology is
   retained. The consolidated writing guide now records the vocabulary.
2. **Holm transparency.** New Section B.9 contains the six existing
   unadjusted application p-values for both tests, a concise definition
   of the Adult and Student Performance comparisons, and the Holm
   calculation. Section 6.4 points to the table. The additional four
   comparisons receive no new interpretation or analysis.
3. **Conditional false-positive interpretation.** Table 6.1's existing
   layout and values are retained. Its interpretation now starts with
   29 improvements among 38 settings where Wald over-rejects, including
   the qualification that four reductions overshoot. The following
   sentence explains why lowering an already conservative rate cannot
   improve calibration.
4. **Equal-sample scope.** Chapter 5 states that the leading bias
   corrections cancel from the difference in the reported simulations,
   while residual biases can differ between distinct populations.
   Chapter 7 identifies unequal-sample correction performance as outside
   the reported evaluation, retaining the residual-bias qualification.

## Verification

- Every pre-existing figure, table and mathematical display is
  byte-identical to the preceding source. The six-row application table
  is the only added display. Existing inline mathematical expressions,
  labels, citations and references are retained.
- Section 2.3 remains byte-identical. The Figure 6.1 interpretation and
  the pending local definition of h are preserved.
- All twelve p-values in the added table agree with the saved six-case
  application results at the displayed precision. Independent Holm
  calculations from the unrounded values reproduce both methods' saved
  adjusted results, including the reported month conclusions.
- Data-preparation rules confirm the Adult group/outcome definitions and
  the Portuguese-course grade threshold and school groups. The existing
  application tests independently reproduce the full-data calculations
  and six-comparison Holm adjustment.
- Existing saved-result macros supply the 29, 38 and four counts in the
  revised interpretation. No rate, tolerance, test rule or experiment
  setting changed.
- Protected source, figure/data, typography, PDF and delivery files are
  unchanged. All five existing thesis-consistency tests and eleven
  application tests pass, together with source reference/structure,
  paragraph-style and whitespace checks.

Detailed results are recorded in
`FOUR_READER_CLARIFICATIONS_VERIFICATION_2026-10-31.json`.
At the source-edit stage no PDF rebuild or delivery publication was performed.
The user subsequently requested the rebuild on 31 October 2026. The resulting
109-page PDF passes compilation, reference and paragraph-style checks without
LaTeX warnings. Twenty-two affected or boundary pages were rendered and visually
reviewed, including the new application-family table and h definition. No source
or formatting change was needed during the rebuild. Main, build and named PDFs
are identical; the refreshed 95-file source archive is verified. The unchanged
25,010-file supplement and its checksum were reused after inventory, size and
exact timestamp checks. The preceding PDF and delivery metadata are preserved
in `archive/before_four_reader_clarifications_build_2026-10-31.zip`.
No Git commit was performed.
