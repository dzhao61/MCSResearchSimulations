# C3_shape_mismatch_i0p005: Near-zero MI with different margins

## Population tables

- True MI: P = `0.005`, Q = `0.005` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.2749791440368653, 0.22502085596313473], [0.22502085596313473, 0.2749791440368653]]`.
- Q probabilities: `[[0.4425477177574097, 0.25745228224259026], [0.15745228224259025, 0.14254771775740974]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p005_n20 | C3 | 20 | 20 | 2.851 | Expanded Welch | 0.016194 | 0.98381 | 0.98381 | 0.988 | 1.1013 |
| C3_C3_shape_mismatch_i0p005_n20 | C3 | 20 | 20 | 2.851 | Normal Wald | 0.026104 | 0.9739 | 0.9739 | 0.996 | inf |
| C3_C3_shape_mismatch_i0p005_n20 | C3 | 20 | 20 | 2.851 | Simple Welch | 0.024096 | 0.9759 | 0.9759 | 0.996 | 25.965 |
| C3_C3_shape_mismatch_i0p005_n50 | C3 | 50 | 50 | 7.1274 | Expanded Welch | 0.0040241 | 0.99598 | 0.99598 | 0.994 | 1.3454 |
| C3_C3_shape_mismatch_i0p005_n50 | C3 | 50 | 50 | 7.1274 | Normal Wald | 0.004 | 0.996 | 0.996 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n50 | C3 | 50 | 50 | 7.1274 | Simple Welch | 0.004 | 0.996 | 0.996 | 1 | 68.36 |
| C3_C3_shape_mismatch_i0p005_n100 | C3 | 100 | 100 | 14.255 | Expanded Welch | 0 | 1 | 1 | 0.996 | 1.6575 |
| C3_C3_shape_mismatch_i0p005_n100 | C3 | 100 | 100 | 14.255 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n100 | C3 | 100 | 100 | 14.255 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 135.19 |
| C3_C3_shape_mismatch_i0p005_n200 | C3 | 200 | 200 | 28.51 | Expanded Welch | 0.008016 | 0.99198 | 0.99198 | 0.998 | 2.6588 |
| C3_C3_shape_mismatch_i0p005_n200 | C3 | 200 | 200 | 28.51 | Normal Wald | 0.012 | 0.988 | 0.988 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n200 | C3 | 200 | 200 | 28.51 | Simple Welch | 0.012 | 0.988 | 0.988 | 1 | 294.01 |
| C3_C3_shape_mismatch_i0p005_n500 | C3 | 500 | 500 | 71.274 | Expanded Welch | 0.006012 | 0.99399 | 0.99399 | 0.998 | 5.4242 |
| C3_C3_shape_mismatch_i0p005_n500 | C3 | 500 | 500 | 71.274 | Normal Wald | 0.006 | 0.994 | 0.994 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n500 | C3 | 500 | 500 | 71.274 | Simple Welch | 0.006 | 0.994 | 0.994 | 1 | 862.84 |
| C3_C3_shape_mismatch_i0p005_n1000 | C3 | 1000 | 1000 | 142.55 | Expanded Welch | 0.018 | 0.982 | 0.982 | 1 | 11.229 |
| C3_C3_shape_mismatch_i0p005_n1000 | C3 | 1000 | 1000 | 142.55 | Normal Wald | 0.028 | 0.972 | 0.972 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n1000 | C3 | 1000 | 1000 | 142.55 | Simple Welch | 0.028 | 0.972 | 0.972 | 1 | 1838.9 |

No row is averaged with another population pair or sample-size setting.
