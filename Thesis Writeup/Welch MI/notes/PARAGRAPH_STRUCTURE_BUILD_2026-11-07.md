# Paragraph structure revision and PDF build, 7 November 2026

The user authorised the three small Chapter 6 paragraph changes identified
in the paragraph-structure review and requested a main thesis PDF rebuild.
This build also incorporates the earlier approved source-only revisions
recorded in `APPENDIX_CLARITY_REVISION_2026-11-07.md` and
`MAIN_TEXT_CLARITY_REVISION_2026-11-07.md`.

## Three paragraph changes

1. Section 6.1.3's final paragraph now opens with its finding: the population
   first-order and average sample-based variance predictions err in opposite
   directions at the smallest MI values. The existing prediction definitions,
   repeated-sample comparison, numerical evidence and qualifications remain.
2. Section 6.2.3 separates the comparison across MI levels at fixed sample
   size from the subsequent change with sample size. The new paragraph
   begins with diminishing bias and rejection as sample size increases.
   Its final sentence retains the possibility that an oversized standard
   error suppresses rejection after bias has diminished, without repeating
   the new opening's sample-size condition.
3. Section 6.5's second paragraph now identifies both effects of variance
   estimation: the degrees of freedom and the size of the test statistic.
   Its first example connects replacing the larger sampling mean of V-hat
   with V to the population first-order degrees of freedom falling below
   the moment target. The existing standard-error diagnostic, rejection
   interpretation and literature comparison follow.

These are local changes to emphasis and paragraph progression. They add no
new experiment, statistical claim or derivation. The surrounding passages
were reread against the thesis writing guide and the earlier review of the
three sample theses. Longer derivation and results paragraphs that retain
one explanatory purpose were preserved.

## Build and layout review

- Built and packaged with `package_deliverables.py --no-push` before visual
  review. The PDF has 110 physical pages, previously 109. Chapters 1--7
  retain their previous page spans; Appendix A gains one page from the
  earlier approved explanation. Appendix B and the bibliography begin one
  page later and retain their lengths.
- Inspected 37 affected and nearby PDF pages, including the earlier clarity
  revisions, the three paragraph changes, the application tables, the
  conclusion, the expanded appendix calculations and the final bibliography
  pages.
- The first build split the two-line MI and pointwise-variance definition
  in Appendix A.3 across pages. Changed its internal line break to `\\*`
  so both lines stay together, rebuilt, and inspected the four pages whose
  text reflowed. No equation, label, wording, font size, margin or figure
  dimension changed for this layout correction.

## Verification

- All five existing thesis-consistency tests pass after the final change.
- The three Chapter 6 paragraph changes preserve every displayed equation,
  numerical token, reference, citation, heading and environment from the
  source snapshot immediately before this pass.
- All 181 source references resolve in the compiled document. Paragraph
  style, contextual Australian English review and whitespace checks pass.
- The final LaTeX log contains no warnings, overfull or underfull boxes,
  missing-character messages or unresolved references.
- The build PDF, main PDF and named delivery PDF have identical SHA-256
  hashes. Every source archive entry matches the current source, and the
  published delivery checksums match the files. Packaging verified and
  reused the unchanged experiment supplement.
- Of 638 preservation inputs captured before this pass, 632 are unchanged.
  The six changed inputs are Chapter 6, the single Appendix A layout
  control, the main PDF, the delivery PDF, the source archive and the
  checksum list. The prior approved source edits and their notes, other
  chapters, abstract, derivation benchmark, figures, bibliography, code,
  historical drafts and separate personal study guide are preserved.

The verified files and all three revision notes are included in the scoped
build commit and push. The unrelated `output/` study-guide folder is excluded.
