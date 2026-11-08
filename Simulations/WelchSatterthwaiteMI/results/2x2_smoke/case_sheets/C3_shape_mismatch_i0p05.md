# C3_shape_mismatch_i0p05: Near-zero MI with different margins

## Population tables

- True MI: P = `0.05`, Q = `0.05` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.32839079918248304, 0.17160920081751696], [0.17160920081751696, 0.32839079918248304]]`.
- Q probabilities: `[[0.4912371977070939, 0.20876280229290606], [0.1087628022929061, 0.1912371977070939]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p05_n20 | C3 | 20 | 20 | 2.1753 | Expanded Welch | 0.050403 | 0.9496 | 0.9496 | 0.992 | 4.2119 |
| C3_C3_shape_mismatch_i0p05_n20 | C3 | 20 | 20 | 2.1753 | Normal Wald | 0.086172 | 0.91383 | 0.91383 | 0.998 | inf |
| C3_C3_shape_mismatch_i0p05_n20 | C3 | 20 | 20 | 2.1753 | Simple Welch | 0.072144 | 0.92786 | 0.92786 | 0.998 | 28.436 |
| C3_C3_shape_mismatch_i0p05_n50 | C3 | 50 | 50 | 5.4381 | Expanded Welch | 0.026 | 0.974 | 0.974 | 1 | 7.3927 |
| C3_C3_shape_mismatch_i0p05_n50 | C3 | 50 | 50 | 5.4381 | Normal Wald | 0.05 | 0.95 | 0.95 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n50 | C3 | 50 | 50 | 5.4381 | Simple Welch | 0.038 | 0.962 | 0.962 | 1 | 84.635 |
| C3_C3_shape_mismatch_i0p05_n100 | C3 | 100 | 100 | 10.876 | Expanded Welch | 0.022 | 0.978 | 0.978 | 1 | 13.298 |
| C3_C3_shape_mismatch_i0p05_n100 | C3 | 100 | 100 | 10.876 | Normal Wald | 0.03 | 0.97 | 0.97 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n100 | C3 | 100 | 100 | 10.876 | Simple Welch | 0.026 | 0.974 | 0.974 | 1 | 183.85 |
| C3_C3_shape_mismatch_i0p05_n200 | C3 | 200 | 200 | 21.753 | Expanded Welch | 0.036 | 0.964 | 0.964 | 1 | 25.331 |
| C3_C3_shape_mismatch_i0p05_n200 | C3 | 200 | 200 | 21.753 | Normal Wald | 0.05 | 0.95 | 0.95 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n200 | C3 | 200 | 200 | 21.753 | Simple Welch | 0.046 | 0.954 | 0.954 | 1 | 382.3 |
| C3_C3_shape_mismatch_i0p05_n500 | C3 | 500 | 500 | 54.381 | Expanded Welch | 0.056 | 0.944 | 0.944 | 1 | 59.652 |
| C3_C3_shape_mismatch_i0p05_n500 | C3 | 500 | 500 | 54.381 | Normal Wald | 0.068 | 0.932 | 0.932 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n500 | C3 | 500 | 500 | 54.381 | Simple Welch | 0.066 | 0.934 | 0.934 | 1 | 981.48 |
| C3_C3_shape_mismatch_i0p05_n1000 | C3 | 1000 | 1000 | 108.76 | Expanded Welch | 0.04 | 0.96 | 0.96 | 1 | 118.69 |
| C3_C3_shape_mismatch_i0p05_n1000 | C3 | 1000 | 1000 | 108.76 | Normal Wald | 0.04 | 0.96 | 0.96 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n1000 | C3 | 1000 | 1000 | 108.76 | Simple Welch | 0.04 | 0.96 | 0.96 | 1 | 1980.7 |

No row is averaged with another population pair or sample-size setting.
