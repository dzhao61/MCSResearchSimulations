# Differential-MI Pilot: Go/No-Go Report

Date: 25 July 2026

> **Superseded recommendation:** The later two-seed randomized validation
> found that the classical analytic bias correction is simpler and slightly
> better calibrated than jackknife-Wald. See `ROBUST_VALIDATION_REPORT.md`.
> This document is retained as the historical pre-randomization pilot.

Decision: **conditional GO for a focused thesis-development phase**

## Executive Finding

The proposed research problem is real:

```text
H0: I_P(X;Y) = I_Q(X;Y)
```

is not the same as testing `P = Q`. In the simulations, ordinary
unstudentized group-label permutation was correctly calibrated when `P = Q`,
but often badly calibrated when `P != Q` and the two population MI values were
exactly equal.

Influence-function studentization fixed most of this error. A delete-one
jackknife correction was also important when the samples had different sizes
or different sparse-table biases.

The strongest practical candidate from this pilot is a deterministic,
jackknife-corrected influence-function Wald test, with studentized permutation
as a robust validation/reference method. The first-order method is not a
complete general solution: it is strongly conservative near independence,
where the MI influence function degenerates.

This is enough evidence to justify a focused novelty review and theory phase.
It is not yet enough to abandon the preserved sparse-CMI saddlepoint thesis.

## What Was Tested

The protocol was written before inspecting simulation results. It is in
`EXPERIMENT_PROTOCOL.md`.

### Pre-specified experiment

- 2,000 null replicates per configuration.
- 1,000 power replicates per configuration.
- 999 group-label permutations per replicate.
- Shapes from `2x2` through `10x10`.
- Balanced, mild, and strong marginal skew.
- Equal and unequal sample sizes.
- Strong nulls (`P = Q`), weak nulls (`P != Q` but equal MI), sparse cases,
  near-independence cases, and alternatives.

### Post-protocol adversarial experiment

- 2,000 null replicates per configuration with a different seed.
- Rectangular `2x3`, `3x5`, and `5x10` tables.
- Ordinal, cyclic, and checkerboard dependence structures.
- Cases with equal margins but different dependence structures.
- Additional regular and sparse `10x10` cases.
- A separate 1,500-replicate power curve.

All weak-null distribution pairs were constructed to have equal population MI
within approximately `1e-11` nats or better. The L1 distances between many
pairs exceeded one, so they were not nearly identical distributions.

## Correctness Checks

Seven deterministic tests passed:

- known independent and perfectly associated tables;
- iterative proportional fitting recovers requested margins;
- equal-MI root solving;
- finite-difference verification of the MI influence function;
- zero influence variance at exact independence;
- vectorized jackknife against literal leave-one-out calculation; and
- finite, bounded p-values from all methods on a supported example.

The table-level permutation sampler draws from the multivariate hypergeometric
distribution conditional on pooled cell counts. This is the count-table
equivalent of permuting individual group labels.

## Main Accuracy Results

The table below combines all 10 regular weak-null configurations from the
pre-specified and adversarial high-replicate runs.

| Method | Mean absolute error from 5% | Observed rejection-rate range |
|---|---:|---:|
| Naive raw permutation | 0.03075 | 0.0055-0.0710 |
| Studentized permutation, plug-in MI | 0.00710 | 0.0340-0.0545 |
| Studentized permutation, jackknife MI | 0.00565 | 0.0375-0.0535 |
| Deterministic Wald, plug-in MI | 0.00980 | 0.0385-0.0890 |
| Deterministic Wald, jackknife MI | **0.00360** | **0.0405-0.0510** |

Important interpretations:

- Naive permutation was usually very conservative, sometimes rejecting only
  `0.55%` of true nulls at nominal `5%`. This loses substantial power.
- It was not always conservative. With equal margins but different dependence
  structures, it rejected `7.1%`, whose Wilson interval excluded `5%`.
- Studentization substantially repaired both directions of error.
- The uncorrected deterministic Wald test rejected `8.9%` in one regular
  unequal-sample `10x10` case.
- Jackknife bias correction reduced that Wald rejection rate to `4.5%`.
- Jackknife-Wald 95% interval coverage ranged from `94.9%` to `95.95%` over
  the regular weak-null cases.

At nominal `10%`, the corresponding mean absolute errors were `0.0547` for
naive permutation, `0.0081` for studentized-jackknife permutation, and `0.0053`
for jackknife-Wald. The finding is therefore not specific to one significance
cutoff.

Under four strong-null cases where `P = Q`, the permutation methods rejected
between `4.4%` and `5.25%`. This supports the implementation and confirms that
the failure is about the weak parameter null rather than permutation coding.

## Boundary and Sparse Results

The method does not solve every regime.

Near independence:

- `2x2`, true MI `0.002`: studentized-jackknife rejection was `0.5%`.
- `5x5`, true MI `0.005`: studentized-jackknife rejection was `2.75%`.

This conservatism is expected because the first-order influence function
vanishes at exact independence. A first-order normal or studentized method
cannot simply be declared valid there.

The three deliberately sparse large-table cases were more encouraging but
mixed:

- Original `10x10`: studentized-jackknife `5.3%`.
- Adversarial `5x10`: studentized-jackknife `6.65%`.
- Equal-margin/different-structure `10x10`: studentized-jackknife `5.85%`.

