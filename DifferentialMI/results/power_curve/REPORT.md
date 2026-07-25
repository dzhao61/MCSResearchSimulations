# Differential-MI Validation: power_curve

## Run

- Null replicates per scenario: 1000
- Power replicates per scenario: 1500
- Permutations per replicate: 499
- Seed: 20260727

## Pre-Specified Decision Metrics

- Regular weak-null mean absolute FPR error, naive permutation: nan
- Regular weak-null mean absolute FPR error, studentized jackknife permutation: nan
- Relative calibration-error reduction: nan%
- Regular weak-null studentized cases within [0.035, 0.065]: nan%
- Material naive failures with Wilson interval excluding 0.05: 0

These metrics are decisive only for the `decisive` profile. Smoke and screen
runs are exploratory because their Monte Carlo intervals are wide.

## Calibration

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Power

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | power | True | 0.0260 | 0.0813 | 0.0767 | 0.0820 | 0.0780 | 0.9493 |
| curve_effect_d05_n300 | power | True | 0.1493 | 0.2653 | 0.2467 | 0.2713 | 0.2573 | 0.9387 |
| curve_effect_d10_n300 | power | True | 0.6047 | 0.7200 | 0.7053 | 0.7327 | 0.7113 | 0.9393 |
| curve_sample_d05_n150 | power | True | 0.0873 | 0.1547 | 0.1480 | 0.1613 | 0.1580 | 0.9427 |
| curve_sample_d05_n600 | power | True | 0.3327 | 0.5200 | 0.5167 | 0.5193 | 0.5120 | 0.9547 |

## Runtime

- Mean deterministic time: 0.117 ms/table
- Mean permutation time: 0.729 ms/table

See `summary.csv`, `replicates.csv`, and `scenarios.csv` for full results.
