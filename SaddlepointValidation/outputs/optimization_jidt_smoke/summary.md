# Saddlepoint MI Validation Summary

Profile: `focused`. Null replicates per configuration: `1`. JIDT-shuffled replicates per configuration: `1`. JIDT shuffles per p-value: `5`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_nominal_mean_abs_calibration_error | chi2_dynamic_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_nominal_within_20pct_fraction | chi2_dynamic_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.2333 | 0.1 | 0.1667 | 0.1 | 0.1667 | 0 | 0 | 0 | 0 | 0 |
| 0.05 | 0.125 | 0.05 | 0.05 | 0.05 | 0.125 | 0 | 0 | 0 | 0 | 0 |
| 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.09167 | 0 | 0 | 0 | 0 | 0 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than nominal chi-squared: `1.000`.
Median fraction of tables where saddlepoint/exact was closer to JIDT than dynamic chi-squared: `1.000`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.1148`, nominal chi-squared `0.1883`, dynamic chi-squared `0.1438`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_than_chi2_nominal_fraction | saddle_closer_than_chi2_dynamic_fraction | mae_saddle_vs_jidt | mae_chi2_nominal_vs_jidt | mae_chi2_dynamic_vs_jidt |
| --- | --- | --- | --- | --- | --- |
| 2x2_N50_balanced | 1 | 1 | 0.008837 | 0.09039 | 0.09039 |
| 2x2_N50_strong | 1 | 1 | 0 | 0.596 | 0.596 |
| 3x3_N50_balanced | 1 | 1 | 0.1639 | 0.1779 | 0.1779 |
| 3x3_N50_strong | 1 | 1 | 0 | 0.1987 | 0.1987 |
| 6x3_N50_balanced | 1 | 1 | 0.07348 | 0.2118 | 0.2118 |

## Worst Nominal Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_nominal_05 | fpr_chi2_dynamic_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- | --- |
| 2x2_N50_balanced | 0 | 0 | 0 | 0 | 0.05 | 0.05 |
| 2x2_N50_mild | 0 | 0 | 0 | 0 | 0.05 | 0.05 |
| 2x2_N50_strong | 0 | 0 | 0 | 0 | 0.05 | 0.05 |
| 3x3_N50_balanced | 0 | 0 | 0 | 0 | 0.05 | 0.05 |
| 3x3_N50_mild | 0 | 0 | 0 | 0 | 0.05 | 0.05 |

## Runtime
Median per-table times: saddlepoint/exact `0.001298s`, nominal/dynamic chi-squared `4.44e-05s`, low-shuffle JIDT `8.504e-05s`.
Saddlepoint/exact is slower than this low-shuffle JIDT setting on `11` of `12` configurations with JIDT timings. The advantage being tested here is deterministic fixed-margin tail resolution and agreement with high-shuffle anchors, not beating tiny-shuffle JIDT on every dense balanced table.
| name | median_saddle_time_s | median_jidt_time_s |
| --- | --- | --- |
| 3x3_N50_balanced | 0.01447 | 8.4e-05 |
| 8x3_N50_balanced | 0.0117 | 0.0001096 |
| 6x3_N50_balanced | 0.01134 | 9.354e-05 |
| 3x3_N50_mild | 0.00329 | 8.283e-05 |
| 8x3_N50_mild | 0.002204 | 8.608e-05 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small. Nominal chi-squared uses configured alphabet size; dynamic chi-squared uses observed nonempty rows and columns.
