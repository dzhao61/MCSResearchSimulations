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

## Status

The original `n - 1` Welch reference remains a useful baseline but is not a
new test architecture: Hutcheson's 1970 Shannon-diversity test is the direct
entropy-template predecessor. The frozen experiment recorded `NO-GO` under
its pre-specified 20% materiality rule; it achieved a real but modest 7.9%
hard-grid error reduction.

A later post-hoc audit derived full variance-functional component degrees of
freedom. This candidate reduced alpha-`0.05` hard-grid MAE by about 33-35% in
the audited populations and helped more strongly at alpha-`0.01`, but it was
not uniformly better across 72 fresh regular scenarios. It is promising and
requires a new pre-specified validation against local-kurtosis df,
studentized permutation, and multinomial bootstrap-t before becoming the
primary thesis method.

See `FINAL_ASSESSMENT.md` for the historical decision,
`results/decisive/REPORT.md` for the frozen experiment, and
`results/variance_bias_audit/REPORT.md` for the new diagnostic.

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

The post-hoc variance audit is:

```bash
.venv/bin/python WelchSatterthwaiteMI/experiments/audit_variance_bias.py \
  --output-dir WelchSatterthwaiteMI/results/variance_bias_audit
```
