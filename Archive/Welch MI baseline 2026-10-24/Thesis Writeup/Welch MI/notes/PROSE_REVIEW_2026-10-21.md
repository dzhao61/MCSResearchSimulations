# Thesis prose review — 21 October 2026

## Scope and overall judgement

I read all eight active chapters and all three appendices, including their figure captions and surrounding table explanations. I also checked the acknowledgements, title material and generated table headings. The recently revised abstract is outside this review. Locations below refer to the LaTeX source at the time of review, not an archived draft. No manuscript or delivery files were changed for this review.

Subsequent edits: Appendix C was shortened later on 21 October 2026, then its complete null-results table and two full-range power plots were moved to the experiment supplement. The exploratory-dataset descriptions were condensed and Chapter 6's references updated. Notes concerning Appendix C and Chapter 6 describe the text before those edits; their line numbers are no longer current. The other manuscript sources were unchanged in these passes.

“AI-sounding” here describes a reading problem, not evidence about who wrote a passage. The useful questions are whether the prose says something concrete, whether the explanation follows, and whether the reader has to reconstruct the intended meaning.

The strongest problems are **repetition, compressed summaries and writing about the argument instead of making it**. There is relatively little flamboyant vocabulary. The thesis more often sounds mechanically assembled because it repeatedly announces a comparison, lists several findings and ends by saying that those findings “distinguish” something or “show” that performance depends on several quantities. Some passages also compress a setting into a string such as “the sparse 16 × 16 different-skew 0.01-nat alternative.” The terminology is legitimate; the sentence construction makes it difficult to read.

The mathematics should not be shortened indiscriminately. Section 2.3 is a particularly useful model: it names the quantity being calculated, shows the transformations and explains the cancellations. Much of Chapter 4 and Appendix A has the same strength. Their length is usually doing explanatory work. The most substantial restructuring is needed in Chapters 1, 5, 7 and 8, and in Chapter 6's supporting-check discussion.

## How to use the notes

There are **69 review notes: 13 high, 38 medium and 18 low priority**. Several notes concern different occurrences of the same pattern; they are not 69 equally serious defects. Start with the high-priority passages rather than applying every suggested deletion mechanically.

- **High:** restructure or rewrite before making sentence-level edits. These passages most strongly resemble the problem raised about the abstract, or their framing can obscure the statistical argument.
- **Medium:** a specific clarity, transition, emphasis or repetition problem worth fixing.
- **Low:** optional polish. These passages are understandable and are not strong evidence of an artificial voice on their own.

Examples of replacement wording illustrate the intended direction; they are not approved manuscript edits. Equations, numerical evidence, citations, assumptions and scientific qualifications should survive a later revision. Where the issue is excessive numerical narration, move secondary values to the existing tables or appendix rather than discard evidence from the thesis.

| Area | Notes | High-priority notes |
| --- | --- | --- |
| Chapter 1: Introduction | R01–R05 | R03 |
| Chapter 2: Background and literature | R06–R13 | R09 |
| Chapter 3: Test and Wald baseline | R14–R17 | R17 |
| Chapter 4: Expanded Welch derivation | R18–R25 | R25 |
| Chapter 5: Experimental design | R26–R33 | R27 |
| Chapter 6: Results and application | R34–R48 | R34, R37, R43 |
| Chapter 7: Implications and limitations | R49–R54 | R49, R52, R53 |
| Chapter 8: Conclusion | R55–R60 | R55, R57 |
| Appendix A: Supporting calculations | R61 | — |
| Appendix B: Experimental details | R62–R63 | — |
| Appendix C: Additional results | R64–R68 | — |
| Acknowledgements | R69 | — |

## Patterns across the thesis

1. **The contribution is introduced too many times.** Chapter 1, lines 45–53 and 80–108; Chapter 2, lines 558–575, 595–603, 625–639 and 683–705; Chapter 3, lines 177–195; Chapter 4, lines 4–10; and Chapter 8, lines 6–16 all explain the variance sensitivity, the degrees of freedom and the retained Wald statistic. Each occurrence has a local purpose, but the cumulative effect is repetitive. Keep a short motivation in Chapter 1, a synthesis of the literature gap at the end of Chapter 2, and the full construction in Chapter 4. Use shorter links elsewhere.
2. **Some paragraph endings merely repackage the preceding evidence.** Examples include “This identifies where…”, “These comparisons distinguish…”, “Allocation therefore changes…” and “would extend the practical reach…”. Keep an ending when it explains a mechanism or establishes a necessary inference. Remove it when it only puts an abstract label on facts already stated.
3. **Setting descriptions become strings of modifiers.** “Matched,” “same-skew,” “different-skew,” “sparse,” table size, sample size and effect size often precede the actual subject. State the setting in one sentence and the result in the next. Use the defined regime names consistently; do not invent more shorthand to solve this problem.
4. **Several passages perform too many jobs.** The most difficult paragraphs combine a result, a comparison between constructions, a validity qualification, a limitation and a recommendation. Split at the change in scientific question, not at an arbitrary sentence count.
5. **The experimental design is narrated repeatedly.** Chapter 5 provides an opening overview, three study descriptions, an overview table and then another set of detailed descriptions. Chapter 6 and Appendix C sometimes repeat the same result and interpretation at similar length. Keep full settings in the methods and appendix, the main explanation in the results, and implications in the discussion.
6. **Difficult quantities sometimes receive vague names just when the distinction matters most.** “Uncertainty,” “variability,” “estimation diagnostics,” “the approximation” and “performance” can refer to different objects. Name the MI difference, its sampling variance, the estimated variance or the sampling variance of that estimate as appropriate. Do not replace every precise term with a shorter synonym.
7. **Scientific qualifications and defensive framing are mixed together.** Positive cell probabilities, the independence boundary, the validity denominator and the unmeasured small-sample power cost are necessary. Phrases that simply announce that a comparison does not cover everything can often be shortened. Preserve the actual condition and its consequence.

## Chapter 1 — Introduction

Source: [01_introduction.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/01_introduction.tex>).

### R01 — The equal-MI distinction is stated twice in one sentence block

**Priority: Medium. Location: lines 18–20.**

> “this does not mean that their joint probability tables are the same, as two populations can have equal MI while having different probability tables.”

The second clause repeats the first rather than explaining it. This is a clear example of prose growing without adding meaning.

**Suggested action:** retain the important distinction in one sentence: “Equal MI does not require identical joint probability tables.” If an example is needed, explain how different margins or association patterns can produce equal MI; do not restate the distinction.

### R02 — The method preview carries too much of the later derivation

**Priority: Medium. Location: lines 45–53.**

> “requires estimating how much the MI variance estimates change from sample to sample”

