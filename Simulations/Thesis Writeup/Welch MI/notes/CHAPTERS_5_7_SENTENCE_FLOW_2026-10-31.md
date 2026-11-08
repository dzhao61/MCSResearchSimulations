# Sentence construction and progression in Chapters 5–7

Implemented on 31 October 2026 following the user's request to apply the
new sentence-construction principles to Chapters 5, 6 and 7 while leaving
the earlier derivations alone. This is a source revision; no rebuild was
requested in this turn.

## Scope and preservation

The sources immediately before this revision, current writing instructions,
Chapter 6 guide and README are preserved in
`archive/before_chapters_5_7_sentence_flow_2026-10-31.zip`. The review covers
all three chapters, with more extensive editing in Chapters 5 and 7 and a
lighter pass in Chapter 6, which had already undergone sentence-flow and
punctuation revisions.

The purpose is to make explanatory relationships easier to follow. Sentence
length, punctuation frequency and paragraph length are diagnostic measures,
not editing targets. Short definitions, individual mathematical steps and
distinct findings remain separate where a longer sentence would increase
the reader's working-memory burden.

## Changes

- **Chapter 5:** connect the known-population design to the quantities it
  permits us to measure; integrate the square-table and copying-probability
  definitions; connect copying to matches and margin preservation; keep
  example settings with their numerical consequences; explain how each
  sampled variance estimate enters the difference variance; connect moment
  comparisons to their purpose; and integrate power-path, calibration,
  sampling and uncertainty reminders with the calculations they clarify.
  The cell-probability calculation, worked conditional probabilities,
  construction equations and procedural lists retain their steps.
- **Chapter 6:** name the changing variance prediction when explaining its
  effect on estimated degrees of freedom; connect the two sampled inputs
  and averaging of ratios directly; introduce the near-independence
  diagnostic setting with the calculation being checked; name the two
  recovering false-positive rates; separate the two errors at B from their
  opposing effects on rejection; and state the cross-null validation
  question directly with its setting. Already clear figure introductions,
  numerical-setting lists and category coding are retained. Figure 6.1's
  three row paragraphs are byte-identical to the pre-edit source.
- **Chapter 7:** carry the observation-level sensitivity into its role in
  moment matching; connect the squared-mean mechanism to degrees of freedom;
  keep the common-MI condition with the reported improvements; connect
  competing errors with their possible compensation; explain bias
  cancellation directly; carry nominal power and false-positive rates into
  the reason for calibration; and explain the surviving power dip through
  the unchanged difference estimate. Selection, independent evaluation,
  calibration limitations and the evaluation of a proposed correction are
  expressed with explicit referents.

The review retained or restored sentence breaks where joining axes, row
definitions, category lists or several numerical settings increased the
reading load. It also avoids introducing a causal connector merely to join
two statements: for example, the calibration limitations remain a statement
of the scope of the two checks, without treating knowledge of the simulation
populations as proof of that limitation.

## Verification

`CHAPTERS_5_7_SENTENCE_FLOW_VERIFICATION_2026-10-31.json` records the checks.

- All figure, table, equation and aligned-equation blocks are byte-identical
  to the pre-edit sources, including captions, dimensions and placement
  options. Heading, label, input and citation occurrences are unchanged;
  reference occurrences are preserved, allowing changes in prose order.
- All distinct inline mathematical expressions and numerical values are
  preserved. Paragraph boundaries and the order of prose and displays are
  unchanged. No experiment, result, test rule or substantive qualification
  has been added or removed.
- All 99 recorded protected files remain unchanged, including earlier
  chapters, appendices, figure/data sources, typography and existing PDF
  and delivery artifacts. The large supplement is checked by its recorded
  size and exact timestamp; the remaining protected files are hash-checked.
- The active input graph has 21 TeX files and 140 unique labels, with no
  dangling references, missing citations, missing inputs or unbalanced
  braces/environments. No directions to unsubmitted supplementary evidence
  have been introduced.
- Paragraph-style checks, five existing thesis-consistency tests and
  `git diff --check` pass. Sentence diagnostics were reviewed in context;
  they are not quality scores. The previous counting procedure can join
  sentences ending in setting labels such as `B.` or `A--C.` because it
  mistakes the label for a person's initial. The verification records both
  that legacy procedure and counts with this setting-label issue handled.

The current PDF and delivery packages remain the preceding 109-page build.
No simulation, fitting, bootstrap, PDF compilation, package publication or
Git commit was performed. A future explicitly requested rebuild should
include these edits and inspect the changed pages for actual line and page
breaks.


## Requested rebuild, 31 October 2026

The requested rebuild includes the revisions in the 108-page main and named PDF, with clean compilation/reference logs and paragraph style. Changed pages were rendered and visually reviewed. Two layout fixes were made during review: Table 5.5 now uses `[H]` to keep its interpretation after the table; the final application recap sentence was removed to avoid two lines on an otherwise empty page. The application's qualification about unknown population tables, moment targets and false-positive rates remains. No fonts, margins, line spacing, numerical results or equations changed. Appendices and bibliography are text-identical apart from page numbers. The source archive and checksums were refreshed; the unchanged 25,010-file supplement was reused after inventory, size and timestamp checks.
