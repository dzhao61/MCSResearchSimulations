# Chapter 4 derivation flow revision

## Agreed purpose and scope

The user authorised planning and executing a Chapter 4 revision after the
review identified five connections that were explained too late. Use the
Section 2.3 reading order and the consolidated research-prose guidelines:
state the target, explain why each intermediate quantity is required, show
the working, and interpret the result. Preserve useful algebra and the
distinctions between exact derivatives, first-order approximations, and
the Student t reference distribution approximation.

## Implementation plan

1. In Section 4.1, connect the exact Student t construction to the actual
   MI statistic by normalising its numerator and squared denominator with
   the population sampling variance. Use existing notation. Explain which
   terms correspond to Z and U/nu and preserve the approximate status of
   the MI reference distribution. Retain the full moment-matching and
   sample-size scaling calculations. Introduce the combining formula
   after the component inputs have acquired a meaning.
2. At the end of Section 4.1, link the remaining variance calculation to
   Section 2.3's sample-average argument. Explain why an observation-level
   effect is the quantity needed to describe variation across whole tables.
3. In Section 4.2, move the second-moment expression for V, the definition
   of its influence function, and its derivative decomposition ahead of
   the subsidiary derivatives. Establish the perturbation path before
   using it. Show how the resulting sensitivities will supply the sampling
   variance, then calculate the joint, marginal, pointwise-MI, MI, and
   second-moment changes with the existing intermediate algebra.
4. In Section 4.3, derive the empirical-table error and its linearisation
   before checking the sensitivity's sampling moments. Explain before
   substituting t=1 that the small displacement is the table error and t
   parameterises the path. Then verify the zero mean, derive the mean
   approximation, define the sensitivity variance, and derive the sampling
   variance. Place the positive-sensitivity-variance assumption beside
   the component formula that requires it.
5. Explain the change from population inputs to observed estimates, retain
   the three-role comparison table, and preserve the combining-rule proof.
   Keep the worked example, operational algorithm, and near-independence
   and theoretical-status discussion intact where they already explain
   their purpose clearly.

## Preservation and verification

- Preserve all existing displayed equations, labels, citations, numerical
  examples, and assumptions; moving equations may change their eventual
  printed numbers. Add only the mathematical identities needed for the
  missing connections.
- Preserve Section 2.3, the recent Chapters 2 and 3 revisions, the standing
  submission-copy instructions, and all existing PDFs.
- Reread the completed chapter for named referents, logical paragraph
  transitions, complete distribution names, Australian spelling, and
  Oxford commas. Check the exact/approximate distinctions at each step.
- Run source-preservation checks, the paragraph-style check, and the
  existing independent numerical derivation audit. Do not add tests that
  merely assert the new wording.
- This editing request does not request a PDF rebuild. Leave the verified
  108-page submission PDF available until the user requests the next build.

## Completed revision and checks

Implemented the plan in Sections 4.1–4.3. The combining formula now follows
the explanation of its component inputs. The variance derivative is
introduced as the target before its joint, marginal, pointwise-MI, and MI
ingredients are calculated. The whole-sample linearisation now precedes
the sampling-moment checks that use it.

The revised Taylor explanation identifies the table-probability errors as
the small displacement, explains the endpoint t=1, and explains derivative
linearity through fixed Taylor coefficients. Positive population cell
probabilities make V smooth locally, which supports the stated quadratic
and higher-order remainder interpretation.

The sentence and paragraph review checked the purpose of each new
calculation, named referents between sentences, approximation conditions,
Australian spelling, Oxford commas, and complete distribution names.
The normalised MI ratio is an algebraic identity. The early sampling-
variance relationship is explicitly a first-order result derived later
in Section 4.3. Moment matching is not presented as establishing the
independence needed for an exact Student t distribution.

Verification passed:

- All 64 original displayed equation and table blocks are preserved,
  allowing for their new positions. Two unnumbered explanatory displays
  were added; no original mathematical display was changed or removed.
- All labels, cited sources, and assumption statements are preserved.
  All reference targets resolve in the active sources, and LaTeX
  environments and braces are balanced.
- The worked example, operational algorithm, and behaviour and limitations
  section are byte-for-byte unchanged.
- The recent Chapter 2 and Chapter 3 edits, standing submission-copy
  instructions, and all existing PDFs are unchanged.
- All 11 existing independent numerical derivation-audit tests pass,
  including finite differences and the worked-example calculations.
- The paragraph-style check, regional-spelling scan excluding LaTeX
  identifiers, and `git diff --check` pass.

No PDF rebuild, delivery refresh, commit, or push was performed. Typeset
page breaks and revised equation numbers await the next requested build.

## Subsequent requested PDF rebuild

The user subsequently requested the rebuild and its completion on
8 November 2026. The final PDF has 109 pages, compared with 108 in the
previous submission copy. Chapter 4 occupies physical PDF pages 32–49,
and Chapter 5 begins on page 50.

The build review added two `samepage` groups to keep the row/column
derivative evaluation and the first-order expectation calculation with
their explanations. These changes affect page grouping only; the
mathematical text is unchanged. The final LaTeX log contains no warnings,
undefined references, or box warnings. Rendered pages 32–50 were reviewed,
including all of Chapter 4 and its transition to Chapter 5.

The read-only delivery check passes. The source archive has 117 entries,
and its Chapter 4 source matches the current manuscript exactly. The
unchanged experiment supplement was verified and reused.

The existing signature and 07/11/2026 date were restored to the rebuilt
signed PDF. Its compliance page is pixel-identical to the previous signed
copy, and all unsigned page contents are preserved. The signed document
retains the unsigned document's 70 bookmarks, 98 external links, 444
internal links, and 416 named destinations. All internal link targets and
named destinations were verified.

The signed deliverable and FINAL SUBMISSION thesis were refreshed with
byte-identical files. The previous submission thesis was backed up in
Archive, and the separate consent declaration and AI acknowledgement
files are unchanged.

Unsigned PDF SHA-256:
`726b42a941736f0992dc03a0f6dbc83f088988a666f0bf8f5cdf2a10c7edfb98`

Signed PDF SHA-256:
`e4c33520ba44bcdbf96e76946fb5cb1aa35a0f9d652ddcba4307cbaffda14bba`
