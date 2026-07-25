# Saddlepoint MI Significance Testing Handoff

This document summarizes the current state of the saddlepoint mutual information
significance-testing experiment: the statistical problem, implemented algorithm,
validation results, runtime findings, limitations, and recommended next steps.

The short version:

- The exact-CGF saddlepoint method is statistically promising for small-to-moderate
  sparse/skewed discrete MI tables.
- In the original target regime (`N=50`, alphabets up to `8x3`), it agrees with
  JIDT permutation p-values much better than either nominal or dynamic
  chi-squared.
- The current exact fixed-margin DP implementation is not a universal faster
  replacement for JIDT.
- Runtime is good when fixed-margin support is small, often under strong skew.
- Runtime is bad when margins are dense or `N` is large, even for `2x2`.
- Larger alphabets on both sides are fundamentally out of scope for this exact DP
  unless a different approximation or specialized algorithm is added.

## 1. Research Problem

For two discrete variables, the plug-in mutual information test statistic is:

```text
G = 2N * I_hat
```

where `I_hat` must be in nats.

The standard analytical null approximation is:

```text
G ~ chi-squared(df = (r - 1)(c - 1))
```

This asymptotic approximation ignores the marginal distributions. It often fails
when:

- sample size is small,
- marginals are skewed,
- observed rows or columns are empty,
- the table is sparse.

JIDT's default `computeSignificance()` method avoids this by permutation/shuffling,
but it is Monte Carlo:

- runtime grows with observations times shuffles,
- tail resolution is limited by `1 / (shuffles + 1)`,
- high-shuffle tests can become expensive or hit Java heap limits.

The method tested here is a conditional fixed-margin saddlepoint method based on
the exact conditional cumulant-generating function (CGF) of `G`.

## 2. Methods Compared

The validation compares four p-value routes:

| Method | Description |
| --- | --- |
| `saddle_p` | Tiered exact/saddlepoint p-value under fixed observed margins. |
| `chi2_nominal_p` | Standard chi-squared using configured alphabet sizes. |
| `chi2_dynamic_p` | Chi-squared using observed nonempty rows and columns. |
| `jidt_p` | JIDT `MutualInformationCalculatorDiscrete.computeSignificance()`. |

JIDT is treated as the operational permutation baseline, not as exact truth.
For small shuffle counts it is noisy and has coarse tail resolution.

## 3. Repository Artifacts

Main files:

| Path | Purpose |
| --- | --- |
| `SaddlepointValidation/saddlepoint_cgf.py` | Exact fixed-margin CGF, exact tails, saddlepoint p-values. |
| `SaddlepointValidation/jidt_utils.py` | JIDT bridge and manual-vs-JIDT `G` check support. |
| `SaddlepointValidation/run_validation.py` | Grid runner comparing saddlepoint, chi-squared, and JIDT. |
| `SaddlepointValidation/validation_checks.py` | Correctness checks. |
| `SaddlepointValidation/high_shuffle_anchors.py` | Higher-shuffle JIDT anchor comparisons. |
| `SaddlepointValidation/long_jidt_case.py` | One-case timing runner for larger `N` / alphabet stress tests. |
| `SaddlepointValidation/README.md` | Basic usage notes. |

Important outputs:

| Path | Purpose |
| --- | --- |
| `SaddlepointValidation/outputs/optimization_benchmark/` | Main optimized focused benchmark. |
| `SaddlepointValidation/outputs/optimization_high_shuffle_anchors/` | 10,000-shuffle anchor checks. |
| `SaddlepointValidation/outputs/long_jidt_benchmark/` | Larger-`N` runtime experiments. |
| `SaddlepointValidation/outputs/focused_hardened/` | Earlier hardened focused benchmark before the general optimization pass. |

## 4. Algorithm Summary

### 4.1 Statistic

The implementation computes:

```text
G = 2 * sum_ij n_ij * log(n_ij * N / (n_i. * n_.j))
```

This is equivalent to `2N * I_hat` in nats.

The JIDT bridge computes MI in bits and converts to nats by multiplying by
`log(2)`. Correctness checks verified that the manual `G` and JIDT `G` match to
approximately `1e-10` or better.

