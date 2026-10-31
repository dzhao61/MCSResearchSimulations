# Chapter 6 results writing guidelines

Established on 30 October 2026 from the revision and discussion of Section
6.1.1. Apply these alongside the workspace research writing preferences and
the thesis `AGENTS.md`. Section 2.3 remains the benchmark for derivation depth.
This guide does not itself request further manuscript edits or a PDF rebuild.

## What improved in Section 6.1.1

- The figure introduction states the common MI and identifies the different
  margins locally, using the established notation: row and column margins
  are \(m_k(0.7)\) for \(P\) and \(m_k(0.8)\) for \(Q\).
- The interpretation follows the three rows, with one substantial paragraph
  per row. Each paragraph connects trends along the curves, differences
  between table sizes, the mechanism, and the comparison between populations.
- Signposting marks the move from describing a pattern to explaining it.
  The explanation names the changing quantities and how they affect the plot.
- The top-row comparison identifies both reasons for the larger normalised
  peaks in \(P\): its higher peak mean estimate and smaller population
  benchmark. Equal MI fixes the mean of pointwise MI, while its variance also
  depends on the cell values and their probability weights.
- The middle-row explanation follows both the fall and recovery. The
  population prediction decreases as \(1/n\), while rare-cell effects can
  make the observed variance initially rise or decline more slowly. Repeated
  counts eventually improve the local approximation, bringing the ratio
  towards one.
- The claims were checked against saved moment summaries and component
  diagnostics, including the covariance of the linear term with the
  remaining error.

The discussion also clarified how the two variance rows are calculated:
the population prediction uses the true probabilities; the sample-based
prediction is calculated separately from each observed table and then
averaged. That procedural distinction should be explicit wherever a reader
could confuse the quantities.

## 1. Introduce the comparison before interpreting it

State the question a display answers and the local settings needed to read
it. Identify what varies along the horizontal axis, what is held fixed, what
the lines represent, and how panels differ. Name populations and methods
explicitly. Use established notation such as \(m_k(0.8)\) for settings;
explain a feature of that construction in words when it drives the mechanism.

For a ratio, identify its numerator, denominator and reference value. State
which direction means underprediction, overprediction or better agreement.
For rejection rates, distinguish approaching the nominal rate from simply
increasing rejection. Explain inclusion rules when missing points or validity
restrictions affect the comparison.

Keep captions short. Put necessary settings, calculation details and
interpretation in the body beside the display.

## 2. Explain how the plotted quantity is calculated

Distinguish a value calculated from one sampled table from a summary across
repetitions. Where needed, describe the sequence: draw a table, calculate
the estimate, repeat, then take the required mean or sampling variance.
Use the repetition count and inclusion rule for that experiment.

The two variance rows of Figure 6.1 provide the model:

| Row | Numerator | Denominator | Question |
| --- | --- | --- | --- |
| Middle | \(\tau^2(P)/n_P\), calculated from the true population table | Sampling variance of \(\widehat V(P)\), measured across the simulated tables | How accurate is the first-order prediction with known population inputs? |
| Bottom | Average of \(\widehat\tau^2(P)/n_P\), calculated separately from each sampled table | The same observed sampling variance of \(\widehat V(P)\) | How accurate is the sample-based prediction on average? |

Both rows concern variation in the variance estimate itself. This is
distinct from the estimated MI sampling variance \(\widehat V(P)/n_P\).
Make similarly explicit distinctions between population benchmarks,
sampling-moment targets and sample-based estimates elsewhere in the chapter.

Identify the order of operations when it matters. Averaging a ratio is
generally different from taking a ratio of averages. An average performance
comparison also does not describe every individual sampled table.

## 3. Organise interpretation around the display

When rows answer different questions, finish each row's discussion before
moving to the next. Retain the agreed three-paragraph structure for Figure
6.1. For other figures, start with one focused paragraph per comparable visual
question; let the argument determine its length rather than a sentence quota.

