# Figure and table coverage audit — 28 October 2026

## What the earlier reviews established

The language review explicitly covered the labels of all eight included figures and the wording of the included tables. Its R12 finding identified the lower-panel label “Valid” in the two false-positive figures. Figures 6.4–6.5 were therefore not entirely omitted. The first-reader revision subsequently explained why failed calculations can lower the reported rejection rate, but did not implement R12 or add a detailed reading of these two plots.

The requested PDF build checked all pages for formatting, with selected pages examined at greater resolution. That establishes layout coverage, not a complete interpretation of every plotted pattern. The earlier results-display review also assessed evidence placement; its older figure/table numbering should not be used as the current inventory.

The gap is uneven substantive attention: Figures 6.1–6.3 and the power comparison received much more detailed interpretation than the broad false-positive figures. The prior language findings and the eleven first-reader issues were separate lists; completing the latter did not implement every former recommendation. The record should not imply otherwise.

## Current audit scope

The delivered 99-page PDF contains **8 figures and 27 tables**, confirmed against the current compiled lists. Each is listed below. This pass read the displayed content, its introduction and adjacent interpretation, checked its purpose in the argument, and inspected the corresponding rendered page. This is a comprehension/evidence-placement audit, not a fresh numerical reproduction of all tables. For Figures 6.4–6.5, the numerical examples below were additionally checked against saved configuration and rejection summaries. No simulations, fitting or bootstraps were run.

### Figures

| Figure | Purpose and current assessment | Follow-up |
| --- | --- | --- |
| 2.1 | Shows how Student t tail weight and the rejection cutoff depend on degrees of freedom. The surrounding text explains the mechanism and the large-df limit. | No substantive repair identified. |
| 6.1 | Separates mean error, population sampling-variance prediction and sample-based sampling-variance prediction. The three rows, benchmarks and an explicit numerical example are explained. | No priority gap. Preserve the distinct rows and common variance benchmark. |
| 6.2 | Separates first-order and mean sampled component df relative to their moment targets. The text gives the squared-mean mechanism and an inclusion rule for missing bottom-row values. | No priority gap. Missing early values are intentional, not evidence of numerical zero. |
| 6.3 | Checks the near-independence moment predictions and distinguishes estimated df, moment target and first-order df. The low-MI result is explained. The visible departure of the near-independence variance prediction at larger MI is not directly unpacked. | Add a brief reading of that departure and the local scope of this prediction. Distinguish it from the different first-order tau-squared prediction discussed subsequently. |
| 6.4 | Broad uniform-margin false-positive and validity curves. The text supplies the denominator/validity convention but gives little panel-specific interpretation. | High priority: explain improvement versus increased conservatism, non-monotone behaviour, the 5% reference, and convergence towards 5% in these plotted settings. Rename “Valid” to “Valid fraction”. |
| 6.5 | Corresponding different-skew comparison. The later 16-by-16 diagnostic explains one important case, but the connection to this figure is indirect. | High priority: explicitly connect severe 16-by-16 over-rejection to the later bias evidence; distinguish this from the conservative smaller-table region. Explain that incomplete validity affects some smallest-sample points. |
| 6.6 | Nominal power for A–C. The text defines the effect axis, shows an A example, explains B's initial decline and quantifies C's small difference. | Substantively covered. A–C require the nearby definitions; preserve these. |
| 6.7 | Lower-null calibrated power on the same alternatives. The text explains calibration, validation, the reversal at A, setting sensitivity and the persistence of B's distorted curve. | Substantively covered. A short B/C comparison could improve the immediate graph reading, but is secondary. |

Figures 6.4–6.5 also use automatically different vertical limits between panels and between the two figures. A visually higher curve need not mean a higher numerical rate in another panel. The 5% line is not labelled inside the panels, although the body explains the nominal target. Any revision should make the reference and scales explicit. A single universal limit would compress the smaller rates, so do not impose one without evaluating readability. Percent-versus-fraction labels should be consistent and explicit. The small validity strips need legible labels; neither their presence nor near-one values establishes independence or good calibration.

### Tables

