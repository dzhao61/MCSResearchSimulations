# Targeted depth pass: 6 October 2026

## Purpose

Develop the interpretation of the focused study without broadening its
232-setting experiment or writing to a page target. Preserve the accessible
derivation style, short captions and discussion beside each lead figure.
The review found sufficient mathematical detail in Section 2.3 and Chapter 4;
those derivations do not need expansion in this pass.

## Edits and evidence

| Location | Addition | Verification |
| --- | --- | --- |
| Chapter 1 | A hypothetical categorical feature/class-label comparison across independent datasets. | Keep the target as equal population MI, not classification performance or equal complete distributions. |
| Sections 2.4-2.5 | Compare MI sampling variance, entropy-based Welch comparison and variability of an estimated variance; explain the remaining MI-specific calculation. | Existing first-order formulas, Hutcheson's checked component assignments, Pan and Wall's publisher abstract, and Brillinger's and Paninski's original papers. |
| Chapter 5 | Explain why the common positive-MI baseline, geometric table sizes, margin contrasts and sample-size sweeps answer the three questions. | The settings and construction remain those of the completed focused protocol. Avoid an empirical safety threshold or an optimal-design claim. |
| Sections 6.1 and 6.3 | Show the exact bias-difference identity and its numerical consequence for the falling detection curve. | Saved individual biases and difference means at 16x16, different skew, n=1000, MI pairs (0.02,0.02), (0.02,0.03), (0.02,0.04). Do not assume the bias is constant across alternatives. |
| Section 6.2 | Connect degrees of freedom to numerical Student t cutoffs and distinguish true-population from plug-in first-order variance. | SciPy quantiles at the reported median degrees of freedom; saved variance ratios; first- and second-order calculations already in Chapters 2/4 and Appendix A. The cutoffs illustrate medians, not every replicate's actual cutoff. |
| Section 6.3.2 | Relate the margin-related detection contrast to observed precision. | Saved standard deviations at 4x4, n=10000, MI pair (0.02,0.03), all three margin regimes. |
| Chapter 7 | Explain reporting and calibration in an application, including usable-output versus inferential reliability; develop the consequences of construction and equal-sample scope. | Existing findings and the algebra of the leading bias correction. No new validated selection rule. |
| Chapter 8 | State the knowledge contribution and prioritise future work by the failure it would address. | Agreement with the research questions, derivation and focused results. |

## Boundaries

- No new simulation, statistical method, population setting or figure.
- No wholesale transfer of supporting algebra or complete result tables into
  the main text.
- No repeated validity caveats, manuscript administration or length padding.
- Preserve all old working-draft sources and PDFs. This pass updates only the
  main manuscript; any later draft rebuild must be Working Draft v3.
- Correct the missing backslash in Appendix B's copying equation, without
  changing its construction.

## Acceptance checks

1. Recalculate every added numerical example from the existing records.
2. Verify the distinction between exact expectation identities and empirical
   or first-order approximations.
3. Check source attribution and the transition from literature to the method.
4. Build with resolved references/citations and no overfull boxes or errors.
5. Review the affected rendered pages, paragraphs and figure placement.
6. Run the relevant mathematical/report tests and independent evidence audit.
7. Refresh the named main-PDF/source deliverables, verify an isolated source
   build, and confirm that old working drafts and scientific inputs are unchanged.

Status: complete, verified 7 October 2026. The 87-page PDF contains 54
main-text pages. All 147 workspace tests, 65 extracted-package tests and the
independent raw-record audits pass. The clean source build has the same
extracted thesis text as the workspace PDF, with no warnings or unresolved
references. Rendered-page review and working-draft preservation checks pass.
The named main PDF, source and supplement are refreshed. Detailed results
are recorded in SUBMISSION_CHECK.md and SCIENTIFIC_AUDIT.md.
