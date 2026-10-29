# Research status — Codex recovery, 2026-10-28

The recovery started at fetched8810b3730a0fb788af3eac2b447dea65372f597f. Verified research main now includes Core15 reset/map, raw AI initialization, Core16 bindings/classification, Missions11 complete placement and Core17 complete Chemin_Remap, pushed/reproduced at09d3953c6dda02ba6e4f6ca9ac61e51ca48782e6, followed by3Economy initializer queries at85dc8130cf45966f8cde6001b6ccb860d32d4db1. [PROGRESS](PROGRESS.md) records each round and all four stage dimensions; [Claude handover](HANDOVER_CLAUDE_20261028.md) records final freeze, pending work and exact next actions. No M1–M4 acceptance. Original-first methodology, ownership and quality gates are unchanged.

## Verified integrated scope

These findings come from committed history, domain contracts and preserved reports. Earlier domain results remain historical. Core15 and AI initialization recovery results below are fresh from this resumption, including mandatory integration gates and committed-main reproductions.

| Front | Integrated evidence and behavior | Remaining boundary |
|---|---|---|
| Core | Stage 14 discovery/light domain (`f8d9371`, main `7b7b969`): MONDE01 unit 15 and its type-2 structure's 13/10 radii are supported. Existing physical world, navigation, task/VM, pool/reset, placement and experience-queue providers remain available. | Complete Chemin_Remap is integrated/reproduced at09d3953; experience retrieval remains open; Stage15 terrain/minimap/reset providers are now validated/integrated at `b610bfa`; caller composition remains. |
| Missions | Stage 9 complete eight-loader auxiliary chain; Stage 10 reset-prefix composition (`a0e0211`, main `57aa441`) with explicit missing-provider stops. Stage11 complete unit+structure placement with actual providers is integrated/reproduced at7f617fa; mission-number and existence getters are available. | Close inherited raw-state/file-resource handlers and compose all load tails, then compare whole `MissionLoad`; events and `TestFinDeMission` remain separate. |
| AI/runtime | Stage1 contracts plus Stage2 bounded raw-memory IaReset/IaAlloc/IAResetAttaque, recovered from ad97e42 and integrated at `5d24c91`. Core retains VM/task primitives. | Concrete production adapters and Core experience retrieval remain needed for L9. Frame/unit/structure dispatchers, kernels, operations and messages remain open. |
| Economy | Structure habitation and economy `MissionLoad` initializer tails (`b6eebec`, main `8204deb`), plus prepared production through the supported cleanup boundary. | Natural production inventory is integrated at2456848 (research only); complete transport/work cycles remain open. |
| Combat | Stage 18 live state-1/24 attack chain through emission, projectile simulation, impact, damage and supported physical death (`248d055`, main `b602b07`); reset provider is integrated. | Real mission raid, AI messages, audio, diplomacy, level effects and building-target/turret/trap branches remain separate. |
| Graphics | Cache lifecycle and bounded `AffGame` composition (`7eff798`, checkpoint correction `d483dec`, main `0756062`). MONDE01 input is a pinned partial-load checkpoint. | Type-2 structure facade/lookup, overlays, unit types 1/8, HUD and remaining viewport/render paths; no complete loaded-mission frame. |
| Audio | Bank readers and IMA ADPCM decoding (`fa4a759`, `0fc99df`); fresh three-way report `9a0c171`; merge `8810b37`. Committed native/Python/capture comparisons pass for 551 bank sounds. | `PlaySnd_PostSound`, queues, `Manage`, lifecycle and actual playback remain open. |
| macOS | Existing app consumes an immutable committed revision in a synthetic training exercise via `compilar-jogável`. | Switch to real mission state at the M1 trigger. The training exercise is not MONDE01. |

All listed feature and merge commits are reachable from the fetched `origin/main` snapshot. Consult each domain manual and handoff for precise supported inputs, original executable identity, mutation order and validation limits. Original media and predecessor captures have been preserved.

## Pending local recovery

At initial recovery inspection all worktrees were clean; the shared integration lock was free and no earlier native comparison/integration child process was running. Claude application processes were still present, without a research child process at that inspection. Two old detached integration candidates remain preserved at `worktrees/integration-graphics-a0f20f22` and `worktrees/integration-macos-56537e42`.

| Front | Preserved local commit | Required recovery gate |
|---|---|---|
| Core | Preserved `a572e8c`, recovery `2f9d0df`, merge `b610bfa` | **Recovered/integrated/reproduced.** Fresh reset14/759entries/2139segments and discovery32/4293entries/10503segments pass,0 native skips/faults/limits. Core382/181optional; common gate passed. |
| AI/runtime | Preserved `ad97e42`, recovery `1e56e5c`, merge `5d24c91` | **Recovered/integrated/reproduced.** Fresh native36/36,0 skips/failures; local/domain36/4optional. Two failed initial cycle proofs preserved; final explicit repeated-state proof passed. Adapter/full MissionLoad remain open. |
| Economy | Inventory3868ce5/auditcbb0728 integrated at2456848; live-query implementation4181758 is validated/integrated/reproduced at85dc813. | Final disposition in the handover; natural production remains inventory only. |
| Audio | Already integrated at `8810b37` | Do not duplicate integration or rerun the full unchanged corpus without cause. Continue queue research as a new bounded stage. |

The coordinator reuses six archived Codex executor chats and creates only the missing AI/runtime chat. Work proceeds in waves of at most three active executors plus the coordinator. Heavy native runs, domain/integration checks and Ghidra are serialized separately. Historical Claude `local_` IDs are retained as references, never used as Codex chat IDs. Current dispatch and heavy-work ownership live in workspace `local-data/coordination/progress.json` and `CODEX_RESUME.md`.

## Milestones and estimate

M1 complete load, M2 advancing mission, M3 interactive original mission and M4 demonstrated objective/transitions have not been accepted. The next critical path is Core's remaining full-remap region/cleanup/final-return sequence, Core experience retrieval and concrete AI provider adaptation, then Missions' complete composition and whole-state oracle. The Core reset/map and raw AI initialization providers are already integrated. The old unit-15 discovery boundary is resolved.

MONDE01 starts with a type-2 Santuário, not a type-3 Armazém/CAVE. The objective condition must be established by `TestFinDeMission`, not inferred from briefing prose.

The coarse full-game estimate remains **50% (40–60%, change 0 percentage points)**. The inventory in [the roadmap](ROADMAP_MONDE01.md#inventory-for-the-completion-estimate) separates implemented, original-validated, integrated and real-mission-tested work. Recovering accurate status does not itself increase completion. Save/load, menus/campaign progression and broader original-game behavior remain beyond the immediate M1 work.

## Final timed handover

Development stops18:25BRT on28October2026; handover only until18:40. Preserve Core local handoff-only commit, Missions pushed Stage12checkpoint33a09a1 (scaffolde7ea60f), AI pushed adapter/proof checkpoint16e5ada (sourceWIP1a455b0), Graphics2921122, Audio c464dcd and six uncommitted Combat paths. Consult the final handover rather than replaying older recovery instructions.

Actual AI adapter fresh11case comparison passed before cutoff:2completeMONDE01+9explicitstoppedimages, all whole images/providerorder/checkedaliases equal. This is feature-only proof; fullsuite/domain/helper/mainintegration were NOTRUN. See handover for the exact commands and preserved remoteSHA.
