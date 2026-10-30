# Parallel research workflow

The fronts below are the write owners; the coordinator's maintenance front owns every other path. Each front works from `origin/main` in its own worktree and branch. The canonical checkout remains a stable entry point; simultaneous executors never share a mutable index, branch checkout, or report output directory. The target is [a running original mission](ROADMAP_MONDE01.md); the current plan is [M3/M4](M3_PLAN.md). `python3 scripts/workstream.py fronts` prints the authoritative ownership table.

## Working mode (since 2026-10-29, current at 2026-10-30)

- **Coordinator: Claude**, in one chat on the MacBook. It dispatches work, reviews every delivery, integrates through `scripts/workstream.py`, records acceptances in `integracao/validacao/` and maintains the shared documents. It prefers fresh subagents with concise briefs over long-lived sessions.
- **Codex is a subordinate executor.** The coordinator dispatches it directly with `local-data/coordination/codex-bridge/codex_task.py` (`run --name --cd --brief [--full-access]`, `resume`, `list`, `quota`); briefs are files under `codex-bridge/briefs/`. One executor per front or worktree at a time, never Codex and a Claude agent on the same one. Codex never merges to main or records acceptance; the coordinator reviews its diff and integrates it. Fronts are split so that both weekly quotas are used.
- **Mac mini for long native runs** (multi-frame original captures, pass-2 segments, replay checks, second-machine reproductions). A Claude session there is the sole writer of `feat/re-missions` and pushes `runs/<front>/<tag>` branches for other fronts; the coordinator drives it without asking the user. The MacBook keeps translations, short native comparisons, chain proofs and integration.
- **Rust engine and macOS app** are Codex workstreams: `motor/` (integrated through maintenance) and `feat/macos-playable`.
- **Unvalidated work is parked, not merged.** When an executor stops mid-stage, its diff is committed to an `origin/wip/<front>-<time>` branch and the feature worktree is left clean at its pushed head.

### Rules learned

- **No foreign-file byte pins in tests.** A test that pins the exact bytes of another front's file deadlocks integrations (Core↔Economy twice, once in the engine's player pins). Bind the front's own files strictly; accept any foreign version that has a committed native run, otherwise skip with the rerun named.
- **Clean tree before `integrate`.** The helper merges main into the feature worktree, so it needs a clean tree. Never integrate while an executor is editing that worktree; park leftover WIP on a `wip/*` branch first.
- **Integrations serialize on their own.** `integrate` holds a blocking `flock`; launch integrations directly and let the lock order them. No `pgrep` wait loops: their own command lines match and they deadlock.
- **Rust gate pins by commit.** `sh motor/validate.sh` runs on every integration and reads its Python/Graphics references from fixed commits. If it fails, rerun it in the preserved candidate, then fix the pin in `motor/` through maintenance.
- **Mini fetch over HTTPS.** Over plain SSH, `git fetch` of the `git@github` remote hangs; fetch the public repository by its HTTPS URL. Symlink `.local/python` into new worktrees on both machines.
- **Cross-machine pass-2 segments work.** Rsync the snapshots and the pass-1 set to the MacBook, run `passo2_sondas.py politica --de --ate` for a frame range, and rsync each pickle back without `--delete`.
- **Prefer fresh Codex sessions over very long threads.** Long threads failed during compaction; start a new session with a handover brief. "Selected model is at capacity" failures usually clear when the same session is resumed later.
- **Disk.** Keep at least 20 GB free on both machines.

## Fronts

