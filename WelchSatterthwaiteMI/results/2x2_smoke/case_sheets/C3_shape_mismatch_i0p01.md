# C3_shape_mismatch_i0p01: Near-zero MI with different margins

## Population tables

- True MI: P = `0.01`, Q = `0.01` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.28529628513674743, 0.21470371486325257], [0.21470371486325257, 0.28529628513674743]]`.
- Q probabilities: `[[0.4519159556072204, 0.24808404439277953], [0.14808404439277956, 0.15191595560722043]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p01_n20 | C3 | 20 | 20 | 2.9617 | Expanded Welch | 0.0060484 | 0.99395 | 0.99395 | 0.992 | 1.245 |
| C3_C3_shape_mismatch_i0p01_n20 | C3 | 20 | 20 | 2.9617 | Normal Wald | 0.014028 | 0.98597 | 0.98597 | 0.998 | inf |
| C3_C3_shape_mismatch_i0p01_n20 | C3 | 20 | 20 | 2.9617 | Simple Welch | 0.008016 | 0.99198 | 0.99198 | 0.998 | 26.09 |
| C3_C3_shape_mismatch_i0p01_n50 | C3 | 50 | 50 | 7.4042 | Expanded Welch | 0.002008 | 0.99799 | 0.99799 | 0.996 | 1.6859 |
| C3_C3_shape_mismatch_i0p01_n50 | C3 | 50 | 50 | 7.4042 | Normal Wald | 0.004 | 0.996 | 0.996 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n50 | C3 | 50 | 50 | 7.4042 | Simple Welch | 0.004 | 0.996 | 0.996 | 1 | 69.638 |
| C3_C3_shape_mismatch_i0p01_n100 | C3 | 100 | 100 | 14.808 | Expanded Welch | 0.006012 | 0.99399 | 0.99399 | 0.998 | 2.7042 |
| C3_C3_shape_mismatch_i0p01_n100 | C3 | 100 | 100 | 14.808 | Normal Wald | 0.014 | 0.986 | 0.986 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n100 | C3 | 100 | 100 | 14.808 | Simple Welch | 0.014 | 0.986 | 0.986 | 1 | 147.06 |
| C3_C3_shape_mismatch_i0p01_n200 | C3 | 200 | 200 | 29.617 | Expanded Welch | 0.004 | 0.996 | 0.996 | 1 | 4.9332 |
| C3_C3_shape_mismatch_i0p01_n200 | C3 | 200 | 200 | 29.617 | Normal Wald | 0.012 | 0.988 | 0.988 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n200 | C3 | 200 | 200 | 29.617 | Simple Welch | 0.012 | 0.988 | 0.988 | 1 | 333.08 |
| C3_C3_shape_mismatch_i0p01_n500 | C3 | 500 | 500 | 74.042 | Expanded Welch | 0.03 | 0.97 | 0.97 | 1 | 10.468 |
| C3_C3_shape_mismatch_i0p01_n500 | C3 | 500 | 500 | 74.042 | Normal Wald | 0.042 | 0.958 | 0.958 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n500 | C3 | 500 | 500 | 74.042 | Simple Welch | 0.04 | 0.96 | 0.96 | 1 | 920.91 |
| C3_C3_shape_mismatch_i0p01_n1000 | C3 | 1000 | 1000 | 148.08 | Expanded Welch | 0.028 | 0.972 | 0.972 | 1 | 20.748 |
| C3_C3_shape_mismatch_i0p01_n1000 | C3 | 1000 | 1000 | 148.08 | Normal Wald | 0.034 | 0.966 | 0.966 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n1000 | C3 | 1000 | 1000 | 148.08 | Simple Welch | 0.034 | 0.966 | 0.966 | 1 | 1912.1 |

No row is averaged with another population pair or sample-size setting.
