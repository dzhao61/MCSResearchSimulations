# General Fixed-Margin Approximation Smoke Summary

Method: sample fixed-margin contingency tables with `scipy.stats.random_table`, estimate moments of `G`, fit a gamma null, and compare against JIDT `computeSignificance`.

| case | samples | gamma time | JIDT time | speedup | gamma p | table empirical p | JIDT p | chi2 p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `8x3_N50_strong` | 20000 | 0.005917s | 0.0103s | 1.7x | 0.5956 | 1 | 1 | 0.9976 |
| `80x80_N1000000_balanced_5k` | 5000 | 2.2s | 11.9s | 5.4x | 0.3198 | 0.3171 | 0.32 | 0.2941 |
| `80x80_N1000000_balanced` | 20000 | 9.051s | 12.67s | 1.4x | 0.316 | 0.3183 | 0.293 | 0.2941 |
| `50x10_N2000000_mild_5k` | 5000 | 0.1847s | 33.07s | 179.1x | 0.11 | 0.1076 | 0.116 | 0.1081 |
| `20x3_N2000000_strong_5k` | 5000 | 0.01962s | 35.5s | 1809.3x | 0.9177 | 0.9164 | 0.911 | 0.9135 |

Interpretation:
- This is not the exact-DP saddlepoint method. It is a general fixed-margin table-sampling + moment-matched gamma approximation.
- It matches JIDT's fixed-margin permutation null more directly than an unconditional multinomial bootstrap.
- On large-`N` cases, it can be orders of magnitude faster than JIDT because it samples tables rather than shuffling raw observations.
- The gamma p-value should be validated more broadly before treating it as final; the empirical table-sampling p-value is a useful diagnostic baseline.