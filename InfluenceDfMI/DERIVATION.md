# MI-Specific Influence-Matched Degrees of Freedom

Derivation frozen: 27 July 2026

## Target

For two independent discrete joint distributions, test

```text
H0: I(P) = I(Q), allowing P != Q.
```

The existing regular-case statistic is

```text
Delta_BC = [I(P_hat) - d/(2 n_P)] - [I(Q_hat) - d/(2 n_Q)]

SE^2 = V(P_hat)/n_P + V(Q_hat)/n_Q

T = Delta_BC / SE,
```

where `d=(r-1)(c-1)` and

```text
V(P) = Var_P(log[p_XY/(p_X p_Y)]).
```

The current Welch-inspired reference assigns each estimated variance
component `n_i-1` degrees of freedom. That assignment is exact for an
ordinary Gaussian sample variance, not for the nonlinear plug-in functional
`V(P_hat)`.

## Influence Function of MI

Define

```text
l_ij = log[p_ij/(p_{i+} * p_{+j})]
mu = I(P) = E_P[l].
```

Under contamination

```text
P_epsilon = (1-epsilon) P + epsilon delta_(a,b),
```

the influence function of MI is

```text
IF_I(a,b) = l_ab - mu.
```

This gives the familiar first-order variance `V(P)/n`.

## Influence Function of the Variance Functional

Let

```text
M2 = E_P[l^2]
r_i = E_P[l | X=i]
c_j = E_P[l | Y=j]
V(P) = M2 - mu^2.
```

The derivative of the local score under contamination at `(a,b)` is

```text
d l_ij =
    1[(i,j)=(a,b)] / p_ij
    - 1[i=a] / p_i+
    - 1[j=b] / p_+j
    + 1.
```

Differentiating `M2` and then subtracting the derivative of `mu^2` gives

```text
IF_V(a,b) =
    l_ab^2 - M2
    + 2(l_ab - r_a - c_b + mu)
    - 2 mu(l_ab - mu).
```

As required for an influence function,

```text
E_P[IF_V] = 0.
```

Define

```text
tau_V^2 = Var_P(IF_V).
```

For fixed positive support and away from first-order degeneracy,

```text
sqrt(n) [V(P_hat) - V(P)] -> Normal(0, tau_V^2).
```

Therefore, for the variance component

```text
a_hat = V(P_hat)/n,
```

the leading sampling variance is

```text
Var(a_hat) approximately tau_V^2 / n^3.
```

## MI-Specific Component Degrees of Freedom

Approximate `a_hat` by a scaled chi-square variable with component degrees of
freedom `nu_V`. A scaled chi-square variable with mean `a` has variance
`2a^2/nu_V`. Matching this to the leading variance above gives

```text
2 [V(P)/n]^2 / nu_V = tau_V^2 / n^3
```

and hence

```text
nu_V = 2 n V(P)^2 / tau_V^2.
```

The plug-in estimate used by the candidate is

```text
nu_P_hat = 2 n_P V(P_hat)^2 / tau_P_hat^2
nu_Q_hat = 2 n_Q V(Q_hat)^2 / tau_Q_hat^2.
```

For independent groups, combine the two estimated components using the
general Satterthwaite moment match:

```text
a = V(P_hat)/n_P
b = V(Q_hat)/n_Q

nu_IF = (a+b)^2 / [a^2/nu_P_hat + b^2/nu_Q_hat].
```

The proposed reference is

```text
p_IF = 2 * StudentT_nu_IF.sf(abs(T)).
```

## What This Derivation Does and Does Not Establish

It establishes a first-order moment match for the sampling variability of the
plug-in denominator. It gives a principled replacement for the unexplained
`n_i-1` component degrees of freedom.

It does not prove that `T` is exactly Student distributed. In particular:

- `Delta_BC` and its estimated variance can be strongly correlated;
- the bias correction is only first order;
- empirical zero cells can invalidate smooth positive-support reasoning;
- MI near zero has a degenerate first-order influence function; and
- estimating `tau_V^2` adds another plug-in approximation.

The candidate is therefore an influence-matched Satterthwaite approximation,
not an exact finite-sample test.
