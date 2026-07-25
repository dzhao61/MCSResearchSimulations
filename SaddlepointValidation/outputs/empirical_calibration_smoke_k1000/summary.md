# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 12 |
| `rows` | 24 |
| `median_gamma_time_s` | 0.04787 |
| `median_empirical_table_time_s` | 0.04787 |
| `median_jidt_time_s` | 0.1048 |
| `median_empirical_speedup_vs_jidt` | 2.338 |
| `median_gamma_speedup_vs_jidt` | 2.338 |
| `median_abs_gamma_vs_empirical` | 0.007223 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.5099 |
| `median_abs_gamma_vs_jidt` | 0.009318 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.6263 |
| `median_abs_empirical_vs_jidt` | 0.008712 |
| `median_abs_chi2_nominal_vs_jidt` | 0.6263 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_empirical_speedup_vs_jidt | median_gamma_speedup_vs_jidt | median_abs_empirical_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_nominal_vs_jidt | median_abs_chi2_dynamic_vs_jidt | empirical_closer_than_chi2_dynamic_fraction | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100x50_N100000_extreme | 2 | 0.131 | 1.048 | 8.022 | 8.022 | 0.007647 | 0.00659 | 0.009936 | 0.655 | 0.655 | 1 | 1 |
| 100x50_N100000_strong | 2 | 0.1984 | 1.435 | 7.223 | 7.223 | 0.004357 | 0.00866 | 0.02065 | 0.361 | 0.361 | 1 | 1 |
| 20x20_N1000_balanced | 2 | 0.01012 | 0.0264 | 2.554 | 2.554 | 0.01478 | 0.007454 | 0.01576 | 0.5977 | 0.5977 | 1 | 1 |
| 20x20_N1000_strong | 2 | 0.008399 | 0.01074 | 1.322 | 1.322 | 0.009776 | 0.008096 | 0.0004559 | 0.786 | 0.786 | 1 | 1 |
| 20x20_N1000_zipf_strong | 2 | 0.00905 | 0.0109 | 1.201 | 1.201 | 0.00227 | 0.0103 | 0.01292 | 0.728 | 0.728 | 1 | 1 |
| 50x20_N10000_balanced | 2 | 0.05891 | 0.1285 | 2.122 | 2.122 | 0.02031 | 0.004837 | 0.02466 | 0.1543 | 0.1543 | 1 | 1 |
| 50x20_N10000_extreme | 2 | 0.01726 | 0.1101 | 6.451 | 6.451 | 0.006776 | 0.02639 | 0.007812 | 0.783 | 0.783 | 1 | 1 |
| 50x20_N10000_strong | 2 | 0.03646 | 0.1108 | 3.036 | 3.036 | 0.02256 | 0.00573 | 0.01682 | 0.422 | 0.422 | 1 | 1 |
| 50x20_N10000_x_balanced_y_strong | 2 | 0.05617 | 0.08339 | 1.482 | 1.482 | 0.005333 | 0.009213 | 0.002634 | 0.66 | 0.66 | 1 | 1 |
| 50x20_N10000_x_strong_y_zipf_strong | 2 | 0.03935 | 0.1067 | 2.734 | 2.734 | 0.0135 | 0.006711 | 0.005926 | 0.488 | 0.488 | 1 | 1 |
| 80x80_N10000_zipf_mild | 2 | 0.1292 | 0.1029 | 0.7678 | 0.7678 | 0.005045 | 0.005892 | 0.006132 | 0.95 | 0.95 | 1 | 1 |
| 80x80_N10000_zipf_strong | 2 | 0.0854 | 0.0856 | 1.006 | 1.006 | 0.01205 | 0.01223 | 0.0087 | 0.059 | 0.059 | 1 | 1 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution around `1 / shuffles`; finite-sample p-value conventions may differ by about `1 / shuffles`.