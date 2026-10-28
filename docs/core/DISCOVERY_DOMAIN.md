# Discovery and light beyond vision sum 8

Stage 14, 2026-10-28, base main `8a499a9` merged with `f18b5a0` (economy) and `dbff651` (missions 9a). Intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; the Ghidra function list used for the writer scan comes from the normalized analysis copy `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`, while every byte and native run comes from the intact oracle. Ranges are end exclusive. No REA session was used; original assembly is the only behavioral source.

## Published domain

| Symbol | Value | Canonical module | Re-exported by | Meaning |
|---|---:|---|---|---|
| `SOMA_VISAO_MAXIMA_INSERCAO` | 11 | `insercao_unidades` | `colocacao_missao`, `colocacao_saida` | Inclusive maximum normal-owner vision sum u8 `+0xbb` + u8 `+0xf5` for which `PlaceEngin` 0x456fa6 and `SetSortEngin` 0x445fbc execute discovery, light and minimap |
| `RAIO_DESCOBERTA_MAXIMO_VALIDADO` | 23 | `visao_movimento` | `insercao_unidades`, `colocacao_missao`, `colocacao_saida` | Validated DX argument of a direct `DecouvreTerrain` 0x476851 call (the body adds one more cell) |
| `RAIO_LUZ_MAXIMO_VALIDADO` | 20 | `visao_movimento` | same | Validated DX argument of a direct `IllumineTerrain` 0x476cb3 call |

