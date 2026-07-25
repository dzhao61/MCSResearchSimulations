# Randomized Regular-Case Validation

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Deterministic Screen

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 | mean_coverage_95 | within_coverage_935_965 | mean_absolute_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wald_plugin | 72 | 0.0722 | 0.0083 | 0.6250 | 0.0377 | 0.9583 | 0.8809 | 0.6250 | 0.0076 |
| wald_analytic | 72 | 0.0054 | 0.0042 | 0.9444 | 0.0377 | 0.0733 | 0.9498 | 0.9444 | 0.0006 |
| wald_jackknife | 72 | 0.0063 | 0.0050 | 0.9028 | 0.0377 | 0.0803 | 0.9486 | 0.9028 | 0.0004 |

Mean vectorized deterministic runtime: 3.63 microseconds per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
