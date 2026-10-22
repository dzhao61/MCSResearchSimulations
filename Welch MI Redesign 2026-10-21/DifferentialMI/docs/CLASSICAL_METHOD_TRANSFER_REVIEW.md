# Classical-Statistics Method Transfer Review for Differential Discrete MI

Date: 27 July 2026

## Executive Verdict

There is a credible and focused next direction:

> Develop and validate constrained multinomial test-inversion inference for
> the difference between two discrete mutual informations.

The first implementation should compare three statistics computed from the
same constrained fit:

1. the Pearson/profile-score statistic;
2. the profile likelihood-ratio statistic; and
3. the Cressie-Read power-divergence statistic with `lambda = 2/3`.

This is a better first move than adding another approximation to the current
Wald statistic. It directly fits the null hypothesis

```text
H0: I(P) - I(Q) = 0
```

inside the correct two-multinomial sampling model. It therefore retains the
nonlinear likelihood geometry that the current Wald test replaces with a
local normal approximation.

The statistical machinery is not new. Generic score, profile-likelihood, and
power-divergence confidence intervals for arbitrary contingency-table
functionals are established in classical categorical-data analysis. However,
this review found no paper that explicitly derives, implements, and robustly
validates these methods for equality of two discrete mutual informations.

The defensible provisional contribution is therefore:

> To our knowledge, the first MI-specific development and systematic
> finite-sample validation of constrained score, profile-likelihood, and
> power-divergence inference for comparing two discrete mutual-information
> functionals.

That sentence still requires an authenticated database search and supervisor
review. The work must not be described as inventing profile likelihood,
score tests, power divergence, or equal-MI inference.

## Exact Research Target

Let two independent samples produce count tables

```text
A = {a_ij}, total n_P
B = {b_ij}, total n_Q.
```

The population cell-probability vectors are `p` and `q`. The target is

```text
Delta = I(p) - I(q),
```

where

```text
I(p) = sum_ij p_ij log[p_ij / (p_i+ p_+j)].
```

The primary hypothesis is the weak null

```text
H0: Delta = 0,
```

while allowing `p != q`. This is not a test that the two full distributions
are equal, and it is not a test that either table is independent.

The initial scope should remain:

- independent samples;
- fixed finite alphabets;
- ordinary multinomial sampling within each sample;
- positive cell probabilities in the population;
- MI sufficiently above zero for the equality constraint to be regular; and
- table dimensions modest relative to sample size.

The method is not expected to repair the nonregular point `I = 0`, where the
first derivative of MI vanishes on the multinomial simplex.

## Why the Current Wald Test Leaves Room for Improvement

The retained `wald_analytic` method is already strong. Its error comes from
approximating the MI-difference estimator by a bias-corrected normal random
variable:

```text
Z = (Delta_hat_corrected - Delta_0) / estimated_SE.
```

This makes three local approximations:

1. the nonlinear MI functional is linearized at the estimated tables;
2. the sampling distribution is treated as symmetric normal; and
3. uncertainty is evaluated at the unrestricted estimates rather than under
   the null constraint.

Those approximations are most vulnerable in the same settings that remain
hard in the existing validation: skewed probabilities, low expected counts,
unequal sample sizes, and likelihood surfaces with appreciable curvature.

Profile and score procedures replace the local linearization with an explicit
fit under `I(p) - I(q) = Delta_0`. They do not guarantee good behavior at a
boundary, but they address the main regular-case approximation more directly.

## Recommended Method

### Unrestricted fit

The unrestricted maximum-likelihood estimates are the empirical proportions:

```text
p_hat_ij = a_ij / n_P
q_hat_ij = b_ij / n_Q.
```

The unrestricted log likelihood, ignoring multinomial constants, is

```text
l_unrestricted =
    sum_ij a_ij log(p_hat_ij)
  + sum_ij b_ij log(q_hat_ij).
```

### Constrained fit

For a candidate MI difference `Delta_0`, compute

```text
(p_tilde, q_tilde) =
    argmax l(p, q)
```

subject to

```text
sum_ij p_ij = 1
sum_ij q_ij = 1
p_ij >= 0
q_ij >= 0
I(p) - I(q) = Delta_0.
```

For the equal-MI test, only the fit at `Delta_0 = 0` is required.

The regular asymptotic theory assumes an interior population parameter, but
finite samples from that population can contain zero-count cells. The exact
optimization domain is therefore the closed simplex. A logit/softmax
implementation can approximate its boundary, but must detect and report when
the result depends materially on the numerical probability floor.

The MI gradient with respect to a cell probability is

