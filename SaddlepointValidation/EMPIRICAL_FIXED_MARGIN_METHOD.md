# Empirical Fixed-Margin Table Sampling for MI Significance

This document describes the current most promising general method for mutual-information significance testing in this project.

The short version:

- Use the observed contingency table.
- Keep its row totals and column totals fixed.
- Sample new contingency tables from the exact fixed-margin independence null.
- Compute `G = 2N * MI` for each sampled table.
- Estimate the p-value by the fraction of sampled null tables with `G >= G_obs`.

This is a direct table-level analogue of JIDT permutation testing. It targets the same fixed-margin null distribution, but avoids repeatedly shuffling raw observation arrays of length `N`.

## Why This Method Exists

The standard analytic test uses

```text
G = 2N * I_hat ~ chi-squared(df = (r - 1)(c - 1))
```

asymptotically under independence.

This works well for large, balanced, well-populated tables. It can fail badly when:

- the alphabet is large,
- the sample size is modest relative to the number of cells,
- the marginals are skewed,
- many expected cell counts are tiny,
- many rows or columns are rare or empty.

JIDT's default `computeSignificance` avoids the chi-squared approximation by shuffling observations. That is statistically safer, but runtime scales strongly with the raw sample size `N`.

Empirical fixed-margin table sampling keeps the statistical target of JIDT shuffling, but samples contingency tables directly. This makes it much faster for large `N`.

## Null Distribution

Given an observed table `T` with row totals `r_i`, column totals `c_j`, and total sample size `N`, the fixed-margin null is:

```text
all contingency tables U such that
sum_j U_ij = r_i
sum_i U_ij = c_j
sum_ij U_ij = N
```

with probability

```text
P(U | row totals, column totals)
  = prod_i(r_i!) * prod_j(c_j!) / (N! * prod_ij(U_ij!)).
```

This is the same distribution induced by fixing the `X` labels and randomly permuting the `Y` labels in the original observation list.

That is why this method is comparable to JIDT permutation/shuffling.

## Statistic

For a contingency table `T`, compute expected counts under independence:

```text
E_ij = row_i * col_j / N
```

Then compute the likelihood-ratio MI statistic:

```text
G(T) = 2 * sum_ij T_ij * log(T_ij / E_ij)
```

with the convention that cells where `T_ij = 0` contribute zero.

This is equivalent to:

```text
G = 2N * I_hat
```

when `I_hat` is measured in nats.

## Primary P-Value

Let `G_obs = G(T_obs)`.

Sample `K` null tables:

```text
U_1, ..., U_K ~ fixed-margin null(row totals, column totals)
```

Compute:

```text
G_k = G(U_k)
```

Then estimate the upper-tail p-value as:

```text
p_empirical = (1 + count(G_k >= G_obs - tie_tol)) / (K + 1)
```

The `+1` correction avoids returning exactly zero from finite Monte Carlo sampling. This is a standard conservative convention. JIDT's reported p-values may use a slightly different finite-sample convention, so differences of order `1 / K` are not meaningful.

The tolerance is important:

```text
tie_tol = max(1e-12, 1e-12 * max(abs(G_obs), max(abs(G_k))))
```

Sparse discrete nulls often put large probability mass exactly at `G_obs`. Floating-point roundoff can make exact ties appear slightly smaller than `G_obs`. Without the tolerance, the p-value can be biased downward.

This tie convention is required to match JIDT's upper-tail permutation p-values.

## Optional Gamma Approximation

The current implementation also computes a moment-matched gamma approximation from the sampled null `G` values:

```text
mu = mean(G_k)
variance = var(G_k, ddof=1)
shape = mu^2 / variance
scale = variance / mu
p_gamma = Gamma(shape, scale).sf(G_obs)
```

This is useful as a smoothed diagnostic and may be useful for future amortized approximations.

However, the direct empirical table p-value is the primary method.

Do not rely on the gamma approximation alone for sparse discrete tables. It cannot represent point masses or exact ties, so it can be wrong when the null distribution is highly discrete.

If the fixed-margin null is degenerate, for example only one nonempty row or one nonempty column, all sampled `G` values are zero. In that case the empirical p-value is exactly `1.0`, while the gamma shape and scale are undefined. The implementation returns `gamma_p = empirical_p = 1.0` and leaves the gamma parameters as `NaN`.

## Minimal Implementation

The core implementation is in:

```text
SaddlepointValidation/general_fixed_margin.py
```

The essential logic is:

