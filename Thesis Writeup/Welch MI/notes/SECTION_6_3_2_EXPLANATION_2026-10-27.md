# Section 6.3.2 explanation, 27 October 2026

The user requested clearer explanation following discussion of calibrated
power. The revision uses the established order: scientific question,
motivation, procedure, evidence, interpretation and a related follow-up.

## Reading sequence

- The title is now Power after matching false-positive rates.
- Start with the nominal comparison: lower power at A/B accompanies fewer
  false positives. Ask whether the power ordering persists after matching
  false-positive rates.
- Explain that calibration replaces the usual p-value threshold separately
  for each method. Fit independently, freeze thresholds, validate on separate
  null samples, then compare on the original alternative samples. Estimates,
  standard errors and calculated p-values stay fixed.
- Introduce calibration at common MI 0.02, the achieved 4.93--4.99% rates,
  and how the graph's zero and positive horizontal coordinates differ.
- Walk through A at two null SDs: Wald 32.57%, Expanded Welch 36.15%, a
  3.58 percentage-point gain. This reverses the nominal ordering there.
- Then introduce the second question: whether the result persists when the
  fitting population changes. Define lower and upper nulls in two short
  bullets and explain that the alternative samples remain the same.
- Define table columns, gain signs and uncertainty before the table.
- Preserve all sensitivity findings, the restriction to the checked nulls
  and the persistence of B's bias-related power-curve distortion.

## Checks

- Archived prior source in
  `archive/before_section_6_3_2_explanation_2026-10-27.zip`.
- Only Section 6.3.2 manuscript prose and its heading changed.
- Original figure/table blocks, dimensions, captions, table data and all
  numerical findings are unchanged. The new A walkthrough uses existing
  saved rates, displayed with the established decimal half-up convention.
- Other Chapter 6 text, including Section 6.4, is byte-identical, as are
  all other manuscript sources and figure/table assets.
- Seven calibration-sensitivity checks and five manuscript-consistency
  checks pass. Active labels/references, environments, braces and the
  flush-left paragraph policy pass source checks.
- No experiment, bootstrap, PDF build or packaging refresh was run for
  the revision. Existing PDF and delivery hashes are unchanged. Layout and
  pagination remain to be checked at the next requested rebuild.
