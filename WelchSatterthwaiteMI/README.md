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

Simple Welch appears only in supplementary checks; constrained
likelihood-ratio methods remained exploratory.

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

## Previous experiment (preserved)

The final thesis experiment is the frozen
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
  .venv/bin/python -m unittest \
  WelchSatterthwaiteMI.tests.test_thesis_redesign \
  WelchSatterthwaiteMI.tests.test_thesis_derivation_audit \
  WelchSatterthwaiteMI.tests.test_thesis_mechanism_check \
  WelchSatterthwaiteMI.tests.test_welch
```

Regenerate the saved-run report and atlas without resampling:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python WelchSatterthwaiteMI/experiments/run_thesis_redesign.py \
  --report-only --output-dir WelchSatterthwaiteMI/results/thesis_redesign
```

The full repository's [`experiments/README.md`](experiments/README.md)
indexes exploratory scripts separately from the final thesis protocol.
