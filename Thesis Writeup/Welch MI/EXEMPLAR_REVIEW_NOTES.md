# Exemplar Review and Writing Notes

Reviewed 13 September 2026. These notes guide the [new thesis plan](THESIS_REWRITE_PLAN.md). They supersede the older style guide where its examples or recommendations depend on the previous experiments.

## 1. Materials and scope of the review

The review covered the three supplied theses' contents, introductions, literature-to-question transitions, methodological explanations, experimental sections, results, conclusions and limitations. Close reading focused on the passages identified below. Representative equation and figure pages were also inspected visually. This is a study of presentation and research design, not an independent verification of every scientific claim in these theses.

Page references below use the **printed thesis page number**, followed by the PDF page where helpful. The distinction matters because the front matter shifts the PDF numbering.

| Source | Structure and length observed | Most useful model for our thesis |
| --- | --- | --- |
| [Zhiyin (Grace) Yan, Relationships between stock market equities and their dynamics](../Example%20Thesis/GraceYan-Thesis.pdf) | Seven chapters; main text pp. 1-65; references start p. 66; extensive appendices follow. | An accessible progression from data and a simple analysis to more detailed comparisons, with consistent graphical scales. |
| [Michael Fang, Estimate Active Information Storage for Neural Spike Trains](../Example%20Thesis/MichaelFang-Thesis.pdf) | Six chapters; main text pp. 1-58; method pp. 24-33, synthetic validation pp. 34-43, application pp. 44-53. | Explaining a mathematical method, implementing it, then testing it against known quantities. |
| [Riley Jones, Inferring Human Whole-Brain Effective Connectivity from Resting-State fMRI Using Linear Least Squares Regression](../Example%20Thesis/RileyJones-Thesis-Brain_Network_Inference-FINAL.pdf) | Six chapters; main text pp. 1-87; synthetic study pp. 23-48 and empirical study pp. 49-79. | Explicit research questions, controlled failure experiments, and discussion of what the observations actually permit us to infer. |
| [Supplied LaTeX template](../Example%20Thesis/thesis_2024/thesis.tex) | A `usydthesis` project with separate chapter files, front matter, bibliography and placeholder prose. Its configured degree is Bachelor of Advanced Computing (Honours). | Document organisation and formatting conventions. It does not establish current Master's submission requirements. |
| [Previous Welch-MI draft](main.tex) | Eight chapters and five appendices, with a compiled PDF and an existing bibliography connection. | Reusable LaTeX infrastructure and some mathematical material; the empirical argument requires replacement. |

The examples demonstrate several viable structures. They do not imply that a good thesis needs a particular page count, a real-data chapter, or a method that outperforms every baseline.

## 2. Grace Yan: build understanding through a sequence of analyses

### Structure and argument

The introduction moves from stock-market relationships to the need to study how those relationships change. Section 1.2, pp. 4-5, names concrete operations: construct a network, identify groups, examine changing states and compare approaches. The literature review ends with an explicit gap section, Section 2.2.3, p. 26. Chapter 3 establishes the dataset before Chapters 4-6 use it.

The important structural feature is the transition from **static relationships to changing relationships to time-lagged relationships**. Each stage adds a question the previous analysis cannot answer. The ending of Section 4.2, p. 38, explains what the static network has established and why the next chapter studies change over time. The opening of Chapter 5, p. 39 (PDF p. 54), makes that connection again in a short paragraph.

For our thesis, the corresponding progression is: define the two-sample problem, construct the proposed correction, show the broad performance landscape, then examine the factors that alter that performance. It should feel like a sequence of questions, rather than a chronological record of experiments.

### Tone, sentences and vocabulary

The strongest passages start with familiar objects such as stocks, prices or windows, and introduce the technical term after its role is apparent. Section 3.1, p. 27, explains the dataset through concrete dimensions: dates, stocks, rows and columns. This is useful for describing our probability tables and sampled count tables.

