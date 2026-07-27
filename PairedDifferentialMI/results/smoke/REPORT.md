# Paired Differential-MI Feasibility Results

## Decision: **NO-GO IN CURRENT FORM**

The decision applies to the positive-MI paired weak-null direction. Boundary scenarios remain outside the supported scope.

## Regular Positive-MI Calibration

| method | mean_absolute_fpr_error_05 | scenarios_in_035_065 | min_rejection_05 | max_rejection_05 |
| --- | --- | --- | --- | --- |
| paired_wald_normal | 0.0250 | 0.5000 | 0.0133 | 0.0633 |
| paired_wald_t | 0.0250 | 0.5000 | 0.0100 | 0.0600 |
| paired_jackknife_t | 0.0250 | 0.5000 | 0.0067 | 0.0567 |
| unpaired_wald_normal | 0.0383 | 0.0000 | 0.0033 | 0.0800 |

## Sparse Calibration

| method | mean_absolute_fpr_error_05 | scenarios_in_035_065 | min_rejection_05 | max_rejection_05 |
| --- | --- | --- | --- | --- |
| paired_wald_normal | 0.0395 | 0.0000 | 0.0105 | 0.0105 |
| paired_wald_t | 0.0395 | 0.0000 | 0.0105 | 0.0105 |
| paired_jackknife_t | 0.0323 | 0.0000 | 0.0177 | 0.0177 |
| unpaired_wald_normal | 0.0500 | 0.0000 | 0.0000 | 0.0000 |

## Power Controls

| scenario_id | true_delta | paired_wald_normal_reject_05 | paired_wald_t_reject_05 | paired_jackknife_t_reject_05 |
| --- | --- | --- | --- | --- |
| power_2x2_n100 | -0.0500 | 0.1350 | 0.1300 | 0.0850 |

## Bootstrap Anchors

- Median deterministic latency: `0.157 ms`.
- Median 999-bootstrap latency: `0.000 s`.
- Median measured speedup: `2.7x`.
- Median absolute jackknife-t versus bootstrap p-value difference: `0.0255`.

## Pre-Specified Rules

- Rule 1, regular calibration: **FAIL**.
- Rule 3, sparse refinement value: **FAIL**.
- Rule 5, runtime: **FAIL**.

Rules concerning pairing signs and the boundary are interpreted from the scenario-level table rather than reduced to one scalar.

## Important Limits

- Repeated simulation from the known paired population is the calibration truth; bootstrap agreement alone is not treated as proof.
- The unpaired calculation is a diagnostic, not a valid competitor.
- Exact and near independence are nonregular and remain outside the method claim.
- This pilot establishes plausibility, not novelty or publication-ready validation.
