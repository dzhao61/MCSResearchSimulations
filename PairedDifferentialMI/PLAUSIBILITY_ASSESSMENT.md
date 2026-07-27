# Paired Differential-MI Plausibility Assessment

Date: 27 July 2026

## Bottom Line

The covariance-aware paired Wald architecture is mathematically sound and
converges as sample size increases. However, the proposed paired
jackknife-t finite-sample refinement did not improve it. Both deterministic
methods become strongly conservative when positive pairing makes the
first-order MI-difference variance small, especially with sparse tables.

Therefore:

```text
Basic paired Wald method: plausible and useful in a regular regime.
Proposed improved method: no-go in its current jackknife-t form.
Small/sparse/high-pairing thesis objective: not yet solved.
```

This direction should not replace the existing safety-net thesis unless a
genuinely second-order method is developed and passes a new validation gate.

## Question Tested

For IID paired observations

```text
Z_i = (X_Ai, Y_Ai, X_Bi, Y_Bi),
```

test the weak null

```text
H0: I(X_A;Y_A) = I(X_B;Y_B)
```

without requiring equal condition-specific tables, margins, or interaction
patterns.

The tested improvement was a deterministic delete-one jackknife
pseudo-value-t test. It was compared with paired influence-function
Wald-normal, paired Wald-t, an intentionally incorrect unpaired Wald
diagnostic, and a 999-replicate paired bootstrap-t reference.

## Why the Experiment Is Auditable

Each condition-specific probability table was constructed with an exact
target MI. A separate coupling matrix preserved both tables while controlling
the covariance of their local-information scores. This allowed MI equality,
marginal skewness, sparsity, and pairing strength to vary independently.

Across the pilot:

- the largest null MI-construction error was `4.97e-14` nats;
- the largest coupling-margin error was `4.44e-16`;
- direct and batch MI formulas matched hand-checked cases;
- closed-form jackknife pseudo-values matched brute delete-one calculations;
- paired variance matched the variance of explicitly expanded subject scores;
- swapping conditions reversed the estimate and preserved two-sided p-values;
- all seven correctness tests passed.

## Validation Scale

Two independent-seed pilots each included:

- 20 null scenarios with 3,000 samples each;
- 3 power scenarios with 2,000 samples each;
- shapes `2x2`, `3x3`, and `5x5`;
- balanced, mild, and strong margins;
- negative, zero, and positive pairing;
- positive MI from `0.05` to `0.15` nats;
- severe sparse and near-independence controls; and
- 48 selected 999-bootstrap p-value anchors.

Together these runs contain 120,000 null and 12,000 power samples.

A separate operating-boundary screen used 225,000 null samples across 45
sample-size-by-pairing scenarios. A targeted bootstrap calibration used 2,000
null tables and approximately two million bootstrap replicates.

## Replicated Main Results

The table pools scenario FPRs from both independent pilots.

| Regime | Method | Mean 5% FPR | Mean absolute error | Scenarios in 3.5%-6.5% |
| --- | --- | ---: | ---: | ---: |
| Regular | Paired Wald-normal | 0.0444 | 0.0101 | 66.7% |
| Regular | Paired Wald-t | 0.0418 | 0.0110 | 75.0% |
| Regular | Paired jackknife-t | 0.0374 | 0.0141 | 66.7% |
| Regular | Unpaired Wald-normal | 0.0362 | 0.0334 | 16.7% |
| Sparse | Paired Wald-normal | 0.0335 | 0.0165 | 60.0% |
| Sparse | Paired Wald-t | 0.0305 | 0.0195 | 40.0% |
| Sparse | Paired jackknife-t | 0.0273 | 0.0227 | 40.0% |
| Sparse | Unpaired Wald-normal | 0.0207 | 0.0293 | 40.0% |

The two runs reached the same pre-specified decision:

```text
Regular calibration rule: FAIL
Sparse refinement rule:   FAIL
Runtime rule:             PASS
```

The jackknife reduced estimator bias in some cases but generally made the
test more conservative. Better point estimation did not produce better tail
calibration.

## Pairing Is Essential

Ignoring covariance was not a harmless simplification. Across regular
scenarios, unpaired FPR ranged from approximately zero to `0.117`.

- Positive covariance reduces the true variance. Ignoring it overestimates
  the standard error and can remove nearly all power.
- Negative covariance increases the true variance. Ignoring it underestimates
  the standard error and can inflate false positives.

This validates the paired architecture, but accounting for covariance is a
standard requirement rather than a new finite-sample solution.

## Operating Boundary

