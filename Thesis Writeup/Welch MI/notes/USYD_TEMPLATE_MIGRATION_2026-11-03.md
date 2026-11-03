# Sydney template migration — 3 November 2026

## Authorised scope

Switch the active thesis to the supplied Sydney LaTeX template and rebuild
the manuscript. Retain the existing argument, chapters, appendices,
derivations, experiments and research questions. The user supplied SID
510546500; the title date is 3 November 2026. No additional literature,
experiments or manuscript sections were requested.

The starting source already contained the three approved edits naming the
variance influence function, making the near-independence prediction colour
consistent, and connecting the conclusion to the existing regression
literature. Those edits are retained in this build.

## Template and adaptations

The source template is `Thesis Writeup/Example Thesis/thesis_2024/`.
Its source files, rather than its older bundled example PDF, define the
layout. They remain unchanged in that folder.

- Copy `usydthesis.cls`, `style/prettyref.sty`, `style/footmisc.sty`,
  `style/mybibstyle.bst` and `style/usyd-primary-colour.pdf` into the active
  thesis and include them in the source archive.
- Use the class's A4, one-sided, 11pt AMS book layout, Times-style prose,
  native chapter headings, running headings, captions and contents format.
  Retain the template entry point's one-inch side margins.
- Use the template title page with Daniel's existing degree, school and
  supervisor metadata, the supplied SID and the agreed date. Change only
  `fulfillment` to Australian `fulfilment` in the copied class.
- Include the template's plagiarism compliance statement with Daniel's
  name and blank signature/date lines. Do not copy the example signature.
- Apply the shared 19.5pt body baseline and half-line paragraph gap after
  the single-spaced title page. Retain flush-left paragraphs and compact
  contents/figure/table lists through the shared preamble commands.
- Use `\raggedbottom` to prevent AMS page stretching from enlarging
  paragraph gaps around fixed-position figures. Keep all existing figure
  sizes and logical locations.
- Reserve a wider page-number column in the contents. Remove redundant
  manual abstract/acknowledgement entries, because AMS creates them.
- Use the supplied author-year bibliography style with a local addition
  printing DOI and URL fields. Its original hyperlink support alone would
  leave those identifiers invisible in the reference list.
- Fill PDF subject and keyword metadata. This also avoids a Poppler text
  bounding-box extraction failure with empty metadata fields.

## Preservation and verification

- The preceding named manuscript contains 103 pages; the new layout has
  100 pages, including the added compliance page. No scientific content
  was cut to reduce page count.
- All 104 chapter, appendix, bibliography and display inputs match the
  pre-migration snapshot byte for byte.
- Abstract and acknowledgement prose is unchanged; only their redundant
  contents-entry commands were removed.
- All 136 existing active numbered labels retain their numbers. The
  compliance statement adds one label.
- All 46 cited bibliography entries are retained. Existing visible URL
  fields are preserved, and the new bibliography prints DOI fields too.
- The paragraph-style policy passes. The main and independent source
  builds produce no LaTeX warnings, overfull boxes or underfull boxes.
- All 100 pages were rendered and inspected, including the title,
  compliance statement, contents, dense equations, results figures,
  tables, appendices and bibliography. The final contents layout was
  checked again at full size.
- A clean build outside the thesis tree, using only the source archive,
  reproduces all extracted text and page breaks exactly.
- New authored front-matter wording follows Australian English. Published
  titles, citation keys, source identifiers and the template's original
  policy wording are retained.

## Final delivery checks

The main PDF, named PDF, 117-input source archive, 37,649-input experiment
archive and SHA-256 checksums were refreshed together. The full
`package_deliverables.py --check` verification passes, comparing both
archive inventories and every archived file with its current source.

A second clean build from the final delivered source archive has no
LaTeX warnings or overfull/underfull boxes and reproduces all 100 pages'
extracted text and page breaks exactly. Main, build and named PDFs are
byte-identical. Extracted text bounding boxes remain inside page boundaries.

All 48 protected historical files, separate presentation and user-provided
documents retain their original size and exact modification time. The
separate `AI_Acknowledgement.docx` and `Declaration-thesis.pdf` were not
changed or incorporated. No simulations were rerun. No git commit or push
is part of this migration request.
