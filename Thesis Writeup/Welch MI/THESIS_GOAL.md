# Goal: complete the master's thesis

Set 15 September 2026; acceptance criteria refreshed 6 October 2026. The
original working target of **22 September 2026** was a project estimate, not a
University submission deadline. Completion is now determined by the checks
below, not that past date.

## 1. Objective

Complete a clear, technically sound, submission-ready master's thesis titled
**Comparing Mutual Information in Finite Samples: Wald and Expanded
Welch-Satterthwaite Inference**, with depth, length and presentation comparable
to the three supplied example theses. The final work must explain and derive
the proposed method, evaluate it fairly against Normal Wald using the completed
experiments, and give a practical conclusion supported by the individual
regimes. Deliver the finished PDF, reproducible LaTeX source, supporting
experimental material and a completed verification record.

The reader should understand what is being tested, how each method is
calculated, why the proposed adjustment could help, where it succeeds or fails,
and what the evidence supports in practice.

The manuscript must stand alone: assume the reader has no access to the
codebase or experimental archives. Describe the scientific construction,
settings, evaluation and validity rules in the manuscript and its appendices.
Keep file inventories, paths, build commands, configuration IDs,
version-control history and protocol-freeze records outside the reader-facing
thesis. Internal verification and delivery records may retain those details.

### Agreed basis

- The user clarified on 15 September that there is no AI-use limitation for this task and that CSYS5061 is the wrong course. Its report length, assessment dates and AI restrictions do not apply to this thesis.
- Length and writing quality are benchmarked against the supplied Grace Yan, Michael Fang and Riley Jones theses, using the analysis in [EXEMPLAR_REVIEW_NOTES.md](EXEMPLAR_REVIEW_NOTES.md).
- Use the later Daniel Li exemplar review in [DLI_EXEMPLAR_REVIEW_NOTES.md](DLI_EXEMPLAR_REVIEW_NOTES.md) for concrete mechanisms, question-led transitions, purpose-led literature and findings-first discussion. It is a language and narrative model, not an additional length requirement or a reason to shorten the central derivations.
- The active manuscript and completed fixed-population experiments are the starting point. Existing verified work counts toward the targets below; it should be extended where incomplete.
- Routine writing, editing, verification and small diagnostic calculations can proceed autonomously. Supervisor consultation is not a prerequisite for each decision.
- The final research comparison is Normal Wald versus Expanded Welch. The central contribution is the derivation and careful evaluation of the proposed correction, including its limitations.
- Retain the completed population tables. Explain the binary construction through its equivalent copying-and-independent-drawing mechanism and larger tables through probability transfers; keep the general matrix formulas, feasibility limits and numerical search in Appendix B.
- Use three focused appendices: A, supporting calculations; B, experimental details; C, additional results. Remove repeated derivations and peripheral arguments while retaining assumptions, exact settings, validity rules and evidence needed to assess the thesis. Keep all 84 reported main null settings visible individually rather than substituting an aggregate summary.
- Report settings with at least 10 observations in each population. Apply this sample-size rule across all families, without filtering on validity or rejection outcomes. Preserve the original runs internally, including the omitted n=1, 2 and 5 settings; do not change populations, statistical methods or retained results.

### Questions the thesis must answer

| Research question | Required evidence | Main location |
| --- | --- | --- |
| RQ1. How can changes in the estimated MI variance be used to choose degrees of freedom for a two-sample test using a Student t distribution? | Checked derivation, defined assumptions, implemented algorithm and worked calculations. | Chapters 3-4; Appendix A. |
| RQ2. Does the resulting Expanded Welch test offer a useful improvement over Normal Wald? | Corresponding null and alternative regimes, validity, paired comparisons, effects of margins, association and sample allocation, convergence, runtime and a bounded practical recommendation. | Chapters 5-8; Appendices B-C. |

These are the two questions stated in the current Introduction. The earlier
four-question list is retained in substance as evidence strands for RQ2, not
as four separately announced research questions.

## 2. Length and depth benchmark

The following lengths were checked against the supplied PDFs and their tables
of contents on 15 September. Main text means Introduction through Conclusion,
including its figures and tables, before references and appendices.

