# Joint Studentized Edgeworth Differential MI

This project tests a deterministic MI-specific correction for the independent
two-sample weak null

```text
H0: I(P) = I(Q), allowing P != Q.
```

The candidate models the MI difference and its estimated variance jointly.
It uses the third moment of the MI influence function and its covariance with
the variance-functional influence function to form a first
studentized-Edgeworth correction.

## Final Status

**NO-GO as a usable significance test.**

The frozen mechanical criteria initially returned `GO`:

- hard alpha-`0.05` MAE improved from `0.01130` to `0.00681`;
- broad MAE improved from `0.00531` to `0.00428`;
- balanced MAE improved from `0.00556` to `0.00484`;
- median runtime was `0.265 ms`; and
- all nine pre-specified criteria passed.

The required adversarial audit then found that locally invalid Edgeworth
evaluations were concentrated almost entirely in the rejection tails.
Among invalid regular-grid cases, `99-100%` were significant under the normal
reference. Conditioning calibration on valid cases therefore removed extreme
observations and made the candidate look better.

With the only defensible simple completion, normal fallback:

- hard MAE becomes `0.01082`, only about `4.2%` better than naive Welch and
  below the required `10%` improvement;
- broad MAE becomes `0.00582`, worse than naive Welch;
- balanced MAE becomes `0.00680`, worse than normal; and
- strong-null MAE becomes `0.00556`, outside the frozen tolerance.

See `FINAL_ASSESSMENT.md` and `ADVERSARIAL_AUDIT.md`. The original
prospective output remains unchanged in `results/frozen_decisive/REPORT.md`.

## Commands

Run the correctness tests:

```bash
PYTHONPATH=JointEdgeworthMI/src:InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python -m unittest discover -s JointEdgeworthMI/tests -v
```

Run a new external replication:

```bash
PYTHONPATH=JointEdgeworthMI/src:InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python JointEdgeworthMI/experiments/run_validation.py \
  --output-dir JointEdgeworthMI/results/a_new_external_replication
```

Audit result integrity:

```bash
PYTHONPATH=JointEdgeworthMI/src:InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python JointEdgeworthMI/experiments/audit_results.py \
  --results-dir JointEdgeworthMI/results/frozen_decisive \
  --output JointEdgeworthMI/results/frozen_decisive/AUDIT.json
```

Regenerate the exact tables and audit invalid tails:

```bash
PYTHONPATH=JointEdgeworthMI/src:InfluenceDfMI/src:DifferentialMI/src:WelchSatterthwaiteMI/src \
  .venv/bin/python JointEdgeworthMI/experiments/audit_invalid_cases.py \
  --results-dir JointEdgeworthMI/results/frozen_decisive \
  --output JointEdgeworthMI/results/frozen_decisive/invalid_case_audit.csv
```
