# Conclusions chapter merge, 27 October 2026

## Plan and scope

Combine the former Chapter 7, Implications and Limitations, and Chapter 8,
Conclusion, into Chapter 7, Conclusions. Use one contribution statement,
explicit answers to RQ1, RQ2.1 and RQ2.2, one limitations section and one
future-work section. Preserve mechanisms and scientific qualifications;
remove repeated result summaries. Keep numerical evidence in Chapter 6
and the appendices. Apply the established preference for connected prose,
concrete quantities, explanations of mechanisms and purposeful paragraphs.

The user has suspended PDF and delivery-package rebuilds until explicitly
requested. This revision is source-only. The existing 103-page PDF is the
previous build, so no new page count or visual-layout claim is made.

## Implementation

- `chapters_rewrite/07_conclusions.tex` is the single final chapter.
- 7.1 Contributions and main findings contains the derivation contribution,
  then RQ1, RQ2.1 and RQ2.2 subsections.
- 7.2 Limitations consolidates assumptions, tested populations, calibration
  scope, simulation uncertainty and limits of the application evidence.
- 7.3 Future work connects mean correction, sparse-table estimation,
  independence and broader population comparisons to those limitations.
- `main.tex` includes the merged chapter instead of two ending chapters.
- The Introduction's organisation paragraph points to the merged chapter.
- The old chapter sources are preserved in
  `archive/before_conclusion_merge_2026-10-27.zip`, along with the previous
  entry point, Introduction, current Results source, instructions, README,
  verification record and PDF. They are removed from the active source folder.
- The thesis AGENTS.md records the user's build deferral for future turns.

## Scientific and editorial review

Preserved explanations:

- Squaring the mean in the moment target means replacing an inflated sampling
  mean with V(P) lowers the population first-order degrees of freedom.
- Replacing population probabilities with sample proportions introduces a
  further discrepancy in estimated component degrees of freedom.
- Quadratic sampling terms matter near independence.
- A larger Student t cutoff can reduce excessive rejection or deepen
  conservatism. A near-5% rate can reflect compensating errors.
- Nominal power losses and calibrated power gains answer different comparisons;
  gains can reverse when the calibration population changes.
- Changing a cutoff leaves difference bias unchanged, including the initial
  decline in rejection at B and the sparse-table direction failure.
- Cancellation of expected difference bias does not ensure an accurate
  estimated standard error, and unequal sample sizes can leave residual bias.
- Calibration at two null populations does not establish control over the
  entire equal-MI null. Application population MI remains unknown.

Repeated 3--4%, 17--19%, 44% and 99% numerical recaps are removed from the
ending; their underlying evidence remains in Section 6.1 and its tables.
The interpretation of nearly doubled squared standard errors and the
0.01-nat sign-reversal example is retained because those values explain
distinct failures. No equations, figures, tables or experimental results
are changed by this merge.

The proposed removal of the fixed moment reference from the main manuscript
is a separate, unimplemented recommendation. The merge retains its relevant
limitation rather than silently changing experimental scope.

## Validation

- All active include/input targets exist.
- No undefined cross-reference labels or duplicate labels in the active source.
- All LaTeX environments balance; final source also checked for balanced braces.
- Five existing manuscript-consistency tests pass.
- PDF and all existing delivery files retain their pre-merge SHA-256 hashes.
- No LaTeX build, packaging refresh or simulation was run.

Visual layout and resulting pagination remain to be checked when the user
requests the next PDF rebuild.
