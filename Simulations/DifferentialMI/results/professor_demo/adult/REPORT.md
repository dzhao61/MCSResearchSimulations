# UCI Adult Differential-MI Case Study

## Question

Does the education-income mutual information differ between female and
male records in this dataset?

## Result

- Female sample size: `16192`
- Male sample size: `32650`
- Female corrected MI: `0.039021` nats
- Male corrected MI: `0.076156` nats
- Corrected difference, Female - Male: `-0.037135` nats
- Standard error: `0.003034`
- 95% confidence interval: `[-0.043082, -0.031189]`
- Analytic Wald p-value: `1.88975e-34`
- Raw permutation p-value: `0.0001`
- Studentized analytic permutation p-value: `0.0001`

## Diagnostics

- Zero-cell fractions: female `0.062`, male `0.000`
- Expected-count-below-5 fractions: female `0.031`, male `0.000`
- Minimum expected counts: female `2.622`, male `17.922`
- Pooled-mixture MI: `0.063819` nats
- Pooled influence variance: `0.120915`
- Simple support screen passed: `True`

## Runtime

- Analytic Wald: `0.224 ms`
- 9999 table permutations: `0.050 s`

## Important Boundary

The two within-group chi-square p-values test independence of education
and income separately. They do not test whether the two MI values are
equal. The analysis is descriptive, unweighted, and not causal.
