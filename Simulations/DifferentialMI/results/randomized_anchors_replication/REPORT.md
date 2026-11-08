# Randomized Regular-Case Validation

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Pre-Selected Permutation Anchors

| method | anchors | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 |
| --- | --- | --- | --- | --- | --- | --- |
| naive_perm_plugin | 12 | 0.1099 | 0.0225 | 0.4167 | 0.0520 | 0.9720 |
| student_perm_plugin | 12 | 0.0582 | 0.0080 | 0.7500 | 0.0300 | 0.6600 |
| student_perm_analytic | 12 | 0.0559 | 0.0050 | 0.8333 | 0.0340 | 0.6600 |
| student_perm_jackknife | 12 | 0.0559 | 0.0060 | 0.9167 | 0.0410 | 0.6600 |
| wald_plugin | 12 | 0.1008 | 0.0125 | 0.5833 | 0.0380 | 0.6220 |
| wald_analytic | 12 | 0.0047 | 0.0035 | 1.0000 | 0.0380 | 0.0600 |
| wald_jackknife | 12 | 0.0072 | 0.0060 | 0.9167 | 0.0380 | 0.0680 |

Mean full permutation runtime: 7.777 ms per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
