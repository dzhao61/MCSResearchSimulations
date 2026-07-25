# Current Handoff: Empirical Fixed-Margin MI Significance Testing

Date: 2026-07-06

This is the current handoff for the mutual-information significance-testing work. It supersedes the earlier saddlepoint-only framing. The most promising current direction is not one method replacing all others, but a routed test suite.

## Executive Summary

We want a significance test for discrete plug-in mutual information that is:

- more accurate than asymptotic chi-square in skewed/sparse finite-sample regimes,
- faster than JIDT permutation/shuffling when `N` is large,
- general enough for larger alphabet sizes.
- not worse than chi-square or JIDT permutation in reasonably balanced, well-populated tables.

The strongest practical tier discovered in the recent experiments is:

```text
Empirical fixed-margin table sampling
```

Given an observed contingency table, keep its row and column totals fixed, sample new contingency tables from the fixed-margin independence null, compute `G = 2N * MI_nats` for each sampled table, and estimate the upper-tail p-value.

This targets the same conditional null as JIDT shuffling, but samples tables directly rather than shuffling raw observation arrays. This is best understood as the classical Monte Carlo exact test for contingency tables, not as a new statistical test. Its contribution here is as an engineering tier and evidence engine.

Current verdict:

```text
Promising and not invalidated by audits.
Needs more publication-grade validation before being written up as final.
```

Important framing for the paper:

```text
The goal is not to beat chi-square in every table.
The goal is to match chi-square/JIDT when chi-square assumptions are healthy,
and improve substantially over analytic chi-square when skewed marginals and low expected counts break the asymptotic approximation.
```

## Current Synthesis

The project should now be framed as a four-tier routed significance test:

| tier | use when | value |
| --- | --- | --- |
| exact conditional / specialized kernels | tiny supports, especially all `2x2` tables via the hypergeometric | exact, deterministic, fast in small support |
| saddlepoint conditional CGF | small-to-moderate support where far-tail p-values matter | deterministic, far-tail capable, novel core |
| empirical fixed-margin table sampling | large alphabets or regimes where exact DP is too costly | general, JIDT-like null, faster than raw shuffling at large `N` |
| chi-square / corrected chi-square | dense, high expected-count asymptotic regime | free and accurate when assumptions hold |

The key observation is:

```text
The regimes where exact DP is expensive are often the regimes where chi-square is already reliable.
The regimes where chi-square fails are often sparse/skewed regimes where exact or saddlepoint methods are tractable.
```

That makes the router the central research object.

The empirical table-sampling tier should be cited honestly as classical Monte Carlo exact testing, e.g. Patefield-style fixed-margin table sampling. The paper contribution is not inventing this sampler. The contribution is showing how it compares to JIDT at scale and how it fits into a routed MI significance-testing system.

## What To Trust

The core result appears sound:

- JIDT shuffling was audited from source and with controlled permutation tests.
- Our wrapper uses JIDT shuffling correctly.
- Empirical fixed-margin table sampling matches the same fixed-margin null as JIDT shuffling.
- Manual `G`, vectorized `G`, and JIDT MI agree after correct unit conversion.
- The standard nats-based chi-square implementation is correct.
- JIDT's built-in analytic significance is a separate bits-scaled convention and should not be used as the main chi-square baseline.

Nothing found so far invalidates the empirical fixed-margin method.

## Method

Input:

```text
observed contingency table T
```

Let:

```text
row totals = T.sum(axis=1)
column totals = T.sum(axis=0)
N = T.sum()
```

The null is all contingency tables with the same row and column totals as `T`.

For each sampled null table `U_k`, compute:

```text
G(U_k) = 2 * sum_ij U_ij * log(U_ij / E_ij)
E_ij = row_i * col_j / N
```

where zero cells contribute zero.

The empirical p-value is:

```text
p = (1 + count(G_k >= G_obs - tie_tol)) / (K + 1)
```

The tie tolerance matters because sparse discrete nulls can put large probability mass exactly at `G_obs`.

Implementation:

```text
SaddlepointValidation/general_fixed_margin.py
```

Main functions:

