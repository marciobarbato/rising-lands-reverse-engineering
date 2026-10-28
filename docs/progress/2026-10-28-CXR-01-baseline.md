# Consolidated progress — MONDE01

Round: **CXR-20261028-01 (recovery, in progress)**. Snapshot: **28 October 2026, 16:17 BRT (America/Sao_Paulo)**. Verified research main: `8810b3730a0fb788af3eac2b447dea65372f597f`. Changes still in feature worktrees are identified separately below. [Roadmap](../ROADMAP_MONDE01.md), [current inventory](../STATUS.md), [round snapshots](README.md).

## Resumo executivo

**Estamos mais próximos de executar a primeira missão original? Sim, em relação à última rodada formalmente encerrada; ainda não demonstramos um novo avanço integrado de M1 nesta retomada.** São duas comparações diferentes, e ambas precisam ficar visíveis.

Na última rodada formal encerrada (`2da89cd`), a colocação das unidades parava no limite de visão da unidade 15. Desde então, esse limite foi resolvido: a varredura dos 16 registros de unidades de MONDE01 chega ao ponto anterior à colocação das construções, respeitando quais unidades devem ser colocadas no terreno. Também foram integrados os oito carregadores auxiliares e os inicializadores econômicos. Essas entregas retiraram obstáculos reais do carregamento, com comparações contra o executável original.

Nesta retomada recebemos a main em `8810b37`. Até este retrato, nenhuma nova etapa de M1 foi integrada depois dela. Core já aprovou uma nova validação dos resets e do minimapa e executa a regressão de descoberta; IA/runtime e Economia concluíram auditorias leves. Isso reduz dúvidas e prepara entregas, mas código local e testes de componentes ainda não carregam a missão inteira.

**O que funciona hoje:** leitura de dados reais, colocação das unidades até um ponto delimitado, várias regras de mundo/economia/combate, renderização parcial e decodificação dos bancos de som em cenários comprovados. O aplicativo continua usando um treino sintético. **Ainda não demonstramos MONDE01 carregado de ponta a ponta, avançando ou jogável.**

**Próximo resultado concreto esperado:** integrar os resets/mapa recuperados, terminar a validação da inicialização da IA e permitir à frente de Missões compor a colocação das construções. O carregamento completo ainda dependerá do remapeamento e da recuperação de experiência. A aprovação de M1 exigirá comparar todo o estado final carregado com o original; essa exigência permanece igual.

## Comparison windows and round boundaries

| Reference | What it establishes | Change recognized at this snapshot |
|---|---|---|
| Last formally closed/reported round: `2da89cd` (28 October, 13:41 BRT) | Historical cutoff recorded in `local-data/coordination/progress.json`, `last_notification` and `stop_after_current.final_main`. | Discovery, full auxiliary loading, habitation/economy tails and later bounded combat/rendering/audio work were delivered afterward. These are historical advances, not newly executed work in this recovery. |
| Human handover photograph: `0756062` (15:54 BRT) | Snapshot explicitly supplied by the user, not a revision to restore. | Audio bank/decoder Stage 1 was subsequently integrated at `8810b37`; useful original-game capability, but not an M1 loading blocker removed. |
| Current recovery starting main: `8810b37` (commit time 15:59 BRT; fetched at resumption) | Freshly fetched, clean canonical main at resumption. This is the baseline for the **next closed execution round**. | No new research merge yet. Fresh Core validation and AI/Economy audits are local preparation; no full-load success is claimed. |

An execution round closes when its scheduled bounded slice has reached a reported disposition: integrated and verified, failed with a preserved candidate, or explicitly pending at a declared dependency. Waiting for a long run does not create an extra round. At closure the coordinator updates this report and saves a new dated snapshot; the next round starts from that verified-main revision. A heartbeat without a material state change does not create artificial progress.

## Current milestone and acceptance

**Current milestone: M1 — load original MONDE01 completely and match the original post-load state. Status: not accepted.**

