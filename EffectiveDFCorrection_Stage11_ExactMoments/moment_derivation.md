# Moment Equations For The MI Null

This note derives the first finite-sample moment corrections for

```text
T = 2 N I_hat(X;Y)
```

under the product-multinomial independence null

```text
P(X = i, Y = j) = p_i q_j.
```

Let

```text
kx  = number of X states
ky  = number of Y states
nu0 = (kx - 1)(ky - 1)
Sx  = sum_i 1 / p_i
Sy  = sum_j 1 / q_j
Sx2 = sum_i 1 / p_i^2
Sy2 = sum_j 1 / q_j^2
```

The statistic uses empirical marginals, so

```text
I_hat = H_hat(X) + H_hat(Y) - H_hat(X,Y).
```

## Mean

For a multinomial plug-in entropy estimator with category probabilities `r_l`,
the Taylor expansion of

```text
g(x) = -x log x
```

around `r_l` gives

```text
E[H_hat(r)]
  = H(r)
    - (m - 1) / (2N)
    - (sum_l 1/r_l - 1) / (12 N^2)
    - (sum_l 1/r_l^2 - sum_l 1/r_l) / (12 N^3)
    + O(N^-4).
```

Apply this to `X`, `Y`, and the joint distribution `pi_ij = p_i q_j`.
Because `H(X) + H(Y) - H(X,Y) = 0` under independence, the entropy terms cancel.

The leading term is

```text
E[I_hat]
  = nu0 / (2N)
    + ((Sx - 1)(Sy - 1)) / (12 N^2)
    + O(N^-3).
```

Therefore

```text
E[T]
  = nu0
    + ((Sx - 1)(Sy - 1)) / (6N)
    + O(N^-2).
```

Define

```text
B = ((Sx - 1)(Sy - 1)) / 6.
```

Then the first-order mean equation is

```text
mu = E[T] = nu0 + B/N + O(N^-2).
```

The next term from the same entropy expansion is

```text
E[T]
  = nu0
    + B/N
    + C/N^2
    + O(N^-3),
```

where

```text
C = (Sx2 Sy2 - Sx Sy - (Sx2 - Sx) - (Sy2 - Sy)) / 6.
```

For sparse marginals, this higher-order term can be large unless every expected
cell count is already comfortably above 1.

## Variance

The regular large-sample likelihood-ratio expansion gives a Bartlett-scaled
chi-square approximation:

```text
T / (1 + B/(nu0 N)) = chi2_nu0 + O_p(N^-2)
```

equivalently

```text
T ~= s chi2_nu0,
where
s = 1 + B/(nu0 N).
```

This scaling reproduces the mean correction:

```text
E[s chi2_nu0]
  = s nu0
  = nu0 + B/N.
```

It also gives the first-order variance correction:

```text
Var[T]
  = Var[s chi2_nu0] + O(N^-2)
  = 2 nu0 s^2 + O(N^-2)
  = 2 nu0 + 4B/N + O(N^-2).
```

So the first-order variance equation is

```text
sigma2 = Var[T] = 2 nu0 + 4B/N + O(N^-2).
```

Substituting `B`:

```text
sigma2
  = 2 nu0
    + (2/3) ((Sx - 1)(Sy - 1)) / N
    + O(N^-2).
```

## Consequence For Scaled Chi-Square Parameters

Moment matching uses

```text
nu_eff = 2 mu^2 / sigma2
a      = sigma2 / (2 mu).
```

Using the first-order equations:

```text
mu    = nu0 + B/N
sigma2 = 2 nu0 + 4B/N.
```

Then

```text
a = 1 + B/(nu0 N) + O(N^-2),
```

but

```text
nu_eff = nu0 + O(N^-2).
```

This is important: in the regular asymptotic regime, the first-order correction
is mostly a scale correction, not an effective-DF correction.

The strong `nu_eff` deviations seen in sparse simulations are therefore not
explained by the first regular asymptotic term. They come from non-regular
sparse-cell behavior: zeros, boundary effects, and the geometry of many low
expected-count cells.

## Binary Example

For binary variables with

```text
p_X = (1-p, p)
p_Y = (1-q, q)
```

we have

```text
Sx = 1/p + 1/(1-p)
Sy = 1/q + 1/(1-q)
nu0 = 1.
```

So

```text
B = ((Sx - 1)(Sy - 1)) / 6.
```

If `p = q = 1/2`, then `Sx = Sy = 4`, so

```text
B = 3 * 3 / 6 = 1.5.
```

Thus

```text
E[T]   = 1 + 1.5/N + O(N^-2)
Var[T] = 2 + 6/N + O(N^-2).
```

If `p` and `q` are small, then `Sx ~ 1/p` and `Sy ~ 1/q`, giving

```text
B ~ 1 / (6 p q).
```

Since the rarest expected cell is approximately

```text
lambda = N p q,
```

the mean correction becomes

```text
E[T] ~ 1 + 1/(6 lambda).
```

This is the theoretical origin of the `lambda` / `lambda_tp` correction scale.
