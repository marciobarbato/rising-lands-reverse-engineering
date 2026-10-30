# M3/M4 plan — interactive MONDE01, then mission completion

Status: DRAFT plan, published 2026-10-29 for the next coordinator, with the user's architecture decisions at the end. It is based on `origin/main` `8e90beb` and `origin/runs/core/coverage-9200` `7193999`. It establishes no acceptance. Refine it after M2.3 closes and after the scripted-input coverage capture (S1). Original addresses apply only to intact `RISING.EXE` SHA-256 `6c556520…8543fb`.

Evidence labels used on every claim:
- **[B] byte-proven**: original instruction/table/data bytes, accepted original reference bytes (M1/M2.2 captures), or counts from a native run of the intact executable (the coverage run).
- **[S] static**: synthesis from those bytes and owner contracts; reachability, ordering or meaning not executed.

Unlabelled imperative items (for example "capture X" or "owner Y delivers Z") are plan decisions, not claims about the game.

## 0. Starting point

- M1, M2.1 and M2.2 are accepted. M2.2: 257/257 phases equal, 999 logic bytes compared, 153,060 display-only bytes masked with writer/reader proof [B] (`docs/PROGRESS.md`). M2.3 (frame 9000 raid) is still running.
- Every accepted run uses the declared no-input answers `GetAsyncKeyState 0`, `PeekMessageA` no message and `GetCursorPos (0,0)` [B] (`cobertura-quadros-exibicao-9200.json:inputs`).
- The no-input run to frame 9200 enters 215 routines in 4,461 s (≈0.48 s/frame on the Mac mini) [B]. Of the 94 player-action map nodes, 78 are not imports; 21 of those are entered and 57 are **never entered** in that run (`MissionLoad` and `PlaceBatiment` among the 57 only because the run starts after the load). The 57 include `SetPlayerOrdre 0x45ecd4`, every `Set*EnginSelect`, `SetConstruitBatimentSelect 0x473a07`, `CalculConstruireBatiment 0x44ab60`, `CreerBatiment 0x41fea2`, `CalculWorkEngin 0x44bc74`, `CalculTransporteEngin 0x44f2d4`, `CalculAttaqueEngin 0x451914`, `PartieGetResultat 0x4585e4` and `MissionNext 0x46c08c` [B] (cross-join of `callgraph.json:nodes` with `routines`). `ProcessInputGame 0x45edc0` runs only on its no-command path (36,804 entries) [B].
- The cursor already affects logic. Cursor (0,0) edge-scrolls the view to origin (0,0) by frame 6, and the viewport size sets the 425 `rand` calls per frame in `NextAnimTerrain` [B] (`docs/GRAPHICS.md`, `PROGRESS.md` round 3). AffGame and logic share the permutation cursor `0x4e1d18` [B]. Input and display are therefore part of the logic oracle, not a UI layer on top of it.

**MONDE01 objective** [B] (accepted M1 bytes, `monde01-action-context.json`; evaluator translated in `pesquisas-paralelas/missoes/fim_missao.py`, 38/38 isolated cases):

| Record @ `0x4e1d20` | Bytes | Meaning in `testar_fim_missao` |
|---|---|---|
| 0 | `04 00 0300 0000 ffff ffff` | type 4: some structure with owner 0 and type 3 (`CAVE`) whose `CaseGetZoneInfluence 0x47bf66` equals zone word 0 (`0xffff` is not a wildcard; only `0x00ff` is) |
| 1 | `00 00 3200 …` | type 0: `TestRessource 0x4676e5` food ≥ 50 |
| 2, 9 | `01 00 3200 …` | type 1: stone ≥ 50 (tested twice) |
| 3–8 | `ff …` | inert (only a record-0 `0xff` blocks) |

