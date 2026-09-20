# Thesis completion check

Updated 20 September 2026. The current objective, SMART targets and working
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
| Manuscript | The final A4 PDF has 109 pages, including 68 numbered main-text pages. The active source reads `chapters_rewrite/` and `appendices_rewrite/`. | Complete. |
| Mathematics | `SCIENTIFIC_AUDIT.md` records independent derivative checks, local near-independence limits, implementation comparisons, worked-example reproduction and regularity qualifications. All 100 tests pass. | Complete. |
| Literature | `LITERATURE_SOURCE_CHECK.md` records a source and claim disposition for all 35 active references. The local bibliography contains the same 35 checked records, with no missing or unused citations. | Complete. |
| Experimental evidence | The audit reconstructs the frozen protocol and checks every Chapter 6 value, the exact source rows for all 22 confirmatory figures, generated macros, paired results, convergence and runtime. It also checks the 809-configuration post-review study, its 169 independent null pilots, ablations and quoted diagnostic values. | Complete. |
| Build | The active source builds to 109 A4 pages with zero errors, undefined citations or references, missing assets, and overfull boxes. Fonts are embedded. | Complete. |
| Visual presentation | The previously reviewed pages and every page changed or added in the post-review revision were inspected at final size. Figures, captions, equations and the 108-row null table show no clipping or overlap. | Complete. |
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
| Chapter 2 | Prior-work scope agrees with the expanded 35-source audit, including Hutcheson's direct information-theoretic comparison, general sandwich-df and higher-moment MI precedents. Standardisation wording was made consistent and unnecessary “oracle” jargon was removed. |
| Chapter 3 | Bias correction, (V) versus (V/n), shared statistic and null interpretation agree with the implementation. The confidence-interval sentence was repaired and spelling made consistent. |
| Chapter 4 | The derivation proceeds from moment matching through the complete variance sensitivity to the final reference. It now derives the local `df approximately nI` behaviour and the quadratic terms omitted near independence. Assumptions, invalidity, nesting and numerator-denominator dependence are explicit. |
| Chapter 5 | The fixed population construction, margins, sample randomness, metrics, family counts and runtime design agree exactly with the frozen protocol. |
| Chapter 6 | Every stated result and all 22 confirmatory figure selections pass the source-linked audit. Strong and weak nulls are separated, and the post-review mechanism values are checked against saved outputs. |
| Chapters 7-8 | All four research questions are answered; the practical recommendation distinguishes calibration, nominal-threshold detection and validity. The mechanism conclusion is qualified to include denominator estimation, quadratic numerator error and their dependence. |
| Appendix A | The supporting derivatives agree with the mathematical tests. The finite-difference step was renamed (eta) so it is not confused with the earlier perturbation direction (h). |
| Appendix B | The constructors and every exact grid agree with the reconstructed protocol; reused configurations and infeasible extensions are distinguished. |
| Appendix C | The evidence files, denominators, intervals and expected-count terminology agree with the saved outputs. |
| Appendix D | The independence construction and second-order Taylor expansion agree with the independent numerical check and the (G)-test boundary. |
| Appendix E | Run metadata and commands agree with the saved record. Its description now includes the exact 22-figure and Chapter 6 evidence checks. |
| Appendix F | The independent-SD diagnostic, component-df comparison, three ablations, support-correction sensitivity and all 108 main null rows agree with the post-review result files. |

No active manuscript file contains a TODO or drafting placeholder. The only
remaining front-matter action is the author's signature and date on the
declaration; no personal attestation has been invented.

The final comprehensive audit also compared the retained implementation with
the source hashes recorded by the confirmatory run. The frozen protocol,
population and simulation core, test implementation, and imported statistical
dependencies still match exactly. The orchestration runner has two later,
non-statistical additions: more precise atlas-count metadata and hashes for
saved outputs. Its simulation path is unchanged, so this source drift does not
alter the frozen results. The source package is rebuilt without disposable
LaTeX auxiliary files.

## Final verification record

Final checks run on 20 September 2026:

- clean build from a fresh extraction of the final source archive;
- 109 A4 pages and 1,040,550 bytes before packaging;
- final named PDF SHA-256 `1ad864783746e1dea9d7116179adc964722a657d2fc957f1c6ea135267066ffa`;
- zero LaTeX errors, undefined citations or references, missing files, and overfull boxes;
- all 100 unit, derivation and experiment tests passed;
- complete evidence audit passed, including all 22 confirmatory thesis figures, every reported Chapter 6 value and the post-review mechanism evidence;
- a fresh combined extraction of the source and experiment archives rebuilt
  the 3,111-configuration preflight, passed all 35 bundled tests, regenerated the
  22 confirmatory thesis figures and mechanism report, passed the evidence
  audit and compiled the 109-page thesis without access to the working tree;
- 35 checked bibliography records, with every manuscript citation resolved and no unused records;
- all newly added and changed pages inspected at final pagination, building on the prior full-page review;
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
