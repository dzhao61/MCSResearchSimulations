# JIDT Conditional MI Significance Baseline Audit

## Finding

JIDT's default discrete conditional-MI permutation method is not a general
conditional permutation test for

```text
X independent of Y given Z.
```

In the local JIDT source,
`ConditionalMutualInformationCalculatorDiscrete.computeSignificance(int)`
generates unrestricted permutations of all `N` observations. The implementation
holds variable 2 and the conditional variable fixed, then globally reorders
variable 1.

Relevant local source:

```text
.../ConditionalMutualInformationCalculatorDiscrete.java:464-554
```

The source documentation itself says that it fixes the relationship between
variable 2 and the conditional and shuffles variable 1 with respect to them.

## Consequence

A global shuffle destroys both:

- any association between `X` and `Y` within `Z`; and
- the nuisance relationship between `X` and `Z`.

The general conditional-independence null permits `P(X | Z)` to vary with
`Z`. Therefore JIDT's default surrogate distribution does not preserve the
null's nuisance structure when `X` depends on `Z`.

It is valid only under a stronger exchangeability condition, such as `X`
having the same distribution across all conditioning states.

## Correct reference for this project

The project uses within-stratum permutation:

```text
for each z:
    hold the X and Y margins in stratum z fixed
    permute one binary label vector only inside that stratum
```

Equivalently, sample independently:

```text
A_z | n_z, r_z, s_z ~ Hypergeometric(n_z, s_z, r_z).
```

The equivalence is checked independently in the unit tests by exhaustively
enumerating all observation-level label assignments for a small stratum.

## Floating-point tie behavior

JIDT's implementation increments its exceedance count when

```java
newCondMI >= actualCondMI
```

with no numerical tolerance. In coarse conditional null distributions, many
different permutations can be mathematically tied but accumulate their
floating-point MI terms in different orders. JIDT can consequently count only
part of a probability atom.

This was reproduced on `homogeneous_k20_n10_both_skew`. With 100,000 explicit
within-stratum JIDT permutations:

| Quantity | p-value |
|---|---:|
| Exact inclusive conditional tail | 0.132953 |
| JIDT raw reported p-value | 0.108290 |
| Recomputed from JIDT surrogates with `G^2` tolerance `1e-10` | 0.132850 |

The manual and JIDT observed `G^2` values differed by only `4.3e-14`, ruling
out a bits/nats conversion problem. The saved reproduction is in
`results/jidt_tie_anchor_b100000/`.

This issue matters for discrete inclusive-tail tests. A fair comparison should
save JIDT's surrogate statistics and recompute exceedances with a documented
tolerance, while also retaining JIDT's raw p-value for transparency.

## How JIDT should be used in later benchmarking

- Report JIDT's default result as a separate baseline with a clearly labelled
  stronger/null-mismatch warning.
- For a fair conditional-permutation benchmark, provide explicit blockwise
  orderings through JIDT's `computeSignificance(int[][])` overload, after
  verifying the reconstructed observation ordering.
- Recompute inclusive-tail ranks from the returned surrogate distribution with
  a small statistic-scale tolerance, and report both raw and corrected values.
- Do not describe default JIDT CMI shuffling as ground truth in heterogeneous
  `P(X | Z)` regimes.
- JIDT returns discrete CMI in bits; use consistent units if comparing the
  statistic itself. Permutation ranks are invariant to the bits/nats scale.
