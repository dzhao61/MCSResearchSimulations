# Terminology clarity revision, 6 November 2026

The user authorised planning, implementing and validating the terminology
changes from the ambiguity review. This pass starts from the uncommitted
distribution-naming revision and preserves that work. The earlier five
general-review suggestions remain deferred. No main PDF rebuild or delivery
refresh is requested.

## Plan

| Term | Intended change | Preservation requirement |
| --- | --- | --- |
| Calculation validity | Define calculation success by the existing numerical requirements; use that name for success rates, statuses and figure strips. | Preserve every numerical requirement, denominator, treatment of unsuccessful calculations and selection of finite values for diagnostics. Keep statistical validity in the permutation discussion. |
| Independence | Identify the samples, the variables within a population, or the variables in the Student t construction where the relationship could be unclear. | Preserve all independence assumptions and probability models. |
| Common | Use shared for equal population MI or table dimensions and same for thresholds shared by methods. | Keep common when it means frequent or denotes an algebraic common factor. Preserve identifiers. |
| Regular | Name the positive sensitivity-variance assumption and state the applicable fixed-table conditions in the asymptotic discussion. | Preserve the positive-cell, positive-variance and local-alternative conditions. |
| Conservative | Explain the false-positive meaning at the introduction's first use. | Keep the distinction between lower rejection and better calibration. |
| Reference | Complete the identifying noun in the MI and ordinary Welch passages. | Keep the reference distributions and the supporting role of ordinary Welch. |
| Sensitivity and skew | Clarify the observation-level effect in the introductory contribution and explain the meaning of the existing skew regime names. | Keep the influence-function definition and the three named regimes. |

Update the two active null/power figure generators and regenerate their six
figures from existing summaries. Do not rerun experiments or change plot
dimensions, scales, curves or numerical labels.

## Validation plan

- Compare the edited passages with the source snapshot taken before this
  pass, including surrounding definitions, assumptions and conclusions.
- Verify displayed algebra, numerical evidence, citations and LaTeX labels.
  The performance table's text labels may change, but its fractions and
  denominators must retain the same meaning.
- Verify that Section 2.3, the abstract, experimental result inputs and
  published delivery files are preserved.
- Compare figure evidence and rendered plots, allowing only the intended
  labels to differ; inspect the longer calculation-success labels visually.
- Check Australian spelling, remaining ambiguous uses, paragraph style and
  whitespace. Record the outcome after the final contextual reread.

## Implementation and contextual review

Completed in eight manuscript files, the two active null/power figure
generators and their six figures. The workspace writing instructions now
record the terminology distinctions for future revisions.

Calculation success is defined by the existing numerical requirements.
The definition, performance table, results, conclusion, appendix and figure
strips use the same term. The former data fields and Boolean masks retain
their identifiers and values. Rejection rates still divide rejections from
successful calculations by all repetitions, with unsuccessful calculations
counted as non-rejections. Finite MI differences and finite zero variance
estimates remain in the diagnostic calculations under the original rules.

The contextual reread confirmed the following distinctions:

- RQ1 names independence between X and Y. The Student t construction names
  independence between Z and U, while statements about independent samples
  retain that separate relationship. Appendix A now identifies the product
  of empirical row and column probabilities instead of calling the margins
  independent.
- Shared MI is introduced as the MI value shared by the two populations.
  Common remains in the frequency description of categories and in the
  algebraic common factor.
- The sensitivity assumption names its positive variances. The asymptotic
  discussion explicitly concerns sample sizes tending to infinity under
  the stated assumptions. Appendix A retains fixed dimensions, positive
  limiting cell probabilities and the stated local alternatives in place
  of the generic phrase regular models.
- The first use of conservatism explains that rejection rates already below
  5% are reduced further. The MI reference distribution and the reference
  distribution with ordinary Welch degrees of freedom are named explicitly.
- The introductory contribution describes the effect of an observation on
  the pointwise-MI variance. The existing influence-function definition is
  preserved. The skew labels are retained and explained as uneven category
  probabilities without an assumed numerical ordering of category labels.

## Validation outcome

- All displayed mathematics is byte-identical to the snapshot before this
  pass. Existing inline mathematical quantities are preserved. Only the
  two intended text labels in the performance-table fractions change; the
  events counted and denominators retain their definitions.
- All reported numerical evidence, citations, LaTeX labels and structural
  commands are preserved. One additional 5% reminder explains conservatism
  in the introduction.
- Chapter 2, including Section 2.3, and the abstract are unchanged in this
  pass. The preceding distribution-naming edits remain intact.
- Figure evidence files, the compact diagnostic table and the experimental
  input hashes are unchanged. The plot generators differ only in display
  text and one docstring. No experiments were rerun.
- Before/after renders of all six figures have identical dimensions.
  Curves, axes and numerical labels are pixel-identical outside the intended
  text changes. All six figures were visually inspected: the longer
  calculation-success labels fit and do not cover the curves.
- Australian-spelling, source-reference, paragraph-style and whitespace
  checks pass. The remaining statistical use of validity in the permutation
  discussion is preserved, as are internal reference identifiers.
- The main PDF and every published delivery file have unchanged hashes.
  Manuscript pagination and the assembled table layout await an explicitly
  requested rebuild.

The final reread found the revised terms consistent with their equations
and experimental use. The earlier general-review recommendations remain
deferred.