```python
import numpy as np
from scipy.stats import random_table


def g_statistics_batch(tables):
    counts = np.asarray(tables, dtype=np.float64)
    if counts.ndim == 2:
        counts = counts[None, :, :]

    totals = counts.sum(axis=(1, 2), keepdims=True)
    rows = counts.sum(axis=2, keepdims=True)
    cols = counts.sum(axis=1, keepdims=True)
    expected = rows * cols / totals

    mask = counts > 0
    terms = np.zeros_like(counts, dtype=np.float64)
    terms[mask] = counts[mask] * np.log(counts[mask] / expected[mask])
    return 2.0 * terms.sum(axis=(1, 2))


def empirical_fixed_margin_pvalue(table, k=1000, seed=None, batch_size=10000):
    rng = np.random.default_rng(seed)
    table = np.asarray(table, dtype=np.int64)

    # Drop rows and columns with zero total. They are structurally fixed at zero.
    table = table[table.sum(axis=1) > 0]
    table = table[:, table.sum(axis=0) > 0]

    row_totals = table.sum(axis=1)
    col_totals = table.sum(axis=0)
    observed_g = float(g_statistics_batch(table)[0])

    rv = random_table(row_totals, col_totals)
    null_g = np.empty(k, dtype=np.float64)

    pos = 0
    while pos < k:
        size = min(batch_size, k - pos)
        sampled = rv.rvs(size=size, random_state=rng)
        null_g[pos:pos + size] = g_statistics_batch(sampled)
        pos += size

    tie_tol = max(1e-12, 1e-12 * max(abs(observed_g), float(np.max(np.abs(null_g)))))
    pvalue = (np.count_nonzero(null_g >= observed_g - tie_tol) + 1) / (k + 1)
    return float(pvalue)
```

## Current Project Implementation Map

Important files:

- `general_fixed_margin.py`: direct fixed-margin table sampler, vectorized `G`, empirical p-value, optional gamma fit.
- `run_general_approx.py`: one-case comparison runner.
- `run_general_validation.py`: grid runner comparing empirical table sampling, gamma, chi-squared, and JIDT.
- `jidt_utils.py`: JPype/JIDT bridge for `computeSignificance`.
- `outputs/EMPIRICAL_TABLE_STRESS_K1000_TIEFIX_SUMMARY.md`: latest stress-test summary.

Important output columns:

- `g_statistic`: observed `G`.
- `empirical_fixed_margin_p`: primary p-value from sampled fixed-margin tables.
- `gamma_fixed_margin_p`: optional gamma approximation.
- `chi2_nominal_p`: chi-squared p-value using configured alphabet sizes.
- `chi2_dynamic_p`: chi-squared p-value after dropping observed empty rows and columns.
- `jidt_p`: JIDT `computeSignificance` p-value.
- `empirical_table_time_s`: wall-clock time for fixed-margin table sampling and p-value computation.
- `jidt_time_s`: wall-clock time for JIDT statistic plus shuffling.
- `table_json`: full observed table for reproducibility.
- `row_totals_json`, `col_totals_json`: observed fixed margins.
- `observed_r`, `observed_c`, `dynamic_df`: dimensions after empty margins are dropped.

## How To Run

From the simulations workspace:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile empirical_stress \
  --replicates 1 \
  --samples 1000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/empirical_table_validation_stress_k1000_tiefix
```

For the larger `N = 2,000,000` anchor cases:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile empirical_mega_anchors \
  --replicates 1 \
  --samples 1000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/empirical_table_validation_mega_k1000_tiefix
```

The stress profile currently covers:

- shapes: `20x20`, `50x20`, `80x80`, `100x50`, `100x100`,
- sample sizes: `1,000`, `10,000`, `100,000`, `1,000,000`,
- skewness regimes: `balanced`, `slight`, `mild`, `strong`, `extreme`, `zipf_mild`, `zipf_strong`.

The mega-anchor profile currently covers:

- shapes: `50x20`, `100x50`, `100x100`,
- sample size: `2,000,000`,
- skewness regimes: `balanced`, `mild`, `strong`, `extreme`, `zipf_strong`.

## Verification Checklist

A new implementation should pass these checks before being trusted.

1. Statistic check

Confirm that the manual `G` statistic matches JIDT's `G` statistic to numerical precision on several tables.

Expected tolerance:

```text
abs(G_manual - G_JIDT) < 1e-10
```

2. Fixed-margin equivalence check

For a moderate table, compare:

- empirical fixed-margin table sampling,
- manual raw-observation permutation,
- JIDT `computeSignificance`.

The p-values should agree up to Monte Carlo noise.

3. Sparse tie regression

Use an extreme sparse large-alphabet table where the observed `G` is the minimum or near-minimum possible under the fixed margins.

Expected result:

```text
empirical_fixed_margin_p ~= 1.0
JIDT p ~= 1.0
```

If the empirical method returns something like `0.2` or `0.3`, tie handling is probably wrong.

4. Degenerate fixed-margin regression

Use a table with only one nonempty row or one nonempty column, such as:

```text
[[5, 0],
 [0, 0]]
```

Expected result:

```text
G = 0
empirical_fixed_margin_p = 1
no method-level error
```

5. Monte Carlo resolution check

With `K=1000`, Monte Carlo p-values have resolution about:

```text
1 / K ~= 0.001
```

The standard error is approximately:

```text
sqrt(p * (1 - p) / K)
```

At `p = 0.5`, this is about `0.016`.

So median absolute empirical-vs-JIDT differences around `0.01` are consistent with both methods using `K=1000`.

