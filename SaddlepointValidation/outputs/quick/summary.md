# Saddlepoint MI Validation Summary

Profile: `quick`. Null replicates per configuration: `4`. JIDT-shuffled replicates per configuration: `4`. JIDT shuffles per p-value: `500`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.1438 | 0.125 | 0.1125 | 0 | 0 | 0 |
| 0.05 | 0.1 | 0.05938 | 0.07812 | 0 | 0 | 0 |
| 0.01 | 0.04 | 0.01 | 0.01 | 0 | 0 | 0 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than chi-squared: `1.000`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.0145`, chi-squared `0.1206`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_to_jidt_fraction | mae_saddle_vs_jidt | mae_chi2_vs_jidt |
| --- | --- | --- | --- |
| 2x2_N120_strong | 1 | 0.01763 | 0.2689 |
| 2x2_N50_balanced | 1 | 0.01927 | 0.0845 |
| 2x2_N50_strong | 1 | 0.009008 | 0.2757 |
| 3x3_N120_balanced | 1 | 0.01449 | 0.02276 |
| 3x3_N120_strong | 1 | 0.01282 | 0.07715 |

## Worst Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- |
| 8x3_N50_balanced | 0 | 0.25 | 0 | 0.05 | 0.2 |
| 2x2_N120_balanced | 0 | 0 | 0 | 0.05 | 0.05 |
| 2x2_N120_strong | 0 | 0 | 0 | 0.05 | 0.05 |
| 2x2_N50_balanced | 0 | 0 | 0 | 0.05 | 0.05 |
| 2x2_N50_strong | 0 | 0 | 0 | 0.05 | 0.05 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small.