A useful sequence within a discussion is:

1. Identify the row or panel and its main result.
2. Describe the important changes along the curves and differences between
   lines, including meaningful exceptions.
3. Explain those patterns and give the supporting evidence.
4. Develop the \(P\)-versus-\(Q\) comparison, naming what differs and why it
   matters.

Use this flexibly, integrating a comparison with its explanation where that
reads naturally. Finish the current figure before introducing another display
that requires a new comparison. Keep a table beside the claim it supports and
introduce its necessary column definitions before using its entries.

## 4. Mark the move from description to explanation

Use a short, substantive transition where the paragraph moves from what is
visible to why it happens: "This dip develops because ...", "The larger
numerator and smaller denominator therefore ...", or "With larger samples,
repeated counts ...".

Name the preceding result when an isolated "this" would be ambiguous. Use
causal language when the derivation or diagnostics support it. For an inferred
mechanism, state the supported connection without presenting association as
proof. The transition should begin the explanation itself; a sentence merely
announcing that analysis follows adds little.

## 5. Explain the complete shape through changing quantities

Explain both sides of a peak or trough and the transition between them. A
label such as sparsity or nonlinear error does not explain a curve by itself.
Show how the sample or setting changes, how that affects the estimate, and
what the change does to the plotted result.

In the middle row of Figure 6.1, the explanation follows this sequence:

1. At fixed population probabilities, \(\tau^2(P)\) is constant, so the
   predicted variance decreases as \(1/n_P\).
2. Sampled tables differ in which rare cells are absent or observed once.
   Their contributions to \(\widehat V\) can differ substantially. A change
   of \(1/n\) in a rare cell's proportion can be large relative to its true
   probability, making a local linear approximation inaccurate.
3. The observed variance can initially rise or decrease more slowly than the
   prediction, so the ratio falls.
4. Repeated counts make cell probabilities and log ratios more stable.
   The observed variance approaches the prediction and the ratio recovers.

Check the quantities behind every explanation. A ratio's trough need not
occur where its denominator is largest. A peak in the mean, a trough in the
population variance ratio and a crossing of one in the sample-based ratio
are distinct features and can occur at different sample sizes. Use the actual
horizontal-axis variable: some later figures vary MI at fixed sample size.

## 6. Explain comparisons using both parts of the calculation

For normalised curves, check how both the estimate and its benchmark differ.
A comparison of two ratios can require examining both numerators and both
denominators. Equal MI or common sample size does not make other inputs equal.

For degrees of freedom, explain how errors in the squared numerator and
variance denominator affect the result. For mean estimated degrees of
freedom, also consider averaging the sampled ratio; average-input errors
alone do not determine its magnitude.

Keep population first-order approximation error distinct from the additional
effect of estimating its inputs. Also distinguish a sampling mean from
variation about that mean: a mean can remain biased after its sampling
variance is predicted accurately.

## 7. Keep evidence beside the claim

Use existing displays and saved diagnostics to support the explanation.
Preserve necessary numerical evidence and qualifications. Keep the main
result and interpretation together; use an appendix for detailed support
rather than making the reader reconstruct the central argument there.

Assume the examiner receives only the submitted thesis PDF. References to
an experimental supplement, companion report or internal archive must not
appear as directions to supporting evidence. Include the essential setting,
calculation or result in the main text or submitted appendices, and remove
secondary claims or promises of analyses that are not presented. Preserve
internal evidence separately without directing the examiner to it.

Choose numerical anchors that help the reader assess a claim. Avoid making
the prose a second inventory of every plotted value. Add a table or graph
when it resolves a specific comparison that existing displays cannot convey
clearly. Place displays according to the argument and size them for
readability, independently of page-count considerations.

## 8. Make targeted improvements

Use formal, direct prose with concrete subjects and verbs. Explain technical
language where it affects interpretation. Keep connected sentences when a
claim needs its reason or qualification; avoid blanket sentence shortening.

