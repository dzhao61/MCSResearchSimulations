# Welch-Satterthwaite Differential-MI Validation

Profile: `decisive`.

## Decision: NO-GO

Hard-grid alpha-0.05 MAE changed from `0.01177` to `0.01084`, a relative improvement of `7.9%`.
Broad-grid MAE changed from `0.00514` to `0.00504`.

- [ ] `hard_alpha05_mae_reduction_at_least_20pct`
- [x] `hard_alpha10_mae_does_not_increase`
- [x] `broad_alpha05_mae_increase_at_most_0_001`
- [x] `broad_in_band_drop_at_most_0_02`
- [x] `mean_power_loss_at_most_0_03`
- [x] `valid_rate_at_least_0_995`
- [x] `runtime_below_2x_and_1ms`

The sensitivity variant cannot overturn the primary decision.

## Null Calibration

| stage | method | mean_fpr_05 | mean_absolute_fpr_error_05 | within_035_065 | mean_coverage_95 |
| --- | --- | --- | --- | --- | --- |
| broad | wald_normal | 0.04977 | 0.00514 | 0.97222 | 0.95023 |
| broad | welch_reference | 0.04951 | 0.00504 | 0.97917 | 0.95049 |
| broad | welch_unbiased | 0.04933 | 0.00497 | 0.97917 | 0.95067 |
| hard | wald_normal | 0.06177 | 0.01177 | 0.75000 | 0.93823 |
| hard | welch_reference | 0.06084 | 0.01084 | 0.91667 | 0.93916 |
| hard | welch_unbiased | 0.06030 | 0.01030 | 0.91667 | 0.93970 |
| stress | wald_normal | 0.06580 | 0.03180 | 0.19231 | 0.93420 |
| stress | welch_reference | 0.06276 | 0.03037 | 0.15385 | 0.93724 |
| stress | welch_unbiased | 0.06113 | 0.02949 | 0.19231 | 0.93887 |

## Power

| scenario_id | method | true_delta | power_05 | coverage_95 |
| --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | wald_normal | -0.0200 | 0.0797 | 0.9513 |
| curve_effect_d02_n300 | welch_reference | -0.0200 | 0.0792 | 0.9516 |
| curve_effect_d02_n300 | welch_unbiased | -0.0200 | 0.0787 | 0.9518 |
| curve_effect_d05_n300 | wald_normal | -0.0500 | 0.2776 | 0.9450 |
| curve_effect_d05_n300 | welch_reference | -0.0500 | 0.2761 | 0.9454 |
| curve_effect_d05_n300 | welch_unbiased | -0.0500 | 0.2753 | 0.9455 |
| curve_effect_d10_n300 | wald_normal | -0.1000 | 0.7438 | 0.9414 |
| curve_effect_d10_n300 | welch_reference | -0.1000 | 0.7419 | 0.9416 |
| curve_effect_d10_n300 | welch_unbiased | -0.1000 | 0.7406 | 0.9421 |
| curve_sample_d05_n150 | wald_normal | -0.0500 | 0.1559 | 0.9408 |
| curve_sample_d05_n150 | welch_reference | -0.0500 | 0.1527 | 0.9426 |
| curve_sample_d05_n150 | welch_unbiased | -0.0500 | 0.1511 | 0.9433 |
| curve_sample_d05_n600 | wald_normal | -0.0500 | 0.5227 | 0.9497 |
| curve_sample_d05_n600 | welch_reference | -0.0500 | 0.5221 | 0.9498 |
| curve_sample_d05_n600 | welch_unbiased | -0.0500 | 0.5214 | 0.9498 |

## Runtime

| scenario_seed | scenario_id | rows | columns | repetitions | median_normal_ms | median_welch_ms | welch_over_normal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026072501 | random_2x2_d5 | 2 | 2 | 200 | 0.1166 | 0.1275 | 1.0936 |
| 2026072501 | random_2x5_d5 | 2 | 5 | 200 | 0.1176 | 0.1289 | 1.0958 |
| 2026072501 | random_3x7_d5 | 3 | 7 | 200 | 0.1171 | 0.1278 | 1.0912 |
| 2026072501 | random_4x6_d5 | 4 | 6 | 200 | 0.1170 | 0.1279 | 1.0929 |
| 2026072501 | random_5x5_d5 | 5 | 5 | 200 | 0.1176 | 0.1281 | 1.0891 |
| 2026072501 | random_5x10_d5 | 5 | 10 | 200 | 0.1178 | 0.1284 | 1.0898 |
| 2026072601 | random_2x2_d5 | 2 | 2 | 200 | 0.1185 | 0.1297 | 1.0945 |
| 2026072601 | random_2x5_d5 | 2 | 5 | 200 | 0.1164 | 0.1275 | 1.0952 |
| 2026072601 | random_3x7_d5 | 3 | 7 | 200 | 0.1167 | 0.1278 | 1.0953 |
| 2026072601 | random_4x6_d5 | 4 | 6 | 200 | 0.1170 | 0.1279 | 1.0929 |
| 2026072601 | random_5x5_d5 | 5 | 5 | 200 | 0.1175 | 0.1284 | 1.0925 |
| 2026072601 | random_5x10_d5 | 5 | 10 | 200 | 0.1182 | 0.1292 | 1.0929 |

## Permutation Anchors

| scenario_id | replicates | wald_normal_fpr_05 | welch_reference_fpr_05 | student_perm_analytic_fpr_05 | mean_permutation_ms |
| --- | --- | --- | --- | --- | --- |
| random_2x2_d5 | 1000 | 0.0820 | 0.0810 | 0.0590 | 1.0614 |
| random_2x5_d5 | 1000 | 0.0620 | 0.0620 | 0.0500 | 1.6523 |
| random_3x7_d5 | 1000 | 0.0600 | 0.0590 | 0.0560 | 2.7406 |
| random_4x6_d5 | 1000 | 0.0680 | 0.0660 | 0.0620 | 3.2056 |
| random_5x5_d5 | 1000 | 0.0660 | 0.0660 | 0.0630 | 3.3766 |
| random_5x10_d5 | 1000 | 0.0580 | 0.0580 | 0.0580 | 5.8532 |
| random_2x2_d5 | 1000 | 0.0660 | 0.0620 | 0.0550 | 1.2976 |
| random_2x5_d5 | 1000 | 0.0510 | 0.0490 | 0.0400 | 1.6526 |
| random_3x7_d5 | 1000 | 0.0570 | 0.0560 | 0.0510 | 2.8067 |
| random_4x6_d5 | 1000 | 0.0550 | 0.0540 | 0.0500 | 3.2190 |
| random_5x5_d5 | 1000 | 0.0560 | 0.0540 | 0.0490 | 3.3176 |
| random_5x10_d5 | 1000 | 0.0640 | 0.0630 | 0.0620 | 5.8205 |

## Degrees of Freedom

Hard-grid median effective df ranged from `185.65` to `812.38`.

JIDT does not provide this independent two-sample equal-MI test.
The permutation comparator is the optimized table-level
studentized analytic implementation for the same estimand.

See the CSV and compressed replicate files for complete
scenario-level intervals, paired p-values, seeds, and diagnostics.
