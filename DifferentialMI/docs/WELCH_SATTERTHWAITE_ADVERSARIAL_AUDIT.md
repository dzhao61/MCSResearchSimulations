# Adversarial Audit: Welch-Satterthwaite Differential MI

Audit date: 27 July 2026

## Executive Verdict

The result survives a code and data-leakage audit, but with an important
theoretical qualification.

| Area | Verdict |
|---|---|
| Statistic and p-value implementation | Pass |
| Units, null construction, and reproducibility | Pass |
| RNG separation and conventional data leakage | Pass |
| Fresh-population empirical replication | Pass, small improvement |
| Uniform improvement across regimes | No |
| Classical Welch finite-sample justification | Not established |
| Exact or generally valid sparse-table test | No |
| Use as a prospective conservative baseline | Defensible with warnings |
| Claim of a pre-specified `GO` | False |

The current method computes exactly what it says it computes. Its small
conservative effect is real and reproduced on an untouched population grid.
However, the `n_i-1` component degrees of freedom are borrowed from ordinary
sample variances rather than derived for plug-in MI influence variances.
Accordingly, this is an empirically calibrated Welch-type refinement, not an
exact Welch theorem for MI.

## Findings

### High: Component Degrees of Freedom Are Heuristic

Classical Welch inference combines ordinary sample-variance components whose
chi-square degrees of freedom are known under Gaussian sampling. The current
MI method instead uses

```text
a_hat = V_hat(P) / n_P
b_hat = V_hat(Q) / n_Q
```

where `V_hat` is itself a nonlinear plug-in functional of the empirical
contingency table. The local MI scores change when the table changes. Thus
`n_P-1` and `n_Q-1` are not automatically the sampling degrees of freedom of
these components.

This was checked directly with 50,000 table pairs per representative
population:

| Scenario | Naive total df | Empirical moment df | IF-predicted df |
|---|---:|---:|---:|
| `2x2 d0` | 771.6 | 28.2 | 26.4 |
| `2x2 d5` | 170.8 | 45.4 | 41.5 |
| `2x5 d5` | 183.4 | 76.0 | 63.3 |
| `4x6 d5` | 377.8 | 90.6 | 69.8 |
| `5x5 d2` | 858.0 | 196.3 | 181.1 |

The scale mismatch shows that the current formula is not moment matching the
actual variance estimator. It still converges to the normal reference in the
regular fixed-alphabet limit, so the first-order asymptotic validity claim is
not affected. What is unsupported is the stronger finite-sample Welch
interpretation.

### Medium: Baseline Promotion Was Post Hoc

The frozen validation protocol required at least a 20% hard-grid MAE
reduction. The observed reduction was 7.9%, and the saved metadata correctly
records `NO-GO`.

The later decision to accept a smaller benefit and use Welch prospectively is
an engineering or research-policy amendment after viewing the result. It is
allowed if disclosed, but it cannot be represented as a pre-specified
successful decision.

The original protocol file predates the decisive output by approximately six
minutes on the local filesystem. Because the project is untracked and was not
externally preregistered, that timestamp is supporting evidence rather than an
immutable preregistration record.

### Medium: Hard and Stress Stages Are Not Independent Population Replications

The decisive run contains 1.22 million null table pairs but only 144 unique
broad population pairs. The hard grid resamples 12 populations already in the
broad grid, and the stress grid changes sample sizes for populations drawn
from that same generated grid.

Fresh table samples make the Monte Carlo rejection rates precise. They do not
create new population regimes. Claims should report both the number of table
pairs and the number of unique population pairs.

### Medium: Hard-Grid Improvement Is Partly Structural

All 12 hard scenarios were liberal under normal Wald. At a fixed statistic,
a finite-df Student p-value is never smaller than its normal p-value.
Therefore Welch can only remove normal-Wald rejections.

On this deliberately liberal subset, reduced FPR error is expected. The broad
grid is more diagnostic:

```text
improved scenarios: 40
worsened scenarios: 29
ties:               75
mean MAE gain:       0.000103
```

