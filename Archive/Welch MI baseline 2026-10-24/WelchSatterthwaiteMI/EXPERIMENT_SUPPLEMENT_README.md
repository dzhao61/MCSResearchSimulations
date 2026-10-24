# Welch-MI Focused Experiment Supplement

This supplement reproduces the focused study in the current Master of
Computer Science thesis: 312 settings, 104 population pairs and 20,000 paired
samples per setting. It contains the Normal Wald and Expanded
Welch implementations, all population definitions, per-repetition scalar
records, summaries, figure-generation scripts and independent audits.
The earlier broad-study archive is not part of this supplement.
The 17 October numerical correction enforces the existing zero-component
validity rule with exact count-table checks and centred variance algebra.
The original populations and random streams are unchanged; current records
were regenerated under the corrected source fingerprint.
The original study has 232 settings; the unequal-sample check adds four and
reuses two balanced settings, without changing the original records.
The large-table construction check adds another four settings and two
population pairs, matched to existing copying comparisons.
The 19 October same-skew extension adds 72 matched settings and 34 previously
unused population pairs. It provides a same-skew baseline in every main study
and supporting check without changing or resampling any original setting.
The combined evidence has 6,240,000 distinct sampled table pairs.
The bounded jackknife diagnostic reuses four original copying settings and
80000 table pairs. It changes only the MI bias correction, retaining the
original standard errors and normal distribution cutoff. It adds no
settings, populations or sampled pairs to the study's counts.

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

`WelchSatterthwaiteMI/supplementary_displays/` retains the complete
120-setting equal-MI table as CSV and LaTeX, plus the full-range margin
and same-skew power plots omitted from the shortened Appendix C. Its
README defines the columns and settings. These are existing results;
the manuscript reduction changes no simulations or numerical evidence.

`WelchSatterthwaiteMI/results/focused_study/` contains the population arrays
and definitions, configuration and display manifests, method and paired
results, diagnostics, timing measurements and verification records.
`records/` contains all 4,640,000 scalar record pairs in compressed NPZ chunks
with checksums. Invalid test outputs are retained. Pilot records are excluded
because they do not contribute to the reported results.

`WelchSatterthwaiteMI/results/unequal_sample_check/` contains the six
fixed-total allocation comparisons. Two balanced checkpoints are identical
copies of the main-study records; four unequal allocations add 80,000 new
sampled pairs. Their identity records distinguish imported and newly sampled
results. The combined evidence contains 4,720,000 distinct table pairs,
before the construction extension, not the sum of both directories' counts.

`WelchSatterthwaiteMI/results/large_table_construction_check/` contains four
16 x 16 different-skew first-block transfer settings, using MI pairs
(0.02, 0.02) and (0.02, 0.03), each at n=1000 and 10000. All 80000
sampled pairs are new. Its population definitions, raw chunks, summaries
and independent audit bring the combined evidence to 4800000 distinct pairs.

`WelchSatterthwaiteMI/results/same_skew_extension/` contains only the 72 new
same-skew settings and their 1,440,000 sampled pairs. Its 36 referenced
population pairs include two already used in the original study. The
`combined_*` manifests and summaries select all 312 settings exactly once;
`combined_verification.json` identifies the original directory containing each
setting's raw records. Balanced allocation and zero-difference power results
are reused, not counted as additional samples. The protocol and fingerprints
authenticate the original evidence and new settings separately.

`WelchSatterthwaiteMI/results/focused_jackknife_check/` contains all four
16 x 16 different-skew copying comparisons at MI pairs (0.02,0.02) and
(0.02,0.03), each at n=1000 and 10000. Its protocol, per-repetition outputs,
paired summaries and evidence retain all planned outcomes. The jackknife
replaces the analytic correction; negative corrected estimates are retained.

Run the bundled tests and independent audit from the extracted archive root:

```bash
.venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -p 'test_*.py'
.venv/bin/python -m unittest discover -s DifferentialMI/tests -p 'test_*.py'
.venv/bin/python -m unittest discover -s PracticalMIExploration -p 'test_*.py'
.venv/bin/python WelchSatterthwaiteMI/experiments/audit_focused_study.py
.venv/bin/python WelchSatterthwaiteMI/experiments/run_unequal_sample_check.py audit
.venv/bin/python WelchSatterthwaiteMI/experiments/run_large_table_construction_check.py audit
.venv/bin/python WelchSatterthwaiteMI/experiments/run_same_skew_extension.py audit
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py audit
.venv/bin/python PracticalMIExploration/run_exploration.py verify-full
```

The independent audit validates raw checksums and counts, regenerates sampled
inputs, and recomputes statistics, degrees of freedom, p-values, validity,
rejection rates, intervals and estimation diagnostics. The two older helper
modules are included because the focused code imports their four-cell
constructor and interval functions; they are not instructions to run the old
experiment.
The base audit also compares every configuration, display assignment,
population array and checkpoint identity with the planned design. The base
reporter performs a fresh audit rather than trusting an old success flag.

`PracticalMIExploration/` supplies the protocol, runner, tests, attributed
raw UCI archives and `thesis_application/` evidence for all six full-data
comparisons and their Holm correction. Reproduce only this manuscript
application, without any exploratory subset simulations, using:

```bash
.venv/bin/python PracticalMIExploration/run_exploration.py full --output application-reproduction
.venv/bin/python PracticalMIExploration/run_exploration.py verify-full --output application-reproduction
```

