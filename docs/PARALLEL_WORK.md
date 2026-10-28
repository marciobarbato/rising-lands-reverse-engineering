# Seven-front research workflow

The current round uses seven research owners plus the coordinator's maintenance front. Each starts from the organized `origin/main` in its own worktree and branch. The canonical checkout remains a stable entry point; simultaneous chats never share a mutable index, branch checkout, or report output directory. The target of the round is [a running original mission](ROADMAP_MONDE01.md).

| Front | Branch | Worktree under workspace | Write ownership | Wave-1 mandate |
|---|---|---|---|---|
| Core and World Lifecycle | `feat/re-core` | `worktrees/re-core` | `ferramentas/`, `testes/`, `evidencias/`, `relatorios/`, `docs/CORE.md`, `docs/core/` | Physical/navigation providers for MONDE01 initialization: discovery beyond radius 8, complete `Chemin_Remap`, remaining resets, harness bindings |
| Missions and Runtime Integration | `feat/re-missions` | `worktrees/re-missions` | `pesquisas-paralelas/missoes/`, `docs/MISSIONS.md` | Remaining loaders, reset prefix, structure placement scan, end-to-end `MissionLoad` composition and oracle, then events/end conditions |
| AI and Runtime | `feat/re-ai-runtime` | `worktrees/re-ai-runtime` | `pesquisas-paralelas/ia-runtime/`, `docs/AI_RUNTIME.md` | Contracts first; AI table initializers; frame, unit and structure dispatchers; AI kernels/operations for the first raid |
| Economy and Production | `feat/re-economy` | `worktrees/re-economy` | `pesquisas-paralelas/economia/`, `docs/ECONOMY.md` | Load-tail providers, natural production start, transport/work cycle to store bags in the cave |
| Combat and Projectiles | `feat/re-combat` | `worktrees/re-combat` | `pesquisas-paralelas/combate/`, `docs/COMBAT.md` | Projectile reset, live attack state machine through the dispatcher into impact/damage/death, building-target branch |
| Graphics and Animation | `feat/re-graphics` | `worktrees/re-graphics` | `pesquisas-paralelas/graficos-animacao/`, `docs/GRAPHICS.md` | Cache initialization and complete `AffGame` frames over the real loaded state |
| macOS Playable Build and Validation | `feat/macos-playable` | `worktrees/macos-playable` | `apps/macos-preview/`, `compilar-jogável`, `docs/MACOS_PLAYABLE.md` | Milestone-triggered consumer builds and divergence records |
| Coordinator maintenance | `coordinator/maintenance` | `worktrees/maintenance` | Every shared path | Infrastructure, shared manuals, estimate and inventory |

## Starting

From the canonical repository, run the matching command once per chat:

```sh
python3 scripts/workstream.py start core
python3 scripts/workstream.py start missions
python3 scripts/workstream.py start ai-runtime
python3 scripts/workstream.py start economy
python3 scripts/workstream.py start combat
python3 scripts/workstream.py start graphics
python3 scripts/workstream.py start macos
python3 scripts/workstream.py start maintenance   # coordinator only
python3 scripts/workstream.py fronts              # print the ownership table
```

The helper fetches main and creates or resumes only its named branch/worktree, tracking an existing remote branch when the local branch is absent. It adds ignored links for existing original inputs and reference dependencies without replacing tracked manifests. Every subsequent tool/shell call uses that chat's explicit worktree path. Inspect `git status --short --branch` before editing. If resuming a preexisting branch, inspect its history and local changes first; do not reset or discard them. Untracked notes left by an earlier round (for example core's `docs/core/REMAP_CLASSIFICATION.md`) are inputs to the next stage, not garbage.

The old `codex/*` checkouts under `archive/retired-worktrees/` are complete, merged records. New work does not continue there.

## Working together

Read the shared status, the roadmap and your contract; independently reproduce the relevant baseline. Select one bounded, valuable slice supported by original bytes. Publish new API contracts and assumptions in your own handoff early. Include exact input widths, domain, original addresses/hash, mutation order, callbacks, failure behavior, and unimplemented dependencies. Keep external effects explicit until their owner implements them.

Core owns world state, occupancy, structure allocation/physical lifecycle, movement, task effects and the VM/task primitives. Missions owns loading, remapping orchestration, mission tables, events and end conditions. AI/runtime owns the frame/unit/structure dispatchers, AI kernels, VM world operations and messages. Combat owns attack/projectile/damage-request sequencing. Economy owns economic arithmetic, charging/progress, production, transport and economic callers. Graphics owns sprite IDs, clocks used for drawing, palette/shadow composition, indexed render order and frame orchestration. The macOS front consumes committed APIs only. The same gate can be investigated independently: physical counter/collision changes are core; consuming that counter to select a sprite is graphics; calling the gate branch from the structure dispatcher is ai-runtime.

Read other workstreams for context, but do not import files from an actively changing worktree. Use committed revisions, written callback contracts, or immutable captures. Original media and linked private snapshots/dependencies are shared read-only. No shared writable Ghidra project, app build, report, or generated-artifact destination. Shared documentation and infrastructure are changed in a later serialized maintenance commit by the coordinator.

If one domain needs another's implementation, finish its independent investigation and declare the dependency. Exchange the smallest data/API contract. A worker may wait for a committed dependency or scope down its demonstrable scenario; it must not edit another owner's implementation to avoid a handoff. The roadmap lists the contracts requested for wave 1.

## Completion and merging

1. Run the owning front's local checks, changed behavior's differential tests, and a reproducible bounded demonstration when relevant. Report unsupported callbacks, skipped tests, expected exceptions, and reference-only behavior accurately.
2. Update the English domain manual and owned `HANDOFF.md`; keep PT-BR game content unchanged. Inspect the complete diff and commit only owned paths.
3. From that clean feature worktree, run `python3 scripts/workstream.py integrate <front>`. This requires the task's authorization to push; the restart prompt explicitly includes it.
4. The helper acquires one advisory lock in the common Git directory, fetches main, enforces ownership, merges main into the feature branch, pushes the feature branch, then creates a detached integration worktree. It performs a `--no-ff` merge, runs the common local suites plus the front's own validation (missions and ai-runtime: their native suites with `RISING_EMULAR=1`; macos: `compilar-jogável --development-ref HEAD`), uses a normal non-force push to `main`, and verifies that the feature and merge commits are ancestors of fetched `origin/main`.
5. If another machine advances remote main, the push is rejected; the helper fetches, merges that advance into the candidate, reruns checks, and retries up to three times. Authentication/policy failures and conflicts stop with the candidate preserved. Review conflicts semantically; never force or blindly choose an entire side.
6. On success, record the implementation, final feature and remote-main merge commits in the chat's response and handoff. Do not amend the branch afterward merely to record its own merge hash. Update a central overview only in a subsequent agreed maintenance pass.

Any finished front can enter the queue; no cross-domain merge ordering is needed for an independent slice. If there is an implemented dependency, integrate the provider first. The lock prevents local simultaneous main pushes; non-force rejection handles writers elsewhere. No script bypasses remote branch protection. A rejected main push remains a reported integration failure until resolved under the repository's actual policy.

The common integration gate is local Python/reference-capture testing plus the front's declared native suite. It does not silently opt into all x86/JIT runs. Workers must run and record the differential coverage relevant to their change before integrating. Historical suite counts are not a substitute for new validation.