An addition should remove a demonstrated inference burden: an unclear
calculation, a missing mechanism, an unexplained shape, an ambiguous comparison
or a reading loop between displays. Replace overlapping text so the explanation
does not accumulate restatement or side tangents. Retain passages that already
perform these jobs.

## Applying the guide to the remaining sections

| Location | Main distinctions to make explicit |
| --- | --- |
| 6.1.2: moment errors and degrees of freedom | Moment target, population first-order value and sample-based estimate; competing numerator and denominator errors; averaging a ratio; missing points. |
| 6.1.3: behaviour near independence | Fixed sample size and changing MI; meaning of scaled moments; how each prediction departs from its comparison quantity and why. |
| 6.2.1: overall false-positive patterns | Calculation of rejection rates; validity and inclusion; movement towards or away from 5%; differences between margins and table sizes. |
| 6.2.2: bias and standard-error accuracy | Changes in the estimated difference, its sampling spread and estimated standard error; their effects on the shared statistic before applying the rejection cutoff. |
| 6.3.1: nominal power | What changes along the alternative axis; direction of the corrected difference and absolute statistic; why a curve may initially fall before rising. |
| 6.3.2: calibrated power and sensitivity | Fitting null, evaluation population and fixed alternatives; fitted thresholds; what is matched and where; limits of calibration at one null. |
| 6.4: application | Question, direction and units of the MI difference, statistic and decision; what the observed data establish about equality and approximation accuracy. |

These are revision priorities, not findings that every passage needs rewriting.

## Acceptance check

A first-time reader should be able to explain:

- the question and which setting changes;
- how the plotted quantities are calculated, including the order of averaging;
- the main pattern and important exceptions;
- which quantities change to produce the pattern and the supporting evidence;
- what differs between populations or methods; and
- the conclusion and its relevant limits.

Check revised claims against saved evidence. Preserve result equations,
labels, numerical results, citations and uncertainty; verify references and
paragraph style. Rebuild only when explicitly requested, then inspect the
changed pages for the actual order of prose and displays.

## Paragraph continuity, 31 October 2026

The comparison with the three sample theses found that Chapter 6's
interpretation paragraphs are not generally shorter. Shorter sentences
and repeated setup passages can nevertheless interrupt the argument.

- Connect an observation with its reason, consequence or qualification
  when the relationship is clearer within one sentence. Retain short
  sentences for distinct results and definitions; do not replace them
  with long sentences containing several unrelated claims.
- Keep table settings with the explanation of that table when they answer
  the same question. Combine related setup fragments without merging
  distinct panel interpretations or moving text across its display.
- Explain why a comparison is needed before listing its procedural choices.
  In calibration sensitivity, establish that equal MI leaves the common
  value unspecified before defining the lower and upper fitting nulls.
- Preserve Figure 6.1's three row paragraphs and substantive explanations.
  Sentence wording may be revised for continuity without changing that
  organisation. Paragraph length is not a target, and the sample medians
  are descriptive rather than writing rules.
- Improve continuity by replacing fragmented or repeated text. Do not add
  filler, extra numerical cases or new results to lengthen a paragraph.

## Sentence construction and progression, 31 October 2026

The sample comparison identified three useful patterns: Michael commonly
keeps a finding with its interpretation or qualification; Grace carries a
specific result into the next sentence before explaining its significance;
Riley develops mechanisms through successive changes in named quantities.
Adopt these relationships while preserving the thesis's statistical precision.
Longer sentences are useful when they complete an explanation, not as a
general replacement for short sentences.

### Develop one relationship within a sentence

Keep the main statement with its immediate cause, consequence, comparison,
condition or qualification when the reader would otherwise have to connect
two separate statements. Use `because` for an established explanation,
`as` for a changing condition, `although` for a qualification, and `whereas`
or `while` for a substantive comparison. A relative clause can identify what
an estimate measures or how a statistic is used. Select the construction
that expresses the actual relationship, rather than adding connectors by habit.

