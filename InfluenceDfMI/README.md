# MI-Specific Influence Degrees of Freedom

This isolated project derives and tests a deterministic finite-sample
reference for the independent two-sample weak null

```text
H0: I(P) = I(Q), allowing P != Q.
```

It keeps the existing bias-corrected differential-MI estimate and influence
standard error unchanged. The only candidate change is a Student reference
whose degrees of freedom are derived from the influence function of the
MI-variance functional, rather than assigning each group `n-1` degrees of
freedom.

## Result

The frozen experiment produced a **NO-GO as a universal replacement**.

- Hard weak-null alpha-`0.05` MAE improved by `35.0%`.
- Stress-grid MAE improved from `0.03567` to `0.02658` versus naive Welch.
- Denominator-df log-error fell by `95.4%`.
- Scalar time was `0.162 ms`, or `1.37x` the normal method.
- Broad-grid MAE increased slightly from `0.00462` to `0.00494`.
- Balanced-grid MAE worsened from `0.00546` for normal to `0.00735`.

The derivation accurately models the variability of the estimated
denominator, but that alone does not imply the full statistic is Student-t.
The method is promising in heterogeneous/sparse regimes and too conservative
in balanced regimes.

See:

- `DERIVATION.md` for the calculation.
- `VALIDATION_PROTOCOL.md` for the rules frozen before the run.
- `FINAL_ASSESSMENT.md` for interpretation and next steps.
- `results/frozen_decisive/REPORT.md` for complete results.
- `results/frozen_decisive/AUDIT.json` for the independent artifact audit.

## Commands

Run the correctness tests:

```bash
PYTHONPATH=InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python -m unittest discover -s InfluenceDfMI/tests -v
```

The decisive run is creation-only and should not overwrite the frozen output:

```bash
PYTHONPATH=InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python InfluenceDfMI/experiments/run_validation.py \
  --output-dir InfluenceDfMI/results/a_new_external_replication
```

Audit an existing result:

```bash
PYTHONPATH=InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python InfluenceDfMI/experiments/audit_results.py \
  --results-dir InfluenceDfMI/results/frozen_decisive \
  --output InfluenceDfMI/results/frozen_decisive/AUDIT.json
```