| Thesis | Main text | Complete PDF |
| --- | ---: | ---: |
| Michael Fang | 58 pages | 75 pages |
| Grace Yan | 65 pages | 126 pages |
| Riley Jones | 87 pages | 104 pages |
| Current Welch-MI manuscript (6 October) | 51 pages | 86 pages |

The exemplars' **58-87 main-text pages** and **75-126 total pages** are depth
and presentation benchmarks, not pass/fail limits. The current main text is
shorter because supporting plots and technical detail were moved to appendices
to keep the argument focused. Review whether any necessary explanation is
missing; do not restore material merely to reach an exemplar page count.

Use a consistent A4 layout with readable body text, equations and figures.
Keep normal thesis typography; do not change margins, font size, spacing or
figure placement merely to meet a page count. Do not add repetitive explanation
or unrelated literature to reach a numerical target. Record a word count as a
secondary diagnostic using the same counting method across revisions; no
unverified word limit is imposed. The current main text has 13,700
whitespace-separated tokens extracted with `pdftotext` from PDF pages 9-59
(printed pages 1-51). This diagnostic includes headings, captions, mathematical
tokens and plot labels; it is not a prose-only word count.

### Working chapter allocation

These are the current printed-page allocations, not quotas. Move space between
chapters when the explanation requires it.

| Chapter | Current pages | Required purpose |
| --- | ---: | --- |
| 1. Introduction | 3 | Establish the problem, two research questions, contributions and scope. |
| 2. Background and Literature Review | 11 | Teach the necessary concepts and locate the contribution in verified prior work. |
| 3. The Two-Sample MI Test and Wald Baseline | 4 | Define the data, estimates, bias correction, variance, statistic and reference. |
| 4. The Expanded Welch--Satterthwaite Test for MI | 12 | Derive variance sensitivity and degrees of freedom, with intuition, worked calculations and assumptions. |
| 5. Experimental Design | 5 | Explain the binary sampling mechanism, larger-table probability transfers, controlled factors, sampling and evaluation; place general construction formulas, numerical search and exact grids in Appendix B. |
| 6. Experimental Results and Discussion | 12 | Develop the argument around selected figures, interpreting each beside the evidence; retain the individual main null table and focused supporting figures in Appendix C. |
| 7. Implications and Limitations | 2 | Synthesize the practical trade-off and evidence limits without repeating the figure readings. |
| 8. Conclusion | 2 | Restate contributions and impact, limitations, future work and the resulting recommendation. |

## 3. SMART targets

Each target identifies a specific outcome, measurable acceptance evidence and
a due date. The work is achievable from the existing manuscript, implementation
and completed simulations. Its relevance is the reader's ability to understand,
reproduce and assess the thesis's scientific argument.

| ID | Specific outcome | Measurable acceptance criterion | Due |
| --- | --- | --- | --- |
| T1 | Agree the scope and exemplar benchmark. | Record all three exemplar lengths, the chapter allocation, two research questions and the evidence each requires. Remove the unrelated course restriction from active notes. | 15 Sep |
| T2 | Finish the mathematical explanation. | Check every central equation against an independent derivation and the implemented estimator. Define every substantive symbol at first use; label all Taylor expansions and distributional approximations. Verify the worked examples and relevant mathematical tests. | 16 Sep |
| T3 | Finish the literature argument. | Map every substantive prior-work and novelty claim to an inspected source and location. Verify every cited bibliography entry; resolve or explicitly narrow any unsupported claim. Cover MI estimation and variance, related information comparisons, Welch-Satterthwaite theory, simulation construction and the independence boundary. | 17 Sep |
| T4 | Complete the experimental design chapter. | Account for every experiment family and all 2,760 reported configurations, 534 population pairs and 20,000 replicates per configuration. Explain P and Q construction with a numerical example and distinguish fixed population differences from sample randomness. Reconcile repeated design values with the stated sample-size scope and the original protocol records. | 18 Sep |
| T5 | Complete the results and interpretation. | Answer both research questions with equations and results presented in the manuscript. Select main figures for a question-led argument, interpret each beside its evidence, and keep focused supporting figures in the appendix. Address every experimental family and retain every individual regime in separate project records without making their availability a condition for reading the thesis. Verify all numerical claims, all 15 included plots and every cell of the 84-setting main null table against exact source rows. | 19 Sep |
| T6 | Complete the substantive and language edits. | Review every chapter and appendix once for scientific coherence and once for readability. Resolve every material issue found in those passes. Check notation, equation explanations, repeated settings, terminology and parallel presentation across all experiment sections. | 20 Sep |
| T7 | Complete technical and visual verification. | Build from a clean copy of the final source package; obtain zero build errors, undefined citations/references, missing figures or overfull boxes. Inspect every rendered page at its final size, resolve visual defects and rerun the relevant evidence checks after final changes. | 21 Sep |
| T8 | Deliver the final thesis package. | Provide the standalone PDF, self-contained source, bibliography and figures, plus separate experiment records, reproduction instructions and completed acceptance record. Include accurate front matter with no editing placeholders or invented personal attestations. All material findings must be resolved before marking the goal complete. | 22 Sep |

