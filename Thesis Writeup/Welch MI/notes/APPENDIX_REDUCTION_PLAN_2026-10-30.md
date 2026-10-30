# Plan: remove Appendix C and retain essential supporting material

30 October 2026. Planning only: no manuscript edits, PDF rebuild or delivery refresh has been performed for this plan.

## Intended outcome

The submitted thesis should contain two appendices: A for near-independence mathematics and B for essential experimental construction, validity and uncertainty calculations. Remove Appendix C as a whole and preserve its current contents in the experimental supplement.

The current PDF has 122 pages, including six pages of Appendix A, nine of B and eleven of C. Removing C is the principal reduction. Final savings depend on the small main-text additions, B cuts and regenerated front matter; do not promise a final page count before building.

The main argument must remain understandable and assessable without opening the supplement. Keep decisive evidence beside its interpretation. The supplement may contain fuller diagnostics and secondary comparisons, but must not become the sole support for a central conclusion.

## 1. Preserve the current material first

- Archive the pre-edit manuscript source and current PDF.
- Preserve the current eleven-page C as a readable PDF, together with its source, nine external table inputs and the inline Holm table, in a new dated supplementary folder. Record the original numbering and provenance.
- Keep the older nineteen-page supplementary Appendix C unchanged. It is a historical version and does not contain the exact current appendix.
- Retain all experiment outputs and analysis code. This change requires no new simulations, fitting batches or bootstrap runs.

## 2. Resolve Appendix C's dependencies before removing it

The current appendix defines fifteen labels. There are incoming references on fourteen source lines in Chapter 6, one in Chapter 7, one in Appendix A and one in B. These references need an explicit disposition, rather than a blanket replacement with “see supplement”.

| Current material | Treatment in the submitted thesis |
| --- | --- |
| C.1: component moments and degrees of freedom | Retain the existing self-contained Chapter 6 example: approximately 19% mean error, 3% variance error, and first-order versus moment-target degrees of freedom of 15.30 versus 21.03. Remove the full-table pointer. Do not restore the large table to Chapter 6. |
| C.2: scaled mean-error ranges | Keep the detailed correction investigation in the supplement. Remove the appendix pointer and any claim requiring those ranges. Future work may retain the general motivation already visible in the main MI-sweep figure, without treating a particular correction as established. |
| C.3: component sampling-spread table | Supplement only. Remove the lookup sentence; retain the distinction between moment matching and an exact Student t distribution. |
| C.4: full estimator diagnostics | Keep the selected diagnostics and rejection rates already in Chapter 6. Remove pointers to the fuller table. Check that each retained recovery or bias claim has visible evidence in the main figures or selected tables; trim extra claims that do not. |
| C.5: fitted null SDs and Monte Carlo uncertainty | Keep the exact SD constants already in B.3. Add their three Monte Carlo standard errors compactly there: 0.000363, 0.000152 and 0.000007 nats for A–C. Retain independent fitting and fixed-alternative rules. No additional table is needed. |
| C.6: paired nominal/calibrated power contrasts | Keep the main power figures and existing calibration-gain table. Remove the appendix-dependent paragraph about nominal contrast intervals; retain the visible near-overlap at C and the transition to calibrated power. Preserve the full contrasts in the supplement. |
| C.7: absolute sensitivity powers | Supplement only. The main calibration-gain table already carries the comparison needed for the argument. |
| C.8: complete cross-null validation | Supplement only. Keep the decisive validation rows already in Chapter 6 and their limitation: fitting at one equal-MI population does not establish control throughout the composite null. |
| C.9: wrong-direction rejections in a separate sparse alternative | Remove the conclusion-only discussion of this additional experiment and its bias-shift equation reference. Remove the Chapter 6 pointer to it. Keep the complete analysis in the supplement. Retain the main sparse-null failure, four-cell robustness result and focus-setting B power dip, which have their own main-text evidence. |
| C.10: six-comparison Holm table | Retain the shopping results, exploratory selection disclosure and adjusted month p-values in Chapter 6. Briefly identify the six-comparison family and state that Holm adjustment is applied separately to each method. Keep full p-values and dataset preparation in the supplement; do not turn Adult and Student Performance into additional main-text applications. |

### Preserve the explanations that currently rely on C's prose

Three explanatory checks need brief support in the main text because removing their evidence would weaken the recent Chapter 6 revisions:

1. **The mean peaks and variance troughs in Section 6.1.1.** Keep the row-by-row explanations. Identify the diagnostic scope briefly: existing 16×16 different-skew samples, 10,000 repetitions at selected sample sizes, with singleton contributions and the linear/remainder decomposition checked. Keep the result beside the relevant row; leave the full decomposition in the supplement. Verify the evidence before retaining strong wording such as “most” or “confirms”, including the covariance when discussing total variance.
2. **The near-independence prediction in Section 6.1.3.** Keep the two-step explanation: replacing V-hat by twice plug-in MI, then using the local noncentral chi-squared variance prediction. State the observed direction of each error and the setting locally. Remove the appendix lookup without removing the explanation.
3. **The uniform 2×2 rejection-rate trough.** Keep the numerator–standard-error dependence mechanism. Include one compact numerical anchor: the centred-magnitude rank correlation falls from 0.656 at n=50 to 0.167 at n=1,000. Define the correlation in the same passage so the reader can interpret it. Avoid introducing the other rank-correlation examples.