The focused screen shows convergence rather than a fundamental inconsistency.
Selected paired Wald-normal FPRs are:

| Design | Pairing | N=50 | N=100 | N=200 | N=500 | N=1000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Balanced `2x2`, MI=0.10 | 0.0 | 0.052 | 0.052 | 0.048 | 0.054 | 0.047 |
| Balanced `2x2`, MI=0.10 | 0.8 | 0.018 | 0.039 | 0.045 | 0.046 | 0.055 |
| Weak-null skewed `2x2`, MI=0.05 | 0.8 | 0.019 | 0.030 | 0.041 | 0.047 | 0.054 |
| Sparse strong-margin `3x3`, MI=0.05 | 0.8 | 0.010 | 0.016 | 0.016 | 0.038 | 0.043 |

Strong positive pairing is difficult because it cancels much of the
first-order variation between conditions. The nominal sample size can then be
large while the effective amount of information in the contrast is small.
Sparse cells add discreteness and unstable estimated local scores.

The method works once sampling is sufficiently dense, but that is narrower
than the motivating goal.

## Bootstrap Result

Ordinary paired bootstrap-t did not solve the hard cases:

| Scenario | Wald FPR | Jackknife FPR | 999-bootstrap FPR |
| --- | ---: | ---: | ---: |
| Balanced `2x2`, N=50, pairing=0.8 | 0.012 | 0.000 | 0.000 |
| Weak-null `2x2`, N=100, pairing=0.8 | 0.032 | 0.026 | 0.020 |
| Regular `3x3`, N=150, pairing=0.8 | 0.046 | 0.042 | 0.048 |
| Sparse `3x3`, N=50, pairing=0.8 | 0.012 | 0.010 | 0.006 |

Each result used 500 independently simulated null tables. The bootstrap is
well calibrated in the supported regular `3x3` case but is at least as
conservative as the deterministic tests in the difficult cases. This
indicates a genuinely low-information, discrete-tail problem rather than
only a poor choice of normal reference.

## Runtime

For the pilot anchors:

```text
Median deterministic single-test latency: 0.156 ms
Median vectorized 999-bootstrap latency:   about 2 ms
Median speedup:                            10.8x
```

The bootstrap implementation is optimized and vectorized, making this a
stronger runtime comparator than a literal subject-by-subject loop. The
deterministic method is fast enough; accuracy, not runtime, is the blocker.

## Interpretation Relative to MI = 0

The paired problem is still easier in regular mathematical terms. At positive
MI, its first derivative is nonzero and first-order normal theory eventually
works. Testing `MI=0` begins at a nonregular point where that derivative is
zero.

However, strong positive pairing can nearly cancel the two nonzero
first-order terms. The paired contrast then behaves partly like a
second-order problem even though each individual MI is positive. This is why
the difficult regime starts to resemble the original sparse-independence
problem.

## Credible Next Step, If Continued

The only well-motivated methodological continuation is a second-order
linear-plus-quadratic approximation for the paired multinomial functional:

```text
Delta_hat - Delta
approximately
linear influence term
+ quadratic Hessian term.
```

A defensible continuation would:

1. derive the gradient and Hessian with respect to the full paired
   multinomial distribution;
2. quantify the quadratic contribution relative to first-order variance;
3. use that ratio as an operating-regime diagnostic;
4. approximate the linear-plus-quadratic Gaussian tail deterministically;
5. test whether it fixes high-pairing and sparse calibration without harming
   ordinary cases; and
6. stop immediately if it cannot beat paired Wald by a pre-specified margin.

This is substantially more complex than the failed jackknife correction. It
should be treated as a new high-risk project, not a routine refinement.

## Recommendation

Do not promote paired jackknife-t as the thesis method. Retain paired
Wald-normal as a useful validated baseline and negative result.

For thesis planning:

- keep the sparse binary CMI method as the safety net;
- discuss paired differential MI with the supervisor as a possible
  higher-risk second-order direction;
- do not claim that the current paired method solves sparse finite-sample MI
  comparison; and
- only continue implementation if the supervisor agrees that the
  linear-plus-quadratic derivation is an acceptable level of complexity.

## Reproducible Artefacts

- Protocol: `FEASIBILITY_PROTOCOL.md`
- Core implementation: `src/paired_differential_mi/core.py`
- Distribution construction: `src/paired_differential_mi/distributions.py`
- Main pilots: `results/pilot/` and `results/pilot_replication/`
- Operating boundary: `results/operating_boundary/`
- Bootstrap calibration: `results/bootstrap_calibration/`
- Correctness tests: `tests/test_core.py`
