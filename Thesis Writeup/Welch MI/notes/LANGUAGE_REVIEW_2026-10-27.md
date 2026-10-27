# Whole-thesis language review — 27 October 2026

The current thesis is predominantly clear and coherent. The useful next pass is a set of local edits: name statistical quantities precisely, make calibration settings unambiguous, keep claims within their evidence, and remove occasional repetition. The detailed derivations and the construction explanation in Section 5.1 should retain their teaching depth.

This review read the active manuscript sentence by sentence, including headings, captions, table wording and the labels of the eight included figures. Findings below appear in manuscript order and include source locations, reasons, proposed wording and dependencies. A sentence left unflagged was considered in its surrounding paragraph; it is not an instruction to rewrite that sentence. The recommendations are contextual editorial judgements, not authorship detection.

**Status:** review only. No manuscript, plot, PDF, delivery package or historical draft was changed. No LaTeX or packaging build was run. All line references identify the source reviewed on this date, not the older October 21 prose review.

## How to use the review

- **P1 — statistical scope/precision (12):** wording can blur an approximation, its object or the strength of the evidence. Resolve these first.
- **P2 — reader clarity (27):** wording creates avoidable ambiguity, delayed explanation or decoding work.
- **P3 — optional refinement (11):** useful tightening or consistency; lower priority than protecting the argument and readable derivations.

There are **50 findings**, several covering repeated wording or linked labels. This is not a count of incorrect sentences. Some findings replace a short passage or address a dependency elsewhere.

Keep the current abstract. Preserve the Section 2.3 algebra, Chapter 4’s sensitivity derivation and worked example, Section 5.1’s copying construction, the common benchmark denominators, the separation of population predictions from sample-based predictions, and the independent fitting/evaluation distinction. Keep the complete distribution names already used consistently. Do not restore the fixed-reference testing arm or removed sample-size comparator.

Preserve equations, numerical results and citation-supported scientific claims when editing for style; B07 concerns citation placement, not removing the literature connection. A02 identifies one explicit approximation marker needed in a prose moment statement; K04 identifies an assumption already present in Chapter 4 that should also appear in the concluding scope. Neither changes the scientific method.

## Coverage and retained material

| Material | Review decision |
| --- | --- |
| Title page, metadata and acknowledgements | Retain. Conventional, concise and appropriate; no invented personal detail or new title needed. |
| Abstract | Retain. The current version motivates the comparison, identifies the contribution and gives the qualified findings without restoring a detailed results inventory. |
| Chapter 1 — Introduction | Read all sentences, research questions and contribution items. Preserve the equal-MI versus equal-distribution distinction; tighten repetition, calibration motivation and the practical contribution. |
| Chapter 2 — Background and literature | Read all sentences and equation explanations. Preserve Section 2.3’s general Taylor formula, explicit substitution, reindexing, cancellations and observation-level variance derivation. Retain the bootstrap/permutation distinction; identify only the scope clarification in B03 within Section 2.3. |
| Chapter 3 — Statistic and Wald baseline | Read all prose, assumptions and definitions. Retain the sampling assumptions, declared categories, zero-cell explanation, correction and shared-statistic construction. Two local refinements are recorded. |
| Chapter 4 — Expanded Welch derivation | Read every explanation beside the moment matching, perturbation derivatives, conditional means, mean-zero argument, linearisation and worked example. Retain the mathematical teaching detail and theoretical-status paragraph. Two optional local refinements are recorded. |
| Chapter 5 — Experimental design | Read all construction explanations, parameter tables, research-question sections and calibration steps. Preserve the copying example and the lower/upper-null table. Main refinement: distinguish a calibration setting from an individual population. |
| Chapter 6 — Results | Read every result paragraph, caption, table description and application interpretation. Retain numerical evidence, consistent benchmark denominators, split plot rows and the two application questions. Prioritise variance terminology, inclusion rules and scope of diagnostic explanations. |
| Chapter 7 — Conclusions | Read all RQ findings, limitations and future work. Preserve the squared-mean mechanism and cutoff/bias distinction. Clarify the target of the derived approximation, scope of power gains and the additional positive-sensitivity assumption. |
| Appendix A — Near-independence calculations | Read both derivations and their interpretation. Preserve all intermediate algebra, fixed-margin conditions and quadratic terms. Clarify approximate G moments and the status of nI(P). |
| Appendix B — Experimental details | Read all eight sections, parameter sets, eligibility rules, inclusion rules, uncertainty and calibration procedures. Preserve substantive construction and uncertainty details. Clarify fitting repetitions, positivity wording and the existing FO notation alias. |
| Appendix C — Additional results | Read all supporting-result descriptions, application-family definition and Holm procedure. Clarify the proposed variance correction, centring/correlation labels and signed power differences. |
| Included generated tables | Read all 13 included table sources and the two included macro-definition files. Numeric entries were used to check nearby language, without recalculating the experiment. Abbreviations and setting labels have grouped findings. |
| Included figure labels | Extracted and read the text of all eight figures actually included in the thesis. Current main legends do not contain the obsolete A.4 labels. The lower-panel “Valid” label is the remaining wording refinement. |