For the power-curve explanation, retain a concise local check of changing alternative spread if needed to support the comparison between panels. Prefer one relevant value over importing the entire diagnostic discussion. Confirm every retained value against the existing evidence records; do not infer causation solely from an accompanying diagnostic.

These additions belong inside the existing explanation paragraphs. Do not add another results subsection, large table or diagnostic figure.

## 3. Shorten Appendix B conservatively

B was already reduced on 27 October. Further cuts should remove duplication and material used only by the retired C analysis, rather than compress the remaining derivations.

- **B.1–B.2, construction:** retain the copying construction's justification, feasible targets, root and acceptance tolerances, and the four-cell construction supporting the main robustness result.
- **B.3, grids and sampling:** compare each row of the exact-grid table with Chapter 5. Replace genuinely duplicated rows with precise references to the main design tables. Retain any unique grids, effect-size values or construction settings still needed to reproduce the main results. If only the four-cell row remains unique, state it beside B.2 and remove the duplicated table. Keep exact SD constants, fitting uncertainty, sampling, seed/stream rules and sparse-cell conventions.
- **B.4, validity:** retain all thresholds, component exclusions and unconditional/conditional denominators. Keep the direct combined-df equation and its explanation of the zero-component case.
- **B.5, diagnostics:** retain bias, matched-subset variance ratios, finite-zero inclusion and component/combined-df distinctions. Move the standalone wrong-direction counting recipe to the supplement if no retained main result uses it.
- **B.6, simulation uncertainty:** retain rate uncertainty and paired-comparison rules needed by the remaining results.
- **B.7, moment targets:** cross-reference definitions already derived in Chapter 4 where this removes actual repetition. Keep the exact mean/variance-error decomposition and the joint uncertainty calculation, including covariance. Do not remove intermediate steps that make the calculation understandable.
- **B.8, calibration:** retain strict threshold/tie handling, invalid-output treatment, independent fitting and validation, fixed alternatives, and joint bootstrap dependence. These rules support central results and are not expendable detail.

Do not set an arbitrary page target for B. Keep its current descriptive title unless the final contents warrant a clearer one.

## 4. Protect Appendix A and the main narrative

Keep Appendix A's two mathematical derivations intact. Replace its reference to C.1 with an appropriate main near-independence comparison, checking that the replacement supports the particular claim.

In Chapter 7, remove the separate sparse-alternative sign-reversal example while preserving the already established result that changing the cutoff does not correct estimation bias. Retain the four-cell robustness conclusion with a reference to its main-text evidence, rather than deleting it with the surrounding paragraph.

Apply the current research writing guidelines throughout: explicit quantities, mechanisms before shorthand, clear transitions from observation to explanation, and no new tangents. Preserve the three-row structure of Section 6.1.1 and the existing placement and readable size of its figures.

## 5. Remove C from the submitted build and verify the boundary

After the evidence edits, remove C's input from main.tex and retire its source from the active appendix directory into the dated supplement. The source packager currently includes every active appendix source, so removing the input alone would still place an unused C in the thesis source archive. Check that archive explicitly. Preserve shared generated assets and report code.

Update manuscript references, README descriptions and any affected evidence checks. Inspect tests that refer to moved labels or source fragments: point preservation checks at the supplementary copy where appropriate, while keeping numerical checks intact. Do not weaken a check simply to accommodate a missing source.

Before a requested rebuild:

- Audit every retired C label, reference and “additional results” instruction. No dangling references or instructions to inspect a missing appendix may remain.
- Check each central claim against evidence visible in the submitted thesis. Supplement references should offer detail rather than complete a missing argument.
- Check that retained parameter grids, uncertainty methods and application selection disclosures remain reproducible and unambiguous.
- Verify retained equations, scientific values, figure assets and typography against the pre-edit version; review deliberate prose deletions separately.
- Run relevant source consistency, derivation and packaging/style checks.

When a rebuild is explicitly requested, check the contents, list of tables, references, changed passages and appendix/bibliography transition visually. Report the actual page reduction. Refresh the named PDF, source package and checksums. The experimental supplement will have changed, so its old archive/checksum cannot be reused unchanged.

## Implementation order

1. Preserve the exact current appendix and source dependencies.
2. Resolve the main-text evidence dependencies and conclusion-only result.
3. Remove duplication and retired-only diagnostic material from B.
4. Unlink and retire C; update references, packaging and checks.
5. Review the source edits against the claim/evidence boundary above.
6. Rebuild and verify delivery files only when requested.

The intended result is a shorter thesis with the same central mathematical and experimental argument, supported by two purposeful appendices. The reduction comes primarily from removing secondary results, not from shrinking figures, changing spacing or making explanations harder to follow.
