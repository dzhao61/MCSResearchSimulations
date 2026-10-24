# Appendix reduction - 23 October 2026

The user requested substantial appendix cuts, including whole sections. The manuscript is reduced from 108 to 95 pages. Appendix C falls from 19 to 6 pages; the combined appendices fall from 38 to 25 pages. The main chapters retain their previous page spans. Plot dimensions, fonts and statistical results are unchanged.

## Preserved material

The complete pre-cut draft, sources and figures are saved in `archive/before_appendix_reduction_2026-10-23.zip`. The full previous Appendix C is preserved as a readable 19-page PDF, source fragment and all 20 local figure/table dependencies under `WelchSatterthwaiteMI/supplementary_displays/full_additional_results/`. The experiment supplement includes that directory automatically. The supplementary PDF retains its original numbering; its text and rendered pages match the original appendix exactly.

The original workspace and historical working drafts are unchanged. Chapters 2-4, Appendices A-B, every figure PDF, estimators, simulation records and numerical evidence are unchanged. No new simulations or statistical calculations were required.

## Entire sections removed from the thesis

| Previous section | Treatment and reason |
| --- | --- |
| C.1 Companion approximation comparisons | Full companion plots moved to the supplement. The main chapter already explains the approximation using its principal figures. The scaled mean-error ranges remain in the shortened appendix to support the population-dependent correction argument. |
| C.3 Same-skew null comparison | Companion curve moved to the supplement. The main grid summary covers all three margin regimes, and the selected same-skew rates remain in the main results and diagnostic tables. |
| C.6 Matched construction comparison | Full table and extended interpretation moved to the supplement. Chapter 6 retains the mechanism, key matched results and scientific conclusion. Appendix B retains the construction formula and complete settings. |
| C.7 Unequal allocation at a fixed total | Full table and extended interpretation moved to the supplement. Chapter 6 retains the fixed-total comparison, direction of imbalance, SD change and power example; Appendix B retains every allocation and population setting. |
| C.8 A jackknife check of MI difference bias | Entire side investigation moved to the supplement. Its references in Chapters 5, 6 and 8 were removed. The thesis's comparison remains focused on the existing four rules. The original estimator, settings, evidence and limitations remain available in the supplement. |
| C.9 Computational cost | Entire timing section moved to the supplement. The corresponding timing claim was removed from the introduction's contribution list. |

## Other cuts and retained support

The broader power curves from old C.5 were moved to the supplement. The direction counts, bias-shift equation and explanation of wrong-direction rejection remain in the shortened appendix because Chapter 7 relies on that mechanism.

The lower-null calibrated-power rate table was removed because it repeats the retained calibrated-power curve. The paired nominal/calibrated contrasts, actual sensitivity power rates and complete cross-null validation table remain. The compact gain table in Chapter 6 is unchanged.

Repeated narration of A/B/C diagnostic values was removed. The component means and sampling spread, shared-estimator diagnostics and independent reference-fitting table remain. Their definitions, inclusion rules and Monte Carlo uncertainty remain in the manuscript.

The Holm table and all six comparison definitions remain, preserving transparency about application selection. Its adjustment algorithm is shortened while retaining the complete calculation rule.

## New Appendix C structure

1. Component diagnostics and reference fitting.
2. Calibrated power and sensitivity checks.
3. Sparse-table bias and estimated direction.
4. Holm adjustment for the application.

Main-text references were updated to the retained sections or to the experiment supplement. Removed jackknife and timing claims no longer appear in the main argument. Appendix A retains the derivations supporting the central theory, and Appendix B retains the scientific construction, full parameter grids, validity rules, moment identities and uncertainty calculations needed to reproduce the main study.

The existing jackknife and same-skew report tests now inspect the preserved supplementary source for relocated material; their statistical evidence checks remain intact. Current verification results are recorded in `REDESIGN_VERIFICATION.json` after delivery refresh.

Final verification: 275 local tests and 185 extracted-package tests pass. The final manuscript is 95 pages and its isolated source build has identical extracted text with no LaTeX warnings. Changed pages, contents, figure/table lists and all six pages of the new Appendix C were rendered and inspected. All 19 supplementary pages match the preserved original visually and in extracted text. All 30,042 original files match their hashes. Delivery archives and checksums are current. No Git commit was made in this pass.
