# Variance-Bias and Degrees-of-Freedom Audit

## Status

This is a **post-hoc diagnostic**, not a confirmatory validation. It was
motivated by an external critique of the original Welch-type differential-MI
test. The original decisive outputs remain unchanged.

The audit evaluated 240,000 new table pairs from the 12 decisive hard
populations and 720,000 table pairs from 72 newly generated weak-null
populations. The fresh population seed (`2026080301`) and simulation seed
(`2026080302`) were fixed before running the audit.

## Main Finding

The original `n - 1` component degrees of freedom are too large for the
plug-in influence-variance estimator. However, a simple downward bias in the
estimated variance is **not** the primary explanation:

- Mean estimated `SE^2 / true asymptotic SE^2` was `1.0014` on the decisive
  hard grid and `1.0662` on the 72-scenario fresh grid.
- The empirical variance of the corrected MI difference was about `1.0710`
  and `1.0632` times the first-order population variance, respectively.
- The mean correlation between the corrected difference and estimated
  `SE^2` was `0.5865` on the decisive hard grid and `0.3963` on the fresh
  grid.
- Replacing the estimated variance by the known population variance did not
  uniformly repair calibration.

The bottleneck is therefore the joint finite-sample distribution of the MI
estimate and its estimated uncertainty, not a single universal multiplicative
variance bias.

## Candidate References

The audit compared:

- `normal`: bias-corrected influence-function Wald test.
- `naive_welch`: the original `n - 1` Welch-Satterthwaite analogy.
- `local_kurtosis`: component df from the fourth moment of the local score,
  treating that score as fixed.
- `variance_if`: component df from the full influence function of the
  variance functional, accounting for changes in the empirical local score.
- `oracle_variance_normal`: diagnostic normal test using known population
  influence variances.

### Mean Absolute FPR Error

| Population set | Alpha | Normal | Naive Welch | Local kurtosis | Variance IF | Oracle variance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Decisive hard (12) | 0.10 | 0.01677 | 0.01565 | 0.01425 | **0.01213** | 0.01133 |
| Decisive hard (12) | 0.05 | 0.01270 | 0.01169 | 0.01040 | **0.00823** | 0.00785 |
| Decisive hard (12) | 0.01 | 0.00568 | 0.00506 | 0.00428 | **0.00266** | 0.00354 |
| Fresh hard (6) | 0.10 | 0.01553 | 0.01430 | 0.01307 | **0.01167** | 0.01180 |
| Fresh hard (6) | 0.05 | 0.00993 | 0.00912 | 0.00775 | **0.00662** | 0.00837 |
| Fresh hard (6) | 0.01 | 0.00407 | 0.00360 | 0.00317 | **0.00232** | 0.00317 |
| Fresh all (72) | 0.05 | 0.00463 | 0.00445 | **0.00423** | 0.00446 | 0.00756 |

All methods had a valid-result rate of `1.0` in this regular positive-support
audit.

## Interpretation

The full variance-functional reference is substantially better in the
deliberately liberal hard regimes. At alpha `0.05`, it reduced mean absolute
FPR error by `35.2%` on the decisive hard populations and `33.4%` on the
fresh hard subset relative to normal Wald. The gain was larger at alpha
`0.01`.

It is not uniformly better across the complete fresh grid. At alpha `0.05`,
the variance-functional candidate improved 28 scenarios, worsened 39, and
tied 5 relative to normal Wald, although its average MAE was slightly lower.
The simpler local-kurtosis version had the best all-grid mean MAE but was
weaker than the full variance-functional calculation in the hard subset.

These results justify a new pre-specified validation of the
variance-functional candidate. They do not justify silently replacing the
original method or claiming universal superiority.

## Reproduction

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/audit_variance_bias.py \
  --output-dir WelchSatterthwaiteMI/results/variance_bias_audit
```

Outputs:

- `scenario_audit.csv`: scenario-level variance and calibration diagnostics.
- `method_summary.csv`: aggregate calibration by source and alpha.
- `run_metadata.json`: seeds, replicate counts, and software versions.

## Required Next Experiment

Freeze a second-stage protocol before further inspection. It should compare
the normal baseline, the Hutcheson-type `n - 1` reference, local-kurtosis df,
full variance-functional df, and studentized permutation. Include alpha
`0.10`, `0.05`, and `0.01`, power, declared-versus-observed support
sensitivity, and a multinomial bootstrap-t comparator. Use entirely new
population and simulation seeds.
