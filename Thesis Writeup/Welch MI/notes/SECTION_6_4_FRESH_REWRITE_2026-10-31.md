# Section 6.4: application structure and explanation

Rewritten on 31 October 2026 following the user's request to reconsider the
whole section using the accumulated writing principles. The immediately
preceding Chapter 6 source, README and writing instructions are preserved in
`archive/before_section_6_4_fresh_rewrite_2026-10-31.zip`. This preserves the
earlier sentence-flow work elsewhere in Chapter 6.

## Structure

1. **Question and statistical objects.** State the month--purchase MI
   comparison and the parallel weekend comparison directly, then identify
   the predictor, outcome, populations P/Q and equal-MI hypothesis.
2. **Data and count tables.** Give retained groups, exclusions, outcome
   coding and independence assumptions. Explain the ten month rows through
   the absence of January and April, followed by the common category set,
   sparse February row and weekend table. Naming the two absent calendar
   months replaces the long inventory of the ten included months without
   changing the category set.
3. **Exploratory context.** Identify the original six-comparison family and
   Holm adjustment before interpreting results, so the reader does not
   discover the selection context after the conclusions.
4. **Estimation and test calculation.** Define the signed difference and
   its interpretation, retain the two bias corrections, and introduce the
   estimate table with units. Use month for the worked statistic, then
   explain the reference distributions before the test-results table.
5. **Month interpretation.** Keep the rejection, effect of the Student t
   distribution and Holm-adjusted conclusion together in one paragraph.
6. **Weekend interpretation.** Connect the small estimated difference to
   its near-zero statistic, high p-values and non-rejection. Retain the
   distinction between non-rejection and equality, then explain the small
   degrees of freedom through estimated uncertainty relative to the
   variance coefficients.
7. **Scope.** Explain why unknown population tables prevent direct checks
   of the moment target or false-positive rates, distinguishing the
   application's interpretation of outputs from the simulations' assessment
   under known populations.

These are stages in the argument, not new subsection headings. The section
uses connected paragraphs and keeps both existing tables and the worked
equation. No new analysis or numerical case is introduced. The early
exploratory context allows the final month interpretation to include both
unadjusted and adjusted evidence without sending readers back to reconsider
the testing family.

## Verification

`SECTION_6_4_FRESH_REWRITE_VERIFICATION_2026-10-31.json` records the checks.

- Chapter 6 before Section 6.4 is byte-identical to the pre-edit snapshot.
  The other chapters and appendices are unchanged by this rewrite.
- Both complete table blocks and the month-statistic equation are
  byte-identical, including labels, captions, numerical values and formatting.
  All distinct inline mathematical expressions, numerical values, citation
  occurrences and reference occurrences are retained.
- Raw data confirm that January and April are absent, all ten recorded
  months occur in both visitor groups, the February new-visitor row is
  `[1, 0]`, and both weekend tables have four observed cells. The published
  group sizes, exclusions, estimates and adjusted p-values are unchanged.
- The weekend variance coefficients and their estimated sampling variances
  reproduce the saved component degrees of freedom. Their substantial
  estimated relative fluctuations support the explanation of small degrees
  of freedom despite the large samples; this is an explanation of the
  calculated inputs, not a claim that their population accuracy is known.
- All 120 recorded protected files remain unchanged, including figures,
  typography and the current PDF and delivery files. The unchanged large
  supplement is checked by size and exact timestamp; the other protected
  files are hash-checked.
- The active input graph has 21 TeX files and 140 unique labels, with no
  missing inputs, dangling references, missing citations or unbalanced
  braces/environments. No direction to unsubmitted supplementary evidence
  has been introduced.
- Paragraph style and `git diff --check` pass. All five existing
  thesis-consistency tests and eleven application-data/calculation tests
  pass, including independent calculations and the six-comparison Holm
  adjustment. No estimator, experiment or dataset was changed.

No PDF rebuild or delivery refresh was requested in this turn. The existing
PDF remains the preceding 109-page build; a future requested build should
include both this rewrite and the earlier pending Chapters 5–7 revisions,
then inspect the changed pages for actual line and page breaks. No Git
commit was made.


## Requested rebuild, 31 October 2026

The requested rebuild includes the revisions in the 108-page main and named PDF, with clean compilation/reference logs and paragraph style. Changed pages were rendered and visually reviewed. Two layout fixes were made during review: Table 5.5 now uses `[H]` to keep its interpretation after the table; the final application recap sentence was removed to avoid two lines on an otherwise empty page. The application's qualification about unknown population tables, moment targets and false-positive rates remains. No fonts, margins, line spacing, numerical results or equations changed. Appendices and bibliography are text-identical apart from page numbers. The source archive and checksums were refreshed; the unchanged 25,010-file supplement was reused after inventory, size and timestamp checks.
