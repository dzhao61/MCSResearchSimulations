# C3_same_balanced_i0p0001: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `9.999999999e-05`, Q = `9.999999999e-05` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.2535354749788844, 0.2464645250211156], [0.2464645250211156, 0.2535354749788844]]`.
- Q probabilities: `[[0.2535354749788844, 0.2464645250211156], [0.2464645250211156, 0.2535354749788844]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p0001_n20 | C3 | 20 | 20 | 4.9293 | Expanded Welch | 0.0020747 | 0.99793 | 0.99793 | 0.964 | 0.76546 |
| C3_C3_same_balanced_i0p0001_n20 | C3 | 20 | 20 | 4.9293 | Normal Wald | 0.0020121 | 0.99799 | 0.99799 | 0.994 | inf |
| C3_C3_same_balanced_i0p0001_n20 | C3 | 20 | 20 | 4.9293 | Simple Welch | 0.0020121 | 0.99799 | 0.99799 | 0.994 | 24.169 |
| C3_C3_same_balanced_i0p0001_n50 | C3 | 50 | 50 | 12.323 | Expanded Welch | 0 | 1 | 1 | 0.978 | 0.74098 |
| C3_C3_same_balanced_i0p0001_n50 | C3 | 50 | 50 | 12.323 | Normal Wald | 0 | 1 | 1 | 0.996 | inf |
| C3_C3_same_balanced_i0p0001_n50 | C3 | 50 | 50 | 12.323 | Simple Welch | 0 | 1 | 1 | 0.996 | 64.652 |
| C3_C3_same_balanced_i0p0001_n100 | C3 | 100 | 100 | 24.646 | Expanded Welch | 0 | 1 | 1 | 0.992 | 0.62322 |
| C3_C3_same_balanced_i0p0001_n100 | C3 | 100 | 100 | 24.646 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n100 | C3 | 100 | 100 | 24.646 | Simple Welch | 0 | 1 | 1 | 1 | 136.47 |
| C3_C3_same_balanced_i0p0001_n200 | C3 | 200 | 200 | 49.293 | Expanded Welch | 0 | 1 | 1 | 0.996 | 0.77426 |
| C3_C3_same_balanced_i0p0001_n200 | C3 | 200 | 200 | 49.293 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n200 | C3 | 200 | 200 | 49.293 | Simple Welch | 0 | 1 | 1 | 1 | 263.71 |
| C3_C3_same_balanced_i0p0001_n500 | C3 | 500 | 500 | 123.23 | Expanded Welch | 0 | 1 | 1 | 0.998 | 0.80918 |
| C3_C3_same_balanced_i0p0001_n500 | C3 | 500 | 500 | 123.23 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n500 | C3 | 500 | 500 | 123.23 | Simple Welch | 0 | 1 | 1 | 1 | 669.29 |
| C3_C3_same_balanced_i0p0001_n1000 | C3 | 1000 | 1000 | 246.46 | Expanded Welch | 0 | 1 | 1 | 0.998 | 0.87601 |
| C3_C3_same_balanced_i0p0001_n1000 | C3 | 1000 | 1000 | 246.46 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n1000 | C3 | 1000 | 1000 | 246.46 | Simple Welch | 0 | 1 | 1 | 1 | 1351 |

No row is averaged with another population pair or sample-size setting.
