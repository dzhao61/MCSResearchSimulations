# Thesis Rewrite Plan

13 September 2026. This is the active plan for the next thesis draft. It replaces the empirical direction in [THESIS_PLAN.md](THESIS_PLAN.md) and draws on the [exemplar review and writing notes](EXEMPLAR_REVIEW_NOTES.md). The existing LaTeX manuscript is the previous draft; this planning stage does not revise its chapters.

## 1. Thesis direction

### Working title

**Comparing Mutual Information in Finite Samples: Wald and Expanded Welch-Satterthwaite Inference**

This title names the problem and methods without promising that the proposed correction improves inference. The central question is:

> When does an MI-specific Welch-Satterthwaite correction improve inference about the difference between two populations' mutual information, and what costs accompany that correction?

The thesis studies two independent categorical samples and the hypothesis

\[
H_0:I(P)=I(Q),\qquad H_1:I(P)\ne I(Q).
\]

Equality of MI allows different joint distributions and different margins. Independence of the two **samples** does not require independence of X and Y **within** either population.

### Central argument supported by the current evidence

Expanded Welch derives effective degrees of freedom from the sampling variability of the estimated MI variance. The resulting Student reference gives a more stringent rejection threshold than the normal reference for the same finite statistic. This can reduce excessive false positives, but it can also make an already conservative test more conservative. The observed loss of rejection under alternatives also reflects additional invalid outputs in some sparse regimes.

The completed experiments do not support Expanded Welch as a general replacement for Normal Wald. They establish a more specific result: the usefulness of the correction depends on the population table and sampling regime, and improved null rejection alone is insufficient to establish an improvement in the complete procedure.

This also does not establish that Wald is universally reliable or optimal. Wald has failures in the tested regimes, and the final experiment compares only these two implementations. Near independence, even a large nominal sample can remain outside a satisfactory approximation regime.

### Contributions

1. Derive an MI-specific Welch-Satterthwaite reference adjustment by differentiating the complete MI variance functional, including changes to its estimated margins and pointwise MI values.
2. Implement the method and identify its theoretical assumptions, numerical validity requirements and relationship to Normal Wald.
3. Evaluate calibration, detection, validity and computation through explicit fixed populations, paired simulations and individually reported regimes.
4. Characterise the correction's benefits and limitations, including sensitivity to baseline MI, unequal samples, construction and sparse support.

The mathematical ingredients are established ideas. Any claim that the particular combination or derivation is new must follow a checked literature comparison. A carefully explained limitation is part of the contribution; the thesis does not require a uniformly superior test.

## 2. Scope and evidence hierarchy

| Material | Role in the new thesis |
| --- | --- |
| [Completed thesis experiment report](../../WelchSatterthwaiteMI/docs/experiments/THESIS_EXPERIMENTS.md) and `results/thesis_redesign/` | Primary empirical evidence. All headline conclusions and numerical tables should come from this run. |
| [Frozen executable protocol](../../WelchSatterthwaiteMI/experiments/THESIS_REDESIGN_PROTOCOL.json) and [experiment design](../../WelchSatterthwaiteMI/docs/experiments/THESIS_EXPERIMENT_PLAN.md) | Authoritative design, parameter values and reporting conventions. |
| [Expanded Welch derivation](../../WelchSatterthwaiteMI/docs/theory/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md) and the implemented statistic | Main mathematical source, reconciled with the actual implementation before drafting. |
| [MI Taylor expansion](../../WelchSatterthwaiteMI/docs/theory/MI_TAYLOR_EXPANSION.md) and [independence note](../../WelchSatterthwaiteMI/docs/theory/INDEPENDENCE_REFERENCE_DISTRIBUTION.md) | Mathematical presentation model and boundary explanation. |
| [Earlier construction check](../../WelchSatterthwaiteMI/docs/experiments/CONSTRUCTION_CHECK.md) | Development context and pointers to construction literature; the matched construction section in the final run supplies the primary comparison. |
| [Binary LR validation](../../WelchSatterthwaiteMI/docs/experiments/CONSTRAINED_LR_2X2_VALIDATION.md), [larger-alphabet LR validation](../../WelchSatterthwaiteMI/docs/experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md) and other exploratory refinements | Optional short discussion of alternatives. They are separate experiments with different designs and replication counts, not additional curves in the final Wald-Welch study. |
| Previous draft, figures and 60-pair results | Historical material. Do not carry their numerical claims into the new results or abstract. |

The core thesis covers finite, fixed categorical alphabets, independent multinomial samples and a two-sided test at alpha=0.05. It includes regular positive-MI settings and explicitly labelled stress checks at the independence boundary. It does not validate paired data, time dependence, continuous estimators or alphabets growing with sample size.

Simple Welch can appear briefly as the motivating n-1 analogy. It is not a third comparator in the completed final experiment. LR may receive one short alternatives subsection or appendix, but it does not need its own main chapter. Do not revive oracle comparisons, size-adjusted power or additional correction rules as required thesis deliverables.

A real-data case study is not required by the present scientific question. Simulations provide known population truth for calibration and power. An eventual application could illustrate use, but would not substitute for that validation. The examples' application chapters are structural choices, not a requirement inferred for this thesis.

