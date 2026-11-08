# Requested PDF rebuild and formatting review — 28 October 2026

The user requested a PDF rebuild after the display and Chapter 6 mechanism revisions. The canonical main PDF and named delivery PDF are now current. The final thesis has **102 pages**, compared with 99 in the preceding delivery: 67 printed main-text pages, including 19 in Chapter 6, followed by Appendices A/B/C of 5/9/7 pages. The additional pages accommodate the revised explanations and expanded table labels at their existing readable sizes.

## Formatting changes

The rendered review found that expanded tables could interrupt the explanation of a different table or appear after their own interpretation. Tables 6.4, 6.5, C.2 and C.3 now use the existing fixed-placement option so they follow their introduction and precede their interpretation. No prose, equation, numerical cell, citation, figure asset or scientific algorithm changed during this build phase. A comparison with the pre-build snapshot confirms that the only manuscript-source changes are those four placement arguments. The thesis README now records the current delivery and page count.

## Verification

- All 102 pages were rendered and reviewed in contact sheets. Chapter 6 (physical pages 54–72), Appendix C (91–97), and the contents and figure/table lists (4–9) were also inspected in larger renders. The final published pages match the reviewed renders pixel for pixel.
- Tables fit within the margins, their expanded labels remain legible, and figures and captions have no observed clipping or overlap. The paragraph-style guard confirms flush-left paragraphs throughout the active sources. All 102 pages are A4, and all 41 fonts are embedded.
- Both the canonical build and the independent build from the final exported source archive completed without LaTeX warnings, unresolved references, or overfull/underfull boxes. The independently built PDF has the same extracted text as the delivered PDF.
- The main, build and named delivery PDFs have identical SHA-256 hashes. The full delivery check confirms that the PDF, source archive, supplement and checksum manifest match their current inputs.
- All 7,381 saved result-summary hashes remain unchanged. No new simulations, fits or bootstraps were run for this rebuild. The 27 passing source-phase tests are recorded separately in the mechanism revision checks; this phase adds compilation, archive and rendered-layout verification.

The preceding delivery and pre-formatting sources are preserved in `archive/before_mechanism_pdf_build_2026-10-28.zip`. Machine-readable checks are in `notes/MECHANISM_PDF_BUILD_CHECKS_2026-10-28.json`. Future PDF rebuilds remain subject to an explicit user request.