The effect is positive on average but not universal.

### Low: Balanced-Like Scenarios Can Become Slightly Worse

In the new holdout's approximately balanced `design 0` stratum, normal Wald
was already conservative:

```text
normal MAE: 0.005208
Welch MAE:  0.005350
```

The degradation is small, but this prevents a claim that Welch always
improves calibration. Its value is primarily in mildly liberal regimes.

### Low: Invalid-Case FPR Is Conditional on Computability

Broad and hard runs had 100% valid calculations. The stress run marked 34
degenerate cases invalid and excluded them from FPR denominators. That is a
reasonable reporting choice, but stress FPR is conditional on a computable
first-order statistic. Software must return an explicit invalid result rather
than interpreting it as non-significance.

## Leakage and Look-Ahead Audit

### Checks That Passed

- Population-generation seeds are distinct from table-simulation seeds.
- Each of the 182 decisive null jobs has a unique simulation seed.
- Permutation RNGs use separately derived seeds.
- Power jobs receive separate spawned streams after the null jobs.
- Broad and hard stages reuse populations but use fresh table streams.
- Methods receive the same table pairs, which is correct paired experimental
  design rather than leakage.
- The method has no fitted hyperparameter, learned threshold, or training
  phase that could consume validation outcomes.
- The weak null is numerically exact: maximum saved
  `abs(I(P)-I(Q)) = 9.3e-14`.
- Recalculation from `null_replicates.csv.gz` exactly reproduces the published
  broad, hard, and stress summaries.
- Repeating the fresh holdout with the same seeds produced byte-identical
  scenario output.

### Look-Ahead That Must Be Disclosed

- The decision to promote Welch after a frozen `NO-GO` is post hoc.
- The hard grid targets a design known to be difficult and is not a neutral
  sample of regimes.
- The current audit derived an influence-based component-df alternative after
  viewing the naive-df discrepancy. That alternative must be tested on another
  untouched seed set before any selection decision.

No conventional train/test contamination or accidental RNG reuse was found.

## Fresh Holdout

The audit runner fixed new population, simulation, and bootstrap seeds before
execution. It generated populations not present in the decisive experiment.

| Stage | Population pairs | Tables per pair | Normal MAE | Welch MAE | Mean gain, 95% scenario bootstrap |
|---|---:|---:|---:|---:|---:|
| Fresh weak-null broad | 72 | 10,000 | 0.004792 | 0.004582 | 0.000210 [0.000090, 0.000344] |
| Frozen hard design | 6 | 10,000 | 0.009083 | 0.007800 | 0.001283 [0.000917, 0.001650] |
| Fresh strong null | 72 | 5,000 | 0.005142 | 0.004958 | 0.000183 [0.000064, 0.000322] |

All calculations were valid. At alpha `0.05`, the weak-null broad holdout had
225 normal-only rejections and zero Welch-only rejections, as required by the
nested conservative reference.

This is meaningful independent support for the direction of the effect. Its
magnitude remains small.

## Mathematical Reconstruction

For positive fixed support and MI away from zero, the estimator uses

```text
Delta_BC = [MI_hat(P) - d/(2n_P)] - [MI_hat(Q) - d/(2n_Q)]
SE^2 = V_hat(P)/n_P + V_hat(Q)/n_Q
T = Delta_BC / SE
```

with natural logarithms and `d=(r-1)(c-1)`. The code then sets

```text
nu = (a+b)^2 / [a^2/(n_P-1) + b^2/(n_Q-1)]
p = 2 * StudentT_nu.sf(abs(T)).
```

A new independent hand calculation reproduces the implementation to at least
12 decimal places.

For a theory-backed component-df candidate, let

```text
l_ij = log[p_ij/(p_i+ p_+j)]
mu = E[l]
M2 = E[l^2]
r_i = E[l | X=i]
c_j = E[l | Y=j].
```

The contamination influence function of `V(P)=Var(l)` is

