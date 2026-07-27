# MI-Specific Influence-DF Validation

## Decision: NO-GO

The hard-grid alpha-0.05 MAE changed from `0.01131` for the naive Welch reference to `0.00736` for the MI-specific influence reference (`35.0%` improvement).
Across the broad grid, MAE changed from `0.00462` to `0.00494`.

- [x] `hard_alpha05_mae_at_least_10pct_lower_than_naive`
- [x] `hard_alpha10_mae_does_not_increase`
- [ ] `broad_alpha05_mae_within_0_00025_of_naive`
- [ ] `balanced_alpha05_mae_within_0_00050_of_normal`
- [x] `strong_alpha05_mae_within_0_00025_of_naive`
- [x] `mean_power_loss_vs_naive_at_most_0_01`
- [x] `broad_hard_strong_valid_rate_at_least_0_995`
- [x] `scalar_runtime_below_3x_normal_and_1ms`
- [x] `df_log_error_at_least_50pct_lower_than_naive`

## Null Calibration

| stage | method | population_pairs | mean_fpr_05 | mean_absolute_fpr_error_05 | mean_absolute_fpr_error_10 | mean_coverage_95 |
| --- | --- | --- | --- | --- | --- | --- |
| broad | wald_normal | 144 | 0.05026 | 0.00480 | 0.00645 | 0.94974 |
| broad | welch_n_minus_1 | 144 | 0.04995 | 0.00462 | 0.00627 | 0.95005 |
| broad | if_satterthwaite | 144 | 0.04815 | 0.00494 | 0.00644 | 0.95185 |
| hard | wald_normal | 12 | 0.06231 | 0.01231 | 0.01498 | 0.93769 |
| hard | welch_n_minus_1 | 12 | 0.06131 | 0.01131 | 0.01400 | 0.93869 |
| hard | if_satterthwaite | 12 | 0.05736 | 0.00736 | 0.01020 | 0.94264 |
| strong | wald_normal | 144 | 0.04997 | 0.00530 | 0.00740 | 0.95003 |
| strong | welch_n_minus_1 | 144 | 0.04967 | 0.00513 | 0.00728 | 0.95033 |
| strong | if_satterthwaite | 144 | 0.04789 | 0.00537 | 0.00773 | 0.95211 |
| stress | wald_normal | 26 | 0.07034 | 0.03729 | 0.05089 | 0.92966 |
| stress | welch_n_minus_1 | 26 | 0.06703 | 0.03567 | 0.04954 | 0.93297 |
| stress | if_satterthwaite | 26 | 0.05456 | 0.02658 | 0.04281 | 0.94544 |
| broad_balanced_design0 | wald_normal | 24 | 0.04454 | 0.00546 | 0.00667 | 0.95546 |
| broad_balanced_design0 | welch_n_minus_1 | 24 | 0.04443 | 0.00557 | 0.00676 | 0.95557 |
| broad_balanced_design0 | if_satterthwaite | 24 | 0.04265 | 0.00735 | 0.00875 | 0.95735 |

## Degrees-of-Freedom Audit

| population_seed | scenario_id | empirical_total_df | median_naive_total_df | median_if_total_df | population_if_total_df |
| --- | --- | --- | --- | --- | --- |
| 73105913 | random_2x2_d0 | 28.178 | 772.714 | 27.145 | 26.298 |
| 73105913 | random_2x2_d5 | 60.133 | 183.913 | 56.285 | 54.185 |
| 73105913 | random_2x5_d5 | 32.392 | 194.579 | 30.575 | 27.103 |
| 73105913 | random_4x6_d5 | 113.551 | 371.882 | 103.060 | 83.180 |
| 73105913 | random_5x5_d2 | 192.071 | 965.709 | 190.262 | 180.469 |
| 84207631 | random_2x2_d0 | 29.188 | 771.976 | 27.537 | 26.491 |
| 84207631 | random_2x2_d5 | 52.881 | 177.968 | 48.556 | 46.980 |
| 84207631 | random_2x5_d5 | 80.230 | 187.092 | 75.036 | 74.133 |
| 84207631 | random_4x6_d5 | 129.267 | 360.043 | 110.805 | 97.509 |
| 84207631 | random_5x5_d2 | 216.057 | 981.966 | 211.307 | 191.219 |

