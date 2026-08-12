# Joint-Influence Experiment

This experiment reuses the 16 fixed configurations, ten population realizations per configuration, and the requested null replicate count. No configuration-specific tuning is used.

## Overall calibration

| method_label | mean_valid_rate | configuration_mae_10 | configuration_mae_05 | configuration_mae_01 |
| --- | --- | --- | --- | --- |
| Normal Wald | 0.999991 | 0.042101 | 0.036222 | 0.023848 |
| Simple Welch | 0.999991 | 0.040984 | 0.034969 | 0.022775 |
| Expanded Welch | 0.996334 | 0.031611 | 0.025355 | 0.014218 |
| Joint Edgeworth | 0.979763 | 0.029399 | 0.022494 | 0.010462 |
| Joint-Influence Welch | 0.988657 | 0.026548 | 0.018703 | 0.010414 |

The lowest alpha=0.05 configuration MAE was produced by **Joint-Influence Welch** (0.018703).
Joint-Influence Welch changed MAE from 0.025355 for Expanded Welch and 0.036222 for Normal Wald to 0.018703.

## Equal-sample configurations

| method_label | alpha_05_mae |
| --- | --- |
| Simple Welch | 0.008067 |
| Expanded Welch | 0.008183 |
| Normal Wald | 0.008792 |
| Joint-Influence Welch | 0.011509 |
| Joint Edgeworth | 0.013889 |

The Edgeworth methods report invalid results when their approximate CDF leaves [0,1]; these replicates are not silently clipped or routed to another method.
