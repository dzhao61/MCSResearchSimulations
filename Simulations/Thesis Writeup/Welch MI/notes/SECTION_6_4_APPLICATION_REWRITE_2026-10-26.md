# Section 6.4 application rewrite — 26 October 2026

The user requested a revision incorporating the clarified meanings of the two comparisons, P/Q, the p-values and small estimated degrees of freedom.

The preceding 103-page source, PDF and application regression test are preserved in `archive/before_section_6_4_application_rewrite_2026-10-26.zip`.

## Exposition and tables

- The opening identifies one testing question applied to two predictors. Each predictor has its own joint distributions P (new visitors) and Q (returning visitors), with the same visitor groups and purchase outcome. Month is the primary example; weekend supplies a weak-association example.
- The sample sizes, excluded visitor category, independent-session assumption, source citation, ten month categories, sparse February row, complete weekend table and bias corrections are retained.
- Table 6.8 now shows corrected MI for both groups, corrected difference, shared standard error and shared T. Their roles and units are introduced before the table. The original displayed month statistic is unchanged.
- The normal and Student t reference distributions are introduced before the test results. Table 6.9 separates the p-values and Expanded Welch degrees of freedom from effect estimation.
- Month's rejection is explained through the difference being about 4.07 standard errors from zero. The heavier Student t tails explain its larger p-value.
- Weekend's difference is about 0.056 standard errors from zero, explaining both high p-values. The low df are explained through substantial estimated sampling uncertainty relative to the variance coefficients, with a link to Figure 6.3. The qualification about unknown population tables and the sampling-moment target remains.
- All original MI values, differences, standard errors, statistics, p-values, estimated df and Holm-adjusted p-values are preserved. The six-comparison family is unchanged. Lack of evidence of a weekend difference is explicitly distinguished from equality.

The existing independent-data regression check now verifies the estimate and decision rows separately. It still recomputes all underlying values from the original count tables, rather than accepting the new formatting as evidence of correctness. No estimator or application calculation changes.

The application remains two pages (printed pages 58–59). The manuscript remains 103 pages, including 64 pages of main text and 17 pages in Chapter 6. Fonts, page dimensions and figure assets are unchanged. All 17 application tests, five manuscript-consistency tests and eight packaging tests pass. Final archival, source-build, preservation and visual checks are recorded in `REDESIGN_VERIFICATION.json`.

The final two-page application was rendered and reviewed. The main PDF builds without warnings; the source archive builds independently to identical extracted PDF text. The delivery check verifies the PDF, source, experiment archive and checksums against current inputs. All application datasets and calculation files are byte-identical. Chapter 6 before Section 6.4 and all 93 other manuscript/figure inputs are unchanged. The only code change adapts the existing application regression check to the two-table presentation.
