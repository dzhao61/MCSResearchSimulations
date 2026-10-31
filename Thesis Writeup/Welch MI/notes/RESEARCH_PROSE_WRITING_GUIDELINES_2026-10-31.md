# Research prose: reading order, explanation and sentence construction

Consolidated on 31 October 2026 from the revisions to Chapters 5–7, the
Section 6.1.1 discussions, the application rewrite and the comparison with
the three sample theses. Use alongside the workspace research-writing
preferences and the [Chapter 6 results guide](CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md).
The latter retains detailed guidance for figures and experimental results.
This guide supplies the transferable principles for other chapter types.

The purpose is to reduce what a first-time reader must infer, remember or
look up. Sentence length, paragraph length and punctuation frequency are
diagnostics, not targets. A successful edit makes a particular relationship
easier to follow while preserving the scientific claim. It need not make
the sentence longer, the paragraph larger or the manuscript shorter.

Expanded on 31 October after reviewing the implementation records, archived
before-text and current Chapters 5–7. The examples below distinguish actual
sentence edits from broader changes to the order of explanation. The
Chapters 1–4 plan is checked against the current working sources, which
already contain some improvements; an old example is not a standing reason
to edit a passage again.

## What changed in Chapters 5–7

The following summarises the accumulated exposition changes, rather than
claiming that each was made in the final sentence-level pass. Later passes
were deliberately lighter where earlier revisions had already clarified
the argument. The current research-question mapping is RQ1 for approximation
accuracy, RQ2 for false-positive rates and RQ3 for power.

| Area | Changes made | Reading difficulty addressed |
| --- | --- | --- |
| Chapter 5: population construction | Explained category frequencies, independent and copying choices, fixed margins, cell probabilities and target-MI search in sequence; retained the worked example. Later edits connected definitions and settings to their immediate consequences. | The reader could otherwise know the formula without understanding what population it constructs or what changes when a parameter changes. |
| Chapter 5: evaluation | Distinguished a variance coefficient, MI sampling variance and the sampling variance of the coefficient estimate; explained repeated-table calculations, moment targets, independent fitting, fixed alternatives and threshold calibration. | Similar symbols and repeated-sampling operations could be confused, while procedures could appear before their purpose was clear. |
| Chapter 6: display introductions | Defined local populations, settings, axes, ratios, reference values, uncertainty and validity rules before interpreting the displays. Kept necessary reminders near their use. | The reader had to remember settings or infer what a ratio or missing point represented. |
| Chapter 6: interpretation order | Organised Figure 6.1 into three developed row paragraphs; finished each figure comparison before introducing a different display. Kept bias and standard-error evidence beside the rejection patterns it explains. | Unfinished comparisons and jumps between displays required readers to retain several arguments at once. |
| Chapter 6: mechanisms | Explained peaks, troughs and recovery through changes in counts, means, variances, ratios, estimated degrees of freedom and cutoffs. Distinguished the population prediction from the average sample-based prediction. | Naming sparsity or approximation error alone did not explain the complete shape or the difference between populations. |
| Chapter 6: calibration | Explained why the common MI can vary under the equal-MI null, then distinguished lower/upper fitting nulls, evaluation nulls and fixed alternative samples. Presented decisive cross-null evidence in the main discussion. | A calibrated-power comparison could be misread as general false-positive control or a stable advantage across the whole null. |
| Chapter 6: application | Rebuilt Section 6.4 around the questions, data, count tables, exploratory family, estimates, test calculation, month result, weekend result and scope. Explained the missing January/April records and kept the adjusted month conclusion with its interpretation. | The reader could encounter unexplained table dimensions or have to revisit a result after discovering the multiple-comparison context. |
| Chapter 7: synthesis | Connected the sensitivity calculation to moment matching, findings to their mechanisms, nominal power to null rejection, and conclusions to their tested settings and limits. | A list of accurate findings could still leave the reader to assemble the contribution and practical judgment. |
| Across Chapters 5–7: sentence flow | Integrated detached consequences, definitions, setting reminders and cross-references where they completed one relationship; named the changing quantity in the next sentence. Retained or restored separate steps when joins became crowded. | Short sentences could sound choppy, while indiscriminate merging could create long sentences with several competing jobs. |
| Across Chapters 5–7: paragraph continuity | Grouped sentences that complete one explanation, while retaining separate paragraphs for distinct panels, settings and calculations. In the calibration discussion, replaced fragmented introductions and isolated reminders with connected explanations of the question and design. | A paragraph break could make a consequence seem unrelated to its cause; a large paragraph could also obscure a change of question. |
| Chapter 6: punctuation | Recast colon-led announcements and semicolon-attached reminders as explicit relationships, retaining useful lists, equations, parallel comparisons and independent sentence breaks. | Punctuation could join two clauses without explaining their relationship or merely disguise choppy prose. |
| Chapter 6: tables and numerical comparisons | Aligned diagnostic and rejection tables by setting; cross-tabulated whether Wald was above or below 5% against whether Welch moved closer to or farther from 5%; replaced the application's simple variable-mapping table with local definitions. | Readers had to remember row order, reconstruct a comparison from totals, or consult a display for a definition that fitted naturally in prose. |
| Across Chapters 5–7: economy and evidence | Removed repeated framing and recap; retained useful tables and algebra; removed reader directions to unsubmitted evidence while preserving essential support within the thesis. | Extra words and inaccessible pointers could interrupt the assessed manuscript's argument. |

