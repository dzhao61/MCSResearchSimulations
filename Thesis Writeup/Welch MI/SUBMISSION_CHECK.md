# Thesis completion check

## Targeted consistency and standalone adjustment: 11 October 2026

The five approved review findings are addressed. Section 6.5 points to
Appendix C.7's compact six-comparison table, with raw and separately
Holm-adjusted p-values for both methods, group/predictor/outcome definitions,
relevant preparation and the adjustment procedure. The two additional
dataset citations have primary-source-checked metadata. The main text
identifies the jackknife check's unchanged standard error and normal
distribution cutoff, focuses practical interpretation on the MI difference
and its uncertainty, removes calibration wording under alternatives,
and keeps copying-population sparse-cell counts beside their bias
explanation. Section 2.4 names its conditions instead of using
"regular positive-support" shorthand.

All 217 workspace tests pass: 174 Welch-project, 27 DifferentialMI and
16 practical-data tests. Two new application tests independently recompute
all six comparisons and their Holm adjustments, protect all 24 rounded
table values and check the standalone inputs/citations. The jackknife
reporting test now requires explicit main-text method/cutoff scope.
All 10773 scientific-source, input and result preservation hashes match.
Section 2.3, Chapters 3-4 and the older working-draft source/PDFs are
unchanged. No statistical method, population, experiment or sampled record
changes; the simulation scope remains 240 settings, 70 population pairs
and 4800000 sampled pairs.

The PDF has 100 A4 pages: eight front-matter, 57 main-text, 30 appendix and
five bibliography pages. The main-text token diagnostic is 17358, using
pdftotext on PDF pages 9-65; this includes captions, equations and labels.
The final build has no warnings, unresolved citations/references, missing
characters or overfull/underfull boxes. Affected prose, contents, table
list, appendix opening, new table and bibliography pages are visually
checked. The bibliography has 47 entries, 46 cited.

The extracted source archive rebuilds the same 100 pages with identical
pdftotext output and no build warnings or layout boxes. The named PDF
matches main.pdf. Both archives pass CRC, inventory and member-content
hash checks: 56 source members and 10004 supplement members. Delivery
checksums match. The four full evidence audits remain recorded in the
preceding pass; they were not rerun for this wording and reporting pass.

## Bounded jackknife appendix addition: 11 October 2026

Appendix C.3 gives the approved four-setting diagnostic, including the
delete-one formula and intermediate algebra, occupied-cell weighting,
fixed standard error and normal distribution cutoff, exact populations,
all eight paired result rows and an integrated interpretation. Chapter 5
contains a short description beside estimation diagnostics, and Section
6.3.1 reports the direction improvement and low null rejection together.
Chapters 3 and 4 are unchanged. The check replaces the analytic correction
and does not evaluate a jackknife standard error or jackknife Expanded Welch.

All four original 16 x 16 different-skew copying settings are reported:
MI pairs (0.02,0.02)/(0.02,0.03), at n=1000/10000, with 20000 paired
repetitions each. Every calculation is valid. At n=1000, difference bias
falls mainly because similar positive individual MI biases cancel; wrong-
direction rejections fall from 2009 to 5. The unchanged standard error
still overestimates observed variability, and null rejection is 0.845%.
At n=10000 the null rate is 5.070%, but alternative detection and RMSE
do not improve. The text reports the gains and limitations together.

All 215 workspace tests pass: 174 Welch-project, 27 DifferentialMI and
14 practical-data tests. Fourteen diagnostic tests and five reporting tests
cover exact saved outputs, scope, literal/weighted deletion, replacement
of the analytic correction, unchanged standard error, rejection direction,
Monte Carlo precision, eight-row table generation and manuscript values.
The jackknife audit regenerates all 80000 original count-table pairs and
reproduces all records and summaries exactly. The original three independent
audits also pass. No original methods, populations or sampled records change;
the combined study remains 240 settings, 70 pairs and 4800000 distinct samples.