```text
dI(p) / dp_ab =
    log[p_ab / (p_a+ p_+b)] - 1.
```

The constant term is irrelevant in a simplex tangent direction but should be
retained in a direct constrained implementation. Exact gradients and Hessians
should be used rather than finite differences.

### Statistic 1: Pearson/profile score

Let

```text
e^P_ij = n_P p_tilde_ij
e^Q_ij = n_Q q_tilde_ij.
```

Then

```text
X2 =
    sum_ij (a_ij - e^P_ij)^2 / e^P_ij
  + sum_ij (b_ij - e^Q_ij)^2 / e^Q_ij.
```

Because the unrestricted alternative is saturated and the null imposes one
regular scalar restriction,

```text
X2 -> chi-square_1.
```

This is the primary candidate. Classical categorical-data evidence often
finds null-standardized score inference better calibrated than Wald
inference, including at relatively small counts.

### Statistic 2: Profile likelihood ratio

The likelihood-ratio statistic is

```text
G2 = 2 * (l_unrestricted - l_constrained).
```

Equivalently,

```text
G2 =
    2 sum_ij a_ij log(a_ij / e^P_ij)
  + 2 sum_ij b_ij log(b_ij / e^Q_ij),
```

with zero observed-count terms defined as zero. Under the same regularity
conditions,

```text
G2 -> chi-square_1.
```

This is profile-likelihood inference for `Delta`. It preserves likelihood
curvature, is invariant to a one-to-one transformation of `Delta`, and can
produce asymmetric confidence intervals by inversion.

### Statistic 3: Cressie-Read power divergence

For observed counts `o_k` and constrained expected counts `e_k`, define

```text
CR_lambda =
    2 / [lambda * (lambda + 1)]
    * sum_k o_k * [(o_k / e_k)^lambda - 1].
```

The cells from both tables are included in the sum. Important special cases
are:

```text
lambda = 1       Pearson X2
lambda -> 0      likelihood-ratio G2
lambda = 2/3     Cressie-Read compromise statistic.
```

Cressie and Read identified `lambda = 2/3` as a useful finite-sample
compromise between Pearson and likelihood-ratio behavior. It should be
pre-specified, not selected after looking at which method gives the desired
answer.

### P-value and interval

For any of the three statistics `T`,

```text
p_value = P(chi-square_1 >= T).
```

This `chi-square_1` reference is not the usual
`chi-square_((r-1)(c-1))` independence test. The degrees of freedom are one
because the null imposes one scalar equality, regardless of the table size.

A confidence interval for `Delta` is obtained by retaining every candidate
`Delta_0` for which

```text
T(Delta_0) <= chi-square_1,1-alpha.
```

The test requires one constrained fit. A complete interval requires repeated
fits while finding two endpoints.

## Why This Transfer Is Credible

### Generic contingency-table theory already exists

Lang developed a general algorithm for score and profile-likelihood intervals
for broad classes of contingency-table functionals. The paper explicitly
reports better finite-sample behavior than Wald intervals in its simulations:

