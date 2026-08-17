# Thesis Writing Plan: Welch-Type Inference for Differential Mutual Information

## 1. Proposed Thesis Direction

### Working title

**Finite-Sample Welch-Satterthwaite Inference for Comparing Mutual Information Between Independent Categorical Populations**

### Central research question

For two independent categorical populations with joint distributions $P$ and
$Q$, can an MI-specific Welch-Satterthwaite reference distribution improve
finite-sample inference for

\[
H_0:I(P)=I(Q)
\]

relative to the usual normal Wald test, particularly when tables are skewed,
sparse, or have unequal sample sizes?

### Central thesis claim

The proposed expanded Welch-Satterthwaite test retains the bias-corrected MI
difference and influence-function standard error of the normal Wald test, but
uses MI-specific effective degrees of freedom to represent uncertainty in the
estimated variance. The method is deterministic, requires $O(rc)$ work for an
$r\times c$ table, leaves well-sampled inference largely unchanged, and
improves rejection calibration in several difficult finite-sample regimes. It
is a targeted correction rather than a uniformly exact replacement for Wald
inference.

### Scope

The thesis will focus on the independent two-sample weak null
$I(P)=I(Q)$, allowing $P\ne Q$. It will not present testing independence
$I(P)=0$ as the main problem, because that is a nonregular boundary where the
first-order MI influence variance vanishes. Transfer entropy, paired samples,
conditional MI, jackknife centring, and abandoned hybrid methods will remain
outside the main thesis.

## 2. Lessons From the Exemplar Theses

The three exemplars use different applications, but their strongest common
features provide a clear model for this thesis.

| Exemplar | Useful feature for this thesis |
| --- | --- |
| Grace Yan | Keeps the introduction short, separates limitations from future work, and moves extensive secondary figures to appendices. |
| Michael Fang | Gives the methodological contribution its own chapter, validates it on synthetic data with known truth, and only then discusses practical use. This is the closest structural model for our thesis. |
| Riley Jones | Ends the literature review with an explicit synthesis and research questions, then opens validation with a method outline tied to those questions. |

The main text of the exemplars runs from approximately 58 to 87 pages before
references. A suitable target for this thesis is **70-85 pages of main text**,
followed by references and technical appendices. The thesis should use fewer,
more purposeful subsections than the most fragmented exemplar.

## 3. Research Questions

The thesis will answer three questions.

**RQ1: Method construction.** How can the Welch-Satterthwaite principle be
adapted to the nonlinear plug-in MI variance estimator?

**RQ2: Statistical performance.** Does the expanded method improve type-I
error calibration and confidence-interval coverage relative to normal Wald and
simple Welch-Satterthwaite inference across well-sampled, skewed, sparse, and
unequal-sample regimes?

**RQ3: Practical trade-offs.** What power, computational cost, validity rate,
and operating-range trade-offs accompany the correction?

These questions correspond directly to the derivation, validation, and
discussion chapters. Novelty will be stated cautiously: the Welch-Satterthwaite
architecture and influence-function theory are established, while the proposed
contribution is their MI-specific combination, derivation, implementation, and
finite-sample evaluation for the equal-MI weak null.

## 4. Proposed Chapter Structure

### Chapter 1: Introduction (6-8 pages)

Start with the scientific need to compare the strength of association between
two populations, rather than testing whether either association is zero.
Introduce MI as a general measure of discrete dependence, state the weak null,
and explain why finite-sample variance uncertainty matters for nonlinear table
statistics. End with the research gap, questions, contributions, scope, and a
brief chapter outline.

The contribution statement should make four claims only:

1. An MI-specific derivation of component degrees of freedom for the estimated MI variance.
2. A deterministic expanded Welch-Satterthwaite test with $O(rc)$ complexity.
3. A controlled finite-sample validation against normal Wald and simple Welch baselines.
4. An empirical characterization of where the correction helps and where first-order inference remains unreliable.

### Chapter 2: Background and Related Work (14-18 pages)

Build only the background needed by the method. Cover entropy, pointwise mutual
information, mutual information, contingency-table estimation, plug-in bias,
first-order sampling variance, Wald inference, Welch-Satterthwaite inference,
and resampling approaches to comparing nonlinear statistics.

The literature review should move from broad foundations to the precise gap:

1. Shannon information, entropy, and MI.
2. Estimation and leading finite-sample bias of discrete MI.
3. Analytic comparison of smooth statistical functionals using influence functions and Wald tests.
4. Welch, Satterthwaite, and Hutcheson's entropy comparison.
5. Existing MI comparison and segregation-index literature, including Mora and Ruiz-Castillo.
6. Resampling under strong and weak null hypotheses.
7. Literature synthesis, novelty boundary, and the three research questions.