- Victory sequence [B, local stores; ordering S]: AL is stored to `0x4e05a0` at `0x42d486`. On nonzero AL, `0x4e061c` is incremented; at 100 the game calls `PlaySnd_StopAllSound` and `MenuInit` mode `0x13` (`0x42d4d4→0x42c92c`). After the confirmation click, the result screen goes `PartieGetResultat` → `MissionNext 0x42ca6e`, which increments `0x496fe4` and does not call MissionLoad.
- Initial player-0 food and stone are 30 each (`0x4e2ea8 + id*8 + 2`, ids 1 and 2) [B] (`economia/M2_FRAME_INVENTORY.md`). Word `0x4e1a3a = 0xffff`, so completion is not forced at start [B].
- MONDE01 starts with **no cave**: structure 0 is type 2 `SANCTUAIRE`, origin cell 2828 = (12,11) on a 256-wide grid [B]. Builder unit 12 is type 7 `BATISSEUR`; units 13 and 14 are type 5, 11 is type 1, 15 is type 8 and 0–2 are soldiers. Units 3–10 are colonists inside the sanctuary (state 14, cell 3086 = (14,12)) [B].

## 1. Acceptance criteria (original first: capture → translation → per-frame comparison under a published mask)

**Common rule.** Each criterion is met only in this order:
1. An intact-executable capture with a committed **scripted input file** (§2), made before translation and replay-checked for determinism on two runs.
2. A Python chain fed the **same declared input answers**.
3. Per-phase whole-state equality under the published cumulative mask, with zero crossings and with the RNGs, allocation records, binding/boundary logs and registers compared.

The mask grows only by byte ranges with writer/reader proof. Any new display-only bytes under input (cursor, hover, drag box) are added this way, never by widening.

**M3 — interactive original MONDE01 on macOS**
- **M3.1 Input path.** The original capture S1 (§2) is reproduced by the Python chain through every order-issue window: each of the selection, move, CAVE-order and gather orders, plus 200 frames after each. `SetPlayerOrdre`/`ProcessInputGame` packets (tag and arguments at `[0x4e2458+4*player]`) are equal, as are the selection area `0x508728`, the unit order fields (`+2`, `+0xb2`, `+0xb7/+0xb8`, `+0xbe`, `+0x110`) and the whole state per phase.
- **M3.2 Live frames.** For every drawing phase of the M3.1 windows, render API ≥ 1.3 returns `parada = None`, including the HUD from `0x417B1C`, the cursor and the drag box `0x417AC8`. The result equals the native phase-end surface hash: the full 800×600 surface, not only rows 0..543.
- **M3.3 App equivalence.** The macOS app runs the live Python chain (today `apply_frame` raises `RuntimeContractPending` [B]). Its event mapper turns macOS events into the same per-poll declared answers (`GetCursorPos 0x475044`, `PeekMessageA`/`WndProc 0x4181a1` messages, `GetAsyncKeyState` via IAT `0x523290`) [S, poll sites B].
  - Test A: replaying S1's input file through the mapper yields an identical answer stream and identical per-frame state hashes.
  - Test B: a recorded human app session of at least 3,000 frames with one order of each kind, replayed on the intact executable, gives identical state hashes at every frame. Any divergence is listed per frame in `docs/MACOS_PLAYABLE.md`; M3 is accepted only with an empty list.
- **M3.4 End detection.** `TestFinDeMission 0x458606` is evaluated live each frame in the chain. Marks `0x4e1d88..0x4e1d91` and the latch `0x4e1d84` are equal to S1 per frame, including the first frame where record 0 becomes 1 (the cave exists).
- **M3.5 Rate.** The macOS app sustains **≥ 60 fps** in the real UI on the MacBook, with headroom (user requirement, 2026-10-29). Play mode runs without the per-frame audit and projection; those stay in the tests. Game speed is configurable and decoupled from display fps. This is not an equivalence criterion, but M3 is not "playable" without it.

**M4 — mission objectives, victory/defeat and transitions**
- **M4.1 Victory.** S1 runs on the original from load to victory: records 0, 1, 2 and 9 marked; AL = 1 stored at `0x42d486`; `0x4e061c` reaching 100; `MenuInit(0x13)`; the confirmation click; `MissionNext` returning 1; the `IaRechercheAjuste`/`Engin_StoreExperimente`/`RechercheStore`/`PlayerStore` stores. Stop before any MONDE02 `MissionLoad`. The Python chain equals it in every phase under the mask, through the `MissionNext` return.
- **M4.2 Defeat.** A separate capture D1 reaches result 0 at `0x4e1d84` and the failure branch of the result screen. The Python chain is equal over the same window. The trigger (`0x4e1a3a = 0` or another path) is unknown [S] and must be found by experiment, not assumed.
- **M4.3 App.** A human app session that wins MONDE01 replays on the original to the same victory frame with equal per-frame hashes.

