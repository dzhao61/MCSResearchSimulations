# Thesis completion check

The 5 October 2026 record below verifies the current thesis and deliverables.
The later dated September notes are retained as historical audit evidence;
their earlier page counts and references to a "current" PDF do not supersede
this record. The acceptance targets are in [THESIS_GOAL.md](THESIS_GOAL.md).

## Agreed requirements

The user has confirmed that the supplied example theses determine the desired
length and that there is no AI-use limitation for this task. CSYS5061 was an
incorrect course assumption; its assessment restrictions and report length have
been removed from the active requirements.

The examples have 58, 65 and 87 pages of main text and complete PDFs of 75,
126 and 104 pages. They set a benchmark for depth and presentation, not a
minimum page count. The current main text is shorter because secondary plots
and technical detail are in the appendices.

## Current Verification

T1-T8 are complete for the 5 October revision.

| Area | Evidence available | Status |
| --- | --- | --- |
| Manuscript | The standalone A4 PDF has 86 pages, including 50 numbered main-text pages and three focused appendices occupying 24 pages. Chapter 6 contains seven lead figures; Appendix C contains eight supporting figures and all 108 individual main null settings. File inventories, local paths, build commands, configuration IDs and protocol-freeze records are excluded from the reader-facing manuscript. | Complete. |
| Mathematics | `SCIENTIFIC_AUDIT.md` records independent derivative, worked-example and implementation checks. The 102 Welch-project tests, 27 DifferentialMI tests and 37 archive-bundled tests pass. The added cell-level check verifies the intermediate pointwise MI, conditional means, variance contribution and variance sensitivity in Section 4.4; the binary construction check also verifies Section 5.1's new first-cell calculation. The condensed independence calculation also passes 30 independent positive-table finite-difference checks. | Complete. |
| Literature | `LITERATURE_SOURCE_CHECK.md` records the claim checks supporting all 35 remaining active references. The removed transfer-entropy aside and its citation are retained in the historical source check. The clean build resolves every citation. | Complete. |
| Experimental evidence | The full audit reconstructs the frozen protocol and verifies Chapter 6 claims, all 22 available figures, the 15 included figures, all 432 rejection/validity values in the 108-setting null table, paired results, convergence, runtime and supplementary mechanism diagnostics against saved rows. It passes both in the workspace and in the extracted archives. | Complete. |
| Build | A clean build from the extracted source produces 86 A4 pages with the same extracted text as the working PDF. The log has no errors, undefined citations or references, missing characters or overfull boxes. | Complete. |
| Visual presentation | The revised manuscript was inspected as rendered contact sheets, with selected final pages checked at larger size. Paragraph and figure page breaks were reinspected after the last edits. The 12 square-table figures use 96% of the text width rather than 118%; the single-panel wider-difference plot uses 70%. The figures remain within the margins with readable labels. | Complete. |
| Source package | The named PDF, source ZIP and supplement ZIP are synchronized. The extracted package includes the bibliography, active source, all 22 figures and the result files needed by the audit. `SHA256SUMS.txt` validates the three named artifacts. | Complete. |
| Front matter | The title page, abstract and acknowledgements contain no drafting placeholders. The title page names the author's confirmed degree, “Master of Computer Science.” The declaration page remains excluded at the author's request. | Complete. |

The current main-text length diagnostic is 13,958 whitespace-separated tokens
from `pdftotext` on PDF pages 9-58 (printed pages 1-50). This includes
headings, captions, mathematical tokens and plot labels, so it is not a
prose-only word count. `git diff --check` passes for the thesis tree.

The 5 October Daniel Li-informed writing pass reviewed the abstract, all eight
chapters and the three active appendices. It strengthens concrete explanations
of sampling and variance-estimate variability, sharpens the literature-to-method
transition, puts findings before supporting rates, and removes repeated
commentary. Chapter 1 already meets those aims and is unchanged. The central
derivation steps and the existing evidence limits are retained.

A comparison against the pre-pass source verifies all 126 displayed
mathematics blocks, 17 table/figure blocks, reference labels, figure assets
and the occurrence counts of all 35 citation keys are unchanged. No
statistical source, population, saved result or working-draft file changed.
The evidence audit and 129 workspace tests pass. All 86 pages were rendered
and reviewed, with key revised pages inspected at larger size. Short
explanation units were kept together and a stale forced page break was
removed. The source archive now includes the Daniel Li review note linked
from the goal and README. The final isolated build, archive evidence audit,
37 bundled tests and delivery checksums also pass.

