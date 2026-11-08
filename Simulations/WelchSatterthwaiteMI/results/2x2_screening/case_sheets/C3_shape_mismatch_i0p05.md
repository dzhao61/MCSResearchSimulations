# C3_shape_mismatch_i0p05: Near-zero MI with different margins

## Population tables

- True MI: P = `0.05`, Q = `0.05` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.32839079918248304, 0.17160920081751696], [0.17160920081751696, 0.32839079918248304]]`.
- Q probabilities: `[[0.4912371977070939, 0.20876280229290606], [0.1087628022929061, 0.1912371977070939]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p05_n20 | C3 | 20 | 20 | 2.1753 | Expanded Welch | 0.037331 | 0.96267 | 0.96267 | 0.9938 | 3.908 |
| C3_C3_shape_mismatch_i0p05_n20 | C3 | 20 | 20 | 2.1753 | Normal Wald | 0.054527 | 0.94547 | 0.94547 | 0.9995 | inf |
| C3_C3_shape_mismatch_i0p05_n20 | C3 | 20 | 20 | 2.1753 | Simple Welch | 0.046723 | 0.95328 | 0.95328 | 0.9995 | 29.393 |
| C3_C3_shape_mismatch_i0p05_n50 | C3 | 50 | 50 | 5.4381 | Expanded Welch | 0.017221 | 0.98278 | 0.98278 | 0.9988 | 7.0768 |
| C3_C3_shape_mismatch_i0p05_n50 | C3 | 50 | 50 | 5.4381 | Normal Wald | 0.024 | 0.976 | 0.976 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n50 | C3 | 50 | 50 | 5.4381 | Simple Welch | 0.0214 | 0.9786 | 0.9786 | 1 | 85.105 |
| C3_C3_shape_mismatch_i0p05_n100 | C3 | 100 | 100 | 10.876 | Expanded Welch | 0.0248 | 0.9752 | 0.9752 | 1 | 12.879 |
| C3_C3_shape_mismatch_i0p05_n100 | C3 | 100 | 100 | 10.876 | Normal Wald | 0.037 | 0.963 | 0.963 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n100 | C3 | 100 | 100 | 10.876 | Simple Welch | 0.0347 | 0.9653 | 0.9653 | 1 | 184.3 |
| C3_C3_shape_mismatch_i0p05_n200 | C3 | 200 | 200 | 21.753 | Expanded Welch | 0.0357 | 0.9643 | 0.9643 | 1 | 24.46 |
| C3_C3_shape_mismatch_i0p05_n200 | C3 | 200 | 200 | 21.753 | Normal Wald | 0.0438 | 0.9562 | 0.9562 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n200 | C3 | 200 | 200 | 21.753 | Simple Welch | 0.0429 | 0.9571 | 0.9571 | 1 | 383 |
| C3_C3_shape_mismatch_i0p05_n500 | C3 | 500 | 500 | 54.381 | Expanded Welch | 0.0483 | 0.9517 | 0.9517 | 1 | 59.706 |
| C3_C3_shape_mismatch_i0p05_n500 | C3 | 500 | 500 | 54.381 | Normal Wald | 0.0519 | 0.9481 | 0.9481 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n500 | C3 | 500 | 500 | 54.381 | Simple Welch | 0.0515 | 0.9485 | 0.9485 | 1 | 982.33 |
| C3_C3_shape_mismatch_i0p05_n1000 | C3 | 1000 | 1000 | 108.76 | Expanded Welch | 0.0477 | 0.9523 | 0.9523 | 1 | 118.07 |
| C3_C3_shape_mismatch_i0p05_n1000 | C3 | 1000 | 1000 | 108.76 | Normal Wald | 0.0504 | 0.9496 | 0.9496 | 1 | inf |
| C3_C3_shape_mismatch_i0p05_n1000 | C3 | 1000 | 1000 | 108.76 | Simple Welch | 0.0502 | 0.9498 | 0.9498 | 1 | 1982.4 |

No row is averaged with another population pair or sample-size setting.
