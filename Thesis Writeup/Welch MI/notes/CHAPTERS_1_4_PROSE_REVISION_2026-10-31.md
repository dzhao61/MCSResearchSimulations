# Chapters 1–4: prose revision and preservation

Implemented on 31 October 2026 following the user's approval of the
[revision plan](CHAPTERS_1_4_PROSE_REVISION_PLAN_2026-10-31.md) and instruction
to retain the literature discussions. The pass applies the
[research prose guidelines](RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md)
to the current sources, preserving improvements already made in earlier
turns. No PDF rebuild or Git commit was requested.

## Review decisions and changes

| Chapter | Reading difficulty addressed | Revision |
| --- | --- | --- |
| 1: Introduction | A vague “This” followed the lower-rejection finding, and the scope paragraph used two sentences to establish the categorical-table setting. | Named the lower rejection rate directly and connected the scope to the aligned count tables. The already connected sampling-variation explanation, questions, contributions and outline were retained. |
| 2: Background and literature | Some literature transitions introduced a generic observation before explaining the estimator, or left the relevant uncertainty or calculation implicit. | Connected missing categories to the coverage adjustment; introduced the specialised sampling regime directly with its estimator; named the changing rare-cell probabilities and the normal limit; clarified the parallel regression and MI variance calculations; connected Bayesian uncertainty to its model; and explained the cell and margin changes needed for MI-specific degrees of freedom. |
| 2: Hypotheses and contribution | Punctuation carried part of the relationship between equal MI and permutation validity, while the evaluation was announced before its immediate reason. | Expressed the hypothesis and permutation qualification through explicit connections. Ended the chapter by deriving the need to evaluate estimation errors from the finite-sample limitations already described. |
| 3: Test overview | “It”, “their difference” and “estimated effect” required the reader to infer the relevant assumption, correction or estimate. The shared-input/different-reference comparison was stated twice. | Named the positive-MI assumption, difference between corrections and bias-corrected MI difference. Retained one complete explanation of the shared statistic and differing reference distributions. Introduced the remaining variance input explicitly as a first-order approximation. |
| 4: Derivation | Some equation lead-ins named a step without identifying its role, and the interpretation of relative variability used an ambiguous “the estimate”. | Connected the second-moment calculation to the preceding MI derivative; named the probability-weight and pointwise-MI terms in the product rule; explained the row-indicator calculation; connected independent observations to vanishing covariance terms in the variance approximation; and named the fluctuating variance estimate. |
| 4: Targets and limitations | Table 4.1's introduction referred only to “the three quantities” and “the first two”; the near-independence transition used a generic appendix reminder. | Named the moment target, population approximation and sample estimate, including which are fixed and which vary. Connected the fixed-margin expansion directly to the quantities and local relations it supplies. |

All literature approaches remain, including the alternative estimators,
Bayesian uncertainty, regression precedents, Hutcheson comparison and
resampling alternatives. Their substantive findings and qualifications
are retained. No citation or literature topic was removed in response to
the earlier discussion of optional shortening.

Short definitions, mathematical cancellations, substitutions and distinct
decisions remain separate where that helps the calculation. One long
interpretation of relative variability was split so that the small- and
large-fluctuation consequences remain easy to follow. Neither sentence
length nor a reduction in page count was an editing target.

## Preservation and verification

The preceding four chapter sources, README, writing instructions and plans
are preserved in
`archive/before_chapters_1_4_prose_implementation_2026-10-31.zip`.
The older `before_chapters_1_4_prose_revision_2026-10-31.zip` is unchanged.
Checks are recorded in
`CHAPTERS_1_4_PROSE_REVISION_VERIFICATION_2026-10-31.json`.

- Section 2.3 is byte-identical to the starting source. Figure 2.1's
  discussion and the whole Section 4.4 worked example, algorithm and
  complexity explanation are also byte-identical.
- All 113 figure, table and mathematical display blocks are byte-identical,
  including captions, dimensions, placement settings and intermediate
  algebra. All distinct inline expressions and numerical values are
  preserved, together with headings, labels, citation sequence and
  reference occurrences. Paragraph boundaries are preserved.
- All 120 protected manuscript, asset and delivery files are unchanged.
  These include Chapters 5–7, appendices, typography, the existing PDF and
  delivery packages. Small files are hash-checked; the large supplement is
  checked by size and exact timestamp.
- The active input graph contains 21 TeX files and 140 unique labels,
  with no missing inputs, dangling references, missing citations or
  unbalanced braces/environments. No direction to unsubmitted evidence
  was introduced.
- Paragraph-style checks, all five existing thesis-consistency tests and
  whitespace checks pass. The revised passages were reviewed with their
  surrounding explanations for preserved assumptions, approximation
  strength and causal claims.

The README, plan status, high-impact-plan pointer and writing instructions
now identify this as an implemented source revision. The submitted PDF
and delivery archives still await an explicit rebuild request. At that
build, inspect the affected pages for line breaks, display order and page
breaks; source checks alone do not verify typeset layout. No simulation,
fitting, bootstrap or delivery publication was performed.
