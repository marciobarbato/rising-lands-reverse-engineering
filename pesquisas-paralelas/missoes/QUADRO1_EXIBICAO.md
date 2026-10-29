# MONDE01 frames 0/1 with the display path executed (M2 round 3)

Original-only. The intact executable (SHA-256 `6c556520…43fb`) runs the display code instead of skipping it, and the result is compared with the v1 frame capture. Nothing in the accepted M1 or v1 evidence was modified.

## Scenario `exibicao`

Bench: [oraculo_exibicao_missao.py](oraculo_exibicao_missao.py), scenario definitions in [cenarios_oraculo.py](cenarios_oraculo.py).

**Startup** runs AppInit as in M1, then **the real `_WinMain@16` loop** from `0x4601c0`. Each iteration runs PeekMessageA → ProgIteration (counters, GetCursorPos, CalculGame, AffGame) → PlaySnd_Manage / MCICD_Manage. After 5 iterations the original reaches `CALL MissionLoad`.

**Executed natively** (skipped in v1):
- AffInit / DDInit;
- LoadPalette, DDSetPalette, DDLockSurface/DDUnlockSurface, DDFlipPage;
- FilledBox;
- LoadSTRATBank / LoadBank / SetBank / DeleteBank (25,480 bank allocations);
- RestoreAll;
- menu and game AffGame.

**DirectDraw** is the declared interim backend [exibicao_declarada.py](exibicao_declarada.py):
- the `DirectDrawCreate` import plus COM vtables;
- every call recorded, with traps on undeclared methods;
- surfaces as declared regions;
- `BltFast` as an exact bounded copy.

Graphics owns the final backend; this one is replaced when Graphics' lands.

**Still declared boundaries:**

| Routine(s) | Reason |
|---|---|
| InitTextLangue, TextGetMessage, AffText | need CRT `fgets` `0x48ce96` |
| LoadPie | needs CRT `fseek` `0x48cda2` |
| PlayVideo, credits | video and credits |
| MCICD_* and PlaySnd_* | audio, never initialized |

Neither `fgets` nor `fseek` is in Core's inventoried I/O set.

**Named inputs:**
- **Clock:** declared per call site. IaAlloc's `iaRandom(0)` keeps the M1 value, so the game RNG seed is the same as v1. Display calls take `0x123456+40k`.
- **Surfaces:** fill 0.
- **Cursor:** (0,0), the last SetCursorPos target. The program never issues another.
- **Keys:** not pressed.

## Evidence

All committed before any translation.

| File | What |
|---|---|
| [entrada-carga-missao-exibicao.json](evidencias/entrada-carga-missao-exibicao.json) | new MissionLoad entry snapshot: 25,344 blocks / 16.9 MB |
| [captura-carga-missao-exibicao.json](evidencias/captura-carga-missao-exibicao.json) | whole MissionLoad. Returns at `0x42d22d` with AL=1 and **the same 1,400 ordered binding requests as v1**. Delta-encoded against the entry snapshot. |
| [captura-quadro1-monde01-exibicao.json](evidencias/captura-quadro1-monde01-exibicao.json) and [rastro-quadro1-monde01-exibicao.json](evidencias/rastro-quadro1-monde01-exibicao.json) | frames 0/1 to the real return `0x475063`, with no declared caller frame (the loop is real), plus the per-routine entry trace |

## Checks (all passed)

| Report | Result |
|---|---|
| [m2r3-m1-composition-strict-exibicao.json](validacao/m2r3-m1-composition-strict-exibicao.json) | **Stage14 strict Python composition regression:** whole state equal over 25,343 blocks / 16,813,542 bytes, 25,482 allocation records and 1,400 binding requests; AL=1; deterministic, no bridge |
| [m2r3-missionload-exibicao-x86.json](validacao/m2r3-missionload-exibicao-x86.json) | MissionLoad replay; code integrity; segmentation 77,777 vs 1,000,000; fill 0x5A; skip markers (0 propagated bytes); Windows inputs; flushed footprint of 9,585 bytes (0 skip-derived, 0 skipped-store) |
| [m2r3-frame1-exibicao-x86.json](validacao/m2r3-frame1-exibicao-x86.json) | frame replay; integrity; segmentation; fills 0x5A and 0x00; boundary markers (0 bytes); M1 inputs (0 bytes); cursor/registers; **display ticks and surface fill**, which change only the stored tick copies `0x4e17b0/b4`; footprint of 191,061 bytes, almost all bank and surface reads by executed code |

## Game-logic state: v1 vs display ([report](validacao/m2r3-frame1-v1-vs-exibicao.json), [writers](validacao/m2r3-v1-vs-exibicao-writers.json))