### 4.2 Fixed-Margin Conditional Null

The saddlepoint method conditions on observed row and column totals. Under the
null of independence with fixed margins, the probability of a table is
multivariate hypergeometric:

```text
P(table | margins) proportional to prod_i row_i! * prod_j col_j! / (N! * prod_ij n_ij!)
```

The implementation computes the conditional CGF:

```text
K(s) = log E[exp(sG) | row totals, column totals]
```

Then:

- if the number of feasible tables is small enough, it computes the exact tail;
- otherwise it uses Lugannani-Rice saddlepoint approximation for the upper tail.

### 4.3 Dynamic Programming Structure

The DP processes rows one at a time.

State:

```text
remaining column capacities
```

For each row, it enumerates all feasible allocations of that row total across
the remaining columns. Each allocation creates a transition from one remaining
capacity vector to the next.

The code transposes internally so the smaller side is the column/state side:

```text
d = min(r, c)
m = max(r, c)
```

This is important because DP state size grows very quickly with `d`.

### 4.4 P-Value Route

For each observed table:

1. Drop empty rows and columns.
2. Compute `G`.
3. Build the conditional CGF object from nonempty row and column totals.
4. Count support up to `exact_table_limit`.
5. If support is below the limit, compute exact conditional p-value.
6. Otherwise use saddlepoint approximation.
7. Also compute nominal and dynamic chi-squared p-values.
8. Optionally call JIDT `computeSignificance()`.

## 5. Complexity and Scaling

### 5.1 JIDT Significance Testing

JIDT permutation/shuffling cost is roughly:

```text
time ~= O(S * N)
```

where:

- `S` is the number of shuffles,
- `N` is the number of observations.

It does not directly care much about fixed-margin support. It shuffles the
observation sequence. In our tests, alphabet size below `100x100` mattered less
than `N`.

JIDT can hit Java heap limits for large `N * S`, depending on JVM heap and JIDT's
internal surrogate distribution storage.

### 5.2 Exact-CGF DP

The DP cost is governed by the number of feasible states and transitions:

```text
setup time ~= O(T)
p-value time ~= O(L * T)
memory ~= O(T)
```

where:

- `T` is the number of DP transitions,
- `L` is the number of CGF evaluations needed by root finding, often about
  `10-30`.

The number of states is bounded by the number of possible remaining column
capacity vectors. For dense margins and smaller dimension `d`:

```text
states per layer roughly grow like O(N^(d - 1))
row allocations roughly grow like O(N^(d - 1))
naive transitions can approach O(m * N^(2d - 2))
```

This is only a rough dense-regime bound, but it explains the observed behavior:

| Smaller side `d` | Practical meaning |
| ---: | --- |
| `2` | Should be manageable with specialized code, but current generic DP gets slow at large `N`. |
| `3` | Works for small/moderate `N`, especially skewed margins. |
| `10` | Generally not feasible exactly with this DP. |
| `80` | Completely out of scope for exact DP. |

### 5.3 Key Scaling Distinction

JIDT scales with:

```text
observations x shuffles
```

The saddlepoint implementation scales with:

```text
fixed-margin support / DP transition graph size
```

This means either method can be faster depending on regime. The saddlepoint
method is not automatically faster just because JIDT has many observations.

## 6. Correctness Checks Performed

Command:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
.venv/bin/python SaddlepointValidation/validation_checks.py
```

Result:

```text
All saddlepoint validation checks passed.
```

Checks included:

- exact enumeration cross-checks for small tables,
- `K(0)`, `K'(0)`, and `K''(0)` against exact distributions,
- monotonicity of saddlepoint p-values,
- left-of-mean p-value regression,
- JIDT statistic check: manual `G` and JIDT `G` match within tolerance.

The maximum manual-vs-JIDT `G` difference in the optimized focused benchmark was:

```text
2.03e-14
```

## 7. Implementation Hardening and Optimizations

Implemented hardening:

- fixed left-of-mean saddlepoint p-value bug,
- clipped invalid p-values to `[0, 1]`,
- added saddlepoint root diagnostics,
- added full table/margin JSON fields for each replicate,
- added dynamic chi-squared p-values,
- added JIDT p-value floor and manual-vs-JIDT `G` diagnostics,
- added support count status instead of capped support count ambiguity.