## 3. What must change from the previous draft

| Previous content | Required revision |
| --- | --- |
| Abstract and conclusion describe a broadly useful refinement with a small power cost. | Rewrite around conditional usefulness, substantial possible conservatism, method-specific validity and measured computational cost. |
| Primary study uses 60 random equal-MI population pairs and five alternatives. | Replace with the completed fixed-population design: 3,111 unique configurations, 534 population pairs and 20,000 sampled pairs per configuration. |
| Random Dirichlet margins and fitted random interactions dominate the design chapter. | Explain explicit marginal vectors and additive cell changes first. Put the ordinal log-linear comparison in a short construction-sensitivity subsection. |
| Sample sizes begin at 50 and sparse cases are selected using expected-count bands. | Describe the actual fixed sample ladders, including n=1 stress cases, with no expected-count eligibility filter. State the finite tested ranges rather than claiming unlimited sparsity coverage. |
| Calibration averages across shapes and regimes lead the results. | Lead with individual-regime panels. Any descriptive count of favourable regimes is secondary and is not a performance average or statistical test. |
| Methods share a validity mask. | Describe separate Wald and Expanded Welch validity, and distinguish unconditional, method-valid and common-valid rejection rates. |
| Pairing is said to remove Monte Carlo variation from method differences. | Explain that pairing usually reduces Monte Carlo uncertainty; it does not eliminate it. Use the saved paired comparisons. |
| Normal Wald is described as treating the variance as known. | State that it uses a plug-in standard error and an asymptotic normal reference, without the proposed finite-sample degrees-of-freedom adjustment. |
| Confidence-interval coverage and several significance levels are primary findings. | The final run records testing performance at alpha=0.05. Do not report old coverage or additional-alpha results as outcomes of this design. |
| A new confirmatory grid and broader power experiment are proposed as future work. | These have been completed. Future work should address remaining scientific limitations, not completed tasks. |
| Figures are found through old global search paths. | Generate a dedicated thesis figure directory from the final results, with explicit source mappings. |

Reuse the LaTeX organisation, notation macros where appropriate, and checked mathematical derivations. Rebuild Chapters 5-8 and the abstract. Revise Chapters 1-4 for the new questions, scope, assumptions and interpretation.

## 4. Research questions and how they are answered

| Question | Evidence and assessment | Chapters |
| --- | --- | --- |
| RQ1. How can uncertainty in the estimated MI variance be translated into an MI-specific Welch-Satterthwaite reference? | Derivation of the MI and variance sensitivities, moment matching, a worked calculation, and checks against the implementation. Separate identities from approximation assumptions. | 3-4 |
| RQ2. How does Expanded Welch change false positives, detection and valid-result frequency relative to Normal Wald across fixed regimes? | Full main landscape; null point and alternative curve in each panel; intervals and validity; paired method comparisons. | 5-6 |
| RQ3. How do baseline MI, marginal distributions, unequal samples, cell changes and population construction affect that comparison? | Matched focused comparisons, rectangular tables, extreme skew and boundary experiments. Interpret each factor within the settings actually held fixed. | 5-7 |
| RQ4. What happens with larger samples, and what computational cost and practical recommendation follow? | Fixed-population convergence curves, exact-regime scalar runtimes, and the combined calibration-power-validity evidence. | 6-8 |

"Better" must be defined before examining results. Under H0, a two-sided 5% test should reject near 5%, not as rarely as possible. Under H1, larger rejection is useful when the null behaviour and validity are acceptable. The main comparison uses the nominal 5% threshold; it does not estimate power at equal achieved size.

## 5. Chapter plan

The proposed structure retains eight chapters, with a larger empirical emphasis than the old draft. A working allocation is about 68-88 main-text pages, excluding references and appendices. These are planning ranges, not a degree requirement or a target to fill with prose.

| Chapter | Working pages | Role |
| --- | --- | --- |
| 1. Introduction | 4-5 | Establish the problem, questions and contribution. |
| 2. Background and Related Work | 10-12 | Supply the necessary foundations and locate the methodological question. |
| 3. Comparing Mutual Information with Normal Wald | 7-9 | Define the data, estimand, estimator, standard error and baseline test. |
| 4. Expanded Welch-Satterthwaite Inference | 10-12 | Derive the adjustment, its interpretation and limitations. |
| 5. Experimental Design | 9-12 | Explain fixed populations, sampling, comparisons and metrics. |
| 6. Experimental Results | 19-25 | Show the landscape, focused comparisons, limits and runtime. |
| 7. Discussion | 7-10 | Answer the questions and explain the practical implications and limitations. |
| 8. Conclusion | 2-3 | State what was established and the resulting recommendation. |

### Chapter 1. Introduction

**Purpose:** explain why a difference in measured dependence needs an uncertainty assessment.

Open with a concrete generic example: two independent groups are observed on the same categorical variables, and their estimated MI values differ. The scientific question is whether that difference is compatible with sampling variation. Distinguish this from asking whether either group's variables are independent.

Use four sections: problem and motivation; limitations of existing first-order comparison; research questions and contributions; scope and thesis outline. Introduce only the equal-MI hypothesis and enough terminology to state the question. Defer the variance formula and degrees-of-freedom derivation.

