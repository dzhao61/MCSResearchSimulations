# Section 5.1 explanation rewrite - 25 October 2026

The user requested a slower introduction to the population construction.
Section 5.1 has been rewritten around the choices needed to construct each
population before sampling. The previous 95-page manuscript and its source
inputs are preserved in `archive/before_section_5_1_revision_2026-10-25.zip`.

## Explanation and reading order

1. State why the simulation needs specified equal and unequal MI values.
2. Define the category count and probability vector, identifying row and
   column margins within one population.
3. Begin with independent draws and zero MI, then introduce the copying
   probability and two explicit choices for generating Y.
4. Explain chance matches, guaranteed matches and why both choices preserve
   the population margins. Distinguish those fixed probabilities from
   fluctuating sample proportions.
5. Derive each mixture contribution in words before showing the unchanged
   joint-probability formula. Explain positive cells and the numerical
   search for a desired MI before reporting a fitted copying probability.
6. Set the binary example's frequencies and target MI first. Explain the
   two conditional-probability calculations, complete the remaining cells,
   construct Q and identify the true signed difference.
7. Explain the table sizes and frequency patterns before presenting the
   uneven-margin formula and regime table. Retain the distinction between
   identical tables and distinct equal-MI tables, bias cancellation and
   the probability changes accompanying larger tables.

The worked examples and short two-choice list provide the additional
explanation. Repeated conclusions were removed during contextual review.
The final manuscript is 96 pages, one page longer than before. Section 5.1
occupies printed pages 34-37. Fonts, margins and figure sizes are unchanged.

## Scientific preservation and verification

Only Section 5.1 changed within the manuscript body. Its original displayed
equations, worked numerical displays, margin table and citation are
unchanged. All other chapters, appendices, the abstract, bibliography,
figures, experiment settings, source kernels and numerical evidence are
unchanged. The displayed binary examples were independently calculated:
both margins match their specified vectors and the MI targets agree within
the precision of the displayed copying probabilities. No simulations were
rerun.

All five existing manuscript-consistency tests pass. The main PDF builds
without LaTeX warnings, unresolved references or overfull/underfull boxes.
The four Section 5.1 pages were inspected individually, along with the
remaining Chapter 5 pages, the Chapter 6 transition, contents and lists of
figures and tables. The text was reread in context for definition order,
paragraph focus and statistical precision. The source archive builds
independently and yields PDF text identical to the delivery PDF. Packaging
and consistency checks confirm that the PDF, source ZIP, experiment
supplement and checksums are current. Full-suite historical test counts
in the root verification record retain their previous run date; this
revision reran the five manuscript-consistency tests. No Git staging or
commit is part of this revision.