## 2. Scripted-input coverage capture

**Harness.** Extend Missions' display scenario (`oraculo_exibicao_missao.py`) and Core's `ferramentas/cobrir_quadros_exibicao.py`. Neither changes engine code; only the declared answers become frame-scheduled.
- Input file schema `rising-lands/monde01-scripted-input/1`. Per frame k it holds the `GetCursorPos` answer, the ordered `PeekMessageA` messages (msg, wParam, lParam), and the `GetAsyncKeyState` table by vkey. Frames not listed keep the no-input answers.
- `DispatchMessageA` is bound to call the registered window procedure `WndProc 0x4181a1` natively. Its flag stores (`0x5099a8/aa` coordinates; `0x5099ae/af/b1/b2` for `0x201/0x202/0x204/0x205`) are byte-proven encodings [B]. Bypassing WndProc by poking those flags is not allowed.
- The run starts from the accepted M2.2 frame-128 checkpoint, so its prefix is already proven. The cursor stays at (0,0) until F0 = 129. View origin is (0,0) from frame 6 [B], so screen pixel = (32·x+16, 32·y+16) for cell (x,y) = (cell mod 256, cell div 256), playfield rows 0..543 [S: inferred from the 25×17 window and 32-px cells in GRAPHICS.md, not traced through `MouseZone`].
- Each click is a `WM_MOUSEMOVE` at frame k, `WM_LBUTTONDOWN` at k+1 and `WM_LBUTTONUP` at k+3, with `GetCursorPos` holding the same point from k to k+3. The cursor never rests on an edge after F0.

**Step 0 — static target extraction (MacBook, no emulation).** From the accepted M1 or M2.2-frame-128 state, using the committed providers, fix:
- the cell of unit 12 (`EnginGetCase`) and of units 13, 14, 11 and 15;
- zone-0 cells (`influencia_missao.zona_influencia`) and free cells near the sanctuary that are not in collision;
- food (field/`TerrainEstSac`) cells and stone (`TerrainEstMine`, `LoadMine 0x47534a` table) cells;
- the `MouseSetZone`/`MouseTestZone` HUD rectangles active after a builder is selected.

All of these are readable; none is published as a list today [S].

**Minimal sequence S1** (frames are relative to F0; waits are upper bounds that the author shortens after the probes):

| # | Input | Expected original path (static unless noted) |
|---|---|---|
| 1 | Click on unit 12's cell | tag 1 (or 36) via `SetPlayerOrdre` at `0x42ba20`/`0x42b9aa` → `SelectionEngin 0x4742dc`; `0x508728` = count 1, entry 12 [S] |
| 2 | Click the CAVE icon in the action zone (`AffZoneIconeAction`) | byte `0x496207` := 3 [S; **unproven**] |
| 3 | Click a zone-0 site cell near (12,11) | tag 4 at `0x42a03c`; packet +2 = 3, +4 = cell → `SetConstruitBatimentSelect` type-7 gate `0x473a71` → unit 12: `+2` = 11, `+0xbe` = 3, `+0xb2` = cell [S, setter stores B] |
| 4 | Wait (≤ 3,000 frames) | `EnginNextEtape` → `CalculConstruireBatiment` → `CreerBatiment` (`TestRessource`/`EnleveMatiere`, `PlaceBatiment 0x41c4ac`) → `BatimentConstruction 0x41cf59`; record-0 mark `0x4e1d88` = 1 [S] |
| 5 | Click unit 13, shift- or drag-add unit 14, click a food cell | tag 7 at `0x42b486` → `SetRecolteEngin` (`+2` = 5); depot tuple +4/+6/+8 via `SetDepotEnginSelect 0x45f037` [S] |
| 6 | Select a stone-capable unit (11, 15 or colonists, to be determined) and click a stone/mine cell | tag 6 (`SetMineEnginSelect 0x473324`) or 7; deposit via tag 19 (`SetDechargeCaveEnginSelect`) or 8 if the UI asks [S] |
| 7 | Wait until food ≥ 50 and stone ≥ 50 at `0x4e2ea8` | `TestFinDeMission` AL = 1 → `0x4e061c` 1..100 → `MenuInit(0x13)` [B branch encoding] |
| 8 | Click the confirmation on the result screen | `PartieGetResultat 0x42c9cc` → `MissionNext 0x42ca6e`; **stop** at its return |

