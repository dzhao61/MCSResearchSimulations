# Explanatory expansions: rebuilt thesis, 7 November 2026

The requested main-thesis rebuild incorporates the three expansions
recorded in `EXPLANATORY_EXPANSIONS_2026-11-06.md` and the fuller proof
recorded in `POSITIVE_MI_VARIANCE_EXPLANATION_2026-11-06.md`. Those earlier
records describe source-only stages; the current PDF now includes all four
additions.

The thesis has 109 pages, compared with 104 before these additions.
Appendix A.3 begins on printed page 86. The construction, diagnostic and
Monte Carlo uncertainty explanations remain in Appendix B.

## Build and layout verification

- Built through `package_deliverables.py --no-push` and refreshed the
  main PDF, named delivery PDF, source archive and checksums.
- The final LaTeX log contains no warnings, overfull or underfull boxes,
  or missing-character messages. The shared paragraph-style check passes.
- Visually inspected 23 affected or boundary pages, including the contents,
  Chapter 3 cross-reference, Chapter 6 connection, Appendix A derivations
  and examples, Appendix B derivations, application table and bibliography
  transition. Rechecked the three proof pages after the layout adjustment.
- Added two nonbreaking alignment-row controls to keep the three-step
  pointwise-MI ratio calculation together. This is the only manuscript
  change made during the rebuild. No wording, equations, assumptions,
  figures, font sizes or margins were removed or reduced.
- Verified that the compiled, main and named delivery PDFs are identical,
  that every archived source matches its current input, and that the
  PDF and source-archive checksums are current.
- Packaging verified and reused the unchanged experimental supplement.
  Its checksum matches the previous delivery checksum. No experiments
  were rerun.

## Preservation

Compared 634 input and output hashes saved immediately before rebuilding.
The only changes are Appendix A's two alignment-row controls and the four
refreshed outputs: the main PDF, named delivery PDF, source archive and
checksum file. The other 629 hashes match. This includes the approved
Appendix B and Chapter 3/6 source changes, abstract, conclusion, historical
files, inspected code and the separate personal study guide.

The four approved manuscript files, refreshed outputs and three explanatory
review records form the scoped build commit. The separate `output/`
directory remains outside that commit.
