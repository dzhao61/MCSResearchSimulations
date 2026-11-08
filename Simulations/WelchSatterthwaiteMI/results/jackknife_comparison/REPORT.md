# Jackknife Centering Comparison

The experiment changes only the MI bias correction. The standard error and both Welch degrees-of-freedom calculations are identical for the analytic and jackknife versions, and every method is applied to the same simulated table pairs.

## Expanded Welch comparison

| alpha | population_pairs | analytic_expanded_mean_absolute_fpr_error | jackknife_expanded_mean_absolute_fpr_error | jackknife_minus_analytic_error | jackknife_wins | analytic_wins | ties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.100000 | 60 | 0.011791 | 0.020724 | 0.008933 | 14 | 45 | 1 |
| 0.050000 | 60 | 0.008249 | 0.014869 | 0.006620 | 10 | 48 | 2 |
| 0.010000 | 60 | 0.002783 | 0.005521 | 0.002738 | 15 | 40 | 5 |

## Overall method calibration

| method | method_label | mean_absolute_fpr_error_10 | mean_absolute_fpr_error_05 | mean_absolute_fpr_error_01 |
| --- | --- | --- | --- | --- |
| analytic_normal | Analytic correction + Normal Wald | 0.017155 | 0.013423 | 0.006075 |
| analytic_simple | Analytic correction + Simple Welch | 0.015602 | 0.011942 | 0.005139 |
| analytic_expanded | Analytic correction + Expanded Welch | 0.011791 | 0.008249 | 0.002783 |
| jackknife_normal | Jackknife correction + Normal Wald | 0.026065 | 0.020415 | 0.009900 |
| jackknife_simple | Jackknife correction + Simple Welch | 0.024629 | 0.019016 | 0.008771 |
| jackknife_expanded | Jackknife correction + Expanded Welch | 0.020724 | 0.014869 | 0.005521 |

## Centering diagnostics by regime

| regime | regime_label | correction | population_pairs | mean_absolute_standardized_bias | median_absolute_standardized_bias | mean_sd_to_mean_se_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| well_sampled | Well sampled | analytic | 12 | 0.008305 | 0.007679 | 1.008771 |
| well_sampled | Well sampled | jackknife | 12 | 0.006660 | 0.005223 | 1.006310 |
| moderate | Moderate | analytic | 12 | 0.028109 | 0.017112 | 1.038175 |
| moderate | Moderate | jackknife | 12 | 0.031169 | 0.019315 | 1.052303 |
| highly_sparse | Highly skewed and sparse | analytic | 12 | 0.014317 | 0.007480 | 1.023499 |
| highly_sparse | Highly skewed and sparse | jackknife | 12 | 0.019790 | 0.010966 | 1.023169 |
| ultra_sparse | Ultra-skewed and sparse | analytic | 12 | 0.100272 | 0.065080 | 1.072863 |
| ultra_sparse | Ultra-skewed and sparse | jackknife | 12 | 0.106789 | 0.040419 | 1.160744 |
| widespread_sparse | Widespread sparsity | analytic | 12 | 0.229064 | 0.225408 | 1.019236 |
| widespread_sparse | Widespread sparsity | jackknife | 12 | 0.061746 | 0.048903 | 1.068745 |
