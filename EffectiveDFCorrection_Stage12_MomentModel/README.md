# Current Method: Moment-Based Null Approximation

This method gives a cheap approximation to the null distribution of discrete
mutual information without bootstrapping every new dataset.

We work with the statistic:

```text
T = 2 N I_hat(X; Y)
```

Under the usual large-sample independence test, `T` is compared to:

```text
chi2(nu0)
nu0 = (kx - 1)(ky - 1)
```

The problem is that this standard chi-square null is inaccurate when the table
is sparse. The current method fixes this by predicting the null mean and
variance first.

## Basic Idea

Instead of directly guessing an effective degrees of freedom, we estimate:

```text
mu     = E[T under independence]
sigma2 = Var[T under independence]
```

Then we convert those moments into a scaled chi-square approximation:

```text
T approx a * chi2(nu_eff)

a      = sigma2 / (2 mu)
nu_eff = 2 mu^2 / sigma2
```

So the main job is: predict `mu` and `sigma2` cheaply.

## What We Calculate

Given marginal probabilities:

```text
p_i = P(X = i)
q_j = P(Y = j)
```

we form the independence null cell probabilities:

```text
pi_ij = p_i q_j
lambda_ij = N pi_ij
```

The method computes two kinds of information.

## 1. Bartlett Moment Core

This is the regular dense-table correction:

```text
nu0 = (kx - 1)(ky - 1)

B = ((sum_i 1/p_i - 1) (sum_j 1/q_j - 1)) / 6

mu_bartlett     = nu0 + B / N
sigma2_bartlett = 2 nu0 + 4 B / N
```

This part is analytic and cheap.

It works best when expected cell counts are not too small.

## 2. Sparse Occupancy Correction

Sparse tables behave differently because many cells are empty or have only one
sample. So we compute occupancy descriptors from `lambda_ij`.

Important examples:

```text
expected zero cells
  = sum_ij exp(-lambda_ij)

expected singleton cells
  = sum_ij lambda_ij exp(-lambda_ij)

expected doubleton cells
  = sum_ij 0.5 lambda_ij^2 exp(-lambda_ij)
```

We also compute descriptors like:

```text
fraction of cells with lambda_ij < 1
fraction of cells with lambda_ij < 5
collision probability = sum_ij pi_ij^2
effective Simpson support = 1 / sum_ij pi_ij^2
```

These tell us how sparse or collision-heavy the null table is.

## Moment Model

Stage12 fits residual corrections:

```text
log(mu / mu_bartlett)
log(sigma2 / sigma2_bartlett)
```

So prediction works like:

```text
mu_hat     = mu_bartlett     * exp(predicted log mean residual)
sigma2_hat = sigma2_bartlett * exp(predicted log variance residual)
```

Then:

```text
a_hat      = sigma2_hat / (2 mu_hat)
nu_eff_hat = 2 mu_hat^2 / sigma2_hat
```

Finally:

```text
T approx a_hat * chi2(nu_eff_hat)
```

This gives approximate thresholds and p-values:

```text
p_value = 1 - chi2_cdf(T_observed / a_hat, df = nu_eff_hat)
```

## How To Use It On A Dataset

For observed samples `x` and `y`:

1. Count categories in `x` and `y`.
2. Estimate marginals:

```text
p_i = count_i(x) / N
q_j = count_j(y) / N
```

3. Compute `T = 2N I_hat(x; y)`.
4. Compute Bartlett and occupancy descriptors from `p_i`, `q_j`, and `N`.
5. Use the Stage12 coefficients to predict `mu_hat` and `sigma2_hat`.
6. Convert them to `a_hat` and `nu_eff_hat`.
7. Compute p-value or critical thresholds from `a_hat * chi2(nu_eff_hat)`.

## What The Validation Says

Stage12 trained on large vectorized simulations.

Stage13 then tested the same coefficients using JIDT-generated null samples on
new shapes, rectangular alphabets, and sparse regimes.

In the 2000-repeat JIDT validation run:

```text
mu prediction:
  median predicted / observed = 1.004
  within 10% = 100.0%

sigma2 prediction:
  median predicted / observed = 0.992
  within 10% = 96.6%

q95 threshold:
  Stage12 within 10% of JIDT empirical q95 = 100.0%

q99 threshold:
  Stage12 within 10% of JIDT empirical q99 = 100.0%
```

This suggests the method is robust as a product-null approximation.

## Important Caveats

This currently approximates the product-multinomial null:

```text
X ~ p
Y ~ q
X independent of Y
```

This is not exactly the same as a fixed-marginal permutation null. In many cases
they are close, but they are conceptually different.

Also, the method needs a support rule. If a category has true probability zero,
it should not be included in `p_i` or `q_j`. For real data, the simplest current
rule is observed support only.

## Current Files

Main model:

```text
EffectiveDFCorrection_Stage12_MomentModel/moment_model.py
```

Exact descriptor enrichment:

```text
EffectiveDFCorrection_Stage12_MomentModel/enrich_exact_descriptors.py
```

JIDT validation:

```text
EffectiveDFCorrection_Stage13_JIDTValidation/jidt_moment_validation.py
```

Main takeaway:

```text
Predict moments first. Then derive a and nu_eff.
The sparse correction is mostly explained by expected zeros, singletons,
doubletons, and collision geometry.
```
