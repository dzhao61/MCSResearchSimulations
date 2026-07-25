# Reasonable Fixed-1000-Shuffle JIDT Timing Summary

All rows use JIDT `computeSignificance(1000)` with alphabet sizes below `100x100`.

| alphabet | N | skewness | shuffles | heap | JIDT time s | JIDT p | saddle status | G diff |
| --- | ---: | --- | ---: | --- | ---: | ---: | --- | ---: |
| `20x3` | 1000000 | strong | 1000 | 4GB | 13.759 | 0.023 | timeout >3s | 2.96e-12 |
| `80x20` | 1000000 | strong | 1000 | 4GB | 14.047 | 0.262 | timeout >3s | 3.41e-12 |
| `80x80` | 1000000 | balanced | 1000 | 4GB | 12.724 | 0.703 | skipped | 1.64e-11 |
| `20x3` | 2000000 | strong | 1000 | 8GB | 34.475 | 0.935 | timeout >3s | 2.37e-12 |
| `50x10` | 2000000 | mild | 1000 | 8GB | 29.966 | 0.112 | skipped | 2.93e-10 |
| `80x80` | 2000000 | balanced | 1000 | 8GB | 31.336 | 0.172 | skipped | 1.73e-11 |

Notes:
- With the same fixed `1000` shuffles and a `4GB` JVM heap, JIDT succeeded at `N=1,000,000` in about `13-14s` but hit Java heap errors at `N=2,000,000` for `20x3`.
- Giving the JVM `8GB` heap allowed `N=2,000,000` cases to complete around `30-35s`.
- The current exact-CGF saddlepoint implementation timed out on the `20x3, N=2,000,000` case and was skipped for wider alphabets. These timing rows therefore show when JIDT becomes expensive under reasonable data sizes, not a claim that the current saddlepoint kernel is fast in those large-N regimes.