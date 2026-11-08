# Targeted clarification revision — 2 November 2026

The user approved the recommended edits from the sentence-review assessment,
including consideration of its three optional improvements. This is a targeted
source revision, not a new general prose pass or a PDF rebuild.

## Plan

| Review point | Planned change | Constraint |
| --- | --- | --- |
| 1 | Explain the opposing effects of the two near-independence substitutions and their net upward error in the mean estimated degrees of freedom. | Base the explanation on successive calculations within each saved repetition, not ratios of mean inputs. Do not add the intermediate diagnostic numbers to the manuscript. |
| 2 | State that the sampling means at MI 0.05 remain roughly 6% above the population pointwise-MI variances. | Retain the separate finding that the variance predictions are close to the observed sampling variances. |
| 3–4 | Identify the mean-zero linear term and the covariance between observation contributions precisely. | These two specifically approved sentences are the only changes within the Section 2.3 derivation benchmark. Keep all algebra and displayed equations. |
| 5 | State the wrong-sign rejection result using the estimated MI difference explicitly. | Retain the true negative difference, positive estimation bias and two-sided interpretation. |
| 6 | Separate restrictions shared by the null and power studies from the power study's fixed starting MI and direction of change. | Do not imply that either broad study covers alternative constructions or unequal within-table margins. |
| 7 | Keep the sample-substitution finding with the general approximation comparison and remove its misleading attachment to the near-independence recap. | Preserve both the general finding and the near-independence explanation without another numerical example. |
| 8 | Describe the larger-gap power ordering directly once bias diminishes. | Retain the qualification about bias; do not imply the same ordering in the biased small-sample range. |
| 9 | Anchor the RQ1 conclusion with the existing population first-order value 15.30 and moment target 21.03. | Identify population P, table size, margins, MI and sample size. Do not add a new result or table. |
| 11 | Remove the final sentence that restates the moment-target definition for Q. | Retain the observed P/Q ordering. |
| 12 | Present Hutcheson's entropy comparison as a precedent for a Student t approximation and identify the role of the MI-specific derivatives directly. | Retain the literature discussion and citation; make no claim that it is the nearest or uniquely relevant prior method. |
| 13 | State the fixed-category derivation's scope directly. | Do not extend the derivation to growing alphabets or continuous estimators. |
| 15 | Identify a reference distribution for the MI difference as the possible use of the quadratic sampling approximation. | Keep this a future research direction, not a validated test or an additional formula. |
| 16 | Remove the final population-scope reminder. | Keep the proposed application-population simulations. |
| Strict comparisons | Allow equality when describing Expanded Welch's rejection rate and power relative to Wald. | Retain the larger-cutoff mechanism and the observed method separations. |

Leave review points 10, 14 and 17 unchanged. Retain the explicit Taylor
mappings, product-rule steps, nested-sum explanations, figure-row structure,
near-independence investigation and weekend interpretation. Add no footnote
example, new simulation, figure, table or reference.

## Verification plan

Read every changed paragraph together with its neighbours. Check that each
connector preserves the distinction between an exact relation, an empirical
finding and an approximation. Verify the added numerical reminder against
the saved approximation-study moments. Preserve displayed mathematics,
headings, labels, citations, existing reference targets, figure dimensions,
typography, appendices and all unaffected source files. Run the paragraph
style and source consistency checks, then review the diff once more.

Keep the existing PDF and delivery files unchanged until a rebuild is
explicitly requested. Do not commit or push this revision without a request.

## Completion

Implemented the planned edits in the abstract and Chapters 1, 2, 6 and 7,
including the modest improvements in points 8, 9 and 15. Fifteen paragraph
units changed; their existing boundaries remain intact. The sample-substitution
finding now accompanies the general approximation comparison in the RQ1
conclusion, while the following paragraph focuses on near independence.

The final context review retained short sentences for the two precise
derivation statements and retained the developed figure-row explanation.
It also made the population-specific sampling variances explicit after the
new roughly-6% mean comparison and used the complete name Student t
distribution when describing the approximate entropy-test reference.

Verification completed:

- The successive substitution effects were checked within each of the
  100,000 saved repetitions for both populations at MI 0.01, 0.02 and
  0.05. Chunk checksums and the component formula agree. The denominator
  substitution raises the mean estimated degrees of freedom, and the
  subsequent MI substitution partly offsets that increase in all six
  population/settings comparisons. No new samples were generated.
- At MI 0.05, the observed means exceed the population pointwise-MI
  variances by 6.58% in P and 5.74% in Q, supporting the approximate
  prose comparison. The Chapter 7 example matches the existing saved
  values 15.2955 and 21.0311 before rounding to 15.30 and 21.03.
- All 48 displayed equation, figure and table blocks in the five modified
  manuscript files are unchanged. Existing headings, labels, citations,
  reference targets and environment sequences are preserved. Inline
  notation changes consist only of the substitution reminders, the existing
  numerical example and removal of the redundant Q sentence.
- Recursive inspection of the 18 active TeX inputs resolves all 164
  reference occurrences against 137 unique labels and all 46 citation
  keys against the bibliography.
- The Section 2.3 benchmark differs only in the two approved sentences.
  Sections 6.1.1, 6.1.2 and 6.4, the pointwise-interval paragraph, both
  appendices, the figures, bibliography, typography and 124 other inventoried
  source/assets are unchanged. Review points 10, 14 and 17 were left alone.
- The paragraph-style check and whitespace check pass. All 15 changed
  paragraph units were reread with their neighbouring text.

The PDF and delivery-file sizes and exact modification times remain
unchanged. No LaTeX build, package refresh, commit or push was performed.
The new source therefore awaits the next explicitly requested PDF rebuild.

## Final-delivery rebuild and review

Later on 2 November, the user explicitly requested a rebuild with the care
appropriate to a final copy. The full packaging procedure was run, followed
by the native delivery check, rather than reusing the interim supplement
verification shortcut.

- The rebuilt main and named thesis PDFs are identical: 104 A4 pages,
  757,963 bytes. The final compilation log has no warnings, overfull or
  underfull boxes, or missing-character messages.
- Every page was rendered and visually reviewed, including the contents
  lists, equations, all figures and tables, appendices and bibliography.
  No defect requiring a manuscript or layout change was found.
- All fonts are embedded, with no Type 3 fonts. No extracted text falls
  outside the page bounds; 907 internal hyperlink page destinations are
  valid. The extracted manuscript has no unresolved-reference markers or
  draft placeholders.
- The delivered source ZIP was extracted into an isolated temporary
  directory and built without the workspace's local build configuration.
  Its final log is clean. Its extracted text, page breaks and all 104
  rendered page images match the main build exactly.
- The full archive checks match all 111 source-archive entries and 37,649
  evidence-archive entries against their current source files. The evidence
  ZIP is 12,670,746,690 bytes. Delivery checksums and instructions pass the
  native verification.
- The packaged source files did not change during the rebuild. Evidence
  input inventories, sizes and exact modification times are unchanged.
  The separate presentation PDF and historical draft PDFs are unchanged.

No further manuscript edits, experiments, commit or push were made during
this rebuild. The main PDF, named PDF, source archive, evidence archive and
delivery checksums have been refreshed together.