S1 uses no keys. Key coverage is a separate short probe K1: arrow or edge scroll, plus any hotkeys `InputGame` tests through `GetAsyncKeyState`, recorded as M3 coverage only.

**Uncertain until it runs on the original:**
- whether the CAVE icon sets `0x496207` to 3, and its screen rectangle;
- the cave cost, and therefore the real food/stone targets (cost is charged by `EnleveMatiere` from the initial 30/30);
- placement validity and zone 0's extent;
- whether a cave under construction already passes record 0 (`BatimentExiste` + type);
- which unit type mines stone, and whether colonists must leave the sanctuary;
- the tag-8 producer;
- whether `TestRessource` reads player totals only. The map infers no per-cave storage rule [S].
- Whether victory comes **before frame 9000**. If not, the raid and combat are on the M4 path, and a player attack (tag 14 at `0x42a52c`/`0x42a5e6`/`0x42aecf`) is added to S1.

**Probes before the long run (MacBook, ≤ 500 frames each, from the frame-128 checkpoint):** P1 selection, P2 move (tag 5), P3 CAVE order, P4 food, P5 stone. Each probe fixes one row of S1, and every probe file is committed with its capture.

**Recorded outputs (S1 and the probes):**
1. Per-frame JSONL, extending the coverage schema: frame, counter `0x508f7c`, `new_routines` with **first-entry phase and caller return address**, entry counts, whole mapped-state SHA-256 and `dgroup_sha256`, game RNG `0x497164` plus the world and CRT RNGs, cursor `0x4e1d18`, view origin, and phase-end surface hash.
2. An input log: every declared answer consumed, with poll site, and the WndProc flag bytes after dispatch.
3. Per command: the packet before `SetPlayerOrdre` and at `ProcessInputGame` entry, the jump target from table `0x45ed20`, and the frame.
4. An objective trace per frame: `0x4e1d84..0x4e1d91`, `0x4e05a0`, `0x4e061c`, `0x4e1a3a`, the player-0 resource records and the structures by owner/type/cell.
5. Full checkpoints at F0, at each order, at cave creation, at the first AL = 1, at `MenuInit(0x13)` and every 1,000 frames, so phase-delta capture can run segment-parallel. Segment parallelism is already proven byte-equal on M2.2 [B].
6. The boundary log: `PlaySnd_*` and `MCICD_*` arguments, in order.

Pass 1 is coverage only, with cheap block hooks. Pass 2 is the M2.2-style delta capture per segment, for the windows a proof needs.

**Driving the split.** Join (1) with `callgraph.json` owners and run the `M2_3_PRONTIDAO.md` method. Each first-entered routine gets an owner, a provider, its validating captures and a status: direct / nested / display / boundary / not-wired / none. The result is the M3 and M4 readiness matrices, one per S1 segment.

## 3. Workstreams by owner (routines from `callgraph.json`; deliverables are captured first, then translated)

