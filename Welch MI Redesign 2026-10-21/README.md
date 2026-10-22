# Welch MI redesign: independent working copy

The completed redesign is in this folder. The parent workspace versions of WelchSatterthwaiteMI, DifferentialMI, PracticalMIExploration and Thesis Writeup/Welch MI are unchanged. All 30,042 original files were verified against the pre-copy SHA-256 manifest.

## Review the manuscript

Open `Thesis Writeup/Welch MI/deliverables/Working Draft v3.pdf`. Its source and experiment archives are alongside it. The current manuscript target is `Working Draft v3.tex`; copied main.pdf and historical drafts remain unchanged.

## Evidence

The fresh run contains 366 evaluation and 186 independent fitting settings, with 100,000 pairs per batch: 55.2 million pairs in total. The independent audit reconstructs 4,416 input pairs and checks the full scalar records, identities, validity masks and p-values. Calibrated power uses a 1,000-repetition paired fitting/evaluation bootstrap. The experiment README gives rerun commands.

`ORIGINAL_FILES_SHA256.json` records the pre-copy originals; `ORIGINAL_PRESERVATION_CHECK.json` records the final verification. `Thesis Writeup/Welch MI/notes/REDESIGN_PROTOCOL_2026-10-21.md` documents the design.

For local execution use the parent workspace .venv Python, which contains the numerical dependencies. Scientific imports resolve inside this copy, independently of the original project source.

## Git and large evidence files

The local `.gitignore` keeps the thesis source, final PDF, source ZIP, code,
input datasets and manuscript figure and table files in Git. Reproducible
experiment results, temporary extractions, build products, copied historical
archives and the large experiment supplement ZIPs remain local. No evidence
is deleted by these rules. Existing tracked files in the original workspace
are unaffected; these exclusions apply to this independent redesign copy.

The current experiment supplement is approximately 7.4 GB and exceeds
GitHub's regular-file limit. Preserve it separately when backing up or sharing
the complete experiment. Its SHA-256 checksum is recorded in
`Thesis Writeup/Welch MI/deliverables/SHA256SUMS.txt`.

A Git clone can compile the supplied manuscript using the committed figure
and table files. To audit the saved experiment or regenerate figures from
saved records, restore the separately preserved supplement into this folder.
Alternatively, rerun the experiment using the environment and commands in
`WelchSatterthwaiteMI/README.md`. Reproduce the manuscript application with the
`full` command documented in `PracticalMIExploration/README.md`. The experiment
tests, result audits and complete delivery packager require their generated
evidence; the Git checkout alone does not contain it.