The main PDF has 99 A4 pages: eight front-matter pages, 57 main-text pages,
29 appendix pages and five bibliography pages. Its build has no warnings,
unresolved citations/references, missing characters or overfull/underfull
boxes. The affected main-text, contents, table-list and appendix pages
have been rendered and visually checked. Existing figures, typography
and main-text length are unchanged. The pre-addition manuscript and
delivery source/PDF are preserved in archive/pre_jackknife_20261011/manuscript.tar.
Preservation hashes match for Chapters 3-4 and the original working-draft
source/PDF plus named Working Draft and Working Draft v2 PDFs. No working
draft was edited or rebuilt.

The independently extracted source builds the same 99 pages and identical
pdftotext output, without warnings. The combined source/supplement extraction
passes all 117 bundled tests (90 Welch-project and 27 DifferentialMI), with
no skips, and all four audits. It regenerates the new jackknife table and
evidence JSON byte-for-byte. The source archive has 56 members; the supplement
has 10004, including the diagnostic runner, reporter, tests and records.
Archive CRC, inventory, member SHA-256 and delivery checksum checks pass;
the named PDF matches main.pdf. The supplement instructions explain both
auditing the delivered evidence and reproducing it in a separate directory.

## Core literature and presentation fixes: 11 October 2026

The approved main fixes are implemented without changing the statistical
methods, population definitions, sampled records or application results.
Section 2.2 now explains analytical, coverage-based and Bayesian approaches
to sparse information estimation, their entropy-to-MI connection and their
conditions. Seven primary-source-checked references are added, including
a 2024 study. Section 2.4 explains separate-sample bootstrap uncertainty
and the unobserved-cell difficulty without treating computational cost as
a statistical reason to exclude it. Chapter 1 adds an independent-trial
information-dynamics motivation. Existing Welch-Satterthwaite precedents
remain credited, and Section 2.3 is identical to the pre-pass source.

The abstract and Introduction identify the larger-cutoff rejection reduction
as a consequence of the method. Chapters 6-8 retain the empirical bias,
direction and validity findings, with less repeated numerical discussion.
The outdated future real-data-evaluation sentence is corrected to reflect
the completed shopping application. The focused report generator fixes the
overlapping panel labels in Figures 6.4 and C.2 and displays null differences
as zero rather than negative zero in Table C.6. The observed SD is consistently
0.01449, and the 8 x 8 uniform n=100 Wald rate is consistently 0.0736.

All 196 workspace tests pass: 155 Welch-project, 27 DifferentialMI and 14
practical-data tests. Three additional tests cover displayed zero,
source-derived manuscript rounding and citation-key consistency; the existing
eight-figure geometry test now also checks upper-label/lower-title overlap.
All three independent raw-record audits pass. All 4879 preservation hashes
match, covering tracked method sources, simulation records, practical inputs
and results, the earlier working-draft artifacts and unchanged Chapters 3-4.
No working draft was edited or rebuilt. The pre-pass manuscript and delivery
PDF/source are preserved in archive/pre_core_fixes_20261011/manuscript.tar.

The main PDF has 97 A4 pages: eight front-matter pages, 57 main-text pages,
27 appendix pages and five bibliography pages. The source bibliography has
45 entries, with 44 cited in the manuscript. The final build has no warnings,
unresolved citations/references, missing characters or overfull/underfull boxes.
The affected prose, figures, table and bibliography pages have been visually
checked. The introduction roadmap fits with its scope paragraph instead of
spilling onto a nearly empty page. Unchanged plots retain their original PDFs;
regeneration was checked to differ only in creation-date metadata.

The named PDF, source ZIP, experiment supplement and delivery checksums are
refreshed. All 54 source-archive members and 9989 supplement-archive members
match the workspace, with CRC and SHA-256 checks passing. The isolated source
build produces the same 97 pages and identical pdftotext output without
warnings. The combined extraction of the two archives passes all 98 bundled
tests (71 Welch-project and 27 DifferentialMI), with no skips, and all three
independent audits. It regenerates nine table fragments and three evidence
JSON files byte-for-byte; all eight figure PDFs match after excluding
creation-date metadata. The standalone supplement skips only its existing
manuscript-consistency check when the separate source archive is absent.
No optional jackknife or bootstrap experiment was run.

## Self-contained shopping application: 11 October 2026

