# Current Delivery Files

Use these stable filenames for the latest successfully packaged thesis:

- `Daniel_Zhao_Welch_MI_Thesis.pdf`: final full manuscript to send for review.
- `Daniel_Zhao_Welch_MI_Thesis_Source.zip`: self-contained current LaTeX source.
- `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`: current code and evidence.
- `SHA256SUMS.txt`: checksums for those three current files.

`Working Draft.pdf` and `Working Draft v2.pdf` are preserved historical
artifacts, not the latest thesis. They are never replaced by packaging.

From the parent thesis folder, run `python3 package_deliverables.py` (or
`make`) to build the current manuscript and refresh all three files together.
Run `python3 package_deliverables.py --check` (or `make check`) to verify
that they still match the current source, main PDF and experimental evidence.