Sentences often begin with the object already under discussion and add one new property or operation. For example, the Chapter 5 transition starts from the static network before introducing changes over time. This gives the reader continuity. Some passages are more repetitive or promotional; those are not features to copy.

**Application to our writing:** start with "The row probabilities describe how often each category of X occurs" before introducing a marginal vector. Follow with the formula and then a numerical example. Do not introduce "marginal heterogeneity" before explaining what varies.

### Experimental and visual presentation

Chapter 5 evaluates several window lengths and compares sliding-window analysis with an HMM. Section 5.1, p. 39, explicitly fixes colour limits across its connectivity figures. Alternative window results also appear in appendices, keeping secondary comparisons available without repeatedly interrupting the main discussion. Section 5.3.2, p. 51, introduces an external comparison with volatility and explains what agreement would mean.

**Application to our study:** keep the same colours, line styles and axes for comparable regimes. Show how changing sample size affects both methods on the same fixed population pair. Put the full collection of detailed panels in a companion atlas, with a clear map from the thesis figures to that atlas.

### Limitations as boundaries on interpretation

Section 7.2, pp. 62-64, identifies concrete choices: the selected exchange, selected stocks, correlation measure and time windows. The useful pattern is **choice, consequence, scope**. Our counterpart is the choice of population family, its effect on the cell probabilities, and the resulting limit on generalisation to other tables.

Do not reproduce prefatory assurances about demonstrating rigour. State the limitation and its consequence directly.

## 3. Michael Fang: connect each mathematical step to a computational need

### Structure and argument

The method chapter follows a literature review that culminates in the research problem, Section 2.5, p. 23. The thesis then moves through method construction, synthetic validation and application. This is the closest overall methodological model for our work, although our thesis has a simulation evaluation rather than an application as its main empirical contribution.

Chapter 3, pp. 24-33, begins with a definition that is difficult to calculate directly. It changes the representation, defines the objects needed by the calculation, and gives an algorithm. This connects theory to an executable procedure.

### How the equations are explained

Section 3.1, pp. 24-26 (PDF pp. 34-36), provides a particularly useful pattern:

1. Recall the starting quantity and define its symbols.
2. Explain the practical obstacle in calculating it.
3. Name the mathematical operation that resolves the next part of the obstacle.
4. Display the resulting equation.
5. Explain what can now be calculated and what remains to be defined.

The passage introducing Equation 3.2 names the probability representation before using it. The next step names Bayes' theorem and explicitly identifies cancellation. The discussion after Equation 3.6 explains why the reformulation is useful. The reader is told what the algebra achieves.

For Expanded Welch, this becomes: the test needs a variance estimate; the proposed reference also needs the uncertainty of that estimate; differentiating the complete variance functional supplies that uncertainty. Each new symbol must have that explicit purpose.

The visually inspected PDF p. 35 uses separated equations, definitions immediately below them, and ordinary paragraphs between steps. We should reproduce that reading rhythm, while avoiding a separate subsection for every elementary manipulation.

### Synthetic experiments as questions with known answers

Chapter 4, pp. 34-43, proceeds through a memoryless process, a process with a refractory period and a more complicated bursting process. The first case has a known zero target. The second has an analytical reference. The third uses an approximate reference and needs a different interpretation.

Sections 4.2.1 and 4.2.2, pp. 37-38, separately vary the effect-producing parameter and sample size. This distinction is directly useful: increasing the true MI difference asks about detection, while increasing sample size at fixed populations asks about sampling behaviour.

The bursting discussion, pp. 39-43, also demonstrates why the status of a benchmark must be explicit. Agreement with a numerical target, agreement with an approximate formula and an exact identity provide different kinds of evidence. In our thesis, numerical agreement with the requested MI checks population construction; it does not validate the Student reference distribution.

### Tone and sentence construction

