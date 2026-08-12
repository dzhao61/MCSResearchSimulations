# Corrected Satterthwaite Check

This experiment changes only the final combination of the two expanded
component degrees of freedom. The corrected candidate uses

$$
\widehat\nu_{\mathrm{corrected}}=
\frac{(C_P+C_Q)^2}
{C_P^2/(\widehat\nu_V(P)+2)+C_Q^2/(\widehat\nu_V(Q)+2)}-2,
$$

where $C_P=\widehat V(P)/n_P$ and
$C_Q=\widehat V(Q)/n_Q$. The MI difference and standard error are
identical for both methods.

## Overall null calibration

| Alpha | Current MAE | Corrected MAE | Relative change | Corrected/current/tied scenarios |
| ---: | ---: | ---: | ---: | ---: |
| 0.10 | 0.00801 | 0.00780 | -2.6% | 33/16/143 |
| 0.05 | 0.00577 | 0.00567 | -1.7% | 36/19/137 |
| 0.01 | 0.00207 | 0.00205 | -1.2% | 27/18/147 |

A negative relative change means that the correction reduced mean
absolute false-positive-rate error.

## Power

Mean alpha-0.05 power change: `+0.00040`. 
Range across alternatives: `+0.00010` to 
`+0.00090`.

## Conclusion

The correction increased the median effective degrees of freedom from
`294.29` to `296.32` and therefore made the test slightly less conservative.
Across approximately 1.92 million valid null comparisons, this changed only
`593`, `432`, and `212` rejection decisions at alpha `0.10`, `0.05`, and
`0.01`, respectively.

The overall mean absolute calibration error fell by `0.00021` at alpha `0.10`,
`0.00010` at alpha `0.05`, and `0.00002` at alpha `0.01`. The alpha-`0.10`
change was the clearest paired improvement (`p=0.009`); the alpha-`0.05` and
alpha-`0.01` changes were not clearly distinguishable from zero by paired
t-tests (`p=0.060` and `p=0.364`).

The aggregate improvement came from widespread sparsity, where the current
expanded method is strongly conservative. After removing that regime, the
correction changed mean absolute error by `+0.000002`, `+0.000022`, and
`+0.000006` at the three alpha levels, with positive values indicating a
slight worsening. Across the sparse-and-imbalanced, highly skewed, and
ultra-skewed target regimes, it worsened error by `0.000053`, `0.000049`, and
`0.000042`.

The corrected equation is mathematically relevant, but it does not provide a
consistent practical improvement for this MI test. The current expanded
Welch-Satterthwaite equation should remain the primary method.

## Regime detail

| regime | regime_label | method | method_label | scenarios | mean_valid_rate | median_df | mean_fpr_10 | mean_absolute_error_10 | mean_fpr_05 | mean_absolute_error_05 | mean_fpr_01 | mean_absolute_error_01 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| well_sampled | Well sampled | expanded_welch | Expanded Welch | 24 | 1.00000 | 336.45466 | 0.09398 | 0.00612 | 0.04505 | 0.00516 | 0.00789 | 0.00217 |
| well_sampled | Well sampled | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 338.45703 | 0.09406 | 0.00604 | 0.04512 | 0.00510 | 0.00790 | 0.00216 |
| moderate | Moderate | expanded_welch | Expanded Welch | 24 | 1.00000 | 213.51945 | 0.09498 | 0.00593 | 0.04645 | 0.00411 | 0.00872 | 0.00152 |
| moderate | Moderate | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 215.27454 | 0.09516 | 0.00592 | 0.04662 | 0.00414 | 0.00886 | 0.00158 |
| sparse_imbalanced | Sparse and imbalanced | expanded_welch | Expanded Welch | 24 | 1.00000 | 210.12865 | 0.10464 | 0.00537 | 0.05350 | 0.00410 | 0.01142 | 0.00155 |
| sparse_imbalanced | Sparse and imbalanced | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 211.15557 | 0.10476 | 0.00549 | 0.05357 | 0.00418 | 0.01149 | 0.00162 |
| highly_sparse | Highly skewed and sparse | expanded_welch | Expanded Welch | 24 | 1.00000 | 17067.64263 | 0.09960 | 0.00274 | 0.05002 | 0.00245 | 0.01019 | 0.00114 |
| highly_sparse | Highly skewed and sparse | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 17069.22065 | 0.09961 | 0.00275 | 0.05007 | 0.00249 | 0.01022 | 0.00117 |
| ultra_sparse | Ultra-skewed and sparse | expanded_welch | Expanded Welch | 24 | 1.00000 | 4267.92468 | 0.10189 | 0.00331 | 0.05159 | 0.00220 | 0.01055 | 0.00086 |
| ultra_sparse | Ultra-skewed and sparse | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 4268.93655 | 0.10192 | 0.00334 | 0.05163 | 0.00222 | 0.01058 | 0.00089 |
| widespread_sparse | Widespread sparsity | expanded_welch | Expanded Welch | 24 | 0.99154 | 39.38940 | 0.08208 | 0.02455 | 0.03673 | 0.01730 | 0.00532 | 0.00559 |
| widespread_sparse | Widespread sparsity | corrected_expanded_welch | Corrected expanded Welch | 24 | 0.99154 | 41.36993 | 0.08379 | 0.02290 | 0.03767 | 0.01638 | 0.00557 | 0.00536 |
| shape_mismatch | Equal-MI shape mismatch | expanded_welch | Expanded Welch | 24 | 1.00000 | 433.51069 | 0.10178 | 0.00802 | 0.05095 | 0.00535 | 0.01016 | 0.00193 |
| shape_mismatch | Equal-MI shape mismatch | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 435.50994 | 0.10188 | 0.00795 | 0.05106 | 0.00525 | 0.01020 | 0.00190 |
| extreme_imbalance | Extreme sample imbalance | expanded_welch | Expanded Welch | 24 | 1.00000 | 102.31411 | 0.10220 | 0.00805 | 0.05122 | 0.00546 | 0.01013 | 0.00184 |
| extreme_imbalance | Extreme sample imbalance | corrected_expanded_welch | Corrected expanded Welch | 24 | 1.00000 | 102.49800 | 0.10249 | 0.00805 | 0.05158 | 0.00561 | 0.01046 | 0.00174 |

Elapsed time: `25.96` seconds.

Source: Matthias von Davier (2026), *A Corrected Welch
Satterthwaite Equation*, arXiv:2602.20912.
