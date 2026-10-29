# Construction routines for Economy's build path (M3 groundwork)

Status: captured natively, translated and validated natively on `feat/re-core`, not yet integrated. These are the Core routines that Economy's construction path (`ordens_economia`: CreerBatiment and the CalculConstruireBatiment tick) calls but had no translation over live memory ([ECONOMY](../ECONOMY.md), "Named dependencies"). None of them runs in the no-input coverage run, so this is the first execution evidence for them in the M2 state. Addresses apply only to the intact `RISING.EXE` (SHA-256 `6c556520…8543fb`).

**Concrete target.** The CAVE (type 3, 5×5) clicked at (21,12) is built at reference cell (23,14) (offset 0x202). Its record origin is (19,10). PlaceBatiment there writes tiles 0x306.. over the 5×5 rectangle, collision bit 0 and region tags 0x8020..0x8026 on the 7 mask cells, and one new structure colour (0xfd). Replayed through Economy's own translation with these providers, Economy's native case `build_tick_arrived_cave` leaves food/stone 20/24 and the record (+5 = 2, type 3, origin (19,10)); see "Economy composition" below.

## Method (original first)

1. **Bench.** It reuses `bancada_selecao_ordens` unchanged ([SELECTION_ORDERS](SELECTION_ORDERS.md)): Missions' accepted MONDE01 display path, paused at frame 1's first `ProcessInputGame` entry. Each case runs one routine natively as a leaf call from the exact restored state plus its declared writes and argument registers.
2. **Cases** (`ferramentas/casos_construcao_core.py`): 153. The capture checks the pause facts the cases rely on (`verificar_pausa`: map size, wall/gate objects, free colours, cave size, the type-20 mask pointer, the builder, the sanctuary record, the free cave site). They cover:
   - PlaceBatiment: the CAVE target, all 22 structure types at (19,10), the type-20 runtime mask (zero and declared), record 999, overlaps with the sanctuary and the builder's region tag, the map edge (61,61), a row wrap (19,254), column 254, colours exhausted and one colour left, a CAVE next to the sanctuary's colour, upper register bits; walls (isolated, four neighbours, W+S, on a gate object, on a unit tag, next to a colour) and gates (no neighbours, horizontal, vertical, both, column 0, west only, on a unit tag);
   - ResetCheminTerrainModify: the sanctuary, a tag mismatch, a declared placed CAVE (full and partial tags, full free list), placed walls with and without a colour, the type-20 alias;
   - BatimentCollision: types 3, 9, 20 (alias of 15) and 22;
   - BatimentConstructible: the CAVE target, the builder inside the footprint (cell, last cell, reserved +0x7c), another unit inside, the builder with +0xab and mask 1, state 14, quad-type units, an out-of-table unit type, the sanctuary, attribute bit 1 only, types 1/2/4/9, the top-edge wrap, upper bits, and type 12 on an own wall, a foreign wall, a wall without a tag, a free cell and a unit tag;
   - BatimentPosable: the CAVE target, types 1/2/4/9/12, the discovered east edge (24,12) and the undiscovered corner (25,12), the sanctuary, the builder or another unit inside, one hidden cell, non-grass and grass-bound tiles, a player-1 unit, the four bound checks (left/top edges, columns 254/255, rows 254/255), gates on walls;
   - EnginOccupeCase, TerrainEstHerbe, ValideHerse, ChercheMurCombinaisons: their branch tables directly;
   - DeplaceEngin of the builder carrying the CAVE order: path states 0 (turning, facing so AvanceEngin and CalculFatigue run, a completing step with the cell transfer and discovery, the fatigue threshold with provisions, a hidden unit, blocked by unit 13, already at the target), 1, 2, 3 (search busy, pushed, the path search), 4 (blocked, status 8), 6 (counting and the wait over), 7, and unit 13.
