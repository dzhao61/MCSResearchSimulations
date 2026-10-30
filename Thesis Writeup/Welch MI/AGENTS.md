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

The user requested on 27 October 2026 that PDF builds and delivery-package
refreshes wait until explicitly requested. Until then, edit and check the
source without running LaTeX or `package_deliverables.py`; the existing PDF
and delivery files will lag behind the source. When a rebuild is requested,
use the complete packaging and verification procedure below.

On 28 October 2026 the user requested quicker interim builds. For these,
compile with the paragraph-style and log/reference checks, inspect changed
sections for obvious layout defects, and refresh the main/named PDF and
source archive. Reuse the previously verified experimental supplement and
its checksum when its input inventory, sizes and modification times are
unchanged. Do not rerender every page, rebuild an unchanged large supplement,
or independently compile the exported source on each interim request.
Reserve the full procedure below for final delivery or substantive build,
figure, formatting or experiment changes that warrant it. An explicit rebuild
request is still required. This interim preference takes precedence over
the otherwise mandatory full-package refresh described below.

Current delivery files belong in `deliverables/`. After any manuscript,
figure, bibliography, source or evidence change, run `python3
package_deliverables.py` from this folder. It builds `main.tex`, keeps
generated LaTeX files in `build/`, and refreshes the PDF, source archive,
experiment supplement and checksums together. Run `python3
package_deliverables.py --check` to check that the delivery files match
current inputs. Do not deliver an older PDF by merely copying it.

The local `.latexmkrc` hooks successful direct builds of `main.tex` into
`package_deliverables.py --publish-built`, which validates the completed
PDF/log and refreshes the named PDF, archives and checksums without
compiling again. Other TeX targets, including historical drafts, do not
trigger it. The normal packaging command suppresses this hook internally
so it publishes only once. Always link the named PDF in `deliverables/`
when returning a rebuilt thesis to the user.

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

For Chapter 6 results writing, use
`notes/CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md` alongside the
workspace research writing preferences. It records the explanation and
reading-order standards established through the Section 6.1.1 revision.

When editing prose, preserve equations, scientific qualifications, numerical
evidence, citations, figure dimensions and typography. Keep Section 2.3 as the
derivation benchmark and do not revise it without a specific request.

The main build is a deliverable build. Only an explicitly requested
working-draft rebuild uses a separate `Working Draft v3` source/output
target. Preserve all archived and historical sources and PDFs.

Use flush-left body paragraphs throughout: `\parindent` is `0pt`, with
the existing `0.25em` paragraph spacing controlled in `preamble.tex`.
Do not add local indentation or paragraph-spacing overrides to chapter,
appendix or generated-display sources. The packaging build checks this
policy before running LaTeX; `python3 package_deliverables.py --check-style`
checks it without building or refreshing deliveries.

# Main project paths

The experiment, estimator and application folders are at the workspace root.
All imports and packaging must resolve to those main folders. The old
redesign-directory paths are compatibility symlinks to this same project.
