# Restart prompt for four collaborating chats

Paste the coordinator prompt into a new chat for this project after the organization commit is available on `origin/main`. It explicitly requests four new chats, authorizes coordination messages between them, and authorizes each completed feature to merge/push through the queue. This file is a prompt; the organization task itself does not launch the research chats.

## Coordinator prompt

```text
Continue the reverse engineering of the Brazilian edition of Rising Lands.

Create exactly four new collaborating chats in this project: Core and World Lifecycle, Combat and Projectiles, Economy and Production, and Graphics and Animation. Use the available chat-creation tools, inspect the project inventory to select this repository, and dispatch all four assignments below without waiting for the first worker to finish. I authorize coordination messages between the coordinator and these four chats, and among these four chats, for this research round. Do not create additional workers.

Canonical repository: /Users/marcio/git/Rising Lands/engenharia-reversa
Workspace: /Users/marcio/git/Rising Lands
Read AGENTS.md, docs/README.md, docs/STATUS.md, docs/PARALLEL_WORK.md, and docs/WORKSPACE.md before dispatch. Fetch origin/main and verify that the organization baseline, English manuals, apps/macos-preview source, and scripts/workstream.py are committed there. If they are not available, report the concrete missing prerequisite rather than launching workers against an old layout.

Each worker must create/resume its own isolated worktree using python3 scripts/workstream.py start <domain>, and then use that worktree explicitly for every file or shell operation. Merely creating four chats in the same project does not isolate their Git index. The worktree and branch names are specified below. Inspect any preexisting worktree/branch before resuming; preserve uncommitted work.

All maintained documentation and commit messages must be English. Keep every player-facing game string, mission story/objective, name, accent, and audio in PT-BR. Preserve original French evidence symbols and existing API identifiers. Treat original media, private reference snapshots/dependencies, and historical release manifests as read-only. Never change evidence to match an implementation.

Choose one meaningful bounded slice per worker, grounded in original bytes and the documented gaps. Implement it, publish exact supported inputs/effects and remaining dependencies, add useful differential or captured-buffer validation, update the owned English documentation and HANDOFF.md, and finish the slice. Do not broaden into another owner's implementation. Communicate callback/interface requests through the authorized chat messages and the owning handoff. Read committed versions or immutable captures; never depend on another live worktree's files.

I authorize all four workers to commit their completed features, push their feat/ branches, and merge and push to origin/main after their checks pass. Each worker must use python3 scripts/workstream.py integrate <domain> from its clean feature worktree. That helper serializes the complete fetch/merge/test/non-force-push operation under one shared lock. Never force-push main, bypass branch protections, merge unverified work, or resolve conflicts blindly. If the remote advances, merge the new main and rerun the candidate checks. If integration fails, preserve the reviewable candidate and report the actual blocker.

Shared scripts, common documentation, requirements, AGENTS.md, Ghidra infrastructure, and apps/ are reserved for a separate integration/maintenance change. Each worker edits only the paths assigned below. Core owns physical gate/world state; graphics owns interpreting that state for rendering. Economy owns cost/progress; core owns world allocation. Combat publishes damage requests/callbacks without rewriting navigation.

Follow progress through compact status/wait tools. Help resolve cross-domain contracts, and prioritize an independent demonstrable slice if a dependency is not yet implemented. Do not report old x86 counts as freshly rerun. At the end report each chat, worktree, feat branch/commit, actual validation, remote-main merge commit, and remaining gaps. Verify all four successful integrations are reachable from origin/main; explicitly identify any unfinished integration. Do not claim the full game is complete.

Assignments:
1. Core: domain core, feat/re-core, worktrees/re-core. Read docs/CORE.md. Own ferramentas/, testes/, evidencias/, relatorios/, docs/CORE.md, docs/core/. Investigate structure allocation/initialization and lifecycle callers, real-mission loading/remapping, or global gate dispatch. Publish allocation/lifecycle callbacks needed by economy and state inputs needed by graphics. Keep economics and sprite mapping outside your implementation. Handoff: docs/core/HANDOFF.md.
2. Combat: domain combat, feat/re-combat, worktrees/re-combat. Read docs/COMBAT.md. Own pesquisas-paralelas/combate/ and docs/COMBAT.md. Trace original impact/damage consumers or missing +0x8A=2/3 producers and connect a bounded supported combat scenario through explicit callbacks. Preserve projectile pool/update/RNG order; do not invent missing phases. Handoff: pesquisas-paralelas/combate/HANDOFF.md.
3. Economy: domain economy, feat/re-economy, worktrees/re-economy. Read docs/ECONOMY.md. Own pesquisas-paralelas/economia/ and docs/ECONOMY.md. Investigate unit production completion/spawn handoff, transport credit, or higher-level market callers. Preserve resource IDs, signedness, x87 rounding, partial mutations, and explicit balloon/exit dependencies. Publish core callbacks instead of implementing world allocation/navigation. Handoff: pesquisas-paralelas/economia/HANDOFF.md.
4. Graphics: domain graphics, feat/re-graphics, worktrees/re-graphics. Read docs/GRAPHICS.md. Own pesquisas-paralelas/graficos-animacao/ and docs/GRAPHICS.md. Investigate remaining building/gate sprite mappings or render-order callers. Compare original indexed pixel buffers, opacity, palette/shadow behavior, and anchors. Preserve previous frozen stages and predecessor hashes; do not infer economic meaning or change physical gate behavior. Handoff: pesquisas-paralelas/graficos-animacao/HANDOFF.md.
```

## Starting the chats manually

If you prefer to open the four chats yourself, paste the common worker prompt plus one matching assignment into each chat. No coordinator is needed for integration serialization; the common lock and remote push checks still apply.

```text
Work as the <DOMAIN> owner for the next Rising Lands reverse-engineering round. Read /Users/marcio/git/Rising Lands/engenharia-reversa/AGENTS.md, docs/STATUS.md, docs/PARALLEL_WORK.md, and your domain manual. Use scripts/workstream.py start <DOMAIN> and work only in the resulting feat/re-<DOMAIN> worktree and owned paths. Use the matching assignment in docs/RESTART_PROMPT.md.

I authorize this chat to coordinate with the other three research chats for this round, commit and push its completed feat/ branch, then merge and push to origin/main using scripts/workstream.py integrate <DOMAIN> after appropriate local and original-x86/captured-buffer checks. Preserve evidence, obey the merge lock, never force-push, and report real failures. Keep documentation English and the game PT-BR. Complete one meaningful bounded slice, update your HANDOFF.md, and report feature and remote-main commits plus actual tests and remaining gaps.
```
