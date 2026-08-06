# Results

## Primary Evidence

[`supervisor_full/`](supervisor_full/) contains the current unified experiment
and is the result set to use when presenting the method. Start with its
[`REPORT.md`](supervisor_full/REPORT.md).

## Routing Evidence

[`custom_decision_audit/`](custom_decision_audit/) contains the crossed
development/holdout experiment for selecting between normal Wald and expanded
Welch. Start with the interpretive
[`decision audit`](../docs/CUSTOM_WELCH_DECISION_AUDIT.md), then use the
generated [`REPORT.md`](custom_decision_audit/REPORT.md) and CSV files for the
complete numerical results.

## Historical Evidence

- [`decisive/`](decisive/) contains the earlier frozen validation experiment.
- [`adversarial_holdout/`](adversarial_holdout/) contains the independent
  holdout and variance-component checks.
- [`variance_bias_audit/`](variance_bias_audit/) contains the variance-bias
  audit that motivated the expanded method.
- [`smoke/`](smoke/) contains the small pipeline validation for the earlier
  experiment runner.

Historical outputs are retained because they document the development and
adversarial checking of the method. Generated `supervisor_smoke/` output is
not retained; it can be recreated with the smoke command in the project
README.