The [coverage ledger](LANGUAGE_REVIEW_COVERAGE_2026-10-27.tsv) groups the reviewed source into 418 contiguous blocks so equations and their explanatory sentences stay together. It is a source-coverage index, not an automatically inferred sentence count. “Retain” means no local edit is proposed; a cross-file dependency in a finding can still apply. [Structured findings and SHA-256 fingerprints](LANGUAGE_REVIEW_2026-10-27.json) record the exact source and PDFs reviewed.

## Detailed findings


### Chapter 1

#### I01 · P2 · Keep the equal-MI distinction without stating it twice

Location: [chapters_rewrite/01_introduction.tex:18](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/01_introduction.tex:18>).

Current:

> Under \(H_0\), the populations have equal MI. However, this does not mean that their joint probability tables are the same, as two populations can have equal MI while having different probability tables.

Reason: The second clause repeats the first. The distinction itself is essential and should stay.

Proposed:

Under \(H_0\), the populations have equal MI even though their joint probability tables may differ.

#### I02 · P2 · Name the variance estimate used by the standard error

Location: [chapters_rewrite/01_introduction.tex:47](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/01_introduction.tex:47>).

Current:

> Choosing its degrees of freedom requires estimating how much the MI variance estimates change from sample to sample.

Reason: “MI variance estimates” can mean an estimated variance of MI or the sampling variance of that estimate. This is the first explanation of the second layer of uncertainty.

Proposed:

Choosing its degrees of freedom requires estimating how much the variance estimates used in the standard error change between samples.

Context/dependencies: In the next two sentences, use “pointwise MI values” for the cell-level logarithms, rather than the less specific “MI values”. Keep the explanation that changing a cell changes its margins.

#### I03 · P2 · Explain calibration when first introducing it

Location: [chapters_rewrite/01_introduction.tex:59](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/01_introduction.tex:59>).

Current:

> The evaluation measures the resulting false-positive rates and nominal power, then compares power after matching rejection at specified equal-MI populations through independent simulation. Changing the calibration population checks whether the resulting power comparison is stable.

Reason: “Matching rejection” leaves the quantity and target unstated. “Calibration population” then appears before calibration has been explained.

Proposed:

The evaluation measures false-positive rates and power under the usual cutoffs. It then adjusts each test’s cutoff using independent equal-MI simulations to target a 5\% false-positive rate before comparing power. Repeating this calibration at a different common MI checks whether the power comparison changes.

Context/dependencies: Keep the fuller fitting and independent validation procedure in Chapter 5. Use the terminology decision in D01 consistently.

#### I04 · P1 · Describe a first-order sensitivity rather than an exact finite change

Location: [chapters_rewrite/01_introduction.tex:84](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/01_introduction.tex:84>).

Current:

> The thesis derives how changing one observation affects the estimated MI variance, including the resulting changes in the row and column totals and in pointwise MI.

Reason: The contribution is an exact derivative used in a first-order approximation. “How changing one observation affects” can suggest an exact formula for replacing a whole observation.

Proposed:

The thesis derives the first-order effect of an observation on the estimated MI variance, accounting for changes in the row and column totals and in pointwise MI.

Context/dependencies: Keep the exact derivative/approximate sampling-error distinction in Chapter 4; no equation change is proposed.

#### I05 · P2 · Split the practical contribution into parallel claims

Location: [chapters_rewrite/01_introduction.tex:104](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/01_introduction.tex:104>).

Current:

> The evaluation identifies selected populations at common MI 0.02 nats where Expanded Welch brings false-positive rates closer to 5\% than Normal Wald, the dependence of calibrated power on the fitting population, and estimation errors that make both tests unreliable.

Reason: The verb “identifies” governs populations, a dependence and errors in one long list. Those objects require the reader to reconstruct the sentence.

Proposed:

At common MI 0.02 nats, the evaluation identifies settings where Expanded Welch brings false-positive rates closer to 5\% than Normal Wald. It also shows how calibrated power depends on the setting used to fit the cutoffs and how errors in the shared estimates can make both tests unreliable.

Context/dependencies: Avoid duplicating the empirical contribution’s full parameter list.


### Chapter 2

#### B01 · P2 · Use the stated positive-cell assumption instead of undefined support shorthand

Location: [chapters_rewrite/02_background_literature.tex:123](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:123>).

Current:

> For a fixed positive \(r\times c\) support,

Reason: “Positive support” is compressed terminology. Here the intended condition is a fixed table whose population cell probabilities are all positive.

Proposed:

For a fixed \(r\times c\) population table with positive cell probabilities,

#### B02 · P1 · Remove a misleading contrast with plug-in estimation

Location: [chapters_rewrite/02_background_literature.tex:164](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:164>).

Current:

> Bayesian estimators model the unknown probabilities rather than treating observed proportions as the complete population.

Reason: The plug-in estimator substitutes empirical probabilities; it does not assert that the sample is the complete population. The present contrast understates the other approach.

Proposed:

Bayesian estimators place a probability distribution on the unknown cell probabilities.

Context/dependencies: The following explanation of priors can remain; it develops what that distribution does.