| Front | M3 | M4 |
|---|---|---|
| **Core** | Movement and pathfinding over **live memory** (`SetDeplaceEngin 0x4457d3`, `ResetOrdre 0x44357c`, `DeplaceEngin 0x44930c`, `AvanceEngin`, `CalculNextCase`, `CheminCalcul`, `OptimiseChemin`, `EnginNextCaseChemin`; shared with M2.3 [B, readiness matrix]). Selection: `SelectionEngin 0x4742dc`, `EnginAddSelection 0x4741cd`, `SelectionAddEngin`, `DeselectionEngin`, `DeSelectionGroupe 0x47268b`, `BatimentSelection 0x41b673`, `BatimentDeselectionner`. Order setters: `SetDeplaceEnginSelect 0x473e6e`, `SetConstruitBatimentSelect`, `SetEnginConstruitBatiment 0x4454ce`, `SetRecolteEngin*`, `SetTransporteEngin*`, `SetAttaqueEnginSelect 0x473dbf`. Harness: the scripted-input bindings | Shared parts of `CalculConstruireBatiment`/`CreerBatiment`/`BatimentConstruction`: `BatimentAlloc 0x418e95`, `PlaceBatiment`, `BatimentModifyMap`, discovery for the new structure |
| **AI/runtime** | `InputGame 0x429278` click/zone branches (`MouseZone 0x479cac`, `MouseEstDeplacer`, `KeyPressed`/`KeyUnPressed`/`KeyTestRelease` translations), `SetPlayerOrdre`, all `ProcessInputGame` cases used (1, 2, 3, 4, 5, 6, 7, 8, 14, 17, 18, 19, 36), slot cleanup `0x45f2de`, `GrabAllInput`, `InitInputPlayer`. New `EnginNextEtape` state branches: 11 (build), 5 (harvest), 18 (transport), 1 (attack), 2 (move). `BatimentNextEtape` with a second structure; the chain proof per segment | Result-screen `CalculGame` path (`MenuInit 0x4682bb` mode `0x13`, the confirm/click route), the proof through `MissionNext` |
| **Economy** | `TestRessource`, `GetRessourceStock 0x46769d`, `EnleveMatiere 0x46792c`, `CalculConstruireBatiment 0x44ab60`, `CreerBatiment`, `BatimentConstruction`, `BatimentConstruit 0x41c652`, `InitBatimentPlayer 0x41be88`, `BatimentHabitable` for a type-3 cave, `SetMineEnginSelect`, `SetDepotEnginSelect 0x47312c`, `SetRamasseEnginSelect` | Work and transport cycles: `CalculWorkEngin`, `TerrainRecolte 0x4781e8`, `MineRecolte 0x4755a7`, `TerrainRetireMatiere 0x476662`, `CalculTransporteEngin`, `BatimentAjouteMatiere 0x42340f`, `SetDechargeCaveEnginSelect`. Recruitment only if S1 needs it (`InitRecruteTroupe 0x4283e2`, `CalculTroupe`, `ConstruitPerso 0x423b9b`) |
| **Combat** | `SetAttaqueEngin 0x445a36` (needed only for M3 attack-order coverage) | `CalculAttaqueEngin`, `InfligeDegat 0x450874`, death, if the raid falls before victory or D1 uses it. `ProjectileInit`/`ProjectileCalcul` are ready for the raid states [B] |
| **Graphics** | Render API 1.3: HUD from `0x417B1C` (`AffZoneIconeAction`, `AffZoneInfo`, `AffMiniMap`, `AffCompteurMatiere`, `AffChrono`, `AffInfoAide`, `MessageBoxAffiche`, all entered natively [B]); cursor; drag box `0x417AC8`; selection frame/gauge `0x4022C8`/`0x4020EC`; `AffInfoSelection 0x410BE4`; unit bodies for types 1 and 8 (`0x41591F`); structure modes 0/1/2/6/7 (`0x408AC8`) and uninhabited states (`0x40892D`, `0x40863E`); `Cyclage` palette | Cave (type 3) facade and construction stages (`0x40F23B` family), harvest/transport/bag bodies, attack/corpse bodies over live state, mode-`0x13` result screen (today stop `0x4176A8`) |
| **Missions** | Step-0 target extraction, the scripted-input oracle scenario, S1/P1–P5/K1 captures on both machines, `EvenementEnCours`/`EvenementAffiche` if S1 enters them (R3 is open [B]), and live wiring of the 10 named stops of `fim_missao` | `TestFinDeMission6 0x4585ea`, `PartieGetResultat`, `MissionNext 0x46c08c`, `MissionReStart 0x46b57f` (defeat/retry), the D1 capture |
| **Audio** (Codex) | The ordered `PlaySnd_PostSound 0x48aa79`/`PlaySnd_Manage 0x48aaca` request log equal to S1's boundary log; playback in the app | `PlaySnd_StopAllSound` at victory, the result-screen `MCICD_*` music |
| **macOS** (Codex) | Live `apply_frame`; the event→declared-answer mapper (Windows 0x200–0x205 semantics, held/release timing, per-poll answers); the input recorder and replay exporter; Test A and Test B | Result-screen UI and the app-side victory/defeat flow; stop before MONDE02 |

