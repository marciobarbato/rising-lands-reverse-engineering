# Documentation index

The maintained manuals below replace the scattered research handoffs. Historical wording, complete prior notes, frozen deliveries, and their hashes remain recoverable as described in [migration](MIGRATION.md). Read current status before using an old report as a statement about today's runtime.

**Start here:** the latest [coordinator handover (2026-10-30 07:00)](HANDOVER_CLAUDE_20261030_0700.md), then the top of [consolidated progress](PROGRESS.md) and [status](STATUS.md).

## Milestones at a glance (2026-10-30 07:00)

| Milestone | State | Record |
|---|---|---|
| M1 MONDE01 loaded | accepted at `927c7e5` | [`cxr-20261028-08-m1-acceptance.json`](../integracao/validacao/cxr-20261028-08-m1-acceptance.json) |
| M2 frames 0–9,200 without input (M2.1, M2.2, M2.3) | accepted at `32bb391`, `b9f4b5d`, `ea62eb4` | [`cxr-20261029-m2r7-m2-3-acceptance.json`](../integracao/validacao/cxr-20261029-m2r7-m2-3-acceptance.json) |
| M3.1 input path, P1/P2 part | accepted at `c9c85eb` (P1 1,002/1,002, P2 1,202/1,202 phases) | [`cxr-20261030-m3r1-m3-1-p1-p2-acceptance.json`](../integracao/validacao/cxr-20261030-m3r1-m3-1-p1-p2-acceptance.json) |
| M3.1 rest, M3.2–M3.5 | open; per-criterion state in [M3 plan](M3_PLAN.md#status-2026-10-30-0700) | — |
| M4 | open; the S1 victory and D1 defeat captures on the original exist | [M3 plan](M3_PLAN.md#status-2026-10-30-0700) |

## Coordination

| Document | Contents |
|---|---|
| [Coordinator handover 2026-10-30 07:00](HANDOVER_CLAUDE_20261030_0700.md) | Latest: overnight results, runs in flight at the MacBook pause, preserved `wip/*` branches, next steps, rules learned |
| [Coordinator handover 2026-10-30](HANDOVER_CLAUDE_20261030.md) | State at the M3R1 checkpoint, Codex/Mac mini sessions, key M3 facts from the probes |
| [Coordinator handover 2026-10-29](HANDOVER_CLAUDE_20261029.md) | State at M2.3 closure, machines, leases, working mode, Codex workstreams, architecture decisions |
| [Claude handover 2026-10-28](HANDOVER_CLAUDE_20261028.md) | Historical: the 2026-10-28 freeze, preserved writers/worktrees |
| [Consolidated progress](PROGRESS.md) | Milestone acceptance, per-round integrations, critical path, Portuguese executive summary; [snapshots](progress/README.md) |
| [Status](STATUS.md) | Current milestone state, per-front state and pointers |
| [Roadmap to MONDE01](ROADMAP_MONDE01.md) | Milestones, dependency map, fronts, oracle strategy, completion inventory |
| [M3/M4 plan](M3_PLAN.md) | Acceptance criteria and their current state, scripted-input capture, workstreams, the Rust engine decision, future features |
| [Parallel work](PARALLEL_WORK.md) | Fronts, ownership, the coordinator/Codex/Mac mini working mode, integration rules |
| [Restart prompt](RESTART_PROMPT.md) | Copyable coordinator prompt and individual front assignments |

## Domain manuals

| Manual | Contents |
|---|---|
| [Core](CORE.md) | Units, navigation, tasks, structure placement, and gate simulation; detailed notes in [core/](core/), including the [S1 coverage survey](core/S1_COVERAGE.md) |
| [Combat](COMBAT.md) | Targets, aiming, attacks, projectiles, raid fights, caller cadence, and dependencies |
| [Economy](ECONOMY.md) | Resource layout, buildings, production, work cycle, hunger, learning, and market transfers |
| [Graphics](GRAPHICS.md) | Bank IDs, opacity, composition, the render API, structures, objects, and sequences |
| [Missions](MISSIONS.md) | Mission loading stages, frame oracles, scripted-input captures, original caller inventory |
| [AI and runtime](AI_RUNTIME.md) | Dispatchers, AI kernels, VM operations, messages, the input path, and ownership with core |
| [Audio](AUDIO.md) | Sound banks, sample decoding, request queue, and the DirectSound boundary |
| [Native Rust engine](ENGINE.md) | Rust engine C ABI (1.0–1.6), frame logic, renderer, input, play mode, validation |
| [macOS playable](MACOS_PLAYABLE.md) | Building the app from one revision, live play on the Rust engine, input recording, Test A |
| [macOS preview](MACOS_PREVIEW.md) | Historical research preview: launching, rebuilding, immutable snapshots |

## Reference

| Manual | Contents |
|---|---|
| [Formats](FORMATS.md) | BIN/CUE, CMP, PIE, ETA, unit serialization, and PT-BR text |
| [Assets](ASSETS.md) | Asset extraction tooling and pinned external asset data |
| [Validation](VALIDATION.md) | Local checks, x86 opt-in, report semantics, and source verification |
| [Provider imports](PROVIDER_IMPORTS.md) | Same-process loading of the construction providers |
| [Ghidra and symbols](GHIDRA.md) | Toolchain, normalized PE, original SBL names, and analysis limits |
| [M1 oracle review](M1_ORACLE_REVIEW.md) | Historical: whole-MissionLoad oracle architecture review |
| [Workspace](WORKSPACE.md) | Repository, original media, converted assets, apps, and archives |
| [Organization checks](ORGANIZATION_CHECKS.md) | Historical: checks after the 2026-10-28 reorganization |
| [Migration](MIGRATION.md) | Preserved historical records, compatibility, and recovery |