The subsequent 5 October paragraph-cohesion pass addresses overly fragmented
prose. Connected claims, evidence, explanations and qualifications now form
developed paragraphs in the literature, methods, design, results and closing
chapters. The conclusion has four paragraphs rather than eight; the practical
implications have three rather than five. Short passages around equations and
separate research questions retain their useful breaks. Apart from a two-word
contrast between earlier comparison methods, the prose wording is unchanged:
the improvement comes from grouping the existing argument, not padding it.
The new preference is recorded in the goal. Page-break controls prevent a
single prose line being detached from its paragraph, and the closing
future-work paragraph is kept together. Equations, tables, figures, citation
counts, scientific code and the working draft remain unchanged. The evidence
audit and 129 workspace tests pass; the delivery package is clean-built and
checked again after the final layout review.

The 4 October paragraph-coherence pass reviewed the abstract, all eight main
chapters and the active appendices. Mixed-focus passages were separated into
one main idea per paragraph, with evidence, explanation and transitions where
they advance the argument. Equations and their surrounding prose remain one
explanatory unit. The pass changed no mathematical formulas, numerical results,
experimental settings or references. The working draft was not rebuilt.

The opening paragraph of Section 2.4 was then rewritten to state the equal-MI
question directly, replacing abstract language about assessing predecessors.
This targeted wording change leaves the scientific scope unchanged.

The subsequent whole-thesis direct-explanation pass removed abstract framing,
immediate restatements, repeated method contrasts and incidental instructions
to the reader. Distinct literature findings, figure interpretations,
reproduction settings and useful intermediate algebra were retained.
Comparison with the pre-pass source confirms that every displayed equation,
table and figure inclusion is unchanged and all 36 bibliography keys remain.
The evidence audit passes. No statistical code or experimental result changed,
and the working draft was not rebuilt. The main-text length diagnostic fell
from 14,685 to 13,231 tokens, without changing typography or figure sizes.

The Chapter 5 opening was subsequently reorganised to explain the simulation's
purpose and fixed-population sampling before introducing the construction.
The standalone numerical-example section was removed. Its independence
tables, cell changes and resulting population pair now appear together after
the general construction rule, within Section 5.1. Every displayed equation,
table, reference label and citation in the chapter is unchanged, apart from
the ordering and automatic numbering. The revised manuscript remains 93
pages with 49 main-text pages. The evidence audit and build pass; the affected
pages were reinspected. No experiment or working-draft content changed.

The construction explanation was then simplified without replacing any
population. Section 5.1 introduces the binary example through a mixture of
copying and independent drawing, then explains larger tables through
four-cell probability transfers. The general matrix formula, transfer block
and feasible-strength equation are now in Appendix B, alongside the existing
numerical search and checks. Appendix B also shows the exact algebraic
equivalence between binary copying and the additive construction. The Chapter
6 figure settings use the same plain-language transfer description.

The binary mixture was checked against all 222 saved additive binary tables:
the largest cell discrepancy was \(1.11\times10^{-16}\). The numerical
example preserves the existing tables and MI values. The full evidence audit
passes; no statistical code, population, sampled result or figure changed,
and no simulation rerun was needed. The revised PDF has 94 pages, with the
same 49 main-text pages. The affected pages were rendered and inspected, and
the source archive was clean-built before refreshing the delivery checksums.
The working draft remains unchanged.

The appendix simplification replaces the five-appendix structure with:

- A, Supporting Calculations: the mean-zero sensitivity check, fixed-margin
  local expansions, MI/variance covariance, the independence boundary and the
  zero-component combined formula.
- B, Experimental Details: population formulas and searches, exact grids,
  rate denominators, paired intervals, numerical validity rules and the
  independent-pilot diagnostic.
- C, Additional Results: all 108 individual main null settings, two selected
  intermediate-shape curves and the six controlled comparisons cited by the
  main discussion.