The method passages work best when the main clause names an operation: define, substitute, differentiate or estimate. Technical vocabulary is appropriate when it identifies an actual object. Repeating phrases about robustness, novelty or broad applicability adds little information.

We should keep the explanatory method passages but use more restrained results language. "The estimate approached the reference over the tested sample sizes" is more precise than treating a simulation curve as proof of consistency.

### A useful consistency lesson

The application parameter table specifies k=5 on p. 46, while the limitations mention k=4 on p. 56. This is a reminder to check every repeated parameter against one authoritative specification. Likewise, descriptions of uncertainty must distinguish standard deviations across trials from confidence intervals for a mean or rejection probability. We should take the structural lessons from the example without assuming every sentence is a model to copy.

## 4. Riley Jones: evaluate where the method breaks

### Research questions connected to experiments

Sections 3.4 and 3.5, pp. 21-22, move directly from a literature synthesis to two research questions. Chapter 4 then states why synthetic data are useful: the underlying network is known and relevant properties can be controlled. Section 4.1, p. 24, gives an experimental outline tied to the first question.

This is a useful model for the correspondence between our research questions, experiment families and conclusions. A reader should be able to trace a question to the figures that answer it.

### Success and failure belong in the same evaluation

Sections 4.5-4.6, pp. 28-30, place successful and unsuccessful reconstructions next to each other, then investigate sample size. The unsuccessful example does not end the study; it motivates the next controlled comparison. Later sections vary sampling, temporal dependence and modelling choices.

Sections 4.12-4.13, pp. 45-48, connect numerical observations to assumptions. The discussion distinguishes having many nominal observations from having enough informative observations. Our analogous point is that sample size alone does not determine whether first-order MI inference works: baseline dependence, cell probabilities and empirical support also matter.

### Writing style and density

The thesis uses explicit section names and links results to questions. Its longer sentences sometimes combine a mathematical condition, an empirical observation and an explanation. Those ideas are easier to assess when separated.

For our thesis, first state the observation, then give the proposed explanation and its evidence. For example: "Both tests remained conservative at the smallest baseline MI. This is consistent with slow approach to the regular first-order regime." The second sentence is an interpretation; it should not silently become a demonstrated causal mechanism.

The synthetic chapter contains many numbered subsections. We can keep the experimental organisation while grouping closely related steps, rather than adopting the same depth of headings.

### Figures and scope

Figures 4.4 and 4.5, pp. 29-30, include concrete network and sample settings. The inspected PDF p. 40 makes the failed reconstruction visually accessible before explaining the next experiment. For our figures, repeat the actual P and Q settings, not just a label such as "sparse".

The distinction between different metrics in Section 6.2.3, p. 84, is also valuable. A favourable value of one metric does not establish overall usefulness. Our thesis must interpret false positives, power and valid-result frequency together.

## 5. Shared writing principles to adopt

### Structure

The introduction should establish the problem, the unresolved question and the contribution. The background should supply only concepts needed later. The method chapter should explain the calculation. The experiment chapter should make the evaluation reproducible. Results should answer the stated questions, and the discussion should explain implications and limitations.

Each chapter needs a short opening that explains its role. Avoid opening every subsection with a second roadmap. End a chapter with what has been established and the specific question that follows, if a transition is needed.

### Tone and vocabulary

Use formal, direct, explanatory prose. Prefer "use", "calculate", "change", "estimate" and "compare". Keep necessary terms such as mutual information, sampling variance and degrees of freedom, but define them before relying on them.

Use "this thesis" for the contribution and scope; use "we" consistently for mathematical and experimental actions. Use present tense for definitions and displayed results, and past tense for completed simulations. Reserve "significant" for statistical significance.

Do not make the method sound successful before showing the evidence. "We evaluate an MI-specific correction" is appropriate. "We develop a robust solution to sparse-table inference" is not supported by the current results.

### Sentences and paragraphs

