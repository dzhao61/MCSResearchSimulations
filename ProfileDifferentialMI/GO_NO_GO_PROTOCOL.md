# Pre-Specified Go/No-Go Protocol

## Question

Does fitting two multinomial tables under the nonlinear constraint
`I(P) = I(Q)` produce a deterministic finite-sample test that is materially
better calibrated than the existing analytically bias-corrected Wald test,
without an unacceptable numerical-failure or runtime cost?

This is a method-development gate, not a final publication experiment.

## Fixed Methods

- `wald_analytic`: existing bias-corrected influence-function Wald test.
- `profile_lr`: likelihood-ratio statistic from the constrained MLE.
- `profile_pearson`: Pearson divergence from the constrained MLE.
- `profile_cr_2_3`: Cressie-Read divergence with lambda `2/3`.

Every profile statistic uses a chi-squared reference distribution with one
degree of freedom because the null imposes one scalar restriction. No result
from an untrustworthy constrained fit is counted as a valid test result.

## Scenario Families

The focused pilot uses frozen, reproducible weak-null distributions generated
by the existing `DifferentialMI` machinery. Each pair has:

- exactly equal population MI;
- different population joint distributions;
- population MI at least `0.03` nats;
- positive cell probabilities.

The selected cases cover:

- regular controls with large expected counts;
- unequal sample sizes;
- heterogeneous and skewed margins;
- sparse observations and zero sampled cells;
- square and rectangular alphabets.

The main calibration analysis is restricted to the regular MI regime. Exact
independence remains outside scope because the first derivative of MI
degenerates there.

## Evidence

For each scenario, estimate null rejection rates at alpha `0.10` and `0.05`.
Report Wilson intervals, mean absolute false-positive-rate error, valid-fit
rate, optimizer diagnostics, and wall-clock time per pair.

Run two fixed scenario seeds to guard against conclusions tied to one random
set of margins and interactions. Use common random table pairs for every
method within a scenario.

A small alternative set checks that improved calibration is not obtained by
making the test powerless. This power result is descriptive in the pilot.

## Go Criteria

Proceed to a thesis-scale validation only if all conditions hold:

1. At least one profile statistic reduces mean absolute FPR error at alpha
   `0.05` by at least `20%` versus `wald_analytic` in the hard sparse/skewed
   subset.
2. The same statistic does not increase mean absolute FPR error by more than
   `0.005` in regular controls.
3. At least `99.5%` of constrained fits are trustworthy.
4. Category relabelling and group swapping change profile statistics by less
   than `1e-7` in correctness tests.
5. Median runtime is below a 999-permutation test on the same table pairs.
6. The selected profile method retains broadly comparable power to the Wald
   baseline in the pilot alternatives.

## No-Go Criteria

Stop this direction if any condition holds:

- no profile statistic meets the calibration improvement criterion;
- apparent gains depend on excluding zero-cell samples;
- trustworthy-fit rate is below `99.5%`;
- optimizer solutions materially depend on starts or category ordering;
- runtime is not competitive with the relevant resampling baseline;
- gains are explained by severe power loss.

## Interpretation Limits

A `go` means the method deserves broader validation and theoretical work. It
does not establish novelty, uniform validity, or superiority for all tables.
A `no-go` is still useful: it prevents investing a thesis in a numerically
complex method that does not improve the already strong Wald baseline.

