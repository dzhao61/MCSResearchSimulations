# Adversarial Audit

## Overall Verdict

Artifact integrity: **PASS**.

Method as a usable test: **NO-GO**.

The saved prospective decision is correctly reproduced as `GO`, but that
decision is conditional on locally valid Edgeworth evaluations. Exact-table
regeneration shows validity is strongly outcome-dependent, invalidating the
practical interpretation of the conditional calibration result.

## Correctness and Integrity

- Thirteen mathematical and software tests passed.
- Both influence functions matched contamination finite differences.
- The known studentized-mean Edgeworth formula was recovered exactly.
- Existing normal, naive-Welch, and influence-df results were unchanged.
- Scalar/vectorized parity, group-swap invariance, and relabelling invariance
  passed.
- All 326 scenario keys and simulation seeds were unique.
- Power seeds were disjoint from null seeds.
- Saved weak-null distributions had equal MI within numerical tolerance.
- Strong-null probability arrays were exactly equal.
- Rejection counts, Wilson intervals, valid denominators, and aggregate
  metrics recomputed exactly.
- Recorded hashes match the exact candidate and validation runner.

See `results/frozen_decisive/AUDIT.json`.

## Selective Invalidity

The frozen guardrail rejects an Edgeworth calculation when the raw CDF is
outside `[0,1]` or its local density is non-positive. Exact regeneration found:

- broad: 1,407 invalid among 720,000;
- hard: 1,021 invalid among 240,000;
- strong null: 1,363 invalid among 720,000; and
- stress: 7,465 Edgeworth-invalid among base-valid pairs.

In broad, hard, and strong-null stages, about `99-100%` of invalid cases had a
normal p-value at or below `0.05`. Their median absolute statistic was around
`3`. Invalidity therefore removes rejection-tail observations rather than a
random subset.

The complete regeneration is saved in
`results/frozen_decisive/invalid_case_audit.csv`.

## Tail Balance

At alpha `0.05`, hard-grid valid Edgeworth rejections were:

```text
left tail:  4,853
right tail: 8,724
```

The normal comparator produced:

```text
left tail:  8,179
right tail: 6,772
```

An asymmetric null can legitimately have asymmetric raw-statistic tails, but
an accurately equal-tailed CDF should allocate approximately equal rejection
probability after correction. The large residual imbalance is further
evidence that the first-order approximation is not fully calibrated.

## Leakage Assessment

No fitted constants, empirical thresholds, or method switches use validation
outcomes. The population and simulation seeds were fresh and frozen before
the run. Hard cases reuse broad population distributions but use independent
table samples, exactly as specified.

The invalid-case analysis is explicitly post hoc and does not alter the
frozen candidate. It is a safety audit demonstrating why the original
mechanical decision should not be adopted.

## Residual Scope

Even with a globally valid CDF completion, this remains a regular
positive-support method away from MI zero. Sparse empirical boundaries,
residual MI bias, and full second-order tail behavior remain unresolved.
