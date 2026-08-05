# Experiments

## Primary Experiment

`run_supervisor_experiment.py` is the current unified experiment. It compares
normal Wald, simple Welch-Satterthwaite, and expanded Welch-Satterthwaite on
the same null and alternative table pairs. Its full output is in
[`../results/supervisor_full/`](../results/supervisor_full/).

## Historical Experiments

- `run_validation.py` produced the earlier decisive validation grid.
- `run_adversarial_holdout.py` produced the independent adversarial holdout.
- `audit_variance_bias.py` examined bias and dependence in estimated variance
  components.
- `audit_variance_components.py` performed the smaller component audit.

These scripts are retained for reproducibility and research provenance. Run
all scripts from the repository root so their local import paths resolve
consistently.
