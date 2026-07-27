# Final Assessment: Constrained-Profile Differential MI

## Decision

**No-go for the uncorrected constrained-profile direction.**

The general constrained fit is numerically implementable, but none of the
three standard chi-squared-calibrated statistics solves the target problem.
In sparse/skewed tables they reject the true equal-MI null too often, and the
fit is much slower than the existing optimized table-permutation comparator.

This conclusion applies to:

- profile likelihood ratio;
- Pearson divergence from the constrained MLE;
- Cressie-Read divergence with lambda `2/3`;
- a chi-squared reference distribution with one degree of freedom.

It does not prove that a new analytic Bartlett, Skovgaard, or other
higher-order correction is impossible. Such a correction would be a separate,
substantially harder research project.

## Experiment

The focused run used:

- 16 weak-null scenarios: eight fixed designs under each of two independent
  scenario-generation seeds;
- exactly equal population MI with `P != Q`;
- easy regular controls and hard heterogeneous/sparse cases;
- shapes from `2x2` through `5x10`;
- 1,000 null replicates per scenario, for 16,000 table pairs;
- 100 alternative replicates per scenario, for 1,600 power pairs;
- common sampled tables for Wald and all profile methods;
- 999 optimized table permutations on a timing subset;
- three deterministic constrained-optimizer starts per table pair.

Near-independence was excluded as pre-specified. Population MI was at least
`0.03` nats.

## Main Results

At nominal alpha `0.05`:

| Subset | Method | Mean FPR | Mean absolute FPR error |
| --- | --- | ---: | ---: |
| Easy | corrected Wald | 0.04075 | 0.00925 |
| Easy | profile Pearson | 0.04312 | 0.00813 |
| Hard | corrected Wald | 0.06150 | 0.01150 |
| Hard | profile LR | 0.10495 | 0.05495 |
| Hard | profile Pearson | 0.10120 | 0.05120 |
| Hard | profile CR `2/3` | 0.10157 | 0.05157 |

The profile methods are therefore acceptable in the easy regular controls but
fail exactly where an improvement is needed. Pearson profile increases hard
false rejections over corrected Wald by about `0.0396`; a paired replicate
normal interval is `[0.0332, 0.0460]`.

The failure is especially clear in the two `5x10` sparse scenarios:

| Scenario seed | Corrected Wald FPR | Profile Pearson FPR |
| --- | ---: | ---: |
| 2026072501 | 0.063 | 0.217 |
| 2026072601 | 0.050 | 0.175 |

The mean Pearson statistic was `0.968` in easy cases, close to the expected
mean of chi-squared with one degree of freedom. It rose to `1.421` in hard
cases. This shows that the asymptotic reference distribution, rather than the
optimizer, is the central statistical problem.

The apparent profile power advantage is not evidence of better sensitivity:
profile Pearson rejected `56.1%` of alternatives versus `45.4%` for Wald, but
its null test was also substantially liberal.

## Runtime

The focused timing subset, measured under the same four-worker workload, gave:

| Method | Median time per pair |
| --- | ---: |
| Corrected Wald | 0.171 ms |
| Constrained profile | 142.829 ms |
| 999 optimized table permutations | 5.578 ms |

Profile fitting was `25.8x` slower than table permutation. A separate
single-process audit removed parallel contention and found `77.5 ms` for
profile versus `2.34 ms` for permutation, a consistent `26.6x` slowdown.

JIDT does not implement the independent two-sample weak null
`I(P) = I(Q)`. The runtime comparator is the existing optimized table-level
studentized permutation test for this estimand. Sampling allocation tables is
distributionally equivalent to shuffling group labels conditional on the
pooled table, while avoiding work proportional to raw sample size.

## Numerical Audit

- Trustworthy constrained fits: `15,997 / 16,000 = 99.98125%`.
- Every fit had three constraint-converged starts.
- Invalid fits: three, all in `5x10`; they were retained in the output and
  excluded from profile rejection-rate denominators.
- Mean absolute MI constraint residual: approximately `3.1e-13`.
- All saved p-values were finite and in `[0, 1]`.
- Recomputed p-values matched `chi2.sf(statistic, 1)` within `3.7e-15`.
- A saved table pair reproduced MI, statistics, and p-values to floating-point
  precision.
- Profile statistics were invariant to group swapping and category
  relabelling in tests.
- Sparse-table statistics were stable across logit bounds of 24 and 36.
- All 21 frozen `DifferentialMI` tests and all 8 new profile tests passed.

Boundary estimates are expected when sampled cell counts are zero. They were
flagged explicitly rather than silently discarded.

## Why It Fails

The constrained MLE solves the population null correctly, and Wilks' theorem
explains the good regular-case behavior. Sparse tables are too far from that
asymptotic regime. Standard LR, Pearson, and Cressie-Read reference
distributions all become liberal; changing the divergence within this family
does not supply the missing finite-sample correction.

The corrected Wald baseline directly removes the leading unequal-sample MI
bias. The raw profile tests contain no comparable finite-sample adjustment.
That is consistent with their much worse behavior in sparse rectangular
tables.

## Recommendation

Do not use the raw constrained-profile method as the thesis's main method and
do not spend time merely tuning its optimizer. The optimizer is not the main
failure.

Retain this project as a documented negative result. The current
analytically bias-corrected Wald method remains the stronger deterministic
safety-net thesis direction.

Only reopen profile likelihood if the thesis deliberately pivots to deriving
a deterministic higher-order correction. A bootstrap-estimated correction
would undermine the speed goal, and a simple empirical scale correction would
need an independent derivation and validation rather than being estimated
from these same null simulations.

## Files

- Pre-specified decision rules: `GO_NO_GO_PROTOCOL.md`
- Implementation: `src/profile_differential_mi/profile.py`
- Experiment runner: `experiments/run_go_no_go.py`
- Focused generated report: `results/focused/REPORT.md`
- Scenario-level results: `results/focused/null_summary.csv`
- Aggregate results: `results/focused/method_summary.csv`
- Runtime results: `results/focused/runtime_summary.csv`
- Full reproducible tables and diagnostics:
  `results/focused/null_replicates.csv.gz`

