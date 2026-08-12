# Supervisor Experiment: Differential Mutual Information

Profile: `full`. Each null population used `10,000` independently simulated table pairs.

## Experiment in one sentence

Generate two different categorical populations with exactly equal true
mutual information, repeatedly sample one table from each, and check how
often each analytic test incorrectly rejects equality.

## Design

The null grid contains 192 fixed
population pairs across 8 regimes. Every method sees
the same table pairs and uses the same bias-corrected MI difference and
standard error.

- **Well sampled:** Equal sample sizes and high observations per cell; includes one near-balanced and one skewed-margin variant.
- **Moderate:** A 2:1 sample-size ratio and moderate observations per cell, with increasingly heterogeneous margins.
- **Sparse and imbalanced:** A 4:1 sample-size ratio, low observations per cell, and heterogeneous margins.
- **Highly skewed and sparse:** Both populations have minimum true expected cell counts from 1 (inclusive) to 5 (exclusive), with heterogeneous margins.
- **Ultra-skewed and sparse:** Both populations have positive minimum true expected cell counts below 1, so their rarest cells are usually unobserved.
- **Widespread sparsity:** In both populations, 25-50% of cells have true expected counts below 1 and at least half have expected counts below 5.
- **Equal-MI shape mismatch:** A near-balanced population is compared with a strongly skewed population having exactly the same mutual information.
- **Extreme sample imbalance:** Sample-size ratios of 1:10 and 1:20 stress the unequal-variance combination beyond the main grid.

The methods differ only in reference calibration: normal Wald uses
a standard normal distribution, simple Welch uses ordinary `n-1`
component degrees of freedom, and expanded Welch estimates component
degrees of freedom from the MI-variance influence function.

## Rejection calibration

The figure traces the empirical rejection probability over nominal
significance levels from 0 to 0.10. A calibrated test follows the
diagonal. Curves above it are liberal and curves below it are
conservative. Each line is the equal-weight mean across population
pairs in that regime; shading spans their 10th to 90th percentiles.

![Rejection calibration](rejection_calibration.png)

## Main calibration results

