# M2.1 round 4 — chained composition of MONDE01 frames 0/1 on the display reference

Main `81e0a26`. Intact `RISING.EXE` `6c556520…43fb`. Reference: Missions' display scenario (`QUADRO1_EXIBICAO.md`):
- entry `entrada-carga-missao-exibicao.json`;
- MissionLoad `captura-carga-missao-exibicao.json`, whose final state the Stage14 regression showed equal to Python's composition;
- frames `captura-quadro1-monde01-exibicao.json`.

Reports, each from a clean tree and a fresh native collection:
- [validacao/m2-quadro1-exibicao-ia.json](validacao/m2-quadro1-exibicao-ia.json): display, the reference;
- [validacao/m2-quadro1-v1-r4-ia.json](validacao/m2-quadro1-v1-r4-ia.json): v1 regression with the same code.

Missions' display-only exclusion mask was not yet published, so **every byte is compared** and the bytes written by crossings are classified below. M2 acceptance is the coordinator's decision.

## Result: all three phases equal, chained from Python

| Phase (display) | Python input | Result |
|---|---|---|
| (a) `load_tail` | one map built from the display MissionLoad final state (25,343 blocks) | **equal**: all blocks (146 bank allocations released, as in the original), RNGs, 616/616 bindings (DirectDraw COM, GlobalFree/Handle/Unlock, ShowCursor, 12 GetAsyncKeyState), 5/5 boundaries |
| (b) `between_frames` | Python's (a) output | **equal**: all blocks, RNGs, 10/10 bindings (AffGame's tick/COM/palette calls, PeekMessageA, GetCursorPos), 2/2 boundaries, and the 8 modeled registers |
| (c) `frame1` | Python's (b) output | **equal**: all blocks, RNG `0x497164` = `0x78fe3b37`, 13/13 bindings, 1/1 boundary |

All 96 checkpoints are equal. They sit at every MenuInit, input, AI, dispatcher (32 EnginNextEtape), Economy, Combat, Missions and Core call.

**Not modeled.** The four stack words of MCICD_Play in the CalculGame frame bodies, which are uninitialized locals. EFLAGS/EIP. The real ProgIteration frame words: saved EDX/ECX/EBX = 0, as the boundary registers show, and the MSG buffer holding the bench loop sentinel `0x3000000`, which is declared from the bench.

**v1 regression (same code):** all three phases are equal. Only RestoreAll is crossed. Core's SetClipping, InitGameZone and NextAnim* run as providers with no stop, because v1 has a 0×0 viewport.

## First stops, owners and addresses

| Phase | Routine | Owner | Stop | Handling |
|---|---|---|---|---|
| (a) | NextAnimTerrain | **Core** | `DependenciaRamoCore` at `0x477737` ("viewport with rows: cell loop not translated"). The 25×17 viewport needs 425 LongRand/rand calls | crossed: the state matched at entry |
| (a) | NextAnimVeget | **Core** | `0x47731b` (same domain) | crossed |
| (c) | NextAnimTerrain, NextAnimVeget | **Core** | `0x477737`, `0x47731b` | crossed |

No divergence was found. The first non-crossed stop on the display reference is **Core's NextAnimTerrain at `0x477737` in frame 0**.

## RestoreAll, AffGame and the other display routines: which written bytes are logic state

Crossings applied (Graphics owns these display routines; each crossing happened only after an exact entry-state match):

| Phase | Crossed call (CALL site) | Bytes written by the original call | Logic? |
|---|---|---|---|
| (a) | RestoreAll `0x42d27f` | 77 bank/surface buffers (`alloc02196..02346`), the 233-byte bob cache (`alloc24329`: GetNumBob/InitCache), clip word `0x49a04e`; 13 bindings | **none** |
| (a) | MenuInit → DDLockSurface `0x46837a` | `0x4e17a6..a8` (lock count/flags); EAX = surface `0x60080000`, stored by MenuInit at `0x508f70` | **none** (`0x508f70` is a display pointer) |
| (a) | MenuInit → DeleteBank `0x4683ae` | releases 146 bank allocations (584 GlobalHandle/Unlock/Free bindings); MenuInit then clears `0x508f64` | **none** (bank memory) |
| (a) | MenuInit → FilledBox `0x468400`, DDFlipPage `0x468ca2` | no block byte (surface pixels lie outside the state) | — |
| (a) | MenuInit → DDUnlockSurface `0x468c91` | `0x4e17a6..a8` | **none** |
| (b) | AffGame `0x475063` | fps digits `0x496394..96`, text page `0x4963b5`, saved clip `0x49a02e/32`, cursor copy `0x49a042..45`, display ticks `0x4e17b0..b6`, palette cycle (25 bytes of `alloc00002`); 8 bindings | **none** |
| (a), (c) | NextAnimTerrain (Core stop) | CRT rand seed `0x340000c..f` (thread block +0xc), advanced 425 times | **logic** |
| (a) | NextAnimVeget (Core stop) | permutation cursor `0x4e1d18` | **logic** |

So under any mask that keeps game logic, **RestoreAll and AffGame write no logic byte at frames 0/1**. The only logic state still taken from the original is what Core's NextAnim* cell loops write (the CRT seed and `0x4e1d18`), together with any tile/object changes they would make on other frames.

## Input-side pieces (this front, original-first)

Captures, committed before translation: [evidencias/captura-entradas-quadro1-ia-exibicao.json](evidencias/captura-entradas-quadro1-ia-exibicao.json) (`ad27649`), with every executed block of MenuInit, InputGame, InputSend, CalculIconeAction and EnginNextEtape on the display path.

- **Cursor and view origin.** MouseInit centres the cursor variables on the 800×600 screen. It runs in the load entry before MissionLoad, so its result (400, 300) is part of the entry state and not of phases (a)–(c). The game mouse zones come from Core's InitGameZone/MouseSetZone. In frame 0 **MouseZone finds no zone** and returns 0 (tail `0x479d06`, now translated). InputGame then takes the **cursor-over-map hover** path (`0x429800..0x42b854`, now translated): it computes the cell (cursor/32 + view origin) and runs CaseEstDecouverte/CaseEstIlluminee (Core), TerrainEstSac/Gc/Mine/Piege, the region-grid structure bit and ChercheIndiceEngin (with Combat's `ocupa_celula` for EnginOccupeCase). It finds nothing, so there is **no edge scroll in frame 0**. In frame 1 GetCursorPos (0, 0) gives zone 1 and the **−1, −1 edge scroll of `0x508720/22`**: the same path as v1.
- **MenuInit (display path).** The DeleteBank branch (`0x508f64` set) is translated. Its display calls are providers: crossings here, declared boundaries in v1. Core's InitGameZone returns EBX = (17<<5); MenuInit and CalculGame then carry it into the recorded MCICD_Play registers (EBX `0x201`/`0x202`), which match.
- **The task VM.** iaSolver is Core's `MaquinaTarefasViva` over the live `0x512320..0x514908`; `PonteTarefas` is no longer used.

## Requests

- **Core:** NextAnimTerrain/NextAnimVeget for a viewport with rows (25×17): the cell loops, LongRand/CRT rand and the permutation cursor. They are the only logic crossings left in frames 0/1.
- **Graphics:** RestoreAll, AffGame and the DD*/FilledBox/DeleteBank routines. They write no logic byte here, and their crossings become providers when they land.
- **Missions:** the exclusion-mask policy file. This report's classification uses its writer attribution and should be re-checked against the mask once it is published.
- **Economy/Core:** the tile-grid list/bytes contract for UpdateChamp (first needed at counter 128).
