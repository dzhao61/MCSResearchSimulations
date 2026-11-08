# Fast Differential Mutual Information

## 1. Scientific Question

```text
H0: I_P(X;Y) = I_Q(X;Y), allowing P != Q
```

- Compare association strength across two populations.
- Not one-sample independence.
- Not equality of complete distributions.

## 2. Applied Motivation

- Published immune-sequence analyses compare MI matrices.
- Their significance method is raw group-label permutation.
- Raw permutation is exact for `P=Q`, not generally for equal MI.

## 3. Why Raw Permutation Can Fail

- True weak-null variance uses `V(P)/n + V(Q)/m`.
- Permutation samples from pooled mixture `R`.
- Its unstudentized variance depends on `V(R)`.
- Equal MI does not imply these variances agree.

## 4. Proposed Practical Method

```text
MI_BC = MI_plugin - (r-1)(c-1)/(2n)
SE^2  = V_hat(P)/n + V_hat(Q)/m
Z     = (MI_BC,P - MI_BC,Q)/SE
```

- Deterministic.
- General fixed rectangular tables.
- Natural-log units.
- Explicit diagnostics and exclusions.

## 5. Broad Null Calibration

144 scenarios, 432,000 table pairs:

| Method | Mean abs. 5% error | In 3.5%-6.5% |
|---|---:|---:|
| Plugin Wald | 0.07116 | 61.1% |
| Analytic corrected Wald | **0.00513** | **95.8%** |
| Jackknife Wald | 0.00610 | 91.0% |

Corrected Wald mean 95% coverage: `0.94986`.

## 6. Permutation Comparison

On regular pooled-mixture anchors:

| Method | Mean abs. 5% error |
|---|---:|
| Raw permutation | 0.03878 |
| Studentized permutation | 0.00743 |
| Corrected Wald | 0.00791 |

Raw permutation can fail badly under the exact target null.

## 7. Runtime

- All deterministic estimators: `0.170 ms`.
- 999 optimized table permutations: `7.775 ms`.
- Mean advantage: `40.8x`.
- UCI case, standalone Wald: `0.46 ms`.
- UCI case, 9,999 permutations: `50 ms`.

## 8. Attempted Refinements

- Simple Edgeworth: theory-gate no-go.
- General influence saddlepoint: implemented and tested.
- 288,000 null comparisons.
- Wald MAE `0.00561`; saddlepoint `0.00571`.
- Rejected under the pre-specified rule.

Takeaway: a more complex tail approximation did not fix errors arising
earlier in nonlinear estimation.

## 9. Real-Data Example

UCI Adult, education-income MI:

| Group | Corrected MI, nats |
|---|---:|
| Female | 0.03902 |
| Male | 0.07616 |

Difference `-0.03714`, 95% CI `[-0.04308,-0.03119]`,
Wald `p=1.89e-34`.

## 10. Scope and Risks

In scope:

- independent samples;
- fixed aligned alphabets;
- positive support;
- MI away from zero.

Out of scope:

- near independence;
- structural zeros and growing alphabets;
- time series, CMI, and TE.

## 11. Novelty Boundary

Not new:

- MI bias/variance;
- influence functions;
- studentized permutation;
- empirical saddlepoint theory.

Candidate contribution:

- correction of an existing applied weak-null practice;
- MI-specific theory and pooled-mixture failure boundary;
- broad adversarial validation;
- fast tested implementation.

## 12. Decisions Requested

1. Is this correction-and-validation contribution sufficient for the thesis?
2. Should the final extension be simultaneous differential-MI network
   inference?
3. Is excluding near independence acceptable for the main thesis?
4. Which formal literature databases and claim wording should be required?

