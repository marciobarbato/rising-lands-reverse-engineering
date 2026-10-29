# M3 Step 0: static targets for P1–P5 and S1

Status: static extraction, no emulation. It implements Step 0 of [M3_PLAN §2](../../../docs/M3_PLAN.md). Nothing here claims that a branch runs. Labels follow M3_PLAN:
- **[B]** read from accepted state bytes or from an instruction encoding of the intact executable;
- **[S]** inferred. This covers a translation run over those bytes, a reachability or ordering claim, or a preference.

- Machine-readable output: [alvos-m3-monde01.json](alvos-m3-monde01.json), schema `rising-lands/monde01-m3-static-targets/1`.
- Generator: [extrair_alvos_m3.py](extrair_alvos_m3.py), run as `python3 -B pesquisas-paralelas/missoes/m3/extrair_alvos_m3.py`.
- Tests: [test_alvos_m3.py](../testes/test_alvos_m3.py), part of the missions suite (`python3 -B scripts/check.py --domain missions`).

## Inputs

**State source: the M2.2 frame-128 checkpoint.** This is `state_after.full_state` of phase `frame128` in `evidencias/captura-quadros128-monde01-exibicao-v2.json.xz`, the state S1 starts from (F0 = 129). The loader reproduces the recorded summary SHA-256 before using it.

**Cross-check: the accepted M1 MissionLoad state** (`captura-carga-missao-original-v2.json`, every block hash checked). Between M1 and frame 128 only three things change:
- the view;
- the mouse-zone table, which InitGameZone has not yet filled at M1;
- 11 object-grid cells (field growth).

Unit cells, the builder's bag, the cave cost, the stocks and the mines are identical.

**Code ranges:** the 44 cited code ranges are hash-anchored. The generator rehashes them from the intact `RISING.EXE` when it is present; status `verified`.

**Providers, imported rather than copied:**
- Core `incursao_core.caso_unidade` (EnginGetCase), `chamadas_quadro_core.caso_estrutura` (BatimentGetCase) and `caso_esta_descoberta`;
- Missions `influencia_missao.zona_influencia`;
- Economy `extracao.RecursosTerreno` (MineGetIndice/MineGetCapacite and TerrainEstChampi; both are cross-checked inside the run), loaded through `integracao.providers`.

## Targets (frame 128; view origin (0,0), 25×17 cells, screen 800×600, panel offset 0 [B])

**Screen mapping.** Cell (x,y) is at pixel (32x+16, 32y+16) [S], as the plan states. Byte evidence that supports this:
- InputGame `0x429800..0x42984a` computes cell = ((Y>>5)+vy)<<8 + (X>>5)+vx, but only when MouseZone returns 0 [B encoding].
- The tests check the inverse for every on-screen cell.

**Units:**

| Unit | Type | Cell | (x,y) | Pixel |
|---|---|---|---|---|
| 12 | 7 BATISSEUR | 4113 | (17,16) | (560,528) |
| 13 | 5 | 4110 | (14,16) | (464,528) |
| 14 | 5 | 4108 | (12,16) | (400,528) |
| 11 | 1 | 5387 | (11,21) | off-screen |
| 15 | 8 | 4877 | (13,19) | off-screen |

Unit cells are [B]; pixels are [S].

**Mouse zones [B]** (table `0x5099b4`, tested range 1..31):
- 1–8 are the 2-px screen edges.
- 10 is the minimap, (0,0)–(128,128). It hides the centre pixel of every cell with x−vx ≤ 3 and y−vy ≤ 3.
- 11 is the HUD panel, (0,544)–(800,600).
- 26–31 are dummies, (0,0,1,1).

Only InitGameZone, the market routines and AffIconeSousCurseur call MouseSetZone. InitGameZone mode 1 does not read the selection, so selecting the builder adds no zone [S].

**Action icons.** These are IconeGetZone `0x45da4e` sub-rectangles inside zone 11, not mouse zones [B]. Icon i covers x ∈ [31+60i, 89+60i] and y ∈ [548, 598]. Icons 8 and 9 scroll.

**CAVE icon.** Unit 12's bag holds four code-3 (structure) entries, types 1, 2, 3 and 4, with scroll 0 [B]. CAVE is therefore slot 2, rectangle (151,548)–(209,598), centre **(180,573)**.

The code-3 press does three things [B encoding]:
1. It tests TestRessource(cost).
2. It stores `0x4e05ae := 3` and `0x496207 := 3`.
3. It does this only with exactly one unit selected and with `0x5099ae` and `0x5099af` both set.

**Cave.** The type-3 structure is 5×5. It costs **food 10, stone 6, parts 0** [B]. CreerBatiment tests and charges the same table words.

The build offset is `0x202` [B]. The footprint is therefore centred on the clicked cell, the same footprint BatimentPosable tests [S].

**Stocks.** Player 0 has food 30 and stone 30 [B]. After paying for the cave this leaves 20/24, so **30 food and 26 stone** must still be gathered [S].

**Zone 0** is record (0,0)–(28,25): 754 cells [B]. The sanctuary's BatimentGetCase is (14,12), which is the colonists' cell, and it lies in zone 0.

**Proposed CAVE site [S]:** click cell **3093 = (21,12)** at pixel **(688,400)**.
- Footprint: (19,10)–(23,14).
- BatimentGetCase: (20,10), in zone 0.
- MouseZone at the pixel: 0.
- No objects in the footprint.
- Chebyshev distance 4 from the builder.

The basis is BatimentPosable `0x41fc40` translated without EnginOccupeCase. Over the map it gives 112 valid sites, 87 that depend on EnginOccupeCase and 3,897 invalid ones. 25 of the valid sites are on screen and free of objects; the JSON lists the first 12.