Implemented general optimization pass:

- vectorized log-factorials with `scipy.special.gammaln`,
- changed transition layers from Python tuple lists to typed NumPy arrays,
- vectorized grouped reductions in `K_moments()`,
- added canonical-margin CGF caching,
- added per-configuration checkpoints,
- added `--resume`,
- added optional `--workers` for non-JIDT parallel calibration screens,
- added `JIDT_JVM_ARGS` support for JVM heap options.

Optimization benchmark result:

```text
old median saddle/exact time: 0.00273s
new median saddle/exact time: 0.000966s
median speedup: 1.80x
mean speedup: 5.81x
```

Largest speedups were dense balanced focused-grid cases:

| Config | Old median saddle time | New median saddle time | Speedup |
| --- | ---: | ---: | ---: |
| `8x3_N50_balanced` | `0.2120s` | `0.01234s` | `17.18x` |
| `6x3_N50_balanced` | `0.2067s` | `0.01402s` | `14.75x` |
| `3x3_N50_balanced` | `0.1337s` | `0.01139s` | `11.74x` |
| `8x3_N50_mild` | `0.01520s` | `0.001654s` | `9.19x` |
| `6x3_N50_mild` | `0.01421s` | `0.001627s` | `8.74x` |

Small exact-route cases changed little.

## 8. Focused Accuracy Benchmark

Focused benchmark:

```bash
.venv/bin/python SaddlepointValidation/run_validation.py \
  --profile focused \
  --replicates 100 \
  --jidt-replicates 10 \
  --shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/optimization_benchmark \
  --exact-table-limit 1000
```

Grid:

- shapes: `2x2`, `3x3`, `6x3`, `8x3`,
- `N = 50`,
- skewness: balanced, mild, strong,
- 100 analytical replicates per configuration,
- 10 JIDT replicates per configuration,
- 1000 JIDT shuffles.

Overall calibration:

| alpha | Saddle mean abs FPR error | Nominal chi2 error | Dynamic chi2 error | JIDT error |
| ---: | ---: | ---: | ---: | ---: |
| `0.10` | `0.0350` | `0.0725` | `0.0592` | `0.0750` |
| `0.05` | `0.0200` | `0.0350` | `0.0333` | `0.0583` |
| `0.01` | `0.0075` | `0.00917` | `0.00917` | `0.0300` |

Median p-value agreement against JIDT:

```text
saddle/exact median absolute error: 0.00856
nominal chi2 median absolute error: 0.1166
dynamic chi2 median absolute error: 0.1089
```

Saddlepoint/exact was closer to JIDT than both chi-squared variants on a median
fraction of:

```text
1.00
```

Interpretation:

- In the original small-`N` target regime, saddlepoint/exact is much closer to
  JIDT than chi-squared.
- This is especially useful when marginals are skewed.
- Balanced cases still benefit in p-value agreement but are less compelling
  because chi-squared is less catastrophically wrong and the DP can be denser.

## 9. Runtime by Skewness in Focused Benchmark

Median values across focused configurations:

| Skewness | Median saddle time | Median JIDT time | Saddle MAE vs JIDT | Nominal chi2 MAE vs JIDT |
| --- | ---: | ---: | ---: | ---: |
| balanced | `0.0119s` | `0.000654s` | `0.0102` | `0.0912` |
| mild | `0.00164s` | `0.000518s` | `0.00954` | `0.1148` |
| strong | `0.000211s` | `0.000443s` | `0.00613` | `0.1837` |

Interpretation:

- Strong skew usually reduces fixed-margin support, so saddlepoint can become
  very fast.
- Strong skew is also where chi-squared p-values are most wrong.
- Balanced dense cases are slower for saddlepoint and less urgent statistically.

## 10. High-Shuffle Anchor Checks

Three skewed anchors were rerun with 10,000 JIDT shuffles:

