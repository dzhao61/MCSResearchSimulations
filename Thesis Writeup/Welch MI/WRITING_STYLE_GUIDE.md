# Writing Style Guide for the Welch-MI Thesis

## 1. Overall Style

The target style is **formal, direct, and explanatory**. It should read like a
clear statistical methods thesis rather than a compressed journal article or
an informal tutorial. The mathematical content can be advanced, but the prose
surrounding it should use ordinary words and make the logical purpose of each
step explicit.

The reader should never have to infer why a quantity is being introduced. The
usual order is:

1. State the statistical quantity or problem being addressed.
2. Explain why the method needs it.
3. Present the definition or derivation.
4. Interpret the result in one or two sentences.
5. Connect it to the next step.

This is the strongest feature of the method writing in Michael Fang's thesis
and of the revised expanded Welch-Satterthwaite derivation already developed
for this project.

## 2. What the Exemplars Show

### Grace Yan

Grace's thesis uses an accessible, application-led narrative. Paragraphs
usually begin with the practical phenomenon, explain why it matters, and then
introduce the technical method. The prose is formal but uses familiar words.
The sampled introduction had a median sentence length of approximately 20
words.

Useful features to adopt:

- Begin chapters with the scientific or statistical problem, not notation.
- Explain practical relevance before technical detail.
- Keep the main argument focused and move secondary analyses to appendices.
- Separate conclusions, limitations, and future work.

Features not to adopt:

- Repeating the thesis roadmap or contribution in several forms.
- Meta-statements such as "this section demonstrates rigour."
- Promotional language that is stronger than the evidence.

### Michael Fang

Michael's thesis is the closest stylistic model for a methodological
contribution. Its strongest derivation passages start from an existing
equation, identify the practical obstacle, and explain the transformation
needed before showing the next equation. The sampled introduction had a median
sentence length of approximately 22 words.

Useful features to adopt:

- Put the purpose of a derivation immediately before the mathematics.
- Develop the method in one chapter and validate it in a separate chapter.
- Define technical terms at first use and then use them consistently.
- Use synthetic data with known truth to support methodological claims.

Features not to adopt:

- Repeating the same motivation before several consecutive equations.
- Long strings of adjectives such as "novel, robust, practical, and broadly applicable."
- Claiming novelty or reliability without immediately identifying its basis.

### Riley Jones

Riley's thesis provides explicit research questions and useful method
outlines. It often links an experimental stage directly to the question it is
intended to answer. However, its sampled introduction used substantially longer
sentences, with a median of approximately 26 words and several sentences above
50 words. Some sections also divide the argument into too many small units.

Useful features to adopt:

- End the literature review with a short synthesis and explicit research questions.
- Open the validation chapter with a concise experimental roadmap.
- State the known ground truth and evaluation target before describing simulations.

Features not to adopt:

- Combining motivation, assumptions, procedure, and interpretation in one sentence.
- Creating a subsection for every small algebraic or experimental step.
- Allowing grammatical complexity to obscure the main claim.

The sentence statistics above are indicative measurements from representative
introductory passages, not evaluations of the complete theses.

## 3. Recommended Voice and Tone

Use a calm, evidence-led voice. The thesis should sound confident when stating
definitions or derived results and appropriately qualified when discussing
approximations or empirical findings.

| Context | Preferred tone |
| --- | --- |
| Definition or algebraic identity | Direct: "Mutual information is..." or "Differentiating gives..." |
| First-order approximation | Qualified: "Under the first-order expansion..." |
| Simulation result | Evidence-led: "Expanded Welch reduced mean calibration error in four difficult regimes." |
| Interpretation | Calibrated: "This suggests that accounting for variance uncertainty improves finite-sample calibration in these settings." |
| Limitation | Specific: "The first-order variance vanishes at independence, so the method does not cover (I(P)=0)." |
| Novelty | Bounded: "The contribution is the MI-specific variance-influence degrees-of-freedom construction and its finite-sample evaluation." |

Prefer **"this thesis"** when describing scope and contributions and **"we"**
when guiding the reader through a derivation or describing an experiment. Do
not alternate unpredictably among "I," "we," and impersonal passive voice.

Avoid defensive or conversational phrases:

- "It is obvious that..."
- "Clearly..."
- "It is important to note..."
- "For completeness..."
- "This proves that our method is better..."
- "This section demonstrates rigour..."

State the relevant fact directly instead.

## 4. Sentence Construction

Aim for an average sentence length of approximately **20-25 words**. Sentence
length should vary naturally, but sentences above about 35 words should be
checked for more than one independent idea.

Each sentence should normally perform one role:

- state a claim;
- provide a reason;
- define a quantity;
- report evidence; or
- interpret a result.

Do not force all five roles into the same sentence. For example:

> The normal Wald test treats the estimated standard error as sufficiently
> stable. This approximation can be inaccurate in small or sparse tables,
> where the estimated MI variance changes substantially between samples.

This is preferable to a single sentence containing the baseline, assumption,
failure regime, proposed correction, and conclusion.

