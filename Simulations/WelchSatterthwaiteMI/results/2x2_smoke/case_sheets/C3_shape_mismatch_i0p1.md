# C3_shape_mismatch_i0p1: Near-zero MI with different margins

## Population tables

- True MI: P = `0.1`, Q = `0.1` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.3598973130807049, 0.14010268691929512], [0.14010268691929512, 0.3598973130807049]]`.
- Q probabilities: `[[0.5199980234815429, 0.180001976518457], [0.08000197651845703, 0.21999802348154296]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p1_n20 | C3 | 20 | 20 | 1.6 | Expanded Welch | 0.058116 | 0.94188 | 0.94188 | 0.998 | 8.1793 |
| C3_C3_shape_mismatch_i0p1_n20 | C3 | 20 | 20 | 1.6 | Normal Wald | 0.076 | 0.924 | 0.924 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n20 | C3 | 20 | 20 | 1.6 | Simple Welch | 0.068 | 0.932 | 0.932 | 1 | 34.385 |
| C3_C3_shape_mismatch_i0p1_n50 | C3 | 50 | 50 | 4.0001 | Expanded Welch | 0.054 | 0.946 | 0.946 | 1 | 17.504 |
| C3_C3_shape_mismatch_i0p1_n50 | C3 | 50 | 50 | 4.0001 | Normal Wald | 0.068 | 0.932 | 0.932 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n50 | C3 | 50 | 50 | 4.0001 | Simple Welch | 0.062 | 0.938 | 0.938 | 1 | 92.452 |
| C3_C3_shape_mismatch_i0p1_n100 | C3 | 100 | 100 | 8.0002 | Expanded Welch | 0.04 | 0.96 | 0.96 | 1 | 32.435 |
| C3_C3_shape_mismatch_i0p1_n100 | C3 | 100 | 100 | 8.0002 | Normal Wald | 0.05 | 0.95 | 0.95 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n100 | C3 | 100 | 100 | 8.0002 | Simple Welch | 0.05 | 0.95 | 0.95 | 1 | 191.58 |
| C3_C3_shape_mismatch_i0p1_n200 | C3 | 200 | 200 | 16 | Expanded Welch | 0.042 | 0.958 | 0.958 | 1 | 60.437 |
| C3_C3_shape_mismatch_i0p1_n200 | C3 | 200 | 200 | 16 | Normal Wald | 0.042 | 0.958 | 0.958 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n200 | C3 | 200 | 200 | 16 | Simple Welch | 0.042 | 0.958 | 0.958 | 1 | 391.72 |
| C3_C3_shape_mismatch_i0p1_n500 | C3 | 500 | 500 | 40.001 | Expanded Welch | 0.058 | 0.942 | 0.942 | 1 | 141.63 |
| C3_C3_shape_mismatch_i0p1_n500 | C3 | 500 | 500 | 40.001 | Normal Wald | 0.064 | 0.936 | 0.936 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n500 | C3 | 500 | 500 | 40.001 | Simple Welch | 0.064 | 0.936 | 0.936 | 1 | 991.61 |
| C3_C3_shape_mismatch_i0p1_n1000 | C3 | 1000 | 1000 | 80.002 | Expanded Welch | 0.06 | 0.94 | 0.94 | 1 | 291.73 |
| C3_C3_shape_mismatch_i0p1_n1000 | C3 | 1000 | 1000 | 80.002 | Normal Wald | 0.06 | 0.94 | 0.94 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n1000 | C3 | 1000 | 1000 | 80.002 | Simple Welch | 0.06 | 0.94 | 0.94 | 1 | 1991.6 |

No row is averaged with another population pair or sample-size setting.
