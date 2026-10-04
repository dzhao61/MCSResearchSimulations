# Research Writing Preference

For the Welch MI thesis and related research writing, use Section 2.3 of
`Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex` as the
model for the depth of important derivations. Assume the reader knows basic
calculus and probability but is new to this particular MI argument.

- State the target result, its purpose, assumptions, and a short roadmap.
- For Taylor expansions, show the general formula and explicitly map the
  function, expansion point, new value, and difference before substituting.
- Display non-obvious intermediate algebra. Make nested sums, reindexing,
  product-rule terms, cancellations, and independence assumptions explicit.
- Explain in words what each key equation does and distinguish approximations
  from exact equalities. End with the result's meaning or intuition.
- Avoid notation introduced only to shorten an equation, skipped steps that a
  first-time reader must reconstruct, and repetitive or irrelevant detail.

For prose throughout the thesis, explain the mechanism rather than merely
name it. Identify what quantity changes, why, and what that change does;
anchor the explanation to the equation or comparison at hand. Avoid vague
technical shorthand and false contrasts between methods (for example, calling
one denominator random when both methods estimate it). Use formal, direct,
confident language at an honours/master's level. Define necessary jargon,
state real approximations or limitations once where they matter, and avoid
repeated defensive caveats. Simpler wording must remain statistically precise.
State the scientific question or result directly. Avoid abstract commentary
about how a method must be assessed when the actual comparison can be stated
plainly. Use concrete subjects and verbs instead of making the reader infer
the point from a description of the reasoning process.
Use complete names for statistical objects when the noun matters: write
"Student t distribution" or "cutoff from the Student t distribution", not
"Student" or "Student cutoff" alone. Do the same for normal and chi-squared
distributions instead of relying on the reader to supply "distribution".

Keep each passage focused on the question it is answering. Detailed explanation
belongs where it advances the argument; omit or relocate short technical
digressions that interrupt the transition to the next idea. When describing a
connection, comparison or change, explicitly name both quantities or methods
so the reader does not have to infer the missing subject.
Use TEEL as a flexible paragraph guide: establish one main idea, support it
with evidence or an equation, explain its meaning, and link it to the argument
or next question. Split paragraphs that introduce a second main idea, but do
not force four sentences or a generic linking sentence into every paragraph.
Treat a displayed equation and its surrounding explanation as one connected
unit. Make transitions show how the next idea follows from the previous one,
rather than merely announcing the next section.
Keep figure captions short and descriptive. Put detailed experiment settings
and interpretation in ordinary body paragraphs beside each figure, rather
than in long captions or separate small-text interpretation blocks.
Keep figures within the text margins and proportional to the surrounding
prose. Size plots for readability, not page count; single-panel plots can be
narrower than multi-panel comparisons. Do not shrink dense plots until their
labels become difficult to read.

The thesis must be understandable as a standalone manuscript without access
to the codebase. Keep scientific construction details, parameter settings and
validity rules in the text or appendices. Omit file inventories, local paths,
configuration identifiers, build commands, version-control history and
protocol-freeze administration from the manuscript; internal project records
can retain them.
Avoid incidental editorial notes about presentation, obvious workflow
properties, and assurances about rounding or numerical housekeeping. Keep a
numerical detail when it affects the calculation, reproduction or
interpretation. Describe an approximation positively by what it does and its
conditions, instead of adding disclaimers about stronger claims not being
made.

Keep ordinary chat answers as concise as the user's question warrants; this
preference chiefly governs substantial derivations and thesis exposition.
