# Welch-MI Thesis

## Active manuscript

The focused revision uses the design in
[FOCUSED_EXPERIMENT_PLAN.md](FOCUSED_EXPERIMENT_PLAN.md): three question-led
studies, estimation diagnostics and a four-setting construction check.
The original 232 settings and 68 population pairs have been simulated, with
20,000 table pairs per setting. The bounded extension in
[UNEQUAL_SAMPLE_CHECK_PLAN.md](UNEQUAL_SAMPLE_CHECK_PLAN.md) adds four unequal
allocations and reuses two balanced settings. The extension in
[LARGE_TABLE_CONSTRUCTION_CHECK_PLAN.md](LARGE_TABLE_CONSTRUCTION_CHECK_PLAN.md)
adds four matched 16 x 16 four-cell settings: 240 unique settings,
70 population pairs and 4,800,000 sampled pairs overall. The two statistical
methods are unchanged.

`main.pdf` is built from `chapters_rewrite/`, `appendices_rewrite/` and
`frontmatter/`. It presents five lead figures, a diagnostic table, a timing
table, three focused appendices and the complete 120-setting null table.
Interpretation accompanies each comparison. The degree is Master of
Computer Science. The thesis itself contains the scientific reproduction
details and does not require access to this project.

Section 6.5 is a self-contained application to the UCI Online Shoppers
Purchasing Intention dataset. It keeps the group selection, categorical
count-table construction, two full-data comparisons and interpretation
together. It does not add resampling results or change the simulation
design. Its numerical checks use the separate PracticalMIExploration
records and the original source data; the six-comparison exploratory
selection and Holm adjustment are disclosed in the section. Appendix C.7
identifies all six comparisons, their preparation and raw/adjusted p-values,
with the adjustment procedure explained beside the table.

The 11 October core pass strengthens the sparse-estimation literature and
resampling discussion, adds a short information-dynamics motivation, and
reduces repetition in the final chapters. It fixes detection-panel spacing,
negative-zero display and prose/table rounding in the report generator and
manuscript. No statistical method, simulation or older working draft changes.
The subsequent bounded jackknife diagnostic reuses 80,000 original table
pairs from four 16 x 16 copying settings. Appendix C.3 gives its formula,
settings, eight paired result rows and interpretation. Chapters 5 and 6
contain brief pointers; Chapters 3 and 4 and the primary two-method comparison
are unchanged. The diagnostic retains the original standard errors and normal
distribution cutoff, and reports both improved sparse difference estimates
and remaining calibration error. No new populations or samples are added.
The targeted consistency pass makes the main-text jackknife scope explicit,
focuses interpretation on the MI difference and its uncertainty, removes
calibration wording under alternatives, and places the empty-cell counts
beside the copying-population bias explanation. Section 2.3 and Chapters 3-4
remain unchanged in that pass. The subsequent explicit-naming pass replaces
vague references with the actual method or quantity throughout the abstract,
chapters and appendices, distinguishing rejection cutoffs, degrees of freedom,
MI bias correction and Holm's multiple-testing adjustment. Equations,
citations, methods, evidence and older working drafts are unchanged.
The explicit-comparison follow-up names the variables, populations, visitor
groups, methods and estimators where a comparison's subjects were unclear.
It distinguishes changes across alternatives from differences between
populations, while retaining clear local pronouns.
The Introduction narrative pass then gives the chapter one computing example
and a connected progression through sampling variation, the hypotheses,
the Wald baseline, Expanded Welch and the research questions. It removes
the additional stimulus-response example and corrective sampling caveat,
clarifies the evaluation trade-off, and retains the scientific contributions.
The lecture-aligned terminology pass defines MI through average uncertainty
reduction and names population MI directly in the controlled comparisons.
It introduces local MI, alphabet sizes, marginal probabilities and
undersampling alongside the existing academic terminology. Association
patterns retain their distinct meaning. The study, equations, citations
and older working drafts are unchanged.
The four remaining manuscript uses of "inference" are replaced with the
specific task: tests in the title, the Normal Wald test, MI uncertainty
and comparisons, or methods for comparing an MI index. Bibliographic
publication titles remain unchanged.
The power-terminology pass introduces statistical power with a definition,
then uses power in the alternative comparisons, headings and supporting
tables. Curves that include equal MI retain rejection-rate captions; their
zero point estimates false positives rather than power. The two table
reporting templates use the same terminology. No glossary is added, and
no calculations, numerical evidence or historical working drafts change.
The current PDF has 102 pages, including 59 main-text pages; verification is
recorded in SUBMISSION_CHECK.md.

