# Current Delivery Files

Use these stable filenames for the latest successfully packaged thesis:

- `Working Draft v3.pdf`: final full manuscript to send for review.
- `Working Draft v3 Source.zip`: self-contained current LaTeX source.
- `Working Draft v3 Experiment Supplement.zip`: current code and evidence.
- `SHA256SUMS.txt`: checksums for those three current files.

`Working Draft.pdf` and `Working Draft v2.pdf` are preserved historical
artifacts, not the latest thesis. They are never replaced by packaging.

From the versioned thesis folder, run `python3 package_deliverables.py` (or
`make`) to build the versioned manuscript and refresh all three files together.
Run `python3 package_deliverables.py --check` (or `make check`) to verify
that they still match the current source, versioned PDF and experimental evidence.