#### B03 · P1 · Limit the chi-squared statement to the likelihood-ratio approximation

Location: [chapters_rewrite/02_background_literature.tex:475](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:475>).

Current:

> Testing independence therefore uses a chi-squared distribution rather than the normal approximation for comparing positive MI values.

Reason: Independence can also be tested by other procedures. The derivation establishes the chi-squared limiting distribution for the usual likelihood-ratio statistic, not a requirement for every independence test.

Proposed:

The usual likelihood-ratio test of independence therefore uses a chi-squared limiting distribution, while the first-order normal approximation for positive MI degenerates at independence.

Context/dependencies: This is in Section 2.3, which local instructions protect from unsolicited revision. It is a narrowly identified scope clarification for review; retain all its algebra and teaching steps.

#### B04 · P2 · Distinguish the two variances directly

Location: [chapters_rewrite/02_background_literature.tex:574](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:574>).

Current:

> The estimate \(\Vhat(P)/n_P\) describes the expected spread of an MI estimate across samples. The variability of \(\Vhat(P)\) describes how much that assessment of spread itself changes across samples.

Reason: “Expected spread” can mean either variance or standard deviation, and “assessment of spread itself” adds another verbal layer at the point where the distinction matters.

Proposed:

\(\Vhat(P)/n_P\) estimates the sampling variance of \(\Ihat(P)\). In contrast, \(\Var\{\Vhat(P)\}\) measures how much \(\Vhat(P)\) itself changes between samples.

Context/dependencies: Keep the following explanation of equal means, different variability and the moment-matching cutoff. This replacement belongs in Section 2.4, not the protected derivation.

#### B05 · P2 · Replace a compressed historical label with the actual operation

Location: [chapters_rewrite/02_background_literature.tex:619](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:619>).

Current:

> Hutcheson's test is a direct information-theoretic Welch predecessor.

Reason: The stacked label does not say what Hutcheson compares; the following sentence provides that explanation.

Proposed:

Hutcheson applies a Welch-type comparison to two estimates of Shannon diversity.

Context/dependencies: Merge with the following sentence so “compares two Shannon diversity estimates” is not repeated. Preserve the formula and citation.

#### B06 · P1 · Describe a precedent without implying general validity

Location: [chapters_rewrite/02_background_literature.tex:636](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:636>).

Current:

> The entropy comparison establishes that a Student \(t\) distribution can be used to compare estimated information quantities, but MI requires more than substituting a different numerator.

Reason: An entropy test supplies a precedent. It does not establish the validity of a Student t approximation for information estimators generally. The “different numerator” phrase also obscures the linked entropy errors explained next.

Proposed:

Hutcheson’s test provides a precedent for comparing information estimates using a Student \(t\) distribution. Applying this approach to MI requires accounting for the linked errors in its joint and marginal entropy estimates.

Context/dependencies: Keep the next cell-count explanation. Remove any immediately repeated statement that MI combines those same entropies only if it adds no mechanism.

#### B07 · P3 · Keep the scientific connection instead of publication-status commentary

Location: [chapters_rewrite/02_background_literature.tex:650](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:650>).

Current:

> Their later peer-reviewed account places the MI index within the segregation literature \citep{mora2011}.

Reason: The publication status does not help explain the MI comparison. The earlier sentence already provides the relevant methodological precedent.

Proposed:

Omit this sentence; retain the 2011 citation beside the segregation-literature claim if it supports that claim.

Context/dependencies: Check citation placement rather than deleting the reference automatically.

#### B08 · P2 · Name what is paired in the bootstrap

Location: [chapters_rewrite/02_background_literature.tex:666](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:666>).

Current:

> and the MI difference recalculated for each pair.

Reason: “Pair” could refer to an observation (X,Y), populations, tables or method decisions.

Proposed:

and the MI difference recalculated from each pair of resampled count tables.


### Chapter 3

#### M01 · P3 · Present units separately from statistical assumptions

Location: [chapters_rewrite/03_problem_baselines.tex:66](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:66>).

Current:

> \begin{assumption}[Logarithm units]

Reason: The block itself correctly says this is a choice of units. Labelling it an assumption creates an unnecessary conceptual contradiction.

Proposed:

Present the existing paragraph under the miniheading “Logarithm units” rather than as an assumption.

Context/dependencies: Preserve all wording about nats and invariance. Check assumption numbering and references if the environment is changed; do not renumber manually in prose.

#### M02 · P2 · Identify both component estimates

Location: [chapters_rewrite/03_problem_baselines.tex:178](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:178>).

Current:

> Expanded Welch uses the variability of that variance estimate to choose a Student \(t\) distribution instead.

Reason: “That variance estimate” follows a sentence about the standard error and can refer either to its square or to the individual V-hat terms. The derivation that follows uses their component sampling moments.

Proposed:

Expanded Welch uses the sampling variability of \(\Vhat(P)\) and \(\Vhat(Q)\) to choose the degrees of freedom of a Student \(t\) distribution.


### Chapter 4

#### E01 · P3 · Place the plug-in cancellation beside its empirical use