## Power

| scenario_id | method | true_delta | power_05 | coverage_95 |
| --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | wald_normal | -0.0200 | 0.0790 | 0.9537 |
| curve_effect_d02_n300 | welch_n_minus_1 | -0.0200 | 0.0783 | 0.9539 |
| curve_effect_d02_n300 | if_satterthwaite | -0.0200 | 0.0706 | 0.9602 |
| curve_effect_d05_n300 | wald_normal | -0.0500 | 0.2843 | 0.9449 |
| curve_effect_d05_n300 | welch_n_minus_1 | -0.0500 | 0.2817 | 0.9456 |
| curve_effect_d05_n300 | if_satterthwaite | -0.0500 | 0.2693 | 0.9516 |
| curve_effect_d10_n300 | wald_normal | -0.1000 | 0.7351 | 0.9423 |
| curve_effect_d10_n300 | welch_n_minus_1 | -0.1000 | 0.7341 | 0.9435 |
| curve_effect_d10_n300 | if_satterthwaite | -0.1000 | 0.7269 | 0.9471 |
| curve_sample_d05_n150 | wald_normal | -0.0500 | 0.1541 | 0.9408 |
| curve_sample_d05_n150 | welch_n_minus_1 | -0.0500 | 0.1509 | 0.9416 |
| curve_sample_d05_n150 | if_satterthwaite | -0.0500 | 0.1403 | 0.9523 |
| curve_sample_d05_n600 | wald_normal | -0.0500 | 0.5297 | 0.9501 |
| curve_sample_d05_n600 | welch_n_minus_1 | -0.0500 | 0.5286 | 0.9503 |
| curve_sample_d05_n600 | if_satterthwaite | -0.0500 | 0.5209 | 0.9526 |

## Scalar Runtime

| scenario_id | rows | columns | median_wald_normal_ms | median_welch_n_minus_1_ms | median_if_satterthwaite_ms | if_over_normal |
| --- | --- | --- | --- | --- | --- | --- |
| random_2x2_d5 | 2 | 2 | 0.1177 | 0.1265 | 0.1607 | 1.3654 |
| random_2x5_d5 | 2 | 5 | 0.1194 | 0.1279 | 0.1624 | 1.3601 |
| random_3x7_d5 | 3 | 7 | 0.1214 | 0.1296 | 0.1652 | 1.3610 |
| random_4x6_d5 | 4 | 6 | 0.1179 | 0.1268 | 0.1607 | 1.3629 |
| random_5x5_d5 | 5 | 5 | 0.1191 | 0.1268 | 0.1606 | 1.3476 |
| random_5x10_d5 | 5 | 10 | 0.1196 | 0.1284 | 0.1625 | 1.3587 |
| random_2x2_d5 | 2 | 2 | 0.1194 | 0.1285 | 0.1632 | 1.3663 |
| random_2x5_d5 | 2 | 5 | 0.1182 | 0.1278 | 0.1619 | 1.3704 |
| random_3x7_d5 | 3 | 7 | 0.1176 | 0.1260 | 0.1603 | 1.3636 |
| random_4x6_d5 | 4 | 6 | 0.1183 | 0.1271 | 0.1618 | 1.3680 |
| random_5x5_d5 | 5 | 5 | 0.1178 | 0.1263 | 0.1606 | 1.3637 |
| random_5x10_d5 | 5 | 10 | 0.1186 | 0.1271 | 0.1620 | 1.3663 |

The small-sample stress stage is diagnostic only and cannot change
the prospective decision. See the CSV files for all scenario-level
Wilson intervals, seeds, population probabilities, and diagnostics.
