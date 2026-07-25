# Deterministic Sparse-CMI Validation Report

Date: 25 July 2026

## Executive Conclusion

The method is promising enough to continue as a master's thesis project, with
a narrower claim than originally proposed.

For binary `X` and `Y` conditioned on an arbitrary number of discrete `Z`
states, the implementation now provides a deterministic fixed-margin test:

1. use numerical exact convolution when conservative state and work bounds are
   at most 100,000;
2. otherwise use a factorized Lugannani-Rice saddlepoint tail;
3. group identical stratum CGFs by multiplicity, so runtime depends mainly on
   the number of distinct margin patterns rather than the raw number of
   strata.

The optimized full grid had no invalid p-values, root failures, or
monotonicity violations. On the 74 configurations absent from the routing
pilot, mean absolute FPR error at nominal `alpha=0.05` was `0.00011` for the
routed method and `0.21728` for nominal chi-square. This very large chi-square
error is specific to the sparse fixed-margin conditional regimes in the grid;
it must not be generalized to ordinary dense contingency tables.

The present result is not a general larger-alphabet CMI solution. It is a
strong binary-CMI result and a plausible methods-transfer contribution.

## Statistical Construction

In each conditioning stratum, fixed binary margins leave one free count:

```text
A_z | n_z, r_z, s_z ~ Hypergeometric(n_z, s_z, r_z).
```

The likelihood-ratio statistic is

```text
G^2 = 2 N I_hat(X;Y|Z) = sum_z g_z(A_z).
```

The component distributions are conditionally independent. Their exact CGFs
therefore add. For an observed statistic `t`, the saddlepoint solves
`K'(s_hat)=t` and the upper tail is approximated with Lugannani-Rice. Exact
endpoint masses, degenerate distributions, and near-mean cases have explicit
guardrails.

The router does not estimate reliability from alphabet labels or a
configuration name. It derives conservative state and transition-work bounds
from the finite component supports. Repeated supports are handled
combinatorially, allowing exact convolution in cases that a crude
"number-of-strata" cutoff would reject.

## Correctness Work

The 33-test suite covers:

- `G^2 = 2N CMI_nats`;
- exact hypergeometric probabilities;
- exact moments and convolution against brute-force enumeration;
- fixed-margin sampling versus observation-level permutation;
- `K(0)`, `K'(0)`, `K''(0)`, and the third cumulant;
- grouped versus ungrouped CGF identities;
- finite, bounded, monotone saddlepoint p-values;
- left-of-mean and endpoint regressions;
- conservative exact-convolution complexity bounds;
- exact and saddlepoint routing;
- JIDT observation reconstruction and block-preserving orderings.

An additional adversarial check generated 250 random small stratum sets. The
estimated exact state bound was never below the realized convolution size; its
median bound/actual ratio was `1.0` and maximum was `2.0`.

Two implementation errors were found and corrected before the final run:

- A guard incorrectly assumed every threshold below the mean must have
  upper-tail probability above `0.5`. This is false for some skewed discrete
  distributions.
- The first router used only the number of informative strata. It missed exact
  convolutions with many repeated low-support components.

## Full-Grid Accuracy

The final fixed-margin run used 103 predeclared configurations, 100,000
conditional-null draws where exact convolution was unavailable, and 1,000
literal within-stratum permutations for timing. Eighty-four configurations
routed to exact convolution and 19 to saddlepoint.

Mean absolute FPR error against the attainable conditional reference on the
stable held-out subset:

| Alpha | Raw saddlepoint | Routed test | Chi-square nominal | Chi-square informative |
|---:|---:|---:|---:|---:|
| 0.10 | 0.01266 | 0.00028 | 0.31807 | 0.28179 |
| 0.05 | 0.01535 | 0.00030 | 0.24727 | 0.23638 |
| 0.01 | 0.00299 | 0.00004 | 0.14710 | 0.15276 |
| 0.001 | 0.00033 | 0.00002 | 0.06978 | 0.07034 |

The raw saddlepoint column intentionally includes coarse cases that the router
handles exactly. It shows why saddlepoint alone is not a universal answer.

The router was corrected after inspecting the 29-configuration smoke pilot.
The stricter confirmation set is therefore the 74 configurations absent from
that pilot:

| Alpha | Raw saddlepoint | Routed test | Chi-square nominal |
|---:|---:|---:|---:|
| 0.10 | 0.01799 | 0.00035 | 0.26479 |
| 0.05 | 0.01444 | 0.00011 | 0.21728 |
| 0.01 | 0.00305 | 0.00010 | 0.11835 |
| 0.001 | 0.00036 | 0.00002 | 0.05909 |

Of those 74 confirmation cases, 13 required saddlepoint. At `alpha=0.05`,
their saddlepoint mean FPR error was `0.00063`, median was `0.00060`, and
maximum was `0.00236`. This is the cleanest evidence for the approximation
itself; the near-zero overall router error is partly expected because 61 of 74
confirmation cases were evaluated exactly.

