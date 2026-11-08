# C3_same_balanced_i0p01: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0.01`, Q = `0.01` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.28529628513674743, 0.21470371486325257], [0.21470371486325257, 0.28529628513674743]]`.
- Q probabilities: `[[0.28529628513674743, 0.21470371486325257], [0.21470371486325257, 0.28529628513674743]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p01_n20 | C3 | 20 | 20 | 4.2941 | Expanded Welch | 0.0061224 | 0.99388 | 0.99388 | 0.98 | 1.4038 |
| C3_C3_same_balanced_i0p01_n20 | C3 | 20 | 20 | 4.2941 | Normal Wald | 0.022177 | 0.97782 | 0.97782 | 0.992 | inf |
| C3_C3_same_balanced_i0p01_n20 | C3 | 20 | 20 | 4.2941 | Simple Welch | 0.014113 | 0.98589 | 0.98589 | 0.992 | 27.311 |
| C3_C3_same_balanced_i0p01_n50 | C3 | 50 | 50 | 10.735 | Expanded Welch | 0.0020243 | 0.99798 | 0.99798 | 0.988 | 1.7407 |
| C3_C3_same_balanced_i0p01_n50 | C3 | 50 | 50 | 10.735 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_same_balanced_i0p01_n50 | C3 | 50 | 50 | 10.735 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 68.295 |
| C3_C3_same_balanced_i0p01_n100 | C3 | 100 | 100 | 21.47 | Expanded Welch | 0.004 | 0.996 | 0.996 | 1 | 2.9143 |
| C3_C3_same_balanced_i0p01_n100 | C3 | 100 | 100 | 21.47 | Normal Wald | 0.006 | 0.994 | 0.994 | 1 | inf |
| C3_C3_same_balanced_i0p01_n100 | C3 | 100 | 100 | 21.47 | Simple Welch | 0.004 | 0.996 | 0.996 | 1 | 153.22 |
| C3_C3_same_balanced_i0p01_n200 | C3 | 200 | 200 | 42.941 | Expanded Welch | 0.008 | 0.992 | 0.992 | 1 | 4.6416 |
| C3_C3_same_balanced_i0p01_n200 | C3 | 200 | 200 | 42.941 | Normal Wald | 0.02 | 0.98 | 0.98 | 1 | inf |
| C3_C3_same_balanced_i0p01_n200 | C3 | 200 | 200 | 42.941 | Simple Welch | 0.02 | 0.98 | 0.98 | 1 | 330.59 |
| C3_C3_same_balanced_i0p01_n500 | C3 | 500 | 500 | 107.35 | Expanded Welch | 0.016 | 0.984 | 0.984 | 1 | 11.219 |
| C3_C3_same_balanced_i0p01_n500 | C3 | 500 | 500 | 107.35 | Normal Wald | 0.03 | 0.97 | 0.97 | 1 | inf |
| C3_C3_same_balanced_i0p01_n500 | C3 | 500 | 500 | 107.35 | Simple Welch | 0.03 | 0.97 | 0.97 | 1 | 920.77 |
| C3_C3_same_balanced_i0p01_n1000 | C3 | 1000 | 1000 | 214.7 | Expanded Welch | 0.026 | 0.974 | 0.974 | 1 | 21.35 |
| C3_C3_same_balanced_i0p01_n1000 | C3 | 1000 | 1000 | 214.7 | Normal Wald | 0.032 | 0.968 | 0.968 | 1 | inf |
| C3_C3_same_balanced_i0p01_n1000 | C3 | 1000 | 1000 | 214.7 | Simple Welch | 0.032 | 0.968 | 0.968 | 1 | 1920.6 |

No row is averaged with another population pair or sample-size setting.
