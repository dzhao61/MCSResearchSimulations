# Welch-MI Experiment Supplement

This archive contains the frozen confirmatory protocol, implementation,
consolidated results, individual-regime atlas and tests used by the thesis.
It also contains the separately labelled supplementary mechanism check under
`results/thesis_mechanism_check/`; that check does not modify the frozen run.
The 3,111 individual checkpoint files are included alongside the consolidated
tables so each configuration can be inspected directly.

## Environment

The retained run used Python 3.13.5 on macOS, with the exact numerical package
versions in `WelchSatterthwaiteMI/requirements-thesis.txt`. From the directory
containing `WelchSatterthwaiteMI/` and `DifferentialMI/`, create an environment:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r WelchSatterthwaiteMI/requirements-thesis.txt
```

The code supports Python 3.10 or later, but the pinned versions reproduce the
recorded software environment most closely.

## Inspect and verify the saved run

The principal human-readable result is
`WelchSatterthwaiteMI/docs/experiments/THESIS_EXPERIMENTS.md`. The frozen
protocol and consolidated tables are under `experiments/` and
`results/thesis_redesign/` respectively.

Run the mathematical and protocol tests from this archive root with:

```bash
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  .venv/bin/python -m unittest \
  WelchSatterthwaiteMI.tests.test_thesis_redesign \
  WelchSatterthwaiteMI.tests.test_thesis_derivation_audit \
  WelchSatterthwaiteMI.tests.test_thesis_mechanism_check \
  WelchSatterthwaiteMI.tests.test_welch
```

To regenerate the complete atlas and verification records from the saved
tables without resampling:

```bash
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  .venv/bin/python WelchSatterthwaiteMI/experiments/run_thesis_redesign.py \
  --report-only \
  --output-dir WelchSatterthwaiteMI/results/thesis_redesign
```

## Reconstruct or rerun the protocol

The preflight mode reconstructs all populations and configuration manifests
without simulation:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_thesis_redesign.py \
  --preflight-only --output-dir WelchSatterthwaiteMI/results/reproduction_preflight
```

The complete run requests 62,220,000 paired count tables and can be reproduced
with:

```bash
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  .venv/bin/python WelchSatterthwaiteMI/experiments/run_thesis_redesign.py \
  --full --workers 4 --output-dir WelchSatterthwaiteMI/results/reproduction
```

Stable configuration-specific seeds make the statistical outputs independent
of worker completion order. Runtime measurements remain machine-dependent.

To regenerate the mechanism-check report from its saved CSV files, run:

```bash
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  .venv/bin/python WelchSatterthwaiteMI/experiments/report_thesis_mechanism_check.py
```

The full follow-up simulation can be reproduced with
`run_thesis_mechanism_check.py`; it evaluates 809 configurations and uses an
independent pilot for each of 169 nulls.

The saved `run_metadata.json` records the exact source hashes used for the
confirmatory run. The protocol, simulation core, test implementation, and
imported statistical dependencies still match those hashes. The bundled
orchestration runner has since gained atlas-count metadata, hashes for saved
outputs on future runs, and one-pass handling of a failed preflight. Its
population construction, simulation, and method-evaluation path are unchanged.
The recorded runner SHA-256 is
`42c0ef36f46c88e7828a628ee68fbeb18dbde5d978291d849dc4847c2b857908`;
the supplied runner SHA-256 is
`0fd0247da05e5bea92e4f56c9956b0671ae93244a4e433c421ccf53aac8095bf`.
The historical metadata are intentionally not rewritten. Their figure count
of 99 refers to primary atlas figures; the later report and preflight records
add seven companion calibration zooms, giving 106 files in total. The original
metadata predate per-output hashes, so `SHA256SUMS.txt` authenticates the
delivered archives and the verification scripts check their internal evidence.

## Use with the thesis source archive

Extract the thesis source and this supplement into the same directory. The
thesis can then regenerate its 22 selected figures and verify every reported
Chapter 6 value with:

```bash
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  .venv/bin/python figures_rewrite/make_figures.py
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  .venv/bin/python figures_rewrite/audit_evidence.py
```

If the two trees are stored separately, set `WELCH_MI_WORKSPACE_ROOT` to the
directory containing `WelchSatterthwaiteMI/` before running either script.
