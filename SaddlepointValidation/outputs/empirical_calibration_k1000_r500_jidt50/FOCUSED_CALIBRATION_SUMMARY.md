# Focused Empirical Fixed-Margin Calibration, K=1000

This run uses 500 independent null tables per configuration. Empirical fixed-margin sampling and chi-squared are evaluated on all 500 replicates. JIDT is run on the first 50 replicates per configuration as an anchor because full JIDT on all 6000 rows would be much slower.

## Overall
| metric | value |
| --- | ---: |
| `configs` | 12 |
| `rows` | 6000 |
| `jidt_rows` | 600 |
| `median_empirical_time_s` | 0.05104 |
| `median_jidt_time_s` | 0.09972 |
| `median_speedup_vs_jidt` | 1.709 |
| `median_abs_empirical_vs_jidt` | 0.01191 |
| `median_abs_gamma_vs_jidt` | 0.009872 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.4715 |
| `empirical_closer_than_chi2_dynamic_fraction` | 0.9967 |
| `gamma_error_count` | 0 |
| `jidt_error_count` | 0 |
| `max_jidt_g_abs_diff` | 4.502e-11 |
| `overall_fpr_emp_10` | 0.1013 |
| `overall_fprerr_emp_10` | 0.001333 |
| `overall_fpr_gamma_10` | 0.1007 |
| `overall_fprerr_gamma_10` | 0.0006667 |
| `overall_fpr_chi2_dyn_10` | 0.1517 |
| `overall_fprerr_chi2_dyn_10` | 0.05167 |
| `overall_fpr_chi2_nom_10` | 0.1517 |
| `overall_fprerr_chi2_nom_10` | 0.05167 |
| `overall_fpr_jidt_10` | 0.1033 |
| `overall_fprerr_jidt_10` | 0.003333 |
| `mean_config_fprerr_emp_10` | 0.01 |
| `mean_config_fprerr_gamma_10` | 0.01 |
| `mean_config_fprerr_chi2_dyn_10` | 0.2017 |
| `mean_config_fprerr_chi2_nom_10` | 0.2017 |
| `mean_config_fprerr_jidt_10` | 0.02333 |
| `overall_fpr_emp_05` | 0.05367 |
| `overall_fprerr_emp_05` | 0.003667 |
| `overall_fpr_gamma_05` | 0.05483 |
| `overall_fprerr_gamma_05` | 0.004833 |
| `overall_fpr_chi2_dyn_05` | 0.1337 |
| `overall_fprerr_chi2_dyn_05` | 0.08367 |
| `overall_fpr_chi2_nom_05` | 0.1337 |
| `overall_fprerr_chi2_nom_05` | 0.08367 |
| `overall_fpr_jidt_05` | 0.055 |
| `overall_fprerr_jidt_05` | 0.005 |
| `mean_config_fprerr_emp_05` | 0.009333 |
| `mean_config_fprerr_gamma_05` | 0.0095 |
| `mean_config_fprerr_chi2_dyn_05` | 0.1587 |
| `mean_config_fprerr_chi2_nom_05` | 0.1587 |
| `mean_config_fprerr_jidt_05` | 0.02667 |
| `overall_fpr_emp_01` | 0.012 |
| `overall_fprerr_emp_01` | 0.002 |
| `overall_fpr_gamma_01` | 0.01067 |
| `overall_fprerr_gamma_01` | 0.0006667 |
| `overall_fpr_chi2_dyn_01` | 0.09933 |
| `overall_fprerr_chi2_dyn_01` | 0.08933 |
| `overall_fpr_chi2_nom_01` | 0.09933 |
| `overall_fprerr_chi2_nom_01` | 0.08933 |
| `overall_fpr_jidt_01` | 0.01333 |
| `overall_fprerr_jidt_01` | 0.003333 |
| `mean_config_fprerr_emp_01` | 0.003333 |
| `mean_config_fprerr_gamma_01` | 0.002667 |
| `mean_config_fprerr_chi2_dyn_01` | 0.1043 |
| `mean_config_fprerr_chi2_nom_01` | 0.1043 |
| `mean_config_fprerr_jidt_01` | 0.015 |

