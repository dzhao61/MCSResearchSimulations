# Repeated qualifications and signed thesis rebuild: 8 November 2026

Applied the approved removals and direct rewrites, preserving item 6's
plot-reading explanations.

- Introduction: removed the sentence after the hypotheses that repeated
  equal MI and qualified it by allowing different joint probability tables.
- Section 2.4: retained the equal-MI hypothesis and removed its repeated
  qualification about different cell probabilities. The substantive
  explanation in Section 2.1.2 and the permutation-test discussion remain.
- Section 3.1: removed the closing aside about an alternative correction
  based on occupied cells. The declared-category rule and its explanation remain.
- Section 4.1: removed the repeated statement of the Student t construction's
  conditions. The conditions immediately before the equation and the full
  theoretical-status discussion in Section 4.5 remain.
- Section 4.3: removed the zero-variance calculation aside from the rejection
  comparison. Section 4.5 and Appendix B.3 retain the calculation requirements.
- Section 6.4: removed the closing paragraph about unknown population tables
  preventing direct assessment of degrees-of-freedom targets and false positives.
  The corresponding limitation remains in Chapter 7.
- Sections 6.2.4 and 7.1.2: replaced the general warning about agreement with
  the direct finding that the tests' rates can be similar while remaining
  below the 5% target. The numerical comparisons remain.
- Section 7.1: stated that neither test provides evidence of a weekend–purchase
  MI difference. The fuller non-rejection interpretation remains beside the
  application result in Section 6.4.

## Source and evidence checks

Verified unchanged displayed equations, tables, figures, citation keys,
labels and reference targets. Section 2.3, the appendices, experimental
inputs and the two plot-reading passages excluded from the requested
changes remain unchanged. Australian spelling and paragraph-style checks pass.

Checked the large-sample wording against the saved null-study results for
16-by-16 tables, shared MI 0.005 nats and 50,000 observations per population:

| Margin regime | Wald false-positive rate | Expanded Welch false-positive rate |
| --- | ---: | ---: |
| Uniform | 3.427% | 3.398% |
| Same skew | 3.652% | 3.584% |
| Different skew | 3.659% | 3.600% |

## Rebuild and signed copies

Built using `package_deliverables.py --no-push`. The final PDF remains
109 pages, with no LaTeX warnings, overfull boxes or underfull boxes.
Visually reviewed every page affected by text changes or reflow: physical
PDF pages 10, 22, 29, 34, 45, 74, 83, 84, 85 and 86.

The main and named unsigned PDFs match, and the refreshed source archive
matches the active manuscript. Packaging verified and reused the unchanged
experiment supplement.

Transferred the existing signature and corrected date, 07/11/2026, onto the
rebuilt PDF using an incremental update. All original page-content streams
and original unsigned PDF bytes are preserved. The signed compliance page
is pixel-identical to the previous signed page, and the signing-area check
finds no other visual changes. Navigation is preserved: 70 bookmarks,
450 internal links, 98 URL links and 417 named destinations.

Updated the signed copy in `deliverables/` and the thesis in
`FINAL SUBMISSION`; the two copies are byte-identical. The previous signed
submission is backed up in the Research archive. The other submission
documents were not changed.