```text
IF_V(i,j) =
    l_ij^2 - M2
    + 2(l_ij - r_i - c_j + mu)
    - 2mu(l_ij - mu).
```

Finite-difference contamination checks match this expression. If
`tau^2 = Var_P(IF_V)`, first-order moment matching suggests the component df

```text
nu_V approximately 2 n V(P)^2 / tau^2.
```

This prediction tracks the empirical component-df audit far better than
`n-1`. It is a promising next candidate, not yet a validated replacement.
The strong observed correlation between `Delta_BC` and its estimated variance
in skewed regimes, as high as 0.84 in the audit, also means matching the
denominator alone may not produce an exact t law.

## Code Audit

The production implementation passed:

- direct hand calculation of MI, bias, variance, df, statistic, and p-value;
- group-swap and row/column relabelling invariance;
- scalar versus aggregate API parity;
- main-package versus isolated implementation parity;
- large-sample convergence to the normal reference;
- explicit rejection of malformed and one-observation inputs;
- explicit invalid output at first-order degeneracy;
- p-value bounds and the expected `p_Welch >= p_Normal` ordering; and
- compilation and all project regression tests.

No unit-conversion issue was found. `plugin_mi()` uses natural logarithms, so
MI, bias correction, variance, and the test statistic are all consistently in
nats.

The full-support `d/(2n)` correction intentionally uses declared alphabet
dimensions even when an empirical row or column is empty. This is correct for
the stated fixed-positive-population-support asymptotics but can overcorrect
sparse finite samples. It is a scope limitation, not a hidden coding error.

## Defensible Claim

Safe:

> We propose and systematically evaluate a Welch-Satterthwaite-inspired
> finite-df reference for bias-corrected influence-function inference on the
> difference between two independent discrete mutual information values. It
> is asymptotically equivalent to the normal Wald test and produced a small,
> reproducible conservative calibration improvement in the tested regular
> and liberal regimes.

Not safe:

- exact Welch test for MI;
- proven finite-sample type-I error control;
- uniformly better than normal Wald;
- a solution to independence, structural zeros, or sparse support;
- a pre-specified `GO`; or
- 1.22 million independent distributional regimes.

## Recommendation

The current method may remain the prospective software baseline if the goal
is a cheap, mildly conservative default. Every thesis result should continue
to report the normal comparator.

For a stronger methodological contribution, the next experiment should
freeze the derived `IF_V` component-df formula, test it on a new untouched
population grid, and compare it with both current Welch and normal Wald.
External timestamping or preregistration should occur before that run.

## Reproducible Artifacts

- Holdout runner:
  `WelchSatterthwaiteMI/experiments/run_adversarial_holdout.py`
- Holdout summaries:
  `WelchSatterthwaiteMI/results/adversarial_holdout/`
- Variance-component audit:
  `WelchSatterthwaiteMI/experiments/audit_variance_components.py`
- Variance-component results:
  `WelchSatterthwaiteMI/results/adversarial_holdout/variance_component_audit.csv`
- Original protocol:
  `WelchSatterthwaiteMI/docs/history/VALIDATION_PROTOCOL.md`
- Original immutable conclusion:
  `WelchSatterthwaiteMI/docs/history/FINAL_ASSESSMENT.md`

## Primary Statistical Sources

- [Satterthwaite (1946), *An Approximate Distribution of Estimates of Variance Components*](https://doi.org/10.2307/3002019)
- [Welch (1947), *The Generalization of Student's Problem When Several Different Population Variances Are Involved*](https://doi.org/10.1093/biomet/34.1-2.28)
- [Moddemeijer (1989), *On Estimation of Entropy and Mutual Information of Continuous Distributions*](https://doi.org/10.1016/0165-1684(89)90132-1)
- [Mora and Ruiz-Castillo (2009), *The Statistical Properties of the Mutual Information Index of Multigroup Segregation*](https://www.researchgate.net/publication/4724169_The_statistical_properties_of_the_Mutual_Information_index_of_multigroup_segregation)