Section 6.5, Application to Online Shopping Data, is complete on printed
pages 50-51. Its question, data preparation, group sizes, category definitions,
bias corrections, result table and interpretation stay together in Chapter 6.
It compares month-purchase and weekend-purchase MI between 1694 new-visitor
and 10551 returning-visitor sessions. The methods, simulation design and
simulation counts are unchanged. No subset analysis is added to the manuscript.
The section discloses its selection from six exploratory comparisons and
reports the original six-comparison Holm adjustment. The dataset and Holm
procedure have primary-source citations. The conclusion now acknowledges
the application rather than proposing it as unfinished future work.

All 193 workspace tests pass: 152 Welch-project, 27 DifferentialMI and 14
practical-data tests. Four new application regression tests check the original
source count tables, preparation and sparse-cell details, independently
recomputed estimates/standard errors/statistics/degrees of freedom/p-values,
the rounded manuscript table and body values, the six-comparison adjustment
and the self-contained section structure. All 30 saved subset-record hashes
also match their original checksums; those records are not used in the thesis.

The main PDF has 95 A4 pages: eight front-matter pages, 56 main-text pages,
27 appendix pages and four bibliography pages. The two application pages
and revised conclusion have been visually checked. The result table fits
within the text margins at the existing body font size. Main and isolated
source builds have no warnings, unresolved references/citations, missing
characters or overfull/underfull boxes. The isolated source builds to the
same 95 pages and identical pdftotext output. All 54 source-archive members
match the workspace files, and the named PDF matches main.pdf.

The named PDF, source ZIP and delivery checksum manifest are refreshed.
The large experimental supplement remains unchanged and retains its
simulation-only scope; the separate PracticalMIExploration records hold the
application's numerical evidence. Preservation hashes match for all 11
tracked method-source files, 4853 tracked simulation-result files, 12 tracked
practical-data/input-result files and six older working-draft artifacts.
No working draft was edited or rebuilt. The pre-addition manuscript and
delivery source/PDF are preserved in
archive/pre_shoppers_20261011/manuscript.tar. Earlier checks below remain
historical verification of their respective versions.

## Matched large-table construction check: 10 October 2026

The approved four-setting construction check, contribution alignment and
examiner-focused claim/evidence review are complete. The extension compares
16 x 16 different-skew four-cell transfer populations with the four existing
copying settings at MI pairs (0.02, 0.02) and (0.02, 0.03), each at n=1000
and 10000. It adds 80000 sampled table pairs without changing either method
or any original samples. The combined scope is 240 unique settings, 70
population pairs and 4800000 distinct sampled pairs.

At n=1000, the four-cell null has difference bias 0.03145 nats and rejection
rates 0.30945 for Wald and 0.29770 for Expanded Welch. At the alternative,
2493 of 2494 Wald rejections and 2350 of 2351 Expanded Welch rejections have
the opposite estimated direction. The estimation failure therefore occurs
under both tested constructions. At n=10000, the four-cell null rates are
0.04990 and 0.04910, and all alternative rejections have the correct sign.
Detection differs between constructions, so the manuscript reports agreement
on the sparse failure rather than identical performance or universal
robustness. Complete matched results are in Appendix C; Chapter 6 gives
brief interpretations alongside the main bias and direction findings.

All 179 workspace tests pass (152 Welch-project and 27 DifferentialMI),
including 11 new construction-check tests. All three independent raw-record
audits pass. The new runner, reporter, records, scientific construction
details and reproduction instructions are included in the delivery packages.
Normal Wald and Expanded Welch remain the only compared methods.

The main PDF has 93 A4 pages: eight front-matter pages, 54 main-text pages,
27 appendix pages and four bibliography pages. Its main-text diagnostic is
16172 whitespace-separated pdftotext tokens on PDF pages 9-62, including
headings, captions, equations and plot labels, not prose-only words.
All citations/references resolve with no warnings, missing characters or
overfull/underfull boxes. All 93 pages have rendered visual coverage, with
the new table, main-text interpretations and construction equations also
inspected at larger size. No page-count or global typography adjustment was
made; the supporting table uses locally reduced column spacing to stay
within the text margins.

