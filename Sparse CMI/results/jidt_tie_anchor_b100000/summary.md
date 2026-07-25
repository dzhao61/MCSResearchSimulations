# JIDT Blockwise Anchor Comparison

JIDT blockwise orderings preserve both binary margins inside every conditioning stratum. JIDT's default global shuffle is reported separately and is not the same null in heterogeneous strata.

| Configuration | N | Route | Reference p | Router p | JIDT blockwise p (corrected) | JIDT raw p | JIDT default raw p | Router ms | JIDT blockwise ms | Speedup |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| homogeneous_k20_n10_both_skew | 200 | exact_convolution | 0.13295 | 0.13295 | 0.13285 | 0.10829 | 0.01332 | 0.252 | 457.275 | 1817.7x |

## Aggregate

- Median speedup versus JIDT blockwise permutation: 1817.7x.
- Median absolute p-value error: router 0.00000, JIDT blockwise 0.00010, chi-square nominal 0.05582.
- Maximum manual-versus-JIDT `G^2` difference: 4.263e-14.
- JIDT Monte Carlo p-values use `count / permutations`; with 100,000 permutations their resolution is 1e-05.
- JIDT's raw p-value uses an exact floating-point `>=` comparison. The corrected column recomputes the rank from JIDT's own surrogate values with a `G^2` tolerance of `1e-10`, so mathematically tied tables are counted together.
- Runtime is a steady-state comparison: JVM startup and a small JIT warmup are excluded; JIDT ordering construction and conversion are included. Router time is the mean of ten complete calls.
