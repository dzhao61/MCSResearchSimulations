# Jackknife Centering Comparison

The experiment changes only the MI bias correction. The standard error and both Welch degrees-of-freedom calculations are identical for the analytic and jackknife versions, and every method is applied to the same simulated table pairs.

## Expanded Welch comparison

| alpha | population_pairs | analytic_expanded_mean_absolute_fpr_error | jackknife_expanded_mean_absolute_fpr_error | jackknife_minus_analytic_error | jackknife_wins | analytic_wins | ties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.100000 | 192 | 0.008011 | 0.007331 | -0.000680 | 83 | 87 | 22 |
| 0.050000 | 192 | 0.005769 | 0.005321 | -0.000448 | 89 | 76 | 27 |
| 0.010000 | 192 | 0.002075 | 0.002077 | 0.000002 | 69 | 76 | 47 |

## Overall method calibration

| method | method_label | mean_absolute_fpr_error_10 | mean_absolute_fpr_error_05 | mean_absolute_fpr_error_01 |
| --- | --- | --- | --- | --- |
| analytic_normal | Analytic correction + Normal Wald | 0.007404 | 0.005508 | 0.002402 |
| analytic_simple | Analytic correction + Simple Welch | 0.007231 | 0.005372 | 0.002298 |
| analytic_expanded | Analytic correction + Expanded Welch | 0.008011 | 0.005769 | 0.002075 |
| jackknife_normal | Jackknife correction + Normal Wald | 0.008487 | 0.006318 | 0.002793 |
| jackknife_simple | Jackknife correction + Simple Welch | 0.008239 | 0.006079 | 0.002652 |
| jackknife_expanded | Jackknife correction + Expanded Welch | 0.007331 | 0.005321 | 0.002077 |

## Centering diagnostics by regime

| regime | regime_label | correction | population_pairs | mean_absolute_standardized_bias | median_absolute_standardized_bias | mean_sd_to_mean_se_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| well_sampled | Well sampled | analytic | 24 | 0.017465 | 0.010338 | 0.988497 |
| well_sampled | Well sampled | jackknife | 24 | 0.013096 | 0.008646 | 0.988933 |
| moderate | Moderate | analytic | 24 | 0.016343 | 0.008130 | 0.992116 |
| moderate | Moderate | jackknife | 24 | 0.019280 | 0.012648 | 0.991657 |
| sparse_imbalanced | Sparse and imbalanced | analytic | 24 | 0.046338 | 0.034794 | 1.016745 |
| sparse_imbalanced | Sparse and imbalanced | jackknife | 24 | 0.027923 | 0.024675 | 1.027903 |
| highly_sparse | Highly skewed and sparse | analytic | 24 | 0.010196 | 0.010427 | 1.001769 |
| highly_sparse | Highly skewed and sparse | jackknife | 24 | 0.009524 | 0.009263 | 1.001676 |
| ultra_sparse | Ultra-skewed and sparse | analytic | 24 | 0.007164 | 0.006189 | 1.009295 |
| ultra_sparse | Ultra-skewed and sparse | jackknife | 24 | 0.007165 | 0.005247 | 1.014546 |
| widespread_sparse | Widespread sparsity | analytic | 24 | 0.168803 | 0.139238 | 0.970340 |
| widespread_sparse | Widespread sparsity | jackknife | 24 | 0.069555 | 0.071254 | 1.029699 |
| shape_mismatch | Equal-MI shape mismatch | analytic | 24 | 0.129420 | 0.116482 | 0.997355 |
| shape_mismatch | Equal-MI shape mismatch | jackknife | 24 | 0.065750 | 0.066431 | 1.001020 |
| extreme_imbalance | Extreme sample imbalance | analytic | 24 | 0.055731 | 0.041951 | 1.010400 |
| extreme_imbalance | Extreme sample imbalance | jackknife | 24 | 0.031877 | 0.031662 | 1.025673 |
