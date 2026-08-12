# Joint-Influence Experiment

This experiment reuses the 16 fixed configurations, ten population realizations per configuration, and the requested null replicate count. No configuration-specific tuning is used.

## Overall calibration

| method_label | mean_valid_rate | configuration_mae_10 | configuration_mae_05 | configuration_mae_01 |
| --- | --- | --- | --- | --- |
| Normal Wald | 0.999896 | 0.048874 | 0.041887 | 0.026566 |
| Simple Welch | 0.000000 | nan | nan | nan |
| Expanded Welch | 0.995521 | 0.037957 | 0.029909 | 0.015044 |
| Joint Edgeworth | 0.980104 | 0.031494 | 0.022608 | 0.009214 |
| Joint-Influence Welch | 0.987292 | 0.029113 | 0.018705 | 0.008524 |

The lowest alpha=0.05 configuration MAE was produced by **Joint-Influence Welch** (0.018705).
Joint-Influence Welch changed MAE from 0.029909 for Expanded Welch and 0.041887 for Normal Wald to 0.018705.

## Equal-sample configurations

| method_label | alpha_05_mae |
| --- | --- |
| Joint-Influence Welch | 0.012596 |
| Expanded Welch | 0.014549 |
| Joint Edgeworth | 0.014574 |
| Normal Wald | 0.015572 |
| Simple Welch | nan |

The Edgeworth methods report invalid results when their approximate CDF leaves [0,1]; these replicates are not silently clipped or routed to another method.
