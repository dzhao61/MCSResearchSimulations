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

The primary evidence comes from one unified experiment with 60 equal-MI
population pairs and 10,000 independently simulated table pairs per
population. It covers five regimes and six table shapes while keeping both
sample sizes between 50 and 1,000. The same three analytic methods are
evaluated on every replicate.

Expanded Welch left the well-sampled control essentially unchanged and
reduced alpha-`0.05` calibration error relative to Normal Wald by 29% to 47%
across the moderate, rare-cell, ultra-sparse, and widespread-sparsity
regimes. Its measured runtime remained about 1.9 times the Normal Wald
implementation but negligible in absolute terms.

The result supports expanded Welch as a targeted finite-sample correction,
not as a uniformly superior replacement for normal Wald. See the
[`primary experiment report`](results/supervisor_practical/REPORT.md) for the
concise results and its
[`rejection-calibration figure`](results/supervisor_practical/rejection_calibration.png)
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
  --output-dir WelchSatterthwaiteMI/results/supervisor_practical
```

See [`experiments/README.md`](experiments/README.md) and
[`results/README.md`](results/README.md) for the distinction between the
primary experiment and historical research records.