| Config | Saddle p | JIDT p | Nominal chi2 p | Dynamic chi2 p | JIDT time |
| --- | ---: | ---: | ---: | ---: | ---: |
| `8x3_N50_strong` | `0.1066` | `0.1061` | `0.9110` | `0.2722` | `0.0135s` |
| `6x3_N50_strong` | `0.1200` | `0.1267` | `0.8699` | `0.0705` | `0.0051s` |
| `2x2_N50_strong` | `1.0000` | `1.0000` | `0.3625` | `0.3625` | `0.0043s` |

Median absolute errors on these anchors:

```text
saddle/exact: 0.00048
nominal chi2: 0.743
dynamic chi2: 0.166
```

Interpretation:

- Saddlepoint/exact tracks high-shuffle JIDT closely in these skewed small-`N`
  cases.
- Both chi-squared variants can be severely wrong.

## 11. Fair Runtime Comparison Against JIDT

After correcting earlier flawed stress tests, the fair comparison required:

- both methods completed,
- no saddlepoint skip,
- no short saddlepoint timeout,
- fixed JIDT shuffles at `1000`.

Results:

| Alphabet | N | Shuffles | Saddle time | JIDT time | Saddle / JIDT | Saddle p | JIDT p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `2x2` | `10,000` | `1000` | `0.167s` | `0.160s` | `1.04x` | `0.6983` | `0.757` |
| `2x2` | `20,000` | `1000` | `0.587s` | `0.200s` | `2.94x` | `0.6314` | `0.473` |
| `2x2` | `30,000` | `1000` | `1.323s` | `0.424s` | `3.12x` | `0.0312` | `0.036` |
| `2x2` | `50,000` | `1000` | `3.715s` | `0.602s` | `6.18x` | `0.6060` | `0.445` |
| `2x2` | `100,000` | `1000` | `14.878s` | `1.452s` | `10.25x` | `0.2881` | `0.323` |
| `3x2` | `50,000` | `1000` | `6.072s` | `0.601s` | `10.11x` | `0.1985` | `0.220` |

Interpretation:

- With the current exact-DP implementation, saddlepoint is not faster than JIDT
  at `1000` shuffles once `N` grows.
- It is roughly tied around `2x2, N=10,000`.
- It becomes increasingly slower as fixed-margin support grows.
- This is a real implementation/algorithm scaling problem, not a benchmark
  timeout artifact.

## 12. Larger-`N` JIDT Stress Tests

These tests used fixed `1000` JIDT shuffles and alphabets below `100x100`.

| Alphabet | N | Skewness | Shuffles | JVM heap | JIDT time | Saddle status |
| --- | ---: | --- | ---: | --- | ---: | --- |
| `20x3` | `1,000,000` | strong | `1000` | `4GB` | `13.759s` | timeout guard in stress script |
| `80x20` | `1,000,000` | strong | `1000` | `4GB` | `14.047s` | timeout guard in stress script |
| `80x80` | `1,000,000` | balanced | `1000` | `4GB` | `12.724s` | skipped |
| `20x3` | `2,000,000` | strong | `1000` | `8GB` | `34.475s` | timeout guard in stress script |
| `50x10` | `2,000,000` | mild | `1000` | `8GB` | `29.966s` | skipped |
| `80x80` | `2,000,000` | balanced | `1000` | `8GB` | `31.336s` | skipped |

Important caveat:

These are **not** fair saddlepoint-vs-JIDT comparisons. They show where JIDT
becomes expensive under reasonable `N` and alphabet sizes, but the current
saddlepoint implementation did not complete or was skipped for several of these
cases.

## 13. Balanced vs Skewed Marginal Interpretation

The current method is best described as:

```text
promising for small-to-moderate, skewed/sparse, low-dimensional discrete tables
```

It is not best described as:

```text
a general faster replacement for JIDT
```

Good regime:

| Property | Why it helps |
| --- | --- |
| small/moderate `N` | fixed-margin support remains tractable |
| skewed/sparse marginals | fewer feasible tables and chi-squared is more wrong |
| smaller side has `2-3` categories | DP state dimension remains low |
| high need for deterministic p-values | avoids JIDT Monte Carlo floor |

Bad regime:

