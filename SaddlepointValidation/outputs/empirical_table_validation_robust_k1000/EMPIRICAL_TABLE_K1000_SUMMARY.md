# Empirical Fixed-Margin Table Sampling vs JIDT vs Chi-Squared, K=1000

Both JIDT and empirical table sampling used `K=1000`. The empirical method samples fixed-margin contingency tables directly with `scipy.stats.random_table`, computes `G` on each sampled table, and reports the fraction with `G_sample >= G_observed`.

## Moderate Robust Grid

Grid: `72` configurations, `2` null replicates each: shapes `2x2`, `8x3`, `20x3`, `50x10`, `80x20`, `80x80`; `N = 50, 1000, 10000, 100000`; skewness balanced, mild, strong.

| metric | value |
| --- | ---: |
| `rows` | 144 |
| `configs` | 72 |
| `median_empirical_table_time_s` | 0.002953 |
| `median_jidt_time_s` | 0.04873 |
| `median_speedup` | 3.409 |
| `median_abs_empirical_vs_jidt` | 0.01217 |
| `median_abs_gamma_vs_jidt` | 0.01192 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.1063 |
| `median_abs_chi2_nominal_vs_jidt` | 0.1218 |
| `empirical_closer_than_dynamic_chi2_fraction` | 0.7917 |
| `empirical_closer_than_nominal_chi2_fraction` | 0.7917 |

### Moderate Grid By N

| N | rows | empirical time | JIDT time | speedup | empirical vs JIDT | chi2 dynamic vs JIDT |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 50 | 36 | 0.0009584s | 0.001034s | 0.7998x | 0.02641 | 0.2114 |
| 1000 | 36 | 0.005681s | 0.0105s | 2.209x | 0.01217 | 0.2013 |
| 10000 | 36 | 0.01224s | 0.08651s | 13.07x | 0.01118 | 0.04422 |
| 100000 | 36 | 0.01625s | 1.197s | 147.8x | 0.0107 | 0.01626 |

### Moderate Grid By Skewness

| skewness | rows | empirical time | JIDT time | speedup | empirical vs JIDT | chi2 dynamic vs JIDT | empirical closer fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| balanced | 48 | 0.00396s | 0.04873s | 3.323x | 0.01399 | 0.05807 | 0.729 |
| mild | 48 | 0.002414s | 0.04704s | 3.258x | 0.01428 | 0.09076 | 0.792 |
| strong | 48 | 0.001924s | 0.04551s | 4.117x | 0.01104 | 0.1805 | 0.854 |

### Moderate Grid Null Rejection Rates

| alpha | empirical | JIDT | chi2 nominal | chi2 dynamic | gamma |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.1 | 0.07639 | 0.09028 | 0.1736 | 0.1736 | 0.09028 |
| 0.05 | 0.04167 | 0.04861 | 0.1389 | 0.1389 | 0.04861 |
| 0.01 | 0 | 0 | 0.0625 | 0.0625 | 0.006944 |

## Large-N Anchor Grid

Grid: `9` configurations, `1` null replicate each: shapes `20x3`, `50x10`, `80x80`; `N = 1,000,000`; skewness balanced, mild, strong.

| metric | value |
| --- | ---: |
| `rows` | 9 |
| `configs` | 9 |
| `median_empirical_table_time_s` | 0.03437 |
| `median_jidt_time_s` | 11.36 |
| `median_speedup` | 330.6 |
| `median_abs_empirical_vs_jidt` | 0.009101 |
| `median_abs_gamma_vs_jidt` | 0.008566 |
| `median_abs_chi2_dynamic_vs_jidt` | 0.006465 |
| `median_abs_chi2_nominal_vs_jidt` | 0.006465 |
| `empirical_closer_than_dynamic_chi2_fraction` | 0.4444 |
| `empirical_closer_than_nominal_chi2_fraction` | 0.4444 |

### Large Grid Null Rejection Rates

| alpha | empirical | JIDT | chi2 nominal | chi2 dynamic | gamma |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.1 | 0.1111 | 0.1111 | 0.2222 | 0.2222 | 0.2222 |
| 0.05 | 0 | 0 | 0.2222 | 0.2222 | 0 |
| 0.01 | 0 | 0 | 0.1111 | 0.1111 | 0 |

## Takeaways

- Empirical fixed-margin table sampling is much closer to JIDT than chi-squared on the moderate robust grid.
- Runtime advantage grows strongly with `N` because table sampling avoids shuffling raw observations.
- At `N=50`, JIDT is so cheap that table sampling is not reliably faster, but empirical table p-values are still generally closer than chi-squared.
- At `N=100000`, the empirical method has about `148x` median speedup over JIDT in this run.
- At `N=1,000,000`, the empirical method has about `331x` median speedup over JIDT, but chi-squared is often already accurate in large asymptotic regimes.
- The strongest research claim is therefore: empirical fixed-margin table sampling is a fast, margin-aware replacement for JIDT in skewed/sparse finite-sample regimes, while chi-squared remains acceptable for very large well-behaved tables.
- Gamma is secondary. The empirical table p-value is the safer primary method when `K=1000` is affordable.