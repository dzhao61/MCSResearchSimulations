# Saddlepoint MI Validation Summary

Profile: `focused`. Null replicates per configuration: `100`. JIDT-shuffled replicates per configuration: `0`. JIDT shuffles per p-value: `1000`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_nominal_mean_abs_calibration_error | chi2_dynamic_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_nominal_within_20pct_fraction | chi2_dynamic_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.035 | 0.0725 | 0.05917 | 0.0725 |  | 0.3333 | 0.08333 | 0.08333 | 0.08333 |  |
| 0.05 | 0.02 | 0.035 | 0.03333 | 0.035 |  | 0.4167 | 0.25 | 0.25 | 0.25 |  |
| 0.01 | 0.0075 | 0.009167 | 0.009167 | 0.009167 |  | 0.3333 | 0.3333 | 0.3333 | 0.3333 |  |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than nominal chi-squared: `nan`.
Median fraction of tables where saddlepoint/exact was closer to JIDT than dynamic chi-squared: `nan`.
Median absolute p-value error versus JIDT: saddlepoint/exact `nan`, nominal chi-squared `nan`, dynamic chi-squared `nan`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_than_chi2_nominal_fraction | saddle_closer_than_chi2_dynamic_fraction | mae_saddle_vs_jidt | mae_chi2_nominal_vs_jidt | mae_chi2_dynamic_vs_jidt |
| --- | --- | --- | --- | --- | --- |
| 2x2_N50_balanced |  |  |  |  |  |
| 2x2_N50_mild |  |  |  |  |  |
| 2x2_N50_strong |  |  |  |  |  |
| 3x3_N50_balanced |  |  |  |  |  |
| 3x3_N50_mild |  |  |  |  |  |

## Worst Nominal Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_nominal_05 | fpr_chi2_dynamic_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- | --- |
| 3x3_N50_mild | 0.08 | 0.11 | 0.11 |  | 0.03 | 0.06 |
| 6x3_N50_strong | 0.05 | 0 | 0.01 |  | 0 | 0.05 |
| 8x3_N50_balanced | 0.07 | 0.1 | 0.11 |  | 0.02 | 0.05 |
| 8x3_N50_strong | 0.06 | 0 | 0.02 |  | 0.01 | 0.05 |
| 3x3_N50_strong | 0.01 | 0.01 | 0.01 |  | 0.04 | 0.04 |

## Runtime
Median per-table times: saddlepoint/exact `0.0009953s`, nominal/dynamic chi-squared `3.604e-05s`, low-shuffle JIDT `nans`.
Saddlepoint/exact is slower than this low-shuffle JIDT setting on `0` of `0` configurations with JIDT timings. The advantage being tested here is deterministic fixed-margin tail resolution and agreement with high-shuffle anchors, not beating tiny-shuffle JIDT on every dense balanced table.
| name | median_saddle_time_s | median_jidt_time_s |
| --- | --- | --- |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small. Nominal chi-squared uses configured alphabet size; dynamic chi-squared uses observed nonempty rows and columns.
