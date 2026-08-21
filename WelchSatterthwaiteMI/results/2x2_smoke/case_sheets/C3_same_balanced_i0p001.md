# C3_same_balanced_i0p001: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0.001`, Q = `0.001` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.2611784760935585, 0.23882152390644149], [0.23882152390644149, 0.2611784760935585]]`.
- Q probabilities: `[[0.2611784760935585, 0.23882152390644149], [0.23882152390644149, 0.2611784760935585]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p001_n20 | C3 | 20 | 20 | 4.7764 | Expanded Welch | 0.0040486 | 0.99595 | 0.99595 | 0.988 | 0.94039 |
| C3_C3_same_balanced_i0p001_n20 | C3 | 20 | 20 | 4.7764 | Normal Wald | 0.01002 | 0.98998 | 0.98998 | 0.998 | inf |
| C3_C3_same_balanced_i0p001_n20 | C3 | 20 | 20 | 4.7764 | Simple Welch | 0.008016 | 0.99198 | 0.99198 | 0.998 | 25.907 |
| C3_C3_same_balanced_i0p001_n50 | C3 | 50 | 50 | 11.941 | Expanded Welch | 0 | 1 | 1 | 0.988 | 0.89238 |
| C3_C3_same_balanced_i0p001_n50 | C3 | 50 | 50 | 11.941 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p001_n50 | C3 | 50 | 50 | 11.941 | Simple Welch | 0 | 1 | 1 | 1 | 65.237 |
| C3_C3_same_balanced_i0p001_n100 | C3 | 100 | 100 | 23.882 | Expanded Welch | 0 | 1 | 1 | 0.992 | 0.92622 |
| C3_C3_same_balanced_i0p001_n100 | C3 | 100 | 100 | 23.882 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p001_n100 | C3 | 100 | 100 | 23.882 | Simple Welch | 0 | 1 | 1 | 1 | 130.7 |
| C3_C3_same_balanced_i0p001_n200 | C3 | 200 | 200 | 47.764 | Expanded Welch | 0 | 1 | 1 | 0.996 | 1.0456 |
| C3_C3_same_balanced_i0p001_n200 | C3 | 200 | 200 | 47.764 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_same_balanced_i0p001_n200 | C3 | 200 | 200 | 47.764 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 259.41 |
| C3_C3_same_balanced_i0p001_n500 | C3 | 500 | 500 | 119.41 | Expanded Welch | 0 | 1 | 1 | 1 | 1.4486 |
| C3_C3_same_balanced_i0p001_n500 | C3 | 500 | 500 | 119.41 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_same_balanced_i0p001_n500 | C3 | 500 | 500 | 119.41 | Simple Welch | 0 | 1 | 1 | 1 | 683.25 |
| C3_C3_same_balanced_i0p001_n1000 | C3 | 1000 | 1000 | 238.82 | Expanded Welch | 0 | 1 | 1 | 1 | 2.5421 |
| C3_C3_same_balanced_i0p001_n1000 | C3 | 1000 | 1000 | 238.82 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_same_balanced_i0p001_n1000 | C3 | 1000 | 1000 | 238.82 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 1496.7 |

No row is averaged with another population pair or sample-size setting.
