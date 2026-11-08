# Chapter 4 local transition edits — 8 November 2026

The user authorised the two identified flow improvements and questioned
the purpose of the summation following the probability derivatives.

## Changes

1. Consolidated the explanation following the definition of the variance
   sensitivity in Section 4.2.1. Retained the derivative's meaning,
   linearity in the table change, observation averaging, individual
   contribution divided by sample size, and sampling-variance preview.
   A single forward reference replaces the two repeated references to
   Section 4.3.
2. Replaced the four-equation-reference opening in Section 4.2.3 with the
   operation being performed: subtract the derivative of squared MI from
   the second-moment derivative. The next sentence identifies the
   probability-weight term being combined with the derivative of negative
   squared MI. The algebra and subsequent assembly remain unchanged.
3. Explained that summing the joint-cell derivatives checks conservation
   of total probability. Expanded the existing zero-sum identity to show
   the derivatives on its left-hand side, connecting the check directly
   to the preceding cell-level derivative. The equation's value and its
   position in the derivation are unchanged.

## Validation

- Reread the edited passages with their preceding definitions, displays,
  following calculations, and subsection transitions.
- All 11 existing independent derivation-audit tests passed.
- All but one mathematical/table display are unchanged. The sole expanded
  display retains the original equality and adds the summed derivatives
  that its right-hand side already evaluates.
- Labels and citation occurrences are unchanged. Section 4.3 onwards,
  including the worked example and limitations, is unchanged.
- Paragraph-style, Australian-spelling, and `git diff --check` checks passed.
- The main PDF, named unsigned and signed PDFs, and FINAL SUBMISSION PDF
  retain their pre-edit hashes.

This is a source-only revision. No PDF rebuild, packaging refresh,
commit, or push was requested or performed. Verification evidence is in
`/private/tmp/welch-chapter4-local-flow-2026-11-08-8krnc3tb/`.

## Subsequent requested rebuild and submission check

The user then requested a PDF rebuild and another submission-readiness
check. The final PDF remains 111 pages and compiles without warnings,
undefined references, missing characters, or overfull/underfull boxes.

The initial visual review found that a page break separated the variance
preview's introductory sentence from its final phrase. A `samepage` group
now keeps the complete introductory sentence, equation, and immediate
explanation together. The grouping changes no wording or mathematics.

Rendered and inspected physical pages 5–8 and 33–51, covering the complete
contents, Chapter 4, and the Chapter 5 boundary. Inspected the three changed
pages at full size. The expanded conservation identity fits within the
margins, the revised transitions read continuously, and no new layout
issues remain.

A comparison of every page's extracted text and word positions shows
changes only on physical pages 36, 37, and 40. All other pages match the
version covered by the preceding complete submission review. The document
retains 105 bookmarks, 456 named destinations, and 98 external links. All
477 internal links resolve; four redundant references were removed by
the prose edit. The front-list links remain correct.

The delivery-package check passed. The refreshed source archive has 117
entries and matches the current manuscript. Comparing archive contents
with the previous committed source package shows only Chapter 4 changed.
The unchanged experiment supplement was verified and reused. No statistical
code, numerical results, or other manuscript content changed, so the
preceding 317-test final audit remains applicable alongside the 11
derivation checks recorded above.

Preserved the authorised signature and date, 07/11/2026. The signed
compliance page renders pixel-identically to the preceding signed copy,
and the signed PDF preserves every rebuilt page's contents and navigation.
The separate consent declaration and AI acknowledgement were visually
checked and retain their previous hashes. The signed deliverable and
FINAL SUBMISSION thesis are byte-identical; the previous submission PDF
was backed up in the parent Research archive before replacement.

Build, comparison, and publication evidence:
`/private/tmp/welch-chapter4-local-flow-build-2026-11-08-q1fzbn93/`.

- Unsigned PDF SHA-256: `91c5e0abaace5037f4a3c2ebf08cb767cccc352c8c4d67aec863aca411822177`.
- Signed PDF SHA-256: `163f34b602bed9f868398a7175e0653a1882ea7658ca3b641a60c71141b54a59`.

The source edit, verified build, signed deliverable, and this review record
are included in the requested automatic commit-and-push step. The local
submission check found no remaining issue requiring an edit. Portal
similarity results and upload confirmation are outside this file check.
