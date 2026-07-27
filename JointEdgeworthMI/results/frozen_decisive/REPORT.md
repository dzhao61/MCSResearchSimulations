# Joint Studentized Edgeworth MI Validation

## Decision: GO

Hard alpha-0.05 MAE: normal/naive/influence-df/joint = `0.01230` / `0.01130` / `0.00810` / `0.00681`.
Broad alpha-0.05 MAE changed from `0.00531` for naive Welch to `0.00428`.

- [x] `hard_alpha05_mae_at_least_10pct_lower_than_naive`
- [x] `hard_alpha10_mae_does_not_exceed_naive`
- [x] `hard_alpha05_mae_within_0_00050_of_influence_df`
- [x] `broad_alpha05_mae_within_0_00025_of_naive`
- [x] `balanced_alpha05_mae_within_0_00050_of_normal`
- [x] `strong_alpha05_mae_within_0_00025_of_naive`
- [x] `mean_power_loss_vs_naive_at_most_0_01`
- [x] `broad_hard_strong_valid_rate_at_least_0_995`
- [x] `scalar_runtime_below_3x_normal_and_1ms`

## Null Calibration

| stage | method | population_pairs | aggregate_valid_rate | mean_fpr_05 | mean_absolute_fpr_error_05 | mean_absolute_fpr_error_10 |
| --- | --- | --- | --- | --- | --- | --- |
| broad | wald_normal | 144 | 1.00000 | 0.05125 | 0.00550 | 0.00753 |
| broad | welch_n_minus_1 | 144 | 1.00000 | 0.05098 | 0.00531 | 0.00734 |
| broad | if_satterthwaite | 144 | 1.00000 | 0.04915 | 0.00514 | 0.00740 |
| broad | joint_edgeworth | 144 | 0.99805 | 0.05148 | 0.00428 | 0.00592 |
| hard | wald_normal | 12 | 1.00000 | 0.06230 | 0.01230 | 0.01582 |
| hard | welch_n_minus_1 | 12 | 1.00000 | 0.06130 | 0.01130 | 0.01471 |
| hard | if_satterthwaite | 12 | 1.00000 | 0.05810 | 0.00810 | 0.01144 |
| hard | joint_edgeworth | 12 | 0.99575 | 0.05681 | 0.00681 | 0.00734 |
| strong | wald_normal | 144 | 1.00000 | 0.05015 | 0.00536 | 0.00778 |
| strong | welch_n_minus_1 | 144 | 1.00000 | 0.04985 | 0.00520 | 0.00760 |
| strong | if_satterthwaite | 144 | 1.00000 | 0.04803 | 0.00558 | 0.00800 |
| strong | joint_edgeworth | 144 | 0.99811 | 0.05071 | 0.00417 | 0.00598 |
| stress | wald_normal | 26 | 0.99987 | 0.06542 | 0.03045 | 0.04166 |
| stress | welch_n_minus_1 | 26 | 0.99987 | 0.06187 | 0.02888 | 0.04032 |
| stress | if_satterthwaite | 26 | 0.99987 | 0.05225 | 0.02325 | 0.03703 |
| stress | joint_edgeworth | 26 | 0.97116 | 0.06330 | 0.01366 | 0.01534 |
| broad_balanced_design0 | wald_normal | 24 | 1.00000 | 0.04462 | 0.00556 | 0.00787 |
| broad_balanced_design0 | welch_n_minus_1 | 24 | 1.00000 | 0.04456 | 0.00563 | 0.00789 |
| broad_balanced_design0 | if_satterthwaite | 24 | 1.00000 | 0.04270 | 0.00735 | 0.01029 |
| broad_balanced_design0 | joint_edgeworth | 24 | 0.99788 | 0.04923 | 0.00484 | 0.00679 |

## Cumulant Diagnostics

| population_seed | scenario_id | population_standardized_third_cumulant | median_plugin_standardized_third_cumulant | population_standardized_variance_covariance | median_plugin_standardized_variance_covariance |
| --- | --- | --- | --- | --- | --- |
| 91370211 | random_2x2_d0 | 0.0003 | -0.0001 | 0.0003 | 0.0027 |
| 91370211 | random_2x2_d5 | -0.1188 | -0.1152 | 0.1211 | 0.1166 |
| 91370211 | random_2x5_d5 | -0.0806 | -0.0848 | 0.1693 | 0.1506 |
| 91370211 | random_4x6_d5 | -0.0471 | -0.0438 | 0.1107 | 0.0989 |
| 91370211 | random_5x5_d2 | -0.0418 | -0.0419 | 0.0670 | 0.0648 |
| 47628903 | random_2x2_d0 | 0.0007 | 0.0006 | 0.0018 | 0.0030 |
| 47628903 | random_2x2_d5 | 0.0571 | 0.0617 | 0.1797 | 0.1740 |
| 47628903 | random_2x5_d5 | -0.0724 | -0.0347 | 0.1057 | 0.1134 |
| 47628903 | random_4x6_d5 | -0.0356 | -0.0287 | 0.1172 | 0.1092 |
| 47628903 | random_5x5_d2 | -0.0311 | -0.0278 | 0.0700 | 0.0711 |

