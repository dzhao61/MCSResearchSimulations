# Randomized Regular-Case Validation

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Deterministic Screen

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 | mean_coverage_95 | within_coverage_935_965 | mean_absolute_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wald_plugin | 72 | 0.0701 | 0.0065 | 0.5972 | 0.0410 | 0.9670 | 0.8822 | 0.5972 | 0.0077 |
| wald_analytic | 72 | 0.0049 | 0.0043 | 0.9722 | 0.0410 | 0.0707 | 0.9500 | 0.9722 | 0.0005 |
| wald_jackknife | 72 | 0.0059 | 0.0048 | 0.9167 | 0.0400 | 0.0803 | 0.9489 | 0.9167 | 0.0004 |

Mean vectorized deterministic runtime: 3.65 microseconds per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
