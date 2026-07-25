# Saddlepoint MI Validation Summary

Profile: `robust`. Null replicates per configuration: `3`. JIDT-shuffled replicates per configuration: `1`. JIDT shuffles per p-value: `1000`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_nominal_mean_abs_calibration_error | chi2_dynamic_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_nominal_within_20pct_fraction | chi2_dynamic_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.1254 | 0.127 | 0.1302 | 0.127 | 0.1667 | 0 | 0 | 0 | 0 | 0 |
| 0.05 | 0.075 | 0.06944 | 0.07222 | 0.06944 | 0.09286 | 0 | 0 | 0 | 0 | 0 |
| 0.01 | 0.02119 | 0.02119 | 0.02492 | 0.02119 | 0.03333 | 0 | 0 | 0 | 0 | 0 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than nominal chi-squared: `1.000`.
Median fraction of tables where saddlepoint/exact was closer to JIDT than dynamic chi-squared: `1.000`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.0056`, nominal chi-squared `0.0542`, dynamic chi-squared `0.0520`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_than_chi2_nominal_fraction | saddle_closer_than_chi2_dynamic_fraction | mae_saddle_vs_jidt | mae_chi2_nominal_vs_jidt | mae_chi2_dynamic_vs_jidt |
| --- | --- | --- | --- | --- | --- |
| 10x3_N120_balanced | 1 | 1 | 0.004142 | 0.09973 | 0.09973 |
| 4x3_N250_mild | 1 | 1 | 0.003873 | 0.05245 | 0.05245 |
| 4x3_N60_strong | 1 | 1 | 0 | 0.0008114 | 0.01395 |
| 4x3_N60_mild | 1 | 1 | 0.01543 | 0.213 | 0.213 |
| 4x3_N60_balanced | 1 | 1 | 0.003066 | 0.04372 | 0.04372 |

## Worst Nominal Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_nominal_05 | fpr_chi2_dynamic_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- | --- |
| 8x3_N120_balanced | 0 | 0.3333 | 0.3333 | 0 | 0.05 | 0.2833 |
| 3x2_N250_balanced | 0.3333 | 0.3333 | 0.3333 | 0 | 0.2833 | 0.2833 |
| 6x3_N30_balanced | 0 | 0.3333 | 0.3333 | 0 | 0.05 | 0.2833 |
| 3x3_N120_balanced | 0.3333 | 0.3333 | 0.3333 | 1 | 0.2833 | 0.2833 |
| 10x3_N60_balanced | 0 | 0.3333 | 0.3333 | 0 | 0.05 | 0.2833 |

## Runtime
Median per-table times: saddlepoint/exact `0.0156s`, nominal/dynamic chi-squared `4.094e-05s`, low-shuffle JIDT `0.001045s`.
Saddlepoint/exact is slower than this low-shuffle JIDT setting on `57` of `84` configurations with JIDT timings. The advantage being tested here is deterministic fixed-margin tail resolution and agreement with high-shuffle anchors, not beating tiny-shuffle JIDT on every dense balanced table.
| name | median_saddle_time_s | median_jidt_time_s |
| --- | --- | --- |
| 6x3_N250_balanced | 149.4 | 0.003598 |
| 4x3_N250_balanced | 143.6 | 0.003568 |
| 8x3_N250_balanced | 123.8 | 0.003613 |
| 3x3_N250_balanced | 88.96 | 0.003682 |
| 10x3_N250_balanced | 84.52 | 0.003652 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small. Nominal chi-squared uses configured alphabet size; dynamic chi-squared uses observed nonempty rows and columns.
