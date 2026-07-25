# Optimization Benchmark: Saddlepoint vs JIDT

Run:

```bash
.venv/bin/python SaddlepointValidation/run_validation.py \
  --profile focused \
  --replicates 100 \
  --jidt-replicates 10 \
  --shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/optimization_benchmark \
  --exact-table-limit 1000
```

Additional timing screens:

- No-JIDT serial: `5.73s` wall time for `1,200` analytical evaluations.
- No-JIDT with four workers: `3.31s` wall time for the same workload.
- JIDT subset benchmark: `7.09s` wall time for `1,200` analytical evaluations plus `120` JIDT calls with `1,000` shuffles.

## Speed

Compared with the earlier `focused_hardened` run, the optimized median saddlepoint/exact runtime improved from `0.00273s` to `0.000966s` per table: median speedup `1.80x`, mean speedup `5.81x`.

The biggest wins were the dense balanced configurations:

| config | old median saddle s | new median saddle s | speedup |
| --- | ---: | ---: | ---: |
| `8x3_N50_balanced` | `0.2120` | `0.01234` | `17.18x` |
| `6x3_N50_balanced` | `0.2067` | `0.01402` | `14.75x` |
| `3x3_N50_balanced` | `0.1337` | `0.01139` | `11.74x` |
| `8x3_N50_mild` | `0.01520` | `0.001654` | `9.19x` |
| `6x3_N50_mild` | `0.01421` | `0.001627` | `8.74x` |

Small exact-route cases changed little, and a few moved slightly slower because array setup overhead can dominate microsecond-scale exact tables.

## JIDT Agreement

With `1,000` shuffles and `10` JIDT replicates per configuration:

- Median absolute p-value error vs JIDT: saddlepoint/exact `0.00856`.
- Median absolute p-value error vs JIDT: nominal chi-squared `0.1166`.
- Median absolute p-value error vs JIDT: dynamic chi-squared `0.1089`.
- Median chi-squared error was about `13.1x` larger than saddlepoint/exact error.
- Saddlepoint/exact was closer to JIDT than both chi-squared variants on a median fraction of `1.00` across configurations.
- Max manual-vs-JIDT `G` difference: `2.03e-14`.
- Saddlepoint error rows: `0 / 1200`.

## High-Shuffle Anchors

Three skewed anchors were rerun with `10,000` JIDT shuffles.

| config | saddle p | JIDT p | nominal chi2 p | dynamic chi2 p | JIDT time s | JIDT / median saddle |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `8x3_N50_strong` | `0.1066` | `0.1061` | `0.9110` | `0.2722` | `0.01354` | `44.4x` |
| `6x3_N50_strong` | `0.1200` | `0.1267` | `0.8699` | `0.07047` | `0.00506` | `21.4x` |
| `2x2_N50_strong` | `1.0000` | `1.0000` | `0.3625` | `0.3625` | `0.00427` | `81.3x` |

The median saddlepoint absolute error on these anchors was `0.00048`, versus `0.743` for nominal chi-squared and `0.166` for dynamic chi-squared. Two of three saddlepoint p-values were inside the JIDT 95% Monte Carlo interval; the remaining case was borderline with absolute difference `0.0067`.

## Interpretation

The optimization worked where it was supposed to: dense saddlepoint DP cases are now an order of magnitude faster. Low-shuffle JIDT can still be faster per table, especially at `1,000` shuffles, but it has coarse tail resolution. In higher-shuffle regimes, JIDT runtime scales with shuffles while saddlepoint/exact remains fixed, and saddlepoint retains much better agreement with JIDT than either chi-squared approximation.
