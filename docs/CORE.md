# Core reconstruction contract

Implementation lives in `ferramentas/`, tests in `testes/`, and original-byte evidence in `evidencias/`. Preserve existing Portuguese API identifiers and original French symbols; English prose explains their meaning. Addresses below apply only to the original executable hash in the repository README.

## Units, movement, and time

The runtime unit record stride is 276 bytes (`0x114`). The ETA disk record is 784 bytes: the loader copies its first 140 bytes, skips 512, then copies 132 into RAM offset `0x8C`. Thus 272 serialized bytes populate a 276-byte stride; disk fields alone are not a fully initialized live unit.

`unidades.py`, `regras.py`, and `movimento.py` reconstruct 26 type initializers, loading effects, health/healing, direction, turn permission, neighboring cells, and movement parameters. `combate.py` contains shared damage/reload primitives; the autonomous combat state machines stay in their own domain. Retain 8/16/32-bit wrapping and original signedness, including nonintuitive damage edges.

Important reference entries include healing `0x457122`, direction `0x477042`, neighbor `0x4770EE`, squared distance `0x479555`, orientation `0x448599`, movement prefix `0x448704`, reload `0x454530`, RNG `0x489728`, and the update/draw cycle near `0x475014`. The drawing divisor selected by F1–F4 does not establish a wall-clock simulation frequency. The older Swift proof's 1/60-second tick and 72 pixels/second are experimental, independent of the reverse-engineered cadence.

## Navigation and task effects

`MundoNavegacao` in `navegacao_unidades.py` joins supported occupancy, movement, routes, vision/minimap, messages, and tasks. `solucionador_python.py` provides destination preparation, candidate selection, both obstacle contours, route choice, and optimization for occupancy classes 1–3 and all 26 types. `solucionador_original.py` and `solucionador_misto.py` remain reference backends with explicit x86 dependencies.

The route pipeline spans `preparacao_destino.py`, `candidatos_rota.py`, `contornos_caminhos.py`, `otimizacao_caminhos.py`, and structure-region helpers. Keep requested destination, effective destination, final position, and cancellation reason distinct. A route-search success does not prove arrival; a movement order may end because passage became unavailable. Recheck occupancy as movement proceeds rather than treating a planned route as a permanent reservation.

Natural regions, alliances, unit blockers, structure labels, auxiliary colors, and compact footprint slots are distinct inputs. Structure labels use bit `0x8000`. Do not flatten all these checks into the disk attribute mask or a generic A* implementation. Some original edge reads are linear rather than constrained by playable width.

`tarefas_ia.py`, `ordens_unidades.py`, `avanco_unidades.py`, and `mensagens_chegada.py` reconstruct creation, waiting, subtasks, completion, reuse, orders/reset effects, physical movement, and state-change messages. The task pool has 100 records totaling 9,600 bytes. Tests compare whole task memory and lists. The upper AI dispatcher test substitutes some internal stages; it validates dispatch/arguments, not complete AI behavior. `RISING.RUL` decoding and SBL name recovery provide evidence, not an implementation of every rule opcode.

## Structure terrain and placement

`ciclo_estruturas.py` now implements selective structure-pool initialization and reset, with a first-free query from `CreerBatiment`. The original pool is 1,000 records of 276 bytes. `inicializar_registros_estruturas` stops at `0x419004`, before `BatimentAlloc`'s economic and characteristic-loading effects. `resetar_todas_estruturas` and `resetar_estrutura` translate complete original routines. Their retained fields differ: none clears a whole record, and single reset preserves gate counter `+0x76`. `buscar_estrutura_livre` checks state `+5 == 0` only, returns the first index or `0xffff`, and does not reserve it. `MundoUnidades` exposes explicit adapters; its synthetic constructor remains zero-filled. See the [exact lifecycle contract](core/STRUCTURE_LIFECYCLE.md) for byte widths, ordered stores, stops, failures, and 648 newly executed original-x86 comparisons.

`posicao_saida.py` adds complete `CalculPosition` (`0x420698`): `calcular_posicao_saida(mundo, indice, direcao=0, dimensoes=None)` returns the original caller-consumed u16 cell for all 22 structure types. The direction byte is unused; types 9/12/17 return literal zero. Current u16 width/height may be supplied explicitly; no passage test or world mutation occurs. See the [exit-position contract](core/EXIT_POSITION.md) for original tables, 22 independent original captures, and 7,546 fresh x86 comparisons.

`conversao_unidades.py` connects the committed combat local conversion to live core unit records and navigation-search release. `converter_unidade` uses the existing provider through a writable memoryview; read-only economic capacity/bonus queries remain explicit. `retomar_conversao_saida` composes the original position call, live building `+7b` reload, and conversion, stopping before healing at `0x420f6e`. The [shared conversion contract](core/CONVERSION.md) records 1,986 fresh native executions, deliberate query stops, the consumed combat callback-order correction, and a synthetic demonstration with committed economic providers. No allocator, physical reservation, or complete production effect is implied.

