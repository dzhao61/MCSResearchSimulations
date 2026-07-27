# Final Assessment: Welch-Satterthwaite Differential MI

## Decision

**Go as a focused master's-thesis method and empirical contribution.**

The Welch-Satterthwaite reference is mathematically coherent as a first-order
analogy, inexpensive, and mildly beneficial. It provides a small,
reproducible calibration improvement without materially harming broad-regime
calibration or power.

The original automated decision was `NO-GO` because the frozen protocol
required at least a `20%` reduction in hard-grid calibration error. That
cutoff was an internal materiality screen rather than a scientific validity
criterion. It is retired as a thesis gate but remains documented in the
protocol and generated report to preserve the experimental audit trail.

The thesis should present the method as a modest deterministic refinement,
not as a complete solution to sparse or highly skewed MI inference.

## What Was Tested

The primary candidate changed only the reference distribution:

```text
Delta = [MI_hat(P) - d/(2 n_P)] - [MI_hat(Q) - d/(2 n_Q)]
a     = V_hat(P)/n_P
b     = V_hat(Q)/n_Q
SE    = sqrt(a+b)
T     = Delta/SE
nu    = (a+b)^2 / [a^2/(n_P-1) + b^2/(n_Q-1)]
p     = 2 * StudentT_nu.sf(|T|)
```

The estimate, bias correction, standard error, and standardized statistic
were identical to the frozen normal Wald baseline. This isolates the
finite-degrees-of-freedom effect.

The decisive run contained:

- 144 broad weak-null scenarios with 5,000 replicates each;
- 12 targeted hard weak-null scenarios with 20,000 replicates each;
- 26 small-sample stress scenarios with 10,000 replicates each;
- five power scenarios with 10,000 replicates each;
- 12,000 table pairs with 999 studentized analytic permutations;
- two independently generated population grids;
- 1,220,000 null table pairs and 50,000 power table pairs overall.

Every weak-null population pair had equal population MI while allowing
different joint distributions and margins.

## Main Calibration Result

At nominal alpha `0.05`:

| Stage | Method | Mean FPR | Mean absolute FPR error | In 3.5%-6.5% band |
| --- | --- | ---: | ---: | ---: |
| Broad | normal Wald | 0.04977 | 0.00514 | 97.22% |
| Broad | Welch reference | 0.04951 | 0.00504 | 97.92% |
| Hard | normal Wald | 0.06177 | 0.01177 | 75.00% |
| Hard | Welch reference | 0.06084 | 0.01084 | 91.67% |
| Stress | normal Wald | 0.06580 | 0.03180 | 19.23% |
| Stress | Welch reference | 0.06276 | 0.03037 | 15.38% |

The hard-grid FPR-error improvement was `7.9%`. Broad performance improved
very slightly rather than degrading. The frozen experiment compared this
result with an internal `20%` materiality target, which is retained in the
generated report but is no longer used as a thesis pass/fail rule.

The exploratory unbiased-variance sensitivity version reduced hard-grid MAE
to `0.01030`, a `12.5%` improvement over normal Wald. It remains a sensitivity
analysis because it was not the pre-specified primary candidate.

## Why the Change Is Small

The hard-grid median effective degrees of freedom ranged from approximately
`186` to `812`. Student critical values at those degrees of freedom are only
slightly larger than the normal critical value. Consequently:

- Welch removed 224 normal-Wald rejections among 240,000 hard null pairs;
- the paired rejection-rate change was `-0.000933`;
- its approximate 95% interval was `[-0.001056, -0.000811]`;
- only 188 of 720,000 broad-grid alpha-`0.05` decisions changed.

The correction is real and consistently conservative, but it is too small to
address residual MI bias, nonlinearity, sparse support, or influence-variance
estimation error.

In the low-sample stress grid, Welch modestly improved liberal scenarios but
made already-conservative `2x2` scenarios more conservative. It is therefore
not a uniformly useful boundary fix.

## Permutation Comparison

Across the 12 hard-grid permutation anchors:

| Method | Mean FPR | Mean absolute FPR error | In band |
| --- | ---: | ---: | ---: |
| normal Wald | 0.06208 | 0.01208 | 66.67% |
| Welch reference | 0.06083 | 0.01100 | 75.00% |
| unbiased Welch sensitivity | 0.06017 | 0.01033 | 83.33% |
| studentized analytic permutation | 0.05458 | 0.00642 | 100.00% |

The table-permutation reference remains better calibrated in this hard
regime. The deterministic methods remain substantially faster.

JIDT does not provide the independent two-sample weak-null test
`I(P) = I(Q)`, so its standard one-table independence significance API is not
a valid comparator for this experiment.

## Power and Runtime

Mean power loss for the primary Welch reference was only `0.00154` absolute.
The largest scenario-level loss was `0.0032`, at `N=150`.

Median single-pair runtime was:

```text
normal Wald:       0.1173 ms
Welch calculation: 0.1280 ms
```

The measured overhead was approximately `9.1%`, and every tested table
remained well below `1 ms`.

## Correctness and Reproducibility Audit

- All 21 frozen `DifferentialMI` tests passed.
- All eight new Welch tests passed.
- The normal component matched the frozen analytic Wald API.
- Group swapping and category relabelling were invariant.
- Finite-df p-values were never smaller than their normal counterparts.
- The large-sample result converged to the normal reference.
- Broad and hard valid-result rates were 100%.
- Stress valid-result rate was 99.987%; 34 degenerate first-order cases were
  explicitly marked invalid and their p-values were saved as missing.
- No valid p-value was nonfinite or outside `[0,1]`.
- Reconstructing a saved replicate from its scenario and simulation seeds
  reproduced its estimate, degrees of freedom, and p-values to floating-point
  precision.
- The calibration plot was visually inspected.

## Recommendation

Develop the Welch-Satterthwaite differential-MI procedure as the thesis's
primary proposed refinement, with the normal-reference corrected Wald test as
its direct baseline and studentized permutation as the stronger calibration
benchmark.

The contribution should be framed around the complete MI-specific procedure,
its deterministic implementation, and its finite-sample evaluation. Report
the improvement as modest and preserve the negative boundary findings:
ordinary Welch degrees of freedom do not eliminate MI estimator nonlinearity,
sparse-support bias, or degenerate first-order variance cases.

## Reproducible Files

- Protocol: `VALIDATION_PROTOCOL.md`
- Method: `src/welch_differential_mi/welch.py`
- Runner: `experiments/run_validation.py`
- Generated report: `results/decisive/REPORT.md`
- Aggregate results: `results/decisive/method_summary.csv`
- Scenario results: `results/decisive/null_summary.csv`
- Full null replicate data: reproducible with `experiments/run_validation.py`
- Permutation anchors: `results/decisive/permutation_summary.csv`
- Power: `results/decisive/power_summary.csv`
- Runtime: `results/decisive/runtime_summary.csv`
- Seeds and environment: `results/decisive/run_metadata.json`