The extracted supplement passes all 97 bundled tests (70 Welch-project and
27 DifferentialMI), with no skips, and all three independent raw-record
audits. It reproduces all nine table fragments and three evidence JSON files
byte-for-byte. All eight figure PDFs have identical content after excluding
creation-date metadata. The isolated source builds to the same 93 pages
and exactly the same pdftotext output, without warnings or unresolved
references. ZIP CRC checks pass, and all 54 source-archive members and 9989
supplement-archive members match their workspace files. Delivery SHA-256
checks pass, and the named PDF matches main.pdf.

The 43 pre-pass preservation hashes match: older working drafts, original
method and experiment code, original population/summary records and figure
assets are unchanged. Chapters 2-4 and Appendix A were not edited. The
pre-pass manuscript/source is preserved in
archive/pre_construction_20261010/manuscript.tar. No working draft was rebuilt.
The named PDF and packages are refreshed. Older records below remain
historical verification of their respective versions.

## Saved-sample mechanism checks: 10 October 2026

The approved direction check, direct variance-estimate variability check and
conclusion alignment are implemented. Both analyses revealed interpretable
findings and are reported in Chapter 6, with complete calculations and two
supporting tables in Appendices B-C. Neither analysis changes the methods,
experiment settings, populations or sampled-pair count.

All 168 workspace tests pass (141 Welch-project and 27 DifferentialMI),
including 13 new mechanism tests. Both independent raw-record audits pass.
The mechanism reporter recomputes population sensitivities, verifies the
saved rejection totals and regenerates its two tables and evidence JSON.

The main PDF has 91 A4 pages: eight front-matter pages, 54 main-text pages,
25 appendix pages and four bibliography pages. Its main-text diagnostic is
15967 whitespace-separated pdftotext tokens on PDF pages 9-62, including
headings, captions, equations and plot labels, not prose-only words.
All citations/references resolve with no warnings, missing characters or
overfull/underfull boxes. All 91 pages have rendered visual coverage; the
new tables and main-text interpretations were also inspected at larger size.
No typography changes were made to adjust length.

Chapters 2-4, Appendix A, all eight figure assets, method code, original
population/summary records and older working drafts retain their pre-pass
hashes. The pre-pass manuscript/source is preserved in
archive/pre_mechanism_20261010/manuscript.tar. No working draft was rebuilt.

The extracted supplement passes all 86 bundled tests (59 Welch-project and
27 DifferentialMI), with no skips, and both independent raw-record audits.
It reproduces all eight table fragments and both evidence JSON files
byte-for-byte. All eight figure PDFs have byte-identical content after
excluding their creation-date metadata; the original figure assets remain
unchanged. The isolated source builds to the same 91 pages and exactly the
same pdftotext output, without warnings or unresolved references. Both ZIP
CRC checks and all delivery SHA-256 checks pass. The named PDF and packages
are refreshed. Older dated records below remain historical verification of
their respective versions.

## Unequal-sample extension: 10 October 2026

The approved fixed-total allocation check and final verification are complete.
Six comparisons reuse two balanced settings
and add four unequal settings. The combined evidence is 236 settings, 68
population pairs and 4720000 distinct sampled table pairs. Neither statistical
method nor the original population/simulation records changed.

All 155 workspace tests pass (128 Welch-project and 27 DifferentialMI).
Both independent audits pass, including exact allocation scope, checkpoint
provenance, copied balanced records and unequal correction/variance/df
calculations. The new appendix table is generated from audited summaries,
and tests verify its selection, numerical values and rendered text fragment.

The main PDF has 89 A4 pages: eight front-matter pages, 54 main-text pages,
23 appendix pages and four bibliography pages. All citations and references
resolve with no warnings, missing characters or overfull/underfull boxes.
All pages are covered by rendered visual review, with the final allocation
table inspected at full size. Its interpretation stays on the same page;
the original figures, typography and Chapters 2-4 are unchanged.

The source and experimental supplement include the allocation runner,
reporter, eight tests, full records and replication instructions. The
extracted supplement passes all 73 bundled tests (46 Welch-project and 27
DifferentialMI), both independent evidence audits and byte-identical
regeneration of the allocation table and its evidence JSON. The extracted
source builds cleanly to 89 pages and exactly the same pdftotext output as
the workspace PDF. Both ZIP CRC checks and all delivery SHA-256 checks pass.
The named PDF and packages are refreshed. Older dated checks below remain
historical records of their respective versions.

