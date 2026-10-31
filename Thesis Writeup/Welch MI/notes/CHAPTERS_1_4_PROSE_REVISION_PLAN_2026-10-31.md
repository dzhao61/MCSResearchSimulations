# Applying the prose guidelines to Chapters 1–4

31 October 2026 · Planning update only. No manuscript edits are made by
this review; existing working-tree revisions are preserved.

Use the [consolidated prose guidelines](RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md)
and the existing research-writing preferences. The completed Chapters 5–7
revisions supply examples of reading order, explanatory relationships and
sentence continuity. Their result-discussion structures should not be
imposed on an introduction, literature review or derivation.

## Objective and boundaries

Make the existing argument easier to follow by connecting related prose,
clarifying referents and removing genuine repetition. Preserve the depth
of the mathematical explanation, the scientific content and the established
roles of the chapters. Do not broaden the literature, add experiments,
change methods, reduce algebra or introduce new notation.

The current source uses RQ1 for approximation accuracy, RQ2 for false-positive
rates and RQ3 for nominal and calibrated power. It also already contains
some of the sentence improvements identified by the earlier audit. Use the
current source as the baseline for any future pass, not an archived passage
or a sentence-count table from a preceding PDF. This planning work does not
request or perform a rebuild.

## Lessons to transfer from Chapters 5–7

The [expanded guide](RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md)
contains the full retrospective, before/after examples and editing rules.
The transferable changes have six levels:

1. **Reading order:** state the question and essential conditions before
   the calculation or claim that depends on them. Section 6.4's selection
   context moved ahead of the results for this reason.
2. **Paragraph purpose:** complete one explanation before switching to a
   new comparison. Figure 6.1's row paragraphs are an example of organising
   around the reader's question, not a universal paragraph-size template.
3. **Explanatory links:** keep the result with its immediate reason or
   consequence, or carry a named quantity across a necessary sentence break.
4. **Mechanism:** explain which quantity changes and how that produces the
   result. In a derivation, the corresponding task is to explain why a step
   is valid and what it supplies for the next step.
5. **Evidence and memory:** keep definitions and evidence close to their
   use, select rather than recite numerical comparisons, and retain tables
   that distinguish easily confused objects.
6. **Restraint:** remove redundant framing, preserve useful short steps,
   and accept an edit only when the paragraph becomes easier to understand
   without changing the scientific claim.

Sentence length is one symptom to investigate. It is not the organising
principle of the revision.

## What the sentence comparison establishes

The 31 October audit found shorter complete prose sentences in Chapters
1–4 than in the sample introductions, background and technical passages.
Those counts describe the audited PDF, not a fresh measurement of the
current working source.
However, derivation steps, definitions and chapter outlines have different
functions from extended interpretation paragraphs. Counts locate review
opportunities; they do not establish that any particular sentence is poor.

The main Chapter 1 argument is closer to the samples than its whole-chapter
count suggests. Chapter 2 retains many short prose sentences even outside
Section 2.3. Chapter 3's compact assumptions and definitions explain part
of its short-sentence share. Chapter 4's shortest sentences often mark
valid mathematical steps or state the decision in the worked example.

The Section 2.3 benchmark itself has many short sentences. Its clarity is
a reason to preserve it, not evidence that it should be lengthened to match
the samples. The comparison used body text from the three sample PDFs,
matching by chapter purpose and excluding display-linked sentences from
the main prose counts. It is not a controlled measure of reading difficulty
or a comparison of marks.

## Review plan by chapter

| Chapter | Review intensity and priority | Candidate improvements | Preserve explicitly |
| --- | --- | --- | --- |
| 1: Introduction | Light pass after the conceptual terminology in Chapters 2–3 has been checked. | Check the existing sampling-variation explanation and evaluation summary in context; remove genuine restatement while keeping the scientific comparison explicit. | The three research questions, contribution claims and qualifications, scope assumptions, equal MI versus equal tables, and short outline sentences where useful. |
| 2: Background and literature | Main review priority in Sections 2.2 and 2.4; lighter checks in 2.1 and 2.5. | Check that existing integrations read smoothly; connect each cited approach to the relevant uncertainty or testing problem; carry a named quantity into the explanation of why a different method needs another input. | Definitions, citations, bias-correction conditions, the distinction between sampling and posterior uncertainty, the distinction between equal MI and equal distributions, and necessary unit/support conventions. |
| 3: Test overview and baseline | Moderate local pass. | Improve transitions from assumptions to the estimator, from the estimator to uncertainty, and from the shared statistic to the different reference distributions. | The separate assumptions, signed difference, null/alternative, correction and cancellation rules, variance definitions, Table 3.1, and p-value calculation. |
| 4: Detailed derivation | Selective pass after Chapters 2–3; focus on motivation, interpretation and transitions. | Connect moment matching to the quantities it needs; make referents explicit when moving between a target, approximation and estimate; improve the prose introducing substitutions and the conclusions drawn from results. | Every important intermediate mathematical step, exact/approximate distinction, the Taylor mapping, independence and positivity assumptions, both tables, the worked example and the validity/near-independence qualifications. |

