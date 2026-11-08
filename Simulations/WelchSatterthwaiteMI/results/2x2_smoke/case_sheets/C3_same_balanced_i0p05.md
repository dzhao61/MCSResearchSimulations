# C3_same_balanced_i0p05: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0.05`, Q = `0.05` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.32839079918248304, 0.17160920081751696], [0.17160920081751696, 0.32839079918248304]]`.
- Q probabilities: `[[0.32839079918248304, 0.17160920081751696], [0.17160920081751696, 0.32839079918248304]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p05_n20 | C3 | 20 | 20 | 3.4322 | Expanded Welch | 0.032129 | 0.96787 | 0.96787 | 0.996 | 3.5551 |
| C3_C3_same_balanced_i0p05_n20 | C3 | 20 | 20 | 3.4322 | Normal Wald | 0.054 | 0.946 | 0.946 | 1 | inf |
| C3_C3_same_balanced_i0p05_n20 | C3 | 20 | 20 | 3.4322 | Simple Welch | 0.048 | 0.952 | 0.952 | 1 | 29.227 |
| C3_C3_same_balanced_i0p05_n50 | C3 | 50 | 50 | 8.5805 | Expanded Welch | 0.02004 | 0.97996 | 0.97996 | 0.998 | 7.8971 |
| C3_C3_same_balanced_i0p05_n50 | C3 | 50 | 50 | 8.5805 | Normal Wald | 0.03 | 0.97 | 0.97 | 1 | inf |
| C3_C3_same_balanced_i0p05_n50 | C3 | 50 | 50 | 8.5805 | Simple Welch | 0.028 | 0.972 | 0.972 | 1 | 86.672 |
| C3_C3_same_balanced_i0p05_n100 | C3 | 100 | 100 | 17.161 | Expanded Welch | 0.024 | 0.976 | 0.976 | 1 | 12.724 |
| C3_C3_same_balanced_i0p05_n100 | C3 | 100 | 100 | 17.161 | Normal Wald | 0.044 | 0.956 | 0.956 | 1 | inf |
| C3_C3_same_balanced_i0p05_n100 | C3 | 100 | 100 | 17.161 | Simple Welch | 0.04 | 0.96 | 0.96 | 1 | 183.25 |
| C3_C3_same_balanced_i0p05_n200 | C3 | 200 | 200 | 34.322 | Expanded Welch | 0.028 | 0.972 | 0.972 | 1 | 25.746 |
| C3_C3_same_balanced_i0p05_n200 | C3 | 200 | 200 | 34.322 | Normal Wald | 0.036 | 0.964 | 0.964 | 1 | inf |
| C3_C3_same_balanced_i0p05_n200 | C3 | 200 | 200 | 34.322 | Simple Welch | 0.034 | 0.966 | 0.966 | 1 | 383.47 |
| C3_C3_same_balanced_i0p05_n500 | C3 | 500 | 500 | 85.805 | Expanded Welch | 0.032 | 0.968 | 0.968 | 1 | 60.164 |
| C3_C3_same_balanced_i0p05_n500 | C3 | 500 | 500 | 85.805 | Normal Wald | 0.034 | 0.966 | 0.966 | 1 | inf |
| C3_C3_same_balanced_i0p05_n500 | C3 | 500 | 500 | 85.805 | Simple Welch | 0.034 | 0.966 | 0.966 | 1 | 983.71 |
| C3_C3_same_balanced_i0p05_n1000 | C3 | 1000 | 1000 | 171.61 | Expanded Welch | 0.054 | 0.946 | 0.946 | 1 | 117.56 |
| C3_C3_same_balanced_i0p05_n1000 | C3 | 1000 | 1000 | 171.61 | Normal Wald | 0.058 | 0.942 | 0.942 | 1 | inf |
| C3_C3_same_balanced_i0p05_n1000 | C3 | 1000 | 1000 | 171.61 | Simple Welch | 0.058 | 0.942 | 0.942 | 1 | 1980.9 |

No row is averaged with another population pair or sample-size setting.