- `g_statistics_batch()`
- `sample_fixed_margin_g()`
- `fixed_margin_gamma_approx()`

Despite the historical name `fixed_margin_gamma_approx`, the important output is:

```text
empirical_p
```

The gamma approximation is secondary.

## Why This Beats The Old Saddlepoint Direction

The exact DP/saddlepoint work was accurate in small regimes but not general enough. DP scaling becomes bad for larger alphabets or dense margins.

Empirical fixed-margin table sampling is simpler and more general:

- no exact DP state explosion,
- works for larger alphabets such as `100x100`,
- targets the same null as JIDT shuffling,
- runtime depends heavily on table dimensions and `K`, not directly on raw `N`.

It is not always faster for tiny `N`, because JIDT shuffling is already cheap there. It becomes attractive when `N` is large.

## JIDT Findings

JIDT discrete MI returns MI in bits:

```java
Math.log(...) / log_2
```

JIDT shuffle significance:

```python
calc.computeSignificance(shuffles)
```

does this internally:

1. reconstructs marginal arrays from observed counts,
2. generates random permutations,
3. permutes one variable against the other,
4. recomputes MI,
5. returns `count(surrogate_MI >= observed_MI) / K`.

Important details:

- JIDT shuffling uses fixed observed margins.
- JIDT shuffle p-values use `count / K`, with no `+1` correction.
- JIDT default shuffle calls are not seeded.
- For reproducible JIDT tests, use `computeSignificance(int[][] newOrderings)` with explicit permutation arrays.

Source-level audit:

```text
SaddlepointValidation/JIDT_IMPLEMENTATION_AUDIT.md
```

## Chi-Square Findings

The standard likelihood-ratio chi-square test is:

```text
G = 2N * MI_nats
p = chi2.sf(G, df)
```

Our implementation of this is correct. It matches SciPy's built-in log-likelihood contingency-table test:

```python
scipy.stats.contingency.chi2_contingency(
    table,
    correction=False,
    lambda_="log-likelihood",
)
```

JIDT's no-argument analytic significance method is different:

```python
calc.computeSignificance()
```

It uses:

```text
2N * MI_bits
```

not:

```text
2N * MI_bits * ln(2)
```

So JIDT analytic p-values are more aggressive than the standard chi-square p-values by a statistic scaling factor of:

```text
1 / ln(2) ~= 1.4427
```

Conclusion:

```text
Use JIDT shuffling as the JIDT baseline.
Use standard nats-based chi-square as the analytic chi-square baseline.
Report JIDT analytic only as a separate software convention if needed.
```

Chi-square audit:

```text
SaddlepointValidation/CHI_SQUARE_ANALYTIC_AUDIT.md
```

## Current Validation Results

### Stress Screen

Corrected stress screen:

- 140 stress configurations up to `100x100`, `N=1,000,000`.
- 15 mega-anchor configurations at `N=2,000,000`.
- `K=1000` for empirical fixed-margin table sampling and JIDT.

Combined headline:

| rows | empirical time | JIDT time | speedup | empirical error vs JIDT | chi2 error vs JIDT | empirical closer than chi2 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 155 | 0.0741s | 0.9768s | 3.66x | 0.0101 | 0.2442 | 91.6% |

Stress summary:

```text
SaddlepointValidation/outputs/EMPIRICAL_TABLE_STRESS_K1000_TIEFIX_SUMMARY.md
```

### Focused Calibration

Focused calibration:

- 12 selected configurations.
- 500 null replicates per configuration.
- 6,000 total empirical/chi-square rows.
- JIDT shuffling on 50 anchor replicates per configuration, 600 total JIDT anchors.
- `K=1000`.

Headline:

| metric | value |
| --- | ---: |
| median empirical time | 0.051s |
| median JIDT time | 0.100s |
| median empirical vs JIDT p-error | 0.0119 |
| median chi-square vs JIDT p-error | 0.4715 |
| empirical closer than chi-square vs JIDT | 99.7% |

False-positive rates:

