# Welch-Satterthwaite Differential-MI Validation

Profile: `smoke`.

## Decision: NO-GO

Hard-grid alpha-0.05 MAE changed from `0.01300` to `0.01200`, a relative improvement of `7.7%`.
Broad-grid MAE changed from `0.01125` to `0.01125`.

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
| broad | wald_normal | 0.05500 | 0.01125 | 0.87500 | 0.94500 |
| broad | welch_reference | 0.05500 | 0.01125 | 0.87500 | 0.94500 |
| broad | welch_unbiased | 0.05438 | 0.01063 | 0.87500 | 0.94562 |
| hard | wald_normal | 0.06300 | 0.01300 | 0.50000 | 0.93700 |
| hard | welch_reference | 0.06200 | 0.01200 | 0.50000 | 0.93800 |
| hard | welch_unbiased | 0.06000 | 0.01000 | 0.50000 | 0.94000 |
| stress | wald_normal | 0.02403 | 0.02597 | 0.25000 | 0.97597 |
| stress | welch_reference | 0.02002 | 0.02998 | 0.00000 | 0.97998 |
| stress | welch_unbiased | 0.01902 | 0.03098 | 0.00000 | 0.98098 |

## Power

| scenario_id | method | true_delta | power_05 | coverage_95 |
| --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | wald_normal | -0.0200 | 0.0660 | 0.9520 |
| curve_effect_d02_n300 | welch_reference | -0.0200 | 0.0660 | 0.9520 |
| curve_effect_d02_n300 | welch_unbiased | -0.0200 | 0.0660 | 0.9520 |
| curve_effect_d05_n300 | wald_normal | -0.0500 | 0.2580 | 0.9440 |
| curve_effect_d05_n300 | welch_reference | -0.0500 | 0.2540 | 0.9460 |
| curve_effect_d05_n300 | welch_unbiased | -0.0500 | 0.2540 | 0.9460 |
| curve_effect_d10_n300 | wald_normal | -0.1000 | 0.7020 | 0.9440 |
| curve_effect_d10_n300 | welch_reference | -0.1000 | 0.7000 | 0.9440 |
| curve_effect_d10_n300 | welch_unbiased | -0.1000 | 0.7000 | 0.9440 |
| curve_sample_d05_n150 | wald_normal | -0.0500 | 0.1840 | 0.9580 |
| curve_sample_d05_n150 | welch_reference | -0.0500 | 0.1840 | 0.9580 |
| curve_sample_d05_n150 | welch_unbiased | -0.0500 | 0.1820 | 0.9580 |
| curve_sample_d05_n600 | wald_normal | -0.0500 | 0.5120 | 0.9540 |
| curve_sample_d05_n600 | welch_reference | -0.0500 | 0.5100 | 0.9560 |
| curve_sample_d05_n600 | welch_unbiased | -0.0500 | 0.5100 | 0.9560 |

## Runtime

| scenario_seed | scenario_id | rows | columns | repetitions | median_normal_ms | median_welch_ms | welch_over_normal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026072501 | random_2x2_d5 | 2 | 2 | 30 | 0.1130 | 0.1239 | 1.0962 |
| 2026072501 | random_2x5_d5 | 2 | 5 | 30 | 0.1145 | 0.1257 | 1.0979 |

## Permutation Anchors

| scenario_id | replicates | wald_normal_fpr_05 | welch_reference_fpr_05 | student_perm_analytic_fpr_05 | mean_permutation_ms |
| --- | --- | --- | --- | --- | --- |
| random_2x2_d5 | 20 | 0.0500 | 0.0500 | 0.0000 | 1.0499 |
| random_2x5_d5 | 20 | 0.1000 | 0.1000 | 0.0500 | 1.6269 |

## Degrees of Freedom

Hard-grid median effective df ranged from `185.53` to `205.22`.

JIDT does not provide this independent two-sample equal-MI test.
The permutation comparator is the optimized table-level
studentized analytic implementation for the same estimand.

See the CSV and compressed replicate files for complete
scenario-level intervals, paired p-values, seeds, and diagnostics.
