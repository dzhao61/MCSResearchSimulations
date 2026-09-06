# Experiments

## Final Confirmatory Experiment

`run_detection_breakdown_sweep.py` implements the frozen protocol in
`FINAL_PROTOCOL.json`. It compares Normal Wald, Simple Welch, and Expanded
Welch across calibration, power, interaction-pattern robustness, and unequal-
sample robustness cells. The runner constructs deterministic populations,
uses stable configuration-specific seeds, processes simulations in bounded
batches, and generates all aggregate data, checks, figures, and `REPORT.md`.

`make_final_experiment_landscape.py` converts the frozen configuration-level
results into the Wald-versus-Expanded-Welch atlas in
[`../docs/experiments/FINAL_EXPERIMENT_LANDSCAPE.md`](../docs/experiments/FINAL_EXPERIMENT_LANDSCAPE.md).
Its heatmaps preserve every exact configuration at the primary significance
level rather than pooling regimes.

Routine simulation work follows a run-first convention: once an experiment or
diagnostic is sufficiently specified and low risk, implement and run it, then
use the evidence to guide discussion. Supervisor confirmation is reserved for
consequential changes to the research question, method, or thesis scope rather
than ordinary implementation and empirical checks.

## Exploratory Constrained-LR Program

The constrained-LR derivation, 2x2 validation, and multi-alphabet screen are
retained as exploratory work outside the final confirmatory protocol.

### 2x2 experiments

The supervisor-guided design and its interpreted results are documented in
[`../docs/experiments/EQUAL_MI_2X2_BASELINE.md`](../docs/experiments/EQUAL_MI_2X2_BASELINE.md).
It uses
deterministic `2x2` population pairs to map calibration, validity, breakdown,
and power without imposing an expected-cell-count floor.

The complete screening and independent confirmatory outputs are retained in
[`../results/2x2_screening/`](../results/2x2_screening/) and
[`../results/2x2_confirmatory/`](../results/2x2_confirmatory/).

`run_critical_value_audit.py` diagnoses the location, scale, shape, and
numerator-denominator dependence of the current statistic.
`run_joint_cornish_fisher_audit.py` performs the independent development and
validation experiment that rejected a joint higher-order moment correction as
the next primary method. Its confirmatory output is in
[`../results/2x2_joint_cf_confirmatory/`](../results/2x2_joint_cf_confirmatory/).

`run_constrained_lr_audit.py`, `run_constrained_lr_power.py`, and
`run_constrained_lr_full_curves.py` test the directly usable constrained
likelihood-ratio statistic for equal MI using its \(\chi^2_1\) reference. The
final five-start calibration and power outputs are in
[`../results/2x2_constrained_lr_confirmatory_fullstarts/`](../results/2x2_constrained_lr_confirmatory_fullstarts/)
and
[`../results/2x2_constrained_lr_power_fullstarts/`](../results/2x2_constrained_lr_power_fullstarts/).
The full feasible-range results are in
[`../results/2x2_constrained_lr_full_curves/`](../results/2x2_constrained_lr_full_curves/).
The interpreted LR validation is in
[`../docs/experiments/CONSTRAINED_LR_2X2_VALIDATION.md`](../docs/experiments/CONSTRAINED_LR_2X2_VALIDATION.md).

## Multi-Alphabet LR Experiment

`run_multialphabet_lr_experiment.py` extends the equal-MI comparison to 3x3,
4x4, 5x5, and 8x8 tables. It records each exact shape, marginal regime, and
sample size separately. The interpreted design and results are in
[`../docs/experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md`](../docs/experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md),
with generated outputs in
[`../results/multialphabet_lr_screen/`](../results/multialphabet_lr_screen/).

`run_multialphabet_lr_confirmatory.py` reruns six prespecified favorable,
unfavorable, and control configurations with higher replication. Its outputs
are in
[`../results/multialphabet_lr_confirmatory/`](../results/multialphabet_lr_confirmatory/).

## Prior Broad Experiment

`run_supervisor_experiment.py` is the earlier broad experiment. It compares
normal Wald, simple Welch-Satterthwaite, and expanded
Welch-Satterthwaite on the same null and alternative table pairs. Its full
output is in
[`../results/supervisor_practical/`](../results/supervisor_practical/).

The null run records rejection rates over 101 nominal significance levels
from 0 to 0.10. It saves scenario-level curves, regime summaries with
population-variability bands, the complete null p-value arrays, and PNG/PDF
rejection-calibration figures. The full design has 60 scenarios across five
regimes and six table shapes, with both sample sizes restricted to 50--1,000.

## Scaled Chi-Squared Mechanism Audit

`validate_scaled_chi_square.py` directly tests the Satterthwaite working
model for the MI variance estimator. For each fixed population it uses one
Monte Carlo sample to estimate the finite-sample mean and variance of
`V-hat`, then evaluates moment-matched chi-squared, normal, and lognormal
models on an independent holdout sample. It separately evaluates the fully
population-predicted first-order chi-squared approximation and the plug-in
component degrees of freedom used by the implemented method.

The separate focused mechanism audit covers `2x2`, `3x3`, `5x5`, and `10x10`
tables across the earlier broad regime set:

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
