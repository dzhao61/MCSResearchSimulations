# High-impact thesis revision — 30 October 2026

The three approved packages have been implemented and included in the requested PDF rebuild. The revised passages were read with their surrounding explanations and checked against the root and thesis-folder writing guidelines. The affected rendered pages were then inspected for table placement, page flow, readability and margins. The final PDF has 107 pages, unchanged from the previous build.

## Implemented changes

1. **Section 6.1.2:** completed the explanation of both rows of the component-degrees-of-freedom figure before introducing the detailed numerical table. The column definitions now precede the table. The following worked comparison explicitly identifies the population prediction of the sampling variance, the population benchmark for the sampling mean, and the resulting 15.30-versus-21.03 degrees-of-freedom comparison. The sampling-moment target, population first-order value and sample-based estimate remain distinct.
2. **Section 6.2.2:** grouped the sparse-table diagnosis with the selected-setting bias, standard-error and rejection tables. The complete sparse same-skew/different-skew comparison, bias-shift equation and four-cell construction check now precede the uniform-curve mechanism and stronger-common-MI comparison. The explanations and numerical evidence remain intact; the moved paragraph now names excessive rejection directly instead of referring generically to “the failure.”
3. **Section 6.3.2:** added a compact independent-null-validation table for A at two null SDs. Its eight rates reproduce the saved cross-null evidence. The body specifies the lower and upper common MI values, the validation denominator and the relationship to the fixed alternative. The interpretation connects calibration-dependent power to changing relative false-positive rates without treating two null settings as a complete validity assessment.
4. **Chapter 7:** described A, B and C where needed, connected the calibrated-power interpretation to the new main-text validation table, and integrated the mathematical contribution and empirical judgment in a final assessment of the main findings. Overlapping recap was removed. The conclusion retains the distinction between approximation accuracy, test calibration and errors in the shared statistic.

The abstract and introduction were checked against this assessment. Their existing claims remain consistent and were preserved. The online-shopping application retains its role as an illustration of calculation and interpretation; it does not establish error rates for unknown populations.

## Writing review

The changes preserve connected academic prose, explicit statistical objects and explanations of mechanisms. They introduce no new notation, derivation shortcuts, manuscript workflow details or unsupported claims of general reliability. The new table caption is short; settings and interpretation are in the body. Existing figure dimensions and typography are unchanged. The previous reading-order improvements in Sections 6.1.3 and 6.3.2 remain in place.

## Verification

- All five existing manuscript-consistency tests pass, including checks against saved numerical evidence and bibliography entries.
- The paragraph-style check and `git diff --check` pass.
- The eight newly displayed rejection rates and the upper common MI agree with their saved source tables.
- All 18 original numbered equation, figure and table blocks in Chapter 6 are byte-identical, including the moved bias-shift equation. One new table was added. Citations in both edited chapters are preserved.
- Static traversal of the active manuscript finds 158 unique labels and resolves all 216 reference uses. Environments, braces and inline/display math delimiters are balanced in the edited chapters.
- Only the three intended Chapter 6 subsections changed. Its other sections and subsections, including the near-independence discussion, nominal-power discussion and application, are byte-identical.
- At the source-edit stage, only Chapters 6 and 7 changed among 125 fingerprinted manuscript, figure and delivery inputs. Section 2.3, Chapter 4, figure assets, generated evidence tables, bibliography, abstract and introduction retain their original hashes. The subsequent requested rebuild refreshed the main and named PDFs, source archive and checksums.

The original chapters and baseline fingerprints are preserved in `../archive/before_high_impact_revision_2026-10-30.zip`. Machine-readable source checks are in [HIGH_IMPACT_REVISION_CHECKS_2026-10-30.json](HIGH_IMPACT_REVISION_CHECKS_2026-10-30.json).

## Requested PDF rebuild and rendered review

The final LaTeX log contains no warnings, overfull or underfull boxes, or unresolved references. All 41 fonts are embedded, and the document remains A4 with the shared paragraph style.

Inspected PDF pages 58–59, 67–70, 72–73 and 77–79 (printed pages 49–50, 58–61, 63–64 and 68–70). Table 6.1 follows the complete figure explanation and column guide; the selected-setting tables remain close to their interpretation; and new Table 6.7 fits within the margins beside its settings and interpretation. The adjoining power figure, conclusion, headings and page breaks remain readable. No further manuscript or layout changes were needed during this build.

The main, build and named delivery PDFs have identical SHA-256 hashes. The refreshed source archive was checked against every packaged source file. The previously verified 7.0 GB experiment supplement and its checksum were reused after checking its full 24,996-file inventory, sizes and modification times. No experiments, full supplement rebuild/content rehash or independent exported-source compile were run for this interim build.

The previous PDF, source archive and checksums are preserved in `../archive/before_high_impact_pdf_build_2026-10-30.zip`. Historical drafts are unchanged.

Final PDF SHA-256: `1c6b6b29c2a34fbeaa0f91f8ed5fd16fe60a876b314c15bfacfa0db8faf7b4ff`.

Source archive SHA-256: `46442cbc811c584df32ee00ac0edc9b9e3ff79f7538a355fa9931b33d0181535`.
