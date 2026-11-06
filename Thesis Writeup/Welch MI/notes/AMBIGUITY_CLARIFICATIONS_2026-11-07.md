# Ambiguity clarifications and verified rebuild, 7 November 2026

The user authorised the eight wording changes identified in the latest
ambiguity review, validation after editing, and publication of the rebuilt
PDF through the existing scoped commit-and-push workflow.

## Changes and contextual validation

1. Chapter 6's discussion now describes tables with uniform margins,
   avoiding the implication of equal joint-cell probabilities. The stated
   positive MI and numerical example are preserved.
2. The Chapter 5 power comparison explicitly names the p-value threshold
   of 0.05, distinguishing it from the larger test-statistic cutoff used
   by Expanded Welch.
3. The Chapter 6 variance comparison now names the average squared
   standard error, preserving its comparison with the observed sampling
   variance of the estimated MI difference.
4. Chapter 4 states that an unsuccessful calculation cannot be used to
   draw a test conclusion. This remains distinct from counting failures
   as non-rejections when reporting simulation rates.
5. Appendix A.2 identifies substitution of the approximate sampling moments
   into the moment-matching formula, replacing the ambiguous reference to
   keeping both terms. The approximation and all displayed algebra remain.
6. The different-skew null discussion replaces the recovery of unnamed
   estimates with diminishing bias in the estimated MI difference and
   changes in its estimated standard error relative to the difference's
   sampling standard deviation. The wording does not imply that both
   estimation errors decline monotonically or that increasing sample size
   guarantees rejection near 5% throughout the plotted range.
7. The shopping application explains the absence of smoothing as retaining
   zero cells without adding artificial counts to empty cells. Appendix
   B.2 uses the same description for the simulations.
8. Appendix A is titled Supporting MI Derivations. Its introduction now
   identifies the first two calculations as supporting the near-independence
   analysis, preserving the broader scope of the final positive-MI proof.

All affected passages were reread with their surrounding explanations and
compared with the previous source. These are local clarity changes; the
calculation requirements, simulation denominators and statistical claims
retain their meaning.

## Verification and delivery

- All five existing thesis-consistency tests pass.
- Every displayed and inline mathematical expression, citation, label,
  reference, LaTeX environment and figure-dimension command in the five
  edited files is preserved. Numerical tokens are unchanged except for
  explicitly repeating the existing 0.05 p-value threshold in Chapter 5.
- All 180 source references resolve against 154 unique labels. Australian
  spelling, shared paragraph style and whitespace checks pass.
- The packaging build completed without LaTeX warnings, overfull or
  underfull boxes, or missing-character messages. The thesis remains
  109 pages.
- Eleven PDF pages have changed text. Those pages and five adjacent pages
  were rendered and visually inspected, including the contents, both
  application tables, the discussion transition and the appendix headings
  and equations. No layout correction was required.
- The compiled, main and named delivery PDFs are identical. The source
  archive matches every current source input, and the refreshed PDF and
  source checksums match their files. Packaging verified and reused the
  unchanged experimental supplement.
- A comparison of 635 saved hashes finds only the five approved manuscript
  files and four rebuilt outputs changed. The other 626 files match,
  including the abstract, conclusion, Chapter 2 derivation benchmark,
  figures, bibliography, historical files, inspected code and separate
  personal study guide.

The scoped build commit includes the five manuscript files, four refreshed
outputs and this review record. The separate `output/` directory is excluded.