| Milestone | Acceptance criterion | Unmet criteria / current limit |
|---|---|---|
| M1 — complete load | Run `MissionLoad 0x46c2cf` through its real return, composing reset, remap, pools, all auxiliary loaders, placement and initializer tails. Match every declared loaded buffer, return and external-binding log with the intact executable. | Generic declared bindings and complete Chemin_Remap; integration/composition of recovered terrain/minimap resets; complete structure traversal; Core experience retrieval and AI reset integration; whole-load oracle and state comparison. No complete post-load snapshot exists. |
| M2 — advancing mission | From accepted M1 state, compare complete per-frame state for a declared run including events, AI, units, structures, projectiles, end-condition test and first scripted raid. | M1, runtime dispatchers/kernels/messages, required economy/combat branches, events/end-condition evaluation and frame oracle. No original mission frame sequence has been accepted. |
| M3 — interactive original mission | App consumes the accepted live mission state, composes its real frames and accepts human orders, with divergences recorded against the original. | M1/M2, facade/overlay/type and input coverage, app live-state integration. Existing training and partial frames do not satisfy this criterion. |
| M4 — proven objective and transition | Trace `TestFinDeMission` and demonstrate the required state sequence plus victory/defeat transition against the original. | End-condition implementation/query providers and real economy/transport/combat progression. Briefing mentions 50/50 bags; the actual condition must be traced. MONDE01 begins with a type-2 Santuário, not a type-3 Armazém. |

## Stage status: four independent dimensions

**Complete** below always means the named bounded stage, not the game. **Partial** names what is missing. **Local WIP** is excluded from integrated capability. **Not run** is distinct from a failed test or a declared dependency stop. The **full-flow** column requires the complete loading/frame path defined by the milestone; a real-data fixture stopping mid-call is not a pass there.

### Loading: L1–L9

| Stage / owner | Implementation | Validation against original | Integrated in main | Tested in complete flow |
|---|---|---|---|---|
| L1 Filename — Missions | Complete MakeMissionName supported domain. | Historical complete-call/filename/query comparisons. | Yes. | Not run through complete MissionLoad. |
| L2 Reset prefix — Missions/Core/Combat | Partial composition and UI/unit/structure/projectile providers. Terrain/minimap implementations local in Core Stage 15. | Historical whole-prefix checkpoints; **fresh** local reset/map run passed, discovery regression in progress. | Prefix/providers partial; Core Stage 15 not yet integrated. | Not run; current composed path has declared missing-provider stops. |
| L3 Header prelude — Missions | Complete bounded pre-remap prelude. | Historical native comparisons over actual map/camera inputs. | Yes. | Not run through complete MissionLoad. |
| L4 Remap — Core | Pre-allocation reset prefix only; continuation inventory committed. | Prefix validated; full allocation/classification/component-label/cleanup sequence not demonstrated. | Prefix only. | Not run; complete Chemin_Remap remains a blocker. |
| L5 Structure copy — Missions | Complete indexed copy supported domain. | Historical whole-pool original comparisons. | Yes. | Not run through complete MissionLoad. |
| L6 Unit loading — Missions/Core/Combat | LoadEngin + SelectionInit + supported postload composed. | Historical native real-map and bounded synthetic comparisons. | Yes. | Not run through complete MissionLoad. |
| L7 Eight auxiliary loaders — Missions | Complete raw-loader chain in original order. | Historical whole-image/read/profile-log equality; strict unsupported inputs stop explicitly. | Yes, Stage 9. | Not run through complete MissionLoad; runtime table meanings are separate. |
| L8 Terrain placement — Missions/Core/Economy | Unit scan complete to pre-structure checkpoint; habitation provider integrated. Structure traversal not composed; minimap provider local. | MONDE01 unit scan matches original at `0x46c16d`; habitation matches at `0x46c1a7`. Neither is full placement/load. | Units/habitation yes; structure loop and Core Stage 15 no. | Not run through complete MissionPlaceTerrain plus MissionLoad. |
| L9 Initializer tails — Economy/Core/AI | Four economy tails implemented; Core Engin_RetrieveExperimente missing; IaReset local WIP. | Economy tails historical original equality. AI capture replay passed locally; fresh native gate not run. | Economy yes; missing Core/AI tails no. | Not run as the complete six-tail sequence after real loading. |