| Property | Why it hurts |
| --- | --- |
| very large `N` | row/column margins create huge fixed-margin support |
| balanced dense margins | many feasible tables |
| both sides have many categories | DP state dimension explodes |
| chi-squared already adequate | saddlepoint accuracy gain may not justify cost |

## 14. What Went Wrong in Earlier Runtime Thinking

Some earlier stress tests were not fair comparisons because saddlepoint was
skipped or capped while JIDT was timed. Those tests are still useful as JIDT
scaling probes, but they should not be used to claim saddlepoint speedups.

The corrected fair-runtime table is Section 11.

The key corrected conclusion:

```text
Current saddlepoint/exact implementation is accurate in the target small-N
regime, but it is not currently faster than JIDT for large-N fair comparisons at
1000 shuffles.
```

## 15. Fundamental Limitations vs Fixable Limitations

| Limitation | Type | Explanation |
| --- | --- | --- |
| `2x2` slow at large `N` | fixable implementation issue | Binary-side tables should not need the generic transition graph. |
| `r x 2` slow at large `N` | fixable with specialized kernel | Can use one-dimensional hypergeometric-style support. |
| `r x 3` moderately slow | partly fixable | Dense 2D arrays, compiled kernels, and better recurrences may help. |
| `50x10` exact DP infeasible | mostly fundamental | Smaller side dimension `10` makes exact state space too large. |
| `80x80` exact DP infeasible | fundamental | Exact fixed-margin DP is the wrong tool. |
| JIDT heap errors at very large `N*S` | JIDT implementation/resource limit | Can sometimes be mitigated with JVM heap, but not eliminated. |

## 16. Recommendations for Next Human/Agent

### Priority 1: Implement a specialized binary-side method

For `2x2` and `r x 2`, do not use the generic transition graph.

Reason:

- The fair runtime table shows current generic DP becomes slower than JIDT as
  `N` grows.
- Binary-side fixed-margin distributions should admit much cheaper 1D recurrences.
- This is the best chance of turning the method into a genuine JIDT runtime win
  in a meaningful regime.

Target:

```text
2x2 and r x 2 should be near O(N) or O(number of feasible binary allocations),
not generic graph construction over row allocation/state transitions.
```

Validation:

- compare against current generic DP at small `N`,
- compare against exact enumeration where possible,
- compare against JIDT at `N=10k`, `50k`, `100k`, `500k`,
- keep JIDT shuffles fixed at `1000` and possibly `5000`.

### Priority 2: Add a tractability estimator before running saddlepoint

Before constructing `CondCGF`, estimate expected state/transition size.

If estimated cost is too high:

- route to JIDT,
- route to chi-squared/gamma approximation,
- or report "not tractable for exact-CGF saddlepoint".

This avoids silent long hangs.

### Priority 3: Specialize `d = 3`

For smaller side dimension `3`, replace tuple/dict graph construction with a
dense or sparse 2D kernel.

This may substantially expand the useful regime for `r x 3` tables.

### Priority 4: Do not pursue exact DP for large two-sided alphabets

For `50x10`, `80x80`, etc., exact fixed-margin DP is not the right direction.

Possible alternatives:

- analytic moment-matched gamma,
- approximate saddlepoint using analytic cumulants,
- category pooling,
- sparse/low-rank approximations,
- JIDT/permutation fallback,
- asymptotic corrections using observed margins.

### Priority 5: Make the benchmark suite enforce fair comparisons

A fair runtime comparison must record:

- whether saddlepoint completed,
- whether JIDT completed,
- whether either method hit memory/time limits,
- JIDT shuffles,
- JVM heap,
- exact route vs saddlepoint route,
- support count/status,
- observed nonempty dimensions.

Rows where one method was skipped should be reported separately as stress tests,
not runtime comparisons.

## 17. Suggested Future Benchmark Grid

Use three categories of benchmarks.

### A. Accuracy target grid

Purpose: validate p-values.

```text
N: 20, 50, 100, 200
shapes: 2x2, 3x2, 3x3, 6x3, 8x3
skewness: balanced, mild, strong
JIDT shuffles: 5000 or 10000 anchors
```

### B. Fair runtime grid

