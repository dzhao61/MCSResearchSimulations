# Constrained-Profile Go/No-Go Result

## Decision: NO-GO

The best hard-subset profile method was `profile_pearson`. Its alpha=0.05
FPR MAE was `0.05120` versus `0.01150` for the
bias-corrected Wald baseline, a relative improvement of `-345.2%`.
Its easy-subset MAE change was `-0.00112`.

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
| easy | wald_analytic | 0.00925 | 0.04075 | 1.00000 |
| easy | profile_lr | 0.00800 | 0.04325 | 1.00000 |
| easy | profile_pearson | 0.00813 | 0.04312 | 1.00000 |
| easy | profile_cr_2_3 | 0.00813 | 0.04312 | 1.00000 |
| hard | wald_analytic | 0.01150 | 0.06150 | 1.00000 |
| hard | profile_lr | 0.05495 | 0.10495 | 0.99962 |
| hard | profile_pearson | 0.05120 | 0.10120 | 0.99962 |
| hard | profile_cr_2_3 | 0.05157 | 0.10157 | 0.99962 |
| all | wald_analytic | 0.01038 | 0.05113 | 1.00000 |
| all | profile_lr | 0.03147 | 0.07410 | 0.99981 |
| all | profile_pearson | 0.02966 | 0.07216 | 0.99981 |
| all | profile_cr_2_3 | 0.02985 | 0.07235 | 0.99981 |

## Runtime

| subset | pairs | median_wald_ms | median_profile_ms | median_permutation_ms | profile_over_permutation |
| --- | --- | --- | --- | --- | --- |
| easy | 80 | 0.173 | 123.658 | 5.578 | 22.177 |
| hard | 80 | 0.168 | 146.889 | 5.291 | 27.603 |
| all | 160 | 0.171 | 142.829 | 5.578 | 25.768 |

The permutation comparator is the existing optimized table-level
studentized differential-MI permutation implementation with 999 draws.
JIDT does not provide this two-sample equal-MI test.

## Power

| method | replicates | valid_rate | rejection_rate_05 | mean_true_delta |
| --- | --- | --- | --- | --- |
| wald_analytic | 1600 | 1.0000 | 0.4537 | 0.0371 |
| profile_lr | 1600 | 1.0000 | 0.5637 | 0.0371 |
| profile_pearson | 1600 | 1.0000 | 0.5606 | 0.0371 |
| profile_cr_2_3 | 1600 | 1.0000 | 0.5606 | 0.0371 |

## Numerical Audit

Overall trustworthy constrained-fit rate: `0.99981`.
Boundary hits are retained as diagnostics because multinomial MLEs can
legitimately lie on the simplex boundary; separate tests check statistic
stability as the numerical logit bound changes.
