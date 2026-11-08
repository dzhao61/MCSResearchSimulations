# C3_same_balanced_i0p1: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0.1`, Q = `0.1` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.3598973130807049, 0.14010268691929512], [0.14010268691929512, 0.3598973130807049]]`.
- Q probabilities: `[[0.3598973130807049, 0.14010268691929512], [0.14010268691929512, 0.3598973130807049]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p1_n20 | C3 | 20 | 20 | 2.8021 | Expanded Welch | 0.061464 | 0.93854 | 0.93854 | 0.9957 | 8.261 |
| C3_C3_same_balanced_i0p1_n20 | C3 | 20 | 20 | 2.8021 | Normal Wald | 0.078708 | 0.92129 | 0.92129 | 0.9999 | inf |
| C3_C3_same_balanced_i0p1_n20 | C3 | 20 | 20 | 2.8021 | Simple Welch | 0.070707 | 0.92929 | 0.92929 | 0.9999 | 33.734 |
| C3_C3_same_balanced_i0p1_n50 | C3 | 50 | 50 | 7.0051 | Expanded Welch | 0.036504 | 0.9635 | 0.9635 | 0.9999 | 16.831 |
| C3_C3_same_balanced_i0p1_n50 | C3 | 50 | 50 | 7.0051 | Normal Wald | 0.0449 | 0.9551 | 0.9551 | 1 | inf |
| C3_C3_same_balanced_i0p1_n50 | C3 | 50 | 50 | 7.0051 | Simple Welch | 0.0415 | 0.9585 | 0.9585 | 1 | 92.357 |
| C3_C3_same_balanced_i0p1_n100 | C3 | 100 | 100 | 14.01 | Expanded Welch | 0.0411 | 0.9589 | 0.9589 | 1 | 31.152 |
| C3_C3_same_balanced_i0p1_n100 | C3 | 100 | 100 | 14.01 | Normal Wald | 0.0472 | 0.9528 | 0.9528 | 1 | inf |
| C3_C3_same_balanced_i0p1_n100 | C3 | 100 | 100 | 14.01 | Simple Welch | 0.0459 | 0.9541 | 0.9541 | 1 | 192.08 |
| C3_C3_same_balanced_i0p1_n200 | C3 | 200 | 200 | 28.021 | Expanded Welch | 0.0483 | 0.9517 | 0.9517 | 1 | 59.473 |
| C3_C3_same_balanced_i0p1_n200 | C3 | 200 | 200 | 28.021 | Normal Wald | 0.0528 | 0.9472 | 0.9472 | 1 | inf |
| C3_C3_same_balanced_i0p1_n200 | C3 | 200 | 200 | 28.021 | Simple Welch | 0.052 | 0.948 | 0.948 | 1 | 391.54 |
| C3_C3_same_balanced_i0p1_n500 | C3 | 500 | 500 | 70.051 | Expanded Welch | 0.0463 | 0.9537 | 0.9537 | 1 | 145.56 |
| C3_C3_same_balanced_i0p1_n500 | C3 | 500 | 500 | 70.051 | Normal Wald | 0.0484 | 0.9516 | 0.9516 | 1 | inf |
| C3_C3_same_balanced_i0p1_n500 | C3 | 500 | 500 | 70.051 | Simple Welch | 0.0481 | 0.9519 | 0.9519 | 1 | 991.77 |
| C3_C3_same_balanced_i0p1_n1000 | C3 | 1000 | 1000 | 140.1 | Expanded Welch | 0.0533 | 0.9467 | 0.9467 | 1 | 288.41 |
| C3_C3_same_balanced_i0p1_n1000 | C3 | 1000 | 1000 | 140.1 | Normal Wald | 0.0545 | 0.9455 | 0.9455 | 1 | inf |
| C3_C3_same_balanced_i0p1_n1000 | C3 | 1000 | 1000 | 140.1 | Simple Welch | 0.0545 | 0.9455 | 0.9455 | 1 | 1991.7 |

No row is averaged with another population pair or sample-size setting.
