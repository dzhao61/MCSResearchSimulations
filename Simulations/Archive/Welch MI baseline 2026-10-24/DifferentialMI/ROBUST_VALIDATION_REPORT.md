# Robust Validation Report

Date: 25 July 2026

## Decision

**Continue the differential-MI direction, but replace jackknife-Wald as the
primary candidate with the simpler analytic-bias-corrected Wald test.**

The numerical result is strong. The methodological novelty is not yet strong
enough by itself because the bias and variance ingredients are classical.
The next contribution should be a deterministic finite-sample refinement or
a clearly validated operating-regime diagnostic, not another broad
simulation of the same first-order formula.

Near-independence of the two original populations was excluded from this
phase as requested.

## Methods Compared

The target was

```text
H0: I(P) = I(Q), allowing P != Q.
```

The deterministic methods were uncorrected plug-in Wald,
analytic-bias-corrected Wald subtracting `(r-1)(c-1)/(2n)` from each MI
estimate, and delete-one jackknife-Wald.

The resampling methods used 999 optimized count-table label permutations:
raw plug-in, studentized plug-in, studentized analytic correction, and
studentized jackknife.

The table-level multivariate-hypergeometric sampler is exactly equivalent to
permuting individual group labels conditional on pooled cell counts.

## Validation Scale

- Two independent sets of 72 randomized weak-null distributions.
- 3,000 replicate pairs per distribution: 432,000 weak-null comparisons.
- Shapes from `2x2` to `20x20`, including rectangular tables.
- Sample ratios `1:1`, `1:2`, and `1:4`.
- Common MI targets `0.03`, `0.07`, and `0.15` nats.
- Random Dirichlet margins and random log-linear interaction matrices.
- 72 randomized `P=Q` controls with 216,000 replicate pairs.
- 24 pre-selected permutation anchors with 24,000 replicate pairs.
- Six post-hoc hard cases with 60,000 deterministic and 18,000 permutation
  replicate pairs.

Every randomized weak-null pair had equal population MI to approximately
`1e-13` nats or better. Their L1 distribution distances ranged from about
`0.055` to `1.64`, so the test was not comparing nearly identical
populations.

## Main Accuracy Result

Across the 144 randomized weak-null scenarios:

| Method | Mean absolute 5% FPR error | In 3.5%-6.5% band | FPR range | Mean 95% coverage |
|---|---:|---:|---:|---:|
| Plug-in Wald | 0.07116 | 61.1% | 0.0377-0.9670 | 0.88154 |
| Analytic-corrected Wald | **0.00513** | **95.8%** | **0.0377-0.0733** | **0.94986** |
| Jackknife-Wald | 0.00610 | 91.0% | 0.0377-0.0803 | 0.94875 |

The uncorrected plug-in difference can be catastrophically biased when
sample sizes differ because its two leading MI biases do not cancel. The
classical analytic correction removes this problem almost completely.

Jackknife had slightly smaller mean estimator bias but worse tail calibration
and coverage than the analytic correction. Small estimator bias does not
guarantee a better significance test.

The independent 72-scenario replication produced essentially the same
analytic result as the first run:

```text
FPR MAE: 0.00487 and 0.00539
In-band: 97.2% and 94.4%
Mean coverage: 0.94995 and 0.94977
```

## Strong-Null Control

The 72 randomized `P=Q` controls reproduced the finding:

| Method | Mean absolute 5% FPR error | In 3.5%-6.5% band | Mean 95% coverage |
|---|---:|---:|---:|
| Plug-in Wald | 0.07111 | 59.7% | 0.88152 |
| Analytic-corrected Wald | **0.00496** | **97.2%** | **0.95030** |
| Jackknife-Wald | 0.00588 | 93.1% | 0.94918 |

This confirms that the weak-null result is not caused by inaccurate equal-MI
root solving.

## Permutation Comparison

Across all 24 pre-selected anchors:

| Method | Mean absolute 5% FPR error | In 3.5%-6.5% band |
|---|---:|---:|
| Raw permutation | 0.07558 | 33.3% |
| Studentized analytic permutation | 0.03254 | 87.5% |
| Analytic-corrected Wald | **0.00775** | **95.8%** |