Usually give each sentence one main job. Start with a familiar object and introduce the next concept toward the end, so the next sentence can develop it. Prefer explicit subjects: "The simulation holds P fixed" is easier to read than "Fixing of the first population is undertaken".

Vary sentence length naturally. Check sentences above roughly 30-35 words for multiple ideas; this is an editing aid, not a numerical writing target. The earlier guide's sentence-length estimates have not been remeasured here and should not be treated as a criterion of thesis quality.

A technical paragraph usually needs an objective, the relevant definition or calculation, and an interpretation. A results paragraph usually needs a question, an observed pattern with evidence, and a limited conclusion. Not every paragraph needs all of these parts, and none needs a stock introductory phrase.

### Mathematics and intuition

State whether a line is an identity, a Taylor approximation, an asymptotic statement or a working distributional model. Explain notation immediately and keep the same notation across chapters.

For a Taylor expansion, first define the function, variable and expansion point. Then use the familiar template

\[
f(z)\approx
\underbrace{f(a)}_{\text{zeroth order}}
+\underbrace{f'(a)(z-a)}_{\text{first order}}
+\underbrace{\frac{f''(a)}{2!}(z-a)^2}_{\text{second order}}.
\]

Calculate the terms separately before combining them. If the function is a cell contribution such as z log(z/a), differentiate the complete contribution, including the factor in front of the logarithm. For a multivariate functional, define a scalar perturbation path or explicitly explain the vector version; do not silently apply a one-variable formula to an entire table.

When explaining sampling scales, give one concrete fact: a sample proportion has standard deviation proportional to 1/sqrt(n); its squared error is therefore typically of order 1/n. Explain why that fact matters for the displayed term. A full derivation can follow in an appendix.

### Results and graphical specifications

Use the same order of explanation for parallel experiments: question, figure, exact specifications, interpretation. A panel represents one fixed regime and contains both methods. Keep comparable axes consistent and repeat row and column settings so each figure is understandable on its own.

Error bars or bands must say exactly what uncertainty they show. A Monte Carlo interval for a rejection probability is different from a confidence interval for an MI difference. Report sensible precision: usually three or four decimal places for rates, and scientific notation for very small MI targets rather than rounding them to zero.

Present the broad landscape before selecting examples for explanation. Preserve every regime in a systematically organised appendix or companion atlas. No average across table sizes or marginal profiles should replace those individual results.

## 6. Template and previous draft: what to retain

The supplied template's `methodology.tex` and `results.tex` contain TODO descriptions and `Blindtext`. These are placeholders, not substantive examples of experimental design. Its front matter, chapter separation, lists of figures and tables, and bibliography are useful layout references. Any placeholder names, degree declarations or signatures are template content, not instructions to adopt them.

The previous draft already has a workable book-class project, separate chapters, equation labels, notation macros and a bibliography. Retain that organisation. Check the required degree wording and formatting against the applicable course material before submission; do not infer them from an Honours example.

The draft's main empirical narrative is obsolete. It relies on 60 random equal-MI pairs, limited alternatives, averages across regimes and shared validity assumptions. The new experiment uses fixed interpretable populations, a broader sample-size range, paired comparisons and method-specific validity. These differences require rewritten design, results, discussion and abstract chapters.

One mathematical wording change is especially important: Normal Wald uses an **estimated** standard error and an asymptotic normal reference. It does not literally assume the variance is known. Expanded Welch adds an approximate reference adjustment for denominator uncertainty; that adjustment is not an exact Student theorem.

## 7. Practical standard for the new thesis

A good version of this thesis will let a reader answer four questions: what the method calculates, why that calculation was proposed, what the experiments actually establish, and when the resulting recommendation applies. The contribution is the derivation and a careful assessment of its usefulness. That contribution remains meaningful when the assessment finds substantial limitations.

The [rewrite plan](THESIS_REWRITE_PLAN.md) turns these observations into chapter specifications, an evidence map, figure rules and a drafting sequence.