Table restructuring, typography and float placement also improved the final
reading experience. Those choices are assessed separately from sentence
construction: a useful table should remain even when its entries can be
mentioned in prose, and its position must follow the argument. Do not undo
the agreed typography or shrink displays to make revised prose fit.

### Concrete examples of the changes and their transferable lessons

The following excerpts are from the preserved sources and current chapter
text, with LaTeX formatting removed. They illustrate editing decisions,
not wording to repeat throughout the thesis.

**Connect a procedure to its purpose.** Chapter 5 previously opened:

> The simulations draw count tables from populations with known MI. This
> allows us to measure errors in the estimated MI difference and its
> standard error, and to count false positives when the population MI
> values are equal.

It now opens:

> The simulations draw count tables from populations with known MI,
> allowing us to measure errors in the estimated MI difference and its
> standard error, and to count false positives when the population MI
> values are equal.

The edit keeps the known-population design and what that design permits
within one explanatory relationship. It removes a detached “This allows”
without adding a new claim or another example.

**Make the reason for a check part of its description.** Chapter 5 previously
said:

> Each calibration is also evaluated at both null settings. Matching
> rejection at one equal-MI setting does not ensure the same false-positive
> rate elsewhere under equal MI.

The revised passage says:

> We also evaluate each calibration at both null settings because matching
> rejection at one equal-MI setting does not ensure the same false-positive
> rate elsewhere under equal MI.

The reader learns why the second check is needed as it is introduced.
The subsequent appendix reference still has its own function and need not
be attached to the same sentence.

**Use sentence succession to develop a mechanism.** In Chapter 7, a
detached reminder that calibration leaves a distortion unchanged was
integrated with the opening claim:

> Changing the cutoff leaves errors in the estimated MI difference
> unchanged, so calibration does not remove the initial power dip at B.
> At the first alternatives, the increasingly negative true difference
> partly cancels the persistent positive estimation bias, moving the
> sampling mean of the estimated difference towards zero. Rejection
> therefore initially falls even though the population MI values move
> farther apart.

Here “the estimated difference” renders the source's mathematical symbol
in words. The passage retains three sentences because they have different
jobs: identify the remaining problem, explain the changing sampling centre,
and connect that change to rejection. The subject of each sentence carries
forward a quantity or consequence established in the preceding sentence.

**Repair the order before repairing the rhythm.** Section 6.4 moved the
scientific questions and population definitions ahead of the data details,
and the six-comparison selection context ahead of the results. The month
interpretation now includes both the unadjusted and adjusted conclusion.
These changes prevent a later condition from forcing the reader to
reinterpret an earlier result; longer sentences alone would not do that.

**Keep a short sentence when it separates necessary objects.** Chapter 5
still distinguishes “One observation records an (X,Y) outcome” from the
explanation of one simulation repetition. Figure 6.1 still states “A ratio
of one indicates agreement.” Each gives the reader a useful reference
point. A sentence-length audit is not a reason to bury either definition.

**Use an existing symbol when it reduces repetition.** The Figure 6.1
introduction uses the previously defined margin profiles \(m_k(0.7)\) and
\(m_k(0.8)\), explicitly attached to P and Q. This compact reminder removes
a repeated verbal definition while making the populations distinguishable.
It does not justify introducing a new abbreviation solely to shorten prose.

## 1. Decide the reading order before polishing sentences

For a section, establish its question and the sequence needed to answer it.
Introduce the objects and essential conditions before using them. Present
the calculation or evidence, explain what follows, and state the limit where
it affects interpretation. The reader should not have to reinterpret an
earlier result after discovering an essential condition much later.