Location: [chapters_rewrite/04_expanded_welch.tex:368](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:368>).

Current:

> This weighted cancellation also holds after exact plug-in substitution.

Reason: The empirical sensitivities are introduced later in this section. This preview interrupts the population mean-zero argument before the reader needs it.

Proposed:

Move this point to the paragraph introducing \(\widehat\tau^2(P)\): “The empirical sensitivities also have probability-weighted mean zero under exact substitution; the displayed variance centres them explicitly.”

Context/dependencies: Keep the probability-weighted mean-zero proof and the centred empirical formula unchanged. Do not add a second proof.

#### E02 · P3 · Use an explicit noun and verb for the plug-in calculation

Location: [chapters_rewrite/04_expanded_welch.tex:403](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:403>).

Current:

> The plug-in \(\Vhat(P)\) applies the variance calculation to this empirical table.

Reason: “The plug-in V-hat” is grammatically awkward and makes the calculation sound like an operator.

Proposed:

The plug-in estimate \(\Vhat(P)\) evaluates \(V\) at this empirical table.


### Chapter 5

#### D01 · P2 · Use “calibration setting” for a specification of both populations

Location: [chapters_rewrite/05_experimental_design.tex:348](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:348>).

Current:

> To examine how that choice affects the power comparison, we repeat calibration at \(h=2\) and \(h=4\) for A--C using the two null populations in Table~\ref{tab:design-calibration-populations}.

Reason: Each lower or upper null specifies both P and Q. Calling these “two null populations” can make the reader think they are P and Q themselves.

Proposed:

To examine how that choice affects power, we repeat calibration for A--C at \(h=2\) and \(h=4\), using the lower and upper equal-MI settings in Table~\ref{tab:design-calibration-populations}.

Context/dependencies: Use “lower-null setting”, “upper-null setting” or “setting used to fit the cutoffs” in the corresponding Chapter 6, conclusion and appendix passages. Reserve “population P” and “population Q” for the individual joint distributions. Retain actual population terminology where a single table is intended.

#### D02 · P3 · Use a table heading that includes the alternative

Location: [chapters_rewrite/05_experimental_design.tex:363](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:363>).

Current:

> Calibration case & \(I(P)\) & \(I(Q)\)

Reason: The first row is a fixed alternative, so it is not itself a calibration case.

Proposed:

Scenario & \(I(P)\) & \(I(Q)\)

#### D03 · P3 · Remove a repeated supplement signpost

Location: [chapters_rewrite/05_experimental_design.tex:380](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:380>).

Current:

> The experimental supplement reports broader MI differences from 0 to 0.2 nats at \(n=1{,}000\) and 10,000, and a separate sample-allocation analysis. The experimental supplement specifies those additional settings.

Reason: The second sentence adds no scientific information.

Proposed:

The experimental supplement specifies the broader comparison over MI differences from 0 to 0.2 nats at \(n=1{,}000\) and 10,000, together with a separate sample-allocation analysis.


### Chapter 6

#### R01 · P1 · Distinguish simulation checks from an application without known truth

Location: [chapters_rewrite/06_results.tex:7](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:7>).

Current:

> Supporting simulations and the online shopping application examine how the findings extend to other settings.

Reason: The application illustrates the outputs but cannot establish rejection behaviour because its population MI values are unknown. This opening gives the application the same evidential role as supporting simulations.

Proposed:

Supporting simulations examine additional settings, and the online-shopping application illustrates interpretation of the test outputs.

Context/dependencies: The conclusion already makes this distinction clearly; retain that explanation.

#### R02 · P2 · Identify the simulated estimate of the expectation

Location: [chapters_rewrite/06_results.tex:59](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:59>).

Current:

> The top row divides \(\E\{\Vhat(P)\}\) by the population benchmark \(V(P)\), and likewise for \(Q\).

Reason: The plotted numerator is an empirical mean used to estimate the expectation. The mathematical target and its Monte Carlo estimate should not silently become the same object.

Proposed:

The top row divides the simulated mean of \(\Vhat(P)\) by the population benchmark \(V(P)\), and likewise for \(Q\).

Context/dependencies: Keep the expectation symbol in the axis label; the body explains how it is estimated. No new symbol is needed.

#### R03 · P2 · Keep the direction of error tied to the example

Location: [chapters_rewrite/06_results.tex:91](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:91>).

Current:

> The population calculation therefore underestimates variation, whereas the sample-based calculation overestimates it.

Reason: The preceding values describe one setting; this final sentence can sound like a universal property of the two calculations.

Proposed:

At this setting, the population prediction underestimates \(\Var\{\Vhat(P)\}\), while the average sample-based prediction overestimates it.

#### R04 · P2 · State which benchmark defines “too few”

Location: [chapters_rewrite/06_results.tex:118](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:118>).

Current:

> Ratios below one mean too few degrees of freedom; ratios above one mean too many.

Reason: The benchmark is a sampling-moment target. It is not a degree-of-freedom value proven to calibrate T exactly.

Proposed:

Ratios below one indicate fewer degrees of freedom than the moment target; ratios above one indicate more.

