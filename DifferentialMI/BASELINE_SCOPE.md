# Baseline and Scope

Date fixed: 25 July 2026
Prospective baseline amendment: 27 July 2026

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

## Prospective Primary Baseline

For experiments initiated after the amendment date, the primary deterministic
baseline is analytic-bias-corrected influence-function inference with a
Welch-Satterthwaite reference:

```text
I_BC(P_hat) = I(P_hat) - (r-1)(c-1)/(2n)

Delta_BC = I_BC(P_hat) - I_BC(Q_hat)

a = V_hat(P)/n
b = V_hat(Q)/m

SE = sqrt{a + b}

T = Delta_BC / SE

nu = (a+b)^2 / [a^2/(n-1) + b^2/(m-1)]

p_primary = 2 Pr(t_nu >= abs(T)).
```

Here `V_hat` is the empirical variance of the local log density ratio

```text
log[p_hat_ij/(p_hat_i+ p_hat_+j)].
```

The implementation is `differential_mi.welch_satterthwaite_test`.

This changes only the reference distribution and confidence-interval critical
value. It does not change the MI estimate, bias correction, influence variance,
standard error, statistic, assumptions, or failure boundary.

This prospective designation is a post-protocol engineering amendment. The
original pre-specified Welch experiment returned `NO-GO` because the hard-grid
improvement did not reach its deliberately high 20% materiality threshold.
The amendment accepts a smaller improvement as useful; it must not be described
as the original pre-specified decision.

An adversarial holdout using 72 newly generated weak-null populations later
confirmed the direction of the effect without reusing the original population
pairs. This supports prospective use but does not turn the reference into an
exact finite-sample test.

## Historical Frozen Baseline

Experiments frozen or completed before 27 July 2026 used the same statistic
with the standard normal reference:

```text
p_normal = 2 Phi(-abs(T)).
```

Those saved results remain valid historical comparisons and must not be
relabeled as Welch results. The implementation is
`differential_mi.analytic_wald_test`, and it remains a required comparator in
all future validation.

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

- Analytic-bias-corrected normal Wald, the historical frozen baseline.
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

## Baseline Amendment Rule

The original normal baseline remains frozen for all experiments designed
before the amendment date. The Welch-Satterthwaite refinement becomes the
prospective primary baseline because the original validation showed a small
calibration improvement at negligible cost and a fresh population-grid
holdout independently confirmed its direction. This is a transparent post-hoc
change to the required improvement threshold, not a retrospective `GO`.

Future corrections must be compared against both the prospective Welch
baseline and the historical normal comparator. No historical CSV, report, or
acceptance decision may be rewritten or relabeled.
