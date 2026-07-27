# Paired Differential-MI Feasibility Results

## Decision: **NO-GO IN CURRENT FORM**

The decision applies to the positive-MI paired weak-null direction. Boundary scenarios remain outside the supported scope.

## Regular Positive-MI Calibration

| method | mean_absolute_fpr_error_05 | scenarios_in_035_065 | min_rejection_05 | max_rejection_05 |
| --- | --- | --- | --- | --- |
| paired_wald_normal | 0.0102 | 0.6667 | 0.0180 | 0.0677 |
| paired_wald_t | 0.0110 | 0.7500 | 0.0130 | 0.0643 |
| paired_jackknife_t | 0.0135 | 0.5833 | 0.0053 | 0.0583 |
| unpaired_wald_normal | 0.0336 | 0.1667 | 0.0000 | 0.1153 |

## Sparse Calibration

| method | mean_absolute_fpr_error_05 | scenarios_in_035_065 | min_rejection_05 | max_rejection_05 |
| --- | --- | --- | --- | --- |
| paired_wald_normal | 0.0166 | 0.6000 | 0.0118 | 0.0497 |
| paired_wald_t | 0.0198 | 0.6000 | 0.0084 | 0.0463 |
| paired_jackknife_t | 0.0234 | 0.4000 | 0.0088 | 0.0397 |
| unpaired_wald_normal | 0.0287 | 0.4000 | 0.0000 | 0.0487 |

## Power Controls

| scenario_id | true_delta | paired_wald_normal_reject_05 | paired_wald_t_reject_05 | paired_jackknife_t_reject_05 |
| --- | --- | --- | --- | --- |
| power_2x2_n100 | -0.0500 | 0.1145 | 0.1080 | 0.0845 |
| power_3x3_n150 | -0.0500 | 0.1485 | 0.1445 | 0.1290 |
| power_5x5_n500 | -0.0500 | 0.4990 | 0.4975 | 0.5635 |

## Bootstrap Anchors

- Median deterministic latency: `0.156 ms`.
- Median 999-bootstrap latency: `0.002 s`.
- Median measured speedup: `10.8x`.
- Median absolute jackknife-t versus bootstrap p-value difference: `0.0244`.

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