State the empirical outcome briefly and honestly: the proposed correction helps some regimes but does not support a general replacement for Wald. The introduction should motivate investigating the correction, not assume its success.

**Outputs:** a concise contribution list and a question-to-chapter map. Avoid a long overview of all of information theory or a list of every exploratory method attempted.

### Chapter 2. Background and Related Work

**Purpose:** explain which established ideas the method uses and what is being evaluated beyond them.

Organise by problem rather than one paragraph per paper:

1. Categorical joint distributions, margins, entropy, pointwise MI and MI, using one small table throughout.
2. Estimating discrete MI from counts: sampling error, leading bias and why unobserved cells matter.
3. Comparing a scalar functional across independent samples: first-order Taylor theory, plug-in standard errors and Wald inference.
4. The classical Student and Welch constructions: random denominators, moment matching and why a normal numerator divided by an estimated standard deviation is not automatically Student distributed.
5. Existing entropy and MI comparison methods, including the relevant influence-function and resampling literature.
6. Synthesis: the proposed MI-specific denominator calculation, the assumptions that remain, and the empirical questions it leaves open.

Retain relevant bibliography entries for Shannon, Miller, Moddemeijer, Paninski, Satterthwaite, Welch, Hutcheson and the functional-comparison literature, after checking the actual cited passages. The older draft also cites Mora and Ruiz-Castillo and weak-null permutation work; verify what hypothesis and setting each source addresses before using it as a comparator.

Add verified primary references for simulation reporting and the additive table construction. The construction-check note points to Berrett and Samworth and a later comparison paper; check their original parameterisations and explain the adaptation from independence testing to equal positive MI. A construction borrowed for one hypothesis does not validate a different test.

**Outputs:** a compact prior-work comparison table with columns for target hypothesis, data assumptions, method and relevance; a claim-to-source record for the author. The literature refresh is a drafting task still to perform, not something this plan claims to have completed.

### Chapter 3. Comparing Mutual Information with Normal Wald

**Purpose:** make the shared statistic understandable before adding the proposed correction.

Use five sections: data and hypothesis; MI estimation and bias correction; first-order sampling variance; the Wald statistic; assumptions and validity.

Define population probabilities, count tables, empirical probabilities and natural-log units. Retain the signed convention

\[
\Delta=I(P)-I(Q).
\]

The graph axis will be the true magnitude |Delta|. The saved experiment field `signed_mi_difference_q_minus_p` has the opposite sign, so the thesis export must convert it explicitly. Under the usual experiment direction, I(Q)>I(P), hence Delta<0 even though the horizontal coordinate is positive.

Derive the shared estimates:

\[
\ell_P(i,j)=\log\frac{p_{ij}}{p_{i+}p_{+j}},\qquad
V(P)=\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2,
\]

\[
\widehat I_{\rm BC}(P)=\widehat I(P)-\frac{(r-1)(c-1)}{2n_P},
\]

\[
T=\frac{\widehat I_{\rm BC}(P)-\widehat I_{\rm BC}(Q)}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
\]

Explain that V(P) is the variance of a pointwise contribution; V(P)/n_P is the first-order approximation to the sampling variance of estimated MI. Neither is the variance of the category labels. Derive this through a labelled first-order Taylor expansion rather than introducing an influence function without explanation.

State that the full declared table dimensions determine the bias correction, even when observed cells are empty. The implementation does not clip negative bias-corrected estimates. For equal sample sizes the two fixed corrections cancel in the difference; for unequal sample sizes they do not. This will be important when interpreting imbalance experiments.

Explain separately what is calculated from observations and where H0 is used: the population equality supplies the reference centring and rejection interpretation. We do not replace observed quantities by zero just because the null is being tested.

**Outputs:** a notation table, the derivation of the standard error, and a worked observed-table calculation that is checked against the software. Give the normal two-sided p-value after defining T. Reserve extended independence algebra for an appendix.

### Chapter 4. Expanded Welch-Satterthwaite Inference

**Purpose:** derive exactly what changes and why this change remains an approximation.

Use six connected sections:

1. The Welch-Satterthwaite combination, with the two variance contributions identified as Vhat(P)/n_P and Vhat(Q)/n_Q.
2. Moment matching: relate the mean and variance of a positive variance estimate to effective degrees of freedom.
3. Sensitivity of the complete MI variance: define a one-cell perturbation, explain how it changes the joint probabilities and both margins, and derive g_P.
4. Sampling variability of the variance estimate and the estimated component degrees of freedom.
5. The final Student reference, algorithm, numerical validity and computational complexity.
6. What follows from the construction and what still requires empirical assessment.

The key chain is

\[
\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\},\qquad
\operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P},\qquad
\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
\]

Then combine the two component degrees of freedom using the variance weights. Define all quantities before using the compact formula. Show the purpose and the main derivative calculations in the chapter; put repeated algebra in Appendix A. Follow the Taylor presentation in the companion notes, including the function being differentiated and the expansion point.

Make three distinctions explicit. Independence between the P and Q samples gives independent variance contributions. It does not make the numerator and denominator computed from the same sample independent. Matching two moments of the denominator does not determine the finite-sample distribution of their ratio.

