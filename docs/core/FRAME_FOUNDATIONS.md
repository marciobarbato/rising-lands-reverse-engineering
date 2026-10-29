# Frame foundations of `CalculGame 0x42c868` (M2 Core inventory)

Static inventory, 2026-10-28, branch `feat/re-core` at main `81ebbf9`. Original executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; the normalized analysis PE is not used. Every interval, hash, operand-derived read/write set, callee list and whole-code reference list below is regenerated from the intact bytes by `python3 -B ferramentas/extrair_fundacoes_quadro.py` into [`evidencias/fundacoes-quadro/manifesto.json`](../../evidencias/fundacoes-quadro/manifesto.json) with one `.asm` file per interval. Nothing in this section was executed.

## Frame entry and order (proven from `0x42d1da..0x42d4f5` and the state table `0x42c804`)

`ProgIteration 0x47500e` runs once per Windows iteration:
1. It runs the counter prefix `0x475014..0x475041`. The u32 `0x508f7c` is incremented. Then the u32 `0x508f80` is incremented if the new `0x508f7c` is even, and the u32 `0x508f84` if it is divisible by 3. All three wrap; this is `cadencia.avancar_contadores`.
2. It calls `GetCursorPos` into a stack POINT, and stores the low words as u16 at `0x5099a8`/`0x5099aa`.
3. It calls `CalculGame` and then `AffGame`.
4. It clears the input-edge byte pairs `0x5099af`/`0x5099ae` and `0x5099b2`/`0x5099b1` when the first byte of each pair is nonzero.

`CalculGame` dispatches on the u8 state `0x4e2f78`, which must be at most 24, through the table `0x42c804`.
- **State 0** (`0x42d1da`) is the new-mission load. It runs `MouseInit`, `InitCache` and `InitGouttes` and sets three flags. It then calls `MissionLoad` (or `MissionLoadName` when the network byte `0x4e0730` is set). The M1 return is `0x42d22d`.
- From `0x42d27f` the load case continues with `RestoreAll` and then `SetClipping(ax=0, dx=0, bx=width*32-1, cx=height*32-1)`. The width and height are the u16 viewport size `0x508724`/`0x508726`.
- It then stores **zero** into the counters `0x508f7c`, `0x508f80` and `0x508f84`, in that order (`0x42d2be..0x42d2ca`). It calls `MenuInit(al=player 0x508041, edx=0x12, ecx=1)` and then `InitGameZone(eax=1, edx=0)`. It falls through into `PlayerAttaqueReset`, which is the body shared with state 18.
- **State 18** (`0x12`) enters at `0x42d2de`. This is the per-frame path: `PlayerAttaqueReset` → `EvenementEnCours` (a nonzero AL ends the call) → the CD branch → the per-player input loop → `ProcessInputGame`×4. Then comes the gate at `0x42d3c0`: the frame body runs if the state is `0x12`, or if it is `0x10` and the network byte is set. The body is `MessageBoxCalcul`, `GameNextFrame`, `CalculIconeAction`, `ProjectileCalcul`, `CalculEnginNextEtape`, `CalculBatimentNextEtape`, `RechercheCalcul`, `PlayerInitAllianceCompteur`, `SetUpdateChamp`, `UpdateChamp`, `CalculMatiere`, `CalculCompteurMarche(al=player)`, `CalculCompteurProposition(al=player, edx=0)`, `NextAnimTerrain(ax=u16 0x508720, dx=u16 0x508722)`, then `NextAnimVegetFullMap()` if the network byte is set or `NextAnimVeget(ax, dx)` if it is not, then `PlayerAttaqueCalculSympa`, and, only if the network byte is clear, `TestFinDeMission(al=player)`.

**Consequence for M2.** The CalculGame call that loads the mission continues into one frame body in the same call, provided `MenuInit(..., 0x12, ...)` leaves state `0x12`. That condition was not executed here; the Missions entry trace decides it. That first frame sees all three counters equal to 0. The next `ProgIteration` makes the counter 1 before the second frame.

## Per-routine inventory

Ranges are end-exclusive. "World" means the stores are read by game-logic routines; the manifest's `code_references` lists each reader.

