# Welch MI approximation and test redesign

This independent copy contains the fresh 366-setting four-rule study and the versioned Working Draft v3 manuscript. Original folders in the parent workspace are preserved. The original-file SHA-256 manifest is at the copy root.

## Current experiment

The weak null is H0:I(P)=I(Q), allowing distinct joint probability tables. The rules share the same bias-corrected categorical MI difference and influence-function standard error: normal Wald; sample-size degrees of freedom using n_i exactly; unchanged Expanded Welch; and a fixed, independently fitted moment reference.

There are 366 distinct evaluation settings and 186 null fitting settings, each with 100,000 independent table pairs. Total: 55.2 million pairs. All 312 previous settings are rerun, the complete MI sweep adds 30, and focused SD-scaled alternatives add 24. The technical pilot uses separate streams and 200 pairs per batch.

The 22 October calibration sensitivity extension adds six upper equal-MI populations: A/B/C at two and four original null SDs. Each has 100,000 fresh fitting and 100,000 independent validation pairs, adding 1.2 million pairs (56.4 million including the base redesign). Both MI values equal the fixed alternative's larger MI; margins, dimensions, sample sizes and construction are unchanged. Both calibrations use the same saved alternative pairs, and both are validated at both null populations. This measures population-specific calibration, not size control over the composite null.

The 174-setting core checks the mean and sampling variance of Vhat separately, the implied population and plug-in degrees of freedom, and Appendix A.4 predictions. Focus settings A/B/C are 4x4 uniform n20, 8x8 different skew n100 and 4x4 different skew n10000. Null reference degrees of freedom stay fixed across each alternative curve. Independent empirical calibration fits variable-df p thresholds and a common absolute-T threshold for Wald/reference. A 1,000-repetition paired bootstrap includes calibration uncertainty.

Finite zero Vhat values belong in moment calculations. Positive-finite df summaries state inclusion counts. Rejection rates retain all-attempt, method-valid and four-method common-valid denominators. The reference contrast does not isolate estimation error; bias/correlation/shape diagnostics do not establish separate causal effects.

## Run and verify

Install `requirements-thesis.txt` in a Python environment. From the directory containing WelchSatterthwaiteMI and DifferentialMI:

```bash
python WelchSatterthwaiteMI/experiments/redesign_study.py preflight
python WelchSatterthwaiteMI/experiments/redesign_study.py pilot --output WelchSatterthwaiteMI/results/redesign_technical_check --workers 4
python WelchSatterthwaiteMI/experiments/redesign_study.py all --workers 4
python WelchSatterthwaiteMI/experiments/calibration_sensitivity.py pilot --workers 4
python WelchSatterthwaiteMI/experiments/calibration_sensitivity.py all --workers 4
python WelchSatterthwaiteMI/experiments/report_calibration_sensitivity.py --bootstrap 1000 --workers 3
python WelchSatterthwaiteMI/experiments/redesign_report.py --bootstrap 1000 --workers 3
python WelchSatterthwaiteMI/experiments/redesign_study.py audit
python WelchSatterthwaiteMI/experiments/calibration_sensitivity.py audit
python -m unittest discover -s WelchSatterthwaiteMI/tests -p 'test_*.py'
```

For the full test suite, extract the separately delivered thesis source
archive into `Thesis Writeup/Welch MI/` beside the experiment folders;
manuscript-consistency tests read that source and its generated tables.
The statistical audit can run from the experiment supplement alone.

All statistical imports resolve to the local copied source directories. Fitting and evaluation outputs, chunk checksums, source identities, populations, summaries, bootstrap intervals and independent audit are in `results/approximation_redesign/`. A run refuses incompatible checkpoints. `redesign_report.py --bootstrap 0` reuses the saved calibration bootstrap while regenerating displays. The manifest study name `null` is literal text and must not be interpreted as a missing value by CSV readers.

The extension is isolated under `results/approximation_redesign/calibration_sensitivity/`; its sampler has a separate immutable fingerprint and never modifies the base sampling kernel or records. Its audit reconstructs 96 pairs independently and checks every new chunk. `power.csv` contains all method rates, paired contrasts and changes in gains, with 1,000-repetition joint bootstrap intervals including fitting uncertainty. The lower fitting resample is shared across each focus setting's alternatives. `cross_null_rates.csv` retains conditional Wilson intervals and validity counts; `dependence_diagnostics.csv` records centered-magnitude Spearman correlations and inclusion counts, leaving original signed diagnostics intact. The base reporter reads this new diagnostic before printing the updated appendix table. Reuse saved sensitivity bootstraps with `report_calibration_sensitivity.py --bootstrap 0`.

The copied thesis builds from `Thesis Writeup/Welch MI/Working Draft v3.tex`. Run its copied `package_deliverables.py`, then `--check`. The copied `main.pdf` and historical working drafts remain snapshot artifacts.

## Historical 20,000-pair evidence

The following original project description is retained for provenance. Its counts and two-method comparisons describe the earlier evidence, not the current fresh study.

# Equal-MI Significance Testing

This project studies analytic tests for the independent two-sample weak null

```text
H0: I(P) = I(Q), allowing P != Q.
```

Two methods form the final thesis comparison:

