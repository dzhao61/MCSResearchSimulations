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
| C3_C3_same_balanced_i0p01_n20 | C3 | 20 | 20 | 4.2941 | Expanded Welch | 0.012632 | 0.98737 | 0.98737 | 0.9816 | 1.274 |
| C3_C3_same_balanced_i0p01_n20 | C3 | 20 | 20 | 4.2941 | Normal Wald | 0.021046 | 0.97895 | 0.97895 | 0.9978 | inf |
| C3_C3_same_balanced_i0p01_n20 | C3 | 20 | 20 | 4.2941 | Simple Welch | 0.017539 | 0.98246 | 0.98246 | 0.9978 | 25.859 |
| C3_C3_same_balanced_i0p01_n50 | C3 | 50 | 50 | 10.735 | Expanded Welch | 0.0016157 | 0.99838 | 0.99838 | 0.9903 | 1.7349 |
| C3_C3_same_balanced_i0p01_n50 | C3 | 50 | 50 | 10.735 | Normal Wald | 0.003401 | 0.9966 | 0.9966 | 0.9997 | inf |
| C3_C3_same_balanced_i0p01_n50 | C3 | 50 | 50 | 10.735 | Simple Welch | 0.0028008 | 0.9972 | 0.9972 | 0.9997 | 68.408 |
| C3_C3_same_balanced_i0p01_n100 | C3 | 100 | 100 | 21.47 | Expanded Welch | 0.001303 | 0.9987 | 0.9987 | 0.9977 | 2.6813 |
| C3_C3_same_balanced_i0p01_n100 | C3 | 100 | 100 | 21.47 | Normal Wald | 0.0049 | 0.9951 | 0.9951 | 1 | inf |
| C3_C3_same_balanced_i0p01_n100 | C3 | 100 | 100 | 21.47 | Simple Welch | 0.0045 | 0.9955 | 0.9955 | 1 | 148.25 |
| C3_C3_same_balanced_i0p01_n200 | C3 | 200 | 200 | 42.941 | Expanded Welch | 0.0054022 | 0.9946 | 0.9946 | 0.9996 | 4.752 |
| C3_C3_same_balanced_i0p01_n200 | C3 | 200 | 200 | 42.941 | Normal Wald | 0.014 | 0.986 | 0.986 | 1 | inf |
| C3_C3_same_balanced_i0p01_n200 | C3 | 200 | 200 | 42.941 | Simple Welch | 0.0136 | 0.9864 | 0.9864 | 1 | 328.27 |
| C3_C3_same_balanced_i0p01_n500 | C3 | 500 | 500 | 107.35 | Expanded Welch | 0.015302 | 0.9847 | 0.9847 | 0.9999 | 10.962 |
| C3_C3_same_balanced_i0p01_n500 | C3 | 500 | 500 | 107.35 | Normal Wald | 0.0295 | 0.9705 | 0.9705 | 1 | inf |
| C3_C3_same_balanced_i0p01_n500 | C3 | 500 | 500 | 107.35 | Simple Welch | 0.0291 | 0.9709 | 0.9709 | 1 | 918.4 |
| C3_C3_same_balanced_i0p01_n1000 | C3 | 1000 | 1000 | 214.7 | Expanded Welch | 0.0287 | 0.9713 | 0.9713 | 1 | 21.315 |
| C3_C3_same_balanced_i0p01_n1000 | C3 | 1000 | 1000 | 214.7 | Normal Wald | 0.0385 | 0.9615 | 0.9615 | 1 | inf |
| C3_C3_same_balanced_i0p01_n1000 | C3 | 1000 | 1000 | 214.7 | Simple Welch | 0.0385 | 0.9615 | 0.9615 | 1 | 1917.5 |

No row is averaged with another population pair or sample-size setting.
