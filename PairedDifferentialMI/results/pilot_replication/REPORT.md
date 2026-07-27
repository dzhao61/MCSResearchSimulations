# Paired Differential-MI Feasibility Results

## Decision: **NO-GO IN CURRENT FORM**

The decision applies to the positive-MI paired weak-null direction. Boundary scenarios remain outside the supported scope.

## Regular Positive-MI Calibration

| method | mean_absolute_fpr_error_05 | scenarios_in_035_065 | min_rejection_05 | max_rejection_05 |
| --- | --- | --- | --- | --- |
| paired_wald_normal | 0.0103 | 0.8333 | 0.0217 | 0.0637 |
| paired_wald_t | 0.0115 | 0.7500 | 0.0173 | 0.0627 |
| paired_jackknife_t | 0.0147 | 0.5833 | 0.0090 | 0.0593 |
| unpaired_wald_normal | 0.0333 | 0.3333 | 0.0003 | 0.1190 |

## Sparse Calibration

| method | mean_absolute_fpr_error_05 | scenarios_in_035_065 | min_rejection_05 | max_rejection_05 |
| --- | --- | --- | --- | --- |
| paired_wald_normal | 0.0165 | 0.4000 | 0.0150 | 0.0497 |
| paired_wald_t | 0.0192 | 0.4000 | 0.0112 | 0.0437 |
| paired_jackknife_t | 0.0219 | 0.4000 | 0.0133 | 0.0407 |
| unpaired_wald_normal | 0.0298 | 0.4000 | 0.0000 | 0.0490 |

## Power Controls

| scenario_id | true_delta | paired_wald_normal_reject_05 | paired_wald_t_reject_05 | paired_jackknife_t_reject_05 |
| --- | --- | --- | --- | --- |
| power_2x2_n100 | -0.0500 | 0.1310 | 0.1250 | 0.1015 |
| power_3x3_n150 | -0.0500 | 0.1475 | 0.1425 | 0.1245 |
| power_5x5_n500 | -0.0500 | 0.4805 | 0.4770 | 0.5330 |

## Bootstrap Anchors

- Median deterministic latency: `0.160 ms`.
- Median 999-bootstrap latency: `0.002 s`.
- Median measured speedup: `10.7x`.
- Median absolute jackknife-t versus bootstrap p-value difference: `0.0199`.

## Pre-Specified Rules

- Rule 1, regular calibration: **FAIL**.
- Rule 3, sparse refinement value: **FAIL**.
- Rule 5, runtime: **PASS**.

Rules concerning pairing signs and the boundary are interpreted from the scenario-level table rather than reduced to one scalar.

## Important Limits

- Repeated simulation from the known paired population is the calibration truth; bootstrap agreement alone is not treated as proof.
- The unpaired calculation is a diagnostic, not a valid competitor.
- Exact and near independence are nonregular and remain outside the method claim.
- This pilot establishes plausibility, not novelty or publication-ready validation.
