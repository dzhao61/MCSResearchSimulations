# Welch-MI Thesis

## Final manuscript

The goal and SMART acceptance targets are in
[THESIS_GOAL.md](THESIS_GOAL.md), refreshed 4 October 2026. The detailed chapter plan is
[THESIS_REWRITE_PLAN.md](THESIS_REWRITE_PLAN.md). The companion [EXEMPLAR_REVIEW_NOTES.md](EXEMPLAR_REVIEW_NOTES.md)
records the review of the three example theses and the writing conventions
for the new draft.

The plan uses the completed fixed-population comparison of Normal Wald and
Expanded Welch. It replaces the older draft's empirical argument with an
assessment of calibration, power, validity and computational cost by exact
regime.

The active unsigned manuscript is `main.pdf`, built from `chapters_rewrite/` and
`appendices_rewrite/`. It uses the completed fixed-population comparison of
Normal Wald and Expanded Welch, including validity and runtime. The preceding
LaTeX source and PDF are preserved in `archive/previous_draft_2026-09-13/`;
the older `chapters/`, `appendices/`, and `figures/` directories remain only
for history and are not read by `main.tex`. `THESIS_PLAN.md` and
`WRITING_STYLE_GUIDE.md` are historical planning material.

## Build

With the experiment supplement extracted beside this source directory,
regenerate the 22 thesis figures and numerical macros from the final saved
CSVs with:

```bash
MPLBACKEND=Agg MPLCONFIGDIR="$PWD/.mplcache" XDG_CACHE_HOME="$PWD/.cache" \
  python figures_rewrite/make_figures.py
```

From this thesis directory, build the PDF with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The 36 actively cited and source-audited bibliography records are stored in
the local `references.bib`, so the manuscript can compile without the parent
methods project. The active preamble searches only `figures_rewrite/`,
preventing an old pilot figure from being used silently.
`figures_rewrite/figure_manifest.json` maps every thesis
figure to the final display/configuration identifiers. In the workspace, the
full companion atlas is
`../../WelchSatterthwaiteMI/docs/experiments/THESIS_EXPERIMENTS.md`; after
extracting the two archives together, it is
`WelchSatterthwaiteMI/docs/experiments/THESIS_EXPERIMENTS.md`.
The source-linked numerical audit is `figures_rewrite/audit_evidence.py` and
can be run with the same environment. Both scripts automatically locate a
neighbouring `WelchSatterthwaiteMI/` tree; alternatively set
`WELCH_MI_WORKSPACE_ROOT` to the directory containing that tree.

## Structure

- `main.tex`: document entry point.
- `metadata.tex`: author, degree, supervisor, and submission metadata.
- `preamble.tex`: shared packages, notation, and formatting.
- `frontmatter/`: title page, abstract, and acknowledgements.
- `chapters_rewrite/`: eight active main chapters.
- `appendices_rewrite/`: active derivations, exact design grids, evidence index,
  supporting experimental figures, independence boundary and reproduction record.
- `figures_rewrite/`: source-linked PDFs, generation script and figure manifest.
- `LITERATURE_SOURCE_CHECK.md`: targeted check of close primary sources and contribution scope.
- `SCIENTIFIC_AUDIT.md`: independent mathematical, implementation, and evidence review.
- `REVIEW_RESPONSE.md`: point-by-point disposition of the external assessment.
- `BIBLIOGRAPHY_REVIEW_RESPONSE.md`: disposition of the later source and literature assessment.
- `THESIS_GOAL.md`: current objective, exemplar length benchmark, SMART targets and completion criteria.
- `SUBMISSION_CHECK.md`: current verification record and historical acceptance checks.
- `THESIS_REWRITE_PLAN.md`: active research, chapter and evidence plan.
- `EXEMPLAR_REVIEW_NOTES.md`: current exemplar analysis and writing guidance.
- `THESIS_PLAN.md`: previous research and chapter plan.
- `WRITING_STYLE_GUIDE.md`: previous writing guide, with outdated empirical examples.

Detailed independent-pilot, degree-of-freedom ablation and complete main-null
diagnostics are retained in the experiment supplement rather than the
reader-facing thesis.

The 4 October named PDF, source archive, experiment supplement and checksums
in `deliverables/` match the active 98-page manuscript. Chapter 6 has seven
lead figures, and Appendix D has 15 supporting figures. The source archive
builds independently when extracted with the supplement; the evidence audit
and bundled tests also pass there. The declaration page is intentionally
excluded at the author's request.

The source archive includes the current goal, detailed rewrite plan and review
records. Links in those records to the supplied example theses and historical
workspace material are context references, not compilation dependencies; that
material is not redistributed in the final archives.
