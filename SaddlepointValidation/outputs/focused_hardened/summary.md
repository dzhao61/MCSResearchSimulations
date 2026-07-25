# Saddlepoint MI Validation Summary

Profile: `focused`. Null replicates per configuration: `1000`. JIDT-shuffled replicates per configuration: `100`. JIDT shuffles per p-value: `5000`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_nominal_mean_abs_calibration_error | chi2_dynamic_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_nominal_within_20pct_fraction | chi2_dynamic_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.02258 | 0.06058 | 0.05267 | 0.06058 | 0.02833 | 0.5 | 0.1667 | 0.1667 | 0.1667 | 0.4167 |
| 0.05 | 0.0125 | 0.034 | 0.02917 | 0.034 | 0.01917 | 0.5 | 0.1667 | 0.1667 | 0.1667 | 0.4167 |
| 0.01 | 0.002917 | 0.006833 | 0.006333 | 0.006833 | 0.005833 | 0.4167 | 0.25 | 0.25 | 0.25 | 0.5 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than nominal chi-squared: `0.985`.
Median fraction of tables where saddlepoint/exact was closer to JIDT than dynamic chi-squared: `0.985`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.0049`, nominal chi-squared `0.1143`, dynamic chi-squared `0.1021`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_than_chi2_nominal_fraction | saddle_closer_than_chi2_dynamic_fraction | mae_saddle_vs_jidt | mae_chi2_nominal_vs_jidt | mae_chi2_dynamic_vs_jidt |
| --- | --- | --- | --- | --- | --- |
| 2x2_N50_mild | 1 | 1 | 0.003512 | 0.1127 | 0.1127 |
| 2x2_N50_strong | 1 | 1 | 0.001663 | 0.3524 | 0.3524 |
| 6x3_N50_balanced | 1 | 1 | 0.004801 | 0.09663 | 0.09663 |
| 6x3_N50_strong | 1 | 0.99 | 0.003124 | 0.211 | 0.1076 |
| 8x3_N50_balanced | 1 | 1 | 0.00499 | 0.1618 | 0.1618 |

## Worst Nominal Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_nominal_05 | fpr_chi2_dynamic_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- | --- |
| 8x3_N50_balanced | 0.053 | 0.142 | 0.143 | 0.06 | 0.003 | 0.092 |
| 6x3_N50_strong | 0.031 | 0 | 0.02 | 0.03 | 0.019 | 0.05 |
| 8x3_N50_strong | 0.034 | 0 | 0.017 | 0.03 | 0.016 | 0.05 |
| 6x3_N50_balanced | 0.038 | 0.088 | 0.088 | 0.05 | 0.012 | 0.038 |
| 8x3_N50_mild | 0.048 | 0.014 | 0.02 | 0.03 | 0.002 | 0.036 |

## Runtime
Median per-table times: saddlepoint/exact `0.00273s`, nominal/dynamic chi-squared `3.28e-05s`, low-shuffle JIDT `0.002123s`.
Saddlepoint/exact is slower than this low-shuffle JIDT setting on `6` of `12` configurations with JIDT timings. The advantage being tested here is deterministic fixed-margin tail resolution and agreement with high-shuffle anchors, not beating tiny-shuffle JIDT on every dense balanced table.
| name | median_saddle_time_s | median_jidt_time_s |
| --- | --- | --- |
| 8x3_N50_balanced | 0.212 | 0.003248 |
| 6x3_N50_balanced | 0.2067 | 0.002689 |
| 3x3_N50_balanced | 0.1337 | 0.002107 |
| 8x3_N50_mild | 0.0152 | 0.002712 |
| 6x3_N50_mild | 0.01421 | 0.002567 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small. Nominal chi-squared uses configured alphabet size; dynamic chi-squared uses observed nonempty rows and columns.
