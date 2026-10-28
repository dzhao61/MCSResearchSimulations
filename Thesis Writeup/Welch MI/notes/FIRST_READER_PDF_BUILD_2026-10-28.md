# Requested PDF build and formatting review — 28 October 2026

The first-reader source revision is now in the main deliverable. The final PDF has **99 pages**, compared with 98 before this revision. Main text is 66 pages; Chapter 6 remains 18 pages. Appendices A, B and C occupy 5, 9 and 5 pages respectively.

The prior PDF, source archive, checksum file, verification record and pre-formatting manuscript sources are preserved in `archive/before_first_reader_pdf_build_2026-10-28.zip`. Historical working drafts and the archived baseline were untouched.

## Formatting review

Rendered all 99 pages and inspected seven contact sheets for page flow, margins, paragraph consistency, headings, figures, tables, captions, numbering and bibliography layout. Inspected PDF pages 29, 33, 34, 39, 40, 55, 64, 67, 69, 87, 92 and 93 in greater detail, covering the moved variance guide, the new Student t construction and component target, the component-role table, results diagnostics and calibration, and appendix definitions/tables.

The only source adjustment during this build was the text-column alignment in Table 4.1. Ragged-right columns keep “Expanded Welch” and ordinary words together instead of forcing awkward hyphenation. The final table was rendered and inspected. Only PDF page 40 changed; all other 98 pages are pixel-identical to the reviewed preliminary build. No scientific wording, equations, values, figure dimensions or plot data changed during this formatting correction.

## Validation

- Final LaTeX log: no warnings, overfull boxes, underfull boxes or unresolved references.
- All 41 fonts are embedded. All pages are A4, with the existing typography and flush-left body-paragraph policy.
- The main packaging command refreshed the named PDF, self-contained source archive, experiment supplement and checksums. Its complete archive-content check passed, and a separate final `--check` passed.
- Extracted the final source archive to a separate temporary folder and built it independently. The full extracted PDF text matches the delivered PDF exactly, with no LaTeX warnings.
- `build/main.pdf`, `main.pdf` and the named delivery PDF have identical SHA-256 hashes.
- All 7,381 saved result-summary hashes remain unchanged. No experiments, fitting batches or bootstraps were rerun.

Final PDF SHA-256: `e1cd07279e5f7ccb93ae187d0e167e2d8b5b91fc7b839180550fc172bec6738b`.

Source archive SHA-256: `0095cc29dc78d74b667cfb17cd43bbcdc82b9631839d6f91d460845bccc7f1ec`.

The current PDF is [the named thesis delivery](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/deliverables/Daniel_Zhao_Welch_MI_Thesis.pdf>). Source and delivery consistency are current; no rebuild remains pending. Future builds continue to wait for an explicit user request.
