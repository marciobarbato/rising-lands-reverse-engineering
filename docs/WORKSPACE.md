# Workspace and asset storage

The workspace is `/Users/marcio/git/Rising Lands`. The Git repository is its `engenharia-reversa/` child. Run Git commands there, or use `git -C engenharia-reversa ...`.

```text
Rising Lands/
  README.md                 workspace entry point
  Jogar.command             PT-BR launcher for the legacy Swift proof
  engenharia-reversa/       canonical Git repository
  local-data/
    originals/              original BIN/CUE, extracted CD, existing Python vendor files
    converted/legacy-prototype/  converted legacy PNG/JSON/audio assets
    macos-preview/          generated preview payloads and pinned runtime inputs
  legacy-prototype/         original Swift proof, extraction tools, tests, and build
  archive/
    graphics-releases/      immutable complete historical releases
    retired-worktrees/      completed, merged research checkouts
    documentation-before-organization.tar.gz
    documentation-provenance.json
  worktrees/                new feat/* research worktrees and temporary integration checkouts
  source -> local-data/originals
```

## Rules for assets

Treat `local-data/originals/` as read-only. Preserve original names, directory layout, bytes, PT-BR strings, and audio. Never normalize the original executable in place. Do not commit CD images, extracted commercial media, bundled toolchains, local runtimes, caches, or app builds.

Converted legacy assets live in `local-data/converted/legacy-prototype/`, with audio, soldier frames, sprite banks, mission data, and terrain images in their existing subdirectories. The legacy app reads them through `legacy-prototype/assets`. Its tools read originals through `legacy-prototype/source`. The top-level `source` compatibility link keeps existing research readers working.

Generated preview assets, builds, dependencies, distributions, research captures, and snapshots live in `local-data/macos-preview/`. Ignored links at `apps/macos-preview/` retain the app's expected paths. The versioned app directory contains source, scripts, tests, reference metadata, and English instructions. `snapshot.json` and `research.json` are local activation state, not shared configuration.

Graphics research uses hash-checked input copies in its ignored `fontes/`, `snapshot/`, and `dependencias/` directories. Existing manifests remain versioned. Frozen releases live under `archive/graphics-releases/`, reached by an ignored `entregas` link; originals of the tracked release files also remain in Git history.

## Worktrees

The three old worktrees are registered but retired; do not continue editing them. Use `scripts/workstream.py start <domain>` to create fresh `feat/re-<domain>` worktrees from `origin/main`. The helper links missing local inputs without changing tracked manifests. All four workers must treat shared linked inputs and the central Ghidra project as read-only.

Do not put a Git worktree inside another tracked source or release directory. Do not delete a worktree directory manually. Use `git worktree remove` only after its branch is merged and local/ignored data have been preserved.

## Reconstructing on another machine

Clone the repository, then supply the same legally available Brazilian CD corpus at `../source/cd` or a link to your local original-media directory. Install dependencies from the pinned requirements. Graphics test inputs need the files described by its `fontes/manifesto.json`, the snapshot identified in `snapshot/manifesto.json`, and its recorded dependencies. The complete local archive is a convenience, not a prerequisite for synthetic core tests. See [validation](VALIDATION.md) for missing-input behavior.
