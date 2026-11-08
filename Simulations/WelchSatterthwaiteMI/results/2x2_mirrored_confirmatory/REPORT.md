# 2x2 Expanded Welch-Satterthwaite Experiment

## Scope

Profile: `confirmatory`.
Exact simulated configurations: `39`.
Each result below belongs to one exact population pair and sample-size setting.
No false-positive rate or power value is averaged across configurations.

## Equal-size null calibration

### N0

| n_p | minimum_expected_either | false_positive_rate_05: Expanded Welch | false_positive_rate_05: Normal Wald | false_positive_rate_05: Simple Welch | true_negative_rate_05: Expanded Welch | true_negative_rate_05: Normal Wald | true_negative_rate_05: Simple Welch | valid_rate: Expanded Welch | valid_rate: Normal Wald | valid_rate: Simple Welch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 1.401 | 0.047622 | 0.133 | 0.098814 | 0.95238 | 0.867 | 0.90119 | 0.97224 | 0.99702 | 0.99702 |
| 50 | 7.0051 | 0.037886 | 0.04718 | 0.04376 | 0.96211 | 0.95282 | 0.95624 | 0.99984 | 1 | 1 |
| 1000 | 140.1 | 0.05024 | 0.05134 | 0.05132 | 0.94976 | 0.94866 | 0.94868 | 1 | 1 | 1 |

Full case sheet: [`case_sheets/N0.md`](case_sheets/N0.md).

### N3

| n_p | minimum_expected_either | false_positive_rate_05: Expanded Welch | false_positive_rate_05: Normal Wald | false_positive_rate_05: Simple Welch | true_negative_rate_05: Expanded Welch | true_negative_rate_05: Normal Wald | true_negative_rate_05: Simple Welch | valid_rate: Expanded Welch | valid_rate: Normal Wald | valid_rate: Simple Welch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 1.7298 | 0.018097 | 0.030341 | 0.027621 | 0.9819 | 0.96966 | 0.97238 | 0.99464 | 0.99998 | 0.99998 |

Full case sheet: [`case_sheets/N3.md`](case_sheets/N3.md).

### N6

| n_p | minimum_expected_either | false_positive_rate_05: Expanded Welch | false_positive_rate_05: Normal Wald | false_positive_rate_05: Simple Welch | true_negative_rate_05: Expanded Welch | true_negative_rate_05: Normal Wald | true_negative_rate_05: Simple Welch | valid_rate: Expanded Welch | valid_rate: Normal Wald | valid_rate: Simple Welch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 0.24263 | 0.0065359 | 0.064945 | 0.062405 | 0.99346 | 0.93505 | 0.9376 | 0.9945 | 0.99992 | 0.99992 |
| 200 | 0.48526 | 0.039622 | 0.13964 | 0.13876 | 0.96038 | 0.86036 | 0.86124 | 0.99996 | 1 | 1 |

Full case sheet: [`case_sheets/N6.md`](case_sheets/N6.md).

### N7

| n_p | minimum_expected_either | false_positive_rate_05: Expanded Welch | false_positive_rate_05: Normal Wald | false_positive_rate_05: Simple Welch | true_negative_rate_05: Expanded Welch | true_negative_rate_05: Normal Wald | true_negative_rate_05: Simple Welch | valid_rate: Expanded Welch | valid_rate: Normal Wald | valid_rate: Simple Welch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000 | 0.27991 | 2.3438e-05 | 0.0026037 | 0.0026037 | 0.99998 | 0.9974 | 0.9974 | 0.8533 | 0.99856 | 0.99856 |

Full case sheet: [`case_sheets/N7.md`](case_sheets/N7.md).

## Other null experiments

C2-C4 are reported configuration by configuration in `null_summary.csv` and
the corresponding files under `case_sheets/`.

## Power

Power rows distinguish the null point from true alternatives and include
false-positive, true-negative, true-positive, and false-negative counts.
Detection power uses the fixed p <= 0.05 rejection threshold.

- [Mirrored alternatives](case_sheets/POWER_mirrored.md)

## Mathematically infeasible requests

These settings were not simulated because the requested MI exceeds the
attainable range for the fixed margins. They were not removed for low
expected counts.

| experiment | pair_id | s | target_mi | reason |
| --- | --- | --- | --- | --- |
| C4 | C4_s0p001_i0p005 | 0.001 | 0.005 | Target MI 0.005 exceeds branch maximum 0.00317565591968. |

## Output guide

- `configurations.csv`: exact P, Q, sample sizes, MI, and expected counts.
- `null_summary.csv`: configuration-specific null decisions and diagnostics.
- `power_summary.csv`: configuration-specific null/alternative decisions.
- `rejection_curves.csv.gz`: lower-tail calibration for every null configuration.
- `mechanism_diagnostics.csv`: estimator, standard-error, sparsity, and df diagnostics.
- `replicate_blocks.csv`: independent seed-block stability.
- `power_null_thresholds.csv`: independent size-adjustment thresholds.
- `case_sheets/`: readable records for each population pair.
- `figures/`: unpooled calibration, validity, and power plots.
