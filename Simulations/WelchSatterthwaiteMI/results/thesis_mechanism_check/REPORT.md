# Supplementary mechanism checks

This is a post-protocol diagnostic study, separate from the frozen confirmatory run.

## Design

The saved tables supply all populations. There are 809 unique configurations: the complete main grid, the 3x3 different-skew baseline and imbalance checks, and the 3x3/8x8 convergence checks. Every configuration uses 20,000 new evaluation pairs; every null also uses an independent 20,000-pair pilot. Seeds and source hashes are in metadata.json.

All five reference variants share the corrected numerator and plug-in standard error. The Hutcheson-style MI analogue uses n per component, following Hutcheson's information-theoretic Satterthwaite assignment. Simple Welch uses n-1 per component. Kurtosis-only Welch freezes the pointwise scores when differentiating the variance. Expanded Welch differentiates the complete functional. The separate observed-support sensitivity changes the numerator correction to (occupied cells - occupied rows - occupied columns + 1)/(2n). It is not a validated replacement.

Across the 809 configurations, Hutcheson-style and Simple Welch have identical rejection rates in 494 cases. Their mean absolute difference is 0.00047 and their largest difference is 0.01235, in the 5x5 uniform n=5 alternative with target MI values 0.020 and 0.022.

## Denominator diagnostic

| configuration_id | pair_id | shape | profile | n_p | n_q | target_mi_p | target_mi_q | section | replicates | pilot_sd | standardized_bias | mean_se2_over_empirical_var | empirical_var_over_first_order | normal_wald_rate | independent_mc_sd_rate | population_first_order_sd_rate | median_combined_df | numerator_se2_correlation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| config_f67e74127a56dc37 | pair_fb6e4c79f03f599b | 3x3 | different_skew | 100 | 100 | 0.02 | 0.02 | main | 20000 | 0.036674 | -0.018355 | 1.1699 | 1.4249 | 0.0166 | 0.0551 | 0.0976 | 6.0747 | -0.065882 |
| config_1b6b2afc5ccb1291 | pair_fb6e4c79f03f599b | 3x3 | different_skew | 1000 | 1000 | 0.02 | 0.02 | main | 20000 | 0.0098146 | -0.011497 | 1.0636 | 1.0205 | 0.0384 | 0.0509 | 0.05315 | 35.469 | -0.11203 |

The MC SD is estimated from the independent pilot at the known null population. It is an explanatory reference, unavailable from a single real dataset. It leaves numerator bias and non-normal shape intact, but removes the random denominator and its dependence on the numerator together. It therefore does not isolate mean variance bias alone. The population first-order SD omits quadratic sampling variation and is not the finite-sample true SD.

## Component degrees of freedom

| configuration_id | pair_id | shape | profile | n_p | n_q | target_mi_p | target_mi_q | section | population | mi | v | tau2 | mean_vhat | var_vhat | mean_vhat_over_v | n_var_ihat_over_v | population_first_order_df | empirical_moment_df | median_plugin_df | first_order_var_ratio | local_moment_df |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| config_f67e74127a56dc37 | pair_fb6e4c79f03f599b | 3x3 | different_skew | 100 | 100 | 0.02 | 0.02 | main | p | 0.02 | 0.044747 | 0.23204 | 0.078524 | 0.0025455 | 1.7548 | 1.5154 | 1.7258 | 4.8446 | 3.1437 | 1.097 | 5.5462 |
| config_f67e74127a56dc37 | pair_fb6e4c79f03f599b | 3x3 | different_skew | 100 | 100 | 0.02 | 0.02 | main | q | 0.02 | 0.049643 | 0.32675 | 0.080714 | 0.0034541 | 1.6259 | 1.3609 | 1.5084 | 3.7721 | 2.429 | 1.0571 | 5.7693 |
| config_1b6b2afc5ccb1291 | pair_fb6e4c79f03f599b | 3x3 | different_skew | 1000 | 1000 | 0.02 | 0.02 | main | p | 0.02 | 0.044747 | 0.23204 | 0.048827 | 0.00023241 | 1.0912 | 1.027 | 17.258 | 20.516 | 18.816 | 1.0016 | 25.416 |
| config_1b6b2afc5ccb1291 | pair_fb6e4c79f03f599b | 3x3 | different_skew | 1000 | 1000 | 0.02 | 0.02 | main | q | 0.02 | 0.049643 | 0.32675 | 0.053549 | 0.00032652 | 1.0787 | 1.0304 | 15.084 | 17.564 | 16.52 | 0.99927 | 27.86 |

The empirical moment df validates approximation quality; finite-difference tests only validate the derivative. These are component dfs, distinct from the combined two-sample df.

## Complete evidence

- ablation_rates.csv: every selected regime, all six arms, rejection counts, validity, MC standard errors and paired differences from Wald.
- denominator_diagnostics.csv: all selected nulls and both population-SD diagnostics.
- component_diagnostics.csv: both populations at every selected null, variance ratios and three empirical or first-order df definitions; the local-moment column in the thesis table is calculated from the recorded population V, n and table dimension.
- selected_displays.csv: exact selected settings and frozen configuration identifiers.
- ablation_2x2.pdf through ablation_8x8.pdf: main curves, rows = margin profiles, columns = n=10,100,1000. All axes use MI difference 0--0.02 and rejection 0--0.15; larger rates are outside this calibration zoom and remain in the CSV. Hollow markers mean validity below 90%.

## Strong and weak nulls

| profile | method | regimes | below | inside | above | low_valid | minimum_valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| uniform | normal_wald | 36 | 10 | 18 | 8 | 4 | 0 |
| uniform | expanded_welch | 36 | 19 | 16 | 1 | 5 | 0 |
| same_skew | normal_wald | 36 | 14 | 15 | 7 | 8 | 0 |
| same_skew | expanded_welch | 36 | 25 | 11 | 0 | 12 | 0 |
| different_skew | normal_wald | 36 | 9 | 16 | 11 | 8 | 0 |
| different_skew | expanded_welch | 36 | 19 | 13 | 4 | 12 | 0 |

These descriptive bins use the wide interval [0.025,0.075]; being inside is not proof of nominal calibration. They accompany all 108 exact main-null rates in the thesis appendix. Same-margin nulls here have P=Q; different-skew nulls have equal MI but P!=Q.
