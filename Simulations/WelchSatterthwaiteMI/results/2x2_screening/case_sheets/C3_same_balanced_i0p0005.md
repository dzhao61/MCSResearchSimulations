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
| C3_C3_same_balanced_i0p0005_n20 | C3 | 20 | 20 | 4.8419 | Expanded Welch | 0.0049251 | 0.99507 | 0.99507 | 0.9746 | 0.92935 |
| C3_C3_same_balanced_i0p0005_n20 | C3 | 20 | 20 | 4.8419 | Normal Wald | 0.0098305 | 0.99017 | 0.99017 | 0.9969 | inf |
| C3_C3_same_balanced_i0p0005_n20 | C3 | 20 | 20 | 4.8419 | Simple Welch | 0.0085264 | 0.99147 | 0.99147 | 0.9969 | 25.615 |
| C3_C3_same_balanced_i0p0005_n50 | C3 | 50 | 50 | 12.105 | Expanded Welch | 0.00010157 | 0.9999 | 0.9999 | 0.9845 | 0.76409 |
| C3_C3_same_balanced_i0p0005_n50 | C3 | 50 | 50 | 12.105 | Normal Wald | 0.00020002 | 0.9998 | 0.9998 | 0.9999 | inf |
| C3_C3_same_balanced_i0p0005_n50 | C3 | 50 | 50 | 12.105 | Simple Welch | 0.00020002 | 0.9998 | 0.9998 | 0.9999 | 65.347 |
| C3_C3_same_balanced_i0p0005_n100 | C3 | 100 | 100 | 24.209 | Expanded Welch | 0 | 1 | 1 | 0.9907 | 0.8044 |
| C3_C3_same_balanced_i0p0005_n100 | C3 | 100 | 100 | 24.209 | Normal Wald | 0.00040004 | 0.9996 | 0.9996 | 0.9999 | inf |
| C3_C3_same_balanced_i0p0005_n100 | C3 | 100 | 100 | 24.209 | Simple Welch | 0.00030003 | 0.9997 | 0.9997 | 0.9999 | 131.82 |
| C3_C3_same_balanced_i0p0005_n200 | C3 | 200 | 200 | 48.419 | Expanded Welch | 0.00010041 | 0.9999 | 0.9999 | 0.9959 | 0.85555 |
| C3_C3_same_balanced_i0p0005_n200 | C3 | 200 | 200 | 48.419 | Normal Wald | 0.00040008 | 0.9996 | 0.9996 | 0.9998 | inf |
| C3_C3_same_balanced_i0p0005_n200 | C3 | 200 | 200 | 48.419 | Simple Welch | 0.00040008 | 0.9996 | 0.9996 | 0.9998 | 267.46 |
| C3_C3_same_balanced_i0p0005_n500 | C3 | 500 | 500 | 121.05 | Expanded Welch | 0 | 1 | 1 | 0.9986 | 1.08 |
| C3_C3_same_balanced_i0p0005_n500 | C3 | 500 | 500 | 121.05 | Normal Wald | 0.001 | 0.999 | 0.999 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n500 | C3 | 500 | 500 | 121.05 | Simple Welch | 0.001 | 0.999 | 0.999 | 1 | 671.41 |
| C3_C3_same_balanced_i0p0005_n1000 | C3 | 1000 | 1000 | 242.09 | Expanded Welch | 0.0005003 | 0.9995 | 0.9995 | 0.9994 | 1.5839 |
| C3_C3_same_balanced_i0p0005_n1000 | C3 | 1000 | 1000 | 242.09 | Normal Wald | 0.0017 | 0.9983 | 0.9983 | 1 | inf |
| C3_C3_same_balanced_i0p0005_n1000 | C3 | 1000 | 1000 | 242.09 | Simple Welch | 0.0017 | 0.9983 | 0.9983 | 1 | 1387.2 |

No row is averaged with another population pair or sample-size setting.
