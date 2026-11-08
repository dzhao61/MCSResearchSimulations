# Influence-Saddlepoint Validation

Mode: `smoke`.

## Calibration

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 |
| --- | --- | --- | --- | --- | --- | --- |
| wald_analytic | 6 | 0.01000 | 0.00500 | 0.66667 | 0.02000 | 0.07000 |
| influence_saddlepoint | 6 | 0.01000 | 0.00500 | 0.66667 | 0.02000 | 0.07000 |

## Frozen Decision Rule

- Relative MAE improvement: `0.000%`
- Change in in-band proportion: `0.000%`
- New bad scenarios: `0`
- Maximum invalid rate: `0.000%`
- Stage-2 pass: `False`

## Runtime and Routes

- Mean scenario median runtime: `0.662 ms`
- Mean scenario p95 runtime: `0.764 ms`
- Mean fallback rate: `0.000%`
- Complete run wall time: `0.65 s`

The smoke run is an implementation check only. The pass/fail rule is
interpreted decisively only for the complete two-seed broad run.