The pre-extension manuscript is preserved in
`archive/pre_unequal_20261010/manuscript.tar`. No working draft has been
edited or rebuilt. The unversioned source retains SHA-256
`b0e8aaf52ac589cf6cab551e1cf1ae31536d1a04339010b6f52090e80adeb419`.
The unversioned PDF and Working Draft.pdf retain
`ef4d9a7f39101ed0cb4f0624179d5fd32b78bc765e917d5d2d08656f4b260897`;
Working Draft v2.pdf retains
`a8f6f47cc3f8b660dc3269d0fdcb2765ff5702bb06949da9deffad4b8f7de932`.

## Targeted depth pass: 7 October 2026

The approved edits in THESIS_DEPTH_PLAN.md develop the computing motivation,
closest-method literature synthesis, design rationale, results mechanisms,
practical implications and future-work priorities. There are no new
experiments, figures, test variants or typography changes. The active PDF
has 87 A4 pages: eight front-matter pages, 54 main-text pages, 21 appendix
pages and four bibliography pages. The main-text diagnostic is 15,396
whitespace-separated `pdftotext` tokens from PDF pages 9-62, including
captions, equations and plot labels, not a prose-only word count.

All 147 workspace tests and the independent raw-record audit pass. Three
new regression checks verify the added bias arithmetic, numerical cutoffs
and margin-related precision examples directly from the saved diagnostics.
The build resolves all citations and references and has no warnings,
missing characters or overfull/underfull boxes. All pages have been covered
by rendered contact-sheet review, with the new calculations, design layout
and conclusion also inspected at larger size. Short calculations stay with
their introductions; the design summary table no longer interrupts a
paragraph. The methods in Chapters 3-4 and all figure assets are unchanged.

The extracted source builds to the same 87 pages and exactly the same
`pdftotext` output as the workspace manuscript, without warnings or unresolved
references. All 38 bundled Welch-project tests and 27 DifferentialMI tests
pass, as does the independent audit using the extracted repetition records.
The named PDF and source/supplement packages are refreshed. The original
unversioned working-draft PDF and Working Draft.pdf retain SHA-256
`ef4d9a7f39101ed0cb4f0624179d5fd32b78bc765e917d5d2d08656f4b260897`;
Working Draft v2.pdf retains
`a8f6f47cc3f8b660dc3269d0fdcb2765ff5702bb06949da9deffad4b8f7de932`.
No working-draft source was edited.
The pre-pass manuscript/source snapshot is in
`archive/pre_depth_20261006/manuscript.tar`. Earlier working drafts remain
historical artifacts; this pass does not request or produce Working Draft v3.

## Focused revision: 6 October 2026

The current PDF is the focused-study manuscript, with 81 A4 pages: eight
front-matter pages, 48 main-text pages, 21 appendix pages and four bibliography
pages. It uses five lead figures, a compact diagnostic table, a small timing
table, three companion figures and the complete 120-setting main null table.
All 81 pages have been reviewed as rendered contact sheets. Main-text length
is 13,369 whitespace-separated `pdftotext` tokens from PDF pages 9-56, including
captions, equations and plot labels; this is not a prose-only word count.

The 232-setting, 68-population-pair run is complete at 20,000 repetitions per
setting. All 117 Welch-project and 27 DifferentialMI tests pass. The independent
audit verifies all raw records, regenerates 3,944 sampled inputs, and checks
population construction, p-values, rates, uncertainty and diagnostics. All
eight new figure layouts have tested printed bounds and unchanged plotted
values. The final build resolves all citations and references and has no
errors, missing characters or overfull boxes. The association-strength heading
was shortened to remove its awkward spacing. The degree remains Master of Computer
Science, and the working-draft PDF has not been rebuilt.

