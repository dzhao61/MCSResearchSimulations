# C3_shape_mismatch_i0p001: Near-zero MI with different margins

## Population tables

- True MI: P = `0.001`, Q = `0.001` nats.
- P margins: `(0.5, 0.5)`.
- Q margins: `(0.3, 0.4)`.
- P probabilities: `[[0.2611784760935585, 0.23882152390644149], [0.23882152390644149, 0.2611784760935585]]`.
- Q probabilities: `[[0.4300633642171996, 0.26993663578280036], [0.1699366357828004, 0.13006336421719958]]`.

## Configuration-level results at alpha = 0.05

| configuration_id | experiment | n_p | n_q | minimum_expected_either | method_label | false_positive_rate_05 | true_negative_rate_05 | coverage_95_valid | valid_rate | median_degrees_of_freedom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_C3_shape_mismatch_i0p001_n20 | C3 | 20 | 20 | 2.6013 | Expanded Welch | 0.0060852 | 0.99391 | 0.99391 | 0.986 | 0.97301 |
| C3_C3_shape_mismatch_i0p001_n20 | C3 | 20 | 20 | 2.6013 | Normal Wald | 0.022088 | 0.97791 | 0.97791 | 0.996 | inf |
| C3_C3_shape_mismatch_i0p001_n20 | C3 | 20 | 20 | 2.6013 | Simple Welch | 0.018072 | 0.98193 | 0.98193 | 0.996 | 26.21 |
| C3_C3_shape_mismatch_i0p001_n50 | C3 | 50 | 50 | 6.5032 | Expanded Welch | 0 | 1 | 1 | 0.994 | 0.8273 |
| C3_C3_shape_mismatch_i0p001_n50 | C3 | 50 | 50 | 6.5032 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n50 | C3 | 50 | 50 | 6.5032 | Simple Welch | 0 | 1 | 1 | 1 | 63.68 |
| C3_C3_shape_mismatch_i0p001_n100 | C3 | 100 | 100 | 13.006 | Expanded Welch | 0 | 1 | 1 | 0.996 | 0.93226 |
| C3_C3_shape_mismatch_i0p001_n100 | C3 | 100 | 100 | 13.006 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n100 | C3 | 100 | 100 | 13.006 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 134.39 |
| C3_C3_shape_mismatch_i0p001_n200 | C3 | 200 | 200 | 26.013 | Expanded Welch | 0 | 1 | 1 | 1 | 0.89682 |
| C3_C3_shape_mismatch_i0p001_n200 | C3 | 200 | 200 | 26.013 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n200 | C3 | 200 | 200 | 26.013 | Simple Welch | 0 | 1 | 1 | 1 | 275.79 |
| C3_C3_shape_mismatch_i0p001_n500 | C3 | 500 | 500 | 65.032 | Expanded Welch | 0 | 1 | 1 | 1 | 1.6094 |
| C3_C3_shape_mismatch_i0p001_n500 | C3 | 500 | 500 | 65.032 | Normal Wald | 0 | 1 | 1 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n500 | C3 | 500 | 500 | 65.032 | Simple Welch | 0 | 1 | 1 | 1 | 707.98 |
| C3_C3_shape_mismatch_i0p001_n1000 | C3 | 1000 | 1000 | 130.06 | Expanded Welch | 0 | 1 | 1 | 1 | 2.4518 |
| C3_C3_shape_mismatch_i0p001_n1000 | C3 | 1000 | 1000 | 130.06 | Normal Wald | 0.002 | 0.998 | 0.998 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n1000 | C3 | 1000 | 1000 | 130.06 | Simple Welch | 0.002 | 0.998 | 0.998 | 1 | 1513 |

No row is averaged with another population pair or sample-size setting.
