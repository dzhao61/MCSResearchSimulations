# Active Welch MI Thesis

This is the main thesis directory, promoted from the experimental redesign
on 24 October 2026. Use `main.tex` and `main.pdf` for builds and the named
Daniel_Zhao_Welch_MI files in `deliverables/` for delivery. This is the main
deliverable, not an active working draft. Previous main files and Working
Draft v3 are preserved in `archive/before_main_deliverable_2026-10-24/`.
The previous baseline is preserved under the workspace root's
`Archive/Welch MI baseline 2026-10-24/`. Earlier thesis archives remain
under `Thesis Writeup/Archive/`. Do not edit or rebuild those archives or
any historical working draft.

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

The main build is a deliverable build. Only an explicitly requested
working-draft rebuild uses a separate `Working Draft v3` source/output
target. Preserve all archived and historical sources and PDFs.

# Main project paths

The experiment, estimator and application folders are at the workspace root.
All imports and packaging must resolve to those main folders. The old
redesign-directory paths are compatibility symlinks to this same project.
