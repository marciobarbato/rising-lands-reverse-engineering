# Roadmap to a running original mission (MONDE01)

Coordinator architecture for the seven-front research round, written 2026-10-28 at main `2da89cd7655998f3b3f240be192b4b2badf94b63`. It replaces the four-chat plan as the authorized organization. Every claim below about reconstructed behavior refers to the committed contracts in the domain manuals; nothing here upgrades a bounded fixture into a running game. Original addresses apply only to executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

## Goal and milestones

The first major milestone is **loading MONDE01 exactly as the original does, running the complete mission, and comparing its behavior with the original executable**. MONDE01's PT-BR briefing (`WORLD/MONDE01.TXT`, read-only) sets the player goal: protect a cave and store 50 bags of food and 50 bags of stone in it, while the "Grupo dos Assassinos" raids the region. The map holds one structure (disk type byte +8 = 2, origin cell 2828) and 16 owner-0 units (disk type byte +1): three type 0, eight type 9 in state 14 at cell 3086, and single units of types 1, 7, 5, 5, 8. The hostile group is not serialized as units; it comes from the loaded attack table (`IALoadAttaqueIni`, 100×8-byte records) and the AI war/unit kernels. Economy confirmed from original tables during this round that structure type 2 is **not** the cave. The type-name table read by `BatimentGetTypeName 0x418af7` (`0x495d8c + type*52 + 0x13`) names type 2 `SANCTUAIRE` (PT-BR "Santuário") and type 3 `CAVE` (PT-BR "Armazém"). `BatimentInitCave 0x419112` counts only type 3, so MONDE01 starts with no cave and a zero warehouse count. Its structure 0 (owner 0, state 5) holds the eight type-9 colonists. The missions front must establish from the objective/end-condition trace whether the objective requires building a type-3 cave; the story does not settle it.

| Milestone | Definition | Acceptance evidence |
|---|---|---|
| **M1 MONDE01 loaded** | `MissionLoad 0x46c2cf` composed end to end from committed providers: reset prefix, filename, header prelude, complete `Chemin_Remap`, structure/unit loaders, all eight auxiliary loaders, `MissionPlaceTerrain` for units and structures, and the six initializer tails | Whole post-load state (every mapped buffer: terrain layers, regions/colors/search, 800 units, 1,000 structures, selections, Bags, tables, AI tables, players, market, technology) equals the native whole-`MissionLoad` oracle run described below; zero silent defaults; every unsupported branch is an explicit dependency exception with its original address |
| **M2 MONDE01 advances** | `CalculGame 0x42c868` frames run without human input from the M1 state: events, AI players, units, structures, projectiles, end-condition test | Per-frame whole-state equality with the native frame oracle for a declared number of frames, including the first scripted raid; explicit stops listed per frame |
| **M3 MONDE01 playable** | Frames composed by graphics from the live M2 state; human orders through the app; mission end detected by `TestFinDeMission` | App session on the real loaded mission; divergences from the original recorded per frame in `docs/MACOS_PLAYABLE.md` |
| **M4 Mission 1 complete** | Objective reached (cave protected, 50/50 bags stored) through reconstructed transport, production and combat; victory/loss transition observed | Original comparison of the end-condition evaluation and of the state sequence leading to it |

Loading terrain, an interactive demonstration or isolated routines passing their fixtures do **not** count as a mission running. Progress is reported per milestone with the four statuses *implemented*, *validated against the original*, *integrated on main* and *tested in a real mission*.

## Dependency map on the critical path

Status keys: **done** = integrated on main with original comparison; **partial** = bounded prefix or subset integrated; **open** = not reconstructed. Owners name the front that implements; consumers compose through committed contracts only.

### Phase L — complete `MissionLoad 0x46c2cf`

