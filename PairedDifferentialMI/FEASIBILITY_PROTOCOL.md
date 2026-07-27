# Paired Differential-MI Feasibility Protocol

Protocol fixed before inspecting paired simulation outcomes.

Date: 27 July 2026

## Research Question

Can a deterministic covariance-aware test of

```text
H0: I(X_A;Y_A) = I(X_B;Y_B)
```

provide calibrated inference for positive discrete MI under paired sampling,
including moderately skewed and sparse tables, while being substantially
faster than resampling complete paired units?

This is not a test that either MI is zero.

## Data-Generating Design

Each IID unit is one draw from a joint distribution of
`(X_A,Y_A,X_B,Y_B)`. The two condition-specific table distributions are
constructed to have exact target MI values. A coupling matrix then preserves
both tables exactly while inducing negative, zero, or positive covariance
between their population local-information scores.

This separates three features that must not be confounded:

- equality or inequality of the two population MI values;
- skewness and sampling density of each condition-specific table; and
- dependence caused by pairing.

## Frozen Methods

### Paired Wald-normal

```text
Delta_hat = I_hat_A - I_hat_B
SE_IF = sd[local_A - local_B] / sqrt(n)
Z = Delta_hat / SE_IF
```

The full-support leading MI bias corrections cancel when both conditions
have the same alphabet and sample size, as in this pilot.

### Paired Wald-t

Uses the same statistic and a Student-t reference with `n-1` degrees of
freedom.

### Paired jackknife-t

Computes one delete-one pseudo-value for the MI difference per paired unit,
then applies a one-sample Student-t calculation to those pseudo-values. This
is the candidate nonlinear finite-sample refinement.

### Unpaired Wald-normal

Drops the paired covariance term. It is not a candidate method; it verifies
that the experiment can detect the consequence of ignoring pairing.

### Paired bootstrap-t

Selected anchors resample complete paired units from their empirical joint
distribution. The bootstrap re-estimates the jackknife statistic in every
replicate and recentres at the observed estimate. It is a computational
reference, not finite-sample truth.

Repeated sampling from the known population distribution is the ground truth
for false-positive rate and power.

## Regimes

- Table shapes: `2x2`, `3x3`, and `5x5`.
- Sample sizes: 50 through 1,000.
- Margins: balanced, mildly skewed, and strongly skewed.
- Pairing: negative, zero, and positive local-score covariance.
- Positive MI: 0.05 through 0.15 nats.
- Sparse stress cases: many expected joint counts below 1 or 5.
- Boundary controls: MI 0, 0.002, and 0.005 nats.
- Power controls: MI differences of 0.05 nats.

## Primary Metrics

- false-positive rate at `alpha=0.05` and `0.10`;
- mean absolute false-positive-rate error by regime;
- valid-result rate;
- estimator bias;
- paired versus unpaired standard-error ratio;
- power under unequal MI;
- deterministic and 999-bootstrap runtimes.

The primary candidate for the proceed/no-go decision is paired
jackknife pseudo-value-t. Paired Wald-normal is the frozen simpler baseline;
the report must not select the better-looking method after simulation.

## Pilot Decision Rules

Proceed to a larger validation study only if all of the following hold:

1. In regular positive-MI null scenarios, paired jackknife-t has mean absolute
   5% FPR error at most 0.01 and at least 80% of scenarios fall between 3.5%
   and 6.5%.
2. Paired methods remain calibrated across both signs of pairing while the
   unpaired diagnostic changes in the theoretically expected direction.
3. The jackknife-t refinement improves sparse-regime mean absolute 5% FPR
   error by at least 20% relative to Wald-normal, or Wald-normal is already
   within 0.01 and the refinement does not materially worsen it.
4. Near-independence failures, if present, are visible in diagnostics and
   are not included in the supported claim.
5. The selected deterministic method has sub-millisecond single-test latency
   for the pilot shapes and is at least ten times faster than 999 paired
   bootstrap replicates.

Failure of rule 1 is a no-go for the paired direction in its current form.
Failure of rule 3 means the proposed refinement is not useful, even if the
basic paired Wald test remains a valid baseline.
