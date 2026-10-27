# Welch MI: current thesis and experiment

The revised Welch MI project became the main version on 24 October 2026.

- Read `Thesis Writeup/Welch MI/deliverables/Daniel_Zhao_Welch_MI_Thesis.pdf` (98 pages).
- Edit `Thesis Writeup/Welch MI/main.tex` and its included sources; the compiled manuscript is `main.pdf`.
- Use `WelchSatterthwaiteMI/` for the current experiment and saved evidence.
- `DifferentialMI/` supplies the estimator code; `PracticalMIExploration/` supplies the application.
- `REDESIGN_VERIFICATION.json` records the current delivery checks.

The main thesis source compares Expanded Welch with Normal Wald. The fixed moment reference and sample-size df comparisons are preserved in the experiment supplement. The 27 October rebuild includes the latest abstract, chapter structure, appendix reductions and flush-left paragraph formatting.

The complete previous baseline is preserved in
`Archive/Welch MI baseline 2026-10-24/`, including its thesis, code, results
and historical drafts. All 30,042 baseline files were checked against their
original SHA-256 manifest before promotion. Treat the archive as historical.

`Welch MI Redesign 2026-10-21/` now contains compatibility links to the main
project, plus the original redesign records. Existing paths through that
directory still open the promoted files; use the canonical paths above for
future work.

From `Thesis Writeup/Welch MI/`, run `python3 package_deliverables.py` to
build and refresh the PDF, source ZIP, experiment supplement and checksums;
then run `python3 package_deliverables.py --check`. The active build target
is `main.tex`, with generated files in `build/`. The prior main files and
Working Draft v3 delivery set are preserved under the thesis folder's
`archive/before_main_deliverable_2026-10-24/`; older working drafts remain
historical artifacts.

The root `.venv/bin/python` provides the existing numerical environment.
Reproducible results and the large experiment supplement stay local under
the Git ignore rules. No evidence was deleted during promotion.

The 23 earlier experiment projects formerly at the workspace root are preserved in `Archive/Past experiments 2026-10-25.zip`. The verified ZIP replaces their uncompressed copies, reducing their footprint from about 456 MB to 146 MB. See [the archive guide](Archive/PAST_EXPERIMENTS_2026-10-25.md) for the project list, checksums and restoration instructions.
