# Supervisor Experiment: Differential Mutual Information

Profile: `full`. Each null population used `10,000` independently simulated table pairs.

## Experiment in one sentence

Generate two different categorical populations with exactly equal true
mutual information, repeatedly sample one table from each, and check how
often each analytic test incorrectly rejects equality.

## Design

The null grid contains 12 table shapes and six designs, grouped into
three regimes with two population variants per regime. The full profile
therefore contains 72 population pairs. Every method sees the same table
pairs and uses the same bias-corrected MI difference and standard error.

- **Well sampled:** Equal sample sizes and high observations per cell; includes one near-balanced and one skewed-margin variant.
- **Moderate:** A 2:1 sample-size ratio and moderate observations per cell, with increasingly heterogeneous margins.
- **Sparse and imbalanced:** A 4:1 sample-size ratio, low observations per cell, and heterogeneous margins.

The methods differ only in reference calibration: normal Wald uses
a standard normal distribution, simple Welch uses ordinary `n-1`
component degrees of freedom, and expanded Welch estimates component
degrees of freedom from the MI-variance influence function.

## Main calibration results

| Regime | Method | FPR at 0.05 | Error at 0.05 | FPR at 0.01 | Error at 0.01 | 95% coverage |
| --- | --- | --- | --- | --- | --- | --- |
| Well sampled | Normal Wald | 0.04651 | 0.00369 | 0.00875 | 0.00137 | 0.95349 |
| Well sampled | Simple Welch | 0.04645 | 0.00375 | 0.00869 | 0.00143 | 0.95355 |
| Well sampled | Expanded Welch | 0.04507 | 0.00510 | 0.00809 | 0.00197 | 0.95493 |
| Moderate | Normal Wald | 0.04790 | 0.00395 | 0.00965 | 0.00158 | 0.95210 |
| Moderate | Simple Welch | 0.04769 | 0.00391 | 0.00954 | 0.00154 | 0.95231 |
| Moderate | Expanded Welch | 0.04543 | 0.00473 | 0.00841 | 0.00176 | 0.95457 |
| Sparse and imbalanced | Normal Wald | 0.05556 | 0.00589 | 0.01266 | 0.00278 | 0.94444 |
| Sparse and imbalanced | Simple Welch | 0.05504 | 0.00538 | 0.01235 | 0.00247 | 0.94496 |
| Sparse and imbalanced | Expanded Welch | 0.05306 | 0.00358 | 0.01115 | 0.00138 | 0.94694 |

False-positive-rate error is the absolute difference between observed
and nominal rejection rates, so lower is better.

## Overall summary

| Method | MAE at 0.10 | MAE at 0.05 | MAE at 0.01 | 95% coverage |
| --- | --- | --- | --- | --- |
| Normal Wald | 0.00639 | 0.00451 | 0.00191 | 0.95001 |
| Simple Welch | 0.00618 | 0.00435 | 0.00181 | 0.95027 |
| Expanded Welch | 0.00639 | 0.00447 | 0.00170 | 0.95215 |

## Direct interpretation

- In the target sparse and imbalanced regime, expanded Welch reduced
  mean calibration error relative to normal Wald by
  **39.2% at alpha 0.05** and
  **50.6% at alpha 0.01**.
- This was not a universal improvement. In well-sampled tables at
  alpha 0.05, expanded Welch increased mean absolute error from
  `0.00369`
  to `0.00510`
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
| 2 | 2 | Normal Wald | 0.0849 | 1.0000 |
| 2 | 2 | Simple Welch | 0.1002 | 1.1802 |
| 2 | 2 | Expanded Welch | 0.1614 | 1.9016 |
| 5 | 5 | Normal Wald | 0.0864 | 1.0000 |
| 5 | 5 | Simple Welch | 0.1011 | 1.1710 |
| 5 | 5 | Expanded Welch | 0.1631 | 1.8888 |
| 10 | 10 | Normal Wald | 0.0872 | 1.0000 |
| 10 | 10 | Simple Welch | 0.1015 | 1.1644 |
| 10 | 10 | Expanded Welch | 0.1643 | 1.8846 |
| 20 | 20 | Normal Wald | 0.0933 | 1.0000 |
| 20 | 20 | Simple Welch | 0.1078 | 1.1559 |
| 20 | 20 | Expanded Welch | 0.1752 | 1.8789 |

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