The balanced adequate-count controls also passed. In the five balanced
`n_z=30` configurations, each expected binary cell count is `7.5`. Mean error
against the conditional reference was `0.00187` for the router and `0.03170`
for nominal chi-square; mean absolute size distortion was `0.00337` and
`0.02926`, respectively. The common expected-count-above-five rule is only a
heuristic, and approximation errors can accumulate when many strata
contribute degrees of freedom.

## Runtime and JIDT

Against the optimized Python literal within-stratum permutation baseline, the
full grid's median speedup was `46.2x`. On the 13 post-pilot saddlepoint-only
configurations, median speedup was `63.3x`, with a minimum of `12.5x`.

Six direct JIDT anchors used 1,000 explicit blockwise orderings and tables
selected near the conditional 95th percentile:

| Metric | Result |
|---|---:|
| Median deterministic/JIDT speedup | 17.5x |
| Median deterministic absolute p error | 0.00026 |
| Median JIDT blockwise absolute p error | 0.00763 |
| Median nominal chi-square absolute p error | 0.04875 |
| Reference p inside JIDT 95% Monte Carlo interval | 6/6 |
| Maximum manual/JIDT `G^2` difference | `1.42e-13` |

These are steady-state timings. JVM startup and a small JIT warmup were
excluded, while JIDT ordering construction and Python-to-Java conversion were
included. Router timings are ten-call averages. This avoids inflating the
claimed speedup with one-time JVM startup.

JIDT's p-value error here is ordinary `B=1000` Monte Carlo noise, not evidence
that JIDT samples the wrong distribution when correct blockwise orderings are
supplied. The deterministic test avoids that noise and the `1/B` tail
resolution.

JIDT's default `computeSignificance(int)` globally shuffles one variable. It
does not preserve the `X-Z` margin and targets a stronger null when `P(X|Z)`
varies. It is recorded as a separate baseline, not ground truth. The explicit
blockwise orderings use the saved NumPy seed; JIDT's default overload owns its
random-number generator and its diagnostic p-values are not reproducible from
that seed.

A second JIDT issue was reproduced: raw JIDT p-values compare floating MI
values with no tolerance. In one coarse exact-support anchor, 100,000
blockwise permutations gave raw p `0.10829`, while the exact inclusive tail
was `0.132953`. Recomputing the rank from JIDT's own surrogate values with a
`G^2` tolerance of `1e-10` gave `0.13285`. This is a numerical tie-handling
issue, not a bits/nats problem.

## What the Evidence Establishes

The evidence supports these statements:

- Conditioning on per-stratum binary margins produces a valid exact
  product-hypergeometric null.
- Exact convolution and the factorized saddlepoint can be combined
  deterministically.
- Observable support/work bounds identify many coarse cases that should be
  handled exactly.
- The routed test is much better calibrated than chi-square on the tested
  sparse/skewed regimes and remains well calibrated on the included balanced
  controls.
- Repeated-component grouping can make the method materially faster than
  1,000 JIDT permutations while removing Monte Carlo tail resolution.

The evidence does not establish:

- validity for non-binary `X` and `Y`;
- unconditional optimality of conditioning on all observed margins;
- power relative to permutation under alternatives;
- validity under temporal dependence or transfer-entropy embeddings;
- a universal finite-sample error bound for Lugannani-Rice;
- novelty of saddlepoint conditional testing; or
- superiority to chi-square in every table.

Numerical exact convolution also rounds support sums to 12 decimals. It is
validated against brute force on small cases, but should be described as
"numerically exact" rather than symbolic exactness.

## Thesis Recommendation

Proceed, subject to supervisor approval of the narrowed novelty claim:

> A deterministic fixed-margin significance test for binary conditional
> mutual information, using bounded exact convolution and a factorized
> saddlepoint approximation, with a validated regime router and comparison to
> chi-square and JIDT.

The contribution is primarily the CMI-specific construction, bounded routing
algorithm, software, null audit, and validation map. General conditional
saddlepoint theory and exact conditional contingency-table inference are prior
art.

## Next Experiments

1. Repeat the full confirmation grid with at least two additional random seeds
   and add binomial uncertainty intervals to Monte Carlo-reference errors.
2. Add conditional alternatives to measure power and not only Type-I error.
3. Add dense, classical chi-square controls with clearly adequate expected
   counts, verifying that routing does not sacrifice standard-regime behavior.
4. Formally map the finite-support setup to the assumptions in Niu, Ray
   Choudhury, and Katsevich's conditional saddlepoint theorem.
5. Complete the citation-chain novelty review and a one-page comparison to
   `spaCRT`.
6. Decide whether larger alphabets are a thesis extension or explicit future
   work; their fixed-margin fibers are multidimensional and are not solved by
   this binary implementation.

## Reproducible Artifacts

- Full validation:
  `results/saddlepoint_full_k100000_b1000/`
- Direct JIDT anchors:
  `results/jidt_blockwise_anchors_b1000_k200000/`
- High-shuffle JIDT tie reproduction:
  `results/jidt_tie_anchor_b100000/`
- Novelty boundary:
  `docs/NOVELTY_AUDIT_AND_CLAIM_BOUNDARY.md`
- JIDT source audit:
  `docs/JIDT_CMI_BASELINE_AUDIT.md`
