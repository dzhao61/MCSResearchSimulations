# Welch-MI Thesis

This directory contains a complete first thesis draft for the expanded
Welch--Satterthwaite test for comparing mutual information between two
independent categorical populations. The compiled manuscript is
`main.pdf`.

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
- `THESIS_PLAN.md`: research and chapter plan.
- `WRITING_STYLE_GUIDE.md`: prose and mathematical presentation guide.

Before submission, confirm the degree name, supervisor title, declaration,
acknowledgements, and final submission date. The empirical results in the
draft are drawn from the accepted simulation artefacts under
`../../WelchSatterthwaiteMI/results/`.
