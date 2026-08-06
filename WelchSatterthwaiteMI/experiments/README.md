# Experiments

## Primary Experiment

`run_supervisor_experiment.py` is the current unified experiment. It compares
normal Wald, simple Welch-Satterthwaite, expanded Welch-Satterthwaite, and the
guarded Custom Welch rule on the same null and alternative table pairs. Its
full output is in
[`../results/supervisor_full/`](../results/supervisor_full/).

## Custom Welch Routing Audit

`investigate_custom_welch_decision.py` crosses sample-size ratio, population
regime, table shape, and allocation direction in separate development and
holdout cohorts. It compares ratio thresholds and observed-data guards for
choosing between normal Wald and expanded Welch. The analysis is summarized
in
[`../docs/CUSTOM_WELCH_DECISION_AUDIT.md`](../docs/CUSTOM_WELCH_DECISION_AUDIT.md),
with complete output in
[`../results/custom_decision_audit/`](../results/custom_decision_audit/).

## Historical Experiments

- `run_validation.py` produced the earlier decisive validation grid.
- `run_adversarial_holdout.py` produced the independent adversarial holdout.
- `audit_variance_bias.py` examined bias and dependence in estimated variance
  components.
- `audit_variance_components.py` performed the smaller component audit.

These scripts are retained for reproducibility and research provenance. Run
all scripts from the repository root so their local import paths resolve
consistently.