The paragraph moves from the reference distribution to variability of a variance estimate, then to cell probabilities, row and column totals, calculated MI values and back to degrees of freedom. Each statement is relevant, but their accumulation is difficult before the reader knows the variance formula. The last sentence repeats the purpose already given.

**Suggested action:** introduce the retained statistic and the change of distribution, then give one plain explanation of how the degrees of freedom are chosen. Leave the cell-and-margin mechanism for the literature review and derivation. For example: “Its degrees of freedom depend on how much the estimated MI variance changes between samples. This thesis derives an approximation to that variability.”

### R03 — Four contribution labels inflate two connected contributions

**Priority: High. Location: lines 80–108.**

> “Mathematical contribution”; “Methodological contribution”; “Empirical contribution”; “Practical contribution”

The mathematical derivation and its use in the test are parts of one contribution. The practical conclusions come from the empirical comparison. Dividing these into four labelled achievements makes the section sound promotional and formulaic. The empirical item then becomes an inventory of every check. “Additional supplementary checks” at line 100 is redundant wording.

**Suggested action:** state two substantive contributions: the derivation and resulting test, and the evaluation explaining when the test helps or fails. Keep any distinct practical finding as a finding, rather than another category of contribution. Remove the inventory of supplementary analyses from this section.

### R04 — Evaluation plans are repeated around the research questions

**Priority: Low. Location: lines 59–61 and 74–78.**

> “The evaluation therefore examines both outcomes…”
>
> “An analytical derivation addresses the first question, while controlled simulations… address the second…”

The research questions and contribution list already identify the derivation, simulations and outcomes. Several nearby previews make the introduction sound as though it is following a section template.

**Suggested action:** retain one brief link between the questions and the approach. Remove a duplicate preview rather than shortening all of them into equally terse sentences.

### R05 — Scope and roadmap have dispensable opening sentences

**Priority: Low. Location: lines 113–114 and 123–124.**

> “The scope of this thesis is the comparison of MI between two populations using categorical data.”
>
> “The organisation of the thesis follows the development, evaluation and interpretation of the two-sample MI test.”

The first repeats the opening; the second says little beyond announcing a roadmap. The category definitions, independence assumptions and chapter references that follow are useful.

**Suggested action:** begin with the fixed categories and independent samples. If a roadmap is retained, start with the chapter sequence and omit the abstract description of that sequence.

## Chapter 2 — Background and Literature Review

Source: [02_background_literature.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex>).

### R06 — The sparse-sample qualification repeats within one paragraph

**Priority: Low. Location: lines 130–134.**

> “although it does not describe every small or sparse sample”
>
> “Sparse sampling can produce further error beyond this leading approximation”

These make substantially the same qualification on either side of the citations. The limitation matters, but the double statement sounds defensive.

**Suggested action:** explain once that the leading bias term can be inaccurate when cells are poorly sampled, keeping the supporting references.

### R07 — The Bayesian contrast gives the plug-in estimator an exaggerated position

**Priority: Medium. Location: lines 164–172, especially 164–165.**

> “rather than treating observed proportions as the complete population”

The plug-in estimator substitutes observed proportions into the MI formula; using it does not itself mean claiming that they are the complete population. The contrast is rhetorically neat but less precise than a description of what the estimators calculate.

**Suggested action:** describe the Bayesian mechanism positively: it places a probability distribution over unknown cell probabilities and derives MI estimates from that model. Keep the explanation of prior strength and unobserved categories, which is concrete and helpful.

### R08 — A generic literature transition hides the actual sampling condition

**Priority: Medium. Location: lines 183–192.**

> “The sampling pattern can also suggest a more targeted estimator.”

“Sampling pattern” and “targeted” do not tell the reader which feature matters. The next sentence does: one variable is well sampled and the other has many poorly sampled categories. The closing move to two-population bias is relevant, but arrives after another paper summary without a strong connection.

**Suggested action:** lead with the unequal sampling of the two variables. Then explain the limitation relevant to this thesis: improving individual MI estimates does not by itself establish the accuracy of their difference or its standard error. Preserve the paper's actual setting rather than turning it into a general claim about all MI estimators.

### R09 — The motivation for changing the reference distribution needs a more careful inference

**Priority: High. Location: lines 510–513. Related: Chapter 3, lines 177–185.**

> “The Wald test still uses the same standard normal distribution cutoff, regardless of how much the estimated standard error varies.”

The sentence is understandable, but its framing can make a fixed normal cutoff sound wrong merely because the standard error is estimated. Both tests estimate the standard error, and the amount of variation alone does not establish that a Student t distribution is appropriate. The uncertainty in the estimated variance motivates the proposed approximation; it does not validate it.

**Suggested action:** explicitly connect variance-estimate variability to the proposal: “A Welch–Satterthwaite approximation uses this variability to choose the degrees of freedom of a Student t distribution. The simulations assess whether that change improves the MI test.” Retain the separate possibility that the MI difference itself is poorly approximated by a normal distribution.

### R10 — An important distinction is wrapped in abstract explanation

**Priority: Medium. Location: lines 566–575.**

> “the size of a variance estimate and its stability answer different questions”
>
> “how much that assessment of spread itself changes across samples”

This distinction must stay: the sampling variance of MI and the sampling variance of its variance estimate are different quantities. The “questions” and “assessment of spread” framing makes the reader translate the explanation back into the mathematics.

**Suggested action:** name the two quantities directly. For example: “V-hat(P)/n estimates the sampling variance of MI. Var{V-hat(P)} measures how much that variance estimate changes between samples. Satterthwaite's degrees of freedom decrease as the latter grows relative to the squared mean.” Keep the mean/variance relationship rather than replacing it with the vague word “stability.”

### R11 — The regression connection is described through labels rather than one clear mechanism

**Priority: Medium. Location: lines 577–588.**

> “The same principle has been used in regression…”
>
> “These regression precedents address variance estimates that are too small or confidence intervals that cover too rarely…”

The passage introduces several citations, a comparison with Pan and Wall, a return to Expanded Welch and then a general claim about intervals. “Cover too rarely” also leaves the object of coverage implicit. The connection is harder to see than it needs to be.

**Suggested action:** centre the paragraph on the specific shared calculation: choosing degrees of freedom from the variability of an estimated variance. State that the cited regression corrections address confidence intervals whose coverage of the population parameter is below the intended level. Do not imply that their success establishes the MI approximation's validity.

### R12 — The Hutcheson comparison ends in dense, abstract contribution language

**Priority: Medium. Location: lines 612–639.**

> “a direct information-theoretic Welch predecessor”
>
> “Hutcheson supplies a close comparison framework, while the cell and margin derivatives supply the MI-specific inputs.”

The opening piles descriptors onto “predecessor.” The ending replaces the concrete distinction with “framework” and “inputs.” Between them, the explanation that the three entropies share observations is useful and should stay.

