# Chapter 4 direct-derivation comparison

This copy was requested on 9 November 2026 to compare a more direct
explanation with the existing thesis. Only Chapter 4 manuscript source
changes; all other chapters, appendices, figures, numerical results,
metadata, and template assets match the original snapshot.

The revised proof differentiates the centred variance directly. It separates
changes in probability weights from changes in pointwise MI, cancels the
mean-derivative term through the zero average of centred deviations, and
obtains the existing sensitivity formula. It removes the separate MI
influence-function rederivation, second-moment calculation, completion of
the square, and unused probability-conservation display.

The moment-matching calculation is consolidated, and the explanation of
whole-sample error retains the Taylor formula, its mapping, linearity in
the table direction, and the small-error condition. The worked example,
algorithm, and near-independence section are unchanged. The final
sensitivity, estimated sensitivities, moment formulas, component degrees
of freedom, combined degrees of freedom, and p-value are unchanged.

Validation:

- 11 existing derivation audit tests pass.
- 48 probability tables and 456 cell perturbations verify the direct proof.
- The maximum numerical derivative discrepancy is below 4.2e-10.
- Eleven core displayed equations match the original after whitespace removal.
- The PDF has 108 pages; Chapter 4 occupies printed pages 23–37 (15 pages),
  compared with 18 pages in the original 111-page thesis.
- All 108 rendered pages were inspected, with the central proof inspected
  at full size. Central equation groups and their explanations are kept
  together where needed.
- The final LaTeX log has no warnings, missing references, missing characters,
  or overfull/underfull boxes. Internal navigation resolves, and fonts are embedded.
- The 120-entry source archive matches the delivered copy. A fresh extraction
  compiles independently and reproduces every PDF page-content stream and
  named destination without accessing the active thesis.
- Australian spelling, complete distribution names, and the existing paragraph
  and heading conventions are preserved.
- Hash checks confirm that 534 protected original/submission/presentation
  files are unchanged. The signed submission remains the existing version.

This is an unsigned comparison copy. It has its own local build script and
no active-thesis publication or automatic-push hook. Detailed checks are in
`verification.json`; `verify_direct_derivation.py` reruns the numerical proof
checks with NumPy. The named PDF and self-contained LaTeX archive are in
`../deliverables/`.