The extracted source compiles from a clean directory to the same 81 pages
and exactly the same `pdftotext` output. The extracted supplement passes all
35 bundled Welch tests and 27 DifferentialMI tests, and passes the full
independent audit against its own raw records. Its report generator reproduces
all eight rendered figures and five table fragments byte-for-byte. ZIP CRC
checks and the three delivery checksums pass. The source archive has 44 files;
the supplement has 9,551 files, including all raw scalar chunks. The report
generator's final status line was subsequently corrected to say five tables;
this does not change any generated output or scientific-source fingerprint.
T1-T8 are complete for the focused revision.

The preceding manuscript and deliverables are preserved under
`archive/pre_focused_20261006/`; all earlier simulation archives are unchanged.
The remaining dated records below apply to that earlier manuscript, not the
new study's counts, findings or artifacts.

## Historical verification records

The earlier 6 October 2026 record below verifies the pre-focused thesis and deliverables.
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

T1-T8 are complete for the 6 October revision.

| Area | Evidence available | Status |
| --- | --- | --- |
| Manuscript | The standalone A4 PDF has 86 pages, including 51 numbered main-text pages and three focused appendices occupying 23 pages. Chapter 6 contains seven lead figures; Appendix C contains eight supporting figures and all 84 reported main null settings. File inventories, local paths, build commands, configuration IDs and protocol-freeze records are excluded from the reader-facing manuscript. | Complete. |
| Mathematics | `SCIENTIFIC_AUDIT.md` records independent derivative, worked-example and implementation checks. The 102 Welch-project tests, 27 DifferentialMI tests and 37 archive-bundled tests pass. The added cell-level check verifies the intermediate pointwise MI, conditional means, variance contribution and variance sensitivity in Section 4.4; the binary construction check also verifies Section 5.1's new first-cell calculation. The condensed independence calculation also passes 30 independent positive-table finite-difference checks. | Complete. |
| Literature | `LITERATURE_SOURCE_CHECK.md` records the claim checks supporting all 35 remaining active references. The removed transfer-entropy aside and its citation are retained in the historical source check. The clean build resolves every citation. | Complete. |
| Experimental evidence | The full audit reconstructs the original protocol and independently selects all 2,760 reported configurations with both samples at least 10. It verifies all 12 plain Table 5.2 counts, Chapter 6 claims, all 22 available figures, the 15 included figures, all 336 rejection/validity values in the 84-setting null table, paired results, convergence, runtime and supplementary mechanism diagnostics against saved rows. It passes both in the workspace and in the extracted archives. | Complete. |
| Build | A clean build from the extracted source produces 86 A4 pages with the same extracted text as the working PDF. The log has no errors, undefined citations or references, missing characters or overfull boxes. | Complete. |
| Visual presentation | All 86 pages were inspected as rendered contact sheets in the preceding pass. This table simplification changes only PDF pages 42-43, which were checked again at larger size; all other rendered pages match the preceding version. The 22 figure assets are unchanged. All three-column plots are 142 mm wide, two-column plots 116 mm and the single-panel plot 85 mm. Panels share a 34 mm height; ticks are 8 pt and titles, axis labels and legends 9 pt. The PDFs are included at native size, within the text margins. Nine layout, five scope and two table regression tests pass. | Complete. |
| Source package | The named PDF, source ZIP and supplement ZIP are synchronized. The extracted package includes the bibliography, active source, all 22 figures and the result files needed by the audit. `SHA256SUMS.txt` validates the three named artifacts. | Complete. |
| Front matter | The title page, abstract and acknowledgements contain no drafting placeholders. The title page names the author's confirmed degree, “Master of Computer Science.” The declaration page remains excluded at the author's request. | Complete. |

The current main-text length diagnostic is 13,700 whitespace-separated tokens
from `pdftotext` on PDF pages 9-59 (printed pages 1-51). This includes
headings, captions, mathematical tokens and plot labels, so it is not a
prose-only word count. `git diff --check` passes for the thesis tree.