| Regime | Method | FPR at 0.05 | Error at 0.05 | FPR at 0.01 | Error at 0.01 | Valid rate | 95% coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Well sampled | Normal Wald | 0.04660 | 0.00377 | 0.00860 | 0.00154 | 1.00000 | 0.95340 |
| Well sampled | Simple Welch | 0.04653 | 0.00384 | 0.00857 | 0.00157 | 1.00000 | 0.95347 |
| Well sampled | Expanded Welch | 0.04505 | 0.00516 | 0.00789 | 0.00217 | 1.00000 | 0.95495 |
| Moderate | Normal Wald | 0.04865 | 0.00363 | 0.01005 | 0.00167 | 1.00000 | 0.95135 |
| Moderate | Simple Welch | 0.04840 | 0.00366 | 0.00995 | 0.00163 | 1.00000 | 0.95160 |
| Moderate | Expanded Welch | 0.04645 | 0.00411 | 0.00872 | 0.00152 | 1.00000 | 0.95355 |
| Sparse and imbalanced | Normal Wald | 0.05598 | 0.00631 | 0.01292 | 0.00299 | 1.00000 | 0.94402 |
| Sparse and imbalanced | Simple Welch | 0.05545 | 0.00581 | 0.01264 | 0.00271 | 1.00000 | 0.94455 |
| Sparse and imbalanced | Expanded Welch | 0.05350 | 0.00410 | 0.01142 | 0.00155 | 1.00000 | 0.94650 |
| Highly skewed and sparse | Normal Wald | 0.05063 | 0.00298 | 0.01061 | 0.00153 | 1.00000 | 0.94937 |
| Highly skewed and sparse | Simple Welch | 0.05050 | 0.00288 | 0.01053 | 0.00146 | 1.00000 | 0.94950 |
| Highly skewed and sparse | Expanded Welch | 0.05002 | 0.00245 | 0.01019 | 0.00114 | 1.00000 | 0.94998 |
| Ultra-skewed and sparse | Normal Wald | 0.05243 | 0.00270 | 0.01099 | 0.00125 | 1.00000 | 0.94757 |
| Ultra-skewed and sparse | Simple Welch | 0.05224 | 0.00257 | 0.01090 | 0.00116 | 1.00000 | 0.94776 |
| Ultra-skewed and sparse | Expanded Welch | 0.05159 | 0.00220 | 0.01055 | 0.00086 | 1.00000 | 0.94841 |
| Widespread sparsity | Normal Wald | 0.04732 | 0.01036 | 0.00836 | 0.00392 | 0.99980 | 0.95268 |
| Widespread sparsity | Simple Welch | 0.04665 | 0.01041 | 0.00801 | 0.00415 | 0.99980 | 0.95335 |
| Widespread sparsity | Expanded Welch | 0.03673 | 0.01730 | 0.00532 | 0.00559 | 0.99154 | 0.96327 |
| Equal-MI shape mismatch | Normal Wald | 0.05257 | 0.00459 | 0.01097 | 0.00168 | 1.00000 | 0.94743 |
| Equal-MI shape mismatch | Simple Welch | 0.05237 | 0.00463 | 0.01082 | 0.00163 | 1.00000 | 0.94763 |
| Equal-MI shape mismatch | Expanded Welch | 0.05095 | 0.00535 | 0.01016 | 0.00193 | 1.00000 | 0.94905 |
| Extreme sample imbalance | Normal Wald | 0.05628 | 0.00850 | 0.01397 | 0.00450 | 1.00000 | 0.94372 |
| Extreme sample imbalance | Simple Welch | 0.05556 | 0.00785 | 0.01346 | 0.00399 | 1.00000 | 0.94444 |
| Extreme sample imbalance | Expanded Welch | 0.05122 | 0.00546 | 0.01013 | 0.00184 | 1.00000 | 0.94878 |

False-positive-rate error is the absolute difference between observed
and nominal rejection rates among valid calculations, so lower is
better. Validity is reported separately so undefined calculations
are not hidden by conditioning only on successful results.

## Overall summary

| Method | MAE at 0.10 | MAE at 0.05 | MAE at 0.01 | Mean valid rate | 95% coverage |
| --- | --- | --- | --- | --- | --- |
| Normal Wald | 0.00732 | 0.00535 | 0.00239 | 0.99998 | 0.94869 |
| Simple Welch | 0.00713 | 0.00521 | 0.00229 | 0.99998 | 0.94904 |
| Expanded Welch | 0.00801 | 0.00577 | 0.00207 | 0.99894 | 0.95181 |

## Direct interpretation

- Relative calibration changes in the difficult regimes are
  reported directly below; positive percentages mean that expanded
  Welch reduced error relative to normal Wald.
- **Sparse and imbalanced:** 35.0% at alpha 0.05 and 48.2% at alpha 0.01.
- **Highly skewed and sparse:** 17.9% at alpha 0.05 and 25.1% at alpha 0.01.
- **Ultra-skewed and sparse:** 18.4% at alpha 0.05 and 31.2% at alpha 0.01.
- **Widespread sparsity:** -67.0% at alpha 0.05 and -42.8% at alpha 0.01.
- **Equal-MI shape mismatch:** -16.6% at alpha 0.05 and -14.4% at alpha 0.01.
- **Extreme sample imbalance:** 35.8% at alpha 0.05 and 59.1% at alpha 0.01.
- This was not a universal improvement. In well-sampled tables at
  alpha 0.05, expanded Welch increased mean absolute error from
  `0.00377`
  to `0.00516`
  by becoming mildly conservative.
- Across the five power scenarios, expanded Welch lost
  `0.0102` power on average and at most
  `0.0123` relative to normal Wald.
- The simple Welch correction changed both calibration and power only
  slightly, consistent with its usually large effective degrees of freedom.
- Scenario-level Wilson intervals, sparsity diagnostics, validity rates,
  and effective degrees of freedom are retained in `scenario_results.csv`.