This sequence depends on the chapter's purpose:

- An introduction moves from the scientific comparison to the difficulty,
  proposed contribution, questions and scope.
- A literature discussion connects each existing approach to what it
  estimates or tests, its relevant limitation and the remaining problem.
- A method explanation identifies inputs, assumptions, calculation and the
  meaning of the output.
- A derivation states the target and develops the necessary mathematical
  steps with their assumptions and interpretations.
- A result discussion introduces the comparison, follows its evidence and
  explains the finding with its relevant qualifications.
- A conclusion connects the contribution, evidence and resulting judgment.

These are reading needs, not compulsory paragraph templates. Do not insert
an extra roadmap, definition, caveat or summary when the passage already
provides it adequately.

## 2. Let each paragraph complete one explanatory task

A paragraph may introduce a construction, interpret one figure row, compare
methods or explain a limitation. Its sentences should develop that task
instead of switching to a second calculation or display halfway through.
Finish the task before moving to a new comparison that requires different
settings or quantities.

Use TEEL flexibly: identify the idea, support it, explain it and connect it
to the argument where a connection is needed. A displayed equation and the
surrounding prose form one unit. A short paragraph can be complete; a long
paragraph can be necessary for a coherent mechanism. Neither length is a
reason by itself to split or merge.

Figure 6.1's three row paragraphs work because each answers a different
question and completes its trends, mechanism and population comparison.
This does not establish a rule that every figure needs three paragraphs or
every subsection needs large paragraphs.

Paragraph continuity depends on how one sentence prepares the next. Start
with the object or result that the reader already knows, add the information
needed now, and use that information as the subject of the next step where
appropriate. For example, the sequence can move from an underestimated
variance to a smaller denominator, then to a larger absolute statistic and
its effect on rejection. Avoid repeatedly restarting with “This shows”,
“It is important” or “We next consider” when the scientific relationship
itself can supply the transition.

A paragraph's ending may state what its evidence establishes, explain a
limitation, or make the next question necessary. It need not repeat the
opening claim. Remove a generic closing sentence if the paragraph already
finishes its explanation; retain a specific consequence the reader needs.

## 3. Complete relationships within sentences where that helps

Keep a statement with its immediate cause, consequence, condition,
comparison or qualification when a sentence break would detach the second
part from the idea it explains. Choose the connector after identifying the
relationship.

| Relationship | Suitable construction | Precision check |
| --- | --- | --- |
| Established explanation | because | Does the derivation or evidence support the explanation? |
| Consequence | so, therefore | Does the preceding statement actually imply the consequence? |
| Changing condition | as, when | Is the changing quantity and its effect explicit? |
| Qualification | although, even when | Does the condition genuinely qualify this claim? |
| Comparison | whereas, while | Are both quantities or methods named and compared on the same basis? |
| Definition or role | relative clause or apposition | Is the referent clear, with no ambiguity about which quantity is being defined? |

For example, the Chapter 5 revision connects the simulation setup to its
purpose:

> The simulations draw count tables from populations with known MI,
> allowing us to measure errors in the estimated MI difference and its
> standard error, and to count false positives when the population MI
> values are equal.

The application similarly connects a coding fact to the table dimension:

> January and April have no recorded sessions, so each month table has
> ten rows for the recorded months and two columns for the purchase outcome.

These examples complete specific relationships. They do not justify
joining unrelated settings, results or numerical cases into one sentence.

## 4. Carry a named quantity into the next sentence

Begin from information already established when developing the next step.
Prefer a specific subject such as “the underestimated variance”, “the
larger cutoff” or “this sampling mean” to an isolated “this” when several
referents are possible. In a sequence of equations, identify what the next
substitution changes or what the next result permits us to calculate.

For example:

> The variance estimate is too small. For a fixed difference estimate,
> the smaller denominator enlarges the absolute statistic and can move it
> beyond the rejection boundary.

The sentence break separates the observed error from its effect on the
decision, while the repeated quantity supplies continuity. This is often
clearer than combining the entire mechanism into one sentence.

## 5. Retain short sentences with a distinct job

Keep a short sentence when it establishes a definition, states an important
finding, separates mathematical steps or prevents an overloaded comparison.
Review a short sentence for integration when it only names what the previous
sentence already explained, adds a detached reminder or repeats a result.

