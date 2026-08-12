# Supervisor Experiment: Differential Mutual Information

Profile: `smoke`. Each null population used `300` independently simulated table pairs.

## Experiment in one sentence

Generate two different categorical populations with exactly equal true
mutual information, repeatedly sample one table from each, and check how
often each analytic test incorrectly rejects equality.

## Design

The null grid contains 54 fixed
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
- **Zero MI (independence):** Both populations are independent product distributions with different margins, so I(P)=I(Q)=0 exactly; the two variants cover dense near-balanced and lower-density skewed tables.

The methods differ only in reference calibration: normal Wald uses
a standard normal distribution, simple Welch uses ordinary `n-1`
component degrees of freedom, and expanded Welch estimates component
degrees of freedom from the MI-variance influence function.

## Main calibration results

| Regime | Method | FPR at 0.05 | Error at 0.05 | FPR at 0.01 | Error at 0.01 | Valid rate | 95% coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Well sampled | Normal Wald | 0.04667 | 0.00778 | 0.00778 | 0.00556 | 1.00000 | 0.95333 |
| Well sampled | Simple Welch | 0.04611 | 0.00833 | 0.00778 | 0.00556 | 1.00000 | 0.95389 |
| Well sampled | Expanded Welch | 0.04111 | 0.00889 | 0.00611 | 0.00500 | 1.00000 | 0.95889 |
| Moderate | Normal Wald | 0.05722 | 0.01944 | 0.01056 | 0.00389 | 1.00000 | 0.94278 |
| Moderate | Simple Welch | 0.05611 | 0.01833 | 0.01056 | 0.00389 | 1.00000 | 0.94389 |
| Moderate | Expanded Welch | 0.05056 | 0.01611 | 0.00833 | 0.00278 | 1.00000 | 0.94944 |
| Sparse and imbalanced | Normal Wald | 0.06556 | 0.01556 | 0.02056 | 0.01056 | 1.00000 | 0.93444 |
| Sparse and imbalanced | Simple Welch | 0.06556 | 0.01556 | 0.02000 | 0.01000 | 1.00000 | 0.93444 |
| Sparse and imbalanced | Expanded Welch | 0.06333 | 0.01333 | 0.01611 | 0.00611 | 1.00000 | 0.93667 |
| Highly skewed and sparse | Normal Wald | 0.06000 | 0.01333 | 0.01056 | 0.00500 | 1.00000 | 0.94000 |
| Highly skewed and sparse | Simple Welch | 0.05889 | 0.01222 | 0.01056 | 0.00500 | 1.00000 | 0.94111 |
| Highly skewed and sparse | Expanded Welch | 0.05611 | 0.00944 | 0.00778 | 0.00222 | 1.00000 | 0.94389 |
| Ultra-skewed and sparse | Normal Wald | 0.06167 | 0.01167 | 0.01667 | 0.00667 | 1.00000 | 0.93833 |
| Ultra-skewed and sparse | Simple Welch | 0.06111 | 0.01111 | 0.01667 | 0.00667 | 1.00000 | 0.93889 |
| Ultra-skewed and sparse | Expanded Welch | 0.05833 | 0.00833 | 0.01667 | 0.00667 | 1.00000 | 0.94167 |
| Widespread sparsity | Normal Wald | 0.05064 | 0.01175 | 0.00834 | 0.00611 | 0.99833 | 0.94936 |
| Widespread sparsity | Simple Welch | 0.05009 | 0.01120 | 0.00722 | 0.00722 | 0.99833 | 0.94991 |
| Widespread sparsity | Expanded Welch | 0.02376 | 0.02624 | 0.00278 | 0.00722 | 0.97056 | 0.97624 |
| Equal-MI shape mismatch | Normal Wald | 0.03778 | 0.01667 | 0.00833 | 0.00389 | 1.00000 | 0.96222 |
| Equal-MI shape mismatch | Simple Welch | 0.03722 | 0.01722 | 0.00833 | 0.00389 | 1.00000 | 0.96278 |
| Equal-MI shape mismatch | Expanded Welch | 0.03667 | 0.01778 | 0.00611 | 0.00611 | 1.00000 | 0.96333 |
| Extreme sample imbalance | Normal Wald | 0.06444 | 0.01667 | 0.01944 | 0.01056 | 1.00000 | 0.93556 |
| Extreme sample imbalance | Simple Welch | 0.06222 | 0.01444 | 0.01833 | 0.00944 | 1.00000 | 0.93778 |
| Extreme sample imbalance | Expanded Welch | 0.04667 | 0.00667 | 0.00944 | 0.00389 | 1.00000 | 0.95333 |
| Zero MI (independence) | Normal Wald | 0.02944 | 0.03722 | 0.01333 | 0.01333 | 1.00000 | 0.97056 |
| Zero MI (independence) | Simple Welch | 0.02833 | 0.03722 | 0.01278 | 0.01389 | 1.00000 | 0.97167 |
| Zero MI (independence) | Expanded Welch | 0.00111 | 0.04889 | 0.00056 | 0.00944 | 1.00000 | 0.99889 |

