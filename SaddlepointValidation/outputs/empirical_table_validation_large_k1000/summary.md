# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 9 |
| `rows` | 9 |
| `median_gamma_time_s` | 0.03437 |
| `median_empirical_table_time_s` | 0.03437 |
| `median_jidt_time_s` | 11.36 |
| `median_empirical_speedup_vs_jidt` | 330.6 |
| `median_gamma_speedup_vs_jidt` | 330.6 |
| `median_abs_gamma_vs_empirical` | 0.007711 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.01889 |
| `median_abs_gamma_vs_jidt` | 0.008566 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.006465 |
| `median_abs_empirical_vs_jidt` | 0.009101 |
| `median_abs_chi2_nominal_vs_jidt` | 0.006465 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_empirical_speedup_vs_jidt | median_gamma_speedup_vs_jidt | median_abs_empirical_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_nominal_vs_jidt | median_abs_chi2_dynamic_vs_jidt | empirical_closer_than_chi2_dynamic_fraction | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20x3_N1000000_balanced | 1 | 0.006524 | 11.26 | 1726 | 1726 | 0.01434 | 0.01317 | 0.001173 | 0.006465 | 0.006465 | 0 | 1 |
| 20x3_N1000000_mild | 1 | 0.005066 | 11.35 | 2240 | 2240 | 0.02015 | 0.005354 | 0.0148 | 0.001258 | 0.001258 | 0 | 0 |
| 20x3_N1000000_strong | 1 | 0.003818 | 11.6 | 3039 | 3039 | 0.01534 | 0.007711 | 0.007633 | 0.002508 | 0.002508 | 0 | 0 |
| 50x10_N1000000_balanced | 1 | 0.04388 | 10.61 | 241.9 | 241.9 | 0.0006703 | 0.008001 | 0.00733 | 0.008627 | 0.008627 | 1 | 1 |
| 50x10_N1000000_mild | 1 | 0.03437 | 11.36 | 330.6 | 330.6 | 0.009101 | 0.004044 | 0.01314 | 0.005698 | 0.005698 | 0 | 0 |
| 50x10_N1000000_strong | 1 | 0.02996 | 12.25 | 408.8 | 408.8 | 0.005443 | 0.01401 | 0.008566 | 0.03239 | 0.03239 | 1 | 1 |
| 80x80_N1000000_balanced | 1 | 0.4738 | 10.6 | 22.37 | 22.37 | 0.006866 | 0.01048 | 0.01735 | 0.004622 | 0.004622 | 0 | 0 |
| 80x80_N1000000_mild | 1 | 0.4034 | 11.42 | 28.32 | 28.32 | 0.01208 | 0.00244 | 0.009644 | 0.07743 | 0.07743 | 1 | 1 |
| 80x80_N1000000_strong | 1 | 0.3903 | 12.32 | 31.55 | 31.55 | 0.00364 | 0.001609 | 0.002031 | 0.356 | 0.356 | 1 | 1 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution `1 / (shuffles + 1)`.