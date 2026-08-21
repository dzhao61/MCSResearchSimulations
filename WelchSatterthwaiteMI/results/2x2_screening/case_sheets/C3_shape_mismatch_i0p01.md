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
| C3_C3_shape_mismatch_i0p01_n20 | C3 | 20 | 20 | 2.9617 | Expanded Welch | 0.012784 | 0.98722 | 0.98722 | 0.9856 | 1.275 |
| C3_C3_shape_mismatch_i0p01_n20 | C3 | 20 | 20 | 2.9617 | Normal Wald | 0.025055 | 0.97494 | 0.97494 | 0.9978 | inf |
| C3_C3_shape_mismatch_i0p01_n20 | C3 | 20 | 20 | 2.9617 | Simple Welch | 0.019643 | 0.98036 | 0.98036 | 0.9978 | 26.358 |
| C3_C3_shape_mismatch_i0p01_n50 | C3 | 50 | 50 | 7.4042 | Expanded Welch | 0.0030163 | 0.99698 | 0.99698 | 0.9946 | 1.6716 |
| C3_C3_shape_mismatch_i0p01_n50 | C3 | 50 | 50 | 7.4042 | Normal Wald | 0.0046014 | 0.9954 | 0.9954 | 0.9997 | inf |
| C3_C3_shape_mismatch_i0p01_n50 | C3 | 50 | 50 | 7.4042 | Simple Welch | 0.0042013 | 0.9958 | 0.9958 | 0.9997 | 68.82 |
| C3_C3_shape_mismatch_i0p01_n100 | C3 | 100 | 100 | 14.808 | Expanded Welch | 0.0019036 | 0.9981 | 0.9981 | 0.9981 | 2.6838 |
| C3_C3_shape_mismatch_i0p01_n100 | C3 | 100 | 100 | 14.808 | Normal Wald | 0.0056 | 0.9944 | 0.9944 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n100 | C3 | 100 | 100 | 14.808 | Simple Welch | 0.005 | 0.995 | 0.995 | 1 | 147.44 |
| C3_C3_shape_mismatch_i0p01_n200 | C3 | 200 | 200 | 29.617 | Expanded Welch | 0.0036011 | 0.9964 | 0.9964 | 0.9997 | 4.6334 |
| C3_C3_shape_mismatch_i0p01_n200 | C3 | 200 | 200 | 29.617 | Normal Wald | 0.0109 | 0.9891 | 0.9891 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n200 | C3 | 200 | 200 | 29.617 | Simple Welch | 0.0104 | 0.9896 | 0.9896 | 1 | 330.98 |
| C3_C3_shape_mismatch_i0p01_n500 | C3 | 500 | 500 | 74.042 | Expanded Welch | 0.0155 | 0.9845 | 0.9845 | 1 | 10.689 |
| C3_C3_shape_mismatch_i0p01_n500 | C3 | 500 | 500 | 74.042 | Normal Wald | 0.0276 | 0.9724 | 0.9724 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n500 | C3 | 500 | 500 | 74.042 | Simple Welch | 0.0274 | 0.9726 | 0.9726 | 1 | 914.93 |
| C3_C3_shape_mismatch_i0p01_n1000 | C3 | 1000 | 1000 | 148.08 | Expanded Welch | 0.0279 | 0.9721 | 0.9721 | 1 | 20.849 |
| C3_C3_shape_mismatch_i0p01_n1000 | C3 | 1000 | 1000 | 148.08 | Normal Wald | 0.0392 | 0.9608 | 0.9608 | 1 | inf |
| C3_C3_shape_mismatch_i0p01_n1000 | C3 | 1000 | 1000 | 148.08 | Simple Welch | 0.0391 | 0.9609 | 0.9609 | 1 | 1913.9 |

No row is averaged with another population pair or sample-size setting.
