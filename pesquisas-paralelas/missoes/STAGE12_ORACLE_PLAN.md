# Stage12: whole-MissionLoad original oracle preparation

Status (updated): **runnable; the intact MissionLoad reached its real return for MONDE01 — see [Stage12 result](#stage12-result-runnable-program-start-oracle-and-original-only-missionload-capture-2026-10-28-claude). The Python whole-load composition exists. [Stage13](#stage13-m1-composition-and-comparison-2026-10-28-claude) stopped at an Economy contract. With that contract integrated, the [Stage14](#stage14-strict-m1-composition-on-integrated-code-2026-10-28-claude) strict run reaches AL=1 with the whole state equal: an M1 candidate, not yet accepted.** Original preparation status: light scaffold only. Stage11 is integrated at main `7f617fab29ce382f96b690ea70da25a33fab8bae` (pushed feature `c0f0a873c3657e72a3e478cf6fd7ea73c84dd58a`, implementation `2f6d96b89039590c598f312752d4fe0e3c5b3607`, original captures `ed0172a364310b28584824b3e49dc63db371ed93`). All four commits are ancestors of fetched main. Its locked candidate passed80native tests, common local gates, then9focused native tests reproduced on main with unchanged counts/state/trace. The heavy lease was released; no prior work or evidence is replaced here.

## Scaffold and inherited-state closure

[estado_herdado_missao.py](estado_herdado_missao.py) defines `BlocoHerdadoMissao` and `EstadoHerdadoMissao`. The caller must supply every byte, address, source revision and provenance. There is no world/player/rule constructor or zero-fill fallback. Aliases are views into one declared backing block; overlapping independent blocks are rejected. The registry validates all known physical grids, units, live/stored80-byte players, projectiles, four2704-byte type Bags,800route buffers and complete585728-byte DGROUP+.bss.

The live player types and stored player types are recorded independently. No all-human/disabled-AI table is synthesized to avoid research branches. A complete original input source or an explicitly identified nontrivial inherited fixture must be assembled and reviewed; **the Stage11 hash-only captures do not supply missing raw bytes**. Engine state produced by earlier constructor defaults cannot silently fill gaps. The M1 schema/alias/provenance requirements remain in [M1_SNAPSHOT_CONTRACT.md](M1_SNAPSHOT_CONTRACT.md).

[bancada_mission_load_original.py](bancada_mission_load_original.py) defines a native scaffold on the committed Stage11/Core harness. It overwrites every game-state arena from the inherited registry before use and requires explicit additional arena pages and external handlers. The class is not instantiated by import and has not been run. All original executable-section intervals come from the intact PE's protected-code metadata, so reached engine bodies execute as original instructions rather than Python replacements. Original loop heads may resume through Core's existing preserved-stack/register mechanism. Unknown imports/unsupported state remain errors/stops, never successful no-ops.

Finite limits are mandatory: total wall time≤300seconds, segment count≤10000, binding count≤10000 and≤1000000instructions per segment. These are upper guards, **not an estimated runtime or evidence of completion**. Binding and segment exhaustion must retain/report the partial original frame and memory. A caller-specified checkpoint is distinct from the real return. Reported `m1_accepted` and `whole_load_python_composed` remain false.

## Explicit external boundaries

Core16's validated generic binding API is consumed from committed main `b4c5a1072a2b2e494b3a6bf374bd978fc6e67b9a`. No live sibling import, OS emulation or engine provider stub is introduced. `FronteirasExternasCargaMissao` requires eleven named handlers and their provenance; none has a default return.

| Boundary | Original ABI / fixture obligation |
|---|---|
| CRT `fopen 0x48c71f` | EAX=path, EDX=mode; explicit known-file mapping and nonzero stream identity or declared failure. Native FileOpen stores that stream at0x4e1d1c and computes AL |
| CRT `fread 0x48c97b` | EAX=destination, EDX=item size, EBX=item count, ECX=stream. Supply actual declared bytes/cursor, preserve typed writes and return actual item count. Never confuse byte count with item count or fabricate EOF success |
| CRT `fclose 0x48c80b` | EAX=stream, explicit result. Native FileClose performs its global clear; the external handler must not duplicate engine stores |
| Inventoried I/O wrapper `FileSeek 0x45848b` | EAX=offset, DL=origin; handler reads the actual stream at0x4e1d1c. Wrapper bytes only save EBX/ECX, reorder arguments and call CRT fseek0x48cda2; no global stores. This one wrapper is an explicitly declared external I/O boundary permitted by Core's FRONTEIRAS_IO; it must be disclosed in reports. A future owner-reviewed CRT fseek registration could retain this wrapper too |
| IAT `GlobalAlloc 0x5231c0` | two stdcall dwords flags,size; choose only an explicit finite planned allocation, with retained initial bytes and no automatic zero allocation |
| IAT `GlobalLock 0x5231d0` | handle→locked pointer; do not assume opaque handle equals pointer |
| IAT `GlobalHandle 0x5231cc` | actual locked **pointer**→opaque handle. Python counterpart resolves the identity of the actual live buffer, not equal bytes or a copied allocation |
| IAT `GlobalUnlock 0x5231d8` / `GlobalFree 0x5231c8` | exact handle and explicitly declared results/lifetime, retaining all resource bytes and ordered cleanup events |
| IAT `GetPrivateProfileIntA 0x5231ac` / `StringA 0x5231b0` | four/six stdcall arguments, actual shipped MONSTRE.INI input and original default arguments. Reuse the committed profile protocol; do not install implicit absence or return empty strings for unknown files |

The file input is actual `WORLD/MONDE01.ETA` SHA-256 `19237b8c3f3c0c76022276da229bec727b17603440823c43561aba159dd47015`. The profile is actual `INSTALHD/MONSTRE.INI` SHA-256 `6be59feea11e20eda101ee1e528b3306be447da9e9c3a3807bc2c1bf9e071046`. They remain read-only. Briefing TXT is not read by MissionLoad.

## Resource ownership proposal for Core17 compatibility

Prepare a finite explicit resource registry carrying `(opaque handle, native pointer, actual Python buffer identity, size, initial bytes, active lifetime, declared results)`. Core reports a64KiB classification allocation and a1MiB component LIFO. A freed temporary remains in the state/binding report; reusing an address/buffer and its tail bytes requires an explicit lifetime plan. No new bytes are zeroed merely because a system allocation was requested.

The proposed Core17 Python shape is compatible: `alocar(flags,size)->handle`, `fixar(handle)->live mutable buffer`, `obter_handle(the_same_buffer)->handle`, `desfixar(handle)->explicit u32`, `liberar(handle)->explicit u32`. Native GlobalHandle receives the locked pointer. This is still a pending provider contract until its validated main commit is supplied. Do not import its live implementation or substitute the first lock's handle for the second lock's pointer. Native second-lock NULL is reported as the original fault at0x42efd9, never converted into a clean return.

## Remaining work before a measured original run

1. Assemble the complete raw inherited registry, including exact stored/live player provenance and program-start AI allocations/rules. The scaffold deliberately rejects missing references; it does not create substitute players, Bags or runtime tables.
2. Implement/review the explicit finite file/profile/resource fixtures against the above ABI and preserve all aliases. Eleven callable slots alone are an interface, **not implemented Windows semantics or a runnable fixture**.
3. Audit oracle segmentation/budget behavior and whole-memory capture under Core's committed opt-in dispatcher. No new native execution was performed in this light turn, so the new scaffold has no validation claim.
4. Ask the coordinator for one measured calibration window only when input/handler closure is complete. Suggested first bounded experiment: one actual MONDE01 original entry with a≤60second total cap and explicit partial checkpoints; retain a fault/stop exactly. A later≤300second whole-return attempt needs its own justified grant and enough time before18:25BRT. These are proposed bounds, not measured estimates; do not launch a broad matrix on that basis.
5. Freeze/commit the complete original-only result before writing a Python whole-load composition.

Core17 full remap/cleanup/final AL is not adopted yet; current committed class reset/allocation/classification stops at0x42ef8b. Core `Engin_RetrieveExperimente 0x441623` and the production AI/Economy adapters remain explicit composition dependencies. The original oracle may execute original engine bodies once inputs are declared, but Python M1 acceptance requires the actual committed providers and full post-load byte equality at return to0x42d22d. No whole-load, real mission or objective result is claimed here.

## Late published provider update for handover

At18:19BRT Core published and reported exact-main reproduction of full remap main `09d3953c6dda02ba6e4f6ca9ac61e51ca48782e6`. Its committed `docs/core/REMAP_COMPLETION.md` was read directly from that immutable commit and its local fetched-main ancestry verified. This resolves the earlier **availability** gap; the Stage12 prototype remains based on Missions main7f617fa and has not merged, consumed or validated the new provider.

Use the actual `conclusao_remapeamento.remapear_mundo(world, *, alocar, fixar, obter_handle, desfixar, liberar)`; it returns the original consumedAL bool, performs no unit reinsertion, and preserves callback exceptions/resource effects. `retomar_conclusao_remapeamento` accepts retained state, preserving the class buffer and completed work. GlobalHandle consumes live-buffer identity on the Python side and locked pointers natively. The original ignores unlock/free return values; do not invent a conditional engine branch based on them. Component-lock NULL remains an explicit original write fault at42efd9/address0.

Published measurement: original MONDE01 full remap alone31.157seconds,56components,731segments; Core also reproduced realRET/AL1 on main. This is a measured **remap** cost, not a whole-MissionLoad estimate. Core's original snapshots include compressed full mapped input/output bytes, resource states and traces; they may supply identified raw subsets for the inherited registry, but they are not a complete program-start/MissionLoad input package. Preserve their exact base/alias/provenance rather than treating unrelated constructor arenas as interchangeable.

`Engin_RetrieveExperimente0x441623` remains unimplemented and was canceled for this development window. Raw inherited-state assembly, concrete external fixtures and real AI/Economy adapter adoption remain as above. No new run or implementation was started on this notification; preserve the pending Stage12 branch for the next owner.

## Stage12 result: runnable program-start oracle and original-only MissionLoad capture (2026-10-28, Claude)

**Status: the intact original MissionLoad 0x46c2cf for MONDE01 reached its real return 0x42d22d (AL=1) from an inherited state produced by the original program-start path. Original-only; no Python whole-load composition exists; M1 is not accepted.** The earlier scaffold below (`estado_herdado_missao.py`, `bancada_mission_load_original.py`) is kept; its registry now validates the frozen entry state.

### What runs

[oraculo_carga_missao.py](oraculo_carga_missao.py) (`BancadaCargaMissaoOriginal`) runs the intact executable on Core's `BancadaX86` and the committed Stage16 binding transport. Core's per-instruction Python checker is replaced, for speed, by equivalent native guards: address-scoped stop hooks, BEGTEXT `R|X`, headers/.reloc/.rsrc `R`, DGROUP/.bss/.idata `RW`, the mapped tail `0x52e000..0x600000` without access, stack/arena/thread pages `RW` without execute, and instruction-count segments resumed at the same instruction. The code-section SHA-256 is recorded before and after and must equal the executable bytes (`02985de5…`).

Startup, all original code executed natively in one memory image:

1. CRT main-thread data: `__InitThreadData` 0x490de8 on a zeroed 0xe4-byte block (the `__WinMain` memset at 0x48fe2a), pointer stored at 0x522244 as `__NTInit` does at 0x48e7ee; then `__NTInitFileHandles` 0x48fc83. Needed because `InitRand` calls CRT `rand` (thread data) and `IaAlloc`'s `debugSymLoad` uses CRT `open/read/lseek/close`.
2. `AppInit` 0x418188 (EAX = declared hInstance 0x400000), i.e. the whole `ProgInit`: MemInit, Randomize/InitRand, getcwd, FindCD, path strings, SortLoadCaract, palette, all allocators (Engin/Batiment/Mission/Player/MiniMap/Chemin/Ia/Projectile), RISING.SBL/RUL loading, RechercheInit, MarcheInit, InitPlayer, InitInputPlayer, TerrainLoadObstacle/Color and the palette tables.
3. Five native `CalculGame` frames: state 1 (intro probe, main menu `MenuInit(0,2)` with RechercheReset/Engin_ResetExperience/InitPlayer), state 2 (Enter on default item 0 → `MenuNewSelect`), state 3 (Enter on item 0 → new campaign: ReseauActif=0, MissionReset, viewer 0, SetPlayerType ×4, `MenuInit(0,0x11)` with ObjectifLoadText and RechercheCalculNew), state 0x11 (Enter, no research click → state 0), state 0 (MouseInit, InitCache, InitGouttes, stores) which stops at the real `CALL MissionLoad` 0x42d228.

Not executed during startup (47 calls of 16 routines, each stopped at its entry and returned with its own RET cleanup and declared/unchanged EAX): AffInit, DDSetPalette, DDLockSurface (EAX 0), DDUnlockSurface, DDFlipPage, LoadPie, FilledBox (`ret 8`), ResetMode, AffText (`ret 0x10`), MCICD_Play/Stop, PlayVideo, Create/FreeCredits, InitTextLangue (needs `FileReadLine`/CRT `fgets`, not an inventoried I/O boundary), TextGetMessage (EAX 0), LoadSTRATBank (EAX 0, 24k sprite allocations), SetBank, LoadBank (EAX 0), DeleteBank. ProgIteration (frame counters, cursor), AffGame, WndProc, AppWindowInit, DisableIME, PlaySnd_InitSoundLib and MCICD_Init are not run either. During the oracle phase a skip address is a hard stop.

The oracle phase resumes the stopped CPU at 0x46c2cf with the real CalculGame frame and stops at the real return 0x42d22d. Only declared bindings answer calls; any other import reaches a trap page and stops.

### Declared external boundaries ([fronteiras_carga_missao.py](fronteiras_carga_missao.py))

| Boundary | Fixture |
|---|---|
| CRT fopen/fread/fclose 0x48c71f/0x48c97b/0x48c80b, FileSeek 0x45848b | Read-only original media: install dir → `source/cd/INSTALHD`, `D:` → `source/cd`, case-insensitive, `.\` = current dir. Modes `rb`/`r` only (TEXTES.TXT `rt` is why InitTextLangue is skipped). FILE* is an unmapped opaque value; fread returns item counts and copies partial tails; a path absent from the media returns NULL; paths outside the roots stop |
| GlobalAlloc/Lock/Handle/Unlock/Free | Finite arena 0x40000000..0x50000000, ≤60,000 allocations, GMEM_FIXED/ZEROINIT only, handle==pointer, page-aligned, never reused, declared fill byte for non-ZEROINIT; unlock-without-lock, free-while-locked and stale handles stop |
| VirtualAlloc | Commit (±reserve), RW/RWX, zero pages from the same arena (CRT heap growth) |
| GetPrivateProfileIntA/StringA | Windows subset: `;` comments, trimmed names/values, quoted strings unquoted, decimal integers only, queried duplicate keys and enumeration stop; file must exist on the media |
| CreateFileA/ReadFile/SetFilePointer/CloseHandle/GetFileType/GetLastError/GetStdHandle | Read-only OPEN_EXISTING over the media (debugSymLoad's RISING.SBL via original CRT bodies); GetStdHandle answers 0 (GUI process) |
| timeGetTime/GetTickCount, GetAsyncKeyState, SetCursorPos, ShowCursor, SetErrorMode, GetDriveTypeA, GetVolumeInformationA, GetCurrentDirectoryA, GetCurrentThreadId, GlobalMemoryStatus/Compact | Named inputs below; ordered answers are consumed and exhaustion stops |

Named inputs (all recorded in the captures): install directory `C:\RISING` (installer `TemplateTargetDir`), CD drive `D`, volume label `RISING_LANDS_BR_` from the BIN PVD, clock 0x00123456 (seeds `0x498db4` via `iaRandom(0)`), allocation fill 0xA7, MEMORYSTATUS 32 zero bytes, thread id 1, key script Enter/release ×2 then Enter.

### Startup-control and inherited-state findings

- **Live player controls at MissionLoad entry are (1,2,2,2)**, written by original code twice: `InitPlayer` 0x46dcb4 (ProgInit and the main-menu block 0x468e37) and the new-campaign `SetPlayerType(0,1),(1,2),(2,2),(3,2)` at 0x42c479..0x42c4b2. This equals the AI front's fixture. The stored player table's type bytes are never initialized (allocation fill); `PlayerRetrieve` copies only +6 and +0xc..+0x13, so it does not touch types.
- Mission byte 0x496fe4=1 (`MissionReset`), viewer 0x508041=0, ReseauActif 0x4e0730=0, state 0x4e2f78=0.
- Saved experience 0x4e19ec..0x4e1a14 = `ff00`×20 (`Engin_ResetExperience` in MenuInit(2)); after MissionLoad the current buffer 0x4e19c4 holds the same 40 bytes.
- Research tables 0x508134.. are zero after RechercheReset/RechercheCalculNew with no research click.
- `ObjectifLoadText` 0x47c557 opens MONDE01.TXT as an existence test and reopens it without closing the first FILE*: one original leaked stream is recorded in the entry artifact.

### Evidence

| File | SHA-256 | Content |
|---|---|---|
| `evidencias/captura-carga-missao-original.json` (v1, commit 61847e5, source 865d5ab) | `e0b7ca47…331ec` | First capture, before the coordinator review |
| `evidencias/captura-carga-missao-original-v2.json` (commit 81815eb, source 14b56a9) | `eb7d2303…3afc` | Hardened bench; inherited image, final image and 1,400-event oracle binding log byte-identical to v1 |
| `evidencias/entrada-carga-missao-original.json` | `0692dea1…2ddf` | First-class MissionLoad entry: 882 blocks (DGROUP+.bss, CRT thread data, 879 live allocations, 64 KiB native stack), registers, segments/GDT, arena next-free 0x418e9000 and policy, open streams/handles, remaining declared answers |
| `validacao/stage12-missionload-original-x86.json` | `4355d395…5efe` | Original-only checks below |

Startup: 31.0 s, 3,583 segments, 3,106 binding calls (1,276 profile reads, 879 GlobalAlloc), 881 allocations. Oracle: 2.49 s, 1,425 segments, 1,400 binding calls (1,019 fread, 1 fopen/fclose, 17 FileSeek, 4+16 profile reads, 57 Global allocation lifecycles = remap class buffer + 56 components). Every compressed block carries its SHA-256.

### Original-only checks (validation report, all passed)

1. **Replay**: same inputs reproduce the committed inherited image, real return, AL=1, final image and binding log (with footprint hooks active).
2. **Code integrity**: code SHA-256 before = after = executable bytes, in the capture and the replay.
3. **Segmentation invariance**: oracle with 77,777-instruction segments (1,741 segments) vs 1,000,000 (1,425): identical entry, final image, binding log and AL.
4. **Fill independence**: fill 0x5A vs 0xA7: 552,340 final bytes still hold the fill, 0 other differing bytes, 0 fill bytes copied by MissionLoad, identical binding log.
5. **Input footprint** (oracle-only read-before-write over DGROUP+.bss, CRT thread page, native stack and all pre-entry arena bytes; binding writes mark their destinations): 1,757 bytes in 972 ranges. Classes from perturbation masks: 1,701 startup-executed original code or PE image; 4 declared inputs (the clock-seeded RNG 0x498db4 by `iaRandom`, the CD drive letter 0x509594 by MissionLoad's path strcpy); 4 native stack (the entry return-address slot read by the final RET); 48 untouched allocation fill, all read by Watcom `__STOSD`'s cache-touch `cmp byte [eax+0x20],dl` 0x48d8ee (and `__STOSB`) just before overwriting, flags discarded, consistent with check 4. Skip-derived values (21-byte mask, e.g. DDLockSurface→0 at 0x508f70) and skipped-routine static stores: **0 bytes read**. With every skipped call returning a distinct marker, the final image differs only inside the entry skip mask and the binding log is identical. Changing clock/install directory/drive/thread id/memory status changes 11 final bytes outside the input mask (clock-driven IaReset draws), as expected for a named input.
6. A separate static read-watch of 70 ranges written by non-executed routines recorded no reads.

### Tests and gates

- Light CPU-free: `test_carga_missao_original.py` 10 tests (handlers, profile subset, CRT/Win32 files, arena identity/budgets, declared answers, PVD label, skip RET cleanup vs original bytes, frozen-entry closure of the Stage12 registry: live types (1,2,2,2), saved XP). Native replay test (`RISING_EMULAR=1`) re-runs both captures: 11 run, 0 skipped, passed (68 s).
- `python3 -B scripts/check.py --domain missions`: 93 tests, 32 optional native skips, passed.
- Full native missions suite, common checks, integration and committed-main reproduction: **not run** in this slice.

### Development attempts preserved or recorded

Trial stops while closing inputs (all superseded by the committed captures): CRT `rand` fault on uninitialized thread data (→ step 1); fopen `rt` for TEXTES.TXT (→ InitTextLangue skip); sprite banks exhausted an 8,192-allocation budget (→ LoadSTRATBank skip); `debugSymLoad` reached undeclared CreateFileA (→ Win32 file fixture); wrong stack cleanup for FilledBox (fault at 0x1b3, → RET-immediate table); 90 s wall budget under Core's per-instruction hook (→ native guards); `./monstre.ini` path (→ `.\` handling); entry-state check found the leaked briefing stream (→ recorded). Kept under `.local/`: `stage12-calibration-1.json`, `stage12-calibration-fill5a.json`, `stage12-hardened-trial.json`, `stage12-validation-trial.json`, `stage12-missionload-failed-*.json`, capture/validation/test/domain logs.

### Limits

Startup frames between CalculGame calls are not executed (ProgIteration frame counters stay 0; no AffGame/WndProc). The research screen gets no click. Menu text pointers are NULL. The profile parser and Win32 file fixtures are declared subsets. Host-side fixture reads (path strings, 0x4e1d1c in FileSeek) are not in the footprint. The static watch over-approximates direct stores only.

### Next: Python composition (superseded by Stage13 below)

Start from `entrada-carga-missao-original.json` bytes exactly and compare against the v2 final image, AL and ordered binding log. Needed providers: Core resets/remap/placement (on main), Core `Engin_RetrieveExperimente` (main 3d782ca), the AI adapter `reinicio_ia_compartilhado` for IaReset over live types (1,2,2,2) and the clock-seeded RNG (main 977c890), Economy MarcheResetAll/initializers, and the Missions loaders. The declared file/profile/allocation answers in the oracle log are the composition's external inputs.

## Stage13: M1 composition and comparison (2026-10-28, Claude)

**Result: NOT M1.** The strict composition stops at `EnginInitTechnologie 0x441459` (MissionLoad CALL `0x46c5af`, owner Economy). Up to that point every binding request and every allocation record equals the original. A declared diagnostic bridge past the stop gives AL=1 and a byte-identical whole state; that run is not M1 evidence. Report: [validacao/stage13-m1-composition.json](validacao/stage13-m1-composition.json) (source `b114fa7`, clean tree, CPU-free).

### Design as implemented

1. **One memory map** (`mapa_memoria_m1.MapaMemoriaM1`). The 882 entry blocks are decompressed with their SHA-256 verified. Each provider's own buffer is bound at its original address and filled in place by slice assignment. Most of these are Core world pools, Economy tables, market/cycle buffers, `BonusUnidades`, `Economia`, the 800 route buffers, the four Bag pools and the vision grids. DGROUP and the allocations are split around them, and the remaining bytes become Missions gap segments. That gives 950 non-overlapping segments. Three Core representations are not raw bytes, so each has one declared codec:
   - u16 Python lists (tiles, regions, color stack): the list is canonical.
   - 161 scalar caches (search context, dimensions, iterators, RNG, fatigue limits/bonus, controls, alliance masks, …): the bytes are canonical. The composer pulls them before and pushes them after every provider call or callback. A divergence raises.
   - Core minimap layers: these are 65,536 bytes, but the native allocations are 16,384 bytes. The map exposes the first 16,384 bytes. The provider-private excess is poisoned with 0x5c and verified unchanged at the end, together with `mascaras_alianca[4]`, which has no original address.

   When two providers model the same bytes, the Core buffer keeps ownership and Economy points to it by identity, following the committed `montar_habitacao` pattern. Seven such links are listed in the report. Every other constructor attribute is denied by a class-swap guard: reading or writing it raises `AtributoNaoMapeadoM1`. Rebinding a mapped buffer raises too.
2. **Arena** (`arena_composicao_m1`). It continues from the entry next-free `0x418e9000` with a page-aligned bump allocator: handle==pointer, fill 0xA7 (ZEROINIT gives zero), no reuse. Each allocation is a new map block, and a freed one leaves the map with its bytes SHA-256 recorded. The class buffer and the 56 component buffers land on the native pointers, and their freed SHA-256 values equal the original.
3. **External inputs.** `WORLD/MONDE01.ETA` and `INSTALHD/MONSTRE.INI` are read from the read-only media through `fronteiras_carga_missao.MidiaOriginal`/`PerfilWindows`, the oracle's own resolution and INI parsing. A recording `Leitor` logs fread and FileSeek with their cursors. FileOpen/FileClose are Missions caller code (`[0x4e1d1c]` store/clear, AL), and stream identity follows the entry `crt_next_stream_index`. Nothing is replayed from the capture.
4. **Order.** The composition follows `0046c2cf.asm` in this sequence:
   - `reinicio_missao.resetar_para_missao`, which covers MakeMissionName, the path build, the 0xffff stores, IconeReset, Core TerrainReset/MiniMapReset/BatimentResetAll/EnginResetAll, combat ProjectileReset, MessageBoxInit and BallonInit;
   - FileOpen;
   - the header prelude (FileSeek, the four layers, 54→66, resources, dimensions, view);
   - Core `remapear_mundo` (AL 1);
   - the structure copy;
   - LoadEngin;
   - the eight auxiliary loaders, each at its own CALL;
   - FileClose;
   - MissionPlaceTerrain (units 0,1,2,11..15 placed; structure 0 placed and inhabited);
   - the six tails;
   - AL=1.

   A provider exception stops the run at its CALL and keeps every earlier effect.
5. **Comparison** (`comparacao_carga_missao`). It covers all 881 final blocks byte for byte, all 938 allocation records (`active/events/flags/index/initial_byte/locks/pointer/size/freed_sha256/kind`), AL and the 1,400 normalized binding requests. Nothing is masked. The only fields not compared are the oracle's native call-site and stack metadata of allocation records, and the 16 profile key strings that the original builds in an uncaptured stack frame. Both are reported.

### Counts

| Run | Steps | AL | Bindings | Allocation records | State |
|---|---|---|---|---|---|
| strict (M1 candidate) | 26 completed, stop at EnginInitTechnologie 0x46c5af | — | 1,400/1,400 equal | 938 equal | 3,966 bytes differ: 4×26 Bag bytes, 4 player +6 bytes, 3,858 DGROUP bytes (all six tails' writes) |
| strict repeated | identical stop and state SHA-256 | — | — | — | deterministic |
| diagnostic, bridge `ordens` (NOT M1) | 32, return reached | 1 | 1,400/1,400 equal | 938 equal | 881 blocks / 2,659,375 bytes equal |

The strict run takes about 2.9 s.

**Blocking contract (Economy, not edited).** In `proprietarios.PropriedadeConstrucoes`, `ordens` is a copied single 10,816-byte buffer with a 2,704-byte owner stride. It must accept the four live Bag pools of `[0x4e19b8]` by identity: Core's `bolsas_tipos_unidades`, the allocations `0x41781000..0x41784000`. `cauda_carga.definir_tecnologia_unidades` and `aprendizagem.atualizar_ordens` must then address owner j as `ordens[j] + type*104`.

**Non-blocking recommendations (Core).** Accept the exact 16,384-byte minimap allocations. Optionally use u16 views for tiles, regions and the color stack.

**Tests.** `test_composicao_carga_missao.py` ran 10 tests, all passed with none skipped. `scripts/check.py --domain missions` ran 103 tests with 32 optional native skips and passed.

**Not run:** native suites, common gates, integration and committed-main reproduction. Logs are in `.local/stage13-m1-composition-attempt1.log` (pre-commit run, same result), `.local/stage13-m1-composition-final.log` and `.local/stage13-domain.log`.

## Stage14: strict M1 composition on integrated code (2026-10-28, Claude)

Economy's per-owner `[0x4e19b8]` Bag contract is on main ff2f5cf. Source `ea1aac5` makes it mandatory and removes every bridge. Report: [validacao/stage14-m1-composition-strict.json](validacao/stage14-m1-composition-strict.json). It is CPU-free and was generated from a clean tree. The Stage13 report is kept unchanged as history.

| Criterion | Result |
|---|---|
| Return semantics (0x42d22d) and AL | reached, AL=1, 32 steps, no stop |
| Whole state | 881/881 blocks, 2,659,375 bytes, 0 differing |
| Allocation records | 938/938 equal (881 entry + 57 remap, freed-bytes SHA-256 included) |
| Binding requests | 1,400/1,400 equal |
| Bridges / provider excess | none / unchanged |
| Determinism | two runs: identical state SHA-256 `da9ce107…`, binding SHA-256 and AL |

**Explicit comparison exclusions:**
- The 16 `GetPrivateProfileStringA` key strings `GROUPE00..15`. The original builds them in its stack frame at 0x2007d38, which the capture does not keep. All other fields at those positions are compared.
- The allocation-record `caller_return`, `freed_caller_return` and `stack` fields. These are native observation metadata, not state.
- The native stack. It is not in the original final capture and is not mission state.

**Status: M1 candidate.** Acceptance requires the coordinator's gates, integration and committed-main reproduction.

**Non-blocking Core recommendations, unchanged from Stage13:**
- accept exact 16,384-byte minimap allocations;
- use optional u16 views for the list grids.

**Tests:** `test_composicao_carga_missao.py` ran 11 tests, 0 skipped, all passed. `scripts/check.py --domain missions` under the lease ran 104 tests with 32 optional native skips and passed.

**Logs:**
- `.local/stage14-strict-trial.log`: pre-commit run, same result.
- `.local/stage14-strict-final.log`
- `.local/stage14-domain.log`
