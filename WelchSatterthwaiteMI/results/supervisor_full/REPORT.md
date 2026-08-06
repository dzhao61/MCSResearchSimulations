# Supervisor Experiment: Differential Mutual Information

Profile: `full`. Each null population used `10,000` independently simulated table pairs.

## Experiment in one sentence

Generate two different categorical populations with exactly equal true
mutual information, repeatedly sample one table from each, and check how
often each analytic test incorrectly rejects equality.

## Design

The null grid contains 216 fixed
population pairs across 9 regimes. Every method sees
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
- **Support instability:** At least one complete row or column in each population has a true expected total below 1 and is frequently absent in samples.

The methods differ only in reference calibration: normal Wald uses
a standard normal distribution, simple Welch uses ordinary `n-1`
component degrees of freedom, and expanded Welch estimates component
degrees of freedom from the MI-variance influence function.

## Main calibration results

| Regime | Method | FPR at 0.05 | Error at 0.05 | FPR at 0.01 | Error at 0.01 | Valid rate | 95% coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Well sampled | Normal Wald | 0.04740 | 0.00326 | 0.00879 | 0.00148 | 1.00000 | 0.95260 |
| Well sampled | Simple Welch | 0.04733 | 0.00333 | 0.00876 | 0.00151 | 1.00000 | 0.95267 |
| Well sampled | Expanded Welch | 0.04582 | 0.00466 | 0.00814 | 0.00199 | 1.00000 | 0.95418 |
| Moderate | Normal Wald | 0.04826 | 0.00370 | 0.00979 | 0.00153 | 1.00000 | 0.95174 |
| Moderate | Simple Welch | 0.04804 | 0.00365 | 0.00970 | 0.00155 | 1.00000 | 0.95196 |
| Moderate | Expanded Welch | 0.04593 | 0.00419 | 0.00850 | 0.00172 | 1.00000 | 0.95407 |
| Sparse and imbalanced | Normal Wald | 0.05576 | 0.00615 | 0.01261 | 0.00286 | 1.00000 | 0.94424 |
| Sparse and imbalanced | Simple Welch | 0.05526 | 0.00565 | 0.01227 | 0.00252 | 1.00000 | 0.94474 |
| Sparse and imbalanced | Expanded Welch | 0.05332 | 0.00395 | 0.01105 | 0.00145 | 1.00000 | 0.94668 |
| Highly skewed and sparse | Normal Wald | 0.05085 | 0.00275 | 0.01063 | 0.00162 | 1.00000 | 0.94915 |
| Highly skewed and sparse | Simple Welch | 0.05069 | 0.00262 | 0.01057 | 0.00156 | 1.00000 | 0.94931 |
| Highly skewed and sparse | Expanded Welch | 0.05023 | 0.00217 | 0.01025 | 0.00124 | 1.00000 | 0.94977 |
| Ultra-skewed and sparse | Normal Wald | 0.05233 | 0.00312 | 0.01081 | 0.00133 | 1.00000 | 0.94767 |
| Ultra-skewed and sparse | Simple Welch | 0.05215 | 0.00296 | 0.01071 | 0.00125 | 1.00000 | 0.94785 |
| Ultra-skewed and sparse | Expanded Welch | 0.05150 | 0.00248 | 0.01040 | 0.00098 | 1.00000 | 0.94850 |
| Widespread sparsity | Normal Wald | 0.05263 | 0.01064 | 0.01110 | 0.00500 | 0.99980 | 0.94737 |
| Widespread sparsity | Simple Welch | 0.05192 | 0.01076 | 0.01068 | 0.00504 | 0.99980 | 0.94808 |
| Widespread sparsity | Expanded Welch | 0.03913 | 0.01439 | 0.00586 | 0.00463 | 0.99143 | 0.96087 |
| Equal-MI shape mismatch | Normal Wald | 0.05305 | 0.00420 | 0.01112 | 0.00153 | 1.00000 | 0.94695 |
| Equal-MI shape mismatch | Simple Welch | 0.05285 | 0.00424 | 0.01103 | 0.00149 | 1.00000 | 0.94715 |
| Equal-MI shape mismatch | Expanded Welch | 0.05153 | 0.00443 | 0.01043 | 0.00158 | 1.00000 | 0.94847 |
| Extreme sample imbalance | Normal Wald | 0.05616 | 0.00876 | 0.01428 | 0.00497 | 1.00000 | 0.94384 |
| Extreme sample imbalance | Simple Welch | 0.05533 | 0.00801 | 0.01382 | 0.00452 | 1.00000 | 0.94467 |
| Extreme sample imbalance | Expanded Welch | 0.05110 | 0.00582 | 0.01052 | 0.00205 | 1.00000 | 0.94890 |
| Support instability | Normal Wald | 0.03881 | 0.01465 | 0.00677 | 0.00415 | 0.97569 | 0.96119 |
| Support instability | Simple Welch | 0.03738 | 0.01606 | 0.00646 | 0.00445 | 0.97569 | 0.96262 |
| Support instability | Expanded Welch | 0.03161 | 0.02074 | 0.00505 | 0.00544 | 0.90405 | 0.96839 |

