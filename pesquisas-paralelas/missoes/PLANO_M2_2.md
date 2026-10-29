# M2.2 / M2.3 preparation: frame sequence, events and boundaries (MONDE01)

**Status:** M2.2 is captured. The original-only 128-frame capture and its comparison policy are committed evidence (HANDOFF Stage20). The sections below are the preparation record. The multi-frame runs they mention wrote under `.local/` and are not evidence. Addresses refer to the intact `RISING.EXE` (SHA-256 `6c556520…43fb`). The MONDE01 values come from the `-v2` reference state.

## 1. Tooling (committed)

- **N frames.** `BancadaExibicaoOriginal.executar_quadros(n)` yields load_tail, then `between_frames(k)` and `frame(k)` for k = 1..n. Frame 1 keeps the committed phase names. Frame k ≥ 2 is `between_frames{k}` / `frame{k}`, and `eh_fase_quadro` replaces the fixed phase tuple.
- **Policy over N frames.** `politica_comparacao_quadros.py --quadros N` makes two native passes:
  1. find the bytes that change in each phase;
  2. rerun with read/write hooks on exactly those bytes and the surface region, tracked by display roots that end exactly when their RET lands on the return address with ESP = entry+4.

  The rule is unchanged: **a byte is masked only when every writer and every reader is display or backend**. It is applied per frame window (load_tail joins window 1) and cumulatively; only the cumulative mask may exclude bytes from a whole-run comparison. Pass 2 must reproduce pass 1's phase states.

  Validation: with N=1 it **reproduces the committed M2.1 policy exactly** (same mask, 78,093 display-only and 776 logic bytes). The N=3 trial is reported in §4.
- **Event probe.** `varrer_eventos_quadros.py --quadros N` records per phase the boundaries reached, routines entered for the first time, DirectDraw calls, clock answers, both RNG states, the counters, the game state, the UpdateChamp row, the event flag and the message indices.

## 2. Static analysis

**Frame counter.** ProgIteration increments `[0x508f7c]` before each CalculGame. Its even and third-frame companions are `0x508f80` and `0x508f84`. The load-state frame ("frame 0", phase load_tail) resets all three to 0 at `0x42d2be`, so **frame k runs with counter k**. Every periodic gate below tests this counter.

### Field growth

- `SetUpdateChamp 0x475328` sets `[0x509952]=1` when `counter mod [0x4973ea]` (=128) is 0.
- `UpdateChamp 0x478806` runs while that flag is set or the row `[0x4973e8]` is > 1. It processes **one row per frame** (x = 1..254). For object bytes `0x1c..0x34` it draws `Random 0x4704dc`, with `Random(5)` for `0x1c` and `Random(10)` tests for `0x1d..0x34`, and may call `ScanNouvellePatate`. After row 255 it clears the flag and resets the row to 1.

So **field processing starts in frame 0, not at counter 128**. The load-state frame calls SetUpdateChamp with counter 0, and the reference shows the flag set and the row going 1 → 2 → 3 over load_tail and frame 1. Row r is processed in frame r−1.

MONDE01's first candidate objects are in **row 32 → frame 31**. There are 124 candidate cells in rows 32–52, covering frames 31–51; from frame 31 on, the Random stream depends on these cells. Counter 128 has no visible effect, because the flag is already set. The first sweep ends after row 255 (frame 254). Counter 256 restarts it, so the second sweep reaches the candidate rows in frames 287–307.

### First scripted raid

The only scripted attack source in MONDE01 is the monster-entry table that `LoadEntrerMonstre` fills: `0x50a9bc`, with the count at `0x50a9ce` and 12-byte records at `0x50a9d0`. The attack table `0x50d5b4` has count 0, and the AI players 1–3 have no units.

`AvanceMonstre 0x47b283` runs every frame for player 4:
- On its first call (flag `0x50a9cc` = 0, frame 0) it stamps every record's last-time field +8 with the counter, which is 0.
- Afterwards record r fires when `counter − last ≥ period` (u16+4, the loaded value ×30). It then advances the entry bit in the +2 mask, restamps last, and calls `ConstruitGroupeMonstre 0x47a81d (AX = word0, DL = bit)`.

MONDE01 has five records. Two are active:

| Record | Entry word0 | Mask | Period | Fires at frames | Group |
|---|---|---|---|---|---|
| 0 | `0x3f3f` | bit 0 | 9000 | 9000, 18000, … | 0 (MONSTRE.INI `GROUPE00=0`) |
| 1 | `0x3f00` | bit 0 | 10800 | 10800, 21600, … | 0 |

Records 2–4 have period 0 and never fire. **The first raid is in frame 9000.**

### Other periodic gates before it