Context/dependencies: Keep the later single sentence explaining that matching moments does not guarantee an exact Student t distribution. Do not repeat that qualification after every plot.

#### R05 · P2 · Make the plotted inclusion rule explicit

Location: [chapters_rewrite/06_results.tex:119](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:119>).

Current:

> Bottom-row curves require all component estimates to be positive and finite.

Reason: “All component estimates” can mean both components in one repetition or every repetition for the component being plotted. Appendix B specifies the latter condition for these mean curves.

Proposed:

A bottom-row value is shown only when that component’s estimate is positive and finite in all 100,000 repetitions.

Context/dependencies: Confirm that this matches the plot mask when implementing; do not substitute a conditional mean or silently change which points are shown. Appendix B already distinguishes conditional summaries.

#### R06 · P3 · Avoid implying that the preceding RQ1 simulations used unequal MI

Location: [chapters_rewrite/06_results.tex:229](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:229>).

Current:

> We now set \(I(P)=I(Q)\), so every rejection is a false positive.

Reason: RQ1 also used equal-MI grids. The scientific transition is from approximation accuracy to rejection rates.

Proposed:

Under \(I(P)=I(Q)\), every rejection is a false positive. We now compare how often the two tests reject.

#### R12 · P2 · Label the validity panels as fractions

Location: [chapters_rewrite/06_results.tex:283](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:283>).

Current:

> \includegraphics[width=\textwidth]{focused_redesign_null_uniform.pdf}

Reason: The embedded axes say “Valid”, which names a property rather than the plotted quantity. Their values are fractions between zero and one.

Proposed:

Use “Valid fraction” on the lower panels of both main false-positive figures.

Context/dependencies: Change the active plotting template in WelchSatterthwaiteMI/experiments/redesign_report.py and update only the corresponding current figures when figure edits are authorized. Do not revive older A.4 legends or supplementary figures that are no longer included in the thesis.

#### R07 · P1 · Describe estimation errors without claiming a causal separation

Location: [chapters_rewrite/06_results.tex:305](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:305>).

Current:

> These diagnostics distinguish a shifted estimated difference from an inaccurate standard error.

Reason: The summaries measure mean error and average variance error. They do not isolate each error’s contribution to rejection, and changes between margin regimes change more than bias alone.

Proposed:

These diagnostics measure bias in \(\Deltahat\) and average error in \(\SEhat^2\), both of which can affect rejection.

Context/dependencies: Also replace “The matched populations distinguish rejection driven by a large difference bias from conservative behaviour when that bias cancels” with “In the different-skew case, large difference bias accompanies excessive rejection; in the same-skew case, that bias cancels and both tests are conservative.” Retain the mechanism and numeric evidence. Appendix B already states the causal limitation once.

#### R08 · P1 · Report the squared-standard-error quantity actually assessed

Location: [chapters_rewrite/06_results.tex:333](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:333>).

Current:

> At A, difference bias is negligible, but \(\SEhat\) understates the variation of \(\Deltahat\).

Reason: The table compares mean squared SE with the observed variance. That is not a direct comparison of the mean SE with the observed SD.

Proposed:

At A, difference bias is negligible, but the average \(\SEhat^2\) is below the observed \(\Var(\Deltahat)\).

Context/dependencies: Use the same precise comparison in the corresponding Chapter 7 explanation. The plain-language consequence can follow: “The estimated uncertainty is too small on average.”

#### R09 · P2 · Anchor B’s power explanation to its sampling mean along the alternatives

Location: [chapters_rewrite/06_results.tex:420](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:420>).

Current:

> As \(I(Q)\) increases, the true signed difference becomes negative, initially offsetting the positive estimation bias observed under the null. The estimated difference moves towards zero, reducing \(|T|\) and rejection before the curve rises.

Reason: The mechanism is supported by the saved alternative-path diagnostics. The current paragraph refers only to bias under the null and says that “the estimated difference” moves, without identifying its sampling mean. It should connect the available evidence explicitly and avoid attributing the whole rate change to the mean alone.

Proposed:

At B, positive estimation bias persists at the first alternatives. As \(I(Q)\) increases, the negative true difference partly offsets this bias, moving the sampling mean of \(\Deltahat\) towards zero. This movement helps explain the initial fall in rejection. A larger cutoff leaves the estimated difference and standard error unchanged.

Context/dependencies: Read-only evidence check: focus.csv and diagnostics.csv in results/approximation_redesign give mean Delta-hat approximately +0.056712 at h=0, +0.023695 at h=0.5 and -0.007704 at h=1. Bias remains positive; the variance ratio also changes. Retain the direct mechanism with this scope in Chapter 7 and the calibrated-power paragraph; avoid repeating the full explanation three times. The numbers need not all be added to the manuscript.

#### R10 · P3 · Define the paired comparison once

Location: [chapters_rewrite/06_results.tex:434](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:434>).

Current:

> Each interval uses both methods' decisions from the same simulation repetitions to estimate their power difference. These are paired comparisons: the pairing is between methods applied to the same data.

Reason: Two consecutive sentences explain the same pairing. Retain the explicit subjects because “paired” was a genuine source of confusion.