Purpose: compare saddlepoint and JIDT only where both complete.

```text
shuffles: fixed at 1000
shapes: 2x2, 3x2, 6x2, 10x2, 3x3
N ladder: 1000, 5000, 10000, 20000, 50000, 100000
skewness: mild, strong
```

### C. Routing stress grid

Purpose: decide when to route away from exact DP.

```text
shapes: 20x3, 50x10, 80x80
N: 100000, 1000000
shuffles: 1000
```

Do not mix routing stress rows into fair runtime claims.

## 18. Bottom-Line Conclusion

The saddlepoint/exact-CGF approach has real statistical value in the original
small-`N`, skewed-marginal problem:

- much closer to JIDT than chi-squared,
- deterministic p-values,
- no Monte Carlo floor,
- very fast when fixed-margin support is small.

However, the current generic exact-DP implementation does **not** yet deliver a
general runtime advantage over JIDT:

- it becomes slower than JIDT for large `N` even in `2x2`,
- it cannot handle large two-sided alphabets exactly,
- it needs specialized kernels and routing before it can be positioned as a
  practical replacement or supplement.

The next decisive engineering step is a specialized binary-side implementation.
If `2x2` / `r x 2` can be made fast at large `N`, the method may become valuable
as a targeted deterministic alternative to JIDT in skewed low-dimensional MI
testing. If not, its role should be limited to small-support exact/saddlepoint
correction and as a proof-of-concept for future analytic approximations.

## 19. New Generalization Direction: Fixed-Margin Table Sampling + Gamma

After deciding that exact DP is unlikely to become a general large-alphabet
solution, a new prototype was added:

| Path | Purpose |
| --- | --- |
| `SaddlepointValidation/general_fixed_margin.py` | Fixed-margin table sampler and moment-matched gamma p-value. |
| `SaddlepointValidation/run_general_approx.py` | One-case runner. |
| `SaddlepointValidation/run_general_validation.py` | Grid validation runner. |

This method uses `scipy.stats.random_table` to sample contingency tables directly
from the fixed-margin null distribution. This is much closer to JIDT's
permutation null than unconditional multinomial bootstrap, but it avoids
shuffling raw observations.

For each observed table:

1. Drop empty margins.
2. Compute observed `G`.
3. Sample `K` fixed-margin null tables.
4. Compute `G` for each sampled table.
5. Estimate empirical fixed-margin p-value from those sampled tables.
6. Estimate mean and variance of `G`.
7. Fit a gamma distribution by moment matching.
8. Compute `gamma_fixed_margin_p`.

This is not the exact-CGF saddlepoint method. It is a general fixed-margin Monte
Carlo/moment-matching approximation.

### 19.1 Smoke Validation

Smoke command:

```bash
JIDT_JVM_ARGS=-Xmx4g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile smoke \
  --replicates 3 \
  --samples 5000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/general_validation_smoke
```

Overall result:

| Metric | Value |
| --- | ---: |
| Rows | `12` |
| Median gamma/table-sampling time | `0.0788s` |
| Median JIDT time | `0.523s` |
| Median speedup vs JIDT | `4.42x` |
| Median abs gamma vs JIDT | `0.0127` |
| Median abs dynamic chi2 vs JIDT | `0.121` |

Important per-config result:

| Config | Gamma time | JIDT time | Gamma vs JIDT error | Dynamic chi2 vs JIDT error |
| --- | ---: | ---: | ---: | ---: |
| `20x3_N10000_strong` | `0.0136s` | `0.121s` | `0.00386` | `0.123` |
| `50x10_N100000_mild` | `0.144s` | `1.207s` | `0.0183` | `0.0390` |
| `80x80_N100000_balanced` | `2.035s` | `1.074s` | `0.00824` | `0.187` |
| `8x3_N50_strong` | `0.0030s` | `0.00175s` | `0.240` | `0.168` |

Interpretation:

- The general gamma approximation is promising in moderate/large regimes.
- It can fail badly on tiny sparse/discrete regimes such as `8x3_N50_strong`.
- In tiny regimes, the empirical fixed-margin p-value or exact/saddlepoint route
  should be preferred over gamma.

