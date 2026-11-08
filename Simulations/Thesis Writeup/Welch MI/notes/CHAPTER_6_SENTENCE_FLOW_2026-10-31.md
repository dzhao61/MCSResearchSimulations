# Chapter 6 sentence construction and progression

Implemented on 31 October 2026 after the user approved applying the patterns identified in the three sample theses and adding them to the writing guidelines. This is a source revision; the PDF and delivery files remain unchanged.

## Preservation and scope

The pre-edit chapter, current chapter guide, thesis/workspace instructions, README and current PDF are preserved in `archive/before_chapter6_sentence_flow_2026-10-31.zip`. Earlier continuity edits and their history are retained.

The review covers Chapter 6's figure introductions, interpretation, calibration and application. It retains the chapter, section and panel organisation, including the three substantial row paragraphs for Figure 6.1. No result, numerical case, display, experiment or test rule has been added.

## Applied principles

- Keep a finding with its immediate explanation, comparison, consequence or qualification where that relationship forms one readable sentence.
- Carry a named estimate, error or finding from one sentence into the next. Replace a generic announcement of an explanation with the quantities that supply it.
- Integrate detached reminders about populations, scales, repeated calculations, uncertainty bands and units into the sentences they clarify.
- Retain short definitions, distinct findings and necessary mathematical steps. Do not join unrelated observations or several numerical cases just to reduce the short-sentence count.
- Preserve scientific conditions and claim strength, including the distinction between a diagnostic association and an established mechanism.

## Main changes

- The chapter introduction connects repetition counts to independent sampling and shared evaluation of the two methods.
- RQ1 connects mean-error comparisons with their squared-numerator effect, integrates the corresponding Q calculations and shared-scale reminder, and joins the near-independence approximation steps to the error they explain. The three Figure 6.1 row paragraphs retain their mechanisms and comparisons.
- Null-result figure guidance now directly compares the margin regimes. Within the panel explanations, variance errors remain connected to the statistic and rejection rate; the text retains the qualification that joint numerator/denominator behaviour contributes to the trough rather than isolating every cause.
- Bias and variance remain separate checks. Sparse-table centring stays connected to its displayed equation, and every validity threshold, count, uncertainty statement and comparison remains available.
- Nominal power connects the changing rejection boundaries to the narrowing power gap. Calibration guidance integrates fitting/evaluation results and bootstrap bands with their figure, while the lower/upper definitions retain separate, manageable explanatory steps.
- The application integrates table coding, units and reference distributions with their use. The weekend statistic is connected to its near-one p-values, with the non-rejection limitation and unknown-population qualification retained.

## Writing guidelines

The workspace `AGENTS.md` now states the general sentence-construction principles for research prose. The current `CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md` adds detailed guidance on complete explanatory relationships, information carried between sentences, varied rhythm, scientific precision and a sentence-in-context review procedure. Its earlier Figure 6.1 instruction now explicitly preserves the structure and substance while allowing wording improvements. The historical writing-style guide is unchanged.

## Verification

`CHAPTER_6_SENTENCE_FLOW_VERIFICATION_2026-10-31.json` records the source checks.

- All seven figure blocks, eight table blocks and two displayed equations are byte-identical to the pre-edit snapshot, including captions, dimensions and placement options.
- All distinct inline mathematical expressions, numerical values, heading/label occurrences, reference occurrences and citations are preserved. The three Figure 6.1 row paragraphs remain in order.
- The 117 protected manuscript, figure/data, PDF and delivery files match their recorded hashes. Other thesis chapters and appendices are unchanged.
- The active input graph contains 21 TeX files and 140 unique labels. There are no missing inputs, duplicate labels, dangling references, missing citations or unbalanced braces/environments. Paragraph-style checks and five existing numerical-consistency tests pass.
- A repeat of the earlier approximate sentence-counting procedure gives 385 sentences before and 342 after. Sentences of ten words or fewer decrease from 53 to 11 (13.8% to 3.2%); mean length changes from 19.0 to 21.3 words. No revised sentence exceeds 45 words under that procedure. These measures diagnose rhythm; they were not editing quotas.
- The retained short sentences include a ratio definition, distinct curve changes, the common-setting statement and the signed-difference definition. They were reviewed for their individual purpose.
- Whitespace-delimited chapter source length changes from 7,527 to 7,502 words. Improved continuity does not increase the chapter's source length.

No simulation, fitting, bootstrap, PDF compilation, delivery refresh or Git commit was performed. Rebuild only when explicitly requested, then inspect the changed pages for actual line and page breaks.

## Requested PDF rebuild

The subsequent explicit rebuild includes the sentence-level revision and remains 109 pages. The final LaTeX log has no warnings, overfull boxes or underfull boxes. All 27 Chapter 6 pages were rendered and reviewed; extracted text changes on 23 of them, with every page outside Chapter 6 text-identical to the preceding build. The source archive is refreshed and content-verified, and the main/build/named PDF hashes match. The unchanged, previously verified 25,010-file supplement is reused after inventory, size and exact timestamp checks; its archive timestamp and size are unchanged. Delivery instructions and checksums are current. No Git commit was made.
