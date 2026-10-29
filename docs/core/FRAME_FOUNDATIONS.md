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

- The frame-1 re-validation waits for Missions' frame-1 capture and entry trace. It must be rerun at the exact frame-1 inputs and extended only to the branches the trace reaches.
- `iaRandom(0)` needs a declared clock value from the frame oracle. Core supplies no default.
- Not translated by Core: `InitRand` (startup producer of the table), CRT `srand`, and the owners' routines (`SetUpdateChamp`/`UpdateChamp`: Economy; `NextAnim*`: Graphics; `CalculNextReflect`/`PlayerAttaqueReset`: ai-runtime; `SetClipping`: Graphics; `InitGameZone`: UI).
- The viewport size (0×0 in M1) and the rendering-side cursor consumption are frame-oracle inputs that Core cannot decide.
