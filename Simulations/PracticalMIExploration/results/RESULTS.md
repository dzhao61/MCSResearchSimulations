# Exploratory application: Normal Wald versus Expanded Welch

Six comparisons were specified before method p-values were calculated.
P/Q labels and preparation are in PROTOCOL.md. Differences are P minus Q in nats.
The thesis, methods, prior simulations and working drafts are unchanged.

## Full-data comparisons

| Comparison | P / Q sample sizes | Corrected MI P / Q | Difference | Wald p | Expanded p | Expanded df | Empty cells P / Q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Adult: education | 16192 / 32650 | 0.03902 / 0.07616 | -0.03714 | 1.89e-34 | 4.93e-33 | 1644.8 | 2 / 0 |
| Adult: occupation | 14919 / 31114 | 0.03542 / 0.07724 | -0.04183 | 1.184e-44 | 1.635e-42 | 1850.0 | 2 / 1 |
| Online Shoppers: Month | 1694 / 10551 | 0.00432 / 0.01788 | -0.01356 | 4.714e-05 | 0.0003726 | 26.8 | 1 / 0 |
| Online Shoppers: Weekend | 1694 / 10551 | 0.00066 / 0.00073 | -0.00006 | 0.9554 | 0.9601 | 2.2 | 0 / 0 |
| Student Performance: studytime | 423 / 226 | 0.01698 / 0.00146 | 0.01551 | 0.1982 | 0.2339 | 8.1 | 1 / 0 |
| Student Performance: Medu | 423 / 226 | 0.00317 / 0.00125 | 0.00192 | 0.8361 | 0.8468 | 3.8 | 1 / 1 |

Both methods use the same effect estimate and standard error. Intervals are
pointwise approximations, not multiple-comparison-adjusted intervals.

| Comparison | Raw 5% decisions Wald / Expanded | Holm-adjusted p Wald / Expanded | Holm 5% decisions Wald / Expanded |
| --- | --- | --- | --- |
| Adult: education | reject / reject | 9.449e-34 / 2.465e-32 | reject / reject |
| Adult: occupation | reject / reject | 7.105e-44 / 9.813e-42 | reject / reject |
| Online Shoppers: Month | reject / reject | 0.0001886 / 0.001491 | reject / reject |
| Online Shoppers: Weekend | retain / retain | 1 / 1 | retain / retain |
| Student Performance: studytime | retain / retain | 0.5946 / 0.7016 | retain / retain |
| Student Performance: Medu | retain / retain | 1 / 1 | retain / retain |

Here 'retain' means do not reject equal MI, not proof of equality.

## Subset decision stability

Each size uses 5000 uniform subsets without replacement per group.
The two methods see the same subset pairs. Frequencies are unconditional:
invalid calculations remain in the denominator and are reported separately.

