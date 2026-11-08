# Fixed moment reference moved to the supplement, 27 October 2026

The user authorised moving the fixed-reference testing rule out of the
thesis. The main comparison is Expanded Welch against Normal Wald.
RQ1's component sampling-moment targets are retained: they assess the
derivation and do not introduce another testing rule.

## Changes

- Removed the fixed-reference definition and discussion from the Introduction,
  experimental design, results and combined Conclusions chapter.
- Reduced null and nominal-power plots to two tests; calibrated plots continue
  to show the two distinct curves. Validity panels and interval definitions stay.
- Removed reference-rate, reference-df and combined Wald/reference headings
  from thesis tables, retaining the original Wald and Expanded Welch values.
- Retained the independently fitted null SDs, their precision, and exact
  constants used to construct the focused power alternatives.
- Appendix B retains the component moment target and mean/variance ratio
  decomposition. The combined-reference calculation and component-combination
  proof move to the supplement. Other appendix material has not been reduced.
- Retained uncertainty calculations needed for RQ1 and calibrated power.
- Removed the 186-fitting-setting and total-pair recap from the main design;
  those totals include fitting work for the supplementary reference. The
  supplement retains the original counts. The main design specifies the
  fitting populations actually needed for focused power and calibration.
- Main common-valid wording now refers to the two tests. Saved reference and
  Wald validity counts are identical, so removing that rule does not change
  the relevant intersection.

## Preservation and regeneration

`WelchSatterthwaiteMI/supplementary_displays/fixed_moment_reference/` contains
the standalone diagnostic source, full combined-moment derivation fragment,
16 original figure/table assets and a SHA-256 preservation record. The
original source snapshot is
`archive/before_fixed_reference_move_2026-10-27.zip` in the thesis folder.

The existing packaging script automatically includes the new supplement
folder at the next requested refresh. The thesis PDF and existing delivery
files have not been rebuilt or changed. The new standalone supplement source
has not been compiled either.

The main report generator defaults to two display methods. Its new
`--displays-only` route updates the affected plots and tables from saved
CSV/JSON summaries without simulation, fitting, bootstrap sampling or result
writes. The extra-display generator and calibration-sensitivity table reporter
also use two-test labels. Updated display evidence matches the reduced tables.
Original four-rule evidence remains in the saved experiment outputs.

## Validation

- All active LaTeX inputs, graphics and cross-reference labels resolve.
- Source environments and braces are checked without compiling.
- No fixed-reference rule remains in active manuscript text or included tables.
  Ordinary references to probability distributions and RQ1 moment targets stay.
- All 348 rate points in the five affected plot definitions match saved values
  exactly; only Wald and Expanded Welch are present.
- Retained cells in the rate, diagnostic, null-SD and construction tables
  are identical to their pre-move values.
- The 14 initially preserved assets are byte-identical; two additional
  sensitivity tables retain their original headers in the supplement.
- All 7,381 saved CSV/JSON evidence files are byte-identical.
- Protected Chapters 2--4, Appendix A and RQ1 figure assets are unchanged.
- Existing tests: approximation redesign 8; manuscript consistency 5;
  calibration sensitivity 7; ratio displays 7; delivery packaging 11.
- Revised null, nominal-power and calibrated-power plot images were inspected.
  Page layout and pagination await the next requested thesis rebuild.
