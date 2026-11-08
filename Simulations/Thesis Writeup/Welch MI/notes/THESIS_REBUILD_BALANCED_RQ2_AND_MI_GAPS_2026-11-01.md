# Thesis rebuild after the balanced RQ2 and MI-gap revisions

Explicitly requested and completed on 1 November 2026.

The main and named thesis PDFs contain 104 pages, compared with 105 in
the preceding build. This build includes the balanced null study at
common MI 0.005, 0.02 and 0.30, the power study at MI-gap magnitudes
0.005, 0.01 and 0.02, six replacement figures and the compact null
diagnostic table. The related design, introduction, abstract, conclusions
and Appendix B changes are included. No experimental sampling was repeated.

## Verification

- Compiled `main.tex` through the packaging module's main-build function.
  The completed LaTeX log has no warnings, overfull boxes, underfull boxes
  or unresolved references. Paragraph-style checks pass.
- Rendered and visually inspected 40 changed or boundary pages, including
  the abstract, contents and figure/table lists, experimental design,
  every page of the revised null/power discussion, all six new figures,
  the diagnostic table, application, conclusions, Appendix B and final
  bibliography pages. Figure labels, captions, margins and table rows
  remain readable and unclipped.
- The source archive contains 111 files. Its extracted source was compiled
  independently with a separate build directory; the resulting PDF has
  identical extracted text and page breaks and no LaTeX warnings. The
  independently compiled inputs exactly match the final archive members.
- Regenerated and verified the experimental supplement because its inputs
  changed. It contains 37,649 files and occupies 12,670,746,708 bytes.
  Both new studies, raw records, combined summaries and audits are included.
- The full `package_deliverables.py --check` command passes, verifying
  both archive inventories and file contents, main/named PDF equality,
  delivery instructions and all three published SHA-256 checksums.
- The user's presentation PDF is unchanged. Historical drafts and archives
  were not build targets.

## Published files

- `deliverables/Daniel_Zhao_Welch_MI_Thesis.pdf`: 758,546 bytes.
- `deliverables/Daniel_Zhao_Welch_MI_Thesis_Source.zip`: 1,188,239 bytes.
- `deliverables/Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`.
- `deliverables/SHA256SUMS.txt`.

The thesis PDF SHA-256 is
`eaa37ab19960b4bda3362bf4ab7094c448adcea5b28e8b9a4787840bed9bba90`.
RQ2 begins on printed page 59, the diagnostic table is on page 65,
and the power section begins on page 66.

This rebuild supersedes the build-pending statements in the preceding
balanced-RQ2 and MI-gap source-revision records.
