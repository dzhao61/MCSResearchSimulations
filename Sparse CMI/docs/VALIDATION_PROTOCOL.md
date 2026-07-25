# Validation Protocol

## Hypothesis under test

Conditioning on every observed `(n_z, r_z, s_z)` turns binary CMI into a sum
of independent finite-support random variables. Exact conditional cumulants
may therefore make a normal or higher-order approximation more accurate than
the usual chi-square approximation in the many-sparse-strata regime.

The conditional construction itself is classical. The empirical question is
whether the approximation is accurate and useful enough to support the narrow
CMI-specific thesis described in the handoff.

## Reference hierarchy

1. Numerical exact convolution, where state count is manageable.
2. Direct independent hypergeometric sampling for each fixed stratum.
3. Literal within-stratum label permutation as an equivalence/runtime check.

Direct hypergeometric sampling and label permutation induce the same
fixed-margin null. They are separate implementations to avoid mistaking shared
code for independent validation.

## Predeclared regimes

The main grid varies:

- number of strata: 5, 10, 20, 50, 100;
- stratum size: 3, 5, 10, 20, 30;
- balanced, singly skewed, jointly skewed, and opposing margins;
- homogeneous and heterogeneous strata;
- only 2, 3, 5, or 10 informative strata;
- a dominant-stratum adversarial family.

The full grid has more than 100 fixed-margin configurations. It is not tuned
after seeing approximation performance.

## Methods

- chi-square with nominal `K` degrees of freedom;
- chi-square with the observed informative-stratum count;
- exact-moment normal;
- first-order Edgeworth;
- Cornish-Fisher critical values;
- exact or conditional Monte Carlo reference.

## Primary metrics

At alpha 0.05, 0.01, and 0.001:

- rejection probability;
- absolute error relative to the exact conditional test's attainable size;
- absolute error relative to nominal alpha;
- mean absolute p-value error;
- maximum p-value error in the upper 10% tail;
- monotonicity of reported p-values.

## Diagnostics

- Lyapunov/Berry-Esseen ratio;
- maximum variance share;
- aggregate skewness;
- number of informative strata;
- total variance;
- fraction of expected cell counts below 1 and below 5.

## Decision rule

The first-stage report labels the result:

- `PROCEED`: centring/scaling beats informative-df chi-square broadly in sparse
  regimes, skewness correction broadly helps, diagnostics predict failures,
  and moment calculation is materially faster than 1,000 permutations.
- `NARROW_OR_REVISE`: the exact-cumulant normal method is useful, but the
  proposed higher-order correction or diagnostic certificate is not yet
  defensible.
- `PIVOT`: exact-moment methods do not materially improve the target regime or
  remain badly calibrated in its important upper tails.

Novelty is a separate gate and is not inferred from simulation results.

