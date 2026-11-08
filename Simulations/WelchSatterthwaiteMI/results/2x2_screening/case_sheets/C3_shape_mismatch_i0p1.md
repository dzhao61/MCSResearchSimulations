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
| C3_C3_shape_mismatch_i0p1_n20 | C3 | 20 | 20 | 1.6 | Expanded Welch | 0.065778 | 0.93422 | 0.93422 | 0.9973 | 8.2313 |
| C3_C3_shape_mismatch_i0p1_n20 | C3 | 20 | 20 | 1.6 | Normal Wald | 0.0883 | 0.9117 | 0.9117 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n20 | C3 | 20 | 20 | 1.6 | Simple Welch | 0.0774 | 0.9226 | 0.9226 | 1 | 33.968 |
| C3_C3_shape_mismatch_i0p1_n50 | C3 | 50 | 50 | 4.0001 | Expanded Welch | 0.042804 | 0.9572 | 0.9572 | 0.9999 | 17.184 |
| C3_C3_shape_mismatch_i0p1_n50 | C3 | 50 | 50 | 4.0001 | Normal Wald | 0.0531 | 0.9469 | 0.9469 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n50 | C3 | 50 | 50 | 4.0001 | Simple Welch | 0.0489 | 0.9511 | 0.9511 | 1 | 92.686 |
| C3_C3_shape_mismatch_i0p1_n100 | C3 | 100 | 100 | 8.0002 | Expanded Welch | 0.043 | 0.957 | 0.957 | 1 | 31.301 |
| C3_C3_shape_mismatch_i0p1_n100 | C3 | 100 | 100 | 8.0002 | Normal Wald | 0.0507 | 0.9493 | 0.9493 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n100 | C3 | 100 | 100 | 8.0002 | Simple Welch | 0.049 | 0.951 | 0.951 | 1 | 191.94 |
| C3_C3_shape_mismatch_i0p1_n200 | C3 | 200 | 200 | 16 | Expanded Welch | 0.0442 | 0.9558 | 0.9558 | 1 | 59.766 |
| C3_C3_shape_mismatch_i0p1_n200 | C3 | 200 | 200 | 16 | Normal Wald | 0.0491 | 0.9509 | 0.9509 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n200 | C3 | 200 | 200 | 16 | Simple Welch | 0.0486 | 0.9514 | 0.9514 | 1 | 391.76 |
| C3_C3_shape_mismatch_i0p1_n500 | C3 | 500 | 500 | 40.001 | Expanded Welch | 0.0482 | 0.9518 | 0.9518 | 1 | 146.19 |
| C3_C3_shape_mismatch_i0p1_n500 | C3 | 500 | 500 | 40.001 | Normal Wald | 0.0499 | 0.9501 | 0.9501 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n500 | C3 | 500 | 500 | 40.001 | Simple Welch | 0.0493 | 0.9507 | 0.9507 | 1 | 991.49 |
| C3_C3_shape_mismatch_i0p1_n1000 | C3 | 1000 | 1000 | 80.002 | Expanded Welch | 0.0512 | 0.9488 | 0.9488 | 1 | 289.53 |
| C3_C3_shape_mismatch_i0p1_n1000 | C3 | 1000 | 1000 | 80.002 | Normal Wald | 0.0522 | 0.9478 | 0.9478 | 1 | inf |
| C3_C3_shape_mismatch_i0p1_n1000 | C3 | 1000 | 1000 | 80.002 | Simple Welch | 0.052 | 0.948 | 0.948 | 1 | 1992 |

No row is averaged with another population pair or sample-size setting.
