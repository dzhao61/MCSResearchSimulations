# Randomized Regular-Case Validation

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Deterministic Screen

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 | mean_coverage_95 | within_coverage_935_965 | mean_absolute_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wald_plugin | 8 | 0.0181 | 0.0175 | 0.5000 | 0.0350 | 0.0850 | 0.9406 | 0.5000 | 0.0027 |
| wald_analytic | 8 | 0.0175 | 0.0125 | 0.6250 | 0.0350 | 0.0850 | 0.9387 | 0.6250 | 0.0012 |
| wald_jackknife | 8 | 0.0175 | 0.0125 | 0.6250 | 0.0350 | 0.0850 | 0.9387 | 0.6250 | 0.0011 |

Mean vectorized deterministic runtime: 1.87 microseconds per table pair.

## Pre-Selected Permutation Anchors

| method | anchors | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 |
| --- | --- | --- | --- | --- | --- | --- |
| naive_perm_plugin | 2 | 0.1167 | 0.1167 | 0.0000 | 0.0000 | 0.2333 |
| student_perm_plugin | 2 | 0.0333 | 0.0333 | 0.0000 | 0.0000 | 0.0667 |
| student_perm_analytic | 2 | 0.0333 | 0.0333 | 0.0000 | 0.0000 | 0.0667 |
| student_perm_jackknife | 2 | 0.0333 | 0.0333 | 0.0000 | 0.0000 | 0.0667 |
| wald_plugin | 2 | 0.0500 | 0.0500 | 0.0000 | 0.0000 | 0.1000 |
| wald_analytic | 2 | 0.0333 | 0.0333 | 0.0000 | 0.0000 | 0.0667 |
| wald_jackknife | 2 | 0.0333 | 0.0333 | 0.0000 | 0.0000 | 0.0667 |

Mean full permutation runtime: 0.231 ms per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
