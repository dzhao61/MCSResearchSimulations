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
| C3_C3_shape_mismatch_i0p0005_n20 | C3 | 20 | 20 | 2.5422 | Expanded Welch | 0.005184 | 0.99482 | 0.99482 | 0.9838 | 0.9262 |
| C3_C3_shape_mismatch_i0p0005_n20 | C3 | 20 | 20 | 2.5422 | Normal Wald | 0.015652 | 0.98435 | 0.98435 | 0.9967 | inf |
| C3_C3_shape_mismatch_i0p0005_n20 | C3 | 20 | 20 | 2.5422 | Simple Welch | 0.011438 | 0.98856 | 0.98856 | 0.9967 | 25.899 |
| C3_C3_shape_mismatch_i0p0005_n50 | C3 | 50 | 50 | 6.3556 | Expanded Welch | 0.00040359 | 0.9996 | 0.9996 | 0.9911 | 0.79761 |
| C3_C3_shape_mismatch_i0p0005_n50 | C3 | 50 | 50 | 6.3556 | Normal Wald | 0.00080024 | 0.9992 | 0.9992 | 0.9997 | inf |
| C3_C3_shape_mismatch_i0p0005_n50 | C3 | 50 | 50 | 6.3556 | Simple Welch | 0.00070021 | 0.9993 | 0.9993 | 0.9997 | 65.438 |
| C3_C3_shape_mismatch_i0p0005_n100 | C3 | 100 | 100 | 12.711 | Expanded Welch | 0 | 1 | 1 | 0.9946 | 0.76458 |
| C3_C3_shape_mismatch_i0p0005_n100 | C3 | 100 | 100 | 12.711 | Normal Wald | 0.0002 | 0.9998 | 0.9998 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n100 | C3 | 100 | 100 | 12.711 | Simple Welch | 0.0002 | 0.9998 | 0.9998 | 1 | 131.06 |
| C3_C3_shape_mismatch_i0p0005_n200 | C3 | 200 | 200 | 25.422 | Expanded Welch | 0.0001001 | 0.9999 | 0.9999 | 0.999 | 0.85129 |
| C3_C3_shape_mismatch_i0p0005_n200 | C3 | 200 | 200 | 25.422 | Normal Wald | 0.00060006 | 0.9994 | 0.9994 | 0.9999 | inf |
| C3_C3_shape_mismatch_i0p0005_n200 | C3 | 200 | 200 | 25.422 | Simple Welch | 0.00050005 | 0.9995 | 0.9995 | 0.9999 | 265.12 |
| C3_C3_shape_mismatch_i0p0005_n500 | C3 | 500 | 500 | 63.556 | Expanded Welch | 0.00010009 | 0.9999 | 0.9999 | 0.9991 | 1.1093 |
| C3_C3_shape_mismatch_i0p0005_n500 | C3 | 500 | 500 | 63.556 | Normal Wald | 0.0007 | 0.9993 | 0.9993 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n500 | C3 | 500 | 500 | 63.556 | Simple Welch | 0.0007 | 0.9993 | 0.9993 | 1 | 669.75 |
| C3_C3_shape_mismatch_i0p0005_n1000 | C3 | 1000 | 1000 | 127.11 | Expanded Welch | 0.00010009 | 0.9999 | 0.9999 | 0.9991 | 1.5171 |
| C3_C3_shape_mismatch_i0p0005_n1000 | C3 | 1000 | 1000 | 127.11 | Normal Wald | 0.0009 | 0.9991 | 0.9991 | 1 | inf |
| C3_C3_shape_mismatch_i0p0005_n1000 | C3 | 1000 | 1000 | 127.11 | Simple Welch | 0.0008 | 0.9992 | 0.9992 | 1 | 1378.1 |

No row is averaged with another population pair or sample-size setting.
