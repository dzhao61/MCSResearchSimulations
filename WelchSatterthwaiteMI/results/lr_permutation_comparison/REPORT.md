# Constrained LR and Studentized Permutation: Secondary Evaluation

This is not part of the primary thesis evidence. Expanded Welch is
validated on the full grid in `run_supervisor_experiment.py`; this
script answers a narrower question -- how does the constrained LR
test compare on accuracy and runtime, evaluated on the identical
population-pair grid -- before deciding whether to also propose it.

Profile: `full`. Replicate counts are scaled down by table
size because LR's per-replicate constrained optimization and the
permutation test's per-replicate resampling are far more expensive
than the closed-form Wald/Welch calculations used elsewhere in this
project; this is a disclosed trade-off appropriate only for this
secondary comparison, not for primary evidence.

## Overall calibration and runtime

| Method | Mean FPR (0.05) | Mean absolute error | Mean valid rate | Median runtime (ms) | p95 runtime (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| normal_wald | 0.0624 | 0.0214 | 0.9997 | 0.1833 | 0.1999 |
| expanded_welch | 0.0546 | 0.0165 | 0.9959 | 0.1833 | 0.1999 |
| constrained_lr | 0.0805 | 0.0407 | 0.9993 | 14.6280 | 26.5089 |
| student_permutation | 0.0782 | 0.0396 | 0.9997 | 0.7530 | 0.8267 |

## Output map

- `scenario_results.csv`: every population pair and method,
  including runtime percentiles.
- `regime_summary.csv`: regime-level aggregates; `all` rows give
  the overall summary above.