| alpha | empirical fixed-margin | JIDT shuffle anchors | standard chi-square |
| ---: | ---: | ---: | ---: |
| 0.10 | 0.1013 | 0.1033 | 0.1517 |
| 0.05 | 0.0537 | 0.0550 | 0.1337 |
| 0.01 | 0.0120 | 0.0133 | 0.0993 |

Focused summary:

```text
SaddlepointValidation/outputs/empirical_calibration_k1000_r500_jidt50/FOCUSED_CALIBRATION_SUMMARY.md
```

### High-K Anchors

Five representative anchor tables were rerun with:

```text
empirical fixed-margin K = 100000
JIDT shuffling K = 10000
```

Empirical and JIDT remained close, with absolute p-value differences around `0.0002` to `0.0037`. Chi-square remained badly wrong on selected failure cases.

High-K summary:

```text
SaddlepointValidation/outputs/empirical_calibration_k1000_r500_jidt50/HIGH_K_ANCHOR_SUMMARY.md
```

## Acceptance Criteria For The Paper Claim

A proposed routed method should be judged against two regimes.

### Regime A: balanced / well-populated tables

Examples:

```text
uniform or near-uniform marginals
most expected cell counts > 5
no extreme sparsity
```

Requirement:

```text
The routed method should perform about as well as standard chi-square and JIDT permutation.
It should not introduce obvious calibration harm or major runtime cost.
```

This is where chi-square is expected to work, so matching it is success.

### Regime B: skewed / low-expected-count tables

Examples:

```text
dominant marginal categories
Zipf or long-tailed marginals
many expected counts < 5
many expected counts < 1
sparse observed tables
```

Requirement:

```text
The routed method should be much better calibrated than analytic chi-square,
and should remain close to JIDT permutation or exact conditional results.
```

This is the paper's core claim.

### Metrics

For each regime, report:

- false positive rate at `alpha = 0.10, 0.05, 0.01`,
- absolute FPR error from nominal,
- p-value agreement against JIDT permutation or exact conditional p-values,
- runtime per test,
- expected-count diagnostics.

Suggested summary language:

```text
In well-populated balanced tables, the routed method agrees with chi-square and JIDT.
In skewed low-expected-count tables, where analytic chi-square is miscalibrated,
the routed method tracks the fixed-margin permutation/null distribution instead.
```

## Bugs Found And Fixed

### 1. Sparse Tie Handling

Problem:

Sparse fixed-margin nulls can have large point mass exactly at `G_obs`. Floating-point noise made some exact ties look slightly smaller than `G_obs`, biasing empirical p-values downward.

Fix:

```text
count(G_k >= G_obs - tie_tol)
```

This made sparse point-mass cases match JIDT.

### 2. Degenerate Fixed-Margin Nulls

Problem:

If only one row or one column is nonempty, the fixed-margin null has zero variance. The empirical p-value should be valid, but the optional gamma fit failed.

Fix:

Degenerate nulls now return:

```text
G = 0
empirical_p = 1
gamma_p = 1
gamma_shape = NaN
gamma_scale = NaN
error = ""
```

### 3. Chi-Square / JIDT Analytic Confusion

Problem:

JIDT analytic significance looked extremely miscalibrated. This raised concern that our chi-square baseline was wrong.

Finding:

Our standard chi-square is correct. JIDT analytic uses a bits-scaled statistic and is a separate convention.

Fix:

Outputs now separate:

```text
chi2_nominal_p
chi2_dynamic_p
jidt_analytic_bits_nominal_p
mi_nats_observed
mi_bits_observed
jidt_analytic_bits_nominal_statistic
```

## Important Files

Core method:

```text
SaddlepointValidation/general_fixed_margin.py
```

Verification checks:

```text
SaddlepointValidation/fixed_margin_tier_checks.py
```

Validation runner:

```text
SaddlepointValidation/run_general_validation.py
```

JIDT bridge:

```text
SaddlepointValidation/jidt_utils.py
```

Method document:

```text
SaddlepointValidation/EMPIRICAL_FIXED_MARGIN_METHOD.md
```

Adversarial audit:

```text
SaddlepointValidation/EMPIRICAL_FIXED_MARGIN_ADVERSARIAL_AUDIT.md
```

JIDT source audit:

