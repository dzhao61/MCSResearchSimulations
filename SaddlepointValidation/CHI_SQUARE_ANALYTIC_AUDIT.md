# Chi-Square / JIDT Analytic Significance Audit

Date: 2026-07-06

This note answers a specific concern: whether the chi-squared baseline used in the empirical fixed-margin validation was implemented correctly, and whether it used JIDT's built-in analytical significance test.

## Short Answer

The validation was using the standard likelihood-ratio chi-square test:

```text
G = 2N * MI_nats
p = P(ChiSquare_df >= G)
```

It was not using JIDT's built-in analytical significance method.

After auditing, the standard chi-square implementation is correct. It matches SciPy's built-in log-likelihood contingency-table G-test:

```python
scipy.stats.contingency.chi2_contingency(table, correction=False, lambda_="log-likelihood")
```

On a random sample of 300 saved calibration tables:

```text
max p-value difference: 1.94e-15
max statistic difference: 4.27e-11
bad degrees-of-freedom count: 0
```

So the large errors are not from a coding mistake in the standard chi-square test.

## Important Distinction: JIDT Analytic Is Different

JIDT's `MutualInformationCalculatorDiscrete.computeSignificance()` with no shuffle argument returns an analytic `ChiSquareMeasurementDistribution`.

Source and bytecode inspection show JIDT computes discrete MI in bits:

```java
double localValue = Math.log(jointProb / (probi * probj)) / log_2;
```

This is in:

```text
infodynamics/measures/discrete/MutualInformationCalculatorDiscrete.java
```

around lines 245-291 in the local JIDT source tree.

JIDT's analytic significance method then passes that bit-valued `average` directly into `ChiSquareMeasurementDistribution`:

```java
return new ChiSquareMeasurementDistribution(average,
        observations,
        (base1 - 1) * (base2 - 1));
```

The analytic distribution computes:

```java
1 - MathsUtils.chiSquareCdf(2.0 * numObservations * estimate, degreesOfFreedom)
```

Therefore JIDT uses:

```text
df = (base1 - 1) * (base2 - 1)
p = P(ChiSquare_df >= 2N * MI_JIDT)
```

JIDT reports discrete MI in bits. Therefore JIDT's built-in analytic statistic is:

```text
2N * MI_bits
```

The standard likelihood-ratio statistic is:

```text
2N * MI_nats = 2N * MI_bits * ln(2)
```

So JIDT's built-in analytic statistic is larger than the standard likelihood-ratio statistic by:

```text
1 / ln(2) ~= 1.4427
```

This makes JIDT's built-in analytic p-values smaller than the standard nats-based chi-square p-values.

## Hand-Checked Examples

The unit check below compares manual MI in bits, JIDT MI, manual MI in nats, JIDT analytic p-values, and SciPy chi-square p-values using both the bits-scaled and nats-scaled statistics.

| case | manual bits | JIDT MI | manual nats | JIDT analytic p | chi2 using bits | chi2 using nats |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `2x2 independent` | 0 | 0 | 0 | 1 | 1 | 1 |
| `2x2 diagonal` | 1 | 1 | 0.693147 | 2.54e-10 | 2.54e-10 | 1.40e-7 |
| `2x2 mild` | 0.191165 | 0.191165 | 0.132505 | 0.005688 | 0.005688 | 0.021323 |
| `3x3 skew` | 0.0142325 | 0.0142325 | 0.0098652 | 1.00e-5 | 1.00e-5 | 0.000564 |
| `4x4 diagonal` | 2 | 2 | 1.386294 | 0 | 7.43e-30 | 9.63e-20 |

For a perfectly dependent `2x2` table:

```text
table = [[10, 0],
         [0, 10]]
```

JIDT reports:

```text
MI_bits = 1.0
JIDT analytic p = chi2.sf(40, df=1) = 2.54e-10
```

Standard likelihood-ratio chi-square gives:

```text
G = 2 * 20 * ln(2) = 27.73
p = chi2.sf(27.73, df=1) = 1.40e-7
```

Both are extremely significant, but they are not the same p-value.

For a milder `2x2` table:

```text
table = [[8, 2],
         [3, 7]]
```

Results:

```text
JIDT analytic p = 0.00569
standard nats-based chi-square p = 0.02132
```

Again, JIDT analytic is more aggressive.

## Calibration Comparison

