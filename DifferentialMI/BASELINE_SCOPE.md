# Fixed Baseline and Scope

Date fixed: 25 July 2026

## Scientific Question

Given two independent samples of the same aligned categorical variables
`(X,Y)`, test

```text
H0: I_P(X;Y) = I_Q(X;Y)
```

without requiring the complete joint distributions `P` and `Q` to be equal.
The estimand is the signed difference

```text
Delta = I(P) - I(Q)
```

in nats.

## Primary Baseline

The fixed baseline is analytic-bias-corrected influence-function Wald
inference:

```text
I_BC(P_hat) = I(P_hat) - (r-1)(c-1)/(2n)

Delta_BC = I_BC(P_hat) - I_BC(Q_hat)

SE = sqrt{V_hat(P)/n + V_hat(Q)/m}

Z = Delta_BC / SE

p = 2 Phi(-abs(Z)).
```

Here `V_hat` is the empirical variance of the local log density ratio

```text
log[p_hat_ij/(p_hat_i+ p_hat_+j)].
```

The implementation is `differential_mi.analytic_wald_test`.

## In Scope

- Two independent samples.
- Discrete variables with fixed finite alphabet sizes.
- The same aligned row and column categories in both populations.
- Positive population support on the declared alphabet.
- Population MI and influence variance sufficiently away from zero for
  first-order asymptotics.
- Square or rectangular contingency tables.
- Equal or unequal sample sizes.
- Balanced or skewed marginal distributions.
- Estimation, two-sided testing, and confidence intervals for `Delta`.

## Out of Scope

- Exact or near independence.
- Alphabet dimensions increasing asymptotically with sample size.
- Structural zeros or unknown support.
- Paired, clustered, longitudinal, or time-series samples.
- Conditional MI, transfer entropy, and continuous-variable MI.
- Automatic routing to a fallback method.

These exclusions must appear in every thesis claim and software description.

## Fixed Comparators

- Uncorrected plug-in Wald, to expose finite-sample bias.
- Delete-one jackknife-Wald, to test whether generic bias correction adds
  value.
- Raw table-label permutation, to demonstrate weak-null failure.
- Studentized analytic table-label permutation, as the regular resampling
  reference.

JIDT's standard significance test is not a direct comparator because it tests
one-population independence rather than equality of two population MI values.
JIDT may be used to verify MI calculations.

## Diagnostics, Not Validity Guarantees

The API reports:

- zero-cell fractions;
- empirical-independence expected-count fractions below 1 and 5;
- minimum empirical-independence expected counts;
- empirical influence variances;
- the bias-correction difference relative to the standard error.

These diagnostics describe the observed table. They are not currently
claimed to form a proven validity rule.

`numerically_computable` reports only whether a finite positive empirical
standard error and test statistic could be calculated. The legacy
`valid_first_order_calculation` field is retained for compatibility and has
the same limited meaning. Neither field can verify positive population
support, distance from independence, fixed-alphabet asymptotics, or
independence of observations from one table pair.

## Frozen Baseline Rule

The baseline formulas, assumptions, and primary metrics will not be changed
after inspecting refinement results. New corrections must be compared
against this frozen method, not substituted into its historical results.
