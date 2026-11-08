# Chapter 4: four further flow refinements

## Plan

The user authorised these four refinements, verification, and a main PDF
rebuild. Apply the research-prose guide's reading-order principle: keep
each calculation with the question it answers, state the mathematical
connection explicitly, and preserve useful algebra and qualifications.

1. Remove the combining-rule preview from Section 4.1 and place its
   labelled formula beside the combining-rule derivation in Section 4.3.
   Keep Section 4.1 focused on the moments needed for one component.
2. Explain the perturbation as proportional downweighting of the original
   table plus added mass at the selected cell. Distinguish the fixed
   selected cell (x,y) from the cell index (i,j). Explain that g is the
   derivative with respect to the mixture weight and that one observation
   enters the error average with weight 1/n.
3. Show the substitution of E(Vhat) approximately equal to V and
   Var(Vhat) approximately equal to tau squared divided by n into the
   component moment target before defining the population first-order
   degrees of freedom.
4. Explain beside the empirical sensitivity-variance formula that dividing
   the estimate of tau squared by n estimates Var(Vhat). Connect the
   resulting component formula to its population counterpart.

## Verification and publication plan

- Preserve existing mathematical displays, assumptions, cited sources,
  labels, numerical examples, and exact/approximate distinctions. Check
  transitions and reference targets after the equation move.
- Reread Sections 4.1–4.3 sentence by sentence for the named quantities,
  logical relationships, Australian spelling, Oxford commas, and complete
  distribution names. Preserve the rest of the chapter where it already
  explains its purpose clearly.
- Run the existing independent numerical derivation checks, source-
  preservation checks, and paragraph-style check before rebuilding.
- Build with `--no-push`, inspect revised pages and chapter boundaries,
  check the final LaTeX log and delivery package, and refresh the signed
  deliverable and FINAL SUBMISSION PDF. Preserve the existing signature
  and date, back up the previous submission, and verify the separate
  submission forms are unchanged before the scoped commit and push.

## Source revision and verification

Implemented the four changes in the planned locations. The combining
equation now appears immediately before its derivation. Section 4.1
continues directly from sample-size scaling to the moments required for
one component. The perturbation explanation names the downweighting,
added probability, fixed selected cell, general cell index, and distinction
between a derivative and one observation's weighted contribution.

The population substitution uses an approximation sign when replacing
the sampling moments and an equality sign for the subsequent algebra.
The empirical sensitivity variance is connected explicitly to the
estimated sampling variance of Vhat by division by n.

All 66 previous equation and table displays are preserved; one
unnumbered substitution display was added. Labels, citation occurrences,
assumptions, and reference targets are preserved. The worked example,
operational algorithm, and limitations are unchanged.

All 11 existing independent numerical derivation-audit tests pass.
Additional numerical checks confirm preservation of total probability,
proportional changes in the other cells, observation-average weighting,
and the component substitution. Paragraph-style, regional-spelling, and
source-diff checks pass. The revised passages were reread for logical
order, named referents, genuine sentence connections, complete distribution
names, and the distinction between exact and approximate statements.

The first PDF review found a page break within the two-line combined
variance calculation. A non-breaking line separator keeps that equation
together without changing its mathematical content.

## Verified PDF publication

The final PDF remains 109 pages. Physical pages 32–50 were rendered and
reviewed, covering all of Chapter 4 and the Chapter 5 boundary. The final
LaTeX log has no warnings, undefined references, or box warnings. The
read-only delivery check passes, and the unchanged experiment supplement
was verified and reused. The 117-entry source archive contains the exact
revised Chapter 4 source.

The existing signature and 07/11/2026 date were preserved. The signed
compliance page is pixel-identical to the previous signed copy; all
unsigned page contents and navigation are preserved. All 416 named
destinations and 446 internal links resolve. The document retains 70
bookmarks and 98 external links.

The signed deliverable and FINAL SUBMISSION PDF are byte-identical. The
previous submission thesis was backed up in Archive, and the separate
consent declaration and AI acknowledgement files are unchanged.

Unsigned PDF SHA-256:
`e507638907e3a5d2a2e4e792f39fa182bdbef65c235893ada89d6323978a8638`

Signed PDF SHA-256:
`94bcd77d80427f420a7c878d60cb47b0aeca32f42a132e4d7daf58359532ad40`