| Sentence type | Default review decision |
| --- | --- |
| “These four contributions cancel.” after the four contributions | Retain if it makes the cancellation and following equation easier to follow. |
| “Here set …” when mapping a Taylor expansion | Retain the explicit mapping; do not compress it to improve sentence statistics. |
| “Neither method rejects at the 5% level.” after the worked p-values | Retain as the distinct decision. |
| A new symbol or assumption | Define it clearly before use; integrate only if the definition remains immediately identifiable. |
| A sentence that merely gives the name of the method just explained | Consider incorporating the name into that explanation. |
| A detached reminder about units, populations or repeated calculations | Integrate where the information is needed, unless its importance warrants emphasis. |
| A necessary limit on inference | Keep explicit beside the claim; retain a separate sentence if that makes the limit more visible. |

After joining sentences, check for a crowded list, several numerical cases,
nested qualifications, a delayed main verb or two different explanatory
tasks. Restore a sentence break if the reader must hold too much at once.
Fewer short sentences is not an acceptance criterion.

## 6. Explain the mechanism at the right depth

Identify what changes, why it changes and what that change does to the
quantity being interpreted. For a ratio, consider both numerator and
denominator. For a test, distinguish errors in the estimated difference,
standard error and reference cutoff. For an average of sampled ratios,
do not substitute a ratio of average inputs without justification.

Explain the whole pattern that matters. A trough needs an explanation of
both its decline and recovery; a changing method ranking needs the relevant
fixed and changing quantities. Use existing evidence and retain uncertainty
about a mechanism when the diagnostics do not isolate it completely.

In earlier chapters, apply this principle to definitions and equations:
explain why the mathematical step is valid and what it achieves. Do not
introduce later experimental details merely to add a mechanism to a passage
whose purpose is defining a quantity or reviewing prior work.

Make the move from observation to explanation visible. “The ratio falls”
describes a pattern; “The ratio falls because the prediction decreases as
1/n while the observed variance decreases more slowly” explains the
calculation producing that pattern. The Figure 6.1 revision then explains
why rare-cell counts can make the observed variance behave that way, and
why the ratio recovers. A useful explanation connects the visible result,
the relevant calculation and the underlying sampling behaviour at the depth
the evidence supports.

Use “because” for a supported explanation, “therefore” for a consequence
that follows, and “is consistent with” or “helps explain” when the evidence
supports a contribution without establishing a complete cause. A smoother
sentence must not turn an observed association into a demonstrated cause.

## 7. Use punctuation for its actual function

Use a colon for a list, displayed equation or explanation that benefits from
an introduction. Use a semicolon for closely related parallel statements or
lists whose items contain commas. A full stop is appropriate when the next
statement has a distinct task or needs emphasis.

Do not attach a reminder or cross-reference with a semicolon merely to avoid
a short sentence. Do not replace semicolons mechanically with “and”,
“because” or “while”. The revised connector must express an existing
relationship without strengthening causality, adding contrast or changing
the scientific claim. Mathematical punctuation is a separate matter.

## 8. Keep scientific distinctions and necessary repetition

Retain population-versus-sample distinctions, target-versus-approximation
distinctions, exact-versus-approximate statements, independence assumptions,
validity rules, uncertainty and directional qualifications. Preserve “can”,
“approximately” and similar wording where it limits a claim meaningfully.

Repeated notation or a brief local setting reminder can reduce memory
demands. Delete repeated wording when it adds no definition, evidence,
mechanism, qualification or useful orientation. The aim is to remove
unnecessary inference and repetition, not to eliminate every repeated term.

The three component quantities in Table 4.1 remain necessary because the
target, population first-order approximation and sample-based estimate have
different roles in the analysis. Their distinction must survive any prose
revision. The table is not a proposed deletion under this guide.

Keep the thesis self-contained. Essential conditions and evidence belong
in the submitted text or appendices; the reader must not depend on an
unsubmitted supplement, codebase or internal archive.

### Reduce memory demands through placement and selective detail

Introduce the quantities, comparison and reference value before asking the
reader to interpret a display. Then keep the display close to the paragraphs
that use it, checking the final typeset order when a build is requested.
Keep complementary tables in a consistent setting order so readers can
compare them directly. Finishing one explanation before switching displays
is usually more useful than adding another summary table.

Use prose to select the important numerical comparison and explain what it
means; let the table supply the remaining values. Repeat a number when it
is needed for a calculation or a decisive contrast, not merely to narrate
every table entry. Retain local reminders such as the P/Q margin profiles
or the direction of a signed difference when otherwise the reader must
look back to interpret the result.