For example, develop the shared-statistic comparison as one unit:

> Both methods use this statistic, which Normal Wald compares with the
> standard normal distribution and Expanded Welch compares with a Student
> t distribution with estimated degrees of freedom.

This connects the shared input to the methods' different reference
distributions. It does not combine a second result or numerical case.

### Carry established information into the next step

Begin a sentence from a quantity or finding the preceding sentence has
established, then explain what changes or follows. Prefer specific subjects
such as "this variance underestimation", "the larger cutoff" or "the
remaining bias" to an isolated "this" or a generic statement that the
results need explanation. Use the changing quantity to link sentences:

> The variance estimate is too small. For a fixed difference estimate,
> the smaller denominator enlarges the absolute statistic and can move it
> beyond the rejection boundary.

The first sentence establishes the error; the second carries that same error
through the statistic to the decision. Retain a sentence break when it helps
the reader follow a genuinely distinct mathematical or interpretive step.

### Vary sentence length without creating overloaded sentences

End a sentence when its main relationship is complete. Keep important
definitions, new findings and non-obvious derivation steps separate when
they need emphasis. Review short reminders about populations, scales,
uncertainty bands or repeated calculations for integration into the sentence
they explain. Do not join different panels, several numerical comparisons
or unrelated procedural details simply because their sentences are short.
A semicolon must express a close relationship; it is not a substitute for
explaining how two statements connect.

### Choose colons and semicolons for a clear purpose

Use a colon to introduce a list, displayed equation or explanation that
benefits from an explicit introduction. Prefer stating an explanation
directly when a generic introduction such as "the diagnostics reveal
competing effects:" merely postpones the quantities and their relationship.

Keep semicolons selectively for closely related parallel statements and
lists whose items already contain commas, such as the A/B/C settings.
Opposing effects on a denominator or degrees of freedom can benefit from
a clearly balanced construction. Mathematical colons, such as the one in
the null-hypothesis notation, are not prose punctuation.

Recast reminders and procedural asides into the statements they clarify.
For example:

> Changing the rejection thresholds leaves the estimated difference,
> standard error and calculated p-values unchanged.

This expresses the effect of the threshold change directly, rather than
joining "only the thresholds change" to a second independent statement
with a semicolon. Similarly, describe a figure as showing matched
false-positive rates at zero and calibrated power as the MI advantage
increases, rather than repeatedly joining separate plot instructions.

Use a full stop when the next statement needs independent emphasis.
For example, a rate's calculation and the finding that both methods are
valid in every repetition may warrant separate sentences. Keep the
qualification that non-rejection does not establish equality explicit.
Do not replace semicolons mechanically with commas or conjunctions,
strengthen a causal claim to justify a join, or introduce long, nested
sentences to avoid a full stop. Punctuation frequencies are diagnostic
checks, not targets.

### Preserve the scientific claim when improving the connection

Keep the quantities, direction of error, sample/population distinction,
inclusion rule and approximation conditions explicit. Preserve words such
as "can", "tends" and "approximately" where they express real limitations.
Connecting an observation to a diagnostic must not turn association into
proof of a mechanism. Keep all necessary intermediate algebra and do not
reduce derivation depth to make the prose sound smoother.

### Review sentences in context

1. Read the whole paragraph and identify the question it answers.
2. For each short sentence, decide whether it introduces a distinct point
   or completes an explanation already underway. Retain the former;
   consider connecting or integrating the latter.
3. Check that the next sentence starts from an identifiable quantity or
   explicitly motivates a new comparison. Remove only genuine repetition.
4. Reread the revised paragraph for one clear main clause per sentence,
   manageable qualifications and visible transitions between steps.
5. Compare the numerical evidence, assumptions, references and claim strength
   with the original before accepting the edit.

Sentence counts and lengths are diagnostic checks, not quotas. A reduction
in short sentences is useful only when the explanation becomes easier to follow.
