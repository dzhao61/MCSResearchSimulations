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
| C3_C3_same_balanced_i0p001_n20 | C3 | 20 | 20 | 4.7764 | Expanded Welch | 0.0066523 | 0.99335 | 0.99335 | 0.9771 | 0.92635 |
| C3_C3_same_balanced_i0p001_n20 | C3 | 20 | 20 | 4.7764 | Normal Wald | 0.013044 | 0.98696 | 0.98696 | 0.9966 | inf |
| C3_C3_same_balanced_i0p001_n20 | C3 | 20 | 20 | 4.7764 | Simple Welch | 0.010636 | 0.98936 | 0.98936 | 0.9966 | 25.361 |
| C3_C3_same_balanced_i0p001_n50 | C3 | 50 | 50 | 11.941 | Expanded Welch | 0.00071016 | 0.99929 | 0.99929 | 0.9857 | 0.86661 |
| C3_C3_same_balanced_i0p001_n50 | C3 | 50 | 50 | 11.941 | Normal Wald | 0.001201 | 0.9988 | 0.9988 | 0.9992 | inf |
| C3_C3_same_balanced_i0p001_n50 | C3 | 50 | 50 | 11.941 | Simple Welch | 0.001201 | 0.9988 | 0.9988 | 0.9992 | 65.794 |
| C3_C3_same_balanced_i0p001_n100 | C3 | 100 | 100 | 23.882 | Expanded Welch | 0.00010088 | 0.9999 | 0.9999 | 0.9913 | 0.90706 |
| C3_C3_same_balanced_i0p001_n100 | C3 | 100 | 100 | 23.882 | Normal Wald | 0.00060012 | 0.9994 | 0.9994 | 0.9998 | inf |
| C3_C3_same_balanced_i0p001_n100 | C3 | 100 | 100 | 23.882 | Simple Welch | 0.0005001 | 0.9995 | 0.9995 | 0.9998 | 131.13 |
| C3_C3_same_balanced_i0p001_n200 | C3 | 200 | 200 | 47.764 | Expanded Welch | 0.00010029 | 0.9999 | 0.9999 | 0.9971 | 1.0111 |
| C3_C3_same_balanced_i0p001_n200 | C3 | 200 | 200 | 47.764 | Normal Wald | 0.0008 | 0.9992 | 0.9992 | 1 | inf |
| C3_C3_same_balanced_i0p001_n200 | C3 | 200 | 200 | 47.764 | Simple Welch | 0.0008 | 0.9992 | 0.9992 | 1 | 266.76 |
| C3_C3_same_balanced_i0p001_n500 | C3 | 500 | 500 | 119.41 | Expanded Welch | 0.0002003 | 0.9998 | 0.9998 | 0.9985 | 1.5764 |
| C3_C3_same_balanced_i0p001_n500 | C3 | 500 | 500 | 119.41 | Normal Wald | 0.00090009 | 0.9991 | 0.9991 | 0.9999 | inf |
| C3_C3_same_balanced_i0p001_n500 | C3 | 500 | 500 | 119.41 | Simple Welch | 0.00080008 | 0.9992 | 0.9992 | 0.9999 | 690.46 |
| C3_C3_same_balanced_i0p001_n1000 | C3 | 1000 | 1000 | 238.82 | Expanded Welch | 0.00080016 | 0.9992 | 0.9992 | 0.9998 | 2.5258 |
| C3_C3_same_balanced_i0p001_n1000 | C3 | 1000 | 1000 | 238.82 | Normal Wald | 0.0042 | 0.9958 | 0.9958 | 1 | inf |
| C3_C3_same_balanced_i0p001_n1000 | C3 | 1000 | 1000 | 238.82 | Simple Welch | 0.0042 | 0.9958 | 0.9958 | 1 | 1482.8 |

No row is averaged with another population pair or sample-size setting.
