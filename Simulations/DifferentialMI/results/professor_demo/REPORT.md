# Professor Demo Verification

## Tests and Units

- Unit tests: `21/21 passed`
- Maximum JIDT/manual MI error: `6.106e-16` nats
- JIDT analytic matches its bit-scaled convention: `True`
- JIDT analytic matches standard nats chi-square: `False`

## Broad Calibration

| method | mean_absolute_fpr_error_05 | within_035_065 | maximum_fpr_05 | mean_coverage_95 |
| --- | --- | --- | --- | --- |
| wald_plugin | 0.07116 | 0.61111 | 0.96700 | 0.88154 |
| wald_analytic | 0.00513 | 0.95833 | 0.07333 | 0.94986 |
| wald_jackknife | 0.00610 | 0.90972 | 0.08033 | 0.94875 |

## Saddlepoint Decision

| method | mean_absolute_fpr_error_05 | within_035_065 | maximum_fpr_05 |
| --- | --- | --- | --- |
| wald_analytic | 0.00561 | 0.96528 | 0.07700 |
| influence_saddlepoint | 0.00571 | 0.96528 | 0.08000 |

The influence-saddlepoint refinement failed its pre-specified
improvement rule and was not retained.

## Runtime

- Mean 999-permutation advantage over the original full deterministic estimator set: `40.8x`

## UCI Adult Case

- Corrected difference: `-0.037135` nats
- 95% CI: `[-0.043082, -0.031189]`
- Wald p-value: `1.890e-34`
- Studentized permutation p-value: `0.0001`
- Wald runtime: `0.224 ms`
- 9999 permutation runtime: `0.050 s`
