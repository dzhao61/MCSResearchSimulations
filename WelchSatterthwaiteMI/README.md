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

## Current focused study (6 October 2026)

The thesis now uses the [focused study](results/focused_study/): 232 settings,
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
`../Thesis Writeup/Welch MI/FOCUSED_EXPERIMENT_PLAN.md`.

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
in margins, MI targets and sample sizes. The combined study has 240 unique
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
