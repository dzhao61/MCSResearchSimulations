# Sparse CMI Validation Project

This project tests, rather than assumes, the proposal in
`README_sparse_cmi_thesis_handoff.md`.

The current measured recommendation is in
`docs/SADDLEPOINT_ROUTER_VALIDATION_REPORT.md`. JIDT's conditional-MI baseline
caveats are documented separately in `docs/JIDT_CMI_BASELINE_AUDIT.md`. The
current novelty risk and safe claim boundary are documented in
`docs/NOVELTY_AUDIT_AND_CLAIM_BOUNDARY.md`.

For binary `X` and `Y`, conditional on each stratum's observed margins,
the only free cell count is hypergeometric. The package computes the exact
finite-sample distribution and cumulants of each stratum's likelihood-ratio
contribution, then tests whether normal and skewness-corrected approximations
are accurate for the sum across many sparse strata.

## Current scope

- Exact conditional stratum distributions and cumulants
- Exact convolution when the combined support is manageable
- A bounded-work exact-convolution/saddlepoint router
- Factorized-CGF Lugannani-Rice upper-tail approximation
- Exact-moment normal, Cornish-Fisher, and Edgeworth approximations
- Conditional Monte Carlo and literal within-stratum label permutation
- Observable reliability diagnostics
- Reproducible falsification grids and go/no-go summaries

The JIDT comparison bridge is implemented. Production integration into JIDT,
larger `X/Y` alphabets, and transfer entropy remain deferred.

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

Run the held-out deterministic saddlepoint/router benchmark:

```bash
PYTHONPATH="Sparse CMI/src" .venv/bin/python \
  "Sparse CMI/experiments/03_saddlepoint_validation.py" \
  --profile smoke --null-samples 20000 --permutations 1000 --seed 5030
```

Run direct JIDT anchors using correct within-stratum orderings:

```bash
PYTHONPATH="Sparse CMI/src" .venv/bin/python \
  "Sparse CMI/experiments/04_jidt_blockwise_anchors.py" \
  --permutations 1000 --reference-samples 200000 --seed 5030
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

The current result is promising because:

1. the routed test beats chi-square in sparse regimes without degrading the
   balanced adequate-count controls;
2. coarse finite supports are routed to bounded numerical exact convolution;
3. saddlepoint-only confirmation cases remain well calibrated;
4. direct JIDT blockwise anchors confirm units, p-values, and speed; and
5. the literature audit identifies a narrow CMI-specific claim rather than
   claiming invention of conditional saddlepoint inference.