### 19.2 Targeted Validation

Targeted command:

```bash
JIDT_JVM_ARGS=-Xmx4g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile targeted \
  --replicates 2 \
  --samples 5000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/general_validation_targeted
```

Grid:

- `8x3, N=50`
- `20x3, N=10000`
- `50x10, N=100000`
- `80x80, N=100000`
- balanced, mild, and strong skewness

Overall result:

| Metric | Value |
| --- | ---: |
| Rows | `24` |
| Median gamma/table-sampling time | `0.0770s` |
| Median JIDT time | `0.569s` |
| Median speedup vs JIDT | `3.02x` |
| Median abs gamma vs empirical table p | `0.00377` |
| Median abs dynamic chi2 vs empirical table p | `0.0598` |
| Median abs gamma vs JIDT | `0.0112` |
| Median abs dynamic chi2 vs JIDT | `0.0540` |

Interpretation:

- Across this mixed grid, gamma was closer to JIDT than dynamic chi-squared at
  the median.
- It was also faster than JIDT at the median.
- It was not faster for all configs. `80x80_N100000` had table-sampling overhead
  comparable to or slower than JIDT.
- Tiny `N=50` skewed cases remain problematic for gamma.

### 19.3 Large Validation

Large command:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile large \
  --replicates 1 \
  --samples 5000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/general_validation_large
```

Grid:

- `20x3, N=2,000,000, strong`
- `50x10, N=2,000,000, mild`
- `80x80, N=1,000,000, balanced`

Overall result:

| Metric | Value |
| --- | ---: |
| Rows | `3` |
| Median gamma/table-sampling time | `0.234s` |
| Median JIDT time | `30.5s` |
| Median speedup vs JIDT | `139x` |
| Median abs gamma vs empirical table p | `0.00163` |
| Median abs gamma vs JIDT | `0.0150` |
| Median abs dynamic chi2 vs JIDT | `0.00226` |

Per-config:

| Config | Gamma time | JIDT time | Speedup | Gamma vs JIDT error | Dynamic chi2 vs JIDT error |
| --- | ---: | ---: | ---: | ---: | ---: |
| `20x3_N2000000_strong` | `0.0188s` | `30.5s` | `1625x` | `0.0124` | `0.00226` |
| `50x10_N2000000_mild` | `0.234s` | `32.6s` | `139x` | `0.0186` | `0.0169` |
| `80x80_N1000000_balanced` | `3.162s` | `10.6s` | `3.35x` | `0.0150` | `0.00210` |

Interpretation:

- For large `N`, fixed-margin table sampling is dramatically faster than JIDT.
- Gamma matches the empirical table-sampling p-value closely.
- However, in large asymptotic regimes, dynamic chi-squared can already be very
  accurate, sometimes closer to JIDT than gamma.
- This means the general method should not automatically replace chi-squared in
  all large-`N` regimes. It should be routed by diagnostics.

## 20. Updated General-Solution Recommendation

The best general path is now:

```text
fixed-margin table sampling + empirical p-value + moment-matched gamma
```

not exact DP saddlepoint.

Recommended router:

```text
if support is tiny:
    exact conditional p-value
elif exact-CGF saddlepoint is tractable:
    exact/saddlepoint p-value
elif table-sampling gamma agrees with empirical table-sampling diagnostics:
    gamma_fixed_margin_p
elif table-sampling itself is cheap enough:
    empirical_fixed_margin_p
elif N is large and expected counts are high:
    dynamic chi-squared may be sufficient
else:
    adaptive JIDT/permutation fallback
```

Key research question now:

```text
Can we predict when the gamma fit to fixed-margin table samples is reliable?
```

Potential diagnostics:

- gamma p-value vs empirical table-sampling p-value disagreement,
- null skewness/kurtosis from sampled `G` values,
- number of distinct `G` values / discreteness,
- minimum expected cell count,
- observed nonempty dimensions,
- effective sample size in rare cells.

This route is much more general than exact DP because it can handle large
alphabets and large `N`. It is still Monte Carlo, but it samples count tables
directly rather than shuffling raw observations, which can be much faster in
large datasets.
