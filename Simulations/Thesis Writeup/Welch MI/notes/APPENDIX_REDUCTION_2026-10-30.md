# Appendix C removal and conservative B reduction

Implemented on 30 October 2026 after approval of `APPENDIX_REDUCTION_PLAN_2026-10-30.md`. Source edits only; the existing thesis PDF and delivery archives have not been rebuilt or refreshed.

## Preservation

The complete pre-edit manuscript source, figures and current 122-page PDF are archived in `archive/before_appendix_c_removal_2026-10-30.zip`.

The exact current Appendix C is preserved under `WelchSatterthwaiteMI/supplementary_displays/additional_results_2026_10_30/`, including its eleven-page PDF, original source, nine external table inputs, inline Holm table and preservation manifest. The original B source is preserved there as well. The supplementary PDF retains printed pages 98–108 and the original reference numbering. Extracted text is identical, and all eleven rendered pages are pixel-identical to the original at 65 dpi. The first and last preserved pages were also inspected visually.

The older nineteen-page appendix and all other historical supplements are unchanged. Archive and supplementary-display folders remain locally preserved under the existing Git ignore policy; the experiment packager includes the new supplementary files on the next refresh.

## Submitted-thesis changes

- Removed C's include and retired its source from the active appendix directory. Only A and B remain in the main build.
- Updated Chapter 1's roadmap to identify the two appendices by purpose.
- Kept Chapter 6's three-row explanation structure and all existing figures, tables and displayed equations. Replaced C-dependent lookups with brief local evidence where it supports a central explanation: the singleton/decomposition check, near-independence approximation checks, centred-magnitude rank correlations and changing alternative spread at B.
- Retained the worked component-df example, selected estimator/rejection tables, calibrated-gain table and decisive cross-null validation rows. Removed pointers to the longer supplementary tables and the paragraph depending on nominal contrast intervals.
- Retained the application selection disclosure and adjusted month p-values. Named all six exploratory comparisons, preserving the Adult and Student Performance citations in the main text. Full application-family preparation and p-values remain supplementary.
- Removed the separate sparse-alternative sign-reversal result from the conclusion. Retained the sparse-null failure and four-cell robustness finding under RQ2.1, with a reference to their main-text evidence. Future-work motivation now refers to the main MI-sweep figure rather than requiring the supplementary mean-error analysis.
- Removed the Chapter 5 direction-measure row and promise to report separate direction counts, since those results are now supplementary. Two-sided power still explicitly includes both rejection directions. Removed the promise of component percentile summaries that are no longer printed.
- Preserved all mathematical work in A; replaced its retired C-table reference with the main near-independence comparison and adjacent interpretation.

## Appendix B

- Removed the duplicated grid table and margin definitions. Added precise references to the Chapter 5 grids, focus settings, alternative equation and calibration table.
- Retained the unique supporting four-cell null settings beside their construction. The retired alternative grid remains in the preserved original B.
- Retained the exact fitted SD constants and added their three Monte Carlo standard errors locally.
- Removed the supplementary-only rejection-direction counting recipe.
- Replaced two repeated moment-target definitions with references to their Chapter 4 equations. Retained the exact moment-error decomposition and the full existing joint uncertainty calculation.
- Preserved construction proofs, root/acceptance tolerances, sampling and random-stream rules, sparse-cell handling, all validity rules and rate denominators, finite-zero inclusion, the direct combined-df equation, and calibration/tie/bootstrap rules.

B falls from 2,307 to 2,068 whitespace-delimited source words; Chapter 6 falls from 7,518 to 7,462. These are source counts, not rendered word or page counts. The main saving is removal of the eleven-page C; actual total savings await a requested rebuild.

## Verification

Results are recorded in `APPENDIX_REDUCTION_VERIFICATION_2026-10-30.json`.

- Fifteen packaging tests, five thesis numerical-consistency tests and eleven independent derivation checks pass: 31 tests total. Packaging tests use temporary fixtures and mocked compilation; they do not rebuild the actual thesis or refresh deliveries.
- The active input tree contains 21 TeX files, 140 unique labels, 82 reference targets and 46 citation keys. No dangling references, duplicate labels, missing citations, missing inputs or unbalanced environments/braces were found.
- All fifteen C labels are absent from active reference targets. The main source-package inventory excludes the retired C source; the experiment inventory includes all fourteen files in the new supplementary folder. No packaging-code change was needed.
- The paragraph-style check passes. Preamble, metadata, bibliography, Chapters 2–4 and all existing figure/table assets are byte-identical to the pre-edit snapshot. Chapter 6's figure, table and displayed-equation blocks and A's mathematical display blocks are unchanged.
- Retained mechanism values were checked against existing evidence. Around the checked troughs, the linear/remainder variance decomposition includes covariance; the uniform 2×2 correlations round to 0.656 and 0.167; B's four-SD alternative spread rounds to 1.70 times its fitted null SD.
- The current main PDF is byte-identical to its archived pre-edit version. No simulation, fitting or bootstrap was rerun.

## Next requested build

Rebuild only on explicit request. Verify changed passages, table/equation numbering, contents/list of tables and the B-to-bibliography transition visually. Refresh main/named PDFs, source ZIP, experiment supplement and checksums. The supplement inventory has changed, so do not reuse its previous ZIP/checksum unchanged. Report the actual final page count after compilation; no new page count is claimed here.

## Requested rebuild, 30 October 2026

The user subsequently requested a rebuild after the inline sample-size formatting change to Table 6.3. The completed PDF has 109 pages, down from 122. The eight front-matter pages precede 82 pages of main text, six pages of Appendix A, eight pages of B and five bibliography pages. Appendix C is absent from the PDF and front lists.

The final LaTeX log has no warnings, overfull boxes or underfull boxes. Visual review covers 26 targeted pages, including contents and list of tables, the changed explanations and design table, Table 6.3 with all sample sizes on the setting line, the conclusion, the end of A, all of B and the bibliography transition. Existing figure sizes and body typography are retained. The delivery refresh rebuilds the changed supplement rather than reusing its previous archive.

The final `package_deliverables.py --check` passes. Main, build and named delivery PDFs have identical hashes; the source ZIP excludes retired C and contains the inline Table 6.3 labels, and the refreshed experiment ZIP includes all fourteen preserved-C files. All delivery checksums are current. No Git commit was requested or made.
