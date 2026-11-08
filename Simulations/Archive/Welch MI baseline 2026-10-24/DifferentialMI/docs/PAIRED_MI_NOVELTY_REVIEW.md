# Literature Review: Paired Weak-Null Tests for Equal Discrete Mutual Information

Review date: 25 July 2026

## Executive Verdict

The proposed method is:

```text
Data: paired IID units Zi = (XA_i, YA_i, XB_i, YB_i)

Target: Delta = I_A(XA; YA) - I_B(XB; YB)

Null: H0: Delta = 0

Inference: a deterministic influence-function / delta-method Wald test
that estimates the covariance between the two MI estimators from the
paired observations.
```

The broad novelty claims are not supported.

- Tests comparing association measures across contingency tables existed
  by at least Zografos (1993). Shannon mutual information is a special case
  of the association measure in that paper.
- The influence function, first-order variance, and asymptotic normality of
  nonzero discrete MI are established results.
- Estimating covariance between two statistics measured on the same units
  is standard paired delta-method and repeated-categorical-data theory.
- When both MI values share the same target `Y`, the proposed statistic
  reduces algebraically to a pointwise conditional log-likelihood ratio.
  This is the structure of Vuong's model-closeness test.
- A June 2026 preprint already formulates
  `H0: I(X1;Y) = I(X2;Y)` for dependent predictors and proposes a paired
  swap permutation test.

The following narrow claim remains plausible, but is not proven by a web
search:

> To our knowledge, this is the first explicit, deterministic,
> covariance-aware Wald procedure developed and systematically validated
> for the weak null of equal discrete mutual information in general paired
> condition data `(XA,YA,XB,YB)`, while allowing the two condition-specific
> joint distributions and marginals to differ.

This is a viable master's thesis direction if the contribution is framed as
an MI-specific synthesis, finite-sample refinement, validation study, and
software implementation. The unrefined first-order formula alone is too
close to established statistical theory to support a strong methodological
novelty claim.

Novelty confidence for the narrow claim: **moderate, provisional**.

## The Exact Candidate Method

Suppose the data consist of `n` independent subjects. Subject `i` supplies
four categorical measurements:

```text
Zi = (XA_i, YA_i, XB_i, YB_i).
```

The observations within a subject may be arbitrarily dependent. Subjects
are assumed IID.

Let `P_A` and `P_B` be the two condition-specific joint distributions. The
scientific estimand is

```text
Delta = I(P_A) - I(P_B).
```

The weak null is

```text
H0: I(P_A) = I(P_B).
```

It does not require:

```text
P_A = P_B,
(XA,YA) exchangeable with (XB,YB),
equal condition-specific marginals,
or equal condition-specific conditional distributions.
```

For a discrete distribution `P`, define the local log density ratio

```text
l_P(x,y) = log[p(x,y) / {p_X(x) p_Y(y)}].
```

Then

```text
I(P) = E_P[l_P(X,Y)]
```

and, away from independence and the boundary of the probability simplex,
the influence function is

```text
psi_P(x,y) = l_P(x,y) - I(P).
```

For the paired contrast, the influence function is

```text
psi_Delta(ZA,ZB) = psi_A(ZA) - psi_B(ZB).
```

Therefore,

```text
sqrt(n) (Delta_hat - Delta)
  -> Normal(0, V_Delta)

V_Delta
  = Var[psi_A(ZA) - psi_B(ZB)]
  = V_A + V_B - 2 Cov[psi_A(ZA), psi_B(ZB)].
```

An empirical implementation computes

```text
d_i = l_A_hat(XA_i,YA_i) - l_B_hat(XB_i,YB_i)

Delta_hat = mean(d_i)

SE_hat = sd(d_i) / sqrt(n)

Z = Delta_hat / SE_hat.
```

The equality `Delta_hat = mean(d_i)` is exact for plug-in discrete MI.
Thus, the proposed method can also be understood as a paired asymptotic test
on estimated local-information differences. It is not a paired t-test on
one independently estimated MI value per subject.

A leading plug-in bias correction may be applied to the numerator:

```text
I_BC = I_hat - (r-1)(c-1)/(2n)
```

when the fixed, positive support assumptions justify it. The correction is
classical and does not change the first-order covariance formula.

## Why the Mathematics Is Not New in Principle

