# Extensive Literature Review: Equality of Mutual Information

Review date: 25 July 2026

## Executive Verdict

The broad novelty claim is not supported:

> "This is the first weak-null test of `I(P) = I(Q)`."

The review found earlier work that reaches the same mathematical target.
Most importantly, Mora and Ruiz-Castillo (2009) study the Mutual Information
segregation index for a nonparametric multinomial contingency table, derive
its regular asymptotic normal distribution, and explicitly state that the
result permits pairwise tests of MI levels across cities, countries, schools,
and time periods. Their M-index is ordinary Shannon mutual information.

The modern `segregation` R package makes the overlap operational: it accepts
two contingency-table datasets, reports the difference between their two
M-indices, and can use bootstrap bias correction, standard errors, and
confidence intervals. Earlier neuroscience, genomics, and immunology papers
also test differences between MI values by permutation or resampling.

The current analytic test is still potentially useful, but its contribution
must be narrower:

> A fast bias-corrected implementation and systematic finite-sample
> validation of equal discrete MI inference, with particular attention to
> heterogeneous margins, sparse tables, and the failure of raw group-label
> permutation under the composite equal-MI null.

This is a potentially worthwhile master's thesis contribution. It is not the
first formulation of the null, the first MI-difference test, or a new
first-order asymptotic test.

## Exact Question

Let

```text
P = distribution of (X, Y) in population 1
Q = distribution of (X, Y) in population 2
```

and let the two samples be independent. The target null is

```text
H0: I_P(X;Y) = I_Q(X;Y),
```

while allowing

```text
P != Q.
```

This is a weak, composite, or parameter null. It is weaker than equality of
the complete joint distributions.

For the primary project scope:

- `X` and `Y` are discrete with fixed finite alphabets;
- the category definitions are aligned across the two samples;
- both population MI values and their first-order variances are away from
  zero;
- the population cell probabilities are positive; and
- near-independence, structural zeros, growing alphabets, and dependent
  observations are excluded.

## Inclusion Rule

A work was classified as a direct predecessor if it did at least one of the
following:

1. formulated equality of MI or conditional MI across two distributions;
2. constructed uncertainty intervals or a significance test for a
   difference between two within-population MI values; or
3. derived general asymptotic theory that directly specializes to that
   contrast.

Works testing only `I(P)=0`, testing `P=Q`, or using MI as a generic
two-sample statistic were retained as adjacent literature but not counted as
direct solutions.

## Search Method

The review used primary papers, author repositories, publisher pages,
preprints, software documentation, and citation chains. Query families
included:

- `"equality of mutual information"` and `"equal mutual information"`;
- `"difference in mutual information" test`, p-value, permutation, bootstrap,
  confidence interval, and standard error;
- `"compare mutual information estimates" significance`;
- `"mutual information index" pairwise comparison, inference, and
  asymptotic`;
- `"I(P)=I(Q)"`, `I_P(X;Y)`, and conditional-MI equivalents;
- differential MI, comparative MI, information networks, and condition-
  specific MI;
- entropy and information-functional two-sample inference;
- studentized weak-null permutation;
- MI segregation index, M-index, social mobility, and school segregation;
- citation chains from Moddemeijer, Brillinger, Chung and Romano, and direct
  application papers; and
- domain searches of IEEE, ACM, PMLR, JMLR, PubMed/PMC, arXiv, OpenReview,
  RePEc, university repositories, and journal publisher sites.

The search crossed statistics, information theory, signal processing,
neuroscience, genomics, immunology, causal discovery, sociology, and
economics. The cross-disciplinary search was essential because the closest
predecessor calls MI the "Mutual Information index of segregation."

This is an extensive structured review, not proof that no uncatalogued work
exists. It does not replace authenticated searches in Scopus, Web of Science,
MathSciNet, zbMATH, ProQuest Dissertations, or non-English databases.

## Decisive Mathematical Predecessor

### Mora and Ruiz-Castillo (2009)

Mora and Ruiz-Castillo define

```text
M(P) = sum_ij p_ij log[p_ij / (p_i+ p_+j)].
```

