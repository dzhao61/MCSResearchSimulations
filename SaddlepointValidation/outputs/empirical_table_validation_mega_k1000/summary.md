# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 15 |
| `rows` | 15 |
| `median_gamma_time_s` | 0.3104 |
| `median_empirical_table_time_s` | 0.3104 |
| `median_jidt_time_s` | 29.75 |
| `median_empirical_speedup_vs_jidt` | 96.53 |
| `median_gamma_speedup_vs_jidt` | 96.53 |
| `median_abs_gamma_vs_empirical` | 0.007469 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.2413 |
| `median_abs_gamma_vs_jidt` | 0.004858 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.2382 |
| `median_abs_empirical_vs_jidt` | 0.008462 |
| `median_abs_chi2_nominal_vs_jidt` | 0.2382 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_empirical_speedup_vs_jidt | median_gamma_speedup_vs_jidt | median_abs_empirical_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_nominal_vs_jidt | median_abs_chi2_dynamic_vs_jidt | empirical_closer_than_chi2_dynamic_fraction | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100x100_N2000000_balanced | 1 | 0.7373 | 28.69 | 38.91 | 38.91 | 0.007691 | 0.01255 | 0.004858 | 0.03519 | 0.03519 | 1 | 1 |
| 100x100_N2000000_extreme | 1 | 0.3526 | 30.06 | 85.25 | 85.25 | 0.06957 | 0.005105 | 0.06446 | 0.638 | 0.638 | 1 | 1 |
| 100x100_N2000000_mild | 1 | 0.6599 | 29.75 | 45.09 | 45.09 | 0.02559 | 0.0153 | 0.01029 | 0.2157 | 0.2157 | 1 | 1 |
| 100x100_N2000000_strong | 1 | 0.6269 | 30.35 | 48.4 | 48.4 | 0.03665 | 0.004412 | 0.03224 | 0.316 | 0.316 | 1 | 1 |
| 100x100_N2000000_zipf_strong | 1 | 0.4745 | 29.16 | 61.46 | 61.46 | 0.01293 | 0.008637 | 0.004291 | 0.941 | 0.941 | 1 | 1 |
| 100x50_N2000000_balanced | 1 | 0.3925 | 25.94 | 66.1 | 66.1 | 0.008149 | 0.01105 | 0.002906 | 0.008398 | 0.008398 | 1 | 1 |
| 100x50_N2000000_extreme | 1 | 0.2026 | 30.41 | 150.2 | 150.2 | 0.00709 | 0.002389 | 0.004701 | 0.903 | 0.903 | 1 | 1 |
| 100x50_N2000000_mild | 1 | 0.335 | 29.78 | 88.89 | 88.89 | 0.003565 | 0.007469 | 0.01103 | 0.09979 | 0.09979 | 1 | 1 |
| 100x50_N2000000_strong | 1 | 0.3104 | 29.96 | 96.53 | 96.53 | 0.02544 | 0.001398 | 0.02683 | 0.536 | 0.536 | 1 | 1 |
| 100x50_N2000000_zipf_strong | 1 | 0.2793 | 29.25 | 104.7 | 104.7 | 0.003296 | 0.00577 | 0.002474 | 0.299 | 0.299 | 1 | 1 |
| 50x20_N2000000_balanced | 1 | 0.09582 | 28.67 | 299.2 | 299.2 | 0.008484 | 0.0183 | 0.009816 | 0.01423 | 0.01423 | 1 | 1 |
| 50x20_N2000000_extreme | 1 | 0.06499 | 30.29 | 466 | 466 | 0.008462 | 0.01087 | 0.01933 | 0.5257 | 0.5257 | 1 | 1 |
| 50x20_N2000000_mild | 1 | 0.07948 | 29.65 | 373 | 373 | 0.005406 | 0.002328 | 0.003077 | 0.004525 | 0.004525 | 0 | 1 |
| 50x20_N2000000_strong | 1 | 0.06347 | 30.13 | 474.8 | 474.8 | 0.01564 | 0.01225 | 0.003394 | 0.08659 | 0.08659 | 1 | 1 |
| 50x20_N2000000_zipf_strong | 1 | 0.06706 | 29.5 | 439.9 | 439.9 | 0.003099 | 0.002076 | 0.001023 | 0.2382 | 0.2382 | 1 | 1 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution `1 / (shuffles + 1)`.