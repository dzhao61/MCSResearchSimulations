# Deterministic Sparse-CMI Saddlepoint Validation

Profile `full` evaluated 103 configurations. The development/held-out split is a stable hash of the configuration name and is independent of method performance.

## Held-out calibration

Mean absolute rejection-rate error versus the conditional reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Raw saddlepoint | Deterministic router | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.02114 | 0.01419 | 0.01386 | 0.01266 | 0.00028 | 0.31807 | 0.28179 |
| 0.05 | 0.02054 | 0.01407 | 0.01455 | 0.01535 | 0.00030 | 0.24727 | 0.23638 |
| 0.01 | 0.01055 | 0.00371 | 0.00292 | 0.00299 | 0.00004 | 0.14710 | 0.15276 |
| 0.001 | 0.00485 | 0.00133 | 0.00011 | 0.00033 | 0.00002 | 0.06978 | 0.07034 |

## Post-pilot confirmation set

These 74 configurations were absent from the smoke grid used to correct the router. Mean absolute rejection-rate error:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Raw saddlepoint | Deterministic router | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.02953 | 0.01447 | 0.01827 | 0.01799 | 0.00035 | 0.26479 | 0.29332 |
| 0.05 | 0.02296 | 0.01473 | 0.01403 | 0.01444 | 0.00011 | 0.21728 | 0.23825 |
| 0.01 | 0.01139 | 0.00335 | 0.00231 | 0.00305 | 0.00010 | 0.11835 | 0.13118 |
| 0.001 | 0.00542 | 0.00134 | 0.00011 | 0.00036 | 0.00002 | 0.05909 | 0.06116 |

## Route coverage

Exact convolution handled 29/37 held-out configurations; the remainder used saddlepoint.
Median held-out speedup versus 1,000 literal within-stratum permutations was 59.9x.

## Saddlepoint-only held-out cases at alpha=0.05

| Method | Mean FPR error | Maximum FPR error |
|---|---:|---:|
| edgeworth | 0.00136 | 0.00357 |
| cornish_fisher | 0.00080 | 0.00298 |
| saddlepoint | 0.00140 | 0.00605 |
| chi2_nominal | 0.35817 | 0.92222 |

## Guardrails

- Numerical failures: 0 during critical-value searches and 0 across p-value diagnostic quantiles.
- Raw saddlepoint and routed results are reported separately. Exact routing cannot be used to conceal saddlepoint failures.
- Exact routing requires guaranteed upper bounds of at most 100,000 states and 100,000 transitions.
- Monte Carlo reference rows have finite resolution; alpha 0.001 remains exploratory unless exact convolution is available.