| Step | Original routines | Status | Owner | Notes |
|---|---|---|---|---|
| L1 Filename | `MakeMissionName 0x46c1b8` | done (missions S6) | missions | |
| L2 Reset prefix `0x46c2cf..0x46c396` | handles/globals, `TerrainReset 0x46b315`, `MiniMapReset 0x469f00`, `BatimentResetAll 0x41a75c`, `EnginResetAll 0x441659`, `ProjectileReset 0x46e00a`, message/balloon state (`BallonInit 0x441b6c`) | partial: unit/structure resets done (core); others open | missions orchestrates; core (terrain/minimap), combat (projectile pool reset), economy (balloon/market), ai-runtime (message tables) provide | Inventory the exact call order first; each missing reset is a named dependency, never a constructor zero |
| L3 Header prelude | `0x46c396..0x46c512` | done (missions S2) | missions | |
| L4 `Chemin_Remap 0x42ee1c` | reset prefix to `0x42eebd` done; `GlobalAlloc`/`GlobalLock`, two-pass classification, per-component region labeling and stacks, cleanup, final AL | partial (core S13) | core | Inventory for the allocation/classification continuation exists in core's worktree (`docs/core/REMAP_CLASSIFICATION.md`, uncommitted) |
| L5 Structure copy | inline `0x46c517..0x46c578` | done (missions S5) | missions | |
| L6 `LoadEngin 0x46acbf` | with `SelectionInit`, postload | done (missions S4, core S9, combat postload) | missions | |
| L7 Auxiliary loaders, in order | `LoadMine 0x47534a` done, `IALoadAttaqueIni 0x47c24d` done, `LoadBatimentGhost 0x47bcc7`, `LoadCadreInfluence 0x47c04a`, `LoadFinMission 0x458b05` done, `LoadCalculMissionDivers 0x47c30f`, `LoadObjectif 0x47c404` done, `LoadEntrerMonstre 0x47ac30` | partial (missions S3/S7) | missions | Four raw loaders remain; disk layouts are in `FORMATS.md`, runtime meaning is not |
| L8 `MissionPlaceTerrain 0x46c122` | unit scan done through `PlaceEngin`; capacity refresh done; structure scan: `PlaceBatiment` done (core), `BatimentHabitable`, `BatimentModifyMap(...,1)` | partial (missions S8, core S12) | missions orchestrates; core supplies `DecouvreTerrain 0x476851` for vision radius > 8 and `BatimentModifyMap`; economy supplies `BatimentHabitable` | Actual MONDE01 stops at unit 15 (radius 10) inside core's discovery boundary; this is the first blocker |
| L9 Initializer tails | `EnginInitTechnologie 0x441459`, `BatimentInitCave 0x419112`, `Engin_RetrieveExperimente 0x441623`, `PlayerRetrieve 0x46df41`, `IaReset 0x47f36e`, `MarcheResetAll 0x46027c` | partial: cave counts and selective market reset exist (economy) | economy (technology, cave, players, market), core (experience retrieval), ai-runtime (`IaReset`/`iaInit` tables) | Each tail is a separate bounded provider with its own original comparison |

### Phase R — frame loop `0x47500e` → `CalculGame 0x42c868`

