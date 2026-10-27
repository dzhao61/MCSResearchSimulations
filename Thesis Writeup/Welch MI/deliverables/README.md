# Current Delivery Files

Use these stable filenames for the latest successfully packaged thesis:

- `Daniel_Zhao_Welch_MI_Thesis.pdf`: final full manuscript to send for review.
- `Daniel_Zhao_Welch_MI_Thesis_Source.zip`: self-contained current LaTeX source.
- `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`: current code and evidence.
- `SHA256SUMS.txt`: checksums for those three current files.

Historical working drafts are preserved in `archive/` and as existing
snapshot PDFs. Packaging builds `main.tex` and never rebuilds those drafts.

From the thesis folder, run `python3 package_deliverables.py` (or
`make`) to build the main manuscript and refresh all three files together.
Run `python3 package_deliverables.py --check` (or `make check`) to verify
that they still match the current source, main PDF and experimental evidence.
Direct `latexmk` builds of `main.tex` also refresh this delivery set through
the project's post-build hook. Failed builds do not publish delivery files.