**Suggested action:** open with the actual method: “Hutcheson used a Student t distribution to compare Shannon diversity estimates.” End with what the MI extension needs: an approximation to the variability of its estimated variance, including changes in pointwise MI and the margins. Avoid another full preview of Chapter 4.

### R13 — The final contribution section repeats the method more than it synthesises the literature

**Priority: Medium. Location: lines 683–705.**

> “This thesis derives how changes in the observed count table affect the estimated MI variance…”

The three paragraphs repeat material already stated in the Welch, regression and Hutcheson discussions and in Chapter 1. The final paragraph also previews empirical findings. A literature synthesis belongs here, but it need not explain the whole test again.

**Suggested action:** keep a short synthesis distinguishing the established MI bias/variance formulas from the calculation developed here. Use one sentence to identify the proposed test and one to explain why its empirical evaluation must check the shared estimates. Leave the fuller contribution statement in Chapter 1 and the actual derivation in Chapter 4.

**Retain:** Section 2.3, lines 198–472, is generally clear. The Taylor mapping, nested sums, cancellations, independence explanation and distinction between first- and second-order variation are doing necessary work. Do not remove them to make the prose seem less formal. The bootstrap/permutation discussion at lines 656–681 also makes a substantive distinction and is not merely a defensive caveat.

## Chapter 3 — The Two-Sample MI Test and Wald Baseline

Source: [03_problem_baselines.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex>).

### R14 — A formal assumption contains experimental reporting instructions

**Priority: Medium. Location: lines 52–56.**

> “Such samples remain in the study; we record how often cells have zero observed counts…”

The mathematical assumption is that population cell probabilities are positive. The distinction between a positive population cell and an observed zero is helpful, but recording zeros is part of the experiment. Mixing the two makes the assumption block read like a protocol.

**Suggested action:** keep the positivity assumption and the explanation that observed zeros remain possible. Move the reporting procedure to the sparse-sample measures in Chapter 5 or Appendix B.

### R15 — A choice of units is packaged as an assumption and then disclaimed

**Priority: Low. Location: lines 66–71.**

> “Assumption [Logarithm units]”
>
> “This is a choice of units, not a condition for the test to be valid.”

The prose has to undo the implication of its own heading. This is avoidable formal packaging rather than a mathematical difficulty.

**Suggested action:** put the natural-logarithm convention in an ordinary paragraph. Keep the invariance of the statistic under a change of units.

### R16 — The support convention ends with an unneeded hypothetical alternative

**Priority: Low. Location: lines 106–114, especially 113–114.**

> “A correction that estimates support from occupied cells would be a different estimator.”

The preceding text already specifies fixed declared categories, observed zeros and retained negative estimates. The final sentence anticipates a different method without explaining or using it.

**Suggested action:** retain the actual estimator convention and the cancellation under equal sample sizes. Remove the hypothetical alternative unless a later comparison genuinely requires it.

### R17 — “Even though” creates a weak contrast between Wald and Expanded Welch

**Priority: High. Location: lines 177–185.**

> “Wald uses the standard normal distribution at every sample size, even though its standard error is estimated…”
>
> “Neither assignment measures how cell probabilities and margins make the estimated MI variance change…”

The first sentence can suggest that estimating a standard error is itself a reason a normal approximation is inappropriate. The second can make the sample-size degrees of freedom in ordinary Welch sound like a defective calculation, although they have a specific justification for normal sample variances. The MI extension needs a different calculation because its variance estimator has a different form.

**Suggested action:** say what changes for MI: its estimated variance is not an ordinary sample variance with the same scaled chi-squared distribution. The proposed degrees of freedom use an approximation to its sampling variability. Link to Chapter 4 without restating the entire contribution.

**Retain:** the signed parameter, bias-corrected estimator, fixed-support convention and interpretation of the statistic are mostly direct. Repeating the two tests' shared statistic immediately after defining it is useful local clarification, not a passage that needs to be cut merely because the fact also appears in the introduction.

## Chapter 4 — The Expanded Welch–Satterthwaite Test for MI

Source: [04_expanded_welch.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex>).

### R18 — The opening repeats the test description and gives an unclear explanation of its name

**Priority: Low. Location: lines 4–10.**

> “The name Expanded Welch refers to this expansion of the MI variance as the table probabilities change.”

This almost defines “Expanded” with “expansion.” It does not tell the reader whether expansion means a Taylor approximation or a more elaborate method. The preceding distribution comparison has also just been made at the end of Chapter 3.

**Suggested action:** keep a short bridge. If the name needs explanation, identify the first-order expansion of the MI variance as the table probabilities change.

### R19 — A definition is introduced through commentary about introducing variables

**Priority: Low. Location: lines 29–34.**

> “The new variables being introduced are the component degrees of freedom…”

This describes the writing process instead of defining the quantities. The explanation of their statistical role is useful.

**Suggested action:** begin directly: “Here nu_P and nu_Q are the component degrees of freedom…” Then retain the explanation of relative sampling variability.

### R20 — “One observation's direction” is difficult shorthand

**Priority: Medium. Location: lines 367–381, especially 377–381.**

> “gives its first-order change for one observation's direction”

The preceding construction of delta_Z − P is concrete, but this phrase replaces it with an abstract “direction.” A reader new to influence functions must infer which direction is meant and what is changing.

**Suggested action:** explicitly connect the derivative to the probability redistribution delta_Z − P and then to the empirical average. Keep the displayed linearisation and the independence calculation; they are important derivation steps.

### R21 — The interpretation of relative variance runs into a different special case

**Priority: Medium. Location: lines 409–424.**

> “Positive V(P) does not guarantee positive tau-squared(P)…”

The relative-variance explanation is useful, but the last three lines switch to a zero-sensitivity case after the paragraph has already explained large and small degrees of freedom. The reader has to change questions without a paragraph break.

**Suggested action:** keep the interpretation together. Put the zero-sensitivity condition in a separate paragraph beside the regularity assumption or the relevant limitation. Do not delete the condition.

### R22 — A simple ordering result is mixed with implementation rules

**Priority: Medium. Location: lines 497–505.**

> “also Wald-valid… including when invalid outputs count as non-rejections…”

The paragraph combines the ordering of p-values, the nesting of valid outputs, unconditional rejection denominators and a zero-component exception. “Wald-valid” is compact internal shorthand. The main result is straightforward, but the prose makes it laborious.

**Suggested action:** first state that, on pairs for which both tests are valid, Expanded Welch cannot reject when Wald does not. Then explain separately why the implemented validity rules extend that nesting to the reported overall rates. Place the zero-component cross-reference with the validity discussion.

### R23 — The algorithm table uses specification language

**Priority: Low. Location: line 604; related headings at 591 and 598.**

> “Validate the two aligned count tables and their declared alphabet dimensions”