1. **Normal Wald** uses the bias-corrected plug-in MI difference, its
   influence-function standard error, and a standard-normal reference.
2. **Expanded Welch** keeps the same statistic but uses MI-specific
   Satterthwaite degrees of freedom.

Historical exploratory work also considered Simple Welch and constrained
likelihood-ratio tests; neither is part of the current thesis comparison.

## Current Focused Study

The current thesis combines 312 unique settings, 104 population pairs and
6,240,000 sampled table pairs. The 19 October [same-skew extension](results/same_skew_extension/)
adds matched same-skew baselines to all five comparisons, retaining every
original result. Its 72 new settings use the existing parameter grids,
estimators, validity rules and 20,000 repetitions per setting.
`experiments/run_same_skew_extension.py` runs and audits the additions;
`experiments/report_same_skew_extension.py` assembles deduplicated evidence,
compares both skew regimes and reports degrees of freedom across studies.

### Original Focused Study And Supporting Checks

The original [focused study](results/focused_study/) has 232 settings,
68 population pairs and 20,000 paired repetitions per setting. Three studies
vary sample size and population structure, common positive MI, and the true
MI difference. The primary construction is a copying mixture; four matched
settings use a four-cell transfer. Diagnostics and strict validity rules are
reported alongside rejection. Neither statistical method changed.

Run `experiments/run_focused_study.py` with `preflight`, `pilot`, `full`,
`audit` or `timing`. `experiments/audit_focused_study.py` independently checks
raw records, regenerated count inputs, formulas and summaries.
`experiments/report_focused_study.py` generates the new manuscript figures
and tables. The active plan is in
`../Thesis Writeup/Welch MI/notes/FOCUSED_EXPERIMENT_PLAN.md`; the amendment is
`../Thesis Writeup/Welch MI/notes/SAME_SKEW_EXTENSION_PLAN_2026-10-19.md`.

The 10 October supporting [allocation check](results/unequal_sample_check/)
adds four unequal-sample settings and reuses two balanced settings. It keeps
two 4 x 4 different-skew pairs fixed and allocates 2000 observations as
1000/1000, 400/1600 or 1600/400. Combined evidence has 236 unique settings
and 4720000 sampled pairs. `experiments/run_unequal_sample_check.py` runs and
audits the extension; `experiments/report_unequal_sample_check.py` builds its
appendix table. The main study and statistical methods remain unchanged.

The saved-sample mechanism checks in `experiments/report_focused_mechanisms.py`
generate two additional appendix tables without sampling new observations.
They assess the variance-variability formula at six existing null settings
and estimated direction among rejections at four existing alternatives.
The evidence distinguishes population and plug-in predictions and retains
opposite-sign rejections in the original two-sided detection rates.

The supporting [large-table construction check](results/large_table_construction_check/)
adds four 16 x 16 four-cell settings matched to existing copying populations
in margins, MI targets and sample sizes. Before the same-skew extension,
the combined study had 240 unique
settings, 70 population pairs and 4800000 distinct sampled pairs.
`experiments/run_large_table_construction_check.py` runs and audits the new
settings; `experiments/report_large_table_construction_check.py` compares
all eight matched rows with rejection, validity, bias, variance and estimated
direction. The original study, allocation results and methods are unchanged.

## Previous experiment (preserved)

The previous thesis experiment is the preserved
[`thesis_redesign`](results/thesis_redesign/) run. Its
[`protocol`](experiments/THESIS_REDESIGN_PROTOCOL.json) and
[`results`](docs/experiments/THESIS_EXPERIMENTS.md) compare Normal Wald with
Expanded Welch across 3,111 fixed statistical configurations. Each
configuration has 20,000 paired samples; saved rates and validity remain
available individually. The separate
[`thesis_mechanism_check`](results/thesis_mechanism_check/) is a supplementary
diagnostic, not a change to the confirmatory run.

## Reproducibility

Start with the bundled
[`EXPERIMENT_SUPPLEMENT_README.md`](EXPERIMENT_SUPPLEMENT_README.md) for the
software environment, saved evidence, verification commands and full rerun
instructions. The confirmatory run used no minimum-expected-count admission
rule and records invalid calculations separately from rejections.

## Theory

Chapter 4 and Appendix A of the thesis source archive give the Expanded Welch
derivation. The full research repository also retains exploratory notes under
`docs/theory/`; these are not needed to reproduce the final experiment.

## Verification

Run the bundled thesis tests from the directory containing
`WelchSatterthwaiteMI/` and `DifferentialMI/`:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -p 'test_*.py'
.venv/bin/python -m unittest discover -s DifferentialMI/tests -p 'test_*.py'
.venv/bin/python -m unittest discover -s PracticalMIExploration -p 'test_*.py'
.venv/bin/python WelchSatterthwaiteMI/experiments/audit_focused_study.py
.venv/bin/python PracticalMIExploration/run_exploration.py verify-full
```

Regenerate the focused figures and tables without resampling:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python WelchSatterthwaiteMI/experiments/report_focused_study.py \
  --figures /path/to/thesis-source/figures_rewrite
```

The full repository's [`experiments/README.md`](experiments/README.md)
indexes exploratory scripts separately from the final thesis protocol.
