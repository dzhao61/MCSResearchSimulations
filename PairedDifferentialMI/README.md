# Paired Differential Mutual Information

This project tests the feasibility of deterministic inference for

```text
H0: I(X_A; Y_A) = I(X_B; Y_B)
```

when both conditions are measured on the same IID units. Each observation is

```text
(X_A, Y_A, X_B, Y_B).
```

The weak null only requires the two scalar MI values to be equal. The two
condition-specific distributions, marginals, and interaction patterns may
differ.

## Candidate Methods

The frozen pilot compares:

1. paired influence-function Wald with a normal reference;
2. paired influence-function Wald with a Student-t reference;
3. paired delete-one jackknife pseudo-values with a Student-t reference; and
4. an unpaired Wald calculation that deliberately discards covariance.

A 999-replicate paired nonparametric bootstrap-t is used on selected anchors
as a slower resampling reference. It resamples complete paired units, not the
two conditions separately.

## Why This May Be Easier Than Testing MI = 0

At positive MI, the difference of two MI values is a regular smooth
functional with a nonzero first derivative. At independence, the first
derivative vanishes and the problem becomes second-order and non-normal.
Near-independence scenarios are therefore included as expected failure
controls rather than silently treated as supported cases.

## Run

From the repository root:

```bash
PYTHONPATH=PairedDifferentialMI/src \
  .venv/bin/python PairedDifferentialMI/experiments/run_pilot.py
```

For a quicker smoke test:

```bash
PYTHONPATH=PairedDifferentialMI/src \
  .venv/bin/python PairedDifferentialMI/experiments/run_pilot.py \
  --profile smoke
```

Outputs are written to `PairedDifferentialMI/results/pilot/` by default.

## Scope

The pilot assumes fixed finite alphabets, positive population cell
probabilities, and IID paired units. It does not claim validity at exact or
near independence, with structural zeros, or with alphabet sizes growing
with sample size.
