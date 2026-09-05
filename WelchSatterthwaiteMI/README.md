# Equal-MI Significance Testing

This project studies analytic tests for the independent two-sample weak null

```text
H0: I(P) = I(Q), allowing P != Q.
```

Three methods form the current comparison:

1. **Normal Wald** uses the bias-corrected plug-in MI difference, its
   influence-function standard error, and a standard-normal reference.
2. **Expanded Welch** keeps the same statistic but uses MI-specific
   Satterthwaite degrees of freedom.
3. **Constrained likelihood ratio (LR)** directly maximises the two-sample
   multinomial likelihood under `I(P) = I(Q)` and compares the loss of fit with
   the regular asymptotic `chi-squared(1)` reference.

## Current status

The constrained LR is the leading current research direction. In the final
2x2 null experiment, its mean absolute false-positive-rate error at
`alpha = 0.05` was `0.0210`, compared with `0.0329` for Expanded Welch and
`0.0762` for Normal Wald. It was numerically valid for at least 99.9% of
replicates, but remained conservative in several severe rare-cell cases.

A subsequent screen covered 3x3, 4x4, 5x5, and 8x8 tables. LR had the lowest
aggregate calibration error, often reduced severe liberal Wald behaviour, and
usually had similar power once `N >= 250`. It did not dominate every exact
configuration. The 8x8 estimates use only 250 replicates per configuration and
remain preliminary screening evidence.

A focused 2,000-replicate confirmation then reran six prespecified cases. LR
was close to the nominal 0.05 rate in the ordinary control and three cases in
which Wald was liberal, but was strongly conservative in two ultra-skewed
cases. This confirms both the useful regime and the principal failure mode.

Expanded Welch remains an important baseline and mechanism study, not the
primary current candidate. Its finite-degrees-of-freedom correction improved
some difficult null configurations but was often conservative and could be
undefined in highly sparse tables.

The current evidence is reported directly in the
[`2x2 LR validation`](docs/experiments/CONSTRAINED_LR_2X2_VALIDATION.md) and
[`multi-alphabet LR validation`](docs/experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md).

## Next planned work

[`NEXT_EXPERIMENT_PLAN.md`](NEXT_EXPERIMENT_PLAN.md) specifies the next
experiment: a detection and breakdown sweep that measures false-positive and
true-positive rates on one surface, removes every artificial lower bound on
sample size and expected cell counts, and extends beyond `2x2` tables. It also
records the current state of uncommitted work and the empirically established
floors of the Expanded Welch method.

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

See [`experiments/README.md`](experiments/README.md) and
[`results/README.md`](results/README.md) for executable and generated artefact
indexes.
