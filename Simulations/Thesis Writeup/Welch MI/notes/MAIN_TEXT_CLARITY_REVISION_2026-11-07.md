# Eight main-text clarity edits, 7 November 2026

The user authorised the eight main-text edits from the narrower shortlist:
items 2, 6, 7, 9, 10, 12, 13 and 15 of the consolidated review. This pass
implements those edits in Chapters 2, 6 and 7. The appendix changes recorded
in `APPENDIX_CLARITY_REVISION_2026-11-07.md` are preserved.

## Changes and contextual review

1. Section 2.5 now explains the effect of an inaccurate standard error on
   the absolute test statistic for a fixed estimated difference. The
   conditional qualification and the possibility wording are retained.
2. Section 6.1.2 states that the sampling mean of V-hat exceeds V by a
   smaller percentage in Q than in P. It connects that relative comparison
   to the smaller proportional reduction in the squared numerator.
3. Section 6.1.3 explicitly assigns both sampling moments in the target's
   initial dip to V-hat, removing the ambiguous possessive.
4. Section 6.1.3 identifies the variance of the linear sampling term and
   the observed sampling variance it approximates, replacing the vague
   description of the linear term becoming more informative.
5. Section 6.2.3 makes the suppression of rejection explicit: as bias
   diminishes, an oversized standard error can still take rejection below
   the target. This remains a possible contribution rather than a claim
   that one diagnostic establishes every cause of the rejection pattern.
6. Section 6.3.3 states that changing the cutoff lowers rejection on both
   sides of the trough without changing bias in the estimated MI difference.
   It no longer gives the power curve an apparent sampling centre.
7. Section 7.1.1 begins with the degrees-of-freedom finding. Three sentences
   state the finding, explain the smaller substituted mean, and connect its
   square to the downward error while retaining the qualification about
   accurate sampling-variance prediction. The existing sample-size finding
   and sample-substitution qualification remain in the paragraph.
8. Section 7.3 explicitly allows populations with different probability
   tables to satisfy the null when their MI values are equal.

Each passage was reread with its surrounding explanation and compared with
the previous source. No new main-text derivations, examples or displayed
equations are added. The other main-text review suggestions remain deferred.

## Verification

- All five existing thesis-consistency tests pass.
- Displayed equations, numerical tokens, citations, labels, references,
  headings, environments and figure commands in the three edited chapters
  are preserved. Additional inline names identify already defined variance
  quantities; no algebra or reported numerical result changes.
- Section 2.3, the derivation benchmark, is byte-identical to the snapshot
  before this pass.
- All 181 source references resolve against 154 unique labels. Braces and
  environments balance. Australian spelling, shared paragraph style and
  whitespace checks pass.
- Of 637 preservation inputs, only the three authorised chapter sources
  change. The other 634 hashes match, including both revised appendices,
  the abstract, other chapters, figures, bibliography, current PDFs and
  delivery archives, historical files, inspected code and the separate
  personal study guide.

No PDF rebuild, delivery refresh, commit or push was requested or performed.
The current PDF predates this pass and the preceding appendix revision.
Pagination and assembled layout await the next requested rebuild.