“Declared alphabet dimensions” is less accessible than the fixed row and column category counts already defined. “Operational algorithm” adds little to “algorithm.”

**Suggested action:** use the established category terminology. Keep the fact that independence is a sampling assumption rather than something the algorithm can verify; it can be stated in the surrounding text rather than appended to the input-check step.

### R24 — The local-expansion qualifications are repeated after the explanation

**Priority: Low. Location: lines 651–657.**

> “These local expansions assume fixed table dimensions, positive cell probabilities and the fixed-margin path.”

These conditions are necessary, but the fixed-margin path has already been introduced at lines 625–632 and the positivity conditions appear earlier. Repeating the full list at the end gives the paragraph a caution-then-cross-reference rhythm.

**Suggested action:** put the applicable conditions beside the approximation once. Preserve the distinction between the population approximation and finite-sample estimated degrees of freedom; that is the important point of this paragraph.

### R25 — “Theoretical status and validity conditions” is an omnibus section

**Priority: High. Location: lines 663–684.**

The passage covers exact derivatives, first-order sampling approximations, the scaled chi-squared approximation, the Student t approximation, dependence between numerator and denominator, asymptotic convergence, numerical eligibility and invalid outputs. These are several different questions under one heading. The progression feels like accumulated qualifications rather than an argument.

**Suggested action:** separate the approximation's theoretical status from the conditions for returning a p-value. Within the theoretical discussion, give the dependence between the MI difference and its standard error its own paragraph. Keep the approximation labels and validity criteria; reorganise them rather than weaken them.

**Retain:** the product-rule calculations, cancellation of derivative terms, completion of the square, interpretation of the two parts of g_P, and worked example are mostly clear. Instructions such as “The first sum is…” or “Substitution gives…” are appropriate when they identify a real algebraic operation.

## Chapter 5 — Experimental Design

Source: [05_experimental_design.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex>).

### R26 — The opening announces several stages before giving the defining design fact

**Priority: Medium. Location: lines 4–14.**

> “It first measures… then examines… and finally estimates…”
>
> “Bias and variance diagnostics link rejection rates to errors…”

The opening duplicates the study overview immediately below. Its clearest fact arrives last: the population tables and true MI difference are known. “Performance” and “diagnostics link” are abstract compared with that fact.

**Suggested action:** lead with simulations from known population tables, explaining that this permits direct measurement of false positives, power and estimation error. Retain the Morris framework citation in a sentence that identifies how it informs the design, rather than using the citation as the paragraph's subject.

### R27 — The three-study design is described twice, in addition to the overview table

**Priority: High. Location: lines 18–44, table at 46–62, and detailed studies at 179–292.**

The first section explains each study and both supporting checks. The later subsections explain them again with parameter values. The overview table repeats the same factors and purposes. The reader repeatedly encounters the plan instead of advancing through it.

**Suggested action:** keep a short overview and the table, then use the detailed subsections for the actual settings and reasons for choosing them. Remove the first set of full prose descriptions, or merge the overview with the detailed descriptions. Preserve all scientific settings in one clearly identified place.

### R28 — The same-skew rationale ends in abstract classification, then changes subject

**Priority: Medium. Location: lines 162–177.**

> “The two regimes therefore distinguish failures that also occur… from those observed…”
>
> “This comparison shows what happens under a common margin rule as the table grows.”

The cancellation argument is concrete and useful. The closing classification repeats the rationale without stating what is being estimated. The next paragraph moves to how increasing table size changes cell probabilities, then to two other margin comparisons. Several design questions are packed together.

**Suggested action:** keep the bias-cancellation mechanism as the reason for the same-skew comparison. Explain separately that increasing table size under the skew rule changes both the number of cells and their probabilities. Omit the broad “shows what happens” sentence.

### R29 — Some sentences justify having a sample-size range without adding a scientific reason

**Priority: Low. Location: lines 190–202, especially 201–202.**

> “The sweep includes small samples, intermediate samples and large-sample checks so that both calculation failures and convergence are visible.”

The grid and the preceding explanation already establish this. “Sweep” and “visible” give the sentence the tone of an experiment log.

**Suggested action:** remove the final restatement. Keep the important point that equal population MI does not imply equal sampling variance or estimation difficulty, and keep the distinction between low rejection and failed calculations.

### R30 — The population-MI rationale repeats obvious properties of the design

**Priority: Low. Location: lines 213–223.**

> “The two sample sizes show whether these patterns persist with more observations.”

The paragraph repeatedly says what changing MI, sample size and regime will show. The important rationale is the approach to the independence boundary and its effect on the degrees of freedom.

**Suggested action:** retain that rationale and the fact that all targets remain positive. Compress the generic sentences about patterns persisting. The overlap count at the end can sit with the complete design accounting rather than interrupt the explanation.

### R31 — The power-study rationale is too generic

**Priority: Medium. Location: lines 240–246.**

> “Small differences show where the methods may disagree; larger differences show whether power eventually becomes high.”

Almost any power study could use this sentence. The surrounding design is more specific: P is fixed, Q changes, and the null point anchors each rejection curve.

**Suggested action:** explain that the small differences reveal the practical cost of the larger cutoff and that the full range measures how detection changes as the population difference increases. Preserve the null-point comparison, since actual false-positive rates differ between the tests.

### R32 — The supporting checks are labelled like additions to a project plan

**Priority: Low. Location: headings at 248, 273 and 295; wording at 289–306.**

> “A supporting change in construction”
>
> “Both tests use their existing estimators and validity rules…”

“Supporting” and “existing” describe the status of the work rather than the scientific question. Repeated statements that settings are already included also interrupt the design narrative, although the final count of distinct settings is useful.

**Suggested action:** name the questions directly, such as “Changing the association pattern,” “Unequal sample sizes” and “Changing the bias correction.” State the common estimators and validity rules once. Keep the unique-setting accounting together and preserve the reuse of the same simulations where relevant.

### R33 — The degrees-of-freedom paragraph ends with another factor inventory

**Priority: Low. Location: lines 362–366.**

> “We examine how these summaries change with population MI, sample size, table size, construction and allocation.”

These factors have just been specified at length. The median, percentile range and valid-output denominator are the new information here.

**Suggested action:** keep the summary definitions and omit the repeated factor list.

**Retain:** the copying construction and binary example are useful explanations. The bias definition and estimated/observed variance comparison at lines 340–357 also explain mechanisms directly. Do not replace these with labels such as “estimation quality” merely to shorten the chapter.

## Chapter 6 — Experimental Results and Discussion

Source: [06_results.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex>).

### R34 — The chapter opening combines a roadmap, design recap and validity inventory

**Priority: High. Location: lines 4–19.**