### Runtime and presentation: R1–R11

| Stage / owner | Implementation | Validation against original | Integrated in main | Tested in complete flow |
|---|---|---|---|---|
| R1 Cadence/clocks — AI/Core | Core counters/RNG subset; runtime composition incomplete. | Bounded primitive validation; complete frame path not run. | Primitives yes; driver no. | Not run from accepted M1. |
| R2 Input — AI/macOS | Synthetic training controls; original InputGame/ProcessInputGame path open. | Original mission input path not run. | Training app only. | Not run in original mission. |
| R3 Events — Missions | EvenementInit/EnCours/Affiche/End open. | Not run for reconstructed events. | No. | Not run. |
| R4 AI players — AI/Core | Core orchestration/VM and five operations; kernels/world operations/messages incomplete. AI initialization local WIP belongs to L9. | Bounded VM/orchestration evidence; first-raid kernels not demonstrated. | Existing subset yes; kernels/messages no. | Not run from accepted M1. |
| R5 Unit dispatcher — AI with domain owners | Dispatcher/prelude not implemented; movement/attack/economy branch subsets exist. | Historical component comparisons, including bounded live attack chain. | Branch subsets yes; whole dispatcher no. | Not run for all units in a mission frame. |
| R6 Structure dispatcher — AI with Core/Economy | Gate and prepared-production subsets; natural start inventory only; dispatcher incomplete. | Existing gate/production fixtures; natural-start captures not yet executed. | Existing subsets yes; inventory/local work not integrated. | Not run for all structures in a mission frame. |
| R7 Projectiles — Combat | Pool/dispatch/impact/damage/death in supported modes. | Historical native lockstep; broader building-target/diplomacy/AI/audio paths remain open. | Supported subset yes. | Not run in original MONDE01 raid. |
| R8 End conditions — Missions | Table loading only; TestFinDeMission evaluation open. | Loader equality; victory/defeat predicate/transition not run. | Loaders yes; evaluation no. | Not run. |
| R9 Audio — Audio/macOS | Banks/IMA decoding; PostSound/queues/Manage/playback open. | Historical 551-sound three-way native/Python/capture equality; queue/playback not run. | Banks/decoder yes. | Not run during actual mission simulation/playback. |
| R10 Rendering — Graphics | Cache lifecycle and bounded AffGame; facade/lookup, overlays, types 1/8, HUD/other paths open. | Historical complete supported frames and named partial-checkpoint comparisons. | Bounded composition yes. | Not run over accepted complete M1/M2 state. |
| R11 Save/load — later owner | Original GameSave/GameLoad not reconstructed. | Not run. | No. | Not run. |

## Evolution and the next three critical blockers

**Removed since the last formally closed round:** the old unit-15 discovery boundary; four missing raw auxiliary loaders; required economy habitation and load-tail providers. Live attack and bounded frame/cache/audio deliveries also improve proven component coverage. These are already on the received main and must not be recounted as new recovery deliveries. [STATUS.md](../STATUS.md) lists their commits and exact remaining scope.

**This recovery so far:** preserved every worktree/capture; recovered the three pending research commits; Core fixed byte-view protection and passed fresh bounded reset/map comparisons; AI removed timeout-as-success logic in favor of an unrun deterministic cycle proof; Economy verified its original-byte inventory. **No new integrated M1 blocker has closed at this snapshot.**

| Priority | Blocker preventing M1 acceptance | Responsible owner | Dependency / concrete next evidence |
|---|---|---|---|
| 1 | Complete Chemin_Remap and generic declared bindings. | Core. | Allocation/classification, region labeling/stacks, cleanup/final return; whole-routine comparison over real MONDE01 layers. Missions' full-load oracle consumes this committed harness. |
| 2 | Complete and integrated initializer state. | AI/runtime for IaReset; Core for Engin_RetrieveExperimente. | Finish WIP native/cycle/domain gates and integration; implement/validate Core retrieval. Economy's four MissionLoad tails already exist. Require explicit inherited program-start/AI memory; no constructor defaults. |
| 3 | Complete load composition and whole-state proof. | Missions, consuming Core/AI/Economy/Combat. | Consume integrated terrain/minimap/reset providers and compose structure scan, all tails and real file/allocator bindings. Compare at MissionLoad return after blockers 1–2. Partial checkpoints remain evidence, not M1 acceptance. |