Two saved-sample analyses directly check the variance-variability prediction
at six existing null settings and the estimated direction among rejections
at four existing alternatives. Their appendix tables and main-text readings
add no populations or sampled table pairs. The generator is
`report_focused_mechanisms.py`; its evidence includes deterministic
Monte Carlo precision checks by resampling paired variance/sensitivity
outputs, not observations.

The goals and writing preferences are in [THESIS_GOAL.md](THESIS_GOAL.md).
The current verification record is [SUBMISSION_CHECK.md](SUBMISSION_CHECK.md),
and the mathematical and evidence checks are in
[SCIENTIFIC_AUDIT.md](SCIENTIFIC_AUDIT.md). Earlier records below their current
sections are historical. The earlier thesis source, PDF and deliverables
are preserved in `archive/pre_focused_20261006/`; the previous simulation
archives remain unchanged. The working-draft PDF has not been rebuilt.

## Build

The source archive is self-contained for compilation. From its thesis
directory, run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

To regenerate the figures with the supplement beside the source directory,
run its `WelchSatterthwaiteMI/experiments/report_focused_study.py` and supply
`--figures` with this source directory's `figures_rewrite/` path. This makes
the source and supplement usable without the original workspace layout.

In the development workspace, the experiment commands are:

```bash
python WelchSatterthwaiteMI/experiments/run_focused_study.py preflight
python WelchSatterthwaiteMI/experiments/run_focused_study.py pilot
python WelchSatterthwaiteMI/experiments/run_focused_study.py full
python WelchSatterthwaiteMI/experiments/run_focused_study.py audit
python WelchSatterthwaiteMI/experiments/run_focused_study.py timing
python WelchSatterthwaiteMI/experiments/audit_focused_study.py
python WelchSatterthwaiteMI/experiments/report_focused_study.py
python WelchSatterthwaiteMI/experiments/run_unequal_sample_check.py audit
python WelchSatterthwaiteMI/experiments/report_unequal_sample_check.py
python WelchSatterthwaiteMI/experiments/report_focused_mechanisms.py
python WelchSatterthwaiteMI/experiments/run_large_table_construction_check.py audit
python WelchSatterthwaiteMI/experiments/report_large_table_construction_check.py
python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py audit
python WelchSatterthwaiteMI/experiments/report_focused_jackknife_check.py
```

Use the pinned packages in `WelchSatterthwaiteMI/requirements-thesis.txt`.
The full run resumes verified fixed-size chunks; the pilot uses separate
streams and output. `--batch-size` and `--workers` affect resource use, not
the simulated samples. A changed scientific-source fingerprint requires
a separate output directory. Set `MPLCONFIGDIR` to a writable directory
when running in a restricted environment.

## Evidence and presentation

`WelchSatterthwaiteMI/results/focused_study/` contains the population
definitions and arrays, configuration/display manifests, method rates,
paired contrasts, estimation diagnostics, timing records and audits.
Its `records/` directory retains all per-repetition scalar outputs in
checksum-verified NPZ chunks. These large reproducible checkpoints are
not versioned; the compact definitions and summaries are retained.
The separate `results/unequal_sample_check/` directory holds all six allocation
comparisons, with identical copies of the two original balanced records.
The separate `results/large_table_construction_check/` directory contains
the four newly sampled first-block transfer settings. Its reporter compares
these with the four original copying settings, including estimated direction.
The separate `results/focused_jackknife_check/` directory contains the
four saved-sample jackknife comparisons. Its audit regenerates all 80,000
original input pairs, checks their baseline outputs, and reproduces the
diagnostic records and summaries exactly.

All eight new figure assets are exported at their intended printed width
of 148 mm with 8 pt ticks and 9 pt main labels. Null figures use matching
rejection panels and validity strips. The detection companions show the
full effect range without compressing the small-effect main figures.
The layout tests verify printed geometry, label bounds, CSV selection and
unaltered plotted values:

```bash
python -m unittest discover -s WelchSatterthwaiteMI/tests -p 'test_*.py'
python -m unittest discover -s DifferentialMI/tests -p 'test_*.py'
```

The named thesis PDF, self-contained source ZIP, full experimental
supplement ZIP and checksums are generated by `package_deliverables.py`.
The supplement includes the raw scalar chunks needed by the independent
audit. Earlier broad-study figures, evidence scripts and plans remain
historical and are not used to produce the focused manuscript.
