# Sample-thesis typography match — 30 October 2026

The user requested formatting like the three supplied sample theses after
comparing their body font, line spacing and paragraph gaps. The current
delivery is 123 pages. The previous 114-page PDF, source delivery and formatting
are preserved in `../archive/before_sample_typography_2026-10-30.zip`.

## Formatting

- Body text now uses the 11pt class setting and the same Nimbus Roman
  Times-style font found in all three samples. Computer Modern mathematics
  matches the samples' text/mathematics combination.
- The body baseline is 19.5 TeX points, measured as 19.43 PDF points, matching
  the samples. The `book` class uses a 13.6pt unscaled baseline, so its stretch
  factor is 1.433824 rather than the AMS template's 1.5 on a 13pt baseline.
- Extra paragraph spacing is half the body baseline, measured as 9.71 PDF
  points. Consecutive paragraphs therefore have approximately 29.14 PDF points
  between the last and first baselines, matching the samples. Paragraphs remain
  flush left.
- The text block matches the samples: horizontal limits approximately 72.00
  and 523.28 PDF points, with the ordinary first body-text box at 119.65 PDF
  points from the page top. The document remains A4.
- Captions use the normal body font size. The existing chapter structure,
  title material, section headings and figure/table sequence are retained.
- Bibliography entries use ragged-right alignment to avoid stretched word
  spaces after the font change. Bibliographic content is unchanged.

The thesis instructions and packaging style check now enforce the revised
paragraph spacing. The existing packaging test also rejects restoration of
the previous spacing.

## Verification

- Fingerprints confirm that all scientific chapter and appendix sources,
  bibliography entries, table data and figure assets are unchanged.
- The final build has no LaTeX warnings, missing characters, overfull or
  underfull boxes, or unresolved references.
- All 123 pages were rendered and reviewed in page overviews. Twelve
  representative pages were also inspected at larger resolution, covering
  body prose, Chapter 4 equations, Chapter 6 figures and tables, the application,
  the moved component table and the bibliography. No text extends outside the
  page, and no accidental blank pages were introduced.
- All 38 fonts in the PDF are embedded. Body measurements were checked against
  the earlier PDF measurements for Grace Yan, Michael Fang and Riley Jones.
- All 15 existing packaging tests pass; source whitespace checks pass.
- The source archive builds independently without warnings and produces
  identical PDF text to the main build.
- The named PDF, source archive and checksums were refreshed. The experiment
  supplement was reused after verifying all 24,996 input paths, sizes and
  modification times against the previously verified archive.

No scientific prose, equations, estimates or experiment results were edited.
