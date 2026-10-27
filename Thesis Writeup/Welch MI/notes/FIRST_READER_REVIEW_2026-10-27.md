# First-reader comprehension review — 27 October 2026

Yes: a reader new to MI testing is likely to stop and backtrack at several important transitions, especially in Chapters 4 and 6. Most individual sentences are understandable. The larger difficulty is maintaining the relationship between the quantities and recognising which question each calculation answers.

For this pass, I assumed basic calculus and probability, including expectations, variances and elementary conditional probabilities. I did not assume previous knowledge of MI tests, influence functions, Welch–Satterthwaite moment matching or empirical power calibration. I followed the manuscript in reading order and distinguished a concept explained at its point of use from one whose purpose becomes clear only later. These are editorial predictions about a first reader, not observations from a reader study.

This record supplements the earlier sentence-level language review. It gives higher priority to missing conceptual links than to optional copyedits. No manuscript, equations, figures, PDF or delivery files have been changed.

## The main comprehension breaks

### N01 — Some basic testing language arrives before its meaning

**Priority: Moderate.** Locations: [Section 2.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:123>); [Section 3.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:166>).

**Likely reader question:** “What exactly is bias, and what probability does this p-value represent?”

**What the text already provides:** The introduction explains false positives and power. Section 2.3 derives a sampling variance, and Chapter 3 defines the statistic and normal distribution function.

**Where the reader may get stuck:** Bias is used before an explicit definition of E(estimate) minus the population value. The p-value is given as a CDF expression without a plain-language interpretation of the two tails. The word “standard error” is also used before its relationship to sampling standard deviation is stated directly. A reader who has studied probability but little inference must supply these connections.

**Recommended repair:** Give each term one short explanation when it becomes operational: bias as average estimation error; standard error as an estimate of the sampling SD; the two-sided p-value as the probability, under the reference distribution for equal MI, of a statistic at least as extreme in either direction. Connect the factor two to the two symmetric tails. Keep these explanations in the body rather than expanding the abstract.

### N02 — A zero-mean linear error can appear to contradict the earlier bias correction

**Priority: Moderate.** Locations: [Section 2.3, centred contributions](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:401>).

**Likely reader question:** “We just showed that the MI error has mean zero. Why did we previously say the estimator is biased?”

**What the text already provides:** Section 2.3 carefully labels the expansion as first order, and its ending explains that the leading bias shrinks faster than the sampling error.

**Where the reader may get stuck:** At the mean-zero calculation, the reader must remember that a discarded higher-order part of the estimation error can have a nonzero mean. “First order” alone does not explain how the displayed zero mean and the positive bias formula coexist.

**Recommended repair:** A brief explanation can connect them: the linear part has mean zero; the omitted higher-order terms generate the leading bias discussed in Section 2.2. The existing Taylor derivation should remain intact. Section 2.3 is protected by the local writing instructions; record this narrow explanatory proposal for a specifically authorised edit rather than rewriting the derivation.

### N03 — The second layer of uncertainty needs a concrete introduction

**Priority: High.** Locations: [Section 2.4](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:573>); [Section 3.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:116>); [Section 6.1 table](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:26>).

**Likely reader question:** “Are we studying how the MI estimate varies, or how its variance estimate varies? What is being averaged over?”

**What the text already provides:** The individual formulas are defined. Section 2.4 discusses variance size and stability, Chapter 4 derives the extra variability, and Chapter 6 supplies a useful quantity table.

**Where the reader may get stuck:** The reader must coordinate variation across observation outcomes, variation across sampled tables, and uncertainty in the estimate of that variation. The most compact table distinguishing these objects appears only in Chapter 6, after they have already carried the derivation. Section 4.5 also calls tau-squared the “variance sensitivity”, although g-P is the sensitivity and tau-squared is its variance; that change of noun can send the reader back to its definition.

**Recommended repair:** Introduce a compact distinction around Sections 3.2–4.1: \(V(P)\) describes variation of pointwise MI across outcomes; \(\Vhat(P)/n_P\) estimates the sampling variance of \(\Ihat(P)\); \(\Var\{\Vhat(P)\}\) describes changes in the variance coefficient across repeated tables. State that Expanded Welch needs this extra layer to choose its cutoff. Introduce \(\tau^2(P)\) only when its sensitivity definition is available. Relocate or streamline the existing Chapter 6 table instead of duplicating a full glossary. Keep the sensitivity g-P distinct from its variance tau-squared in the prose.

### N04 — Moment matching does not by itself explain why a Student t distribution appears

**Priority: High.** Locations: [Section 2.4](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:523>); [Section 4.1](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:45>).