Include a short proposition, with a checked justification, that for the shared statistic and positive finite Expanded Welch degrees of freedom, its two-sided p-value is no smaller than Wald's. On common-valid inputs its rejection set is therefore contained in Wald's. This explains why the proposed correction can lower rejection but cannot directly raise it when Wald is too conservative.

Document implemented validity separately from population assumptions. Wald requires a usable total estimated variance. Expanded Welch additionally requires usable component and combined degrees of freedom. A zero variance contribution from one group need not invalidate Wald if the other group supplies a positive denominator, whereas the current Expanded Welch implementation rejects unusable component calculations. Record the existing numerical variance tolerance in the algorithm appendix. Do not silently change these rules while writing.

**Outputs:** one comparison diagram or compact formula table, one pseudocode algorithm, and one worked example continuing Chapter 3. Explain O(rc) work from counts and the extra constant factor. Do not include population-construction optimisation in test-time complexity.

### Chapter 5. Experimental Design

**Purpose:** let the reader reconstruct what each plotted point means without reading the simulation code.

Use five sections: evaluation questions and fixed design; constructing P and Q; sampling and paired methods; measured outcomes and uncertainty; experiment families and runtime.

Start with a small worked population example. The reader should understand the distinction between the fixed table of probabilities and the random table of observed counts before seeing the complete experiment grid.

Present the additive family for one population R as

\[
R(t)=a b^{\mathsf T}+tH,
\qquad H\mathbf 1=0,\quad \mathbf 1^{\mathsf T}H=0.
\]

Here a and b in this equation are row and column vectors; use a separate symbol, I_0, for baseline MI throughout the final manuscript to avoid the old collision between a baseline and an independence table. The simplest H contains the block

\[
\begin{pmatrix}1&-1\\-1&1\end{pmatrix}
\]

in the first two rows and columns and zeros elsewhere. Explain adding and subtracting the same mass in plain language, show that margins remain fixed, and state the positive range

\[
0\le t<t_{\max},\qquad
t_{\max}=\min_{H_{ij}<0}\frac{a_i b_j}{-H_{ij}}.
\]

Solve separately for t_P and t_Q to achieve the requested MI. The complete numerical algorithm belongs in Appendix B. The family endpoint is not the maximum MI over all possible tables with those margins. Targets were checked for feasibility before sampling; do not extrapolate curves beyond constructed targets.

For a dimension of size k, define a skewed margin by

\[
m_k(\rho)=\left(\rho,\frac{1-\rho}{k-1},\ldots,
\frac{1-\rho}{k-1}\right).
\]

Use rho here only for the dominant marginal probability, and write sample ratios explicitly as n_Q:n_P. For rectangular tables apply m_r to rows and m_c to columns. State P and Q separately for every profile: uniform/uniform, 0.8/0.8, and 0.7/0.8.

For the standard direction set I(P)=I_0 and I(Q)=I_0+|Delta|. The reverse-direction experiment switches which population receives the higher target. At the same-margin main null, the construction gives P=Q; the different-margin null gives equal MI for distinct distributions. This distinction is essential when interpreting how broadly the weak null has been tested.

Explain the remaining constructions precisely. The rare block occupies the last two rows and columns. The spread pattern uses an outer product of equally spaced, centred row and column scores; it is not simply a collection of separate four-cell blocks. The log-linear comparator uses an ordinal interaction with fitted margins. In that comparison, matching margins and MI does not hold every cell probability or expected count fixed.

End with the fixed experiment-family table in Section 6 of this plan and the metrics in Section 7. Mention the frozen protocol and completed run, but move seeds, hashes and software records to the reproducibility appendix.

**Outputs:** a numerical 2x2 population example, diagrams of the change matrices, the exact experiment-family table, and definitions of rejection, validity and uncertainty.

### Chapter 6. Experimental Results

**Purpose:** show the complete landscape first, then explain how the controlled comparisons refine it.

Use the same order as the design. Suggested subsections are:

1. Main landscape across table size, margins and sample size.
2. Baseline MI and the location or spread of cell changes.
3. Unequal sample sizes and which population has greater MI.
4. Larger effects and rectangular tables.
5. Sensitivity to the population construction.
6. Extreme skew and empirical support loss.
7. Exact independence and large-sample behaviour.
8. Runtime.

Each ordinary power panel includes its H0 point at zero and H1 points at positive differences. Avoid separating them into unrelated experiments with different settings. Explain their distinct interpretation in the caption. Convergence panels instead vary n at fixed equal-MI populations and need a clearly labelled sample-size axis.

Within each subsection use the same reading sequence: the question; the figure; its self-contained specifications; the observed pattern; any immediate validity qualification. Group similar panels for legibility but do not average their rates. Results prose should name specific regimes and changes, not describe every plotted point.

Use the design-based display scheme in Section 8. Report both improvements and failures visible in the full landscape. Small numerical differences near the nominal rate should be interpreted with Monte Carlo intervals, not converted into confident "wins".

The final section reports per-call runtime with units and exact settings. A median ratio across timing regimes may be a secondary summary, accompanied by the individual results. It does not establish the statistical value of the method.

