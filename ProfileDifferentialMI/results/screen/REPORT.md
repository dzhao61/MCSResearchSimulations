# Constrained-Profile Go/No-Go Result

## Decision: NO-GO

The best hard-subset profile method was `profile_pearson`. Its alpha=0.05
FPR MAE was `0.03875` versus `0.01375` for the
bias-corrected Wald baseline, a relative improvement of `-181.8%`.
Its easy-subset MAE change was `+0.00125`.

- [ ] `hard_calibration_improvement_at_least_20pct`
- [x] `easy_mae_degradation_at_most_0_005`
- [x] `trustworthy_fit_rate_at_least_0_995`
- [ ] `median_faster_than_999_permutations`
- [x] `power_not_more_than_0_10_below_wald`

This decision applies to the pilot protocol only. Monte Carlo uncertainty
and any failed criterion must be considered before making a thesis claim.

## Calibration

| subset | method | mean_absolute_fpr_error_05 | mean_fpr_05 | mean_valid_rate |
| --- | --- | --- | --- | --- |
| easy | wald_analytic | 0.01500 | 0.04250 | 1.00000 |
| easy | profile_lr | 0.01625 | 0.04375 | 1.00000 |
| easy | profile_pearson | 0.01625 | 0.04375 | 1.00000 |
| easy | profile_cr_2_3 | 0.01625 | 0.04375 | 1.00000 |
| hard | wald_analytic | 0.01375 | 0.06125 | 1.00000 |
| hard | profile_lr | 0.04250 | 0.08750 | 1.00000 |
| hard | profile_pearson | 0.03875 | 0.08375 | 1.00000 |
| hard | profile_cr_2_3 | 0.04000 | 0.08500 | 1.00000 |
| all | wald_analytic | 0.01438 | 0.05188 | 1.00000 |
| all | profile_lr | 0.02937 | 0.06563 | 1.00000 |
| all | profile_pearson | 0.02750 | 0.06375 | 1.00000 |
| all | profile_cr_2_3 | 0.02813 | 0.06438 | 1.00000 |

## Runtime

| subset | pairs | median_wald_ms | median_profile_ms | median_permutation_ms | profile_over_permutation |
| --- | --- | --- | --- | --- | --- |
| easy | 40 | 0.086 | 60.364 | 2.789 | 22.396 |
| hard | 40 | 0.094 | 82.592 | 3.341 | 27.956 |
| all | 80 | 0.089 | 82.592 | 3.089 | 26.834 |

The permutation comparator is the existing optimized table-level
studentized differential-MI permutation implementation with 999 draws.
JIDT does not provide this two-sample equal-MI test.

## Power

| method | replicates | valid_rate | rejection_rate_05 | mean_true_delta |
| --- | --- | --- | --- | --- |
| wald_analytic | 320 | 1.0000 | 0.4156 | 0.0371 |
| profile_lr | 320 | 1.0000 | 0.5687 | 0.0371 |
| profile_pearson | 320 | 1.0000 | 0.5594 | 0.0371 |
| profile_cr_2_3 | 320 | 1.0000 | 0.5625 | 0.0371 |

## Numerical Audit

Overall trustworthy constrained-fit rate: `1.00000`.
Boundary hits are retained as diagnostics because multinomial MLEs can
legitimately lie on the simplex boundary; separate tests check statistic
stability as the numerical logit bound changes.
