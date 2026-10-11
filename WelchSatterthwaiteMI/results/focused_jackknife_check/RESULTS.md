# Focused Jackknife Diagnostic

Original standard errors and normal-distribution cutoffs are unchanged.
The jackknife replaces the analytic correction; negative estimates are retained.
All rates use all 20,000 repetitions. Direction is undefined under equal MI.

| n | True difference | Correction | Difference bias | Observed SD | SE variance ratio | Rejection | Correct-direction rejection | Opposite-direction rejection |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 0.00 | Analytic | 0.02960 | 0.01449 | 1.942 | 0.2522 | N/A | N/A |
| 1,000 | 0.00 | Jackknife | -0.00116 | 0.01521 | 1.762 | 0.0084 | N/A | N/A |
| 1,000 | -0.01 | Analytic | 0.03061 | 0.01564 | 1.811 | 0.1005 | 0.0001 | 0.1004 |
| 1,000 | -0.01 | Jackknife | -0.00024 | 0.01638 | 1.652 | 0.0274 | 0.0272 | 0.0003 |
| 10,000 | 0.00 | Analytic | -0.00088 | 0.00387 | 1.073 | 0.0462 | N/A | N/A |
| 10,000 | 0.00 | Jackknife | -0.00045 | 0.00401 | 1.001 | 0.0507 | N/A | N/A |
| 10,000 | -0.01 | Analytic | -0.00094 | 0.00433 | 1.053 | 0.6992 | 0.6992 | 0.0000 |
| 10,000 | -0.01 | Jackknife | -0.00057 | 0.00447 | 0.991 | 0.6619 | 0.6619 | 0.0000 |

## Paired Changes

Intervals below quantify Monte Carlo uncertainty, not uncertainty for one observed dataset.

- n=1,000, true difference=0.00: bias change -0.03075 [-0.03087, -0.03064]; rejection-rate change -0.2437 [-0.2499, -0.2376].
- n=1,000, true difference=-0.01: bias change -0.03085 [-0.03096, -0.03074]; rejection-rate change -0.0731 [-0.0779, -0.0682].
- n=10,000, true difference=0.00: bias change 0.00043 [0.00042, 0.00044]; rejection-rate change 0.0044 [0.0028, 0.0061].
- n=10,000, true difference=-0.01: bias change 0.00037 [0.00037, 0.00038]; rejection-rate change -0.0373 [-0.0403, -0.0343].

These fixed-standard-error results are a diagnostic. Check the standard-error
variance ratio before treating the changed numerator as a calibrated test.
