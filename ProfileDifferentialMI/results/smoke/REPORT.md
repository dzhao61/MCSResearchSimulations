# Constrained-Profile Go/No-Go Result

## Decision: NO-GO

The best hard-subset profile method was `profile_lr`. Its alpha=0.05
FPR MAE was `0.11042` versus `0.06042` for the
bias-corrected Wald baseline, a relative improvement of `-82.8%`.
Its easy-subset MAE change was `+0.00000`.

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
| easy | wald_analytic | 0.04167 | 0.04167 | 1.00000 |
| easy | profile_lr | 0.04167 | 0.04167 | 1.00000 |
| easy | profile_pearson | 0.04167 | 0.04167 | 1.00000 |
| easy | profile_cr_2_3 | 0.04167 | 0.04167 | 1.00000 |
| hard | wald_analytic | 0.06042 | 0.07292 | 1.00000 |
| hard | profile_lr | 0.11042 | 0.13542 | 1.00000 |
| hard | profile_pearson | 0.11042 | 0.13542 | 1.00000 |
| hard | profile_cr_2_3 | 0.11042 | 0.13542 | 1.00000 |
| all | wald_analytic | 0.05104 | 0.05729 | 1.00000 |
| all | profile_lr | 0.07604 | 0.08854 | 1.00000 |
| all | profile_pearson | 0.07604 | 0.08854 | 1.00000 |
| all | profile_cr_2_3 | 0.07604 | 0.08854 | 1.00000 |

## Runtime

| subset | pairs | median_wald_ms | median_profile_ms | median_permutation_ms | profile_over_permutation |
| --- | --- | --- | --- | --- | --- |
| easy | 16 | 0.079 | 57.835 | 2.443 | 20.856 |
| hard | 16 | 0.084 | 110.845 | 3.448 | 28.324 |
| all | 32 | 0.080 | 84.650 | 3.144 | 25.382 |

The permutation comparator is the existing optimized table-level
studentized differential-MI permutation implementation with 999 draws.
JIDT does not provide this two-sample equal-MI test.

## Power

| method | replicates | valid_rate | rejection_rate_05 | mean_true_delta |
| --- | --- | --- | --- | --- |
| wald_analytic | 64 | 1.0000 | 0.5000 | 0.0371 |
| profile_lr | 64 | 1.0000 | 0.6250 | 0.0371 |
| profile_pearson | 64 | 1.0000 | 0.6250 | 0.0371 |
| profile_cr_2_3 | 64 | 1.0000 | 0.6250 | 0.0371 |

## Numerical Audit

Overall trustworthy constrained-fit rate: `1.00000`.
Boundary hits are retained as diagnostics because multinomial MLEs can
legitimately lie on the simplex boundary; separate tests check statistic
stability as the numerical logit bound changes.