**Outputs:** thesis-sized figures generated from the saved data, concise numerical comparisons with configuration identifiers in the source manifest, and direct links to complete supplementary results.

### Chapter 7. Discussion

**Purpose:** explain what the results mean for the original proposal and for someone choosing a test.

Open with direct answers to RQ1-RQ4. Then discuss the mechanisms: a heavier-tailed reference can address some excessive rejection, but it does not repair residual numerator bias, an inadequate first-order variance approximation, or dependence between the estimated numerator and denominator. Distinguish these plausible mechanisms from mechanisms specifically diagnosed by the recorded outputs.

Discuss the unequal-sample correction terms, the distinction between exact independence and small positive MI, and the role of empty empirical cells. The constructor comparison should be interpreted as a robustness check across matched MI/margins, not proof that all population-generation bias has been eliminated.

State the practical recommendation conditionally. The current evidence favours retaining Wald as the simpler baseline rather than adopting Expanded Welch generally. In a particular regime, check calibration and valid-result frequency before interpreting its power curve. Choosing the method after seeing an individual p-value is not a validated selection procedure.

The limitations section should cover fixed selected populations, restricted dependence patterns, finite alphabet sizes and sample ladders, one nominal alpha, lack of real-data validation, method-specific invalid outputs, and the unvalidated finite-sample Student assumptions. Twenty thousand repeats estimate behaviour for each fixed pair precisely; they do not turn 534 selected population pairs into a representative sample of all distributions.

Describe the experiment as a protocol frozen before its final simulation, following exploratory work. The local freeze is not external preregistration or a completely untouched scientific hypothesis. Reused configurations displayed in several sections are the same simulation, not independent replications.

Briefly position LR and earlier refinements as alternatives investigated in separate studies, if they help explain the research boundary. Avoid a catalogue of unsuccessful attempts. Future work can address numerator-denominator behaviour jointly or the transition near independence, with empirical validation still required. Do not promise that a fancier correction will succeed.

**Outputs:** an evidence-bounded recommendation and specific limitations, each linked to the relevant assumption or result.

### Chapter 8. Conclusion and abstract

The conclusion should answer the main question in two or three pages without new results: what was derived, what the broad evaluation established, what practical trade-off remains and what the evidence does not settle.

Write the abstract last, provisionally in 250-350 words unless the applicable requirements specify otherwise. Use this sequence: the equal-MI problem; the proposed variance-based adjustment; the completed controlled experiment; the conditional findings; the recommendation. Include at most a few representative numbers with clear meaning. Do not lead with the total number of evaluations as if it were the scientific contribution.

## 6. Completed experiment families to describe

All statistical configurations use 20,000 sampled table pairs, both methods on the same samples and alpha=0.05. The following summarises the frozen protocol, not proposals for a new simulation. Values of I_0 and |Delta| are in nats.

| Family | Fixed and varied settings | What it addresses |
| --- | --- | --- |
| Main | Shapes 2x2, 3x3, 5x5, 8x8; all three margin profiles; I_0=0.02; differences {0, 0.001, 0.002, 0.005, 0.01, 0.02}; equal n in {2, 5, 10, 20, 50, 100, 250, 500, 1000}; first block. | Broad calibration, detection and validity landscape. |
| Baseline | Same four shapes and profiles; I_0 in {0.0001, 0.001, 0.02}; main difference grid; equal n in {20, 100, 1000}; first block. | Sensitivity to the starting amount of dependence. |
| Changed cells | Shapes 3x3, 5x5, 8x8; different-skew profile; I_0=0.0001; differences {0, 0.0001, 0.00025, 0.0005, 0.001, 0.002}; n in {20, 100, 1000}; first/rare blocks and spread for 5x5 and 8x8. | Sensitivity to where dependence is placed. |
| Imbalance | Four square shapes and all profiles; I_0=0.02; main differences; sample pairs {(50,50), (50,100), (100,50), (50,250), (250,50), (50,500), (500,50), (500,500)}; both MI directions. | Sample allocation and direction, with balanced controls. |
| Larger effects | Shapes 2x2, 3x3; all profiles; I_0=0.02; main difference grid extended by {0.05, 0.1, 0.2}; n in {20, 100, 1000}. | Detection over a wider feasible MI range. |
| Rectangular | Shapes 2x3, 3x5; all profiles; I_0=0.02; main differences; n in {20, 100, 1000}. | Unequal row and column alphabet sizes. |
| Construction | Shapes 3x3, 5x5, 8x8; uniform/different-skew profiles; I_0 in {0.0001, 0.02}; main differences; n in {20, 100, 1000}; additive first block versus ordinal log-linear tables. | Dependence on the chosen construction. |
| Extreme skew | Shapes 2x2, 3x3, 8x8; P/Q dominant probabilities {(0.9,0.95), (0.99,0.995), (0.999,0.9995)}; I_0=0.00001; differences {0, 0.00001, 0.00005, 0.0001, 0.0002}; n in {1, 2, 5, 20, 100, 1000, 10000}. | Very rare categories and very small samples. |
| Rare-cell stress | Shapes 3x3, 8x8; dominant pair (0.9,0.95); first/rare blocks; I_0=0.00001; differences {0, 0.00001, 0.000025, 0.00005, 0.0001}; same n ladder as extreme skew. | Location of dependence under extreme sparsity. |
| Independence | Shapes 2x2, 8x8; all profiles; I_0=0; main differences; n in {2, 20, 100, 1000}. | Explicit boundary check outside the regular two-positive-MI derivation. |
| Convergence | Four square shapes and all profiles; equal MI in {0.0001, 0.02}; n in {1000, 2500, 10000, 50000}; first block. Additional rare-block controls use 3x3, 5x5, 8x8, different-skew margins and MI=0.0001. | Behaviour as samples grow while populations remain fixed. |
| Runtime | Shapes 2x2, 3x3, 5x5, 8x8, 3x5; uniform/different-skew margins; n in {20, 100, 1000}; I_0=0.02; differences {0, 0.02}; 200 saved inputs per regime, 20 warm-up calls, five timing passes. | Cost of complete scalar test calls. |

