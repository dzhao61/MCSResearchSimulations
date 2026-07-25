# Initial Go/No-Go Assessment

## Recommendation

**Proceed with a narrower, routed sparse-CMI project, subject to a high-risk
novelty gate.**

The exact conditional construction is valid, and the first empirical results
are strong enough to justify the next research stage. The evidence does not
support presenting the Edgeworth or normal approximation as universally
reliable. Low-information and coarse-support tables need an exact,
saddlepoint, or conditional-Monte-Carlo fallback.

## What was validated

For binary `X` and `Y`, conditioning on every observed `(n_z, r_z, s_z)` gives

```text
A_z ~ Hypergeometric(n_z, s_z, r_z).
```

Each stratum's likelihood-ratio contribution is a deterministic function of
`A_z`. Conditional stratum distributions are independent, so their cumulants
add. The implementation calculates exact stratum mean, variance, third and
fourth cumulants, absolute third central moments, and observable CLT
diagnostics.

The 18-test suite checks:

- exact hypergeometric probabilities against combinatorial probabilities;
- `G^2 = 2N * CMI_nats`, including the maximal binary case;
- exact moments against direct finite-support sums;
- aggregate moments against brute-force convolution;
- exhaustive label-permutation/hypergeometric equivalence;
- swapping and relabelling invariance;
- degenerate and positive-constant null distributions;
- finite bounded approximation p-values and per-table broadcasting.

## Fixed-margin falsification grid

The full run evaluated 103 predeclared configurations with 100,000 conditional
null draws per configuration. Numerical exact convolution was available for
53 configurations; 50 used conditional Monte Carlo.

Mean absolute rejection-rate error relative to the attainable conditional
reference:

| Alpha | Normal | Edgeworth | Cornish-Fisher | Chi2 nominal | Chi2 informative |
|---:|---:|---:|---:|---:|---:|
| 0.10 | 0.02536 | 0.01455 | 0.01710 | 0.26931 | 0.28541 |
| 0.05 | 0.02268 | 0.01422 | 0.01397 | 0.21349 | 0.23344 |
| 0.01 | 0.01118 | 0.00306 | 0.00208 | 0.12462 | 0.13157 |
| 0.001 | 0.00517 | 0.00126 | 0.00010 | 0.06860 | 0.06186 |

In sparse configurations, normal had lower FPR error than informative-df
chi-square in 77.3% of cases and lower p-value MAE in 90.9%. Edgeworth reduced
upper-tail p-value error in 98.9% and was non-worse in tail FPR error in 99.6%.

Median runtimes were approximately:

```text
exact moments and approximation: 0.000814 s
1,000 literal within-stratum permutations: 0.029101 s
speedup: 36.4x
```

## Unconditional repeated-sampling screen

The second run generated 160,000 independent null datasets across 32
data-generating regimes. Stratum counts and/or the observed `X-Z` and `Y-Z`
margins were regenerated on every replicate.

Mean absolute size distortion at alpha 0.05:

| Method | Error |
|---|---:|
| Normal | 0.01783 |
| Edgeworth | 0.00391 |
| Cornish-Fisher | 0.00309 |
| Chi2 nominal | 0.07448 |
| Chi2 informative | 0.20073 |
| Conditional Monte Carlo anchors | 0.02000 |

The conditional Monte Carlo value is based on only 100 anchor tables per
configuration, so its FPR estimate is much noisier. On those anchors, mean
absolute p-value differences were:

| Method | MAE vs conditional Monte Carlo |
|---|---:|
| Normal | 0.04653 |
| Edgeworth | 0.04319 |
| Chi2 nominal | 0.24885 |
| Chi2 informative | 0.27092 |

Edgeworth and normal were closer to the conditional Monte Carlo p-value than
nominal chi-square in 93.75% of data-generating configurations.

## Important failures

The approximation is weakest when:

- only 2-10 strata have positive conditional variance;
- one stratum contributes a large share of total variance;
- the exact support is coarse near the requested critical value;
- aggregate Lyapunov ratio or skewness remains large.

At alpha 0.05, some exact fixed-margin cases had approximation error between
0.05 and 0.08. In several of those tiny/coarse cases chi-square happened to
match the attainable exact rejection probability better. This prevents a
universal replacement claim.

The proposed diagnostics are useful: maximum variance share had Spearman
correlation 0.678 with normal upper-tail error, and Lyapunov ratio had
correlation 0.617. These are predictors, not yet validated certificates.

## JIDT baseline caveat

JIDT's default discrete conditional-MI significance method globally shuffles
variable 1. It does not preserve the observed `X-Z` margin and therefore does
not implement the general within-stratum conditional null when `P(X | Z)`
varies. See `JIDT_CMI_BASELINE_AUDIT.md`.

The correct primary baseline is within-stratum permutation or the equivalent
product-hypergeometric table sampler. JIDT can be tested later using explicit
blockwise permutation orderings.

## What remains unproven

- No conditional CLT or Berry-Esseen theorem has yet been written formally.
- No held-out router threshold has been selected.
- Power under conditional alternatives has not been tested.
- Alpha 0.001 needs more exact or higher-replication reference results.
- The full unconditional grid has not yet been run.
- Temporal dependence and transfer entropy remain out of scope.
- Novelty has not yet passed an independent literature review.

The preliminary literature screen found close prior work on exact conditional
likelihood-ratio tests, product-hypergeometric stratified inference, and
Gaussian approximation of sparse likelihood-ratio statistics. See
`PRELIMINARY_LITERATURE_MAP.md`. The empirical result is useful, but the
project is not yet cleared as an original thesis contribution.

## Next research stage

1. Fit a diagnostic router on one configuration set and validate it on held-out
   regimes. Route unreliable cases to exact convolution, saddlepoint, or
   conditional Monte Carlo.
2. Run the full unconditional grid and selected million-replicate tail anchors.
3. Add noncentral-hypergeometric power experiments.
4. Compare against explicit blockwise JIDT orderings, not only JIDT's default
   global shuffle.
5. Develop the conditional triangular-array theorem and a conservative
   Berry-Esseen-based reliability statement.
6. Complete the novelty/literature gate before committing to the thesis claim.