## Passage-level candidates and decisions

These are locations to inspect, not pre-approved replacements. An edit must
show a clear reading benefit in its surrounding paragraph. A candidate
already resolved in the current source should be marked complete and left
alone.

### Improvements already present in the current source

| Location | Current improvement | Consequence for the next pass |
| --- | --- | --- |
| Chapter 1 opening | Observed counts, sampling variation and unequal sample MI under equal population MI are connected in one sentence. Usable p-values are included with the evaluation measures. | Retire the earlier proposals to make these joins; check their paragraph context only. |
| Section 2.2 | The NSB estimator is named within its explanation, and the zero-cell convention is connected to empty cells' contribution. | Preserve these integrations; inspect transitions between the different estimation approaches. |
| Section 2.4 | The opening connects the two variance contributions to the standard error. The later discussion distinguishes uncertainty in MI from uncertainty in its estimated variance. | Check the progression into the additional moment-matching input, not whether these definitions exist. |
| Chapter 3 | Taking the square root is connected to the meaning of the standard error; the p-value is explained through the reference distribution and two tails. | Retain the mathematical steps and review adjacent transitions. |
| Section 4.1 | Moment matching is explicitly a choice of degrees of freedom; the rescaling cancellation is displayed; the first-order mean is explained through mean-zero cell errors. | Protect these expanded explanations. The previous confusing compression is not a model to restore. |

These observations come from the current source. They do not establish
which previous turn introduced each edit or imply that the PDF already
contains all of them.

### Chapter 1

Read the opening through the research questions as one argument: the
scientific comparison, sampling uncertainty, the difficulty with the
baseline, the proposed change and what its evaluation must establish.
The empirical-estimation setup and usable-p-value reminder are already
integrated. Check whether any remaining transition repeats the previous
paragraph instead of advancing that argument. Retain concise hypothesis
interpretation and the chapter outline when their separate emphasis helps.

Do not expand the Introduction into a preview of all diagnostic mechanisms.
Its task is to establish why the comparison matters, the unresolved problem,
the contribution and what the three questions ask.

### Chapter 2

In Section 2.1, retain the progression from information content to entropy,
pointwise MI and average MI. Treat each displayed definition and its
interpretation as a unit. Only join short surrounding prose when it
clarifies a relationship without making the definition harder to find.

In Section 2.2, check how the discussion moves from plug-in estimation and
leading bias correction to sparse-sample and Bayesian approaches. The NSB
name is already integrated. Each approach should leave the reader knowing
what is estimated or corrected and why its relevant limitation matters
here. A cited paper does not need a separate paragraph solely because it
is a new citation. Conversely, keep sampling uncertainty and posterior
uncertainty distinguishable when the discussion changes between them.

In Section 2.4, check the whole sequence from the Normal Wald standard
error through ordinary Welch and Satterthwaite to the MI-specific input.
The useful relationship is between an existing uncertainty estimate and
the additional sampling-variance information required for moment matching.
The former standalone “This supplies a standard error” wording has already
been replaced. Preserve the two variance definitions and make their roles
easy to carry through the comparison.

Review the current Hutcheson comparison for any remaining repetition of
its sample-size assignment and check the connection to the MI-specific
quantity still required.
Retain its equation and the qualifications distinguishing entropy components
from the connected row, column and joint entropy errors in MI.

Section 2.5 already develops the contribution in relatively connected prose.
Leave it largely intact unless the preceding edits reveal an actual repeated
claim or terminology mismatch.

Section 2.3 is excluded from the first implementation pass. Preserve it
byte-for-byte as the agreed derivation benchmark. This is a proposed scope
choice based on its successful exposition, not a request for extra approval.
Only revisit it later if a concrete reading problem is demonstrated.

Keep literature transitions tied to the question being reviewed. A change
from estimating MI to testing equality of MI needs a clear conceptual
connection; adding “Furthermore” between summaries of papers is insufficient.
Preserve the hypotheses each cited method addresses, particularly the
distinction between equal MI and equality of complete distributions.

### Chapter 3

Keep the assumption list easy to locate. A positivity assumption and its
consequence for the first-order variance may need adjacent sentences rather
than a single sentence containing all exclusions and qualifications.
The bias correction, equal-sample cancellation and unequal-sample case should
remain distinguishable steps.

