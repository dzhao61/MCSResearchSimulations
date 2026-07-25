# Influence-Function Saddlepoint Refinement

## Status

This is an experimental deterministic refinement of the frozen
analytic-bias-corrected Wald baseline. It is not yet the primary method.

The construction combines established ingredients:

- the first-order influence function of discrete mutual information;
- the classical leading bias correction;
- empirical saddlepoint approximation for sums and M-estimators; and
- the Lugannani-Rice tail formula.

The project-specific contribution being evaluated is their use for fast
two-sample inference on an equal-MI weak null.

## Target

For two independent positive fixed-alphabet distributions, test

```text
H0: Delta = I(P) - I(Q) = 0.
```

The observed estimate remains the frozen baseline estimate

```text
Delta_BC =
  I(P_hat) - df/(2n)
  - I(Q_hat) + df/(2m),

df = (r-1)(c-1).
```

## Linearized Sampling Error

For group `P`, define the empirical local MI score and centered influence
score

```text
l_P(i,j) =
  log[p_hat_ij/(p_hat_i+ p_hat_+j)]

psi_P(i,j) = l_P(i,j) - I(P_hat).
```

Only observed cells have positive empirical probability and enter the
calculation. Define `psi_Q` analogously. The first-order error in the
two-sample difference is approximated by

```text
S =
  (1/n) sum_{a=1}^n psi_P(Z_a)
  - (1/m) sum_{b=1}^m psi_Q(W_b).
```

Under the empirical distributions, the summands are independent and
centered. The first two cumulants are exactly

```text
K'(0) = 0

K''(0) =
  V_hat(P)/n + V_hat(Q)/m,
```

so the normal approximation to this construction is the frozen Wald
baseline.

## Empirical Cumulant-Generating Function

Because the influence scores take one value per occupied table cell, the CGF
can be evaluated without expanding the counts into individual observations:

```text
K(t) =
  n log sum_ij p_hat_ij exp{t psi_P(i,j)/n}
  + m log sum_ij q_hat_ij exp{-t psi_Q(i,j)/m}.
```

Its derivatives are weighted moments under exponential tilting. The
saddlepoint `t_hat` solves

```text
K'(t_hat) = Delta_BC.
```

Evaluation is `O(s rc)` for `s` root iterations and does not scale linearly
with `n+m`. It is deterministic and uses no permutations or bootstrap
samples.

## Lugannani-Rice Tail

For `x = Delta_BC`, define

```text
w = sign(t_hat) sqrt{2[t_hat x - K(t_hat)]}

u = t_hat sqrt{K''(t_hat)}.
```

The approximate CDF and upper tail are

```text
F(x) =
  Phi(w) + phi(w){1/w - 1/u}

S(x) =
  Phi(-w) + phi(w){1/u - 1/w}.
```

The two-sided p-value is

```text
p = 2 min{F(x), S(x)},
```

clipped to `[0,1]` after checking finiteness.

## Guardrails and Routes

The implementation reports, rather than hides, the calculation route:

- `lugannani_rice`: a valid interior root and numerically stable tail;
- `normal_near_mean`: `x` is too close to the CGF mean for the raw
  Lugannani-Rice expression;
- `normal_support_boundary`: `x` is at or beyond the support of the empirical
  linearized sum;
- `normal_numerical_fallback`: root or tail evaluation failed;
- `invalid`: the first-order variance is zero or nonfinite.

Every finite route must return a p-value in `[0,1]`. The root residual,
iterations, empirical support bounds, and saddlepoint quantities are saved.

## What This Approximation Does Not Include

The method approximates the distribution of the first-order linearized
sampling error. It does not exactly reproduce:

- the nonlinear finite-sample distribution of plug-in MI;
- uncertainty from estimating the influence scores;
- higher-order bias after the analytic correction;
- a fully studentized saddlepoint distribution; or
- independence and near-independence, where the first-order derivative
  degenerates.

These omissions are why the method must beat the frozen Wald baseline in
pre-specified simulations before it can be retained.

## Prior-Art Boundary

Empirical saddlepoint approximation is established statistical prior art,
including Feuerverger (1989) and Ronchetti and Welsh (1994). Saddlepoint
approximations for genuinely studentized statistics are more involved, as
shown by Daniels and Young (1991).

No claim should be made that empirical saddlepoint approximation itself is
new. The candidate contribution is the discrete-MI two-sample construction,
its computational form over occupied cells, and its validated operating
regime.

## Primary Sources

- Feuerverger (1989), *On the empirical saddlepoint approximation*:
  https://doi.org/10.1093/biomet/76.3.457
- Daniels and Young (1991), *Saddlepoint approximation for the studentized
  mean, with an application to the bootstrap*:
  https://doi.org/10.1093/biomet/78.1.169
- Ronchetti and Welsh (1994), *Empirical Saddlepoint Approximations for
  Multivariate M-Estimators*:
  https://doi.org/10.1111/j.2517-6161.1994.tb01980.x

