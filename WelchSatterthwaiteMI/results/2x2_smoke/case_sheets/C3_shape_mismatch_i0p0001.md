# C3_shape_mismatch_i0p0001: Near-zero MI with different margins

## Population tables

- True MI: P = `9.999999999e-05`, Q = `0.0001` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.2535354749788844, 0.2464645250211156], [0.2464645250211156, 0.2535354749788844]]`.
- Q probabilities: `[[0.42317746548538415, 0.2768225345146158], [0.17682253451461583, 0.12317746548538415]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p0001_n20 | C3 | 20 | 20 | 2.4635 | Expanded Welch | 0.0040323 | 0.99597 | 0.99597 | 0.992 | 0.87174 |
| C3_C3_shape_mismatch_i0p0001_n20 | C3 | 20 | 20 | 2.4635 | Normal Wald | 0.016064 | 0.98394 | 0.98394 | 0.996 | inf |
| C3_C3_shape_mismatch_i0p0001_n20 | C3 | 20 | 20 | 2.4635 | Simple Welch | 0.0080321 | 0.99197 | 0.99197 | 0.996 | 25.19 |
| C3_C3_shape_mismatch_i0p0001_n50 | C3 | 50 | 50 | 6.1589 | Expanded Welch | 0.0020243 | 0.99798 | 0.99798 | 0.988 | 0.7625 |
| C3_C3_shape_mismatch_i0p0001_n50 | C3 | 50 | 50 | 6.1589 | Normal Wald | 0.004 | 0.996 | 0.996 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n50 | C3 | 50 | 50 | 6.1589 | Simple Welch | 0.004 | 0.996 | 0.996 | 1 | 69.341 |
| C3_C3_shape_mismatch_i0p0001_n100 | C3 | 100 | 100 | 12.318 | Expanded Welch | 0 | 1 | 1 | 0.994 | 0.75525 |
| C3_C3_shape_mismatch_i0p0001_n100 | C3 | 100 | 100 | 12.318 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n100 | C3 | 100 | 100 | 12.318 | Simple Welch | 0 | 1 | 1 | 1 | 127.97 |
| C3_C3_shape_mismatch_i0p0001_n200 | C3 | 200 | 200 | 24.635 | Expanded Welch | 0 | 1 | 1 | 0.998 | 0.75817 |
| C3_C3_shape_mismatch_i0p0001_n200 | C3 | 200 | 200 | 24.635 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n200 | C3 | 200 | 200 | 24.635 | Simple Welch | 0 | 1 | 1 | 1 | 269.73 |
| C3_C3_shape_mismatch_i0p0001_n500 | C3 | 500 | 500 | 61.589 | Expanded Welch | 0 | 1 | 1 | 0.998 | 0.69112 |
| C3_C3_shape_mismatch_i0p0001_n500 | C3 | 500 | 500 | 61.589 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n500 | C3 | 500 | 500 | 61.589 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 655.72 |
| C3_C3_shape_mismatch_i0p0001_n1000 | C3 | 1000 | 1000 | 123.18 | Expanded Welch | 0 | 1 | 1 | 1 | 0.77679 |
| C3_C3_shape_mismatch_i0p0001_n1000 | C3 | 1000 | 1000 | 123.18 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n1000 | C3 | 1000 | 1000 | 123.18 | Simple Welch | 0 | 1 | 1 | 1 | 1310.9 |

No row is averaged with another population pair or sample-size setting.