```text
SaddlepointValidation/JIDT_IMPLEMENTATION_AUDIT.md
```

Chi-square audit:

```text
SaddlepointValidation/CHI_SQUARE_ANALYTIC_AUDIT.md
```

Older saddlepoint handoff:

```text
SaddlepointValidation/SADDLEPOINT_MI_VALIDATION_HANDOFF.md
```

## How To Rerun

From:

```text
/Users/danielzhao/MyMac/Masters Degree/Research/Simulations
```

Focused calibration:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile empirical_calibration \
  --replicates 500 \
  --samples 1000 \
  --jidt-shuffles 1000 \
  --jidt-replicates 50 \
  --checkpoint-every 25 \
  --output-dir SaddlepointValidation/outputs/empirical_calibration_k1000_r500_jidt50
```

Balanced high-expected-count controls:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile empirical_balanced_controls \
  --replicates 500 \
  --samples 1000 \
  --jidt-shuffles 1000 \
  --jidt-replicates 50 \
  --checkpoint-every 25 \
  --output-dir SaddlepointValidation/outputs/empirical_balanced_controls_k1000_r500_jidt50
```

This profile is important because it tests the non-negotiable control condition:

```text
when chi-square assumptions are healthy, the routed method should agree with chi-square and JIDT.
```

Stress screen:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile empirical_stress \
  --replicates 1 \
  --samples 1000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/empirical_table_validation_stress_k1000_tiefix
```

Mega anchors:

```bash
JIDT_JVM_ARGS=-Xmx8g .venv/bin/python SaddlepointValidation/run_general_validation.py \
  --profile empirical_mega_anchors \
  --replicates 1 \
  --samples 1000 \
  --jidt-shuffles 1000 \
  --output-dir SaddlepointValidation/outputs/empirical_table_validation_mega_k1000_tiefix
```

## What To Worry About

Do not worry much about:

- whether JIDT shuffling was used correctly,
- whether MI units are understood,
- whether standard chi-square was coded incorrectly,
- whether empirical table sampling targets the same null as JIDT shuffling.

Those have been audited.

Still worry about:

1. Publication-grade calibration

The focused run is strong, but a paper needs more selected regimes with more replicates. It should explicitly include both healthy balanced tables and skewed low-expected-count tables.

2. Tail resolution

`K=1000` is fine for screening. For very small p-values, use `K=10000` or `K=100000`.

3. Very large alphabets

The method avoids raw `O(KN)` shuffling, but sampled table scoring still depends on table dimensions. Larger alphabets like `500x100` or `1000x20` need separate benchmarking.

4. Asymmetric margins

Some asymmetric cases were added, but this should be expanded.

5. Gamma approximation

Gamma is useful as a diagnostic or possible smoothed approximation, but empirical fixed-margin p-values are the primary method. Do not rely on gamma alone in sparse point-mass regimes.

## Recommended Next Steps

1. Produce paper-ready figures:

- FPR calibration by method and alpha.
- Runtime scaling versus `N`.
- P-value scatter against JIDT shuffling.
- Expected-count diagnostics showing where chi-square fails.

2. Add a clean public API:

```python
fixed_margin_mi_significance(table, k=1000, seed=None)
```

returning:

```text
G_obs
MI bits/nats
empirical p-value
optional gamma p-value
row/column margins
diagnostics
runtime
```

3. Expand validation:

- more asymmetric marginals,
- larger realistic alphabets,
- more high-`K` anchors,
- more per-configuration replicates for publishable FPR estimates.

4. Decide how to discuss JIDT analytic:

Recommended language:

```text
JIDT shuffling is used as the permutation baseline. JIDT's analytic significance method is reported separately only as a software convention because it uses a bits-scaled chi-square statistic, whereas the standard likelihood-ratio chi-square uses nats.
```

## Bottom Line

The current story is:

```text
Empirical fixed-margin table sampling closely matches JIDT shuffling,
is much better calibrated than chi-square in sparse/skewed regimes,
and becomes much faster than JIDT as N grows.
```

The method is not yet a finished paper result, but it is now a strong and well-audited research direction.
