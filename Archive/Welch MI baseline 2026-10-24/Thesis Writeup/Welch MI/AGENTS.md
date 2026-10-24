# Active Welch MI Thesis

This is the active thesis directory. Use `main.tex` and `main.pdf` for ordinary
builds and delivery. The approved sentence-cohesion revision was promoted
here on 17 October 2026. The previous main version is preserved in
`../Archive/Welch MI (before conjunction revision 2026-10-17)/`; do not edit or
rebuild that archive or any historical working draft.

Current delivery files belong in `deliverables/`. After any manuscript,
figure, bibliography, source or evidence change, run `python3
package_deliverables.py` from this folder. It builds `main.tex`, keeps
generated LaTeX files in `build/`, and refreshes the PDF, source archive,
experiment supplement and checksums together. Run `python3
package_deliverables.py --check` to check that the delivery files match
current inputs. Do not deliver an older PDF by merely copying it.

Internal plans and review records are under `notes/`. Superseded loose
sources, plots and comparison entry points are preserved under
`archive/cleanup_2026-10-18/`; they are not active build inputs.

Use connected, varied academic prose rather than uniformly short sentences.
Longer sentences are useful when they keep a claim with its reason,
consequence, qualification or comparison. Keep a clear main clause and avoid
stacking unrelated ideas, numerical cases or nested qualifications. Use
conjunctions to express genuine relationships, not to decorate the prose.
Retain short sentences for new definitions, key results and distinct
derivation steps. Keep each paragraph focused and link paragraphs through
the argument itself. Do not restore removed tangents or technical previews.

When editing prose, preserve equations, scientific qualifications, numerical
evidence, citations, figure dimensions and typography. Keep Section 2.3 as the
derivation benchmark and do not revise it without a specific request.

Any requested working-draft rebuild must use a separate `Working Draft v3`
source/output target. Preserve the older working-draft sources and PDFs.
