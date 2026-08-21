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
| C3_C3_shape_mismatch_i0p0001_n20 | C3 | 20 | 20 | 2.4635 | Expanded Welch | 0.0053889 | 0.99461 | 0.99461 | 0.9835 | 0.88667 |
| C3_C3_shape_mismatch_i0p0001_n20 | C3 | 20 | 20 | 2.4635 | Normal Wald | 0.015757 | 0.98424 | 0.98424 | 0.9964 | inf |
| C3_C3_shape_mismatch_i0p0001_n20 | C3 | 20 | 20 | 2.4635 | Simple Welch | 0.011542 | 0.98846 | 0.98846 | 0.9964 | 25.725 |
| C3_C3_shape_mismatch_i0p0001_n50 | C3 | 50 | 50 | 6.1589 | Expanded Welch | 0.0016158 | 0.99838 | 0.99838 | 0.9902 | 0.76485 |
| C3_C3_shape_mismatch_i0p0001_n50 | C3 | 50 | 50 | 6.1589 | Normal Wald | 0.0024005 | 0.9976 | 0.9976 | 0.9998 | inf |
| C3_C3_shape_mismatch_i0p0001_n50 | C3 | 50 | 50 | 6.1589 | Simple Welch | 0.0023005 | 0.9977 | 0.9977 | 0.9998 | 65.258 |
| C3_C3_shape_mismatch_i0p0001_n100 | C3 | 100 | 100 | 12.318 | Expanded Welch | 0.00010048 | 0.9999 | 0.9999 | 0.9952 | 0.73609 |
| C3_C3_shape_mismatch_i0p0001_n100 | C3 | 100 | 100 | 12.318 | Normal Wald | 0.00030003 | 0.9997 | 0.9997 | 0.9999 | inf |
| C3_C3_shape_mismatch_i0p0001_n100 | C3 | 100 | 100 | 12.318 | Simple Welch | 0.00030003 | 0.9997 | 0.9997 | 0.9999 | 131.58 |
| C3_C3_shape_mismatch_i0p0001_n200 | C3 | 200 | 200 | 24.635 | Expanded Welch | 0 | 1 | 1 | 0.9988 | 0.74361 |
| C3_C3_shape_mismatch_i0p0001_n200 | C3 | 200 | 200 | 24.635 | Normal Wald | 0.00010001 | 0.9999 | 0.9999 | 0.9999 | inf |
| C3_C3_shape_mismatch_i0p0001_n200 | C3 | 200 | 200 | 24.635 | Simple Welch | 0.00010001 | 0.9999 | 0.9999 | 0.9999 | 260.96 |
| C3_C3_shape_mismatch_i0p0001_n500 | C3 | 500 | 500 | 61.589 | Expanded Welch | 0 | 1 | 1 | 0.999 | 0.77825 |
| C3_C3_shape_mismatch_i0p0001_n500 | C3 | 500 | 500 | 61.589 | Normal Wald | 0.0004 | 0.9996 | 0.9996 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n500 | C3 | 500 | 500 | 61.589 | Simple Welch | 0.0004 | 0.9996 | 0.9996 | 1 | 672.6 |
| C3_C3_shape_mismatch_i0p0001_n1000 | C3 | 1000 | 1000 | 123.18 | Expanded Welch | 0 | 1 | 1 | 0.9994 | 0.85632 |
| C3_C3_shape_mismatch_i0p0001_n1000 | C3 | 1000 | 1000 | 123.18 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p0001_n1000 | C3 | 1000 | 1000 | 123.18 | Simple Welch | 0 | 1 | 1 | 1 | 1333.9 |

No row is averaged with another population pair or sample-size setting.
