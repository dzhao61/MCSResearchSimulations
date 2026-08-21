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
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Expanded Welch | 0.01388 | 0.98612 | 0.98612 | 1 | 10.695 |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Normal Wald | 0.02698 | 0.97302 | 0.97302 | 1 | inf |
| C3_C3_same_balanced_i0p005_n1000 | C3 | 1000 | 1000 | 225.02 | Simple Welch | 0.0268 | 0.9732 | 0.9732 | 1 | 1838 |

No row is averaged with another population pair or sample-size setting.
