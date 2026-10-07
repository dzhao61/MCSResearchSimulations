# Welch-MI Focused Experiment Supplement

This supplement reproduces the focused study in the current Master of
Computer Science thesis: 232 settings, 68 population pairs and 20,000 paired
samples per setting. It contains the unchanged Normal Wald and Expanded
Welch implementations, all population definitions, per-repetition scalar
records, summaries, figure-generation scripts and independent audits.
The earlier broad-study archive is not part of this supplement.

## Environment

The recorded environment is Python 3.13.5, NumPy 2.4.4, SciPy 1.17.1,
pandas 3.0.3 and Matplotlib 3.10.9. From the extracted archive root:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r WelchSatterthwaiteMI/requirements-thesis.txt
```

The timing check used macOS 26.6.2 on arm64. Timing remains machine-dependent;
the statistical samples are determined by the recorded random streams.
Set `MPLCONFIGDIR` to a writable directory in restricted environments.

## Inspect and verify the results

`WelchSatterthwaiteMI/results/focused_study/` contains the population arrays
and definitions, configuration and display manifests, method and paired
results, diagnostics, timing measurements and verification records.
`records/` contains all 4,640,000 scalar record pairs in compressed NPZ chunks
with checksums. Invalid test outputs are retained. Pilot records are excluded
because they do not contribute to the reported results.

Run the bundled tests and independent audit from the extracted archive root:

```bash
.venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -p 'test_*.py'
.venv/bin/python -m unittest discover -s DifferentialMI/tests -p 'test_*.py'
.venv/bin/python WelchSatterthwaiteMI/experiments/audit_focused_study.py
```

The independent audit validates raw checksums and counts, regenerates sampled
inputs, and recomputes statistics, degrees of freedom, p-values, validity,
rejection rates, intervals and estimation diagnostics. The two older helper
modules are included because the focused code imports their four-cell
constructor and interval functions; they are not instructions to run the old
experiment.

## Reconstruct or rerun

Use a separate output directory for a new run. Reusing saved checkpoints
requires the recorded source fingerprint and software environment to match.

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_study.py preflight --output reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_study.py pilot --output reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_study.py full --output reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_study.py audit --output reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_study.py timing --output reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/audit_focused_study.py --results reproduction
```

The master seed is 20261006. Configuration-specific, independent P and Q
streams use fixed chunks of 1,000 repetitions. Changing `--workers` or
`--batch-size` does not change the statistical outputs. Interrupted runs
resume only checksum-verified chunks. The pilot uses separate streams and
does not enter the full results.

## Rebuild the figures

The separately supplied thesis source already contains the figure PDFs and
tables needed to compile it. To regenerate them from this supplement, give
the extracted source directory explicitly:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/report_focused_study.py --figures /path/to/thesis-source/figures_rewrite
```

This generates five lead figures, three companions and five table fragments
at the manuscript's intended printed dimensions. Complete scientific
construction, parameter grids, validity and uncertainty rules are also in
Appendix B of the thesis; a reader does not need this codebase to understand
or independently recreate the study.