**Likely reader question:** “I can follow the chi-squared mean and variance calculation. How does that lead to a Student t reference for T?”

**What the text already provides:** The normal/t density figure explains the heavier tails. Section 4.1 shows every important moment-matching step, and Section 4.5 correctly describes the resulting test as an approximation.

**Where the reader may get stuck:** The familiar construction of a Student t variable from a normal numerator and an independent scaled chi-squared denominator is assumed rather than explained. A reader can reproduce the algebra without understanding why it is useful for testing.

**Recommended repair:** Briefly state the standard construction, \(Z/\sqrt{U/\nu}\), for independent standard normal \(Z\) and chi-squared \(U\) with \(\nu\) degrees of freedom. Explain that matching the estimated variance to a scaled chi-squared variable motivates the t approximation here. Keep clear that the required independence and distributional identities are not exact properties of the MI statistic. Also describe \(\nu\) as a positive tail-shape parameter that can be noninteger. This can be one compact explanatory unit rather than a new derivation.

### N05 — The purpose of perturbing one population cell is explained late

**Priority: High.** Locations: [Section 4.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:101>); [Section 4.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:393>).

**Likely reader question:** “We need variability between random samples. Why are we now moving a small amount of probability into an imagined cell?”

**What the text already provides:** The perturbation path and point-mass table are defined clearly. Section 4.3 eventually shows that the empirical-table error averages these one-observation directions.

**Where the reader may get stuck:** That last fact is the reason for choosing the path, but it appears after a substantial derivative calculation. The reader may need to return to the start of Section 4.2 once Section 4.3 reveals the purpose.

**Recommended repair:** After defining the perturbation, explain that it isolates an observation’s first-order contribution to table error, and that averaging these contributions will give the repeated-sample variance. Keep the full averaging identity and proof in Section 4.3. Give the reason early without moving all the later algebra forward.

### N06 — Three degrees-of-freedom quantities need stable identities

**Priority: High.** Locations: [Section 4.1 moment target](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:88>); [Section 5.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:200>); [Section 6.1.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:104>).

**Likely reader question:** “Is this the degrees of freedom used by the test, the theoretical approximation to it, or the simulation benchmark? Why would their means differ?”

**What the text already provides:** The later design and results distinguish the sampling-moment target, population first-order value and sampled estimate. All three have definitions.

**Where the reader may get stuck:** In Chapter 4, \(\nu_P\) first denotes the exact moment-matching expression and then appears in an approximate first-order formula. Later the moment target becomes \(\nu_{P,\mathrm{mom}}\), while \(\nu_P\) denotes the first-order value. Appendix B adds \(\nu_{P,\mathrm{FO}}\). A first reader must reconstruct the change in roles. It is also easy to assume that averaging the sampled estimate must recover the moment target, although an average of a nonlinear ratio need not equal a ratio of sampling moments.

**Recommended repair:** Establish three roles when they first become distinct: the benchmark defined by the actual sampling moments, the population first-order approximation to that benchmark, and the estimate calculated from one observed table. Use a compact table showing which inputs each uses and which one changes between repetitions. Keep their notation stable through the results and appendices. Explain the nonlinear-average distinction briefly. A note that fixed division by n leaves the moment-matched degrees of freedom unchanged would also explain why the derivation matches V-hat before combining V-hat/n. This is more substantial than the one alias sentence suggested in X03 of the earlier language review; any notation edit needs a complete dependency check.

### N07 — “Quadratic sampling terms” needs an immediate mechanism in the main text

**Priority: High.** Locations: [Section 4.5](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:649>); [Section 6.1.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:178>); [Appendix A.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/A_derivation_details.tex:183>).

**Likely reader question:** “Why should a second-order term become important? Why can the first-order degrees of freedom approach zero while the estimates remain around five?”

**What the text already provides:** The main text says the first-order change vanishes and sampling noise creates apparent MI. Appendix A gives the full quadratic and noncentral chi-squared calculations, including the approximately half-target estimated degrees of freedom near independence.

**Where the reader may get stuck:** The main results move quickly from “quadratic terms” to several numerical curves. A reader may understand the sentence yet have no usable picture of the omitted contribution. Obtaining that picture currently invites a long excursion into the appendix’s more advanced asymptotics.

**Recommended repair:** Connect the existing first-order error formula to the mechanism: its cell-error weights are pointwise MI values, which vanish at independence; quadratic cell-error terms can then remain as the leading source of variation. Explain that population MI can be near zero while sampled tables retain noise-induced association. Keep the full noncentral chi-squared argument in Appendix A, with a short main-text account of the consequence for the estimated degrees of freedom. Avoid describing the problem only as “the first-order approximation breaks down”.

