# Differential-MI Validation: adversarial

## Run

- Null replicates per scenario: 2000
- Power replicates per scenario: 1000
- Permutations per replicate: 999
- Seed: 20260726

## Pre-Specified Decision Metrics

- Regular weak-null mean absolute FPR error, naive permutation: 0.0239
- Regular weak-null mean absolute FPR error, studentized jackknife permutation: 0.0037
- Relative calibration-error reduction: 84.3%
- Regular weak-null studentized cases within [0.035, 0.065]: 100.0%
- Material naive failures with Wilson interval excluding 0.05: 3

These metrics are decisive only for the `decisive` profile. Smoke and screen
runs are exploratory because their Monte Carlo intervals are wide.

## Calibration

| scenario_id | family | regular | naive_perm_plugin_fpr_05 | student_perm_plugin_fpr_05 | student_perm_jackknife_fpr_05 | wald_plugin_fpr_05 | wald_jackknife_fpr_05 | wald_jackknife_95_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| adv_strong_3x5_cyclic_400 | strong_null | True | 0.0445 | 0.0460 | 0.0465 | 0.0440 | 0.0440 | 0.9560 |
| adv_weak_2x3_bal_strong_150_300 | weak_null | True | 0.0055 | 0.0380 | 0.0420 | 0.0385 | 0.0425 | 0.9575 |
| adv_weak_3x5_bal_mild_300_600 | weak_null | True | 0.0445 | 0.0535 | 0.0505 | 0.0540 | 0.0500 | 0.9500 |
| adv_weak_5x10_mild_strong_1000_2000 | weak_null | False | 0.0690 | 0.0580 | 0.0665 | 0.0700 | 0.0580 | 0.9420 |
| adv_weak_10x10_bal_mild_2000_4000 | weak_null | True | 0.0255 | 0.0465 | 0.0470 | 0.0890 | 0.0450 | 0.9550 |
| adv_weak_5x5_same_margin_structure | weak_null | True | 0.0710 | 0.0545 | 0.0535 | 0.0500 | 0.0480 | 0.9520 |
| adv_weak_10x10_same_margin_structure | weak_null | False | 0.0775 | 0.0595 | 0.0585 | 0.0420 | 0.0445 | 0.9555 |

## Runtime

- Mean deterministic time: 0.123 ms/table
- Mean permutation time: 4.617 ms/table

See `summary.csv`, `replicates.csv`, and `scenarios.csv` for full results.