The repeated MI-gradient and variance derivations and direct table
substitutions were removed because Chapters 2-4 already provide them. The
Student-tail convexity proof, independent-reference reconstruction and
resampling/transfer-entropy digressions were removed. The independence
calculation retains its positive-support and fixed-alphabet assumptions,
Taylor steps and likelihood-ratio limit, with no association-residual symbol
introduced solely to shorten the equation. Numerical derivative verification
is recorded in one paragraph.

Seven repetitive square-table plots and the aggregate null-band summary were
replaced by the complete individual-setting null table. Rejection and validity
remain separate, including the zero-validity n=2 settings. All six sensitivity
figures referenced in Chapter 6 remain; no main-text lead figure was removed.
The table generator and evidence audit were extended to check every table
value, the 15 included figures and exactly three active appendix inputs.
Population construction, test implementations, protocols and saved outcomes
are unchanged. The prior 94-page PDF and source ZIP are archived in
`archive/pre_appendix_simplification_2026-10-04/`.

The appendix-simplification PDF was 84 pages, down from 94 without changing the 49 main-text
pages or typography. All appendix pages and revised front-matter lists were
rendered and inspected. The evidence audit and 128 workspace tests pass;
the source and supplement were also checked in an isolated extraction before
refreshing the named deliverables and checksums. The working draft was not
rebuilt.

The subsequent targeted explanation pass adds intermediate steps within the
existing argument, without new theory or sections:

- Section 4.2 shows the substituted logarithm derivatives, the constant
  cancellation and the completion of the square in the variance sensitivity.
- Section 4.4 traces cell (1,1) from its count and margins to pointwise MI,
  its MI-variance contribution, the row and column conditional means, its
  variance sensitivity and its contribution to the sensitivity variance.
- Section 5.1 calculates the first joint probability directly from copying
  or independent drawing.
- Appendix A.2 explains the remainder notation and shows the multiplication,
  second-moment calculation and conditional-mean cancellation behind the
  local MI, variance and sensitivity approximations.

The added cell-level regression check passes, along with all 129 workspace
tests and the full evidence audit. The prior statistical formulas, worked
example totals, populations, test implementations and saved results are
unchanged. The final PDF has 86 pages, with 50 main-text pages and 24 appendix
pages. A stale forced page break was removed; short calculations and their
explanations are kept together. The affected pages and revised front-matter
lists were rendered and inspected, and the final source package was checked
in an isolated extraction. The named artifacts and checksums are refreshed;
the working-draft PDF was not rebuilt.

## Earlier Acceptance Record

The following dated records describe earlier manuscript states. They show how
the checks developed but are not the current release specification.

### Substantive and readability pass

T6 was completed on 16 September 2026. Each active chapter and appendix was
read once for scientific continuity and once for clarity. The pass used the
audited equations, sources, protocol and result rows as constraints; it did
not change the frozen evidence or add material for length alone.

| Part | Check and disposition |
| --- | --- |
| Chapter 1 | The estimand, weak null, four research questions, contribution and scope agree with the later method and evidence. No material change required. |
| Chapter 2 | Prior-work scope agrees with the expanded 36-source audit, including Hutcheson's direct information-theoretic comparison, general sandwich-df and higher-moment MI precedents. The first-order MI variance derivation now shows the Taylor expansion, cell-error collection, observation-level representation and variance calculation without skipped algebra. |
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

No active manuscript file contains a TODO or drafting placeholder. No personal
attestation has been invented.

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

The 27-28 September acceptance refresh tightened the abstract to one page,
removed duplicate contribution and chapter summaries, kept a variance
calculation together, and prevented the main landscape figures from
interrupting their interpretation mid-sentence. Two undefined uses of the
dimension shorthand in Chapter 6 were replaced by the full expressions.
The isolated reproduction also exposed a stale, empty list of figures in
the working PDF; a forced main build restored all 22 entries. The refreshed
PDF matches the clean archive reproduction on every full-page raster.
The source archive now also includes the detailed rewrite plan referenced
by its README and goal. No statistical implementation, frozen population,
simulation result or working-draft PDF was changed by this refresh.

At the 27-28 September acceptance refresh, the main text ended on printed
page 70 and Appendix A started on page 71. The current revision ends on
page 72 and Appendix A starts on page 73. Extracting pages 9-78 of the
earlier PDF with `pdftotext` gave 18,892
whitespace-separated tokens, including headings, captions, mathematical
tokens and plot labels. This is a repeatable secondary length diagnostic,
not a prose-only word count.

