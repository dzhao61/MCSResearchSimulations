# Sparse CMI Validation Project

This project tests, rather than assumes, the proposal in
`README_sparse_cmi_thesis_handoff.md`.

The current measured recommendation is in
`docs/INITIAL_GO_NO_GO_ASSESSMENT.md`. JIDT's conditional-MI baseline caveat is
documented separately in `docs/JIDT_CMI_BASELINE_AUDIT.md`. The current novelty
risk is summarized in `docs/PRELIMINARY_LITERATURE_MAP.md`.

For binary `X` and `Y`, conditional on each stratum's observed margins,
the only free cell count is hypergeometric. The package computes the exact
finite-sample distribution and cumulants of each stratum's likelihood-ratio
contribution, then tests whether normal and skewness-corrected approximations
are accurate for the sum across many sparse strata.

## Current scope

- Exact conditional stratum distributions and cumulants
- Exact convolution when the combined support is manageable
- Exact-moment normal, Cornish-Fisher, and Edgeworth approximations
- Conditional Monte Carlo and literal within-stratum label permutation
- Observable reliability diagnostics
- Reproducible falsification grids and go/no-go summaries

JIDT integration and transfer entropy are intentionally deferred until the
statistical method passes the first-stage falsification experiment.

## Run

From the repository root:

```bash
PYTHONPATH="Sparse CMI/src" .venv/bin/python -m unittest discover \
  -s "Sparse CMI/tests" -v
```

Run the quick validation screen:

```bash
PYTHONPATH="Sparse CMI/src" .venv/bin/python \
  "Sparse CMI/experiments/01_first_stage_falsification.py" \
  --profile smoke --seed 5030
```

Run the larger first-stage grid:

```bash
PYTHONPATH="Sparse CMI/src" .venv/bin/python \
  "Sparse CMI/experiments/01_first_stage_falsification.py" \
  --profile full --null-samples 100000 --permutations 1000 --seed 5030
```

Run the unconditional repeated-sampling screen, which regenerates margins on
every null dataset:

```bash
PYTHONPATH="Sparse CMI/src" .venv/bin/python \
  "Sparse CMI/experiments/02_unconditional_calibration.py" \
  --profile smoke --replicates 5000 --anchor-replicates 100 \
  --anchor-samples 1000 --seed 5030
```

Results are written below `Sparse CMI/results/`. The experiment records its
configuration, package versions, per-configuration metrics, and a Markdown
go/no-go summary.

## Interpretation

The Monte Carlo reference samples the same conditional null as within-stratum
permutation:

```text
A_z | n_z, r_z, s_z ~ Hypergeometric(n_z, s_z, r_z).
```

It is used as a scalable reference, not counted as the proposed approximation.
Where feasible, numerical exact convolution is the stronger reference.

The project is promising only if:

1. exact-moment centring and scaling beat chi-square in sparse regimes;
2. skewness correction helps across a broad, predeclared grid;
3. diagnostics identify important failure regimes;
4. moment computation is materially faster than conditional permutation; and
5. later literature review supports a narrow CMI-specific novelty claim.
