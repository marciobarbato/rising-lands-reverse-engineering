# Repository instructions

Read `docs/STATUS.md`, `docs/PARALLEL_WORK.md`, and your domain manual before changing research. This is the canonical repository; the directory above it is the local workspace. Do not initialize a second Git repository there.

## Language

Maintained documentation, handoffs, and commit messages are English. The game remains Brazilian Portuguese: preserve player-visible labels/errors, stories, objectives, unit/resource names, and audio. Preserve original French symbols and established code identifiers. Do not translate immutable historical evidence or regenerate its hashes.

## Four-chat ownership

Each research chat works on one `feat/re-<domain>` branch in a separate worktree created by `python3 scripts/workstream.py start <domain>`. Never switch the canonical checkout's branch to do a worker's research. Use explicit working directories in shell/tool calls.

- Core owns `ferramentas/`, `testes/`, `evidencias/`, `relatorios/`, `docs/CORE.md`, and `docs/core/`.
- Combat owns `pesquisas-paralelas/combate/` and `docs/COMBAT.md`.
- Economy owns `pesquisas-paralelas/economia/` and `docs/ECONOMY.md`.
- Graphics owns `pesquisas-paralelas/graficos-animacao/` and `docs/GRAPHICS.md`.

Shared scripts, `AGENTS.md`, root README, common status/workflow/format manuals, requirements, Ghidra tooling, and `apps/` are reserved for a separate integration/maintenance change. A worker records a cross-domain dependency in its own handoff and communicates the requested contract; it does not silently edit the other owner's files. Do not spawn additional agents unless the user explicitly requests them for the current work.

## Inputs and evidence

Original media at `../source/cd` and linked `.local`/graphics input copies are read-only. Do not share a writable Ghidra database. Never edit frozen releases, predecessor manifests, original-byte evidence, or pinned snapshots to make a new implementation pass. Add new evidence with explicit provenance and scope. Do not put worktrees, complete repository copies, commercial media, dependencies, caches, or app bundles inside tracked research folders.

## Completion and integration

Run `python3 -B scripts/check.py --domain <domain>`. For changed reconstructed behavior, run the corresponding bounded original-x86 comparisons and record actual outputs/skips/dependency stops. English `HANDOFF.md` must state API inputs, supported domain, mutation/callback order, original hashes/addresses, validation, and gaps. Core uses `docs/core/HANDOFF.md`; the other domains use their own module folder.

Commit the owned change, then run `python3 scripts/workstream.py integrate <domain>` **from that feature worktree**, when the user's task authorizes merge/push. The restart prompt grants that authorization. The helper locks the common Git directory, checks ownership, fetches main, merges it into the feature branch, pushes the feature branch, creates a separate merge candidate, runs all common local checks, and pushes non-forcibly to main. Remote races require merging and rerunning checks. A failure preserves the candidate for inspection. Never force-push main or use a blanket ours/theirs conflict resolution. The lock must cover the entire integration operation.
