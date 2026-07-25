# General Fixed-Margin Gamma Validation

This validates a general approximation: sample fixed-margin contingency tables with SciPy, fit a moment-matched gamma null for `G`, and compare to JIDT and chi-squared.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 12 |
| `rows` | 24 |
| `median_gamma_time_s` | 0.07703 |
| `median_jidt_time_s` | 0.5692 |
| `median_gamma_speedup_vs_jidt` | 3.02 |
| `median_abs_gamma_vs_empirical` | 0.003773 |
| `median_abs_chi2_dynamic_vs_empirical` | 0.05978 |
| `median_abs_gamma_vs_jidt` | 0.01118 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.05403 |

## Per Configuration
| name | replicates | median_gamma_time_s | median_jidt_time_s | median_gamma_speedup_vs_jidt | median_abs_gamma_vs_empirical | median_abs_gamma_vs_jidt | median_abs_chi2_dynamic_vs_jidt | gamma_closer_than_chi2_dynamic_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20x3_N10000_balanced | 2 | 0.0159 | 0.1073 | 6.721 | 0.001812 | 0.006712 | 0.006758 | 0.5 |
| 20x3_N10000_mild | 2 | 0.01517 | 0.07431 | 4.899 | 0.007266 | 0.001444 | 0.01289 | 1 |
| 20x3_N10000_strong | 2 | 0.01353 | 0.07252 | 5.36 | 0.002829 | 0.003306 | 0.04609 | 1 |
| 50x10_N100000_balanced | 2 | 0.1602 | 1.17 | 7.303 | 0.004192 | 0.001824 | 0.006548 | 1 |
| 50x10_N100000_mild | 2 | 0.1489 | 1.277 | 8.576 | 0.003461 | 0.01072 | 0.01347 | 0.5 |
| 50x10_N100000_strong | 2 | 0.1382 | 1.417 | 10.26 | 0.00792 | 0.0194 | 0.2737 | 1 |
| 80x80_N100000_balanced | 2 | 2.024 | 1.051 | 0.5197 | 0.004159 | 0.01699 | 0.1461 | 1 |
| 80x80_N100000_mild | 2 | 1.926 | 1.376 | 0.7137 | 0.001285 | 0.02866 | 0.3915 | 1 |
| 80x80_N100000_strong | 2 | 1.229 | 1.133 | 0.9216 | 0.001624 | 0.01169 | 0.582 | 1 |
| 8x3_N50_balanced | 2 | 0.003703 | 0.003318 | 0.8928 | 0.003796 | 0.004708 | 0.06485 | 1 |
| 8x3_N50_mild | 2 | 0.004199 | 0.0006684 | 0.159 | 0.005762 | 0.01718 | 0.0541 | 1 |
| 8x3_N50_strong | 2 | 0.002411 | 0.0005172 | 0.231 | 0.1338 | 0.1331 | 0.09849 | 0.5 |

## Interpretation Notes
- `empirical_fixed_margin_p` is the direct Monte Carlo p-value from fixed-margin table samples.
- `gamma_fixed_margin_p` is the moment-matched gamma approximation fitted from those same samples.
- If gamma and empirical table-sampling disagree strongly, gamma is not trustworthy for that table even if table sampling itself is valid.
- JIDT p-values have Monte Carlo noise and resolution `1 / (shuffles + 1)`.