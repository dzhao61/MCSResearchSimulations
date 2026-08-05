# Pre-Specified Welch-Satterthwaite Validation Protocol

## Research Question

Does replacing the standard-normal reference in the analytically
bias-corrected differential-MI Wald test with a Welch-Satterthwaite
finite-degrees-of-freedom reference materially improve small-sample
calibration without harming broad regular-case performance?

The test concerns two independent multinomial joint distributions:

```text
H0: I(P) = I(Q), allowing P != Q.
```

Near-independence remains outside the claimed first-order operating regime.

## Frozen Methods

### Existing baseline: `wald_normal`

```text
Delta = [MI_hat(P) - d/(2 n_P)] - [MI_hat(Q) - d/(2 n_Q)]
SE^2  = V_hat(P)/n_P + V_hat(Q)/n_Q
z     = Delta / SE
p     = 2 * Normal.sf(|z|)
```

Here `d = (r-1)(c-1)` and `V_hat` is the empirical influence variance.

### Primary candidate: `welch_reference`

The estimate, standard error, and standardized statistic are identical to
`wald_normal`. Define

```text
a  = V_hat(P)/n_P
b  = V_hat(Q)/n_Q
nu = (a+b)^2 / [a^2/(n_P-1) + b^2/(n_Q-1)]
p  = 2 * StudentT_nu.sf(|z|)
```

Only the reference distribution changes. This is the method used for the
go/no-go decision.

### Sensitivity candidate: `welch_unbiased`

This exploratory variant first treats the empirical influence variances as
population-denominator sample variances:

```text
a_u = V_hat(P)/(n_P-1)
b_u = V_hat(Q)/(n_Q-1)
```

It uses `sqrt(a_u+b_u)` in the statistic and the corresponding
Welch-Satterthwaite degrees of freedom. It is reported separately and cannot
rescue a failed primary candidate.

## Correctness Gates

Before simulation:

- the primary statistic equals the normal Wald statistic exactly;
- finite Student p-values are no smaller than normal p-values at fixed
  statistic;
- equal sample sizes and equal variance contributions give
  `nu = 2(n-1)`;
- swapping groups or relabelling categories does not change the result;
- large sample sizes make the Student and normal p-values converge;
- invalid or zero first-order variances are reported, never coerced;
- every p-value is finite and in `[0,1]` when the calculation is valid.

## Decisive Simulation

All methods use common sampled table pairs.

### Stage A: broad regular grid

- Two independently generated sets of 72 weak-null populations.
- Shapes from `2x2` through `20x20`, including rectangular tables.
- Equal and unequal sample sizes with ratios `1:1`, `1:2`, and `1:4`.
- Target MI values `0.03`, `0.07`, and `0.15` nats.
- Random Dirichlet margins and random interaction structures.
- `5,000` null replicates per population pair.
- Total: 144 scenarios and 720,000 table pairs.

### Stage B: targeted hard grid

- The six frozen design-5 scenarios:
  `2x2`, `2x5`, `3x7`, `4x6`, `5x5`, and `5x10`.
- Sample-size ratio `1:4`, target MI `0.15`, and low density.
- Both independent scenario-generation seeds.
- `20,000` fresh null replicates per scenario.
- Total: 12 scenarios and 240,000 table pairs.
- For each scenario, `1,000` table pairs also receive 999 optimized
  studentized analytic table permutations.

### Stage C: small-sample stress grid

This stage is deliberately outside or near the first-order validity boundary.
It tests whether the correction fails gracefully rather than defining the
main claim.

- Frozen weak-null populations on `2x2`, `2x5`, `3x3`, and `4x6` tables.
- Sample sizes from `20` through `200`, with `1:1` and `1:4` ratios.
- Two independent population-generation seeds.
- `10,000` null replicates per scenario.

### Stage D: power

- The five frozen `3x3` power-curve scenarios.
- MI differences `0.02`, `0.05`, and `0.10`.
- Equal sample sizes `150`, `300`, and `600`.
- `10,000` replicates per scenario.

## Metrics

At alpha `0.10` and `0.05`, report:

- scenario-level rejection rates and Wilson intervals;
- mean and median absolute FPR error;
- proportion of scenarios in the `0.035`-`0.065` band at alpha `0.05`;
- paired changes in rejection decisions;
- effective-df median, range, and lower quantiles;
- 95% interval coverage;
- power and absolute power loss;
- single-pair and vectorized runtime;
- invalid calculation rate.

## Primary Go/No-Go Rule

Adopt `welch_reference` only if all conditions hold:

1. Hard-grid mean absolute FPR error at alpha `0.05` falls by at least `20%`
   relative to `wald_normal`.
2. Hard-grid mean absolute FPR error at alpha `0.10` does not increase.
3. Broad-grid alpha-`0.05` mean absolute FPR error does not increase by more
   than `0.001`.
4. Broad-grid in-band proportion does not fall by more than two percentage
   points.
5. Mean power loss is no more than `0.03` absolute.
6. Valid-result rate is at least `99.5%`.
7. Median single-pair runtime is less than twice the normal Wald runtime and
   remains below `1 ms`.

The result is a no-go if any criterion fails. The stress grid is diagnostic
and cannot overturn the regular/hard decision.

## Interpretation

A go would justify presenting a bias-corrected Welch-type differential-MI
test as the candidate method, followed by theory and a larger external audit.
A no-go would establish that finite Welch degrees of freedom are too small a
change to repair the remaining MI nonlinearity and sparsity error.

