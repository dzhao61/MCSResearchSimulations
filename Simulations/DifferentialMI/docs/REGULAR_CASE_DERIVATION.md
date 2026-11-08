# Regular-Case Derivation for Differential Discrete Mutual Information

## Scope

This document derives inference for

```text
H0: I(P) = I(Q)
```

where `P` and `Q` are two independent joint distributions for the same pair
of finite-alphabet variables. This is not a test that `P = Q`, and it is not
the usual one-sample test that `I(P) = 0`.

The derivation covers the regular first-order regime: fixed alphabets,
positive population cell probabilities, nonzero population mutual
information, and independent identically distributed observations within
each population. Exact independence and local-to-independence sequences are
deliberately outside the present scope because the first-order variance
degenerates there.

All formulas use natural logarithms. Changing to bits multiplies the
estimates and standard errors by the same constant and therefore leaves the
studentized statistic unchanged.

## 1. Mutual Information as a Multinomial Functional

For an `r x c` joint probability table `P = (p_ij)`, define the row and
column margins

```text
p_i+ = sum_j p_ij
p_+j = sum_i p_ij
```

and

```text
I(P) = sum_ij p_ij log[p_ij / (p_i+ p_+j)].
```

For a positive cell, the ambient derivative is

```text
dI(P) / dp_ij = log[p_ij / (p_i+ p_+j)] - 1.
```

Probability perturbations lie in the simplex tangent space and sum to zero,
so the constant `-1` has no effect on the directional derivative.

For contamination by one observation in cell `(i,j)`,

```text
P_epsilon = (1 - epsilon)P + epsilon delta_ij,
```

the influence function is

```text
IF_P(i,j) = log[p_ij / (p_i+ p_+j)] - I(P).
```

It is centered because its expectation under `P` is zero.

## 2. First-Order Sampling Distribution

Let `P_hat_n` be the empirical joint table from `n` independent observations
from `P`. For a fixed positive table,

```text
sqrt(n) {I(P_hat_n) - I(P)}
  = (1 / sqrt(n)) sum_k IF_P(Z_k) + o_P(1).
```

Therefore,

```text
sqrt(n) {I(P_hat_n) - I(P)} -> Normal(0, V(P)),
```

where

```text
V(P) = Var_P(log[p_XY / (p_X+ p_+Y)]).
```

This is the first-order MI variance derived by Moddemeijer. At independence,
the log density ratio is identically zero and `V(P) = 0`; this is why the
regular normal approximation does not cover independence.

For independent samples of sizes `n` and `m`, define

```text
Delta = I(P) - I(Q)
Delta_hat = I(P_hat_n) - I(Q_hat_m).
```

Then

```text
Var(Delta_hat) = V(P)/n + V(Q)/m + o(1/n + 1/m).
```

The empirical variance estimator is

```text
V_hat(P) =
  sum_{ij: p_hat_ij > 0} p_hat_ij
    {log[p_hat_ij / (p_hat_i+ p_hat_+j)] - I(P_hat)}^2.
```

The plug-in Wald statistic is

```text
Z_plugin =
  {I(P_hat_n) - I(Q_hat_m)}
  / sqrt{V_hat(P)/n + V_hat(Q)/m}.
```

Under the regular null, `Z_plugin` converges to a standard normal
distribution.

## 3. Bias Correction

For a fixed positive `r x c` table, the plug-in MI estimator has leading bias

```text
E[I(P_hat_n)] - I(P)
  = (r - 1)(c - 1)/(2n) + O(n^-2).
```

Consequently, even under `I(P) = I(Q)`, the uncorrected difference has
leading bias

```text
(r - 1)(c - 1)/2 * (1/n - 1/m)
```

when both populations have the same full alphabet. This term is especially
important for unequal sample sizes.

The analytic first-order correction is

```text
I_analytic(P_hat_n) =
  I(P_hat_n) - (r - 1)(c - 1)/(2n).
```

This correction assumes the nominal full support is the population support.
Replacing the dimensions with observed nonempty dimensions changes the
estimator and needs separate theoretical justification.

For any estimator with expansion

```text
E[T_n] = T + a/n + b/n^2 + o(n^-2),
```

the delete-one jackknife estimator

```text
T_JK = n T_n - (n - 1) mean_k(T_{n,-k})
```

removes the `a/n` term. Applied to MI,

