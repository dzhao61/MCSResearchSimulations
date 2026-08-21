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
| C3_C3_same_balanced_i0p05_n20 | C3 | 20 | 20 | 3.4322 | Expanded Welch | 0.03368 | 0.96632 | 0.96632 | 0.9917 | 4.0045 |
| C3_C3_same_balanced_i0p05_n20 | C3 | 20 | 20 | 3.4322 | Normal Wald | 0.047524 | 0.95248 | 0.95248 | 0.9995 | inf |
| C3_C3_same_balanced_i0p05_n20 | C3 | 20 | 20 | 3.4322 | Simple Welch | 0.041921 | 0.95808 | 0.95808 | 0.9995 | 29.275 |
| C3_C3_same_balanced_i0p05_n50 | C3 | 50 | 50 | 8.5805 | Expanded Welch | 0.017719 | 0.98228 | 0.98228 | 0.9989 | 7.1416 |
| C3_C3_same_balanced_i0p05_n50 | C3 | 50 | 50 | 8.5805 | Normal Wald | 0.0258 | 0.9742 | 0.9742 | 1 | inf |
| C3_C3_same_balanced_i0p05_n50 | C3 | 50 | 50 | 8.5805 | Simple Welch | 0.0233 | 0.9767 | 0.9767 | 1 | 85.469 |
| C3_C3_same_balanced_i0p05_n100 | C3 | 100 | 100 | 17.161 | Expanded Welch | 0.021902 | 0.9781 | 0.9781 | 0.9999 | 12.979 |
| C3_C3_same_balanced_i0p05_n100 | C3 | 100 | 100 | 17.161 | Normal Wald | 0.0331 | 0.9669 | 0.9669 | 1 | inf |
| C3_C3_same_balanced_i0p05_n100 | C3 | 100 | 100 | 17.161 | Simple Welch | 0.0318 | 0.9682 | 0.9682 | 1 | 184.32 |
| C3_C3_same_balanced_i0p05_n200 | C3 | 200 | 200 | 34.322 | Expanded Welch | 0.0349 | 0.9651 | 0.9651 | 1 | 24.49 |
| C3_C3_same_balanced_i0p05_n200 | C3 | 200 | 200 | 34.322 | Normal Wald | 0.0426 | 0.9574 | 0.9574 | 1 | inf |
| C3_C3_same_balanced_i0p05_n200 | C3 | 200 | 200 | 34.322 | Simple Welch | 0.0421 | 0.9579 | 0.9579 | 1 | 383.59 |
| C3_C3_same_balanced_i0p05_n500 | C3 | 500 | 500 | 85.805 | Expanded Welch | 0.0402 | 0.9598 | 0.9598 | 1 | 59.674 |
| C3_C3_same_balanced_i0p05_n500 | C3 | 500 | 500 | 85.805 | Normal Wald | 0.0458 | 0.9542 | 0.9542 | 1 | inf |
| C3_C3_same_balanced_i0p05_n500 | C3 | 500 | 500 | 85.805 | Simple Welch | 0.0457 | 0.9543 | 0.9543 | 1 | 983.31 |
| C3_C3_same_balanced_i0p05_n1000 | C3 | 1000 | 1000 | 171.61 | Expanded Welch | 0.0442 | 0.9558 | 0.9558 | 1 | 118.82 |
| C3_C3_same_balanced_i0p05_n1000 | C3 | 1000 | 1000 | 171.61 | Normal Wald | 0.0461 | 0.9539 | 0.9539 | 1 | inf |
| C3_C3_same_balanced_i0p05_n1000 | C3 | 1000 | 1000 | 171.61 | Simple Welch | 0.046 | 0.954 | 0.954 | 1 | 1982.4 |

No row is averaged with another population pair or sample-size setting.
