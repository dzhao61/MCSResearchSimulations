# Focused Novelty Audit: Differential Discrete Mutual Information

Date: 25 July 2026

## Question Audited

The candidate thesis problem is inference for

```text
H0: I_P(X;Y) = I_Q(X;Y)
```

from two independent samples of discrete `(X,Y)` pairs, allowing `P != Q`.
This differs from:

- testing independence within one population, `I(P) = 0`;
- testing whether two full distributions are equal, `P = Q`;
- using MI between a group label and measurements as a two-sample statistic;
- estimating one MI value accurately.

## Search Scope

The search used exact-title, keyword, and citation-chain queries around:

- equality or difference of mutual information across two samples;
- two multinomial populations and entropy/MI confidence intervals;
- jackknife and bias-corrected MI;
- influence functions and delta methods for MI;
- weak-null and studentized permutation tests;
- MI-based two-sample tests.

Primary papers and publisher or repository versions were preferred. This was
a focused technical audit, not a systematic review of Scopus, Web of Science,
MathSciNet, dissertations, and non-English literature.

## What Is Established Prior Art

| Ingredient | Prior-art finding | Novel here? |
|---|---|---|
| Plug-in discrete MI | Classical multinomial functional | No |
| Leading MI bias `(r-1)(c-1)/(2n)` | Derived in the entropy/MI estimation literature, including Moddemeijer | No |
| First-order MI variance | Moddemeijer gives `Var(log[p_XY/(p_X p_Y)])/n` | No |
| MI influence-function inference | Modern influence-function literature treats MI and related functionals | No |
| Delete-one jackknife MI | Used for bias-corrected MI in applied and methodological work | No |
| Weak-null raw-permutation failure | General parameter-permutation theory establishes this failure | No |
| Studentized weak-null permutation | Chung and Romano establish the general asymptotic result | No |
| Delta-method comparison of multinomial information functionals | Closely neighboring work exists for entropy | No |
| One-sample MI significance and confidence bounds | Extensive existing literature | No |

The most important correction to the initial project framing is that the exact
first-order variance used by our Wald test is already present in
Moddemeijer's 1989 analysis. A thesis cannot claim that variance formula or
the associated delta method as a new method.

## Nearby Work That Is Not the Same Target

- Guha and Chothia test whether two continuous distributions are identical by
  measuring dependence between sample label and observation. Their null is
  `P = Q`, not equality of the within-population MI values.
- Recent generalized-MI two-sample tests similarly use MI-like divergences to
  test equality of full continuous distributions.
- Rey et al. compare entropy values between multinomial samples. This is a
  very close methodological analogue, but entropy equality is not MI
  equality.
- Stefani et al. provide finite-alphabet bounds for one MI value, not a
  direct two-population equal-MI test.
- Kandasamy et al. derive general influence-function estimators for
  information functionals, but do not appear to make this discrete equal-MI
  comparison the main problem.

## Search Result for the Exact Problem

This focused search did not locate a paper whose primary target is the
regular two-sample discrete null

```text
I(P) = I(Q), with P and Q otherwise unrestricted.
```

That absence is encouraging, but it is not proof of novelty. The result must
be phrased as "no direct treatment was located in the focused search" until a
formal library search and supervisor review are complete.

## Honest Novelty Boundary

A paper or thesis that only:

1. writes down two plug-in MI estimates;
2. inserts the known first-order variances; and
3. uses a normal or studentized permutation reference

would probably be too incremental as a methodological contribution. All
three ingredients follow fairly directly from established theory.

A defensible master's thesis can still make a useful contribution by
developing and validating the problem as a coherent information-theoretic
procedure:

- explicitly formulate differential discrete MI under the weak null;
- quantify how badly raw permutation fails for this target;
- compare classical analytic bias correction, jackknife correction, Wald,
  and studentized permutation in finite samples;
- identify a transparent regular operating regime from observable table
  diagnostics;
- provide reproducible software and a broad adversarial benchmark;
- extend the procedure to simultaneous differential-MI comparisons, if time
  permits.

The strongest current wording is:

> A finite-sample validation and practical inference framework for
> differences in discrete mutual information across heterogeneous
> multinomial populations.

It should not currently be described as a fundamentally new asymptotic test.

## Go/No-Go Implication

The project remains suitable for a focused master's thesis if robust testing
shows that:

- a deterministic correction is reliably calibrated in a clearly stated
  regular regime;
- it materially improves on raw permutation for the equal-MI weak null;
- jackknife correction offers measurable value beyond the classical
  first-order analytic correction, or the simpler analytic correction is
  adopted instead;
- failures can be predicted using observable diagnostics rather than hidden
  knowledge of the population distribution.

If jackknife and analytic correction perform equivalently, the cleaner
analytic method should be preferred. If neither can be assigned a useful
observable operating regime, the methodological claim is too weak.

Near-independence theory is intentionally deferred at this stage. It should
be reported as an excluded boundary, not used as a pass/fail criterion for
the regular-case thesis.

## Update After Randomized Validation

The subsequent two-seed randomized experiment found that the classical
analytic bias correction was slightly better calibrated than the delete-one
jackknife. This strengthens the practical baseline but further weakens any
claim that the current estimator is itself novel.

The experiment also exposed an MI-specific permutation boundary: two regular
populations with opposite association directions can have an almost
independent pooled mixture. Studentized permutation then violates its
positive-mixture-variance assumption, while deterministic two-sample Wald
inference can remain regular. This is a useful theoretical and practical
observation, but it is an implication of general permutation theory rather
than a new permutation theorem.

The recommended new-method target is now a deterministic finite-sample tail
refinement for highly unequal, low-density samples. Without such a
refinement, simultaneous-inference extension, or another substantive
addition, the current work is best described as a carefully validated
application framework rather than a new foundational estimator.

## Remaining Novelty Work

Before making a formal originality claim:

1. Search Scopus, Web of Science, MathSciNet, ProQuest dissertations, and
   Google Scholar citation chains using the exact target and synonyms.
2. Trace citations to Moddemeijer, entropy-comparison papers, jackknife MI,
   and Chung-Romano for direct equal-MI applications.
3. Ask a statistician or supervisor to challenge the proposed claim boundary.
4. Record search strings, dates, and inclusion decisions in the thesis.

## Primary Sources

- Moddemeijer (1989), entropy and MI bias/variance:
  https://doi.org/10.1016/0165-1684(89)90132-1
- Chung and Romano (2013), weak-null studentized permutation:
  https://doi.org/10.1214/13-AOS1090
- Kandasamy et al. (2015), influence-function estimators for information
  functionals: https://arxiv.org/abs/1411.4342
- Stefani et al. (2013), finite-alphabet MI confidence bounds:
  https://arxiv.org/abs/1301.5942
- Rey et al. (2023), comparison of entropies from multinomial samples:
  https://doi.org/10.3390/e25050734
- Guha and Chothia (2014), MI-based `P = Q` two-sample testing:
  https://doi.org/10.1177/0008068320140103
