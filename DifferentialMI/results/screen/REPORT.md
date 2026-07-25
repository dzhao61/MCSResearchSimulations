# Differential-MI Validation: screen

## Run

- Null replicates per scenario: 300
- Power replicates per scenario: 300
- Permutations per replicate: 199
- Seed: 20260725

## Pre-Specified Decision Metrics

- Regular weak-null mean absolute FPR error, naive permutation: 0.0350
- Regular weak-null mean absolute FPR error, studentized jackknife permutation: 0.0144
- Relative calibration-error reduction: 58.7%
- Regular weak-null studentized cases within [0.035, 0.065]: 66.7%
- Material naive failures with Wilson interval excluding 0.05: 5

These metrics are decisive only for the `decisive` profile. Smoke and screen
runs are exploratory because their Monte Carlo intervals are wide.

## Calibration

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strong_2x2_bal_100 | strong_null | True | 0.0400 | 0.0400 | 0.0400 | 0.0200 | 0.0200 | 0.9800 |
| strong_3x3_strong_250 | strong_null | True | 0.0633 | 0.0667 | 0.0700 | 0.0767 | 0.0767 | 0.9233 |
| strong_5x5_mild_500 | strong_null | True | 0.0700 | 0.0700 | 0.0733 | 0.0667 | 0.0667 | 0.9333 |
| weak_2x2_bal_strong_100_100 | weak_null | True | 0.0067 | 0.0200 | 0.0267 | 0.0267 | 0.0267 | 0.9733 |
| weak_2x2_bal_strong_100_250 | weak_null | True | 0.0100 | 0.0400 | 0.0400 | 0.0600 | 0.0733 | 0.9267 |
| weak_3x3_bal_strong_200_200 | weak_null | True | 0.0100 | 0.0300 | 0.0300 | 0.0333 | 0.0367 | 0.9633 |
| weak_3x3_bal_strong_150_400 | weak_null | True | 0.0100 | 0.0500 | 0.0633 | 0.0533 | 0.0667 | 0.9333 |
| weak_5x5_bal_strong_500_500 | weak_null | True | 0.0133 | 0.0300 | 0.0367 | 0.0367 | 0.0400 | 0.9600 |
| weak_5x5_mild_strong_300_800 | weak_null | True | 0.0600 | 0.0800 | 0.0567 | 0.0967 | 0.0633 | 0.9367 |
| weak_10x10_bal_strong_1000 | weak_null | False | 0.0200 | 0.0567 | 0.0400 | 0.0567 | 0.0367 | 0.9633 |
| near_2x2_bal_strong_500 | near_boundary | False | 0.0000 | 0.0067 | 0.0067 | 0.0067 | 0.0100 | 0.9900 |
| near_5x5_bal_strong_1000 | near_boundary | False | 0.0000 | 0.0167 | 0.0300 | 0.0133 | 0.0267 | 0.9733 |

## Power

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| power_2x2_bal_strong_200 | power | True | 0.1767 | 0.2033 | 0.2000 | 0.2067 | 0.2033 | 0.9500 |
| power_3x3_bal_strong_300 | power | True | 0.1833 | 0.3067 | 0.3100 | 0.3200 | 0.3100 | 0.9300 |
| power_5x5_mild_strong_600 | power | True | 0.4767 | 0.4433 | 0.4600 | 0.4367 | 0.4600 | 0.9367 |

## Runtime

- Mean deterministic time: 0.116 ms/table
- Mean permutation time: 0.532 ms/table

See `summary.csv`, `replicates.csv`, and `scenarios.csv` for full results.