| Table | Purpose and current assessment | Follow-up |
| --- | --- | --- |
| 3.1 | Distinguishes observation-level variance, estimated coefficients and sampling variances before the derivation. | Adequate; retain at this early location. |
| 4.1 | Distinguishes the moment target, first-order value and sample estimate by role and inputs. | Adequate; repaired typography is legible. |
| 4.2 | Collects the operational algorithm after the worked example. | Adequate in context; not intended as a standalone derivation. |
| 5.1 | Specifies both populations' margins for each regime. | Adequate; the preceding definition of the margin vector is necessary and present. |
| 5.2 | Specifies the two grids and their parameters. | Adequate; the nearby paragraph states all three regimes and equal sample sizes. |
| 5.3 | Defines A–C and fitted null SDs before the power comparison. | Adequate. |
| 5.4 | Separates the fixed alternative from lower/upper calibration nulls. | Adequate; h and sigma-zero are introduced before use. |
| 5.5 | Defines performance measures and their denominators. | Adequate; validity and finite-value rules are explained beside it. |
| 6.1 | Gives numeric component moments/df at three MI levels. All columns are explained in the body, but six compact diagnostic columns require considerable decoding. | Secondary readability issue: group moment ratios and df comparisons or improve headers; preserve its scientific role and values. |
| 6.2 | Classifies closeness to 5% over 120 settings. | Adequate after the explicit tolerance rule; counts are not weighted by practical importance. |
| 6.3 | Links difference bias and squared-standard-error accuracy at selected settings. | Adequate; the shared statistic and benchmark are now explicit. |
| 6.4 | Gives corresponding rejection rates and intervals. | Expand sparse-case labels such as “16, same, 1,000”; this prior T01 finding remains open. |
| 6.5 | Checks stronger common MI for A/B. | Adequate in context: the body says rates/intervals are percentages and explains retained sizes/margins. |
| 6.6 | Compares signed power gains under lower/upper calibration. | Adequate: direction, units, alternative and intervals are explained. |
| 6.7 | Gives X, Y, P, Q and H0 for the two shopping questions. | Adequate; prevents population/variable confusion. |
| 6.8 | Shows group MI estimates, difference, standard error and T. | Adequate; units and subtraction direction are explicit. |
| 6.9 | Shows df and p-values from each test. | Adequate; both rejection and non-rejection are interpreted with their limits. |
| B.1 | Supplies exact grids for replication beyond the compact design overview. | Adequate; technical detail belongs here. |
| C.1 | Summarises scaled mean-error ranges relevant to a possible correction of V-hat. | Adequate for an appendix; the range deliberately pools multiple conditions. |
| C.2 | Shows spread of component df and its target. | Expand compressed setting labels; identify percentile range as component-df spread rather than uncertainty on a mean. The latter distinction is already in the body. |
| C.3 | Shows shared-estimator diagnostics and combined df. | Expand setting labels; replace “Median df” with “Median combined df” and “Skew” with “Skewness”; explain skewness rather than just repeating “Skew describes the difference estimates”. These earlier T01/T03/C03 issues remain. |
| C.4 | Reports fitted null SDs and their Monte Carlo uncertainty. | Expand “MCSE” to “Monte Carlo SE”, as already recommended in T04. |
| C.5 | Shows paired nominal/calibrated power differences at h=2. | Caption should explicitly say “power”; body phrase “Wald contrasts” later is also ambiguous about direction. Earlier C04 remains open. |
| C.6 | Gives absolute power behind the signed calibration comparisons. | Adequate; define “null” as fitting null in the header if revising these tables together. |
| C.7 | Cross-validates both calibrations at both equal-MI settings. | Add one worked row comparison. The current paragraph states the procedure/scope but leaves the key magnitude of transfer failure to the reader. |
| C.8 | Gives wrong-direction counts among rejections at a negative true difference. | Adequate; count denominator and bias-shift mechanism are explained. |
| C.9 | Reports the complete exploratory family and Holm adjustment. | Substantively covered; the last algorithm sentence still has the ambiguous “by that value” identified previously in C05. |

## Concrete readings missing from Figures 6.4–6.5

- **Improvement and increased conservatism both occur.** In Figure 6.4's uniform 4-by-4 panel, n=20 gives 8.352% Wald rejection and 4.897% Expanded Welch rejection. At n=100, the same panel instead gives 2.260% and 1.546%: lowering rejection then moves farther below 5%. All outputs are valid at both settings, so this contrast is not caused by invalid results.
- **Smallest-sample validity matters at particular points.** In Figure 6.5's different-skew 4-by-4 panel at n=10, Expanded Welch's all-repetition rate is 4.791%, but only 75.564% of outputs are valid. Its apparent closeness to 5% must be read alongside that loss of usable results. This does not by itself quantify a causal contribution of invalidity to the difference between methods.
- **Sparse-table failure persists despite the larger cutoff.** In Figure 6.5's 16-by-16 panel at n=1,000, Wald rejects 26.011% and Expanded Welch 24.836%; both are valid in every repetition. The later diagnostic identifies large positive difference bias. It should be explicitly connected back to this plot.
- **More observations do not yield a monotone approach over the whole grid.** Uniform 16-by-16 rates cross the 5% line repeatedly, while different-skew 16-by-16 rates remain around 20–27% over several intermediate sample sizes before falling. The text should describe these visible patterns. Explaining every turn causally would require additional diagnostics; the present bias/variance examples do not establish a mechanism for every point.
- **Large-sample convergence is visible within this design.** At n=50,000 all eight panels' two-method rates lie between 4.605% and 5.034%. This is a result for the displayed settings, not uniform control over the entire composite null.

## Another important table example

Table C.7, A at h=2: lower-null fitting gives 4.93%/4.99% rejection at the lower evaluation null but 11.20%/13.71% at the upper evaluation null (Wald/Expanded Welch). Upper-null fitting instead gives 4.87%/4.84% at its matching upper null and 1.63%/0.79% at the lower null. One such comparison would make the calibration-sensitivity limitation concrete without reciting the full table.

## Scope of changes in this turn

Only this internal audit note was added. No manuscript, plot, reporter, results, PDF or delivery files were changed. No build was run. The checked delivery PDF retains SHA-256 e1cd07279e5f7ccb93ae187d0e167e2d8b5b91fc7b839180550fc172bec6738b.

Priority for an authorized editing pass: first Figures 6.4–6.5 and their immediate explanation; then Figure 6.3 and Table C.7; then the outstanding compact-label and wording repairs. Update active generators with any label edits, retain numerical data, and wait for an explicit request before rebuilding the PDF.