The first paragraph moves through three studies, the repetition count, four lists of fully valid analyses and the small-sample exceptions. The second adds graphical conventions, parameter references and another application preview. This is a lot of administration before the first finding.

**Suggested action:** use a brief opening around the scientific progression: false-positive behaviour, its estimation causes and detection of true differences. Keep the plotting key and the meaning of hollow markers. State validity where it affects the interpretation of a specific result, rather than leading with the full inventory. Remove “self-contained” at line 19; the application should demonstrate that quality without announcing it.

### R35 — A vague opening precedes an otherwise useful description

**Priority: Low. Location: lines 39–45.**

> “The false-positive pattern changes substantially with table size.”

The next sentences give the actual pattern. “Changes substantially” adds little and is a common generic lead-in. “Helping where Wald is excessive” is also less precise than describing a rate relative to 5%.

**Suggested action:** lead with the difference: the 2 × 2 tests usually reject too rarely, whereas some smaller-sample 4 × 4 and 8 × 8 settings give excessive rejection. Retain the evidence and the effect of the larger cutoff.

### R36 — The margin comparison has two main ideas and a dense sequence of rates

**Priority: Medium. Location: lines 82–92.**

The paragraph moves from the small margin effect at 4 × 4 to the much larger effect at 16 × 16, with two sets of method-specific rates and a general conclusion. Readers must keep table size, sample size, three regimes and two methods in mind simultaneously.

**Suggested action:** split at “The larger table behaves differently.” Lead the second paragraph with the contrast between conservative same-skew results and excessive different-skew results. Keep the rates in the table/figure and retain the few needed to establish that contrast in the prose. The conclusion that unevenness alone does not explain the excess should stay.

### R37 — “Needs attention” hides the specific approximation error

**Priority: High. Location: lines 145–153.**

> “accompanying the improved null rate”
>
> “showing that the approximation itself also needs attention”

The paragraph contains an important distinction: the plug-in variance overestimates the observed variance, whereas the first-order variance evaluated at the true probabilities underestimates it. “The approximation” and “needs attention” do not express that distinction. The change of question is also compressed into the end of a paragraph about bias and estimated uncertainty.

**Suggested action:** separate the two comparisons and name the result directly: “Even with the true cell probabilities, the first-order approximation underestimates the observed sampling variance.” Explain that substituting true probabilities does not eliminate the approximation error. Keep the reported ratios and avoid implying that the ratios alone decompose every cause of rejection.

### R38 — A degrees-of-freedom comparison interrupts the current margin-and-bias argument

**Priority: Medium. Location: lines 155–165.**

The text switches from different-skew bias and variance diagnostics to same-skew degrees of freedom, starts with 4 × 4, changes to 16 × 16, and then returns to inaccurate uncertainty. The conclusion is useful, but the route is difficult.

**Suggested action:** introduce the question explicitly: do reasonably large degrees of freedom imply an accurate standard error? Use the 16 × 16 example to answer it. Move the separate 4 × 4 growth example to the degrees-of-freedom discussion or its existing table.

### R39 — Parallel same-skew and different-skew paragraphs become repetitive numerical narration

**Priority: Medium. Location: lines 186–211.**

The text gives the different-skew rejection progression, repeats it under same skew, then gives degrees-of-freedom progressions for both and ends by stating that the relationship persists when category frequencies match. The comparison matters, but its parallel structure sounds assembled from separate result summaries.

**Suggested action:** organise around the shared finding first: both regimes are conservative near independence and both show increasing degrees of freedom as MI increases. Use one representative numerical comparison for each claim and leave the complete progressions in the tables. Keep the bias-cancellation explanation because it explains why matching margins is informative.

### R40 — The variance-of-a-variance result needs a firmer organising question

**Priority: Medium. Location: lines 263–280.**

> “the sampling-variability approximation used to calculate degrees of freedom”

The passage carefully distinguishes the MI difference from its estimated variance, but repeated “variance,” “variability,” “prediction” and “approximation” make the conclusion harder to follow. This is a difficult statistical object, not terminology that should simply be removed.

**Suggested action:** lead with the question: does the derived formula predict how much the MI variance estimate changes between samples? Keep the population and plug-in predictions explicitly separate throughout the answer. Replace the final broad statement about “substantial errors” with the two observed directions of error near independence. Preserve the derivation check and numerical evidence.

### R41 — Several sparse-power descriptions begin with overloaded setting labels

**Priority: Medium. Location: lines 354–377; related wording at 437–439 and 470–474.**

> “The matched same-skew curves give a different sparse-table pattern”
>
> “the same-skew difference bias”
>
> “the 16 × 16 different-skew 0.01-nat alternative”

The reader must decode the entire condition before reaching the result. Repeating a newly stacked label for each statistic makes the comparison feel mechanical.

**Suggested action:** state the table size, sample size and margin regime once, then use P, Q and the MI difference consistently. Explain the result before adding the contrast: matching category frequencies removes the initial falling rejection curve in these settings, but power remains low. Keep the comparisons of bias and estimated uncertainty that support that explanation.

### R42 — “Observed precision” is a vague subject for a concrete variance explanation

**Priority: Low. Location: lines 400–410.**

> “The observed precision helps explain the ordering of power.”

The following standard deviations and bias comparisons do the real work. The opening requires the reader to translate “precision” and “ordering” before learning what differs.

**Suggested action:** begin with the smaller sampling variation under uniform margins. Retain the explanation that a fixed MI difference is easier to detect when its estimate varies less. The final connection to the variance formula is useful.

### R43 — The supporting-check section becomes a compressed second results chapter

**Priority: High. Location: lines 420–478.**

Under one small heading, the text covers the representative construction check, the large-table bias failure, reversed estimated ordering, unequal-sample power, same-skew residual bias, reversed allocation effects and the jackknife. These are distinct questions. The repeated parameter strings and rate lists resemble the overloaded abstract.

**Suggested action:** give construction, sample allocation and bias correction separate organising paragraphs or subsections. Decide which findings need a full explanation in Chapter 6 and which can be stated briefly with a reference to Appendix C. The main text should preserve the construction robustness of the bias failure and the jackknife's separation of difference estimation from standard-error estimation; it need not repeat every supporting rate.

### R44 — Broad concluding sentences repeat the preceding comparisons

**Priority: Medium. Location: lines 434–435 and 467–468.**

> “These comparisons distinguish the different-skew bias failure from the low rejection observed when the category frequencies match.”
>
> “Matching category frequencies therefore does not remove the effects of unequal sample sizes on bias and power.”

Both conclusions have a scientific basis, but the prose largely labels what the preceding sentences already state. “Different-skew bias failure” is especially compressed shorthand.

**Suggested action:** retain an ending only if it explains why the quantities differ. For example, connect unequal sample sizes to unequal residual MI biases even with identical populations, rather than making another general statement that allocation affects several outcomes.

