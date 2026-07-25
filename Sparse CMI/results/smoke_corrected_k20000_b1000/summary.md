# Sparse CMI First-Stage Falsification Summary

**Decision: `NARROW_OR_REVISE`**

Profile `smoke` evaluated 29 configurations with 20,000 conditional-null draws per configuration and 1,000 literal label permutations for runtime.

## Decision criteria

| Criterion | Pass | Evidence |
|---|---:|---:|
| Exact-moment normal beats informative-df chi-square in sparse cases | True | FPR: 73.9%; p-value: 91.3% |
| Edgeworth broadly improves on exact-moment normal | False | FPR: 52.2%; p-value: 17.4% |
| Observable diagnostics predict normal tail error | True | best absolute Spearman rho: 0.828 |
| Exact-moment calculation is at least 10x faster than permutation | True | median speedup: 33.2x |

## Calibration

Mean absolute rejection-rate error relative to the attainable exact/Monte Carlo conditional reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.01438 | 0.01463 | 0.01446 | 0.27975 | 0.26405 |
| 0.05 | 0.02198 | 0.01324 | 0.01399 | 0.20245 | 0.22026 |
| 0.01 | 0.01077 | 0.00246 | 0.00167 | 0.14093 | 0.13264 |
| 0.001 | 0.00451 | 0.00112 | 0.00007 | 0.09287 | 0.06378 |

## Reliability diagnostics

| Diagnostic | Spearman rho with normal upper-tail p-value error |
|---|---:|
| lyapunov_ratio | 0.729 |
| max_variance_share | 0.828 |
| skewness | 0.678 |
| informative_strata | -0.300 |

## Reference coverage

- `conditional_monte_carlo`: 15 configurations
- `exact_convolution`: 14 configurations

## Interpretation guardrails

- `PROCEED` is only an empirical first-stage result. Novelty and the conditional Berry-Esseen theorem remain separate gates.
- `NARROW_OR_REVISE` means exact centring/scaling may be useful but the proposed first-order skewness correction is not yet reliable enough to defend.
- Exact conditional p-values are discrete and conservative. Approximation errors are therefore reported against both their attainable reference size and nominal alpha in the CSV.
- Conditional Monte Carlo configurations should be rerun with more draws before publication, especially at alpha=0.001.
