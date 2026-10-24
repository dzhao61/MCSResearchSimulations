# Pre-Specified Finite-Sample Refinement Protocol

Date fixed: 25 July 2026

## Question

Does the influence-function saddlepoint approximation improve finite-sample
two-sided calibration over the frozen analytic-bias-corrected Wald method
without sacrificing its general fixed-table applicability or most of its
runtime advantage over permutation?

The Edgeworth branch was closed for theoretical reasons before this protocol
was written. See `docs/EDGEWORTH_THEORY_GATE.md`.

## Frozen Methods

| Method | Role |
|---|---|
| Analytic-bias-corrected Wald | Primary deterministic baseline |
| Influence-function saddlepoint | Candidate deterministic refinement |
| Raw label permutation | Existing applied practice and weak-null-invalid comparator |
| Studentized analytic permutation | Resampling comparator in its regular pooled-mixture regime |

All methods use natural-log MI. All tests are two-sided at `alpha=0.10` and
`alpha=0.05`. Near-independence of either original population remains out of
scope.

## Stage 1: Implementation Gate

The candidate does not enter simulation unless:

1. `K(0)=0`, `K'(0)=0`, and `K''(0)` equals the Wald variance to numerical
   tolerance on randomized positive tables.
2. Swapping the two groups leaves the two-sided p-value unchanged.
3. Relabeling categories leaves the p-value unchanged.
4. Every non-invalid result is finite and lies in `[0,1]`.
5. Near-mean and empirical-support boundary cases take an explicit recorded
   fallback route.

## Stage 2: Broad Weak-Null Calibration

Reuse the 72 saved randomized weak-null scenarios from the original broad
validation, then independently repeat with its second scenario seed:

- shapes from `2x2` through `20x20`, including rectangular tables;
- equal, `1:2`, and `1:4` sample-size ratios;
- balanced-like through strongly heterogeneous margins;
- common population MI `0.03`, `0.07`, or `0.15` nats;
- at least 2,000 replicate pairs per scenario and seed.

Primary metrics:

- mean absolute error from nominal 5% rejection;
- proportion of scenarios in the pre-specified `[0.035,0.065]` band;
- worst scenario rejection rate;
- nonfinite and fallback rates;
- paired scenario-level difference from analytic Wald.

The candidate passes this stage only if it:

- lowers mean absolute 5% calibration error by at least 10%;
- does not reduce the in-band proportion by more than two percentage points;
- has no unexplained invalid or nonfinite result; and
- does not create a new scenario with 5% rejection outside `[0.025,0.075]`
  when Wald was inside `[0.035,0.065]`.

## Stage 3: Pre-Declared Hard Regime

Use low-density, unequal-sample scenarios selected from generator parameters,
not from the candidate's observed errors:

- shapes `3x7`, `5x10`, `8x12`, `10x15`, and `20x20`;
- sample ratios `1:2` and `1:4`;
- target MI `0.03` and `0.07`;
- heterogeneous Dirichlet margins;
- at least 5,000 replicate pairs per scenario.

Compare to the already identified hard Wald behavior and to studentized
permutation where the pooled influence variance is regular.

The candidate is practically worthwhile if hard-regime mean absolute 5%
calibration error falls by at least 20% without a material broad-regime loss.

## Stage 4: Power

Perturb the common-MI null scenarios to signed alternatives while holding
sample sizes and margins fixed. Report rejection probability against the true
MI difference and compare:

- Wald versus saddlepoint at the same nominal level;
- any power gain only after checking null calibration;
- positive and negative alternatives to expose one-sided distortion.

The saddlepoint is rejected if an apparent power gain is caused by inflated
null size.

## Stage 5: Runtime

Measure warm single-pair runtime for:

- analytic Wald;
- influence saddlepoint;
- 999 optimized count-table permutations;
- 999 individual-label permutations where JIDT is used only as an
  implementation/runtime reference.

Report median and upper-quartile runtime by table size. The candidate passes
the practical runtime gate if it remains at least ten times faster than 999
count-table permutations for the median supported scenario.

## Stage 6: Adversarial Audit

Audit:

- group-swap and category-label invariance;
- exact duplicated-table symmetry;
- unequal sample sizes;
- nearly empty observed margins;
- very skewed influence scores;
- CGF support endpoints;
- near-zero saddlepoint roots;
- monotonic one-sided tails over a fixed CGF;
- reproducibility across simulation seeds; and
- agreement of table MI with JIDT to `1e-10`.

Any failure is retained in the report and either fixed before rerun or
declared as an exclusion.

## Sequential Decision Rule

1. If Stage 2 fails, stop developing saddlepoint and retain analytic Wald.
2. If Stage 2 passes but Stage 3 does not improve, retain Wald for simplicity.
3. If Stages 2 and 3 pass, complete power, runtime, audit, and case-study work.
4. The candidate becomes primary only if the complete evidence supports a
   clear calibration or tail-accuracy advantage.

No threshold, scenario exclusion, or fallback rule may be changed after
Stage 2 results are inspected without labeling the change post hoc and
running an independent confirmation seed.