6. Chi-squared sanity check

In balanced, large-`N`, well-populated tables, chi-squared should often agree reasonably well.

In skewed, sparse, large-alphabet tables, chi-squared may be very wrong. This is expected and is the main motivation for the method.

## Current Validation Results

Corrected stress-test headline results:

| run | rows | median empirical time | median JIDT time | median speedup | median abs empirical-vs-JIDT error | median abs chi2-vs-JIDT error | empirical closer than chi2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Stress to `N=1M` | 140 | 0.0649s | 0.4999s | 2.35x | 0.0100 | 0.2483 | 91.4% |
| Mega anchors `N=2M` | 15 | 0.3079s | 28.2504s | 91.0x | 0.0133 | 0.2442 | 93.3% |
| Combined | 155 | 0.0741s | 0.9768s | 3.66x | 0.0101 | 0.2442 | 91.6% |

Runtime scaling by sample size:

| N | rows | empirical time | JIDT time | speedup | empirical error vs JIDT | chi2 error vs JIDT |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 35 | 0.0156s | 0.0155s | 0.87x | 0.0067 | 0.3800 |
| 10,000 | 35 | 0.0903s | 0.0900s | 1.13x | 0.0128 | 0.3290 |
| 100,000 | 35 | 0.2117s | 1.1405s | 6.09x | 0.0081 | 0.2432 |
| 1,000,000 | 35 | 0.3063s | 11.8594s | 39.94x | 0.0146 | 0.0737 |
| 2,000,000 | 15 | 0.3079s | 28.2504s | 91.01x | 0.0133 | 0.2442 |

Interpretation:

- At tiny `N`, JIDT is already cheap, so fixed-margin sampling is not necessarily faster.
- At large `N`, fixed-margin sampling is much faster because it avoids shuffling arrays of length `N`.
- Accuracy against JIDT is strong and close to expected Monte Carlo noise at `K=1000`.
- Chi-squared is often badly miscalibrated in sparse, skewed, large-alphabet regimes.

## Complexity Intuition

JIDT shuffling:

```text
roughly O(K * N)
```

because each shuffle operates on raw observation arrays of length `N`.

Empirical fixed-margin table sampling:

```text
roughly tied to K and table dimensions, not directly to raw N
```

The exact cost depends on SciPy's `random_table` sampler and on computing `G` over sampled tables. In practice, with fixed `K=1000`, runtime grows much more slowly with `N` than JIDT.

This is why the method is most useful for large `N`.

## When To Use This Method

Use empirical fixed-margin table sampling when:

- you want a JIDT-like permutation null,
- chi-squared may be unreliable,
- `N` is large enough that raw shuffling is expensive,
- the table has skewed or long-tailed marginals,
- you can tolerate Monte Carlo p-value resolution around `1 / K`.

Use JIDT directly when:

- `N` is small and runtime is negligible,
- you need a direct baseline for validation,
- you want to avoid adding a SciPy table-sampling dependency.

Use chi-squared when:

- the table is balanced and well-populated,
- expected counts are comfortably large,
- speed matters more than finite-sample calibration.

## Known Limitations

1. It is still Monte Carlo.

With `K=1000`, this is not a high-resolution tail method. For p-values near `0.001` or below, increase `K`.

2. The method conditions on observed margins.

This matches permutation testing. It is not the same as sampling new independent datasets from estimated marginal probabilities.

3. Gamma is secondary.

Gamma can look good in many smooth regimes, but it can fail in sparse regimes with point masses. The empirical table p-value is the safer method.

4. Very large tables can still be expensive.

The method avoids `O(KN)` raw shuffling, but sampling and scoring `K` tables of size `r x c` is not free. A `1000x1000` table would need a separate performance study.

5. Validation against JIDT has Monte Carlo noise.

When both methods use `K=1000`, observed p-value differences around `0.01` are not concerning by themselves.

## Recommended Next Steps

1. Increase replicates for calibration, not just screening.

The current stress run uses one table per configuration. For publishable false-positive-rate claims, rerun selected regimes with many independent null tables per configuration.

2. Run high-`K` anchors.

For a small number of representative tables, compare:

```text
K = 1000, 10000, 100000
```

for both empirical table sampling and JIDT if JIDT runtime permits.

3. Add asymmetric marginal regimes.

Current stress profiles use the same skewness family for `X` and `Y`. Real data may have one balanced variable and one skewed variable.

4. Test larger but realistic alphabets.

Current validation reaches `100x100`. A useful next screen would include shapes like:

```text
200x20
200x100
500x20
```

with long-tailed marginals.

5. Consider reusable null samples.

For many tests with identical row and column totals, sample the fixed-margin null once, store the `G_k` values, and reuse them.

6. Separate the method API from validation scripts.

Eventually expose a clean function like:

```python
fixed_margin_mi_significance(table, k=1000, seed=None)
```

returning the observed statistic, empirical p-value, optional gamma p-value, timing, and diagnostics.
