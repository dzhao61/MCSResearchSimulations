# Edgeworth Refinement Theory Gate

## Decision

A simple one-term Edgeworth correction is **not** adopted as the next
finite-sample method for the two-sided differential-MI test.

This is a theory-gate decision, not a negative empirical result. The usual
skewness-only Edgeworth formula does not provide a justified improvement to
the current studentized, two-sided statistic.

## Candidate Calculation

Let the first-order sampling error of the analytically bias-corrected MI
difference be

```text
S =
  (1/n) sum_a IF_P(Z_a)
  - (1/m) sum_b IF_Q(W_b),
```

with variance

```text
s^2 = V(P)/n + V(Q)/m.
```

For a non-studentized standardized sum `Z = S/s`, the one-term Edgeworth CDF
has the form

```text
F_E(z) =
  Phi(z) + gamma/6 * (1 - z^2) * phi(z),
```

where

```text
gamma =
  {M3(P)/n^2 - M3(Q)/m^2}
  / {V(P)/n + V(Q)/m}^{3/2}
```

and `M3` is the third centered moment of the influence function.

## Why It Does Not Solve the Present Problem

The first correction term,

```text
gamma/6 * (1 - z^2) * phi(z),
```

is an even function of `z`. It therefore cancels when a symmetric two-sided
tail is formed as

```text
P(|Z| >= |z|)
  = F(-|z|) + 1 - F(|z|).
```

Using `2 min{F(z), 1-F(z)}` instead would preserve an asymmetric correction,
but that does not make the formula valid for the statistic actually used.
The current statistic estimates its standard error from the same samples.
A higher-order expansion for a studentized nonlinear functional contains
additional terms caused by:

- estimating the influence variances;
- the second and higher derivatives of mutual information;
- the first-order bias correction;
- the interaction between numerator and denominator estimation.

Adding only empirical skewness would omit terms of the same asymptotic order
as the retained correction.

## Consequence

Implementing a skewness-only Edgeworth p-value would create an apparently
simple method without a clean validity argument. That conflicts with the
project's thesis goal of a deterministic method whose assumptions and
operating regime can be stated precisely.

The next candidate is instead an influence-function saddlepoint
approximation. It uses the full empirical cumulant-generating function of the
linearized sampling error, remains deterministic, and applies to arbitrary
fixed rectangular tables without contingency-table dynamic programming.

## Reconsideration Rule

Edgeworth can be revisited only if one of the following is completed:

1. a full studentized von Mises/Edgeworth derivation for the corrected MI
   difference; or
2. a literature result whose assumptions directly cover this statistic and
   whose nuisance terms can be estimated consistently.

Until then, Edgeworth is recorded as a justified no-go branch rather than a
failed implementation.