This chapter should distinguish prior components from the thesis contribution
without claiming that Welch-style testing itself is new.

### Chapter 3: Statistical Problem and Baselines (8-10 pages)

Define the two independent count tables, aligned alphabets, population
quantities, and assumptions. Derive the plug-in MI, leading bias correction,
MI influence variance, standard error, and standardized statistic. Then present
the two analytic baselines independently:

1. Normal Wald uses a standard normal reference.
2. Simple Welch-Satterthwaite uses $n_P-1$ and $n_Q-1$ as component degrees of freedom.

This chapter fixes the numerator and standard error shared by every analytic
method. It should also explain why $I(P)=0$ is excluded from the regular
first-order theory and reserve the full independence derivation for an
appendix.

### Chapter 4: Expanded Welch-Satterthwaite Method (15-18 pages)

This is the main methodological chapter and should follow the direct storyline
already developed in `EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`:

1. Start from the ordinary Welch-Satterthwaite equation.
2. Identify $\widehat V(P)/n_P$ and $\widehat V(Q)/n_Q$ as the two estimated variance contributions.
3. Model each positive variance estimate by a scaled chi-squared variable and match its mean and variance.
4. Derive the first-order sampling variance of $\widehat V(P)$.
5. Obtain the variance sensitivity $g_P(x,y)$ by differentiating $V(P)$ along a one-cell perturbation.
6. Use $\widehat{\tau}^2(P)$ to estimate the variability of that sensitivity.
7. Derive the component degrees of freedom and combine them into the final Student reference.
8. Give a table-based algorithm, computational complexity, assumptions, and one worked numerical example.

Every subsection should begin with the quantity being sought and why the final
test needs it. Detailed algebra that interrupts the argument can move to an
appendix, but the main derivation must remain complete enough to reproduce the
method.

### Chapter 5: Experimental Design (10-12 pages)

State the validation question before listing configurations: under population
pairs constructed to satisfy $I(P)=I(Q)$, how often does each method reject?

The primary design will use the existing unified experiment:

| Design element | Primary specification |
| --- | --- |
| Population pairs | 60 fixed equal-MI pairs |
| Regimes | Well sampled, moderate, highly skewed and sparse, ultra-skewed and sparse, widespread sparsity |
| Table shapes | $2\times2$, $2\times5$, $3\times3$, $3\times5$, $5\times5$, $8\times8$ |
| Replicates | 10,000 independent table pairs per population pair |
| Sample-size range | 50 to 1,000 per population |
| Primary nominal level | \(\alpha=0.05\) |
| Additional levels | \(\alpha=0.01\) and the full 0-0.10 calibration curve |
| Comparators | Normal Wald, simple Welch-Satterthwaite, expanded Welch-Satterthwaite |

Explain exactly how the Dirichlet margins and interaction patterns generate
distinct positive-support populations with equal target MI. Give explicit
sample-size rules, expected-count criteria, seeds, software versions, and
acceptance checks. A compact table should state the exact settings of every
regime; complete scenario parameters belong in an appendix or supplementary
CSV.

The primary outcome is rejection calibration. Secondary outcomes are 95%
coverage, power under unequal MI, valid-calculation rate, effective degrees of
freedom, and end-to-end runtime. Monte Carlo uncertainty must accompany
scenario-level rejection rates. Aggregates across scenarios should not replace
the scenario-level results.

### Chapter 6: Results (10-14 pages)

Present results in the same order as the research questions and avoid narrating
every table entry.

1. Begin with implementation and mathematical sanity checks.
2. Show rejection-calibration curves by regime as the main figure.
3. Report FPR at 0.05 and 0.01 with Monte Carlo intervals and mean absolute calibration error.
4. Show scenario-level heterogeneity so aggregate improvements cannot hide failures.
5. Report confidence-interval coverage and valid-calculation rates.
6. Report the power cost of heavier-tailed references.
7. Report runtime in milliseconds and relative to normal Wald.
8. Present the independent adversarial holdout and scaled-chi-squared diagnostic as robustness evidence.

The main results narrative should be: expanded Welch changes well-sampled
inference only slightly, improves average calibration in difficult regimes,
loses a small amount of power, remains computationally negligible, and does
not fully solve widespread or extreme sparsity.

### Chapter 7: Discussion (8-12 pages)

Interpret why the method helps: normal Wald treats the estimated standard
error as effectively known, whereas expanded Welch measures how unstable that
variance estimate is for the observed MI functional and uses a heavier-tailed
reference when warranted.

