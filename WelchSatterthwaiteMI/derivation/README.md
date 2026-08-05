# Expanded Welch-Satterthwaite Derivation PDF

This folder contains the LaTeX and PDF edition of the complete derivation.
The canonical mathematical content is
[`../docs/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`](../docs/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md).

## Files

- `main.tex`: generated standalone LaTeX source.
- `main.pdf`: compiled PDF.
- `header.tex`: page layout and typography customizations.
- `pandoc_filter.lua`: converts the Markdown heading hierarchy and numbers
  display equations.

Every top-level section starts on a new page.

## Rebuild

From the repository root, generate the LaTeX source with:

```bash
pandoc WelchSatterthwaiteMI/docs/EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md \
  --from=markdown+tex_math_dollars \
  --to=latex \
  --standalone \
  --toc \
  --toc-depth=2 \
  --lua-filter=WelchSatterthwaiteMI/derivation/pandoc_filter.lua \
  --include-in-header=WelchSatterthwaiteMI/derivation/header.tex \
  --metadata=title:"Full Derivation of the Expanded Welch-Satterthwaite Mutual Information Test" \
  --metadata=subtitle:"Two Independent Discrete Populations" \
  --metadata=author:"Daniel Zhao" \
  --metadata=date:"August 2026" \
  --variable=documentclass:article \
  --variable=classoption:11pt \
  --variable=geometry:a4paper \
  --variable=geometry:margin=27mm \
  --variable=colorlinks:true \
  --variable=linkcolor:MethodBlue \
  --variable=urlcolor:LinkBlue \
  --output=WelchSatterthwaiteMI/derivation/main.tex
```

Compile it with MacTeX:

```bash
PATH=/Library/TeX/texbin:$PATH \
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -cd WelchSatterthwaiteMI/derivation/main.tex
```
