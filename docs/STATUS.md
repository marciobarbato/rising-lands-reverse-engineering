# Research status — 2026-10-30 07:00

Development on the MacBook paused at 07:00 on 2026-10-30; the user stopped every Codex session at about 07:15. The Mac mini keeps its long native runs. Main is `3874fcc` at this update. Round-by-round evidence is in [PROGRESS](PROGRESS.md); the in-flight work, preserved branches and next steps are in [HANDOVER_CLAUDE_20261030_0700](HANDOVER_CLAUDE_20261030_0700.md). The 2026-10-28 recovery status that this file used to hold is preserved in the [CXR snapshots](progress/README.md) and in git history.

## Milestones

| Milestone | State | Record |
|---|---|---|
| M1 MONDE01 loaded | **accepted** at `927c7e5` | [M1 record](../integracao/validacao/cxr-20261028-08-m1-acceptance.json) |
| M2 frames 0–9,200 without input, first raid | **accepted**: M2.1 `32bb391`, M2.2 `b9f4b5d`, M2.3 and M2 `ea62eb4` (18,401/18,401 phases) | [M2.3 record](../integracao/validacao/cxr-20261029-m2r7-m2-3-acceptance.json) |
| M3.1 input path, P1/P2 part | **accepted** at `c9c85eb`: P1 1,002/1,002, P2 1,202/1,202 phases, 0 crossings, reproduced on both machines | [M3.1 P1/P2 record](../integracao/validacao/cxr-20261030-m3r1-m3-1-p1-p2-acceptance.json) |
| M3.1 input path, P6 part | **accepted** at `92fab50`: strict whole-state P6 (129–2400) 4,544/4,544 phases, 0 crossings, reproduced on both machines; the Rust engine reproduces it too | [M3.1 P6 record](../integracao/validacao/cxr-20261030-m3r2-m3-1-p6-acceptance.json) |
| M3.1 rest (S1 order windows), M3.2–M3.5 | open | [M3 plan status](M3_PLAN.md#status-2026-10-30-0700) |
| M4.1 victory, M4.2 defeat, M4.3 app | open; original captures of S1 (victory) and D1 (defeat) exist | [M3 plan status](M3_PLAN.md#status-2026-10-30-0700) |

## Original captures (Mac mini)

- **S1 wins MONDE01** on the intact executable: two independent runs from F0 (frames 129–17,050) give equal records (`82ec5ea`, on main). AL = 1 at 16,933, `MenuInit(0x13)` at 17,032, `MissionNext` at 17,043, no `MissionLoad`. Pass 2 (whole-state segments) is being captured; the MacBook ran 9,750–12,500.
- **D1 reaches the defeat branch**: the player unit count `0x4e1a3a` reaches 0 at 15,555; `PartieGetResultat` returns 0 at 15,655. The input is on `feat/re-missions` (`bab6c7c`), not yet on main; its replay check from F0 and packaging run on the mini.
- Probes P1–P7 and K1, each replay-equal on two runs; pass-2 windows P1, P2 and P6.

## State by front

| Front | Latest on main | Open |
|---|---|---|
| Core | All 16 S1 coverage gaps validated (windows a/b/c 1,410 comparisons, register queries 546, 0 mismatches); frame-125 minimap divergence explained; hunger, `TerrainEstGc`, `SetMiniMap` mode 4; [S1 coverage survey](core/S1_COVERAGE.md) | — |
| Economy | Exit position, hunger (state 19), sanctuary abandonment, `EnginRestaureEtat`, `BatimentEnleveMatiere`, cave meal and tag 19, all 0 mismatches | Transport states 18/20 (unvalidated WIP on `wip/*`) |
| Combat | Turret `BatimentPeutAttaquer`, tag 14, fatal raid path through death and recount (1,186 cases, 0 mismatches); fatal-window runner | Fatal windows for S1/D1 on the mini |
| Graphics | Render API 1.9 (K1 501/501, P4/P5 3,001/3,001), S1 end screens, P6 guard fixes | Glyphs, view origins (unvalidated WIP on `wip/*`) |
| AI/runtime | M3.1 P1/P2 proof; hunger, restoration, turret and Core providers wired; P6 planning diagnostic 4,544/4,544 phases; S1 proof driver ready | S1 windows once pass 2 lands (frame-2547 dependencies now on main: Core `provedor_recrutamento`, Economy BL) |
| Missions | S1 victory capture, probes, pass-2 windows | Pass-2 S1, D1 packaging (mini) |
| Audio | Sound-request provider and request log | — |
| Rust engine (`motor/`) | Stage 4 orders (ABI 1.5) and play mode (ABI 1.6): logic 0.26 ms/frame, logic plus render 0.65 ms | Chain past frame 220 (unvalidated WIP on `wip/*`) |
| macOS app | Live play on the Rust engine with orders (ABI 1.5); play mode 60 game frames/s, display ~120 fps; Test A answer half 155,597/155,597, state half P1 501/501, P2 601/601, P3/P6/P7 91/91, K1 12/12 up to the engine's stops | ABI 1.6 adoption (unvalidated WIP on `wip/*`); the 60 game-frames/s run with orders stops at frame 2,952 on a named renderer limit; Test B |

## Estimate

The coarse MONDE01 estimate is about **60% (50–70%)** (raised 2026-10-30 13:50); measured indicators — criteria accepted, the Python chain's S1 frame reach, Rust reach, Test A — are at the top of [PROGRESS](PROGRESS.md). It is reviewed only from the [roadmap inventory](ROADMAP_MONDE01.md#inventory-for-the-completion-estimate), never from counts of tests, files or runs. M3 (input and orders) and M4 (objectives, transport, combat on the victory path) remain the main uncertainty; save/load, menus and campaign progression are beyond MONDE01.

MONDE01 starts with a type-2 Santuário, not a type-3 CAVE. The objective is established by `TestFinDeMission`, not by the briefing prose.