| Routine | Condition | Frames | Note |
|---|---|---|---|
| PlayerAttaqueCalculSympa | counter mod 2000 | 0, 2000, 4000, … | MAJSympathie |
| CalculBatimentNextEtape | counter mod `[0x495c02]`=1000 | 0, 1000, … | global structure step |
| BatimentNextEtape | counter mod `[0x495bfc]`=50 | 50, 100, … | plus per-structure (counter+index)&0x1f |
| EnginNextEtape | (counter+unit index)&0x1f | every 32 frames per unit | |
| InitNova | counter mod 100 | — | Nova construction only |
| CalculCompteurMarche | counter mod `[0x496f90]`=100 | 100, 200, … | may call MessageBoxSet |
| CalculCompteurProposition | counter mod 100 and mod 800 | 100…, 800… | alliance propositions; may call MessageBoxSet |
| GetMeteo | counter mod 900 (0x384), plus a 100-frame `Random(5)==3` roll | — | weather byte `0x496d2c`, rain via NextGouttes; caller not resolved statically |
| NextAnimTerrain / NextAnimVeget | counter parity / mod 4 | every frame | over the 25×17 viewport |

**Not expected without input:**
- Victory: TestFinDeMission needs a type-3 cave and 50 food / 50 stone.
- FLI events: EvenementInit is reached only from MessageBoxRun, which InputGame calls on interaction, and from MarcheChangePlayerContact.
- LezardRun: no direct caller, and its state `0x50b17c` is 3.

## 3. Proposed declared frame sequence

