# Randomized Regular-Case Validation

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Pre-Selected Permutation Anchors

| method | anchors | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 |
| --- | --- | --- | --- | --- | --- | --- |
| naive_perm_plugin | 12 | 0.0413 | 0.0280 | 0.2500 | 0.0040 | 0.2130 |
| student_perm_plugin | 12 | 0.0100 | 0.0065 | 0.6667 | 0.0240 | 0.0670 |
| student_perm_analytic | 12 | 0.0092 | 0.0090 | 0.9167 | 0.0350 | 0.0670 |
| student_perm_jackknife | 12 | 0.0106 | 0.0135 | 0.8333 | 0.0350 | 0.0670 |
| wald_plugin | 12 | 0.0990 | 0.0135 | 0.6667 | 0.0350 | 0.5920 |
| wald_analytic | 12 | 0.0107 | 0.0110 | 0.9167 | 0.0330 | 0.0640 |
| wald_jackknife | 12 | 0.0126 | 0.0120 | 0.6667 | 0.0330 | 0.0730 |

Mean full permutation runtime: 7.774 ms per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
