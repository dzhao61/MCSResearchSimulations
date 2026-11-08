# Examiner reading boundary, 31 October 2026

The user clarified that the examiner should be assumed to receive only the submitted thesis PDF. Project evidence archives are not examiner reading. This supersedes earlier plans that retained manuscript pointers to a separate experiment supplement after removing Appendix C.

The pre-edit affected chapters, experimental appendix, instructions, guide, README and current PDF are preserved in `archive/before_examiner_reading_boundary_2026-10-31.zip`. Internal evidence and archived analyses remain unchanged.

## Manuscript corrections

The active manuscript contained eleven mentions of the project supplement, including ten directions to external material and one description of the broader experiment scope. All are removed or replaced with references within the submitted thesis.

- Chapter 4: removed the secondary finite-difference validation claim together with its external-only tables/step-size pointer. Its exact mathematical derivations remain intact. Removed the covariance-calculation pointer while retaining the explanation that the MI difference and standard error use the same sampled tables and can move together.
- Chapter 5: the construction comparison now points to Appendix B for construction/settings and Section 6.2.2 for the reported sparse-table result. Removed the promise of broader power and sample-allocation analyses not presented in the thesis. Replaced the 366-setting main-plus-supplementary description with the scientific roles of the evaluations actually discussed; rates, repetition counts and presented grids remain unchanged.
- Chapter 6: removed the companion-plot pointer, conditional-rate/count pointer highlighted by the user, full-construction-result pointer and application-family archive pointer. Retained the figures' explanations, validity evidence and included-count rules, the quantitative four-cell result, the six-comparison selection disclosure and adjusted month p-values. The Holm procedure and numerical results are unchanged; no alternative correction or additional application was introduced.
- Appendix B: removed the pointer to an unreported unequal-sample comparison and the full-Taylor-expansion pointer. The sampling rules, correction formula, explicit function and derivatives, joint uncertainty calculation and covariance treatment remain in B. The independent-stream comparison statement now refers to the retained construction comparison.

These edits do not restore retired exploratory analyses or enlarge the appendices. The central results and calculations are stated in the manuscript; no direction to an unsubmitted report substitutes for their explanation.

## Persistent instructions

The workspace `AGENTS.md`, thesis `AGENTS.md` and current Chapter 6 writing guide now require the submitted PDF to stand alone as the examiner's reading set. Essential methods/evidence must be in its main text or submitted appendices; claims or promises depending on unavailable secondary material should be omitted. Ordinary literature and public-dataset citations remain appropriate. Internal evidence preservation and packaging continue for project work.

## Verification

- The active 21-file TeX input graph has no project-supplement, companion-report or internal-archive reference. Its 140 unique labels resolve, citations exist and all environments/braces balance.
- Every figure, table and mathematical display in the four edited manuscript files is byte-identical to the pre-edit snapshot, and labels are preserved.
- The 117 protected manuscript, figure/data, PDF and delivery files match their pre-edit hashes. Other chapters and appendices are unchanged.
- Paragraph-style checks, five numerical-consistency tests and eleven independent derivation checks pass (16 tests total).
- The PDF and delivery archives are unchanged and await an explicit rebuild request. No simulation, fitting, bootstrap or Git commit was performed.

Details are recorded in `EXAMINER_READING_BOUNDARY_VERIFICATION_2026-10-31.json`.


## Requested rebuild, 31 October 2026

The requested rebuild includes these edits in the 109-page main and named PDF. Compilation, references and paragraph style pass; all 33 changed pages were visually reviewed. The compiled manuscript has no project-supplement or companion-report pointers. The source archive and checksums were refreshed. The unchanged 25,010-file experiment supplement was reused after checking its inventory, input sizes and timestamps, and archive size and timestamp.
