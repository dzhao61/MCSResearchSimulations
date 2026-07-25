# Saddlepoint MI Validation Summary

Profile: `focused`. Null replicates per configuration: `40`. JIDT-shuffled replicates per configuration: `20`. JIDT shuffles per p-value: `1000`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.03333 | 0.05833 | 0.04583 | 0.3333 | 0.1667 | 0.4167 |
| 0.05 | 0.03125 | 0.04375 | 0.02917 | 0.08333 | 0.08333 | 0.4167 |
| 0.01 | 0.01583 | 0.01125 | 0.015 | 0 | 0 | 0 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than chi-squared: `0.950`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.0091`, chi-squared `0.1074`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_to_jidt_fraction | mae_saddle_vs_jidt | mae_chi2_vs_jidt |
| --- | --- | --- | --- |
| 3x3_N50_mild | 1 | 0.01222 | 0.09541 |
| 6x3_N50_balanced | 1 | 0.01091 | 0.1111 |
| 6x3_N50_strong | 1 | 0.008049 | 0.205 |
| 8x3_N50_balanced | 1 | 0.01021 | 0.1443 |
| 8x3_N50_strong | 1 | 0.003409 | 0.2106 |

## Worst Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- |
| 8x3_N50_balanced | 0.025 | 0.2 | 0 | 0.025 | 0.15 |
| 2x2_N50_mild | 0.025 | 0.1 | 0.05 | 0.025 | 0.05 |
| 3x3_N50_strong | 0 | 0 | 0 | 0.05 | 0.05 |
| 6x3_N50_mild | 0.025 | 0 | 0 | 0.025 | 0.05 |
| 6x3_N50_strong | 0.025 | 0 | 0.05 | 0.025 | 0.05 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small.
