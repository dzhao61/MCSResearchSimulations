# Targeted Unequal-Sample Check

Agreed 10 October 2026. Complete: all simulations, independent audits,
155 workspace tests, manuscript edits and PDF layout checks pass. The
extracted packages pass 73 bundled tests, both evidence audits, identical
allocation-table regeneration and a clean source build. Older drafts remain
unchanged; SUBMISSION_CHECK.md records final verification.

## Question and scope

Does allocating fewer observations to one population change the comparison
between Normal Wald and Expanded Welch at fixed total sample size?

- Copying populations: 4 x 4, different-skew margins, with dominant
  probabilities 0.7 in P and 0.8 in Q, as in the existing study.
- MI pairs: (0.02, 0.02) and (0.02, 0.03) nats. The signed difference is
  therefore 0 or -0.01 nats.
- Allocations (n_P, n_Q): (1000, 1000), (400, 1600), (1600, 400).
  All use 2000 observations in total. Reversing the allocation keeps P and Q
  fixed; it does not reverse the association or swap population labels.
- Both methods on the same sampled pair, two-sided 5% threshold, 20000
  repetitions per setting, unchanged estimators and validity rules.

The six comparisons reuse two balanced settings. Four new settings add
80000 sampled pairs, no new population pairs, and no change to the original
232-setting study. The combined evidence has 236 distinct settings, 68
population pairs and 4720000 sampled table pairs. Balanced samples are not
counted twice. Do not broaden the grid in response to the results.

## Implementation and checks

1. Use a separate runner, output directory and run identity. Reuse unchanged
   sampling, method evaluation and summaries. Copy checksum-verified balanced
   records from the original study and record their provenance.
2. Preserve configuration-derived PCG64 streams from master seed 20261006.
   New allocations have new identifiers and independent P/Q streams. Use
   separate pilot streams, fixed chunks and batch-invariant sampling.
3. Test exact scope, constant total sample size, unchanged populations,
   balanced reuse, unequal bias corrections, variance weighting, batching,
   resume protection and corruption detection. Run a technical pilot before
   the full four new simulations.
4. Independently verify all six settings: population inputs, checksums,
   regenerated count tables, statistic, component and combined degrees of
   freedom, p-values, validity, rejection, Wilson intervals, paired method
   contrasts, bias and variance summaries.

## Reporting

Report every allocation under both MI pairs, whatever the outcome. One
compact appendix table will contain rejection with pointwise 95% intervals,
validity, corrected-difference bias, estimated/observed variance ratio and
median combined degrees of freedom. Bias and variance diagnostics retain
the same masks as the original study. Allocation comparisons use independent
simulation streams; only the within-setting method comparison is paired.

Add the exact settings and unequal correction to Appendix B and a short
design description in Chapter 5. Explain the result briefly in Chapter 6
and qualify the unequal-sample limitation in Chapter 7. Update totals and
scope statements, but keep the original figures and main narrative intact.
No broad claim about all imbalanced samples follows from these two pairs.

## Acceptance

All tests and independent audits pass; the manuscript agrees with the
saved evidence; the PDF builds without unresolved references or layout
warnings and is visually checked. Refresh source and experiment packages
and verify them in isolation. Preserve earlier working drafts unchanged.