## Final verification record

The following checks were completed on 27-28 September 2026 for the earlier
97-page, 35-reference version:

- clean build from a fresh extraction of the final source archive;
- 97 A4 pages and 984,486 bytes before packaging;
- final named PDF SHA-256 `dd40de3b2fa4ea907eff6a351585e588896fa8297c1b60e47473679dccb7ceaf`;
- zero LaTeX errors, undefined citations or references, missing files, and overfull boxes;
- all 101 unit, derivation and experiment tests passed;
- complete evidence audit passed, including all 22 confirmatory thesis figures, every reported Chapter 6 value and the supplementary mechanism evidence;
- a fresh combined extraction of the source and experiment archives rebuilt
  the 3,111-configuration preflight, passed all 36 bundled tests, regenerated the
  22 confirmatory thesis figures and mechanism report, passed the evidence
  audit and compiled the 97-page thesis without using files from the working tree;
- the same extraction regenerated the complete 106-figure atlas; all 117 local
  atlas links resolve, including figures and evidence files;
- all 3,111 checkpoint identities and configuration fingerprints were checked;
  all 6,222 method rows and 3,111 paired rows reproduce the consolidated tables;
  unconditional, conditional and validity denominators, Monte Carlo standard
  errors and Wilson intervals were recalculated;
- 35 checked bibliography records, with every manuscript citation resolved and no unused records;
- all 97 pages covered by the full visual review and final-raster comparison;
- every full-page raster matches the regenerated clean archive build;
- working-draft PDF unchanged, SHA-256 `aa1024f12d853870665dda146497030a1484770ff939519a876a2cdf182abc02`;
- `git diff --check` passed for the thesis tree.

The 28 September derivation and citation refresh builds to 99 pages with 36
resolved bibliography entries and no LaTeX errors, undefined references or
citations, or overfull boxes. The affected pages were reinspected and the
deliverable checksums were refreshed. A fresh isolated build from the updated
source archive also produced 99 pages without warnings. The earlier full
raster comparison above is a historical check, not a claim that a new
whole-manuscript raster comparison was run after this text revision.

The subsequent targeted prose pass clarified the cancellation and conditional
means in Chapter 4, the alternative population constructors, and the three
standard-error comparisons in the Chapter 6 mechanism check. It also replaced
abstract wording in Chapters 2 and 7. No statistical implementation, protocol,
saved result or figure was changed. That revision built to 101 A4 pages
without LaTeX errors, undefined references or overfull boxes; the edited
passages and their page breaks were inspected at final size. This targeted
check does not replace the earlier whole-manuscript visual audit.

The subsequent Section 2.4 flow edit removed the Student-ratio derivation and
the squared-Wald digression from the background discussion. It retains a
short explanation of the Student rejection threshold before returning to MI;
the detailed distributional arguments remain in Chapter 4 and Appendix D.
At that stage the revised PDF had 100 pages. The build passes with no undefined references
or overfull boxes, and the revised passage was inspected in the rendered PDF.

The 29 September readability pass simplified the abstract, introduction,
literature synthesis, method bridges, discussion and conclusion without
changing the experiment or its numerical results. A further targeted pass
shortened the regression precedent, removed its redundant summary table, and
moved covariance, software validity and population-construction detail to the
appendices. The current PDF has 97 pages, with main text ending on numbered
page 67. Both the full manuscript and the working draft (Chapters 1--4 plus a
headings-only outline of the remaining chapters and appendices) rebuild
without missing references or overfull boxes.

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

## Administrative note

The declaration page was removed from the current version at the author's
request. If the School later requires a prescribed declaration, insert the
official form as a preliminary page; the thesis argument and evidence do not
change.

## Acceptance criteria

1. T1-T8 are closed with evidence and dates.
2. Every research question has an explicit answer supported by the derivation or results.
3. All final numerical statements and figures agree with the saved experiments and use the correct denominators.
4. Both editorial passes and the page-by-page visual review are complete.
5. The final PDF builds from the deliverable source package and all mathematical and evidence checks pass.
6. The PDF, source and experimental supplement are assembled.

Scientific writing, editing and verification can proceed throughout. Routine
decisions do not require another supervisor confirmation round. The goal is
complete when the final deliverables satisfy these checks and the detailed
acceptance criteria in `THESIS_GOAL.md`.
