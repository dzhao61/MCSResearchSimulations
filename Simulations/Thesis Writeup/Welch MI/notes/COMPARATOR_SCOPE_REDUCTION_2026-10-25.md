# Comparator scope reduction — 25 October 2026

## Decision and preservation

The reader approved removing the sample-size degrees-of-freedom arm from the main experimental comparison. The thesis now compares Expanded Welch against Normal Wald. The fixed moment reference remains a diagnostic of the denominator-moment argument; the Welch and Hutcheson background remains intact.

The preceding 97-page manuscript and all active manuscript sources and assets are saved in `archive/before_comparator_removal_2026-10-25.zip`. The experiment supplement now includes `WelchSatterthwaiteMI/supplementary_displays/sample_size_df_comparison/`: 35 preserved display/metadata files, two original reporters and their SHA-256 manifest, plus a guide to the removed rule and its evidence. All four-rule raw records, summaries, calibration results and bootstrap intervals remain in the original result directories. No simulation or bootstrap sampling was repeated.

## Manuscript changes

- Narrow the abstract, second research question, stated scope and conclusion to Expanded Welch versus Normal Wald.
- Remove the sample-size comparator's Chapter 5 definition and equation. Retain the slower construction explanation and the new design tables/equations from the earlier presentation revision.
- Remove its numerical comparisons and four-rule wording from Chapters 6–7 and Appendices B–C. Keep all retained numerical results and scientific limitations.
- Define validity and joint bootstrap calculations for the two tests and fixed reference. The saved larger joint resampling vector retains the needed marginal distributions and pairing.
- Reduce null and nominal-power displays from four rules to three. Calibrated plots now show Wald and Expanded Welch because Wald and the reference give identical calibrated decisions.
- Replace the two-panel null-rate table with one side-by-side table for the three retained rules, retaining all confidence intervals.
- Restrict paired power contrasts to Expanded Welch minus Wald, retaining the original estimates and uncertainty.
- Remove the sample-size columns from supporting power, construction/allocation and calibration tables. Show lower and upper evaluation nulls side by side in the cross-null table; all 48 retained rates remain visible.
- Keep relevant paragraphs together and arrange appendix tables without changing fonts, margins or figure dimensions.

The final thesis remains 97 pages, with 59 pages of main text and six pages in Appendix C. The simplification removes a comparison throughout the argument without changing the theoretical derivation or the study populations.

## Scientific and preservation checks

- Hashes of all 13,586 snapshotted scientific evidence/kernel files are unchanged, including stored bootstrap intervals and the two sampling kernels.
- All 37 preserved display/reporter files match their preservation manifest.
- Chapters 2–4, Appendix A, bibliography and preamble remain byte-identical to the pre-edit snapshot. In particular, the protected Section 2.3 is unchanged.
- Fifteen unaffected regenerated plots render pixel-identically to their preserved versions. Only the three null and two focused-power plots have changed method content.
- The sample-size arm's valid counts equal Wald's in every one of the 366 saved evaluation settings. Its validity mask is a subset of the base mask, so omitting it leaves the common-valid denominators unchanged.
- Retained calibrated null rates still range from 4.93% to 4.99% across A–C. The main Wald/Expanded Welch grid classification remains 29 toward, 52 away and 39 within the existing tolerance.
- All 48 cross-null rates were independently checked in their displayed row and column against the saved sensitivity summaries.
- The compiled manuscript and active redesign tables contain no removed-comparator labels or obsolete four-method wording. Background discussion of sample-size assignments is retained where it motivates the MI-specific derivation.

## Verification

All 223 experiment tests and eight packaging tests pass. Existing display tests now check retained values in the manuscript and omitted comparator values in their preserved supplement tables. The final build has no LaTeX warnings, undefined references or overfull/underfull boxes.

Rendered physical pages 2–11, 42–67 and 75–92 were reviewed, with full-page checks of the revised calibration tables. The final delivery package passes checksum/inventory verification. The extracted source builds independently without warnings and produces identical PDF text. These completed checks are recorded in `REDESIGN_VERIFICATION.json`. No Git commit was requested.
