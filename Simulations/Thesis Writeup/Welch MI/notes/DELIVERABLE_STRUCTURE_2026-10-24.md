# Main thesis deliverable structure - 24 October 2026

The user requested the same deliverable structure as the old main thesis,
with no active working-draft build. The reviewed 95-page manuscript now
builds from `main.tex` to `main.pdf`, with generated files in `build/`.
The packager and existing Makefile now publish the named delivery set:

- `Daniel_Zhao_Welch_MI_Thesis.pdf`
- `Daniel_Zhao_Welch_MI_Thesis_Source.zip`
- `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`
- `SHA256SUMS.txt` and current delivery instructions.

## Preservation

`archive/before_main_deliverable_2026-10-24/` preserves the complete Working
Draft v3 delivery set, its entry point and PDF, the previous main files and
named delivery set, the previous build directories and packaging code. The
frozen draft source ZIP contains all chapter, appendix and figure inputs
needed to rebuild that snapshot independently. The older unversioned
working draft and Working Draft/Working Draft v2 historical PDFs retain
their original paths and contents. The complete previous baseline remains
in the workspace's separate dated archive.

The main and v3 entry-point sources were already byte-identical. No chapter,
appendix, abstract, equation, bibliography, figure, experiment or numerical
result was edited. All 107 recorded manuscript, figure and historical-draft
hashes match their pre-conversion values. Active build instructions now use
main.tex/main.pdf; the old draft naming rule applies only to explicitly
requested working drafts. The source ZIP includes main.tex as its sole
root manuscript entry point.

## Verification

All 275 local tests pass, including the eight packaging tests updated for
the main target and historical-file preservation. The main PDF has exactly
the same extracted text as the reviewed draft, and all 95 rendered pages
are pixel-identical at 90 dpi. The cover, contents and representative main
chapter pages were also visually inspected. There are no LaTeX warnings or
unresolved references. The named source archive builds independently from
main.tex and produces identical PDF text. All delivery archives and
checksums match the current main manuscript and full redesigned evidence.
The redesigned supplement inventory was retained intact when restoring the
old main-version filenames. No simulations, Git staging or commit were
performed as part of this conversion.