T1 establishes the agreed target. T2 and T3 can proceed together; T4 and T5
must remain consistent with the final mathematical and evidence checks. T6-T8
review the assembled work. If a stage uncovers a scientific error, fix and
recheck the affected material before proceeding. Record any revised work date
and reason; the target date does not relax the acceptance criteria.

**Status at 6 October 2026:** T1-T8 are complete for the current 86-page A4
manuscript, with 51 printed main-text pages. Chapter 6 uses seven lead figures
and Appendix C retains eight supporting figures plus all 84 reported main
null settings. The three appendices occupy 23 pages, down from 33 before the
appendix simplification. The paragraph-coherence and direct-explanation passes
and full-document visual review are complete. The Daniel Li-informed writing
pass strengthens concrete explanations, literature-to-method links and
findings-first result discussion while preserving all displayed mathematics,
tables, figures and citations. The subsequent paragraph-cohesion pass combines
short claims with their connected explanations and qualifications, including
four developed conclusion paragraphs instead of eight short blocks. It adds
no substantive material and leaves the mathematical explanation intact. All
129 workspace tests and 37 archive-bundled tests pass. The full evidence audit verifies all 22 available
figures, the 15 included figures and every displayed main-null table cell.
A clean build from the extracted source and experiment archives produces the same 86-page text with
no errors, undefined citations/references or overfull boxes. The named PDF,
source archive, experiment supplement and checksums are synchronized; the
current verification record is in `SUBMISSION_CHECK.md`.
The sample-size scope now requires both samples to contain at least 10
observations. Five scope regression tests supplement the nine figure-layout
tests. The original 3,111-configuration archive remains intact; the reported
2,760 configurations comprise 55,200,000 sampled table pairs. Plot assets and
their source selections are unchanged. Section 5.3 returns to a plain
family/count/description table, without bracketed arithmetic or the paragraph
about overlapping family counts. Two additional tests verify the plain table
counts and reject an incorrect count; all 16 figure, scope and table tests pass.

## 4. Scientific acceptance criteria

### The reader can follow the entire calculation

The main text must connect the observed count tables to the final p-values:
empirical probabilities, plug-in MI, the implemented bias correction,
first-order MI variance, shared standard error, Wald statistic, complete
variance sensitivity, component degrees of freedom, combined degrees of
freedom and Student t reference distribution. Each new quantity needs a plain-language
explanation of why it is needed.

Include at least three connected illustrations: a numerical construction of
P and Q, an observed count-table calculation of both tests, and an explanation
of the independence boundary. Check numerical illustrations against the code.
Explain the numerator and denominator dependence, the additional condition on
the variance sensitivity, and the implemented rules for invalid outputs.

For each Taylor expansion, identify the function, expansion variable and
expansion point. Display and calculate the zeroth, first and second terms
separately when second order is used. Differentiate the complete expression,
including probability factors outside logarithms. Explain what cancels and
why the surviving term matters. Use the user's preferred f(a), f'(a) and
f''(a)/2! presentation through a scalar perturbation path where appropriate.

The audit must distinguish identities, Taylor approximations, asymptotic
results and a working reference distribution. Specifically check independence
between samples versus independence within a table; V versus V/n; the
possibility of zero variance sensitivity despite positive MI variance; and
why the independence boundary needs second-order reasoning.

### The experiments can be understood and reconstructed

Explain the fixed joint tables, both sets of margins, changed cells, MI targets,
feasibility limits and sample sizes. Show why changing the true MI difference
is a design choice, while repeated sampling produces random observed estimates.

