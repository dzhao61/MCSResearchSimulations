# C3_same_balanced_i0p0005: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0.0005`, Q = `0.0005` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.25790503527118464, 0.24209496472881536], [0.24209496472881536, 0.25790503527118464]]`.
- Q probabilities: `[[0.25790503527118464, 0.24209496472881536], [0.24209496472881536, 0.25790503527118464]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p0005_n20 | C3 | 20 | 20 | 4.8419 | Expanded Welch | 0.0061728 | 0.99383 | 0.99383 | 0.972 | 0.94808 |
| C3_C3_same_balanced_i0p0005_n20 | C3 | 20 | 20 | 4.8419 | Normal Wald | 0.016 | 0.984 | 0.984 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n20 | C3 | 20 | 20 | 4.8419 | Simple Welch | 0.012 | 0.988 | 0.988 | 1 | 25.56 |
| C3_C3_same_balanced_i0p0005_n50 | C3 | 50 | 50 | 12.105 | Expanded Welch | 0 | 1 | 1 | 0.99 | 0.73912 |
| C3_C3_same_balanced_i0p0005_n50 | C3 | 50 | 50 | 12.105 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n50 | C3 | 50 | 50 | 12.105 | Simple Welch | 0 | 1 | 1 | 1 | 66.504 |
| C3_C3_same_balanced_i0p0005_n100 | C3 | 100 | 100 | 24.209 | Expanded Welch | 0 | 1 | 1 | 0.99 | 0.77838 |
| C3_C3_same_balanced_i0p0005_n100 | C3 | 100 | 100 | 24.209 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n100 | C3 | 100 | 100 | 24.209 | Simple Welch | 0 | 1 | 1 | 1 | 125.89 |
| C3_C3_same_balanced_i0p0005_n200 | C3 | 200 | 200 | 48.419 | Expanded Welch | 0.0020243 | 0.99798 | 0.99798 | 0.988 | 0.85155 |
| C3_C3_same_balanced_i0p0005_n200 | C3 | 200 | 200 | 48.419 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n200 | C3 | 200 | 200 | 48.419 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 265.24 |
| C3_C3_same_balanced_i0p0005_n500 | C3 | 500 | 500 | 121.05 | Expanded Welch | 0 | 1 | 1 | 1 | 1.0705 |
| C3_C3_same_balanced_i0p0005_n500 | C3 | 500 | 500 | 121.05 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n500 | C3 | 500 | 500 | 121.05 | Simple Welch | 0 | 1 | 1 | 1 | 656.64 |
| C3_C3_same_balanced_i0p0005_n1000 | C3 | 1000 | 1000 | 242.09 | Expanded Welch | 0 | 1 | 1 | 1 | 1.6292 |
| C3_C3_same_balanced_i0p0005_n1000 | C3 | 1000 | 1000 | 242.09 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n1000 | C3 | 1000 | 1000 | 242.09 | Simple Welch | 0 | 1 | 1 | 1 | 1379.7 |

No row is averaged with another population pair or sample-size setting.