## Power

| scenario_id | method | true_delta | valid_rate | power_05 |
| --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | wald_normal | -0.0200 | 1.0000 | 0.0725 |
| curve_effect_d02_n300 | welch_n_minus_1 | -0.0200 | 1.0000 | 0.0719 |
| curve_effect_d02_n300 | if_satterthwaite | -0.0200 | 1.0000 | 0.0653 |
| curve_effect_d02_n300 | joint_edgeworth | -0.0200 | 0.9911 | 0.0961 |
| curve_effect_d05_n300 | wald_normal | -0.0500 | 1.0000 | 0.2755 |
| curve_effect_d05_n300 | welch_n_minus_1 | -0.0500 | 1.0000 | 0.2736 |
| curve_effect_d05_n300 | if_satterthwaite | -0.0500 | 1.0000 | 0.2634 |
| curve_effect_d05_n300 | joint_edgeworth | -0.0500 | 0.9760 | 0.3094 |
| curve_effect_d10_n300 | wald_normal | -0.1000 | 1.0000 | 0.7386 |
| curve_effect_d10_n300 | welch_n_minus_1 | -0.1000 | 1.0000 | 0.7373 |
| curve_effect_d10_n300 | if_satterthwaite | -0.1000 | 1.0000 | 0.7307 |
| curve_effect_d10_n300 | joint_edgeworth | -0.1000 | 0.9678 | 0.7526 |
| curve_sample_d05_n150 | wald_normal | -0.0500 | 1.0000 | 0.1575 |
| curve_sample_d05_n150 | welch_n_minus_1 | -0.0500 | 1.0000 | 0.1547 |
| curve_sample_d05_n150 | if_satterthwaite | -0.0500 | 1.0000 | 0.1424 |
| curve_sample_d05_n150 | joint_edgeworth | -0.0500 | 0.9856 | 0.1858 |
| curve_sample_d05_n600 | wald_normal | -0.0500 | 1.0000 | 0.5217 |
| curve_sample_d05_n600 | welch_n_minus_1 | -0.0500 | 1.0000 | 0.5202 |
| curve_sample_d05_n600 | if_satterthwaite | -0.0500 | 1.0000 | 0.5104 |
| curve_sample_d05_n600 | joint_edgeworth | -0.0500 | 0.9425 | 0.5366 |

## Runtime

| scenario_id | rows | columns | median_wald_normal_ms | median_joint_edgeworth_ms | joint_over_normal |
| --- | --- | --- | --- | --- | --- |
| random_2x2_d5 | 2 | 2 | 0.1216 | 0.2658 | 2.1863 |
| random_2x5_d5 | 2 | 5 | 0.1229 | 0.2669 | 2.1721 |
| random_3x7_d5 | 3 | 7 | 0.1230 | 0.2669 | 2.1702 |
| random_4x6_d5 | 4 | 6 | 0.1221 | 0.2660 | 2.1778 |
| random_5x5_d5 | 5 | 5 | 0.1225 | 0.2655 | 2.1672 |
| random_5x10_d5 | 5 | 10 | 0.1230 | 0.2675 | 2.1745 |
| random_2x2_d5 | 2 | 2 | 0.1214 | 0.2646 | 2.1801 |
| random_2x5_d5 | 2 | 5 | 0.1217 | 0.2643 | 2.1717 |
| random_3x7_d5 | 3 | 7 | 0.1214 | 0.2636 | 2.1710 |
| random_4x6_d5 | 4 | 6 | 0.1210 | 0.2631 | 2.1740 |
| random_5x5_d5 | 5 | 5 | 0.1217 | 0.2644 | 2.1720 |
| random_5x10_d5 | 5 | 10 | 0.1212 | 0.2621 | 2.1615 |

The stress stage is diagnostic and cannot rescue a failed decision.
See the CSV files for all population probabilities, seeds, validity
rates, Wilson intervals, and empirical joint-moment diagnostics.
