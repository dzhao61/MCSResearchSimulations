# Appendices A and B reduction, 27 October 2026

The user approved the section-by-section recommendations in the attached
appendix review. The implementation preserves explanatory derivations and
scientific reproduction details, relocating secondary calculations instead
of deleting their evidence. PDF and packaging rebuilds remain deferred.

## Appendix A

- Former A.1: the complete zero-mean proof now sits beside the sensitivity
  variance definition in Chapter 4. Both displayed calculations are retained.
- Former A.2: the fixed-margin near-independence derivation is unchanged.
- Former A.3: the covariance derivation is preserved in the supporting-calculation
  supplement. Chapter 4 retains the explanation of shared-data dependence.
- Former A.4: the independence-boundary and local positive-MI argument is
  unchanged, including its intermediate algebra, assumptions and example.
- Former A.5: the direct combined-df equation and the actual zero-component
  exclusion rule now appear together in Appendix B's validity section.
- Former A.6: test tables and finite-difference details move to the supplement;
  Chapter 4 retains a brief numerical-validation statement.

Appendix A is now titled Near-Independence Calculations and has two sections.
The two Taylor setups are retained because they treat different probability
perturbations; shortening them further would remove useful exposition.

## Appendix B

- B.1 refers to Chapter 5's copying formula rather than printing it again.
  The margin check, monotonicity argument, feasible MI endpoint, root method,
  root tolerances and table-acceptance tolerances remain.
- B.2 retains the four-cell construction, range and target selection. Its
  binary-equivalence derivation is preserved in the supplement.
- B.3 retains grids behind the main results, exact fitted null SD constants,
  multinomial sampling, random-stream conventions, fixed categories, empty
  cells, logarithms, bias correction and no-smoothing rule. Broader power and
  allocation-only rows and allocation-specific arithmetic move to the supplement.
- B.4 retains all validity conditions, denominators and sparse-count rules,
  and now contains the former A.5 equation and explanation.
- B.5 retains bias, observed variance, matched-subset variance ratios, finite
  zero values, df inclusion fractions, conditional summaries and rejection
  direction. The rank-diagnostic method is preserved in the supplement;
  Appendix C specifies its finite-pair inclusion rule beside its results.
- B.6 retains the rate MCSE and paired method-difference calculation. The
  standard Wilson formula moves to the supplement; its citation stays.
- The component moment targets, decomposition and uncertainty method form
  one section. The final U/W/Z calculation retains mean--variance covariance;
  its full Taylor derivation is preserved in the supplement. Fitted null-SD
  uncertainty and paired ratio calculations remain described.
- Calibration and sensitivity form one section. The strict threshold order
  statistic, boundary ties, invalid outputs, independent fitting/validation,
  six upper nulls, 100,000-repetition batches, 1,000 bootstrap repetitions,
  curve-wise and sensitivity-wise sharing, joint decisions under both
  calibrations, fixed populations/effects and conditional Wilson intervals remain.

The previous move of the fixed-reference rule and combined-moment identity
is retained. No fixed-reference material is reintroduced into the thesis.
Appendix B now has eight sections. References to removed section labels and
to supplementary-only parameter settings are updated in the main chapters.
Section labels shared by target and uncertainty discussions are attached to
the section heading, so they do not accidentally refer to an equation.

## Preservation and validation

The pre-edit source is archived in
`archive/before_appendices_a_b_reduction_2026-10-27.zip`. Relocated material
has a standalone source and exact originals under
`WelchSatterthwaiteMI/supplementary_displays/supporting_calculations/`.
The existing package inventory includes that directory automatically.

- The fixed-margin and independence-boundary derivation blocks are byte-identical.
- Retained four-cell, zero-component, moment-target, decomposition and final
  moment-uncertainty equations are byte-identical.
- Root tolerances and exact focused-power SD constants are retained.
- LaTeX inputs, references, labels, environments and braces are checked without
  compiling; the global flush-left paragraph policy passes.
- Eleven existing numerical derivation checks and five manuscript-consistency
  checks pass. No new simulation, fitting or bootstrap was run.
- Chapters 2 and 3, Results, Conclusions and all figure/table assets are unchanged.
- Existing main/delivery PDFs and delivery ZIPs are unchanged. No updated page
  count or page-layout claim is made until an explicitly requested rebuild.
