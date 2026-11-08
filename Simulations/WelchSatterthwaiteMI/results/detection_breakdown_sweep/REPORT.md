# Detection and Breakdown Sweep

Profile: `full`

Frozen Git revision: `264692980043bec192da30a9707de577d6c104ff`

Simulation cells: 5,672

Table pairs: 56,720,000
Elapsed time: 81.5 seconds

## Verification

All automated run checks passed: **True**.

## Primary comparison

At alpha = 0.05 under the equal-MI, different-shape null, Expanded Welch had lower absolute calibration error than Normal Wald in 267 of 576 exact cells; Wald was lower in 277, with 32 exact ties. Configuration-level results remain the primary evidence.

## Files

- `configuration_manifest.csv`: every predeclared simulation cell.
- `population_definitions.csv`: every fixed population pair.
- `cell_results.csv`: rejection, validity, uncertainty, sparsity, and df diagnostics.
- `paired_method_results.csv`: paired rejection contrasts.
- `breakdown_frontier.csv`: sustained operating frontiers.
- `power_reversal_flags.csv`: declines exceeding three combined Monte Carlo standard errors.
- `verification_checks.json`: automated completeness and numerical checks.

## Figures

- `figures/control_calibration.png`
- `figures/breakdown_identical_distribution_balanced.png`
- `figures/breakdown_identical_distribution_strong.png`
- `figures/breakdown_identical_distribution_ultra.png`
- `figures/breakdown_equal_mi_different_shape_balanced.png`
- `figures/breakdown_equal_mi_different_shape_strong.png`
- `figures/breakdown_equal_mi_different_shape_ultra.png`
- `figures/power_identical_distribution_balanced_2x2.png`
- `figures/power_identical_distribution_balanced_3x3.png`
- `figures/power_identical_distribution_balanced_3x5.png`
- `figures/power_identical_distribution_balanced_5x5.png`
- `figures/power_identical_distribution_balanced_8x8.png`
- `figures/power_identical_distribution_strong_2x2.png`
- `figures/power_identical_distribution_strong_3x3.png`
- `figures/power_identical_distribution_strong_3x5.png`
- `figures/power_identical_distribution_strong_5x5.png`
- `figures/power_identical_distribution_strong_8x8.png`
- `figures/power_identical_distribution_ultra_2x2.png`
- `figures/power_identical_distribution_ultra_3x3.png`
- `figures/power_identical_distribution_ultra_3x5.png`
- `figures/power_identical_distribution_ultra_5x5.png`
- `figures/power_identical_distribution_ultra_8x8.png`
- `figures/power_equal_mi_different_shape_balanced_2x2.png`
- `figures/power_equal_mi_different_shape_balanced_3x3.png`
- `figures/power_equal_mi_different_shape_balanced_3x5.png`
- `figures/power_equal_mi_different_shape_balanced_5x5.png`
- `figures/power_equal_mi_different_shape_balanced_8x8.png`
- `figures/power_equal_mi_different_shape_strong_2x2.png`
- `figures/power_equal_mi_different_shape_strong_3x3.png`
- `figures/power_equal_mi_different_shape_strong_3x5.png`
- `figures/power_equal_mi_different_shape_strong_5x5.png`
- `figures/power_equal_mi_different_shape_strong_8x8.png`
- `figures/power_equal_mi_different_shape_ultra_2x2.png`
- `figures/power_equal_mi_different_shape_ultra_3x3.png`
- `figures/power_equal_mi_different_shape_ultra_3x5.png`
- `figures/power_equal_mi_different_shape_ultra_5x5.png`
- `figures/power_equal_mi_different_shape_ultra_8x8.png`
- `figures/validity_normal_wald_identical_distribution_balanced.png`
- `figures/validity_simple_welch_identical_distribution_balanced.png`
- `figures/validity_expanded_welch_identical_distribution_balanced.png`
- `figures/validity_normal_wald_identical_distribution_strong.png`
- `figures/validity_simple_welch_identical_distribution_strong.png`
- `figures/validity_expanded_welch_identical_distribution_strong.png`
- `figures/validity_normal_wald_identical_distribution_ultra.png`
- `figures/validity_simple_welch_identical_distribution_ultra.png`
- `figures/validity_expanded_welch_identical_distribution_ultra.png`
- `figures/validity_normal_wald_equal_mi_different_shape_balanced.png`
- `figures/validity_simple_welch_equal_mi_different_shape_balanced.png`
- `figures/validity_expanded_welch_equal_mi_different_shape_balanced.png`
- `figures/validity_normal_wald_equal_mi_different_shape_strong.png`
- `figures/validity_simple_welch_equal_mi_different_shape_strong.png`
- `figures/validity_expanded_welch_equal_mi_different_shape_strong.png`
- `figures/validity_normal_wald_equal_mi_different_shape_ultra.png`
- `figures/validity_simple_welch_equal_mi_different_shape_ultra.png`
- `figures/validity_expanded_welch_equal_mi_different_shape_ultra.png`
- `figures/operating_frontier.png`
- `figures/robustness_paired_difference.png`

## Interpretation note

Unconditional rejection rates are primary: invalid outcomes count as non-rejections. Power must be read beside the matching null false-positive rate; a liberal method's higher raw power is not automatically better.
