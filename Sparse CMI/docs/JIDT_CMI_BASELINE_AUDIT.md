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

## How JIDT should be used in later benchmarking

- Report JIDT's default result as a separate baseline with a clearly labelled
  stronger/null-mismatch warning.
- For a fair conditional-permutation benchmark, provide explicit blockwise
  orderings through JIDT's `computeSignificance(int[][])` overload, after
  verifying the reconstructed observation ordering.
- Do not describe default JIDT CMI shuffling as ground truth in heterogeneous
  `P(X | Z)` regimes.
- JIDT returns discrete CMI in bits; use consistent units if comparing the
  statistic itself. Permutation ranks are invariant to the bits/nats scale.