### R45 — The runtime discussion partly narrates table bounds

**Priority: Low. Location: lines 504–508.**

> “Median times remain below 115 microseconds for Wald and 205 microseconds…”

The table already gives the times, and the first sentence gives their ratio. The final bounds add little. “Fixed call overhead can be important” is plausible but does not explicitly connect to the nearly flat measured times.

**Suggested action:** keep the cost ratio and, if useful, explain that the small change in measured time across these table sizes is consistent with substantial fixed call overhead. Do not present overhead as separately measured unless it was. Omit the redundant maximum-time summary.

### R46 — The application opens as a dataset inventory rather than a question

**Priority: Medium. Location: lines 513–519.**

> “provides a practical comparison of month–purchase MI”

This is accurate but impersonal. The next sentence already supplies a readable interpretation, so the opening could use the actual scientific question.

**Suggested action:** ask whether the information that month provides about purchasing differs between new and returning visitors. Then introduce the dataset and the weekend comparison. Keep the interpretation in terms of information, not causal effects of month on purchasing.

### R47 — The application repeats the tests' general definitions after five methodological chapters

**Priority: Medium. Location: lines 540–551.**

The application-specific bias corrections, group sizes and sign convention are useful. The final explanation of Wald versus Expanded Welch repeats their common statistic and reference distributions at length.

**Suggested action:** retain how the general formulas specialise to the month and weekend tables. Refer to the established statistic and state the two-sided 5% level briefly. Use the saved space for interpretation of the observed estimates, not another method preview.

### R48 — The application has several endings, followed by a generic return to variance variability

**Priority: Medium. Location: lines 591–606.**

> “Both methods reach the same decisions in this application…”
>
> “large session counts alone need not make its p-values close to Normal Wald's”

The month and weekend paragraphs have already stated the decisions. The closing explanation returns to the general degrees-of-freedom mechanism without showing which observed feature of these tables produced it. The small-statistic explanation for the weekend result is more concrete.

**Suggested action:** end with the substantive application interpretation and the contrast between the month and weekend statistics. Keep the statement that a non-rejection does not establish equality, but avoid another general lesson unless it is tied explicitly to the reported degrees of freedom and p-values. Do not invent an explanation for the estimated degrees of freedom that has not been checked.

**Retain:** the bias calculations at lines 121–143 and 313–345 are among the strongest passages in the results. They explain why a larger true negative difference can move the biased estimate towards zero, then connect that movement to rejection. The excessive-false-positive example with full numerical validity also earns its place here, even though it was too much detail for the abstract.

## Chapter 7 — Implications and Limitations

Source: [07_discussion.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/07_discussion.tex>).

### R49 — A short paragraph contains four different conclusions

**Priority: High. Location: lines 12–19.**

The paragraph moves from an unmeasured small-sample power cost to the observed power comparison, conservative false positives, bias, the choice of baseline and failed calculations. Each point is defensible, but their accumulation prevents any one implication from being developed.

**Suggested action:** separate what the evidence establishes about the method from the limitation on small-sample power. Put usable-result frequency with the interpretation of small-sample rejection rates. Keep the qualification that a simpler baseline is not necessarily reliable for sparse data.

### R50 — Reporting advice contains awkward abstractions

**Priority: Medium. Location: lines 21–30.**

> “gives the sampling uncertainty assigned by the method”

The paragraph offers sensible advice but uses indirect wording, then reprises the bias finding and degrees-of-freedom definition. It reads partly like a standard reporting checklist.

**Suggested action:** state that the estimated difference gives size and direction, and the standard error estimates its sampling variation. Connect the reporting recommendation directly to the observed wrong-direction rejections. Keep reporting the degrees of freedom if Expanded Welch is used, without another full explanation of the test.

### R51 — The application advice is broad and more prescriptive than the study can make concrete

**Priority: Medium. Location: lines 32–38.**

> “assess its performance on populations that match the application's category definitions, sample sizes and margin patterns”
>
> “Choose the method using that evidence before examining… p-values.”

The reader is given a list of validation tasks without an explanation of how to choose plausible unknown population tables. “Match” can sound as if the true application population is available. The final instruction shifts from findings to a generic analysis protocol.

**Suggested action:** frame this as a recommendation for application-specific simulation under plausible populations, including distinct equal-MI tables. State which uncertainty that exercise addresses and that it depends on the chosen populations. Keep the concrete reason: both tests failed in some sparse settings. Avoid presenting the procedure as a guarantee of reliability.

### R52 — The construction limitation repeats results before finally stating the limitation

**Priority: High. Location: lines 50–69.**

> “supports the representative 4 × 4 method comparison”
>
> “keeping those association locations aligned”

This paragraph compresses the construction definition, 4 × 4 findings, 16 × 16 failures, same-skew results, bias cancellation, uncertainty estimation and the range of untested tables. “Representative method comparison” gives no concrete result. The actual limitation—association is placed in aligned cells, with equal row and column margins within each population—arrives late.

**Suggested action:** lead with what the constructions do not vary. Briefly acknowledge that the second construction reproduces the main bias failure, then explain why this does not cover other association locations or unequal row and column margins. Refer back to the results rather than summarising each one again.

### R53 — The unequal-sample limitation mixes a known identity, a results recap and vague balance language

**Priority: High. Location: lines 71–85.**

> “the two contributions to the standard error and degrees of freedom can become less balanced”
>
> “This extends the comparison beyond equal samples…”

“Less balanced” does not identify which variance contribution becomes larger or how that changes the cutoff. The paragraph repeats the cancellation identity and the entire scope of the allocation check before stating its limited coverage.

**Suggested action:** state the limitation directly: unequal samples were examined only for the specified 4 × 4 populations and allocations. Explain the two mechanisms separately—unequal residual biases and changed variance contributions—using a reference to the observed check. Keep the distinction between leading correction and residual bias, but avoid deriving its cancellation again.

### R54 — Scope limitations end in vague descriptions of the approximation problem

**Priority: Medium. Location: lines 87–106, especially 100–104.**

> “small positive MI can remain close to the problematic region”
>
> “improving the rejection cutoff and improving MI's sampling approximation… are separate tasks”

The earlier paired-sample, continuous-estimator and fixed-category limitations are substantive. The final paragraph replaces the specific mechanism near independence with “problematic region” and an abstract statement about tasks. The application limitation is also a different issue from the sampling assumptions and would read better separately.

**Suggested action:** explain that quadratic sampling terms can matter even at small positive MI, while the tests use a first-order approximation. State that consequence directly. Keep the application as an illustration rather than a calibration experiment, in a separate sentence or paragraph.

## Chapter 8 — Conclusion

Source: [08_conclusion.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/08_conclusion.tex>).

### R55 — The opening is a catalogue of contribution categories and supporting analyses

