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
| C3_C3_shape_mismatch_i0p001_n20 | C3 | 20 | 20 | 2.6013 | Expanded Welch | 0.006409 | 0.99359 | 0.99359 | 0.983 | 0.96348 |
| C3_C3_shape_mismatch_i0p001_n20 | C3 | 20 | 20 | 2.6013 | Normal Wald | 0.017063 | 0.98294 | 0.98294 | 0.9963 | inf |
| C3_C3_shape_mismatch_i0p001_n20 | C3 | 20 | 20 | 2.6013 | Simple Welch | 0.012647 | 0.98735 | 0.98735 | 0.9963 | 25.898 |
| C3_C3_shape_mismatch_i0p001_n50 | C3 | 50 | 50 | 6.5032 | Expanded Welch | 0.00040375 | 0.9996 | 0.9996 | 0.9907 | 0.8241 |
| C3_C3_shape_mismatch_i0p001_n50 | C3 | 50 | 50 | 6.5032 | Normal Wald | 0.0013003 | 0.9987 | 0.9987 | 0.9998 | inf |
| C3_C3_shape_mismatch_i0p001_n50 | C3 | 50 | 50 | 6.5032 | Simple Welch | 0.0011002 | 0.9989 | 0.9989 | 0.9998 | 65.49 |
| C3_C3_shape_mismatch_i0p001_n100 | C3 | 100 | 100 | 13.006 | Expanded Welch | 0 | 1 | 1 | 0.996 | 0.85338 |
| C3_C3_shape_mismatch_i0p001_n100 | C3 | 100 | 100 | 13.006 | Normal Wald | 0.0005 | 0.9995 | 0.9995 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n100 | C3 | 100 | 100 | 13.006 | Simple Welch | 0.0005 | 0.9995 | 0.9995 | 1 | 133.15 |
| C3_C3_shape_mismatch_i0p001_n200 | C3 | 200 | 200 | 26.013 | Expanded Welch | 0 | 1 | 1 | 0.9975 | 1.0237 |
| C3_C3_shape_mismatch_i0p001_n200 | C3 | 200 | 200 | 26.013 | Normal Wald | 0.0007 | 0.9993 | 0.9993 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n200 | C3 | 200 | 200 | 26.013 | Simple Welch | 0.0006 | 0.9994 | 0.9994 | 1 | 266.02 |
| C3_C3_shape_mismatch_i0p001_n500 | C3 | 500 | 500 | 65.032 | Expanded Welch | 0.00020008 | 0.9998 | 0.9998 | 0.9996 | 1.4973 |
| C3_C3_shape_mismatch_i0p001_n500 | C3 | 500 | 500 | 65.032 | Normal Wald | 0.0008 | 0.9992 | 0.9992 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n500 | C3 | 500 | 500 | 65.032 | Simple Welch | 0.0008 | 0.9992 | 0.9992 | 1 | 689.2 |
| C3_C3_shape_mismatch_i0p001_n1000 | C3 | 1000 | 1000 | 130.06 | Expanded Welch | 0.00090027 | 0.9991 | 0.9991 | 0.9997 | 2.5094 |
| C3_C3_shape_mismatch_i0p001_n1000 | C3 | 1000 | 1000 | 130.06 | Normal Wald | 0.0048 | 0.9952 | 0.9952 | 1 | inf |
| C3_C3_shape_mismatch_i0p001_n1000 | C3 | 1000 | 1000 | 130.06 | Simple Welch | 0.0048 | 0.9952 | 0.9952 | 1 | 1480.4 |

No row is averaged with another population pair or sample-size setting.
