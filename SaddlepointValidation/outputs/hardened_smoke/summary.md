# Saddlepoint MI Validation Summary

Profile: `focused`. Null replicates per configuration: `4`. JIDT-shuffled replicates per configuration: `2`. JIDT shuffles per p-value: `100`.

## Overall Calibration
| alpha | saddle_mean_abs_calibration_error | chi2_nominal_mean_abs_calibration_error | chi2_dynamic_mean_abs_calibration_error | chi2_mean_abs_calibration_error | jidt_mean_abs_calibration_error | saddle_within_20pct_fraction | chi2_nominal_within_20pct_fraction | chi2_dynamic_within_20pct_fraction | chi2_within_20pct_fraction | jidt_within_20pct_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.1125 | 0.1083 | 0.1083 | 0.1083 | 0.1 | 0 | 0 | 0 | 0 | 0 |
| 0.05 | 0.05 | 0.075 | 0.075 | 0.075 | 0.05 | 0 | 0 | 0 | 0 | 0 |
| 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0 | 0 | 0 | 0 | 0 |

## JIDT Agreement
Median fraction of tables where saddlepoint/exact was closer to JIDT than nominal chi-squared: `1.000`.
Median fraction of tables where saddlepoint/exact was closer to JIDT than dynamic chi-squared: `1.000`.
Median absolute p-value error versus JIDT: saddlepoint/exact `0.0246`, nominal chi-squared `0.1259`, dynamic chi-squared `0.1259`.

## Strongest Saddlepoint Wins Against JIDT
| name | saddle_closer_than_chi2_nominal_fraction | saddle_closer_than_chi2_dynamic_fraction | mae_saddle_vs_jidt | mae_chi2_nominal_vs_jidt | mae_chi2_dynamic_vs_jidt |
| --- | --- | --- | --- | --- | --- |
| 2x2_N50_mild | 1 | 1 | 0.02844 | 0.1434 | 0.1434 |
| 2x2_N50_strong | 1 | 1 | 0.0508 | 0.3886 | 0.3886 |
| 3x3_N50_mild | 1 | 1 | 0.02923 | 0.1797 | 0.1797 |
| 3x3_N50_strong | 1 | 1 | 0.01702 | 0.09816 | 0.09816 |
| 6x3_N50_balanced | 1 | 1 | 0.02903 | 0.1293 | 0.1293 |

## Worst Nominal Chi-Squared Calibration Cases At Alpha 0.05
| name | fpr_saddle_05 | fpr_chi2_nominal_05 | fpr_chi2_dynamic_05 | fpr_jidt_05 | saddle_err | chi2_err |
| --- | --- | --- | --- | --- | --- | --- |
| 2x2_N50_mild | 0 | 0.25 | 0.25 | 0 | 0.05 | 0.2 |
| 6x3_N50_balanced | 0 | 0.25 | 0.25 | 0 | 0.05 | 0.2 |
| 2x2_N50_balanced | 0 | 0 | 0 | 0 | 0.05 | 0.05 |
| 2x2_N50_strong | 0 | 0 | 0 | 0 | 0.05 | 0.05 |
| 3x3_N50_balanced | 0 | 0 | 0 | 0 | 0.05 | 0.05 |

## Notes
The saddlepoint column uses the method's tiered rule: exact conditional tails for small-support tables and saddlepoint inversion otherwise. JIDT p-values are Monte Carlo quantities, so their floor is `1/(shuffles+1)` and their calibration columns are noisier than the analytical methods when `jidt_reps` is small. Nominal chi-squared uses configured alphabet size; dynamic chi-squared uses observed nonempty rows and columns.
