# Differential-MI Validation: smoke

## Run

- Null replicates per scenario: 40
- Power replicates per scenario: 40
- Permutations per replicate: 99
- Seed: 20260725

## Pre-Specified Decision Metrics

- Regular weak-null mean absolute FPR error, naive permutation: 0.0250
- Regular weak-null mean absolute FPR error, studentized jackknife permutation: 0.0000
- Relative calibration-error reduction: 100.0%
- Regular weak-null studentized cases within [0.035, 0.065]: 100.0%
- Material naive failures with Wilson interval excluding 0.05: 0

These metrics are decisive only for the `decisive` profile. Smoke and screen
runs are exploratory because their Monte Carlo intervals are wide.

## Calibration

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strong_2x2_bal_100 | strong_null | True | 0.0750 | 0.0750 | 0.0750 | 0.0500 | 0.0500 | 0.9500 |
| weak_2x2_bal_strong_100_250 | weak_null | True | 0.0250 | 0.0500 | 0.0500 | 0.0250 | 0.0250 | 0.9750 |
| near_2x2_bal_strong_500 | near_boundary | False | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |

## Power

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| power_2x2_bal_strong_200 | power | True | 0.1500 | 0.2000 | 0.2000 | 0.1500 | 0.1500 | 0.9000 |

## Runtime

- Mean deterministic time: 0.114 ms/table
- Mean permutation time: 0.181 ms/table

See `summary.csv`, `replicates.csv`, and `scenarios.csv` for full results.