Proposed:

The intervals account for both tests being applied to the same two sampled count tables in each repetition.

#### R11 · P2 · Name the uncertainty that lowers the weekend degrees of freedom

Location: [chapters_rewrite/06_results.tex:649](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:649>).

Current:

> Expanded Welch's 2.18 degrees of freedom for weekend reflect substantial estimated sampling uncertainty relative to the sizes of \(\Vhat(P)\) and \(\Vhat(Q)\), even with large samples

Reason: “Sampling uncertainty” could mean the uncertainty of the MI difference, the standard error or the variance estimates. Here the degrees of freedom concern the estimated variance components relative to their squared means.

Proposed:

For weekend, the estimated variability of the variance components is large relative to their squared means, giving Expanded Welch only 2.18 degrees of freedom despite the large samples

Context/dependencies: Keep the reference to the near-independence diagnostic. Do not imply that simulation results establish the unknown application population’s moment target.


### Chapter 7

#### K01 · P2 · Name the target of the concluding variance statement

Location: [chapters_rewrite/07_conclusions.tex:10](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/07_conclusions.tex:10>).

Current:

> The variance of this sensitivity gives a first-order sampling-variance approximation, which is used with moment matching to choose MI-specific degrees of freedom for a Student \(t\) distribution.

Reason: The sentence omits what the sampling-variance approximation is for. This is the central mathematical contribution and deserves an explicit object.

Proposed:

The variance of this sensitivity gives the first-order approximation \(\Var\{\Vhat(P)\}\approx\tau^2(P)/n_P\). Moment matching then uses this approximation to choose MI-specific degrees of freedom for a Student \(t\) distribution.

#### K02 · P2 · Lead the RQ1 conclusion with the finding

Location: [chapters_rewrite/07_conclusions.tex:16](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/07_conclusions.tex:16>).

Current:

> The mean and sampling variance of \(\Vhat(P)\) need separate checks. The predicted sampling variance can be close to its observed value while the mean estimate remains above \(V(P)\).

Reason: The opening describes how to assess the approximation before stating the result. “Mean estimate” can also mean an estimator of the mean instead of the sampling mean of V-hat.

Proposed:

The predicted sampling variance of \(\Vhat(P)\) can be close to its observed value even when the sampling mean \(\E\{\Vhat(P)\}\) remains above \(V(P)\).

Context/dependencies: In the following explanation, “sampling mean” is clearer than “inflated sampling mean”. Keep the squared-mean mechanism and population/sample distinction.

#### K03 · P1 · Attach calibrated power gains to the alternatives being compared

Location: [chapters_rewrite/07_conclusions.tex:71](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/07_conclusions.tex:71>).

Current:

> At common MI 0.02 nats, Expanded Welch gains power over Wald at A and B.

Reason: The common MI identifies the calibration null, not the alternatives. The sentence can sound like a gain across every point on both curves; both curves include the null and B is nonmonotone.

Proposed:

After calibration at common MI 0.02 nats, Expanded Welch has higher power at the reported two- and four-null-SD alternatives for A and B.

Context/dependencies: Keep the following reversals at A/2 and B/4 and the table citation. Those identify the alternative and the changed calibration separately.

#### K04 · P1 · Include the additional regularity condition used by Expanded Welch

Location: [chapters_rewrite/07_conclusions.tex:100](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/07_conclusions.tex:100>).

Current:

> The derivation assumes independent categorical observations, fixed categories, positive population cell probabilities and positive first-order MI variance.

Reason: Chapter 4 explicitly also requires positive variance sensitivity tau-squared. Positive V alone does not guarantee it, as Chapter 4 explains.

Proposed:

The derivation assumes independent categorical observations, fixed categories, positive population cell probabilities, and positive \(V(P)\), \(V(Q)\), \(\tau^2(P)\) and \(\tau^2(Q)\).

Context/dependencies: The surrounding discussion already explains independence and higher-order behaviour. A cross-reference to the regular-sensitivity assumption can identify tau-squared without repeating its derivation.


### Appendix A

#### A01 · P1 · Keep nI(P) labelled as a local approximation

Location: [appendices_rewrite/A_derivation_details.tex:218](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/A_derivation_details.tex:218>).

Current:

> even when the population value \(nI(P)\) is very small.

Reason: nI(P) is the near-independence first-order approximation to component degrees of freedom, not the exact population moment target.

Proposed:

even when the population first-order approximation \(nI(P)\) is very small.

#### A02 · P1 · State that the G moments come from the approximating distribution

Location: [appendices_rewrite/A_derivation_details.tex:222](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/A_derivation_details.tex:222>).

Current:

> Since \(\E(G)=d+\kappa\) and \(\Var(G)=2(d+2\kappa)\),

Reason: G was defined as the finite-sample likelihood-ratio statistic and only given an approximate noncentral chi-squared distribution. Its moments should not suddenly be presented as exact finite-sample identities.

Proposed:

Under the noncentral chi-squared approximation, \(\E(G)\approx d+\kappa\) and \(\Var(G)\approx2(d+2\kappa)\). Hence

