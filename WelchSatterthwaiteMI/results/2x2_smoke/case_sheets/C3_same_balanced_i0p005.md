# C3_same_balanced_i0p005: Near-zero MI with identical balanced margins

## Population tables

- True MI: P = `0.005`, Q = `0.005` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.5, 0.5)`.
- P probabilities: `[[0.2749791440368653, 0.22502085596313473], [0.22502085596313473, 0.2749791440368653]]`.
- Q probabilities: `[[0.2749791440368653, 0.22502085596313473], [0.22502085596313473, 0.2749791440368653]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_same_balanced_i0p005_n20 | C3 | 20 | 20 | 4.5004 | Expanded Welch | 0 | 1 | 1 | 0.974 | 1.0816 |
| C3_C3_same_balanced_i0p005_n20 | C3 | 20 | 20 | 4.5004 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_same_balanced_i0p005_n20 | C3 | 20 | 20 | 4.5004 | Simple Welch | 0 | 1 | 1 | 1 | 25.688 |
| C3_C3_same_balanced_i0p005_n50 | C3 | 50 | 50 | 11.251 | Expanded Welch | 0.0020202 | 0.99798 | 0.99798 | 0.99 | 1.3271 |
| C3_C3_same_balanced_i0p005_n50 | C3 | 50 | 50 | 11.251 | Normal Wald | 0.004008 | 0.99599 | 0.99599 | 0.998 | inf |
| C3_C3_same_balanced_i0p005_n50 | C3 | 50 | 50 | 11.251 | Simple Welch | 0.004008 | 0.99599 | 0.99599 | 0.998 | 64.743 |
| C3_C3_same_balanced_i0p005_n100 | C3 | 100 | 100 | 22.502 | Expanded Welch | 0 | 1 | 1 | 0.998 | 1.7036 |
| C3_C3_same_balanced_i0p005_n100 | C3 | 100 | 100 | 22.502 | Normal Wald | 0.004 | 0.996 | 0.996 | 1 | inf |
| C3_C3_same_balanced_i0p005_n100 | C3 | 100 | 100 | 22.502 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 134.35 |
| C3_C3_same_balanced_i0p005_n200 | C3 | 200 | 200 | 45.004 | Expanded Welch | 0 | 1 | 1 | 1 | 2.6143 |
| C3_C3_same_balanced_i0p005_n200 | C3 | 200 | 200 | 45.004 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_same_balanced_i0p005_n200 | C3 | 200 | 200 | 45.004 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 304.59 |
| C3_C3_same_balanced_i0p005_n500 | C3 | 500 | 500 | 112.51 | Expanded Welch | 0.004 | 0.996 | 0.996 | 1 | 5.6996 |
| C3_C3_same_balanced_i0p005_n500 | C3 | 500 | 500 | 112.51 | Normal Wald | 0.016 | 0.984 | 0.984 | 1 | inf |
| C3_C3_same_balanced_i0p005_n500 | C3 | 500 | 500 | 112.51 | Simple Welch | 0.016 | 0.984 | 0.984 | 1 | 853.82 |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Expanded Welch | 0.01 | 0.99 | 0.99 | 1 | 10.162 |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Normal Wald | 0.024 | 0.976 | 0.976 | 1 | inf |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Simple Welch | 0.024 | 0.976 | 0.976 | 1 | 1817.3 |

No row is averaged with another population pair or sample-size setting.
