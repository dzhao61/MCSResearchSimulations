# Goal: complete the master's thesis

Set 15 September 2026. Working completion target: **22 September 2026**.
This is a proposed project schedule, not a University submission deadline.

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

### Agreed basis

- The user clarified on 15 September that there is no AI-use limitation for this task and that CSYS5061 is the wrong course. Its report length, assessment dates and AI restrictions do not apply to this thesis.
- Length and writing quality are benchmarked against the supplied Grace Yan, Michael Fang and Riley Jones theses, using the analysis in [EXEMPLAR_REVIEW_NOTES.md](EXEMPLAR_REVIEW_NOTES.md).
- The active manuscript and completed fixed-population experiments are the starting point. Existing verified work counts toward the targets below; it should be extended where incomplete.
- Routine writing, editing, verification and small diagnostic calculations can proceed autonomously. Supervisor consultation is not a prerequisite for each decision.
- The final research comparison is Normal Wald versus Expanded Welch. The central contribution is the derivation and careful evaluation of the proposed correction, including its limitations.

### Questions the thesis must answer

| Research question | Required evidence | Main location |
| --- | --- | --- |
| RQ1. How does uncertainty in the estimated MI variance lead to the proposed Welch-Satterthwaite adjustment? | Checked derivation, defined assumptions, implemented algorithm and worked calculations. | Chapters 3-4; Appendices A and D. |
| RQ2. How does Expanded Welch change false positives, detection and valid-result frequency relative to Wald? | Corresponding null and alternative regimes, individual curves, validity diagnostics and paired comparisons. | Chapters 5-6. |
| RQ3. How do margins, baseline dependence, sample imbalance and population construction affect that comparison? | Matched focused experiments with explicit settings for both P and Q, including sparse and larger-alphabet cases. | Chapters 5-7. |
| RQ4. Do problems diminish with more data, what does the adjustment cost, and what should a practitioner conclude? | Fixed-population convergence, per-regime runtimes and synthesis of calibration, power and validity. | Chapters 6-8. |

## 2. Length and depth benchmark

The following lengths were checked against the supplied PDFs and their tables
of contents on 15 September. Main text means Introduction through Conclusion,
including its figures and tables, before references and appendices.

| Thesis | Main text | Complete PDF |
| --- | ---: | ---: |
| Michael Fang | 58 pages | 75 pages |
| Grace Yan | 65 pages | 126 pages |
| Riley Jones | 87 pages | 104 pages |
| Current Welch-MI manuscript | About 61 pages | 88 pages |

**Length target:** a main text within the observed **58-87-page range**, with
**65-75 pages as the working centre**. The complete PDF should be comparable to
the examples' **75-126 pages**; around 85-110 pages is a useful planning
estimate, depending on the necessary appendices. The current draft is already
within the observed range, so length alone does not justify adding material.

Use a consistent A4 layout with readable body text, equations and figures.
Keep normal thesis typography; do not change margins, font size, spacing or
figure placement merely to meet a page count. Do not add repetitive explanation
or unrelated literature to reach a numerical target. Record a word count as a
secondary diagnostic using the same counting method across revisions; no
unverified word limit is imposed.

### Working chapter allocation

These allocations guide balance and sum to approximately 70 main-text pages.
Move space between chapters when the explanation requires it.

| Chapter | Working pages | Required purpose |
| --- | ---: | --- |
| 1. Introduction | 4 | Establish the problem, four research questions, contributions and scope. |
| 2. Background and related work | 10 | Teach the necessary concepts and locate the contribution in verified prior work. |
| 3. Normal Wald comparison | 7 | Define the data, estimates, bias correction, variance, statistic and reference. |
| 4. Expanded Welch derivation | 11 | Derive the variance sensitivity and degrees of freedom, with intuition, worked calculations and assumptions. |
| 5. Experimental design | 9 | Explain concrete population construction, controlled factors, sampling and evaluation. |
| 6. Results | 20 | Present the landscape and focused comparisons, with calibration, power, validity and runtime. |
| 7. Discussion | 7 | Answer the questions, interpret tradeoffs, explain limitations and identify justified next research steps. |
| 8. Conclusion | 2 | State what was established and the resulting practical recommendation. |

## 3. SMART targets

Each target identifies a specific outcome, measurable acceptance evidence and
a due date. The work is achievable from the existing manuscript, implementation
and completed simulations. Its relevance is the reader's ability to understand,
reproduce and assess the thesis's scientific argument.