```text
I_JK(P_hat_n)
  = n I(P_hat_n) - (n - 1) mean_k I(P_hat_{n,-k}).
```

The jackknife estimator has the same first-order influence function as the
plug-in estimator. The proposed deterministic statistic is therefore

```text
Z_JK =
  {I_JK(P_hat_n) - I_JK(Q_hat_m)}
  / sqrt{V_hat(P)/n + V_hat(Q)/m}.
```

An approximate two-sided p-value and confidence interval are

```text
p = 2 Phi(-abs(Z_JK))

Delta_JK +/- z_(1-alpha/2)
  sqrt{V_hat(P)/n + V_hat(Q)/m}.
```

The analytic correction and jackknife remove the same leading full-support
bias asymptotically. Their finite-sample comparison is therefore a required
part of validation, not an optional baseline.

## 4. Why Raw Permutation Is Not Generally Valid

Let `N = n + m` and `lambda = n/N`. A label permutation treats both
permuted samples as draws from the pooled mixture

```text
R = lambda P + (1 - lambda) Q.
```

For the unstudentized statistic scaled by `sqrt(N)`, the permutation variance
converges to

```text
V(R) / {lambda(1 - lambda)}.
```

Under the weak null `I(P) = I(Q)`, the actual sampling variance converges to

```text
V(P)/lambda + V(Q)/(1 - lambda).
```

These expressions are not equal in general. Raw permutation is exact under
the stronger null `P = Q`, but it can be conservative or anti-conservative
when only the MI values are equal.

Chung and Romano prove that, for asymptotically linear estimators with
consistent variance estimates, studentizing each permuted statistic makes
both its permutation reference distribution and its true weak-null sampling
distribution converge to standard normal. Our MI statistic is an explicit
finite-multinomial application of that general theorem.

For MI, this permutation result also requires the pooled mixture to be in the
regular regime:

```text
V(R) > 0.
```

It is possible for `P` and `Q` to each have nonzero MI while having opposite
association directions whose mixture is independent or nearly independent.
In that case the deterministic two-sample Wald statistic can remain regular
because `V(P)` and `V(Q)` are positive, while the studentized permutation
reference degenerates because `V(R)` is zero or very small.

## 5. Assumptions for the Regular Theorem

The first-order result requires:

1. Observations are independent and identically distributed within each
   group, and the two groups are independent.
2. `r` and `c` are fixed as `n,m -> infinity`.
3. `P` and `Q` use the same aligned categories and have strictly positive
   population cell probabilities on the declared support.
4. `n/(n+m)` converges to a value strictly between zero and one.
5. `V(P)` and `V(Q)` are positive.
6. The empirical variance estimators are consistent.
7. All estimates use the same logarithm base.

The current theory does not claim validity for:

- exact or near independence;
- alphabet sizes growing with sample size;
- structural zeros or severe sampling sparsity;
- paired observations, clusters, or time series;
- conditional MI or transfer entropy.

These are scope boundaries, not implementation details.

For studentized permutation in particular, the same asymptotic linearity and
positive-variance conditions must additionally hold at the pooled mixture
`R = lambda P + (1-lambda)Q`.

## 6. Claims Supported by This Derivation

The defensible claims are:

- The deterministic jackknife-Wald test is first-order valid for differences
  in discrete MI under the stated regular assumptions.
- Raw label permutation is not generally a valid test of equal MI when the
  two full distributions differ.
- Studentized permutation is asymptotically valid under the same regular
  conditions and remains exact under `P = Q`, subject to permutation
  discreteness/randomization.
- Analytic and jackknife bias correction agree at first order, so any claimed
  practical advantage of the jackknife must be shown empirically or through
  a higher-order argument.

This derivation does not make the underlying influence-function,
bias-correction, jackknife, or studentization ideas novel.

## Primary References

- Moddemeijer, R. (1989), "On estimation of entropy and mutual information of
  continuous distributions."
  https://doi.org/10.1016/0165-1684(89)90132-1
- Chung, E. and Romano, J. P. (2013), "Exact and asymptotically robust
  permutation tests." https://doi.org/10.1214/13-AOS1090
- Kandasamy, K. et al. (2015), "Influence Functions for Machine Learning:
  Nonparametric Estimators for Entropies, Divergences and Mutual
  Informations." https://arxiv.org/abs/1411.4342
