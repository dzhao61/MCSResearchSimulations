# Results

## Final Confirmatory Evidence

[`detection_breakdown_sweep/`](detection_breakdown_sweep/) is reserved for the
frozen final experiment comparing Normal Wald, Simple Welch, and Expanded
Welch. Its `REPORT.md` is generated only by the full protocol run; smoke output
is written outside this directory and discarded.

## Exploratory LR Evidence

- [`2x2_constrained_lr_confirmatory_fullstarts/`](2x2_constrained_lr_confirmatory_fullstarts/)
  is the final 2x2 null-calibration run.
- [`2x2_constrained_lr_power_fullstarts/`](2x2_constrained_lr_power_fullstarts/)
  is the final two-effect 2x2 power run.
- [`2x2_constrained_lr_full_curves/`](2x2_constrained_lr_full_curves/)
  contains the complete feasible-range 2x2 power curves.
- [`multialphabet_lr_screen/`](multialphabet_lr_screen/) contains the 3x3 to
  8x8 calibration and fixed-effect screen.
- [`multialphabet_lr_power_curves/`](multialphabet_lr_power_curves/) contains
  the corresponding multi-alphabet power curves.
- [`multialphabet_lr_confirmatory/`](multialphabet_lr_confirmatory/) contains
  the focused 2,000-replicate confirmation of six prespecified screening
  cases.

## Expanded Welch Evidence

[`supervisor_practical/`](supervisor_practical/) contains the earlier unified
Expanded Welch experiment. Start with its
[`REPORT.md`](supervisor_practical/REPORT.md) and
[`rejection_calibration.png`](supervisor_practical/rejection_calibration.png).

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
