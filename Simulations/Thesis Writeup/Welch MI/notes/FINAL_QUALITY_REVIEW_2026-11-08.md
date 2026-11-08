# Final thesis quality review — 8 November 2026

## Scope and change

Reviewed the active manuscript and its current delivery files for correctness,
clarity, consistency, source completeness and PDF presentation. The earlier
derivation and prose reviews remain applicable: all active manuscript sources
were compared with the snapshot taken before this review.

The only manuscript change is a `samepage` group in Chapter 4. It keeps the
definitions of Z, U and the degrees of freedom with Equation (4.2), rather than
leaving the definitions on the preceding page. No wording, mathematics,
reported values, citations, figure sizes or shared typography changed.

The rebuilt manuscript remains 109 pages. Only physical pages 33–34 reflowed.
Historical drafts and archives were preserved.

## Correctness and consistency checks

All 316 existing tests passed:

- Welch MI calculations, derivation checks and saved evidence: 249.
- Differential MI calculations: 27.
- Thesis packaging and scoped build/push tooling: 24.
- Practical exploration and thesis application checks: 16.

Twenty explicitly reported null and power percentages were checked against
the saved primary results. The larger-sample claims about the differences
between methods, power above 99.9% for the larger gaps, and the 79.87–96.47%
range for the smallest gap were also verified. This review used the saved
simulation evidence; it did not rerun the full simulation grid.

Checked active manuscript sources for unfinished placeholders, ambiguous
baseline naming, internal file references and Australian English spelling.
No new issue requiring a prose or scientific change was identified.

## Build and PDF checks

- Main LaTeX build completed without warnings or overfull/underfull boxes.
- All 109 pages rendered successfully, without Poppler warnings.
- Contact sheets covering every page were inspected for layout problems.
- Full-size checks included the changed Chapter 4 pages, dense results plots,
  the application table and the signed compliance page.
- No empty text pages, unresolved-reference markers or text outside the
  physical page were found. All listed fonts are embedded.
- The freshly exported source ZIP was extracted into a clean directory and
  compiled independently. Its extracted page text matches the main build on
  all 109 pages, with no LaTeX warnings.
- The packaging module's read-only check confirmed that the delivery PDF,
  source archive and experiment supplement match the current source/evidence.

## Signed submission copies

Transferred the existing visible signature and 07/11/2026 date to the rebuilt
PDF. The original unsigned PDF bytes and every original page content stream
are preserved. The signature/date appearance streams match the previous
signed copy. The rendered signed compliance page is pixel-identical to the
previous signed compliance page; differences from the new unsigned copy are
confined to the signature and date.

Navigation is preserved relative to the new unsigned PDF: 70 bookmarks,
450 internal links, 98 URL links and 416 named destinations.

The signed deliverable and the thesis in `FINAL SUBMISSION` have identical
checksums. The previous signed submission was backed up in the existing
Research archive directory before replacement. The consent declaration and
AI acknowledgement files were left unchanged.

## Verified output hashes

- Unsigned main/delivery PDF:
  `f5f518f38eb2c6027a0ea8e2ada6b831c570d17f8752e033cd847611f72534e3`
- Signed delivery/submission PDF:
  `61257162c884db9d4e822dd1b99c13130f3a7b4fc930ee42edb9bcf9a0470697`

Detailed logs, rendered pages and comparison records from this review are in
`/private/tmp/welch-final-quality-2026-11-08-gcyu_m1_/`.
