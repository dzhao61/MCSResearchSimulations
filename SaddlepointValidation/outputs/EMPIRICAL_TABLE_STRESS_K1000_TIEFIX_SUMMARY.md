# Empirical Fixed-Margin Table Sampling Stress Test, K=1000

This run compares three MI null/significance methods:

- Empirical fixed-margin table sampling with `K=1000` sampled contingency tables.
- JIDT `computeSignificance` with `K=1000` shuffles.
- Chi-squared p-values using the observed dynamic degrees of freedom after empty margins are dropped.

The empirical-table p-value is the primary candidate method here. Gamma is still recorded, but it is secondary because sparse discrete nulls can have large point masses that a continuous gamma approximation cannot represent.

## Test Design

Stress grid:

- Shapes: `20x20`, `50x20`, `80x80`, `100x50`, `100x100`.
- Sample sizes: `1,000`, `10,000`, `100,000`, `1,000,000`.
- Skewness regimes: `balanced`, `slight`, `mild`, `strong`, `extreme`, `zipf_mild`, `zipf_strong`.
- Total: 140 configurations, 1 replicate each.

Mega anchors:

- Shapes: `50x20`, `100x50`, `100x100`.
- Sample size: `2,000,000`.
- Skewness regimes: `balanced`, `mild`, `strong`, `extreme`, `zipf_strong`.
- Total: 15 configurations, 1 replicate each.

All empirical-table and JIDT comparisons used `K=1000`.

## Important Fix

The first stress run exposed a sparse-table tie-handling issue. In extreme sparse tables, many fixed-margin null tables have exactly the same `G` value as the observed table. JIDT includes those ties in the upper-tail p-value. The empirical-table sampler now does the same using a small numerical tolerance around `G_obs`.

Without this fix, empirical p-values could be too small in point-mass cases. After the fix, a checked pathological case changed from empirical `p ~= 0.25` to empirical `p = 1.0`, matching JIDT `p = 1.0`.

## Overall Results

| run | rows | median empirical time | median JIDT time | median speedup | median abs empirical-vs-JIDT error | median abs chi2-vs-JIDT error | empirical closer than chi2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Stress to `N=1M` | 140 | 0.0649s | 0.4999s | 2.35x | 0.0100 | 0.2483 | 91.4% |
| Mega anchors `N=2M` | 15 | 0.3079s | 28.2504s | 91.0x | 0.0133 | 0.2442 | 93.3% |
| Combined | 155 | 0.0741s | 0.9768s | 3.66x | 0.0101 | 0.2442 | 91.6% |

## Runtime Scaling By N

| N | rows | empirical time | JIDT time | speedup | empirical error vs JIDT | chi2 error vs JIDT |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 35 | 0.0156s | 0.0155s | 0.87x | 0.0067 | 0.3800 |
| 10,000 | 35 | 0.0903s | 0.0900s | 1.13x | 0.0128 | 0.3290 |
| 100,000 | 35 | 0.2117s | 1.1405s | 6.09x | 0.0081 | 0.2432 |
| 1,000,000 | 35 | 0.3063s | 11.8594s | 39.94x | 0.0146 | 0.0737 |
| 2,000,000 | 15 | 0.3079s | 28.2504s | 91.01x | 0.0133 | 0.2442 |

## Accuracy By Skewness

Stress run only:

| skewness | rows | empirical error vs JIDT | chi2 error vs JIDT | empirical closer than chi2 |
| --- | ---: | ---: | ---: | ---: |
| balanced | 20 | 0.0139 | 0.1553 | 75% |
| slight | 20 | 0.0156 | 0.1260 | 85% |
| mild | 20 | 0.0123 | 0.2385 | 95% |
| strong | 20 | 0.0092 | 0.2790 | 95% |
| extreme | 20 | 0.0069 | 0.4017 | 100% |
| zipf_mild | 20 | 0.0129 | 0.1347 | 90% |
| zipf_strong | 20 | 0.0057 | 0.4885 | 100% |

## Null Rejection Screen

These are screening-level rejection rates across one table per configuration, not per-configuration calibration estimates.

| run | alpha | empirical table | JIDT | chi2 dynamic | gamma |
| --- | ---: | ---: | ---: | ---: | ---: |
| Stress | 0.10 | 0.0786 | 0.0857 | 0.2214 | 0.0929 |
| Stress | 0.05 | 0.0357 | 0.0429 | 0.2000 | 0.0286 |
| Stress | 0.01 | 0.0071 | 0.0071 | 0.1786 | 0.0071 |
| Mega | 0.10 | 0.1333 | 0.1333 | 0.2000 | 0.1333 |
| Mega | 0.05 | 0.0000 | 0.0000 | 0.2000 | 0.0000 |
| Mega | 0.01 | 0.0000 | 0.0000 | 0.2000 | 0.0000 |

## Interpretation

Empirical fixed-margin table sampling is still very promising.

It is not faster than JIDT for tiny `N`, because JIDT shuffling is already cheap there. At `N=100,000`, it is about 6x faster. At `N=1,000,000`, it is about 40x faster. At the `N=2,000,000` anchors, it is about 91x faster.

Accuracy against JIDT is strong: median absolute p-value error is about `0.01`, which is close to the Monte Carlo noise expected from `K=1000`. Chi-squared is much worse across these sparse/large-alphabet regimes, with median absolute errors around `0.24`.

The strongest regimes for empirical table sampling are strongly skewed, extremely skewed, and Zipf-heavy marginals. These are exactly the regimes where chi-squared often becomes badly miscalibrated.

Gamma remains useful as a cheap smoothed approximation in many cases, but it should not replace empirical table sampling for sparse discrete tables because it cannot represent exact point masses and ties.

## Output Files

- Stress results: `SaddlepointValidation/outputs/empirical_table_validation_stress_k1000_tiefix/general_validation_results.csv`
- Stress summary: `SaddlepointValidation/outputs/empirical_table_validation_stress_k1000_tiefix/summary.md`
- Mega-anchor results: `SaddlepointValidation/outputs/empirical_table_validation_mega_k1000_tiefix/general_validation_results.csv`
- Mega-anchor summary: `SaddlepointValidation/outputs/empirical_table_validation_mega_k1000_tiefix/summary.md`

