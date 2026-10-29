# MONDE01 first frame (M2.1): what the original executes

Original-only capture made with the intact executable (SHA-256 `6c556520…43fb`) before any translation. Evidence:

- [captura-quadro1-monde01-original.json](evidencias/captura-quadro1-monde01-original.json): SHA-256 `c06f78ea2f611d668b4a2fc7bde712b07c21ed8eb0a929668d4d70e56d47fed8`, source `e6aa305`, committed in `ca35221`.
- [rastro-quadro1-monde01.json](evidencias/rastro-quadro1-monde01.json): the readable entry trace, SHA-256 `4585933089b12af2c8c9fcf14c6ae4f7e96c2c9ea4cba9c34b4efaa69a43fb0e`.
- [validacao/m2-frame1-original-x86.json](validacao/m2-frame1-original-x86.json): the checks below.

Bench: [oraculo_quadro_missao.py](oraculo_quadro_missao.py). The register view (every entry as `callee@caller+off EAX EDX EBX ECX`) is [rastro-registradores-quadro1-monde01.json](evidencias/rastro-registradores-quadro1-monde01.json). This is M2.1 evidence only. M2 is **not** accepted.

## Timeline

The run reproduces the accepted M1 path unchanged. The entry snapshot, the final state and the 1,400-request binding log all equal the committed M1 artifacts. It then executes three phases:

| Phase | From → to | Native | Bindings | Not-executed boundaries |
|---|---|---|---|---|
| (a) `load_tail` | `0x42d22d` → load-state CalculGame RET | 0.07 s | 12 GetAsyncKeyState, 1 ShowCursor(1) | RestoreAll: DDLockSurface×2, LoadPie×2, DDUnlockSurface×2, DDFlipPage×2, DDSetPalette. MenuInit: DDLockSurface, FilledBox, LoadPie, MCICD_Play, DDUnlockSurface, DDFlipPage. CalculGame: MCICD_Play |
| (b) `between_frames` | ProgIteration `0x475063` → CalculGame entry `0x42c868` | 0.01 s | PeekMessageA (no message), GetCursorPos | AffGame, PlaySnd_Manage, MCICD_Manage |
| (c) `frame1` | `0x42c868` → ProgIteration `0x475063` | 0.06 s | 12 GetAsyncKeyState, SetCursorPos(0,0) | MCICD_Play |

**The load-state invocation is already a game frame.** State 0 jumps from MissionLoad to `0x42d27f`. That path runs RestoreAll, SetClipping, clears the counters `0x508f7c/80/84`, then MenuInit(…, 0x12), InitGameZone and PlayerAttaqueReset. It then falls into the shared frame body: the state is now 0x12, so the gate at `0x42d3c0` passes. Phase (a) therefore runs EvenementEnCours → … → TestFinDeMission once ("frame 0"), and frame 1 is the second pass.

The window loop between frames comes from the `_WinMain@16` and ProgIteration bytes:
1. AffGame runs, the `0x5099af/ae` and `0x5099b2/b1` flags are cleared, and ProgIteration returns to `0x460212`.
2. The loop calls PlaySnd_Manage and MCICD_Manage, then tests the quit flag `[0x49a059]`=0.
3. PeekMessageA returns 0 and the active flag `[0x49a058]`=1 is tested.
4. ProgIteration runs: `++[0x508f7c]` (now 1), `[0x508f80]` is incremented only when the counter is even, and `[0x508f84]` only every 3rd frame. Neither changes here.
5. GetCursorPos stores the cursor to `0x5099a8/aa`, and CalculGame is called.

## Frame-1 callees in call order

Nested routines are listed in first-entry order with counts. `*` marks a routine that is not executed: it is a declared boundary.

