# Four-chat research workflow

The next round uses exactly four research owners. Each starts from the organized `origin/main` in its own worktree and `feat/` branch. The canonical checkout remains a stable entry point; simultaneous chats never share a mutable index, branch checkout, or report output directory.

| Chat/domain | Branch | Worktree under workspace | Write ownership | Next slice |
|---|---|---|---|---|
| Core | `feat/re-core` | `worktrees/re-core` | `ferramentas/`, `testes/`, `evidencias/`, `relatorios/`, `docs/CORE.md`, `docs/core/` | Structure allocation/initialization, lifecycle and real-mission/gate callers |
| Combat | `feat/re-combat` | `worktrees/re-combat` | `pesquisas-paralelas/combate/`, `docs/COMBAT.md` | Impact/damage consumers, missing attack-phase producers, bounded combat pipeline |
| Economy | `feat/re-economy` | `worktrees/re-economy` | `pesquisas-paralelas/economia/`, `docs/ECONOMY.md` | Production completion/spawn handoff, transport and higher-level market callers |
| Graphics | `feat/re-graphics` | `worktrees/re-graphics` | `pesquisas-paralelas/graficos-animacao/`, `docs/GRAPHICS.md` | Remaining building/gate sprite mapping and original render ordering |

## Starting

From the canonical repository, run the matching command once per chat:

```sh
python3 scripts/workstream.py start core
python3 scripts/workstream.py start combat
python3 scripts/workstream.py start economy
python3 scripts/workstream.py start graphics
```

The helper fetches main and creates or resumes only its named branch/worktree. It adds ignored links for existing original inputs and reference dependencies without replacing tracked manifests. Every subsequent tool/shell call uses that chat's explicit worktree path. Inspect `git status --short --branch` before editing. If resuming a preexisting branch, inspect its history and local changes first; do not reset or discard them.

The old `codex/*` checkouts under `archive/retired-worktrees/` are complete, merged records. New work does not continue there. If the same `feat/re-*` branch was used by an earlier round, choose a new agreed suffix before starting a new independent round rather than reusing an obsolete worktree without inspection.

## Working together

Read the shared status and your contract; independently reproduce the relevant baseline. Select one bounded, valuable slice supported by original bytes. Publish new API contracts and assumptions in your own handoff early. Include exact input widths, domain, original addresses/hash, mutation order, callbacks, failure behavior, and unimplemented dependencies. Keep external effects explicit until their owner implements them.

Core owns world state, occupancy, structure allocation/physical lifecycle, movement, and task effects. Combat owns attack/projectile/damage-request sequencing. Economy owns economic arithmetic, charging/progress, and economic callers. Graphics owns sprite IDs, clocks used for drawing, palette/shadow composition, and indexed render order. The same gate can be investigated independently: physical counter/collision changes are core; consuming that counter to select a sprite is graphics.

Read other workstreams for context, but do not import files from an actively changing worktree. Use committed revisions, written callback contracts, or immutable captures. Original media and linked private snapshots/dependencies are shared read-only. No shared writable Ghidra project, app build, report, or generated-artifact destination. Shared documentation and infrastructure are changed in a later serialized maintenance commit.

If one domain needs another's implementation, finish its independent investigation and declare the dependency. Exchange the smallest data/API contract. A worker may wait for a committed dependency or scope down its demonstrable scenario; it must not edit another owner's implementation to avoid a handoff.

## Completion and merging

1. Run the owning domain's local checks, changed behavior's differential tests, and a reproducible bounded demonstration when relevant. Report unsupported callbacks, skipped tests, expected exceptions, and reference-only behavior accurately.
2. Update the English domain manual and owned `HANDOFF.md`; keep PT-BR game content unchanged. Inspect the complete diff and commit only owned paths.
3. From that clean feature worktree, run `python3 scripts/workstream.py integrate <domain>`. This requires the task's authorization to push; the restart prompt explicitly includes it.
4. The helper acquires one advisory lock in the common Git directory, fetches main, enforces ownership, merges main into the feature branch, pushes the feature branch, then creates a detached integration worktree. It performs a `--no-ff` merge, runs all common local suites, and uses a normal non-force push to `main`.
5. If another machine advances remote main, the push is rejected; the helper fetches, merges that advance into the candidate, reruns checks, and retries up to three times. Authentication/policy failures and conflicts stop with the candidate preserved. Review conflicts semantically; never force or blindly choose an entire side.
6. On success, record the final feature commit and remote-main merge commit in the chat's response. Do not amend the branch afterward merely to record its own merge hash. Update a central overview only in a subsequent agreed maintenance pass.

Any finished domain can enter the queue; no cross-domain merge ordering is needed for an independent slice. If there is an implemented dependency, integrate the provider first. The lock prevents local simultaneous main pushes; non-force rejection handles writers elsewhere. No script bypasses remote branch protection. A rejected main push remains a reported integration failure until resolved under the repository's actual policy.

The common integration gate is local Python/reference-capture testing. It does not silently opt into all x86/JIT runs. Workers must run and record the differential coverage relevant to their change before integrating. Historical suite counts are not a substitute for new validation.