Context/dependencies: Only the scope of the G-moment statement changes. The subsequent approximations and numerical predictions remain unchanged; retain the displayed derivation.


### Appendix B

#### X01 · P2 · Identify the fitting units

Location: [appendices_rewrite/B_population_construction.tex:134](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/B_population_construction.tex:134>).

Current:

> Independently generate another 100,000 pairs for each equal-MI fitting setting for the focused power comparison.

Reason: “Pairs” is undefined at this point and could mean categorical observations.

Proposed:

For each equal-MI fitting setting in the focused power comparison, independently generate another 100,000 repetitions, each producing one count table from \(P\) and one from \(Q\).

Context/dependencies: The existing paragraph already defines evaluation repetitions. A shorter acceptable version is “Generate a separate 100,000-repetition fitting batch for each focused equal-MI setting.”

#### X03 · P3 · Make the existing notation equivalence explicit

Location: [appendices_rewrite/B_population_construction.tex:307](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/B_population_construction.tex:307>).

Current:

> The subscript FO identifies the population first-order formula from Chapter~\ref{chap:expanded}.

Reason: The main chapters use nu-P for the first-order formula, while this appendix adds nu-P,FO. Both are understandable locally, but the reader should not have to infer their equivalence.

Proposed:

\(\nu_{P,\mathrm{FO}}\) is the population first-order value denoted by \(\nu_P\) in the main results.

Context/dependencies: Prefer this one equivalence sentence over a thesis-wide symbol replacement. Keep the distinct sampling-moment target and sample-based estimate.

#### X02 · P1 · Distinguish a required assumption from a verified population property

Location: [appendices_rewrite/B_population_construction.tex:315](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/B_population_construction.tex:315>).

Current:

> The assumptions in Chapter~\ref{chap:expanded} ensure positive population variance quantities for the tested populations.

Reason: Assumptions specify which populations the argument covers. They do not, by themselves, verify positivity in every constructed population.

Proposed:

For populations satisfying the assumptions in Chapter~\ref{chap:expanded}, both \(V(P)\) and \(\tau^2(P)\) are positive.

Context/dependencies: If the sentence is intended to report an actual check of all constructed populations, state that check explicitly and retain its evidence in the experiment record. This language review does not assert a failed positivity check.


### Appendix C

#### C01 · P2 · Identify which estimator a proposed 9/n correction would change

Location: [appendices_rewrite/C_additional_results.tex:16](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:16>).

Current:

> The coefficient suggested near independence is \((k-1)^2=9\). Variation in the observed scaled error leaves residual mean error under a fixed \(9/n\) correction.

Reason: The main thesis also subtracts a leading bias correction from MI. A second “correction” without an explicit target can be confused with that existing correction.

Proposed:

Near independence, Appendix~\ref{sec:independence-boundary} predicts \(\E\{\Vhat(P)\}-V(P)\approx9/n\) for these \(4\times4\) tables. The observed scaled errors vary, so subtracting \(9/n\) from \(\Vhat(P)\) would leave residual mean error.

Context/dependencies: Keep this as a diagnostic of a possible variance-estimator correction, not a change to the estimator actually used in the thesis.

#### C02 · P2 · Say what centres the difference in the dependence diagnostic

Location: [appendices_rewrite/C_additional_results.tex:45](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:45>).

Current:

> Rank corr. is Spearman's correlation between the absolute centred difference and its standard error,

Reason: “Centred” could mean subtracting zero, the true Delta or the observed sampling mean. The reporting code uses the observed sampling mean.

Proposed:

“Rank corr.” is Spearman’s correlation between \(|\Deltahat-\operatorname{mean}(\Deltahat)|\) and \(\SEhat\),

Context/dependencies: The reporting calculation was inspected: report_calibration_sensitivity.py subtracts delta.mean() before taking the absolute value. Keep the existing finite-value inclusion rule. In the next example, replace “signed correlation about -0.001” with “Pearson correlation between Delta-hat and SE-hat about -0.001”; identify the 0.547 value as the rank correlation between the centred magnitude and SE-hat. redesign_study.py uses np.corrcoef for the signed statistic. Preserve both figures.

#### C03 · P2 · Explain the shape statistic instead of repeating its column label

Location: [appendices_rewrite/C_additional_results.tex:47](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:47>).

Current:

> Skew describes the difference estimates.

Reason: The current sentence does not explain what “Skew” measures or what its sign means.

Proposed:

“Skew” is the skewness of \(\Deltahat\); positive values indicate a longer right tail and negative values a longer left tail.

Context/dependencies: Use “Skewness” in the generated header if space permits. Keep this short definition near the table.

#### C04 · P2 · Name the direction and quantity in the power contrast

Location: [appendices_rewrite/C_additional_results.tex:103](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:103>).

Current:

> gives the Wald contrasts with intervals.

Reason: “Wald contrasts” does not specify which method is subtracted or that the quantity is power.

Proposed:

gives Expanded Welch minus Normal Wald power differences with their intervals.

Context/dependencies: Also add “power” to the caption “Expanded Welch minus Normal Wald at two null SDs, in percentage points.” The signed direction is already consistent in the data.

