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
| Manuscript | The final A4 PDF has 95 pages, including 66 numbered main-text pages. The active source reads `chapters_rewrite/` and `appendices_rewrite/`. | Complete. |
| Mathematics | `SCIENTIFIC_AUDIT.md` records independent derivative checks, local near-independence limits, implementation comparisons, worked-example reproduction and regularity qualifications. All 101 tests pass. | Complete. |
| Literature | `LITERATURE_SOURCE_CHECK.md` records a source and claim disposition for all 35 active references. The local bibliography contains the same 35 checked records, with no missing or unused citations. | Complete. |
| Experimental evidence | The audit reconstructs the frozen protocol and checks every Chapter 6 value, the exact source rows for all 22 confirmatory figures, generated macros, paired results, convergence and runtime. It also checks the 809-configuration supplementary mechanism study, its 169 independent null pilots, ablations, local-moment predictions and quoted diagnostic values. | Complete. |
| Build | The active source builds to 95 A4 pages with zero errors, undefined citations or references, missing assets, and overfull boxes. Fonts are embedded. | Complete. |
| Visual presentation | The previously reviewed pages and every page changed in the supplementary revision were inspected at final size. Figures, captions, equations and tables show no clipping or overlap. | Complete. |
| Source package | `references.bib`, all active source files and all 22 figure PDFs are local. The isolated copy compiles without an old draft or parent bibliography. | Complete. |
| Front matter | The title page, declaration, abstract and acknowledgements contain no drafting placeholders. “Master of Complex Systems” matches the official University course title. The declaration includes blank signature and date lines. | Author must sign and date the declaration before submission. |

## Substantive and readability pass

T6 was completed on 16 September 2026. Each active chapter and appendix was
read once for scientific continuity and once for clarity. The pass used the
audited equations, sources, protocol and result rows as constraints; it did
not change the frozen evidence or add material for length alone.

| Part | Check and disposition |
| --- | --- |
| Chapter 1 | The estimand, weak null, four research questions, contribution and scope agree with the later method and evidence. No material change required. |
| Chapter 2 | Prior-work scope agrees with the expanded 35-source audit, including Hutcheson's direct information-theoretic comparison, general sandwich-df and higher-moment MI precedents. Standardisation wording was made consistent and unnecessary “oracle” jargon was removed. |
| Chapter 3 | Bias correction, (V) versus (V/n), shared statistic and null interpretation agree with the implementation. Unevaluated confidence-interval formulas were removed. |
| Chapter 4 | The derivation proceeds from moment matching through the complete variance sensitivity to the final reference. It retains the interpretable local `df approximately nI` behaviour without the supplementary higher-order calculation. Assumptions, invalidity, nesting and numerator-denominator dependence are explicit. |
| Chapter 5 | The fixed population construction, margins, sample randomness, metrics, family counts and runtime design agree exactly with the frozen protocol. |
| Chapter 6 | Every stated result and all 22 confirmatory figure selections pass the source-linked audit. Strong and weak nulls are separated; the \(n=5\) zero-rejection finding is not counted as calibration; low-validity settings are exposed; and one representative mechanism check is reported without the full ablation study. |
| Chapters 7-8 | All four research questions are answered; the practical recommendation distinguishes calibration, nominal-threshold detection and validity. The mechanism conclusion is qualified to include denominator estimation, quadratic numerator error and their dependence. |
| Appendix A | The supporting derivatives agree with the mathematical tests. The finite-difference step was renamed (eta) so it is not confused with the earlier perturbation direction (h). |
| Appendix B | The constructors and every exact grid agree with the reconstructed protocol; reused configurations and infeasible extensions are distinguished. |
| Appendix C | The evidence files, denominators, intervals and expected-count terminology agree with the saved outputs. |
| Appendix D | The independence construction and second-order Taylor expansion agree with the independent numerical check and the (G)-test boundary. |
| Appendix E | The concise reproduction record identifies the frozen protocol, saved metadata, evidence audit, archives and build commands. Exact hashes and code-history details remain in the experiment supplement. |
| Mechanism supplement | The independent-SD diagnostic, component-df comparisons, ablations, support-correction sensitivity and all 108 main null rows remain available outside the compiled thesis and agree with the saved result files. |

No active manuscript file contains a TODO or drafting placeholder. The only
remaining front-matter action is the author's signature and date on the
declaration; no personal attestation has been invented.

The final comprehensive audit also compared the retained implementation with
the source hashes recorded by the confirmatory run. The frozen protocol,
population and simulation core, test implementation, and imported statistical
dependencies still match exactly. The orchestration runner has three later,
non-statistical changes: more precise atlas-count metadata, hashes for saved
outputs on future runs, and corrected one-pass handling of a failed preflight.
Its population-construction, simulation and method-evaluation path is
unchanged, so this source drift does not alter the frozen results. Detailed
hashes and runner-history notes remain in the experiment supplement rather
than interrupting the thesis narrative. The source package is rebuilt without
disposable LaTeX auxiliary files.

## Final verification record

Final checks run on 20 September 2026:

- clean build from a fresh extraction of the final source archive;
- 95 A4 pages and 975,342 bytes before packaging;
- final named PDF SHA-256 `c43921ec40570f05dc95da44473b1ae59db745b9bdb388f9c3ce5ea85e97b25d`;
- zero LaTeX errors, undefined citations or references, missing files, and overfull boxes;
- all 101 unit, derivation and experiment tests passed;
- complete evidence audit passed, including all 22 confirmatory thesis figures, every reported Chapter 6 value and the supplementary mechanism evidence;
- a fresh combined extraction of the source and experiment archives rebuilt
  the 3,111-configuration preflight, passed all 36 bundled tests, regenerated the
  22 confirmatory thesis figures and mechanism report, passed the evidence
  audit and compiled the 95-page thesis without access to the working tree;
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
included alongside the consolidated tables, so individual configuration
outputs can also be inspected directly.

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
