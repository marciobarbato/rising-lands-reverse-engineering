# Terrain/minimap reset and structure minimap footprint

Stage 15 (coordinator reorder), 2026-10-28, base main `7b7b969`. Intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; ranges are end exclusive. No REA session was used; original assembly is the behavioral source. [manifesto.json](../../evidencias/reset-terreno-minimapa/manifesto.json) is produced by `extrair_reset_terreno_minimapa.py` and holds:
- 8 hashed intervals: `TerrainReset` 0x46b315..0x46b38f, `Random` 0x4704dc..0x470520, `MiniMapReset` 0x469f00..0x469f68, `memset` 0x48c3b0 and its fill leaf 0x48d890, `BatimentModifyMap` 0x419e97..0x419fc8, its shared epilogue 0x42399a, and `SetMiniMap` 0x46a388..0x46a70c;
- the 7-entry `SetMiniMap` jump table at 0x46a36c;
- the seven `BatimentModifyMap` CALL sites, each with its byte-checked DL load;
- the global map.

These are lower providers. Missions owns the `MissionLoad`/`MissionLoadName` reset order, the structure scan and readiness; economy owns `BatimentHabitable`.

## APIs

| API | Original | Inputs | Effect |
|---|---|---|---|
| `reset_terreno.resetar_terreno(mundo, minas, aleatorio)`; `MundoFisico.resetar_terreno(minas, aleatorio)` | `TerrainReset` 0x46b315 | world `objetos`, `donos_objetos`, `atributos` and four-owner `contagem_luz`/`luz_bordas`/`descoberto` (distinct writable 65,536-byte allocations); `minas` writable 80 bytes (0x509954); `aleatorio` writable 4-byte live `Random` state (0x497164) | Per cell 0..65535 in the original order: objects 0, aux = `Random()` & 3, attributes 0, then per owner 0..3 light count 0, light edges 0x1f, discovery 0x1f. Then zero the origin word of all 20 mine records (offset 4k); reserve words remain |
| `reset_terreno.resetar_minimapa(mundo)`; `MundoFisico.resetar_minimapa()` | `MiniMapReset` 0x469f00 | u16 minimap dimensions `tamanho_minimapa` (0x496fe0/0x496fe2, not the map size), w*h ≤ 65,536; three distinct writable 65,536-byte minimap layers | `memset` of the first w*h bytes: final = 2, then units = 0, then structures = 0; later bytes retained |
| `minimapa_estruturas.modificar_minimapa_estrutura(mundo, indice, ativo)`; `MundoFisico.modificar_minimapa_estrutura(indice, ativo)` | `BatimentModifyMap` 0x419e97 | AX index → u16, 0..999; DL → u8; structure type 0..21; camera 0..3; 128×128 minimap; for mode 6 an owner of 200 or below the 32-byte color table | For the type's W×H footprint (0x495d8c/+2, stride 52), rows in ascending y from origin +2, row-major: `SetMiniMap(owner +4, cell, 6 if DL else 7)`. A cell is skipped only when x or y reaches 256 (not the map size). No structure byte is written |

`Random` 0x4704dc is the Park–Miller step with Schrage's decomposition (unsigned `div` by 127,773, `imul` by 16,807 and 2,836, signed ≤ 0 → +0x7fffffff). It reuses the committed `candidatos_rota.aleatorio_caminhos`. EAX=0x28 is passed but ignored. Seed 0 maps to the fixed point 0x7fffffff. All protected checks, including allocation aliasing by identity or memoryview owner, precede the first store, and nothing can fail afterwards. With distinct protected allocations, filling each layer whole while drawing the 65,536 values in ascending cell order gives the same final state as the per-cell interleaving. The draw count and final seed are compared natively. Tiles, regions, minimap layers, units and structures stay unchanged by `TerrainReset`; it makes no other call.

## SetMiniMap modes 6 and 7

`SetMiniMap` dispatches through table 0x46a36c on `mode-1`; mode 0 and modes 8..255 do nothing. Stage 15 adds the two modes `BatimentModifyMap` reaches to the existing `VisaoMovimento.minimapa` pixel loop. Modes 1–5 are unchanged. For each pixel `p` of the cell's block:
- **Mode 6** (0x46a647):
  - the structure layer gets `PlayerGetColor(owner) + 2` (u8), where `PlayerGetColor` 0x46003b returns 0x1e for owner 200, otherwise byte 0x4e24dc[owner];
  - if the cell is lit for the local camera (`TerrainEstIllumine`), the final layer gets the unit layer if it is nonzero, otherwise the structure layer;
  - there is no discovery or owner-equals-camera test.