#### C05 · P3 · Remove an ambiguous pronoun in the Holm algorithm

Location: [appendices_rewrite/C_additional_results.tex:196](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:196>).

Current:

> replace any value below the preceding adjusted value by that value,

Reason: Two different values appear before “that value”. This is easy to make explicit without adding a formula.

Proposed:

replace any value below the preceding adjusted value with the preceding adjusted value,


### Generated table wording

#### T01 · P2 · Expand compressed setting labels consistently

Location: [figures_rewrite/focused_redesign_cases_rates.tex:8](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/figures_rewrite/focused_redesign_cases_rates.tex:8>).

Current:

> 16, same, 1,000

Reason: The first number is the number of categories, not an MI value or sample size, and “same” abbreviates a margin regime. The legend forces the reader to decode three fields.

Proposed:

Use \(16\times16\), same skew, \(n=1{,}000\), with the analogous labels for the other sparse cases.

Context/dependencies: Apply to cases_rates, cases_diagnostics and component_spread; the latter also needs its P/Q component identified. Change the reporter templates rather than only generated tables. Use line breaks or clearer separate columns if needed; do not shrink the table text to accommodate the expanded wording.

#### T02 · P2 · Use the defined effect-size symbol in calibration tables

Location: [figures_rewrite/focused_redesign_calibration_sensitivity.tex:3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/figures_rewrite/focused_redesign_calibration_sensitivity.tex:3>).

Current:

> Setting: SD & Upper MI

Reason: “Setting: SD” can be mistaken for an estimated standard deviation. The number is h, the number of fitted null SDs separating the alternative MI values.

Proposed:

Use “Setting, \(h\)” and “Upper-null MI (nats)”.

Context/dependencies: Apply the same h convention to sensitivity_power_full and sensitivity_cross_null. Keep lower/upper fitting and evaluation nulls distinct. Define pp as percentage points in the adjacent body or table header; it is already explained in the Chapter 6 paragraph.

#### T03 · P2 · Distinguish combined degrees of freedom from component summaries

Location: [figures_rewrite/focused_redesign_cases_diagnostics.tex:3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/figures_rewrite/focused_redesign_cases_diagnostics.tex:3>).

Current:

> Setting & Bias/SD & Est./obs. var. & Rank corr. & Skew & Median df

Reason: “Median df” has different objects across the component and shared-estimator tables. This table reports combined Expanded Welch degrees of freedom.

Proposed:

Use “Median combined df” here, “Skewness” for the shape statistic, and explicitly define df as degrees of freedom once beside the first abbreviated table.

Context/dependencies: The component-spread table should say “component df” in its caption or header; its existing caption already does. Preserve the numeric values and use a wrapped header if necessary.

#### T04 · P3 · Expand a one-off table abbreviation

Location: [figures_rewrite/focused_redesign_null_sd_fitting.tex:3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/figures_rewrite/focused_redesign_null_sd_fitting.tex:3>).

Current:

> Setting & Null SD (nats) & MCSE (nats)

Reason: MCSE is not explicitly introduced as an abbreviation. “Monte Carlo SE” is readable and short enough for a wrapped header.

Proposed:

Setting & Null SD (nats) & Monte Carlo SE (nats)

Context/dependencies: Keep the body definition of Monte Carlo standard error. This is a label refinement, not a change to its calculation.

## Rules for an eventual editing pass

1. Apply P1 edits with the corresponding design, results, conclusion and appendix passages open together. Preserve the signs, numerator/denominator directions, units and denominators of reported rates.
2. Use “population P” and “population Q” for individual distributions, “sampled count tables” for repetition outputs, and “calibration setting” for a lower/upper-null specification of both populations. Use “paired method comparison” only when its pairing is defined.
3. State whether a variance is V(P), Var(V-hat(P)), the observed variance of Delta-hat or a mean squared standard error. Keep plain-language explanations beside symbols where the distinction is first taught.
4. Keep direct explanations when supported. For B’s power mechanism, use the saved alternative-path mean diagnostics identified in R09. They support the movement towards zero; they do not isolate each error’s causal contribution to rejection. Never strengthen a causal assertion merely to make the prose sound confident.
5. Update active reporter templates along with generated labels, without touching historical/supplementary displays. No experiment rerun is needed for label or language edits.
6. Re-read each edited paragraph with its equation/figure and the next paragraph. Preserve connected prose and varied sentence lengths; do not split every qualified sentence or add a stock transition.
7. Check source formatting without building if needed. Keep flush-left paragraphs and existing figure typography. Wait for an explicit request before rebuilding the PDF or refreshing delivery packages.

## Verification of this review

All ten active chapter/appendix files, the abstract and remaining front matter, included table sources and included figure labels were covered. The current input graph was obtained from main.tex and its active includes. Historical sources and unused plots were excluded from recommendations. Bibliography titles and author names were preserved; this was a language review, not a fresh literature or numerical-validation audit.

The structured record fingerprints the reviewed manuscript inputs, eight included figure PDFs and both current thesis PDFs. Review files live under notes/ and are the only new project artifacts from this task. Unrelated Finder metadata changes were left alone.
