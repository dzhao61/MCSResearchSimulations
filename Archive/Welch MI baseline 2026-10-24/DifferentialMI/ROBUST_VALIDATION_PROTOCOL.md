# Robust Regular-Case Validation Protocol

## Objective

Determine whether deterministic bias-corrected Wald inference is a reliable,
fast method for comparing discrete mutual information across two
heterogeneous populations in the regular, non-near-independent regime.

The experiment must distinguish three questions:

1. Does raw permutation fail under `P != Q` but `I(P) = I(Q)`?
2. Does first-order bias correction fix deterministic Wald calibration?
3. Does the jackknife improve materially on the simpler classical analytic
   correction?

This protocol was fixed before inspecting the new randomized results.

## Methods

All p-values are two-sided.

| Method | Role |
|---|---|
| Raw plug-in Wald | Uncorrected deterministic baseline |
| Analytic-bias-corrected Wald | Classical first-order correction |
| Jackknife-Wald | Candidate finite-sample deterministic method |
| Raw plug-in permutation | Deliberately weak-null-invalid baseline |
| Studentized analytic permutation | Resampling reference |
| Studentized jackknife permutation | More expensive resampling reference |

The variance estimator is the empirical variance of the MI log density ratio.
The analytic MI correction uses the declared full-support dimensions:

```text
I_BC = I_plugin - (r-1)(c-1)/(2n).
```

## Distribution Generator

Each weak-null scenario contains two independently generated positive joint
probability tables with:

- exactly equal population MI;
- different marginal distributions;
- different randomized interaction patterns;
- no population structural zeros;
- target MI at least `0.03` nats.

Margins are drawn from symmetric Dirichlet distributions over a broad range
of concentration parameters. Interaction matrices are random, double
centered, and scaled. Iterative proportional fitting imposes the requested
margins, and scalar root solving chooses the interaction strength that
achieves the common target MI.

Scenarios are generated once from a fixed seed and their complete probability
tables are saved. Failed or infeasible draws are retried and counted.

## Broad Deterministic Screen

- Shapes: square and rectangular tables from `2x2` through `20x20`.
- Sample-size ratios: `1:1`, `1:2`, and `1:4`.
- Margins: Dirichlet concentrations from approximately uniform to strongly
  heterogeneous.
- Common MI targets: `0.03`, `0.07`, and `0.15` nats, subject to feasibility.
- At least 60 accepted randomized weak-null scenarios.
- At least 3,000 multinomial replicate pairs per scenario.

The deterministic methods are evaluated for:

- rejection rates at `alpha = 0.10` and `0.05`;
- Wilson confidence intervals for rejection rates;
- 95% confidence-interval coverage;
- estimator bias and root mean squared error;
- invalid or zero standard-error frequency;
- runtime.

## Permutation Anchors

Before the broad screen is inspected, select at least 12 scenario positions
spanning:

- small, medium, and large tables;
- equal and unequal sample sizes;
- balanced-like and skewed margins;
- low, medium, and high expected occupancy.

For each anchor:

- use at least 1,000 simulated sample pairs;
- use 999 table-level label permutations per pair;
- compare raw, studentized analytic, and studentized jackknife methods;
- save per-replicate p-values.

The table-level multivariate-hypergeometric draw is exactly the count-table
version of permuting individual group labels conditional on pooled counts.

Post-hoc reruns of the worst deterministic cases are allowed, but must be
labeled as adversarial follow-ups rather than pre-specified evidence.

## Observable Regime Diagnostics

Population labels such as "regular" are not enough. Save these observable
sample diagnostics for both groups:

- proportion of zero cells;
- minimum nonzero expected count under empirical independence;
- proportion of empirical-independence expected counts below 1 and below 5;
- effective row and column counts;
- empirical influence variance;
- absolute jackknife-minus-analytic correction;
- standardized correction size relative to the estimated standard error.

Population diagnostics are also saved for scientific interpretation, but
they cannot be used as a deployment rule.

For permutation methods, also save the pooled-mixture MI and influence
variance. Opposite dependence directions can make the pooled mixture nearly
independent even when both original populations are regular, invalidating
the first-order studentized permutation reference without invalidating the
deterministic two-sample statistic.

## Pre-Specified Evaluation

Near-independent scenarios with population MI below `0.03` are excluded from
this phase.

For supported regular scenarios, the primary target at `alpha = 0.05` is:

- mean absolute calibration error no greater than `0.008`;
- at least 90% of scenarios have rejection rate in `[0.035, 0.065]`;
- aggregate 95% interval coverage in `[0.935, 0.965]`;
- no nonfinite p-values or standard errors;
- deterministic inference materially faster than 999 permutations.

The jackknife is preferred over analytic correction only if it has a
meaningful and reproducible calibration or coverage advantage. Otherwise,
the analytic correction wins on simplicity.

## Interpretation Rules

- A Monte Carlo rate outside `[0.035, 0.065]` is a practical warning, not by
  itself proof of failure. Wilson intervals and repeated anchors must be
  inspected.
- Results are stratified by observable sparsity diagnostics; averaging can
  conceal incompatible regimes.
- Random scenario generation does not turn the screen into a formal
  distribution-free proof.
- The experiment validates a fixed-alphabet finite-sample operating regime.
  It does not establish growing-alphabet asymptotics.
