# Welch MI redesign: promoted to the main project

The redesign became the main version on 24 October 2026. Use the canonical
folders at the parent Simulations workspace root:

- `Thesis Writeup/Welch MI/` for the 95-page main thesis, `main.tex` and named delivery files.
- `WelchSatterthwaiteMI/` for the current experiment and evidence.
- `DifferentialMI/` for the estimator code.
- `PracticalMIExploration/` for the application.

The corresponding paths inside this directory are compatibility symlinks
to those main folders. Existing PDF links and commands still reach the
promoted files. Use the canonical paths for future work.

The complete previous baseline is preserved in
`../Archive/Welch MI baseline 2026-10-24/`. Its 30,042 files were checked
against the original SHA-256 manifest before promotion. That archive
contains the baseline thesis, code, results and historical drafts.

`ORIGINAL_FILES_SHA256.json`, `ORIGINAL_PRESERVATION_CHECK.json` and `tmp/`
remain historical redesign records. The original manifest paths now map
to the dated baseline archive. `REDESIGN_VERIFICATION.json` links to the
current record at the workspace root; `WELCH_MI_PROMOTION_2026-10-24.json`
at that root records the promotion.

The root `.venv/bin/python` provides the existing environment. Current
build and packaging instructions are in the main thesis folder. Reproducible
results, build products and the large experiment supplement remain local
under the main project's Git ignore rules; no evidence was deleted.