| Top-level callee | Call site | Calls | Nested routines |
|---|---|---|---|
| PlayerAttaqueReset | CalculGame+0xa7b | 1 | — |
| EvenementEnCours | +0xa80 | 1 | — (AL=`[0x4e1b0e]`=0) |
| MCICD_Play* | +0xac5 | 1 | guard `[0x4e2f29]`=0 |
| PlayerGetType | +0xb16 | 5 | — |
| InputGame | +0xad8 | 1 | MouseZone, ScrollTerrain, NextGouttes |
| InputSend | +0xadf | 1 | ReseauActif |
| MissionGetNum | +0xaf1 | 4 | — |
| CalculNextReflect | +0xafa | 4 | iaCalculPlayer×4, AvanceMonstre, MissionGetNum, iaSolver |
| ProcessInputGame | +0xb4d | 4 | — |
| MessageBoxCalcul | +0xb7e | 1 | — |
| GameNextFrame | +0xb83 | 1 | — |
| CalculIconeAction | +0xb88 | 1 | EnginGetNbSelection, BatimentGetSelection |
| ProjectileCalcul | +0xb8d | 1 | ProjectileAnim×100 |
| CalculEnginNextEtape | +0xb92 | 1 | IATestUtilite×16, iagMessTestSendMessageEngin×16, iabTestEngin×16, EnginNextEtape×16, BonusGetValEngin×24, GetBit×64, CalculFatigue×16, SetEnginCollision×8, SetCollision×8, Chemin_ModifieZone×8, Random×8 |
| CalculBatimentNextEtape | +0xb97 | 1 | ResetTableauHangar, IATestUtilite, BatimentNextEtape, BagContientTroupe, CalculTroupe, BatimentGetCase, BatimentCollision×30, CaseEstDecouverte×93, BatimentEstDecouvert×3, BatimentContourEstIllumine×3, CaseEstIlluminee×78 |
| RechercheCalcul | +0xb9c | 1 | MissionGetNum×4 |
| PlayerInitAllianceCompteur, SetUpdateChamp, UpdateChamp | +0xba1/+0xba6/+0xbab | 1 each | — |
| CalculMatiere | +0xbb0 | 1 | IntToBCD×8, GetBit×16, BCDToInt×4, SetBit×2 |
| CalculCompteurMarche, CalculCompteurProposition | +0xbbc/+0xbca | 1 each | — |
| NextAnimTerrain, NextAnimVeget | +0xbde/+0xc04 | 1 each | — (`[0x4e0730]`=0 selects NextAnimVeget) |
| PlayerAttaqueCalculSympa | +0xc09 | 1 | — (frame 0 also entered MAJSympathie×12) |
| TestFinDeMission | +0xc1e | 1 | BatimentExiste×1000, BatimentGetPlayer, BatimentGetType, TestRessource×3, MissionGetNum |

Frame 0 adds EnginTrouveCible, PlayerEstAllie×7 and PlayerGetType×17 under CalculEnginNextEtape, and MAJSympathie×12. The AI kernels `iagUnitNoyau`/`iagVilleNoyau`/`iagRessNoyau`/`iagWarNoyau` are **not reached** in either frame. There is no file I/O, allocation or clock read in (a)–(c). TestFinDeMission returns AL=0, so CalculGame stores `[0x4e05a0]`=0.

## State and RNG

| | `0x497164` | `0x498db4` | Changed bytes |
|---|---|---|---|
| S0 (MissionLoad return) | `0x4926732e` | `0x3212b7ce` | — |
| after (a) | `0x1c019f87` | unchanged | DGROUP 570; allocations 14 (24), 875 projectiles (100), 876–879 input buffers (10 each) |
| after (b) | unchanged | unchanged | DGROUP 1 (`0x508f7c`) |
| after (c) | `0x78fe3b37` | unchanged | DGROUP 396; allocation 14 (8) |

Each phase in the capture records the full state (per-block hashes plus the bytes of every block changed since the previous phase), registers, the binding log, the boundary events (registers, stack words, guards) and the changed ranges.

## Named inputs and boundary policy

