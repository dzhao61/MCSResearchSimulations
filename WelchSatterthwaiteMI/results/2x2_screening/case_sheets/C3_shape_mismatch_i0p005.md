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
| C3_C3_shape_mismatch_i0p005_n20 | C3 | 20 | 20 | 2.851 | Expanded Welch | 0.0087381 | 0.99126 | 0.99126 | 0.9842 | 1.0607 |
| C3_C3_shape_mismatch_i0p005_n20 | C3 | 20 | 20 | 2.851 | Normal Wald | 0.018841 | 0.98116 | 0.98116 | 0.9978 | inf |
| C3_C3_shape_mismatch_i0p005_n20 | C3 | 20 | 20 | 2.851 | Simple Welch | 0.015033 | 0.98497 | 0.98497 | 0.9978 | 25.962 |
| C3_C3_shape_mismatch_i0p005_n50 | C3 | 50 | 50 | 7.1274 | Expanded Welch | 0.00090671 | 0.99909 | 0.99909 | 0.9926 | 1.1747 |
| C3_C3_shape_mismatch_i0p005_n50 | C3 | 50 | 50 | 7.1274 | Normal Wald | 0.0023002 | 0.9977 | 0.9977 | 0.9999 | inf |
| C3_C3_shape_mismatch_i0p005_n50 | C3 | 50 | 50 | 7.1274 | Simple Welch | 0.0017002 | 0.9983 | 0.9983 | 0.9999 | 66.025 |
| C3_C3_shape_mismatch_i0p005_n100 | C3 | 100 | 100 | 14.255 | Expanded Welch | 0.0004012 | 0.9996 | 0.9996 | 0.997 | 1.6125 |
| C3_C3_shape_mismatch_i0p005_n100 | C3 | 100 | 100 | 14.255 | Normal Wald | 0.0020002 | 0.998 | 0.998 | 0.9999 | inf |
| C3_C3_shape_mismatch_i0p005_n100 | C3 | 100 | 100 | 14.255 | Simple Welch | 0.0018002 | 0.9982 | 0.9982 | 0.9999 | 136.97 |
| C3_C3_shape_mismatch_i0p005_n200 | C3 | 200 | 200 | 28.51 | Expanded Welch | 0.0011003 | 0.9989 | 0.9989 | 0.9997 | 2.5559 |
| C3_C3_shape_mismatch_i0p005_n200 | C3 | 200 | 200 | 28.51 | Normal Wald | 0.004 | 0.996 | 0.996 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n200 | C3 | 200 | 200 | 28.51 | Simple Welch | 0.0038 | 0.9962 | 0.9962 | 1 | 296.18 |
| C3_C3_shape_mismatch_i0p005_n500 | C3 | 500 | 500 | 71.274 | Expanded Welch | 0.0046014 | 0.9954 | 0.9954 | 0.9997 | 5.5053 |
| C3_C3_shape_mismatch_i0p005_n500 | C3 | 500 | 500 | 71.274 | Normal Wald | 0.0129 | 0.9871 | 0.9871 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n500 | C3 | 500 | 500 | 71.274 | Simple Welch | 0.0126 | 0.9874 | 0.9874 | 1 | 849.29 |
| C3_C3_shape_mismatch_i0p005_n1000 | C3 | 1000 | 1000 | 142.55 | Expanded Welch | 0.015 | 0.985 | 0.985 | 1 | 10.646 |
| C3_C3_shape_mismatch_i0p005_n1000 | C3 | 1000 | 1000 | 142.55 | Normal Wald | 0.0262 | 0.9738 | 0.9738 | 1 | inf |
| C3_C3_shape_mismatch_i0p005_n1000 | C3 | 1000 | 1000 | 142.55 | Simple Welch | 0.0261 | 0.9739 | 0.9739 | 1 | 1843.2 |

No row is averaged with another population pair or sample-size setting.
