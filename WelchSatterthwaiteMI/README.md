# Welch-Satterthwaite Differential Mutual Information

This project studies finite-degrees-of-freedom references for the existing
bias-corrected differential-MI Wald statistic. It does not modify the frozen
`DifferentialMI` implementation.

The target is the independent two-sample weak null

```text
H0: I(P) = I(Q), allowing P != Q.
```

The current method combines influence variances as

```text
SE^2 = V_P / n_P + V_Q / n_Q
```

but uses a standard-normal reference. The candidate keeps the estimator and
standard error unchanged and replaces that reference with a Student
distribution using Welch-Satterthwaite effective degrees of freedom.

See `VALIDATION_PROTOCOL.md` for the decision rules fixed before inspecting
the results.

For a short overview of the literature, method, and main results, start with
[`QUICK_SUMMARY.md`](QUICK_SUMMARY.md).

For a first-principles explanation of the research question, derivations,
validation design, results, and limitations, see
[`COMPREHENSIVE_SUMMARY.md`](COMPREHENSIVE_SUMMARY.md).

## Status

The primary evidence now comes from one unified experiment with 72 equal-MI
population pairs and 10,000 independently simulated table pairs per
population. The grid is divided into well-sampled, moderate, and sparse /
imbalanced regimes, with the same three analytic methods evaluated on every
replicate.

Expanded Welch was most useful in the target sparse and imbalanced regime. It
reduced mean calibration error relative to normal Wald by 39.2% at
alpha `0.05` and 50.6% at alpha `0.01`. It was mildly conservative in
well-sampled tables and lost about 0.010 average power in the five tested
alternatives. Its measured runtime was 0.16-0.18 ms per table pair, about
1.9 times the normal Wald implementation but still negligible in absolute
terms.

The result supports expanded Welch as a targeted finite-sample correction,
not as a uniformly superior replacement for normal Wald. See
`results/supervisor_full/REPORT.md` for the concise experiment report.

## Commands

```bash
.venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -v
.venv/bin/python WelchSatterthwaiteMI/experiments/run_supervisor_experiment.py \
  --profile smoke \
  --output-dir WelchSatterthwaiteMI/results/supervisor_smoke
```

The full supervisor experiment is:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_supervisor_experiment.py \
  --profile full \
  --output-dir WelchSatterthwaiteMI/results/supervisor_full
```

The older validation and audit scripts remain in `experiments/` as historical
research records, but they are not needed to explain or reproduce the primary
comparison.
