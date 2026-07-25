# Differential Mutual Information

This project evaluates methods for the two-sample hypothesis

```text
H0: I_P(X;Y) = I_Q(X;Y)
```

where the two samples may come from different joint distributions. This is not
the stronger hypothesis `P = Q`.

The project is deliberately separate from the existing MI and sparse-CMI work.
Its first purpose is falsification: determine whether naive group-label
permutation is miscalibrated for equality of MI, and whether influence-function
studentization fixes the problem in a useful range of finite discrete tables.

## Current result

Across 144 independently randomized weak-null scenarios and 432,000 table
pairs, analytic-bias-corrected Wald had mean absolute 5% calibration error
`0.00513`, mean 95% coverage `0.94986`, and `95.8%` of scenarios in the
pre-specified 3.5%-6.5% rejection band. It was slightly better calibrated
than jackknife-Wald.

Read these first:

- [BASELINE_SCOPE.md](BASELINE_SCOPE.md): frozen target, method, and
  exclusions.
- [ROBUST_VALIDATION_REPORT.md](ROBUST_VALIDATION_REPORT.md): result and
  recommendation.
- [REFINEMENT_DECISION.md](REFINEMENT_DECISION.md): why Edgeworth and the
  tested empirical saddlepoint were not retained.
- [ADVERSARIAL_AUDIT.md](ADVERSARIAL_AUDIT.md): formula, software, JIDT, and
  scope audit.
- [results/adult_case_study/REPORT.md](results/adult_case_study/REPORT.md):
  pre-specified real-data example.
- [docs/REGULAR_CASE_DERIVATION.md](docs/REGULAR_CASE_DERIVATION.md): formal
  derivation and assumptions.
- [docs/NOVELTY_AUDIT.md](docs/NOVELTY_AUDIT.md): prior art and honest claim
  boundary.
- [ROBUST_VALIDATION_PROTOCOL.md](ROBUST_VALIDATION_PROTOCOL.md):
  pre-specified randomized protocol.

## Methods compared

- `naive_perm_plugin`: group-label permutation of the raw plug-in MI
  difference.
- `student_perm_plugin`: the same permutation, but with an
  influence-function studentized statistic.
- `student_perm_analytic`: studentized permutation with the classical
  first-order MI bias correction.
- `student_perm_jackknife`: studentized permutation with a jackknife
  bias-corrected MI difference.
- `wald_plugin`: deterministic normal approximation using the estimated
  influence-function variance.
- `wald_analytic`: deterministic normal approximation with the classical
  `(r-1)(c-1)/(2n)` bias removed from each MI estimate. This is the current
  primary baseline.
- `wald_jackknife`: deterministic normal approximation with the jackknife
  bias-corrected MI difference.

Permutation tables are sampled from the multivariate hypergeometric
distribution conditional on pooled cell counts. This is exactly the table-level
equivalent of permuting group labels on individual observations.

## Quick start

From the repository root:

```bash
.venv/bin/python -m unittest discover -s DifferentialMI/tests -v
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python DifferentialMI/experiments/run_randomized_validation.py \
  --mode smoke --output-dir DifferentialMI/results/randomized_smoke
```

Run the professor-facing verification:

```bash
.venv/bin/python DifferentialMI/experiments/run_professor_demo.py
```

The original controlled pilot remains available:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python DifferentialMI/experiments/run_validation.py \
  --profile smoke --output-dir DifferentialMI/results/smoke
```

The `screen` profile is the broad, inexpensive adversarial pass. The `decisive`
profile uses more replicates and permutations on the pre-specified core grid.

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache \
  .venv/bin/python DifferentialMI/experiments/run_validation.py \
  --profile screen --output-dir DifferentialMI/results/screen

MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache \
  .venv/bin/python DifferentialMI/experiments/run_validation.py \
  --profile decisive --output-dir DifferentialMI/results/decisive
```

## Interpretation boundary

The first-order influence-function methods are expected to work only when MI is
away from zero and the table is sufficiently supported. Independence is a
degenerate point: the first-order variance is zero in the population. Near-zero
MI is explicitly deferred from the current regular-case project.

Studentized permutation has an additional boundary: the pooled mixture must
also have positive influence variance. Opposite dependence directions can
make the pooled mixture nearly independent even when both original
populations are regular. The deterministic two-sample Wald statistic does not
use this mixture reference.
