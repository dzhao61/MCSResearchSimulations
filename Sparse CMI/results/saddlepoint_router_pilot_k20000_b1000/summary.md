# Deterministic Sparse-CMI Saddlepoint Validation

Profile `smoke` evaluated 29 configurations. The development/held-out split is a stable hash of the configuration name and is independent of method performance.

## Held-out calibration

Mean absolute rejection-rate error versus the conditional reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Raw saddlepoint | Deterministic router | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.01291 | 0.01169 | 0.01207 | 0.01153 | 0.00070 | 0.29197 | 0.21687 |
| 0.05 | 0.02397 | 0.01393 | 0.01523 | 0.01520 | 0.00038 | 0.16479 | 0.18105 |
| 0.01 | 0.01103 | 0.00304 | 0.00147 | 0.00148 | 0.00004 | 0.10365 | 0.11101 |
| 0.001 | 0.00512 | 0.00120 | 0.00006 | 0.00022 | 0.00007 | 0.03746 | 0.03807 |

## Route coverage

Exact convolution handled 8/11 held-out configurations; the remainder used saddlepoint.
Median held-out speedup versus 1,000 literal within-stratum permutations was 30.7x.

## Saddlepoint-only held-out cases at alpha=0.05

| Method | Mean FPR error | Maximum FPR error |
|---|---:|---:|
| edgeworth | 0.00417 | 0.00670 |
| cornish_fisher | 0.00152 | 0.00275 |
| saddlepoint | 0.00140 | 0.00180 |
| chi2_nominal | 0.29778 | 0.84275 |

## Guardrails

- Numerical failures: 0 during critical-value searches and 0 across p-value diagnostic quantiles.
- Raw saddlepoint and routed results are reported separately. Exact routing cannot be used to conceal saddlepoint failures.
- Exact routing requires guaranteed upper bounds of at most 100,000 states and 100,000 transitions.
- Monte Carlo reference rows have finite resolution; alpha 0.001 remains exploratory unless exact convolution is available.
