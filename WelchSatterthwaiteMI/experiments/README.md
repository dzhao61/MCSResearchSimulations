# Experiments

## Primary Experiment

`run_supervisor_experiment.py` is the current unified experiment. It compares
normal Wald, simple Welch-Satterthwaite, and expanded
Welch-Satterthwaite on the same null and alternative table pairs. Its full
output is in
[`../results/supervisor_16_config/`](../results/supervisor_16_config/).

The null run records rejection rates over 101 nominal significance levels
from 0 to 0.10. It saves scenario-level curves, regime summaries with
population-variability bands, the complete null p-value arrays, and PNG/PDF
rejection-calibration figures. The full design has 16 pre-specified
configurations, ten population repetitions per configuration, and 5,000 null
table pairs per repetition. It totals 800,000 null table pairs while keeping
both sample sizes between 50 and 1,000.

## Scaled Chi-Squared Mechanism Audit

`validate_scaled_chi_square.py` directly tests the Satterthwaite working
model for the MI variance estimator. For each fixed population it uses one
Monte Carlo sample to estimate the finite-sample mean and variance of
`V-hat`, then evaluates moment-matched chi-squared, normal, and lognormal
models on an independent holdout sample. It separately evaluates the fully
population-predicted first-order chi-squared approximation and the plug-in
component degrees of freedom used by the implemented method.

The separate mechanism audit is retained as supporting evidence for the
scaled chi-squared working approximation:

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