The completed focused calibration output was augmented with:

```text
jidt_analytic_bits_nominal_p
jidt_analytic_bits_nominal_statistic
```

These reproduce JIDT's built-in analytic convention without rerunning Java.

On the 6,000-row focused calibration:

| method | FPR at alpha=0.10 | FPR at alpha=0.05 | FPR at alpha=0.01 |
| --- | ---: | ---: | ---: |
| empirical fixed-margin | 0.1013 | 0.0537 | 0.0120 |
| JIDT shuffle anchors | 0.1033 | 0.0550 | 0.0133 |
| standard chi-square, dynamic df | 0.1517 | 0.1337 | 0.0993 |
| JIDT built-in analytic convention | 0.3622 | 0.3517 | 0.3378 |

Median absolute p-value error against JIDT shuffle anchors:

| method | median abs error |
| --- | ---: |
| empirical fixed-margin | 0.0119 |
| standard chi-square, dynamic df | 0.4715 |
| standard chi-square, nominal df | 0.4715 |
| JIDT built-in analytic convention | 0.4595 |

So using JIDT's built-in analytic significance would not fix the issue. In this focused grid it is even more anti-conservative overall.

## Why Chi-Square Looked So Bad

The calibration grid intentionally stresses regimes where asymptotic chi-square assumptions fail.

Some examples:

| config | median mean expected count | median min expected count | median fraction expected < 5 | standard chi2 FPR at 0.05 | empirical FPR at 0.05 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `20x20_N1000_balanced` | 2.5 | 1.404 | 1.000 | 0.544 | 0.048 |
| `50x20_N10000_balanced` | 10.0 | 7.724 | 0.000 | 0.086 | 0.038 |
| `50x20_N10000_x_balanced_y_strong` | 10.0 | 0.6805 | 0.950 | 0.974 | 0.048 |
| `80x80_N10000_zipf_mild` | 1.562 | 0.0182 | 0.948 | 0.000 | 0.076 |
| `100x50_N100000_strong` | 20.0 | 0.1328 | 0.970 | 0.000 | 0.048 |

The word "balanced" does not automatically mean chi-square is safe. For example:

```text
20x20 with N=1000 gives expected count N / (20 * 20) = 2.5 per cell.
```

That violates the usual expected-count rule of thumb.

The one balanced case with expected counts comfortably above 5, `50x20_N10000_balanced`, is much less pathological than the sparse cases, though still somewhat high in this finite grid:

```text
standard chi2 FPR at alpha=0.05: 0.086
empirical fixed-margin FPR at alpha=0.05: 0.038
```

As a direct sanity check, balanced simulations with genuinely healthy expected counts give approximately calibrated standard nats-based chi-square p-values:

| config | expected/cell | reps | FPR 0.10 | FPR 0.05 | FPR 0.01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `5x5, N=1000` | 40.00 | 5000 | 0.0978 | 0.0498 | 0.0092 |
| `10x10, N=10000` | 100.00 | 2500 | 0.1028 | 0.0488 | 0.0100 |
| `20x20, N=10000` | 25.00 | 1500 | 0.1167 | 0.0647 | 0.0120 |
| `50x20, N=50000` | 50.00 | 1000 | 0.1320 | 0.0550 | 0.0070 |

This supports the interpretation that the standard chi-square formula is not broken. It works much better in the regime where its asymptotic assumptions are closer to true.

## Recommendation

Keep three baselines separate in all future outputs:

1. `chi2_nominal_p`

Standard likelihood-ratio chi-square using:

```text
G = 2N * MI_nats
df = configured (r - 1)(c - 1)
```

2. `chi2_dynamic_p`

Standard likelihood-ratio chi-square using:

```text
G = 2N * MI_nats
df = observed nonempty rows/columns
```

3. `jidt_analytic_bits_nominal_p`

JIDT's built-in analytic convention:

```text
statistic = 2N * MI_bits
df = configured (base1 - 1)(base2 - 1)
```

The output also stores:

```text
mi_nats_observed
mi_bits_observed
jidt_analytic_bits_nominal_statistic
```

For the research claim, the fairest comparison is:

```text
empirical fixed-margin sampling vs JIDT shuffling vs standard likelihood-ratio chi-square
```

JIDT's built-in analytic result can be reported as an additional software baseline, but it should not be confused with the standard nats-based likelihood-ratio chi-square test.
