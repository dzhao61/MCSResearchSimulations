# Welch-MI Thesis

## Final Files

The latest submission files are in [deliverables/](deliverables/):

- `Daniel_Zhao_Welch_MI_Thesis.pdf`: current full thesis.
- `Daniel_Zhao_Welch_MI_Thesis_Source.zip`: self-contained current LaTeX source.
- `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`: current code and evidence.
- `SHA256SUMS.txt`: checksums for the three current files.

The delivery README identifies these files separately from the preserved
`Working Draft.pdf` and `Working Draft v2.pdf`. Those drafts are historical,
not the latest thesis, and are never overwritten.

## Working Folder

`main.tex` and `main.pdf` are the canonical manuscript. Its active inputs are
`frontmatter/`, `chapters_rewrite/`, `appendices_rewrite/`,
`figures_rewrite/`, `preamble.tex`, `metadata.tex` and `references.bib`.
The scientific study has 240 settings, 70 population pairs and 4.8 million
sampled table pairs, plus the saved-sample diagnostics and practical example.

Internal plans, goals, reviews and verification records are grouped under
[notes/](notes/). These are workspace records, not part of the source ZIP.
Start with [the thesis goals](notes/THESIS_GOAL.md),
[the experimental plan](notes/FOCUSED_EXPERIMENT_PLAN.md),
[the scientific audit](notes/SCIENTIFIC_AUDIT.md) or
[the submission checks](notes/SUBMISSION_CHECK.md).

Superseded loose sources, figures and comparison entry points are preserved
under [archive/cleanup_2026-10-18/](archive/cleanup_2026-10-18/), with a
relocation manifest. Existing dated archives are unchanged. The complete
previous main version remains in
`../Archive/Welch MI (before conjunction revision 2026-10-17)/`.

`working_draft.tex`, `working_draft.pdf` and the two historical delivery
drafts remain untouched. Any future requested working-draft build must use
a separate **Working Draft v3** source and output target.

## Build And Verify

From this working folder, refresh the full delivery set with:

```bash
python3 package_deliverables.py
```

`make` runs the same command. Packaging builds `main.tex` first, keeps LaTeX
build files under `build/`, updates `main.pdf`, prepares and verifies both
archives, and then replaces the current delivery set. A failed build or
archive preparation leaves the previous delivery files in place.

To check existing delivery files without rebuilding:

```bash
python3 package_deliverables.py --check
```

`make check` is equivalent. `make test-package` runs the packaging tests.
After every source, figure or evidence change, refresh the delivery set
before sharing it; no background watcher is installed.

The source ZIP is independently compilable. After extracting it, run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Scientific rerun, audit and figure-generation instructions are in the
experiment supplement's `WelchSatterthwaiteMI/EXPERIMENT_SUPPLEMENT_README.md`.
It includes the full-data practical application and its source archives.
The standalone thesis gives the scientific reproduction details without
requiring access to this workspace.