The map lists the platform routines (`MouseZone`, `Key*`, `MouseEstDeplacer`, `WndProc`) under the macos owner [S]. This plan proposes that AI/runtime own their **translation**, because they write game memory and run inside `InputGame`, and that macOS own only the event mapping.

## 4. Ordering, critical path and parallelism

**Critical path:**
1. Close M2.3 (Core live movement and pathfinding, AI battle kernels).
2. Step 0 target extraction.
3. Probes P1–P5.
4. The S1 long run to victory.
5. The M3 readiness matrix per segment.
6. Core selection and order setters, plus AI `InputGame`/`ProcessInputGame` and the new `EnginNextEtape` states.
7. The M3.1 chain proof.
8. Economy construction, then the work/transport cycle.
9. M3.4, then the M4.1 chain proof.

Movement is on both M2.3's path and every player order's path [B, readiness matrix], so it gates everything after step 1.

**Parallel work and machine placement:**
- **Mac mini:** M2.3 to the end; then S1 pass 1 (≈0.5 s/frame, so 1–2 h per 10k frames [B rate, S extrapolation]); then pass-2 segment captures in parallel; then D1. Long runs stay off the MacBook.
- **MacBook:** step 0, probes P1–P5/K1 (minutes each), the translations and short native comparisons of every front, and the chain proofs per segment.
- **Graphics** can start now: the HUD, cursor and type-1/8 bodies are visible in the no-input M2.2/M2.3 states [B, stop list]. Only the cave and construction displays wait for S1.
- **Codex (macOS and Audio)** can start once the input-file schema is fixed (after step 3). The live `apply_frame` can be built against the M2.2 chain before any order exists. Integrate only after review, from its own branch.
- **Economy** can translate `TestRessource`/`EnleveMatiere`/`CreerBatiment` gates from isolated captures at the P3 checkpoint while S1 runs.
- **Missions** prepares D1 (defeat trigger search) in parallel with the M3 proofs.

## 5. Effort, uncertainty and risks

The unit is a coordinator round. Base rates [B, PROGRESS/ROADMAP]: M1 took about 8 rounds (CXR-01..08); M2.1 plus M2.2 took 6 (M2 rounds 1–6). The estimates below are judgement [S]. The ranges are wide because only 21 of the map's 78 non-import routines have run; the other 57 have never been executed, nor have their callees (the M2.3 raid alone added 56 new routines [B]).

| Stream | M3 (rounds) | M4 (extra rounds) | Main driver |
|---|---|---|---|
| Missions (harness, captures) | 2–4 | 2–3 | input binding, victory path discovery, D1 |
| Core | 4–8 | 1–3 | live movement/pathfinding (shared with M2.3), order setters |
| AI/runtime | 3–6 | 1–3 | `InputGame` branches, new unit states, chain proofs |
| Economy | 2–4 | 4–8 | construction plus work/transport cycles, the largest unexecuted body |
| Combat | 0–1 | 0–3 | only if the raid is on the victory path |
| Graphics | 4–7 | 2–4 | HUD/cursor/bodies, then cave/construction/work displays |
| macOS (Codex) | 3–6 | 1–2 | live frames, event mapping, record/replay |
| Audio (Codex) | 1–3 | 0–1 | off the critical path |
| **Overall (critical path)** | **8–16** | **+5–10** | **13–26 rounds to M4; confidence low (±50%)** |

