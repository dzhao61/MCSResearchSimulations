# Joint Studentized Edgeworth Approximation for Differential MI

Derivation frozen: 27 July 2026

## Target Statistic

For independent discrete joint distributions `P` and `Q`, test

```text
H0: I(P) = I(Q), allowing P != Q.
```

The existing bias-corrected statistic is

```text
D_hat =
    I(P_hat) - d/(2 n_P)
    - I(Q_hat) + d/(2 n_Q)

H_hat = V(P_hat)/n_P + V(Q_hat)/n_Q

T = D_hat / sqrt(H_hat),
```

where `d=(r-1)(c-1)` and

```text
V(P) = Var_P(log[p_XY/(p_X p_Y)]).
```

Under the weak null, `D_hat` estimates zero. The normal method treats `T` as
standard normal. The previous influence-df method accurately modelled the
variability of `H_hat`, but a moment-matched random denominator does not make
the ratio Student-t.

## Group-Level Influence Quantities

For one positive-support distribution, define

```text
l_ij = log[p_ij/(p_{i+} p_{+j})]
mu = E[l] = I(P)
u_ij = l_ij - mu
V = E[u^2].
```

The MI influence function is `u`. The variance-functional influence function
derived in `InfluenceDfMI` is

```text
w_ab =
    l_ab^2 - E[l^2]
    + 2(l_ab - E[l|X=a] - E[l|Y=b] + mu)
    - 2 mu(l_ab - mu).
```

Both have probability-weighted mean zero. Define

```text
m3 = E[u^3]
g = E[u w] = Cov(u,w).
```

## Joint Cumulants for Two Groups

Let the population first-order variance of `D_hat` be

```text
h = V_P/n_P + V_Q/n_Q.
```

The leading third cumulant of `D_hat` is

```text
K3 =
    m3_P/n_P^2
    - m3_Q/n_Q^2.
```

The leading covariance between the numerator and estimated squared standard
error is

```text
C =
    g_P/n_P^2
    - g_Q/n_Q^2.
```

The minus signs occur because the `Q` MI estimate enters `D_hat` negatively,
while its variance component enters `H_hat` positively.

Use the standardized quantities

```text
lambda = K3 / h^(3/2)
c = C / h^(3/2).
```

Both are first non-Gaussian-order terms and converge to zero in regular
large-sample regimes.

## Studentized Edgeworth CDF

Write

```text
Z = D_hat/sqrt(h)
R = (H_hat-h)/h.
```

To first non-Gaussian order,

```text
T = Z / sqrt(1+R) = Z - ZR/2 + smaller terms.
```

Combining the ordinary Edgeworth correction for `Z` with
`Cov(Z,R)=c` gives

```text
F_T(x) approximately
    Phi(x)
    + phi(x) [
        lambda(1-x^2)/6
        + c x^2/2
      ].
```

For the ordinary studentized sample mean, `c=lambda`; the expression reduces
to the standard first-order studentized-mean Edgeworth formula

```text
Phi(x) + phi(x) lambda(1+2x^2)/6.
```

This identity is a check on the signs and coefficients.

The candidate uses plug-in estimates of `lambda` and `c`. Its two-sided
equal-tailed p-value is

```text
p = 2 min(F_T(T_observed), 1-F_T(T_observed)).
```

Using `2 min` rather than summing symmetric absolute tails is necessary:
the first-order skew correction cancels from
`F_T(-|T|) + 1-F_T(|T|)`.

## Guardrails

An Edgeworth expansion is not globally guaranteed to be a CDF. The candidate
is valid only when:

- the original first-order MI statistic is valid;
- `lambda`, `c`, the raw CDF, and the local density are finite;
- the raw CDF at the observed statistic lies in `[0,1]`; and
- the local density factor is positive:

```text
1 + (2 a2-a0)x - a2 x^3 > 0,

a0 = lambda/6,
a2 = -lambda/6 + c/2.
```

Invalid calculations return `NaN`; they do not silently revert to normal.
Valid probabilities are clipped only for floating-point roundoff.

## Scope

This is a deterministic, tuning-free, first non-Gaussian-order approximation.
It remains a regular positive-support method. It does not solve:

- MI at or extremely near zero, where first-order influence variance
  degenerates;
- changing support or severe empirical boundary behavior;
- residual bias beyond the leading `d/(2n)` correction; or
- second-order symmetric-tail errors involving fourth cumulants.

The decisive simulation determines whether this first joint correction is
already useful enough or whether a full second-order expansion is required.
