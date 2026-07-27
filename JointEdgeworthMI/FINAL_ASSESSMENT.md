# Final Assessment: Joint Studentized Edgeworth MI

## Decision

The final scientific decision is **NO-GO as a complete significance test**.

The frozen validation mechanically passed all nine adoption criteria, but a
post-run adversarial audit found that the validity guardrail selectively
removed extreme, significant observations. The conditional false-positive
rates used by the frozen decision are therefore not an acceptable measure of
unconditional test calibration.

The underlying covariance derivation remains useful and well supported.

## Method

For the bias-corrected MI difference `D_hat` and estimated squared standard
error `H_hat`, the candidate calculates

```text
lambda = Cum3(D_hat) / h^(3/2)
c = Cov(D_hat,H_hat) / h^(3/2),
```

using MI-specific influence functions. It approximates the CDF of the
studentized statistic by

```text
F_T(x) =
    Phi(x)
    + phi(x) [
        lambda(1-x^2)/6
        + c x^2/2
      ].
```

The calculation is deterministic, has no fitted constants, is invariant to
group swapping and category relabelling, and reduces to the known
studentized-mean Edgeworth formula when `c=lambda`.

## Frozen Evidence

The fresh experiment covered 1.94 million null table pairs and 50,000 power
pairs:

| Regime | Normal MAE | Naive Welch | Influence-df | Joint Edgeworth |
| --- | ---: | ---: | ---: | ---: |
| Broad | 0.00550 | 0.00531 | 0.00514 | 0.00428 |
| Hard | 0.01230 | 0.01130 | 0.00810 | 0.00681 |
| Strong null | 0.00536 | 0.00520 | 0.00558 | 0.00417 |
| Stress diagnostic | 0.03045 | 0.02889 | 0.02325 | 0.01366 |
| Balanced design 0 | 0.00556 | 0.00563 | 0.00735 | 0.00484 |

The candidate was valid for `99.805%` of broad, `99.575%` of hard, and
`99.811%` of strong-null table pairs, passing the frozen aggregate
`99.5%` criterion. Runtime was `0.265 ms`, or `2.18x` normal Wald.

## Why the Mechanical GO Is Rejected

Invalid cases were concentrated in the tails:

| Stage | Invalid cases | Normal-significant at 0.05 |
| --- | ---: | ---: |
| Broad | 1,407 | 98.9% |
| Hard | 1,021 | 100% |
| Strong null | 1,363 | 98.9% |
| Stress | 7,465 | 52.4% |

The regular-grid invalid cases had median absolute statistics around `3`.
Most produced raw Edgeworth CDF values above one or below zero. Dropping them
conditions on not being extreme.

Three possible treatments are:

- Return `NaN`: this is the frozen candidate, but it fails precisely on
  observations most likely to be significant.
- Treat invalid cases as non-significant: this improves apparent calibration
  by suppressing genuine tail evidence and is not defensible.
- Fall back to normal or clip the CDF to its boundary: this retains the
  extreme rejections but removes most of the apparent improvement.

Normal fallback gives:

| Regime | Fallback MAE | Frozen comparator requirement |
| --- | ---: | ---: |
| Broad | 0.00582 | At most 0.00556 |
| Hard | 0.01082 | At most 0.01017 and 10% gain |
| Strong null | 0.00556 | At most 0.00545 |
| Balanced design 0 | 0.00680 | At most 0.00606 |

Thus a usable completed test fails four central adoption conditions.

## Theory Diagnosis

The population influence formula for
`Cov(D_hat,H_hat)` is strongly supported:

- broad Pearson correlation with empirical covariance: about `0.995`;
- hard correlation: about `0.996`; and
- broad sign agreement: about `98%`.

The first-order third-cumulant approximation is not reliable at these sample
sizes. Across the broad grid, its empirical raw counterpart had opposite sign
in most scenarios. The predicted studentized skewness had useful rank
information but often substantially overstated the magnitude.

This explains the mixed result: the correction captures real
numerator/denominator dependence in the central distribution, but its
first-order polynomial CDF is not a globally valid tail approximation.

## Recommendation

Keep the derived covariance expression as a theoretical and diagnostic
result. Do not use or publish the current Edgeworth p-value as a finished
test.

A genuine continuation would require all of:

- fourth cumulants and second-order symmetric-tail terms;
- second-order bias of the MI difference;
- joint cumulants involving the variance estimate; and
- a globally valid tail construction, such as a justified transformed
  expansion or saddlepoint method.

That is now a materially larger project. It should only be pursued if this
level of asymptotic theory fits the thesis scope. The current experiment has
decisively invalidated the simpler first joint correction while preserving a
useful analytic covariance component.