3. **Capture** (`ferramentas/capturar_construcao_core.py` → `evidencias/construcao-core/captura-construcao-core-exibicao.json`). It was committed before any translation (`0a0ff90`, 149 cases). Four DeplaceEngin advance cases were added after the first translation pass and captured natively before their comparison (`8869dbe`); the 149 earlier cases are byte-identical. All 153 return. The run reproduces load_tail, between_frames and frame1, and the code section is unchanged. `extrair_construcao_core.py` exports the 27 bodies, epilogues and five jump tables (`evidencias/construcao-core/*.asm`, `manifesto.json`).
4. **Translation** (`ferramentas/construcao_core.py`, class `ConstrucaoCore`) over live flat memory.
5. **Native differential** (`ferramentas/validar_construcao_core.py` → `relatorios/construcao-core-emulada.json`): **153 comparisons, 0 mismatches.** Compared per case: EAX..EBP and every changed byte of the whole mapped state (7,789 in total). The native run also equals the committed capture in every case. The same run records the bytes each case read before writing (`leituras-construcao-core-exibicao.json`); with them all 135 cases outside DeplaceEngin replay without a CPU in `testes/test_construcao_core.py`, and four deliberate mutations are each detected.

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/capturar_construcao_core.py --saida .local/construcao/x.json   # ~115 s
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_construcao_core.py                                    # ~140 s
RISING_EMULAR=1 PYTHONPATH=ferramentas:testes python3 -B -m unittest testes.test_emulacao_construcao_core
```

| Routine | Cases | Mismatches |
|---|---|---|
| PlaceBatiment | 45 | 0 |
| BatimentConstructible | 25 | 0 |
| BatimentPosable | 25 | 0 |
| DeplaceEngin | 18 | 0 (2 with declared uncertain EAX bits) |
| EnginOccupeCase | 12 | 0 |
| ResetCheminTerrainModify | 9 | 0 |
| BatimentCollision | 7 | 0 |
| TerrainEstHerbe | 6 | 0 |
| ValideHerse, ChercheMurCombinaisons | 3 + 3 | 0 |

## API

`ConstrucaoCore(memoria, *, bonus=None)`.
- **`memoria`**: `u8/u16/u32(addr, value=None)`; DeplaceEngin also needs `vista(addr, n)` (`memoria_quadro_core.MemoriaQuadro`), because M2.3's live navigation world (`mundo_vivo` with `SolucionadorCaminhosVivo`) makes its stores. Every other routine works over any such memory, sparse ones included, and reads only bytes the original reads.
- **`chamar(nome, regs, pilha=())`**: runs `nome` with entry registers EAX..EBP (missing keys are an error). It returns all seven registers as the original leaves them. Each routine is also a method (`place_batiment`, `batiment_constructible`, …). Arithmetic flags are not modeled.
- **Uncertain bits.** DeplaceEngin's EAX is sometimes the EAX a deep callee leaves, including native stack residue. Those bits are never guessed: the result then holds `_incertos = {'EAX': mask}` and the masked bits are 0. That happens at the target after EnginNextCase/EnginNextCaseChemin (mask 0xffff0000; AX = +0x7c is exact), after CheminCalcul (state 3 search, state 4 not concluded) and after EnginDebloqueNextCase (state 4 failure other than status 8) (mask 0xffffffff). Every other bit of every routine is exact.

| Routine | Entry | Arguments | Effects | Registers changed (others preserved) |
|---|---|---|---|---|
| PlaceBatiment | 0x41c4ac | AX structure index | Reads type +8 and origin +2 of a prepared record. Types other than 9/12: BatimentModifyTerrain from the first tile of table 0x41c454. Wall (9): +0x7c = ChercheMurCombinaisons, object = 0xfe (0x495bf8), collision bit 0, region tag slot 0. Gate (12): ValideHerse; 0xff returns with no store; else +0x7c = orientation, object = 0xfd, +0x86 = 0, collision bit 0, tag slot 0 | EAX: the last Chemin_ModifieZone's or the last cell (see below); gate refused: 0xff |
| BatimentModifyTerrain | 0x41ba49 | internal | Row by row, column by column over w×h from the origin (32-bit cell counter, u16 cell): tile = first tile + n; if the mask byte (pointer `[0x495d94 + 52·type]`, RAM 0x4dfb9c for type 20) is set, collision bit 0 and Chemin_ModifieZone mode 3 with the next slot (refused insertions also consume a slot); then object = 0 | — |
| Chemin_ModifieZone mode 3 / 1 | 0x43e138 | internal | Tag = 0x8000 + (index << 5) + slot (8-bit high-byte add). Mode 3: region < 0x4000 → saved to the record's +0xcc + 2·slot, tag stored, MurAjoute. Mode 1: region == tag → restored from the slot, MurRetire | EAX = (MurAjoute/MurRetire EAX with AL = 1) or (region address with AL = 0) |
| MurAjoute / MurRetire | 0x43e616 / 0x43e8b7 | internal | Core's `CoresEstruturas` (component colours, Remplit, the free list) at the original addresses | EAX = the free count before the fourth LibereCouleur; MurAjoute adds AH = count + 1 when that release happens; MurRetire on an uncoloured cell: 0 |
| ResetCheminTerrainModify | 0x41b78f | AX structure index | For each cell of the w×h rectangle whose **static** BatimentCollision mask is set, Chemin_ModifieZone mode 1 with the next slot (consumed only by mask cells) | EAX = height |
| BatimentCollision | 0x41ab5c | AL type, DX mask index | Core's committed `colisao_estrutura` (type 20 uses type 15's mask; above 0x15 AL = 0) | EAX, EDX |
| BatimentConstructible | 0x41fb12 | AL type, DX reference (bottom-right) cell, BX unit | Rectangle origin = EDX − (w−1) − ((h−1) << 8) (full 32 bits, u16 cells). AL = 1 unless a cell has collision bit 0 and EnginOccupeCase(BX, cell, 1) is 0. Type 12: AL = 1 only on a wall object whose region holds a structure tag owned by the unit's owner | EAX, EBX, EDX (from the last callee; see the source) |
| BatimentPosable | 0x41fc40 | AL type, DX centre cell, BX unit | Flag 0x4e05b8 = 1 and memset(0x4e05b9, 1, w·h); a footprint outside x ≥ w/2, y ≥ h/2, x + w − w/2 − 1 ≤ 256, y + h − h/2 − 1 ≤ 256 zeroes both and returns. Otherwise a cell is invalid unless grass (tiles 0x15d..0x1a4), discovered by the unit's owner and free or held by the unit (EnginOccupeCase, mask 1); type 12 needs a wall object where ValideHerse fits. Invalid cells zero their matrix byte and the flag | EAX (AL = flag), EBX, EDX |
| EnginOccupeCase | 0x44246e | AX unit, DX cell, BL mask | AL = 0 for +0xab ≠ 0 with mask 1, +0xab = 0 with mask 2, or state 14. Types 3, 11–16, 25 test +8, its −1/−0x101/−0x100 neighbours, +0x7c and its neighbours; other types +8 and +0x7c; types above 25 give 1 | EAX, EBX, EDX |
| TerrainEstHerbe | 0x47636a | AX cell | AL = tile in 0x15d..0x1a4 | EAX |
| ValideHerse | 0x41ac8b | AX cell | 0 = walls/gates west and east (x > 0), 1 = north and south (y > 0), 0xff otherwise | EAX |
| ChercheMurCombinaisons | 0x41c18a | AX cell | Bits W = 8, S = 4, E = 2, N = 1 for wall/gate neighbours, minus one; 0 on a gate cell | EAX (AH = the gate object byte, upper half kept) |
| DeplaceEngin | 0x44930c | AX unit | M2.3's world `deslocar` and CalculNextCase's steps (`escolher_direto`/`escolher_da_rota`, `animar_movimento`, `girar`, `avancar_passo`) | EAX (exact or `_incertos`): unit for states 1, 2, > 6 and a busy search; the wait counter or 0x14 for state 6; CalculNextCase: 0 when turning, AvanceEngin's EAX after a step (0 dead, type for 11..24, CalculFatigue's for 0..10/25: `(unit·276) & ~0xff` when hidden, the bonus below the threshold, the provisions before at it) |

`PlaceBatiment` reaches neither `BatimentModifyMap`, `BatimentAlloc` nor any discovery or light: the capture of every case records its nested calls, and none of these appears. Those effects belong to the construction progress (`BatimentConstruction`, Economy's +0x89 = 1 branch), which needs a scripted-input capture.

**Faithful corrections to Core's world model.** Remplit with the same colour (`CoresEstruturas.preencher`) used to be refused. The native capture shows the original terminating: a component of three or more cells fills the 1,023-entry stack and returns, an isolated cell empties it. Only a two-cell component cycles forever; that alone is now refused, before any store.

## Economy adapter

`provedor_construcao(core, outros=None)` is the `externo(nome, chamada, registradores) -> registradores` Economy's `OrdensEconomia` takes, for `ROTINAS_ECONOMIA` = PlaceBatiment, BatimentConstructible, BatimentCollision, ResetCheminTerrainModify and DeplaceEngin.
- Input: EAX..EBP (ESP is accepted and unused), optionally `_incertos`.
- Output: EAX..EBP as the callee leaves them, after its stores. `_incertos` in the output marks bits not reconstructed (DeplaceEngin only); input masks are carried for the registers the callee leaves unchanged (Economy's ECX upper half at PlaceBatiment).
- Any other name goes to `outros`, or raises `DependenciaRamoCore` at its call address.

Wiring, together with Core's selection-orders provider:

```python
from ordens_economia import OrdensEconomia, provedor_core
from selecao_ordens import SelecaoOrdens
from construcao_core import ConstrucaoCore, provedor_construcao
externo = provedor_core(SelecaoOrdens(m, som=som),
                        provedor_construcao(ConstrucaoCore(m, bonus=bonus)))