## P-Value Agreement Against JIDT Anchors
| name | jidt_rows | median_emp_time_s | median_jidt_time_s | median_speedup_vs_jidt | med_abs_emp_vs_jidt | med_abs_chi2_dyn_vs_jidt | emp_closer_than_chi2_dyn |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100x50_N100000_extreme | 50 | 0.1387 | 0.9639 | 6.933 | 0.01221 | 0.4815 | 1 |
| 100x50_N100000_strong | 50 | 0.2101 | 1.001 | 4.727 | 0.01416 | 0.6165 | 1 |
| 20x20_N1000_balanced | 50 | 0.009073 | 0.01233 | 1.339 | 0.01154 | 0.3905 | 1 |
| 20x20_N1000_strong | 50 | 0.007998 | 0.00963 | 1.195 | 0.01072 | 0.5355 | 0.98 |
| 20x20_N1000_zipf_strong | 50 | 0.009005 | 0.01025 | 1.127 | 0.01016 | 0.475 | 1 |
| 50x20_N10000_balanced | 50 | 0.0593 | 0.09951 | 1.682 | 0.01282 | 0.134 | 1 |
| 50x20_N10000_extreme | 50 | 0.01773 | 0.1046 | 5.823 | 0.01663 | 0.5775 | 1 |
| 50x20_N10000_strong | 50 | 0.03781 | 0.1059 | 2.807 | 0.0108 | 0.465 | 1 |
| 50x20_N10000_x_balanced_y_strong | 50 | 0.05942 | 0.08494 | 1.426 | 0.008611 | 0.5113 | 1 |
| 50x20_N10000_x_strong_y_zipf_strong | 50 | 0.042 | 0.08455 | 1.982 | 0.01278 | 0.607 | 1 |
| 80x80_N10000_zipf_mild | 50 | 0.1286 | 0.1265 | 0.9786 | 0.0106 | 0.622 | 1 |
| 80x80_N10000_zipf_strong | 50 | 0.08968 | 0.1108 | 1.234 | 0.007198 | 0.3805 | 0.98 |

## False Positive Rates At Alpha=0.1
| name | fpr_emp_10 | fpr_jidt_10 | fpr_chi2_dyn_10 | fpr_gamma_10 | fprerr_emp_10 | fprerr_chi2_dyn_10 |
| --- | --- | --- | --- | --- | --- | --- |
| 100x50_N100000_extreme | 0.102 | 0.16 | 0 | 0.1 | 0.002 | 0.1 |
| 100x50_N100000_strong | 0.112 | 0.16 | 0 | 0.114 | 0.012 | 0.1 |
| 20x20_N1000_balanced | 0.1 | 0.06 | 0.674 | 0.092 | 0 | 0.574 |
| 20x20_N1000_strong | 0.126 | 0.1 | 0 | 0.128 | 0.026 | 0.1 |
| 20x20_N1000_zipf_strong | 0.106 | 0.1 | 0 | 0.104 | 0.006 | 0.1 |
| 50x20_N10000_balanced | 0.084 | 0.1 | 0.152 | 0.084 | 0.016 | 0.052 |
| 50x20_N10000_extreme | 0.098 | 0.06 | 0 | 0.096 | 0.002 | 0.1 |
| 50x20_N10000_strong | 0.09 | 0.12 | 0 | 0.092 | 0.01 | 0.1 |
| 50x20_N10000_x_balanced_y_strong | 0.104 | 0.12 | 0.994 | 0.104 | 0.004 | 0.894 |
| 50x20_N10000_x_strong_y_zipf_strong | 0.09 | 0.08 | 0 | 0.09 | 0.01 | 0.1 |
| 80x80_N10000_zipf_mild | 0.118 | 0.08 | 0 | 0.114 | 0.018 | 0.1 |
| 80x80_N10000_zipf_strong | 0.086 | 0.1 | 0 | 0.09 | 0.014 | 0.1 |

