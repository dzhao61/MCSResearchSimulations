# Thesis completion check

Updated 16 September 2026. The current objective, SMART targets and working
schedule are in [THESIS_GOAL.md](THESIS_GOAL.md).

## Agreed requirements

The user has confirmed that the supplied example theses determine the desired
length and that there is no AI-use limitation for this task. CSYS5061 was an
incorrect course assumption; its assessment restrictions and report length have
been removed from the active requirements.

The examples have 58, 65 and 87 pages of main text and complete PDFs of 75,
126 and 104 pages. The working goal is comparable depth and length, with
65-75 main-text pages as a useful planning centre within the observed range.

## Current evidence

This records the final verification status and the one remaining author-only
submission action.

| Area | Evidence available | Remaining work |
| --- | --- | --- |
| Manuscript | The final A4 PDF has 88 pages, including 61 numbered main-text pages. The active source reads `chapters_rewrite/` and `appendices_rewrite/`. | Complete. |
| Mathematics | `SCIENTIFIC_AUDIT.md` records independent derivative checks, implementation comparisons, worked-example reproduction and regularity qualifications. All 28 final tests pass. | Complete. |
| Literature | `LITERATURE_SOURCE_CHECK.md` records a source and claim disposition for all 15 active references. The local bibliography contains the same 15 checked records, with no missing citations. | Complete. |
| Experimental evidence | The audit reconstructs the frozen protocol and checks every Chapter 6 value, the exact source rows for all 22 thesis figures, generated macros, paired results, convergence, runtime and run-level invariants. It passes on the final manuscript. | Complete. |
| Build | A fresh isolated source copy builds to 88 A4 pages with zero errors, undefined citations or references, missing assets, and overfull boxes. Fonts are embedded. | Complete. |
| Visual presentation | All 88 final pages were rendered and inspected. The abstract and conclusion fit cleanly; figures, captions, equations and tables show no clipping or overlap. | Complete. |
| Source package | `references.bib`, all active source files and all 22 figure PDFs are local. The isolated copy compiles without an old draft or parent bibliography. | Complete. |
| Front matter | The title page, declaration, abstract and acknowledgements contain no drafting placeholders. The declaration includes blank signature and date lines. | Author must sign and date the declaration before submission. |

## Substantive and readability pass

T6 was completed on 16 September 2026. Each active chapter and appendix was
read once for scientific continuity and once for clarity. The pass used the
audited equations, sources, protocol and result rows as constraints; it did
not change the frozen evidence or add material for length alone.

| Part | Check and disposition |
| --- | --- |
| Chapter 1 | The estimand, weak null, four research questions, contribution and scope agree with the later method and evidence. No material change required. |
| Chapter 2 | Prior-work scope agrees with the source audit. Standardisation wording was made consistent and unnecessary “oracle” jargon was removed. |
| Chapter 3 | Bias correction, (V) versus (V/n), shared statistic and null interpretation agree with the implementation. The confidence-interval sentence was repaired and spelling made consistent. |
| Chapter 4 | The derivation proceeds from moment matching through the complete variance sensitivity to the final reference. Assumptions, invalidity, nesting and numerator-denominator dependence are explicit. No equation change was required. |
| Chapter 5 | The fixed population construction, margins, sample randomness, metrics, family counts and runtime design agree exactly with the frozen protocol. |
| Chapter 6 | Every stated result and all 22 figure selections pass the source-linked audit. The opening definition now says explicitly that the plotted numerator is the number of valid rejections. |
| Chapters 7-8 | All four research questions are answered; the practical recommendation distinguishes calibration, nominal-threshold detection and validity. Claims remain within the tested scope. |
| Appendix A | The supporting derivatives agree with the mathematical tests. The finite-difference step was renamed (eta) so it is not confused with the earlier perturbation direction (h). |
| Appendix B | The constructors and every exact grid agree with the reconstructed protocol; reused configurations and infeasible extensions are distinguished. |
| Appendix C | The evidence files, denominators, intervals and expected-count terminology agree with the saved outputs. |
| Appendix D | The independence construction and second-order Taylor expansion agree with the independent numerical check and the (G)-test boundary. |
| Appendix E | Run metadata and commands agree with the saved record. Its description now includes the exact 22-figure and Chapter 6 evidence checks. |

No active manuscript file contains a TODO or drafting placeholder. The working
comments in the declaration, acknowledgements and metadata are administrative
author checks reserved for T8, not missing thesis argument.

## Final verification record

Final checks run on 16 September 2026:

- clean build from `/private/tmp/welch-thesis-final.6duPIf`;
- 88 A4 pages and 937,179 bytes before packaging;
- `texcount` diagnostic of 12,592 words across the complete included source,
  including 9,733 words in Chapters 1--8;
- final named PDF SHA-256 `c2ee067bd000fccce9de784faf1363066428afebc0a981ac2cb8e3bfd2b3beba`;
- zero LaTeX errors, undefined citations or references, missing files, and overfull boxes;
- 28 relevant unit and derivation tests passed;
- complete evidence audit passed, including all 22 thesis figures and every reported Chapter 6 value;
- a fresh combined extraction of the source and experiment archives rebuilt
  the 3,111-configuration preflight, passed all 28 tests, regenerated the
  complete atlas and 22 thesis figures, passed the evidence audit and compiled
  the 88-page thesis without access to the working tree;
- 15 checked bibliography records, with every manuscript citation resolved;
- all 88 pages inspected at final pagination;
- `git diff --check` passed for the thesis tree.

Final deliverables are stored in `deliverables/`:

- `Daniel_Zhao_Welch_MI_Thesis.pdf`;
- `Daniel_Zhao_Welch_MI_Thesis_Source.zip`;
- `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`;
- `SHA256SUMS.txt`.

The source archive is the self-contained compilation package. The experiment
supplement contains the complete regime atlas, its figures, the frozen result
tables, protocol records, pinned numerical dependencies and all directly
imported project source needed by the runner. Its archive-local README gives
commands for preflight reconstruction, report regeneration, tests, evidence
audit and a complete rerun. Raw per-configuration checkpoint files are
intentionally omitted because the consolidated tables contain the reported
outcomes and the checkpoints are not needed to inspect or reproduce any thesis
figure or numerical claim.

## Remaining author action

Print or otherwise complete the signature and date lines on the declaration
before submitting the attested copy. No signature image or date has been
invented. If the School supplies a course-specific declaration form, replace
only that preliminary page; the thesis argument and evidence do not change.

## Acceptance criteria

1. T1-T7 are closed with evidence and dates.
2. Every research question has an explicit answer supported by the derivation or results.
3. All final numerical statements and figures agree with the saved experiments and use the correct denominators.
4. Both editorial passes and the page-by-page visual review are complete.
5. The final PDF builds from the deliverable source package and all mathematical and evidence checks pass.
6. The PDF, source and experimental supplement are assembled; T8 closes when the author signs and dates the declaration.

Scientific writing, editing and verification can proceed throughout. Routine
decisions do not require another supervisor confirmation round. The goal is
complete when the final deliverables satisfy these checks and the detailed
acceptance criteria in `THESIS_GOAL.md`.
