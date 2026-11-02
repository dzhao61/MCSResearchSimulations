# Abstract and conclusion accessibility revision — 2 November 2026

The user authorised revision and a PDF rebuild after reviewing both sections.
The governing constraint is that a reader new to the thesis should understand
the question, contribution, findings and limitations without reconstructing
the derivation. Retain numbers and notation when they communicate a critical
result; simplify material whose interpretation depends on earlier definitions.

## Changes

- The abstract distinguishes independent samples from nearly independent
  variables. Its method paragraph connects the new variance calculation to
  the standard error and the rejection cutoff without listing the cell and
  margin derivatives. Experimental coverage is described through the quantities
  varied, rather than counts of MI values. The findings separate approximation
  behaviour from the false-positive and detection results. Power is explained
  on first use, and the final sentence retains the shared-estimation limitation.
- Chapter 7 opens with the scientific comparison, mathematical contribution
  and overall assessment. That assessment no longer appears under RQ3.
- RQ1 states the dependence on both the mean and sampling variability of the
  estimated variances in words. It removes the symbol-heavy reminder comparing
  15.30 with 21.03; the fully explained example remains in Section 6.1.2.
  The near-independence finding is stated in the conclusion itself, with
  Appendix A supporting the explanation.
- RQ2 retains the critical 36.38% and 34.38% failure example against the 5%
  target, with a direct reference to its experimental setting in Section 6.2.
  The statement about complete computational validity now says that both
  methods return usable results in every repetition.
- RQ3 retains the power difference below 0.32 percentage points at 10,000
  observations per population across the tested settings. Bias cancellation
  and misleading estimated directions are explained without the sign convention
  and detailed trajectory of the sampling mean.
- The limitations preserve the assumptions, restricted population family,
  equal sample sizes, fixed power baseline and direction, nominal-level power
  comparison and application scope. They use ordinary descriptions of the
  category and sampling restrictions instead of the earlier symbols and labels.
- Future work retains improvements to the mean approximation, the MI difference
  and standard error, the near-independence reference distribution, and broader
  population and sampling checks. No new experiment or scientific claim is added.

The abstract is approximately 255 prose words, compared with 260 previously;
the conclusion is approximately 1,012, compared with 1,105 previously. These
counts treat inline mathematics as a token and are descriptive, not targets.
Sentence breaks follow explanatory relationships rather than a length quota.

## Source review

Both revised sections were reread in full. The remaining distinctions include
approximation accuracy versus false-positive accuracy, observed sampling
moments versus a single sampled estimate, and two-sided rejection versus the
estimated direction of an MI difference. The conditional claims about sparse
samples, near independence and the tested population settings are retained.

Only the abstract and conclusion changed during this revision; the other 109
packaged source files, including all derivations, results, figures, tables,
appendices, bibliography and typography, match the baseline. The previously
approved acknowledgement wording is preserved and included in the rebuilt PDF.
All 164 active reference occurrences resolve against 137 unique labels, and
all 46 citation keys resolve. Paragraph-style and whitespace checks pass.

## Build and PDF review

The main and named delivery PDFs were rebuilt successfully and match byte for
byte. The thesis remains 104 pages. Only the abstract, acknowledgements and four
conclusion pages have changed extracted text; all other pages retain their text
and pagination. The six changed pages and eight surrounding or front-matter
pages were visually inspected. A final wording refinement affected only the
last conclusion page, which was rendered and checked again.

The final LaTeX log has no warnings, overfull or underfull boxes, or missing
characters. All 905 internal page links have valid destinations, and no text
extends outside the page bounds. The source archive and delivery checksums were
refreshed. The unchanged experimental archive was reused after its full checksum
and all 37,649 input files' inventory, sizes and exact modification times were
verified against the recent full delivery verification. Protected presentation
and historical draft PDFs remain unchanged.
