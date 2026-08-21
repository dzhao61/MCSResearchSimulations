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
| C3_C3_same_balanced_i0p1_n20 | C3 | 20 | 20 | 2.8021 | Expanded Welch | 0.054217 | 0.94578 | 0.94578 | 0.996 | 8.7917 |
| C3_C3_same_balanced_i0p1_n20 | C3 | 20 | 20 | 2.8021 | Normal Wald | 0.06 | 0.94 | 0.94 | 1 | inf |
| C3_C3_same_balanced_i0p1_n20 | C3 | 20 | 20 | 2.8021 | Simple Welch | 0.054 | 0.946 | 0.946 | 1 | 33.676 |
| C3_C3_same_balanced_i0p1_n50 | C3 | 50 | 50 | 7.0051 | Expanded Welch | 0.048 | 0.952 | 0.952 | 1 | 15.328 |
| C3_C3_same_balanced_i0p1_n50 | C3 | 50 | 50 | 7.0051 | Normal Wald | 0.06 | 0.94 | 0.94 | 1 | inf |
| C3_C3_same_balanced_i0p1_n50 | C3 | 50 | 50 | 7.0051 | Simple Welch | 0.056 | 0.944 | 0.944 | 1 | 91.702 |
| C3_C3_same_balanced_i0p1_n100 | C3 | 100 | 100 | 14.01 | Expanded Welch | 0.04 | 0.96 | 0.96 | 1 | 31.603 |
| C3_C3_same_balanced_i0p1_n100 | C3 | 100 | 100 | 14.01 | Normal Wald | 0.048 | 0.952 | 0.952 | 1 | inf |
| C3_C3_same_balanced_i0p1_n100 | C3 | 100 | 100 | 14.01 | Simple Welch | 0.044 | 0.956 | 0.956 | 1 | 192.55 |
| C3_C3_same_balanced_i0p1_n200 | C3 | 200 | 200 | 28.021 | Expanded Welch | 0.034 | 0.966 | 0.966 | 1 | 60.644 |
| C3_C3_same_balanced_i0p1_n200 | C3 | 200 | 200 | 28.021 | Normal Wald | 0.042 | 0.958 | 0.958 | 1 | inf |
| C3_C3_same_balanced_i0p1_n200 | C3 | 200 | 200 | 28.021 | Simple Welch | 0.042 | 0.958 | 0.958 | 1 | 393.16 |
| C3_C3_same_balanced_i0p1_n500 | C3 | 500 | 500 | 70.051 | Expanded Welch | 0.04 | 0.96 | 0.96 | 1 | 142.59 |
| C3_C3_same_balanced_i0p1_n500 | C3 | 500 | 500 | 70.051 | Normal Wald | 0.042 | 0.958 | 0.958 | 1 | inf |
| C3_C3_same_balanced_i0p1_n500 | C3 | 500 | 500 | 70.051 | Simple Welch | 0.042 | 0.958 | 0.958 | 1 | 991.89 |
| C3_C3_same_balanced_i0p1_n1000 | C3 | 1000 | 1000 | 140.1 | Expanded Welch | 0.042 | 0.958 | 0.958 | 1 | 287.12 |
| C3_C3_same_balanced_i0p1_n1000 | C3 | 1000 | 1000 | 140.1 | Normal Wald | 0.044 | 0.956 | 0.956 | 1 | inf |
| C3_C3_same_balanced_i0p1_n1000 | C3 | 1000 | 1000 | 140.1 | Simple Welch | 0.044 | 0.956 | 0.956 | 1 | 1991.4 |

No row is averaged with another population pair or sample-size setting.
