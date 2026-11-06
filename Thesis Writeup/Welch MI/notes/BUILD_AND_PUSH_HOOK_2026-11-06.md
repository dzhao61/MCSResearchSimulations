# Thesis rebuild and automatic push, 6 November 2026

The user requested a rebuilt PDF, a push of the current changes, and a hook
that pushes after future PDF rebuilds. This build includes the preceding
distribution-name and terminology revisions. The earlier general-review
recommendations remain deferred.

## Build workflow

The existing main-thesis latexmk publication hook now reaches an automatic
commit-and-push step after the PDF and delivery files have been verified.
The standard packaging command and `make` use the same step. The packaging
command suppresses the inner latexmk callback, avoiding duplicate publication
and pushes.

Automatic commits include active manuscript and figure inputs, current main
and named outputs, and build support. Historical drafts, presentations and
unrelated notes are excluded. Unrelated staged work is preserved. Explicitly
reviewed notes can be included separately. The current branch is pushed to
its configured upstream; a branch without an upstream uses the matching
origin branch. No force-push, automatic pull or history rewrite is used.

Read-only checks do not commit or push. `--no-push` allows visual verification
before running the final push step. Build/publication failures stop that
step. Push failures retain the verified local files and local commit, and
are reported explicitly. Retrying a push does not create a duplicate commit
when the build files are unchanged.

The experiment supplement is compared with its complete current input
inventory and file contents. An unchanged archive is reused in place; a
changed inventory or input causes regeneration. This build reused the
existing 12 GB supplement after verification.

The first compilation exposed an existing path issue: the fallback located
latexmk without adding its companion TeX tools to PATH. The packager now
prepends the selected latexmk directory to its inherited PATH. The failed
invocation's generated dependency cache was moved to temporary storage,
then the build completed normally. No manuscript edits were made to obtain
the successful build.

## Verification

- All 24 packaging and automatic-push tests pass. Real temporary local Git
  repositories test scoped commits, unrelated staged work, ignored data,
  historical drafts and presentations, new branches, rejection and retry.
  CLI tests verify that publication precedes pushing and that failed builds
  and read-only/local modes do not push.
- The rebuilt thesis has 104 pages, compared with 103 before this rebuild.
  LaTeX reports no warnings, unresolved references, overfull boxes or
  underfull boxes. No prose was trimmed or figures resized for pagination.
- All manuscript source hashes taken before compilation are unchanged.
  Main and named delivery PDFs are byte-identical. Extracted text contains
  the new terminology and no remaining Normal Wald or Valid fraction labels.
- All 104 pages pass the text-boundary check, and every font entry is
  embedded. Fourteen changed or boundary pages were rendered and inspected:
  physical pages 3, 11, 41, 45, 48, 53, 56, 68, 74, 80, 86, 93, 96 and 98.
  The assumption heading, performance table, longer figure labels and
  appendix requirements fit without layout corrections.
- The complete delivery check passes: current PDF, source archive,
  experiment archive, input inventories and delivery checksums agree.
- Paragraph-style and whitespace checks pass. The requested build was
  reviewed with `--no-push`; the final commit-and-push step follows review.

Historical drafts, separate declaration/acknowledgement documents and
archived sources are unchanged.
