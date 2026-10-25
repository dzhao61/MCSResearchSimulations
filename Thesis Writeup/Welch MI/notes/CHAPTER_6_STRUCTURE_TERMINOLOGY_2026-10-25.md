# Chapter 6 structure and terminology — 25 October 2026

## Scope and preserved version

The reader approved a structural revision of Chapter 6, a smaller terminology pass through Chapter 5, and consistent use of existing symbols after definition. The preceding 98-page PDF, active TeX inputs and current thesis README are preserved in `archive/before_chapter6_structure_terminology_2026-10-25.zip`, together with the preceding root verification record. Historical archives and working drafts were not edited.

## Changes

- Chapters 5–6 distinguish an observation recording (X,Y), the population probability tables P and Q, and a simulation repetition drawing one count table from each population. Ambiguous references to sampled, alternative and simulation “pairs” are replaced. Chapter 5's rate denominators now explicitly count simulation repetitions; its finite-value inclusion rule names both the MI difference and squared standard error.
- Chapter 6 begins with the question sequence and the repeated-sampling unit. Reporting conventions for rejection rates and uncertainty move beside the null comparisons.
- Table 6.1 distinguishes V(P), its estimate, the sampling variance of that estimate, the squared standard error and the sampling variance of the MI difference. Existing notation is retained; no replacement shorthand is introduced.
- Section 6.1 separates mean/sampling-variance predictions, their consequences for component degrees of freedom, and behaviour near independence. The moment target, population first-order calculation and sample-based calculation are distinguished before the figure guide compares them. Predictions use their symbols with the measured quantity and ratio direction stated explicitly.
- Section 6.2 introduces the shared statistic and the effect of the Student t distribution cutoff before reporting the null results. The detailed cases define difference bias and the variance ratio before explaining A, B, C and the sparse-table failure. Comparisons use the average squared standard error and observed variance of the MI difference explicitly.
- Section 6.3 recalls A–C and the fitted null SD before reporting power. It explains calibration before its results and introduces both lower and upper nulls before sensitivity findings. Paired comparisons are explicitly defined as methods applied to the same simulated data; their intervals preserve that relationship.
- Section 6.4 introduces the construction and allocation comparisons before their numerical results and identifies the SD as that of the MI difference. The application removes the ambiguous predictor–purchase “pair” wording.

## Preservation and review

Source comparisons against the preserved version confirm that every existing displayed equation and figure block in Chapters 5–6 remains byte-identical, including figure dimensions and captions. All four preceding Chapter 6 table blocks are unchanged; the sole added table is the symbol guide. All distinct pre-existing numerical literals and the citation sequence are retained. Only Chapters 5 and 6 change among the active TeX inputs. All other chapters and appendices, including Section 2.3 and the derivation, remain unchanged. Scientific qualifications on validity, moment matching, independence, calibration sensitivity, bias, direction and application interpretation are retained. No experiment, bootstrap resampling or numerical analysis was rerun.

The manuscript is 99 pages, up from 98, with 61 pages of main text. Chapter 5 remains nine pages (physical 42–50); Chapter 6 is fourteen pages (physical 51–64), up from thirteen. The increase accommodates the symbol guide and missing explanatory steps without reducing figure sizes.

## Completed validation

- All eight existing packaging tests pass.
- Source-preservation checks pass for equations, figures, Chapter 6 result tables, numerical literals, citations and unaffected TeX inputs.
- The final main build has no LaTeX warnings, unresolved references or overfull/underfull boxes.
- Physical pages 4–8 and 42–64 were rendered and visually reviewed, including the new guide, contents/list entries, result sequence, calibration table and application. The final Chapter 5 opening was rendered again after its paragraph adjustment. Tables and plots are within margins and readable.
- The delivery package and checksums were refreshed; package verification passes. Main, build and delivery PDFs are byte-identical.
- The extracted source archive builds independently without warnings and produces identical PDF text.

No Git commit was requested or performed. Historical validation records remain historical; this prose revision did not rerun the full scientific test suite.
