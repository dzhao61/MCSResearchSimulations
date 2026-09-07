# Documentation

This directory separates the current research narrative, mathematical theory,
experimental records, and historical material.

## Theory

- [`theory/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`](theory/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md)
  gives the main line-by-line derivation of the expanded method.
- [`theory/CONSTRAINED_LIKELIHOOD_RATIO_DERIVATION.md`](theory/CONSTRAINED_LIKELIHOOD_RATIO_DERIVATION.md)
  derives the equal-MI constrained likelihood-ratio statistic, its numerical
  fit, and its one-degree-of-freedom reference distribution.
- [`theory/INDEPENDENCE_REFERENCE_DISTRIBUTION.md`](theory/INDEPENDENCE_REFERENCE_DISTRIBUTION.md)
  explains why comparison with an independent reference does not turn the
  method into a regular independence test.
- [`theory/MI_TAYLOR_EXPANSION.md`](theory/MI_TAYLOR_EXPANSION.md) derives the
  second-order expansion of MI at independence.
- [`../derivation/main.pdf`](../derivation/main.pdf) is the formatted derivation;
  [`../derivation/main.tex`](../derivation/main.tex) is its LaTeX source.

## Experiments

- [Thesis Experiment Redesign](experiments/THESIS_EXPERIMENT_PLAN.md)
  is the current implementation plan: explicit populations, matched MI differences,
  calibration and power, stress tests, and standardized reporting. Not yet run.
- [Population Construction Check](experiments/CONSTRUCTION_CHECK.md)
  retains the separate exploratory evidence motivating the redesign.
- [Archived Experimental Results](experiments/archive/EXPERIMENTAL_RESULTS.md)
  preserves the previous landscape and follow-up with their original data.
- [`experiments/EQUAL_MI_2X2_BASELINE.md`](experiments/EQUAL_MI_2X2_BASELINE.md)
  establishes the 2x2 Normal Wald and Expanded Welch baselines.
- [`experiments/CONSTRAINED_LR_2X2_VALIDATION.md`](experiments/CONSTRAINED_LR_2X2_VALIDATION.md)
  evaluates constrained LR calibration, power, runtime, and failure regimes
  for 2x2 tables.
- [`experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md`](experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md)
  extends the comparison to 3x3, 4x4, 5x5, and 8x8 tables.
- [`../experiments/README.md`](../experiments/README.md) indexes executable
  experiment scripts and earlier studies.

Superseded calibration investigations are retained under
[`experiments/archive/`](experiments/archive/).

Generated reports remain beside their CSV and figure artefacts under
[`../results/`](../results/).

## History

The [`history/`](history/) directory contains the earlier validation protocol,
final assessment, and literature audit. The separate [`../archive/`](../archive/)
directory preserves superseded derivations and discontinued methods together
with their supporting files.
