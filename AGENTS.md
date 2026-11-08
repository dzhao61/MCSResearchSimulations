# Research repository

The Git root is this `Research/` directory. Keep the existing folders in
place; changing the Git root does not relocate their contents.

- `Simulations/` is the scientific workspace, containing the active thesis,
  estimator code, experiments, saved evidence, and numerical environment.
- `Thesis Presentation/` contains the current presentation, speaker notes,
  assets, planning material, and earlier versions. Use its top-level deck
  for current presentation work.
- `FINAL SUBMISSION/` holds the submission copies and remains local.

Read `Simulations/AGENTS.md` for the Welch MI project instructions, research
writing preferences, archive preservation rules, and thesis packaging
workflow. Paths described there as workspace or project-root paths are
relative to `Simulations/`, rather than the Git root. Apply its research
writing preferences to presentation work as well. Use Australian English,
complete distribution names, and Oxford commas in lists of three or more
items. Preserve published titles and direct quotations.

Run scientific commands and thesis packaging from their existing folders
inside `Simulations/`, using `Simulations/.venv/bin/python` where required.
The existing authorisation for a scoped commit and push after each requested
main-thesis rebuild remains in force. The packaging hook excludes unrelated
presentation work and other research folders.

The root ignore file currently limits new tracking to `Simulations/` and
`Thesis Presentation/`, plus these root instructions and README. Preserve
the existing simulation ignore rules for large generated evidence. Do not
bulk-add other Research folders as part of unrelated work.