Retain all completed experiment families: the main square-table landscape,
different margins, baseline MI, locations of association, unequal samples and
both effect directions, wider feasible MI differences, rectangular tables,
alternative population construction, extreme skew, exact independence,
large-sample convergence and runtime. Document the actual finite sample and
skewness ranges, with at least 10 observations per population and no
expected-cell-count eligibility filter. Broad claims about all sample sizes or all tables
must not exceed those tested ranges.

Every displayed empirical quantity must identify its source configuration,
method, denominator and units in the evidence record. Reused display points
must not be counted as independent experiments. Inspect and strengthen the
existing evidence checker where it only tests file existence or selected
headline values; a passing partial check does not verify all manuscript claims.

### The comparison supports a balanced conclusion

Define false-positive rate, power, conservatism and invalidity before interpreting
the curves. Present H0 and H1 behaviour for corresponding regimes. Assess
closeness to the nominal 0.05 rate under H0, and interpret detection under H1
together with null calibration and validity. Explain that the power comparison
uses the fixed nominal threshold.

Report unconditional rejection and valid-result frequency, and use method-valid
or common-valid results where they explain a difference. Explain uncertainty
as Monte Carlo uncertainty at a fixed population pair and use paired comparisons
when comparing methods on the same samples. Keep individual regimes visible;
cross-regime averages must not substitute for them. Report actual runtime units,
the measurement setup and the O(rc) complexity of each calculation.

The conclusion must answer the two research questions and state the practical
limits of both methods. It must remain supported whether Expanded Welch helps,
hurts or closely matches Wald in a given regime. Explain a negative finding as
a scientific result with a defined scope.

## 5. Writing and presentation acceptance criteria

Adopt the examples' formal, explanatory tone and progression from a clear
question through method, evidence and interpretation. Use ordinary verbs and
define technical terms. Give each paragraph one main point; revise long
sentences that combine several claims. Review sentences longer than about
35 words as an editing aid, while allowing necessary mathematical qualifications.

Use TEEL as a flexible guide to paragraph structure: establish one main idea,
support it with evidence or an equation, explain why that support matters,
and connect it to the argument or next question. Separate a second main idea
into its own paragraph. An equation and its surrounding prose form one
explanatory unit; a derivation need not repeat a four-sentence template at
every step. Transitions must explain how successive ideas relate, not merely
announce what comes next. Avoid artificial linking sentences and unnecessary
repetition of the preceding paragraph.
Give prose paragraphs enough development to read as connected academic
arguments, rather than a sequence of isolated claims. One main idea need
not mean one sentence or one small supporting point. Combine adjacent short
paragraphs when they form a single explanation, comparison or recommendation;
keep a break for a genuinely new question or stage of the argument. Do not
pad the prose to reach a paragraph length. Short passages remain appropriate
when introducing or interpreting a displayed equation, and the abstract and
lists have their own structure.
Use consistent paragraph indentation: the first paragraph after either a
numbered heading or a bold mini-heading is unindented; subsequent new
paragraphs are indented. Text continuing after a displayed equation remains
part of its existing paragraph. Keep headings with their opening text.

### Prose clarity: explain the mechanism

Write for an undergraduate honours reader who knows basic calculus and
probability but has not studied this MI inference problem. Prefer a concrete
explanation of what changes, why it changes,
and what follows over a technical label that merely names the phenomenon.
Anchor causal claims to the relevant equation or comparison. Do not use vague
shorthand such as "the denominator is random" when both methods estimate a
denominator; say which quantity varies and how that affects the result.
Avoid contrasts that imply an incorrect property of the baseline method.
Name statistical objects fully: use "Student t distribution" instead of
"Student" alone, and name the distribution when discussing its p-value or
rejection cutoff. Apply the same rule to normal and chi-squared distributions.

Keep the prose formal and confident, but not defensive or needlessly
abstract. Introduce jargon only when it helps and define it in ordinary
language. State a genuine assumption, approximation or limitation where it
matters, without repeating caveats around every sentence. A reader should
be able to tell exactly what a claim means and why it follows from the
preceding argument. Simpler wording must not weaken the statistical claim.
State the scientific question or result directly, using concrete subjects and
verbs. Avoid abstract commentary about how a method must be assessed when the
actual comparison can be stated plainly. Explain the point itself rather than
making the reader reconstruct it from a description of the reasoning process.
Delete framing or restatement that adds neither explanation nor evidence.
Keep useful intermediate derivation steps; do not add sentences to complete
a paragraph template or increase its length.