The run contains 3,111 unique configurations and 4,001 display points because some configurations are reused across sections. The statistical total is 62,220,000 sampled table pairs and 124,440,000 method evaluations. Do not count display points as independent configurations or count a pair as a single observed table.

There is no expected-count floor for admitting a configuration. The design still has finite limits: sample sizes start at one in stress checks, the most dominant tested marginal probability is 0.9995, and the largest square table is 8x8. Numerical positivity and target-feasibility checks remain necessary. At n=1 the statistic cannot be evaluated and is explicitly recorded as invalid.

## 7. Metrics, uncertainty and interpretation

Use R=20,000 for simulation replicates and n_P,n_Q for observations per sample. For method m define the rejection indicator A_m to equal one when the output is valid and its p-value is at most alpha; otherwise it is zero. The primary plotted rate is

\[
\widehat r_m=\frac{\text{number of valid rejections}}{R}.
\]

This is the probability that the procedure produces a rejection, counting invalid outputs as no rejection for this reporting convention. An invalid result is still a failure to obtain a test result, not a valid acceptance of H0 or a true negative.

Always accompany it with valid-result frequency. Report conditional rejection among method-valid replicates and among common-valid replicates in the detailed tables. When no outputs are valid, conditional rejection is undefined, not zero. Different method-valid denominators cannot isolate the effect of changing the reference distribution.

Under equal MI the rate measures false positives; under unequal MI it measures detection at the fixed threshold. Do not add size-adjusted power to the main thesis. State the limitation of interpreting nominal power when achieved null rejection differs.

Use saved pointwise Wilson 95% intervals for individual rejection probabilities. Near 0.05, 20,000 replicates give Monte Carlo standard error approximately 0.00154; near 0.5 it is approximately 0.00354. These measure uncertainty from repeated sampling of the fixed populations. They do not measure uncertainty about whether the selected population families represent an application.

Use the saved paired difference and paired standard error when reporting differences between methods. These are based on the same sampled tables; treating the estimates as independent would discard that information. The saved paired intervals are approximate normal intervals, not Wilson intervals or simultaneous guarantees. A near-zero-discordance result must not be presented as proof of exact equality.

Define minimum expected count explicitly as min over cells of n_P p_ij, separately for each population. It is not the expectation of the minimum observed count. Report empty rows, empty columns and zero-cell fractions when they explain lost validity. The hollow-marker threshold of 90% validity is a display warning, not an established statistical safety threshold.

No single aggregate score will decide the winner. Descriptive counts of regimes and ranges may help orient the reader, but the individual evidence must remain visible. Avoid treating thousands of pointwise intervals as a multiple-comparison claim that every deviation is significant.

## 8. Figures, tables and symmetrical presentation

### Landscape before interpretation

The current report contains 99 primary figures and seven calibration zooms. It is a full research atlas, not a collection to paste unaltered into a thesis chapter. Use two levels of presentation:

1. Main text: a systematic landscape, followed by focused figures organised by experimental question.
2. Companion atlas and appendices: the full configuration coverage, all sample ladders, intervals, validity and exact numerical values, indexed by the same figure and configuration identifiers.

For the main landscape, show all four square alphabet sizes and all three profiles. A compact opening view can use n={10,100,1000} for every shape/profile, selected uniformly by design rather than by observed performance. The full nine-value sample ladder remains in the atlas, with small-sample failure panels discussed explicitly. If the compiled pages remain readable, use the existing small/moderate/large triptychs instead; do not shrink 27 panels onto one portrait page.

For each focused comparison, use complete matched sets for the factor being examined. If a full set needs several pages, split it by alphabet size or sample group. Do not remove a regime because it contradicts the surrounding prose. Final page allocation may expand the results chapter within its working range.

### Standard figure specification

Every panel contains Normal Wald and Expanded Welch. Use the established blue solid circles and magenta dashed squares, distinguishable in greyscale by marker and line style. Keep rejection axes at 0-1 for the primary comparisons and include the 0.05 reference line. Provide a separately labelled 0-0.1 calibration zoom where needed.

Use actual |Delta| in nats on linear axes. Keep the same horizontal limits within a comparison family. For different effect magnitudes, use explicitly labelled separate figure families rather than compressing tiny effects into an unreadable corner or returning to the old M/e scaling. Plot the actual numerical intervals, not equally spaced categories. Curves stop at tested points; connecting segments are visual guides, not additional simulations.

