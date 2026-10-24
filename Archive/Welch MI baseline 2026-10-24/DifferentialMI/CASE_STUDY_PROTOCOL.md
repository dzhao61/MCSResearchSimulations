# Pre-Specified Real-Data Case Study

Date fixed: 25 July 2026

## Data

Use the official UCI Adult dataset, combining the supplied training and test
files after removing the test-file header and trailing period from its income
labels.

Source:

- Becker and Kohavi (1996), Adult, UCI Machine Learning Repository
- DOI: https://doi.org/10.24432/C5XW20

The analysis treats the 48,842 supplied records as the sample. It does not
use `fnlwgt` as frequency counts because the current inference assumes
ordinary independent observations rather than survey-weighted estimation.

## Fixed Scientific Question

Compare the association between education and income across the two recorded
sex groups:

```text
H0:
  I(education; income | recorded sex = Female)
  =
  I(education; income | recorded sex = Male).
```

This is a descriptive association comparison, not a causal or normative
claim about sex, education, or income.

## Tables

- Rows: all 16 education categories declared by UCI.
- Columns: `<=50K` and `>50K`.
- Groups: `Female` and `Male`.
- No category is removed or merged after inspecting its count.
- Records missing any primary variable would be excluded and counted.

The same aligned `16x2` alphabet is used for both groups.

## Methods

1. Analytic-bias-corrected influence-function Wald, the frozen primary
   method.
2. Raw group-label permutation of the plug-in MI difference, representing
   the procedure used in direct applied MI-difference work.
3. Studentized analytic-bias-corrected group-label permutation.
4. Standard one-sample likelihood-ratio chi-square independence p-values
   within each group, reported only to clarify that they answer a different
   question.

Use 9,999 table-level multivariate-hypergeometric permutations and seed
`2026072505`. All MI calculations use nats.

## Outputs

- corrected and uncorrected MI for each group;
- estimated MI difference, standard error, 95% confidence interval, and
  two-sided p-value;
- raw and studentized permutation p-values;
- zero-cell and expected-count diagnostics;
- pooled-mixture MI and influence variance;
- method runtimes; and
- the two complete contingency tables.

## Interpretation Rule

- If diagnostics are compatible with the frozen regular scope, interpret the
  Wald and studentized-permutation agreement directly.
- If sparse support or near-degeneracy is present, report the result as an
  illustration only and do not claim validated calibration.
- A raw-permutation disagreement is interpreted through the weak-null theory,
  not automatically as evidence that either observed conclusion is correct.
- The within-group chi-square tests cannot test equality of the two MI
  values.

