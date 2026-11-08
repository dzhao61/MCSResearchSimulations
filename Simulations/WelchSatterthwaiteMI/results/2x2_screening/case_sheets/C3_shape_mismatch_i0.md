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
| C3_C3_shape_mismatch_i0_n20 | C3 | 20 | 20 | 2.4 | Expanded Welch | 0.0053928 | 0.99461 | 0.99461 | 0.9828 | 0.92406 |
| C3_C3_shape_mismatch_i0_n20 | C3 | 20 | 20 | 2.4 | Normal Wald | 0.016053 | 0.98395 | 0.98395 | 0.9967 | inf |
| C3_C3_shape_mismatch_i0_n20 | C3 | 20 | 20 | 2.4 | Simple Welch | 0.011939 | 0.98806 | 0.98806 | 0.9967 | 25.917 |
| C3_C3_shape_mismatch_i0_n50 | C3 | 50 | 50 | 6 | Expanded Welch | 0.0010099 | 0.99899 | 0.99899 | 0.9902 | 0.74916 |
| C3_C3_shape_mismatch_i0_n50 | C3 | 50 | 50 | 6 | Normal Wald | 0.0013004 | 0.9987 | 0.9987 | 0.9997 | inf |
| C3_C3_shape_mismatch_i0_n50 | C3 | 50 | 50 | 6 | Simple Welch | 0.0013004 | 0.9987 | 0.9987 | 0.9997 | 65.253 |
| C3_C3_shape_mismatch_i0_n100 | C3 | 100 | 100 | 12 | Expanded Welch | 0.00010051 | 0.9999 | 0.9999 | 0.9949 | 0.74473 |
| C3_C3_shape_mismatch_i0_n100 | C3 | 100 | 100 | 12 | Normal Wald | 0.0005 | 0.9995 | 0.9995 | 1 | inf |
| C3_C3_shape_mismatch_i0_n100 | C3 | 100 | 100 | 12 | Simple Welch | 0.0004 | 0.9996 | 0.9996 | 1 | 131.29 |
| C3_C3_shape_mismatch_i0_n200 | C3 | 200 | 200 | 24 | Expanded Welch | 0.00010026 | 0.9999 | 0.9999 | 0.9974 | 0.70314 |
| C3_C3_shape_mismatch_i0_n200 | C3 | 200 | 200 | 24 | Normal Wald | 0.0001 | 0.9999 | 0.9999 | 1 | inf |
| C3_C3_shape_mismatch_i0_n200 | C3 | 200 | 200 | 24 | Simple Welch | 0.0001 | 0.9999 | 0.9999 | 1 | 265.11 |
| C3_C3_shape_mismatch_i0_n500 | C3 | 500 | 500 | 60 | Expanded Welch | 0 | 1 | 1 | 0.9994 | 0.68444 |
| C3_C3_shape_mismatch_i0_n500 | C3 | 500 | 500 | 60 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n500 | C3 | 500 | 500 | 60 | Simple Welch | 0 | 1 | 1 | 1 | 667.46 |
| C3_C3_shape_mismatch_i0_n1000 | C3 | 1000 | 1000 | 120 | Expanded Welch | 0 | 1 | 1 | 0.9992 | 0.69522 |
| C3_C3_shape_mismatch_i0_n1000 | C3 | 1000 | 1000 | 120 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0_n1000 | C3 | 1000 | 1000 | 120 | Simple Welch | 0 | 1 | 1 | 1 | 1328.2 |

No row is averaged with another population pair or sample-size setting.