Audio queue work and graphics facades are valuable for M2/M3; they do not replace any of these M1 proofs. Exclusive heavy-work scheduling is a resource constraint, not an unimplemented game rule.

## Evidence ledger

All oracle results below use intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Normalized analysis PE `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` is analysis-only. Native entries/resumptions/test counts describe evidence scope, never completion percentage. Do not sum overlapping historical regressions as new capabilities.

| Evidence / command | When / result | Pass, skip, not-run and limitations |
|---|---|---|
| Core Stage 14 [discovery report](../../relatorios/descoberta-terreno-emulada.json), [MONDE01 checkpoint](../../relatorios/descoberta-terreno-monde01-emulada.json). Implementation [`f8d9371`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/f8d93718625eb8eaae954d4426651cac4506324d); merge [`7b7b969`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/7b7b96960cee0ec7868914e811f51b851fc27dba). | Historical native 32 tests; MONDE01 native/Python/capture checkpoint equality. | Passed historical runs. No full MissionLoad; new discovery regression is currently **in progress**, not yet passed. |
| Missions [Stage 9](../../pesquisas-paralelas/missoes/validacao/stage9-suite-x86.json), [Stage 10](../../pesquisas-paralelas/missoes/validacao/stage10-suite-x86.json), [handoff](../../pesquisas-paralelas/missoes/HANDOFF.md). Reset composition [`a0e0211`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/a0e02117435965df89e80c0fddc812d0e057b515) / merge [`57aa441`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/57aa4418fbbe7c80a01da0527b62949fb215f634). | Historical full native Stage 10: 71 passed, 0 skipped/errors/faults. Local optional-mode run had 27 skips. | Skips are not passes. An earlier loaded-machine timeout failed and was preserved; later isolated/full passes are separate. Dependency checkpoints do not prove complete load. |
| Economy [habitation](../../pesquisas-paralelas/economia/validacao-habitaveis-emulada.json), [initializer tails](../../pesquisas-paralelas/economia/validacao-cauda-carga-emulada.json), [handoff](../../pesquisas-paralelas/economia/HANDOFF.md). Tails [`b6eebec`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/b6eebec5f90393fb98ee9b6dc36f8588fff9a70f) / merge [`8204deb`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/8204deb304b38d8ee45a9a6edae125e661bfbce6). | Historical tails 11 passed / 435 original entries / 451 segments, 0 mismatches/faults/limits/skips. | Real MONDE01 inputs inside bounded fixtures; no complete post-load caller. Current natural-start inventory is not implementation. |
| Combat [live-attack report](../../pesquisas-paralelas/combate/validacao-ataque-vivo-emulada.json), [handoff](../../pesquisas-paralelas/combate/HANDOFF.md). [`248d055`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/248d0556c216d0a8161a1264525b24ccb69fe51f) / [`b602b07`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/b602b07e406ced7c8c67a9f011a8899718d32a87). | Historical 41 native tests passed; 0 errors/failures/skips. | Whole-state equality in supported chain; final named AI stop and missing building/audio/diplomacy branches remain. No real raid. |
| Graphics [frame comparison](../../pesquisas-paralelas/graficos-animacao/validacao/x86-quadro-jogo.json), [handoff](../../pesquisas-paralelas/graficos-animacao/HANDOFF.md). [`7eff798`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/7eff798b77cc694a6def54a4d5311883651005c9), pinned correction [`d483dec`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/d483dec37b62b570867a4777ca1763ad7c1aa93c), merge [`0756062`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/07560625beb22daafd338937482f2694bc2e39ad). | Historical six complete supported frames plus three named stops; 0 limits/skips. | MONDE01 input is a pinned partial-load fixture with explicit synthetic state; facade stop remains. |
| Audio [three-way comparison](../../pesquisas-paralelas/audio/validacao/x86-som.json), [handoff](../../pesquisas-paralelas/audio/HANDOFF.md). [`fa4a759`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/fa4a759d13107f84e24bd1f2af9d01d0b72403c3) / [`0fc99df`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/0fc99df90ebcadb69f8e6fa5f6603ceae89e79fd) / validation [`9a0c171`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/9a0c17136c1b4e19bdaf872032dbbfe99c96f053) / merge [`8810b37`](https://github.com/marciobarbato/rising-lands-reverse-engineering/commit/8810b3730a0fb788af3eac2b447dea65372f597f). | Historical report `passed=true`: A14+B102+P435 data headers, native/Python/capture differences empty. | Passed bank/decoder comparison; not rerun in this recovery. Queues/Manage/playback **not run**. |
| Core recovery: `python3 -B ferramentas/validar_reset_terreno.py --emular` with additive output, then required `validar_descoberta_terreno.py --emular`, then `scripts/check.py --domain core`. | **Fresh:** 14 reset/map tests passed, 759 original entries / 2,139 segments; 0 failures/errors/skips/faults/limits. Coordinator inspected `relatorios/recuperacao-stage15-reset-emulada.json` in Core’s feature worktree. Discovery still in progress. | Local changes not integrated. Fresh feature-only report: `/Users/marcio/git/Rising Lands/worktrees/re-core/relatorios/recuperacao-stage15-reset-emulada.json`; full log `.local/recuperacao-stage15-reset.log`. The integrated revision/link will be pinned at round closure. Historical 755-entry report `relatorios/reset-terreno-emulada.json` remains unchanged in the Core feature stage and must not be relabeled fresh. |
| AI recovery at local WIP `ad97e42`: captured/static replay and additive byte audit. | **Fresh light:** 8 passed; 3 explicitly skipped native tests. | Fresh x86/cycle proof, heavy domain gate and integration **not executed**. Replay is not an independent new native run. Original capture retained unchanged. |
| Economy recovery at local inventory `3868ce5`: read-only byte/hash audit. | **Fresh static:** all 10 intervals, 3 tables and predecessor identities match. | No original execution/capture, domain gate or integration in this light window. Proposed captures are a plan, not results. Withdrawn apparent syntax defect was an output-boundary reading error; no Core defect demonstrated. |
| Coordinator reconciliation: `b13bbb6`; documentation-link validation, `git diff --check`, documented-commit ancestry checks. | **Fresh:** passed lightweight checks. | Common integration gate/push pending heavy slot. Documentation itself adds visibility, not gameplay. |

## Estimate and interpretation

Historical full-original-game estimate retained: **approximately 50%, uncertainty band 40–60%, change 0 percentage points**. This is a qualitative engineering judgment over the roadmap's capability inventory: formats/world/navigation, loading/remap, AI/runtime, economy/transport, combat, rendering, audio, input/events/objectives, save/load and campaign. It is **not** an arithmetic ratio of completed rows, functions, tests, commits or code, and the band is not a statistical confidence interval. Large unknowns in integrated runtime and later-game behavior justify retaining the uncertainty.

No new accepted load/playability milestone justifies increasing the estimate at this snapshot. Component fidelity can improve while integrated playability remains unproven. M1–M4 acceptance and removal of the named critical blockers are the primary progress measures.

## Updating this report

The coordinator owns this shared report. At every execution-round closure: compare the previous and current freshly verified main SHAs; update all four status dimensions; identify actual blocker changes; attach new commands/results and unrun/skipped/failed boundaries; refresh the top three blockers and Portuguese summary; save a dated immutable copy under `docs/progress/`. Record pending local work even if main did not advance. Preserve prior snapshots and evidence. Workers provide evidence in their owned handoffs; technical quality, ownership, original-first capture and integration gates remain unchanged.
