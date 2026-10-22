# Pre-Specified Experiment Protocol

Status: written before simulation results were inspected

Date: 25 July 2026

## 1. Decision

The experiment asks whether this is a defensible thesis direction:

> Develop valid two-sample inference for a difference in discrete mutual
> information when the populations need not have the same full distribution.

The parameter is

```text
Delta_I = I_P(X;Y) - I_Q(X;Y).
```

The null hypothesis is `Delta_I = 0`. A test of `P = Q` answers a different and
stronger question.

## 2. Claims Tested

### Claim A: naive permutation has a real target-null problem

Ordinary group-label permutation is finite-sample exact when `P = Q`. It is not
generally exact for the weaker null `I(P) = I(Q)`. The first experiment must
construct `P != Q` with equal MI and show whether this difference matters in
practice.

### Claim B: studentization repairs regular weak-null calibration

For a positive discrete joint distribution away from independence, MI has
influence function

```text
IF_P(i,j) = log[p_ij / (p_i. p_.j)] - I(P).
```

The estimated standard error of the difference is

```text
SE = sqrt(Var_P(IF_P) / n_P + Var_Q(IF_Q) / n_Q).
```

The deterministic Wald statistic and the studentized permutation statistic use
this standard error. The test is whether they are calibrated in finite samples,
not merely whether asymptotic theory exists.

### Claim C: the method has an honest operating regime

At independence, the first derivative of MI degenerates. Sparse empirical
tables also lie near the probability-simplex boundary. The experiments must
identify where the first-order method stops being reliable.

## 3. Data-Generating Distributions

Joint distributions are generated from prescribed row and column margins using
the positive log-linear family

```text
p_ij(lambda) = a_i b_j exp(lambda s_i t_j),
```

where iterative proportional fitting chooses `a_i` and `b_j` to recover the
requested margins exactly. A root solver chooses `lambda` to achieve a requested
population MI. This permits two visibly different distributions to have equal
MI to numerical tolerance.

Marginal regimes are:

- `balanced`: all categories equiprobable.
- `mild`: one category has probability `0.70`.
- `strong`: one category has probability `0.90`.

The remaining probability is distributed uniformly.

## 4. Methods

### Baseline 1: naive unstudentized permutation

Pool both samples, randomly reassign the fixed group sizes, and compare the
absolute raw plug-in MI difference. This is exact under `P = Q`, but is the
method suspected of failing under the weak null.

### Candidate 1: deterministic influence-function Wald test

Divide the estimated MI difference by its estimated influence-function
standard error and compare with a standard normal distribution.

### Candidate 2: studentized permutation

Recompute the studentized statistic after every group-label permutation. The
general weak-null permutation theory of Chung and Romano motivates this method.

### Bias handling

Every candidate is reported with:

- the ordinary plug-in MI; and
- a delete-one jackknife bias-corrected MI.

The jackknife is used because unequal sample sizes and different table shapes
can produce unequal plug-in biases even when the true MI values are equal. No
estimate is clipped to zero.

## 5. Validation Layers

### Layer 1: deterministic correctness tests

- Known tables: independence gives MI zero and a balanced diagonal binary table
  gives `log(2)` nats.
- Finite differences of MI agree with the stated influence function.
- Iterative proportional fitting recovers requested margins.
- Equal-MI distribution pairs agree within `1e-10` nats.
- The vectorized jackknife agrees with literal leave-one-out calculation.
- Hypergeometric table permutations preserve pooled counts and group sizes.

### Layer 2: strong-null calibration

Set `P = Q`. All permutation tests should be calibrated here. Failure indicates
an implementation bug or a finite-permutation issue rather than the proposed
weak-null phenomenon.

### Layer 3: weak-null calibration

Set `P != Q` but solve for `I(P) = I(Q)`. Vary:

- shape: `2x2`, `3x3`, `5x5`, and `10x10`;
- equal and unequal sample sizes;
- balanced, mild, and strong margins;
- MI well away from zero and MI near zero; and
- well-supported and sparse expected cells.

The primary endpoint is Type-I error at `alpha = 0.05`. Type-I error at
`alpha = 0.10` and p-value uniformity are secondary endpoints.

### Layer 4: interval coverage and power

- Measure 95% Wald interval coverage for known `Delta_I`.
- Under alternatives, verify that power increases with `|Delta_I|` and sample
  size.
- A calibrated but powerless method is not useful.

### Layer 5: runtime

Report per-table runtime for deterministic Wald inference and permutation
inference. Runtime is secondary to validity for this pilot.

## 6. Simulation Sizes

Profiles are intentionally staged:

- `smoke`: 40 replicates, 99 permutations, a small subset.
- `screen`: 300 replicates, 199 permutations, the full broad grid.
- `decisive`: 2,000 null replicates and 1,000 power replicates, 999
  permutations, the pre-specified core grid.

At a true 5% rejection rate, 2,000 replicates have Monte Carlo standard error
about `0.0049`. This can distinguish 5% from a materially inflated rate such as
8%, but not tiny differences such as 5.0% versus 5.5%.

## 7. Pre-Specified Decision Rules

### Go

Recommend pursuing the direction if all hold:

1. Strong-null permutation calibration has no systematic implementation
   failure.
2. Naive permutation has absolute 5% Type-I error at least `0.02` in two or
   more regular weak-null configurations, with a 95% Wilson interval excluding
   `0.05`.
3. `student_perm_jackknife` reduces mean absolute calibration error by at least
   40% relative to naive permutation over regular weak-null configurations.
4. In at least 80% of regular weak-null configurations, its 5% rejection rate
   is within `[0.035, 0.065]`.
5. The deterministic `wald_jackknife` is either similarly calibrated or its
   failure regime can be diagnosed before testing.
6. Power is monotone in the simulated effect and not materially below a valid
   resampling comparator.

### Refine before committing

Continue only as a narrower methods project if the studentized method works in
regular tables but fails predictably near independence or under sparsity. The
next contribution would then need a principled boundary/sparse route.

### No-go

Return to the safety-net thesis if:

- naive permutation is already well calibrated across adversarial weak-null
  cases;
- studentization does not materially improve calibration;
- bias correction is unstable and no clean diagnostic separates failures; or
- a focused literature review finds an already standard, directly applicable
  method with the same scope.

## 8. Scope of the Pilot

This experiment can establish a reproducible inferential gap and assess a
candidate solution. It cannot by itself establish publication novelty. A
citation-chain review remains mandatory before a thesis pivot.

Key starting references:

- Chung and Romano (2013), *Exact and asymptotically robust permutation
  tests*: https://arxiv.org/abs/1304.5939
- Kandasamy et al. (2015), *Influence Functions for Machine Learning:
  Nonparametric Estimators for Entropies, Divergences and Mutual
  Informations*: https://arxiv.org/abs/1411.4342
- Marinescu and Balcau (2025), *On the use of Mutual Information for Testing
  Independence*: https://arxiv.org/abs/2502.17636

## 9. Post-Protocol Adversarial Extensions

These checks were added after the pre-specified screen and are not used to
rewrite the original go/no-go thresholds:

- rectangular `2x3`, `3x5`, and `5x10` tables;
- cyclic and checkerboard log-linear interactions;
- equal margins but different dependence structures;
- larger `10x10` regular and sparse cases; and
- a `3x3` power curve varying effect size and sample size separately.

Their purpose is to challenge the narrowness of the original ordinal
association family and to complete the monotonic-power check.