Omit incidental editorial and logistical commentary: notes about how the
document is presented, obvious workflow properties, and assurances about
rounding or numerical housekeeping. Retain numerical details that affect
the calculation, reproduction or interpretation. Explain approximations
positively through their purpose and conditions rather than disclaiming
stronger claims that the manuscript has not made.

Preserve the progression of the argument. Explain a technical detail where
the reader needs it to follow the next step; omit or relocate short digressions
that interrupt that progression. Detailed derivations remain appropriate for
central calculations, but background sections need only the detail that
supports their purpose. In sentences describing a connection, comparison or
change, name both quantities or methods explicitly instead of leaving the
reader to infer what is being connected or compared.

Peripheral technical distinctions may be left to an appendix
when they distract from the main argument. Keep the assumptions and
limitations that would change how a result is interpreted; readability is not
a reason to make a stronger statistical claim than the evidence supports.

### Derivation depth: use Section 2.3 as the model

The sampling-variance derivation in Section 2.3 is the preferred level of
detail for important mathematical arguments. Write for a reader who knows
basic calculus and probability but has not seen this MI calculation. Begin
with the quantity to be derived, why it matters, the assumptions needed, and
a short roadmap. Divide the argument into meaningful steps, not a continuous
block of formulas.

At each non-obvious step, show the intermediate equation and explain the
operation in words. For a Taylor expansion, give the general formula, name
the function and expansion point, identify the new value and its difference
from that point, then show the substituted terms. Make nested sums, changes
of summation order, product-rule terms, cancellations and uses of independence
visible instead of asking the reader to infer them. Distinguish approximate
steps from exact algebra after the approximation has been made. After a key
equation, say what it means and how it advances the derivation.

Expand an existing step when doing so saves the reader from reconstructing
algebra or carrying several quantities in memory; do not introduce additional
concepts solely to elaborate the explanation. In worked calculations, trace
one representative cell through the formulas before reporting full-table
totals. Keep the calculation beside its explanation rather than listing
unexplained numerical outputs.

This is a clarity standard, not a request to expand routine arithmetic or
repeat every point. Prefer a slightly longer equation to a new symbol that
the reader must remember, and keep enough detail to reconstruct the argument
without interrupting the main narrative.

Keep a dedicated contribution subsection near the end of the introduction so
the mathematical, methodological, empirical and practical contributions remain
clear in the examiner's mind. In the results chapter, do not stop after quoting
a rate or describing a curve: immediately explain why the result matters, what
comparison it supports and what it does not establish.

Each chapter opens with its purpose and connects to the next part of the
argument. Results sections use the same sequence: **question and essential
settings, figure, immediate discussion**. Keep captions short and descriptive,
identifying the comparison and any necessary panel guide. Put exact settings
and interpretation in adjoining body paragraphs so the reader can understand
each comparison without searching earlier subsections.

Keep figures within the text margins and visually proportional to the body
text. Single-panel plots usually need less width than multi-panel comparisons.
Choose sizes for readable labels and a balanced page, not to increase or
decrease the page count. Use shared three-column, two-column and single-panel
templates with the same printed panel height, typography, markers and line
widths. Export at the intended physical dimensions and include plots without
rescaling; equal overall figure widths are not the goal. Preserve the plotted
values, axis ranges and scientific interpretation when making presentation
changes.

Select the main figures because each answers a question and motivates the next,
not to exhibit the full grid in the main text. Put the first substantive
reading of each figure immediately beside it: null behaviour, change over the
alternative, validity and takeaway where relevant. Let the end of a section
synthesise across figures instead of repeating their first interpretation.
The appendices must contain the supporting comparisons needed to assess the
argument, without directing the reader to a codebase or external atlas. Avoid
duplicating the same numerical reading in the caption and the discussion.
Use supporting calculations, experimental details and additional results as
the three appendix roles. Do not repeat the central derivations already taught
in Chapters 2-4, or retain peripheral distributional proofs and alternative
methods merely because they were developed during the project. Present all
main null settings individually, alongside validity, and select supplementary
curves for the additional question each answers.
Use normal body typography for the discussion, without separate small-text
interpretation blocks.