The archived raw files are checked against the hashes in the supplied
application identity. Dataset citations, download URLs and preparation
rules are in `PracticalMIExploration/PROTOCOL.md`. Tests inspecting thesis
text skip when its separately supplied source is absent.

The allocation audit checks its exact scope, copied populations and checkpoint
provenance before applying the same independent formula and raw-record audit.
The construction audit checks its four-setting scope, reconstructs the
positive transfer populations and applies the same raw-record audit. Its
reporter verifies the copying comparison's study identity as well.
The jackknife audit regenerates all 80000 original input pairs, verifies
their saved baseline outputs and reproduces every diagnostic output and
summary. It also compares the vectorized jackknife with an independent
cell-weighted leave-one-out calculation on 16 full-size sampled tables.
Unit tests check the equivalence to deleting every observation in a smaller table.

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

After the base study has been reproduced, run the supporting check in another
directory. It imports the two checksum-verified balanced checkpoints and only
simulates the four new allocations:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_unequal_sample_check.py preflight --base-results reproduction --output allocation-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_unequal_sample_check.py pilot --base-results reproduction --output allocation-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_unequal_sample_check.py full --base-results reproduction --output allocation-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_unequal_sample_check.py audit --output allocation-reproduction
```

The same master seed, fixed chunks and configuration-derived independent
streams apply. Population identities do not change with sample allocation.

To rerun the 72-setting same-skew extension against the bundled, authenticated
original evidence, use a separate output directory. The defaults locate the
three original results directories relative to the project, not the shell's
working directory:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_same_skew_extension.py preflight --output same-skew-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_same_skew_extension.py pilot --output same-skew-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_same_skew_extension.py full --output same-skew-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_same_skew_extension.py audit --output same-skew-reproduction
```

The extension reconstructs the complete matched design, checks that all 240
original settings are unchanged, and samples only the missing settings. Its
independent audit verifies every new raw chunk and summary, regenerates 17
sampled input pairs per setting and checks the original study and supporting
evidence before assembling deduplicated summaries.

The large-table construction check uses a separate output directory and
independent configuration-derived streams. It samples only its four new
settings; the reporter reads the four copying comparisons from the base run:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_large_table_construction_check.py preflight --base-results reproduction --output construction-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_large_table_construction_check.py pilot --base-results reproduction --output construction-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_large_table_construction_check.py full --base-results reproduction --output construction-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_large_table_construction_check.py audit --output construction-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/report_large_table_construction_check.py --base-results reproduction --results construction-reproduction --figures /path/to/thesis-source/figures_rewrite
```

The jackknife check regenerates the original count tables from their saved
streams and verifies them against the base records. After reproducing the
base study, use another directory for its results:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py preflight --input reproduction --output jackknife-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py run --input reproduction --output jackknife-reproduction
.venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py audit --input reproduction --output jackknife-reproduction
```

Keep the recorded scientific source files and environment for exact
reproduction. The compact reporter checks provenance against the bundled
base-study records; use its defaults for the delivered evidence.

## Rebuild the figures

The separately supplied thesis source already contains the figure PDFs and
tables needed to compile it. To regenerate them from this supplement, give
the extracted source directory explicitly:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/report_focused_study.py --figures /path/to/thesis-source/figures_rewrite
.venv/bin/python WelchSatterthwaiteMI/experiments/report_unequal_sample_check.py --figures /path/to/thesis-source/figures_rewrite
.venv/bin/python WelchSatterthwaiteMI/experiments/report_focused_mechanisms.py --figures /path/to/thesis-source/figures_rewrite
.venv/bin/python WelchSatterthwaiteMI/experiments/report_large_table_construction_check.py --figures /path/to/thesis-source/figures_rewrite
.venv/bin/python WelchSatterthwaiteMI/experiments/report_focused_jackknife_check.py --figures /path/to/thesis-source/figures_rewrite
.venv/bin/python WelchSatterthwaiteMI/experiments/report_same_skew_extension.py --figures /path/to/thesis-source/figures_rewrite
```

These scripts generate the original figures and tables, the matched-skew
population-MI figure, same-skew power companions and supporting tables at
the manuscript's intended printed dimensions. The new reporter also stores
all 312 settings' rates, diagnostics and alternative rejection directions in
`focused_same_skew_evidence.json`, selecting each setting from its recorded
origin. Complete scientific
construction, parameter grids, validity and uncertainty rules are also in
Appendix B of the thesis; a reader does not need this codebase to understand
or independently recreate the study.

The mechanism reporter checks all base records through the independent audit,
then reads six existing null settings for variance-estimate stability and
four existing alternatives for direction among rejections. It recomputes
population sensitivities independently and checks rejection counts against
the audited summaries. `focused_mechanism_evidence.json` stores the values
underlying its two tables. Its precision check uses 1,000 deterministic
bootstrap resamples of paired saved variance/sensitivity outputs, retaining
their association within each population. These are not new multinomial
samples, and do not alter the experiment's settings or its sample count.

The jackknife evidence also quantifies Monte Carlo precision with 1000
deterministic resamples of paired saved outputs. These are precision checks
on the simulation summaries, not bootstrap MI tests or new sampled data.
Appendix C.3 reports its estimator, exact settings and mixed findings within
the standalone manuscript.
