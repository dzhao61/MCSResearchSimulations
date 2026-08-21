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
| C3_C3_same_balanced_i0_n20 | C3 | 20 | 20 | 5 | Expanded Welch | 0.0040816 | 0.99592 | 0.99592 | 0.98 | 0.78302 |
| C3_C3_same_balanced_i0_n20 | C3 | 20 | 20 | 5 | Normal Wald | 0.012024 | 0.98798 | 0.98798 | 0.998 | inf |
| C3_C3_same_balanced_i0_n20 | C3 | 20 | 20 | 5 | Simple Welch | 0.01002 | 0.98998 | 0.98998 | 0.998 | 27.021 |
| C3_C3_same_balanced_i0_n50 | C3 | 50 | 50 | 12.5 | Expanded Welch | 0 | 1 | 1 | 0.988 | 0.76837 |
| C3_C3_same_balanced_i0_n50 | C3 | 50 | 50 | 12.5 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0_n50 | C3 | 50 | 50 | 12.5 | Simple Welch | 0 | 1 | 1 | 1 | 64.656 |
| C3_C3_same_balanced_i0_n100 | C3 | 100 | 100 | 25 | Expanded Welch | 0 | 1 | 1 | 0.998 | 0.74965 |
| C3_C3_same_balanced_i0_n100 | C3 | 100 | 100 | 25 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0_n100 | C3 | 100 | 100 | 25 | Simple Welch | 0 | 1 | 1 | 1 | 128.84 |
| C3_C3_same_balanced_i0_n200 | C3 | 200 | 200 | 50 | Expanded Welch | 0 | 1 | 1 | 0.994 | 0.71967 |
| C3_C3_same_balanced_i0_n200 | C3 | 200 | 200 | 50 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0_n200 | C3 | 200 | 200 | 50 | Simple Welch | 0 | 1 | 1 | 1 | 259.13 |
| C3_C3_same_balanced_i0_n500 | C3 | 500 | 500 | 125 | Expanded Welch | 0 | 1 | 1 | 1 | 0.75862 |
| C3_C3_same_balanced_i0_n500 | C3 | 500 | 500 | 125 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0_n500 | C3 | 500 | 500 | 125 | Simple Welch | 0 | 1 | 1 | 1 | 653.5 |
| C3_C3_same_balanced_i0_n1000 | C3 | 1000 | 1000 | 250 | Expanded Welch | 0 | 1 | 1 | 0.998 | 0.63846 |
| C3_C3_same_balanced_i0_n1000 | C3 | 1000 | 1000 | 250 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0_n1000 | C3 | 1000 | 1000 | 250 | Simple Welch | 0 | 1 | 1 | 1 | 1382.7 |

No row is averaged with another population pair or sample-size setting.
