# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 6 |
| `rows` | 12 |
| `median_gamma_time_s` | 0.0426 |
| `median_empirical_table_time_s` | 0.0426 |
| `median_jidt_time_s` | 0.3216 |
| `median_empirical_speedup_vs_jidt` | 13.62 |
| `median_gamma_speedup_vs_jidt` | 13.62 |
| `median_abs_gamma_vs_empirical` | 0.005795 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.01392 |
| `median_abs_gamma_vs_jidt` | 0.01012 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.02335 |
| `median_abs_jidt_analytic_nominal_vs_jidt` | 0.2583 |
| `median_abs_jidt_analytic_bits_nominal_vs_jidt` | 0.2583 |
| `median_abs_empirical_vs_jidt` | 0.01337 |
| `median_abs_chi2_nominal_vs_jidt` | 0.02335 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_empirical_speedup_vs_jidt | median_gamma_speedup_vs_jidt | median_abs_empirical_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_nominal_vs_jidt | median_abs_chi2_dynamic_vs_jidt | median_abs_jidt_analytic_nominal_vs_jidt | empirical_closer_than_chi2_dynamic_fraction | empirical_closer_than_jidt_analytic_nominal_fraction | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100x50_N500000_balanced | 2 | 0.3353 | 5 | 14.9 | 14.9 | 0.01582 | 0.003812 | 0.008613 | 0.02259 | 0.02259 | 0.162 | 1 | 1 | 1 |
| 10x10_N10000_balanced | 2 | 0.006225 | 0.1016 | 15.7 | 15.7 | 0.01681 | 0.003811 | 0.01164 | 0.02597 | 0.02597 | 0.763 | 1 | 1 | 1 |
| 20x20_N10000_balanced | 2 | 0.02394 | 0.1086 | 4.441 | 4.441 | 0.01032 | 0.007177 | 0.01823 | 0.02411 | 0.02411 | 0.673 | 1 | 1 | 1 |
| 50x20_N50000_balanced | 2 | 0.06223 | 0.5346 | 8.39 | 8.39 | 0.007986 | 0.003121 | 0.006791 | 0.003327 | 0.003327 | 0.006 | 0 | 0 | 0 |
| 50x50_N250000_balanced | 2 | 0.1633 | 2.468 | 14.84 | 14.84 | 0.01091 | 0.006869 | 0.004496 | 0.01378 | 0.01378 | 0.078 | 1 | 1 | 1 |
| 5x5_N1000_balanced | 2 | 0.001671 | 0.02029 | 12.39 | 12.39 | 0.03641 | 0.008233 | 0.03202 | 0.02731 | 0.02731 | 0.3547 | 0 | 1 | 0 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- `chi2_*` columns use the standard likelihood-ratio statistic `2N * MI_nats`.
- `jidt_analytic_bits_nominal_p` reproduces JIDT's built-in analytic convention: nominal df and `2N * MI_bits`.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution around `1 / shuffles`; finite-sample p-value conventions may differ by about `1 / shuffles`.