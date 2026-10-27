# Section 6.4 reduction — 26 October 2026

The user approved removing the standalone association-construction and allocation section, keeping a short construction finding beside the sparse-table failure, and moving the detailed tables and allocation analysis to the experiment supplement.

The preceding 103-page manuscript, current source and packaging inputs are preserved in `archive/before_section_6_4_reduction_2026-10-26.zip`.

## Main narrative

- Section 6.2.1 now ends with a short construction comparison at 16×16, common MI 0.02 nats and n_P=n_Q=1,000. The four-cell construction preserves margins and MI; the different-skew estimated difference remains biased and all three false-positive rates remain near 30%.
- The standalone former Section 6.4 and its two printed tables are removed. The application becomes Section 6.4 and its table becomes Table 6.8 automatically through the existing labels.
- Chapter 5 introduces the supporting construction check beside the false-positive design. Its power section points to broader power and allocation evidence in the supplement.
- The introduction and conclusion no longer present sample allocation as a main empirical finding. Chapter 7 retains the scientific qualification about unequal residual biases at unequal sample sizes, while moving the allocation-result interpretation out of the main discussion.
- Appendix B retains the exact scientific construction, grids and validity rules. The main derivation, numerical evidence, existing figure assets and generated table sources remain unchanged.
- The calibrated-power figure and sensitivity table stay beside their interpretation using fixed float placement. Figure dimensions, typography and scientific content are unchanged.

## Supporting deliverable

`WelchSatterthwaiteMI/supplementary_displays/construction_allocation/` contains a fresh two-page PDF, standalone LaTeX source and byte-identical copies of the two generated table sources. It preserves the original construction and allocation interpretations, setting definitions, nominal-rate denominator and limits of the tested grids. Its source builds independently. Build files stay outside the delivered folder.

The experiment supplement packaging already includes the complete supplementary-displays directory, so the new supporting deliverable and its sources are included without changing the packaging code.

## Verification

The manuscript has 102 pages, including 63 pages of main text and 16 pages in Chapter 6. Both the main build and the supporting PDF build without warnings. Five manuscript-consistency tests and eight packaging tests pass. Final preservation, source-build, rendered-page and delivery checks are recorded in `REDESIGN_VERIFICATION.json`.

All 11,878 saved scientific evidence files are byte-identical. All 79 existing figure/reporting assets and generated table sources are byte-identical; the moved table sources are copied without numerical changes. Protected Chapters 2–4 and all appendix sources are unchanged. The final delivery check passes. The main source archive rebuilds independently to identical PDF text; the five supporting files extracted from the delivered experiment archive also rebuild independently to identical two-page PDF text. Changed main pages and both supplement pages were visually reviewed. No missing references or LaTeX warnings remain.