The radius symbols cover the callers whose radius domain this stage inventoried: PlaceEngin, SetSortEngin and BatimentHabitable. Of the other 46 listed call sites, two are the per-cell calls inside the bodies themselves. The remainder (BatimentDecouvre/BatimentIllumine's direct per-cell calls, AvanceEngin, EnginRetire/EnginRetireType, EnginNextEtape, CalculWorkEngin, ProjectileSet, BallonPrepareArrivee, EnginLogeEngin, EnginSetLevelExperience, PlaceEnginTerrain) carry no radius claim. Consumers key their tests to these attributes. Missions reads `getattr(colocacao_missao, 'SOMA_VISAO_MAXIMA_INSERCAO', 8)` and economy reads `getattr(insercao_unidades, ...)`; both resolve to 11. A normal-owner sum above 11 still raises `DependenciaColocacaoMissao` (checkpoint 0x457019) or `DependenciaColocacaoSaida` (0x446146), both with `.endereco` 0x476851, after collision and the +72 store and before any discovery, light or minimap effect. Owners 4 and 200 never reach discovery at any sum. The Python primitives `descobrir_area`/`iluminar_area` do not guard radius themselves (AvanceEngin also uses them); a direct caller gates on the two radius symbols and on owners 0..3.

## Original-byte inventory

[manifesto.json](../../evidencias/descoberta-terreno/manifesto.json) is produced by `extrair_descoberta_terreno.py` and holds 16 intact intervals with hashes:
- `DecouvreCase` 0x47670a, `DecouvreTerrain` 0x476851..0x47693a, `IllumineCase` 0x476968..0x476adc, `IllumineTerrain` 0x476cb3..0x476e82;
- `Distance` 0x47954c..0x479555 and `SetMiniMap` 0x46a388..0x46a70c, plus `SetMiniMap`'s leaf queries `TerrainGetColor`, `PlayerGetColor`, `TerrainEstDecouvert` and `TerrainEstIllumine`;
- the vision-sum fragments of both insertion callers;
- the `BatimentHabitable` radius fragment, plus `BatimentGetCase`'s register-preservation prologue, tail and shared epilogue.

The manifest also lists all 52 E8 call sites of the four discovery/light bodies.

Arithmetic, as executed:
- Both insertion callers clear AH, load u8 BB, add 2 in 32 bits, add u8 F5 and pass DX. Light reloads both bytes and passes u16 BB+F5. There is no 8-bit wrap.
- `DecouvreTerrain` increments the 32-bit radius. Its threshold is `r*r + (u16 r >= 2)`, compared as u16 against `Distance`'s `imul eax,eax; imul edx,edx; add eax,edx` of the zero-extended u16 offsets. Rows and columns are signed 16-bit, clipped against the u16 map dimensions at 0x497168/0x49716a.
- `IllumineTerrain` uses the radius unchanged. Its second sweep only tests luz_bordas bit 0x10 and discards the result.
- The existing `VisaoMovimento.circulo` already masks the same widths, so no new arithmetic was needed.

Reachable insertion sums:
- The only stores covering unit `+0xbb` are `LoadEngin` 0x46adeb and `EnginSetType` 0x457d55, which copy the type table's low vision byte (0x4965d8 = table+0x2a), plus `EnginResetType` 0x457241 and `EnginSetTypeCaract` 0x457908, which store a literal 5.
- `+0xf5` is stored only with 0 (`LoadEngin` 0x46ae46, `CreerEngin` 0x457f7b) or 1 (`EnginSetNewExperience` 0x44fa98, `EnginSetLevelExperience` 0x44fbfa/0x44fc9d).
- The 26 shipped `RAYON` values in `RISING.INI` are {5,7,8,10}. Every unit `ExisteEngin` admits receives BB from the type table and F5=0 during load. The 38 ETA maps therefore place sums {5,7,8,10}, and the reachable maximum is 10+1 = 11.
- The scan covers displacement stores inside the 1,339 listed bodies. Block restores such as `GameLoad` (second wave) are outside it; they restore values written by these same stores.

Structure caller (`BatimentHabitable` 0x41cc70, reached from the MissionPlaceTerrain structure scan):
- Jump table 0x41cc18 yields R = 20 (type 0), 10 (type 2), 5 (type 4), 7 (types 10/11), 4 (types 19/21) and 8 for types 1, 3, 5–8, 13–16, 18 and 20.
- Types 9/12/17 leave at 0x41ccae..0x41ccc3 before any call. Type bytes above 21 reach the call with the caller's inherited EDI; that stays the caller's named boundary.
- `BatimentGetCase` 0x41aee2 pushes and pops EDX, so the calls are `DecouvreTerrain(cell, (R+3)&0xffff, BL=structure +4)` at 0x41cdb9, then `IllumineTerrain(cell, R, owner)` at 0x41cdca. The maxima are 23 and 20; MONDE01's type-2 structure needs 13/10.
- An owner byte of 4 or more indexes past the four grid pointers (0x507d78+owner*4 aliases the light pointers), so it is outside the primitive domain.
- Economy owns `BatimentHabitable` and its gate.

## Implementation

`insercao_unidades._aplicar_insercao` now compares the sum with `SOMA_VISAO_MAXIMA_INSERCAO` instead of the literal 8. Mutation and call order are unchanged:
1. collision;
2. +72=1;
3. reload of the current cell;
4. for normal owners only, the sum guard, then discovery (sum+2) and light (sum, reloaded);
5. minimap mode 4 for every owner.

Owners 4/200 skip the guard and step 4. A failing guard leaves collision and +72 in place and performs no vision or minimap work. No new discovery arithmetic was written. Native per-cell traces confirm the existing bodies' row-major `DecouvreCase`/`IllumineCase` order and every nested `SetMiniMap` mode.

## Validation

Original-only first: [seven captures](../../relatorios/capturas-descoberta-terreno-original.json) ran before the Python limit changed, so `translation_executed` is false.
- Three were `PlaceEngin` sums 9/10/11, two were `SetSortEngin` sums 11, one a direct `DecouvreTerrain` radius 13 and one a direct `IllumineTerrain` radius 11.
- Fixtures covered 16×16, 64×64, 128×64 and 256×256 maps, a corner and an edge, owners 0–3, cameras 0–3, and fresh, mixed and saturated light/discovery layers.
- Together: 7 entries, 80 bounded segments, 73 preserved minimap-entry resumptions, maximum 64,837 instructions per segment.
- Every capture returned at the real return address. All seven match the Python bodies in whole buffers, the full effect trace and the per-cell trace hash.

The first full native run ([failure record](../../relatorios/descoberta-terreno-emulada-initial.json)) is not a pass:
- The direct-entry interval guard omitted `SetMiniMap`'s leaf queries, so the first fresh light case stopped at `TerrainGetColor` 0x4765f4.
- All other new tests in that run passed. The run was stopped during the regressions.
- Declaring the four exported leaf bodies fixed it; no reconstructed behavior changed.

A separate [diagnostic](../../relatorios/descoberta-terreno-1x1-cap.json) records that one 128×128 `SetMiniMap` block on a 1×1 map exceeds the one-second segment budget when only `SetMiniMap` entries may resume. Two attempts are recorded: 853,170 instructions at 0x46a627 and 838,176 at 0x46a526. The discovery bench therefore also resumes at the pixel-loop head 0x46a623, with every register, flag and stack byte preserved. No instruction, CALL or RET is replaced, and each resume counts as its own bounded segment.

Final `python3 -B ferramentas/validar_descoberta_terreno.py --emular` ([report](../../relatorios/descoberta-terreno-emulada.json)) passes 32 tests with zero failures, errors and skips, over 10,503 bounded segments. Discovery bench:
- 1,433 original entries: 267 `PlaceEngin`, 266 `SetSortEngin`, 480 direct `DecouvreTerrain` (radii 0..23) and 420 direct `IllumineTerrain` (radii 0..20).
- 1,423 returns and 10 declared pre-discovery stops (5 at 0x457019, 5 at 0x446146), each matching a Python dependency exception with partial state.
- 5,527 segments, including 1,310 minimap-entry and 2,784 pixel-loop-head resumptions. Maximum segment: 164,737 instructions.

Coverage of the discovery bench:
- every new sum 9..11, in several BB/F5 compositions, for both callers × owners 0–3 × cameras 0–3;
- maps 1×1, 1×256, 256×1, 3×5, 16×16, 32×16, 64×64, 128×64 and 256×256 at all corners, edge midpoints and centers;
- every direct radius at five positions, including three 256×256 corners/center;
- the regression of sums 0..8 for every normal owner;
- stops at sums 12, (11,1), (0,12), (6,6) and (255,255);
- owners 4/200 at sums up to 510, which complete without discovery.

Whole unit/structure/group/search/route/experience buffers and all physical, discovery, light and minimap grids match after every entry. So do the collision/discovery/light/minimap call trace and the per-cell trace.

The existing Stage 8 and Stage 12 matrices were rerun unchanged except for their stop fixtures, which now use `SOMA+1`:
- `PlaceEngin`/predicates: 2,014 entries / 3,938 segments, 2,002 returns and 12 stops.
- `SetSortEngin`: 846 entries / 1,038 segments, 666 returns, 156 caller checkpoints and 6 stops, plus 18 segmented entries / 192 resumes.
- The maximum ordinary segment is still 929,654 instructions.

Local mode discovers 32 tests and skips 17 optional native tests. The core suite passes 368 tests with 175 optional skips.

Consumer verification on this branch, read-only:
- [`conferir_monde01_descoberta.py --emular`](../../ferramentas/conferir_monde01_descoberta.py) runs missions' committed `preparar_unidades_no_terreno(provedores_terreno_core(...))` on actual MONDE01.
- It places units 0, 1, 2 and 11–15. Unit 15 is type 8 with sum 10, the last one placed.
- It reaches 0x46c16d and equals missions' original v2 capture (SHA-256 `449d2c4e…208e`) in every field.
- A fresh native rerun of their unpatched prefix (85 segments) equals both, with no buffer difference ([report](../../relatorios/descoberta-terreno-monde01-emulada.json)).
- The missions and economy local suites pass on this branch (56/21 and 393/180 optional skips).
- With `RISING_EMULAR=1`, missions `test_terreno_unidades` passes 6/6 natively. That covers MONDE01 through 0x46c16d, the vision-9 continuation and the forced vision-12 stop at 0x457019.
- Economy `test_producao_colocada` passes 13/13 natively, including its eight `erro='visao'` stops at 0x446146, now at sum 12.

## Remaining limits

- Normal-owner sums 12..510 stay `DependenciaColocacaoMissao`/`DependenciaColocacaoSaida` boundaries. No shipped data reaches them.
- Direct radii above 23/20 and owner bytes of 4 or more are outside the primitive domain; callers gate them.
- Radius domains of the other 46 call sites, including AvanceEngin's movement vision and the BatimentDecouvre/BatimentIllumine per-cell loops, were not inventoried here.
- Economy owns `BatimentHabitable` itself and its type-byte > 21 inherited-EDI case.
- No loaded mission, remap or runtime readiness follows from this stage.
