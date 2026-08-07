# Experiments

## Primary Experiment

`run_supervisor_experiment.py` is the current unified experiment. It compares
normal Wald, simple Welch-Satterthwaite, and expanded
Welch-Satterthwaite on the same null and alternative table pairs. Its full
output is in
[`../results/supervisor_full/`](../results/supervisor_full/).

## Scaled Chi-Squared Mechanism Audit

`validate_scaled_chi_square.py` directly tests the Satterthwaite working
model for the MI variance estimator. For each fixed population it uses one
Monte Carlo sample to estimate the finite-sample mean and variance of
`V-hat`, then evaluates moment-matched chi-squared, normal, and lognormal
models on an independent holdout sample. It separately evaluates the fully
population-predicted first-order chi-squared approximation and the plug-in
component degrees of freedom used by the implemented method.

The focused profile covers `2x2`, `3x3`, `5x5`, and `10x10` tables across all
eight regimes:

```bash
MPLBACKEND=Agg .venv/bin/python \
  WelchSatterthwaiteMI/experiments/validate_scaled_chi_square.py \
  --profile focused \
  --output-dir WelchSatterthwaiteMI/results/scaled_chi_square_validation
```

Its retained output is in
[`../results/scaled_chi_square_validation/`](../results/scaled_chi_square_validation/).

## Historical Experiments

- `run_validation.py` produced the earlier decisive validation grid.
- `run_adversarial_holdout.py` produced the independent adversarial holdout.
- `audit_variance_bias.py` examined bias and dependence in estimated variance
  components.
- `audit_variance_components.py` performed the smaller component audit.
- [`../archive/custom_welch/`](../archive/custom_welch/) preserves the
  discontinued routing experiment and its generated evidence.

These scripts are retained for reproducibility and research provenance. Run
all scripts from the repository root so their local import paths resolve
consistently.
