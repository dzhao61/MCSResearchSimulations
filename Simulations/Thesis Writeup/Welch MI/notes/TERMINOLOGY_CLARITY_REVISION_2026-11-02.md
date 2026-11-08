# Terminology clarity revision — 2 November 2026

The user approved the preceding terminology review and requested careful
implementation followed by a contextual reread. The terminology pass initially
updated the source only. The user subsequently requested the rebuild recorded
below.

## Changes

- Replaced compressed descriptions of bias and sampling variance with phrases
  naming the estimated MI difference. Where identical population tables make
  bias cancel, the explanation now identifies the two MI estimates whose
  biases cancel.
- Expanded the references to rates and power calculated over all simulation
  repetitions, retaining the treatment of failed calculations as non-rejections.
- Replaced complete component validity with the requirement for positive,
  finite component degrees of freedom in every repetition. The discussion of
  complete test validity now states that both tests return usable results in
  every repetition, preserving the distinction from accurate inference.
- Spelled out standard deviation in prose. Retained SD in the compact
  diagnostic table heading and in the quoted heading explained beside it.
- Replaced fixed-support bias and aligned fixed alphabets with descriptions
  of the fixed row and column categories. The adjacent description of estimating
  support now names population cells with positive probability.
- Replaced declared alphabet dimensions, common-MI-0.02 settings, MI sweep,
  method gap, detection cost, included fraction and expanded p-value with
  phrases identifying the categories, experiment settings, power comparison,
  retained repetitions or Expanded Welch p-value.

The edited sources are Chapters 1, 3, 4, 5, 6 and 7 and Appendix B. The
abstract, acknowledgements, Chapter 2 (including the Section 2.3 derivation
benchmark), Appendix A, figures, bibliography and typography are unchanged
from the start of this pass. Established technical terms and the distinction
between the moment target, population approximation and sample-based estimate
are retained.

## Review and verification

Every affected paragraph was reread in continuous form after the replacements,
and its meaning was compared with the original. Local sentence wording was
adjusted where a literal expansion sounded awkward. The numerical findings,
conditions and calculation rules remain unchanged.

- All 796 inline mathematical expressions and displayed equation blocks in
  the seven edited files are unchanged, ignoring whitespace.
- Numeric tokens, references, citations, LaTeX environments and formatting
  commands match the before-text.
- All 164 reference occurrences resolve against 137 unique labels across
  the 18 active TeX inputs; all 46 cited keys resolve.
- None of the approved compressed phrases remain in the active manuscript.
  Both remaining SD occurrences refer to the diagnostic table heading.
- The paragraph-style check and `git diff --check` pass.
- The other 115 recorded manuscript files match the baseline byte for byte.
  All ten recorded delivery files retain their sizes and exact modification
  times. The existing PDF and delivery archives have not been refreshed.

The baseline, before-text and machine-readable preservation checks for this
pass are recorded under
`/private/tmp/welch-terminology-2026-11-02-7xqdduul/`.

## Requested PDF rebuild

The main and named delivery PDFs and source archive were refreshed. The
experimental supplement was reused after its input inventory, file sizes and
exact modification times were checked against the verified baseline; native
delivery checks passed.

The first build put the introduction to Figure 6.3 on a mostly empty page
before its plot. One sentence at the end of Section 6.1.2 was tightened while
retaining the explicit positive, finite degrees-of-freedom requirement in every
repetition and naming P as the comparison population. This preserved the
meaning and all formulas, with no change to figure dimensions, placement or
spacing. The final build restores the introduction beside the plot and remains
104 pages.

The final compilation log is clean, all 905 internal page links have valid
destinations, and no extracted text extends beyond the page bounds. The 23
pages with changed content and 11 surrounding pages were rendered and visually
inspected, including both tables with expanded wording. No clipping, overlap
or broken table layout was found. Protected presentation and historical draft
PDFs remain unchanged. The named delivery PDF matches `main.pdf` byte for byte.

Build checks, before/after PDFs and rendered review pages are under
`/private/tmp/welch-terminology-rebuild-2026-11-02/`.
