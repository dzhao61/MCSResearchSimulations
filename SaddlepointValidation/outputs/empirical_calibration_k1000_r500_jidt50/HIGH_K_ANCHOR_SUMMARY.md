# High-K Anchor Checks

Empirical fixed-margin table sampling was rerun with `K=100000`; JIDT was rerun with `K=10000` on five representative calibration tables.

Because empirical used 10x more null samples than JIDT here, wall-clock time is not an equal-K runtime comparison. The normalized per-null-draw speedup column is the fairer timing diagnostic for this anchor run.

| label | name | empirical_k1000_p | empirical_k100000_p | jidt_k1000_p | jidt_k10000_p | chi2_dynamic_p | abs_empirical_highk_vs_jidt_highk | abs_chi2_vs_jidt_highk | empirical_k100000_time_s | jidt_k10000_time_s | per_null_draw_speedup_empirical_vs_jidt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large_N_strong_low_tail | 100x50_N100000_strong | 0.001998 | 0.00241 | 0.003 | 0.0022 | 1 | 0.00020998 | 0.9978 | 20.353 | 9.657 | 4.7448 |
| near_alpha_05_strong | 50x20_N10000_strong | 0.041958 | 0.04532 | 0.049 | 0.0427 | 1 | 0.0026195 | 0.9573 | 3.7611 | 0.86729 | 2.306 |
| near_alpha_05_zipf_mild | 80x80_N10000_zipf_mild | 0.046953 | 0.04591 | 0.045 | 0.0461 | 1 | 0.00019046 | 0.9539 | 13.079 | 1.0432 | 0.7976 |
| large_N_extreme_tail | 100x50_N100000_extreme | 0.022977 | 0.02184 | 0.018 | 0.0181 | 1 | 0.0037398 | 0.9819 | 13.574 | 7.9794 | 5.8784 |
| balanced_small_expected_counts | 20x20_N1000_balanced | 0.031968 | 0.0435 | 0.045 | 0.0417 | 0.00036496 | 0.0017996 | 0.041335 | 0.97529 | 0.12573 | 1.2891 |

## Notes
- The high-K empirical values are consistent with the K=1000 empirical values within expected Monte Carlo variation.
- JIDT K=10000 is broadly consistent with empirical K=100000 on these anchors.
- Chi-squared remains badly wrong on the selected failure cases.
- Per null draw, empirical table sampling is faster than JIDT on most selected anchors, but can be slower for high-dimensional tables like `80x80` where scoring sampled tables is expensive.