Review surrounding prose rather than merging short mathematical definitions.
Follow the calculation once in its existing order: counts and assumptions,
corrected MI difference, estimated variance contributions, standard error,
shared statistic and reference distribution. At each transition, check that
the previous quantity's role is stated before the next quantity is used.
Keep the meaning of a p-value connected to the reference distribution and
the two-sided tail calculation. Preserve the separate rejection decision
where it makes the calculation easier to use.

### Chapter 4

Review Section 4.1's motivation and transitions around the now-explicit
moment-matching steps. Preserve the distinction between choosing a scaled
chi-squared approximation and proving an exact sampling law. Do not shorten
the displayed variance calculation or the fixed-sample-size rescaling
merely because their explanations contain short sentences.

In Sections 4.2–4.3, clarify the subject of prose that introduces a
substitution or explains its result. Retain explicit cancellations,
reindexing, conditional means, covariance/independence arguments and all
necessary algebra. Statements such as “These four contributions cancel”
and “Here set …” remain unless a specific defect is shown.

In Section 4.4, retain the worked calculation and distinct Normal Wald and
Expanded Welch outputs. Do not combine several numerical quantities into
long sentences. The short final decision can remain separate.

In Section 4.5, review connections among independence, vanishing linear
weights and the need for quadratic terms. Preserve the conditions and
distinguish what the derivative establishes from the finite-sample
distributional approximation.

Table 4.1 stays. Its sampling-moment target, population first-order value
and sample-based estimate are used later and are necessary to interpret
the experimental comparisons. No removal or collapse of those quantities
is included in this plan.

The chapter's prose should let a reader identify, at each stage, whether
the calculation is an exact derivative, a first-order approximation, a
moment-matching choice or a sample substitution. Use these distinctions
where the argument changes status; do not append the same caveat to every
equation. For a cancellation or substitution, keep the mathematical reason
beside the displayed step that uses it.

## Implementation sequence

1. Preserve the current working sources, including existing staged and
   unstaged changes, and record the equations, displays,
   citations, labels, values and protected Section 2.3 before editing.
2. Revise Chapter 2 outside Section 2.3 in small coherent blocks, starting
   with the literature discussion and its explanation of the remaining
   methodological need. Reread across each block's boundaries.
3. Review Chapter 3 against those definitions, improving transitions without
   changing its calculation order or assumption structure.
4. Make the light Chapter 1 pass against the clarified concepts and the
   current RQ1–RQ3 mapping. Avoid importing technical detail from later
   chapters into the introduction.
5. Review Chapter 4's explanatory prose against the established terminology.
   Finish by checking that each derivation still works as a guided sequence.
6. Reread Chapters 1–4 as a progression from question to foundations,
   baseline and contribution. Check relevant Chapter 5–7 usage for
   consistency without automatically starting another rewrite there.

Within each block, record the reading difficulty and proposed action before
editing: keep, join, split, move or delete. Use the guide's decision table.
Review the revised paragraph with its neighbours and record why the change
helps; if the only justification is that the sentence becomes longer, do
not make it. Blocks already clear in the current source need no rewrite.

## Acceptance checks and stopping rule

Accept a revision when it resolves a specific inference burden and preserves
or improves the passage's clarity as a whole. Reject or undo a join that
adds several numerical cases, delays the main clause, nests qualifications
or makes a mathematical step harder to locate. Retain short sentences that
perform distinct jobs even if the sentence-length distribution changes little.

Verify that Section 2.3, displayed equations, table/figure contents, numerical
values, scientific qualifications, citations and labels are preserved. Check
references, terminology, TeX syntax and paragraph style. A preserved formula
alone does not establish a preserved claim: reread the prose for changes in
assumptions, causality or approximation strength.

No sentence-count, paragraph-length, punctuation-frequency or page-count
target applies. No global search-and-replace, notation simplification,
figure redesign, literature expansion or appendix reduction is part of this
plan. Once the demonstrated problems are resolved and checks pass, stop
editing. Rebuild only when explicitly requested, then inspect changed PDF
pages for display order, line breaks and new layout problems.

## Review basis

The [general guide](RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md)
summarises the completed revisions and the rules they support. Detailed
implementation records are
[the Chapters 5–7 sentence review](CHAPTERS_5_7_SENTENCE_FLOW_2026-10-31.md),
[the Chapter 6 continuity review](CHAPTER_6_CONTINUITY_2026-10-31.md),
[the punctuation review](CHAPTER_6_PUNCTUATION_2026-10-31.md), and
[the Section 6.4 rewrite](SECTION_6_4_FRESH_REWRITE_2026-10-31.md).
Historical records retain their original numbering; current manuscript
revisions use the three peer research questions.
