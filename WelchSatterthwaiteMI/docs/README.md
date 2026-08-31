# Documentation

This directory separates the current research narrative, mathematical theory,
experimental records, and historical material.

## Overview

[`overview/SUMMARY.md`](overview/SUMMARY.md) presents the complete research
story from first principles, including the literature, methods, experiment
design, results, and limitations.

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

- [`experiments/2X2_EXPERIMENT.md`](experiments/2X2_EXPERIMENT.md) documents
  the interpretable 2x2 design and its calibration, validity, power, and
  breakdown results.
- [`experiments/2X2_CRITICAL_VALUE_AUDIT.md`](experiments/2X2_CRITICAL_VALUE_AUDIT.md)
  diagnoses the finite-sample distortion of the studentized statistic.
- [`experiments/2X2_JOINT_CORNISH_FISHER_AUDIT.md`](experiments/2X2_JOINT_CORNISH_FISHER_AUDIT.md)
  records the confirmatory no-go result for a joint higher-order correction.
- [`experiments/2X2_CONSTRAINED_LIKELIHOOD_RATIO_AUDIT.md`](experiments/2X2_CONSTRAINED_LIKELIHOOD_RATIO_AUDIT.md)
  records the constrained likelihood-ratio calibration and full-range power
  audit, including the regimes where its advantage does and does not persist.
- [`experiments/MULTIALPHABET_CONSTRAINED_LR_EXPERIMENT.md`](experiments/MULTIALPHABET_CONSTRAINED_LR_EXPERIMENT.md)
  extends that audit to exact 3x3, 4x4, 5x5, and 8x8 configurations across a
  detailed sample-size and marginal-skewness grid.
- [`../experiments/README.md`](../experiments/README.md) indexes executable
  experiment scripts and earlier studies.

Generated reports remain beside their CSV and figure artefacts under
[`../results/`](../results/).

## History

The [`history/`](history/) directory contains the earlier validation protocol,
final assessment, and literature audit. The separate [`../archive/`](../archive/)
directory preserves superseded derivations and discontinued methods together
with their supporting files.
