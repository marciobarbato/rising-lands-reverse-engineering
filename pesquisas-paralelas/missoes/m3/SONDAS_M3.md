# M3 scripted-input harness and probes P1–P6, K1

Status: original-only native captures (no translation runs here). This implements the harness, the probes and the S1 draft of [M3_PLAN §2](../../../docs/M3_PLAN.md). Labels follow M3_PLAN:
- **[B]** native run of the intact executable, or its instruction bytes;
- **[S]** inferred.

Every probe below was run twice from the same input file, and both runs gave equal records (`sondas/<P>/replay.json`).

## Harness

| Item | Where |
|---|---|
| Frame-128 start snapshot | [checkpoint_quadro128.py](checkpoint_quadro128.py) |
| Scripted-input oracle | [entrada_roteirizada.py](entrada_roteirizada.py) |
| Probe inputs | [sondas_m3.py](sondas_m3.py) → [entradas/](entradas) |
| Packaging and reports | [relatorio_sondas.py](relatorio_sondas.py) → `sondas/<P>/` |
| Unit tests | [test_entrada_roteirizada.py](../testes/test_entrada_roteirizada.py) |

**Start state.** `checkpoint_quadro128.py` rebuilds the display reference to frame 128 and checks it before saving the snapshot (`segmentos_quadros_missao.salvar`). The frame-1 and frame-128 state summaries must equal the accepted M2.2 capture. The display clock is extended by its own rule to 1,000,000 answers. The snapshot (about 45 MB) stays in `.local/`.

**Input file**, schema `rising-lands/monde01-scripted-input/1`. Frame k may list:
- the `GetCursorPos` answer, which holds until another frame declares one (initially (0,0), the no-input answer);
- the ordered messages `[msg, wParam, lParam]`, only 0x100, 0x101 and 0x200..0x205;
- the `GetAsyncKeyState` table by vkey (i16), for that frame only.

**Frame k** is the phase pair `between_frames{k}` + `frame{k}`.
- The messages are queued when `between_frames{k}` starts. `_WinMain@16` drains them one per loop iteration: `PeekMessageA`(PM_NOREMOVE) 0x4601d1, `GetMessageA`, `TranslateMessage`, `DispatchMessageA`.
- Then ProgIteration's single `GetCursorPos` (site 0x47504b) takes frame k's cursor.
- `GetAsyncKeyState` is polled from InputGame, about 12 polls per frame, for vkeys 0x0d, 0x10, 0x11, 0x12, 0x1b, 0x20, 0x25–0x28, 0x2e, 0x58.

**DispatchMessageA → WndProc 0x4181a1, natively.**
- The declared import returns, then `RegistroComDespacho.invocar` rewrites its frame into `WndProc(hwnd, msg, wParam, lParam)` with the same return address. WndProc's `RET 0x10` leaves ESP where `DispatchMessageA`'s `RET 4` would.
- The harness writes no WndProc flag. The flag bytes 0x5099a8..0x5099b2 are recorded at the return to 0x460203.
- The declared values:
  - `hwnd` is the word at 0x4e27e8 (0, because AppWindowInit never runs);
  - `MSG.time` is 0 and `MSG.pt` is the frame's cursor;
  - `TranslateMessage` answers 0 and posts nothing.

**Checks of the harness itself** [B]:
- Empty input over frames 129–140 matches the no-input coverage run (Core `runs/core/coverage-9200` 7193999) frame by frame: whole-state SHA-256, DGROUP SHA-256, all three RNGs, permutation cursor and view origin.
- A run resumed from one of its own mid-run snapshots (P1, frame 136) reproduces frames 137–150 exactly.

**Recorded outputs** (M3_PLAN §2 items 1–6):

| File | Content |
|---|---|
| `quadros.jsonl` | per-frame summary, including the objective trace (item 4) |
| `entradas.jsonl` | input log |
| `comandos.jsonl` | `SetPlayerOrdre` calls, and `ProcessInputGame` entries with tag ≠ 0 plus their jump target |
| `fronteiras.jsonl` | the `PlaySnd_*`/`MCICD_*` calls |
| `.local` snapshots | taken at input-listed frames, at order frames, at the first CreerBatiment/AL = 1/`MenuInit(0x13)`, every 1,000 frames and at the end |

**Run time.** About 0.5 s/frame per job on the Mac mini with 4–5 jobs. P4 and P5 ran beside 6–8 other jobs at about 0.55 s/frame.

## Probes

Frames are absolute: F0 = 129. "Beyond no-input" counts routines entered here that the 9,200-frame no-input run never enters.

| Probe | Input | Orders (`SetPlayerOrdre` tag, words) | Beyond no-input | Run time (2 runs) |
|---|---|---|---|---|
| P1 | click unit 12 at (560,528) | 133: tag 1, 4113, 4113 | 41 | 310 s, 310 s |
| P2 | P1 + click (624,432) | + 143: tag 5, 3347 | 53 | 370 s, 353 s |
| P3 | P1 + CAVE icon (180,573) + site (688,400) | 153: tag 4, 3, 3093 | 86 | about 1,560 s each |
| P4 | unit 13, minimap move, recentre, field (27,32) | 141–143: tag 5, 8218; 443: tag 7, 8219 | 63 | 1,638 s, 1,651 s |
| P5 | builder, minimap move, recentre, mine (43,8) | 141–143: tag 5, 2091; 593: tag 6, 2091 | 65 | 1,581 s, 1,553 s |
| P6 | P3 + sanctuary select, double click, colonist, cave | 2018: tag 2; 2030: tag 33; 2063: tag 1, 3598; 2073: tag 16, 3, 1 | see report | see `replay.json` |
| K1 | cursor at the centre; arrows, digit 1, Space, X | 200: tag 12, 1 | 6 | 270 s, 268 s |