| Step | Original routines | Status | Owner |
|---|---|---|---|
| R1 Cadence and clocks | counters near `0x475014`, `GameNextFrame 0x45d015`, draw divisor | partial (`ferramentas/cadencia.py`) | ai-runtime composes; core keeps the counter primitives |
| R2 Input | `InputGame 0x429278`, `ProcessInputGame 0x45edc0` | open; not required for M2 (no human input) | ai-runtime (dispatch), macos (UI mapping) |
| R3 Events | `EvenementInit 0x4580d4`, `EvenementEnCours`, `EvenementAffiche`, `EvenementEnd` | open | missions |
| R4 AI players | `iaCalculPlayer 0x47f927` orchestration (core `ia.py`), kernels `iagUnitNoyau 0x482936`, `iagVilleNoyau 0x48453c`, `iagRessNoyau 0x485183`, `iagWarNoyau 0x4866d7`, `iaSolver 0x47d314` VM (core `tarefas_ia.py`), world operations, messages `iagUnitSendMessage 0x4829c8`/`iagVilleSendMessage 0x484808`, `AvanceMonstre 0x47b283` | partial (VM control flow and five operations) | ai-runtime implements kernels/operations/messages; core keeps VM/task primitives |
| R5 Units | `CalculEnginNextEtape 0x456db5` dispatcher → movement (core), `CalculAttaqueEngin 0x451914` (combat), `CalculWorkEngin 0x44bc74`/`CalculTransporteEngin 0x44f2d4` (economy), `CalculEnginStatic 0x453062`, dying (core/combat) | partial per branch | ai-runtime owns the dispatcher skeleton; branches stay with their owners |
| R6 Structures | `CalculBatimentNextEtape 0x4281c7` → gates (core, done), `CalculTroupe 0x4259e6` production (economy, to cleanup boundary), construction/repair/market/nova (economy) | partial | ai-runtime skeleton; economy/core branches |
| R7 Projectiles | `ProjectileCalcul 0x46fc0f`, impacts, damage, death | done for supported modes (combat) | combat |
| R8 End condition | `TestFinDeMission 0x458606` and its 11 resolved queries | open | missions |
| R9 Audio | `PlaySnd_PostSound 0x48aa79`, `PlaySnd_Manage 0x48aaca`, HED/SND backend | open; explicit pending descriptors exist | audio (second wave, anticipated in the macOS chat; [contract](AUDIO.md)) |
| R10 Rendering | `AffGame 0x417698` frame orchestration, `InitCache 0x40fa38` | partial (graphics passes) | graphics |
| R11 Save/load | `GameSave 0x46bd45`, `GameLoad 0x46b88d`, `Sauve*`/`Load*` family | open | second wave |

## Validation strategy: from bounded fixtures to a mission oracle

Everything integrated so far is validated by bounded original-x86 intervals with synthetic memory (`ferramentas/emulador.py`), by original-only captures made before translation, and by whole-buffer comparisons. Those rules stay. M1 and M2 additionally need an **oracle for whole routines**:

