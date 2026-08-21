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
| C3_C3_same_balanced_i0p005_n20 | C3 | 20 | 20 | 4.5004 | Expanded Welch | 0.0072486 | 0.99275 | 0.99275 | 0.9795 | 1.0819 |
| C3_C3_same_balanced_i0p005_n20 | C3 | 20 | 20 | 4.5004 | Normal Wald | 0.014343 | 0.98566 | 0.98566 | 0.997 | inf |
| C3_C3_same_balanced_i0p005_n20 | C3 | 20 | 20 | 4.5004 | Simple Welch | 0.011735 | 0.98826 | 0.98826 | 0.997 | 25.68 |
| C3_C3_same_balanced_i0p005_n50 | C3 | 50 | 50 | 11.251 | Expanded Welch | 0.00060784 | 0.99939 | 0.99939 | 0.9871 | 1.1737 |
| C3_C3_same_balanced_i0p005_n50 | C3 | 50 | 50 | 11.251 | Normal Wald | 0.0016011 | 0.9984 | 0.9984 | 0.9993 | inf |
| C3_C3_same_balanced_i0p005_n50 | C3 | 50 | 50 | 11.251 | Simple Welch | 0.0013009 | 0.9987 | 0.9987 | 0.9993 | 66.063 |
| C3_C3_same_balanced_i0p005_n100 | C3 | 100 | 100 | 22.502 | Expanded Welch | 0.00090425 | 0.9991 | 0.9991 | 0.9953 | 1.6163 |
| C3_C3_same_balanced_i0p005_n100 | C3 | 100 | 100 | 22.502 | Normal Wald | 0.0025003 | 0.9975 | 0.9975 | 0.9999 | inf |
| C3_C3_same_balanced_i0p005_n100 | C3 | 100 | 100 | 22.502 | Simple Welch | 0.0024002 | 0.9976 | 0.9976 | 0.9999 | 136.73 |
| C3_C3_same_balanced_i0p005_n200 | C3 | 200 | 200 | 45.004 | Expanded Welch | 0.0012012 | 0.9988 | 0.9988 | 0.999 | 2.6028 |
| C3_C3_same_balanced_i0p005_n200 | C3 | 200 | 200 | 45.004 | Normal Wald | 0.0054 | 0.9946 | 0.9946 | 1 | inf |
| C3_C3_same_balanced_i0p005_n200 | C3 | 200 | 200 | 45.004 | Simple Welch | 0.0051 | 0.9949 | 0.9949 | 1 | 297.32 |
| C3_C3_same_balanced_i0p005_n500 | C3 | 500 | 500 | 112.51 | Expanded Welch | 0.0065 | 0.9935 | 0.9935 | 1 | 5.6149 |
| C3_C3_same_balanced_i0p005_n500 | C3 | 500 | 500 | 112.51 | Normal Wald | 0.0158 | 0.9842 | 0.9842 | 1 | inf |
| C3_C3_same_balanced_i0p005_n500 | C3 | 500 | 500 | 112.51 | Simple Welch | 0.0155 | 0.9845 | 0.9845 | 1 | 854.57 |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Expanded Welch | 0.0153 | 0.9847 | 0.9847 | 1 | 10.68 |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Normal Wald | 0.0292 | 0.9708 | 0.9708 | 1 | inf |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Simple Welch | 0.029 | 0.971 | 0.971 | 1 | 1834.8 |

No row is averaged with another population pair or sample-size setting.