The results and discussion should form one continuous explanation; the short
later implications chapter is for synthesis and limits, not a delayed first
discussion of plotted evidence. The conclusion should explicitly return to
the contribution and its impact, then state limitations and proportionate
future work. In the design chapter, explain the choices needed to reproduce
the main results; place exact grids, low-level algorithms and secondary
diagnostics in the appendices. Keep codebase administration in separate
internal project records.

The literature review should give the reader enough source-based context to
understand why this comparison is needed. Cite established nontrivial results,
methodological precedents and claims about what earlier papers did; do not
leave such claims unsupported merely because they seem familiar. Do not pad
the review with tangential papers or turn introductory definitions into a
citation list. This review and the method chapters should remain readable by
an honours student with basic calculus and probability.
Organise prior work around the problem it solves and the remaining calculation
needed here, rather than a sequence of author summaries. Keep the connection
visible between those earlier methods, the proposed adjustment and the
results that test it. In results paragraphs, state the finding before the
supporting rates when that order makes the comparison easier to follow.

Each panel represents one fixed regime with both methods. Preserve consistent
colours, distinguishable line styles and comparable axes; clearly identify any
calibration zoom. Use the true absolute MI difference in nats in the current
experiment description. State P and Q margins, table shape, sample sizes,
baseline MI, difference grid, construction, repetition count and the meaning of
markers and uncertainty. Keep software administration outside the manuscript.
Avoid headings or commentary that refer to old prompts or explain
abandoned presentation choices.

Inspect every final PDF page, including the front matter, all equations,
tables, figures, captions, contents lists, appendices and bibliography. Check
clipping, overlaps, tiny text, broken symbols, awkward page breaks and detached
captions. A successful LaTeX build is necessary but does not replace this review.

## 6. Deliverables and proof of completion

| Deliverable | Required contents | Evidence of completion |
| --- | --- | --- |
| Final thesis PDF | Full main argument, appendices, references and accurate front matter at exemplar-comparable length. | Page count, complete visual review and closed editorial findings. |
| LaTeX source package | Main source, chapter/appendix files, metadata, preamble, bibliography, all required figure assets and build instructions. | Successful build in a clean directory without relying on an undocumented parent-workspace file. |
| Experimental supplement | Complete atlas and the saved records needed to identify every plotted regime and quoted result. | Working links, complete source mappings, consistent units and denominators. |
| Scientific and source audits | Equation checks, checked worked examples, claim-to-source records and any resolved findings. | Relevant tests pass; every material audit finding has a disposition and supporting evidence. |
| Final acceptance record | T1-T8 status, final artifact locations, checks performed, dates and remaining author actions. | All required gates pass and personal statements are accurate. |

Use the existing `SCIENTIFIC_AUDIT.md`, `LITERATURE_SOURCE_CHECK.md` and
`SUBMISSION_CHECK.md` as the review records. Extend them where needed instead
of creating another collection of overlapping overview documents. Keep
`THESIS_REWRITE_PLAN.md` as the detailed chapter/evidence plan and this file as
the current goal and acceptance standard.

The existing figure export, evidence audit, mathematical tests and LaTeX build
commands are documented in `README.md` and `SCIENTIFIC_AUDIT.md`. Apply checks
at the scope of the changes: rerun relevant method tests after mathematical or
implementation changes, regenerate affected figures/macros after export changes,
and rebuild after manuscript changes. At final assembly, run the full relevant
verification set once on the final artifacts and retain the outcomes.

## 7. Execution and completion rules

Proceed with authorized writing and verification without repeated supervisor
approval rounds. When a scientific uncertainty can be settled with a focused
calculation or diagnostic, perform it and record the result. Preserve the
frozen experiment record; additional analysis must state its purpose and
provenance. Further experiments are warranted only when a specific remaining
claim cannot be resolved from existing evidence or mathematical checks.

Use the current metadata as the working basis. Personal acknowledgements and
final dates can be handled during final assembly; they do not stop the
scientific or editorial work. Do not fabricate a personal contribution,
source, result or verification outcome.

Mark the thesis goal complete only when the final artifacts satisfy T1-T8 and
the substantive acceptance criteria. A written plan, a long PDF or passing
selected tests alone is insufficient. If an author-only detail remains, state
that exact detail while completing all other authorized work.
