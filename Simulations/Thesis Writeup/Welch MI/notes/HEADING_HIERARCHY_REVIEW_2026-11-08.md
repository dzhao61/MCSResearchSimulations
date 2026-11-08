# Heading hierarchy review — 8 November 2026

The user requested consistent treatment of numbered subsections and
unnumbered bold headings, without subsubsections. The review covered the
active front matter, seven main chapters, both appendices, and generated
figure sources. It did not request a PDF rebuild.

## Rule applied

- Number substantial topics, methods, and derivation stages that readers
  should be able to find in the contents.
- Use local bold headings for proof directions, worked illustrations, and
  brief qualifications within an existing topic.
- Judge the role of the passage rather than its length. Avoid redundant
  consecutive headings and sole subsections that repeat their parent.
- Let subsection commands provide their spacing. Use the existing
  `\thesisminiheading` command for local bold headings.
- Do not introduce subsubsections.

## Source changes

| Location | Treatment |
| --- | --- |
| Chapter 2 | Numbered the two estimation topics, the three sampling-variance derivation stages, and the three testing approaches. Retained the short independence-boundary qualification as a local bold heading. |
| Chapter 3 | Numbered the problem setup and estimator, and the Wald p-value and Student t distribution motivation, as paired topics. |
| Chapter 4 | Applied the same numbered hierarchy to the reference-distribution construction, moment matching, worked test calculation, algorithm, near-independence behaviour, and calculation requirements. Retained the existing derivation subsections. |
| Chapter 5 | Numbered population construction and the experimental table-size/margin settings. Kept the worked construction example within its parent topic. |
| Appendix A | Numbered the independence and small-positive-MI arguments, and the positive-table equivalence and positive-cell requirement. Kept proof directions and the numerical illustration as local divisions. Removed the introductory bold heading immediately beneath the equivalence subsection because the opening prose already explains that distinction. |
| Appendix B | Numbered the distinct diagnostic quantities and the separate moment-target and uncertainty calculations. Named the first diagnostic subsection explicitly to distinguish MI-difference diagnostics from sampling variability of the pointwise-MI variance estimate. |

No changes were needed to headings in Chapters 1, 6, or 7, the front
matter, or the generated figure sources. Table column headings,
contribution-list labels, and declaration fields remain outside the
section hierarchy.

The six remaining local bold headings have these roles:

1. Chapter 2: the independence boundary qualifies the preceding first-order
   sampling-variance result.
2. Chapter 4: table-based component degrees of freedom complete the
   population-to-estimated comparison within one subsection.
3. Chapter 5: the worked two-by-two example illustrates the construction
   already established in the parent subsection.
4. Appendix A: the zero-variance-to-zero-MI direction is one part of the proof.
5. Appendix A: the reverse direction completes that proof.
6. Appendix A: the worked two-by-two example illustrates the equivalence.

The Chapter 4 worked comparison is a numbered subsection because it
presents a complete application of both tests, separate from the general
implementation algorithm. The local construction and proof examples
instead illustrate the argument within their parent subsection.

## Validation

- Compared all 13 active front-matter, chapter, and appendix sources with
  their pre-edit snapshots. After removing subsection/local-heading
  commands and heading-associated spacing, the remaining source is
  identical, including the mathematical displays and scientific prose.
- Confirmed that labels, references, and citations are unchanged and in
  their original order. The body of the Section 2.3 derivation benchmark
  is unchanged.
- Confirmed that no subsubsections, sole numbered subsections, or extra
  `\medskip` commands immediately before subsections remain.
- Reviewed the added titles for meaning, Australian English, and the
  complete naming of distributions.
- `package_deliverables.py --check-style` passed.
- `git diff --check` passed.
- SHA-256 checks confirmed that the main PDF, signed deliverable, and
  FINAL SUBMISSION PDF are unchanged.

The detailed comparison is stored in the task's temporary review record:
`/private/tmp/welch-heading-hierarchy-2026-11-08-y6poxso_/hierarchy-verification.json`.
The consolidated writing guide and both applicable AGENTS files now
record the hierarchy rule. No build, PDF layout review, commit, or push
was performed for this source-only task. The next explicitly requested
rebuild should check the contents pages and the affected heading locations.

## Subsequent requested PDF rebuild

The user then requested a rebuild. The verified PDF has 111 physical
pages, compared with 109 before the hierarchy changes. The contents now
occupy four pages instead of three, and the body occupies one additional
page. No scientific prose or mathematics was added or removed.

The build exposed PDF-bookmark warnings in the two new Student t
distribution subsection headings. The headings now use `\texorpdfstring`
to retain the printed italic letter while providing plain bookmark text.
Navigation validation also found that the existing figure-list and
table-list entries both targeted the acknowledgements. The preamble now
adds an anchor after the AMS front-list page break and before its contents
entry. Both entries now point to their respective lists on physical
pages 9 and 10. The final build has no LaTeX warnings, unresolved
references, or overfull/underfull boxes.

Rendered and visually inspected 36 affected pages, including all 28 added
subsection locations, the complete contents and front lists, and the
retained local-heading examples. Heading detail views confirmed readable
titles and their connection to the opening prose. The 105 bookmarks and
all 481 internal links resolve; the 98 external links retain their URI
actions. The scientific source comparison again confirms that the prose,
mathematics, labels, references, and citations are unchanged.

The refreshed source archive contains 117 entries and matches the active
manuscript sources. Packaging and paragraph-style checks passed. The
unchanged experiment supplement was verified and reused.

Preserved the existing signature and date, 07/11/2026. The rebuilt signed
compliance page renders pixel-identically to the previous authorised
copy, and the signed PDF preserves every rebuilt page's content and
navigation. The signed deliverable and FINAL SUBMISSION PDF were replaced
with byte-identical verified copies; the previous submission PDF was
backed up in the parent Research archive. Other submission documents are
unchanged.

Build and review evidence:
`/private/tmp/welch-heading-hierarchy-build-2026-11-08-mqq02541/`.

- Unsigned PDF SHA-256: `25188790e2632b23021056fe9a3c4a4345fd3d25524cf9030878d40221711b88`.
- Signed PDF SHA-256: `14e831aebab809d9353f727fa426ec88433e2cde225c42f92e4d2ac73f853d89`.

The verified build, signed deliverable, heading guidelines, and this review
record are included in the requested automatic commit-and-push step.
