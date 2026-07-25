# Influence-Saddlepoint Validation

Mode: `broad`.

## Calibration

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 |
| --- | --- | --- | --- | --- | --- | --- |
| wald_analytic | 144 | 0.00561 | 0.00450 | 0.96528 | 0.03500 | 0.07700 |
| influence_saddlepoint | 144 | 0.00571 | 0.00450 | 0.96528 | 0.03500 | 0.08000 |

## Frozen Decision Rule

- Relative MAE improvement: `-1.670%`
- Change in in-band proportion: `0.000%`
- New bad scenarios: `0`
- Maximum invalid rate: `0.000%`
- Stage-2 pass: `False`

## Runtime and Routes

- Mean scenario median runtime: `0.683 ms`
- Mean scenario p95 runtime: `0.778 ms`
- Mean fallback rate: `0.006%`
- Complete run wall time: `202.49 s`

This is the complete two-seed broad run. The frozen decision rule is
interpreted decisively and stops the rejected refinement branch.
