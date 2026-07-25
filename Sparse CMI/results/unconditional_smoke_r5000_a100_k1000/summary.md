# Sparse CMI Unconditional Calibration Summary

Evaluated 32 data-generating configurations with 5,000 independent null datasets per configuration. Every replicate regenerated the observed stratum margins.

## Mean absolute size distortion

| Alpha | Normal | Edgeworth | Cornish-Fisher | Chi2 nominal | Chi2 informative | Conditional MC anchors |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.01210 | 0.00642 | 0.00673 | 0.12157 | 0.26638 | 0.02344 |
| 0.05 | 0.01783 | 0.00391 | 0.00309 | 0.07448 | 0.20073 | 0.02000 |
| 0.01 | 0.01124 | 0.00204 | 0.00223 | 0.02299 | 0.08949 | 0.00781 |

## Conditional Monte Carlo p-value anchors

Mean absolute p-value difference on held-out observed tables:

| Method | Mean MAE | Median MAE |
|---|---:|---:|
| normal | 0.04653 | 0.02388 |
| edgeworth | 0.04319 | 0.01510 |
| chi2_nominal | 0.24885 | 0.19645 |
| chi2_informative | 0.27092 | 0.30519 |

## Runtime

Median per-table speedup over a 1,000-draw conditional table Monte Carlo test: 34.0x.

## Guardrails

- Conditional Monte Carlo FPR uses only the configured anchor replicates and is therefore noisier than the approximation and chi-square FPR estimates.
- Approximation runtime is vectorized batch throughput with a cache shared across repeated margin patterns. Use the fixed-margin runner's literal permutation benchmark for the stronger one-table runtime comparison.
- This validates repeated-sampling calibration under i.i.d. binary CMI nulls. It does not validate transfer entropy or temporally dependent observations.