**Main risks:**
- **Unknown routine volume.** Interval ends are next-symbol bounds, not proven function extents, and indirect calls are unresolved [B, map caveat]. S1 coverage is the only reliable count.
- **CAVE UI and cost.** `0x496207 = 3`, the cave cost and the placement rules are unproven [S]. A wrong guess costs a Mac mini rerun (1–3 h each); expect 3–6 S1 iterations.
- **Raid before victory.** If the 50/50 target plus cave cost cannot be met by frame 9000, combat and AI raid behaviour join M4's critical path.
- **Input determinism.** The original reads input at several poll sites (`0x475044`, WndProc, `GetAsyncKeyState` in `InputGame`), and the `0x203` path depends on cursor Y and window height [B]. The app must reproduce the per-poll answer stream exactly, keyed by game frame, not wall clock. Edge-scroll and the shared `0x4e1d18` cursor make display cadence part of logic [B].
- **Mask creep.** New input-time display bytes need writer/reader proofs. A mask hiding a logic byte would invalidate M3.1.
- **Live-play speed.** The Python chain's frame rate has not been measured for interactive play (M3.5).
- **Open owners.** Events (R3), save/load and menus are open [B]. S1 may enter an event script or a `MessageBox` path that no front owns.
- **External integration.** Codex review latency, and the flat-namespace collisions already seen between Graphics and Economy `construcoes` [B].

## Decision (2026-10-29, user): native engine in Rust

The validated Python reconstruction is the executable reference, but it is too slow to play in real time: about 0.5 s/frame for frame logic and about 0.3 s/frame for rendering, against the original's tens of frames per second (the exact rate is still to be measured).

Decision:
- the playable engine is a native **Rust** port;
- **C** only for small tooling, e.g. the Unicorn native memory hooks;
- **Swift** for the macOS shell;
- **Python** remains the proven reference.

- **New workstream "native engine" (Rust):**
  - a cargo workspace in a new owned path;
  - a C ABI library callable from Swift (the app) and from Python (differential testing);
  - wrapping 16- and 32-bit arithmetic made explicit, to stay byte-exact.
- **Migration order:**
  1. frame logic, the CalculGame pipeline and its providers, behind the same memory-view interface;
  2. the render API (`renderizar_quadro`, contract 1.x);
  3. the input and order paths as M3 translates them.
  Python and Rust coexist during migration.
- **Validation:**
  - per routine, Rust against the original-first captures (the same fixtures the Python routines use);
  - per frame, Rust's chained composition against the accepted M2.2/M2.3 evidence and the M3 captures, under the same published masks;
  - plus Rust against Python on randomized states, as a fast regression.
  - Acceptance claims stay byte-exact against the original evidence.
- **Performance target:** the declared play rate, measured once from the original by a timing probe, with headroom on both Macs.
- **Toolchain:** rustup on both Macs; the gates gain a Rust build and test step for this workstream.
- **Effort:** this adds to the M3 estimate. The port is mostly mechanical, because the Python reference and the captures already pin behaviour, so it parallelizes well across agents. The Python estimate per routine family roughly doubles for the families that must run in real time.

## Architecture decisions confirmed by the user (2026-10-29)

1. Engine state uses idiomatic Rust data structures. Byte-exact validation goes through an explicit, tested projection of that state onto the original memory layout, compared with the captures and the Python reference.
2. Simulation is fixed-step and deterministic: one tick is one logic frame, decoupled from host speed. The ticks/second rate is configurable, with a period-like default, because the original was CPU-speed regulated and runs too fast on modern machines. Wall-clock reads in logic come from a virtual clock tied to ticks. Speed never changes results.
3. Output is the original 800×600 8-bit frame, scaled by the app. The renderer is kept separable for a possible future HD version.
4. Extracted game assets are committed to the public repository with provenance hashes, and bundled with the app. The user accepts the risk and will make the repo private on any complaint.

## Future features requested by the user (after M4, outside fidelity acceptance)

- **Difficulty selector per mission.** "Original" stays the default: byte-exact and the only mode used in acceptance proofs. Optional modes adjust data-driven parameters in the Rust engine:
  - raid periods (MONDE01: 9000/10800);
  - monster group size and types;
  - AI aggressiveness;
  - production and gathering rates;
  - objective thresholds.
  The user recalls no configurable difficulty, but a hidden or unused parameter may exist. Low-priority static check during M3: look for difficulty-like fields in the mission data and the AI/raid code that are never set from UI. If found, base the modes on them; otherwise the modes are new, engine-level options.
- **HD renderer.** Replaces the separable 800×600 renderer; 800×600 remains the reference.
- **Adjustable game speed** (ticks/second), already part of the architecture.
