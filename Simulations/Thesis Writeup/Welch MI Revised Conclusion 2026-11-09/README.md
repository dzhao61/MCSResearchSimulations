# Thesis copy with revised conclusion

This independent comparison copy retains the original signed thesis and
changes Chapter 7 only. Its conclusion gives the overall findings before
selected numerical examples, distinguishes cutoff effects from estimation
errors, and connects limitations and future work to the main judgement.

The active main thesis and its submission PDF remain unchanged. The
separate direct-derivation copy is not used here: Chapter 4 is the original.

Build from this directory with a Python environment providing pypdf:

    python build_copy.py

LaTeX, BibTeX, and latexmk are required. The build uses only local manuscript
inputs and has no signing, Git, or publication dependency on the main thesis.
It preserves the existing authorised signature and date, 07/11/2026, from
`style/authorised_compliance_page.pdf` without creating a new signature.
The named PDF and self-contained source archive are in `deliverables/`.