Use active constructions where they identify the mathematical action:

- "We differentiate (V(P)) along the perturbation path."
- "The simulation draws one table from each population."
- "Figure 6.2 shows the observed rejection rates."

Passive voice remains suitable when the actor is irrelevant:

- "The two component degrees of freedom are combined using the Satterthwaite equation."

## 5. Vocabulary and Conceptual Complexity

Use the required statistical vocabulary, but do not add complexity through
ornamental wording. Prefer:

| Prefer | Avoid when unnecessary |
| --- | --- |
| use | utilise |
| show | elucidate or showcase |
| difference | discrepancy or divergence |
| change | variation or modulation |
| calculate | operationalise |
| helps | facilitates |
| method | methodological framework |

Technical terms such as *influence function*, *weak null*, *pointwise mutual
information*, and *moment matching* are necessary. Define each once in plain
language, give its mathematical definition, and then use the same term
consistently. Do not cycle through synonyms after a term has been fixed.

Complex ideas should be layered in this order:

1. Intuitive statistical role.
2. Formal symbol and definition.
3. Derivation or calculation.
4. Consequence for the test.

The prose should not hide a difficult idea, but it also should not present
intuition, notation, assumptions, and all algebra simultaneously.

## 6. Paragraph Structure

Most paragraphs should contain three to six sentences and develop one focused
idea. A strong technical paragraph often has this form:

1. Topic sentence naming the objective.
2. Explanation of the obstacle or assumption.
3. Definition or equation.
4. Interpretation of the equation.
5. Transition to the next required quantity.

Begin a new paragraph when moving from definition to evaluation, from method to
interpretation, or from one limitation mechanism to another. Do not begin a
new subsection merely because a new equation appears.

Chapter introductions should state the chapter's purpose, its connection to
the research question, and its order of argument in one or two paragraphs.
Chapter conclusions should report what was established, not repeat the table
of contents.

## 7. Presenting Mathematics

Equations should form part of the argument rather than appear as isolated
objects. Use the following sequence.

**Before an equation:** state what is being calculated and why.

**In the equation:** show enough intermediate steps for the transition to be
checked without introducing disposable notation.

**After the equation:** define any new symbol and state what the result means
for the method.

For example:

> The test requires the sampling variance of the estimated MI. To first order,
> the error in the plug-in estimate is the average of the centred pointwise-MI
> contributions:
>
> \[
> \widehat I(P)-I(P)
> \approx
> \frac{1}{n_P}\sum_{a=1}^{n_P}
> \{\ell_P(Z_a)-I(P)\}.
> \]
>
> Because the observations are independent, the variance of this average is
> (V(P)/n_P).

Use display equations for central definitions and derivations. Keep short
symbols and comparisons inline. Avoid presenting several large equations
without explanatory text between them.

## 8. Tense and Evidence

Use the present tense for definitions, established theory, figures, and the
contents of the thesis:

- "Mutual information measures..."
- "Welch's test uses..."
- "Figure 6.1 shows..."

Use the past tense for completed experimental actions:

- "We generated 60 equal-MI population pairs."
- "Each population pair received 10,000 replicates."

Use calibrated verbs for findings:

- **shows** for a directly displayed numerical fact;
- **supports** for evidence consistent with a claim;
- **suggests** for an interpretation with uncertainty;
- **establishes** only when the derivation or design genuinely warrants it.

Reserve *significant* for statistical significance. Use *substantial*,
*material*, or an exact numerical change for ordinary importance.

## 9. Literature Review Style

Organize the literature by the problem being solved, not as one paragraph per
paper. A strong literature paragraph should:

1. state the relevant methodological issue;
2. synthesize what several sources establish;
3. identify what remains unresolved; and
4. connect that gap to the thesis question.

Prior work should be described precisely and without diminishing it. The
novelty boundary is clearer when the thesis states which components are
established and exactly which combination or derivation is new.

## 10. Results and Limitations Style

Results sections should lead with the evaluation question, then the figure or
table, then the main numerical pattern. Do not narrate every cell. Report both
improvement and failure cases, and include Monte Carlo uncertainty where
relevant.

Limitations should use a three-part structure:

1. State the assumption or limitation.
2. Explain how it can affect the result.
3. Define the resulting boundary on interpretation.

For example:

> The derivation assumes a positive first-order MI variance. At independence,
> this variance is zero and the first-order Student approximation is
> nonregular. The proposed test should therefore not be used as a replacement
> for chi-squared or conditional randomization tests of independence.

This is more informative than a general statement that the method "has some
limitations."

## 11. Final Prose Checklist

Before accepting a section, verify that:

- its first paragraph states the purpose;
- every new symbol is defined once;
- every central equation has a reason before it and an interpretation after it;
- no sentence contains several independent claims;
- common words are used where technical words add no precision;
- empirical claims include a number, figure, table, or citation;
- approximations are distinguished from identities;
- the result is not described more strongly than the evidence permits;
- terminology, tense, and authorial voice are consistent; and
- the final paragraph advances the argument rather than repeating the opening.
