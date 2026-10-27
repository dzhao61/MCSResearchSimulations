# PDF rebuild and formatting review, 27 October 2026

The user explicitly requested rebuilding the PDF with formatting checks.
This build incorporates the accumulated source-only revisions. Future
rebuilds still wait for an explicit request.

The previous PDF and pre-formatting sources are preserved in
`archive/before_deliverable_rebuild_2026-10-27.zip`.

## Result

The main thesis is 97 pages, compared with the previous 103-page delivery.
It has nine front-matter pages and 88 numbered pages. Main text occupies
printed pages 1--64; Chapter 6 is 44--60. Appendix A is 65--69, B is 70--78
and C is 79--83, followed by the bibliography on 84--88.

The new seven-page fixed-reference supplement and four-page supporting-
calculations supplement are also compiled and reviewed. Their PDFs are
included in the experiment-supplement inventory.

## Formatting corrections

- Global paragraph indentation remains zero, with 0.25em paragraph spacing.
- Section 6.1.2 is titled How moment errors affect degrees of freedom. It
  now fits cleanly in the contents and in the body without splitting a word.
  The shorter heading also allows Figure 6.2 beside its introducing text;
  no figure size or font was reduced to save space.
- Appendix B.5 is titled Bias, variance and degrees of freedom, avoiding
  a broken word in its heading.
- Appendix C.1 uses fitted null SDs in its heading, avoiding another
  crowded title; SD is already defined in the manuscript.
- The A power walkthrough in Section 6.3.2 is kept together.
- The application notation table includes H0 after X/Y/P/Q, keeping the
  equal-MI hypothesis with its definitions instead of on a separate page.
- The supplementary parameter table uses ragged-right cells, removing
  underfull-box warnings without shrinking text.

No scientific results, numerical table cells, estimator code or saved
experiment outputs change during this formatting review.

## Review and verification

All main-manuscript pages and both new supplement documents were rendered
for visual review. Contents, lists, the abstract, Chapter 4's moved proof,
Chapter 6 figures/tables and revised sections, Conclusions, appendices and
bibliography were checked for clipping, awkward headings, inconsistent
indentation, broken references and legibility. Recent changes were also
inspected at full-page size. Final TeX logs have no warnings, overfull or
underfull boxes, or undefined references.

The source paragraph-style guard passes. Eleven packaging tests, six
application regression checks and five manuscript-consistency checks pass.
All fonts in the main PDF are checked for embedding. Delivery verification passes. An independent build from the extracted
source archive also passes without warnings and produces identical PDF text
to the delivery manuscript. All 41 fonts are embedded. Outcomes and final
checksums are recorded in REDESIGN_VERIFICATION.json.