Every figure should have the following self-contained specification in its caption or immediately below it:

| Field | Required information |
| --- | --- |
| Horizontal graph regime specifications | Exact sample sizes or factor values for the columns, written as an explicit ordered set. |
| Vertical graph regime specifications | Actual P and Q row/column vectors for each row, or the vector formula with all parameters and dimensions specified locally. |
| Fixed population settings | Table size, baseline MI, changed cells or constructor, and which population has greater MI. |
| Axes | Actual MI differences and units, or the n ladder for convergence; rejection denominator and range. |
| Uncertainty and validity | Meaning of intervals and hollow markers; number of replicates. |

State the two methods and alpha once in the chapter introduction and use a shared legend. Do not add repetitive "Methods" and "Test and significance level" rows to every specification table. Do not refer to another subsection for the actual P/Q margins.

In the thesis, rates can usually use three or four decimal places; show percentage-point differences where clearer. Small target values must remain distinguishable. Keep full precision in the saved sources. Clearly label rounded probability-table examples so tiny rounding errors in displayed margins are not mistaken for the constructed inputs.

### Required figure and table groups

| Group | Purpose and data source |
| --- | --- |
| Shared-statistic diagram and worked table | Connect the population, count table, estimate, standard error and alternative references. Verify with the implementation. |
| Population construction diagram | Show the independence table, signed change block and resulting fixed pair. Use saved population definitions. |
| Main landscape | `display_manifest.csv`, section `main`, joined to `cell_results.csv`. |
| Matched focused figures | Sections `baseline`, `patterns`, `imbalance`, `broad_effect`, `rectangular`, `construction`. |
| Boundary and convergence figures | Sections `extreme`, `rare_stress`, `independence`, `convergence`; include validity and explicit null-only sample-size axes where appropriate. |
| Numerical method comparisons | `paired_method_results.csv`, accompanied by the corresponding null behaviour and validity. |
| Runtime table | `runtime_summary.csv`, with exact regime, median, IQR and relative cost. |
| Complete supplementary atlas | All display sections, retaining individual regimes and the display-to-configuration map. |

Create a machine-readable source manifest for each thesis figure/table: identifier, source files, filtering rule, configuration IDs, labels, denominator and generating command. Generated numerical prose or LaTeX macros should prevent repeated values from drifting across chapters.

## 9. Evidence already available for the new argument

The following values were checked against the saved per-method records during this planning review. They are anchors for the argument, not instructions to select only these panels. All rates below are unconditional and use alpha=0.05.

| Observation | Exact scope or identifier | Interpretation to preserve |
| --- | --- | --- |
| In 36 main null settings with n in {5,10,20}, Expanded Welch is numerically closer to 0.05 in 26; Wald in 10. | Main first-block design, all four square shapes and three profiles. | Mixed finite-sample behaviour; this count does not establish 26 statistically significant improvements or satisfactory calibration. |
| Wald is closer in all 24 main null settings with n in {500,1000}. | Same main design. | Evidence against a universal replacement, restricted to these populations and sample sizes. |
| For uniform 8x8, n=20 and I(P)=I(Q)=0.02, rejection is 0.06870 for Wald and 0.05695 for Expanded Welch; both valid rates are 1. | `config_313a5e5c05280f9e` | A calibration improvement with fully valid calculations. |
| For uniform 2x2, n=1000 and I(P)=I(Q)=0.02, rejection is 0.04450 for Wald and 0.03865 for Expanded Welch; both valid rates are 1. | `config_700945d218841f2e` | The correction moves an already conservative estimate farther below nominal. |
| The largest main alternative rejection gap is 0.30865: Wald 0.30865, Expanded Welch 0, with valid rates 0.83840 and 0.31415. | `config_e9b5baebbe3f5535`: 8x8, different-skew margins, n_P=n_Q=5, I(P)=0.02 and I(Q)=0.021. | This is not a clean measure of power sacrificed for equivalent calibration. It combines low validity, a threshold change and potentially liberal baseline behaviour. Show the matched null before interpreting it. |
| At equal MI=0.02 and n=50,000, Wald rates range 0.04700-0.05265 and Expanded Welch 0.04655-0.05255. | First-block convergence, four square shapes and all three profiles. | Agreement with nominal calibration over these fixed populations at this sample size. |
| At equal MI=0.0001 and n=50,000, Wald rates range 0.00890-0.02795 and Expanded Welch 0.00755-0.01380. | Same first-block convergence subset; does not include the additional rare-block subset. | Very small positive MI remains difficult despite large samples. |
| The median Expanded/Wald runtime ratio across 60 timing regimes is approximately 1.75, with ratios approximately 1.72-1.79. | Saved scalar runtime experiment. | Same O(rc) order, a measured constant-factor cost on this implementation and machine. |

The current source and result records support these scoped observations. Claims about the causes of all failures, optimality across all tests, or application-wide operating thresholds require additional evidence and must not be inferred from them.

## 10. Appendices and supplementary material