The complete paired observation `Z` has one joint multinomial distribution
over the product alphabet. Both condition-specific contingency tables are
margins of that one distribution.

Define the functional

```text
T(R) = I(R_A) - I(R_B),
```

where `R` is the distribution of
`(XA,YA,XB,YB)` and `R_A`, `R_B` are its two relevant margins. The
multivariate delta method applied to `T(R_hat)` immediately gives the
paired covariance term.

This places the method inside several established bodies of theory:

1. smooth-function inference for multinomial probabilities;
2. repeated-measures categorical-data analysis;
3. influence-function or von Mises inference for information functionals;
4. paired Wald tests for correlated estimators; and
5. tests comparing two dependent measures of association.

Grizzle, Starmer, and Koch (1969) developed a general linear-model approach
to functions of categorical response probabilities. Later repeated-measures
extensions explicitly handle multivariate categorical observations and
their covariance. Kritzer (1977) described variance-covariance estimation
for several measures of association derived from contingency tables and
the testing of hypotheses about those measures.

These works do not appear to write the exact paired MI formula above, but
they contain the statistical machinery needed to derive it. Consequently,
the covariance principle itself is not defensibly novel.

Sources:

- [Grizzle, Starmer, and Koch (1969), *Analysis of Categorical Data by
  Linear Models*](https://doi.org/10.2307/2528901)
- [Koch et al. (1977), *A General Methodology for the Analysis of
  Experiments with Repeated Measurement of Categorical
  Data*](https://doi.org/10.2307/2529309)
- [Kritzer (1977), *Analyzing Measures of Association Derived From
  Contingency Tables*](https://doi.org/10.1177/004912417700500401)

## Direct Historical Predecessor: Zografos (1993)

Zografos studies `phi`-divergence association between the joint
distribution in a contingency table and the product of its marginals.
For

```text
phi(u) = u log(u),
```

the association functional is Linfoot's informational measure, which is
ordinary Shannon mutual information in nats.

Section 4 explicitly constructs tests for:

```text
H0: association(table 1) = association(table 2)
```

using

```text
{I_hat_1 - I_hat_2}
/
sqrt(sigma_1^2/N_1 + sigma_2^2/N_2),
```

with an asymptotic standard normal reference distribution. It also extends
the comparison to more than two tables.

This is decisive prior art for an analytic equal-MI test under separate
multinomial sampling. It rules out claims such as:

```text
"the first analytic test of equal discrete MI"
"the first weak-null test of I(P)=I(Q)"
"the first Wald comparison of two MI values"
```

Its limitation relative to the proposed project is that the displayed
two-table variance adds the two sampling variances and does not include a
paired cross-covariance. The proposed paired method is therefore best viewed
as a dependent-sample extension of this established test.

Primary source:
[Zografos (1993), *Asymptotic Properties of phi-Divergence Statistic and
Its Applications in Contingency Tables*](https://olympias.lib.uoi.gr/jspui/bitstream/123456789/12570/1/Zografos-1993-Asymptotic%20properties%20of.pdf).

## Earlier and Later MI Asymptotic Theory

The one-MI ingredients are also established.

- Lomnicki and Zaremba (1959) studied asymptotic distributions of
  transmitted information.
- Moddemeijer (1989) derived leading bias and variance results for the
  histogram-based MI estimator.
- Moddemeijer (1999) extended variance estimation to serially dependent
  observation pairs. This is dependence across time, not covariance between
  two condition-specific MI estimates, but it makes broad claims about
  "the first dependent MI variance" unsafe.
- Brillinger (2004) presented delta-method MI analysis and the regular
  non-null variance.
- Mora and Ruiz-Castillo's segregation work derives asymptotic normality
  for the Mutual Information index and motivates pairwise comparisons
  between populations and time periods.
- Kandasamy et al. (2015) developed influence-function estimators and
  normal approximations for entropy, divergence, and MI functionals.

For ordinary discrete MI away from independence, these lines of work yield
the same first-order variance:

```text
Var_P(log[p_XY / (p_X p_Y)]).
```

Sources:

- [Lomnicki and Zaremba (1959), *The Asymptotic Distributions of Estimators
  of the Amount of Transmitted Information*](https://doi.org/10.1016/S0019-9958(59)90223-2)
- [Moddemeijer (1989), *On Estimation of Entropy and Mutual Information of
  Continuous Distributions*](https://doi.org/10.1016/0165-1684(89)90132-1)
- [Moddemeijer (1999), dependent-pair MI variance](https://doi.org/10.1016/S0165-1684(98)00224-2)
- [Brillinger (2004), *Some Data Analyses Using Mutual
  Information*](https://www.stat.berkeley.edu/~brill/Papers/bjps1.pdf)
- [Mora and Ruiz-Castillo, statistical properties of the MI segregation
  index](https://www.researchgate.net/publication/4724169_The_statistical_properties_of_the_Mutual_Information_index_of_multigroup_segregation)
- [Kandasamy et al. (2015), *Influence Functions for Machine
  Learning*](https://arxiv.org/abs/1411.4342)

## The Shared-Outcome Case Is Closely Related to Vuong

Consider the important special design:

```text
Zi = (Y_i, X1_i, X2_i)
```

with a common target `Y`. Then

```text
I(X1;Y) - I(X2;Y)
  = E[
      log p(Y|X1) - log p(Y)
      - log p(Y|X2) + log p(Y)
    ]
  = E[log {p(Y|X1) / p(Y|X2)}].
```

The common `log p(Y)` term cancels. The empirical local MI difference is
therefore the pointwise log-likelihood ratio

```text
m_i = log {p_hat(Y_i|X1_i) / p_hat(Y_i|X2_i)}.
```

The proposed paired statistic becomes

```text
sqrt(n) mean(m_i) / sd(m_i),
```

which is the characteristic statistic in Vuong's test of whether two models
are equally close to the data-generating process in Kullback-Leibler risk.

This equivalence has two implications:

1. a deterministic covariance-aware paired test for the shared-`Y` design
   is not a clean new statistical invention; and
2. Vuong theory, including its regularity and degeneracy issues, must be
   discussed in any thesis using this design.

The fully general `(XA,YA,XB,YB)` design does not literally compare two
models for one common response, but it remains the same general idea:
studentize paired pointwise information contributions.

Sources:

- [Vuong (1989), *Likelihood Ratio Tests for Model Selection and
  Non-Nested Hypotheses*](https://doi.org/10.2307/1912557)
- [Mrkvicka and Radimsky (2026), which explicitly uses Vuong as the
  asymptotic comparator for equal categorical MI](https://arxiv.org/abs/2606.26949)

## Closest Current Paper: Mrkvicka and Radimsky (2026)

The June 2026 preprint *Exact Comparison of Explanatory Strength of Two
Dependent Predictors* is the closest direct paper found in this review.

It studies:

```text
H0: S(X1,Y) = S(X2,Y)
```

for two dependent predictors measured on the same observations. In its
categorical section, it chooses MI and writes:

```text
H0: I(X1;Y) = I(X2;Y).
```

Its proposed Paired Swap Permutation Test independently swaps `X1_i` and
`X2_i` within each observation and recomputes the difference in MI. The
paper compares this procedure with a Vuong asymptotic test, a naive
permutation, and a paired bootstrap.

This paper rules out:

```text
"the first paired comparison of two MI values"
"the first test of I(X1;Y)=I(X2;Y) for dependent predictors"
"the first use of within-unit dependence in an MI comparison"
```

However, it is not identical to the proposed method.

| Feature | 2026 paired-swap paper | Proposed paired Wald method |
|---|---|---|
| Observation | `(Y,X1,X2)` | `(XA,YA,XB,YB)` |
| Target outcome | One shared `Y` | May differ by condition |
| Inference | Random swap distribution | Deterministic normal approximation |
| Main requirement | Functional exchangeability under swaps | IID subjects and regular smooth-functional conditions |
| Predictor alphabets | Restricted to the same state space for categorical data | Need not match merely to compare scalar MI |
| Marginals/joint laws | Swap validity restricts them | May differ under the weak null |
| Computational character | Resampling, unless all swaps are enumerated | One pass after table construction |

There is also an important null-hypothesis distinction. Equal scalar MI does
not imply that

```text
(Y,X1,X2) has the same distribution as (Y,X2,X1).
```

The latter joint invariance, or an equivalent randomization assumption, is
what makes raw within-pair swaps finite-sample exact. The preprint's
categorical development explicitly adds equality of conditional laws,

```text
P(Y|X1) = P(Y|X2),
```

after initially writing an equal-MI null. Equal conditional laws are much
stronger than equal scalar MI, and even swap exactness must ultimately be
justified by the required joint exchangeability or study randomization.

The fair conclusion is:

> The paired-swap procedure may be exact under its stronger functional
> exchangeability assumptions. It is not an exact test for every pair of
> distributions satisfying only `I(X1;Y)=I(X2;Y)`.

That distinction leaves room for a weak-null procedure that allows unequal
marginals and nonexchangeable condition distributions.

Primary source:
[Mrkvicka and Radimsky (2026), arXiv:2606.26949](https://arxiv.org/abs/2606.26949).

## Strong Null Versus Weak Null

Three different questions must not be conflated.

### Independence

```text
H0: I(X;Y) = 0.
```

This is the standard one-table MI significance problem. Chi-squared
approximations and JIDT's usual surrogate significance calculations target
this problem.

### Strong Paired Equality

```text
H0: (XA,YA,XB,YB)
    is invariant when A and B are swapped within each subject.
```

This can justify an exact within-pair permutation test.

### Weak Equality of MI

```text
H0: I_A(XA;YA) = I_B(XB;YB).
```

This constrains one scalar functional. It does not make the observations
exchangeable. A raw paired swap is not generally finite-sample exact for
this null.

Studentized paired resampling can sometimes be asymptotically valid for a
weak parameter null even without exact exchangeability, but then the claim
is asymptotic, not finite-sample exact.

Source:
[Konietschke and Pauly (2014), *Bootstrapping and Permuting Paired t-Test
Type Statistics*](https://doi.org/10.1007/s11222-012-9370-4).

## Applied MI-Difference Practice

The scientific question of comparing MI values is not new.

- MINDy partitions observations into high- and low-modulator groups and
  tests a difference between MI values using empirical resampling.
- Neuroimaging and neural-coding work has compared MI-based quantities
  using permutation, jackknife variance estimates, or tests on
  subject-level summaries.
- Boughter et al. compare discrete MI values between immune-repertoire
  populations using label permutation.
- Bystrova et al. explicitly write equality of conditional MI across two
  distributions, although their paper does not instantiate the proposed
  paired finite-table procedure.

These papers do not necessarily solve the general paired weak-null problem.
They do show that neither the scientific estimand nor MI-difference testing
itself is new.

Representative sources:

- [Wang et al. (2006), MINDy](https://nemenmanlab.org/~ilya/images/e/e6/Wang-etal-06.pdf)
- [Wang et al. (2009), MINDy follow-up](https://nemenmanlab.org/~ilya/images/d/d4/Wang-etal-09.pdf)
- [Hart and Giszter (2010), MI comparisons with jackknife
  uncertainty](https://pmc.ncbi.nlm.nih.gov/articles/PMC6633785/)
- [Boughter et al. (2020)](https://doi.org/10.7554/eLife.61393)
- [Boughter et al. (2023)](https://doi.org/10.1371/journal.pcbi.1011577)
- [Bystrova et al. (2024), Information-Theoretic Causal Difference
  Graphs](https://openreview.net/forum?id=nCR1425CpP)

## Adjacent Tests That Establish the General Pattern

Several classical methods use the same overall architecture for other
functionals.

- Tests comparing dependent Pearson correlations retain the covariance
  created by measuring both correlations on the same individuals.
- DeLong's test compares correlated ROC AUC estimates by estimating their
  covariance.
- Paired multinomial proportion tests use the joint paired table rather than
  adding two independent variances.
- Delta-method tests compare entropy values from multinomial samples.

These are analogues, not direct MI implementations. They matter because
they show that "estimate a scalar functional in each condition, estimate
their covariance, and studentize the difference" is established
statistical design.

Sources:

- [Steiger (1980), tests for dependent correlation
  coefficients](https://doi.org/10.1037/0033-2909.87.2.245)
- [DeLong, DeLong, and Clarke-Pearson (1988), correlated ROC
  areas](https://doi.org/10.2307/2531595)
- [Rey et al. (2023), comparison of multinomial entropy
  values](https://doi.org/10.3390/e25050734)

## Software Audit

No mainstream package was found that exposes the exact general API:

```text
paired_equal_discrete_mi(XA, YA, XB, YB)
```

with an analytic weak-null p-value, covariance diagnostics, bias handling,
and a repeated-condition extension.

Relevant software instead covers neighboring problems:

- JIDT estimates MI and tests one MI against an independence surrogate null.
  It does not provide this paired equal-MI contrast as a standard test.
- `segregation::mutual_difference` compares two MI segregation indices and
  can bootstrap uncertainty, but it is oriented toward separate
  contingency-table populations and does not expose the proposed
  subject-paired covariance.
- General MI packages such as `infotheo`, `pyitlib`, and `infomeasure`
  estimate MI or test independence but do not advertise this paired
  weak-null procedure.
- The 2026 paired-swap authors provide a resampling implementation for the
  shared-target design, not the proposed deterministic four-variable Wald
  procedure.

Sources:

- [JIDT repository and documentation](https://github.com/jlizier/jidt)
- [`segregation::mutual_difference`](https://elbersb.github.io/segregation/reference/mutual_difference.html)
- [`segregation` inference vignette](https://elbersb.github.io/segregation/articles/segregation.html)
- [`infomeasure` statistical tests](https://infomeasure.readthedocs.io/en/0.6.2/guide/statistical_tests/)

Software absence is not strong mathematical novelty, but a clear,
well-tested implementation can still be a useful thesis deliverable.

## Claim Matrix

| Candidate claim | Verdict | Reason |
|---|---|---|
| First test of `I(P)=I(Q)` | False | Zografos, segregation literature, and applied MI-difference tests |
| First analytic comparison of two discrete MI values | False | Zografos (1993) |
| First paired comparison of MI | False | Applied work and the 2026 paired-swap preprint |
| First paired test of `I(X1;Y)=I(X2;Y)` | False | 2026 paired-swap paper; shared-`Y` case also maps to Vuong |
| First MI influence function or variance | False | Classical MI asymptotic and influence-function literature |
| First use of covariance for paired estimators | False | Standard delta-method and repeated-categorical-data theory |
| First bias correction for an MI contrast | False or unsupported | Classical MI bias correction and prior applications |
| First explicit analytic test for general `(XA,YA,XB,YB)` paired weak-null MI equality | Plausible, provisional | No exact paper was found, but it is a routine specialization of general theory |
| First systematic finite-sample study of that general paired test under skewness and sparsity | Plausible, provisional | No matching benchmark was found |
| First production-quality implementation with diagnostics and repeated-condition contrasts | Plausible, but scientifically secondary | No matching package was found |
| A new fundamental statistical test | Not defensible | Core result is a standard smooth-functional paired Wald test |

## What Could Still Be a Real Contribution

The strongest thesis is not "we invented the paired covariance formula."
It is a carefully bounded methods contribution:

1. give the first clear MI-specific derivation for the general paired
   four-variable design;
2. distinguish the weak equal-MI null from exchangeability and
   independence nulls;
3. show exactly when ignoring covariance loses or inflates precision;
4. develop finite-sample bias and sparsity handling beyond the raw Wald
   formula;
5. characterize failure near independence, where the first derivative and
   influence variance vanish;
6. validate calibration, confidence-interval coverage, and power across
   paired dependence strengths, marginal skewness, alphabet sizes, and
   sample sizes;
7. compare against paired bootstrap, studentized paired permutation,
   paired swap under exchangeable designs, and an independence-style
   analysis that answers the wrong null;
8. extend the covariance construction to `K` repeated conditions and
   planned contrasts; and
9. release reproducible software with diagnostics that prevent users from
   silently applying the asymptotic test outside its operating regime.

The finite-sample refinement is especially important. Away from
independence, the first-order test is straightforward. Near independence,
the MI gradient is zero and a second-order, non-normal limit appears. Sparse
or boundary cells create additional nonregularity. A successful
deterministic bridge across some of these regimes would be more
methodologically substantial than the basic paired Wald formula.

## Recommended Thesis Wording

### Do Not Say

- "the first test for equality of mutual information";
- "the first paired MI test";
- "the first analytical MI comparison";
- "a new influence-function variance for MI";
- "the first method that accounts for dependence between MI estimates";
- "paired permutation is invalid" without specifying the weak null; or
- "the 2026 paired-swap method is invalid" without acknowledging its
  stronger exchangeability assumptions.

### Safe Current Wording

> This thesis studies deterministic weak-null inference for differences in
> discrete mutual information measured on paired units. Building on
> established multinomial delta-method and MI variance theory, it derives
> an explicit covariance-aware implementation for general
> `(XA,YA,XB,YB)` data, distinguishes equal MI from exchangeability, and
> maps the method's finite-sample calibration across skewed and sparse
> contingency-table regimes.

### Strongest Provisional Wording

> To our knowledge, this is the first systematic development and
> finite-sample validation of an explicit analytic weak-null test for equal
> discrete mutual information in general paired-condition data, with
> arbitrary condition-specific marginals and outcomes.

The words "to our knowledge," "systematic," "general paired-condition," and
"weak-null" are essential. This statement still requires formal database
searches and supervisor review.

## Go or No-Go Recommendation

**Go, conditionally.**

Proceed if the intended thesis contribution is:

```text
MI-specific derivation
+ weak-null clarification
+ finite-sample refinement
+ adversarial validation
+ useful software.
```

Do not proceed on the premise that this is a wholly new paired test. If the
project stops at

```text
Z = (I_hat_A - I_hat_B)
    / sqrt(V_A + V_B - 2 Cov_A,B),
```

then the contribution is too routine. The project becomes defensible when
it establishes where this very fast deterministic test works, where it
fails, and how to improve or route it in the skewed, sparse regimes that
motivate the research.

## Search Method and Limits

The review searched exact phrases and conceptual variants including:

- `"paired mutual information" test`;
- `"difference in mutual information" paired`;
- `"equality of mutual information" dependent samples`;
- `"I(X1;Y)=I(X2;Y)"`;
- covariance and joint asymptotic distributions of MI estimators;
- dependent measures of association in contingency tables;
- repeated-measures categorical-data delta methods;
- paired entropy and divergence comparisons;
- Vuong tests and pointwise log-likelihood ratios;
- paired permutation, exchangeability, and weak-null studentization;
- MI-difference applications in neuroscience, genomics, immunology,
  sociology, and causal discovery; and
- functionality in JIDT and common R/Python information-theory packages.

Sources included publisher pages, primary PDFs, arXiv, PubMed/PMC, RePEc,
institutional repositories, software documentation, and backward/forward
citation trails available through web search.

No literature search can prove that a method has never appeared. Before a
paper makes a priority claim, the following due diligence remains:

1. run authenticated searches in Scopus and Web of Science;
2. search MathSciNet and zbMATH for divergence and contingency-table
   association contrasts;
3. search ProQuest Dissertations and institutional thesis repositories;
4. forward-chain Zografos (1993), Vuong (1989), Moddemeijer (1999),
   Kritzer (1977), and Mrkvicka and Radimsky (2026);
5. search non-English databases and terminology such as information
   measure of association, transmitted information, and MI segregation
   index;
6. have a mathematical statistician review the claimed distinction from
   Vuong and general multinomial Wald theory; and
7. preserve a dated search log and inclusion/exclusion table for the thesis
   appendix.

## Core References

- [Grizzle, Starmer, and Koch (1969)](https://doi.org/10.2307/2528901)
- [Kritzer (1977)](https://doi.org/10.1177/004912417700500401)
- [Vuong (1989)](https://doi.org/10.2307/1912557)
- [Moddemeijer (1989)](https://doi.org/10.1016/0165-1684(89)90132-1)
- [Zografos (1993)](https://olympias.lib.uoi.gr/jspui/bitstream/123456789/12570/1/Zografos-1993-Asymptotic%20properties%20of.pdf)
- [Moddemeijer (1999)](https://doi.org/10.1016/S0165-1684(98)00224-2)
- [Brillinger (2004)](https://www.stat.berkeley.edu/~brill/Papers/bjps1.pdf)
- [Mora and Ruiz-Castillo](https://www.researchgate.net/publication/4724169_The_statistical_properties_of_the_Mutual_Information_index_of_multigroup_segregation)
- [Kandasamy et al. (2015)](https://arxiv.org/abs/1411.4342)
- [Konietschke and Pauly (2014)](https://doi.org/10.1007/s11222-012-9370-4)
- [Rey et al. (2023)](https://doi.org/10.3390/e25050734)
- [Bystrova et al. (2024)](https://openreview.net/forum?id=nCR1425CpP)
- [Mrkvicka and Radimsky (2026)](https://arxiv.org/abs/2606.26949)
