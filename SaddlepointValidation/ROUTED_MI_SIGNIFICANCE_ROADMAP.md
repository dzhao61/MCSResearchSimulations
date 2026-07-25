# Roadmap: Routed MI Significance Test Suite

Date: 2026-07-06

This document captures the revised project framing after the fixed-margin sampling experiments and audits.

## Core Thesis

The project should not be framed as:

```text
one new method replacing JIDT and chi-square
```

It should be framed as:

```text
a routed significance-testing suite for discrete MI
```

Different regimes need different tests. The router chooses the cheapest method that remains trustworthy for the observed table.

The paper's target is:

```text
match chi-square and JIDT permutation in balanced / well-populated tables,
but outperform analytic chi-square in skewed / low-expected-count tables.
```

The goal is not to make chi-square look bad everywhere. In regimes where chi-square assumptions hold, the routed method should agree with it.

## Why Routing Works

The important empirical/theoretical synthesis is:

```text
DP tractability and chi-square reliability are governed by related table geometry.
```

Dense margins create large fixed-margin support. This makes exact DP expensive, but it also tends to create large expected counts, where chi-square is usually acceptable.

Sparse or skewed margins create small or structured support. This is exactly where chi-square fails, but it is also where exact conditional or saddlepoint methods can be tractable.

So the expensive exact region and the region needing exactness often do not overlap.

## Proposed Four Tiers

### Tier 1: Exact Conditional / Specialized Kernels

Use when:

- support is tiny,
- table is `2x2`,
- table is `r x 2` or `2 x c` with tractable specialized kernels,
- exact p-values are cheap.

For `2x2`, do not use generic DP. The conditional null is a single hypergeometric distribution.

Needed work:

- implement `2x2` hypergeometric exact tail for `G`,
- implement or route `r x 2` / `2 x c` special cases,
- expose support-size diagnostics.

### Tier 2: Saddlepoint Conditional CGF

Use when:

- support is small-to-moderate,
- exact enumeration is too costly,
- far-tail p-values below Monte Carlo resolution matter,
- deterministic p-values are valuable.

This remains the most novel statistical core.

Needed work:

- improve routing so it never handles cases better served by specialized kernels,
- benchmark against exact enumeration on small supports,
- benchmark against high-`K` fixed-margin sampling and JIDT on medium supports,
- preserve root diagnostics and fallback routes.

### Tier 3: Empirical Fixed-Margin Table Sampling

Use when:

- alphabets are large,
- support is too large for exact/saddlepoint DP,
- JIDT shuffling is expensive due to large `N`,
- Monte Carlo resolution is acceptable.

This is classical Monte Carlo exact testing for contingency tables, not a new statistical test.

Value in this project:

- samples sufficient-statistic space directly,
- targets the same null as JIDT shuffling,
- avoids raw `O(KN)` shuffling,
- gives strong finite-sample calibration evidence against chi-square.

Needed work:

- cite Patefield / classical contingency-table Monte Carlo exact-test literature,
- optionally add tail modeling for very small p-values,
- add table-dimension runtime benchmarks beyond `100x100`.

### Tier 4: Chi-Square / Corrected Chi-Square

Use when:

- expected counts are large,
- margins are dense,
- asymptotic approximation is reliable,
- speed matters.

The standard baseline should be:

```text
G = 2N * MI_nats
p = chi2.sf(G, df)
```

JIDT's no-argument analytic significance should be reported separately if used because it uses:

```text
2N * MI_bits
```

Needed work:

- define expected-count and support-size thresholds,
- test Williams or other finite-sample corrections,
- include safe-regime validation where chi-square is expected to work.

This tier is important for the paper's credibility. The validation should show that the routed method does not overcomplicate or degrade healthy balanced cases.

## Router Inputs

The router should compute cheap diagnostics before selecting a tier:

- table shape,
- nonempty rows and columns,
- total `N`,
- row and column totals,
- minimum expected count,
- fraction of expected counts below `1`,
- fraction of expected counts below `5`,
- estimated or exact support size when feasible,
- table sparsity,
- requested p-value resolution,
- time budget / deterministic requirement.

## Draft Routing Logic

Pseudo-rule:

```text
if observed table has <= 1 nonempty row or <= 1 nonempty column:
    return p = 1

if table is 2x2:
    use hypergeometric exact tail

if support size is exactly enumerable under configured limit:
    use exact conditional enumeration

if support estimate is below saddlepoint threshold:
    use saddlepoint conditional CGF

if expected-count diagnostics are safely asymptotic:
    use standard chi-square or corrected chi-square

otherwise:
    use empirical fixed-margin table sampling
```

This ordering can be tuned empirically. In particular, chi-square may be routed before sampling for obviously dense, high-count tables.

## Signature Figure For The Paper

The paper should aim for a regime map:

```text
x-axis: support size or support-size proxy
y-axis: expected-count / sparsity diagnostic
color: best tier by accuracy-runtime tradeoff
markers: empirical failures of chi-square
```

This figure would show:

- where chi-square works,
- where chi-square fails,
- where exact/saddlepoint is tractable,
- where empirical fixed-margin sampling is the right fallback,
- how JIDT shuffling compares in runtime.

The figure should include both:

- a chi-square-friendly region with high expected counts,
- a chi-square-failure region with skewed marginals and low expected counts.

The intended visual message is not "chi-square is bad"; it is "chi-square is good in its regime, and the router knows when to leave that regime."

## Immediate Implementation Priorities

1. Add router diagnostics.

Create a function like:

```python
diagnose_table(table)
```

returning:

```text
nonempty_shape
dynamic_df
expected-count stats
sparsity stats
support estimate/status
recommended_route
```

2. Add `2x2` exact hypergeometric route.

This is a deletion of generic DP work for `2x2`, not an optimization of it.

3. Add fixed-margin verification tests to CI/manual checks.

Current script:

```bash
JIDT_JVM_ARGS=-Xmx4g .venv/bin/python SaddlepointValidation/fixed_margin_tier_checks.py
```

4. Run balanced-control calibration.

The profile exists as:

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

It covers balanced cases with average expected counts:

```text
40, 100, 25, 50, 100, 100
```

This is the fair control group where chi-square should work.

5. Rewrite public framing.

Use:

```text
empirical fixed-margin table sampling = classical Monte Carlo exact-test tier
saddlepoint = deterministic far-tail tier / novel core
router = contribution tying methods together
```

6. Prepare supervisor-facing figures.

Minimum:

- focused calibration FPR bar chart,
- runtime vs `N` plot,
- p-value scatter against JIDT,
- expected-count failure table for chi-square,
- balanced high-expected-count sanity table where chi-square works,
- router regime diagram sketch.

## Transfer Entropy Note

Transfer entropy remains out of scope for the current MI validation, but it is likely where the routed approach becomes more valuable.

TE conditions on past states, splitting the data into strata. These strata often have smaller effective supports, which may make exact/saddlepoint tiers useful even when the global alphabet looks large.

Recommended sequencing:

```text
finish routed MI proof-of-concept first
then port the tiering idea to TE
```
