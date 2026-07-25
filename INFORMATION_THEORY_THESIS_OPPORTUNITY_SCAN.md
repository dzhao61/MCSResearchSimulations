# Information-Theory Methods Thesis Opportunity Scan

Status: preliminary opportunity assessment

Date: 25 July 2026

## Executive Conclusion

The existing sparse-binary-CMI saddlepoint project has been preserved as a
safety-net thesis in:

`Sparse CMI/docs/SAFETY_NET_THESIS.md`

The strongest new direction found in this broad scan is:

> **Valid two-sample inference for changes in discrete mutual information.**

The target question is not "is each population independent?" It is:

```text
H0: I_P(X;Y) = I_Q(X;Y)
```

This is a useful and distinct inferential problem. It asks whether the strength
of dependence changed between two populations, treatments, time periods, or
experimental conditions.

It also contains a sharp methodological issue. A naive permutation of group
labels is exact for the strong null `P = Q`, but not generally for the weaker
and scientifically relevant null `I(P) = I(Q)`. Two groups can have equal MI
while having different margins, variances, or joint-distribution shapes.
General permutation theory shows that unstudentized permutation tests can fail
for weak parameter nulls, while suitable studentization can recover
asymptotic validity
[Chung and Romano (2013)](https://arxiv.org/abs/1304.5939).

A thesis could therefore develop and validate:

1. an influence-function standard error and confidence interval for
   `Delta_I = I_P - I_Q`;
2. a studentized permutation test that targets equality of MI rather than
   equality of the full distributions;
3. a sparse-table correction or constrained-bootstrap fallback;
4. simultaneous/FDR-controlled differential-MI network inference; and
5. extensions to conditional MI and transfer entropy.

This is only a preliminary novelty finding. A focused citation-chain review is
required before committing to the title or claiming that the test is new.

## How Opportunities Were Judged

Each direction was screened for:

- a real, identifiable inferential failure;
- a statistical technique that can plausibly be transferred;
- a clean mathematical target;
- applicability beyond one special table shape;
- a simulation ground truth and clear acceptance criteria;
- a realistic master's timeline; and
- enough novelty headroom after checking direct recent competitors.

Scores are from 1 (weak) to 5 (strong). They are decision aids, not literature
review results.

| Rank | Candidate | Novelty headroom | Feasibility | Generality | Practical value | Clean validation | Total |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Differential MI across populations | 4 | 4 | 5 | 5 | 5 | 23 |
| 2 | Measurement-error-aware discrete MI | 4 | 4 | 4 | 5 | 4 | 21 |
| 3 | Selection-adjusted MI/TE inference | 3 | 4 | 5 | 5 | 4 | 21 |
| 4 | Multiplicity-controlled local TE events | 4 | 3 | 3 | 5 | 4 | 19 |
| 5 | Design-weighted MI effect-size inference | 2 | 4 | 4 | 4 | 4 | 18 |
| 6 | Finite-sample uncertainty for PID | 3 | 2 | 3 | 4 | 2 | 14 |

For comparison, the preserved binary-CMI saddlepoint thesis scores very highly
on feasibility and validation readiness, but lower on generality. It remains
the safest route if the leading ideas fail their novelty or calibration pilots.

## Candidate 1: Differential Mutual Information

### Scientific question

Given independent samples from joint distributions `P` and `Q`, test:

```text
H0: I_P(X;Y) - I_Q(X;Y) = 0
```

and construct a confidence interval for the difference.

This tests equality of one scientifically meaningful property. It does not test
whether `P` and `Q` are identical.

### Why it matters

Many applications compare dependence networks between:

- case and control groups;
- before and after an intervention;
- two species, cohorts, or environments;
- healthy and diseased systems; or
- different operating regimes of a dynamical system.

Applied work does compare MI values across groups, but the targeted search found
examples using ad hoc t-tests on repeated MI estimates rather than a standard
test for equality of the population MI functionals. One example explicitly
uses a t-test to compare original and shuffled MI values
[Pandey et al. (2020)](https://academic.oup.com/mnras/article/497/4/4077/5881970).

### Core statistical transfer

For a strictly positive discrete joint distribution, MI is the smooth
functional:

```text
I(P) = sum_ij p_ij log[p_ij / (p_i. p_.j)].
```

Away from independence and the probability-simplex boundary, its influence
function is:

```text
IF_P(i,j) = log[p_ij / (p_i. p_.j)] - I(P).
```

This gives a first-order variance estimate:

```text
Var(Delta_I_hat)
  approximately Var_P(IF_P) / n_P + Var_Q(IF_Q) / n_Q.
```

The resulting statistic can be studentized. General weak-null permutation
theory is then directly relevant: studentized randomization can be
asymptotically valid for equality of a parameter even when the complete
distributions are unequal
[Dobler (2021)](https://arxiv.org/abs/1912.08233) and
[Chung and Romano (2013)](https://arxiv.org/abs/1304.5939).

A recent paper applies first- and second-order delta methods to MI for
one-sample independence testing, which is close prior work and a useful
technical starting point
[Marinescu and Balcau (2025)](https://arxiv.org/abs/2502.17636). The proposed
contribution must therefore be
the two-population weak-null problem, sparse calibration, and differential
network use, not merely "applying the delta method to MI."

### Main technical challenge

At independence, the first derivative of MI degenerates and the influence
function variance becomes zero. Sparse tables also place estimates on or near
the simplex boundary. A serious method must therefore have explicit routes:

```text
regular route:
    both MI values sufficiently away from zero and cells well supported
    -> influence-function / studentized inference

boundary route:
    both values near independence
    -> second-order or independence-specific null

sparse route:
    low or zero expected counts
    -> smoothing plus constrained bootstrap, exact small-table calculation,
       or a validated higher-order approximation
```

This is a feature of the thesis, not an implementation detail: it exposes where
ordinary "compare two MI numbers" reasoning breaks.

### Proposed thesis contribution

Working title:

> *Valid Inference for Differences in Discrete Mutual Information Across
> Populations*

Deliverables:

- point estimate and confidence interval for `Delta_I`;
- deterministic influence-function test in its regular regime;
- studentized permutation calibration under the weak null;
- sparse/boundary diagnostics and fallback;
- simultaneous differential-MI network inference;
- open implementation and adversarial validation grid.

### Falsification-first pilot

Before choosing this thesis:

1. Construct pairs `P != Q` with exactly equal MI but different margins.
2. Measure Type I error of naive label permutation, studentized permutation,
   Wald/delta, bootstrap, and Bayesian/Dirichlet alternatives.
3. Include balanced, skewed, sparse, unequal-sample-size, and near-independence
   regimes from `2x2` through at least `20x20`.
4. Check confidence-interval coverage for nonzero `Delta_I`.
5. Search the citation chains around two-sample entropy comparison, weak-null
   permutation tests, and differential information networks.

Go only if the proposed method fixes a reproducible error or coverage problem
that is not already solved by a directly applicable published test.

## Candidate 2: Measurement-Error-Aware MI

### Scientific question

Estimate the MI between latent categorical variables when the observed labels
are misclassified by known or estimated error channels.

If `M_X` and `M_Y` are misclassification matrices, then:

```text
vec(P_observed) = (M_Y tensor M_X) vec(P_latent).
```

The method would recover a constrained estimate of `P_latent`, calculate its
MI, and propagate both sampling uncertainty and uncertainty in the error
matrices.

### Statistical techniques to transfer

- constrained maximum likelihood;
- latent-class models;
- algebraic misclassification correction;
- SIMEX;
- profile likelihood;
- regularized inverse problems; and
- delta-method or bootstrap uncertainty propagation.

Measurement-error correction is mature in epidemiology, including categorical
misclassification and SIMEX, but it is usually developed for regression
effects rather than MI as the target functional
[Shaw et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9005058/).

The targeted search did not identify an obvious standard method named
"misclassification-corrected mutual information." That is encouraging, but
not proof of novelty.

### Why it is attractive

- It is general over finite alphabet sizes.
- The observed failure is intuitive: noise channels contract or distort MI.
- There are direct applications to diagnostic tests, coded survey responses,
  sensor classifications, ecological observations, and machine-labelled data.
- The core estimator can be deterministic.
- Simulations have exact ground truth.

### Main risks

- The inverse problem may be non-identifiable without validation data.
- Near-singular misclassification matrices amplify noise.
- Independent nondifferential error is much easier than correlated or
  differential error.
- Valid inference at independence is again nonregular.

A clean master's scope would assume known full-rank error matrices first, then
add estimated matrices from a validation sample as the main extension.

## Candidate 3: Selection-Adjusted MI and TE

### Scientific question

Provide valid inference after an analyst chooses the feature, lag, embedding,
binning, or conditioning set that maximizes an MI/CMI/TE estimate.

The ordinary workflow:

```text
search many candidates -> keep maximum -> report its naive p-value
```

uses the data twice and overstates evidence.

### Statistical techniques to transfer

- simultaneous max-statistic inference;
- selective inference;
- data carving;
- sample splitting;
- Westfall-Young correction; and
- post-selection confidence intervals.

Post-selection inference has mature general frameworks
[Kuchibhotla, Kolassa, and Kuffner (2022)](https://www.annualreviews.org/content/journals/10.1146/annurev-statistics-100421-044639).
Adaptive partition independence tests also already exist, including
distribution-free aggregation over partition sizes
[Heller et al. (2016)](https://www.jmlr.org/papers/v17/14-441.html) and
finite-sample adaptive MultiFIT
[Gorsky and Ma (2022)](https://academic.oup.com/biomet/article/109/3/569/6533498).

The contribution therefore cannot be the generic statement "correct for
searching." It would need a precise unsolved target, such as:

> valid effect-size and p-value inference for the selected lag and embedding
> in transfer-entropy analysis.

This is general and useful, but the novelty boundary is narrower than for
differential MI.

## Candidate 4: Significant Local Transfer-Entropy Events

### Scientific question

Global TE reports average directed information transfer. Local TE provides a
time-resolved value, but users often threshold thousands of dependent local
values using a small surrogate sample and no multiple-testing correction.

For example, one local-TE application reports `p < 0.05` using 100 surrogates
and explicitly labels the result uncorrected
[Martinez-Cancino et al. (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7712258/).

### Statistical techniques to transfer

- cluster-mass permutation from neuroimaging;
- scan statistics;
- block bootstrap for dependent data;
- false-discovery-rate control;
- simultaneous confidence bands; and
- change-point or epidemic-event detection.

The proposed output would be intervals of significant information-transfer
activity, not just a significant global average.

### Strengths and risks

This has a strong application story and a visible reporting problem. However,
the validity of time-series surrogates depends on stationarity, embedding,
autocorrelation, and the null being tested. The method could easily become a
time-series thesis rather than a clean information-theory methods thesis.

It is a good fourth choice, especially with a neuroscience collaborator and a
real dataset, but it is riskier than the first two candidates.

## Candidate 5: Design-Weighted MI Effect Sizes

### Scientific question

Estimate population MI and its uncertainty from complex surveys or
selection-biased samples with unequal observation weights.

### Why it initially looked promising

Software can calculate weighted MI point estimates, but design-correct
uncertainty for MI as an effect size is not prominent in standard information
toolkits. Survey replicate weights, Taylor linearization, and weighted
likelihood bootstrap are transferable tools.

### Why it ranks lower

The MI likelihood-ratio statistic is the contingency-table `G^2` statistic,
and complex-survey corrections to `G^2` are classical. Rao-Scott corrections
already handle design effects for likelihood-ratio tests in contingency tables
[Rao and Scott literature summary](https://support.sas.com/documentation/cdl/en/statug/67523/HTML/default/statug_surveyfreq_details61.htm).
Modern bootstrap-weight tests also cover independence in two-way tables
[Kim, Rao, and Wang (2023)](https://arxiv.org/abs/1902.08944).

There may still be room for MI effect-size confidence intervals rather than
independence tests, but this now looks like a narrower survey-statistics
extension rather than low-hanging information-theory novelty.

## Candidate 6: PID Uncertainty

Partial information decomposition (PID) is scientifically attractive because
it separates unique, redundant, and synergistic information. Its finite-sample
uncertainty is still less standardized than ordinary MI.

However:

- there is no consensus definition for PID components
  [van Enk (2023)](https://pubmed.ncbi.nlm.nih.gov/37329048/);
- finite-sample bias correction is already an active topic
  [Venkatesh et al. (2023)](https://arxiv.org/abs/2307.10515); and
- significance procedures for tripartite measures already exist and expose
  difficulties with naive permutation
  [Mijatovic et al. (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11117094/).

This has novelty potential, but the target itself is contested. It is not
low-hanging or low-risk for a master's thesis.

## Directions Not Recommended as Primary Projects

### Generic neural-MI uncertainty

This space is moving quickly. Recent work explicitly targets reliability
checks and confidence intervals in high-dimensional MI estimation
[Abdelaleem, Martini, and Nemenman (2025)](https://arxiv.org/abs/2506.00330),
while MIST learns MI estimates and quantiles
from 625,000 synthetic distributions
[Gritsai et al. (2026)](https://openreview.net/forum?id=Q3maWATBCE).

The competition, compute requirements, and moving baseline make it a poor
low-risk thesis choice.

### Generic robust MI

A 2026 paper already develops robust MI-like two-sample tests using extended
Bregman divergences, influence functions, and breakdown-point analysis
[Pyne (2026)](https://arxiv.org/abs/2602.04010).

A new robust-MI project would need a much narrower, clearly different target.

### Generic anytime-valid contingency-table inference

E-values and anytime-valid confidence intervals are already available for
contingency-table effect sizes
[Turner and Grunwald (2023)](https://ir.cwi.nl/pub/32994/).
Anytime-valid Monte Carlo permutation testing is also now directly developed
[Fischer and Ramdas (2025)](https://academic.oup.com/jrsssb/article/87/4/1200/8106328).

Applying these techniques to JIDT could be useful software engineering, but
the transfer alone is unlikely to support the main methodological claim.

### Generic permutation-free independence testing

Permutation-free alternatives are already an active area. Cross-HSIC and
cross-distance-covariance provide Gaussian-null, permutation-free
independence tests
[Shekhar, Kim, and Ramdas (2023)](https://jmlr.org/papers/v24/23-0248.html).
Discrete conditional-independence alternatives such as SECMI also already
target poor CMI-test behavior with large conditioning sets
[Kubkowski, Mielniczuk, and Teisseyre (2021)](https://www.jmlr.org/papers/v22/19-600.html).

The current binary-CMI saddlepoint project remains defensible because it has a
specific conditional fixed-margin construction and a bounded sparse regime,
not because permutation-free testing is itself new.

### Generic practical-significance threshold testing

Testing whether MI/CMI is zero versus at least a positive threshold is now the
subject of direct sample-complexity work
[Seyfried, Sen, and Tomamichel (2025)](https://arxiv.org/abs/2506.03894).
Distribution-free finite-alphabet MI confidence intervals also exist
[Stefani et al. (2013)](https://arxiv.org/abs/1301.5942).

There may be applied implementation work here, but it no longer looks like the
best open methodological gap.

## Recommended Decision Process

Do not abandon the saddlepoint safety net yet. Run one short go/no-go study for
differential MI before changing thesis direction.

### Stage 1: one-week mathematical and novelty audit

1. Derive the influence function and variance for discrete MI.
2. State the regularity and boundary conditions explicitly.
3. Map the statistic to Chung-Romano weak-null permutation theory.
4. Search citations for equality of entropy, equality of KL functionals,
   differential association networks, and two-sample MI comparison.
5. Ask a supervisor whether equality of MI is a compelling scientific target.

### Stage 2: one-week adversarial simulation pilot

Build a small independent project with:

- `2x2`, `2x5`, `5x5`, `10x10`, and `20x20` tables;
- balanced and unequal group sample sizes;
- balanced, mildly skewed, and strongly skewed margins;
- exact-equal-MI null pairs with `P != Q`;
- near-independence and exactly independent boundary cases;
- alternatives with controlled `Delta_I`;
- naive label permutation;
- studentized permutation;
- influence-function Wald inference;
- nonparametric bootstrap;
- constrained parametric bootstrap if feasible; and
- confidence-interval coverage, Type I error, power, and runtime.

### Go criteria

Proceed if:

- naive methods show a reproducible inferential failure under the correct weak
  null;
- the proposed test materially improves Type I error or interval coverage;
- the method remains useful beyond binary tables;
- the closest literature does not already provide the same MI-specific test;
- the sparse/boundary route is explainable rather than an uncontrolled patch;
  and
- a real application dataset can be identified.

### Stop criteria

Return to the safety-net thesis if:

- studentization does not stabilize realistic sparse tables;
- the method only works in dense asymptotic regimes where ordinary approaches
  are already adequate;
- a direct prior paper already solves equality-of-MI inference;
- the method needs several unrelated fallback tests to function; or
- no credible application requires equality of MI rather than equality of the
  full distributions.

## Bottom Line

The current saddlepoint project is a valid, evidence-backed fallback. The best
new opportunity is not another way to test independence. It is a method for a
different and under-served question:

> **Did the amount of shared information change between populations?**

That target is general, scientifically interpretable, naturally extends to
CMI and TE, and exposes a specific weakness in naive group-label permutation.
It deserves a tightly bounded pilot before any thesis pivot.