False-positive-rate error is the absolute difference between observed
and nominal rejection rates among valid calculations, so lower is
better. Validity is reported separately so undefined calculations
are not hidden by conditioning only on successful results.

## Overall summary

| Method | MAE at 0.10 | MAE at 0.05 | MAE at 0.01 | Mean valid rate | 95% coverage |
| --- | --- | --- | --- | --- | --- |
| Normal Wald | 0.02144 | 0.01668 | 0.00728 | 0.99981 | 0.94740 |
| Simple Welch | 0.02125 | 0.01618 | 0.00728 | 0.99981 | 0.94826 |
| Expanded Welch | 0.02522 | 0.01730 | 0.00549 | 0.99673 | 0.95804 |

## Direct interpretation

- Relative calibration changes in the difficult regimes are
  reported directly below; positive percentages mean that expanded
  Welch reduced error relative to normal Wald.
- **Sparse and imbalanced:** 14.3% at alpha 0.05 and 42.1% at alpha 0.01.
- **Highly skewed and sparse:** 29.2% at alpha 0.05 and 55.6% at alpha 0.01.
- **Ultra-skewed and sparse:** 28.6% at alpha 0.05 and 0.0% at alpha 0.01.
- **Widespread sparsity:** -123.3% at alpha 0.05 and -18.3% at alpha 0.01.
- **Equal-MI shape mismatch:** -6.7% at alpha 0.05 and -57.1% at alpha 0.01.
- **Extreme sample imbalance:** 60.0% at alpha 0.05 and 63.2% at alpha 0.01.
- This was not a universal improvement. In well-sampled tables at
  alpha 0.05, expanded Welch increased mean absolute error from
  `0.00778`
  to `0.00889`
  by becoming mildly conservative.
- Zero MI is a nonregular boundary: the population first-order MI
  variance is zero, so the normal and Welch reference arguments do
  not apply in their regular form. The boundary results are reported
  as a diagnostic rather than pooled evidence for those arguments.
- In the zero-MI regime at alpha 0.05, the mean FPRs were
  `0.02944` for normal Wald,
  `0.02833` for simple Welch,
  and `0.00111` for expanded Welch.
- Across the five power scenarios, expanded Welch lost
  `0.0108` power on average and at most
  `0.0200` relative to normal Wald.
- The simple Welch correction changed both calibration and power only
  slightly, consistent with its usually large effective degrees of freedom.
- Scenario-level Wilson intervals, sparsity diagnostics, validity rates,
  and effective degrees of freedom are retained in `scenario_results.csv`.

## Power

| Scenario | True MI difference | Method | Power at 0.05 | 95% coverage |
| --- | --- | --- | --- | --- |
| curve_effect_d02_n300 | -0.0200 | Normal Wald | 0.0700 | 0.9580 |
| curve_effect_d02_n300 | -0.0200 | Simple Welch | 0.0680 | 0.9580 |
| curve_effect_d02_n300 | -0.0200 | Expanded Welch | 0.0620 | 0.9700 |
| curve_effect_d05_n300 | -0.0500 | Normal Wald | 0.3240 | 0.9480 |
| curve_effect_d05_n300 | -0.0500 | Simple Welch | 0.3200 | 0.9480 |
| curve_effect_d05_n300 | -0.0500 | Expanded Welch | 0.3040 | 0.9500 |
| curve_effect_d10_n300 | -0.1000 | Normal Wald | 0.7200 | 0.9240 |
| curve_effect_d10_n300 | -0.1000 | Simple Welch | 0.7200 | 0.9240 |
| curve_effect_d10_n300 | -0.1000 | Expanded Welch | 0.7140 | 0.9300 |
| curve_sample_d05_n150 | -0.0500 | Normal Wald | 0.1620 | 0.9540 |
| curve_sample_d05_n150 | -0.0500 | Simple Welch | 0.1620 | 0.9560 |
| curve_sample_d05_n150 | -0.0500 | Expanded Welch | 0.1480 | 0.9720 |
| curve_sample_d05_n600 | -0.0500 | Normal Wald | 0.5160 | 0.9360 |
| curve_sample_d05_n600 | -0.0500 | Simple Welch | 0.5140 | 0.9360 |
| curve_sample_d05_n600 | -0.0500 | Expanded Welch | 0.5100 | 0.9380 |

## Runtime

| Rows | Columns | Method | Route | Median ms | Relative to Wald |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | Normal Wald | Normal Wald | 0.0870 | 1.0000 |
| 2 | 2 | Simple Welch | Simple Welch | 0.1022 | 1.1745 |
| 2 | 2 | Expanded Welch | Expanded Welch | 0.1657 | 1.9038 |

Runtime includes the complete calculation from the two count tables.
All three timings use the same implementation path. Every method
remains deterministic and scans each table a fixed number of times.

## Output map

- `population_scenarios.csv`: the fixed generating distributions and
  difficulty diagnostics.
- `scenario_results.csv`: every scenario-method result.
- `regime_summary.csv`: the presentation-level aggregate table.
- `power_summary.csv`: alternative-hypothesis power and coverage.
- `runtime_summary.csv`: end-to-end timing by table size.
- `calibration_summary.png`: one visual comparison across regimes.
