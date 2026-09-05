# Equal-MI Significance Testing

This project studies analytic tests for the independent two-sample weak null

```text
H0: I(P) = I(Q), allowing P != Q.
```

Three methods form the final confirmatory comparison:

1. **Normal Wald** uses the bias-corrected plug-in MI difference, its
   influence-function standard error, and a standard-normal reference.
2. **Expanded Welch** keeps the same statistic but uses MI-specific
   Satterthwaite degrees of freedom.
3. **Simple Welch** keeps the Wald statistic but uses the ordinary
   Welch-Satterthwaite degrees of freedom.

## Current status

The final thesis experiment is the frozen detection-and-breakdown sweep in
[`NEXT_EXPERIMENT_PLAN.md`](NEXT_EXPERIMENT_PLAN.md). It compares Normal Wald,
Simple Welch, and Expanded Welch across exact table shapes, margins, sample
sizes, effects, and robustness cases without averaging away individual
configurations. Constrained LR and earlier screens remain exploratory evidence,
not part of this confirmatory comparison.

## Next planned work

[`NEXT_EXPERIMENT_PLAN.md`](NEXT_EXPERIMENT_PLAN.md) specifies the experiment,
and [`experiments/FINAL_PROTOCOL.json`](experiments/FINAL_PROTOCOL.json)
provides its machine-readable protocol. The protocol measures false-positive
rates, power, numerical validity, and breakdown with no expected-count floor.

## Theory

- [`docs/theory/CONSTRAINED_LIKELIHOOD_RATIO_DERIVATION.md`](docs/theory/CONSTRAINED_LIKELIHOOD_RATIO_DERIVATION.md)
  derives the current LR method.
- [`docs/theory/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`](docs/theory/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md)
  derives the Expanded Welch baseline.
- [`docs/theory/INDEPENDENCE_REFERENCE_DISTRIBUTION.md`](docs/theory/INDEPENDENCE_REFERENCE_DISTRIBUTION.md)
  explains why the first-order Expanded Welch construction does not become an
  independence test by introducing a reference distribution.

## Verification

Run the complete automated suite from the repository root:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -v
```

Run a small end-to-end LR experiment with:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python WelchSatterthwaiteMI/experiments/run_multialphabet_lr_experiment.py \
  --profile smoke --shape-limit 1 --workers 1 \
  --output-dir /tmp/multialphabet_lr_smoke
```

Run the frozen sweep's smoke profile with:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python WelchSatterthwaiteMI/experiments/run_detection_breakdown_sweep.py \
  --profile smoke --workers 4 --output-dir /tmp/detection_breakdown_smoke
```

See [`experiments/README.md`](experiments/README.md) and
[`results/README.md`](results/README.md) for executable and generated artefact
indexes.
