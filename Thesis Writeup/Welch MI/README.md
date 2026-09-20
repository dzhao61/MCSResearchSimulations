# Welch-MI Thesis

## Final manuscript

The goal and SMART acceptance targets are in
[THESIS_GOAL.md](THESIS_GOAL.md), dated 15 September 2026, with a proposed
completion target of 22 September. The detailed chapter plan is
[THESIS_REWRITE_PLAN.md](THESIS_REWRITE_PLAN.md). The companion [EXEMPLAR_REVIEW_NOTES.md](EXEMPLAR_REVIEW_NOTES.md)
records the review of the three example theses and the writing conventions
for the new draft.

The plan uses the completed fixed-population comparison of Normal Wald and
Expanded Welch. It replaces the older draft's empirical argument with an
assessment of calibration, power, validity and computational cost by exact
regime.

The final unsigned manuscript is `main.pdf`, built from `chapters_rewrite/` and
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

The 35 actively cited and source-audited bibliography records are stored in
the local `references.bib`, so the manuscript can compile without the parent
methods project. The active preamble searches only `figures_rewrite/`,
preventing an old pilot figure from being used silently.
`figures_rewrite/figure_manifest.json` maps every thesis
figure to the final display/configuration identifiers. The full companion
atlas is `../../WelchSatterthwaiteMI/docs/experiments/THESIS_EXPERIMENTS.md`.
The source-linked numerical audit is `figures_rewrite/audit_evidence.py` and
can be run with the same environment. Both scripts automatically locate a
neighbouring `WelchSatterthwaiteMI/` tree; alternatively set
`WELCH_MI_WORKSPACE_ROOT` to the directory containing that tree.

## Structure

- `main.tex`: document entry point.
- `metadata.tex`: author, degree, supervisor, and submission metadata.
- `preamble.tex`: shared packages, notation, and formatting.
- `frontmatter/`: title page, declaration, abstract, and acknowledgements.
- `chapters_rewrite/`: eight active main chapters.
- `appendices_rewrite/`: active derivations, exact design grids and evidence index.
- `figures_rewrite/`: source-linked PDFs, generation script and figure manifest.
- `LITERATURE_SOURCE_CHECK.md`: targeted check of close primary sources and contribution scope.
- `SCIENTIFIC_AUDIT.md`: independent mathematical, implementation, and evidence review.
- `REVIEW_RESPONSE.md`: point-by-point disposition of the external assessment.
- `BIBLIOGRAPHY_REVIEW_RESPONSE.md`: disposition of the later source and literature assessment.
- `THESIS_GOAL.md`: current objective, exemplar length benchmark, SMART targets and completion criteria.
- `SUBMISSION_CHECK.md`: evidence available and the remaining steps to complete the thesis.
- `THESIS_REWRITE_PLAN.md`: active research, chapter and evidence plan.
- `EXEMPLAR_REVIEW_NOTES.md`: current exemplar analysis and writing guidance.
- `THESIS_PLAN.md`: previous research and chapter plan.
- `WRITING_STYLE_GUIDE.md`: previous writing guide, with outdated empirical examples.

Detailed independent-pilot, degree-of-freedom ablation and complete main-null
diagnostics are retained in the experiment supplement rather than the
reader-facing thesis.

The final named PDF, self-contained source archive, experiment supplement and
checksums are in `deliverables/`. `SUBMISSION_CHECK.md` records the completed
scientific, build and page-review gates. The author must sign and date the
declaration before submitting the attested copy.