These results suggest that sparsity alone does not destroy the method, but a
formal support diagnostic and a sparse correction remain necessary.

## Power

For a `3x3` balanced-versus-strong comparison at fixed `N = 300` per group,
studentized-jackknife power increased with the absolute MI difference:

| Absolute MI difference | Power |
|---:|---:|
| 0.02 | 0.0767 |
| 0.05 | 0.2467 |
| 0.10 | 0.7053 |

At fixed absolute MI difference `0.05`, power increased with sample size:

| N per group | Power |
|---:|---:|
| 150 | 0.1480 |
| 300 | 0.2467 |
| 600 | 0.5167 |

The method is not highly powered for small effects at these sample sizes, but
the required monotonic pattern is present.

## Runtime

Across the pre-specified decisive run:

- deterministic inference: about `0.119 ms` per table pair;
- 999 count-level permutations: about `2.227 ms` per table pair.

Across the larger adversarial run:

- deterministic inference: about `0.123 ms` per table pair;
- 999 count-level permutations: about `4.617 ms` per table pair.

The deterministic method was roughly 19-38 times faster in this optimized
Python implementation. These are not JIDT timings and should not be presented
as a direct JIDT speed comparison: JIDT does not provide this two-population MI
parameter test as its standard significance problem.

## Acceptance-Criteria Decision

1. **Strong-null implementation check:** pass.
2. **At least two material naive-permutation failures:** pass; five occurred
   in the pre-specified regular grid.
3. **At least 40% calibration-error reduction:** pass; the pre-specified
   studentized-jackknife reduction was `80.4%`.
4. **At least 80% of regular cases in the 3.5%-6.5% band:** pass; `100%`.
5. **Deterministic method calibrated or diagnosable:** provisional pass;
   jackknife-Wald was excellent under the regular weak null, but one small
   strong-null case was conservative at `3.3%`.
6. **Monotone power:** pass.

## What the Thesis Contribution Could Be

A thesis cannot claim studentization itself as new. General weak-null
studentized permutation theory already exists. A defensible contribution would
need to be MI-specific:

1. derive the two-sample discrete-MI influence-function test and its
   jackknife/bias behavior;
2. prove regular-case asymptotic validity under unequal distributions and
   unequal sample sizes;
3. develop a data-driven diagnostic for first-order validity;
4. provide a second-order route near independence and a sparse-table route;
5. establish simultaneous inference for differential-MI networks; and
6. provide a carefully validated implementation.

The cleanest thesis may be narrower:

> **Valid and Fast Inference for Differences in Discrete Mutual Information
> Across Populations**

with a regular deterministic test, an honest diagnostic, and a second-order or
resampling fallback.

## Preliminary Novelty Audit

A focused title/keyword search did not identify an obvious paper with the exact
target `H0: I(P) = I(Q)` for two independent discrete joint distributions.
That is encouraging but is not proof of novelty.

The neighboring literature substantially narrows what can be claimed:

- Chung and Romano provide the general weak-null studentized permutation
  framework:
  https://arxiv.org/abs/1304.5939
- Rey et al. develop delta-method tests for comparing entropies from two
  multinomial samples:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC10217615/
- Kandasamy et al. study influence-function estimators for entropies,
  divergences, and MI:
  https://arxiv.org/abs/1411.4342
- Stefani et al. give distribution-free finite-alphabet MI confidence bounds:
  https://arxiv.org/abs/1301.5942
- Marinescu and Balcau apply first- and second-order delta methods to
  one-sample MI independence testing:
  https://arxiv.org/abs/2502.17636

Therefore, a thesis whose only contribution is "use a two-sample delta method
for MI" would likely be too incremental. The defensible contribution must be
the finite-sample bias correction, weak-null failure demonstration,
operating-regime diagnostic, boundary/sparse theory, or differential-network
extension.

## Remaining Risks

- Publication novelty has not been established by this simulation.
- The general weak-null permutation idea is established statistics, so the
  novelty must come from MI-specific theory and finite-table corrections.
- The first-order method is invalid or conservative near independence.
- Very sparse high-dimensional tables need more varied random-distribution
  stress tests and a formal route criterion.
- The simulations use positive log-linear families. Three interaction
  structures were tested, but they do not represent every joint distribution.
- No real-data case study, conditional MI, or transfer-entropy extension has
  yet been implemented.

## Recommended Next Gate

Spend one focused week on two tasks before formally pivoting:

1. **Novelty audit:** citation-chain search for equality tests and confidence
   intervals for entropy, divergence, and MI across two multinomial
   populations.
2. **Theory/design audit:** derive the regular theorem, characterize
   degeneracy at independence, and define a diagnostic that does not use the
   unknown true MI.

Proceed with the new thesis only if no directly applicable published method
already supplies the same estimator, correction, diagnostics, and scope. Keep
`Sparse CMI/docs/SAFETY_NET_THESIS.md` unchanged until that gate is passed.

## Reproducibility

Commands are in `README.md`. High-replicate outputs are:

- `results/decisive/`
- `results/adversarial/`
- `results/power_curve/`

Each contains raw replicate CSV data, scenario probability tables, summaries,
plots, metadata, and an automatically generated report.
