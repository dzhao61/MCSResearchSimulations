# Fast Weak-Null Inference for Differences in Discrete Mutual Information

## Proposed Thesis Question

Given two independent populations with the same aligned categorical
variables, test

```text
H0: I_P(X;Y) = I_Q(X;Y)
```

without assuming the complete joint distributions are equal.

This is not the usual one-population independence test `I(P)=0`, and it is
not a two-sample test of `P=Q`.

## Why This Matters

Applied information-theoretic work compares MI matrices across populations.
Boughter et al. (2020, 2023), for example, use raw group-label permutation to
test MI differences in immune-sequence populations.

Raw permutation is exact under the strong null `P=Q`. The scientific target
above is a weak null: two different distributions can have the same MI.
Under that null, raw permutation generally estimates the wrong sampling
variance and can be severely conservative or anti-conservative.

The practical goal is a method that is:

- calibrated for equal MI when `P` and `Q` differ;
- deterministic and much faster than repeated shuffling;
- explicit about finite-sample bias and failure boundaries; and
- usable for rectangular, unequal-sample categorical tables.

## Retained Method

For each group, calculate plug-in MI in nats and remove its classical leading
full-support bias:

```text
I_BC(P_hat) = I(P_hat) - (r-1)(c-1)/(2n).
```

Estimate the first-order MI variance from the empirical local log-density
ratio:

```text
V_hat(P) =
  Var_Phat[log{p_hat_XY/(p_hat_X p_hat_Y)}].
```

Then form

```text
Delta_BC = I_BC(P_hat) - I_BC(Q_hat)

SE = sqrt{V_hat(P)/n + V_hat(Q)/m}

Z = Delta_BC/SE,

p = 2 Phi(-|Z|).
```

All ingredients are established statistical prior art. The thesis
contribution is not invention of the bias or variance formula. The defensible
contribution is identifying and correcting an existing weak-null practice,
mapping finite-sample operating conditions, documenting an MI-specific
permutation degeneracy, and delivering tested software.

## Main Evidence

The broad experiment generated pairs of different positive multinomial
tables with exactly equal population MI.

- 2 independent scenario seeds.
- 144 weak-null scenarios.
- 432,000 table-pair comparisons.
- Shapes from `2x2` to `20x20`, square and rectangular.
- Equal, `1:2`, and `1:4` sample-size ratios.
- Balanced-like through strongly heterogeneous margins.
- Population MI at least `0.03` nats.

At nominal `alpha=0.05`:

| Method | Mean absolute FPR error | Scenarios in 3.5%-6.5% | Maximum FPR |
|---|---:|---:|---:|
| Uncorrected Wald | 0.07116 | 61.1% | 0.967 |
| Analytic corrected Wald | **0.00513** | **95.8%** | 0.073 |
| Jackknife Wald | 0.00610 | 91.0% | 0.080 |

The corrected method's mean 95% coverage was `0.94986`.

On 23 regular pooled-mixture permutation anchors:

| Method | Mean absolute 5% FPR error | Scenarios in 3.5%-6.5% |
|---|---:|---:|
| Raw permutation | 0.03878 | 34.8% |
| Studentized analytic permutation | 0.00743 | 91.3% |
| Analytic corrected Wald | 0.00791 | 95.7% |

The full deterministic estimator set averaged `0.170 ms` per table pair,
versus `7.775 ms` for 999 optimized count-table permutations, a mean
`40.8x` advantage. The standalone primary Wald calculation is simpler still.

## Finite-Sample Refinement Result

Two planned refinements were investigated sequentially.

1. A one-term Edgeworth correction failed its theory gate because its leading
   skewness term cancels in a symmetric two-sided tail; a correct
   studentized expansion would require additional higher-order terms.
2. A general empirical influence-saddlepoint method was implemented for any
   fixed rectangular table and tested on 288,000 null comparisons.

The saddlepoint method was numerically stable after a documented near-mean
fix, but did not improve calibration:

| Method | Mean absolute 5% FPR error | In-band scenarios |
|---|---:|---:|
| Analytic Wald | 0.00561 | 96.5% |
| Influence saddlepoint | 0.00571 | 96.5% |

The pre-specified decision rule therefore rejected it. This negative result
suggests the remaining error is driven more by nonlinear estimation,
residual bias, and variance estimation than by the tail shape of the
first-order influence sum.

## Real-Data Demonstration

The pre-specified UCI Adult analysis compared education-income MI between
female and male records:

```text
Female corrected MI = 0.03902 nats
Male corrected MI   = 0.07616 nats
Difference          = -0.03714 nats
95% CI              = [-0.04308, -0.03119]
Wald p              = 1.89e-34
```

Raw and studentized 9,999-permutation tests both reached only their resolution
floor, `p=0.0001`. Wald took `0.46 ms`; all permutations took `50 ms`.

This example shows the practical tail-resolution and runtime benefit. It is
descriptive and unweighted, not causal.

## Important Boundaries

Current claims are limited to:

- independent samples;
- fixed finite aligned alphabets;
- positive population support;
- MI and influence variance away from zero;
- the declared full-support dimensions; and
- ordinary multinomial sampling.

The method does not currently cover near independence, structural zeros,
growing alphabets, paired/time-series observations, conditional MI, or
transfer entropy.

Studentized permutation has an additional boundary: the pooled mixture must
have positive influence variance. Opposite association directions can make
the pooled mixture nearly independent even when both original populations
are regular.

## Honest Thesis Position

The project is already a strong reproducible methodological validation and
software thesis. Its claim is more modest than “a new estimator”:

> Existing applications compare discrete mutual information across
> populations using raw label permutation. This thesis characterizes the
> weak-null failure of that practice and develops fast, bias-corrected
> deterministic inference with explicitly validated operating conditions.

The key supervisor decision is whether that correction-and-validation
contribution is sufficient for the degree, or whether a further contribution
such as simultaneous differential-MI network inference should be required.