## Power

| Scenario | True MI difference | Method | Power at 0.05 | 95% coverage |
| --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | -0.0200 | Normal Wald | 0.0768 | 0.9555 |
| curve_effect_d02_n300 | -0.0200 | Simple Welch | 0.0759 | 0.9560 |
| curve_effect_d02_n300 | -0.0200 | Expanded Welch | 0.0689 | 0.9614 |
| curve_effect_d05_n300 | -0.0500 | Normal Wald | 0.2775 | 0.9531 |
| curve_effect_d05_n300 | -0.0500 | Simple Welch | 0.2761 | 0.9536 |
| curve_effect_d05_n300 | -0.0500 | Expanded Welch | 0.2652 | 0.9578 |
| curve_effect_d10_n300 | -0.1000 | Normal Wald | 0.7449 | 0.9480 |
| curve_effect_d10_n300 | -0.1000 | Simple Welch | 0.7437 | 0.9484 |
| curve_effect_d10_n300 | -0.1000 | Expanded Welch | 0.7362 | 0.9507 |
| curve_sample_d05_n150 | -0.0500 | Normal Wald | 0.1523 | 0.9453 |
| curve_sample_d05_n150 | -0.0500 | Simple Welch | 0.1498 | 0.9466 |
| curve_sample_d05_n150 | -0.0500 | Expanded Welch | 0.1402 | 0.9557 |
| curve_sample_d05_n600 | -0.0500 | Normal Wald | 0.5161 | 0.9486 |
| curve_sample_d05_n600 | -0.0500 | Simple Welch | 0.5151 | 0.9488 |
| curve_sample_d05_n600 | -0.0500 | Expanded Welch | 0.5063 | 0.9510 |

## Runtime

| Rows | Columns | Method | Route | Median ms | Relative to Wald |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | Normal Wald | Normal Wald | 0.0850 | 1.0000 |
| 2 | 2 | Simple Welch | Simple Welch | 0.0984 | 1.1565 |
| 2 | 2 | Expanded Welch | Expanded Welch | 0.1607 | 1.8895 |
| 5 | 5 | Normal Wald | Normal Wald | 0.0846 | 1.0000 |
| 5 | 5 | Simple Welch | Simple Welch | 0.0996 | 1.1775 |
| 5 | 5 | Expanded Welch | Expanded Welch | 0.1608 | 1.8998 |
| 10 | 10 | Normal Wald | Normal Wald | 0.0856 | 1.0000 |
| 10 | 10 | Simple Welch | Simple Welch | 0.1002 | 1.1712 |
| 10 | 10 | Expanded Welch | Expanded Welch | 0.1625 | 1.8997 |
| 20 | 20 | Normal Wald | Normal Wald | 0.0925 | 1.0000 |
| 20 | 20 | Simple Welch | Simple Welch | 0.1075 | 1.1617 |
| 20 | 20 | Expanded Welch | Expanded Welch | 0.1763 | 1.9057 |

Runtime includes the complete calculation from the two count tables.
All three timings use the same implementation path. Every method
remains deterministic and scans each table a fixed number of times.

## Output map

- `population_scenarios.csv`: the fixed generating distributions and
  difficulty diagnostics.
- `scenario_results.csv`: every scenario-method result.
- `regime_summary.csv`: the presentation-level aggregate table.
- `rejection_calibration_scenarios.csv`: scenario-level rejection
  curves over 101 nominal significance levels.
- `rejection_calibration_regimes.csv`: mean curves and population
  variability bands for each regime and method.
- `null_pvalues.npz`: complete null p-value arrays for follow-up
  calibration or Q-Q plots without rerunning the simulation.
- `power_summary.csv`: alternative-hypothesis power and coverage.
- `runtime_summary.csv`: end-to-end timing by table size.
- `calibration_summary.png`: one visual comparison across regimes.
- `rejection_calibration.png` and `.pdf`: lower-tail rejection
  calibration with scenario-variability bands.
