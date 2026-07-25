# Saddlepoint MI Validation Summary

Profile: `standard`. Null replicates per configuration: `3`. JIDT-shuffled replicates per configuration: `3`. JIDT shuffles per p-value: `500`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.1519 | 0.1315 | 0.1352 | 0 | 0 | 0 |
| 0.05 | 0.07593 | 0.09167 | 0.05648 | 0 | 0 | 0 |
| 0.01 | 0.03611 | 0.01 | 0.01 | 0 | 0 | 0 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than chi-squared: `1.000`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.0132`, chi-squared `0.0698`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_to_jidt_fraction | mae_saddle_vs_jidt | mae_chi2_vs_jidt |
| --- | --- | --- | --- |
| 2x2_N120_balanced | 1 | 0.004711 | 0.07343 |
| 4x3_N50_strong | 1 | 0.008006 | 0.07249 |
| 4x3_N50_balanced | 1 | 0.01331 | 0.05287 |
| 4x3_N120_mild | 1 | 0.03475 | 0.1015 |
| 2x2_N120_mild | 1 | 0.008993 | 0.06243 |

## Worst Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- |
| 6x3_N50_balanced | 0 | 0.6667 | 0 | 0.05 | 0.6167 |
| 4x3_N120_balanced | 0.3333 | 0.3333 | 0.3333 | 0.2833 | 0.2833 |
| 8x3_N50_balanced | 0 | 0.3333 | 0 | 0.05 | 0.2833 |
| 3x3_N50_balanced | 0 | 0.3333 | 0 | 0.05 | 0.2833 |
| 3x2_N120_mild | 0 | 0.3333 | 0 | 0.05 | 0.2833 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small.
