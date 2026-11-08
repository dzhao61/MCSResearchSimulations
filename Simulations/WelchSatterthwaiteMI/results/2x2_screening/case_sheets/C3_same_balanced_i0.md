# C3_same_balanced_i0: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0`, Q = `0` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.25, 0.25], [0.25, 0.25]]`.
- Q probabilities: `[[0.25, 0.25], [0.25, 0.25]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0_n20 | C3 | 20 | 20 | 5 | Expanded Welch | 0.0054253 | 0.99457 | 0.99457 | 0.9769 | 0.90192 |
| C3_C3_same_balanced_i0_n20 | C3 | 20 | 20 | 5 | Normal Wald | 0.011435 | 0.98856 | 0.98856 | 0.9969 | inf |
| C3_C3_same_balanced_i0_n20 | C3 | 20 | 20 | 5 | Simple Welch | 0.0097302 | 0.99027 | 0.99027 | 0.9969 | 25.688 |
| C3_C3_same_balanced_i0_n50 | C3 | 50 | 50 | 12.5 | Expanded Welch | 0.00020358 | 0.9998 | 0.9998 | 0.9824 | 0.73601 |
| C3_C3_same_balanced_i0_n50 | C3 | 50 | 50 | 12.5 | Normal Wald | 0.00030018 | 0.9997 | 0.9997 | 0.9994 | inf |
| C3_C3_same_balanced_i0_n50 | C3 | 50 | 50 | 12.5 | Simple Welch | 0.00030018 | 0.9997 | 0.9997 | 0.9994 | 65.965 |
| C3_C3_same_balanced_i0_n100 | C3 | 100 | 100 | 25 | Expanded Welch | 0.00010092 | 0.9999 | 0.9999 | 0.9909 | 0.72989 |
| C3_C3_same_balanced_i0_n100 | C3 | 100 | 100 | 25 | Normal Wald | 0.00070028 | 0.9993 | 0.9993 | 0.9996 | inf |
| C3_C3_same_balanced_i0_n100 | C3 | 100 | 100 | 25 | Simple Welch | 0.00060024 | 0.9994 | 0.9994 | 0.9996 | 132.2 |
| C3_C3_same_balanced_i0_n200 | C3 | 200 | 200 | 50 | Expanded Welch | 0.00010046 | 0.9999 | 0.9999 | 0.9954 | 0.69796 |
| C3_C3_same_balanced_i0_n200 | C3 | 200 | 200 | 50 | Normal Wald | 0.0003 | 0.9997 | 0.9997 | 1 | inf |
| C3_C3_same_balanced_i0_n200 | C3 | 200 | 200 | 50 | Simple Welch | 0.0002 | 0.9998 | 0.9998 | 1 | 267.66 |
| C3_C3_same_balanced_i0_n500 | C3 | 500 | 500 | 125 | Expanded Welch | 0.00010015 | 0.9999 | 0.9999 | 0.9985 | 0.68586 |
| C3_C3_same_balanced_i0_n500 | C3 | 500 | 500 | 125 | Normal Wald | 0.0001 | 0.9999 | 0.9999 | 1 | inf |
| C3_C3_same_balanced_i0_n500 | C3 | 500 | 500 | 125 | Simple Welch | 0.0001 | 0.9999 | 0.9999 | 1 | 661.46 |
| C3_C3_same_balanced_i0_n1000 | C3 | 1000 | 1000 | 250 | Expanded Welch | 0 | 1 | 1 | 0.9988 | 0.69474 |
| C3_C3_same_balanced_i0_n1000 | C3 | 1000 | 1000 | 250 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0_n1000 | C3 | 1000 | 1000 | 250 | Simple Welch | 0 | 1 | 1 | 1 | 1323.4 |

No row is averaged with another population pair or sample-size setting.
