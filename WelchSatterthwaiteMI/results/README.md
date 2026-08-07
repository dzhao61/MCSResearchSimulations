# Results

## Primary Evidence

[`supervisor_full/`](supervisor_full/) contains the current unified experiment
and is the result set to use when presenting the method. Start with its
[`REPORT.md`](supervisor_full/REPORT.md).

## Mechanism Evidence

[`scaled_chi_square_validation/`](scaled_chi_square_validation/) directly
tests the scaled chi-squared approximation for the MI variance estimator on
2.56 million independently generated tables. Start with its
[`REPORT.md`](scaled_chi_square_validation/REPORT.md). The retained
`replication_stability.csv` repeats the focused comparison under three
independent simulation seeds.

## Historical Evidence

- [`decisive/`](decisive/) contains the earlier frozen validation experiment.
- [`adversarial_holdout/`](adversarial_holdout/) contains the independent
  holdout and variance-component checks.
- [`variance_bias_audit/`](variance_bias_audit/) contains the variance-bias
  audit that motivated the expanded method.
- [`smoke/`](smoke/) contains the small pipeline validation for the earlier
  experiment runner.
- [`../archive/custom_welch/results/`](../archive/custom_welch/results/)
  contains the discontinued routing experiment.

Historical outputs are retained because they document the development and
adversarial checking of the method. Generated `supervisor_smoke/` output is
not retained; it can be recreated with the smoke command in the project
README.