**Priority: High. Location: lines 6–16.**

> “Its mathematical contribution…”
>
> “Its empirical contribution…”
>
> “Three connected studies are supported by direct checks…”

The pattern resembles the previous abstract: contribution label, study count, diagnostics, constructions, allocation and application. “Connected” does not explain a connection. The paragraph emphasises the amount of work before stating what was established.

**Suggested action:** open with the derived test and the answer to the research question. Mention the empirical comparison only to support that answer. The number of settings and full inventory need not be repeated in the conclusion.

### R56 — A result is followed by a sentence saying that it identifies where the result holds

**Priority: Medium. Location: lines 18–23.**

> “This identifies where the first-order approximation describes… and where it needs further development.”

The preceding sentence already says that agreement is good in the well-sampled setting and poor near independence. The ending adds a generic judgement instead of explaining the error.

**Suggested action:** remove the restatement. If a second sentence is needed, distinguish the error in the first-order approximation from the error introduced by substituting empirical probabilities.

### R57 — The main conclusion paragraph repeats almost the whole results chapter

**Priority: High. Location: lines 25–41.**

This single paragraph contains a favourable small-sample example, the unmeasured power cost, near-independence conservatism, underestimated uncertainty with identical populations, unequal biases, reversed ordering, both constructions, same-skew power, larger samples, the general recommendation, the simpler baseline and the practical requirement. The individual sentences are mostly understandable; the paragraph as a whole is overloaded.

**Suggested action:** organise around at most three conclusions: the cutoff sometimes improves excessive rejection but also worsens conservatism; errors in the shared estimates limit both tests; the evidence does not support general replacement of Wald. Keep the power limitation with the first conclusion. Use only the numerical examples necessary to distinguish these findings. Avoid stating the final recommendation in several successive forms.

### R58 — “The recommendation” has an unclear referent

**Priority: Medium. Location: lines 45–50.**

> “The recommendation is limited to…”
>
> “the controlled populations and small allocation check…”

The preceding text recommends against general replacement, calls Wald the simpler baseline and identifies accurate estimation as the practical requirement. It is not clear which is being limited. “Small allocation check” is an imprecise description of the evidence.

**Suggested action:** refer to the scope of the comparison or conclusion explicitly. Say that unequal-sample comparisons covered a limited set of populations and allocations. Keep the positive-cell and first-order-variance conditions, with independence treated separately.

### R59 — Future work is partly phrased as general advice on how to evaluate future work

**Priority: Medium. Location: lines 54–68.**

> “Further comparisons should assess changes… separately before combining them.”
>
> “Alternative bias treatments should therefore be assessed through both null calibration and the shape of rejection curves…”

The jackknife example gives a concrete starting point, but the paragraph then becomes a list of evaluation principles. “An improved comparison” and “alternative bias treatments” hide which estimator or calculation would be developed.

**Suggested action:** name the next statistical problem: improve the sparse MI difference and obtain a standard error appropriate for the changed estimator. Retain the falling rejection curve and wrong-direction rejections as concrete assessment criteria. Do not imply that bias reduction alone will solve the standard-error problem.

### R60 — The final future-work sentence is a generic expansion list

**Priority: Medium. Location: lines 70–78, especially 75–78.**

> “Broader unequal-sample comparisons, other association patterns and applications to additional datasets would extend the practical reach of these conclusions.”

This could conclude almost any simulation thesis. It offers breadth without identifying the unresolved question. The preceding need for a second-order approximation and a valid equal-MI comparison is much more specific.

**Suggested action:** end on the statistical problem near independence. If further population studies are retained, say what needs varying—for example, association locations or unequal row and column margins—and what unresolved claim those comparisons would test. Remove “extend the practical reach.”

## Appendix A — Supporting Calculations

Source: [A_derivation_details.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/A_derivation_details.tex>).

### R61 — The interpretation of local degrees of freedom could distinguish its quantities more explicitly

**Priority: Medium. Location: lines 282–317.**

> “separates that plug-in calculation from matching the actual sampling moments”
>
> “a mean estimated component degree of freedom of approximately 4.6”

This is important mathematics, but the opening is abstract and the example asks the reader to track three different objects: the population first-order value, the plug-in component estimate and degrees of freedom obtained from actual sampling moments. The main results earlier discuss the median combined degrees of freedom, which is yet another summary. The text says “component,” but the distinction could be easier to retain.

**Suggested action:** identify the two calculations before comparing them: substitution into the first-order formula and moment matching using the quadratic sampling approximation. In the numerical example, explicitly remind the reader that 4.6 is a mean for one population's component, not the median combined value plotted in Chapter 6. Keep the algebra and the approximation conditions.

**Retain:** the explanations of fixed-margin cancellations, order terms, covariance and the independence boundary are mostly specific and necessary. The finite-difference procedure and zero-component rule also document actual checks and choices. Their technical detail is not itself an artificial style problem.

## Appendix B — Experimental Details

Source: [B_population_construction.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/B_population_construction.tex>).

### R62 — The appendix switches into the voice of an internal protocol

**Priority: Medium. Location: lines 42–51, 74–76, 130–154, 168–179 and 192–238. Related: Appendix C, lines 213–224.**

> “Accept a table only when…”
>
> “Reshape these counts…”
>
> “Use natural logarithms…”
>
> “do not truncate…”
>
> “Report its included fraction.”

The instructions are often precise and reproducible, but the repeated imperatives make this sound like an execution specification rather than an account of the completed experiment. It also alternates with declarative descriptions of what the simulations use. This is a voice issue, not a reason to remove tolerances, validity rules or subset definitions.

**Suggested action:** describe the procedure consistently: “Tables were accepted when…”, “The counts were arranged into…”, “Negative corrected estimates were retained.” Imperatives can remain where genuinely presenting a mathematical recipe, but avoid moving unpredictably between a recipe and a completed-study report. The first-order approximation and outcome calculations need no change merely because they are formal.

### R63 — A few dense labels and broad caveats obscure precise calculations

**Priority: Low. Location: lines 207–213 and 268–280.**

> “These summaries expose estimation problems but do not isolate the causal contribution of each problem to rejection.”
>
> “For the paired method contrast…”
>
> “their difference uncertainty…”

The limitation on interpreting diagnostic ratios is useful, but “causal contribution” is broader and less concrete than the calculation being discussed. The later labels compress ordinary differences between rates into awkward nouns.

**Suggested action:** say that bias and variance summaries do not by themselves determine the rejection rate of the standardised statistic. Define the paired difference directly as Wald's rejection indicator minus Expanded Welch's. Use “uncertainty in the difference between rejection rates” instead of “difference uncertainty.” Preserve the paired versus independent simulation distinction and all denominators.