- **Mode 7** (0x46a69d): mode 5 with the two layers swapped. The structure layer is cleared. If the cell is discovered for the camera: when lit, the final layer gets the unit layer or the terrain color; when not lit, it gets `sombra[terrain color]`.

Callers, byte-checked:
- DL=1 → mode 6: `BatimentConstruction` 0x41d021, `BatimentRetireColon` 0x41e12c, `BatimentLogeEngin` 0x41fa88 (EDX preserved through `BatimentHabitable`), `SortieTroupe` 0x42114e, `CalculTrajectoire` 0x422cc3 and `MissionPlaceTerrain` 0x46c1b1 (`mov edx,1` at 0x46c1a9). Three of these first set owner +4 = 200.
- DL=0 → mode 7: `DemonteBatiment` 0x41f26b.

## Validation

Original-only first: [eight captures](../../relatorios/capturas-reset-terreno-original.json) ran before any Python body existed, so `translation_executed` is false.
- Fixtures: `TerrainReset` with seeds 0x12345678, 0 and 0xffffffff on 64×64, 256×256 and 16×16 maps; `MiniMapReset` at 128×128 and 64×32; `BatimentModifyMap` with DL 1 (type 2 at 0x0b0c, owner 0), DL 0 (type 5 at 0xfefd, owner 200, clipped to 2×3 cells) and DL 0x80 (type 0 at 0xff00, owner 3, one row). All inherited layers are deterministic random patterns.
- Together: 8 entries and 303 segments (295 TerrainReset-loop resumes), maximum 50,041 instructions per segment.
- All eight returned. They match the new Python bodies in every buffer hash, the mine bytes, the final seed, the `Random` draw count, the `memset` calls and the ordered `SetMiniMap` calls.

`TerrainReset`'s 65,536 iterations with one `Random` call each exceed one bounded segment. The bench therefore resumes at its cell-loop head 0x46b327 with every register, flag and stack byte preserved; no instruction, CALL or RET is replaced. It also keeps Stage 14's `SetMiniMap` entry and pixel-loop resume points.

Final `python3 -B ferramentas/validar_reset_terreno.py --emular` ([report](../../relatorios/reset-terreno-emulada.json)) passes 11 tests with zero failures, errors, skips, native faults or limits:
- 755 original entries, every one at its real return: 11 `TerrainReset`, 10 `MiniMapReset`, 734 `BatimentModifyMap`;
- 1,939 bounded segments, including 1,081 TerrainReset-loop and 103 pixel-loop resumes; maximum 86,186 instructions per segment.

Coverage:
- `Random` state edges 0, 1, 2, 127,772, 127,773, 0x7ffffffe, 0x7fffffff, 0x80000000, 0xfffffffe, 0xffffffff and 0x12345678, with 65,536 draws per entry asserted;
- minimap dimensions 128×128, 64×32, 1×1, 0×0, 0×128, 128×0, 256×256, 128×512, 65535×1 and 3×7, with exact `memset` arguments;
- all 22 structure types × six origins (16×16 corner/edge, 64×64 at 0x0b0c, 256×256 edges and corners clipped at 256) × DL 1/0/0x80, rotating owners 0–4/200, cameras and lit/discovered/hidden layers;
- a full owner (0–4, 31, 200) × camera × visibility × unit-layer × variant matrix;
- MONDE01's 64×64 map with the type-2 sanctuary at 0x0b0c in both variants.

Every comparison covers the whole unit/structure/group/object pools, all physical/vision/minimap layers, the 80-byte mine table, the 4-byte seed and the exact `SetMiniMap` call trace.

Local mode discovers 11 tests and skips 5 optional native tests. Because `minimapa` gained modes 6/7, the Stage 14 suite (modes 1–5, insertion and direct discovery) was rerun; see the handoff.

## Remaining limits

- The `MissionLoad`/`MissionLoadName` reset order, the MissionPlaceTerrain structure scan, `BatimentHabitable` and load readiness belong to their owners.
- `GameLoad`/`MissionAlloc`/`MissionReStart` also call these resets; their sequences are not reconstructed here.
- The other `BatimentModifyMap` callers' preceding stores are theirs.
- Structure type bytes ≥ 22, owners without a color for mode 6, non-128×128 minimaps for the structure path and minimap products above 65,536 bytes stay outside the protected domain.
- `Engin_ResetExperience` 0x441470 (MissionLoadName only) is core-owned but scheduled with Stage 18.
