# Randomized Regular-Case Validation

Run mode: `strong`.

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Deterministic Screen

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 | mean_coverage_95 | within_coverage_935_965 | mean_absolute_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wald_plugin | 72 | 0.0711 | 0.0083 | 0.5972 | 0.0403 | 0.9660 | 0.8815 | 0.5972 | 0.0077 |
| wald_analytic | 72 | 0.0050 | 0.0040 | 0.9722 | 0.0383 | 0.0673 | 0.9503 | 0.9722 | 0.0004 |
| wald_jackknife | 72 | 0.0059 | 0.0040 | 0.9306 | 0.0373 | 0.0777 | 0.9492 | 0.9306 | 0.0004 |

Mean vectorized deterministic runtime: 3.57 microseconds per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