| Routine | Interval / SHA-256 prefix | ABI | Reads | Writes | Callees | Class | Owner |
|---|---|---|---|---|---|---|---|
| Counter prefix of `ProgIteration` | `0x475014..0x475041` `0bca7d80` | none | u32 `0x508f7c`/`80`/`84` | same | — | **game state**: `0x508f7c` is read by 54 routines, including `BatimentNextEtape`, `EnginNextEtape`, `iagWarNoyau`, `AvanceMonstre`, `InfligeDegat` and `SetUpdateChamp` | Core (`cadencia.avancar_contadores`) |
| Load counter reset | `0x42d2be..0x42d2d0`, inside CalculGame | none | — | u32 zeros at `0x508f7c`, `0x508f80`, `0x508f84` | — | game state | ai-runtime composes; Core supplies the primitive |
| `GameNextFrame` | `0x45d015..0x45d01c` `a9e9abc6` | no register is consumed or changed apart from the INC flags | u32 `0x496d40` | u32 `0x496d40`+1 (wraps) | — | game counter **with no code consumer**: `0x496d40` occurs only in this instruction and in no DGROUP pointer | Core |
| `Random` | `0x4704dc..0x470520` `14a68ad1` | EAX out = the new state; EBX/ECX/EDX preserved | u32 `0x497164` | u32 `0x497164` | — | game RNG (world) | Core (`candidatos_rota.aleatorio_caminhos`, existing) |
| `Randomize` | `0x470520..0x470527` | EAX in; EAX out = EAX+1 | — | `0x497164` = EAX+1 | — | provenance (ProgInit) | Core |
| `SetRandomSeed` | `0x470527..0x47054c` | EAX in. If EAX=0: state=1, EAX out 0. Otherwise state = EAX mod 0x7fffffff (unsigned), EAX out = the quotient; EBX/EDX preserved | — | `0x497164` | — | no code caller | Core |
| `GetRandomSeed` | `0x47054c..0x470552` | EAX out = state | `0x497164` | — | — | no code caller | Core |
| `iaRandom` | `0x489728..0x4897a4` `3b27a044` | EAX = a signed limit. If >0: advance the state with the same arithmetic as Random, then EAX out = state mod limit (unsigned). If <0: state = (−limit) srem 0x7fffffff (signed IDIV), EAX out 0. If =0: state = `timeGetTime()` mod 0x7fffffff (unsigned), EAX out 0. EBX/ECX/EDX/ESI preserved | u32 `0x498db4` | u32 `0x498db4` | `0x493a24` → `jmp [0x5234a4]` WINMM.timeGetTime (only when the limit is 0) | AI RNG; the frame reaches it through `iagWarNoyau`, `iagWarSetMode`, `iagWarStartBuildUnits` and `iagWarSetWait` | Core (complete paths; `cadencia.proximo_aleatorio` covers only limit>0) |
| `LongRand` → CRT `rand` | `0x45841b` jmp `0x48c51d..0x48c541` `9a1282e3` | EAX out = (seed'>>16)&0x7fff, with seed' = seed·0x41c64e6d+0x3039 (u32). EDX/ECX preserved | the thread-data pointer: `[0x4990cc]` = `0x48e7c7`, which returns `[0x522244]`; the seed is u32 at thread+0xc | the same seed | `0x48c513` (getter+0xc) | the CRT LCG, a **third** RNG; the frame uses it in `NextAnimTerrain` | Core |
| `InitRand` table | producer `0x4583bc..0x45841b` | — | — | a 256-byte permutation at `0x4e1c18` and the u8 cursor `0x4e1d18` (=0) | `memset`, `rand` | **fourth** RNG source; each consumer reads `0x4e1c18[cursor]` and then stores cursor+1 (u8) | Core (primitive) |
| `SetUpdateChamp` | `0x475328..0x47534a` `4125ba37` | no consumed output | u32 `0x508f7c`, u16 period `0x4973ea` (written by `BatimentLoadCaract`) | u8 `0x509952`=1 when counter mod period = 0; period 0 raises #DE | — | world (field growth) | **Economy** (`extracao.RecursosTerreno.agendar_campos`, committed) |
| `UpdateChamp` + `ScanNouvellePatate` | `0x478806..0x478a01` `f2c9eb78`; `0x478319..0x478806` `d5ab38be` | no consumed output | flag `0x509952`, u16 row `0x4973e8`, and the tile, object and attribute grids | the object grid `[0x507d74]`, the row and the flag | `Random` | world: crops on the object grid, which `CheminCalcul`/`AvanceEngin`/`TerrainEstChampi` read | **Economy** (`atualizar_campos`, committed); consumes Core `Random` |
| `NextAnimTerrain` | `0x477700..0x47790d` `367d82ac`, exits through `0x4774f2` → `0x475bf8` | AX=x and DX=y u16 viewport origin; EAX/EDX clobbered, others restored | the viewport size u16 `0x508724`/`0x508726`, counter bit 0, the tile/object/animation grids, the cursor | tile grid u16 (water cycle `0x95..0x9d` → `0x5d`/`0x94`; `0x251/0x252` +4 when the animation byte ≠0; `0x255/0x256` −4), object byte `0x1b` on tiles `0x8b..0x92`/`0x6d` when the object is 0 and `LongRand()%0x400==0`, and the cursor | `LongRand` | **world**: tile grid read by `TerrainEstEau`/`TerrainEstObstacleNaturel`/...; objects read by pathing | Graphics (per the ai-runtime/Graphics contract); see the cross-front findings below |
| `NextAnimVeget` | `0x4772ec..0x4774fa` `76891268`, epilogue `0x475bf8` | as above | counter bits 0–1, the object/animation grids, the cursor, the viewport size | object and animation grids, the cursor | — | **world**: objects 0x1b/0x37 are removed when their animation byte reaches 16 (it advances on even frames), 0x38..0x3d decay to the object below at 64 (0x38 and 0x3b are removed instead), and 0x3e..0x41 are removed at 32 (it advances every frame) | Graphics |
| `NextAnimVegetFullMap` | `0x4774fa..0x477700` `1b48f09a` | no arguments | the same as `NextAnimVeget` over 256×256 | the same | — | world; only on the network path | Graphics |
| `CalculNextReflect` | `0x47fbea..0x47fbfd` `1c1e95b1` | AL=player, DL=`MissionGetNum` low byte; AL out=1, which the caller ignores | — | — | `iaCalculPlayer 0x47f927` | AI | ai-runtime |
| `SetClipping` | `0x40f519..0x40f535` `73755c55` | AX/BX/DX/CX | — | u16 `0x49a020`/`0x49a022`/`0x49a01c`/`0x49a01e` | — | display only: read by the blitters, `AffGame` and `AffZoneJeu` | Graphics |
| `InitGameZone` | `0x471830..0x472047` `415f5262` | EAX zone set (1..4), EDX | the viewport size, the screen size `0x49a018`/`0x49a01a`, `0x497285`, `0x508f90` | only through `MouseSetZone` (16-byte records at `0x5099b4+16·i`, max index `0x50a9b8`) and `MouseTestZone` (`0x50a9b4`/`0x50a9b6`) | MiniMap/Marche position and size queries, `ChercheContacteur`, `PlayerEstContacterPourAlliance`, `MessageBoxExiste`, `MenuGetNbItem`, `MissionGetNum` | UI/input. The direct stores are mouse zones only; the purity of the queries was not proven here | macOS/UI |
| `PlayerAttaqueReset` | `0x46d628..0x46d629` `ae3f4619` | — | — | — | — | **a single `RET`**, an empty body that runs every frame | ai-runtime (composition; nothing to implement) |

The callers never consume the clobbered EAX/EDX of the Core/Graphics world routines. The next instruction or callee overwrites them before any read: `CalculIconeAction`, `UpdateChamp`, `CalculMatiere` (it clears AH, then writes EAX before reading it), `mov al,[0x4e0730]`, and `PlayerAttaqueCalculSympa`. The manifest records those entries.

## Random sources the frame touches

| Source | State | Advanced by (in the frame) | Notes |
|---|---|---|---|
| World Park–Miller | u32 `0x497164` | `Random`: units, structures, projectiles, `UpdateChamp`, monsters | Core `candidatos_rota.aleatorio_caminhos` is the arithmetic; missions/economy consume it |
| AI Park–Miller | u32 `0x498db4` | `iaRandom`: AI war kernel | The limit=0 path reads the clock; the startup `IaAlloc` used it with a declared clock |
| CRT LCG | u32 at `[0x522244]+0xc` | `LongRand` in `NextAnimTerrain` | Lives in the CRT thread block: in the M1 capture this is block `crt_thread_data` at `0x3400000` |
| Permutation cursor | the table `0x4e1c18[256]` and the u8 `0x4e1d18` | `NextAnimTerrain`, `NextAnimVeget(FullMap)`, the CalculGame CD branch, **and rendering**: `AffBatiments`, `AffCorpsEngin`, `AffDeplaceEngin`, `AffVeget` and `DDFlipPage` | Shared between display and world (see below) |

## Cross-front findings proven from the bytes

1. **Rendering advances a cursor that world routines consume.** `NextAnimTerrain`/`NextAnimVeget` decide world stores from `0x4e1c18[0x4e1d18]`. `AffBatiments`, `AffCorpsEngin`, `AffDeplaceEngin`, `AffVeget` and `DDFlipPage` advance the same cursor during `AffGame`, which runs after every `CalculGame`. `AffGame` is filtered by the F1–F4 draw divisor (`cadencia.deve_desenhar`). So the world state after frame N+1 depends on the number of cursor draws made while frame N was drawn. A frame oracle that excludes rendering is only exact while no consumer of the cursor is reached. Otherwise the cursor consumption of `AffGame` must be part of the oracle, or be supplied as declared per-frame input by Graphics.
2. **The single-player world depends on the viewport.** With the network byte clear, vegetation and terrain animation run only over the viewport rectangle: origin `0x508720`/`0x508722`, size `0x508724`/`0x508726`, in cells. **In the frozen M1 post-load state that size is 0×0**, because the display initialization was skipped at startup. Both routines then visit no cell, and `SetClipping` would receive `0xffff`. The frame oracle must declare where the viewport size comes from; Missions/ai-runtime decide that.
3. **The CD-audio setting changes the cursor.** When `0x4e2f28` is 0, CalculGame consumes one cursor byte for `MCICD_Play(eax = 2 + perm%2, edx=0)` before the input loop of each frame (`0x42d2f0..0x42d328`). In the M1 state `0x4e2f28`=0.
4. **The frame counters are reset at load.** The load case stores zeros into `0x508f7c`/`0x508f80`/`0x508f84` after MissionLoad, so the M1 counter values are not the frame-1 inputs.
5. **Field growth starts on frame 1.** The M1 period `0x4973ea` is 128, and a counter of 0 gives remainder 0. So `SetUpdateChamp` sets the flag on the first frame and `UpdateChamp` processes row 1 with the world RNG. MONDE01 holds 124 objects in `0x1c..0x34` (none equals 0x34).
6. **`GameNextFrame`'s counter is write-only** in the static code, and `PlayerAttaqueReset` is empty.

## Core implementation scope for M2 (Step 2)

Core translates only what it owns and nobody has already implemented. That covers `GameNextFrame`, the world RNG seed family (`Randomize`/`SetRandomSeed`/`GetRandomSeed`, plus `Random` through the existing arithmetic), the three paths of `iaRandom`, the CRT `rand`/`LongRand` over the live thread block, the permutation-cursor read, the `ProgIteration` counter prefix and the load counter reset, over live buffers. `SetUpdateChamp`/`UpdateChamp` remain with Economy and `NextAnim*` with Graphics. The original captures for Step 2 start from the frozen M1 post-load state (Missions `captura-carga-missao-original-v2.json`, final blocks). They are labeled "M1 post-load input, not yet frame-1 input".

## Step 2 delivery: live-buffer API and original-first validation

**Order.** The static inventory came first (`a5830f6`). The original-only capture followed (`9a80499`, before any translation), then the implementation and its validation (`06ed6d9`).

**Input.** All captures and differentials start from Missions' frozen capture v2 (`captura-carga-missao-original-v2.json`, SHA-256 `eb7d2303…3afc`, final-state SHA `58a5020e…1114`). They use its final `dgroup` and `crt_thread_data` blocks at the real return `0x42d22d`. **This is M1 post-load input, not yet frame-1 input.** The load case zeroes the counters and may run one frame body before frame 1's own inputs exist. `estado_m1_quadro.carregar_m1()` checks every hash, and the evidence is never edited. GlobalAlloc blocks are left unmapped, so any access would fault; none occurred. Cases named `derived_*` list their byte overrides explicitly.

### API (`ferramentas/fundacoes_quadro.py`)

Each buffer must be the live original global: a `bytearray` or a writable, one-dimensional, contiguous byte `memoryview` into DGROUP or the thread block. Shape and type checks run before the first store. Each function returns the EAX that callers consume. The other GPRs are preserved by the original. The return flags are not reproduced, because no caller reads them before overwriting them: all 74 `Random`, 14 `iaRandom` and 2 `LongRand` call sites were checked.

| Function | Original | Live inputs | Effect / return |
|---|---|---|---|
| `avancar_quadro_jogo(contador)` | `GameNextFrame 0x45d015` | 4 bytes @`0x496d40` | u32+1 (wraps); no register output |
| `aleatorio_mundo(semente)` | `Random 0x4704dc` | 4 @`0x497164` | stores and returns the new state (`candidatos_rota.aleatorio_caminhos`) |
| `randomizar_mundo(semente, eax)` | `Randomize 0x470520` | 4 @`0x497164` | stores and returns EAX+1 |
| `definir_semente_mundo(semente, eax)` | `SetRandomSeed 0x470527` | 4 @`0x497164` | 0 → stores 1 and returns 0; otherwise stores EAX mod 0x7fffffff and returns the quotient |
| `obter_semente_mundo(semente)` | `GetRandomSeed 0x47054c` | 4 (read-only allowed) | returns the u32 |
| `aleatorio_ia(semente, limite, relogio=None)` | `iaRandom 0x489728` | 4 @`0x498db4`; `relogio()` → declared u32 `timeGetTime` | limit>0: advances the state and returns state mod limit; limit<0: stores (−limit) srem 0x7fffffff and returns 0; limit=0: stores clock mod 0x7fffffff and returns 0. A missing clock raises `DependenciaRelogioIA` at `0x489789` and stores nothing |
| `aleatorio_crt(dados_thread)` | `LongRand 0x45841b` → `rand 0x48c51d` | the thread block (`[0x522244]`, ≥16 bytes) | seed@+0xc ← seed·0x41c64e6d+0x3039; returns (seed>>16)&0x7fff |
| `consumir_permutacao(tabela, cursor)` | the inline draw (CalculGame `0x42d2f9`, NextAnim*, Aff*) | 256 @`0x4e1c18` (read-only), 1 @`0x4e1d18` | returns `tabela[cursor]`; cursor ← cursor+1 (u8) |
| `avancar_contadores_iteracao(contadores)` | `ProgIteration 0x475014..0x475041` | 12 @`0x508f7c` | ordered stores +0 always, +4 if the cycle is even, +8 if it is divisible by 3; returns the offsets stored |
| `zerar_contadores_carga(contadores)` | CalculGame `0x42d2be..0x42d2ca` | 12 @`0x508f7c` | zeros at +0, +4, +8 in that order |

The MenuInit arguments prepared around the load reset (EAX=player byte, EBX=0, ECX=1, EDX=0x12) are not part of this primitive; ai-runtime composes them, and the differential asserts them as observations. For the CD draw, the composer passes `2 + byte % 2` to `MCICD_Play`; the differential asserts EAX, EDX=0, ECX=2 and BL=the new cursor.

### Validation (actual results)

- **Capture** `evidencias/fundacoes-quadro/captura-original.json` (SHA-256 `a3746663…b638`): 62 cases / 195 steps / 202 bounded segments. The code-section hash is unchanged, and the only binding is WINMM.timeGetTime through IAT `0x5234a4`, answered with explicit per-case clock values. No translation ran.
- **CPU-free replay** `testes/test_fundacoes_quadro.py`: all 195 steps match the whole DGROUP+thread byte difference, the ordered non-stack writes, the consumed EAX and the preserved registers. Each case's final SHA matches as well. Input-protection tests cover the clock dependency, malformed and read-only buffers, memoryviews and the agreement with `cadencia.proximo_aleatorio` on its domain.
- **Fresh intact differential** `python3 -B ferramentas/validar_fundacoes_quadro.py --emular`, run under the heavy lease: 11 tests, 659 Python/native comparisons and 677 bounded segments, including 18 declared clock continuations. The maximum is 30 instructions per segment. There were zero failures, errors, skips, native faults, limits or patches, and the code section was unchanged ([report](../../relatorios/fundacoes-quadro-emulada.json)). Local mode runs 11 tests (8 executed, 3 optional x86 skips).

### Gaps and dependency stops

- The frame-1 re-validation is done at the exact frame inputs: see [Frame 0/frame 1](#frame-0frame-1-re-validation-and-the-reached-core-callees-m21) below.
- `iaRandom(0)` needs a declared clock value from the frame oracle. Core supplies no default.
- Not translated by Core: `InitRand` (startup producer of the table), CRT `srand`, and the owners' routines (`SetUpdateChamp`/`UpdateChamp`: Economy; `NextAnim*`: Graphics; `CalculNextReflect`/`PlayerAttaqueReset`: ai-runtime; `SetClipping`: Graphics; `InitGameZone`: UI).
- The viewport size (0×0 in M1) and the rendering-side cursor consumption are frame-oracle inputs that Core cannot decide.

## Frame 0/frame 1: re-validation and the reached Core callees (M2.1)

**Inputs.** Missions' first-frame original capture (`pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json`, SHA-256 `c06f78ea…fed8`) and its entry trace (`rastro-quadro1-monde01.json`, `45859330…3fb0e`). "Frame 0" is the load-state CalculGame body (`load_tail`). Frame 1 is the second pass. Every number below is at these exact frame inputs. None is at the M1 post-load input.

**Order.** The original-only isolated capture came first, committed before any translation (`2e5cc6d`). The translation and its fresh native differential followed.

### Foundations re-validated at the frame inputs

These are checked against the phase snapshots and boundary events in `testes/test_chamadas_quadro_core.py::ReValidacaoFundacoesQuadro1`, with no CPU:

| Primitive | Frame 0 (`load_tail`) | Between frames | Frame 1 |
|---|---|---|---|
| Load counter reset | `zerar_contadores_carga` on S0 (0,0,0) equals the after-(a) bytes | — | — |
| `ProgIteration` prefix | — | `avancar_contadores_iteracao` stores only +0 (cycle 1). It is the only DGROUP change in (b) | counters unchanged |
| `GameNextFrame` | 1 entry, counter 1→2 | — | 1 entry, 2→3 |
| `Random` | 8 entries (one per state-7 unit), `0x4926732e`→`0x1c019f87` | — | 8 entries, →`0x78fe3b37` |
| `iaRandom` | not entered, `0x498db4` unchanged | — | not entered, unchanged |
| Permutation draw | two draws: MenuInit+0x202, then the CalculGame CD branch `0x42d2f9`. The MCICD_Play boundary sees EAX=2+byte%2, EDX=0 and BL=the new cursor (0→1→2) | — | one draw (CD branch), byte `0x81`, EAX=3, cursor 2→3 |
| Viewport size `0x508724/26` | 0×0 | 0×0 | 0×0, so NextAnimTerrain/NextAnimVeget visit no cell. Only the origin changes, through the edge scroll |

The per-frame cursor step is therefore Core's CD-branch draw (`[0x4e2f28]`=0), not NextAnim*. `CalculGame_cd_permutation_draw` is reached in both frames. `LongRand`, `iaRandom` and the counter-reset path in frame 1 are not reached.

**Owners' routines in the trace.** `SetUpdateChamp`/`UpdateChamp` belong to Economy, `NextAnimTerrain`/`NextAnimVeget` to Graphics and `CalculNextReflect` to ai-runtime. `SetClipping` (Graphics) and `InitGameZone` (UI) are entered in frame 0 only. Core has no implementation of these to re-validate. Its share is the inline primitives above.

### Reached Core callees

Ownership was confirmed from the bytes. Callers in the trace:
- ai-runtime: `EnginNextEtape` and `CalculBatimentNextEtape`.
- Economy: `CalculMatiere`, which calls GetBit/SetBit.

The callees are the generic bit helpers, the per-owner discovery/light grids, the structure pool geometry, the unit collision/region tags and unit fatigue.

Not Core:
- `BonusGetValEngin` 0x428cc0 (Economy) is a provider argument.
- `BatimentExiste` belongs to Missions and `BatimentGetPlayer` has a Combat bridge.
- `BatimentGetType` and `EnginTrouveCible`/`PlayerEstAllie` (frame 0, Combat) are not claimed here.
- `CaseGetZoneInfluence`/`GetTopLeftCaseZoneInfluence` are not reached in frame 0/1.

**Native capture** (`evidencias/fundacoes-quadro/captura-chamadas-quadro1.json`, `ferramentas/capturar_chamadas_core_quadro1.py`). The run reuses `oraculo_quadro_missao.Isolamento` over the committed path. It made 678 isolated calls, 339 per frame:

| Routine | Calls per frame |
|---|---|
| GetBit | 80 |
| CaseEstDecouverte | 93 |
| CaseEstIlluminee | 78 |
| BatimentCollision | 30 |
| CalculFatigue | 16 |
| SetEnginCollision / SetCollision / Chemin_ModifieZone / Random | 8 each |
| BatimentEstDecouvert / BatimentContourEstIllumine | 3 each |
| SetBit | 2 |
| BatimentGetCase / GameNextFrame | 1 each |

The path reproduction passed: phase states, boundaries, entry trace and code section. Read and write hooks are added and the Unicorn translation cache is flushed before every isolated call, so no cached block can under-count reads. The earlier `BancadaFundacoesQuadro` adds its hooks before its first translation, so it needs no flush.

**Static evidence** (`evidencias/fundacoes-quadro/chamadas-quadro1/manifesto.json`, `ferramentas/extrair_chamadas_quadro1.py`). It covers 16 hash-checked intervals (routines, shared tails and epilogues), the four jump tables, the four initialized data tables the translations index, and `caller_flag_use`. All 20 captured call sites overwrite the arithmetic flags before reading any.

### API (`ferramentas/chamadas_quadro_core.py`, memory `ferramentas/memoria_quadro_core.py`)

`memoria` is any object with `u8/u16/u32(endereco, valor=None)` over the live original buffers. `MemoriaQuadro(segmentos)` wraps the caller's own writable buffers. Ai-runtime's `MemoriaDeclarada` has the same interface. An address outside every segment raises `AcessoForaDosSegmentos`. Each function returns a dict of the general registers the routine changes. Unlisted registers are preserved.

`provedores_core(memoria, bonus)` adapts the functions to ai-runtime's `provider(sitio=..., **keywords) -> EAX` convention: `caso`, `jogador`, `estrutura`, `unidade`, `valor`/`bit`.

| Function | Original | Domain translated | Registers out |
|---|---|---|---|
| `obter_bit(eax, edx)` | GetBit 0x467d97 | complete | EAX=((AL) sar (DL&31))&1 |
| `definir_bit(m, eax, edx, ebx)` | SetBit 0x467d71 | complete: BL=0 clears, BL=1 sets, BL>1 returns; 8-bit shift (index ≥8 → mask 0) | clear: EBX low=new byte, EDX low=~mask; set: EDX low=mask |
| `caso_esta_descoberta(m, eax, edx)` | CaseEstDecouverte 0x4766d6 | complete; owner byte indexes `0x507d78+4·DL` (owner ≥4 aliases the next tables) | EAX=(AX&0xff00)\|((grid&0x10)==0), EDX=grid pointer |
| `caso_esta_iluminada(m, eax, edx)` | CaseEstIlluminee 0x47693a | complete, table `0x507d88` | same |
| `colisao_estrutura(m, eax, edx)` | BatimentCollision 0x41ab5c | complete; type>0x15 → AL 0 | EAX=(DX&0xff00)\|mask byte, EDX=type; above 0x15 EAX=EDX&~0xff |
| `caso_estrutura(m, eax)` | BatimentGetCase 0x41aee2 | complete, including empty masks and the high word of index·276 in the origin dword | EAX only |
| `estrutura_esta_descoberta(m, eax, edx)` | BatimentEstDecouvert 0x419c4f | complete (rectangle, rows then columns, map clipping) | 1: EAX/EDX = call's \| 1; 0: both = height&0xff00 |
| `contorno_estrutura_iluminado(m, eax, edx)` | BatimentContourEstIllumine 0x4199f9 | complete (ring dy∈[−1,H], dx∈[−1,W]) | 1: EAX low=1, EDX=grid pointer; 0: EAX=(H+1)&~0xff, EDX=H+1 |
| `definir_colisao(m, eax, edx)` | SetCollision 0x47622e | complete | EAX=attribute grid pointer |
| `modificar_zona_caminho(m, eax, edx, ebx, ecx, sub)` | Chemin_ModifieZone 0x43e138 | mode 2 (unit tag insert or occupied) | EAX low=0/1, EBX=tag, EDX=2·cell |
| `definir_colisao_unidade(m, eax, edx)` | SetEnginCollision 0x442cb4 | complete over its type table (single, quad, type-16/17 mask-2, type>0x19) | last Chemin EAX/EDX, or attribute pointer and EDX=2 |
| `calcular_fadiga(m, eax, bonus)` | CalculFatigue 0x452cc8 | +0x72=0, types 11..17, counter below the threshold | EAX |
| `aleatorio_mundo_memoria(m)`, `avancar_quadro_jogo_memoria(m)` | Random, GameNextFrame | as `fundacoes_quadro`, over memory | EAX / none |

Reached at the frame inputs:
- CalculFatigue takes the inactive return and the counter increment (threshold 3000+`+0xf8`+bonus).
- SetEnginCollision takes the single-cell path for unit types {0,1,5,7,8}, with a re-asserted mask and an occupied region (Chemin AL=0).
- The structure visibility queries all return 0.
- The fresh differential's perturbations cover the remaining outcomes.

### Validation (actual results)

- **CPU-free replay** (`testes/test_chamadas_quadro_core.py`, 15 tests). All 678 calls replay from exactly the bytes the original read before writing. Any other read raises, so a translation that reads more than the original fails. Stores and all seven general registers match. CalculFatigue's Economy bonus query gives the same result for table fills 0x00/0x5a/0xa7/0xff outside the footprint. The static manifest regenerates from the intact bytes, and the translation tables equal the jump tables.
- **Fresh native differential** (`python3 -B ferramentas/validar_chamadas_quadro_core.py`, under the heavy lease, 48 s). It made **1,918 Python/native comparisons** at the exact entry states: the 678 captured calls plus declared perturbations on the first 4 calls of each routine per frame. The perturbations cover:
  - registers;
  - unit and structure types and origins;
  - grid owners 0–7;
  - a discovered footprint cell;
  - free region cells (Chemin insert);
  - counter wrap;
  - owner bonus;
  - seed edge values.

  Results:
  - **0 mismatches and 0 dependency stops.**
  - The path reproduction still passed.
  - Positive AL exits were reached for the four visibility queries and for Chemin (insert).
  - 48 SetEnginCollision cases stored.

  `RISING_EMULAR=1` reruns it as `testes/test_emulacao_chamadas_quadro_core.py`. Report: [chamadas-quadro1-emulada.json](../../relatorios/chamadas-quadro1-emulada.json).
- **Failed attempts** are preserved in `.local/frame/`. Three were perturbation-domain or validator bugs, none a translation divergence:
  1. A wrong unit-pool base gave an unmapped native write.
  2. A light-grid owner 11 read pointer slot 15, which is 0, giving a native fault.
  3. Owner 10's light slot points to a smaller block. The Python memory refused a read the native made outside every live allocation.

  Owners are now limited to 0–7.

### Dependency stops and gaps

Each raises `DependenciaRamoCore` before any store:
- **CalculFatigue**:
  - The threshold-reached branch at `0x452d61` (provisions decrement, `BagContient`/`BagRetire`, `SetDyingEngin`, the local-player sound) is not reached in frame 0/1.
  - A missing Economy bonus provider stops at `0x452d48`.
- **Chemin_ModifieZone** modes:
  - 0 (`0x43e153`, unit tag removal);
  - 1 (`0x43e1b4`, MurRetire);
  - 3 (`0x43e256`, MurAjoute);
  - BL>3 (`0x43e29c`).

Not translated: GetBit's callers' bodies (ai-runtime/Economy) and the AffGame cursor consumption (Graphics).

## Frame 0/frame 1, round 3: clipping, mouse zones, NextAnim* and the live task memory

The coordinator assigned `SetClipping`, `InitGameZone` and `NextAnim*` to Core for the frame-0/frame-1 domain, which supersedes the ownership classification of the first inventory. The ai-runtime composition stopped before them at RestoreAll/InputGame.

**Capture first** (`58a0440`): `ferramentas/capturar_zonas_animacao_quadro1.py` writes `evidencias/fundacoes-quadro/captura-zonas-animacao-quadro1.json` (SHA-256 `277496ff…1adc`). It runs on the shared runner `percurso_quadro1.py`, which is Missions' committed path plus `Isolamento`, with an optional native basic-block recorder added after start-up and followed by a translation-cache flush.
- **Calls:** 61 isolated calls at the exact frame inputs, each with its executed native blocks. The path reproduction passed.
- **Not reached:** MarcheGetPos/MarcheGetTaille and NextAnimVegetFullMap (network only).

| Call | Frame 0 (`load_tail`) | Frame 1 |
|---|---|---|
| SetClipping | 1 (CalculGame+0xa43; EBX=ECX=0xffff because the viewport is 0×0) | — |
| InitGameZone(1, 0) | 2: MenuInit+0x1ce (stores 76 bytes), CalculGame+0xa76 (stores nothing new). Nested: MouseSetZone ×17 each, MiniMapGetPos/Taille, ChercheContacteur ×3, MessageBoxExiste, PlayerEstContacterPourAlliance ×3, MouseTestZone | — |
| NextAnimTerrain / NextAnimVeget | 1 each, at the viewport origin | 1 each |

Branches reached by InitGameZone in both calls:
- mode 1 (jump table `0x471820` → `0x471aa4`);
- the screen width u16 `0x49a018` is 0, so not 640 (`0x471d74`);
- the minimap rectangle is used (`0x497285`=1);
- the contact type is not 1/2/3 (ChercheContacteur → 0xff), giving the default zone 0x1a;
- no message box;
- no alliance.

NextAnimTerrain and NextAnimVeget exit at their first row test, because the viewport height is 0.

**API** (`chamadas_quadro_core.py`; `provedores_core` keywords follow ai-runtime's composition):

| Function | Original | Domain | Registers out |
|---|---|---|---|
| `definir_recorte(m, eax, edx, ebx, ecx)` | SetClipping 0x40f519 | complete: u16 `0x49a020`=AX, `0x49a022`=BX, `0x49a01c`=DX, `0x49a01e`=CX in that order | none |
| `definir_zona_mouse(m, eax, edx, ebx, ecx, y1)` | MouseSetZone 0x479c50 (RET 4) | complete: four zero-extended u16 dwords at `0x5099b4+16·AX`, then u16 max `0x50a9b8`. Index 256 aliases `0x50a9b4..` and is validated | EAX=AX<<4, EDX=y1 |
| `testar_zona_mouse(m, eax, edx)` | MouseTestZone 0x479c9e | complete | none |
| `posicao_minimapa`, `tamanho_minimapa`, `posicao_mercado`, `tamanho_mercado` | MiniMapGetPos/Taille, MarcheGetPos/Taille | complete: u16 [EAX], [EDX] | EAX low word = second value |
| `procurar_contato(m, eax)` | ChercheContacteur 0x465818 | complete | EAX |
| `caixa_mensagem_existe(m, eax)` | MessageBoxExiste 0x469c33 | complete | EAX=(EAX&0xffff0000)\|(AX'&0xff00)\|flag |
| `contatado_para_alianca(m, eax, edx)` | PlayerEstContacterPourAlliance 0x46da1e | complete | EAX=flag |
| `iniciar_zonas_jogo(m, eax, edx)` | InitGameZone 0x471830 | mode 1 complete (see below) | EAX=1, EDX=0x1f, EBX=(H<<5)&0xffff, ECX=screen width |
| `animar_terreno(m, eax, edx)` | NextAnimTerrain 0x477700 | zero viewport rows | EAX=EDX=0 |
| `animar_vegetacao(m, eax, edx)` | NextAnimVeget 0x4772ec | zero viewport rows | EDX=EDX<<8 |

Mode 1 covers:
- zones 1–9 from the screen size;
- the minimap or default zone 0xa;
- contact zone 0x1a: panel corner (screen 640 or panel offset s8 `0x508f90`), market rectangle, or default;
- message-box zone 0x1b;
- alliance zones 0x1c–0x1f;
- zone 0xb;
- MouseTestZone(1, 0x1f).

Every coordinate is 16-bit. `0x508f90` and the viewport width are read only on the branches that use them.

**Stops.** Each raises `DependenciaRamoCore` before any store:
- InitGameZone modes 2/3/4/other: `0x4719be`/`0x47194f`/`0x47184d`/`0x471949`;
- NextAnimTerrain with viewport rows: `0x477737`;
- NextAnimVeget with viewport rows: `0x47731b`;
- NextAnimVegetFullMap: `0x4774fa`.

The per-cell animation loops, and their cursor and `LongRand` draws, are not translated. They need a non-empty viewport, which the oracle does not reach.

**Validation.**
- **CPU-free replay:** all 61 calls replay from the bytes the original read. MouseSetZone's pushed word is recovered from its EDX; the native run reads the stack. Every captured change is reproduced, and no known byte changes otherwise. Stores to bytes the original never read, with unchanged values, are compared by the native run.
- **Fresh native differential** over both captures in one run (739 isolated calls), with perturbations at the exact entries:
  - **InitGameZone:** screen 640×480; minimap off; contact types 1, 2 and 3 (market); contact self; message box with a negative panel offset; alliances; local player 2.
  - **MouseSetZone:** index 256 and high bits.
  - **Queries and SetClipping/NextAnim\*:** high bits and table values.

  **2,034 comparisons, 0 mismatches, 0 dependency stops**, path reproduction passed. InitGameZone stored new zone records in 19 cases.

### Task VM over live memory (`tarefas_ia.MaquinaTarefasViva`)

`MaquinaTarefasViva(programa, memoria)` binds the unchanged `MaquinaTarefas` VM to the caller's own buffer of `0x512320..0x514908`, so iaSolver runs over live memory without a load/store bridge. `sobre_memoria` does the same through a flat memory's segments. The buffer holds:
- the 100×0x60 records;
- the free-list header `0x5148a0`;
- the five context headers `0x5148b0+16k` (s32 head, u32 count; listInit's +8 stride and +12 base are left untouched);
- the u32 active count `0x514904`.

Every method is inherited and nothing is initialized. Count stores wrap to u32, as the bridge's store does.

`testes/test_tarefas_ia_viva.py` checks equality with the bridge:
- `atualizar(0..4)` at S0 and after each Missions frame phase (all contexts are empty there; return `0x1a1a000e`);
- `postar(4, t)` followed by `atualizar(4)` for all 42 rule entries, which covers completion, sleep, subtasks and named world-operation stops with partial effects retained;
- writes landing in the caller's buffer.

## Round 4: the display scenario is the M2 reference

Missions' display-executing scenario (`pesquisas-paralelas/missoes/QUADRO1_EXIBICAO.md`) is now the reference. DDInit gives a 25×17 viewport and an 800×600 screen. NextAnimTerrain therefore calls LongRand→CRT `rand` 425 times per frame, and NextAnimVeget walks real cells. This **supersedes** the round-3 "zero viewport rows" domain and its NextAnim* stops.

**Capture first** (`80fd5ef`). `ferramentas/capturar_exibicao_quadro1.py` writes `evidencias/fundacoes-quadro/captura-exibicao-quadro1.json`. It uses `percurso_quadro1.executar(cenario='exibicao', limites=...)`, with isolation limited per phase for the 425-per-frame rand calls. It holds 70 isolated calls at the exact display frame-0/1 inputs, each with its native blocks:
- SetClipping;
- InitGameZone ×2 with its helpers (PlayerEstContacterPourAlliance is also entered from AffGame between frames);
- NextAnimTerrain and NextAnimVeget whole in both frames;
- GameNextFrame;
- the first Random, LongRand and rand calls of each phase.

The path reproduction passed.

What the records show:
- NextAnimTerrain changes only the CRT seed `0x340000c` (425 draws, no drop), and returns EAX=0x11 (rows) and EDX=0xe7.
- In frame 0 (counter 0), NextAnimVeget advances the cursor `0x4e1d18` 2→4 through two tree draws. In frame 1 (counter 1) it stores nothing.

**API changes** (`0b8f1ea`):

| Function | Original | Domain | Registers out |
|---|---|---|---|
| `aleatorio_crt_memoria(m)` | CRT rand 0x48c51d / LongRand 0x45841b | complete. The getter `[0x4990cc]` must be `0x48e7c7`, otherwise it raises at `0x48c513`. A zero seed pointer returns 0 | EAX=(seed'>>16)&0x7fff; EDX kept |
| `animar_terreno(m, eax, edx, edi=None)` | NextAnimTerrain 0x477700 | complete viewport walk (all tile classes, cursor and LongRand draws, object drop) | EAX=rows; EDX exact, or None when a zero-width viewport needs the caller's EDI |
| `animar_vegetacao(m, eax, edx, ecx=None)` | NextAnimVeget 0x4772ec | complete viewport walk (all object classes) | EAX/EDX exact (EAX is None only if ECX's high word is needed and not given); ECX kept |

The providers `NextAnimTerrain(x, y)` and `NextAnimVeget(x, y)` are unchanged; both are void. Per cell, the grid pointers `[0x507d70/74/ac]` and the cycle counter are read only on the branches the original reads them.

**Validation.**
- **CPU-free replay:** all 70 display-scenario calls replay exactly, stores and seven GPRs. `rand` agrees with `fundacoes_quadro.aleatorio_crt` at every captured draw.
- **Fresh native differential** in the display scenario (`validar_chamadas_quadro_core.py --cenario exibicao`, 165 s under the lease): **194 comparisons, 0 mismatches, 0 stops**, and the path reproduction passed ([report](../../relatorios/chamadas-exibicao-quadro1-emulada.json)). The perturbations, all built from the live bench:
  - **Tiles:** the tile classes 0x5d/0x94/0x95/0x9c/0x251/0x252/0x255/0x256, with even and odd counters.
  - **Object drop:** a forced drop on 0x8b and 0x6d, using seed 0x72d.
  - **Degenerate viewports:** zero width with a high EDI or high ECX; zero rows.
  - **Object classes:** 1/0x17/0x1b/0x37/0x38/0x3a/0x3e/0xb, with counters 0, 2 and 1.
  - **rand seeds:** seed edge values and a zero seed pointer.
  - **Shared routines:** the v1 cases for InitGameZone and the other shared routines.

  The v1 rerun is unchanged: 2,034 comparisons, 0 mismatches.
- The remaining stops are InitGameZone modes 2–4 and NextAnimVegetFullMap (network only, not reached).

The task VM's live binding (round 3), the CRT I/O boundaries ([DECLARED_BINDINGS](DECLARED_BINDINGS.md)) and the [live tile grid](LIVE_TILE_GRID.md) complete this round.

## Round 5: frames up to cycle counter 128, unreachable modes, display-path queries

**Reference.** Missions' Stage18 display reference over Graphics' backend (`captura-quadro1-monde01-exibicao-v2.json`). `percurso_quadro1` resolves `'exibicao'` to it, and every new run reproduces frames 0/1 against it.

**Survey first** (`f426e30`, `levantar_quadros_exibicao.py`, `evidencias/fundacoes-quadro/levantamento-quadros-exibicao.json`). The original program kept running with the same declared no-input answers up to cycle counter 128: 128 frames in 197 s. It records per-frame routine entries, boundaries, RNGs, CRT seed, cursor, view origin and state hash. Findings:
- **Only two routines are first entered after frame 1:**
  - Combat's EnginTrouveCibleScan, from frame 17, inside the periodic EnginTrouveCible target scan (frames 17, 21, 30–32, …);
  - Economy's ScanNouvellePatate, from frame 45.
- **No raid by counter 128.** No attack, projectile creation or damage routine is entered, so the first raid lies beyond counter 128. It was not surveyed further.
- **Core routines reached by the frame logic in frames 2–128** are exactly the frame-0/1 set: NextAnim*, GameNextFrame, Random, LongRand/rand, GetBit/SetBit, CalculFatigue (still below its threshold), Set*Collision/Chemin, and the structure and cell queries. All of them are translated.
- **Core queries reached by the display path (AffGame, between frames):** TerrainEstDecouvert, TerrainEstIllumine, ExisteEngin, EnginGetType, EnginGetPlayer, EnginEstArmure/Miroir/Terreur and TypeEnginSeFatigue, alongside the already-translated cell queries and GetBit.

**Capture before translation** (`ca5a7f3`, `capturar_quadros_seguintes.py`, `evidencias/fundacoes-quadro/captura-quadros-seguintes.json`). The run took 2,410 s and covered frames 0–128. It is stored with a lossless run encoding (`compactar_captura_isolada.py`; the 79.7 MB raw file, SHA-256 `07bec0cc…`, is kept under `.local/frame`).
- **NextAnimTerrain/NextAnimVeget:** every frame is isolated. Kept are frame 0, the sampled frames 1, 2, 3, 4, 17, 45, 64, 127, 128, and the 20 frames in which vegetation changed objects. No NextAnimTerrain call changed more than the CRT seed up to counter 128.
- **InitGameZone** in frame 0, with mode perturbations:
  - 2: MissionGetNum < 7 and ≥ 7;
  - 3: the original item count, 5 items, and 0 items with high EBX/ECX;
  - 4;
  - the invalid modes 0 and 5.
- **NextAnimVegetFullMap** as a *foreign entry*. It is network-only: CalculGame calls it at `0x42d44f` only when `[0x4e0730]` is set. It runs natively from NextAnimVeget's exact paused state, which is the same state, since both follow NextAnimTerrain. It ran in frames 1, 2, 64 and 128, with counter cases 0, 2 and 1.
- **In the sampled frames:** the display-path queries, GameNextFrame, Random, LongRand and rand, and all MissionGetNum calls.

Static reach of InitGameZone's modes:
- Game-time callers pass mode 1: CalculGame, alliance counters, the market, message boxes and input.
- Modes 2–4 come from MenuInit's menu states (for example `MenuInit+0x7e0` passes 4), ResetMode, WndProc and GameLoad.
- None is reached without input up to counter 128.

**Translations** (`chamadas_quadro_core.py`):
- **InitGameZone:**
  - mode 2: zones 1–8, with zone 4 only from mission 7 on;
  - mode 3: one zone per menu item, 0x19 apart from y=0x11e, then MouseTestZone(1, n). It needs the caller's EBX/ECX for 0 items, and 256 or more items raise at `0x4719ba`;
  - mode 4: fixed zones 1–8;
  - invalid modes store nothing and return EAX−1.
- **NextAnimVegetFullMap** shares NextAnimVeget's per-cell body over all 65,536 cells. It returns EAX=0x100 and keeps every other register.
- **Display-path queries:** `terreno_esta_descoberto`, `terreno_esta_iluminado`, `unidade_existe`, `tipo_da_unidade`, `dono_da_unidade`, `unidade_terror`/`unidade_espelho`/`unidade_armadura`, `tipo_cansa`.
- **InitGameZone helpers:** `numero_missao` and `itens_menu`, the MissionGetNum/MenuGetNbItem getters it uses.
- All of these are also available through `provedores_core`.

**Validation.**
- **CPU-free replay** of every kept case of the frames 0–128 capture is exact: stores and seven GPRs. That includes 16 FullMap foreign-entry cases, 18 InitGameZone mode cases, the later-frame NextAnim* records, the queries and 1,290 MissionGetNum calls.
- **Fresh native differential**, display reference (`validar_chamadas_quadro_core.py --cenario exibicao`, under the lease): 124 isolated calls (FullMap as a foreign entry at both NextAnimVeget pauses) and **484 comparisons, 0 mismatches, 0 dependency stops**. The path reproduction passed against v2. The perturbations cover:
  - the InitGameZone modes;
  - FullMap object classes with counters 0, 2 and 1;
  - grid owners 0, 4 and 7 and high cell bits for the terrain queries;
  - units 799, high index and overwritten bytes;
  - unit flag bytes 0x0e/0x02/0x04/0x08/0xf1;
  - every TypeEnginSeFatigue class and high bits;
  - MissionGetNum.
- **v1 rerun:** 2,048 comparisons (now with the InitGameZone modes), 0 mismatches.

**Remaining stops:**
- CalculFatigue's threshold branch (`0x452d61`), still unreached at counter 128;
- Chemin_ModifieZone modes 0/1/3;
- InitGameZone mode 3 with 256 or more items (`0x4719ba`).
