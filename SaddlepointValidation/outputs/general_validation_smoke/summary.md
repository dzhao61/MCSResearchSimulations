# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 4 |
| `rows` | 12 |
| `median_gamma_time_s` | 0.07879 |
| `median_jidt_time_s` | 0.5231 |
| `median_gamma_speedup_vs_jidt` | 4.424 |
| `median_abs_gamma_vs_empirical` | 0.006325 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.1448 |
| `median_abs_gamma_vs_jidt` | 0.01273 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.121 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_gamma_speedup_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_dynamic_vs_jidt | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20x3_N10000_strong | 3 | 0.01358 | 0.1209 | 8.366 | 0.002675 | 0.003864 | 0.1233 | 1 |
| 50x10_N100000_mild | 3 | 0.1439 | 1.207 | 8.385 | 0.006149 | 0.01834 | 0.03903 | 1 |
| 80x80_N100000_balanced | 3 | 2.035 | 1.074 | 0.5108 | 0.00506 | 0.008237 | 0.1867 | 1 |
| 8x3_N50_strong | 3 | 0.003025 | 0.001753 | 0.8283 | 0.2445 | 0.2398 | 0.1676 | 0.3333 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution `1 / (shuffles + 1)`.