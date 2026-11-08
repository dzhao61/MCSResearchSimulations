# Final-version rebuild — 4 November 2026

The user requested a PDF rebuild and asked that it be treated as the final
version. This uses the active Sydney-template `main.tex` and the stable
named delivery files. The agreed title-page date remains 3 November 2026.
Historical working drafts and archives are protected.

## Included source edits

- Section 6.1.1 replaces the vague singleton contribution with a numerical
  example: at `n=50` in the different-skew 16 by 16 populations, cells
  observed once account for about 88% of mean estimated pointwise-MI
  variance in P and 92% in Q. The passage states the 10,000 diagnostic
  repetitions and retains the Appendix B.4 methods reference.
- Section 7.1.2 makes the larger-sample rejection result explicit, avoiding
  “remain below” after the preceding over-rejection result.
- Section 7.2 describes Appendix A.2 as an analysis of the quadratic
  sampling variation remaining at independence.
- Section 7.3 identifies improving the shared estimates as a research
  priority, avoiding a universal necessity claim about alternative tests.

The two numerical shares were independently reconstructed from the saved
random streams and matched the saved raw outputs: 87.574784% in P and
91.841881% in Q. The five existing thesis-consistency tests and the shared
paragraph-style check passed after the source edits. Scientific displays,
figure settings, citations, references and labels were preserved.

## Build and visual verification

- The final build contains 100 pages, matching the preceding delivery.
- LaTeX reports no warnings, unresolved references, overfull boxes or
  underfull boxes.
- All 137 active labels retain their numbers.
- All 100 pages were rendered. Physical pages 58, 82, 83 and 84 contain
  the approved edits and were reread and inspected at full size.
- The other 96 page rasters are pixel-identical to the previously reviewed
  Sydney-template build. The title, compliance statement, abstract and
  acknowledgements were also visually checked again.
- Text bounding boxes remain inside the page boundaries. No further
  manuscript, mathematical or layout changes were needed.
- The template compliance statement retains blank signature/date lines.
  The separate acknowledgement and declaration files are not incorporated.

## Final delivery verification

The main and named PDFs, 117-input source archive, 37,649-input experiment
archive and SHA-256 checksums were refreshed together. The full
`package_deliverables.py --check` verification passes, comparing archive
inventories, every archived file and all delivery checksums with the
current inputs. The experiment archive has the same checksum as the
preceding delivery.

A clean build using only the delivered source archive reproduces all
100 pages' extracted text and page breaks exactly, with no LaTeX warnings,
overfull boxes or underfull boxes. Main, build and named PDFs are
byte-identical. All pages are A4 and all 36 font entries are embedded.
The bibliography retains all 46 cited entries.

All 30,686 protected files in the historical archives and separate
deliverables retain their original sizes and exact modification times.
The user's separate acknowledgement and declaration files were preserved.
No new scientific experiments, git commit or git push are part of this
rebuild request.

Final PDF SHA-256:
`6a3442e9732f29daace007433b7ee3c575d984ab1a3196a7a8555c0863b91a94`.