This is exactly Shannon mutual information in nats:

```text
M(P) = I_P(X;Y).
```

Their model allows a fully flexible nonparametric multinomial joint
distribution. Their Theorem 2 gives, away from independence,

```text
sqrt(n) { M(P_hat) - M(P) } -> Normal(0, V(P)).
```

The variance written using their multinomial gradient and covariance is
algebraically

```text
V(P) = Var_P(log[p_XY / (p_X p_Y)]).
```

This is the same first-order influence variance used by this project. For two
independent samples, the standard product-CLT consequence is

```text
M(P_hat) - M(Q_hat)
  approximately Normal(
    M(P) - M(Q),
    V(P)/n + V(Q)/m
  ).
```

The paper's abstract explicitly says that statistical tests for pairwise
comparisons of segregation levels between cities, countries, schools,
districts, groups, and time periods can be performed. Mathematically, these
are pairwise tests of two discrete MI values.

The paper also warns that the normal approximation may be poor in small
samples and suggests bootstrap inference. That warning is directly relevant
to the current finite-sample research.

Primary source:
[Mora and Ruiz-Castillo, *The Statistical Properties of the Mutual
Information Index of Multigroup Segregation* (Working Paper 09-84,
2009)](https://www.researchgate.net/publication/4724169_The_statistical_properties_of_the_Mutual_Information_index_of_multigroup_segregation).

Related repository version:
[Mora and Ruiz-Castillo, *A Kullback-Leibler Measure of Conditional
Segregation* (2010)](https://hdl.handle.net/10016/9162).

### Equivalence to the Current Baseline

The current baseline uses

```text
I_BC(P_hat) = I(P_hat) - d/(2n)
d = (r-1)(c-1)

Delta_BC = I_BC(P_hat) - I_BC(Q_hat)

SE = sqrt{V_hat(P)/n + V_hat(Q)/m}.
```

The components have the following provenance:

| Component | Status |
|---|---|
| Plug-in discrete MI | Classical |
| First-order normal law away from independence | Established |
| `Var(log density ratio)` variance | Moddemeijer and Mora-Ruiz-Castillo |
| Sum of independent sample variances | Standard two-sample delta method |
| Leading `d/(2n)` bias correction | Classical Miller-Moddemeijer correction |
| Wald p-value and interval | Standard consequence |

Therefore, the baseline is a sensible synthesis and implementation of known
ingredients. It is not a new first-order statistical principle.

## Operational Direct Predecessor

The `segregation` R package treats a contingency table as the joint
distribution of a group variable and a unit variable. Its `mutual_difference`
function:

- accepts two datasets;
- reports `M1`, `M2`, and `diff = M2 - M1`;
- optionally bootstraps standard errors;
- applies bootstrap bias correction; and
- returns confidence intervals for the difference and its decomposition.

Because `M1` and `M2` are ordinary MI values, a confidence interval for
`M2-M1` is direct weak-null inference for equal MI. The procedure does not
require the complete distributions to be equal. Its source code draws
separate multinomial bootstrap tables from the two empirical distributions,
so it is not a pooled-label permutation that assumes exchangeability.

Primary software documentation:
[Elbers, `mutual_difference`](https://elbersb.github.io/segregation/reference/mutual_difference.html)
and the
[`segregation` inference vignette](https://elbersb.github.io/segregation/articles/segregation.html).
The
[`mutual_difference.R` source](https://github.com/elbersb/segregation/blob/master/R/mutual_difference.R)
shows the two independent multinomial bootstrap draws.

The 2023 `mutualinf` package paper also describes bootstrap inferential
analysis and pairwise decompositions of the same MI index:
[Fuentealba-Chaura et al., *mutualinf: An R Package for Computing and
Decomposing the Mutual Information Index of Segregation*](https://journal.r-project.org/articles/RJ-2023-047/).

This is decisive evidence against claiming the first weak-null method, even
though the package uses bootstrap rather than the project's analytic
calculation.

## Evidence Matrix

| Work | Year | Target and method | Classification |
|---|---:|---|---|
| Moddemeijer, *On estimation of entropy and mutual information* | 1989 | Derives leading bias and first-order variance for histogram/discrete MI | Theoretical ingredient |
| Morales, Pardo, and Vajda, *Asymptotic divergence of estimates of discrete distributions* | 1995 | General asymptotics for divergences of discrete-distribution estimates | Theoretical ingredient |
| Tononi et al., *Functional Clustering* | 1998 | Compares group MI values in neuroimaging using random permutation | Direct target, different method |
| Moddemeijer, dependent-pair variance paper | 1999 | Motivates variance estimation by deciding whether MI differences are significant | Close theoretical/application predecessor |
| Brillinger, *Some data analyses using mutual information* | 2004 | Delta-method normality for non-null discrete MI and comparative examples | Theoretical ingredient |
| Wang et al., MINDy | 2005/2006 | Tests `abs(I_high-I_low)>0` using an empirical random-subset null | Direct target, different estimator and null calibration |
| Mora and Ruiz-Castillo | 2009 | Nonparametric multinomial MI asymptotics and pairwise significance comparisons | Direct mathematical predecessor |
| Wang et al., MINDy | 2009 | Conditional MI difference between high/low modulator subsets, permutation p-value | Direct target, different estimator and design |
| Hart and Giszter | 2010 | Bias-corrected MI differences with jackknife variances | Direct applied analogue |
| Hutter and Zaffalon | 2004/2005 | Bayesian posterior approximation for one discrete MI | Adjacent one-MI inference |
| Janssen | 1997 | Studentized permutation under non-identically distributed nulls | General weak-null theory |
| Chung and Romano | 2013 | k-sample parameter equality; raw permutation can fail, studentization repairs asymptotically | General weak-null theory |
| Stefani et al. | 2013 | Finite-alphabet confidence intervals for one MI | Adjacent one-MI inference |
| Kandasamy et al. | 2015 | Influence-function estimators and normality for information functionals of one or more distributions | General theoretical ingredient |
| Santolini et al., DMI | 2015 | Permutation inference for differences in multivariate information across conditions | Direct analogue, different functional |
| Elbers, `segregation` package | 2021-present | Bootstrap bias correction, SEs, and CIs for differences between two discrete MI indices | Direct operational predecessor |
| Boughter et al. | 2020 | Raw label-permutation p-values for MI differences in antibody populations | Direct applied target |
| Boughter et al. | 2023 | Raw two-sided permutation for MI differences in immune repertoires | Direct applied target |
| Rey et al. | 2023 | Delta-method comparison of entropy values from multinomial samples | Close functional analogue |
| Fuentealba-Chaura et al., `mutualinf` | 2023 | Bootstrap inference and pairwise MI-index decomposition | Direct operational analogue |
| Bystrova et al., IDI | 2024 | Explicitly writes equality of conditional MI across two distributions | Direct target formulation; test not fully instantiated |
| Marinescu and Balcau | 2025/2026 | First- and second-order delta-method inference and bias correction for one discrete MI | Close current theoretical work |

## Direct MI-Difference Applications

### MINDy

The 2006 MINDy paper partitions samples according to high and low values of a
candidate modulator, defines

```text
Delta I = abs(I_high - I_low),
```

and constructs an empirical null using 1,000 random non-overlapping subsets.
This is an explicit test of whether two MI values differ. The later 2009
paper similarly uses permutation p-values.

Sources:

- [Wang et al. (2006), MINDy conference paper](https://nemenmanlab.org/~ilya/images/e/e6/Wang-etal-06.pdf)
- [Wang et al. (2009), *Genome-wide identification of post-translational
  modulators of transcription factor activity in human B cells*](https://nemenmanlab.org/~ilya/images/d/d4/Wang-etal-09.pdf)

MINDy is not the same estimator or finite-table model, and its resampling
scheme is not demonstrated to be valid for every unrestricted equal-MI null.
It nevertheless refutes a claim that no one previously formulated or tested
an MI equality question.

### Neuroimaging and Neural Coding

Tononi et al. compare MI-based functional clustering between controls and
patients and use random permutation for group differences. Hart and Giszter
use Moddemeijer's MI bias correction, delete-one-trial jackknife uncertainty,
and a variance-combined standardized comparison between MI estimates.

Sources:

- [Tononi et al. (1998), *Functional Clustering: Identifying Strongly
  Interactive Brain Regions in Neuroimaging Data*](https://doi.org/10.1006/nimg.1997.0313)
- [Hart and Giszter (2010), *A Neural Basis for Motor Primitives in the
  Spinal Cord*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6633785/)

These designs do not exactly match two independent multinomial populations,
but they are strong historical evidence of MI-difference inference.

### Immunology

Boughter et al. directly compare within-population discrete MI values. They
pool observations, randomly assign them to group-sized bins, recompute the
MI difference, and use 1,000 permutations. This is the applied practice most
directly motivating the project's weak-null analysis.

Sources:

- [Boughter et al. (2020), eLife](https://doi.org/10.7554/eLife.61393)
- [Boughter et al. (2023), PLOS Computational Biology](https://doi.org/10.1371/journal.pcbi.1011577)

The raw group-label permutation is exact under the strong null `P=Q`. It is
not generally exact for the weaker null `I(P)=I(Q)` when `P` and `Q` differ.
The application is therefore direct precedent for the question, but not a
general solution to the weak-null calibration problem.

### Causal Difference Graphs

Bystrova et al. explicitly formulate

```text
H0: I_P1(X1;X2 | X3) = I_P2(X1;X2 | X3).
```

This is the conditional-MI generalization of the project's null. The short
workshop paper does not provide a complete finite-sample equality test or
calibration analysis and appears to use equality as an oracle in simulation.
It is still direct evidence that the weak-null formulation is not new.

Source:
[Bystrova et al. (2024), *Information-Theoretic Causal Difference
Graphs*](https://openreview.net/forum?id=nCR1425CpP).

## Theoretical Building Blocks

### Bias and Variance of Discrete MI

Moddemeijer derives the leading plug-in bias and the first-order variance

```text
Var_P(log[p_XY/(p_X p_Y)]) / n.
```

The 1999 follow-up explicitly says that variance is needed to decide whether
differences between MI estimates are significant.

Sources:

- [Moddemeijer (1989)](https://ris.utwente.nl/ws/files/6737096/Moddemeijer89on.pdf)
- [Moddemeijer (1999)](https://doi.org/10.1016/S0165-1684(98)00224-2)

Brillinger gives a general delta-method account and reproduces the same
discrete non-null variance:
[Brillinger (2004), *Some data analyses using mutual
information*](https://www.stat.berkeley.edu/~brill/Papers/bjps1.pdf).

### Influence-Function Inference

Kandasamy et al. develop influence-function estimators for information
functionals. Their multi-distribution normality theorem combines separate
influence variances, which is the general structure needed for a two-sample
MI contrast.

Source:
[Kandasamy et al. (2015)](https://arxiv.org/abs/1411.4342).

### Weak-Null Permutation Theory

Chung and Romano establish the general distinction between:

```text
strong null: P = Q
parameter null: theta(P) = theta(Q).
```

They show why an unstudentized permutation distribution need not be valid
for equality of a parameter when the populations differ, and develop
studentized asymptotically valid procedures under regularity conditions.
This theory directly applies in principle to regular MI estimators.

Sources:

- [Janssen (1997)](https://doi.org/10.1016/S0167-7152(97)00043-6)
- [Chung and Romano (2013)](https://arxiv.org/abs/1304.5939)

Consequently, neither the general weak-null objection to raw permutation nor
studentization itself is novel.

### Closely Related Entropy Comparisons

Rey et al. construct two-sample tests for equality of entropy values in
multinomial populations. This is not MI equality, but it is a close
methodological analogue because entropy and MI are smooth multinomial
functionals away from boundary cases.

Source:
[Rey et al. (2023)](https://doi.org/10.3390/e25050734).

### Current Discrete-MI Delta-Method Work

Marinescu and Balcau use first- and second-order delta methods for discrete
MI, derive bias correction, and construct improved one-MI confidence
intervals and independence tests. This work further confirms that the bias
correction and delta-method inference are active prior art.

Sources:

- [Marinescu and Balcau (2025), *On the use of Mutual Information for
  Testing Independence*](https://arxiv.org/abs/2502.17636)
- [Marinescu and Balcau (2026), *A bias correction for the mutual
  information sample estimator*](https://doi.org/10.1016/j.spl.2026.110802)

## Important Non-Matches

The following neighboring problems should not be presented as exact
predecessors:

- One-population independence tests target `I(P)=0`.
- MI-based two-sample tests that measure dependence between a sample label
  and observations target `P=Q`.
- Homogeneous-association or no-interaction tests in three-way contingency
  tables constrain odds ratios or log-linear interactions, not merely the
  equality of two scalar MI values.
- Adjusted or normalized MI tests for comparing clusterings use a
  fixed-margin random-clustering null.
- One-MI Bayesian posteriors and confidence bounds do not automatically
  provide a tested two-population procedure.
- Equality of channel capacities, Gaussian MI, or MIMO random-channel MI is
  a different parametric problem.

These distinctions remain important, but they do not restore the broad
novelty claim because the direct predecessors above do match the target.

## Claim-by-Claim Verdict

| Candidate claim | Verdict | Reason |
|---|---|---|
| First paper to write an equal-MI weak null | False | MINDy and Bystrova explicitly formulate MI-difference/equality targets |
| First empirical test of a difference between MI values | False | Neuroimaging and MINDy precedents predate the project |
| First weak-null test for two discrete contingency-table MI values | Not defensible | Mora-Ruiz-Castillo asymptotics and `segregation` bootstrap inference directly overlap |
| First derivation of the two-sample first-order variance | False as a novelty claim | It is the standard independent-sample consequence of established MI delta-method results |
| First use of bias correction for MI comparisons | False or unsupported | Bias correction and jackknife comparison precedents exist |
| First fast analytic implementation with this exact API and diagnostics | Possibly true but scientifically weak | Software-interface priority is not a strong methods claim |
| First systematic demonstration that raw MI-difference label permutation can fail under equal MI with `P!=Q` | Plausible and not contradicted by this review | General theory exists, but a broad MI-specific finite-sample study was not located |
| First broad finite-sample benchmark of analytic bias-corrected equal-MI inference under heterogeneous discrete margins | Plausible, provisional | No exact benchmark was located; formal database review still required |
| First practical framework combining bias correction, diagnostics, calibration boundaries, runtime, and weak-null comparison | Plausible as an integration contribution | Must be described as synthesis and validation, not invention of the component test |

## What May Still Be Novel

The strongest unresolved contribution is not the Wald formula. It is the
problem-specific correction and validation package:

1. clearly distinguish the strong distributional null from the weak
   equal-MI null in applied MI comparisons;
2. show, theoretically and empirically, how raw group-label permutation can
   be conservative or anti-conservative for equal MI;
3. identify MI-specific pooled-mixture degeneracy that can also undermine a
   studentized permutation route;
4. quantify the benefit and limits of classical bias correction in skewed,
   low-expected-count multinomial tables;
5. provide observable diagnostics for a defensible regular operating regime;
6. benchmark calibration, coverage, power, and runtime against existing
   resampling practice; and
7. provide reproducible, general rectangular-table software.

This can be a useful methods thesis if the empirical claims remain strong
under adversarial validation. The novelty is characterization, validation,
and practical synthesis.

## Recommended Thesis Positioning

### Do Not Say

- "the first weak-null test of equal MI";
- "the first method for comparing two MI values";
- "a new MI variance formula";
- "the first use of the delta method or influence functions for MI";
- "the first bias-corrected MI significance test"; or
- "no one has applied this problem in information theory."

### Safe Current Wording

> This thesis studies weak-null inference for equality of discrete mutual
> information across heterogeneous multinomial populations. Building on
> established MI bias and variance theory, it develops a fast
> bias-corrected implementation and systematically evaluates its
> finite-sample operating regime. It also characterizes why raw
> group-label permutation, used in existing MI-difference applications,
> need not test the equal-MI null when the underlying distributions differ.

### Strongest Provisional Novelty Wording

> To our knowledge, this is the first systematic finite-sample study of
> bias-corrected analytic equal-MI inference and raw-permutation failure
> across heterogeneous discrete contingency-table populations.

This sentence should be used only after the remaining database searches and
supervisor review. "To our knowledge" is essential.

### Suggested Title

> Fast Weak-Null Inference for Differences in Discrete Mutual Information:
> Bias Correction, Permutation Failure, and Finite-Sample Validation

## Thesis Viability

The literature result narrows but does not automatically invalidate the
project. A master's thesis can make a methodological contribution by:

- correcting a demonstrably unreliable applied procedure;
- establishing a practically useful operating regime;
- showing when a much faster analytic method preserves calibration;
- exposing failure modes that existing software does not diagnose; and
- delivering validated software and reproducible benchmarks.

However, if the thesis contribution is only the formula

```text
(I_hat_P - I_hat_Q) /
sqrt(V_hat_P/n + V_hat_Q/m),
```

then it is too close to prior delta-method work to support a strong novelty
claim.

## Remaining Due Diligence

Before a proposal or paper claims priority:

1. run authenticated Scopus and Web of Science searches using the recorded
   query families;
2. search MathSciNet and zbMATH for information-functional equality tests;
3. search ProQuest and institutional thesis repositories;
4. forward- and backward-chain Mora and Ruiz-Castillo (2009),
   Moddemeijer (1989, 1999), and Brillinger (2004);
5. inspect the implementation and papers behind `segregation` and
   `mutualinf` in full;
6. have the supervisor or a statistician challenge the exact novelty
   sentence; and
7. retain a dated inclusion/exclusion spreadsheet for the thesis appendix.

The literature can never prove universal absence. The defensible standard is
a transparent search, a narrow claim, and clear acknowledgement of the
closest predecessors.

## Core References

- [Moddemeijer (1989), bias and variance of MI](https://doi.org/10.1016/0165-1684(89)90132-1)
- [Moddemeijer (1999), variance and significant MI differences](https://doi.org/10.1016/S0165-1684(98)00224-2)
- [Brillinger (2004), delta-method MI analysis](https://www.stat.berkeley.edu/~brill/Papers/bjps1.pdf)
- [Mora and Ruiz-Castillo (2009), statistical properties and pairwise MI-index tests](https://www.researchgate.net/publication/4724169_The_statistical_properties_of_the_Mutual_Information_index_of_multigroup_segregation)
- [Mora and Ruiz-Castillo (2010), repository follow-up](https://hdl.handle.net/10016/9162)
- [Elbers, `segregation` package](https://elbersb.github.io/segregation/)
- [Fuentealba-Chaura et al. (2023), `mutualinf`](https://journal.r-project.org/articles/RJ-2023-047/)
- [Chung and Romano (2013), weak-null permutation](https://doi.org/10.1214/13-AOS1090)
- [Kandasamy et al. (2015), influence functions for information functionals](https://arxiv.org/abs/1411.4342)
- [Rey et al. (2023), two-sample entropy comparison](https://doi.org/10.3390/e25050734)
- [Wang et al. (2006), MINDy](https://nemenmanlab.org/~ilya/images/e/e6/Wang-etal-06.pdf)
- [Boughter et al. (2020), MI-difference permutation](https://doi.org/10.7554/eLife.61393)
- [Boughter et al. (2023), MI-difference permutation](https://doi.org/10.1371/journal.pcbi.1011577)
- [Bystrova et al. (2024), equality of conditional MI across distributions](https://openreview.net/forum?id=nCR1425CpP)
- [Marinescu and Balcau (2026), MI bias correction and confidence intervals](https://doi.org/10.1016/j.spl.2026.110802)