1. **Declared bindings instead of Windows.** The harness stops at the game's own wrappers and at import thunks, never inside Windows: file read `0x458461`/seek `0x45848b` (already used by missions), file open/close wrappers (to be inventoried), `GlobalAlloc`/`GlobalLock`/`GlobalUnlock`/`GlobalFree` through `0x5231c0` and neighbors (core S14 plan), timers and sound posts (recorded, returning declared handles). Each binding records exact arguments and the fixture value returned. A report lists original entries, resumed segments, bound calls and stops separately.
2. **Whole-`MissionLoad` oracle (missions, on core's harness).** Run the intact `MissionLoad 0x46c2cf` for MONDE01 with the real ETA bytes supplied through the file bindings and a deterministic allocation arena. Snapshot every mapped buffer at the original return. Python `carregar_missao(1, ...)` must reproduce the same state. Partial runs stop at declared dependencies and compare the state at that checkpoint.
3. **Frame oracle (ai-runtime, on the same harness).** From the M1 snapshot, run `CalculGame 0x42c868` natively for N frames with no input, binding clock/sound/import calls. Compare whole state after every frame with the Python frame driver. Rendering is excluded from the oracle; graphics compares its frames separately against native `AffGame` runs over the same state.
4. **Harness extension ownership.** The generic binding facility belongs to core (`ferramentas/emulador.py`); mission/frame oracle scripts belong to their fronts. Nobody substitutes an engine routine with Python inside an oracle run; only declared external bindings are replaced.
5. **No fabricated success.** A binding that would need Windows semantics the fixture cannot provide (short reads, allocation failure, sound mixing) stops the run; the stop is reported, not papered over.

Unicorn JIT needs the ordinary macOS execution context; sandboxed SIGILL results are recorded as failures, not as skips.

## Seven fronts

| Front | Branch / worktree | Owned paths | Wave-1 mandate |
|---|---|---|---|
| Core and World Lifecycle | `feat/re-core` / `worktrees/re-core` | `ferramentas/`, `testes/`, `evidencias/`, `relatorios/`, `docs/CORE.md`, `docs/core/` | Physical/navigation providers for M1: discovery beyond radius 8, complete `Chemin_Remap`, remaining resets, experience retrieval, harness bindings |
| Missions and Runtime Integration | `feat/re-missions` / `worktrees/re-missions` | `pesquisas-paralelas/missoes/`, `docs/MISSIONS.md` | Compose `MissionLoad` end to end; remaining loaders; structure placement scan; whole-load oracle; then events and `TestFinDeMission` |
| AI and Runtime | `feat/re-ai-runtime` / `worktrees/re-ai-runtime` | `pesquisas-paralelas/ia-runtime/`, `docs/AI_RUNTIME.md` | Contracts with core/missions first; `iaInit`/`IaReset` and AI table initializers; frame and unit/structure dispatchers; AI kernels and operations for MONDE01 |
| Economy and Production | `feat/re-economy` / `worktrees/re-economy` | `pesquisas-paralelas/economia/`, `docs/ECONOMY.md` | Load-tail providers (`BatimentHabitable`, cave/technology/player initialization), natural production start and the transport cycle needed to store bags in the cave |
| Combat and Projectiles | `feat/re-combat` / `worktrees/re-combat` | `pesquisas-paralelas/combate/`, `docs/COMBAT.md` | Natural emission and runtime integration: live attack state machine through the unit dispatcher into pool, impact, damage and committed physical death; projectile pool reset for L2 |
| Graphics and Animation | `feat/re-graphics` / `worktrees/re-graphics` | `pesquisas-paralelas/graficos-animacao/`, `docs/GRAPHICS.md` | Complete frames (`AffGame`) from the real loaded state: cache initialization, terrain pass, sprite passes, projectiles, selection, over M1 snapshots |
| macOS Playable Build and Validation | `feat/macos-playable` / `worktrees/macos-playable` | `apps/macos-preview/`, `compilar-jogável`, `docs/MACOS_PLAYABLE.md` | Consume committed APIs at milestones only: M1 loaded-mission inspection, M2 running mission, M3 orders; record divergences |
| Coordinator maintenance | `coordinator/maintenance` / `worktrees/maintenance` | every shared path | Infrastructure, shared manuals, estimate, inventory, dependency arbitration |

`python3 scripts/workstream.py start <front>` and `python3 scripts/workstream.py integrate <front>` support all nine names (`core`, `combat`, `economy`, `graphics`, `missions`, `ai-runtime`, `audio`, `macos`, `maintenance`). Integration always runs the common checks; missions, ai-runtime and audio additionally run their native suites with `RISING_EMULAR=1`, and macos runs `compilar-jogável --development-ref HEAD`, all inside the detached candidate under the common lock.

### Wave-1 stage sequence per front

Each stage is one bounded slice: inventory from original bytes → original-only captures → implementation → fresh native comparison → handoff → commit → integrate → reproduce on main → next stage. Owners may reorder within their list when a dependency is not yet committed, but must not start a second implementation before the previous one is integrated.

**Core**
1. `DecouvreTerrain 0x476851` and the light/minimap tail for vision sums above 8, so actual MONDE01 unit 15 (radius 10) completes `PlaceEngin`. Completion: missions' Stage 8 MONDE01 fixture reaches the pre-structure checkpoint with native whole-state equality.
2. Commit the existing `REMAP_CLASSIFICATION.md` inventory, then the remap allocation/classification continuation with declared `GlobalAlloc`/`GlobalLock` bindings in the harness (generic binding facility published for other fronts).
3. Region labeling/component stacks, cleanup and the final `Chemin_Remap` return, compared against a native whole-routine run over MONDE01's layers.
4. `TerrainReset 0x46b315`, `MiniMapReset 0x469f00` and `Engin_RetrieveExperimente 0x441623` as exact providers; `BatimentModifyMap` variant used by structure placement.

**Missions**
1. Remaining raw loaders `LoadBatimentGhost`, `LoadCadreInfluence`, `LoadCalculMissionDivers`, `LoadEntrerMonstre` in original order (both callers), with original-only captures over all 38 maps. Independent of other fronts.
2. Reset-prefix inventory and composition `resetar_para_missao(...)` consuming committed core resets, with named dependencies for the missing ones.
3. Structure traversal of `MissionPlaceTerrain` once core/economy commit `BatimentModifyMap`/`BatimentHabitable`.
4. `carregar_missao(numero, ...)` end-to-end composition and the whole-`MissionLoad` oracle (M1 acceptance). Then events and `TestFinDeMission` for M2.

**AI and Runtime**
1. Contract stage: publish `docs/AI_RUNTIME.md` sections for dispatcher, kernels, VM operations and messages, with exact ownership agreed with core and missions (recorded in all three handoffs). No implementation before this is integrated.
2. `iaInit 0x47f328`/`IaReset 0x47f36e` and the group/city/resource/war table initializers (`iagUnitInit`, `iagVilleInit`, `iagRessInit`, `iagWarInit`, `listInit 0x47cfd0`) as exact table providers needed by L9.
3. `CalculGame` frame skeleton with its three gates and declared order, calling committed providers and stopping at named dependencies; frame oracle on the harness.
4. `CalculEnginNextEtape` state dispatcher for the states present in MONDE01, delegating each branch to its owner's committed API; then the AI kernels/operations used by the first raid.

**Economy**
1. `BatimentHabitable` and the complete `BatimentInitCave`, `EnginInitTechnologie`, `PlayerRetrieve` tails.
2. Natural production start from the structure dispatcher (`InitRecruteTroupe 0x4283e2` → `CalculTroupe`) including the terrain cleanup query `BatimentGetCase 0x41aee2`/`EteintTerrain`, with the pending sound descriptor kept explicit.
3. Transport cycle `CalculTransporteEngin`/`CalculWorkEngin` for bag collection and cave deposit, composed with core movement; this is the mission-1 objective path.

**Combat**
1. `ProjectileReset 0x46e00a` and attack-state reset needed by L2.
2. Live attack state machine entered from the unit dispatcher: `CalculAttaqueEngin 0x451914` → emission → pool → `ProjectileCalcul` → impact → damage → committed physical death, over a loaded world, with AI messages, audio and diplomacy as explicit stops.
3. Building-target damage branch and the lethal tails still undefined, as required by the raid on the cave.

**Graphics**
1. `InitCache 0x40fa38` and verified cache lifecycle, replacing synthetic cache payload binding.
2. `AffGame 0x417698` orchestration over an M1 snapshot: terrain pass, `AffVeget`, `AffBatiments`, `AffEngin`, projectiles, with native whole-frame comparison.
3. Wrapped/negative viewports and remaining building facades needed by MONDE01's structures.

**macOS playable**
- Triggered by the coordinator at M1 (loaded-mission inspection mode fed by `carregar_missao`), M2 (running mission with pause/speed), M3 (orders). Between triggers, maintain the consumer tests against committed APIs without rebuilding after every small change. The script keeps the exact name `compilar-jogável` and output `local-data/macos-playable/dist/RisingLands-ptbr.app`.

### Cross-front contracts requested in wave 1

| Provider → consumer | Contract |
|---|---|
| core → missions | `DecouvreTerrain` radius domain; `TerrainReset`; `MiniMapReset`; `BatimentModifyMap`; complete remap entry/return; harness binding facility |
| core → ai-runtime | Public VM entry points (`MaquinaTarefas`, `atualizar_ia` callback protocol, `OPERACOES` registry, message profiles); movement/arrival advancement API for the unit dispatcher |
| economy → missions | `BatimentHabitable`, `BatimentInitCave`, `EnginInitTechnologie`, `PlayerRetrieve` |
| economy → ai-runtime | Production/transport/work entry points per structure/unit state |
| combat → missions | `ProjectileReset`; postload already committed |
| combat → ai-runtime | `CalculAttaqueEngin` entry contract and the projectile pass entry |
| ai-runtime → missions | `IaReset`/`iaInit` and AI table layouts for L9; message tables for L2 |
| ai-runtime → everyone | Frame/unit/structure dispatcher call order and the per-branch contract each owner must satisfy |
| graphics → macos | Frame composition API over live state |
| missions → graphics/macos | `carregar_missao` result layout (M1 snapshot) |

A requested contract is recorded in the requester's handoff with the exact original address and consumed widths; the provider answers in its own handoff and manual. Nobody edits another owner's files.

## Rules that apply to every front

- **Original bytes first.** Every stage starts from exported intact intervals and original-only captures made before translation. REA/Ghidra output is complementary evidence; Watcom register conventions are checked against assembly.
- **Two identities.** The intact executable is the only execution oracle; the normalized PE (`26c4534b…64d0`) is analysis-only. Reports name both.
- **No artificial defaults.** A missing provider raises a named dependency at its original call site, retaining earlier effects. Constructor zeros, empty callbacks, swallowed exceptions and "no-op" guesses are rejected in review.
- **Flat-module hygiene.** Research modules share a flat import namespace; new module basenames must be unique across `ferramentas/`, the five research folders and the app (`pesquisas-paralelas/ia-runtime/testes/test_namespace.py` enforces it for the new front). Bootstrap through the owned `ambiente_*` modules and `integracao.providers`.
- **One stage at a time.** Validate, update the handoff, commit owned paths, integrate under the lock, verify ancestry from fetched `origin/main`, reproduce on main, then start the next stage. Finished work is never left unmerged.
- **Documentation language.** Manuals, handoffs and commits in English; player-facing text and audio in PT-BR; French symbols and historical evidence unchanged.
- **Reporting after each integrated stage:** gap closed; implementation/feature/merge SHAs with push confirmation; validation performed and remaining limits; the four statuses; coarse estimate with uncertainty and delta.

## Inventory for the completion estimate

The estimate stays approximately **50% (40–60%)** at the start of this round. It is reviewed from this inventory, not computed from counts of tests, files or native executions. A component moves only when its status column changes with original comparison.

| Component | Implemented | Validated vs original | Integrated | Mission-tested |
|---|---|---|---|---|
| File formats, readers, symbols | complete | complete | yes | n/a |
| World/navigation/tasks (core) | large subset | large subset | yes | no |
| Mission loading | prefixes and loaders (L1, L3, L5–L7 partial, L8 units) | yes | yes | no |
| Remapping | prefix | yes | yes | no |
| AI kernels, VM operations, messages | VM control flow, five operations, orchestration skeleton | partial | yes | no |
| Economy rules, production, market | large subset to cleanup boundary | yes | yes | no |
| Transport/work cycles | read-only status queries | partial | yes | no |
| Combat targeting, projectiles, damage, death | supported modes | yes | yes | no |
| Rendering passes and composition | terrain/sprite/projectile passes, caches | yes | yes | no |
| Frame loop, input, events | counters only | partial | yes | no |
| End conditions/objectives | table loaders | yes | yes | no |
| Audio (`PlaySnd_*`, `HandleSnd_*`, HED/SND) | pending descriptors only | no | n/a | no |
| Save/load (`GameSave`/`GameLoad`) | none | no | n/a | no |
| Menus, campaign progression, briefings | filename only | partial | yes | no |

## Second wave

When a wave-1 front closes its mandate, the coordinator reallocates it rather than opening an eighth executor:

- **Audio**: `PlaySnd_PostSound`/`PlaySnd_Manage`/`HandleSnd_*` queues and the HED/SND decoding backend, consuming the pending descriptors already published by core/economy/combat. On 2026-10-28 the human approved anticipating it in the macOS chat, which was idle until its M1 trigger. It is the `audio` front (`feat/re-audio`, `pesquisas-paralelas/audio/`, [contract](AUDIO.md)). No eighth executor exists: at the M1 trigger the chat returns to `macos` and audio pauses at its last integrated stage.
- **Save/load**: `GameSave 0x46bd45`/`GameLoad 0x46b88d` and the `Sauve*`/`Load*` family over the M1 state. Proposed owner: Missions after M2.
- **Input/menus/campaign**: `InputGame`, `MenuBefore`, `MissionNext`/`MissionReStart`, briefing display. Proposed owner: ai-runtime (dispatch) with macos (UI).

## Model difficulty monitoring

The coordinator reports a persistent observable difficulty only with evidence: repeated substantive errors, unresolved divergences despite available inputs, or inability to bound a stage after relevant attempts. Harness host errors (adapter types, sandbox SIGILL, lock waits) and read-only evidence gaps do not qualify. The human decides on model changes; nobody switches models automatically.