| Comparison | n each | Rejection % Wald / Expanded | Valid % Wald / Expanded | Wald-only decisions with both valid | Wald reject / Expanded invalid | Median Expanded df |
| --- | --- | --- | --- | --- | --- | --- |
| adult_education | 50 | 14.02 / 10.42 | 100.00 / 99.70 | 166 | 14 | 15.83 |
| adult_education | 100 | 17.84 / 14.40 | 100.00 / 100.00 | 172 | 0 | 21.07 |
| adult_education | 200 | 25.72 / 22.96 | 100.00 / 100.00 | 138 | 0 | 32.01 |
| adult_education | 500 | 50.34 / 48.70 | 100.00 / 100.00 | 82 | 0 | 66.79 |
| adult_education | 1000 | 73.30 / 72.76 | 100.00 / 100.00 | 27 | 0 | 128.86 |
| adult_education | 2000 | 95.52 / 95.44 | 100.00 / 100.00 | 4 | 0 | 253.48 |
| adult_education | 5000 | 100.00 / 100.00 | 100.00 / 100.00 | 0 | 0 | 632.97 |
| adult_occupation | 50 | 20.54 / 16.22 | 100.00 / 99.64 | 198 | 18 | 16.24 |
| adult_occupation | 100 | 21.44 / 18.02 | 100.00 / 99.98 | 170 | 1 | 20.95 |
| adult_occupation | 200 | 29.68 / 27.16 | 100.00 / 100.00 | 126 | 0 | 34.42 |
| adult_occupation | 500 | 53.68 / 52.50 | 100.00 / 100.00 | 59 | 0 | 78.40 |
| adult_occupation | 1000 | 82.70 / 82.22 | 100.00 / 100.00 | 24 | 0 | 150.54 |
| adult_occupation | 2000 | 99.02 / 99.02 | 100.00 / 100.00 | 0 | 0 | 293.16 |
| adult_occupation | 5000 | 100.00 / 100.00 | 100.00 / 100.00 | 0 | 0 | 716.96 |
| shoppers_month | 50 | 2.52 / 1.28 | 100.00 / 99.92 | 60 | 2 | 7.99 |
| shoppers_month | 100 | 3.00 / 1.72 | 100.00 / 100.00 | 64 | 0 | 9.07 |
| shoppers_month | 200 | 5.86 / 3.58 | 100.00 / 100.00 | 114 | 0 | 11.68 |
| shoppers_month | 500 | 16.86 / 13.22 | 100.00 / 100.00 | 182 | 0 | 18.74 |
| shoppers_month | 1000 | 42.28 / 37.18 | 100.00 / 100.00 | 255 | 0 | 29.86 |
| shoppers_weekend | 50 | 3.88 / 0.98 | 100.00 / 97.94 | 140 | 5 | 0.88 |
| shoppers_weekend | 100 | 1.18 / 0.44 | 100.00 / 97.96 | 36 | 1 | 0.88 |
| shoppers_weekend | 200 | 0.12 / 0.08 | 100.00 / 99.14 | 2 | 0 | 0.94 |
| shoppers_weekend | 500 | 0.08 / 0.00 | 100.00 / 99.80 | 4 | 0 | 1.33 |
| shoppers_weekend | 1000 | 0.02 / 0.00 | 100.00 / 99.98 | 1 | 0 | 2.03 |
| students_studytime | 50 | 2.04 / 0.48 | 100.00 / 98.30 | 63 | 15 | 3.00 |
| students_studytime | 100 | 2.74 / 0.56 | 100.00 / 100.00 | 109 | 0 | 3.83 |
| students_studytime | 200 | 2.34 / 0.52 | 100.00 / 100.00 | 91 | 0 | 5.60 |
| students_maternal_education | 50 | 1.38 / 0.18 | 100.00 / 98.46 | 51 | 9 | 3.14 |
| students_maternal_education | 100 | 0.96 / 0.22 | 100.00 / 100.00 | 37 | 0 | 3.25 |
| students_maternal_education | 200 | 0.56 / 0.12 | 100.00 / 100.00 | 22 | 0 | 3.97 |

## Reading the evidence

These are practical demonstrations, not calibration benchmarks: true population
MI is unknown. A larger p-value, fewer rejections or a disagreement does not show
that Expanded Welch is more accurate. Overlapping subsets of the same data do
not establish power, false-positive rates or independent replication.

Full-data and subset analyses answer different questions; subsets deliberately
balance group sample sizes while the full-data analyses retain natural imbalance.
Holm adjustment applies to the six full-data comparisons separately for each method.
Subset frequencies are descriptive stability measures, not a search for significant
sample sizes or an additional family of scientific discoveries.

Adult is an unweighted survey-derived benchmark. Its survey design and unidentified
duplicate profiles prevent national-population or fully verified independent-person
inference. The two-school data may have within-class dependence. Shoppers has
different users per session by source documentation, but common seasonal effects
are possible. Neither method adjusts for these sampling-design issues.

Empty cells and missing category margins can weaken the fixed-support first-order
approximations. All raw tables and diagnostics are retained; no smoothing is used.
MI also depends on predictor and outcome frequencies, so a group contrast is not
by itself a causal effect or a difference in a classifier's predictive accuracy.

## Sources

- [Adult](https://archive.ics.uci.edu/dataset/2/adult): Becker and Kohavi (1996), doi:10.24432/C5XW20; CC BY 4.0.
- [Online Shoppers](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset): Sakar and Kastro (2018), doi:10.24432/C5F88Q; CC BY 4.0.
- [Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance): Cortez (2008), doi:10.24432/C5TG7T; CC BY 4.0.
