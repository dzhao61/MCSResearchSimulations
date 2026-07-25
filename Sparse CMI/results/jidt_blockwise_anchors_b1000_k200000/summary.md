# JIDT Blockwise Anchor Comparison

JIDT blockwise orderings preserve both binary margins inside every conditioning stratum. JIDT's default global shuffle is reported separately and is not the same null in heterogeneous strata.

| Configuration | N | Route | Reference p | Router p | JIDT blockwise p (corrected) | JIDT raw p | JIDT default raw p | Router ms | JIDT blockwise ms | Speedup |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| homogeneous_k20_n10_both_skew | 200 | exact_convolution | 0.13295 | 0.13295 | 0.13200 | 0.10700 | 0.01300 | 0.275 | 6.733 | 24.5x |
| dominant_stratum_k100 | 360 | exact_convolution | 0.05621 | 0.05621 | 0.04900 | 0.04800 | 0.46000 | 2.934 | 6.790 | 2.3x |
| homogeneous_k10_n30_balanced | 300 | saddlepoint | 0.04995 | 0.05055 | 0.05800 | 0.05800 | 0.04100 | 0.864 | 6.921 | 8.0x |
| homogeneous_k50_n30_both_skew | 1500 | saddlepoint | 0.05593 | 0.05230 | 0.06800 | 0.06800 | 0.02800 | 0.948 | 31.368 | 33.1x |
| homogeneous_k100_n30_balanced | 3000 | saddlepoint | 0.05061 | 0.05047 | 0.05000 | 0.05000 | 0.05600 | 1.702 | 68.692 | 40.4x |
| heterogeneous_k100_v1 | 1360 | saddlepoint | 0.04604 | 0.04641 | 0.03700 | 0.03700 | 0.04900 | 2.532 | 26.763 | 10.6x |

## Aggregate

- Median speedup versus JIDT blockwise permutation: 17.5x.
- Median absolute p-value error: router 0.00026, JIDT blockwise 0.00763, chi-square nominal 0.04875.
- Maximum manual-versus-JIDT `G^2` difference: 1.421e-13.
- JIDT Monte Carlo p-values use `count / permutations`; with 1,000 permutations their resolution is 0.001.
- JIDT's raw p-value uses an exact floating-point `>=` comparison. The corrected column recomputes the rank from JIDT's own surrogate values with a `G^2` tolerance of `1e-10`, so mathematically tied tables are counted together.
- Runtime is a steady-state comparison: JVM startup and a small JIT warmup are excluded; JIDT ordering construction and conversion are included. Router time is the mean of ten complete calls.
- Explicit blockwise orderings use the recorded NumPy seed. JIDT's default-global overload owns its RNG and is retained as a non-reproducible diagnostic baseline only.
