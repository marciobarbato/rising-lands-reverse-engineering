# Organization checks — 2026-10-28

These checks were rerun after moving the workspace data and preview. Historical original-x86 execution counts remain separately identified in [status](STATUS.md); this maintenance task did not rerun those emulation suites.

## Current repository checks

| Suite | Discovered | Passed | Explicit optional skips |
|---|---:|---:|---:|
| Core | 226 | 113 | 113 |
| Combat | 113 | 43 | 70 |
| Economy | 214 | 119 | 95 |
| Graphics, including comparison with captured original buffers | 73 | 73 | 0 |
| Integration and relocated-package regression tests | 3 | 3 | 0 |

No failures or errors. Command: `python3 -B scripts/check.py`. The same complete check also passed in a new detached worktree after `scripts/workstream.py prepare` linked the existing read-only inputs; the fresh worktree remained clean. The infrastructure tests create a temporary local bare remote, start two stale feature workers concurrently, verify serialization and retention of both changes, ensure the canonical checkout is untouched, reject foreign ownership changes, preserve preexisting inputs, and check resolved runtime containment through a symlink without accepting a sibling path.

The graphics reference-reader identity assertion now resolves both paths, so an ignored link to the same immutable snapshot is accepted without weakening its file-hash checks. Maintained Markdown relative links and Python source parsing passed. `git diff --check` passed. No original game UI/source text was translated; the generated unit catalog's documentation headers were changed to English while PT-BR unit names remained unchanged.

## App and prototype checks

The relocated macOS preview's existing pinned snapshots passed: 155 core cases (74 passed, 81 optional skips), 53 economy cases (28 passed, 25 skips), 33 combat cases (12 passed, 21 skips), and 23 adapter cases (all passed). Command, from `apps/macos-preview/`: `dependencies/python/bin/python3 -B scripts/testar.py`.

The preview rebuilt from its existing pinned core commit `5dab3d82a96d7ddb1b7646301a402732983159e8` using `scripts/build.py`. `scripts/verificar_pacote.py` passed: 1,666 bundle files, manifest hashes, the included ARM64 Python runtime, and deep/strict code-signature verification. The package verifier was corrected to compare resolved paths after generated payloads moved behind local-data links; its regression test covers that condition. No new interactive UI opening test was run during this organization task. The preview still consumes its declared older research snapshots.

The legacy proof passed 12 format/media tests plus the Swift movement/path/arrival/fixed-clock checks at 30, 60, 120, 144, and 240 FPS. It rebuilt and was locally signed at its new path. Python tests used the existing bundled Python runtime with Pillow; the system Python did not have Pillow. Stale Swift module caches containing the old absolute paths were removed and rebuilt. The legacy resource-copy command now copies the linked asset directory's contents into the app.

## Integrity and preservation

- All **52 distinct original corpus files** from `relatorios/fontes.json` and `relatorios/fontes-ia.json` matched recorded size and SHA-256 after the move.
- The full original BIN matched **705,418,896 bytes** and SHA-1 `801e7a9bd00954c281f23767568222b23f3c4981`.
- The documentation archive matched its archive SHA-256; all **103 formerly tracked Markdown files** matched their individual recorded hashes. Untracked viewer manuals and legacy notes were additionally preserved in that archive.
- All **seven frozen graphics release manifests** verified, totaling **8,303 manifest entries**. Two prior public-only releases lacked local copied inputs; **2,098 missing entries** were restored from existing inputs/snapshots only after their hashes matched the historical manifests. No existing frozen bytes or manifests were rewritten.
- The original three feature worktrees were moved with Git, remain registered, and their feature commits are reachable from the organization baseline. The fourth, untracked viewer's source is now included in version control.

Workspace originals, archives, generated app data, dependencies, and legacy prototype remain outside the canonical Git repository. Their storage/recovery rules are in [workspace](WORKSPACE.md) and [migration](MIGRATION.md).
