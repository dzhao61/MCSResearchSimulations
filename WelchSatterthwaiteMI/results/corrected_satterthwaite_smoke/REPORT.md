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
| 0.10 | 0.01608 | 0.01543 | -4.0% | 7/2/39 |
| 0.05 | 0.01284 | 0.01283 | -0.0% | 6/5/37 |
| 0.01 | 0.00458 | 0.00437 | -4.5% | 5/1/42 |

A negative relative change means that the correction reduced mean
absolute false-positive-rate error.

## Power

Mean alpha-0.05 power change: `+0.00080`. 
Range across alternatives: `+0.00000` to 
`+0.00200`.

## Regime detail

| regime | regime_label | method | method_label | scenarios | mean_valid_rate | median_df | mean_fpr_10 | mean_absolute_error_10 | mean_fpr_05 | mean_absolute_error_05 | mean_fpr_01 | mean_absolute_error_01 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| well_sampled | Well sampled | expanded_welch | Expanded Welch | 6 | 1.00000 | 68.22080 | 0.08833 | 0.01300 | 0.04433 | 0.00900 | 0.00633 | 0.00367 |
| well_sampled | Well sampled | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 70.24287 | 0.08833 | 0.01300 | 0.04433 | 0.00900 | 0.00667 | 0.00333 |
| moderate | Moderate | expanded_welch | Expanded Welch | 6 | 1.00000 | 42.40552 | 0.09033 | 0.01233 | 0.04733 | 0.01000 | 0.00800 | 0.00467 |
| moderate | Moderate | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 44.54071 | 0.09067 | 0.01200 | 0.04900 | 0.01100 | 0.00833 | 0.00433 |
| sparse_imbalanced | Sparse and imbalanced | expanded_welch | Expanded Welch | 6 | 1.00000 | 60.27967 | 0.10467 | 0.01400 | 0.05867 | 0.01267 | 0.01433 | 0.00500 |
| sparse_imbalanced | Sparse and imbalanced | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 61.30419 | 0.10467 | 0.01400 | 0.05900 | 0.01300 | 0.01467 | 0.00533 |
| highly_sparse | Highly skewed and sparse | expanded_welch | Expanded Welch | 6 | 1.00000 | 715.81076 | 0.10900 | 0.01100 | 0.05833 | 0.00833 | 0.01533 | 0.00533 |
| highly_sparse | Highly skewed and sparse | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 717.48207 | 0.10900 | 0.01100 | 0.05867 | 0.00867 | 0.01533 | 0.00533 |
| ultra_sparse | Ultra-skewed and sparse | expanded_welch | Expanded Welch | 6 | 1.00000 | 185.72724 | 0.10667 | 0.01333 | 0.05500 | 0.01033 | 0.01133 | 0.00333 |
| ultra_sparse | Ultra-skewed and sparse | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 187.18557 | 0.10667 | 0.01333 | 0.05533 | 0.01067 | 0.01133 | 0.00333 |
| widespread_sparse | Widespread sparsity | expanded_welch | Expanded Welch | 6 | 0.96900 | 9.74124 | 0.06371 | 0.03629 | 0.02432 | 0.02568 | 0.00234 | 0.00766 |
| widespread_sparse | Widespread sparsity | corrected_expanded_welch | Corrected expanded Welch | 6 | 0.96900 | 11.73495 | 0.07020 | 0.02980 | 0.02568 | 0.02432 | 0.00267 | 0.00733 |
| shape_mismatch | Equal-MI shape mismatch | expanded_welch | Expanded Welch | 6 | 1.00000 | 80.21882 | 0.10033 | 0.00633 | 0.05067 | 0.00933 | 0.00633 | 0.00367 |
| shape_mismatch | Equal-MI shape mismatch | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 82.59124 | 0.10133 | 0.00733 | 0.05100 | 0.00900 | 0.00633 | 0.00367 |
| extreme_imbalance | Extreme sample imbalance | expanded_welch | Expanded Welch | 6 | 1.00000 | 31.04555 | 0.11033 | 0.02233 | 0.05667 | 0.01733 | 0.00800 | 0.00333 |
| extreme_imbalance | Extreme sample imbalance | corrected_expanded_welch | Corrected expanded Welch | 6 | 1.00000 | 31.48341 | 0.11100 | 0.02300 | 0.05767 | 0.01700 | 0.00900 | 0.00233 |

Elapsed time: `3.98` seconds.

Source: Matthias von Davier (2026), *A Corrected Welch
Satterthwaite Equation*, arXiv:2602.20912.