False-positive-rate error is the absolute difference between observed
and nominal rejection rates among valid calculations, so lower is
better. Validity is reported separately and is part of method
performance in the support-instability boundary regime.

## Overall summary

| Method | MAE at 0.10 | MAE at 0.05 | MAE at 0.01 | Mean valid rate | 95% coverage |
| --- | --- | --- | --- | --- | --- |
| Normal Wald | 0.00902 | 0.00636 | 0.00272 | 0.99728 | 0.94942 |
| Simple Welch | 0.00895 | 0.00636 | 0.00265 | 0.99728 | 0.94989 |
| Expanded Welch | 0.01062 | 0.00698 | 0.00234 | 0.98839 | 0.95331 |

## Direct interpretation

- Relative calibration changes in the difficult regimes are
  reported directly below; positive percentages mean that expanded
  Welch reduced error relative to normal Wald.
- **Sparse and imbalanced:** 35.8% at alpha 0.05 and 49.2% at alpha 0.01.
- **Highly skewed and sparse:** 21.2% at alpha 0.05 and 23.6% at alpha 0.01.
- **Ultra-skewed and sparse:** 20.5% at alpha 0.05 and 26.2% at alpha 0.01.
- **Widespread sparsity:** -35.3% at alpha 0.05 and 7.3% at alpha 0.01.
- **Equal-MI shape mismatch:** -5.6% at alpha 0.05 and -3.6% at alpha 0.01.
- **Extreme sample imbalance:** 33.6% at alpha 0.05 and 58.7% at alpha 0.01.
- **Support instability:** -41.5% at alpha 0.05 and -31.1% at alpha 0.01.
- This was not a universal improvement. In well-sampled tables at
  alpha 0.05, expanded Welch increased mean absolute error from
  `0.00326`
  to `0.00466`
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

| Rows | Columns | Method | Median ms | Relative to Wald |
| --- | --- | --- | --- | --- |
| 2 | 2 | Normal Wald | 0.0855 | 1.0000 |
| 2 | 2 | Simple Welch | 0.1005 | 1.1756 |
| 2 | 2 | Expanded Welch | 0.1626 | 1.9016 |
| 5 | 5 | Normal Wald | 0.0851 | 1.0000 |
| 5 | 5 | Simple Welch | 0.0998 | 1.1734 |
| 5 | 5 | Expanded Welch | 0.1614 | 1.8974 |
| 10 | 10 | Normal Wald | 0.0862 | 1.0000 |
| 10 | 10 | Simple Welch | 0.1008 | 1.1692 |
| 10 | 10 | Expanded Welch | 0.1630 | 1.8922 |
| 20 | 20 | Normal Wald | 0.0931 | 1.0000 |
| 20 | 20 | Simple Welch | 0.1080 | 1.1597 |
| 20 | 20 | Expanded Welch | 0.1756 | 1.8859 |

Runtime includes the complete calculation from the two count tables.
All three timings use the same implementation path. The expanded method
remains deterministic and scans each table a fixed number of times.

## Output map

- `population_scenarios.csv`: the fixed generating distributions and
  difficulty diagnostics.
- `scenario_results.csv`: every scenario-method result.
- `regime_summary.csv`: the presentation-level aggregate table.
- `power_summary.csv`: alternative-hypothesis power and coverage.
- `runtime_summary.csv`: end-to-end timing by table size.
- `calibration_summary.png`: one visual comparison across regimes.
