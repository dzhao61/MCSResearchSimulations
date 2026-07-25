# Fair Saddlepoint vs JIDT Runtime Summary

All rows use both methods to completion: no saddlepoint skip, no short timeout, JIDT `computeSignificance(1000)`.

| alphabet | N | shuffles | saddle time s | JIDT time s | saddle / JIDT | saddle p | JIDT p | abs p diff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `2x2` | 10000 | 1000 | 0.167 | 0.160 | 1.04x | 0.6983 | 0.757 | 0.05875 |
| `2x2` | 20000 | 1000 | 0.587 | 0.200 | 2.94x | 0.6314 | 0.473 | 0.1584 |
| `2x2` | 30000 | 1000 | 1.323 | 0.424 | 3.12x | 0.03121 | 0.036 | 0.004792 |
| `2x2` | 50000 | 1000 | 3.715 | 0.602 | 6.18x | 0.606 | 0.445 | 0.161 |
| `2x2` | 100000 | 1000 | 14.878 | 1.452 | 10.25x | 0.288 | 0.323 | 0.03495 |
| `3x2` | 50000 | 1000 | 6.072 | 0.601 | 10.11x | 0.1985 | 0.22 | 0.02153 |

Interpretation:
- At `2x2, N=10k`, saddlepoint and JIDT are roughly tied at `1000` shuffles.
- By `N=20k-100k`, the current saddlepoint DP is slower than JIDT, increasingly so as margins grow.
- This is a limitation of the current exact fixed-margin DP implementation, not a timeout artifact in these rows.