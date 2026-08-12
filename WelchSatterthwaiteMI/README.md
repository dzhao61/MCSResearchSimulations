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

The current reading path and historical research records are indexed in
[`docs/README.md`](docs/README.md).

For a first-principles explanation of the literature, research question,
method, validation design, results, and limitations, see
[`docs/SUMMARY.md`](docs/SUMMARY.md).

For the complete line-by-line mathematical derivation of the expanded method,
see
[`docs/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`](docs/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md).
The compiled textbook-style edition is available as
[`derivation/main.pdf`](derivation/main.pdf), with reproducible LaTeX source
in [`derivation/main.tex`](derivation/main.tex).

## Status

The primary evidence uses 16 pre-specified configurations: four table shapes
crossed with balanced, moderately sparse, ultra-sparse, and ultra-sparse 5:1
sample-imbalance conditions. Each configuration has ten seeded population
repetitions and 5,000 sampled table pairs per repetition, giving 800,000 null
table pairs. Both sample sizes remain between 50 and 1,000.

At alpha `0.05`, Expanded Welch changed the mean ultra-sparse FPR from
`0.06373` to `0.05153` and the ultra-sparse 5:1 FPR from `0.16851` to
`0.12687`. It was mildly conservative in easier controls and did not fully
calibrate the widest sparse, unequal-sample case. Runtime was about 1.9 times
Normal Wald but only about 0.15 ms per table pair.

The result supports expanded Welch as a targeted finite-sample correction,
not as a uniformly superior replacement for normal Wald. See the
[`primary experiment report`](results/supervisor_16_config/REPORT.md) for the
concise results and its
[`rejection-calibration figure`](results/supervisor_16_config/rejection_calibration.png)
for the complete lower-tail comparison.

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
  --output-dir WelchSatterthwaiteMI/results/supervisor_16_config
```

See [`experiments/README.md`](experiments/README.md) and
[`results/README.md`](results/README.md) for the distinction between the
primary experiment and historical research records.
