# Frozen Validation Protocol: MI-Specific Influence Degrees of Freedom

Protocol frozen: 27 July 2026

This protocol was written before implementing the candidate and before
running any candidate calibration result.

## Methods

All three methods use the same bias-corrected estimate, standard error, and
standardized statistic.

### `wald_normal`

Uses the standard-normal reference.

### `welch_n_minus_1`

Uses the current Welch-inspired reference with component degrees of freedom
`n_P-1` and `n_Q-1`.

### `if_satterthwaite`

Uses the MI-specific variance-functional influence calculation derived in
`DERIVATION.md`:

```text
nu_i = 2 n_i V_i^2 / Var(IF_V_i)

nu = (a+b)^2 / [a^2/nu_P + b^2/nu_Q].
```

This is the only primary candidate. No constants will be fitted from the
validation results.

## Frozen Seeds

```text
population seeds: 73105913, 84207631
simulation seed:  52611907
runtime seed:     31845071
bootstrap seed:   22719043
```

These seeds have not been used by the original Welch experiment or its
adversarial holdout.

## Correctness Gates

Before the decisive run:

- the analytic `IF_V` matches contamination finite differences;
- `E_P[IF_V]=0` numerically;
- scalar and vectorized calculations agree;
- group swapping and category relabelling are invariant;
- the estimate, standard error, and statistic equal the frozen normal method;
- all valid p-values lie in `[0,1]`;
- large samples converge to the normal reference;
- exact independence is marked first-order invalid; and
- malformed or undersized tables are rejected.

## Decisive Experiment

### Broad Weak Null

- Two new independently generated grids of 72 populations.
- Shapes from `2x2` through `20x20`.
- Balanced-like through heterogeneous margins.
- Equal and unequal sample sizes.
- Exactly equal population MI with `P != Q`.
- 5,000 fresh table pairs per population.
- 144 unique population pairs and 720,000 table pairs.

### Frozen Hard Design

- Design 5 for `2x2`, `2x5`, `3x7`, `4x6`, `5x5`, and `5x10`.
- Both population seeds.
- 20,000 fresh table pairs per population.
- 12 population pairs and 240,000 table pairs.
- These populations are a subset of the broad grid; only the table samples
  are new.

### Strong Null

- Set `Q=P` for every broad population while retaining the configured sample
  sizes.
- 5,000 fresh table pairs for each of 144 populations.
- 720,000 table pairs.

### Small-Sample Stress Diagnostic

- The previously defined 13 sample-size configurations.
- Both new population seeds.
- 10,000 fresh table pairs per configuration.
- This stage is outside or near the regular first-order boundary and cannot
  rescue a failed regular-grid decision.

### Power

- Five frozen `3x3` power scenarios.
- 10,000 fresh table pairs per scenario.
- Compare rejection rates at alpha `0.05`.

## Primary Metrics

At alpha `0.05` and `0.10`:

- scenario-level FPR and Wilson interval;
- mean absolute FPR error across populations;
- paired scenario-level MAE change;
- balanced-like design-0 MAE;
- hard-design MAE;
- strong-null MAE;
- valid-result rate;
- interval coverage;
- power and power loss;
- scalar and vectorized runtime; and
- empirical variance-component df versus predicted component df.

Both population-pair counts and table-pair counts will be reported.

## Frozen Adoption Criteria

Adopt `if_satterthwaite` only if all criteria hold:

1. Hard-design alpha-`0.05` MAE is at least 10% lower than
   `welch_n_minus_1`.
2. Hard-design alpha-`0.10` MAE does not increase.
3. Broad alpha-`0.05` MAE is no more than `0.00025` above
   `welch_n_minus_1`.
4. Balanced-like design-0 alpha-`0.05` MAE is no more than `0.00050` above
   `wald_normal`.
5. Strong-null alpha-`0.05` MAE is no more than `0.00025` above
   `welch_n_minus_1`.
6. Mean power loss relative to `welch_n_minus_1` is no more than `0.01`.
7. Broad, hard, and strong-null valid-result rates are at least 99.5%.
8. Median scalar runtime is below three times normal Wald and below 1 ms.
9. Across the frozen variance-component audit cases, the median absolute
   log-ratio error of predicted versus empirical total df is at least 50%
   lower than the `n_i-1` formula.

The result is `GO` only if every criterion passes. The criteria will not be
changed after the run.

## Interpretation Rule

A `GO` supports adopting the influence-matched df as the prospective
reference, followed by external replication. A `NO-GO` still leaves the
derived variance-functional influence function as a valid theoretical and
diagnostic contribution.