A table earns its place by making a comparison, calculation or distinction
easier to inspect. The two-dimensional rejection summary reveals how the
effect of the larger cutoff depends on whether Wald initially over-rejects
or under-rejects. Table 4.1 separates three similar mathematical objects
used later. Both serve an explanatory purpose different from the removed
application table that only mapped a few variables to their names.

### Choose the smallest edit that resolves the difficulty

| What the reader encounters | Preferred response | Check before accepting |
| --- | --- | --- |
| A claim followed by a detached reason or consequence | Join them if they form one manageable relationship. | The connector expresses the original logic and preserves its conditions. |
| Two short sentences that perform different mathematical tasks | Keep the break and strengthen the named connection if needed. | Each step remains easy to find and reconstruct. |
| One long sentence containing several cases or nested qualifications | Split at the change of task, carrying the relevant quantity forward. | The new sentence has an explicit subject and no orphaned condition. |
| A condition, definition or selection rule discovered after the result | Move it to the first point where interpretation depends on it. | The move does not leave an undefined term or interrupted explanation elsewhere. |
| Two paragraphs that each give half of the same explanation | Consider combining them or moving the consequence beside its cause. | The combined paragraph still answers one question. |
| A repeated recap, method name or generic announcement | Integrate a useful name; delete wording that adds no meaning. | No unique evidence, assumption or qualification is lost. |
| Many figures, numbers or table rows recited in prose | Choose the comparison needed for the argument and position the display beside it. | The decisive evidence remains visible and the reader can identify the other values. |
| A clear passage that only falls below a sentence-length threshold | Leave it alone. | No demonstrated inference burden remains. |

## 9. Review in context and verify the result

1. Read the subsection, preceding paragraph and following paragraph before
   editing individual sentences. State the question each passage answers.
2. Identify a demonstrated reading difficulty: an ambiguous referent,
   detached explanation, missing transition, unfinished comparison or
   repeated framing. Leave already clear passages alone.
3. Revise information order or paragraph organisation first when that is
   the source of the difficulty. Improve sentences within the settled order.
4. Reread for a clear main clause, identifiable changing quantities,
   manageable qualifications and visible mathematical steps.
5. Compare the claim, assumptions, signs, values, equations, citations and
   interpretation with the original. Check that an edit has not introduced
   an unsupported causal statement or a new result.
6. Run source consistency checks. When a rebuild is explicitly requested,
   inspect the actual prose/display order and page breaks in the PDF.

Sentence audits can identify places to reread. Compare like chapter roles
and distinguish complete prose from headings, list labels, captions, table
entries and equation lead-ins. Mathematical expressions need consistent
treatment, and counts remain approximate. Do not compare counts produced
under different extraction rules as though they measure an editing effect.

The proposed application to Chapters 1–4 is specified separately in the
[revision plan](CHAPTERS_1_4_PROSE_REVISION_PLAN_2026-10-31.md). This guide
does not itself implement those edits or request a PDF rebuild.

## Records supporting this consolidation

- [Chapter 5 exposition](CHAPTER_5_EXPOSITION_REVISION_2026-10-25.md):
  procedure, purpose, repeated sampling and calibration design.
- [Chapter 6 results rewrite](CHAPTER_6_RESULTS_REWRITE_2026-10-30.md)
  and [results guide](CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md):
  display introductions, complete comparisons and explanations of patterns.
- [Table presentation](TABLE_PRESENTATION_REVISION_2026-10-30.md) and
  [two-dimensional rejection summary](TWO_DIMENSIONAL_NULL_GRID_2026-10-30.md):
  comparisons made visible through table structure.
- [Paragraph continuity](CHAPTER_6_CONTINUITY_2026-10-31.md),
  [sentence flow](CHAPTER_6_SENTENCE_FLOW_2026-10-31.md),
  [punctuation](CHAPTER_6_PUNCTUATION_2026-10-31.md), and
  [Chapters 5–7 sentence review](CHAPTERS_5_7_SENTENCE_FLOW_2026-10-31.md):
  contextual edits and retained sentence breaks.
- [Section 6.4 reconstruction](SECTION_6_4_FRESH_REWRITE_2026-10-31.md):
  question, data, selection context, calculation, interpretation and scope.
- [Examiner reading boundary](EXAMINER_READING_BOUNDARY_2026-10-31.md):
  essential evidence within the submitted manuscript.

These records describe successive versions and retain historical display
numbering. The transfer principles above concern the resulting explanation,
not a requirement to repeat every previous edit in another chapter.
