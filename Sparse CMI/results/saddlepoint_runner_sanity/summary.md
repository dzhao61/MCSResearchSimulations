# Deterministic Sparse-CMI Saddlepoint Validation

Profile `smoke` evaluated 5 configurations. The development/held-out split is a stable hash of the configuration name and is independent of method performance.

## Held-out calibration

Mean absolute rejection-rate error versus the conditional reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Raw saddlepoint | Deterministic router | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| 0.05 | 0.03645 | 0.03645 | 0.03645 | 0.03645 | 0.00000 | 0.06105 | 0.06105 |
| 0.01 | 0.01882 | 0.00787 | 0.00015 | 0.00015 | 0.00000 | 0.01882 | 0.01882 |
| 0.001 | 0.01552 | 0.00344 | 0.00000 | 0.00000 | 0.00000 | 0.00344 | 0.00344 |

## Route coverage

Exact convolution handled 2/2 held-out configurations; the remainder used saddlepoint.
Median held-out speedup versus 20 literal within-stratum permutations was 1.7x.

## Saddlepoint-only held-out cases at alpha=0.05

| Method | Mean FPR error | Maximum FPR error |
|---|---:|---:|
| edgeworth | nan | nan |
| cornish_fisher | nan | nan |
| saddlepoint | nan | nan |
| chi2_nominal | nan | nan |

## Guardrails

- Raw saddlepoint and routed results are reported separately. Exact routing cannot be used to conceal saddlepoint failures.
- The current exact rule (`informative_strata <= 10` and at most 100,000 convolved states) was declared before this benchmark.
- Monte Carlo reference rows have finite resolution; alpha 0.001 remains exploratory unless exact convolution is available.
