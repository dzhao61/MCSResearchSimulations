# C3_shape_mismatch_i0: Near-zero MI with different margins

## Population tables

- True MI: P = `0`, Q = `-2.220446049e-16` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.25, 0.25], [0.25, 0.25]]`.
- Q probabilities: `[[0.42, 0.27999999999999997], [0.18, 0.12]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0_n20 | C3 | 20 | 20 | 2.4 | Expanded Welch | 0.0061856 | 0.99381 | 0.99381 | 0.97 | 0.9065 |
| C3_C3_shape_mismatch_i0_n20 | C3 | 20 | 20 | 2.4 | Normal Wald | 0.01002 | 0.98998 | 0.98998 | 0.998 | inf |
| C3_C3_shape_mismatch_i0_n20 | C3 | 20 | 20 | 2.4 | Simple Welch | 0.008016 | 0.99198 | 0.99198 | 0.998 | 25.277 |
| C3_C3_shape_mismatch_i0_n50 | C3 | 50 | 50 | 6 | Expanded Welch | 0 | 1 | 1 | 0.98 | 0.77855 |
| C3_C3_shape_mismatch_i0_n50 | C3 | 50 | 50 | 6 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n50 | C3 | 50 | 50 | 6 | Simple Welch | 0 | 1 | 1 | 1 | 62.529 |
| C3_C3_shape_mismatch_i0_n100 | C3 | 100 | 100 | 12 | Expanded Welch | 0 | 1 | 1 | 0.996 | 0.71951 |
| C3_C3_shape_mismatch_i0_n100 | C3 | 100 | 100 | 12 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n100 | C3 | 100 | 100 | 12 | Simple Welch | 0 | 1 | 1 | 1 | 131.4 |
| C3_C3_shape_mismatch_i0_n200 | C3 | 200 | 200 | 24 | Expanded Welch | 0 | 1 | 1 | 0.994 | 0.7546 |
| C3_C3_shape_mismatch_i0_n200 | C3 | 200 | 200 | 24 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n200 | C3 | 200 | 200 | 24 | Simple Welch | 0 | 1 | 1 | 1 | 256.62 |
| C3_C3_shape_mismatch_i0_n500 | C3 | 500 | 500 | 60 | Expanded Welch | 0 | 1 | 1 | 1 | 0.72016 |
| C3_C3_shape_mismatch_i0_n500 | C3 | 500 | 500 | 60 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n500 | C3 | 500 | 500 | 60 | Simple Welch | 0 | 1 | 1 | 1 | 651.76 |
| C3_C3_shape_mismatch_i0_n1000 | C3 | 1000 | 1000 | 120 | Expanded Welch | 0 | 1 | 1 | 1 | 0.65886 |
| C3_C3_shape_mismatch_i0_n1000 | C3 | 1000 | 1000 | 120 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n1000 | C3 | 1000 | 1000 | 120 | Simple Welch | 0 | 1 | 1 | 1 | 1328 |

No row is averaged with another population pair or sample-size setting.
