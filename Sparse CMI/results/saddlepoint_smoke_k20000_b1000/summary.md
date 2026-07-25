# Deterministic Sparse-CMI Saddlepoint Validation

Profile `smoke` evaluated 29 configurations. The development/held-out split is a stable hash of the configuration name and is independent of method performance.

## Held-out calibration

Mean absolute rejection-rate error versus the conditional reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Raw saddlepoint | Deterministic router | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.01314 | 0.01192 | 0.01230 | 0.01175 | 0.01175 | 0.29112 | 0.21603 |
| 0.05 | 0.02403 | 0.01393 | 0.01522 | 0.01519 | 0.00240 | 0.16375 | 0.18001 |
| 0.01 | 0.01113 | 0.00298 | 0.00142 | 0.00144 | 0.00052 | 0.10503 | 0.11239 |
| 0.001 | 0.00510 | 0.00119 | 0.00006 | 0.00021 | 0.00013 | 0.03797 | 0.03858 |

## Route coverage

Exact convolution handled 5/11 held-out configurations; the remainder used saddlepoint.
Median held-out speedup versus 1,000 literal within-stratum permutations was 5.5x.

## Saddlepoint-only held-out cases at alpha=0.05

| Method | Mean FPR error | Maximum FPR error |
|---|---:|---:|
| edgeworth | 0.00208 | 0.00670 |
| cornish_fisher | 0.00446 | 0.02220 |
| saddlepoint | 0.00440 | 0.02220 |
| chi2_nominal | 0.26331 | 0.84275 |

## Guardrails

- Numerical failures: 0 during critical-value searches and 0 across p-value diagnostic quantiles.
- Raw saddlepoint and routed results are reported separately. Exact routing cannot be used to conceal saddlepoint failures.
- The current exact rule (`informative_strata <= 10` and at most 100,000 convolved states) was declared before this benchmark.
- Monte Carlo reference rows have finite resolution; alpha 0.001 remains exploratory unless exact convolution is available.