`capacidades_unidades.py` adds complete `EnginResetCapacite` (`0x4475ef`): `atualizar_capacidades_unidades(mundo, jogador, *, capacidade_tipo=None, modificador=None)` scans all 800 slots in original order and changes only the Bag capacity word of active units owned by the input byte. Contents/count are retained; failures preserve earlier stores. It uses economy's committed read-only queries and can serve that owner's bonus-setter callback. The [capacity-refresh contract](core/CAPACITY_REFRESH.md) records 284 new native executions, complete scans and explicit partial-query stops.

`terreno_estruturas.py` implements `BatimentModifyTerrain`, `ResetBatimentTerrainModify`, and `ResetCheminTerrainModify`: rectangles, collision masks, compact slots, tiles, objects, regions, and colors. Type 20 requires its **20-byte runtime mask** as an explicit input; the static geometry must not silently replace it. Natural remapping still refuses already inserted structures.

`colocacao_estruturas.py` adds:

| Original routine | Address | Python entry |
|---|---|---|
| `ValideHerse` | `0x41AC8B` | `validar_portao` |
| `ChercheMurCombinaisons` | `0x41C18A` | `combinacao_muro` |
| `SetMurAllentour` | `0x41C251` | `atualizar_muros_vizinhos` |
| `PlaceBatiment` | `0x41C4AC` | `colocar_estrutura` |

`mundo.colocar_estrutura(indice, mascara_tipo20=None)` consumes an existing caller-prepared structure record. Its origin is u16 at `+0x02`, type at `+0x08`; the index is truncated to u16 then checked against 1,000 records, and supported types are 0–21. It neither allocates a free record nor changes owner/state. Regular buildings select their first tile and apply the terrain operation. Type 20 still requires its runtime mask.

Walls are type 9, default object 254; gates are type 12, default object 253. Wall neighbor bits are west=8, south=4, east=2, north=1; a nonzero combination returns combination−1, otherwise zero. Placement writes `+0x7C`, the object, attribute bit 0, and a structure label with slot zero. It preserves the tile. Region mode 3 and attribute mask 1 are different arguments.

Gate placement requires wall/gate neighbors on both horizontal sides (orientation 0) or both vertical sides (orientation 1); horizontal wins ties. Failure returns 255 without placement effects. Accepted gates also zero u16 `+0x86`. Updating nearby walls is a separate caller operation and must not be invented as an unconditional placement side effect.

Neighbor reads use the linear 65,536-cell object grid. Column 255 can read the next row; bytes outside the modeled allocation produce `NotImplementedError`, not artificial wraparound. Do not add activity, ownership, or type filters absent from the original bodies.

## Physical gate simulation

`portoes.py` reconstructs `HerseEnAnimation` (`0x4191FD`), phase/orientation queries (`0x41934F`, `0x419379`, `0x4193AC`), release/block commands (`0x4193D4`, `0x4195CA`), toggle (`0x419917`), and the type-12 `BatimentNextEtape` branch (`0x427BB7..0x427D5D`).

The byte at `+0x76` is a simulation counter. Stable values are 0, 15, 31; other values transition. Orientation tests the entire u16 `+0x7C`: zero is horizontal, any other value vertical. Advancing a transitioning gate increments u8; results ≥31 become zero, including overflow from 255. Reaching 15 clears attribute bit 0 and removes the gate's region label; returning to zero sets it and restores the label. Stable states do not independently repair mismatched terrain.

`mundo.alternar_portoes(celula, indice)` ignores a reference gate already transitioning. At 15 it requests blocking; at 0/31 it requests release. Group blocking uses a 255-word position list, tests every recorded position for occupancy/reservation before mutating counters, and preserves original scan asymmetries and duplicate-slot effects. Unmodeled list overflow is rejected. These effects must remain distinct from sprite/frame selection.

The gate demonstration reaches `(10,4)` after 169 updates: request at update 0, passage freed at 14, closure refused while reserved at 87, accepted at 121, and collision restored at 136. This synthetic traversal verifies supported movement/task effects, not complete real-mission dispatch or mouse input.

## Reproduction and remaining scope

```sh
python3 -B ferramentas/demonstrar_desvios.py --python
python3 -B ferramentas/demonstrar_terreno_estruturas.py
python3 -B ferramentas/demonstrar_colocacao_estruturas.py
python3 -B ferramentas/demonstrar_portoes.py
sh testar.sh
```

Demos may regenerate their own versioned report. Use an isolated core worktree. Differential validation is described in [validation](VALIDATION.md). Full structure allocation/creation and the remaining startup effects, construction costs/progress, complete demolition, building vision/minimap, full global dispatch, real-mission loading/remapping, and cursor/mouse gate selection remain open integration work. Production's caller effects after local conversion and world occupancy also remain open. The [dependency inventory](core/REMAINING.md) distinguishes implemented, validated, integrated, and runtime-tested scope. Coordinate economic and graphical callbacks through written contracts rather than editing another domain.
