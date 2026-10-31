# Chapter 6 continuity revision, 31 October 2026

The user approved targeted improvements following the paragraph comparison with all three sample theses. The aim is connected exposition rather than longer paragraphs throughout. The pre-edit chapter, writing guide, README and current PDF are preserved in `archive/before_chapter6_continuity_2026-10-31.zip`.

## Changes

- Connected invalid-output handling with the reason for reporting validity separately.
- Joined the selected settings to their diagnostic-table explanation, retaining every setting and column definition.
- Connected bias and variance errors with their effects on rejection; retained separate A/B/C comparisons and the sparse-table explanation around its equation.
- Connected related sentences in the calibration introduction, ranking explanation and panel C interpretation. Panel A and B interpretations remain separate and unchanged.
- Replaced the fragmented calibration-sensitivity introduction, bullets and isolated held-fixed reminder with two developed paragraphs. The first explains why equality leaves the common MI unspecified and why that matters for calibrated thresholds; the second defines the lower/upper nulls, fixed margins/sample sizes and shared alternative samples.
- Made the cross-null validation question explicit before its table and removed repeated wording from the concluding interpretation without changing the limitation on general false-positive control.
- Joined the application's population and variable definitions to its data/group setup. Connected the sign of the month difference with its definition, retaining the displayed statistic calculation and separate month/weekend conclusions.
- Added the continuity principles to the existing Chapter 6 writing guide. No word-count or sentence-length targets were introduced.

## Scope and checks

All of RQ1, including the three developed Figure 6.1 paragraphs, is byte-identical to the pre-edit source. The nominal-power subsection is also unchanged. All seven figure blocks, eight table blocks and two displayed equations are byte-identical, with their positions in the argument retained. Labels, reference/citation occurrences and numerical values are preserved; typography and generated assets are unchanged.

The active input tree has 21 TeX files and 140 unique labels, with no dangling references, missing inputs or unbalanced braces/environments. The paragraph-style check and five existing manuscript numerical-consistency tests pass. Verification is recorded in `CHAPTER_6_CONTINUITY_VERIFICATION_2026-10-31.json`.

Whitespace-delimited chapter source length changes from 7,462 to 7,527 words, an increase of 65 words (under 1%), chiefly to explain the purpose of changing the calibration null before giving its procedure. No new experimental result or numerical case was added.

The PDF and delivery files are unchanged and await an explicitly requested rebuild. No simulation, fitting, bootstrap, PDF compilation or Git commit was performed.

## Requested rebuild

The subsequent requested rebuild remains 109 pages. The final log is free of LaTeX warnings, overfull boxes and underfull boxes. Thirteen relevant pages were rendered and reviewed, including the revised table introductions, calibration discussion and application. Main, build and named delivery PDFs have identical hashes. The source ZIP is refreshed and content-verified; the unchanged, previously fully verified 25,010-file supplement is reused after archive-checksum, inventory, size and timestamp checks. Delivery instructions and checksums are current. No Git commit was made.
