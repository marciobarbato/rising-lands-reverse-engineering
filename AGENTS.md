# Repository instructions

Read the latest `docs/HANDOVER_CLAUDE_*.md`, `docs/STATUS.md`, `docs/M3_PLAN.md`, `docs/PARALLEL_WORK.md`, and your domain manual before changing research. This is the canonical repository; the directory above it is the local workspace. Do not initialize a second Git repository there.

## Language

Maintained documentation, handoffs, and commit messages are English. The game remains Brazilian Portuguese: preserve player-visible labels/errors, stories, objectives, unit/resource names, and audio. Preserve original French symbols and established code identifiers. Do not translate immutable historical evidence or regenerate its hashes.

## Front ownership

Each front works on one branch in a separate worktree created by `python3 scripts/workstream.py start <front>`. Never switch the canonical checkout's branch to do a worker's research. Use explicit working directories in shell/tool calls.

| Front | Branch / worktree | Owned paths |
|---|---|---|
| `core` | `feat/re-core` / `worktrees/re-core` | `ferramentas/`, `testes/`, `evidencias/`, `relatorios/`, `docs/CORE.md`, `docs/core/` |
| `missions` | `feat/re-missions` / `worktrees/re-missions` | `pesquisas-paralelas/missoes/`, `docs/MISSIONS.md` |
| `ai-runtime` | `feat/re-ai-runtime` / `worktrees/re-ai-runtime` | `pesquisas-paralelas/ia-runtime/`, `docs/AI_RUNTIME.md` |
| `economy` | `feat/re-economy` / `worktrees/re-economy` | `pesquisas-paralelas/economia/`, `docs/ECONOMY.md` |
| `combat` | `feat/re-combat` / `worktrees/re-combat` | `pesquisas-paralelas/combate/`, `docs/COMBAT.md` |
| `graphics` | `feat/re-graphics` / `worktrees/re-graphics` | `pesquisas-paralelas/graficos-animacao/`, `docs/GRAPHICS.md` |
| `audio` (second wave) | `feat/re-audio` / `worktrees/re-audio` | `pesquisas-paralelas/audio/`, `docs/AUDIO.md` |
| `macos` | `feat/macos-playable` / `worktrees/macos-playable` | `apps/macos-preview/`, `compilar-jogável`, `docs/MACOS_PLAYABLE.md` |
| `maintenance` (coordinator) | `coordinator/maintenance` / `worktrees/maintenance` | every path not owned above: scripts, `AGENTS.md`, root README, common manuals, requirements, Ghidra tooling, `integracao/`, `motor/` (Rust engine, integrated through maintenance) |

A worker records a cross-domain dependency in its own handoff and communicates the requested contract; it does not silently edit the other owner's files. The coordinator may seed a new front by adding its initial files, but never modifies or deletes research-owned files. Research modules share a flat import namespace: new module basenames must be unique across `ferramentas/`, the research folders and the app, and consumers bootstrap through the owned `ambiente_*` modules or `integracao.providers`.

## Working mode

- **Coordinator.** One Claude coordinator dispatches, reviews, integrates, records acceptances in `integracao/validacao/` and maintains the shared documents. It may use subagents with concise briefs.
- **Codex** is the coordinator's subordinate executor, dispatched through `local-data/coordination/codex-bridge/codex_task.py`. Codex never merges to main or records acceptance; the coordinator reviews its diff and integrates it.
- **One executor per front or worktree at a time**, never Codex and a Claude agent on the same one.
- **The Mac mini runs long native jobs** (multi-frame captures, pass-2 segments, replay checks, second-machine reproductions). Its Claude session is the sole writer of `feat/re-missions` and pushes `runs/<front>/<tag>` branches for other fronts. On the mini, fetch the public repository over HTTPS.
- **Unvalidated work is parked** on `origin/wip/<front>-<time>` branches, leaving the feature worktree clean at its pushed head; a `wip/*` branch is never integrated directly.

Rules learned (details in `docs/PARALLEL_WORK.md`):
- Tests never pin the exact bytes of another front's file. Bind the front's own files strictly; accept a foreign version that has a committed native run, otherwise skip with the rerun named.
- `integrate` needs a clean feature tree; never integrate while an executor is editing that worktree.
- `integrate` holds a blocking lock, so launch integrations directly; never write `pgrep` wait loops.
- The Rust gate (`sh motor/validate.sh`) pins its references by commit; fix a failing pin in `motor/` through maintenance, never by editing a research front's file.
- Prefer fresh Codex sessions with a handover brief over very long threads.
- Play mode must sustain at least 60 fps; per-frame audits stay in tests.

## Inputs and evidence

Original media at `../source/cd` and linked `.local`/graphics input copies are read-only. Do not share a writable Ghidra database. Never edit frozen releases, predecessor manifests, original-byte evidence, or pinned snapshots to make a new implementation pass. Add new evidence with explicit provenance and scope. Do not put worktrees, complete repository copies, commercial media, dependencies, caches, or app bundles inside tracked research folders. The intact executable is the only execution oracle; the normalized analysis PE is a different identity.

## Completion and integration

Run `python3 -B scripts/check.py --domain <front>` (missions, ai-runtime and audio included). For changed reconstructed behavior, run the corresponding bounded original-x86 comparisons and record actual outputs/skips/dependency stops. English `HANDOFF.md` must state API inputs, supported domain, mutation/callback order, original hashes/addresses, validation, and gaps. Core uses `docs/core/HANDOFF.md`; the other fronts use their own folder. Artificial defaults, empty callbacks or suppressed exceptions never stand in for unknown behavior.

Commit the owned change, then run `python3 scripts/workstream.py integrate <front>` **from that feature worktree**, when the user's task authorizes merge/push. The restart prompt grants that authorization. The helper locks the common Git directory, checks ownership, fetches main, merges it into the feature branch, pushes the feature branch, creates a separate merge candidate, runs the common checks plus the front's own validation, pushes non-forcibly to main and verifies that the feature and merge commits are reachable from fetched `origin/main`. Remote races require merging and rerunning checks. A failure preserves the candidate for inspection. Never force-push main or use a blanket ours/theirs conflict resolution. The lock must cover the entire integration operation. Integrate each stage before starting the next.
