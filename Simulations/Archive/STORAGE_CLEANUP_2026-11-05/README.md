# Verified storage cleanup — 5 November 2026

Daniel authorised removal of stale Git temporary files and deduplication of
historical experiment supplements. Thesis sources, PDFs, presentation files
and the presentation execution plan are outside this cleanup.

## Retained archive contents

The former `Working Draft v3 Experiment Supplement.zip` under
`Thesis Writeup/Welch MI/archive/before_main_deliverable_2026-10-24/deliverables/`
contained 24,907 files. SHA-256 comparison established that 24,891 members
already exist in the canonical project folders. Their paths, hashes, sizes
and original ZIP metadata are recorded in `working_draft_manifest.json.gz`.
The 16 other files, totalling 172,853 bytes, are retained in
`unique_entries.zip`. No original member contents have been discarded.

A complete temporary reconstruction was made before deleting the original.
All 24,907 reconstructed members passed SHA-256 verification against the
original archive. ZIP recompression changes the container checksum; the
original checksum is retained in the manifest as a historical record.
`restoration_test.json` records this successful test.

The canonical files referenced by the manifest are part of this recovery
set: retain them, or update the recovery package before changing/removing
them. The restore utility checks every member and stops if a source differs.

The second removed supplement, `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`
in that same deliverables directory, is byte-identical to the retained copy
in `Archive/Welch MI baseline 2026-10-24/Thesis Writeup/Welch MI/deliverables/`.
`duplicate_copy.json` records its SHA-256 hash and both locations. The
baseline archive itself has not been changed.

## Restore

Run from the Simulations workspace root. Existing outputs are never overwritten.

```sh
python3 Archive/STORAGE_CLEANUP_2026-11-05/restore_supplements.py working-draft --output 'Thesis Writeup/Welch MI/archive/before_main_deliverable_2026-10-24/deliverables/Working Draft v3 Experiment Supplement.zip'
python3 Archive/STORAGE_CLEANUP_2026-11-05/restore_supplements.py duplicate-copy --output 'Thesis Writeup/Welch MI/archive/before_main_deliverable_2026-10-24/deliverables/Daniel_Zhao_Welch_MI_Experiment_Supplement.zip'
```

Historical checksum lists remain unaltered. The duplicate-copy restoration
reproduces its original ZIP checksum. The working-draft restoration verifies
all original member contents, rather than promising the old ZIP container
checksum after recompression. Historical PDFs and source archives remain in
place, unchanged.

## Git cleanup

`git_cleanup.json` records removal of the four temporary files reported as
garbage by `git count-objects -vH`. During that first pass, normal object packs, loose commit objects,
refs and the push-repair recovery bundle were retained. See
`cleanup_verification.json` for the final storage and preservation checks.

## Second approved cleanup

Daniel subsequently approved removing the old isolated delivery-test copy
and cleaning unreachable Git objects, while retaining the Claude worktree.
See [round_2/README.md](round_2/README.md) for the preservation map, restore
command, Git maintenance details and verification.
