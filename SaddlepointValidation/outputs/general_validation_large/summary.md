# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 3 |
| `rows` | 3 |
| `median_gamma_time_s` | 0.2339 |
| `median_jidt_time_s` | 30.49 |
| `median_gamma_speedup_vs_jidt` | 139.4 |
| `median_abs_gamma_vs_empirical` | 0.00163 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.01237 |
| `median_abs_gamma_vs_jidt` | 0.01504 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.002255 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_gamma_speedup_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_dynamic_vs_jidt | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20x3_N2000000_strong | 1 | 0.01877 | 30.49 | 1625 | 0.002257 | 0.01237 | 0.002255 | 0 |
| 50x10_N2000000_mild | 1 | 0.2339 | 32.62 | 139.4 | 0.00163 | 0.01863 | 0.01694 | 0 |
| 80x80_N1000000_balanced | 1 | 3.162 | 10.6 | 3.354 | 0.0001336 | 0.01504 | 0.002101 | 0 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution `1 / (shuffles + 1)`.