- **M1 inputs**: unchanged.
- **GetAsyncKeyState**: every frame-phase call answers 0. That is 12 keys per InputGame: 0x1b 0x10 0x11 0x2e 0x12 0x20 0x26 0x28 0x27 0x25 0x0d 0x58.
- **PeekMessageA**: answers 0, so WndProc is not dispatched.
- **GetCursorPos**: (0,0). This equals the last SetCursorPos target of the accepted path; Windows keeps the cursor there when the mouse does not move.
- **Declared caller frame**: ProgIteration/_WinMain@16 return `0x460212`, saved EBX 0 (from `0x4601af`), and saved ECX/EDX and carried ESI/EDI/EBP set to 0. The footprint shows only ProgIteration's own pops/RET read these 16 bytes, and the F run shows the register values do not matter.
- **Boundaries**: display (`AffGame`, `DD*`, `LoadPie`, `FilledBox`, …), the sound library (`PlaySnd_*`; PlaySnd_InitSoundLib is never executed) and MCI CD (`MCICD_Play/Manage/Stop`; MCICD_Init is never executed). The bench stops at entry, records EAX/EDX/EBX/ECX and 4 stack words, then returns with the routine's own cleanup. Every declared cleanup equals the RET immediates reachable in the intact bytes, following shared epilogues, thunks and switch tables. MCICD_Play and MCICD_Manage return with no store while `[0x4e2f29]`=0, which every event records. CalculGame ignores MCICD_Play's AL.

## Checks ([report](validacao/m2-frame1-original-x86.json), passed)

- **Replay**: identical phase states, binding logs, boundaries, Windows answers and entry trace. The code-section SHA-256 is unchanged.
- **Segmentation**: 77,777- vs 1,000,000-instruction segments give equal state, logs, boundaries and trace.
- **Allocation fill**: 0xA7 vs 0x5A and vs 0x00 differ in no computed byte, and the logs and traces are equal. The 208 never-written fill bytes that ProjectileCalcul/ProjectileAnim (allocation 875) and ProcessInputGame (876–879) read do not change behavior for these three fills.
- **Boundary markers**: when every non-executed routine returns a distinct EAX, 0 bytes differ outside the S0 mask in (a)/(b)/(c). The only control-flow difference is one extra non-executed DeleteBank call from MenuInit+0xf8.
- **M1 Windows inputs** (clock, directory, drive, thread, memory status): 0 bytes propagate.
- **Frame inputs** (cursor (320,240), non-zero caller registers): only the cursor stores `0x5099a8..ab` change in (b). In (c), the cursor at the (0,0) corner makes InputGame enter **ScrollTerrain** and edge-scroll the view at `0x508720/22`. Frame 1 under the declared cursor therefore includes an edge scroll, and the (320,240) run shows none.
- **Input footprint**: 4,932 inherited bytes are read before they are written (4,657 in (a), 20 in (b), 255 in (c)):
  - 4,609 are produced by executed original code or come from the PE image.
  - 16 are the declared caller frame.
  - 8 are declared Windows inputs.
  - 44 are stale bench stack bytes, re-read by InitGameZone/InputGame epilogue code.
  - 2 are startup skip-derived values (MenuInit+0xe5 at `0x508f65/67`); they propagate nowhere.
  - 208 are untouched fill, covered by the fill runs above.
  - 45 are static stores of never-executed routines, analyzed next.

## Open dependencies

**Static stores of never-executed routines read by these phases.** Most are UI variables that WndProc or ResetMode/AffInit would write during window creation, which the accepted M1 startup does not execute. The ones that matter frame to frame are **AffGame's possible stores read again in frame 1**:

| Byte(s) | Read in frame 1 by | Writer sites |
|---|---|---|
| `0x4e2f78` (game state) | CalculGame+0xc/+0x3d/+0xb58 | AffGame+0x24f, AffGame+0x82f |
| `0x4e1b0e` (event in progress) | EvenementEnCours | EvenementAffiche+0x1a3 |
| `0x4e060c/0x4e0610` (help info) | InputGame+0x3039/+0x3064 | SetInfoAide |
| `0x507d54` (message box) | MessageBoxCalcul+0x9 | MessageBoxNext+0x1a |
| `0x50a9b4/b6` (mouse zone) | MouseZone | MouseTestZone |
| `0x4e1d18` | CalculGame+0xa91 | AffBatiments+0x1123… |

Whether AffGame takes those branches over the (b) state is a **graphics** question. AffGame is not executable on this bench because the sprite banks were never loaded. Until graphics answers it, frame 1 is the original program with AffGame not executed.
