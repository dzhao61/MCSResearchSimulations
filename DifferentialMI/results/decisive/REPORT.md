# Differential-MI Validation: decisive

## Run

- Null replicates per scenario: 2000
- Power replicates per scenario: 1000
- Permutations per replicate: 999
- Seed: 20260725

## Pre-Specified Decision Metrics

- Regular weak-null mean absolute FPR error, naive permutation: 0.0353
- Regular weak-null mean absolute FPR error, studentized jackknife permutation: 0.0069
- Relative calibration-error reduction: 80.4%
- Regular weak-null studentized cases within [0.035, 0.065]: 100.0%
- Material naive failures with Wilson interval excluding 0.05: 5

These metrics are decisive only for the `decisive` profile. Smoke and screen
runs are exploratory because their Monte Carlo intervals are wide.

## Calibration

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strong_2x2_bal_100 | strong_null | True | 0.0475 | 0.0480 | 0.0480 | 0.0330 | 0.0330 | 0.9670 |
| strong_3x3_strong_250 | strong_null | True | 0.0450 | 0.0440 | 0.0455 | 0.0505 | 0.0505 | 0.9495 |
| strong_5x5_mild_500 | strong_null | True | 0.0525 | 0.0505 | 0.0470 | 0.0450 | 0.0450 | 0.9550 |
| weak_2x2_bal_strong_100_100 | weak_null | True | 0.0105 | 0.0420 | 0.0425 | 0.0405 | 0.0455 | 0.9545 |
| weak_2x2_bal_strong_100_250 | weak_null | True | 0.0060 | 0.0350 | 0.0400 | 0.0420 | 0.0450 | 0.9550 |
| weak_3x3_bal_strong_200_200 | weak_null | True | 0.0170 | 0.0465 | 0.0475 | 0.0515 | 0.0510 | 0.9490 |
| weak_3x3_bal_strong_150_400 | weak_null | True | 0.0085 | 0.0475 | 0.0445 | 0.0495 | 0.0490 | 0.9510 |
| weak_5x5_bal_strong_500_500 | weak_null | True | 0.0090 | 0.0340 | 0.0375 | 0.0390 | 0.0405 | 0.9595 |
| weak_5x5_mild_strong_300_800 | weak_null | True | 0.0370 | 0.0525 | 0.0535 | 0.0630 | 0.0505 | 0.9495 |
| weak_10x10_bal_strong_1000 | weak_null | False | 0.0165 | 0.0610 | 0.0530 | 0.0665 | 0.0590 | 0.9410 |
| near_2x2_bal_strong_500 | near_boundary | False | 0.0000 | 0.0045 | 0.0050 | 0.0035 | 0.0035 | 0.9965 |
| near_5x5_bal_strong_1000 | near_boundary | False | 0.0000 | 0.0165 | 0.0275 | 0.0165 | 0.0260 | 0.9740 |

## Power

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| power_2x2_bal_strong_200 | power | True | 0.1500 | 0.1950 | 0.1940 | 0.1990 | 0.1990 | 0.9460 |
| power_3x3_bal_strong_300 | power | True | 0.1620 | 0.2660 | 0.2570 | 0.2730 | 0.2610 | 0.9420 |
| power_5x5_mild_strong_600 | power | True | 0.5010 | 0.4760 | 0.4910 | 0.4440 | 0.4760 | 0.9550 |

## Runtime

- Mean deterministic time: 0.119 ms/table
- Mean permutation time: 2.227 ms/table

See `summary.csv`, `replicates.csv`, and `scenarios.csv` for full results.