| Appendix | Content |
| --- | --- |
| A. Derivation details | Complete variance-influence algebra, derivative checks and the relationship between component and combined degrees of freedom. |
| B. Population construction | Marginal formulas, change matrices, feasibility bounds, target-solving algorithm and numerical tolerances; reference full-precision population tables. |
| C. Additional experiments and diagnostics | Full sample ladders and matched focused comparisons, validity and paired rates; an index into the companion atlas rather than thousands of printed CSV rows. |
| D. Independence boundary | Why I=0 implies zero population first-order MI variance, the separately labelled first and second Taylor terms, and the relation of 2n I-hat to the classical G-test reference under its regular large-sample conditions. |
| E. Reproducibility | Protocol, unique/configuration display counts, source hashes, commands, environment, tests, source-to-figure manifest and runtime protocol. |

The independence appendix should explain the scope of the proposed test, not claim that setting the Q terms to zero turns Expanded Welch into the G-test. Distinguish the statistic G from its chi-squared reference, and keep the main chapter's boundary explanation concise.

Only include an additional exploratory-method appendix if its evidence is actually discussed in the main text. Do not import old oracle diagnostics as validation of a deployable test or imply that LR was run in the final comparison.

## 11. Writing sequence and deliverables

The experiment is complete. The next work is evidence organisation, drafting and verification; a new large simulation is not a prerequisite for writing.

| Stage | Concrete work | Completion criterion |
| --- | --- | --- |
| 1. Preserve and prepare | Preserve the previous manuscript as an explicitly named archive when the rewrite starts; establish the active bibliography, notation and dedicated final-run figure paths. | The old version remains recoverable, and the new draft cannot silently resolve an old result figure. |
| 2. Create the evidence export | Build the figure/table manifest and exports from `results/thesis_redesign/`; join by configuration IDs and preserve method-specific denominators. | Every planned empirical claim and figure points to exact saved rows. |
| 3. Draft the experiment chapters | Write Chapter 5 from the frozen protocol, then Chapter 6 from the exported evidence, using the same order of questions. | A reader can interpret every main panel without earlier chat or undocumented settings. |
| 4. Draft and reconcile the mathematics | Revise Chapters 3-4 and Appendices A/D; verify the worked examples, bias correction, signs, derivatives, reference assumptions and validity rules against code. | The described method reproduces the implemented calculation, with approximations labelled. |
| 5. Refresh the literature and draft Chapter 2 | Read original methodological sources, check bibliography details, document the construction adaptation and verify the novelty boundary. | Every substantive literature claim has a checked source; no citation is retained merely because it appeared in the old draft. |
| 6. Write the argument around the evidence | Draft Chapters 1, 7 and 8, then the abstract. | Each question has an answer supported by the methods or results; no unsupported claim of superiority remains. |
| 7. Assemble and edit | Compile the full thesis, adjust panel sizes, check notation and repeated parameters, and remove redundant prose. | Equations, captions and tables are readable at the final page size; references resolve. |
| 8. Final audit | Recalculate numerical statements from saved rows; verify links, bibliography, figure manifests and required administrative details. | The abstract, discussion and conclusion agree with the actual final evidence and its limits. |

The first substantive drafting milestone should be a complete experimental design chapter and a readable results landscape, accompanied by the method chapter outline. These now determine the thesis argument more strongly than the previous favourable summary did. Mathematical writing and literature verification can then proceed without holding up the empirical draft.

Routine formatting, export and explanation decisions do not need another supervisor approval round. If a specific verification exposes a scientific ambiguity, perform the smallest useful diagnostic and document it separately. A change to the method or experimental protocol would need a clearly labelled new analysis, not an overwrite of the frozen evidence.

## 12. Checks specific to this rewrite

1. **Numerical traceability:** regenerate values from the final CSVs; distinguish target MI from achieved MI; keep the sign conversion explicit; do not double-count reused configurations.
2. **Fair interpretation:** assess the null point, alternatives and validity together; use paired uncertainty; do not call fewer rejections inherently better or invalid outputs true negatives.
3. **Mathematical precision:** distinguish sample independence from within-population independence, V from V/n, a working Student reference from an exact law, and finite-alphabet asymptotics from growing-alphabet claims.
4. **Construction precision:** show both populations' margins, the actual changed cells, the fixed target solve and finite feasible ranges; do not equate equal MI with equal joint distributions.
5. **Scope:** make clear that the final comparison has two methods and one alpha; empirical coverage, extra thresholds and LR results are not silently added from older runs.
6. **Readability:** use the exemplar notes, explicit Taylor terms and self-contained figure specifications; remove M/e scaling and redundant jargon from the current experiment description.
7. **Provenance:** retain the original run metadata. It records 99 primary figures; the later report metadata records seven additional calibration zooms. Cite source hashes as well as the recorded revision, because a revision alone need not identify the full working state used in a run.
8. **Submission details:** confirm the required degree wording, declaration, formatting and any acknowledgements against the applicable course material. The supplied Honours template provides no basis to assert current Master's requirements.

The completed plan should lead to a thesis whose main achievement is an understandable derivation and a reproducible, balanced evaluation of when its proposed correction is useful. The conclusions should follow the evidence visible in the individual regimes.