| Front | Branch | Worktree under workspace | Write ownership | Wave-1 mandate |
|---|---|---|---|---|
| Core and World Lifecycle | `feat/re-core` | `worktrees/re-core` | `ferramentas/`, `testes/`, `evidencias/`, `relatorios/`, `docs/CORE.md`, `docs/core/` | Physical/navigation providers for MONDE01 initialization: discovery beyond radius 8, complete `Chemin_Remap`, remaining resets, harness bindings |
| Missions and Runtime Integration | `feat/re-missions` | `worktrees/re-missions` | `pesquisas-paralelas/missoes/`, `docs/MISSIONS.md` | Remaining loaders, reset prefix, structure placement scan, end-to-end `MissionLoad` composition and oracle, then events/end conditions |
| AI and Runtime | `feat/re-ai-runtime` | `worktrees/re-ai-runtime` | `pesquisas-paralelas/ia-runtime/`, `docs/AI_RUNTIME.md` | Contracts first; AI table initializers; frame, unit and structure dispatchers; AI kernels/operations for the first raid |
| Economy and Production | `feat/re-economy` | `worktrees/re-economy` | `pesquisas-paralelas/economia/`, `docs/ECONOMY.md` | Load-tail providers, natural production start, transport/work cycle to store bags in the cave |
| Combat and Projectiles | `feat/re-combat` | `worktrees/re-combat` | `pesquisas-paralelas/combate/`, `docs/COMBAT.md` | Projectile reset, live attack state machine through the dispatcher into impact/damage/death, building-target branch |
| Graphics and Animation | `feat/re-graphics` | `worktrees/re-graphics` | `pesquisas-paralelas/graficos-animacao/`, `docs/GRAPHICS.md` | Cache initialization and complete `AffGame` frames over the real loaded state |
| Audio (second wave) | `feat/re-audio` | `worktrees/re-audio` | `pesquisas-paralelas/audio/`, `docs/AUDIO.md` | Sound banks, sample decoding and the request queue reached by `PlaySnd_PostSound`/`PlaySnd_Manage` |
| macOS Playable Build and Validation | `feat/macos-playable` | `worktrees/macos-playable` | `apps/macos-preview/`, `compilar-jogável`, `docs/MACOS_PLAYABLE.md` | Milestone-triggered consumer builds and divergence records |
| Coordinator maintenance | `coordinator/maintenance` | `worktrees/maintenance` | Every path not owned above, including `motor/`, `integracao/`, `scripts/`, shared manuals | Infrastructure, shared manuals, acceptance records, estimate and inventory; integrates the Rust engine (`motor/`, Codex) |

The wave-1 mandates in the last column are historical; current assignments come from the coordinator's briefs and the latest handover.

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
python3 scripts/workstream.py start audio       # macOS chat, second wave
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
4. The helper acquires one advisory lock in the common Git directory, fetches main, enforces ownership, merges main into the feature branch, pushes the feature branch, then creates a detached integration worktree. It performs a `--no-ff` merge, runs the common local suites plus the front's own validation (missions, ai-runtime and audio: their native suites with `RISING_EMULAR=1`; macos: `compilar-jogável --development-ref HEAD`), uses a normal non-force push to `main`, and verifies that the feature and merge commits are ancestors of fetched `origin/main`.
5. If another machine advances remote main, the push is rejected; the helper fetches, merges that advance into the candidate, reruns checks, and retries up to three times. Authentication/policy failures and conflicts stop with the candidate preserved. Review conflicts semantically; never force or blindly choose an entire side.
6. On success, record the implementation, final feature and remote-main merge commits in the chat's response and handoff. Do not amend the branch afterward merely to record its own merge hash. Update a central overview only in a subsequent agreed maintenance pass.

Any finished front can enter the queue; no cross-domain merge ordering is needed for an independent slice. If there is an implemented dependency, integrate the provider first. The lock prevents local simultaneous main pushes; non-force rejection handles writers elsewhere. No script bypasses remote branch protection. A rejected main push remains a reported integration failure until resolved under the repository's actual policy.

The common integration gate is local Python/reference-capture testing plus the front's declared native suite. It does not silently opt into all x86/JIT runs. Workers must run and record the differential coverage relevant to their change before integrating. Historical suite counts are not a substitute for new validation.

## Objective progress reporting

At the end of each execution round, the coordinator updates [the consolidated progress report](PROGRESS.md) and appends an immutable dated snapshot under [progress/](progress/README.md). Record previous/current verified main, M1–M4 unmet criteria, each L1–L9/R1–R11 stage's implementation/original-validation/integration/full-flow status, changes, three critical blockers with owners/dependencies, and source-linked evidence. Distinguish passed, skipped, not-run, failed, in-progress and dependency-stop results, and fresh runs from historical reports. Include an accessible Portuguese executive summary answering whether this round moved the project closer to the first original mission and why. This explicit user-requested summary is the exception to English technical documentation.

A local implementation or component comparison cannot be reported as complete mission playability. No test/commit/code/token count is a completion percentage. If retaining an estimate, explain its capability-inventory basis, uncertainty and change. Existing technical gates and domain ownership are unchanged; workers supply evidence through their owned handoffs and the coordinator maintains the shared report.
