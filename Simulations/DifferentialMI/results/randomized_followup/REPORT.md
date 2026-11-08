# Randomized Regular-Case Validation

Run mode: `followup`.

Near-independence was excluded by design. Every population MI target was
at least 0.03 nats, and each weak-null pair had equal population MI.

## Deterministic Screen

| method | scenarios | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 | mean_coverage_95 | within_coverage_935_965 | mean_absolute_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wald_plugin | 6 | 0.0548 | 0.0418 | 0.1667 | 0.0625 | 0.2026 | 0.8952 | 0.1667 | 0.0192 |
| wald_analytic | 6 | 0.0119 | 0.0105 | 0.8333 | 0.0584 | 0.0689 | 0.9381 | 0.8333 | 0.0008 |
| wald_jackknife | 6 | 0.0199 | 0.0183 | 0.1667 | 0.0635 | 0.0813 | 0.9301 | 0.1667 | 0.0007 |

Mean vectorized deterministic runtime: 1.51 microseconds per table pair.

## Pre-Selected Permutation Anchors

| method | anchors | mean_absolute_fpr_error_05 | median_absolute_fpr_error_05 | within_035_065 | minimum_fpr_05 | maximum_fpr_05 |
| --- | --- | --- | --- | --- | --- | --- |
| naive_perm_plugin | 6 | 0.0379 | 0.0173 | 0.5000 | 0.0537 | 0.2070 |
| student_perm_plugin | 6 | 0.0048 | 0.0048 | 1.0000 | 0.0500 | 0.0617 |
| student_perm_analytic | 6 | 0.0051 | 0.0053 | 1.0000 | 0.0487 | 0.0603 |
| student_perm_jackknife | 6 | 0.0097 | 0.0100 | 0.8333 | 0.0473 | 0.0657 |
| wald_plugin | 6 | 0.0563 | 0.0460 | 0.1667 | 0.0637 | 0.2057 |
| wald_analytic | 6 | 0.0129 | 0.0112 | 0.6667 | 0.0603 | 0.0680 |
| wald_jackknife | 6 | 0.0201 | 0.0200 | 0.0000 | 0.0670 | 0.0727 |

Mean full permutation runtime: 2.979 ms per table pair.

## Interpretation

The jackknife should be retained only if it improves materially over the
classical analytic correction. Raw permutation is included to test the
weak-null failure predicted by theory, not as the expected winner.

See the CSV files for scenario-level Wilson intervals, diagnostics, and
the complete saved probability tables.
