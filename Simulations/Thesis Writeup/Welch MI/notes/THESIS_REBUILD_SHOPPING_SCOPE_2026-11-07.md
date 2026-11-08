# Thesis rebuild: shopping scope and review fixes, 7 November 2026

The user requested a main-thesis PDF rebuild after the approved application
scope revision and fixes 5, 9 and 10. No further appendix deletions or prose
changes were made during the build.

## Included source changes

- The application and appendix changes are recorded in
  `SHOPPING_APPLICATION_SCOPE_REVISION_2026-11-07.md`. That note describes
  the preceding source-only stage; this rebuild brings the PDF and delivery
  files into agreement with those sources.
- Fix 5 replaces the unqualified claim that rejection falls as sample size
  increases with a statement about bias becoming small relative to sampling
  spread and excessive rejection subsiding with sufficiently large samples.
  The replacement allows the initial rise in rejection observed in the
  different-skew results.
- Fix 9 gives the near-independence sample size as 1,000 in Table 5.2,
  matching the results presented in Chapter 6. Internal runs at other sample
  sizes are preserved.
- Fix 10 qualifies the equal-sample limitation with "the simulations reported
  here", leaving the internal unequal-sample check outside the manuscript.

## Build and verification

- Built with `package_deliverables.py --no-push` before visual review.
- The main and named delivery PDFs have 109 pages, previously 110. Removing
  Appendix B.7 accounts for the one-page reduction. Chapter and retained
  appendix starting pages remain unchanged; the bibliography starts one
  page earlier. The bibliography contains 43 cited works.
- The completed LaTeX log has no formatting or reference warnings.
- All five application tests and all five thesis-consistency tests pass.
- All 175 source cross-references resolve against 153 unique labels.
- Visually reviewed physical PDF pages 6, 7, 9, 54, 73, 82--88, 99 and
  105--109, covering the revised text, tables, contents, appendix transition
  and bibliography. No clipping, overlap or broken table layout was found.
- Packaging verified the source archive and rebuilt the experiment
  supplement because the authorised application-test update changed an
  included input. It refreshed the delivery checksums.
- Independently confirmed that the compiled, main and named delivery PDFs
  match; the source archive matches the current source inputs. All 119
  snapshotted active inputs remained unchanged during the build.
- `git diff --check` passes. Historical drafts and presentations are
  unchanged.

PDF SHA-256:
`0246e180ce4f821784a8c99fa8d621b6cc6148d450225f773ba06d95724245e5`.

The verified build is ready for the standing scoped commit-and-push step.