**Food.** 122 field cells match TerrainEstGc (objects `0x1d..0x34`) [B]:
- The nearest are (26,32), (27,32) and (28,32), 16 cells from unit 13.
- None is on screen at view (0,0).
- None is discovered for player 0.

The 16 sacks (object `0x42` parts, `0x43` food) are all off-screen, and a press on a sack is tag `0x12`, not tag 7. [S] View (10,16) shows unit 13 at (144,16) and field (26,32) at (528,528). Two minimap presses relate to it:
- a press at (46,49) with nothing selected sets that view;
- a press at (53,64) with troops selected orders a move to (26,32).

**Stone.** Two entries in the mine table `0x509954` [B]:

| Mine | Origin | Reserve | TerrainEstMine cells |
|---|---|---|---|
| 0 | (43,8) | 50 | (43,8), (44,8) |
| 1 | (6,59) | 200 | (6,59), (7,59) |

There are no stone sacks. Both mines are off-screen and undiscovered. [S] View (31,0) shows (43,8) at (400,272); a minimap press at (87,18) sets it, and a move press at (86,17) orders a move there.

## Order rules read from the bytes (encodings [B]; that they run, [S])

**Food and stone presses (InputGame `0x42b311`/`0x42b4b5`).** EnginTravailSelectionne `0x47248f` requires *every* selected live unit to have the right type:
- food: type 5 or 13;
- stone: type 7, which is only the builder;
- parts: type 6.

A press on a TerrainEstGc cell gives **tag 7** (`0x42b486`). A press on a mine cell gives **tag 6**. A press on a sack gives **tag `0x12`**.

**Undiscovered-cell gate (`0x4298d9`).** It applies when CaseEstDecouverte(cell) is 0 and `0x496208` is nonzero (it is 255 at frame 128). A press with troops selected then gives **tag 5 (move)** instead of a harvest or mine order. A probe must therefore reveal the field or mine first, then press again.

**Tag 8 / 19 (deposit).** These are produced only by the mode-9 table `0x42923c` [B]. Mode 9 needs mode 8, and the only store of 8 found is set while **Ctrl** is held (`0x429629`). A no-key S1 does not issue them.

**Minimap (`0x42bade`).**
- A left-button press alone (`0x5099ae`; no release needed) with nothing selected recentres the view at ((mx−25)/2, (my−17)/2), clamped to (39,47).
- The same press with troops selected issues tag 5 to MiniMapGetCase.
- A right-button press outside the HUD deselects all (`0x4295a1`).

**WndProc.** The messages set these flags:
- `0x201` → `0x5099ae`;
- `0x202` → `0x5099af`;
- `0x203` → `0x5099b0` in the playfield, else `0x5099ae`;
- `0x204` → `0x5099b1`;
- `0x205` → `0x5099b2`.

After AffGame, ProgIteration clears `0x5099ae` and `0x5099af` once `0x5099af` is set. Order presses need both flags in one InputGame pass. With DOWN at k+1 and UP at k+3 that pass is frame k+3 [S].

**Cave owner [B encoding].** CreerBatiment stores owner `0xc8` for type 3. The only store found that turns `0xc8` into a player is BatimentLogeEngin `0x41fa77`.

## M3_PLAN "Uncertain until it runs": what this narrows

| Question | Status | Static answer |
|---|---|---|
| CAVE icon sets `0x496207`=3; its rectangle | narrowed | slot 2, (151,548)–(209,598); the encoding stores 3 after TestRessource(10,6,0) |
| Cave cost and real targets | narrowed | 10 food, 6 stone, 0 parts; then 30 food and 26 stone to gather |
| Placement validity; zone 0 extent | zone settled; placement narrowed | zone (0,0)–(28,25); proposed site (21,12); 112 valid sites without EnginOccupeCase |
| Cave under construction passes record 0? | narrowed | owner is `0xc8` until a unit lodges (BatimentLogeEngin), so probably not [S] |
| Which unit mines stone; must colonists leave? | narrowed | only type 7 (builder 12); colonists (type 9) cannot take these orders |
| Tag-8 producer | narrowed | mode-9 table `0x42923c` entry 2, reached only through Ctrl mode 8 |
| TestRessource reads totals only | settled as an encoding | only `0x4e2ea8+32p` (+2 parts, +0xa food, +0x12 stone) |
| Victory before frame 9000 | open | the targets need exploration first; no timing follows statically |

## What remains for the probes

- **P1.** Press unit 12 at (560,528). The unit under the cursor is `ChercheIndiceEngin(cell)` (`0x429ae3`). The selection producers `0x42b9aa`/`0x42ba20` were not traced.
- **P3.** With only unit 12 selected:
  1. press (180,573), then (688,400);
  2. check packet tag 4 / type 3 / cell 3093;
  3. follow the walk, BatimentConstructible with the builder on its own cell (EnginOccupeCase), the charge to 20/24, owner `0xc8`, and the event that lodges a unit.
- **P4.** Choose a mechanism for units 13 and 14:
  - Selecting both needs a drag box, because shift is a key.
  - Unit 14 at (12,16) falls under the minimap at view (10,16).

  Then move (tag 5) until (26,32) is discovered, and press again for tag 7. Fields may change (11 cells already did between M1 and frame 128).
- **P5.**
  1. Select unit 12 alone.
  2. Minimap move press (86,17), or move it by playfield presses.
  3. Wait for discovery of (43,8).
  4. Deselect with a right-button press, recentre via the minimap (87,18), reselect, then press the mine for tag 6.
- **Credit path.** Whether harvested goods reach the `0x4e2ea8` totals without a Ctrl deposit order.
