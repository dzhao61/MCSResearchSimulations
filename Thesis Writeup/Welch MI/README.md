# Welch-MI Thesis

## Current writing direction

The active plan is [THESIS_REWRITE_PLAN.md](THESIS_REWRITE_PLAN.md), dated
13 September 2026. The companion [EXEMPLAR_REVIEW_NOTES.md](EXEMPLAR_REVIEW_NOTES.md)
records the review of the three example theses and the writing conventions
for the new draft.

The plan uses the completed fixed-population comparison of Normal Wald and
Expanded Welch. It replaces the older draft's empirical argument with an
assessment of calibration, power, validity and computational cost by exact
regime.

The existing LaTeX chapters and `main.pdf` are the **previous draft**. Their
design, numerical results, abstract and conclusions have not yet been
rewritten for the final experiment. `THESIS_PLAN.md` and
`WRITING_STYLE_GUIDE.md` are retained as historical planning material.

## Build

From this directory, run:

```bash
/Library/TeX/texbin/latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Clean auxiliary files with:

```bash
/Library/TeX/texbin/latexmk -c
```

The bibliography is currently read from the validated methods project at
`../../WelchSatterthwaiteMI/article/references.bib`. Figures are read from
the corresponding results and article directories, which keeps the thesis
linked to the generated evidence rather than manually copied outputs.

## Structure

- `main.tex`: document entry point.
- `metadata.tex`: author, degree, supervisor, and submission metadata.
- `preamble.tex`: shared packages, notation, and formatting.
- `frontmatter/`: title page, declaration, abstract, and acknowledgements.
- `chapters/`: eight main chapters.
- `appendices/`: supporting derivations, diagnostics, and reproducibility.
- `THESIS_REWRITE_PLAN.md`: active research, chapter and evidence plan.
- `EXEMPLAR_REVIEW_NOTES.md`: current exemplar analysis and writing guidance.
- `THESIS_PLAN.md`: previous research and chapter plan.
- `WRITING_STYLE_GUIDE.md`: previous writing guide, with outdated empirical examples.

Before submission, confirm the degree name, supervisor title, declaration,
acknowledgements, and final submission date. The previous draft's figures use
older simulation artefacts. The new draft will use
`../../WelchSatterthwaiteMI/results/thesis_redesign/` as its primary empirical
source, as specified in the active plan.