### N08 — Calibration creates an apparent reversal of the earlier nesting result

**Priority: High.** Locations: [Section 4.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:523>); [Section 5.4](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:340>); [Section 6.3.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:440>).

**Likely reader question:** “Expanded Welch was said to reject only when Wald rejects. How can it now have higher power on the same data?”

**What the text already provides:** The calibration procedure is explained in steps, and the text says the two tests can rank samples differently because the estimated degrees of freedom change. The lower/upper-null table is helpful.

**Where the reader may get stuck:** The text does not explicitly tie the nesting result to using the same nominal p-value threshold. After calibration the thresholds differ between methods, so that earlier implication no longer applies. “Orders samples” also introduces a new meaning of “samples”: ranking complete simulated datasets, not rearranging observations within one dataset.

**Recommended repair:** State this connection beside the calibrated comparison: the earlier nesting applies at a common p-value threshold; calibration fits different thresholds, and dataset-dependent degrees of freedom can change which repetitions are most significant. Say “ranks simulated datasets by evidence against equal MI”. Explain once that calibration uses known null settings to compare simulated power; it does not give a ready-made threshold for an arbitrary observed population. Preserve the existing lower/upper-null table and independent validation steps.

### N09 — Sample size and number of repetitions have different jobs

**Priority: Moderate.** Locations: [Section 5.5](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:389>).

**Likely reader question:** “With 100,000 repetitions, why are there still small-sample problems or uncertain variance estimates?”

**What the text already provides:** The text defines an observation, a repetition and the population sample sizes separately. The interval paragraph says the intervals describe finite-simulation uncertainty.

**Where the reader may get stuck:** The distinction is technically available, but readers may still conflate many simulations with a large sample inside each test. The bootstrap adds a third count of repeated operations.

**Recommended repair:** One sentence can state that increasing simulation repetitions improves the precision of reported rates, while the test in each repetition still uses only n-P and n-Q observations. Leave the bootstrap repetition count in the uncertainty procedure where it belongs. No new table or lengthy simulation tutorial is needed.

### N10 — RQ1 and RQ2 assess different variance benchmarks

**Priority: High.** Locations: [Section 6.1.1](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:78>); [Section 6.2.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:299>).

**Likely reader question:** “If the estimated MI variance is too large in RQ1, how can the standard error be too small in RQ2?”

**What the text already provides:** All the ratios are defined, and the Chapter 6 quantity table records the approximate link between V(P)/n and the variance of MI.

**Where the reader may get stuck:** RQ1 compares \(\Vhat(P)\) with \(V(P)\) and studies the sampling variability of \(\Vhat(P)\) for degrees of freedom. RQ2 compares \(\SEhat^2\) with the actual finite-sample sampling variance of \(\Deltahat\). Because \(V(P)/n_P\) is itself a first-order approximation, agreement with V(P), or bias relative to it, does not settle whether the standard error accurately describes the difference. The reader has to recover that approximation chain to reconcile the results.

**Recommended repair:** At the transition, state the new question explicitly: “The test also requires \(\SEhat^2\) to describe the sampling variance of \(\Deltahat\). We assess this by comparing its average with the observed variance of the estimated difference.” Keep the RQ1 and RQ2 benchmark roles visible. Read-only evidence confirms the distinction matters in this study: at A under equal MI, mean V-hat(P)/V(P) is about 4.73, while mean SE-hat-squared/observed Var(Delta-hat) is 0.827. These measure different errors and are consistent; the manuscript need not add both numbers merely to explain the distinction.

### N11 — The meaning of better false-positive calibration needs a plain motivation

**Priority: Moderate.** Locations: [Section 5.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:260>); [Section 6.2.1](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:244>).

**Likely reader question:** “False positives are mistakes. Why would reducing them below 5% count as worse? Could an invalid test look better just by failing more often?”

**What the text already provides:** The revised classification rule clearly defines changes in distance from 5%, and validity fractions are reported beside rejection rates. Chapter 4 says an invalid output is not evidence for the null.

**Where the reader may get stuck:** The motivation for the nonzero calibration target is still mostly assumed. The counting rule for invalid results is explicit, but its consequence for interpreting lower rates is not developed at the figure’s point of use.

**Recommended repair:** Explain that a rule which never rejects has zero false positives and zero power. Here closeness to 5% describes nominal calibration under the stated comparison criterion, with power assessed separately; a rate below 5% is conservative and is not, by itself, an invalid test. Before interpreting validity panels, explain that unusable outputs can also lower the all-repetition rejection rate. Keep these explanations brief and avoid presenting every below-5% result as intrinsically worse in every scientific sense.

