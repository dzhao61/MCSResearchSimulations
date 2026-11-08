# Main version promotion - 24 October 2026

The user requested that the revised thesis become the main version and the
previous baseline become an archive. The promoted manuscript remains the
approved 95-page Working Draft v3; its PDF is byte-identical to the version
approved before promotion.

## Main project

The revised folders now occupy the canonical workspace paths:

- `Thesis Writeup/Welch MI/`
- `WelchSatterthwaiteMI/`
- `DifferentialMI/`
- `PracticalMIExploration/`

Use `Working Draft v3.tex`, its versioned PDF and its delivery folder for
current work. Unversioned main files and older working drafts retain their
historical contents. Root and project instructions identify the active
version. The old redesign-directory project paths are compatibility links
to the canonical folders, so earlier file links still open the main files.

## Baseline archive

`Archive/Welch MI baseline 2026-10-24/` preserves all four previous baseline
folders, including manuscript sources, PDFs, code, input data, saved results
and historical drafts. All 30,042 files match the original SHA-256 manifest
both before and after relocation. Archive instructions make their historical
status explicit. The original folders' contents were not edited.

All 45,412 promoted files retained their identities during the directory
moves. Subsequent changes were limited to project instructions and delivery
refreshes; scientific source, input data, saved results, figures and
historical drafts retain their identities. Nested external Git metadata is
outside the scientific file-identity comparison. No simulations were rerun.

## Verification

The canonical root resolves all four projects and the packager correctly.
All 275 local tests pass: 223 experiment, 27 estimator, 17 application and
8 packaging tests. The refreshed source archive builds independently with
no LaTeX warnings and produces text identical to the main PDF. Delivery
archives and checksums pass the consistency check. The approved PDF is
unchanged. Reproducible evidence and large supplement archives remain local
under the Git ignore rules; no untracked, unignored file exceeds 100 MiB.

`WELCH_MI_PROMOTION_2026-10-24.json` and `REDESIGN_VERIFICATION.json` at the
workspace root record the final checks. No Git staging or commit is part of
this promotion.
