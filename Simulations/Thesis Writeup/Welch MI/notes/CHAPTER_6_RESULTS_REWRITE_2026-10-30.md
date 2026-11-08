# Chapter 6 results rewrite — 30 October 2026

The user requested application of the Section 6.1.1 writing standards to the
rest of Chapter 6. Sections 6.1.2 through 6.4 have been revised against
[the current guide](CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md).
Section 6.1.1 and the preceding chapter introduction remain unchanged.

## Changes

- Sections 6.1.2 and 6.1.3 explain the calculations before the figures, then
  interpret each row in a connected paragraph. The prose distinguishes
  population inputs, sampling-moment targets, mean sample-based estimates,
  competing numerator/denominator errors and the order of averaging.
- The near-independence discussion identifies fixed sample size and changing
  MI. It explains the positive noise contribution, the two steps behind the
  variance prediction, and the different behaviour of the degrees-of-freedom
  quantities before consolidating the numerical comparison.
- Section 6.2 follows the table-size panels and distinguishes movement towards
  5% from a reduction in rejection. It connects the patterns to difference
  bias, standard-error error, numerator/denominator dependence, the cutoff
  and validity. Identical tables are identified as a feature of the experiment,
  rather than inferred from uniform margins alone.
- The selected-case diagnostics now define Bias/SD and the variance ratio
  procedurally, and remind the reader of settings A–C. The sparse-table
  comparison connects opposite rejection outcomes to their different sampling
  centres despite similar variance ratios.
- Section 6.3 interprets A, B and C separately. It explains the initial power
  dip through the signed difference and bias, and explains calibrated ordering
  through separately fitted thresholds and the methods' rankings of samples.
  The fitting null, evaluation null and fixed alternative remain distinct.
- Section 6.4 connects the sign and size of the estimated difference to its
  standard error, reference distribution and decision. It retains the limits
  of non-rejection and of checking population targets in an observed dataset.

## Preservation and verification

The pre-edit chapter is preserved in
`../archive/before_chapter6_results_rewrite_2026-10-30.zip`.

- All seven figure blocks, nine table blocks and two displayed equation blocks
  remain byte-identical, including captions, dimensions and typography.
- Headings, labels, citation sequence and all pre-existing numerical literals
  are retained. All 58 Chapter 6 references resolve uniquely.
- Protected-file fingerprints confirm that the other active sources, assets,
  existing PDF and delivery files are unchanged.
- Curve interpretations were checked against six existing rendered figures,
  saved moment summaries, validity and degrees-of-freedom records, shared
  estimator diagnostics, power-path diagnostics and the existing mechanism
  decomposition. No new evaluation samples were generated.
- All 33 existing `test_thesis_*.py` tests passed. Source structure,
  paragraph style and whitespace checks passed.

The PDF has not been rebuilt. Typeset layout inspection and delivery refresh
remain for the next explicit rebuild request.