### Findings

**Selection (P1)** [B].
- WM_MOUSEMOVE at 130, DOWN at 131, UP at 133. InputGame calls `SetPlayerOrdre` at frame 133 from 0x42ba20 (return 0x42ba25), as the plan expected.
- Packet `01 00 1110 1110`. `ProcessInputGame` jumps to 0x45ee46 → `DeSelectionGroupe`, `SelectionEngin`. Selection 0x508728 becomes count 1, entry 12.
- The flags confirm the timing: 0x5099ae is set from 131, and both flags are set only in frame 133.

**Move (P2)** [B]. Tag 5 → `SetDeplaceEnginSelect` (ProcessInputGame+0x21d). Unit 12 reaches (19,13) at frame 178, then goes to state 7.

**CAVE order (P3)** [B]. This settles M3_PLAN rows 2–4 for this site:
- The icon press stores `0x496207 = 3` at frame 143, with no packet. The rectangle and slot are those of M3_ALVOS.
- The site press gives tag 4 (word2 = 3, word4 = 3093) at frame 153 → `SetConstruitBatimentSelect`, `SetEnginConstruitBatiment`. Unit 12 gets `+2` = 11, `+0xb2` = 3093, `+0xbe` = 3.
- The builder walks. At frame 220: `BatimentConstructible`, `CreerBatiment`, `EnleveMatiere`, `PlaceBatiment`.
  - Food/stone go 30/30 → **20/24**.
  - Structure 1 is created: owner **0xc8**, type 3, origin 2579 = (19,10), state byte +5 = 2.
- Construction completes at **frame 1812** (+5 = 5, `BatimentModifyMap`). The builder is idle at 1813.
- The owner stays 0xc8 and the marks 0x4e1d84..0x4e1d91 stay 0 through frame 3129. A built cave alone does not pass record 0.
- The cave's structure-grid cells (`[0x4e0f38]`, bit 15) are only (19..21, 10..11). The builder stands on (21,12).

**Food (P4) and stone (P5)** [B].
- These confirm the Step-0 order rules:
  - On an undiscovered target, a minimap press with troops selected issues tag 5. It does so on each frame the button is held (141, 142, 143).
  - A right press deselects. A minimap press with nothing selected recentres the view.
  - Tag 7 (field) → `SetRecolteEnginSelect`, `SetDepotEnginSelect`, `CalculWorkEngin`, then `TerrainRecolte` at 710.
  - Tag 6 (mine) → `SetMineEnginSelect`, `SetDepotEnginSelect`, `MineSetWork`, `MineRecolte`, then `MineEndWork` at 760.
- Both units then go idle. With no cave, the player totals at 0x4e2ea8 stay 30/30 through frame 3129.

**Lodging (P6)** [B]. This settles the "lodging event" row:
- Static gate [B encoding]: `EnginSelectPeutEntrer 0x472b6c` lets a selection enter a structure owned by 0xc8 only if every selected live unit is **type 9** (a colonist), and the structure type is not 9 (0x472be5..0x472c50).
  - A type-5 unit pressed on the cave gets no order (frame 2023, P6 development).
  - The builder pressed on the player's own sanctuary gets tag 16 and is lodged there (`EnginResetType`), so S1 must not do that.
- Colonists leave the sanctuary by a **double click** on the selected sanctuary:
  - The input is WM_LBUTTONDBLCLK; WndProc sets 0x5099b0 in the playfield.
  - InputGame 0x42b23b..0x42b259 issues **tag 33** (0x21) → `BatimentRetireColon`, `BatimentEnleveUnColon`.
  - Colonist 3 (type 9) walks out to (14,14).
- Selecting it (tag 1) and pressing a cave grid cell gives **tag 16, word2 = 3, word4 = 1** → `SetEnginSelectRentreBatiment`, `CalculEntreBatiment` (path search). Then at frame 2178:
  - `BatimentLogeEngin` and `BatimentHabitable`;
  - `InitBatimentPlayer` and `GetRessourceStock`;
  - the cave owner goes 0xc8 → **0**;
  - mark **0x4e1d88 = 1** (record 0).
- The sanctuary icons are tag 17 recruitment, not colonist release:
  - slot 0 → type 5, 4 food;
  - slot 1 → type 6, 6 food;
  - slot 2 → type 7.
  - The recruit leaves as its new type (`EnginSetType` at frame 2277).

**Keys (K1)** [B].
- With the cursor off the edges, held arrows scroll the view one cell per frame (view x 1..19, then y).
- WM_KEYDOWN `1` (WndProc 0x418313 stores 0x49a05a) leads InputGame to issue tag 12 → `RestaureSelectionGroupe`.
- X enters `GoLastAttaque`.
- With the cursor at (0,0), edge scroll cancels the arrows. The first K1 attempt showed this, and it was rerun.

## M3_PLAN "uncertain until it runs": status

| Question | Status |
|---|---|
| CAVE icon sets 0x496207 = 3; its rectangle | **settled [B]** (P3, frame 143) |
| Cave cost and targets | **settled [B]**: 10 food / 6 stone are charged at CreerBatiment; 30 food and 26 stone remain to gather |
| Placement validity | **settled for (21,12) [B]**; construction takes 1,592 frames from CreerBatiment |
| A cave under construction or built passes record 0 | **settled [B]: no**; it passes once a colonist lodges (owner 0xc8 → 0) |
| Which unit mines stone; colonists | **settled [B]**: the builder mines (tag 6); a colonist must leave the sanctuary (double click) and enter the cave |
| Tag-8 producer | unchanged (Ctrl mode 8, not used) |
| Gathered goods reaching 0x4e2ea8 | see the S1 draft below |
| Victory before frame 9000 | see the S1 draft below |