**Retain:** exact parameter grids, random-number settings, root tolerances, positivity checks, validity thresholds and inclusion rules belong in this appendix. They should remain reproducible even if their surrounding prose is made less procedural. The short opening inventory at lines 4–7 is conventional appendix navigation, not a high-priority problem.

## Appendix C — Additional Results

Source: [C_additional_results.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex>).

### R64 — Some interpretation repeats within a paragraph as well as repeating the main chapter

**Priority: Medium. Location: lines 157–164 and 393–401.**

> “The same qualitative method comparison persists…”
>
> “Both constructions give the same qualitative comparison between the tests… while numerical power differs.”

At lines 393–401, the first and last sentences make essentially the same point around the numerical evidence. At lines 162–164, “the usefulness of the resulting cutoff also depends on the shared MI statistic” repeats a broad thesis conclusion after a specific variance check.

**Suggested action:** retain the concrete construction difference and its uncertainty, but state the qualitative comparison once. In the variance check, finish with the observed prediction errors unless the following sentence adds a specific explanation. An appendix may need a short recap, but not the same full interpretation as Chapter 6.

### R65 — Definitions and validity assurances restart before almost every table

**Priority: Medium. Locations: lines 46–53, 70–76, 86–92, 129–138, 213–224, 350–356, 378–383, 406–416, 453–457, 489–504 and 533–538.**

> “All repetitions have finite diagnostics and valid test outputs…”
>
> “All outputs and diagnostics are finite and valid.”
>
> “Every output is valid.”

Definitions of bias, observed SD, variance ratios and degrees of freedom also recur. The information matters, particularly because invalid outputs affect the primary denominator, but restarting the entire explanation gives the appendix a repetitive generated-report rhythm.

**Suggested action:** introduce common column definitions once in a short table-reading key. State validity for a group of supporting comparisons where the same statement actually applies, and retain local exceptions or facts needed for interpretation. Keep table-specific definitions, such as opposite-sign percentages or cutoff-at-median values. Do not generalise the validity statement to the full null study, where failures occur. Keep captions short rather than moving all repeated prose into them.

### R66 — Figure presentation commentary and generic qualifications replace interpretation

**Priority: Medium. Location: lines 299–304 and 337–345.**

> “the enlarged main figures show those effects more clearly”
>
> “while the increasing MI difference and changing estimation errors also affect power”

The first is commentary on presentation. The second lists other possible influences without specifying which estimation error changes or how. The numerical results preceding them are useful.

**Suggested action:** state the ceiling effect directly: rates near one provide little separation between the tests for those large differences. Remove the sentence advertising the enlarged figures. In the same-skew paragraph, retain the observed degrees-of-freedom change without appending an unspecified list of other influences, or explain a measured change in the MI difference or standard error.

### R67 — Allocation results force the reader to map several differently ordered lists

**Priority: Medium. Location: lines 558–564. Related: lines 514–531.**

> “Expanded Welch instead gives 0.0946, 0.1033 and 0.0340 for those allocations.”

The paragraph discusses more observations for Q, balance and fewer observations for Q, then changes the order when describing degrees of freedom. It ends with a list of bias, sampling variation and reference-distribution effects. All values have a referent, but reading them requires repeated mental matching.

**Suggested action:** identify the allocation next to any rate retained in the prose, or let the table carry all three and discuss the meaningful asymmetry. Explain why the method comparison differs under imbalance using the reported variance and degrees-of-freedom evidence. Avoid another generic closing inventory of everything allocation changes.

### R68 — The jackknife discussion ends with an imprecise recommendation

**Priority: Medium. Location: lines 234–266, especially 264–266.**

> “This check supports its use for improving the identified sparse differences…”

The evidence concerns four settings with an unchanged standard error, and the paragraph has just shown different effects on bias, direction, variability and power. “Supports its use” is broader than simply reporting that the sparse difference improved in these examples. “Identified sparse differences” is also an awkward object.

**Suggested action:** finish with the concrete result and its scope: the jackknife greatly reduced difference bias and wrong-direction rejections in the sparse settings examined, while the retained standard error still gave conservative null rejection. Keep the larger-sample power and variability trade-off, without turning the check into a general recommendation.

**Retain:** the jackknife bias-cancellation explanation and the 16 × 16 comparison linking larger observed SD to lower power under the four-cell transfer are concrete. The Holm algorithm at lines 609–616 supplies a reproducible calculation rather than empty procedural prose. Neither needs a stylistic rewrite simply because it contains several steps.

## Front matter

Source: [acknowledgements.tex](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/frontmatter/acknowledgements.tex>).

### R69 — The acknowledgements are generic, although conventional

**Priority: Low. Location: lines 4–6.**

> “the colleagues, friends, and family members whose support made this work possible”

This could appear in almost any thesis. It is understandable and not a substantive writing defect, but a personal section is the clearest place for the author's own voice.

**Suggested action:** if desired, replace the broad list with the actual people and specific forms of help the author wants to acknowledge. Do not invent names, experiences or emotions. The standard title-page degree wording and thesis title do not need an “AI-style” edit.

## Suggested order for a later revision

1. **Restructure the conclusion and discussion:** R49, R52, R53, R55 and R57. These contain the densest summaries and the clearest instances of the abstract's earlier problem.
2. **Remove duplicated scaffolding in the introduction and design:** R03, R04, R26 and R27. Decide where each explanation belongs before rewriting individual sentences.
3. **Clarify the statistical motivation and the distinction between errors:** R09, R17, R25, R37 and R40. Avoid making estimated standard errors alone an argument for a Student t distribution; distinguish first-order approximation error from plug-in error.
4. **Reorganise Chapter 6's supporting checks and application:** R43, R46–R48. Keep the main findings and mechanisms, with secondary numerical detail in Appendix C.
5. **Reduce repeated definitions, table narration and generic endings:** R39, R44 and R64–R68, then the low-priority notes.
6. **Read the revised prose continuously.** Check whether each paragraph answers one question and whether the next paragraph follows from it. Do not enforce a fixed sentence length or a fixed four-sentence paragraph template; either can create another mechanical voice.

## Boundaries for the revision

- This is a prose review, not a fresh scientific or bibliographic audit. It does not independently revalidate numerical results or external sources.
- Preserve the teaching depth of Section 2.3 and the useful intermediate calculations elsewhere.
- Preserve the distinction between equal MI and identical tables, between population and empirical probabilities, and between an MI variance and the variability of its estimate.
- Preserve substantive limitations: positive probabilities, the independence boundary, the selected population constructions, restricted allocation study, numerical validity and the unmeasured small-sample power cost.
- Do not “humanise” the writing with informality, unsupported opinions, fabricated personal experience or deliberate errors. The desired change is clearer statistical explanation and less repetitive framing.
- No prose has been edited in this review. Historical working drafts and the current manuscript and delivery set remain unchanged.
