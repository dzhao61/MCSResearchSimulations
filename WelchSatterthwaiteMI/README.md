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

The primary evidence now comes from one unified experiment with 192 equal-MI
population pairs and 10,000 independently simulated table pairs per
population. The eight regimes include controlled isolated sparsity,
widespread sparsity, shape mismatch, and extreme sample imbalance, with the
same three analytic methods evaluated on every replicate.

Expanded Welch reduced alpha-`0.05` calibration error relative to normal Wald
by 35.0% in the sparse-and-imbalanced regime and 35.8% under sample-size
ratios of `1:10` or `1:20`. It also improved the isolated rare-cell regimes.
It did not improve widespread sparsity, where it became conservative and was
slightly less often defined. Its measured runtime remained about 1.9 times
the normal Wald implementation but negligible in absolute terms.

The result supports expanded Welch as a targeted finite-sample correction,
not as a uniformly superior replacement for normal Wald. See the
[`primary experiment report`](results/supervisor_full/REPORT.md) for the
concise results.

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

See [`experiments/README.md`](experiments/README.md) and
[`results/README.md`](results/README.md) for the distinction between the
primary experiment and historical research records.
