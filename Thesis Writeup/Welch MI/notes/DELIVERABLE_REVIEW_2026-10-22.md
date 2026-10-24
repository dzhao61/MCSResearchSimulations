# Full thesis deliverable review

The redesign has received a full manuscript pass against the preserved original, beyond the initial integration of new experiments. All changes remain inside the independent redesign workspace. A pre-polish snapshot of manuscript sources, the PDF and report generator is preserved in archive/pre_delivery_polish_2026-10-22.zip.

## Scientific and expository changes

- Clarified the population variance coefficient V, its estimate Vhat and the sampling variance of that estimate. Defined the exact targets and sampling expectations before the comparisons.
- Added an explicit six-comparison design overview, the exact nominal Student t decision rule, the independent fitting construction and a precise link to the existing derivation.
- Added the cancellation proving the combined component-moment identity, with assumptions and interpretation, in Appendix B.
- Expanded the delta-method uncertainty derivation with the function, expansion point, estimates, differences, partial derivatives and covariance-preserving contribution. Section 2.3 and the original core derivations are untouched.
- Added Wilson intervals to the selected nominal-rate table, paired nominal/calibrated power contrasts, component-spread summaries and independently fitted reference MCSEs.
- Added confidence bands, plug-in variance comparisons and explicit validity panels to the main figures.
- Explained the construction and allocation comparisons numerically, including changes in SD, bias and degrees of freedom. Added signed bias calculations for the sparse null and alternative failures.
- Reworked the discussion, conclusion and 220-word abstract into a connected thesis argument. The power claims remain limited to the selected population paths and distinguish nominal from calibrated comparisons.
- Removed redundant administrative framing and an unnecessary appendix closing section. Retained the separate 20,000-pair jackknife evidence and computational timings with their scientific settings.

## Verification

The statistical simulation inputs, sampled pairs and estimation methods are unchanged. The existing full independent experiment audit applies. Two additional independent reporting tests check Wilson intervals against scipy.stats.binomtest and reconstruct paired contrast uncertainty and percentage-point units from discordant counts. PDF rendering, final tests, source isolation and archive consistency are checked before delivery.

Final verification is complete. All 268 local tests pass: 216 experiment, 27 estimator, 17 application and 8 packaging tests. The extracted supplement and separately extracted thesis source pass all 178 bundled tests: 134 experiment, 27 estimator and 17 application tests. The application test now accepts the count tables in the delivered thesis_application directory when the historical exploratory results directory is absent; the two count-table files were verified identical.

The 109-page final PDF was rendered and inspected. The source archive builds in isolation without LaTeX warnings, and its extracted text is identical to the reviewed delivery PDF. The final archive consistency check passes. The independent experiment audit retains 4,416 reconstructed pairs, and the preservation check confirms all 30,042 original files and protected copied sources remain unchanged. Current numerical verification and the delivery PDF checksum are recorded in REDESIGN_VERIFICATION.json at the redesign workspace root.


## Subsequent readability revision

The user requested a simpler experimental narrative after reviewing the full deliverable. READABILITY_REVISION_2026-10-22.md records the prior-session writing guidance, applied changes and final verification. The current PDF is 104 pages, with Chapters 5–7 reduced from 28 to 22 pages; the core theory and all experimental calculations remain unchanged. The 268 local tests, 178 bundled tests, isolated source build, PDF review and delivery consistency check pass.
