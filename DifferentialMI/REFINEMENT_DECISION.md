# Finite-Sample Refinement Decision

Date: 25 July 2026

## Decision

Retain analytic-bias-corrected Wald as the primary deterministic method.
Do not continue influence-saddlepoint development into hard-regime, power, or
case-study comparisons.

This follows the sequential stopping rule fixed in
`REFINEMENT_VALIDATION_PROTOCOL.md`.

## Edgeworth Branch

The simple Edgeworth branch was stopped before implementation. The leading
skewness correction cancels in a symmetric two-sided tail, and a valid
studentized expansion would require additional terms from variance
estimation and the nonlinear MI functional. See
`docs/EDGEWORTH_THEORY_GATE.md`.

## Influence-Saddlepoint Branch

The candidate passed its implementation gate:

- empirical CGF mean and variance matched the Wald calculation;
- group swapping and category relabeling were invariant;
- all nondegenerate results were finite;
- the method supported arbitrary fixed rectangular tables; and
- its median runtime was approximately `0.68 ms` per table pair.

The pre-specified broad run used:

- 2 independently generated scenario seeds;
- 72 scenarios per seed;
- 2,000 replicate table pairs per scenario;
- 144 total weak-null scenarios; and
- 288,000 total p-value comparisons.

At nominal `alpha=0.05`:

| Method | Mean absolute FPR error | Scenarios in 3.5%-6.5% band | Minimum FPR | Maximum FPR |
|---|---:|---:|---:|---:|
| Analytic Wald | 0.00561 | 96.5% | 0.035 | 0.077 |
| Influence saddlepoint | 0.00571 | 96.5% | 0.035 | 0.080 |

The candidate's relative change in mean absolute error was `-1.67%`: it was
slightly worse, not the pre-specified improvement of at least 10%. It
therefore failed Stage 2.

## Numerical Audit

The first broad implementation used a near-mean normal threshold of
`|Delta|/SE <= 1e-4`. Inspection found Lugannani-Rice cancellation just above
that threshold. One non-significant replicate had saddlepoint `p=0.151`
versus Wald `p=0.9999`.

The default threshold was corrected post hoc to `0.01`, and the case was
added as a regression test. In the saved broad run:

- 2,244 of 288,000 rows, or 0.78%, meet the corrected near-mean rule;
- replacing their tails by the documented normal fallback changes no 5%
  rejection decision;
- the worst p-value discrepancy falls from `0.849` to `0.025`; and
- the broad calibration table and Stage-2 failure are unchanged.

The raw broad files are retained rather than overwritten. This preserves the
audit trail between the pre-specified run and the post-run stability fix.

## Interpretation

The empirical saddlepoint calculation mostly reproduces the normal
approximation because both start from the same first-order influence-function
linearization. The remaining finite-sample error appears to be driven more by
the nonlinear MI estimator, residual bias, and estimated variance than by
non-normality of the fixed empirical influence-score sum.

This is scientifically useful: a more elaborate tail approximation is not
automatically a better MI test when the dominant approximation error occurs
earlier in the construction.

## Consequence for the Thesis

The strongest current method remains:

```text
analytic leading-bias correction
+ influence-function standard error
+ deterministic normal reference.
```

Its value is speed, calibration in the declared regular regime, and
correction of raw weak-null permutation practice. It should not be presented
as a newly invented asymptotic estimator.

The influence-saddlepoint branch can appear briefly as a principled negative
experiment. It should not be promoted as the thesis contribution unless a
future derivation addresses the nonlinear/studentized terms rather than only
the influence-score tail.

## Reproducible Artefacts

- Protocol: `REFINEMENT_VALIDATION_PROTOCOL.md`
- Derivation: `docs/INFLUENCE_SADDLEPOINT_DERIVATION.md`
- Runner: `experiments/run_refinement_validation.py`
- Broad report: `results/refinement_broad/REPORT.md`
- Scenario summary: `results/refinement_broad/summary.csv`
- Aggregate result: `results/refinement_broad/aggregate.csv`
- Full replicate diagnostics:
  `results/refinement_broad/refinement_replicates.csv.gz`
