# Automatic delivery refresh, 27 October 2026

The latest 97-page PDF was already present in the named delivery folder;
the preceding chat linked main.pdf instead. Both copies have SHA-256
`5a0cb3ea9f3e6f280c54e941d5803f9da652e3391fc79491d85e0902d1a1b9a5`.

The user requested an automatic hook. The thesis `.latexmkrc` now publishes
the named PDF, source ZIP, experiment-supplement ZIP and checksums after a
successful direct build of main.tex. It routes through
`package_deliverables.py --publish-built` rather than invoking a second TeX
build. The standard packaging command disables the nested success hook and
therefore still compiles/publishes only once.

The post-build path checks the global paragraph policy, PDF signature,
completed log and absence of formatting/reference warnings before staging
delivery files. Missing/incomplete PDFs or warning-bearing logs are rejected.
Other TeX targets, including historical drafts, do not trigger the hook.
The standalone source ZIP does not include the workspace-specific hook and
continues to build independently as before.

Validation: all 15 packaging/workflow tests pass, including direct publication
without rebuilding, failed/incomplete builds, warning rejection, historical
target exclusion, output arguments with spaces and hook failure propagation.
A real direct latexmk invocation read the hook, found the current PDF
up-to-date and refreshed the delivery set without TeX compilation. The
subsequent delivery check passed. The manuscript PDF is unchanged.

The previous workflow sources are preserved in
`archive/before_delivery_build_hook_2026-10-27.zip`. Future chat delivery links
should point to the named PDF under deliverables/.
