# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 15 |
| `rows` | 15 |
| `median_gamma_time_s` | 0.3079 |
| `median_empirical_table_time_s` | 0.3079 |
| `median_jidt_time_s` | 28.25 |
| `median_empirical_speedup_vs_jidt` | 91.01 |
| `median_gamma_speedup_vs_jidt` | 91.01 |
| `median_abs_gamma_vs_empirical` | 0.007469 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.2413 |
| `median_abs_gamma_vs_jidt` | 0.006394 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.2442 |
| `median_abs_empirical_vs_jidt` | 0.0133 |
| `median_abs_chi2_nominal_vs_jidt` | 0.2442 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_empirical_speedup_vs_jidt | median_gamma_speedup_vs_jidt | median_abs_empirical_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_nominal_vs_jidt | median_abs_chi2_dynamic_vs_jidt | empirical_closer_than_chi2_dynamic_fraction | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100x100_N2000000_balanced | 1 | 0.7382 | 26.09 | 35.34 | 35.34 | 0.009691 | 0.01255 | 0.002858 | 0.03319 | 0.03319 | 1 | 1 |
| 100x100_N2000000_extreme | 1 | 0.3858 | 29.65 | 76.87 | 76.87 | 0.04357 | 0.005105 | 0.03846 | 0.612 | 0.612 | 1 | 1 |
| 100x100_N2000000_mild | 1 | 0.6545 | 27.73 | 42.37 | 42.37 | 0.02859 | 0.0153 | 0.01329 | 0.2127 | 0.2127 | 1 | 1 |
| 100x100_N2000000_strong | 1 | 0.6229 | 31.21 | 50.1 | 50.1 | 0.001647 | 0.004412 | 0.002765 | 0.351 | 0.351 | 1 | 1 |
| 100x100_N2000000_zipf_strong | 1 | 0.4764 | 28.9 | 60.66 | 60.66 | 0.01693 | 0.008637 | 0.008291 | 0.945 | 0.945 | 1 | 1 |
| 100x50_N2000000_balanced | 1 | 0.3938 | 26.09 | 66.26 | 66.26 | 0.002149 | 0.01105 | 0.008906 | 0.002398 | 0.002398 | 1 | 0 |
| 100x50_N2000000_extreme | 1 | 0.244 | 30.61 | 125.4 | 125.4 | 0.00709 | 0.002389 | 0.004701 | 0.903 | 0.903 | 1 | 1 |
| 100x50_N2000000_mild | 1 | 0.3305 | 27.99 | 84.7 | 84.7 | 0.007435 | 0.007469 | 3.399e-05 | 0.08879 | 0.08879 | 1 | 1 |
| 100x50_N2000000_strong | 1 | 0.3079 | 28.02 | 91.01 | 91.01 | 0.02144 | 0.001398 | 0.02283 | 0.54 | 0.54 | 1 | 1 |
| 100x50_N2000000_zipf_strong | 1 | 0.305 | 28.57 | 93.68 | 93.68 | 0.0133 | 0.00577 | 0.007526 | 0.309 | 0.309 | 1 | 1 |
| 50x20_N2000000_balanced | 1 | 0.09527 | 28.52 | 299.3 | 299.3 | 0.01348 | 0.0183 | 0.004816 | 0.009234 | 0.009234 | 0 | 1 |
| 50x20_N2000000_extreme | 1 | 0.06489 | 30.29 | 466.9 | 466.9 | 0.004538 | 0.01087 | 0.00633 | 0.5387 | 0.5387 | 1 | 1 |
| 50x20_N2000000_mild | 1 | 0.07088 | 28.25 | 398.5 | 398.5 | 0.03459 | 0.002328 | 0.03692 | 0.04453 | 0.04453 | 1 | 1 |
| 50x20_N2000000_strong | 1 | 0.06224 | 28.05 | 450.7 | 450.7 | 0.01864 | 0.01225 | 0.006394 | 0.08959 | 0.08959 | 1 | 1 |
| 50x20_N2000000_zipf_strong | 1 | 0.06941 | 28.12 | 405.1 | 405.1 | 0.002901 | 0.002076 | 0.004977 | 0.2442 | 0.2442 | 1 | 1 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution around `1 / shuffles`; finite-sample p-value conventions may differ by about `1 / shuffles`.