The 6 October sample-size revision applies the same rule across every
statistical family: both populations have at least 10 observations. It removes
351 of the original 3,111 unique configurations from the reported study,
leaving 2,760 configurations and all 534 population pairs, each sampled 20,000
times, for 55,200,000 table pairs. The main grid has seven sample sizes and
504 configurations; extreme skew has 180, rare-cell stress 80 and exact
independence 108. The other family counts and all plotted values are unchanged.
The abstract, design totals, bracketed count breakdowns, exact grids and
main-null table agree with this scope. The n=5-specific discussion and macros
are removed. Original simulation files, the full protocol, statistical code,
all figure PDFs, their manifest and the working draft are unchanged.

All 129 scientific workspace tests and 14 figure/scope tests pass. The evidence
audit retains its full-archive reconstruction and adds independent checks of
the reported subset; it does not rewrite the original protocol. The clean
archive build, archive evidence audit, 37 bundled scientific tests and 14
figure/scope tests pass. Delivery checksums validate the refreshed PDF and
source package alongside the unchanged experiment supplement.

The subsequent 6 October Section 5.3 simplification restores the earlier
family/count/description table and removes the bracketed arithmetic, positional
key and highlighted paragraph about overlapping family counts. The current
sample-size range and all configuration counts are preserved. The audit now
checks the 12 plain counts directly; two regression tests verify the table and
reject an incorrect main-family count. All 16 figure/scope/table tests and the
evidence audit pass in the workspace and extracted source package. The clean
build reproduces the working PDF text, with no undefined references, citations
or overfull boxes. No scientific implementation, stored result, figure or
working-draft file changed. The refreshed deliverable checksums pass.

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

The subsequent 5 October indentation fix standardises all 23 bold mini-headings
using the same unindented-opening rule as numbered headings. Later new
paragraphs remain indented; equation continuations keep their existing
paragraph structure. PDF coordinates verify all 23 heading/opening alignments.
The Chapter 4 closing explanation is kept together to avoid a two-line spill
onto a separate page. Source comparison confirms that the manuscript changes
are formatting substitutions and page-break controls only. All 126 displayed
mathematics blocks, 17 table/figure blocks and 35 citation occurrence counts
are unchanged, as are the scientific code, evidence and working draft.
The evidence audit passes. All 87 pages were rendered and reviewed, with
affected pages checked at larger size; the refreshed source archive builds
cleanly and reproduces the working PDF text. Delivery checksums pass.

The binary example's heading was then changed to "Constructing a non-independent
2 x 2 joint distribution" to identify its purpose explicitly. The example
and calculations are unchanged. The affected pages were reinspected; the PDF
remains 87 pages and the refreshed source package builds cleanly.

The subsequent 5 October figure-layout pass removes inconsistent export sizes
and LaTeX scale factors. Shared three-column, two-column and single-panel
templates give every plot the same printed panel height, typography, markers
and line widths. Fixed PDF canvases prevent different tick labels from changing
the printed scale through tight cropping. Longer titles wrap within their
panels; repeated tick labels are omitted and the same three labelled MI-axis
positions are used consistently. Axis ranges and all plotted values remain
unchanged.

All 22 figure selections, source columns and denominators match the pre-pass
manifest. Numerical macros and both generated result tables are byte-identical.
The full evidence audit and nine new layout tests pass, including physical PDF
dimensions and clipping/crowding checks. The body text and scientific sources
are unchanged. The lower token diagnostic reflects plot-label changes, not
removed prose. The working draft is unchanged. The 87-page PDF and source
package were rebuilt and visually checked; an isolated source build reproduces
the same extracted PDF text, and archive audits, layout tests and delivery
checksums pass.

Table 5.2 subsequently gains a bracketed, italic breakdown under each
configuration count and a four-position key beneath the column heading.
The grouped positions count shape/pattern choices, margin choices,
MI/construction choices and sample-size pairs. Nested products separate
starting MI, MI difference and construction choices where relevant. Explicit
sums account for shape-specific patterns, the single equal-MI case in the
imbalance grid and additional rare-block convergence controls. The evidence
audit parses and evaluates all 12 printed breakdowns, checking their totals
against the saved distinct configurations and runtime regimes. The table fits
on its existing page with readable text; the surrounding Chapter 5 prose,
scientific settings, figures and working draft are unchanged. The manuscript
remains 87 pages. The affected pages were rendered and checked, and the
refreshed source package builds cleanly and reproduces the working PDF text.

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
