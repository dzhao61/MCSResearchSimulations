# Sparse CMI First-Stage Falsification Summary

**Decision: `PROCEED`**

Profile `full` evaluated 103 configurations with 100,000 conditional-null draws per configuration and 1,000 literal label permutations for runtime.

## Decision criteria

| Criterion | Pass | Evidence |
|---|---:|---:|
| Exact-moment normal beats informative-df chi-square in sparse cases | True | FPR: 77.3%; p-value: 90.9% |
| Edgeworth broadly improves on exact-moment normal | True | upper-tail p-value: 98.9%; tail FPR non-worse: 99.6% |
| Observable diagnostics predict normal tail error | True | best absolute Spearman rho: 0.678 |
| Exact-moment calculation is at least 10x faster than permutation | True | median speedup: 36.4x |

## Calibration

Mean absolute rejection-rate error relative to the attainable exact/Monte Carlo conditional reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.02536 | 0.01455 | 0.01710 | 0.26931 | 0.28541 |
| 0.05 | 0.02268 | 0.01422 | 0.01397 | 0.21349 | 0.23344 |
| 0.01 | 0.01118 | 0.00306 | 0.00208 | 0.12462 | 0.13157 |
| 0.001 | 0.00517 | 0.00126 | 0.00010 | 0.06860 | 0.06186 |

## Reliability diagnostics

| Diagnostic | Spearman rho with normal upper-tail p-value error |
|---|---:|
| lyapunov_ratio | 0.617 |
| max_variance_share | 0.678 |
| skewness | 0.552 |
| informative_strata | -0.445 |

## Reference coverage

- `exact_convolution`: 53 configurations
- `conditional_monte_carlo`: 50 configurations

## Interpretation guardrails

- `PROCEED` is only an empirical first-stage result. Novelty and the conditional Berry-Esseen theorem remain separate gates.
- `NARROW_OR_REVISE` means exact centring/scaling may be useful but the proposed first-order skewness correction is not yet reliable enough to defend.
- Exact conditional p-values are discrete and conservative. Approximation errors are therefore reported against both their attainable reference size and nominal alpha in the CSV.
- Edgeworth is judged on upper-tail accuracy at alpha <= 0.05. Its whole-distribution p-value MAE is still recorded because a tail improvement can coexist with poorer central p-values.
- Conditional Monte Carlo configurations should be rerun with more draws before publication, especially at alpha=0.001.
