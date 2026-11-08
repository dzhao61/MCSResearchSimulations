# Section 6.4 questions and reading order, 27 October 2026

The user requested two explicit application questions, a quickly readable
X/Y/P/Q guide, and a logical sequence that does not preview unfamiliar
methods or results too early.

## Revised sequence

1. Introduce the shopping dataset and state the month and weekend questions
   separately in ordinary language. These are local application questions,
   not additional thesis-wide RQs.
2. Define the visitor groups, retained sample sizes, purchase outcome and
   observational independence assumptions.
3. Show X/Y/P/Q in one compact table: X differs between the two questions,
   Y is the purchase outcome, and P/Q are joint distributions among new and
   returning visitors. State the equal-MI null after these definitions.
4. Explain the count tables, category retention, sparse February cell and
   bias corrections before presenting corrected estimates and uncertainty.
5. Interpret the month statistic, introduce the normal and Student t
   distributions, and present both methods' p-values.
6. Answer the month and weekend questions and explain the low weekend df.
7. Introduce the original six-comparison family and Holm adjustment after
   the reader has seen the two shopping results.

The early description of weekend as a weak-association comparison is
removed; the estimates establish its association size later. The notation
table does not imply that month and weekend have the same P/Q tables:
each choice of X defines its own joint distributions in the same groups.

## Preservation and checks

The previous source and related test are preserved in
`archive/before_section_6_4_questions_2026-10-27.zip`.

- Chapter 6 before Section 6.4 is byte-identical.
- The two existing numerical table blocks and month-statistic equation are
  byte-identical; corrected MI, group sizes, sparse cells, p-values, df,
  directions, Holm values and the original adjustment family are retained.
- Other chapters, appendices and all figure/table assets are unchanged.
- Six existing application regression checks and five manuscript-consistency
  checks pass. The application test now reads the active merged Conclusions
  source rather than the removed Chapter 8 filename.
- Active references, labels, LaTeX environments and braces pass source checks.
- The global flush-left paragraph rule passes.
- No PDF build, packaging refresh, experiment or bootstrap was run. PDF and
  delivery hashes are unchanged. Table placement, numbering and page layout
  remain to be inspected at the next requested rebuild.