OrdensEconomia(m, externo=externo)
```

**Economy composition (CPU-free).** `testes/test_construcao_core.py` replays Economy's committed native capture through Economy's `OrdensEconomia` with this wiring, instead of the original callees: every CreerBatiment and CalculConstruireBatiment case in Economy's domain that avoids ResetOrdre and DeplaceEngin. It compares exit registers and the final value of every stored byte with Economy's native run. PlaceBatiment, BatimentConstructible, BatimentCollision and ResetCheminTerrainModify are all reached. DeplaceEngin inside Economy's tick is compared only by Core's native differential, because M2.3's world needs the whole mapped state.

## Named dependencies

- **Economy — `bonus(jogador, tipo, seletor) -> EAX`** for BonusGetValEngin 0x428cc0, which CalculFatigue calls after a DeplaceEngin step of a unit of type 0..10 or 25. Only its value is needed: the world's stores read the same live table 0x4dfba0. Without it the step raises `DependenciaRamoCore` at 0x452d48 after the step's stores. The validator wires Economy's committed `bonus_unidades.BonusUnidades`.
- **Audio** — CalculNextCase's local-player sound for unit types 11..16 still raises in M2.3's world (`_som_movimento`, 0x4490c3). The builder (type 7) never reaches it.
- **Not translated here.** Chemin_ModifieZone modes 0 and 2 through this module (mode 2 is `chamadas_quadro_core`'s); AnimBallonStatic (type 17); the hunger branch of CalculFatigue and hostile traps (they raise in M2.3's world).
- Protected inputs raise `ValueError` before any store: a structure index ≥ 1,000, a structure type > 21.

## What needs real input (scripted-input captures)

- The real walk: DeplaceEngin over consecutive frames up to (21,12), and BatimentConstructible when the builder actually stands on the footprint (the leaf cases declare those positions).
- The construction progress (+0x89 = 1: BatimentConstruit, AnimConstruireBatiment, BatimentConstruction → BatimentModifyMap and discovery for the new structure) and the state-15 approach. The leaf bench cannot reach them without faking a structure under construction.
- The CAVE cursor: which pixel and view ProcessInputGame hands to BatimentPosable, and the HUD's use of the 0x4e05b9 matrix.
- Walls and gates the AI or the player actually builds (MONDE01 has none), and SetMurAllentour after a wall.
