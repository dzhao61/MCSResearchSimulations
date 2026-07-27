# Welch-Satterthwaite Differential Mutual Information

This isolated refinement tests a finite-degrees-of-freedom reference
distribution for the existing bias-corrected differential-MI Wald statistic.
It does not modify the frozen `DifferentialMI` implementation.

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

## Status

The decisive experiment produced a **no-go as a material finite-sample
refinement**. The primary Welch reference reduced hard-grid alpha-`0.05` FPR
error by `7.9%`, below the pre-specified `20%` requirement. It was harmless,
cheap, and slightly better calibrated, so it can remain an optional
sensitivity calculation; it is not a solution to the sparse-table problem or
a strong standalone methodological contribution.

See `FINAL_ASSESSMENT.md` and `results/decisive/REPORT.md`.

## Commands

```bash
.venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -v
.venv/bin/python WelchSatterthwaiteMI/experiments/run_validation.py \
  --profile smoke \
  --output-dir WelchSatterthwaiteMI/results/smoke
```

The decisive experiment is:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/run_validation.py \
  --profile decisive \
  --output-dir WelchSatterthwaiteMI/results/decisive
```