| ID | Specific outcome | Measurable acceptance criterion | Due |
| --- | --- | --- | --- |
| T1 | Agree the scope and exemplar benchmark. | Record all three exemplar lengths, the chapter allocation, four research questions and the evidence each requires. Remove the unrelated course restriction from active notes. | 15 Sep |
| T2 | Finish the mathematical explanation. | Check every central equation against an independent derivation and the implemented estimator. Define every substantive symbol at first use; label all Taylor expansions and distributional approximations. Verify the worked examples and relevant mathematical tests. | 16 Sep |
| T3 | Finish the literature argument. | Map every substantive prior-work and novelty claim to an inspected source and location. Verify every cited bibliography entry; resolve or explicitly narrow any unsupported claim. Cover MI estimation and variance, related information comparisons, Welch-Satterthwaite theory, simulation construction and the independence boundary. | 17 Sep |
| T4 | Complete the experimental design chapter. | Account for every frozen experiment family and all 3,111 unique configurations, 534 population pairs and 20,000 replicates per configuration. Explain P and Q construction with a numerical example and distinguish fixed population differences from sample randomness. Reconcile all repeated design values with the protocol. | 18 Sep |
| T5 | Complete the results and interpretation. | Give all four research questions an explicit answer tied to equations, figures or saved results. Include every experimental family; preserve access to every individual regime in the atlas. Verify all numerical claims and every included plot, initially 22 thesis figures, against exact source rows. | 19 Sep |
| T6 | Complete the substantive and language edits. | Review every chapter and appendix once for scientific coherence and once for readability. Resolve every material issue found in those passes. Check notation, equation explanations, repeated settings, terminology and parallel presentation across all experiment sections. | 20 Sep |
| T7 | Complete technical and visual verification. | Build from a clean copy of the final source package; obtain zero build errors, undefined citations/references, missing figures or overfull boxes. Inspect every rendered page at its final size, resolve visual defects and rerun the relevant evidence checks after final changes. | 21 Sep |
| T8 | Deliver the final thesis package. | Provide the final PDF, self-contained source, bibliography, figures, experiment/evidence index, reproduction instructions and completed acceptance record. Include accurate front matter with no editing placeholders or invented personal attestations. All material findings must be resolved before marking the goal complete. | 22 Sep |

T1 establishes the agreed target. T2 and T3 can proceed together; T4 and T5
must remain consistent with the final mathematical and evidence checks. T6-T8
review the assembled work. If a stage uncovers a scientific error, fix and
recheck the affected material before proceeding. Record any revised work date
and reason; the target date does not relax the acceptance criteria.

Current status: **T1-T3 completed on 15 September 2026; T4-T7 completed on
16 September 2026. T8 is assembled, with only the author's signature and date
on the declaration outstanding.** T2 evidence is recorded in
`SCIENTIFIC_AUDIT.md`: the mathematical
tests pass, both worked examples are independently reproduced, all Taylor and
distributional approximations in the method chapters are identified, and the
revised 88-page PDF builds without undefined references, citations or overfull
boxes. T3 evidence is recorded in `LITERATURE_SOURCE_CHECK.md`: all 15 sources
cited by the active manuscript have a source and claim disposition, the newly
identified Moddemeijer (1999) variance paper and Berrett--Samworth construction
precedent are incorporated, and the contribution remains explicitly narrower
than a first-priority claim. T4 reconstructs the frozen protocol exactly and
accounts for all 4,001 display slots, 3,111 unique configurations, 534
population pairs and 62,220,000 sampled table pairs. T5 regenerates and checks
all 22 thesis figures against independently selected source rows, verifies every
reported result in Chapter 6, and retains all individual regimes in the
companion atlas. T6 records a separate scientific-continuity and readability
disposition for every active chapter and appendix in `SUBMISSION_CHECK.md`.
T7 then built the final 88-page A4 manuscript from a fresh source copy, with
zero errors, undefined citations or references, missing assets, and overfull
boxes. All 28 relevant tests and the complete evidence audit pass, and all 88
rendered pages have been inspected. The final PDF, source archive and
experimental supplement are assembled under `deliverables/`; T8 can close
when the author signs and dates the declaration.

## 4. Scientific acceptance criteria

### The reader can follow the entire calculation

The main text must connect the observed count tables to the final p-values:
empirical probabilities, plug-in MI, the implemented bias correction,
first-order MI variance, shared standard error, Wald statistic, complete
variance sensitivity, component degrees of freedom, combined degrees of
freedom and Student reference. Each new quantity needs a plain-language
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
skewness ranges, including n=1 stress cases and the absence of an expected-cell-
count eligibility filter. Broad claims about all sample sizes or all tables
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

The conclusion must answer the four research questions and state the practical
limits of both methods. It must remain supported whether Expanded Welch helps,
hurts or closely matches Wald in a given regime. Explain a negative finding as
a scientific result with a defined scope.

## 5. Writing and presentation acceptance criteria

Adopt the examples' formal, explanatory tone and progression from a clear
question through method, evidence and interpretation. Use ordinary verbs and
define technical terms. Give each paragraph one main point; revise long
sentences that combine several claims. Review sentences longer than about
35 words as an editing aid, while allowing necessary mathematical qualifications.

Each chapter opens with its purpose and connects to the next part of the
argument. Results sections use the same sequence: **question, figure, exact
specifications, interpretation**. Figure captions or adjoining specification
tables repeat all essential settings so the reader can understand them without
searching earlier subsections. The repetition should serve interpretation.

Each panel represents one fixed regime with both methods. Preserve consistent
colours, distinguishable line styles and comparable axes; clearly identify any
calibration zoom. Use the true absolute MI difference in nats in the current
experiment description. State P and Q margins, table shape, sample sizes,
baseline MI, difference grid, construction, repetition count and the meaning of
markers and uncertainty. Keep long software details in the reproducibility
material. Avoid headings or commentary that refer to old prompts or explain
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
| Final acceptance record | T1-T8 status, final artifact locations, checks performed, dates and remaining author actions. | All required gates pass; personal statements are accurate and any required signature is supplied by the author. |

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

Use the current metadata as the working basis. Personal acknowledgements,
final dates and any author signature can be handled during final assembly;
they do not stop the scientific or editorial work. Do not fabricate a signature,
personal contribution, source, result or verification outcome.

Mark the thesis goal complete only when the final artifacts satisfy T1-T8 and
the substantive acceptance criteria. A written plan, a long PDF or passing
selected tests alone is insufficient. If an author-only detail remains, state
that exact detail while completing all other authorized work.
