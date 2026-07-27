# Frozen Validation Protocol: Joint Studentized Edgeworth MI

Protocol frozen: 27 July 2026

This protocol was written before implementing the candidate and before
running any candidate calibration results.

## Methods

All methods use the same bias-corrected MI difference and first-order
influence standard error.

- `wald_normal`: standard-normal reference.
- `welch_n_minus_1`: existing `n-1` Welch-inspired reference.
- `if_satterthwaite`: previous MI-specific denominator-df Student reference.
- `joint_edgeworth`: new direct approximation to the studentized statistic.

No coefficient, threshold, or switch is fitted from validation outcomes.
The Edgeworth validity guardrails are fixed in `DERIVATION.md`.

## Fresh Seeds

```text
population seeds: 91370211, 47628903
simulation seed:  68314527
runtime seed:     55290811
bootstrap seed:   30714983
```

These seeds differ from all prior Welch and influence-df decisive runs.

## Correctness Gates

Before the decisive run:

- the MI and variance influence functions match contamination derivatives;
- all influence functions have probability-weighted mean zero;
- the analytic `m3` and `g` equal direct weighted moments;
- the ordinary studentized-mean special case reduces to
  `lambda(1+2x^2)/6`;
- group swapping preserves the two-sided p-value;
- category relabelling preserves all inference;
- scalar and vectorized APIs agree;
- the estimate, standard error, normal, naive-Welch, and influence-df
  comparators exactly match their frozen implementations;
- equal distributions with equal sample sizes give
  `lambda=c=0` and exactly recover the normal p-value;
- large sample scaling converges to normal;
- malformed and first-order-degenerate inputs are rejected; and
- valid p-values are finite and in `[0,1]`.

## Decisive Experiment

### Broad Weak Null

- Two independently generated 72-population grids.
- Shapes from `2x2` through `20x20`.
- Balanced-like through heterogeneous margins.
- Equal and unequal sample sizes.
- Exactly equal population MI with `P != Q`.
- 5,000 table pairs per population.
- 144 populations and 720,000 table pairs.

### Frozen Hard Design

- Design 5 for `2x2`, `2x5`, `3x7`, `4x6`, `5x5`, and `5x10`.
- Both population seeds.
- 20,000 independently sampled table pairs per population.
- 12 populations and 240,000 table pairs.

### Strong Null

- Set `Q=P` for all 144 broad populations while retaining sample sizes.
- 5,000 table pairs per population.
- 720,000 table pairs.

### Small-Sample Stress Diagnostic

- The frozen 13 sample-size configurations for both population seeds.
- 10,000 table pairs per configuration.
- 260,000 table pairs.
- This stage cannot rescue a failed regular-grid decision.

### Power

- Five frozen `3x3` power scenarios.
- 10,000 table pairs per scenario.

## Primary Metrics

At alpha `0.05` and `0.10`:

- scenario-level FPR and Wilson interval;
- mean absolute FPR error;
- paired scenario-level MAE change and bootstrap interval;
- balanced design-0, hard, strong-null, and stress summaries;
- valid Edgeworth rate;
- interval coverage;
- power and power loss;
- scalar and vectorized runtime; and
- empirical versus influence-predicted third cumulant and
  numerator/denominator covariance diagnostics.

## Frozen Adoption Criteria

Adopt `joint_edgeworth` only if every criterion holds:

1. Hard alpha-`0.05` MAE is at least 10% lower than `welch_n_minus_1`.
2. Hard alpha-`0.10` MAE does not exceed `welch_n_minus_1`.
3. Hard alpha-`0.05` MAE is no more than `0.00050` above
   `if_satterthwaite`.
4. Broad alpha-`0.05` MAE is no more than `0.00025` above
   `welch_n_minus_1`.
5. Balanced design-0 alpha-`0.05` MAE is no more than `0.00050` above
   `wald_normal`.
6. Strong-null alpha-`0.05` MAE is no more than `0.00025` above
   `welch_n_minus_1`.
7. Mean power loss relative to `welch_n_minus_1` is no more than `0.01`.
8. Broad, hard, and strong-null valid-result rates are at least 99.5%.
9. Median scalar runtime is below three times normal Wald and below 1 ms.

The decision is `GO` only if all nine criteria pass. Criteria will not be
changed after the run.

## Interpretation

A `GO` supports external replication before adoption. A `NO-GO` distinguishes
between:

- failed cumulant estimation;
- locally invalid Edgeworth behavior;
- inadequate first-order skew correction; and
- remaining symmetric-tail or bias error requiring a full second-order
  expansion.
