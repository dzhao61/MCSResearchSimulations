# Calibration sensitivity revision — 23 October 2026

## Scope and preservation

Implemented the approved six-case sensitivity check in the independent redesign copy. The pre-revision sources, figures and PDF are preserved in `archive/before_calibration_sensitivity_2026-10-22.zip`. The base sampling kernel and its source fingerprint are unchanged. Chapters 2–4 and Appendix A remain protected. Historical working drafts and the original workspace are preserved.

The new sampler is `WelchSatterthwaiteMI/experiments/calibration_sensitivity.py`; its reporting and bootstrap code is `report_calibration_sensitivity.py`. Evidence is isolated under `results/approximation_redesign/calibration_sensitivity/`. The original 366 evaluation settings, 186 fitting settings and 55.2 million pairs remain separate from the extension's six fitting and six validation batches, which add 1.2 million pairs. No alternative population or saved alternative sample was changed.

## Design and findings

For A/B/C at two and four original null SDs, the upper null sets both MI values to the fixed alternative's larger MI. Dimensions, margins, construction and sample sizes are retained. Each upper null has 100,000 fresh fitting and 100,000 independent validation pairs. Every case is retained. The pilot used separate streams and contributes no reported evidence.

Both calibrations are compared on the same saved alternatives and evaluated at both lower and upper nulls. The 1,000-repetition bootstrap resamples fitting pairs jointly across methods, shares each lower fitting draw across its two alternatives, and resamples the eight paired evaluation decisions jointly. Power-rate intervals, paired contrasts with all comparators, and changes in gains are saved. Cross-null rate intervals are conditional Wilson intervals, with validity counts.

Expanded Welch minus Wald power, in percentage points:

| Setting | Lower-null calibration | Upper-null calibration |
| --- | ---: | ---: |
| A, 2 SD | +3.580 | −0.757 |
| A, 4 SD | +4.007 | +0.180 |
| B, 2 SD | +1.112 | +0.049 |
| B, 4 SD | +3.924 | −0.390 |
| C, 2 SD | +0.044 | −0.057 |
| C, 4 SD | +0.018 | −0.013 |

The appendix retains all rates and cross-null comparisons. The main table reports six paired contrasts and bootstrap intervals, without claiming every gain reverses. Matching the lower null does not match rejection at another equal-MI population; two endpoints also do not establish global composite-null size control. The abstract, introduction, discussion and conclusion now reflect this population dependence.

## Approximation and dependence diagnostics

The bottom row of the existing moment plots now includes mean estimated component df divided by the sampling-moment target. Curves are shown only where all component df estimates are positive and finite; conditional summaries retain inclusion counts. Axis limits include the full added curves. Plot dimensions and font sizes are retained. At A, the P-component mean is approximately 6.52 against target 14.81; at C, ratios are about 99%. The manuscript distinguishes this target from an exact Student t reference.

The printed appendix correlation is now Spearman correlation between the absolute difference centred at its sampling mean and the standard error. All 100,000 pairs are included in each printed case. The original signed correlations remain in the base CSV. The same-skew 2×2, n=100 example has signed correlation approximately −0.001 but magnitude rank correlation 0.547, illustrating why signed symmetry cannot establish independence.

## Writing and structure

Applied the current AGENTS instructions and the prior readability review: direct scientific claims, mechanism tied to the quantities being compared, connected prose, short captions, and scientific construction details in the manuscript. The core derivations are unchanged. The false-positive interpretation allows possible compensation between errors without assigning a sole causal explanation.

The main sequence remains approximation accuracy, false positives and power. One compact six-row sensitivity table replaces the two detailed main-text calibrated-power tables; those tables are preserved in Appendix C. Repeated explanations were trimmed to avoid spillover pages. The final manuscript has 108 pages versus 104 before this revision; Chapters 5–7 still occupy 6, 13 and 3 pages (22 combined). The four additional pages are experimental details and appendix evidence. The main text remains 57 pages.

## Validation

The 1.2 million new pairs passed all chunk hash/dimension checks, validity and p-value checks, and independent count/probability-formula reconstruction for 96 pairs. This is additional to the unchanged base audit's 4,416 independently reconstructed pairs. Local suites passed 273 tests: 221 experiment, 27 estimator, 17 application and 8 packaging. Five sensitivity tests check construction/stream independence, strict ties, joint resampling, conditional-mean plotting and agreement of every reported power rate with the separate decision API.

Final PDF rendering, preservation, archive consistency and isolated source/package checks are recorded in `REDESIGN_VERIFICATION.json` after delivery refresh.

The final changed pages were rendered and inspected, including the six-row sensitivity table, magnitude-correlation table, cross-null table and all three revised moment plots. The final build has no LaTeX warnings. All 30,042 original files again match their hashes. The delivery consistency check passes. Extracting both delivery archives and running their suites passes 183 tests (139 experiment, 27 estimator, 17 application). Building the extracted source with the documented output directories gives PDF text identical to the delivery PDF. The source ZIP, experiment supplement and checksums were refreshed together. Reproducible results and the large supplement remain excluded from Git under the existing ignore rules. No commit was made in this revision.