## Places where the existing explanation works

- **Chapter 1’s basic question:** the reader can identify X and Y, populations P and Q, and the distinction between equal MI and identical distributions.
- **Section 2.1:** the pointwise-MI ratio is connected to independence before it is averaged into MI. The margins and nested sums are explained.
- **Section 2.3’s algebra:** the general Taylor formula, mapping of its arguments, cancellation of constant terms, observation-level average and division by n can be followed in sequence. Preserve these steps.
- **Chapter 4’s worked example:** the same count-table cell is followed through pointwise MI, V-hat and the sensitivity calculation. This supplies useful continuity.
- **Section 5.1:** the copying mechanism is introduced through a sampling story, then translated into cell probabilities and a concrete table. The mathematical construction follows a question the reader already understands.
- **The effect-size example in Section 5.4:** sigma-zero and h are defined before the numerical example at C. Keep this example.
- **The lower/upper-null table:** it makes clear which MI values change while the alternative stays fixed. Preserve it while clarifying “calibration setting”.
- **Section 6.2.2’s bias-shift equation:** the true difference plus bias gives an intelligible account of a shifted estimate. A general identity E(Delta-hat) = Delta + Bias(Delta-hat), near the first definition of bias, would make this and the later power interpretation easier to connect.
- **Section 6.4:** the two questions and the X/Y/P/Q table prepare the reader before the count-table details and test results. This is a useful model for other sections.
- **Chapter 7:** the RQ structure keeps the findings together. The reader is likely to struggle here mainly if the earlier conceptual distinctions have not been established.

## Appendix reading and smaller prerequisite issues

Appendix A.1 follows calculus steps explicitly. Appendix A.2 becomes substantially more advanced at its local-alternative, noncentral chi-squared result. The citation can serve as an accepted standard result, but verifying that result requires asymptotic-statistics knowledge beyond basic calculus and probability. Explain its consequence in the main text as in N07; do not force the reader to verify the full theorem to understand the figure.

Appendix B’s population construction, grids, validity rules and diagnostic denominators are operationally specified. Its uncertainty section assumes familiarity with the delta method. A short identification of the differentiated function, 2 mu-squared/v, would connect the coefficients to the Taylor-expansion method already taught in Chapter 2; a full new derivation is lower priority. The joint bootstrap is also technical, but can remain procedural in the appendix once the main text explains which sources of uncertainty it includes.

The zero-component discussion records an implemented choice even though the simplified combined formula can remain defined. A reader seeking a mathematical necessity for excluding every such case will not find one in that passage. Describe it as the operational validity rule and provide a substantive rationale if available; do not change the rule or its results merely to smooth the explanation.

Other smaller pauses include “fixed positive support”, the first O(n^-2) remainder, “Shannon diversity” without explicitly identifying entropy, “moment” before naming mean and variance, and compressed table labels such as “Setting: SD”. Most need a few words at first use. The reader need not master every Bayesian estimator in the literature review; those paragraphs should communicate each method’s relevance without becoming prerequisites for the proposed test.

## Recommended priority

First address N03–N06, N08 and N10: the layers of uncertainty, why t moment matching is used, why the perturbation is taken, the three degrees-of-freedom roles, and the benchmark/threshold changes between results. These are likely to cause substantial backtracking because later claims depend on them.

Then add the brief connections in N01, N02, N07, N09 and N11 where needed. Prefer moving an existing useful explanation earlier, replacing an abstract sentence with its mechanism, or adding a compact quantity table. Do not expand every paragraph or repeat the full explanation each time a symbol returns. The goal is to let each new calculation answer a question already established for the reader.

No broad chapter reordering or experiment rerun is indicated by this reading assessment. This pass identifies explanatory dependencies. Its recommendations should be reconciled with the earlier 50 language findings before implementation; they are not instructions to apply all proposed wording mechanically.

## Review record

Reviewed the active introduction, background, statistic, derivation, design, results, conclusion and three appendices for sentence-level comprehension and reading order, checking the later location of missing explanations. The abstract was assessed as a research summary rather than a tutorial. Included table/figure wording had been reviewed in the preceding pass and its input fingerprints still match. Used two saved diagnostic summaries to check the example in N10; no simulations were run.

All 31 manuscript-source fingerprints, eight included figure fingerprints and the two current thesis PDF fingerprints still match the earlier language review. Only this internal review note was added. No build or package refresh was run.
