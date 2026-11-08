# C3_shape_mismatch_i0p0005: Near-zero MI with different margins

## Population tables

- True MI: P = `0.0005`, Q = `0.0005` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.25790503527118464, 0.24209496472881536], [0.24209496472881536, 0.25790503527118464]]`.
- Q probabilities: `[[0.42711148572657504, 0.2728885142734249], [0.17288851427342491, 0.12711148572657507]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p0005_n20 | C3 | 20 | 20 | 2.5422 | Expanded Welch | 0.0020121 | 0.99799 | 0.99799 | 0.994 | 0.92788 |
| C3_C3_shape_mismatch_i0p0005_n20 | C3 | 20 | 20 | 2.5422 | Normal Wald | 0.016 | 0.984 | 0.984 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n20 | C3 | 20 | 20 | 2.5422 | Simple Welch | 0.01 | 0.99 | 0.99 | 1 | 27.367 |
| C3_C3_shape_mismatch_i0p0005_n50 | C3 | 50 | 50 | 6.3556 | Expanded Welch | 0 | 1 | 1 | 0.996 | 0.78282 |
| C3_C3_shape_mismatch_i0p0005_n50 | C3 | 50 | 50 | 6.3556 | Normal Wald | 0 | 1 | 1 | 0.998 | inf |
| C3_C3_shape_mismatch_i0p0005_n50 | C3 | 50 | 50 | 6.3556 | Simple Welch | 0 | 1 | 1 | 0.998 | 65.607 |
| C3_C3_shape_mismatch_i0p0005_n100 | C3 | 100 | 100 | 12.711 | Expanded Welch | 0 | 1 | 1 | 0.996 | 0.78874 |
| C3_C3_shape_mismatch_i0p0005_n100 | C3 | 100 | 100 | 12.711 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n100 | C3 | 100 | 100 | 12.711 | Simple Welch | 0 | 1 | 1 | 1 | 128.85 |
| C3_C3_shape_mismatch_i0p0005_n200 | C3 | 200 | 200 | 25.422 | Expanded Welch | 0 | 1 | 1 | 1 | 0.75504 |
| C3_C3_shape_mismatch_i0p0005_n200 | C3 | 200 | 200 | 25.422 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n200 | C3 | 200 | 200 | 25.422 | Simple Welch | 0 | 1 | 1 | 1 | 254.21 |
| C3_C3_shape_mismatch_i0p0005_n500 | C3 | 500 | 500 | 63.556 | Expanded Welch | 0 | 1 | 1 | 0.998 | 1.1797 |
| C3_C3_shape_mismatch_i0p0005_n500 | C3 | 500 | 500 | 63.556 | Normal Wald | 0.004 | 0.996 | 0.996 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n500 | C3 | 500 | 500 | 63.556 | Simple Welch | 0.004 | 0.996 | 0.996 | 1 | 663.08 |
| C3_C3_shape_mismatch_i0p0005_n1000 | C3 | 1000 | 1000 | 127.11 | Expanded Welch | 0 | 1 | 1 | 1 | 1.4431 |
| C3_C3_shape_mismatch_i0p0005_n1000 | C3 | 1000 | 1000 | 127.11 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n1000 | C3 | 1000 | 1000 | 127.11 | Simple Welch | 0 | 1 | 1 | 1 | 1411.2 |

No row is averaged with another population pair or sample-size setting.