Discuss the contribution relative to prior literature, practical operating
range, power-calibration trade-off, deterministic runtime, and reproducibility.
Address limitations directly: first-order asymptotics, positive-support
assumption, residual MI centring bias, nonregular independence boundary,
possible conservative behaviour, and lack of uniform dominance. Explain that
the jackknife refinement was investigated but not adopted because it did not
improve the primary configuration grid consistently.

Finish with focused future work: improved centring in extreme sparse unequal
samples, second-order treatment near independence, extension to conditional MI,
and external application studies.

### Chapter 8: Conclusion (2-3 pages)

Answer each research question directly, restate the contribution without new
claims, identify the practical recommendation, and state the main limitation.

## 5. Figures and Tables for the Main Text

The main thesis should prioritize a small number of figures that each answer a
specific question.

| Item | Purpose |
| --- | --- |
| Method overview diagram | Show the shared statistic and where the three reference distributions differ. |
| One-cell perturbation diagram | Give intuition for the MI-variance influence calculation. |
| Experimental grid diagram or table | Show shapes, sample sizes, MI targets, and sparsity criteria. |
| Rejection-calibration figure | Primary evidence: nominal versus observed rejection rate by regime. |
| Scenario-level calibration plot | Reveal heterogeneity hidden by regime averages. |
| Degrees-of-freedom diagnostic | Connect variance instability to the strength of the correction. |
| Power comparison | Quantify the calibration-power trade-off. |
| Runtime table | Demonstrate negligible deterministic cost. |

Q-Q plots, all individual scenarios, full parameter tables, scaled-chi-squared
diagnostics, and extra significance levels should be placed in appendices.

## 6. Appendices

Use appendices to preserve auditability without breaking the main argument.

| Appendix | Content |
| --- | --- |
| A | Full algebra for the expanded variance-influence derivation. |
| B | Population-construction algorithm and complete scenario specifications. |
| C | Additional calibration, Q-Q, coverage, power, and validity results. |
| D | Scaled chi-squared working-model validation and finite-difference checks. |
| E | Independence as a nonregular boundary and why the first-order method does not replace chi-squared independence testing. |
| F | Reproducibility details, software versions, seeds, repository layout, and commands. |

Abandoned custom rules and exploratory dead ends should remain in the research
archive rather than the thesis, unless they provide evidence needed to justify
a final design decision.

## 7. Writing and Verification Order

Writing should begin with the parts already supported by stable mathematics and
results, rather than drafting the introduction first.

1. Freeze notation, scope, estimand, baselines, and the exact version of the expanded method.
2. Build the LaTeX project and chapter skeleton using the exemplar front matter and formatting conventions.
3. Draft Chapter 3 from the current summary and Chapter 4 from the full derivation.
4. Draft Chapter 5 directly from the primary experiment code, metadata, and fixed scenario files.
5. Draft Chapter 6 from machine-generated result tables and figures; do not transcribe numbers manually.
6. Refresh the literature search and draft Chapter 2 with a claim-to-citation matrix.
7. Write Chapters 1, 7, and 8 after the contribution and empirical boundaries are fixed.
8. Move supporting derivations and diagnostics into appendices.
9. Perform a notation, units, cross-reference, citation, and reproducibility audit.
10. Complete a final claim audit in which every abstract and conclusion statement points to a theorem, derivation, experiment, or cited source.

## 8. Evidence to Freeze Before Final Results Writing

Most required evidence already exists, but the following should be frozen as a
single thesis release before numerical prose is finalized:

1. One clean rerun of all unit tests and the primary experiment from a recorded commit and environment.
2. A manifest linking every thesis table and figure to its generating script and source file.
3. Numerical finite-difference checks of the analytic $g_P(x,y)$ formula on representative positive-support tables.
4. Confirmation that the independent adversarial holdout was not used to tune the final method.
5. A refreshed literature search supporting the final novelty wording.
6. A decision with the supervisor on whether a short real-data illustration is required; it would demonstrate use, not validate type-I error because the population truth is unknown.

## 9. Immediate Next Deliverable

After this plan is agreed, create a compilable LaTeX skeleton in
`Thesis Writeup/Welch MI` with separate files for each chapter, a shared
notation file, bibliography, figure directory, and placeholder chapter
introductions. The first substantive drafting milestone should be complete
drafts of Chapters 3 and 4, because they define the method that every later
chapter evaluates.

The prose, notation, equation presentation, and chapter-level voice should
follow the companion [writing style guide](WRITING_STYLE_GUIDE.md).