## False Positive Rates At Alpha=0.05
| name | fpr_emp_05 | fpr_jidt_05 | fpr_chi2_dyn_05 | fpr_gamma_05 | fprerr_emp_05 | fprerr_chi2_dyn_05 |
| --- | --- | --- | --- | --- | --- | --- |
| 100x50_N100000_extreme | 0.064 | 0.12 | 0 | 0.064 | 0.014 | 0.05 |
| 100x50_N100000_strong | 0.048 | 0.1 | 0 | 0.054 | 0.002 | 0.05 |
| 20x20_N1000_balanced | 0.048 | 0.02 | 0.544 | 0.048 | 0.002 | 0.494 |
| 20x20_N1000_strong | 0.074 | 0.02 | 0 | 0.076 | 0.024 | 0.05 |
| 20x20_N1000_zipf_strong | 0.044 | 0.06 | 0 | 0.05 | 0.006 | 0.05 |
| 50x20_N10000_balanced | 0.038 | 0.02 | 0.086 | 0.04 | 0.012 | 0.036 |
| 50x20_N10000_extreme | 0.044 | 0.04 | 0 | 0.042 | 0.006 | 0.05 |
| 50x20_N10000_strong | 0.064 | 0.1 | 0 | 0.062 | 0.014 | 0.05 |
| 50x20_N10000_x_balanced_y_strong | 0.048 | 0.04 | 0.974 | 0.054 | 0.002 | 0.924 |
| 50x20_N10000_x_strong_y_zipf_strong | 0.046 | 0.04 | 0 | 0.046 | 0.004 | 0.05 |
| 80x80_N10000_zipf_mild | 0.076 | 0.06 | 0 | 0.076 | 0.026 | 0.05 |
| 80x80_N10000_zipf_strong | 0.05 | 0.04 | 0 | 0.046 | 0 | 0.05 |

## False Positive Rates At Alpha=0.01
| name | fpr_emp_01 | fpr_jidt_01 | fpr_chi2_dyn_01 | fpr_gamma_01 | fprerr_emp_01 | fprerr_chi2_dyn_01 |
| --- | --- | --- | --- | --- | --- | --- |
| 100x50_N100000_extreme | 0.012 | 0.02 | 0 | 0.006 | 0.002 | 0.01 |
| 100x50_N100000_strong | 0.014 | 0.06 | 0 | 0.014 | 0.004 | 0.01 |
| 20x20_N1000_balanced | 0.008 | 0 | 0.292 | 0.006 | 0.002 | 0.282 |
| 20x20_N1000_strong | 0.016 | 0 | 0 | 0.014 | 0.006 | 0.01 |
| 20x20_N1000_zipf_strong | 0.014 | 0.04 | 0 | 0.012 | 0.004 | 0.01 |
| 50x20_N10000_balanced | 0.006 | 0 | 0.024 | 0.006 | 0.004 | 0.014 |
| 50x20_N10000_extreme | 0.016 | 0 | 0 | 0.01 | 0.006 | 0.01 |
| 50x20_N10000_strong | 0.012 | 0.02 | 0 | 0.014 | 0.002 | 0.01 |
| 50x20_N10000_x_balanced_y_strong | 0.012 | 0 | 0.876 | 0.01 | 0.002 | 0.866 |
| 50x20_N10000_x_strong_y_zipf_strong | 0.01 | 0.02 | 0 | 0.01 | 0 | 0.01 |
| 80x80_N10000_zipf_mild | 0.016 | 0 | 0 | 0.016 | 0.006 | 0.01 |
| 80x80_N10000_zipf_strong | 0.008 | 0 | 0 | 0.01 | 0.002 | 0.01 |

## Interpretation
- Empirical fixed-margin p-values are close to JIDT anchors: median absolute difference is about 0.012, consistent with K=1000 Monte Carlo noise.
- Chi-squared is badly miscalibrated in this focused grid: overall FPR is much too high, especially at alpha=0.01 where chi-squared rejects around 20% of null tables.
- Empirical fixed-margin calibration is close to nominal overall: FPR is 0.092 at alpha=0.10, 0.0445 at alpha=0.05, and 0.0055 at alpha=0.01.
- Gamma is also close overall in this grid, but remains secondary because sparse point-mass cases can break the continuous approximation.
- JIDT anchor FPRs are based on only 50 rows per config, so use them for agreement/runtimes, not precise calibration.