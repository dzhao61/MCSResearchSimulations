# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 12 |
| `rows` | 6000 |
| `median_gamma_time_s` | 0.05104 |
| `median_empirical_table_time_s` | 0.05104 |
| `median_jidt_time_s` | 0.09972 |
| `median_empirical_speedup_vs_jidt` | 1.709 |
| `median_gamma_speedup_vs_jidt` | 1.709 |
| `median_abs_gamma_vs_empirical` | 0.005259 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.4466 |
| `median_abs_gamma_vs_jidt` | 0.009872 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.4715 |
| `median_abs_empirical_vs_jidt` | 0.01191 |
| `median_abs_chi2_nominal_vs_jidt` | 0.4715 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_empirical_speedup_vs_jidt | median_gamma_speedup_vs_jidt | median_abs_empirical_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_nominal_vs_jidt | median_abs_chi2_dynamic_vs_jidt | empirical_closer_than_chi2_dynamic_fraction | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100x50_N100000_extreme | 500 | 0.1387 | 0.9639 | 6.933 | 6.933 | 0.01221 | 0.005442 | 0.00981 | 0.4815 | 0.4815 | 1 | 1 |
| 100x50_N100000_strong | 500 | 0.2101 | 1.001 | 4.727 | 4.727 | 0.01416 | 0.005151 | 0.01294 | 0.6165 | 0.6165 | 1 | 1 |
| 20x20_N1000_balanced | 500 | 0.009073 | 0.01233 | 1.339 | 1.339 | 0.01154 | 0.005083 | 0.009067 | 0.3905 | 0.3905 | 1 | 1 |
| 20x20_N1000_strong | 500 | 0.007998 | 0.00963 | 1.195 | 1.195 | 0.01072 | 0.005176 | 0.009864 | 0.5355 | 0.5355 | 0.98 | 1 |
| 20x20_N1000_zipf_strong | 500 | 0.009005 | 0.01025 | 1.127 | 1.127 | 0.01016 | 0.005133 | 0.008594 | 0.475 | 0.475 | 1 | 1 |
| 50x20_N10000_balanced | 500 | 0.0593 | 0.09951 | 1.682 | 1.682 | 0.01282 | 0.004631 | 0.00947 | 0.134 | 0.134 | 1 | 1 |
| 50x20_N10000_extreme | 500 | 0.01773 | 0.1046 | 5.823 | 5.823 | 0.01663 | 0.01352 | 0.01708 | 0.5775 | 0.5775 | 1 | 1 |
| 50x20_N10000_strong | 500 | 0.03781 | 0.1059 | 2.807 | 2.807 | 0.0108 | 0.004692 | 0.008001 | 0.465 | 0.465 | 1 | 1 |
| 50x20_N10000_x_balanced_y_strong | 500 | 0.05942 | 0.08494 | 1.426 | 1.426 | 0.008611 | 0.004686 | 0.007015 | 0.5113 | 0.5113 | 1 | 1 |
| 50x20_N10000_x_strong_y_zipf_strong | 500 | 0.042 | 0.08455 | 1.982 | 1.982 | 0.01278 | 0.004835 | 0.01043 | 0.607 | 0.607 | 1 | 1 |
| 80x80_N10000_zipf_mild | 500 | 0.1286 | 0.1265 | 0.9786 | 0.9786 | 0.0106 | 0.004374 | 0.008814 | 0.622 | 0.622 | 1 | 1 |
| 80x80_N10000_zipf_strong | 500 | 0.08968 | 0.1108 | 1.234 | 1.234 | 0.007198 | 0.005374 | 0.009291 | 0.3805 | 0.3805 | 0.98 | 0.98 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples. This is the primary method for this empirical-table validation.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution around `1 / shuffles`; finite-sample p-value conventions may differ by about `1 / shuffles`.