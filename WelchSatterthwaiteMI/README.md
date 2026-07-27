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

The method is a **go as a focused master's-thesis contribution**. The primary
Welch reference reduced hard-grid alpha-`0.05` FPR error by `7.9%`, preserved
broad-grid calibration, incurred negligible power loss, and remained
deterministic and inexpensive.

The generated report records a `NO-GO` because the original validation
protocol used an internal requirement of at least `20%` improvement. That
arbitrary materiality threshold has been retired as a thesis gate, but it is
retained in the protocol and generated results for audit transparency. The
scientific claim is deliberately modest: this is a finite-sample refinement,
not a complete solution to sparse-table MI inference.

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
