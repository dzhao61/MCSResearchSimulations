# C3_same_balanced_i0p0001: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `9.999999999e-05`, Q = `9.999999999e-05` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.2535354749788844, 0.2464645250211156], [0.2464645250211156, 0.2535354749788844]]`.
- Q probabilities: `[[0.2535354749788844, 0.2464645250211156], [0.2464645250211156, 0.2535354749788844]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p0001_n20 | C3 | 20 | 20 | 4.9293 | Expanded Welch | 0.0049125 | 0.99509 | 0.99509 | 0.9771 | 0.86882 |
| C3_C3_same_balanced_i0p0001_n20 | C3 | 20 | 20 | 4.9293 | Normal Wald | 0.0097272 | 0.99027 | 0.99027 | 0.9972 | inf |
| C3_C3_same_balanced_i0p0001_n20 | C3 | 20 | 20 | 4.9293 | Simple Welch | 0.0081227 | 0.99188 | 0.99188 | 0.9972 | 25.315 |
| C3_C3_same_balanced_i0p0001_n50 | C3 | 50 | 50 | 12.323 | Expanded Welch | 0.00010177 | 0.9999 | 0.9999 | 0.9826 | 0.75219 |
| C3_C3_same_balanced_i0p0001_n50 | C3 | 50 | 50 | 12.323 | Normal Wald | 0.00040028 | 0.9996 | 0.9996 | 0.9993 | inf |
| C3_C3_same_balanced_i0p0001_n50 | C3 | 50 | 50 | 12.323 | Simple Welch | 0.00030021 | 0.9997 | 0.9997 | 0.9993 | 65.298 |
| C3_C3_same_balanced_i0p0001_n100 | C3 | 100 | 100 | 24.646 | Expanded Welch | 0.00020149 | 0.9998 | 0.9998 | 0.9926 | 0.72351 |
| C3_C3_same_balanced_i0p0001_n100 | C3 | 100 | 100 | 24.646 | Normal Wald | 0.00020002 | 0.9998 | 0.9998 | 0.9999 | inf |
| C3_C3_same_balanced_i0p0001_n100 | C3 | 100 | 100 | 24.646 | Simple Welch | 0.00020002 | 0.9998 | 0.9998 | 0.9999 | 132.67 |
| C3_C3_same_balanced_i0p0001_n200 | C3 | 200 | 200 | 49.293 | Expanded Welch | 0 | 1 | 1 | 0.9957 | 0.74901 |
| C3_C3_same_balanced_i0p0001_n200 | C3 | 200 | 200 | 49.293 | Normal Wald | 0.0001 | 0.9999 | 0.9999 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n200 | C3 | 200 | 200 | 49.293 | Simple Welch | 0.0001 | 0.9999 | 0.9999 | 1 | 265.1 |
| C3_C3_same_balanced_i0p0001_n500 | C3 | 500 | 500 | 123.23 | Expanded Welch | 0 | 1 | 1 | 0.9982 | 0.78174 |
| C3_C3_same_balanced_i0p0001_n500 | C3 | 500 | 500 | 123.23 | Normal Wald | 0.0001 | 0.9999 | 0.9999 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n500 | C3 | 500 | 500 | 123.23 | Simple Welch | 0.0001 | 0.9999 | 0.9999 | 1 | 666.31 |
| C3_C3_same_balanced_i0p0001_n1000 | C3 | 1000 | 1000 | 246.46 | Expanded Welch | 0 | 1 | 1 | 0.9987 | 0.84418 |
| C3_C3_same_balanced_i0p0001_n1000 | C3 | 1000 | 1000 | 246.46 | Normal Wald | 0.0007 | 0.9993 | 0.9993 | 1 | inf |
| C3_C3_same_balanced_i0p0001_n1000 | C3 | 1000 | 1000 | 246.46 | Simple Welch | 0.0005 | 0.9995 | 0.9995 | 1 | 1328.3 |

No row is averaged with another population pair or sample-size setting.
