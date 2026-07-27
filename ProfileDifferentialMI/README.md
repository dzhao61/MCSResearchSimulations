# Constrained-Profile Tests for Differential Mutual Information

This isolated pilot tests whether classical constrained multinomial
goodness-of-fit statistics improve finite-sample inference for

```text
H0: I(P) = I(Q)
```

where `P` and `Q` are independent multinomial joint distributions on the same
discrete alphabet. It does not modify the frozen `DifferentialMI` project.

The implementation fits the two tables jointly under the one-dimensional
equal-MI constraint, then reports three asymptotic chi-squared tests with one
degree of freedom:

- profile likelihood-ratio (`profile_lr`)
- Pearson divergence from the constrained fit (`profile_pearson`)
- Cressie-Read power divergence with lambda `2/3` (`profile_cr_2_3`)

The existing analytically bias-corrected Wald test remains the primary
baseline. See `GO_NO_GO_PROTOCOL.md` for the decision rules fixed before
examining pilot results.

## Status

The pre-specified focused pilot produced a **no-go** decision for the raw
chi-squared-calibrated profile tests. They behaved correctly in regular
tables, but were materially liberal and slower than table permutation in the
sparse/skewed regimes that motivated the research. See
`FINAL_ASSESSMENT.md` and `results/focused/REPORT.md`.

## Run

From the repository root:

```bash
.venv/bin/python -m unittest discover -s ProfileDifferentialMI/tests -v
.venv/bin/python ProfileDifferentialMI/experiments/run_go_no_go.py \
  --profile smoke \
  --output-dir ProfileDifferentialMI/results/smoke
```

The smoke profile checks the complete pipeline. The focused profile increases
the number of null replicates:

```bash
.venv/bin/python ProfileDifferentialMI/experiments/run_go_no_go.py \
  --profile focused \
  --output-dir ProfileDifferentialMI/results/focused
```
