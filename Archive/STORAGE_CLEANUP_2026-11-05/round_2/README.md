# Second approved storage cleanup — 5 November 2026

Daniel approved removal of the obsolete isolated delivery-test copy and
unreachable Git objects. The Claude worktree was explicitly excluded.

## Old delivery-test copy

Removed `Welch MI Redesign 2026-10-21/tmp/isolated_delivery/`, containing
24,800 files (about 6.9 GiB). Its 165 unique historical files, including
historical draft PDFs and test logs, are retained in
`isolated_delivery_unique.zip`. Their original uncompressed size is
5,346,395 bytes. All other file contents remain in the canonical project.

`isolated_delivery_manifest.json.gz` records each original path, size,
SHA-256, source, permissions and timestamp. Before deletion, the entire
old test directory was reconstructed temporarily and every file was
SHA-256 verified. The temporary verification copy was then removed.
Keep the canonical files referenced by the manifest, or update this
recovery set before changing/removing them.

Restore from the Simulations workspace root into a directory that does
not already exist:

```sh
python3 Archive/STORAGE_CLEANUP_2026-11-05/round_2/restore_isolated_delivery.py --output 'Welch MI Redesign 2026-10-21/tmp/isolated_delivery'
```

## Git maintenance

Git's garbage collector removed unreachable objects and redundant pack
storage. Reflog expiration and worktree pruning were disabled for this
operation. All 10,497 objects reachable from refs or reflogs were retained;
branch refs, reflog bytes and registered worktrees are unchanged. A full
`git fsck` passed after maintenance. The push-repair recovery bundle is
retained. Git object pack storage fell from about 17.43 GiB to 1.77 GiB,
plus removal of about 189 MiB of loose-object storage.

See `git_gc_result.json`, `git_gc_output.txt` and `verification.json` for
the operation and checks. The earlier cleanup's reports describe that
first pass; this second pass subsequently repacked the object store.

## Preservation

All 6,963 protected files in the active thesis folder and Claude worktree
remain SHA-256 identical. The thesis, presentation execution plan, actual
presentations, current experiment records and the Claude working files
are unchanged. No build, experiment, commit or push was performed.
