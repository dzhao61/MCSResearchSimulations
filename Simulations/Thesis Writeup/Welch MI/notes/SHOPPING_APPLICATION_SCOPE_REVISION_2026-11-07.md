# Shopping application scope revision, 7 November 2026

The user authorised keeping only the month and weekend online-shopping
examples and removing the other applications and Holm discussion. The
application retains its existing illustrative purpose and does not add an
explanation of the example-selection history.

## Manuscript changes

- Chapter 6 removes the paragraph introducing the six-comparison family,
  Adult and Student Performance, and its references to Appendix B.7.
- The test-results table explicitly labels the existing raw values as
  unadjusted p-values. All estimates, standard errors, statistics, degrees
  of freedom and raw p-values in the two shopping tables are unchanged.
- The month interpretation removes the Holm-adjusted values and the claim
  about adjustment across six comparisons. The explanation of the larger
  p-value under the Student t distribution remains.
- Chapter 7 summarises the observed month and weekend test decisions and
  the higher corrected month MI estimate among returning visitors. It no
  longer makes a multiple-comparison-adjusted claim.
- Appendix B removes its opening pointer to the adjustment material and
  all of Section B.7, including Table B.1. Sections B.1--B.6, their algebra
  and their numerical examples are preserved.

The exploratory code, raw data, saved six-comparison results, original
adjustments and bibliography database remain available internally. The
three now-uncited bibliography entries will not be printed by BibTeX.
Historical notes, archives, presentations and existing delivery files are
unchanged. Other recommendations from the external review are outside
this revision.

## Verification

- Updated the existing application checks to stop requiring the removed
  appendix table and adjusted claims in the manuscript. Removed the check
  of the deleted appendix section and its unused formatting helper.
- Preserved the existing numerical checks of the original exploratory
  results and adjustments as internal evidence checks.
- All five remaining application tests and all five thesis-consistency
  tests pass. The shopping tables still match the independent calculations.
- All 175 source cross-references resolve against 153 unique labels. No
  references to the deleted section or table remain in the manuscript.
- Contextual rereading, Australian English, paragraph style and
  `git diff --check` pass.
- All Chapter 6 displayed mathematics and both shopping tables are
  preserved, apart from the new unadjusted-p-value heading. The retained
  appendix content is identical after removing its obsolete opening pointer.
- Of 659 tracked preservation inputs, 655 are unchanged. The four changes
  are the three authorised manuscript sources and the application test file.
  This new revision note is additional to that snapshot.

No PDF rebuild, delivery refresh, commit or push was requested or performed.
The existing PDF still contains the previous application and appendix;
layout review and delivery packaging await a requested rebuild.