- [Lang (2008), Score and Profile Likelihood Confidence Intervals for
  Contingency Table Parameters](https://doi.org/10.1002/sim.3391)
- [Lang's `ci.table` documentation and examples](https://homepage.divms.uiowa.edu/~jblang/ci.table.documentation/ci.table.examples.htm)

The software accepts a user-defined functional `S(p)` and product-multinomial
strata. In principle, concatenating the two probability tables and defining
`S(p) = MI(p_P) - MI(p_Q)` places the present problem inside that framework.

Zhu and Lang later generalized and robustified the test-inversion machinery.
Their simulations favored likelihood-ratio intervals over bootstrap and Wald
intervals particularly when counts were small or the estimand was near a
boundary:

- [Zhu and Lang (2022), Test-inversion confidence intervals for estimands in
  contingency tables subject to equality constraints](https://doi.org/10.1016/j.csda.2021.107413)

This is strong supporting evidence, but it also limits the novelty claim:
the generic mathematics already covers arbitrary smooth functionals such as
MI, even if MI was not explicitly studied.

### Power divergence was designed for multinomial fit

The Cressie-Read family unifies Pearson, likelihood-ratio, Freeman-Tukey, and
other multinomial discrepancy statistics. The original study identified
`lambda = 2/3` as a strong compromise in analytic and finite-sample
comparisons:

- [Cressie and Read (1984), Multinomial Goodness-of-Fit
  Tests](https://doi.org/10.1111/j.2517-6161.1984.tb01318.x)

The proposed transfer does not replace mutual information with a different
dependence measure. MI remains the parameter constrained by the null;
power divergence only measures how poorly the constrained tables fit the
observed counts.

### Modern algorithms make the optimization more practical

Profile inference can fail numerically if a solver takes unreliable Newton
steps or a parameter is weakly identified. A modern trust-region profile
algorithm had higher success rates than six comparator algorithms while
remaining among the fastest:

- [Fischer and Lewis (2021), A robust and efficient algorithm to find profile
  likelihood confidence intervals](https://doi.org/10.1007/s11222-021-10012-y)

An MI-specific implementation can exploit closed-form derivatives and the
two-simplex structure rather than relying entirely on a generic black-box
solver.

## Prior MI Work and the Remaining Gap

Direct equal-MI inference is not new.

- Zografos derived a two-sample Wald test for equality of phi-divergence
  association measures. Shannon MI is obtained with
  `phi(u) = u log(u)`.
- Mora and Ruiz-Castillo derived the regular asymptotic distribution of the
  mutual-information segregation index and explicitly supported pairwise
  comparisons.
- The `segregation` software supplies bootstrap inference for differences
  between MI indices.
- The current `DifferentialMI` project implements and validates the same
  first-order family with an explicit leading bias correction and extensive
  weak-null diagnostics.

Primary sources and details are recorded in
[EXTENSIVE_NOVELTY_REVIEW.md](EXTENSIVE_NOVELTY_REVIEW.md).

The searches for this review combined terms including:

```text
"mutual information" "profile likelihood" contingency table
"mutual information" "score confidence interval"
"mutual information" "power divergence" difference
"mutual information index" "profile likelihood" segregation
"equality of mutual information" likelihood ratio
"Linfoot" "profile likelihood" association
"Kullback-Leibler association" profile likelihood contingency
```

No explicit MI-difference implementation or finite-sample validation of the
constrained score, profile likelihood, Cressie-Read, modified likelihood-root,
or adjusted empirical-likelihood methods was located.

This is negative search evidence, not proof of absence. The final novelty
claim needs Scopus, Web of Science, MathSciNet, zbMATH, ProQuest, and citation
chaining from Zografos, Lang, Mora and Ruiz-Castillo, and Zhu and Lang.

## Candidate Ranking

| Rank | Candidate | Expected calibration gain | Cost | Generality | Main risk | Verdict |
|---:|---|---|---|---|---|---|
| 1 | Constrained score/profile LR/Cressie-Read | High enough to test decisively | One nonlinear constrained fit per test | Any fixed regular `r x c` tables | Nonconvex constraint and boundary fits | Implement first |
| 2 | Modified signed likelihood root or Bartlett correction | Potential second-order gain | More derivatives or correction work | Regular fixed-dimensional tables | Considerable mathematical complexity | Add only if rank 1 leaves a gap |
| 3 | Two-sample extended or adjusted empirical likelihood | Moderate | Jackknife pseudo-values plus scalar EL solve | Broad smooth functionals | Can waste known multinomial likelihood and inherit jackknife problems | Backup pilot only |
| 4 | Prepivoted permutation | Good weak-null validity | Repeated permutations, possibly bootstrap inside | Very broad | Does not meet the deterministic speed goal | Comparator, not primary method |
| 5 | Mean/median bias-reduced multinomial fit | Possible sparse stabilization | Iterative adjusted-score fit | Multinomial/log-linear models | Changes the fitting criterion and LR calibration | Exploratory extension |
| 6 | Directional higher-order test | Potentially excellent | Specialized higher-order calculation and integration | Exponential-family models | Hard to adapt cleanly to nonlinear equal MI | Too complex for first pass |

## Higher-Order Extension if the First Pass Is Not Enough

The first extension should refine the profile likelihood, not revive the
previous empirical saddlepoint approximation.

Define the signed likelihood root

```text
r(Delta_0) =
    sign(Delta_hat - Delta_0) * sqrt(G2(Delta_0)).
```

The ordinary first-order reference is standard normal. Barndorff-Nielsen's
modified root has the form

```text
r* = r + log(u / r) / r
```

and attains a substantially higher order of normal approximation under
regularity conditions:

- [Barndorff-Nielsen (1991), Modified signed log likelihood
  ratio](https://doi.org/10.1093/biomet/78.3.557)
- [DiCiccio and Martin (1993), Simple Modifications for Signed Roots of
  Likelihood Ratio Statistics](https://doi.org/10.1111/j.2517-6161.1993.tb01485.x)
- [Skovgaard (1996), An Explicit Large-Deviation Approximation to
  One-Parameter Tests](https://doi.org/10.3150/bj/1193839221)

A 2026 general higher-order Bartlett framework also provides an eventual
route to correcting profile likelihood-ratio calibration using observed
information:

- [Noma (2026), Universal higher-order Bartlett
  correction](https://doi.org/10.1016/j.spl.2026.110818)

This should be Phase 2, not the starting method. The project should first
establish whether ordinary score, LR, or `lambda = 2/3` power divergence
already removes enough finite-sample error.

## Why the Other Transfers Are Lower Priority

### Adjusted or extended empirical likelihood

Empirical likelihood replaces a normal pivot with a likelihood-ratio-like
constraint on observation weights. Jackknife empirical likelihood makes
nonlinear functionals easier by constructing delete-one pseudo-values, and
adjusted variants avoid convex-hull failures:

- [Chen and Ning (2016), Adjusted Jackknife Empirical
  Likelihood](https://arxiv.org/abs/1603.04093)
- [Tsao and Wu (2015), Two-sample extended empirical likelihood for
  estimating equations](https://doi.org/10.1016/j.jmva.2015.07.009)

There is a close precedent for transferring JEL to equality of a dependence
measure:

- [Sang, Dang, and Zhao (2019), Jackknife Empirical Likelihood Methods for
  Gini Correlations and their Equality
  Testing](https://doi.org/10.1016/j.jspi.2018.05.004)

This makes an MI transfer plausible. However, discrete tables already have a
fully specified multinomial likelihood. Replacing it with pseudo-value
empirical likelihood may throw away useful structure. The current project's
jackknife methods also did not outperform the analytic correction. JEL is a
reasonable backup experiment, not the strongest first thesis direction.

### Prepivoted permutation

Prepivoting transforms a statistic using an estimated limiting CDF before
permuting it. It is exact under equality of distributions and asymptotically
valid for equality of a parameter even when the distributions differ:

- [Fogarty (2021), Prepivoted permutation
  tests](https://arxiv.org/abs/2102.04423)

That theory maps closely to the equal-MI weak null and could improve on raw
group-label permutation. It remains a resampling test, however, and bootstrap
prepivoting can be more expensive than the current studentized permutation.
It does not satisfy the central objective of deterministic speed.

### Mean and median bias reduction

Adjusted-score methods can prevent infinite or unstable estimates in sparse
multinomial and Poisson log-linear models:

- [Kosmidis, Kenne Pagui, and Sartori (2020), Mean and median bias reduction
  in generalized linear models](https://doi.org/10.1007/s11222-019-09860-6)

This may later stabilize boundary-prone fits. It should not be mixed into the
initial profile test without a derivation, because penalized or adjusted
likelihood changes the reference distribution and can change what is being
estimated.

## Computational Expectations

After the observations have been reduced to two count tables, the proposed
test does not iterate over the original `n_P + n_Q` rows.

Let

```text
d = r_P c_P + r_Q c_Q - 2
```

be the number of free simplex coordinates. A dense Newton or trust-region
step can cost roughly `O(d^3)` because it solves a linear system, although
the MI Hessian has row/column structure that may permit cheaper operations.
If `J` iterations and `S` multistarts are used, a conservative description is

```text
O(S J d^3)
```

with no direct dependence on sample size after tabulation.

By comparison:

- JIDT's one-table significance method shuffles data labels and recomputes MI,
  so its direct cost grows with the number of shuffles and observations.
- The optimized differential-MI permutation code samples contingency tables
  directly, so its cost is closer to `O(K r c)` and is a much stronger speed
  comparator than data-level shuffling.
- The proposed optimizer should be much faster than data-level JIDT shuffling
  at large `N`, but it is not guaranteed to beat an optimized table sampler
  for every small table.

Runtime must therefore be measured rather than assumed. The scientific
advantage is not only speed: the constrained method directly represents the
weak null, whereas raw group-label permutation represents the stronger
exchangeability null.

JIDT's default `computeSignificance` is not itself a direct baseline for
`I(P) = I(Q)`. It tests one table against an independence/surrogate null. The
appropriate equal-MI resampling comparators are the existing studentized
group-label permutation and a constrained parametric bootstrap.

## Main Technical Risk

The null set

```text
{(p, q): I(p) - I(q) = 0}
```

is nonlinear and generally nonconvex. A generic optimizer can converge to a
local constrained optimum and silently overstate the likelihood-ratio
statistic.

The implementation must therefore include:

- exact objective, gradient, and preferably Hessian;
- simplex-preserving parameterization or explicit positivity constraints;
- multiple deterministic starts in difficult cases;
- KKT residual and constraint-residual reporting;
- verification that the constrained log likelihood never exceeds the
  unrestricted log likelihood;
- agreement between independent solver routes on audit cases;
- explicit handling of zero observed counts;
- flags for fitted expected counts near zero;
- continuation or warm starts when inverting a confidence interval; and
- a failure result rather than a fabricated p-value when optimization is not
  trustworthy.

This optimization work is the main engineering and methodological component
that turns a generic statistical idea into a defensible MI procedure.

## Decisive Validation Plan

### Stage 0: Mathematical and numerical verification

Implement the method in a new project folder, provisionally
`ProfileDifferentialMI`, without changing the frozen `DifferentialMI`
baseline.

Required checks:

1. manual MI, gradient, and Hessian agree with automatic or finite-difference
   derivatives on interior random tables;
2. the unrestricted optimizer reproduces empirical proportions;
3. constrained fits satisfy both simplex constraints and the target MI
   difference to at least `1e-9`;
4. Pearson, LR, and power-divergence statistics are nonnegative;
5. all three statistics converge numerically to zero as `Delta_0` approaches
   `Delta_hat`;
6. results are invariant to row/column permutations and swapping the two
   samples;
7. the test has one degree of freedom regardless of table shape;
8. profile results agree with Lang's generic `ci.table` implementation on
   small positive-count tables, if that software is obtained; and
9. exhaustive or dense multistart checks find no better constrained solution
   for selected `2x2` and `2x3` cases.

### Stage 1: Focused falsification pilot

Reuse frozen equal-MI scenario constructors from `DifferentialMI`.

Methods:

```text
wald_analytic
profile_score
profile_lr
profile_cr_2_3
student_perm_analytic, K = 999
constrained parametric bootstrap, K = 999, audit subset
```

Initial regimes:

```text
Shapes:       2x2, 3x3, 6x3, 6x6
Sample sizes: 30, 50, 100, 200
Marginals:    balanced, mildly skewed, strongly skewed
MI levels:    low regular, moderate, high
Designs:      equal and unequal sample sizes
Nulls:        equal MI with visibly different P and Q
```

Use at least 5,000 null replicates for the main calibration cells and more
for any apparent difference smaller than Monte Carlo uncertainty.

Primary outcomes:

```text
FPR at alpha = 0.10, 0.05, 0.01
absolute FPR error
95% confidence-interval coverage
average interval length
power at pre-specified Delta alternatives
runtime per test
solver convergence and diagnostic failure rate
```

### Stage 2: Decision rule

Proceed with the profile family if at least one candidate:

- reduces mean absolute FPR error relative to `wald_analytic` by at least 20%
  in the pre-specified hard regular regimes;
- does not materially degrade the balanced, well-supported regimes;
- maintains at least 99.5% trustworthy solver completion;
- gives confidence-interval coverage close to nominal;
- remains substantially faster than `K = 999` data-level shuffling in the
  moderate and large sample regimes; and
- has a clear advantage over studentized permutation in weak-null cases where
  the pooled mixture is nearly independent.

If ordinary score/LR/power divergence is still materially miscalibrated,
implement one higher-order likelihood refinement. Do not add JEL, Firth,
prepivoting, and `r*` simultaneously.

Stop this direction if:

- all three constrained statistics are no better than the frozen Wald test;
- solver failures concentrate in scientifically important regimes;
- runtime is comparable to or worse than optimized table resampling without
  an accuracy gain; or
- the apparent improvement depends on excluding ordinary zero-count tables.

## Recommended Thesis Question

The strongest current wording is:

> Can constrained multinomial score, profile-likelihood, and
> power-divergence inference provide better finite-sample calibration for
> differences in discrete mutual information than existing Wald inference,
> while remaining substantially cheaper than resampling?

If a higher-order refinement becomes necessary:

> Can an MI-specific higher-order modification of the signed profile
> likelihood root deliver reliable weak-null inference for differences in
> discrete mutual information under skewed, low-count multinomial sampling?

## Bottom Line

This is a valid next experiment and a better-aligned methodological direction
than continuing to optimize the restricted saddlepoint DP.

The clean contribution is not "profile likelihood is new." It is:

1. formulate equal discrete MI as a nonlinear constrained two-multinomial
   model;
2. build a reliable MI-specific constrained fitting algorithm;
3. compare score, likelihood-ratio, and Cressie-Read test inversion;
4. establish exactly where they improve on the known Wald and resampling
   methods; and
5. add a higher-order correction only if the evidence demands it.

The idea is broad across fixed table configurations, deterministic, and
directly focused on the known finite-sample weakness. Its feasibility is high
enough for a careful pilot, while its thesis novelty depends on producing a
real calibration or computational improvement rather than merely passing MI
into a generic contingency-table routine.