**Method:**
1. All 938 v1 allocations are matched to display allocations by call sequence, using caller return, size, flags and the caller stack.
2. 2,628 bytes differ only because pointers moved; those are normalized away.
3. The remaining 50 / 50 / 328 / 367 / 366 bytes (entry, MissionLoad return, load_tail, between_frames, frame1) are explained below. Each one was attributed natively to its writers in both scenarios.

The 24,316–24,462 display-only blocks are banks, AffInit buffers and similar.

**No unit, structure, player, resource, AI, condition or market byte differs.** The RNG `0x497164` is equal in every phase.

| Bytes | v1 → display | Writer(s) | Kind |
|---|---|---|---|
| `0x49a018..1b` | 0 → 800×600 | DDInit (never written in v1) | display init; logic reads the screen size |
| `0x508724/26` | 0 → **25×17 viewport** | DDInit | display init, **logic input** (see below) |
| `0x4e1788..93`, `0x4e179c`, `0x4e17a0` | 0 → COM objects, palette, pitch 800 | DirectDrawCreate/CreateSurface/CreatePalette bindings, DDInit, DDLockSurface | display backend |
| `0x49a038/3c`, `0x508f5c`, `0x508f64`, `0x508f6c`, `0x508f70` | 0 → AffInit buffers, bank pointers, SetBank table, surface `0x60080000` | AffInit, ProgInit, MenuInit, SetBank, DDLockSurface | display/bank pointers |
| `0x4e2f3c` | 0x1ec34b → 0x1075172 | MemInit/MemAlloc | allocator byte count (bank allocations) |
| `0x508f7c/80/84` at entry and S0 | 0 → 5/2/1 | ProgIteration (5 real loop iterations in startup) | real loop; CalculGame resets them in load_tail, equal afterwards |
| `0x5099a8..ab` at entry and S0 | (0,0) → (400,300) | MouseInit = screen/2 | display-derived cursor variables; ProgIteration's GetCursorPos rewrites them in (b) |
| `0x5099dc..0x509a72` | mouse-zone rectangles | MouseSetZone | screen-geometry-derived UI state |
| **`0x508720/22` view origin** | after (a): (3,5) → (4,6) | v1: ScrollTerrain in (a) and (c); display: only (c) | **logic difference.** In v1, (a) edge-scrolls because MouseInit centred the cursor on a 0-size screen. Both scroll by −1 in frame 1 (cursor (0,0)). |
| **`0x340000c` CRT rand seed** (thread block +0xc) | differs from (a) on | display: `rand` in (a) and (c) | **logic difference.** NextAnimTerrain calls LongRand once per viewport cell: 425 per frame over 25×17; v1 visits 0 cells |
| **`0x4e1d18` permutation cursor** | (a): 2 → 4; (c): 3 → 5 | display: NextAnimVeget in (a) | **logic difference.** The shared Random-permutation cursor is advanced by vegetation animation over the viewport |
| allocation 13 (233 bytes) | zero → cache entries | display: GetNumBob in (a) while RestoreAll/AffTerrain draw (InitCache initializes it in both scenarios) | display bob cache |
| `0x49a01e/22`, `0x49a02e/32`, `0x49a04e` | clip words | SetClipping, Save/RestaureClipping, GetNumBob | display |
| `0x5099ac` | 1 → 0 | InputGame | mouse-zone hit under the centred cursor (a) |
| (b) only: `0x496394`, `0x4963b5`, `0x49a042`, `0x4e17b0/b4`, allocation 2 palette | — | CalculFrame (fps text, ticks), utoa, AffGame (cursor copy), Cyclage (palette cycling) | display only |

**Trace in frame 1.** The only routine-level difference is that **NextAnimTerrain calls LongRand/rand 425 times**. In (b), AffGame executes 66 routines (terrain, 726 structure draws, 16 units, HUD, minimap, palette cycling) and **writes no game-logic byte**. AffBatiments does not advance `0x4e1d18` in this view (no structure in mode 3).

## Verdict

**The v1 boundary was not harmless for frame 1, but AffGame itself was.** The divergence comes from display **initialization**, not from drawing between frames:
- DDInit sets the 25×17 viewport, so NextAnimTerrain and NextAnimVeget animate real cells. That consumes the CRT rand stream and the shared permutation cursor `0x4e1d18`.
- DDInit sets the screen size that MouseInit centres the cursor variables on, so frame 0 does not edge-scroll.

**What this means for the composition** (AI/runtime front):
- Start from the display artifacts.
- Model viewport-driven NextAnimTerrain (CRT LongRand) and NextAnimVeget (permutation cursor).
- Model MouseInit/MouseSetZone geometry, and the counters ProgIteration advances during startup.

Once a structure in mode 3 is on screen, AffBatiments also advances `0x4e1d18`. From then on, AffGame itself must be part of the reference.