| Milestone | Frames | Per-frame stop points | Checkpoints (full snapshot plus mask re-derivation) | Purpose |
|---|---|---|---|---|
| **M2.2** | load_tail + 128 frames | every frame: the next CalculGame entry and the frame's RET at `0x475063` | 1, 31, 32, 50, 51, 52, 64, 100, 101, 128 | field-row Random draws (31–51), first structure step at 50, the 32-frame unit cycles, the market/proposition/Nova gates at 100, counter 128 |
| **M2.3a** | 129 … 8,999 | per-frame state hashes; full snapshots every 100 frames | 254/255 (end of sweep), 256, 287–307, 800, 900, 1000, 2000, 2700, 4000, 6000, 8000, 8999 | long-run drift, weather at 900k, structure step at 1000k, sympathy at 2000k |
| **M2.3b (first raid)** | 9,000 … 9,100, and 10,800 | every frame | 9000 (ConstruitGroupeMonstre), 9001–9100 (the group's AI and movement), 10800 | the monster group, its AI kernels and its first contact |

**Cost.**
- Native speed is about 1 s per frame, mostly AffGame and the window loop. M2.2 takes minutes; M2.3a about 2.5 h native per pass.
- A per-frame policy over thousands of frames is too expensive with Python hooks. I propose:
  - full two-pass policy runs per checkpoint window;
  - plus one whole-run pass with hooks only on the cumulative mask ranges and the surfaces, which proves no logic access ever reaches a masked byte. The terrain cache is read heavily by AffBloc, so this costs about +0.5 s per frame.
- The display-clock named input must be extended beyond its current 4,096 values for M2.3: one answer per frame from CalculFrame.

## 4. Empirical probes (`.local/`, not evidence)

### N=3 policy trial (`.local/m2r5-policy-n3.json`)

The trial passed: all 7 phases reproduce, every changed byte has an observed writer, and no logic-context access reaches a surface.

| Measure | Value |
|---|---|
| Bytes changed | 109,711 |
| Cumulative mask | 108,893 display-only, 818 game logic |
| Window 1 | 78,094 display-only, 818 logic |
| Windows 2 and 3 | ≈13–17k display-only, 611 logic |

Window 2 mostly contains terrain-cache bytes rewritten when the view scrolls.

**Mixed byte.** `0x4e05a2`, the HUD refresh flag, first changes in between_frames2:
- **Writers:** AffGame `+0x7f2/+0x81c` and CalculMatiere `+0x12c`.
- **Readers:** AffGame and AffZoneIconeAction only.

It has a logic writer, so it stays compared. From frame 2 on, **the composition must model AffGame's store to it**. Nothing like it occurs in frame 1.

The other logic bytes that first change after frame 1 are NextGouttes rain-drop slots (`0x4e1da0..0x4e2070`).

### 130-frame event probe (`.local/m2r5-eventos-130.json`, 187 s)

**Boundaries.** Every frame reaches `MCICD_Play@CalculGame+0xac5`; every between-frames phase reaches `PlaySnd_Manage` and `MCICD_Manage`. In 130 frames there is no `PlaySnd_PostSound`, `AffText`, `TextGetMessage` or message box, and the event flag stays 0. The game state stays 0x12 throughout.

**First new routines:**
- frame 17, `EnginTrouveCibleScan`: a unit's target scan on its 32-frame step;
- frame 45, `ScanNouvellePatate`: the first field event in the UpdateChamp sweep. Frame k processes row k+1, and row 32 is reached in frame 31.

**Shared cursor `0x4e1d18`.** It advances by 1 every frame through the CD branch, plus jumps every 4 frames through NextAnimVeget: 5, 6, 7, 14, 15, ….

**Clock and display.** Each between-frames phase reads one display tick (CalculFrame) and makes 3–5 DirectDraw calls.

The market and proposition gates at frame 100 produced no message box with inactive AI players.

### v3 probe

The first attempt stopped at the declared 200,000-segment budget inside MenuInit → LoadPie, because the menu pictures make that many FileRead resumptions. The log is in `.local/`. The v3 scenario now declares a 3,000,000-segment budget and a 1,000,000-binding budget, the cap of Core's bench. A second attempt that requested 3,000,000 bindings was refused by that cap; its log is in `.local/`. **v3 rerun** (`.local/m2r5-eventos-v3-2.json`, 2 frames, 111 s): startup, MissionLoad, load_tail and frames 1–2 complete with LoadPie executed natively over the CRT fseek fixture.
- The LoadPie boundaries disappear; only `MCICD_*` and `PlaySnd_Manage` remain.
- In every phase the RNG, the CRT seed, the shared cursor `0x4e1d18`, the counters and the DirectDraw call counts **equal the `-v2` probe**.
- This is a probe, not a state comparison. A v3 recapture plus a byte comparison against `-v2` waits for M2.1 acceptance and for Core's `ftell`.

## 5. Expected boundaries per frame, and new boundaries that need an owner

**Every frame:**
- `MCICD_Play` from CalculGame's CD branch, because `[0x4e2f28]`=0 (no CD track playing).
- `PlaySnd_Manage` and `MCICD_Manage` between frames.
- AffGame executes natively.

**On events:**
- `PlaySnd_PostSound`: about 25 logic callers (unit/structure steps, damage, fatigue, construction).
- `AffText`/`TextGetMessage`: message boxes and HUD text, while text stays a boundary.

**New boundaries and decisions that need an owner:**

1. **CRT `ftell` 0x48cf11 (Core).** InitTextLangue → LoadFonteExterieur → FileSize calls it. It blocks executing text in v3 (fgets alone is not enough). LoadPie needs only `fseek`, which is inventoried, and is ready in the prepared `exibicao_v3` scenario.
2. **CD audio availability (Audio + coordinator).** While `[0x4e2f28]`=0, CalculGame takes the CD branch **every frame**: it reads the permutation table `0x4e1c18[0x4e1d18]`, **advances the shared cursor `0x4e1d18`**, and calls MCICD_Play. On a machine with CD audio playing, `[0x4e2f28]` would be 1 and the cursor would not advance. Game logic shares that cursor (NextAnimVeget, NextAnimTerrain), so this declared input (MCICD_Init never executed, meaning no CD audio) changes logic state over many frames. It must be declared explicitly, and an owner must say whether to model the CD-playing alternative.
3. **Sound library (Audio).** `PlaySnd_PostSound` and the HandlSnd queue stay output boundaries. Audio should confirm that no logic routine reads sound-library state; the N-frame policy will flag any such read.
4. **Display clock (Missions/Graphics).** CalculFrame's GetTickCount answers feed the fps counter only (the G sensitivity run, frame 1). Re-check over N frames.
5. **Monster group spawn at frame 9000 (AI/runtime, Combat).** ConstruitGroupeMonstre, CreerEngin and the iag*/iaSolver kernels for player 4's group. No new Windows boundary is expected, but sound posts are likely.
6. **FLI/message events (Missions/Graphics).** Only if a MessageBoxSet fires (market or proposition gates at 100k/800k): MessageBoxAffiche, AffText, and possibly EvenementInit/DisplayFliPict, which read FLI frames through FileRead.

## 6. v3 (text and pictures): plan, nothing committed as reference

- **Ready in code** (`exibicao_v3`): CRT `fseek`/`fgets` fixtures with Core's ABI, bound in the v3 bench, and LoadPie executed natively.
- **Missing:** CRT `ftell` (Core) for text. Once it is on main, add `ftell` to the fixture, remove the text routines from the v3 boundary set, and run the v3 trial.
- **After M2.1 acceptance:**
  1. Capture v3 MissionLoad (new entry and capture) and frames 0/1 as new files.
  2. Run the backend-style equivalence report against `-v2`. Expected: LoadPie writes surfaces and, possibly, palette tables; text writes the text-table allocations and font banks; game-logic bytes should not change.
  3. Re-derive the policy.