The all-anchor studentized-permutation average is dominated by one discovered
boundary case. In that `2x2` pair:

```text
I(P) = I(Q) = 0.03
V(P) = 0.05798
V(Q) = 0.05820
I(pooled mixture) = 0.00000484
V(pooled mixture) = 0.00000969
```

`P` and `Q` had opposite association directions, so their 50/50 mixture was
almost independent. The deterministic statistic remained regular, but the
permutation reference was generated from a near-degenerate mixture. Raw
permutation rejected `97.2%`, studentized permutation rejected `66.0%`, and
analytic Wald rejected `4.6%`.

This is predicted by the assumptions of general studentized permutation
theory: asymptotic linearity and positive variance are also required at the
pooled mixture. Excluding this one unsupported mixture-degenerate anchor,
studentized analytic permutation had mean absolute FPR error `0.00743`, with
`91.3%` of anchors in the 3.5%-6.5% band.

## Hard Small-Sample Boundary

The six post-hoc hard cases used a `1:4` sample ratio, common MI `0.15`, and
low sampling density. With 10,000 deterministic replicates per case:

| Method | FPR range | Mean absolute 5% FPR error |
|---|---:|---:|
| Analytic-corrected Wald | 0.0584-0.0689 | 0.01190 |
| Jackknife-Wald | 0.0635-0.0813 | 0.01993 |

With 3,000 independently simulated permutation comparisons per case:

| Method | FPR range | Mean absolute 5% FPR error |
|---|---:|---:|
| Studentized analytic permutation | 0.0487-0.0603 | 0.00511 |
| Analytic-corrected Wald | 0.0603-0.0680 | 0.01289 |
| Studentized jackknife permutation | 0.0473-0.0657 | 0.00972 |

The analytic Wald method is mildly liberal in this difficult small-sample
regime. This is a normal-tail approximation issue that leading bias
correction alone does not remove.

## Runtime

On the 24 anchors, one table pair required on average:

```text
All deterministic estimators and p-values: 0.170 ms
999 optimized table permutations:          7.775 ms
```

The mean speedup was about `40.8x`, ranging from `6.7x` for `2x2` to about
`184x` for `20x20`. The deterministic timing includes plug-in, analytic, and
jackknife estimators together, so an analytic-only implementation can be
faster still.

The vectorized broad screen averaged about `3.64` microseconds per table pair.
This batch figure should not be used as single-test latency.

These are comparisons to an optimized Python count-table permutation
implementation. They are not direct JIDT timings because JIDT's standard MI
significance test asks whether one population is independent, whereas this
project tests equality of two populations' MI values.

## Errors and Assumptions Audited

- Equal-MI construction error was below approximately `1e-13` nats.
- All 12 deterministic correctness tests passed.
- The influence derivative matched finite differences.
- The influence variance matched the multinomial delta-method covariance.
- The MI Hessian trace produced the classical `(r-1)(c-1)/2` bias
  coefficient.
- No reported p-value was nonfinite or outside `[0,1]`.
- Results replicated with independently generated probability tables and
  independently generated samples.
- Full population tables, seeds, diagnostics, and replicate-level p-values
  were saved.

The remaining assumptions are fixed alphabets, independent observations,
aligned categories, positive population support, and positive influence
variance. Exact/near independence, growing alphabets, structural zeros,
paired data, time series, conditional MI, and transfer entropy are not
covered.

## Thesis Interpretation

This is a promising practical result, but it also narrows the novelty:

- the analytic correction is classical;
- the first-order variance is classical;
- the Wald construction follows standard delta-method theory;
- studentized weak-null permutation is general established theory.

Therefore the completed work validates an important problem and gives a very
strong baseline, but it is not yet a sufficiently original standalone method
claim.

The best next methodological target, while continuing to defer
near-independence, is:

> Develop a deterministic finite-sample refinement of analytic-corrected
> differential-MI Wald inference that fixes the mild liberal tail in highly
> unequal, low-density samples.

Candidate routes are an Edgeworth or Cornish-Fisher correction, a
second-order delta approximation, or a deterministic signed-root
approximation. The existing analytic-corrected Wald test should be the
baseline, and studentized analytic permutation should be the reference when
the pooled-mixture variance is not near zero.

