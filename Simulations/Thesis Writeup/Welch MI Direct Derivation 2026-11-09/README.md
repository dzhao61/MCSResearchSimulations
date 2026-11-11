# Thesis comparison copy: direct variance derivation

Created on 9 November 2026 from the current Welch MI thesis. This is a
separate, unsigned copy for comparing the Chapter 4 explanation.

Chapter 4 starts from the centred variance, differentiates the probability
weights and pointwise-MI values, and cancels the mean-derivative term using
the zero average of centred deviations. It then obtains the same variance
sensitivity, sampling-variance approximation, and degrees of freedom. The
moment-matching explanation is consolidated, and the transition from the
sensitivity to whole-sample error is shortened while retaining the Taylor
mapping and its conditions.

The other chapters, appendices, reported results, figures, metadata, and
template assets are unchanged. Internal equation and page references are
regenerated for this copy.

Review files are in `deliverables/`:

- `Daniel_Zhao_Welch_MI_Thesis_Direct_Derivation.pdf`
- `Daniel_Zhao_Welch_MI_Thesis_Direct_Derivation_Source.zip`
- `SHA256SUMS.txt`

Build from this directory with Python 3 and a TeX installation containing
`latexmk`, `pdflatex`, and `bibtex`:

```sh
python3 build_copy.py
```

Within the research workspace, use `../../.venv/bin/python build_copy.py`.
The build is local to this directory and has no publication or signing
hook. The existing active thesis and `FINAL SUBMISSION` files are preserved.
The source archive includes the prebuilt figures and template assets needed
to compile the manuscript independently.
